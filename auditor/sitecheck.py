"""Relecture à la source des barèmes d'honoraires des agences tirées (éditeur, voisines, tirage aléatoire).

Téléchargement direct (sans Firecrawl, sans exécuter de JavaScript ni aucun script). Le texte extrait sert UNIQUEMENT de
donnée aux deux IA, qui le comparent aux points publiés. Il n'est pas republié (droits des agences) : seuls l'URL,
l'heure, le statut HTTP, la taille et l'empreinte SHA-256 du contenu téléchargé sont archivés."""
from __future__ import annotations

import datetime as dt
import hashlib
import html
import re
import urllib.request

UA = 'Mozilla/5.0 (compatible; nice-agencies-open-audit; +https://github.com/thomasgestioncassini/nice-agencies-open-audit)'
MAX_BYTES = 3_000_000
MAX_TEXT = 6000


def page_text(raw: bytes) -> str:
    t = raw.decode('utf-8', 'replace')
    t = re.sub(r'(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>', ' ', t)
    t = re.sub(r'(?s)<!--.*?-->', ' ', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    return ' '.join(t.split())


def fetch(url: str) -> dict:
    meta = {'url': url, 'utc': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}
    if not url.startswith(('http://', 'https://')):
        return {**meta, 'status': 'url_invalide'}
    if url.lower().split('?')[0].endswith('.pdf'):
        return {**meta, 'status': 'pdf_non_lu'}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30) as r:
            raw = r.read(MAX_BYTES + 1)
            meta['http'] = r.status
    except Exception as e:                    # noqa: BLE001
        return {**meta, 'status': 'echec', 'error': type(e).__name__}
    meta.update(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
    txt = page_text(raw)
    if len(txt) < 200:
        return {**meta, 'status': 'contenu_insuffisant (page dynamique ?)'}
    return {**meta, 'status': 'lu', 'text': txt[:MAX_TEXT], 'text_truncated': len(txt) > MAX_TEXT}


def check_sites(sources: dict, criteria: dict, agencies: list[str], fetcher=fetch) -> dict:
    rows = []
    for s in agencies:
        r = sources.get(s) or {}
        url = r.get('url_bareme') or r.get('url_site') or ''
        res = fetcher(url) if url else {'url': '', 'status': 'aucune_url_publiee'}
        rows.append({'agence': s, 'page': 'bareme' if r.get('url_bareme') else 'site',
                     'points_publies': [{k: c[k] for k in ('critere', 'points', 'max', 'date_observation')} for c in
                                        criteria.get(s, []) if c['pilier'] == 'hono'], **res})
    from collections import Counter
    return {'rows': rows, 'counts': dict(Counter(x['status'] for x in rows))}


def public_view(sites: dict) -> dict:
    """Version publiable : sans le texte des pages."""
    return {'counts': sites['counts'], 'rows': [{k: v for k, v in r.items() if k != 'text'} for r in sites['rows']]}

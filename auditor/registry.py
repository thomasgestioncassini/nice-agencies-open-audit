"""Contrôle à la source de l'ancienneté : la date de création de chaque société échantillonnée est comparée à celle du
registre national (API publique « Recherche d'entreprises », recherche-entreprises.api.gouv.fr, gratuite, sans clé).
Réseau requis. Aucune IA. Les réponses brutes sont archivées avec leur empreinte."""
from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
import urllib.request

API = 'https://recherche-entreprises.api.gouv.fr/search'
UA = 'nice-agencies-open-audit (+https://github.com/thomasgestioncassini/nice-agencies-open-audit)'


def lookup(siren: str, get=None) -> dict:
    url = f'{API}?{urllib.parse.urlencode({"q": siren, "per_page": 1})}'
    if get:
        raw = get(url)
    else:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30) as r:
            raw = r.read().decode('utf-8')
    data = json.loads(raw)
    hit = next((x for x in data.get('results', []) if x.get('siren') == siren), None)
    return {'url': url, 'sha256': hashlib.sha256(raw.encode()).hexdigest(),
            'found': hit is not None,
            'date_creation': (hit or {}).get('date_creation'),
            'etat_administratif': (hit or {}).get('etat_administratif'),
            'nom': (hit or {}).get('nom_complet'),
            'date_fermeture': (hit or {}).get('date_fermeture')}


def check_registry(sources: dict, agencies: list[str], get=None, pause: float = 0.2) -> dict:
    out, rows = {}, []
    for s in agencies:
        r = sources.get(s) or {}
        siren = (r.get('siren') or '').replace(' ', '')
        if not siren:
            rows.append({'agence': s, 'statut': 'siren_non_publie'})
            continue
        try:
            reg = out.get(siren) or lookup(siren, get)
            out[siren] = reg
        except Exception as e:                # noqa: BLE001 — publié comme non vérifié
            rows.append({'agence': s, 'siren': siren, 'statut': 'registre_injoignable', 'erreur': f'{type(e).__name__}'})
            continue
        pub = (r.get('date_creation_societe') or '')[:10]
        if not reg['found']:
            st = 'siren_introuvable'
        elif reg['etat_administratif'] == 'C':
            st = 'societe_cessee'
        elif pub and reg['date_creation'] and pub != reg['date_creation'][:10]:
            st = 'date_differente'
        elif not pub:
            st = 'date_non_publiee'
        else:
            st = 'conforme'
        rows.append({'agence': s, 'siren': siren, 'statut': st, 'date_publiee': pub,
                     'date_registre': reg['date_creation'], 'source_anciennete': r.get('source_anciennete'),
                     'enseigne_depuis': r.get('enseigne_depuis') or None, 'preuve': reg['url'], 'sha256': reg['sha256']})
        time.sleep(pause)
    from collections import Counter
    return {'rows': rows, 'counts': dict(Counter(x['statut'] for x in rows)),
            'limite': 'le registre donne la date de création de la société, pas celle de l’enseigne ; une enseigne '
                      'récente exploitée par une société ancienne ne peut pas être détectée ainsi'}

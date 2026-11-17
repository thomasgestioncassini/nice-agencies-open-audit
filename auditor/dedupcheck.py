"""V-14 : contrôle indépendant du dédoublonnage des avis (priorité 4 de la revue ChatGPT de la phase C).

Les fichiers de reproduction donnent, pour chaque avis, le résultat du dédoublonnage du site (retenu_qualite,
retenu_service, nb_agences_partageant) mais pas le texte : le dédoublonnage ne peut pas y être refait. Le site publie aussi
un paquet de données anonymisées (meilleure-agence-nice-calcul.zip) où le texte et l'auteur de chaque avis sont remplacés
par des empreintes salées, qui permettent exactement les mêmes comparaisons. Ce module :

- lit ce paquet comme une DONNÉE (aucun script du paquet n'est exécuté) ;
- refait le dédoublonnage avec sa propre implémentation de la règle (interprétation I-13) ;
- compare, agence par agence, le nombre d'avis uniques retenus et la répartition des avis partagés aux fichiers de
  reproduction.

Les identifiants d'avis sont salés dans le paquet : la comparaison se fait agence par agence et plateforme par plateforme,
en nombres, pas avis par avis.
"""
from __future__ import annotations

import datetime as dt
import json
import zipfile
from collections import Counter
from pathlib import Path

from .recalculate import read_csv

# I-13 : ordre de conservation de la copie en cas de doublon, seuils de ressemblance, clé des avis partagés
PREF = ('opinionsystem', 'immodvisor', 'google')
JACCARD, OVERLAP, MIN_TOKENS = 0.7, 0.9, 5
NOTE_GAP, DAYS = 0.5, 45


def _days(a, b):
    try:
        return abs((dt.date.fromisoformat(a[:10]) - dt.date.fromisoformat(b[:10])).days)
    except (TypeError, ValueError):
        return 10 ** 6


def same(x: dict, y: dict) -> bool:
    tx, ty = x['tok'], y['tok']
    if len(tx) >= MIN_TOKENS and len(ty) >= MIN_TOKENS:
        inter = len(tx & ty)
        return inter / len(tx | ty) >= JACCARD or inter / min(len(tx), len(ty)) >= OVERLAP
    if x['r'] is None or y['r'] is None or abs(float(x['r']) - float(y['r'])) > NOTE_GAP:
        return False
    (f1, i1), (f2, i2) = x['aut'], y['aut']
    if not f1 or f1 != f2 or (i1 and i2 and i1 != i2):
        return False
    return _days(x['date'], y['date']) <= DAYS


def unique(platforms: dict) -> list[dict]:
    kept = []
    for src in sorted(platforms, key=lambda s: PREF.index(s) if s in PREF else 99):
        for it in platforms[src]:
            if it['r'] is None:
                continue
            if any(k['src'] != src and same(it, k) for k in kept):
                continue
            kept.append(it)
    return kept


def _items(v: dict, src: str) -> list[dict]:
    return [{'src': src, 'r': x.get('r'), 'date': x.get('date') or '', 'kind': x.get('kind'),
             'tok': set(x.get('tok') or ()), 'aut': tuple(x.get('aut') or (None, None)), 'key': x.get('key')}
            for x in v.get('items', [])]


def check(data_dir: Path, excluded_profiles=None) -> dict:
    data_dir = Path(data_dir)
    zp = data_dir / 'calcul.zip'
    if not zp.exists():
        return {'status': 'non_verifie', 'reason': 'paquet anonymisé absent de ce relevé (archivé depuis le 17/11/2026)'}
    params = json.loads((data_dir / 'parametres.json').read_text(encoding='utf-8'))
    hors = set(excluded_profiles or params.get('profils_ecartes') or ())
    with zipfile.ZipFile(zp) as z:
        db = json.loads(z.read('data/agencies.json'))
        ags = db if isinstance(db, list) else db['agencies']
        stores = {}
        for a in ags:
            name = f"data/reviews/{a['id']}.json"
            if name in z.namelist():
                stores[a['id']] = json.loads(z.read(name))
    by_slug = {a['slug']: a for a in ags}
    # avis partagés : clé de texte présente sur les fiches de plusieurs agences actives
    seen: dict[str, set] = {}
    for a in ags:
        if a.get('hidden') or a.get('excluded') or a.get('opposition'):
            continue
        for v in (stores.get(a['id']) or {}).values():
            if isinstance(v, dict):
                for x in v.get('items', []):
                    if x.get('key'):
                        seen.setdefault(x['key'], set()).add(a['id'])
    shared = {k: len(v) for k, v in seen.items() if len(v) > 1}

    pub = Counter()
    pub_s = Counter()
    pub_k: dict[str, Counter] = {}
    for x in read_csv(data_dir / 'avis-elementaires.csv'):
        pub[x['agence']] += x['retenu_qualite'] == '1'
        pub_s[x['agence']] += x['retenu_service'] == '1'
        pub_k.setdefault(x['agence'], Counter())[int(x['nb_agences_partageant'] or 1)] += 1
    ranked = [r['agence'] for r in read_csv(data_dir / 'agences.csv')]
    rows, missing = [], []
    for slug in ranked:
        a = by_slug.get(slug)
        if a is None or a['id'] not in stores:
            if pub_k.get(slug):
                missing.append(slug)
            continue
        full = stores[a['id']]
        tx = {s: [i for i in _items(v, s) if i['kind'] not in hors] for s, v in full.items() if isinstance(v, dict)}
        detailed = {s: tx[s] for s, v in full.items() if isinstance(v, dict) and v.get('complete') and tx[s]
                    and v.get('items')}
        q = len(unique(detailed))
        sv = len(unique({s: i for s, i in tx.items() if i}))
        k = Counter()
        for v in full.values():
            if isinstance(v, dict):
                for x in v.get('items', []):
                    k[shared.get(x.get('key'), 1)] += 1
        rows.append({'agence': slug, 'qualite_recalcule': q, 'qualite_publie': pub[slug],
                     'service_recalcule': sv, 'service_publie': pub_s[slug],
                     'partage_recalcule': dict(sorted(k.items())), 'partage_publie': dict(sorted((pub_k.get(slug) or {}).items()))})
    dq = [r for r in rows if r['qualite_recalcule'] != r['qualite_publie']]
    ds = [r for r in rows if r['service_recalcule'] != r['service_publie']]
    dk = [r for r in rows if r['partage_recalcule'] != r['partage_publie']]
    ok = not (dq or ds or dk or missing)
    return {'status': 'conforme' if ok else 'ecarts', 'agences': len(rows), 'sans_donnees_anonymisees': missing,
            'ecarts_qualite': dq, 'ecarts_service': ds, 'ecarts_partage': dk,
            'avis_partages_cles': len(shared), 'interpretation': 'I-13'}

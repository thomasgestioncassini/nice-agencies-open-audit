"""Choix des agences contrôlées à la source : règle publique, reproductible, fixée avant de connaître les résultats.

Règle (config/audit-policy.json, section « sampling ») :
1. Toujours : les agences de l'éditeur (Gestion Cassini, ImmoVendu).
2. Groupe de comparaison fixe : pour chaque agence de l'éditeur, les K agences classées juste au-dessus et juste
   en dessous (rang publié du relevé archivé).
3. Situations comparables pour l'ancienneté : toutes les agences dont la société exploite plusieurs fiches (même SIREN),
   dont l'enseigne a une date de lancement relevée, ou dont l'ancienneté a été saisie à la main.
4. Échantillon aléatoire : N agences tirées parmi les autres. La graine combine l'empreinte SHA-256 des fichiers
   archivés et la valeur aléatoire publique drand (League of Entropy) du premier tour produit APRÈS l'archivage.
   Ni l'éditeur ni l'auditeur ne peuvent la connaître avant que les données soient figées, ni la choisir ensuite.
"""
from __future__ import annotations

import hashlib
import json
import random
import time
import urllib.request

DRAND = 'https://api.drand.sh/52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971'   # chaîne « quicknet »


def drand_after(ts: float, timeout: int = 30) -> dict:
    """Tour drand qui suit l'instant ts (secondes UTC). Attend sa publication si besoin (période de 3 s)."""
    info = json.load(urllib.request.urlopen(f'{DRAND}/info', timeout=timeout))
    rnd = int((ts - info['genesis_time']) // info['period']) + 2
    for _ in range(20):
        try:
            b = json.load(urllib.request.urlopen(f'{DRAND}/public/{rnd}', timeout=timeout))
            return {'chain': info['hash'], 'round': b['round'], 'randomness': b['randomness'], 'signature': b['signature'],
                    'url': f'{DRAND}/public/{rnd}'}
        except Exception:                     # noqa: BLE001 — tour pas encore publié : on attend
            time.sleep(info['period'])
    raise RuntimeError('balise drand indisponible')


def seed_of(inputs_sha256: dict, beacon: dict | None) -> str:
    h = hashlib.sha256()
    for name in sorted(inputs_sha256):
        h.update(f'{name}:{inputs_sha256[name]}\n'.encode())
    h.update(f'drand:{beacon["randomness"] if beacon else "INDISPONIBLE"}'.encode())
    return h.hexdigest()


def select(agencies: list[dict], sources: dict, policy: dict, seed: str) -> dict:
    sp = policy['sampling']
    by_rank = sorted(agencies, key=lambda a: int(a['rang_publie']))
    pos = {a['agence']: i for i, a in enumerate(by_rank)}
    publisher = [s for s in sp['publisher_agencies'] if s in pos]
    picked: dict[str, str] = {s: 'editeur' for s in publisher}
    k = sp['neighbours_each_side']
    for s in publisher:
        i = pos[s]
        for a in by_rank[max(0, i - k): i] + by_rank[i + 1: i + 1 + k]:
            picked.setdefault(a['agence'], f'voisine_de_{s}')
    sirens: dict[str, list] = {}
    for s, r in sources.items():
        if r.get('siren'):
            sirens.setdefault(r['siren'], []).append(s)
    for s, r in sources.items():
        if s in pos and (len(sirens.get(r.get('siren'), [])) > 1 or r.get('enseigne_depuis')
                         or r.get('source_anciennete') == 'rachat_prouve_saisie_manuelle'):
            picked.setdefault(s, 'anciennete_comparable')
    rest = sorted(a['agence'] for a in agencies if a['agence'] not in picked)
    rng = random.Random(int(seed, 16))
    for s in rng.sample(rest, min(sp['random_sample_size'], len(rest))):
        picked[s] = 'tirage_aleatoire'
    return {'seed': seed, 'rule_version': sp['rule_version'], 'agencies': dict(sorted(picked.items()))}

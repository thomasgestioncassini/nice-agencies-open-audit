"""Choix des agences contrôlées à la source : règle publique, reproductible, fixée avant de connaître les résultats.

Règle (config/audit-policy.json, section « sampling ») :
1. Toujours : les agences de l'éditeur (Gestion Cassini, ImmoVendu).
2. Groupe de comparaison fixe : pour chaque agence de l'éditeur, les K agences classées juste au-dessus et juste
   en dessous (rang publié du relevé archivé).
3. Situations comparables pour l'ancienneté : toutes les agences dont la société exploite plusieurs fiches (même SIREN),
   dont l'enseigne a une date de lancement relevée, ou dont l'ancienneté a été saisie à la main.
4. Échantillon aléatoire : N agences tirées parmi les autres. La graine combine l'empreinte SHA-256 des fichiers
   archivés et la valeur aléatoire publique drand (League of Entropy) du tour fixé d'avance pour le relevé : le premier
   mardi 06:00 UTC après sa date. Seul compte le dernier relevé archivé avant cette échéance. La signature BLS de la
   balise est vérifiée avec la clé publique du réseau. Sans balise authentique, aucun tirage n'est fait.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import random
import urllib.request

DRAND = 'https://api.drand.sh/52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971'   # chaîne « quicknet »
CHAIN_HASH = '52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971'
QUICKNET_GENESIS, QUICKNET_PERIOD = 1692803367, 3      # paramètres publics de la chaîne, épinglés ici
SLOT_HOUR_UTC = 6


def draw_deadline(date_releve: str) -> float:
    """Échéance FIXE du tirage, propre au relevé et connue d'avance : le premier mardi à 06:00 UTC qui suit la date du
    relevé. Elle ne dépend ni de l'heure d'archivage ni du moment où le tirage est lancé."""
    d = dt.date.fromisoformat(date_releve)
    ahead = (1 - d.weekday()) % 7 or 7          # mardi = 1
    t = dt.datetime.combine(d + dt.timedelta(days=ahead), dt.time(SLOT_HOUR_UTC), dt.timezone.utc)
    return t.timestamp()


def committed_snapshot(snapshots: list[dict], date_releve: str) -> dict | None:
    """Relevé engagé pour le tirage : le DERNIER relevé de cette date archivé AVANT l'échéance. Les données peuvent
    changer avant l'échéance (l'aléa n'est pas encore connu) ; après, aucun autre relevé ne peut être choisi."""
    dl = draw_deadline(date_releve)
    ok = [m for m in snapshots if m['date_releve'] == date_releve
          and dt.datetime.fromisoformat(m['archived_utc']).timestamp() < dl]
    return max(ok, key=lambda m: m['archived_utc']) if ok else None


def round_at(t: float) -> int:
    """Premier tour drand publié à l'instant t ou après."""
    return max(1, math.ceil((t - QUICKNET_GENESIS) / QUICKNET_PERIOD) + 1)


def check_beacon(b: dict, expected_round: int, require_bls: bool = True) -> list[str]:
    """Tour, chaîne, cohérence de la valeur aléatoire ET signature BLS authentique (drandverify). Sans bibliothèque BLS,
    la balise est refusée si require_bls est vrai."""
    from .drandverify import verify
    errors = []
    if b.get('round') != expected_round:
        errors.append(f"tour {b.get('round')} au lieu du tour attendu {expected_round}")
    if b.get('chain') != CHAIN_HASH:
        errors.append('chaîne drand inattendue')
    try:
        if hashlib.sha256(bytes.fromhex(b['signature'])).hexdigest() != b['randomness']:
            errors.append('valeur aléatoire différente du SHA-256 de la signature')
    except (KeyError, ValueError):
        errors.append('signature ou valeur aléatoire absente')
        return errors
    ok = verify(b['round'], b['signature'])
    if ok is False:
        errors.append('signature BLS invalide : la balise ne provient pas du réseau drand')
    elif ok is None and require_bls:
        errors.append('signature BLS non vérifiable (bibliothèque py_ecc absente, voir requirements-tirage.txt)')
    return errors


def fetch_beacon(rnd: int, timeout: int = 30) -> dict:
    b = json.load(urllib.request.urlopen(f'{DRAND}/public/{rnd}', timeout=timeout))
    return {'chain': CHAIN_HASH, 'round': b['round'], 'randomness': b['randomness'], 'signature': b['signature'],
            'url': f'{DRAND}/public/{rnd}', 'fetched_utc': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}


def seed_of(inputs_sha256: dict, beacon: dict) -> str:
    """Aucun repli : sans balise valide, il n'y a pas de tirage (statut « en_attente » ou « echec »)."""
    if not beacon or 'randomness' not in beacon:
        raise ValueError('balise drand absente : tirage impossible')
    h = hashlib.sha256()
    for name in sorted(inputs_sha256):
        h.update(f'{name}:{inputs_sha256[name]}\n'.encode())
    h.update(f'drand:{beacon["round"]}:{beacon["randomness"]}'.encode())
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

"""Comparaison du recalcul indépendant avec les valeurs publiées.

Règle de tolérance (config/audit-policy.json) : le site publie les piliers au dixième et la note au centième. Une
valeur est « conforme » si la valeur recalculée, arrondie à la même précision, est identique à la valeur publiée.
Aucune marge supplémentaire n'est accordée. Une valeur recalculée située à moins de 1e-9 d'une frontière d'arrondi est
classée « frontière d'arrondi » (ni conforme ni divergente) et listée, car l'ordre des opérations en virgule flottante
peut alors décider du dernier chiffre.
"""
from __future__ import annotations

import csv
import io

from .recalculate import PILLARS, read_csv

COLS = dict(zip(PILLARS, ('avis', 'service', 'honoraires', 'mentions_legales', 'information', 'anciennete')))


def _status(exact: float, published: float, digits: int) -> str:
    if round(exact, digits) == round(published, digits):
        return 'conforme'
    frac = (abs(exact) * 10 ** digits) % 1
    if abs(frac - 0.5) < 1e-6 and abs(exact - published) <= 10 ** -digits:
        return 'frontiere_arrondi'
    return 'divergente'


def compare(data_dir, recalc: dict, policy: dict) -> dict:
    pub = {a['agence']: a for a in read_csv(data_dir / 'agences.csv')}
    pd, nd = policy['tolerance']['pillar_decimals'], policy['tolerance']['note_decimals']
    rows, anomalies = [], []
    counts = {'conforme': 0, 'divergente': 0, 'frontiere_arrondi': 0}
    rank_div = 0
    for s, r in recalc['agencies'].items():
        p = pub[s]
        pill = {}
        for k in PILLARS:
            pv = float(p[COLS[k]]) if p[COLS[k]] != '' else None
            st = 'non_publie' if pv is None else _status(r['pillars'][k], pv, pd)
            pill[k] = (pv, st)
            if st in ('divergente', 'frontiere_arrondi'):
                anomalies.append({'agence': s, 'objet': f'pilier {k}', 'recalcule': r['pillars'][k], 'publie': pv, 'statut': st})
        n_st = _status(r['note_exact'], float(p['note_publiee']), nd)
        # la note publiée est calculée à partir des piliers arrondis : on compare aussi l'exact non arrondi
        counts[n_st] += 1
        if n_st != 'conforme':
            anomalies.append({'agence': s, 'objet': 'note', 'recalcule': r['note_exact'], 'publie': float(p['note_publiee']),
                              'statut': n_st})
        rk_ok = r['rank'] == int(p['rang_publie'])
        if not rk_ok:
            rank_div += 1
            anomalies.append({'agence': s, 'objet': 'rang', 'recalcule': r['rank'], 'publie': int(p['rang_publie']),
                              'statut': 'divergente'})
        rows.append([s, p['rang_publie'], r['rank'], p['note_publiee'], f"{r['note_exact']:.6f}", n_st]
                    + [f'{r["pillars"][k]:.1f}' for k in PILLARS] + [pill[k][1] for k in PILLARS] + [' '.join(r['rules'])])
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=';', lineterminator='\n')
    w.writerow(['agence', 'rang_publie', 'rang_recalcule', 'note_publiee', 'note_recalculee', 'statut_note']
               + [f'{k}_recalcule' for k in PILLARS] + [f'{k}_statut' for k in PILLARS] + ['regles_appliquees'])
    w.writerows(sorted(rows, key=lambda x: x[2]))
    return {'examined': len(rows), 'notes': counts, 'ranks_divergent': rank_div, 'anomalies': anomalies,
            'calculations_csv': buf.getvalue()}

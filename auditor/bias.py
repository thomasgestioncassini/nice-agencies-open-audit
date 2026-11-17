"""Tests de biais et de robustesse, DÉTERMINISTES (sans IA). Diagnostics contrefactuels : ils ne remplacent jamais
les notes officielles. Règles fixées à l'avance, identiques pour toutes les agences."""
from __future__ import annotations

import datetime as dt
import statistics

from .recalculate import PILLARS


def ranks(pillars: dict, weights: dict, tie: dict) -> dict:
    tot = sum(weights.values())
    note = {s: sum(p[k] * weights[k] for k in PILLARS) / tot for s, p in pillars.items()}
    order = sorted(note, key=lambda s: (-round(note[s], 2), -tie.get(s, 0), s))
    return {s: (i + 1, note[s]) for i, s in enumerate(order)}


def _summary(base: dict, var: dict, watch: list[str]) -> dict:
    moved = [abs(var[s][0] - base[s][0]) for s in base if var[s][0] != base[s][0]]
    top10 = len({s for s in base if base[s][0] <= 10} & {s for s in var if var[s][0] <= 10})
    return {'rangs_changes': len(moved), 'deplacement_max': max(moved, default=0),
            'deplacement_median': statistics.median(moved) if moved else 0, 'top10_inchanges': top10,
            'agences_suivies': {s: {'rang': var[s][0], 'rang_officiel': base[s][0], 'note': round(var[s][1], 2),
                                    'note_officielle': round(base[s][1], 2)} for s in watch if s in base}}


def _groupstats(pillars: dict, notes: dict, members: list[str]) -> dict:
    m = [s for s in members if s in pillars]
    if not m:
        return {'n': 0}
    out = {'n': len(m), 'note_moyenne': round(statistics.mean(notes[s] for s in m), 2)}
    for k in PILLARS:
        out[k] = round(statistics.mean(pillars[s][k] for s in m), 1)
    return out


def bias_tests(recalc: dict, weights: dict, sources: dict, publisher: list[str], neighbours: list[str],
               date_releve: str) -> dict:
    ag = recalc['agencies']
    pillars = {s: r['pillars'] for s, r in ag.items()}
    tie = {s: r['reviews_total'] for s, r in ag.items()}
    base = ranks(pillars, weights, tie)
    out = {'scenarios': {}, 'publisher_specific': {}, 'groups': {}}
    w0 = dict(weights, anc=0)
    out['scenarios']['sans_anciennete'] = _summary(base, ranks(pillars, w0, tie), publisher)
    for k in PILLARS:
        for f, lab in ((1.2, 'plus20'), (0.8, 'moins20')):
            w = dict(weights)
            w[k] = weights[k] * f
            out['scenarios'][f'{k}_{lab}'] = _summary(base, ranks(pillars, w, tie), publisher)
    # Ancienneté comptée depuis le lancement de l'enseigne, pour CHAQUE agence dont cette date est relevée
    ref = dt.date.fromisoformat(date_releve)
    alt = {s: dict(p) for s, p in pillars.items()}
    changed = []
    for s, r in sources.items():
        y = r.get('enseigne_depuis')
        if s in alt and y:
            years = (ref.year - int(y)) + (ref.month - 1) / 12
            alt[s]['anc'] = round(max(0.0, min(100.0, years / 20 * 100)), 1)
            changed.append(s)
    out['publisher_specific']['anciennete_depuis_enseigne'] = {
        'agences_concernees': changed,
        'note': 'date de lancement d’enseigne relevée seulement pour ces agences : la même règle ne peut pas être '
                'appliquée aux autres faute de donnée (contrôle V-10b)',
        **_summary(base, ranks(alt, weights, tie), publisher + [s for s in changed if s not in publisher])}
    notes = {s: base[s][1] for s in base}
    terc = sorted(ag, key=lambda s: ag[s]['reviews_total'])
    n3 = len(terc) // 3
    young, old = [], []
    for s, r in sources.items():
        d = r.get('date_creation_societe')
        if d and s in ag:
            (young if (ref - dt.date.fromisoformat(d[:10])).days < 3652 else old).append(s)
    groups = {'editeur': publisher, 'voisines_editeur': neighbours, 'toutes': list(ag),
              'petit_volume_avis': terc[:n3], 'volume_moyen': terc[n3:2 * n3], 'grand_volume_avis': terc[2 * n3:],
              'societe_moins_10_ans': young, 'societe_10_ans_et_plus': old}
    out['groups'] = {g: _groupstats(pillars, notes, m) for g, m in groups.items()}
    out['groups_definition'] = {
        'voisines_editeur': 'les 5 agences classées juste au-dessus et juste en dessous de chaque agence de l’éditeur',
        'volume': 'tiers des agences selon le nombre total d’avis sur les plateformes',
        'societe': 'âge de la société d’après la date de création publiée (registre)'}
    out['not_testable'] = ['réseaux et indépendantes, vente seule et mixtes, outils numériques : ces catégories ne '
                           'figurent pas dans les exports publics', 'exclusion des avis sans profil identifié : le '
                           'profil « non précisé » est publié, mais pas la part des avis exclus pour ce motif']
    return out

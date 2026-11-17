"""Tests de biais et de robustesse, DÉTERMINISTES (sans IA). Diagnostics contrefactuels : ils ne remplacent jamais
les notes officielles. Règles fixées à l'avance, identiques pour toutes les agences."""
from __future__ import annotations

import csv
import datetime as dt
import json
import shutil
import statistics
import tempfile
from pathlib import Path

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
               date_releve: str, extra: dict | None = None) -> dict:
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
    out['not_testable'] = []
    if extra is not None:
        cat = categories(ag, sources, extra.get('criteria') or {}, extra.get('networks') or [])
        out['groups'].update({g: _groupstats(pillars, notes, m) for g, m in cat['groups'].items()})
        out['groups_definition'].update(cat['definition'])
        out['not_testable'] += cat['not_testable']
        if extra.get('data_dir') and extra.get('cfg'):
            out['avis_non_precises'] = non_precise(extra['data_dir'], extra['cfg'], base, tie, publisher)
    else:
        out['not_testable'].append('catégories réseau, activités, outils numériques et profils : données non fournies')
    return out


def categories(ag: dict, sources: dict, criteria: dict, networks: list[str]) -> dict:
    """Catégories fixées par l'auditeur à partir des seuls exports publics (priorité 4 de la revue ChatGPT)."""
    groups, nt = {}, []
    def host(s):
        return (sources.get(s, {}).get('url_site') or '').lower().replace('.', '-').replace('/', '-')
    net = [s for s in ag if any(p in s or p in host(s) for p in networks)]
    groups['reseau'] = net
    groups['independante'] = [s for s in ag if s not in net]
    acts = {s: (sources.get(s, {}).get('activites') or '') for s in ag}
    if any(acts.values()):
        groups['vente_seule'] = [s for s, a in acts.items() if a and set(a.split(',')) <= {'vente'}]
        groups['vente_et_location_ou_gestion'] = [s for s, a in acts.items() if a and set(a.split(',')) - {'vente'}]
    else:
        nt.append('vente seule et mixtes : la colonne « activites » ne figure pas dans sources-agences.csv de ce relevé')
    est = {}
    for s, rows in criteria.items():
        for r in rows:
            if r.get('critere', '').startswith('Estimation en ligne') and r.get('max') not in ('', None):
                est[s] = r.get('points') not in ('', '0', '0.0', None)
    groups['estimation_en_ligne'] = [s for s in ag if est.get(s) is True]
    groups['sans_estimation_en_ligne'] = [s for s in ag if est.get(s) is False]
    return {'groups': groups, 'not_testable': nt, 'definition': {
        'reseau': 'site ou identifiant contenant un motif de config/networks.json (liste fixée avant les résultats)',
        'activites': 'colonne « activites » de sources-agences.csv (vente, location, gestion) telle que relevée par le site',
        'outils_numeriques': 'critère « Estimation en ligne du prix de vente » de criteres-sites.csv (non applicable : exclu)'}}


def non_precise(data_dir, cfg: dict, base: dict, tie: dict, publisher: list[str]) -> dict:
    """Avis dont le profil n'est pas précisé : aucun n'est exclu ; part et effet contrefactuel de leur retrait."""
    from .recalculate import recalculate
    data_dir = Path(data_dir)
    with open(data_dir / 'avis-elementaires.csv', encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter=';'))
    np_ = [r for r in rows if r['profil'] == 'non_precise']
    counted = [r for r in rows if r['compte_vente_achat'] == '1']
    out = {'avis_non_precises': len(np_), 'dont_comptes': sum(r['compte_vente_achat'] == '1' for r in np_),
           'avis_comptes': len(counted),
           'part_dans_les_avis_comptes': round(sum(r['compte_vente_achat'] == '1' for r in np_) / len(counted), 3) if counted else None,
           'exclus_faute_de_profil': sum(r['compte_vente_achat'] != '1' for r in np_)}
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        for p in data_dir.iterdir():
            if p.is_file() and p.name != 'avis-elementaires.csv':
                shutil.copy(p, t / p.name)
        with open(t / 'avis-elementaires.csv', 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=';')
            w.writeheader()
            w.writerows(r for r in rows if r['profil'] != 'non_precise')
        alt = recalculate(t, cfg)['agencies']
    var = ranks({s: r['pillars'] for s, r in alt.items()}, cfg['weights'], tie)
    out['scenario_sans_non_precises'] = _summary(base, var, publisher)
    return out

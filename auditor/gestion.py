"""Recalcul indépendant du comparateur gestion locative de meilleure-agence-nice.fr (méthode G1.2 du 18/11/2026).

Écrit à partir du TEXTE PUBLIC de la méthode (https://meilleure-agence-nice.fr/methode/gestion-locative/, rubrique
« Formules ») et du dossier de recalcul publié par le site (/methode/gestion-locative/reproduction/). Il n'importe ni ne
copie le code de production. Bibliothèque standard de Python uniquement : aucun appel réseau, aucune IA.

Reprises telles quelles (non refaites, comme pour le classement vente) : qualification des avis (bailleur ou non, niveau
de preuve, exclusions), dédoublonnage entre plateformes (colonne retenu), partage entre agences (poids_partage), lecture
des problèmes de service, lecture des sites et barèmes (criteres.csv). Les notes publiées ne sont lues que pour la
comparaison.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
from collections import defaultdict
from pathlib import Path

PILLARS = ('avis', 'serv', 'hono', 'conf', 'info', 'anc')
PUB_COL = {'avis': 'avis', 'serv': 'service', 'hono': 'transparence', 'conf': 'mentions_legales', 'info': 'information',
           'anc': 'anciennete'}
FILES = ('gestion-parametres.json', 'gestion-agences.csv', 'gestion-avis.csv', 'gestion-criteres.csv')


def _csv(p: Path) -> list[dict]:
    with open(p, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def _r1(x: float) -> float:
    return round(x, 1)


def _age(date: str, ref: dt.date, mdays: float) -> float | None:
    try:
        return (ref - dt.date.fromisoformat(date[:10])).days / mdays
    except (TypeError, ValueError):
        return None


def available(data_dir: Path) -> bool:
    return all((Path(data_dir) / f).exists() for f in FILES)


def recalculate(data_dir: Path, cfg: dict) -> dict:
    d = Path(data_dir)
    params = json.loads((d / 'gestion-parametres.json').read_text(encoding='utf-8'))
    ref = dt.date.fromisoformat(params['date_releve'])
    rv, sv, W = cfg['reviews'], cfg['service'], cfg['weights']
    items = _csv(d / 'gestion-avis.csv')
    notes = [float(x['note']) for x in items if x['note'] != '']
    m_ref = round(sum(notes) / len(notes), 3) if notes else None   # moyenne des notes de tous les avis comptés
    by = defaultdict(list)
    for x in items:
        by[x['agence_id']].append(x)
    crit = defaultdict(lambda: defaultdict(list))
    for c in _csv(d / 'gestion-criteres.csv'):
        crit[c['agence_id']][c['pilier']].append(c)
    out = {}
    for a in _csv(d / 'gestion-agences.csv'):
        i = a['agence_id']
        its = by.get(i, [])
        uniq = [x for x in its if x['retenu'] == '1']
        # Avis : qualité (moyenne pondérée par l'âge et le partage, lissée vers M_REF), volume, régularité
        sw = sr = n = 0.0
        sem, n_reg = set(), 0.0
        for x in uniq:
            k = float(x['poids_partage'] or 1)
            age = _age(x['date'], ref, rv['month_days'])
            w = rv['undated_review_weight'] if age is None else 0.5 ** (max(0.0, age) / rv['half_life_months'])
            sw += w * k
            sr += w * k * float(x['note'])
            n += k
            if age is not None and 0 <= age < rv['semesters'] * rv['semester_months']:
                sem.add(int(age // rv['semester_months']))
                n_reg += k
        mean = (rv['smoothing_fictitious_reviews'] * m_ref + sr) / (rv['smoothing_fictitious_reviews'] + sw) if sw else None
        q = _r1(max(0.0, min(100.0, (mean - 3) / 2 * 100))) if mean else rv['no_review_value']
        v = _r1(min(100.0, 100 * math.log(1 + n) / math.log(rv['volume_cap'] + 1)))
        reg = _r1(100 * min(1.0, len(sem) / min(rv['semesters'], max(rv['regularity_min_denominator'], n_reg)))) if sem else 0.0
        avis = rv['no_review_value'] if n == 0 else _r1(rv['quality_share'] * q + rv['volume_share'] * v + rv['regularity_share'] * reg)
        # Service : réponses aux avis Google négatifs (tous les avis comptés, doublons compris), problèmes (avis retenus)
        if not its:
            serv, resp, prob = sv['no_review_value'], None, None
        else:
            neg = [x for x in its if x['plateforme'] == 'google' and x['note'] != '' and float(x['note']) <= 3
                   and x['reponse'] in ('0', '1')]
            resp = (_r1(100 * (sum(x['reponse'] == '1' for x in neg) + 2) / (len(neg) + 4)) if neg
                    else sv['no_negative_value'])
            rd = [x for x in uniq if x['service'] in ('probleme', 'ok')]
            prob = (cfg['neutral_value'] if len(rd) < sv['min_texts'] else
                    _r1(max(0.0, 100 * (1 - sum(x['service'] == 'probleme' for x in rd) / len(rd) / sv['problems_zero_at_share']))))
            wr, wp = round(sv['response_share'] * 100), round(sv['problems_share'] * 100)   # 40 et 60
            serv = _r1((resp * wr + prob * wp) / 100)
        sc = {'avis': avis, 'serv': serv}
        for p in ('hono', 'conf', 'info'):
            rows = [c for c in crit[i][p] if c['max'] not in ('', None)]
            mx = sum(float(c['max']) for c in rows)
            sc[p] = _r1(100 * sum(float(c['points'] or 0) for c in rows) / mx) if mx else None
        da = a['date_anciennete']
        if da:
            y, mo = int(da[:4]), (int(da[5:7]) if len(da) >= 7 else 6)
            sc['anc'] = _r1(max(0.0, min(100.0, ((ref.year - y) + (ref.month - mo) / 12) / cfg['seniority_full_years'] * 100)))
        else:
            sc['anc'] = None
        exact = sum((cfg['neutral_value'] if sc[p] is None else sc[p]) * W[p] for p in PILLARS) / sum(W.values())
        g = cfg['groups']
        grp = ('évaluée' if n >= g['evaluee_min_reviews'] and len(sem) >= g['evaluee_min_semesters']
               else 'peu évaluée' if n > 0 else 'données insuffisantes')
        out[i] = {'nom': a['nom'], 'slug': a['slug'], 'pillars': sc, 'note': round(exact, 2), 'n': round(n, 2),
                  'semesters': len(sem), 'group': grp, 'detail': {'quality': q, 'volume': v, 'regularity': reg,
                                                                  'response': resp, 'problems': prob}}
    for grp, key in (('évaluée', 'rank'), ('peu évaluée', 'rank_ind')):
        lst = sorted((i for i in out if out[i]['group'] == grp), key=lambda i: (-out[i]['note'], -out[i]['n'], out[i]['nom']))
        for k, i in enumerate(lst, 1):
            out[i][key] = k
    return {'date_releve': str(ref), 'm_ref': m_ref, 'm_ref_publie': params.get('moyenne_reference_M_REF'), 'agencies': out}


def compare(data_dir: Path, res: dict) -> dict:
    pub = {a['agence_id']: a for a in _csv(Path(data_dir) / 'gestion-agences.csv')}
    rows, bad = [], []
    for i, r in res['agencies'].items():
        a = pub[i]
        diffs = []
        for p in PILLARS:
            pv = a[PUB_COL[p]]
            if (r['pillars'][p] is None) != (pv == '') or (pv != '' and abs(float(pv) - r['pillars'][p]) > 0.05 + 1e-9):
                diffs.append(f'pilier {p}')
        if abs(float(a['note_publiee']) - r['note']) > 0.005 + 1e-9:
            diffs.append('note')
        if a['groupe_publie'] != r['group']:
            diffs.append('groupe')
        if str(r.get('rank', '')) != a['rang_publie'] or str(r.get('rank_ind', '')) != a['rang_indicatif_publie']:
            diffs.append('ordre')
        if abs(float(a['avis_comptes_publies']) - r['n']) > 0.005 + 1e-9 or int(a['semestres_actifs_publies']) != r['semesters']:
            diffs.append('avis comptés ou semestres')
        rows.append([a['slug'] or i, a['groupe_publie'], r['group'], a['rang_publie'] or a['rang_indicatif_publie'],
                     r.get('rank') or r.get('rank_ind') or '', a['note_publiee'], f"{r['note']:.2f}",
                     *[f"{r['pillars'][p]:.1f}" if r['pillars'][p] is not None else '' for p in PILLARS],
                     'conforme' if not diffs else ' '.join(diffs)])
        if diffs:
            bad.append({'agence': a['slug'] or i, 'ecarts': diffs})
    mref_ok = res['m_ref'] is not None and res['m_ref_publie'] is not None and abs(res['m_ref'] - res['m_ref_publie']) < 0.0005
    head = ['agence', 'groupe_publie', 'groupe_recalcule', 'rang_publie', 'rang_recalcule', 'note_publiee', 'note_recalculee',
            'avis', 'service', 'transparence', 'mentions_legales', 'information', 'anciennete', 'statut']
    csv_txt = '\n'.join(';'.join(str(c) for c in row) for row in [head] + rows) + '\n'
    groups = defaultdict(int)
    for r in res['agencies'].values():
        groups[r['group']] += 1
    return {'status': 'conforme' if not bad and mref_ok else 'divergences', 'examined': len(rows), 'divergent': bad,
            'm_ref': res['m_ref'], 'm_ref_publie': res['m_ref_publie'], 'm_ref_conforme': mref_ok,
            'groups': dict(groups), 'calculations_csv': csv_txt}


def check(data_dir: Path, cfg: dict) -> dict:
    if not available(data_dir):
        return {'status': 'non_execute', 'reason': 'fichiers du comparateur gestion absents du relevé'}
    return compare(data_dir, recalculate(data_dir, cfg))

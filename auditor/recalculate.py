"""Moteur de recalcul indépendant du classement meilleure-agence-nice.fr (méthode v5 du 14/11/2026).

Écrit à partir du TEXTE PUBLIC de la méthode (https://meilleure-agence-nice.fr/methode/details/) et du dictionnaire des
fichiers de reproduction. Il n'importe ni ne copie le code de production. Chaque fois que le texte ne suffisait pas à
fixer une règle, l'interprétation retenue est décrite dans docs/interpretations.md, avec sa source.

Bibliothèque standard de Python 3.10+ uniquement : aucun appel réseau, aucune IA.
Les notes finales publiées ne sont JAMAIS lues ici : elles ne servent qu'à la comparaison (compare.py).
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
from collections import defaultdict
from pathlib import Path

PILLARS = ('avis', 'serv', 'hono', 'conf', 'info', 'anc')


def read_csv(path: Path) -> list[dict]:
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


class Method:
    """Règles de la méthode v5, lues dans config/methodology-v5.json (jamais dans les données auditées)."""

    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.weights = cfg['weights']
        r = cfg['reviews']
        self.prior = r['smoothing_fictitious_reviews']
        self.half_life = r['half_life_months']
        self.vol_cap = r['volume_cap']
        self.excluded = set(r['excluded_profiles'])
        self.q_share, self.v_share, self.r_share = r['quality_share'], r['volume_share'], r['regularity_share']
        s = cfg['service']
        self.resp_share, self.prob_share = s['response_share'], s['problems_share']
        self.prob_zero_at = s['problems_score_zero_at_share']
        self.min_texts = s['min_texts']
        self.neutral = cfg['missing']['neutral_value']
        self.anc_full_years = cfg['seniority']['full_score_years']
        self.undated_weight = r['undated_review_weight']
        self.no_negative = s['no_negative_review_score']


def r1(x: float) -> float:
    """Arrondi au dixième, appliqué par le site à chaque sous-critère et pilier (I-7). Arrondi « au plus proche » de Python."""
    return round(x, 1)


def age_months(date_str: str, ref: dt.date) -> float:
    """Âge d'un avis en mois de 30,44 jours (I-5)."""
    return max(0.0, (ref - dt.date.fromisoformat(date_str[:10])).days / 30.44)


def last_calendar_months(ref: dt.date, n: int = 12) -> set[str]:
    """Les n derniers mois CALENDAIRES, mois du relevé compris (I-3)."""
    y, mo, out = ref.year, ref.month, set()
    for _ in range(n):
        out.add(f'{y:04d}-{mo:02d}')
        mo -= 1
        if mo == 0:
            y, mo = y - 1, 12
    return out


def star_to_100(x: float) -> float:
    """Conversion publiée : 3/5 ou moins = 0, 4/5 = 50, 5/5 = 100 (linéaire entre les deux)."""
    return max(0.0, min(100.0, (x - 3.0) * 50.0))


def nice_average(aggregates: list[dict]) -> float:
    """Moyenne de Nice (I-2) : moyenne simple, sur les agences, de la note moyenne de chaque agence
    (notes de ses plateformes pondérées par leur nombre d'avis). Arrondie au millième."""
    per: dict[str, list] = defaultdict(lambda: [0.0, 0.0])
    for a in aggregates:
        n = float(a['nombre'] or 0)
        per[a['agence']][0] += float(a['note']) * n
        per[a['agence']][1] += n
    means = [num / den for num, den in per.values() if den]
    return round(sum(means) / len(means), 3)


def pillar_reviews(items: list[dict], aggs: list[dict], m: Method, ref: dt.date, m_ref: float) -> tuple[float, dict]:
    """Pilier Avis. Avis retenus pour la qualité : colonne retenu_qualite (doublons retirés par le site, contrôle C-3)."""
    kept = [x for x in items if x['retenu_qualite'] == '1']
    sw = swr = n = 0.0
    for x in kept:
        k = 1.0 / int(x['nb_agences_partageant'] or 1)
        w = 0.5 ** (age_months(x['date'], ref) / m.half_life) * k
        sw += w
        swr += w * float(x['note'])
        n += k
    # Plateformes non relevées avis par avis : comptées par leur note globale, chaque avis au poids fixe 0,5 (I-1)
    detailed = {x['plateforme'] for x in items if x['releve_complet'] == '1'}
    agg_used = 0.0
    for a in aggs:
        if a['plateforme'] in detailed:
            continue
        k = float(a['nombre'] or 0)
        sw += m.undated_weight * k
        swr += m.undated_weight * float(a['note']) * k
        n += k
        agg_used += k
    if sw:
        mean = (m.prior * m_ref + swr) / (m.prior + sw)
        quality = r1(star_to_100(mean))
    else:
        mean, quality = None, m.neutral
    volume = r1(min(100.0, 100.0 * math.log(1 + n) / math.log(1 + m.vol_cap)))
    # Régularité (I-3, I-4) : tous les avis de vente ou d'achat datés des 12 derniers mois calendaires, doublons compris
    win = last_calendar_months(ref)
    rec = [x for x in items if x['compte_vente_achat'] == '1' and x['date'][:7] in win]
    months = {x['date'][:7] for x in rec}
    if items:
        regularity = r1(min(1.0, len(months) / min(12, max(3, len(rec)))) * 100) if rec else 0.0
    else:
        regularity = 0.0 if not aggs else None
    if regularity is None:   # I-6 : régularité non vérifiable, son poids est réparti sur qualité et volume
        score = (m.q_share * quality + m.v_share * volume) / (m.q_share + m.v_share)
    else:
        score = m.q_share * quality + m.v_share * volume + m.r_share * regularity
    return r1(score), {'quality': quality, 'volume': volume, 'regularity': regularity, 'n': n, 'aggregate_reviews': agg_used,
                       'mean_smoothed': mean, 'months_active': len(months), 'reviews_12m': len(rec)}


def pillar_service(items: list[dict], m: Method) -> tuple[float, dict]:
    tx = [x for x in items if x['compte_vente_achat'] == '1']
    # Réponses : avis Google de vente/achat à 3 étoiles ou moins dont la présence d'une réponse a été relevée (I-8)
    neg = [x for x in tx if x['plateforme'] == 'google' and float(x['note'] or 5) <= 3 and x['reponse_agence'] in ('0', '1')]
    if neg:
        resp = r1(100.0 * (sum(1 for x in neg if x['reponse_agence'] == '1') + 2) / (len(neg) + 4))
    else:
        resp = m.no_negative
    # Problèmes : avis uniques avec texte lu (colonne retenu_service, I-9)
    texts = [x for x in items if x['retenu_service'] == '1' and x['probleme'] in ('ok', 'probleme')]
    if len(texts) < m.min_texts:
        prob = m.neutral
    else:
        share = sum(1 for x in texts if x['probleme'] == 'probleme') / len(texts)
        prob = r1(max(0.0, 100.0 * (1 - share / m.prob_zero_at)))
    return r1(m.resp_share * resp + m.prob_share * prob), {'response': resp, 'problems': prob, 'negatives': len(neg),
                                                           'texts': len(texts)}


def pillar_points(rows: list[dict]) -> float | None:
    """Points obtenus / points applicables × 100. Un critère sans maximum est « non applicable » (section 10)."""
    pts = mx = 0.0
    for r in rows:
        if r['max'] in ('', None):
            continue
        pts += float(r['points'] or 0)
        mx += float(r['max'])
    return None if mx == 0 else r1(100.0 * pts / mx)


def pillar_seniority(date_str: str, m: Method, ref: dt.date) -> float | None:
    """0 à la création, 100 à 20 ans. Âge compté en années et mois, le jour étant ignoré (I-10)."""
    if not date_str:
        return None
    y, mo = int(date_str[:4]), (int(date_str[5:7]) if len(date_str) >= 7 else 6)
    years = (ref.year - y) + (ref.month - mo) / 12
    # Ordre des opérations (années / 20 × 100) : il décide des cas situés exactement à 0,05 près de l arrondi (I-12)
    return r1(max(0.0, min(100.0, years / m.anc_full_years * 100)))


def recalculate(data_dir: Path, cfg: dict) -> dict:
    m = Method(cfg)
    params = json.loads((data_dir / 'parametres.json').read_text(encoding='utf-8'))
    ref = dt.date.fromisoformat(params['date_releve'])
    agencies = read_csv(data_dir / 'agences.csv')
    aggs_all = read_csv(data_dir / 'agregats-plateformes.csv')
    m_ref = nice_average(aggs_all)
    aggs: dict[str, list] = defaultdict(list)
    for a in aggs_all:
        aggs[a['agence']].append(a)
    order = {}
    src = data_dir / 'sources-agences.csv'
    if src.exists():
        order = {r['agence']: int(r['id']) for r in read_csv(src)}
    by_ag: dict[str, list] = defaultdict(list)
    for x in read_csv(data_dir / 'avis-elementaires.csv'):
        by_ag[x['agence']].append(x)
    crit: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for r in read_csv(data_dir / 'criteres-sites.csv'):
        crit[r['agence']][r['pilier']].append(r)
    out = {}
    for a in agencies:
        s = a['agence']
        sc, rules = {}, []
        sc['avis'], d_avis = pillar_reviews(by_ag[s], aggs[s], m, ref, m_ref)
        sc['serv'], d_serv = pillar_service(by_ag[s], m)
        for p in ('hono', 'conf', 'info'):
            sc[p] = pillar_points(crit[s][p])
        sc['anc'] = pillar_seniority(a['date_anciennete'], m, ref)
        if a['sans_site'] == '1':
            for p in ('hono', 'conf', 'info'):
                if sc[p] is None:
                    sc[p] = 0.0
                    rules.append(f'{p}:sans_site_0')
        for p in PILLARS:
            if sc[p] is None:
                sc[p] = m.neutral
                rules.append(f'{p}:valeur_neutre_{m.neutral}')
        exact = sum(sc[p] * m.weights[p] for p in PILLARS) / sum(m.weights.values())
        ntot = sum(float(x['nombre'] or 0) for x in aggs[s])
        out[s] = {'pillars': sc, 'note_exact': exact, 'note': round(exact, 2), 'rules': rules, 'reviews_total': ntot,
                  'detail': {'avis': d_avis, 'serv': d_serv}}
    # Rang (I-11) : note arrondie au centième, puis nombre total d'avis des plateformes, puis identifiant stable
    ranking = sorted(out, key=lambda s: (-out[s]['note'], -out[s]['reviews_total'], order.get(s, 10**9), s))
    for i, s in enumerate(ranking, 1):
        out[s]['rank'] = i
    return {'date_releve': str(ref), 'm_ref': m_ref, 'agencies': out}

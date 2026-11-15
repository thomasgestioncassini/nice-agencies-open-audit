"""Contrôles de cohérence des données publiées (sans IA, sans réseau).

Ces contrôles portent sur la cohérence interne des fichiers et sur leur conformité au texte de la méthode. Ils ne
vérifient PAS les données à leur source (avis sur les plateformes, pages des sites, registre des entreprises) : c'est la
dimension « données primaires », traitée séparément et marquée « non vérifiée » tant qu'elle n'a pas été contrôlée.
"""
from __future__ import annotations

import datetime as dt
import json
from collections import Counter, defaultdict
from pathlib import Path

from .recalculate import read_csv

REQUIRED = {
    'agences.csv': ['agence', 'rang_publie', 'note_publiee', 'date_anciennete', 'sans_site', 'piliers_provisoires', 'avis',
                    'service', 'honoraires', 'mentions_legales', 'information', 'anciennete'],
    'avis-elementaires.csv': ['agence', 'plateforme', 'id', 'date', 'note', 'profil', 'compte_vente_achat', 'releve_complet',
                              'retenu_qualite', 'retenu_service', 'nb_agences_partageant', 'reponse_agence', 'probleme'],
    'agregats-plateformes.csv': ['agence', 'plateforme', 'note', 'nombre'],
    'criteres-sites.csv': ['agence', 'pilier', 'famille', 'critere', 'points', 'max'],
}
PROFILES = {'vendeur', 'acquereur', 'non_precise', 'locataire', 'bailleur', 'syndic'}
PLATFORMS = {'google', 'opinionsystem', 'immodvisor'}


def finding(code: str, severity: str, message: str, agencies=(), count=None, **extra) -> dict:
    f = {'code': code, 'severity': severity, 'message': message, 'agencies': sorted(set(agencies))[:50]}
    if count is not None:
        f['count'] = count
    f.update(extra)
    return f


def validate(data_dir: Path, cfg: dict, publisher: list[str]) -> dict:
    out: list[dict] = []
    # V-1 colonnes obligatoires
    for name, cols in REQUIRED.items():
        with open(data_dir / name, encoding='utf-8') as f:
            head = f.readline().rstrip('\n').split(';')
        missing = [c for c in cols if c not in head]
        if missing:
            out.append(finding('V-1', 'bloquant', f'{name} : colonnes absentes {missing}'))
    if any(f['severity'] == 'bloquant' for f in out):
        return {'findings': out, 'blocking': True}
    params = json.loads((data_dir / 'parametres.json').read_text(encoding='utf-8'))
    ref = dt.date.fromisoformat(params['date_releve'])
    ag = read_csv(data_dir / 'agences.csv')
    slugs = [a['agence'] for a in ag]
    items = read_csv(data_dir / 'avis-elementaires.csv')
    crit = read_csv(data_dir / 'criteres-sites.csv')
    src_path = data_dir / 'sources-agences.csv'
    src = {r['agence']: r for r in read_csv(src_path)} if src_path.exists() else {}

    # V-2 paramètres publiés = méthode de l'auditeur
    w_pub = params.get('poids', {})
    if w_pub != cfg['weights']:
        out.append(finding('V-2', 'majeur', f'poids publiés {w_pub} différents de la méthode {cfg["weights"]}'))
    for key, val in (('avis_fictifs_PRIOR', cfg['reviews']['smoothing_fictitious_reviews']),
                     ('demi_vie_mois', cfg['reviews']['half_life_months']), ('plafond_volume', cfg['reviews']['volume_cap'])):
        if params.get(key) != val:
            out.append(finding('V-2', 'majeur', f'paramètre {key} publié {params.get(key)} ≠ méthode {val}'))

    # V-3 rangs : 1..N sans trou ni doublon ; identifiants uniques
    ranks = sorted(int(a['rang_publie']) for a in ag)
    if ranks != list(range(1, len(ag) + 1)):
        out.append(finding('V-3', 'majeur', 'les rangs publiés ne forment pas une suite 1..N sans doublon'))
    if len(set(slugs)) != len(slugs):
        out.append(finding('V-3', 'majeur', 'agence en double dans agences.csv'))
    if src and len({r['id'] for r in src.values()}) != len(src):
        out.append(finding('V-3', 'majeur', 'identifiant stable en double dans sources-agences.csv'))

    # V-4 valeurs des avis
    bad_val = [x for x in items if not (0 <= float(x['note'] or 0) <= 5) or x['profil'] not in PROFILES
               or x['plateforme'] not in PLATFORMS or dt.date.fromisoformat(x['date'][:10]) > ref]
    if bad_val:
        out.append(finding('V-4', 'majeur', 'avis avec note hors de 0 à 5, profil ou plateforme inconnus, ou date future',
                           [x['agence'] for x in bad_val], len(bad_val)))

    low = [x for x in items if float(x['note'] or 0) < 1]
    if low:
        out.append(finding('V-4b', 'mineur', 'avis notés sous 1/5, minimum habituel d’une échelle à étoiles : ils entrent '
                           'tels quels dans la moyenne ; échelle d’Opinion System à vérifier à la source',
                           [x['agence'] for x in low], len(low),
                           counted=sum(1 for x in low if x['retenu_qualite'] == '1')))

    # V-5 cohérence des drapeaux : profil écarté ⇔ compte_vente_achat = 0 ; retenu ⇒ compté et relevé complet
    excl = set(cfg['reviews']['excluded_profiles'])
    incoh = [x for x in items if (x['profil'] in excl) != (x['compte_vente_achat'] == '0')
             or (x['retenu_qualite'] == '1' and (x['compte_vente_achat'] != '1' or x['releve_complet'] != '1'))
             or (x['retenu_service'] == '1' and x['compte_vente_achat'] != '1')]
    if incoh:
        out.append(finding('V-5', 'majeur', 'drapeaux d’avis incohérents avec le profil ou le relevé',
                           [x['agence'] for x in incoh], len(incoh)))

    # V-6 doublons déclarés : avis comptables mais non retenus (le site les dit doublons ; non vérifiable sans texte)
    dup = Counter(x['agence'] for x in items if x['compte_vente_achat'] == '1' and x['releve_complet'] == '1'
                  and x['retenu_qualite'] == '0')
    out.append(finding('V-6', 'info', 'avis déclarés doublons par le site (non vérifiable à partir des exports : '
                       'les textes ne sont pas publiés)', list(dup), sum(dup.values()),
                       publisher_counts={p: dup.get(p, 0) for p in publisher}))

    # V-7 avis partagés : un avis compté 1/k doit figurer chez k agences (même plateforme, même identifiant)
    seen = defaultdict(set)
    for x in items:
        seen[(x['plateforme'], x['id'])].add(x['agence'])
    bad_share = [x for x in items if int(x['nb_agences_partageant'] or 1) > 1
                 and len(seen[(x['plateforme'], x['id'])]) != int(x['nb_agences_partageant'])]
    if bad_share:
        out.append(finding('V-7', 'mineur', 'avis déclarés partagés entre k agences, mais présents sur un autre nombre '
                           'de fiches dans l’export (le partage est détecté sur le texte, que l’export ne contient pas)',
                           [x['agence'] for x in bad_share], len(bad_share)))

    # V-8 points des critères : 0 ≤ points ≤ max, maxima conformes au barème publié
    allowed = {'hono': {20, 30, 100}, 'conf': {5, 10, 15, 20, 25, 100}, 'info': {1}}
    bad_pts = [r for r in crit if r['max'] and (not (0 <= float(r['points'] or 0) <= float(r['max']))
                                                  or int(float(r['max'])) not in allowed.get(r['pilier'], set()))]
    if bad_pts:
        out.append(finding('V-8', 'majeur', 'points de critère hors barème', [r['agence'] for r in bad_pts], len(bad_pts)))

    # V-9 couverture : critères « non applicables » (sans maximum), par critère
    na = Counter(r['critere'] for r in crit if not r['max'])
    tot = Counter(r['critere'] for r in crit)
    for c, n in na.items():
        if n / tot[c] >= 0.5:
            out.append(finding('V-9', 'majeur', f'critère « {c} » non applicable pour {n} agences sur {tot[c]} : '
                               'la méthode le compte parmi les 23 critères, mais il ne pèse presque nulle part',
                               count=n, total=tot[c]))

    # V-10 ancienneté : sociétés partagées, enseignes plus récentes que la société, saisies manuelles
    if src:
        by_siren = defaultdict(list)
        for s, r in src.items():
            if r.get('siren'):
                by_siren[r['siren']].append(s)
        shared = {k: v for k, v in by_siren.items() if len(v) > 1}
        out.append(finding('V-10', 'info', 'agences exploitées par une même société (même SIREN) : même date d’ancienneté',
                           [s for v in shared.values() for s in v], len(shared), groups=shared))
        brand = {s: r['enseigne_depuis'] for s, r in src.items() if r.get('enseigne_depuis')}
        out.append(finding('V-10b', 'majeur' if brand else 'info',
                           'date de lancement d’enseigne relevée pour seulement ' + str(len(brand)) +
                           ' agence(s) sur ' + str(len(src)) + ' : la comparaison « enseigne récente, société ancienne » '
                           'ne peut pas être faite pour les concurrentes à partir des exports',
                           list(brand), len(brand), brands=brand))
        manual = [s for s, r in src.items() if r.get('source_anciennete') == 'rachat_prouve_saisie_manuelle']
        out.append(finding('V-10c', 'info', 'ancienneté saisie à la main (rachat déclaré prouvé)', manual, len(manual)))
        none_ = [s for s, r in src.items() if r.get('source_anciennete') == 'non_relevee']
        if none_:
            out.append(finding('V-10d', 'info', 'date de création de la société non relevée (valeur neutre 50)', none_, len(none_)))
    else:
        out.append(finding('V-11', 'mineur', 'sources-agences.csv absent : identifiants stables, dates d’observation et '
                           'URL des preuves indisponibles pour ce relevé'))
    return {'findings': out, 'blocking': False}

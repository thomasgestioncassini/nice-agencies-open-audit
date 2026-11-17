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


def validate(data_dir: Path, cfg: dict, publisher: list[str], prev_dir: Path | None = None) -> dict:
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

    # V-4 valeurs des avis (une note vide est invalide : elle n'est jamais remplacée par une valeur par défaut)
    empty = [x for x in items if x['note'] == '' or x['date'] == '']
    if empty:
        out.append(finding('V-4a', 'majeur', 'avis sans note ou sans date', [x['agence'] for x in empty], len(empty)))
    items_ok = [x for x in items if x['note'] != '' and x['date'] != '']
    bad_val = [x for x in items_ok if not (0 <= float(x['note']) <= 5) or x['profil'] not in PROFILES
               or x['plateforme'] not in PLATFORMS or dt.date.fromisoformat(x['date'][:10]) > ref]
    if bad_val:
        out.append(finding('V-4', 'majeur', 'avis avec note hors de 0 à 5, profil ou plateforme inconnus, ou date future',
                           [x['agence'] for x in bad_val], len(bad_val)))

    low = [x for x in items_ok if float(x['note']) < 1]
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

    # V-12 avis relevés un par un comparés au nombre d'avis déclaré par la plateforme (plateformes relevées en entier)
    declared = defaultdict(float)
    for a in read_csv(data_dir / 'agregats-plateformes.csv'):
        declared[(a['agence'], a['plateforme'])] += float(a['nombre'] or 0)
    itemized = Counter((x['agence'], x['plateforme']) for x in items if x['releve_complet'] == '1')
    every = {f'{k[0]}|{k[1]}': {'releves': n, 'declares': declared[k]} for k, n in itemized.items()
             if k in declared and n != declared[k]}
    no_agg = [f'{k[0]}|{k[1]}' for k in itemized if k not in declared]
    out.append(finding('V-12a', 'info', 'toutes les plateformes relevées en entier dont le nombre d’avis relevés diffère, '
                       'même d’un avis, du nombre affiché (les deux nombres viennent des exports du site)',
                       [k.split('|')[0] for k in every], len(every), detail=every, sans_agregat=no_agg))
    gaps = {k: v for k, v in every.items() if abs(v['releves'] - v['declares']) > max(2, 0.1 * v['declares'])}
    if gaps:
        out.append(finding('V-12', 'majeur', 'plateformes déclarées relevées en entier dont le nombre d’avis relevés '
                           's’écarte de plus de 10 % (et de plus de 2) du nombre affiché par la plateforme : doubles '
                           'comptages ou fiches de plusieurs établissements possibles', [k.split('|')[0] for k in gaps],
                           len(gaps), detail=gaps, publisher_concerned=[p for p in publisher if any(k.startswith(p + '|') for k in gaps)]))
    else:
        out.append(finding('V-12', 'info', f'nombre d’avis relevés un par un cohérent avec le nombre affiché par la '
                           f'plateforme pour les {len(itemized)} plateformes relevées en entier (écart toléré : 10 % ou 2 avis)',
                           count=0))

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
        exc = [s for s, r in src.items() if (r.get('source_anciennete') or '').startswith('exception_editeur')]
        out.append(finding('V-10e', 'info', 'ancienneté fixée par une exception déclarée par l’éditeur (publiée dans la '
                           'méthode ; à vérifier : elle doit être défavorable à l’agence concernée)', exc, len(exc),
                           sources={s: src[s]['source_anciennete'] for s in exc}))
        dates = {a['agence']: a.get('date_anciennete') or '' for a in ag}
        split = {k: {s: dates.get(s) for s in v} for k, v in shared.items() if len({dates.get(s) for s in v}) > 1}
        unexplained = {k: v for k, v in split.items()
                       if any(src[s].get('source_anciennete') == 'registre_des_entreprises' for s in v)
                       and not any(src[s].get('source_anciennete') != 'registre_des_entreprises' for s in v)}
        out.append(finding('V-10f', 'majeur' if unexplained else 'info',
                           'sociétés partagées dont les agences ont des dates d’ancienneté différentes '
                           '(expliquées par une saisie manuelle ou une exception déclarée, sauf mention contraire)',
                           [s for v in split.values() for s in v], len(split), groups=split,
                           sans_explication=list(unexplained)))
        none_ = [s for s, r in src.items() if r.get('source_anciennete') == 'non_relevee']
        if none_:
            out.append(finding('V-10d', 'info', 'date de création de la société non relevée (valeur neutre 50)', none_, len(none_)))
    else:
        out.append(finding('V-11', 'mineur', 'sources-agences.csv absent : identifiants stables, dates d’observation et '
                           'URL des preuves indisponibles pour ce relevé'))
    if prev_dir is not None:
        out += history(prev_dir, data_dir, publisher)
    return {'findings': out, 'blocking': False}


def history(prev_dir: Path, data_dir: Path, publisher: list[str]) -> list[dict]:
    """V-13 : comparaison avec le relevé archivé précédent. Détecte des signes de falsification que le recalcul seul ne
    voit pas : avis apparus avec une date antérieure au relevé précédent (sur une plateforme déjà relevée en entier),
    avis disparus, points de critères modifiés sans nouvelle lecture du site."""
    out = []
    p_ref = dt.date.fromisoformat(json.loads((prev_dir / 'parametres.json').read_text(encoding='utf-8'))['date_releve'])
    prev = read_csv(prev_dir / 'avis-elementaires.csv')
    cur = read_csv(data_dir / 'avis-elementaires.csv')
    prev_keys = {(x['agence'], x['plateforme'], x['id']) for x in prev}
    cur_keys = {(x['agence'], x['plateforme'], x['id']) for x in cur}
    complete_before = {(x['agence'], x['plateforme']) for x in prev if x['releve_complet'] == '1'}
    back = Counter(x['agence'] for x in cur if (x['agence'], x['plateforme'], x['id']) not in prev_keys
                   and (x['agence'], x['plateforme']) in complete_before and x['date'] and
                   dt.date.fromisoformat(x['date'][:10]) < p_ref - dt.timedelta(days=31))
    # Tous les cas sont publiés agence par agence ; le seuil (5 avis, ou 1 pour l'éditeur) ne fixe que la gravité
    def sev(c):
        return 'majeur' if any(n >= 5 for n in c.values()) or any(c.get(p) for p in publisher) else 'info'
    out.append(finding('V-13a', sev(back), 'avis apparus depuis le relevé précédent avec une date antérieure de plus '
                       'd’un mois, sur une plateforme déjà relevée en entier', list(back), sum(back.values()),
                       per_agency=dict(back), publisher_counts={p: back.get(p, 0) for p in publisher}))
    # une agence retirée du classement emporte ses avis : ce n'est pas une disparition d'avis chez une agence classée,
    # mais un changement de périmètre, publié à part (agences retirées et nombre d'avis concernés)
    cur_ag = {r['agence'] for r in read_csv(data_dir / 'agences.csv')}
    prev_ag = {r['agence'] for r in read_csv(prev_dir / 'agences.csv')}
    removed = Counter(k[0] for k in prev_keys - cur_keys if k[0] not in cur_ag)
    gone = Counter(k[0] for k in prev_keys - cur_keys if k[0] in cur_ag)
    out.append(finding('V-13b', sev(gone), 'avis disparus depuis le relevé précédent, chez des agences toujours classées',
                       list(gone), sum(gone.values()), per_agency=dict(gone), publisher_counts={p: gone.get(p, 0) for p in publisher}))
    left = sorted(prev_ag - cur_ag)
    out.append(finding('V-13e', 'majeur' if any(p in left for p in publisher) else 'info',
                       'agences retirées du classement depuis le relevé précédent (leurs avis sortent avec elles)', left, len(left),
                       per_agency={a: removed.get(a, 0) for a in left}, publisher_counts={p: int(p in left) for p in publisher}))
    # V-13d : même avis (même identifiant), classement modifié : note, profil, problème, drapeaux de comptage
    fields = ('note', 'profil', 'probleme', 'compte_vente_achat', 'retenu_qualite', 'retenu_service', 'nb_agences_partageant')
    pmap = {(x['agence'], x['plateforme'], x['id']): x for x in prev}
    changed_cls = Counter()
    kinds = Counter()
    for x in cur:
        o = pmap.get((x['agence'], x['plateforme'], x['id']))
        if o:
            diff = [f for f in fields if o.get(f) != x.get(f)]
            if diff:
                changed_cls[x['agence']] += 1
                kinds.update(diff)
    out.append(finding('V-13d', sev(changed_cls), 'avis déjà relevés dont la note, le profil, le problème signalé ou '
                       'les drapeaux de comptage ont changé depuis le relevé précédent', list(changed_cls),
                       sum(changed_cls.values()), per_agency=dict(changed_cls), fields=dict(kinds),
                       publisher_counts={p: changed_cls.get(p, 0) for p in publisher}))
    pc = {(r['agence'], r['critere']): r for r in read_csv(prev_dir / 'criteres-sites.csv')}
    # une nouvelle lecture se reconnaît à une nouvelle date ou, pour deux lectures le même jour, à un nouvel identifiant
    # de relecture (colonne id_lecture, publiée par le site depuis sa v5.6)
    cases = [{'agence': r['agence'], 'critere': r['critere'], 'avant': o['points'], 'apres': r['points'],
              'date_observation': r.get('date_observation'), 'id_lecture': r.get('id_lecture') or ''}
             for r in read_csv(data_dir / 'criteres-sites.csv')
             for o in [pc.get((r['agence'], r['critere']))]
             if o and o['points'] != r['points'] and r.get('date_observation')
             and r.get('date_observation') == o.get('date_observation')
             and (r.get('id_lecture') or '') == (o.get('id_lecture') or '')]
    if cases:
        out.append(finding('V-13c', 'majeur', 'points de critère modifiés sans nouvelle date ni nouvel identifiant de lecture '
                           'du site', [c['agence'] for c in cases], len(cases), cases=cases,
                           publisher_counts={p: sum(c['agence'] == p for c in cases) for p in publisher}))
    return out

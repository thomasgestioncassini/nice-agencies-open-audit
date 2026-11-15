"""Rapport d'audit : trois dimensions, trois statuts distincts. Aucun contrôle partiel n'est présenté comme une
validation générale."""
from __future__ import annotations

import json

TITLES = {
    'calculs': 'Exactitude des calculs',
    'donnees_primaires': 'Vérification des données primaires',
    'biais': 'Analyse des biais',
}
LABELS = {
    'conforme': 'CONFORME — toutes les notes, tous les piliers et tous les rangs recalculés sont identiques aux valeurs publiées',
    'divergences': 'DIVERGENCES — au moins une valeur recalculée diffère de la valeur publiée',
    'echec': 'ÉCHEC — le contrôle n’a pas pu être mené ; ce n’est pas une validation',
    'non_execute': 'NON EXÉCUTÉ',
    'non_verifiees': 'NON VÉRIFIÉES — les données d’entrée (avis, pages des sites, registre) n’ont pas été recontrôlées à leur source',
    'non_evalue': 'NON ÉVALUÉ — aucune analyse de biais n’a été menée dans ce rapport',
}


def statuses(cmp: dict | None, val: dict | None, primary: str = 'non_verifiees', bias: str = 'non_evalue') -> dict:
    if cmp is None or (val and val.get('blocking')):
        calc = 'echec'
    elif cmp['notes']['divergente'] or cmp['ranks_divergent'] or any(a['statut'] == 'divergente' for a in cmp['anomalies']):
        calc = 'divergences'
    else:
        calc = 'conforme'
    return {'calculs': calc, 'donnees_primaires': primary, 'biais': bias}


def markdown(rep: dict) -> str:
    st = rep['statuses']
    L = [f"# Rapport d’audit {rep['report_id']}", '',
         f"Classement audité : {rep['target']} · relevé du {rep['date_releve']} · méthode {rep['method_version']}",
         f"Exécuté le {rep['generated_utc']} (UTC) · code de l’auditeur {rep['code_version']}", '',
         '> Ce dispositif est administré par SARL GESTION CASSINI, éditrice du classement et exploitante de deux agences '
         'classées. Il n’est pas une certification indépendante. Voir GOVERNANCE.md.', '',
         '## Statuts', '']
    for k, t in TITLES.items():
        L.append(f'- **{t}** : {LABELS.get(st[k], st[k])}')
    c = rep.get('calculations')
    if c:
        L += ['', '## Exactitude des calculs', '',
              f"- Agences examinées : {c['examined']}",
              f"- Notes conformes : {c['notes']['conforme']} · divergentes : {c['notes']['divergente']} · "
              f"à une frontière d’arrondi : {c['notes']['frontiere_arrondi']}",
              f"- Rangs divergents : {c['ranks_divergent']}",
              f"- Moyenne de Nice recalculée : {c['m_ref']}",
              f"- Valeurs anormales listées dans anomalies.json : {len(c['anomalies'])}", '',
              'Le recalcul utilise les données élémentaires publiées, jamais les notes finales. Il prouve que l’arithmétique '
              'du site est conforme à ses règles ; il ne prouve pas que ces données sont exactes.']
    L += ['', '## Contrôles de cohérence des données publiées', '']
    for f in rep['findings']:
        n = f" ({f['count']})" if f.get('count') is not None else ''
        L.append(f"- [{f['severity']}] {f['code']} · {f['message']}{n}")
    if rep.get('interpretations'):
        L += ['', '## Règles appliquées par le site mais absentes du texte de la méthode', '',
              'Le texte public ne suffisait pas à reproduire les notes. Ces règles ont été établies en lisant le code publié '
              'par le site (docs/interpretations.md) :', '']
        for i in rep['interpretations']:
            L.append(f"- {i['id']} · {i['title']}" + (' — **écart avec le texte publié**' if i.get('contradicts_text') else ''))
    s = rep.get('sampling')
    if s:
        L += ['', '## Agences retenues pour les contrôles à la source (phase C)', '',
              f"Graine : {s['seed']} · règle {s['rule_version']}", '']
        from collections import Counter
        for why, n in sorted(Counter(s['agencies'].values()).items()):
            L.append(f'- {why} : {n}')
    L += ['', '## Limites', '']
    L += [f'- {x}' for x in rep['limits']]
    return '\n'.join(L) + '\n'


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False) + '\n', encoding='utf-8')

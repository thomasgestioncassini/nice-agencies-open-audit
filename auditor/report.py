"""Rapport d'audit : trois dimensions, trois statuts distincts. Aucun contrôle partiel n'est présenté comme une
validation générale."""
from __future__ import annotations

import json

TITLES = {
    'calculs_reproduction': 'Calculs — reproduction des notes publiées',
    'calculs_conformite_texte': 'Calculs — conformité au texte publié de la méthode',
    'donnees_primaires': 'Vérification des données primaires',
    'biais': 'Analyse des biais',
}
LABELS = {
    'conforme': 'CONFORME',
    'ecarts': 'ÉCARTS — le site applique des règles que son texte contredit ou laisse ambiguës (détail et effet ci-dessous)',
    'incomplet': 'INCOMPLET — le texte ne suffit pas à reproduire le calcul',
    'divergences': 'DIVERGENCES — au moins une valeur recalculée diffère de la valeur publiée',
    'echec': 'ÉCHEC — le contrôle n’a pas pu être mené ; ce n’est pas une validation',
    'non_execute': 'NON EXÉCUTÉ',
    'non_verifiees': 'NON VÉRIFIÉES — les données d’entrée (avis, pages des sites, registre) n’ont pas été recontrôlées à leur source',
    'non_evalue': 'NON ÉVALUÉ — aucune analyse de biais n’a été menée dans ce rapport',
}


def statuses(cmp: dict | None, val: dict | None, textc: dict | None = None, primary: str = 'non_verifiees',
             bias: str = 'non_evalue') -> dict:
    if cmp is None or (val and val.get('blocking')):
        calc = 'echec'
    elif cmp['notes']['divergente'] or cmp['ranks_divergent'] or any(a['statut'] != 'conforme' for a in cmp['anomalies']):
        calc = 'divergences'
    else:
        calc = 'conforme'
    text = textc['status'] if textc else 'echec'
    return {'calculs_reproduction': calc, 'calculs_conformite_texte': text, 'donnees_primaires': primary, 'biais': bias}


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
    L += ['', 'Une reproduction conforme prouve que les notes publiées découlent des données publiées selon les règles '
          'appliquées par le site. Elle ne prouve ni que ces règles sont celles du texte publié, ni que les données sont '
          'exactes à leur source : si des données étaient falsifiées de façon cohérente avant leur export, le recalcul '
          'resterait conforme. Seuls les contrôles à la source (phase C) et la comparaison entre relevés (V-13) peuvent '
          'le révéler.']
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
    tc = rep.get('text_conformity')
    if rep.get('interpretations'):
        kinds = {'contradiction': 'contradiction avec le texte', 'ambiguite': 'texte ambigu', 'non_documente':
                 'règle absente du texte', 'precision': 'précision d’implémentation'}
        L += ['', '## Conformité au texte de la méthode', '',
              'Le texte public ne suffisait pas à reproduire les notes. Les règles suivantes ont été établies en lisant le '
              'code publié par le site (docs/interpretations.md) :', '']
        for i in rep['interpretations']:
            L.append(f"- {i['id']} · {i['title']} — {kinds.get(i['kind'], i['kind'])}")
        if tc:
            L += ['', 'Effet de chaque contradiction ou ambiguïté, si l’on applique la lecture littérale du texte '
                  '(diagnostic seulement, les notes officielles ne changent pas) :', '',
                  '| Règle | Notes changées | Rangs changés | Déplacement max | Top 10 inchangé | ImmoVendu | Gestion Cassini |',
                  '| --- | --- | --- | --- | --- | --- | --- |']
            for k, e in tc['effects'].items():
                a = e['agences_suivies']
                cell = lambda s: f"{a[s]['rang_production']} → {a[s]['rang_variante']}" if s in a else '—'
                L.append(f"| {k} | {e['notes_changees']} | {e['rangs_changes']} | {e['deplacement_max']} | "
                         f"{e['top10_inchanges']}/10 | {cell('immovendu')} | {cell('gestion-cassini')} |")
    s = rep.get('sampling')
    if s:
        L += ['', '## Agences retenues pour les contrôles à la source (phase C)', '']
        if s['status'] == 'tire':
            L += [f"Graine : {s['seed']} · règle {s['rule_version']} · tour drand {s['drand']['round']} "
                  '(cohérence de la balise vérifiée ; signature BLS non vérifiée cryptographiquement)', '']
            from collections import Counter
            for why, n in sorted(Counter(s['agencies'].values()).items()):
                L.append(f'- {why} : {n}')
        elif s['status'] == 'en_attente':
            L.append(f"Tirage en attente : échéance fixe {s['planned']['utc']}, tour drand {s['planned']['drand_round']}. "
                     'Aucun échantillon n’est publié avant.')
        else:
            L.append('Tirage en échec : ' + '; '.join(s.get('errors', [])) + '. Aucun échantillon n’est publié.')
    L += ['', '## Limites', '']
    L += [f'- {x}' for x in rep['limits']]
    return '\n'.join(L) + '\n'


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False) + '\n', encoding='utf-8')

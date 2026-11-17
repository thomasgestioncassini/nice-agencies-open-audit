"""Rapport d'audit : trois dimensions, trois statuts distincts. Aucun contrôle partiel n'est présenté comme une
validation générale."""
from __future__ import annotations

import json

TITLES = {
    'calculs_reproduction': 'Calculs — reproduction des notes publiées',
    'texte_documentation': 'Texte de la méthode — règles de calcul décrites',
    'texte_coherence': 'Texte de la méthode — contradictions répertoriées encore présentes',
    'texte_historique': 'Texte de la méthode — écarts dans les versions archivées antérieures',
    'donnees_primaires': 'Vérification des données primaires',
    'biais': 'Analyse des biais',
    'dedoublonnage': 'Dédoublonnage des avis — refait indépendamment sur les données anonymisées',
    'audit_ia': 'Audit contradictoire par deux IA',
}
LABELS = {
    'conforme': 'CONFORME',
    'ecarts': 'ÉCARTS — le site applique des règles que son texte contredit ou laisse ambiguës (détail et effet ci-dessous)',
    'complete': 'OUI — chaque règle répertoriée est décrite dans le texte archivé avec ce relevé',
    'partielle': 'PARTIELLEMENT — des règles appliquées ne sont pas décrites, ou contredites, dans le texte archivé',
    'contradictions_residuelles': 'OUI — le texte affirme encore une règle contraire au calcul',
    'aucune_contradiction_repertoriee': 'AUCUNE parmi celles répertoriées (contrôle par phrases, pas une relecture complète du texte)',
    'ecarts_anterieurs': 'OUI — le calcul appliqué contredisait ou dépassait le texte publié dans au moins une version archivée antérieure ; ces écarts restent publiés ci-dessous',
    'aucun_ecart_anterieur': 'AUCUN dans les versions archivées antérieures',
    'divergences': 'DIVERGENCES — au moins une valeur recalculée diffère de la valeur publiée',
    'echec': 'ÉCHEC — le contrôle n’a pas pu être mené ; ce n’est pas une validation',
    'non_execute': 'NON EXÉCUTÉ',
    'non_verifie': 'NON VÉRIFIÉ — données anonymisées absentes de ce relevé',
    'non_verifiees': 'NON VÉRIFIÉES — les données d’entrée (avis, pages des sites, registre) n’ont pas été recontrôlées à leur source',
    'non_evalue': 'NON ÉVALUÉ — aucune analyse de biais n’a été menée dans ce rapport',
    'partiellement_verifiees': 'PARTIELLEMENT — dates de création des sociétés comparées au registre national et barèmes '
                               'd’honoraires relus pour les agences tirées ; les avis ne sont pas revérifiés sur les plateformes',
    'analyse_publiee': 'ANALYSE PUBLIÉE — tests contrefactuels sans IA et analyses des deux IA ci-dessous (diagnostic, '
                       'les notes officielles ne changent pas)',
    'complet': 'COMPLET — les deux IA ont rendu leur analyse',
    'incomplet': 'INCOMPLET — une seule IA a rendu son analyse ; aucune seconde validation n’est inventée',
}


def statuses(cmp: dict | None, val: dict | None, textc: dict | None = None, primary: str = 'non_verifiees',
             bias: str = 'non_evalue') -> dict:
    if cmp is None or (val and val.get('blocking')):
        calc = 'echec'
    elif cmp['notes']['divergente'] or cmp['ranks_divergent'] or any(a['statut'] != 'conforme' for a in cmp['anomalies']):
        calc = 'divergences'
    else:
        calc = 'conforme'
    t = textc or {'documentation': 'echec', 'coherence': 'echec', 'history': 'echec'}
    return {'calculs_reproduction': calc, 'texte_documentation': t['documentation'], 'texte_coherence': t['coherence'],
            'texte_historique': t['history'], 'donnees_primaires': primary, 'biais': bias}


def markdown(rep: dict) -> str:
    st = rep['statuses']
    L = [f"# Rapport d’audit {rep['report_id']}", '',
         f"Classement audité : {rep['target']} · relevé du {rep['date_releve']} · méthode {rep['method_version']}",
         f"Exécuté le {rep['generated_utc']} (UTC) · code de l’auditeur {rep['code_version']}", '',
         '> Ce dispositif est administré par SARL GESTION CASSINI, éditrice du classement et exploitante de deux agences '
         'classées. Il n’est pas une certification indépendante. Voir GOVERNANCE.md.', '',
         '## Statuts', '']
    for k, t in TITLES.items():
        if k in st:
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
    dd = rep.get('dedup')
    if dd and dd.get('status') != 'non_verifie':
        L += ['', '## Dédoublonnage des avis (V-14)', '',
              f"Refait par l’auditeur, avec sa propre implémentation de la règle I-13, sur le paquet de données anonymisées "
              f"publié par le site (aucun script du paquet n’est exécuté), pour {dd['agences']} agences ayant des avis relevés "
              f"un par un ; {dd['avis_partages_cles']} avis publiés sur les fiches de plusieurs agences.", '',
              f"- Avis uniques retenus pour la qualité : {len(dd['ecarts_qualite'])} agence(s) en écart",
              f"- Avis uniques retenus pour le service : {len(dd['ecarts_service'])} agence(s) en écart",
              f"- Répartition des avis partagés entre agences : {len(dd['ecarts_partage'])} agence(s) en écart",
              f"- Agences classées sans données anonymisées : {len(dd['sans_donnees_anonymisees'])}", '',
              'La comparaison se fait agence par agence, en nombres : les identifiants d’avis sont salés dans le paquet.']
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
        doc = set(tc['current'].get('documented', [])) if tc else set()
        for i in rep['interpretations']:
            k = kinds.get(i['kind'], i['kind'])
            L.append(f"- {i['id']} · {i['title']} — " + (f'désormais décrite dans le texte archivé (à l’origine : {k})'
                                                        if i['id'] in doc else k))
        if tc and tc['past']:
            L += ['', '**Écarts dans les versions antérieures du texte (conservés) :**', '']
            for p in tc['past']:
                L.append(f"- relevé {p['snapshot']} : contradictions {', '.join(p['contradictions']) or 'aucune'} ; "
                         f"ambiguïtés {', '.join(p['ambiguities']) or 'aucune'}")
            L += ['', 'Compléter le texte après coup est une révision de la méthode publiée : elle ne rend pas conformes '
                  'les relevés publiés avant elle.']
        if tc:
            L += ['', 'Effet des règles retenues par le site par rapport à la lecture littérale du texte initial (v5 du '
                  '14/11/2026). Ce tableau reste publié même quand le texte décrit la règle : il montre ce que ce choix '
                  'change (diagnostic seulement, les notes officielles ne changent pas) :', '',
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
                  '(signature BLS de la balise vérifiée avec la clé publique du réseau drand)', '']
            from collections import Counter
            for why, n in sorted(Counter(s['agencies'].values()).items()):
                L.append(f'- {why} : {n}')
        elif s['status'] == 'non_engage':
            L.append(f"Ce relevé n’est pas celui engagé pour le tirage (relevé engagé : {s['committed_snapshot'] or 'aucun'}).")
        elif s['status'] == 'en_attente':
            L.append(f"Tirage en attente : échéance fixe {s['planned']['utc']}, tour drand {s['planned']['drand_round']}. "
                     'Aucun échantillon n’est publié avant.')
        else:
            L.append('Tirage en échec : ' + '; '.join(s.get('errors', [])) + '. Aucun échantillon n’est publié.')
    ai = rep.get('ai_audit')
    if ai:
        L += ['', '## Audit contradictoire par deux IA', '',
              f"Paquet de données identique pour les deux IA, empreinte {ai['package_sha256']} ({ai['package_chars']} caractères).", '']
        for slot in ('A', 'B'):
            m = ai['models'][slot]
            L.append(f"- IA {slot} · {m['provider']} · {m.get('model') or m['model_requested']} · statut **{m['status']}**"
                     + (f" · {m['usd']} $" if m.get('usd') is not None else '') + (f" · {m['error']}" if m.get('error') else ''))
        L += ['', f"Confrontation : A {ai['cross_status']['A']}, B {ai['cross_status']['B']} · constats confirmés par "
                  f"l’autre IA : {ai['reconcile'].get('confirmes', 0)} · contestés : {ai['reconcile'].get('contestes', 0)} · "
                  f"à soumettre à un contrôle humain : {ai['reconcile'].get('controle_humain', 0)}",
              f"Textes ressemblant à des consignes repérés dans les données : {ai['injections_detected']} (injections.json)",
              f"Registre des entreprises : {ai['primary']['registre']} · barèmes : {ai['primary']['baremes']}",
              f"Coût total des appels d’IA : {ai['cost_usd']} $", '',
              'Analyses complètes : agent-a.md, agent-b.md ; confrontation : disagreements.md ; tests de biais : bias.json.']
    L += ['', '## Limites', '']
    L += [f'- {x}' for x in rep['limits']]
    return '\n'.join(L) + '\n'


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False) + '\n', encoding='utf-8')

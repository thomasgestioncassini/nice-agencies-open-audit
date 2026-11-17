"""Phase C : audit contradictoire par deux IA, appuyé sur les contrôles déterministes et des contrôles à la source.

Ordre, fixé et publié :
1. contrôles sans IA (recalcul, cohérence, texte, biais, registre, barèmes) ;
2. audit A (OpenAI) et audit B (Google), lancés ENSEMBLE sur le même paquet, sans accès l'un à l'autre ;
3. leurs sorties sont écrites et horodatées ;
4. confrontation : chaque IA donne sa position sur les constats de l'autre, sans modifier les siens ;
5. publication sans relecture. Une IA en panne ou hors budget est publiée comme telle.
"""
from __future__ import annotations

import concurrent.futures as cf
import datetime as dt
import hashlib
import json
from pathlib import Path

from . import agents as AG
from .bias import bias_tests
from .budget import Ledger
from .registry import check_registry
from .sitecheck import check_sites, public_view

TASK_AUDIT = ('Réalise l’audit défini par ton mandat sur le paquet de données ci-dessous. Donne au plus 25 constats, '
              'classés du plus grave au moins grave, avec des identifiants uniques commençant par ta lettre (A-1, A-2… ou '
              'B-1, B-2…).')
TASK_CROSS = ('Le paquet contient en plus, dans « constats_autre_auditeur », les constats d’un autre auditeur IA. Pour '
              'CHACUN, donne ta position (confirme, conteste, ne_peut_juger) et une justification fondée sur les données. '
              'Tu ne modifies pas tes propres constats.')


def build_package(ctx: dict, max_site_text: int = 6000) -> dict:
    pub = ctx['publisher']
    rec = ctx['recalc']['agencies']
    return {
        'classement': {'site': 'https://meilleure-agence-nice.fr', 'date_releve': ctx['date_releve'],
                       'methode': {'version': ctx['cfg']['version'], 'poids': ctx['cfg']['weights'],
                                   'nombre_criteres': ctx['cfg']['criteria_count'], 'texte_public': ctx['cfg']['source']},
                       'agences_classees': len(rec), 'editeur': 'SARL GESTION CASSINI', 'agences_editeur': pub},
        'resultats_deterministes': {
            'statuts': ctx['statuses'], 'recalcul': ctx['calc_summary'], 'controles': ctx['findings'],
            'regles_appliquees_absentes_ou_contraires_au_texte': ctx['interpretations'],
            'effet_des_regles_vs_texte_initial': ctx['text_effects']},
        'agences_editeur': {s: {'rang': rec[s]['rank'], 'note': round(rec[s]['note_exact'], 2),
                                'piliers': rec[s]['pillars'], 'sources': ctx['sources'].get(s, {})} for s in pub if s in rec},
        'tests_biais': ctx['bias'],
        'registre_entreprises': ctx['registry'],
        'baremes_relus': [{**{k: v for k, v in r.items() if k != 'text'},
                           **({'texte_page': r['text'][:max_site_text]} if r.get('text') else {})}
                          for r in ctx['sites']['rows']],
        'echantillon': ctx['sampling'],
    }


def _md_agent(name: str, res: dict) -> str:
    L = [f'# Analyse initiale — IA {name}', '',
         f"Fournisseur : {res.get('provider')} · modèle : {res.get('model', res.get('model_requested'))} · statut : "
         f"**{res['status']}**", f"Empreinte du mandat : {res.get('mandate_sha256')} · empreinte de l’entrée : "
         f"{res.get('input_sha256')}", f"Coût : {res.get('usd', 0)} $ ({res.get('tokens_in', 0)} jetons lus, "
         f"{res.get('tokens_out', 0)} écrits)", '',
         '> Texte produit par l’IA, publié sans aucune modification ni relecture de l’éditeur.', '']
    out = res.get('output')
    if not out:
        return '\n'.join(L + [f"Aucune analyse : {res.get('error', res['status'])}", ''])
    L += ['## Résumé', '', out.get('resume', ''), '', '## Constats', '']
    for c in out.get('constats', []):
        L += [f"### {c['id']} · {c['titre']}", '',
              f"Catégorie : {c['categorie']} · nature : {c['nature']} · gravité : {c['gravite']} · concerne l’éditeur : "
              f"{'oui' if c['concerne_editeur'] else 'non'}", '', c.get('detail', ''), '',
              'Preuves : ' + ' ; '.join(c.get('preuves', [])), '', f"Incertitude : {c.get('incertitude', '')}", '']
    for t, k in (('Points favorables au classement', 'points_favorables_au_classement'),
                 ('Points défavorables au classement', 'points_defavorables_au_classement'),
                 ('Instructions suspectes repérées dans les données', 'instructions_suspectes'), ('Limites', 'limites')):
        L += [f'## {t}', ''] + [f'- {x}' for x in out.get(k, [])] + ['']
    return '\n'.join(L)


def _md_disagreements(rec: dict) -> str:
    L = ['# Confrontation des deux IA', '',
         'Chaque IA a donné sa position sur les constats de l’autre APRÈS avoir rendu sa propre analyse. Aucun constat '
         'n’a été fusionné, modifié ou supprimé. Il n’y a pas d’obligation de consensus.', '',
         '| Auteur | Constat | Gravité | Éditeur | Position de l’autre IA | Justification |', '| --- | --- | --- | --- | --- | --- |']
    for r in rec['rows']:
        j = r['justification_autre_ia'].replace('|', '/').replace('\n', ' ')
        L.append(f"| {r['auteur']} | {r['id']} · {r['titre'].replace('|', '/')} | {r['gravite']} | "
                 f"{'oui' if r['concerne_editeur'] else 'non'} | {r['position_autre_ia']} | {j} |")
    L += ['', f"Confirmés par l’autre IA : {len(rec['confirmes'])} · contestés : {len(rec['contestes'])} · "
              f"à soumettre à un contrôle humain : {len(rec['controle_humain'])}", '']
    for r in rec['controle_humain']:
        L.append(f"- {r['id']} ({r['auteur']}) · {r['titre']}")
    return '\n'.join(L) + '\n'


def run(ctx: dict, out: Path, models: dict, mandate: str, ledger: Ledger, report_id: str, callers: dict | None = None,
        registry_get=None, site_fetcher=None) -> dict:
    callers = callers or {}
    sample = (ctx['sampling'] or {}).get('agencies', {})
    pub = ctx['publisher']
    to_registry = sorted(sample) if sample else pub
    to_sites = sorted(s for s, why in sample.items() if why != 'anciennete_comparable') if sample else pub
    ctx['registry'] = check_registry(ctx['sources'], to_registry, registry_get, pause=0 if registry_get else 0.2)
    ctx['sites'] = check_sites(ctx['sources'], ctx['criteria'], to_sites, **({'fetcher': site_fetcher} if site_fetcher else {}))
    neighbours = [s for s, why in sample.items() if why.startswith('voisine')]
    ctx['bias'] = bias_tests(ctx['recalc'], ctx['cfg']['weights'], ctx['sources'], pub, neighbours, ctx['date_releve'])
    package = build_package(ctx)
    injections = AG.scan_injections(package)
    pkg_json = json.dumps(package, ensure_ascii=False, sort_keys=True)
    started = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    # 2. Audits A et B en parallèle, chacun ignorant l'autre
    with cf.ThreadPoolExecutor(2) as ex:
        fut = {slot: ex.submit(AG.run_agent, slot, models, mandate, TASK_AUDIT, package, AG.FINDING_SCHEMA, 'audit',
                               ledger, report_id, 'audit', callers.get(slot)) for slot in ('A', 'B')}
        res = {slot: f.result() for slot, f in fut.items()}
    for slot in ('A', 'B'):
        res[slot]['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
        (out / f'agent-{slot.lower()}.json').write_text(json.dumps(res[slot], ensure_ascii=False, indent=1), encoding='utf-8')
        (out / f'agent-{slot.lower()}.md').write_text(_md_agent(slot, res[slot]), encoding='utf-8')
    # 4. Confrontation (seulement si les deux analyses existent)
    cross = {'A': None, 'B': None}
    if res['A']['status'] == 'ok' and res['B']['status'] == 'ok':
        with cf.ThreadPoolExecutor(2) as ex:
            fut = {}
            for slot, other in (('A', 'B'), ('B', 'A')):
                pk = {**package, 'constats_autre_auditeur': res[other]['output']['constats']}
                fut[slot] = ex.submit(AG.run_agent, slot, models, mandate, TASK_CROSS, pk, AG.CROSS_SCHEMA, 'confrontation',
                                      ledger, report_id, 'confrontation', callers.get(slot + '_cross', callers.get(slot)))
            cross = {slot: f.result() for slot, f in fut.items()}
        for slot in ('A', 'B'):
            (out / f'cross-{slot.lower()}.json').write_text(json.dumps(cross[slot], ensure_ascii=False, indent=1), encoding='utf-8')
    rec = AG.reconcile(res['A'], res['B'], cross['A'], cross['B'])
    (out / 'disagreements.md').write_text(_md_disagreements(rec), encoding='utf-8')
    for name, obj in (('bias.json', ctx['bias']), ('registry.json', ctx['registry']), ('sites.json', public_view(ctx['sites'])),
                      ('injections.json', injections)):
        (out / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding='utf-8')
    public_pkg = build_package(ctx, max_site_text=0)
    (out / 'package-public.json').write_text(json.dumps(public_pkg, ensure_ascii=False, indent=1), encoding='utf-8')
    reg_checked = sum(1 for r in ctx['registry']['rows'] if r['statut'] not in ('siren_non_publie', 'registre_injoignable'))
    sites_read = ctx['sites']['counts'].get('lu', 0)
    ia_ok = [s for s in ('A', 'B') if res[s]['status'] == 'ok']
    return {
        'started_utc': started, 'models': {s: {k: res[s].get(k) for k in ('provider', 'model_requested', 'model', 'status',
                                                                          'usd', 'tokens_in', 'tokens_out', 'error')}
                                           for s in ('A', 'B')},
        'cross_status': {s: (cross[s] or {}).get('status', 'non_execute') for s in ('A', 'B')},
        'package_sha256': hashlib.sha256(pkg_json.encode()).hexdigest(), 'package_chars': len(pkg_json),
        'injections_detected': len(injections), 'reconcile': {k: len(v) for k, v in rec.items() if k != 'rows'},
        'primary': {'registre_verifie': reg_checked, 'registre': ctx['registry']['counts'],
                    'baremes_lus': sites_read, 'baremes': ctx['sites']['counts']},
        'ai_status': 'complet' if len(ia_ok) == 2 else ('incomplet' if ia_ok else 'echec'),
        'cost_usd': round(sum((res[s].get('usd') or 0) + ((cross[s] or {}).get('usd') or 0) for s in ('A', 'B')), 4),
    }

"""Point d'entrée de l'auditeur.

  python -m auditor fetch                       télécharge et archive le relevé publié (snapshots/<date>/)
  python -m auditor run snapshots/<date>        recalcule un relevé archivé et écrit reports/<id>/
  python -m auditor verify reports/<id>         vérifie les empreintes d'un rapport et de son relevé
  python -m auditor draw snapshots/<date>       enregistre la balise drand du tour fixé à l'archivage (réseau)

Aucune commande n'appelle d'IA. « run » n'utilise pas le réseau.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from . import fetch as F
from .compare import compare
from .recalculate import read_csv, recalculate
from .report import dump, markdown, statuses
import os

from .commitment import engagements_from_github, evaluate
from .sampling import check_beacon, choose_committed, draw_deadline, fetch_beacon, round_at, seed_of, select
from .textcheck import text_conformity
from .validate import validate

ROOT = Path(__file__).resolve().parent.parent
TARGET = 'https://meilleure-agence-nice.fr'
LIMITS = [
    'Le recalcul reprend tels quels les résultats d’étapes que les exports ne permettent pas de refaire : profil de '
    'l’auteur et problème signalé (lus par une IA du site), points attribués en lisant les sites des agences, date de '
    'création des sociétés. Le dédoublonnage est refait (V-14), mais sur des empreintes produites par le site : il ne '
    'prouve pas que ces empreintes correspondent aux avis réellement publiés sur les plateformes.',
    'Un statut « conforme » vaut pour la dimension qu’il nomme, jamais pour le classement entier. Ce rapport n’est pas '
    'une certification du classement (docs/portee-et-limites.md).',
    'Les écarts entre catégories d’agences (tests de biais) sont descriptifs et non ajustés : ils ne prouvent ni une '
    'discrimination, ni son absence.',
    'Les arbitrages des constats contestés sont rendus par l’éditeur, partie intéressée (docs/arbitrages-phase-c.md) : '
    'ils ne valent pas validation indépendante.',
    'Les données primaires (avis sur les plateformes, pages des sites, registre des entreprises) ne sont pas recontrôlées '
    'à leur source dans ce rapport.',
    'Le moteur a été écrit par Claude (Anthropic), qui a aussi écrit le code de production du site. Il a été rédigé à '
    'partir du texte de la méthode, puis complété en lisant le code publié (docs/interpretations.md). Un tiers peut '
    'écrire et exécuter son propre moteur à partir des mêmes fichiers archivés.',
    'Le dépôt, ses workflows et son financement sont contrôlés par SARL GESTION CASSINI (GOVERNANCE.md).',
]


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def code_version() -> str:
    try:
        rev = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        dirty = subprocess.run(['git', 'status', '--porcelain', '--', 'auditor', 'config'], cwd=ROOT, capture_output=True,
                               text=True).stdout.strip()
        return rev + ('-modifie' if dirty else '')
    except Exception:                         # noqa: BLE001
        return 'inconnue'


def cmd_fetch(args) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        got = F.fetch(tmp, args.base)
        required_missing = [e for e in got['errors'] if e['file'] not in F.OPTIONAL]
        params = json.loads((tmp / 'inputs' / 'parametres.json').read_text(encoding='utf-8')) if (tmp / 'inputs' / 'parametres.json').exists() else {}
        date = params.get('date_releve', dt.date.today().isoformat())
        snap = ROOT / 'snapshots' / date
        if snap.exists():
            old = json.loads((snap / 'manifest.json').read_text(encoding='utf-8'))
            same = all(old['inputs'].get(n, {}).get('sha256') == v['sha256'] for n, v in got['files'].items())
            if same:
                print(f'relevé {date} déjà archivé à l’identique : {snap}')
                return 0
            # tout changement, y compris du seul texte de la méthode, crée un nouveau relevé archivé
            snap = ROOT / 'snapshots' / f"{date}_{got['started_utc'][11:19].replace(':', '')}"
        archived = F.archive(tmp / 'inputs', snap)
        archived_at = time.time()
        dts = draw_deadline(date)
        run = os.environ.get('GITHUB_RUN_ID')
        manifest = {'date_releve': date, 'fetch': got, 'inputs': archived, 'archived_utc':
                    dt.datetime.fromtimestamp(archived_at, dt.timezone.utc).isoformat(timespec='seconds'),
                    'draw_planned': {'utc': dt.datetime.fromtimestamp(dts, dt.timezone.utc).isoformat(timespec='seconds'),
                                     'drand_round': round_at(dts), 'rule': 'premier mardi 06:00 UTC après la date du relevé'},
                    'archive_run': ({'id': run, 'url': f"{os.environ.get('GITHUB_SERVER_URL')}/"
                                     f"{os.environ.get('GITHUB_REPOSITORY')}/actions/runs/{run}"} if run else None),
                    'auditor_code': code_version()}
        dump(snap / 'manifest.json', manifest)
        commit = F.sha256(snap / 'manifest.json')
        line = f'ENGAGEMENT relevé {snap.name} · SHA-256 du manifeste {commit} · archivé {manifest["archived_utc"]}'
        print(line)                           # journal d'exécution GitHub, horodaté par GitHub
        if os.environ.get('GITHUB_STEP_SUMMARY'):
            with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as f:
                f.write(line + '\n\n')
        print(f'archivé : {snap} ({len(archived)} fichiers, {len(got["errors"])} erreur(s))')
        return 1 if required_missing else 0


def all_manifests() -> list[dict]:
    out = []
    for p in sorted((ROOT / 'snapshots').glob('*/manifest.json')):
        m = json.loads(p.read_text(encoding='utf-8'))
        m['_dir'] = p.parent
        out.append(m)
    return out


def planned_draw(snap_manifest: dict) -> dict:
    d = draw_deadline(snap_manifest['date_releve'])
    return {'utc': dt.datetime.fromtimestamp(d, dt.timezone.utc).isoformat(timespec='seconds'), 'drand_round': round_at(d),
            'rule': 'premier mardi 06:00 UTC après la date du relevé'}


def cmd_draw(args) -> int:
    """Tirage d'un relevé daté : vérifie auprès de GitHub l'engagement de chaque relevé archivé pour cette date, retient
    le relevé engagé, récupère et authentifie la balise drand du tour fixé, écrit draw.json dans le relevé engagé."""
    snap = Path(args.snapshot).resolve()
    man = json.loads((snap / 'manifest.json').read_text(encoding='utf-8'))
    date, plan = man['date_releve'], planned_draw(man)
    deadline = dt.datetime.fromisoformat(plan['utc']).timestamp()
    if time.time() < deadline:
        print(f"tirage pas encore possible : échéance {plan['utc']} (tour {plan['drand_round']})")
        return 4
    # 1. Les candidats viennent de GitHub (toutes les exécutions d'archivage réussies avant l'échéance), pas du dépôt
    try:
        engaged = engagements_from_github(date, deadline)
    except Exception as e:                    # noqa: BLE001 — sans liste GitHub, pas de tirage
        print(f'liste des engagements GitHub indisponible ({type(e).__name__}: {e}) : pas de tirage')
        return 6
    local = {m['_dir'].name: F.sha256(m['_dir'] / 'manifest.json') for m in all_manifests() if m['date_releve'] == date}
    candidates, refusal = evaluate(engaged, local, deadline)
    if refusal:
        dump(snap / 'draw-refus.json', {'planned': plan, 'candidates': candidates, 'refusal': refusal})
        print('tirage refusé : ' + refusal)
        return 7
    chosen = choose_committed(candidates)
    for n, c in candidates.items():
        print(f"{n} : {'engagement prouvé' if not c['errors'] else '; '.join(c['errors'])}")
    if chosen is None:
        print('aucun relevé engagé : pas de tirage')
        return 6
    b = fetch_beacon(plan['drand_round'])
    errs = check_beacon(b, plan['drand_round'])
    dump(ROOT / 'snapshots' / chosen / 'draw.json', {
        'planned': plan, 'committed_snapshot': chosen, 'candidates': candidates, 'beacon': b,
        'checks_errors': errs, 'bls_signature_verified': not errs})
    print(f'relevé engagé : {chosen} · ' + ('balise authentifiée' if not errs else 'balise REFUSÉE : ' + '; '.join(errs)))
    return 0 if not errs else 5


def previous_snapshot(snap: Path):
    prev = sorted(p for p in snap.parent.iterdir() if p.is_dir() and (p / 'manifest.json').exists() and p.name < snap.name)
    return prev[-1] if prev else None


def cmd_run(args) -> int:
    snap = Path(args.snapshot).resolve()
    cfg = json.loads((ROOT / 'config' / 'methodology-v5.json').read_text(encoding='utf-8'))
    policy = json.loads((ROOT / 'config' / 'audit-policy.json').read_text(encoding='utf-8'))
    interp = json.loads((ROOT / 'config' / 'interpretations.json').read_text(encoding='utf-8'))
    generated = dt.datetime.now(dt.timezone.utc)
    with tempfile.TemporaryDirectory() as tmp:
        data = Path(tmp)
        snap_manifest = F.restore(snap, data)
        publisher = policy['sampling']['publisher_agencies']
        prev = previous_snapshot(snap)
        prev_dir = None
        if prev:
            prev_dir = data.parent / (data.name + '_precedent')
            F.restore(prev, prev_dir)
        val = validate(data, cfg, publisher, prev_dir)
        cmp_ = res = textc = None
        error = None
        if not val['blocking']:
            try:
                res = recalculate(data, cfg)
                cmp_ = compare(data, res, policy)
                cmp_['m_ref'] = res['m_ref']
                hist = []
                for m in all_manifests():
                    if m['archived_utc'] < snap_manifest['archived_utc'] and 'methode-details.html' in m['inputs']:
                        hp = data.parent / f"{data.name}_texte_{m['_dir'].name}.html"
                        import gzip
                        hp.write_bytes(gzip.open(m['_dir'] / m['inputs']['methode-details.html']['archive']).read())
                        hist.append((m['_dir'].name, hp))
                textc = text_conformity(data, cfg, interp, publisher, hist)
            except Exception as e:            # noqa: BLE001 — un calcul en échec donne un statut « echec »
                error = f'{type(e).__name__}: {e}'
        sources = {r['agence']: r for r in read_csv(data / 'sources-agences.csv')} if (data / 'sources-agences.csv').exists() else {}
        plan = planned_draw(snap_manifest)
        sampling = {'status': 'en_attente', 'planned': plan}
        draw_file = snap / 'draw.json'
        sibling = [m for m in all_manifests() if m['date_releve'] == snap_manifest['date_releve']
                   and (m['_dir'] / 'draw.json').exists() and m['_dir'].resolve() != snap]
        if sibling:
            sampling.update(status='non_engage', committed_snapshot=sibling[0]['_dir'].name)
        elif draw_file.exists():
            draw = json.loads(draw_file.read_text(encoding='utf-8'))
            sampling['committed_snapshot'] = draw['committed_snapshot']
            sampling['commitment'] = (draw['candidates'][draw['committed_snapshot']]['proof'] or {}).get('html_url')
            # rejoué hors ligne : la signature BLS est revérifiée si py_ecc est installé
            errs = check_beacon(draw['beacon'], plan['drand_round'], require_bls=False)
            from .drandverify import verify
            sampling['bls_reverified'] = verify(draw['beacon']['round'], draw['beacon']['signature'])
            if sampling['bls_reverified'] is False:
                errs.append('signature BLS invalide')
            if errs:
                sampling.update(status='echec', errors=errs)
            else:
                seed = seed_of({n: v['sha256'] for n, v in snap_manifest['inputs'].items()}, draw['beacon'])
                sampling.update(select(read_csv(data / 'agences.csv'), sources, policy, seed), status='tire',
                                drand={k: draw['beacon'][k] for k in ('round', 'url')},
                                bls_signature_verified_at_draw=draw.get('bls_signature_verified'))
        reg_none = [s for s, r in (res or {}).get('agencies', {}).items() if r['detail']['avis']['regularity'] is None]
        st = statuses(cmp_, val, textc)
        from .dedupcheck import check as dedup_check
        try:
            dedup = dedup_check(data)
        except Exception as e:                # noqa: BLE001
            dedup = {'status': 'echec', 'error': f'{type(e).__name__}: {e}'}
        st['dedoublonnage'] = {'conforme': 'conforme', 'ecarts': 'divergences'}.get(dedup['status'], dedup['status'])
        if dedup['status'] in ('conforme', 'ecarts'):
            bad = sorted({r['agence'] for k in ('ecarts_qualite', 'ecarts_service', 'ecarts_partage') for r in dedup[k]}
                         | set(dedup['sans_donnees_anonymisees']))
            val['findings'].append({'code': 'V-14', 'severity': 'majeur' if bad else 'info',
                                    'message': 'agences dont le dédoublonnage des avis, refait par l’auditeur, diffère des '
                                               'fichiers publiés', 'agencies': bad[:50], 'count': len(bad),
                                    'publisher_counts': {p: int(p in bad) for p in publisher}})
        rid = f"{snap_manifest['date_releve']}_{generated.strftime('%Y%m%dT%H%M%SZ')}"
        out = ROOT / 'reports' / rid if not args.out else Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        ai = None
        if getattr(args, 'ia', False) and res is not None:
            from . import aiaudit
            from .budget import Ledger
            models = json.loads((ROOT / 'config' / 'ai-models.json').read_text(encoding='utf-8'))
            mandate = (ROOT / 'config' / 'mandate-v1.md').read_text(encoding='utf-8')
            crit = {}
            for r in read_csv(data / 'criteres-sites.csv'):
                crit.setdefault(r['agence'], []).append({**r, 'date_observation': r.get('date_observation', '')})
            ctx = {'recalc': res, 'cfg': cfg, 'publisher': publisher, 'date_releve': snap_manifest['date_releve'],
                   'sources': sources, 'criteria': crit, 'sampling': sampling if sampling.get('status') == 'tire' else None,
                   'statuses': st, 'findings': val['findings'], 'interpretations': interp,
                   'calc_summary': {k: v for k, v in cmp_.items() if k in ('examined', 'notes', 'ranks_divergent', 'm_ref')},
                   'text_effects': (textc or {}).get('effects'), 'data_dir': data,
                   'networks': json.loads((ROOT / 'config' / 'networks.json').read_text(encoding='utf-8'))['patterns']}
            ai = aiaudit.run(ctx, out, models, mandate, Ledger(ROOT, models), rid)
            prim = ai['primary']
            st['donnees_primaires'] = 'partiellement_verifiees' if prim['registre_verifie'] or prim['baremes_lus'] else 'non_verifiees'
            st['biais'] = 'analyse_publiee'
            st['audit_ia'] = ai['ai_status']
    findings = val['findings'] + ([{'code': 'I-6', 'severity': 'info', 'message': 'agences dont la régularité est '
                                    'retirée et son poids redistribué (règle I-6)', 'agencies': reg_none[:50],
                                    'count': len(reg_none)}] if res else [])
    rep = {
        'report_id': rid, 'phase': 'C — audit contradictoire par deux IA' if ai else 'B — recalcul indépendant (sans IA)',
        'target': TARGET,
        'date_releve': snap_manifest['date_releve'], 'method_version': cfg['version'], 'policy_version': policy['policy_version'],
        'generated_utc': generated.isoformat(timespec='seconds'), 'code_version': code_version(),
        'python': platform.python_version(), 'command': 'python -m auditor run ' + rel(snap),
        'snapshot': rel(snap), 'statuses': st, 'error': error,
        'calculations': {k: v for k, v in cmp_.items() if k not in ('calculations_csv',)} if cmp_ else None,
        'findings': findings, 'interpretations': interp, 'text_conformity': textc, 'sampling': sampling,
        'config_sha256': {p.name: F.sha256(p) for p in sorted((ROOT / 'config').glob('*.json'))},
        'previous_snapshot': rel(prev) if prev else None,
        'ai_audit': ai, 'limits': LIMITS, 'dedup': dedup,
    }
    dump(out / 'report.json', rep)
    (out / 'report.md').write_text(markdown(rep), encoding='utf-8')
    dump(out / 'anomalies.json', cmp_['anomalies'] if cmp_ else [])
    if cmp_:
        (out / 'calculations.csv').write_text(cmp_['calculations_csv'], encoding='utf-8')
    files = {p.name: F.sha256(p) for p in sorted(out.iterdir()) if p.name != 'manifest.json'}
    dump(out / 'manifest.json', {'report_id': rid, 'outputs_sha256': files, 'snapshot': rep['snapshot'],
                                 'snapshot_manifest_sha256': F.sha256(snap / 'manifest.json'),
                                 'inputs_sha256': {n: v['sha256'] for n, v in snap_manifest['inputs'].items()},
                                 'code_version': rep['code_version'], 'python': rep['python'], 'command': rep['command']})
    print(f"{out} · " + ' · '.join(f'{k} : {v}' for k, v in st.items()))
    return 0 if st['calculs_reproduction'] == 'conforme' else 2


def cmd_verify(args) -> int:
    rep_dir = Path(args.report).resolve()
    man = json.loads((rep_dir / 'manifest.json').read_text(encoding='utf-8'))
    bad = [n for n, h in man['outputs_sha256'].items() if not (rep_dir / n).exists() or F.sha256(rep_dir / n) != h]
    snap = ROOT / man['snapshot']
    if F.sha256(snap / 'manifest.json') != man['snapshot_manifest_sha256']:
        bad.append('snapshots/…/manifest.json')
    with tempfile.TemporaryDirectory() as tmp:
        try:
            F.restore(snap, Path(tmp))
        except ValueError as e:
            bad.append(str(e))
    print('INTÈGRE' if not bad else 'ALTÉRÉ : ' + ' ; '.join(bad))
    return 0 if not bad else 3


def cmd_canary(args) -> int:
    from .budget import Ledger
    from .canary import run_canary
    models = json.loads((ROOT / 'config' / 'ai-models.json').read_text(encoding='utf-8'))
    mandate = (ROOT / 'config' / 'mandate-v1.md').read_text(encoding='utf-8')
    out = ROOT / 'reports' / ('canari_' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    rep = run_canary(models, mandate, Ledger(ROOT, models), out)
    for s, r in rep['resultats'].items():
        print(f"IA {s} · {r['status']} · {r['model']} · instruction signalée : {r['instruction_signalee']} · "
              f"constat sur l’éditeur conservé : {r['constat_editeur_conserve']} · {r['usd']} $ {r.get('error') or ''}")
    print('CANARI ' + ('RÉUSSI' if rep['reussi'] else 'ÉCHOUÉ (publié tel quel)'))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog='python -m auditor')
    sub = p.add_subparsers(dest='cmd', required=True)
    f = sub.add_parser('fetch'); f.add_argument('--base', default=TARGET); f.set_defaults(fn=cmd_fetch)
    r = sub.add_parser('run'); r.add_argument('snapshot'); r.add_argument('--out')
    r.add_argument('--ia', action='store_true', help='phase C : contrôles à la source et audit par deux IA (réseau, clés)')
    r.set_defaults(fn=cmd_run)
    v = sub.add_parser('verify'); v.add_argument('report'); v.set_defaults(fn=cmd_verify)
    d = sub.add_parser('draw'); d.add_argument('snapshot'); d.set_defaults(fn=cmd_draw)
    c = sub.add_parser('canary'); c.set_defaults(fn=cmd_canary)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == '__main__':
    sys.exit(main())

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
from .sampling import check_beacon, draw_time, fetch_beacon, round_at, seed_of, select
from .textcheck import text_conformity
from .validate import validate

ROOT = Path(__file__).resolve().parent.parent
TARGET = 'https://meilleure-agence-nice.fr'
LIMITS = [
    'Le recalcul reprend tels quels les résultats d’étapes que les exports ne permettent pas de refaire : profil de '
    'l’auteur et problème signalé (lus par une IA du site), détection des doublons et des avis partagés (faite sur les '
    'textes, non publiés), points attribués en lisant les sites des agences, date de création des sociétés.',
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
            same = all(old['inputs'].get(n, {}).get('sha256') == v['sha256'] for n, v in got['files'].items()
                       if n != 'methode-details.html')
            if same:
                print(f'relevé {date} déjà archivé à l’identique : {snap}')
                return 0
            snap = ROOT / 'snapshots' / f"{date}_{got['started_utc'][11:19].replace(':', '')}"   # republication en cours de semaine
        archived = F.archive(tmp / 'inputs', snap)
        archived_at = time.time()
        dts = draw_time(archived_at)
        manifest = {'date_releve': date, 'fetch': got, 'inputs': archived, 'archived_utc':
                    dt.datetime.fromtimestamp(archived_at, dt.timezone.utc).isoformat(timespec='seconds'),
                    'draw_planned': {'utc': dt.datetime.fromtimestamp(dts, dt.timezone.utc).isoformat(timespec='seconds'),
                                     'drand_round': round_at(dts)},
                    'auditor_code': code_version()}
        dump(snap / 'manifest.json', manifest)
        print(f'archivé : {snap} ({len(archived)} fichiers, {len(got["errors"])} erreur(s))')
        return 1 if required_missing else 0


def planned_draw(snap_manifest: dict) -> dict:
    if 'draw_planned' in snap_manifest:
        return snap_manifest['draw_planned']
    t = dt.datetime.fromisoformat(snap_manifest['archived_utc']).timestamp()   # relevés archivés avant la règle 1.1
    d = draw_time(t)
    return {'utc': dt.datetime.fromtimestamp(d, dt.timezone.utc).isoformat(timespec='seconds'), 'drand_round': round_at(d)}


def cmd_draw(args) -> int:
    """Récupère la balise drand du tour fixé à l'archivage et l'enregistre dans snapshots/<date>/draw.json."""
    snap = Path(args.snapshot).resolve()
    man = json.loads((snap / 'manifest.json').read_text(encoding='utf-8'))
    plan = planned_draw(man)
    if time.time() < dt.datetime.fromisoformat(plan['utc']).timestamp():
        print(f"tirage pas encore possible : échéance {plan['utc']} (tour {plan['drand_round']})")
        return 4
    b = fetch_beacon(plan['drand_round'])
    errs = check_beacon(b, plan['drand_round'])
    dump(snap / 'draw.json', {'planned': plan, 'beacon': b, 'checks_errors': errs,
                              'bls_signature_verified': False})
    print('balise enregistrée' + (' AVEC ERREURS : ' + '; '.join(errs) if errs else ''))
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
                textc = text_conformity(data, cfg, interp, publisher)
            except Exception as e:            # noqa: BLE001 — un calcul en échec donne un statut « echec »
                error = f'{type(e).__name__}: {e}'
        sources = {r['agence']: r for r in read_csv(data / 'sources-agences.csv')} if (data / 'sources-agences.csv').exists() else {}
        plan = planned_draw(snap_manifest)
        sampling = {'status': 'en_attente', 'planned': plan, 'bls_signature_verified': False}
        draw_file = snap / 'draw.json'
        if draw_file.exists():
            draw = json.loads(draw_file.read_text(encoding='utf-8'))
            errs = check_beacon(draw['beacon'], plan['drand_round'])
            if errs:
                sampling.update(status='echec', errors=errs)
            else:
                seed = seed_of({n: v['sha256'] for n, v in snap_manifest['inputs'].items()}, draw['beacon'])
                sampling.update(select(read_csv(data / 'agences.csv'), sources, policy, seed), status='tire',
                                drand={k: draw['beacon'][k] for k in ('round', 'url')})
        reg_none = [s for s, r in (res or {}).get('agencies', {}).items() if r['detail']['avis']['regularity'] is None]
    st = statuses(cmp_, val, textc)
    rid = f"{snap_manifest['date_releve']}_{generated.strftime('%Y%m%dT%H%M%SZ')}"
    out = ROOT / 'reports' / rid if not args.out else Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    findings = val['findings'] + ([{'code': 'I-6', 'severity': 'info', 'message': 'agences dont la régularité est '
                                    'retirée et son poids redistribué (règle I-6)', 'agencies': reg_none[:50],
                                    'count': len(reg_none)}] if res else [])
    rep = {
        'report_id': rid, 'phase': 'B — recalcul indépendant (sans IA)', 'target': TARGET,
        'date_releve': snap_manifest['date_releve'], 'method_version': cfg['version'], 'policy_version': policy['policy_version'],
        'generated_utc': generated.isoformat(timespec='seconds'), 'code_version': code_version(),
        'python': platform.python_version(), 'command': 'python -m auditor run ' + rel(snap),
        'snapshot': rel(snap), 'statuses': st, 'error': error,
        'calculations': {k: v for k, v in cmp_.items() if k not in ('calculations_csv',)} if cmp_ else None,
        'findings': findings, 'interpretations': interp, 'text_conformity': textc, 'sampling': sampling,
        'previous_snapshot': rel(prev) if prev else None,
        'ai_agents': {'A': 'non exécuté (phase C)', 'B': 'non exécuté (phase C)'}, 'limits': LIMITS,
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


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog='python -m auditor')
    sub = p.add_subparsers(dest='cmd', required=True)
    f = sub.add_parser('fetch'); f.add_argument('--base', default=TARGET); f.set_defaults(fn=cmd_fetch)
    r = sub.add_parser('run'); r.add_argument('snapshot'); r.add_argument('--out'); r.set_defaults(fn=cmd_run)
    v = sub.add_parser('verify'); v.add_argument('report'); v.set_defaults(fn=cmd_verify)
    d = sub.add_parser('draw'); d.add_argument('snapshot'); d.set_defaults(fn=cmd_draw)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == '__main__':
    sys.exit(main())

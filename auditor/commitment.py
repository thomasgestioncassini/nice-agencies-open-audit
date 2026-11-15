"""Preuve d'engagement d'un relevé, vérifiée HORS du dépôt, auprès de l'API de GitHub.

Un relevé n'est admis au tirage que si :
1. son manifeste désigne l'exécution GitHub Actions qui l'a archivé (archive_run) ;
2. cette exécution appartient à ce dépôt, au workflow d'archivage, et a réussi ;
3. GitHub date sa fin AVANT l'échéance du tirage (horodatage de GitHub, que l'administrateur du dépôt ne peut pas
   modifier ; il peut seulement supprimer l'exécution, ce qui rend le relevé inadmissible, jamais un autre admissible) ;
4. le journal de cette exécution contient la ligne « ENGAGEMENT » portant l'empreinte SHA-256 exacte du manifeste.

Le champ archived_utc du manifeste n'est plus utilisé pour choisir le relevé : seul compte l'horodatage de GitHub.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import urllib.request

API = 'https://api.github.com'
REPO = os.environ.get('GITHUB_REPOSITORY', 'thomasgestioncassini/nice-agencies-open-audit')
WORKFLOW = '.github/workflows/archive.yml'


def _get(url: str, raw: bool = False):
    h = {'Accept': 'application/vnd.github+json', 'User-Agent': 'nice-agencies-open-audit'}
    tok = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if tok:
        h['Authorization'] = f'Bearer {tok}'
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=60) as r:
        data = r.read()
    return data.decode('utf-8', 'replace') if raw else json.loads(data)


def fetch_proof(run_id: str, get=_get) -> dict:
    run = get(f'{API}/repos/{REPO}/actions/runs/{run_id}')
    jobs = get(f'{API}/repos/{REPO}/actions/runs/{run_id}/jobs')['jobs']
    logs = ''.join(get(f"{API}/repos/{REPO}/actions/jobs/{j['id']}/logs", raw=True) for j in jobs)
    return {'run_id': str(run_id), 'repository': run.get('repository', {}).get('full_name'), 'path': run.get('path'),
            'conclusion': run.get('conclusion'), 'updated_at': run.get('updated_at'), 'created_at': run.get('created_at'),
            'html_url': run.get('html_url'), 'engagement_lines': [l.split(' ', 1)[-1] for l in logs.splitlines()
                                                                  if 'ENGAGEMENT relevé' in l]}


def check_proof(proof: dict, snapshot_name: str, manifest_sha256: str, deadline_ts: float) -> list[str]:
    """Erreurs (liste vide = engagement prouvé)."""
    errs = []
    if proof.get('repository') != REPO:
        errs.append(f"exécution d'un autre dépôt ({proof.get('repository')})")
    if proof.get('path') != WORKFLOW:
        errs.append(f"exécution d'un autre workflow ({proof.get('path')})")
    if proof.get('conclusion') != 'success':
        errs.append(f"exécution non réussie ({proof.get('conclusion')})")
    end = proof.get('updated_at')
    if not end or dt.datetime.fromisoformat(end.replace('Z', '+00:00')).timestamp() >= deadline_ts:
        errs.append(f'exécution terminée après l’échéance du tirage ({end})')
    want = f'ENGAGEMENT relevé {snapshot_name} · SHA-256 du manifeste {manifest_sha256}'
    if not any(l.startswith(want) for l in proof.get('engagement_lines', [])):
        errs.append('le journal GitHub ne contient pas l’empreinte de ce manifeste')
    return errs


def engagements_from_github(date_releve: str, deadline_ts: float, get=_get) -> dict:
    """Liste, depuis GitHub et non depuis le dépôt, tous les relevés de cette date engagés avant l'échéance : chaque
    exécution réussie du workflow d'archivage terminée avant l'échéance, et chaque ligne ENGAGEMENT de son journal.
    Renvoie {nom du relevé: {'sha256': ..., 'proof': ...}}. Un relevé ainsi engagé mais absent du dépôt, ou différent,
    rend le tirage impossible : il ne peut pas être remplacé par un autre."""
    out, page = {}, 1
    while True:
        r = get(f'{API}/repos/{REPO}/actions/workflows/archive.yml/runs?status=success&per_page=100&page={page}')
        runs = r.get('workflow_runs', [])
        for run in runs:
            end = run.get('updated_at')
            if not end or dt.datetime.fromisoformat(end.replace('Z', '+00:00')).timestamp() >= deadline_ts:
                continue
            proof = fetch_proof(run['id'], get)
            for line in proof['engagement_lines']:
                parts = line.split()
                try:
                    name, sha = parts[2], parts[parts.index('manifeste') + 1]
                except (IndexError, ValueError):
                    continue
                if name[:10] == date_releve:
                    out[name] = {'sha256': sha, 'proof': proof}
        if len(runs) < 100:
            return out
        page += 1


def evaluate(engaged: dict, local_sha256: dict, deadline_ts: float) -> tuple[dict, str | None]:
    """engaged : sortie de engagements_from_github ; local_sha256 : {relevé du dépôt: empreinte de son manifeste}.
    Renvoie (candidats avec leurs erreurs, motif de refus ou None). Si le dernier relevé engagé selon GitHub est absent
    ou modifié dans le dépôt, le tirage est refusé : aucun relevé antérieur ne peut le remplacer."""
    cands = {}
    for name, e in engaged.items():
        errs = check_proof(e['proof'], name, e['sha256'], deadline_ts)
        if name not in local_sha256:
            errs.append('relevé engagé sur GitHub mais absent du dépôt')
        elif local_sha256[name] != e['sha256']:
            errs.append('manifeste du dépôt différent de celui engagé sur GitHub')
        cands[name] = {'errors': errs, 'proof': e['proof']}
    for name in local_sha256:
        if name not in engaged:
            cands[name] = {'errors': ['aucun engagement GitHub avant l’échéance'], 'proof': None}
    last = max(((e['proof']['updated_at'], n) for n, e in engaged.items()), default=None)
    refusal = None
    if last and cands[last[1]]['errors']:
        refusal = f'le dernier relevé engagé sur GitHub ({last[1]}) est inadmissible : ' + '; '.join(cands[last[1]]['errors'])
    return cands, refusal

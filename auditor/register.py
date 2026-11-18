"""Registre public des audits : un tableau de tous les rapports du dépôt, y compris incomplets, en échec et de test.

Le registre est recalculé à chaque exécution à partir des dossiers de reports/ ; il ne remplace pas les rapports. La
colonne « signature » indique si l'empreinte du manifeste figure dans attestations.json, tenu par les exécutions GitHub
qui ont demandé une attestation Sigstore (vérifiable avec `gh attestation verify`). Les rapports antérieurs à la mise
en place des attestations (17/11/2026) n'en ont pas.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

LABEL = {'conforme': 'conforme', 'divergences': 'ÉCARTS', 'echec': 'ÉCHEC', 'non_execute': 'non exécuté',
         'non_verifie': 'non vérifié', 'complet': 'complet', 'incomplet': 'INCOMPLET'}


def entry(d: Path, attested: dict) -> dict:
    e = {'rapport': d.name, 'type': 'test canari' if d.name.startswith('canari_') else 'recalcul'}
    mp, rp = d / 'manifest.json', d / 'report.json'
    if mp.exists():
        e['manifeste_sha256'] = hashlib.sha256(mp.read_bytes()).hexdigest()
        e['signature'] = attested.get(e['manifeste_sha256'], {}).get('execution')
    if rp.exists():
        r = json.loads(rp.read_text(encoding='utf-8'))
        st = r.get('statuses') or {}
        e.update(releve=(r.get('snapshot') or '').split('/')[-1], genere_utc=r.get('generated_utc'),
                 methode=(r.get('method_version') or '').split(' (')[0], calculs=st.get('calculs_reproduction'),
                 dedoublonnage=st.get('dedoublonnage'), audit_ia=st.get('audit_ia'), erreur=bool(r.get('error')))
        if st.get('calculs_gestion'):
            e['calculs_gestion'] = st['calculs_gestion']
            e['methode_gestion'] = ((r.get('gestion') or {}).get('method_version') or '').split(' (')[0] or None
        if (d / 'agent-a.json').exists() or (d / 'agent-b.json').exists() or st.get('audit_ia') not in (None, 'non_execute'):
            e['type'] = 'audit des deux IA'
    return e


def build(root: Path) -> list[dict]:
    ap = root / 'attestations.json'
    attested = json.loads(ap.read_text(encoding='utf-8')) if ap.exists() else {}
    rows = [entry(d, attested) for d in sorted((root / 'reports').iterdir(), key=lambda d: d.name.split('_')[-1]) if d.is_dir()]
    (root / 'registre.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    L = ['# Registre des audits', '',
         'Tous les rapports du dépôt, du plus récent au plus ancien, y compris les rapports incomplets, en échec et les '
         'tests. Recalculé à chaque exécution ; les rapports eux-mêmes sont dans `reports/`. Ce registre n’est pas une '
         'certification du classement (docs/portee-et-limites.md).', '',
         f'{len(rows)} rapports, dont {sum(r["type"] == "audit des deux IA" for r in rows)} audits des deux IA et '
         f'{sum(bool(r.get("signature")) for r in rows)} avec attestation Sigstore.', '',
         '| Rapport | Type | Relevé | Méthode | Calculs | Doublons | Gestion locative | Audit IA | Attestation |',
         '|---|---|---|---|---|---|---|---|---|']
    f = lambda v: LABEL.get(v, v or '—')
    for r in reversed(rows):
        L.append(f"| [{r['rapport']}](reports/{r['rapport']}/) | {r['type']} | {r.get('releve') or '—'} | {r.get('methode') or '—'} | "
                 f"{f(r.get('calculs'))} | {f(r.get('dedoublonnage'))} | {f(r.get('calculs_gestion'))} | {f(r.get('audit_ia'))} | "
                 f"{'exécution ' + str(r['signature']) if r.get('signature') else '—'} |")
    (root / 'REGISTRE.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    return rows

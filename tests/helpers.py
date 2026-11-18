"""Outils communs aux tests : relevé archivé le plus récent, restauré dans un dossier temporaire."""
import csv
import json
import tempfile
from pathlib import Path

from auditor import fetch as F
from auditor.compare import compare
from auditor.recalculate import recalculate

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / 'config' / 'methodology-v5.json').read_text(encoding='utf-8'))
POLICY = json.loads((ROOT / 'config' / 'audit-policy.json').read_text(encoding='utf-8'))


import os
import unittest

REFERENCE = ROOT / 'snapshots' / '2026-11-15'       # relevé de référence : 552 agences classées
REQUIRE = os.environ.get('AUDIT_REQUIRE_SNAPSHOT') == '1'   # en intégration continue : un test sauté est un échec


def needs_snapshot(cls):
    if latest_snapshot() is None:
        if REQUIRE:
            raise RuntimeError('aucun relevé archivé alors que AUDIT_REQUIRE_SNAPSHOT=1')
        return unittest.skip('aucun relevé archivé')(cls)
    return cls


def latest_snapshot():
    snaps = sorted(p for p in (ROOT / 'snapshots').glob('*') if (p / 'manifest.json').exists())
    return snaps[-1] if snaps else None


def restored(snap=None):
    snap = snap or latest_snapshot()
    tmp = tempfile.TemporaryDirectory()
    F.restore(snap, Path(tmp.name))
    return tmp, Path(tmp.name)


def cfg_for(data_dir):
    """Méthode de l'auditeur applicable au relevé (v5 avant le 18/11/2026, v6 ensuite)."""
    from auditor.__main__ import method_for
    return method_for(data_dir)


def audit(data_dir, variants=()):
    res = recalculate(data_dir, cfg_for(data_dir), variants)
    return res, compare(data_dir, res, POLICY)


def rows(path):
    with open(path, encoding='utf-8', newline='') as f:
        r = csv.DictReader(f, delimiter=';')
        return r.fieldnames, list(r)


def write_rows(path, head, data):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=head, delimiter=';', lineterminator='\n')
        w.writeheader()
        w.writerows(data)

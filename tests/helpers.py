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


def latest_snapshot():
    snaps = sorted(p for p in (ROOT / 'snapshots').glob('*') if (p / 'manifest.json').exists())
    return snaps[-1] if snaps else None


def restored():
    snap = latest_snapshot()
    tmp = tempfile.TemporaryDirectory()
    F.restore(snap, Path(tmp.name))
    return tmp, Path(tmp.name)


def audit(data_dir):
    res = recalculate(data_dir, CFG)
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

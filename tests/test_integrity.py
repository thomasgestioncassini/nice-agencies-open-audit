"""Tests 2, 3 et 4 : altérations volontaires d'un relevé archivé. Test d'altération d'un rapport (empreintes)."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import ROOT, audit, latest_snapshot, restored, rows, write_rows

PUB_COLS = ('avis', 'service', 'honoraires', 'mentions_legales', 'information', 'anciennete')


def flagged(cmp_, agency):
    return {a['objet'] for a in cmp_['anomalies'] if a['agence'] == agency and a['statut'] == 'divergente'}


@unittest.skipIf(latest_snapshot() is None, 'aucun relevé archivé')
class Alterations(unittest.TestCase):
    def test_2_altered_published_note_is_detected(self):
        tmp, d = restored()
        with tmp:
            head, ag = rows(d / 'agences.csv')
            victim = sorted(ag, key=lambda r: int(r['rang_publie']))[200]
            victim['note_publiee'] = f"{float(victim['note_publiee']) + 0.01:.4f}"
            write_rows(d / 'agences.csv', head, ag)
            _, cmp_ = audit(d)
        self.assertIn('note', flagged(cmp_, victim['agence']))

    def _publisher_favoured(self, agency, data_change):
        tmp, d = restored()
        with tmp:
            data_change(d)
            _, cmp_ = audit(d)
        return flagged(cmp_, agency)

    def test_3_artificial_advantage_to_immovendu_is_detected(self):
        """Le site publierait pour ImmoVendu une note plus haute que ses données ne le permettent."""
        def change(d):
            head, ag = rows(d / 'agences.csv')
            for r in ag:
                if r['agence'] == 'immovendu':
                    r['note_publiee'] = f"{float(r['note_publiee']) + 0.5:.4f}"
                    r['honoraires'] = '100.0000'
            write_rows(d / 'agences.csv', head, ag)
        got = self._publisher_favoured('immovendu', change)
        self.assertIn('note', got)
        self.assertIn('pilier hono', got)

    def test_3b_invented_reviews_for_immovendu_are_detected(self):
        """Des avis 5/5 ajoutés aux données d'ImmoVendu sans que les notes publiées changent."""
        def change(d):
            head, items = rows(d / 'avis-elementaires.csv')
            base = next(x for x in items if x['agence'] == 'immovendu' and x['retenu_qualite'] == '1')
            items += [{**base, 'id': f'fictif{i}', 'note': '5.0', 'date': '2026-11-01'} for i in range(40)]
            write_rows(d / 'avis-elementaires.csv', head, items)
        got = self._publisher_favoured('immovendu', change)
        self.assertIn('pilier avis', got)

    def test_4_artificial_penalty_to_gestion_cassini_is_detected(self):
        """Symétrique : le site publierait pour Gestion Cassini une note plus basse que ses données."""
        def change(d):
            head, ag = rows(d / 'agences.csv')
            for r in ag:
                if r['agence'] == 'gestion-cassini':
                    r['note_publiee'] = f"{float(r['note_publiee']) - 0.5:.4f}"
                    r['mentions_legales'] = '0.0000'
            write_rows(d / 'agences.csv', head, ag)
        got = self._publisher_favoured('gestion-cassini', change)
        self.assertIn('note', got)
        self.assertIn('pilier conf', got)

    def test_4b_removed_criterion_points_for_gestion_cassini_are_detected(self):
        def change(d):
            head, cr = rows(d / 'criteres-sites.csv')
            for r in cr:
                if r['agence'] == 'gestion-cassini' and r['pilier'] == 'info' and r['max'] and r['points'] == '1':
                    r['points'] = '0'
                    break
            write_rows(d / 'criteres-sites.csv', head, cr)
        got = self._publisher_favoured('gestion-cassini', change)
        self.assertIn('pilier info', got)


@unittest.skipIf(latest_snapshot() is None, 'aucun relevé archivé')
class ReportTampering(unittest.TestCase):
    def test_modified_report_copy_is_detected(self):
        out = Path(tempfile.mkdtemp())
        try:
            run = subprocess.run([sys.executable, '-m', 'auditor', 'run', str(latest_snapshot()), '--out', str(out)],
                                 cwd=ROOT, capture_output=True, text=True)
            self.assertIn(run.returncode, (0, 2), run.stderr)
            ok = subprocess.run([sys.executable, '-m', 'auditor', 'verify', str(out)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stdout)
            rep = json.loads((out / 'report.json').read_text(encoding='utf-8'))
            rep['statuses']['calculs'] = 'conforme' if rep['statuses']['calculs'] != 'conforme' else 'divergences'
            (out / 'report.json').write_text(json.dumps(rep), encoding='utf-8')
            bad = subprocess.run([sys.executable, '-m', 'auditor', 'verify', str(out)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(bad.returncode, 3)
            self.assertIn('ALTÉRÉ', bad.stdout)
        finally:
            shutil.rmtree(out, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()

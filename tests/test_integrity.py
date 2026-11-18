"""Tests 2, 3 et 4 : altérations volontaires d'un relevé archivé. Test d'altération d'un rapport (empreintes)."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from auditor import fetch as F
from auditor.validate import validate
from tests.helpers import CFG, POLICY, cfg_for, REFERENCE, ROOT, audit, latest_snapshot, needs_snapshot, restored, rows, write_rows

PUB_COLS = ('avis', 'service', 'honoraires', 'mentions_legales', 'information', 'anciennete')


def flagged(cmp_, agency):
    return {a['objet'] for a in cmp_['anomalies'] if a['agence'] == agency and a['statut'] == 'divergente'}


@needs_snapshot
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
                    # on gonfle le premier pilier qui n'est pas déjà au maximum (depuis la v5.2,
                    # le pilier honoraires d'ImmoVendu est à 100 : le gonfler ne changerait rien)
                    col = next(c for c in ('honoraires', 'service', 'avis') if float(r[c]) < 95)
                    r[col] = f"{float(r[col]) + 5:.4f}"
                    picked.append(col)
            write_rows(d / 'agences.csv', head, ag)
        picked = []
        got = self._publisher_favoured('immovendu', change)
        key = {'honoraires': 'hono', 'service': 'serv', 'avis': 'avis'}[picked[0]]
        self.assertIn('note', got)
        self.assertIn(f'pilier {key}', got)

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
                # critère noté (maximum > 0) obtenu en entier ; v6 : les critères de maximum 0 ne sont pas notés
                if (r['agence'] == 'gestion-cassini' and r['pilier'] == 'info' and r['max'] and float(r['max']) > 0
                        and r['points'] == r['max']):
                    r['points'] = '0'
                    break
            write_rows(d / 'criteres-sites.csv', head, cr)
        got = self._publisher_favoured('gestion-cassini', change)
        self.assertIn('pilier info', got)


@needs_snapshot
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
            k = 'calculs_reproduction'
            rep['statuses'][k] = 'conforme' if rep['statuses'][k] != 'conforme' else 'divergences'
            (out / 'report.json').write_text(json.dumps(rep), encoding='utf-8')
            bad = subprocess.run([sys.executable, '-m', 'auditor', 'verify', str(out)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(bad.returncode, 3)
            self.assertIn('ALTÉRÉ', bad.stdout)
        finally:
            shutil.rmtree(out, ignore_errors=True)


def forge_consistently(d, agency='immovendu', n=40, date='2025-06-01'):
    """Falsification coordonnée : avis 5/5 inventés ET piliers, notes et rangs publiés recalculés en conséquence."""
    head, items = rows(d / 'avis-elementaires.csv')
    base = next(x for x in items if x['agence'] == agency and x['retenu_qualite'] == '1' and x['plateforme'] == 'google')
    items += [{**base, 'id': f'fictif{i}', 'note': '5.0', 'date': date, 'reponse_agence': '', 'probleme': ''} for i in range(n)]
    write_rows(d / 'avis-elementaires.csv', head, items)
    head_a, ag = rows(d / 'agregats-plateformes.csv')
    for a in ag:
        if a['agence'] == agency and a['plateforme'] == 'google':
            a['nombre'] = str(int(float(a['nombre'])) + n)
    write_rows(d / 'agregats-plateformes.csv', head_a, ag)
    res, _ = audit(d)
    head_p, pub = rows(d / 'agences.csv')
    cols = dict(zip(('avis', 'serv', 'hono', 'conf', 'info', 'anc'),
                    ('avis', 'service', 'honoraires', 'mentions_legales', 'information', 'anciennete')))
    for p in pub:
        r = res['agencies'][p['agence']]
        p['note_publiee'] = f"{r['note']:.4f}"
        p['rang_publie'] = str(r['rank'])
        for k, c in cols.items():
            p[c] = f"{r['pillars'][k]:.4f}"
    write_rows(d / 'agences.csv', head_p, pub)


@needs_snapshot
class CoordinatedForgery(unittest.TestCase):
    """Limite assumée : une falsification cohérente des données ET des notes n'est pas visible au recalcul. L'auditeur
    doit le dire (statut « données primaires non vérifiées ») et la comparaison entre relevés doit la signaler."""

    def test_recalculation_alone_cannot_see_it(self):
        tmp, d = restored(REFERENCE)
        with tmp:
            forge_consistently(d)
            _, cmp_ = audit(d)
        self.assertEqual(cmp_['notes']['divergente'], 0)          # le recalcul reste conforme : c'est la limite
        self.assertEqual(cmp_['ranks_divergent'], 0)

    def test_report_does_not_claim_primary_data_verified(self):
        out = Path(tempfile.mkdtemp())
        try:
            subprocess.run([sys.executable, '-m', 'auditor', 'run', str(REFERENCE), '--out', str(out)], cwd=ROOT,
                           capture_output=True, text=True)
            rep = json.loads((out / 'report.json').read_text(encoding='utf-8'))
            self.assertEqual(rep['statuses']['donnees_primaires'], 'non_verifiees')
            self.assertIn('falsifiées de façon cohérente', (out / 'report.md').read_text(encoding='utf-8'))
        finally:
            shutil.rmtree(out, ignore_errors=True)

    def test_history_comparison_flags_backdated_reviews(self):
        prev_tmp, prev = restored(REFERENCE)
        cur_tmp, cur = restored(REFERENCE)
        with prev_tmp, cur_tmp:
            # relevé suivant simulé : une semaine plus tard, avec 40 avis antidatés pour ImmoVendu
            pj = json.loads((cur / 'parametres.json').read_text(encoding='utf-8'))
            pj['date_releve'] = '2026-11-22'
            (cur / 'parametres.json').write_text(json.dumps(pj), encoding='utf-8')
            forge_consistently(cur)
            val = validate(cur, cfg_for(cur), POLICY['sampling']['publisher_agencies'], prev)
        f = next(x for x in val['findings'] if x['code'] == 'V-13a')
        self.assertEqual(f['severity'], 'majeur')
        self.assertEqual(f['per_agency'].get('immovendu'), 40)

    def test_history_comparison_flags_vanished_reviews_for_gestion_cassini(self):
        prev_tmp, prev = restored(REFERENCE)
        cur_tmp, cur = restored(REFERENCE)
        with prev_tmp, cur_tmp:
            head, items = rows(cur / 'avis-elementaires.csv')
            gc = [x for x in items if x['agence'] == 'gestion-cassini'][:10]
            write_rows(cur / 'avis-elementaires.csv', head, [x for x in items if x not in gc])
            val = validate(cur, cfg_for(cur), POLICY['sampling']['publisher_agencies'], prev)
        f = next(x for x in val['findings'] if x['code'] == 'V-13b')
        self.assertEqual(f['per_agency'].get('gestion-cassini'), 10)

    def test_history_comparison_flags_reclassified_reviews_even_one(self):
        """Critique de ChatGPT : un avis existant reclassé (profil, problème, drapeaux) doit être signalé, même seul."""
        prev_tmp, prev = restored(REFERENCE)
        cur_tmp, cur = restored(REFERENCE)
        with prev_tmp, cur_tmp:
            head, items = rows(cur / 'avis-elementaires.csv')
            x = next(x for x in items if x['agence'] == 'immovendu' and x['probleme'] == 'probleme')
            x['probleme'] = 'ok'                               # un problème signalé effacé pour l'éditeur
            write_rows(cur / 'avis-elementaires.csv', head, items)
            val = validate(cur, cfg_for(cur), POLICY['sampling']['publisher_agencies'], prev)
        f = next(x for x in val['findings'] if x['code'] == 'V-13d')
        self.assertEqual(f['per_agency'], {'immovendu': 1})
        self.assertEqual(f['severity'], 'majeur')
        self.assertEqual(f['fields'], {'probleme': 1})


if __name__ == '__main__':
    unittest.main()

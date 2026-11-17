"""V-15 : identifiants de lecture, journal des lectures et registre des relectures exceptionnelles."""
import tempfile
import unittest
from pathlib import Path

from auditor.validate import readings


def write(d, name, head, rows):
    (d / name).write_text('\n'.join([';'.join(head)] + [';'.join(r) for r in rows]) + '\n', encoding='utf-8')


def build(d, lect=None, reg=None, crit=None):
    write(d, 'criteres-sites.csv', ['agence', 'critere', 'points', 'id_lecture'],
          crit or [['a', 'Carte', '25', 'r1'], ['b', 'Carte', '0', 'r1'], ['c', 'Carte', '0', '']])
    write(d, 'sources-agences.csv', ['agence', 'url_site', 'sans_site'], [['a', 'https://a', '0'], ['b', 'https://b', '0'], ['c', '', '1']])
    if lect is not None:
        write(d, 'lectures.csv', ['id_lecture', 'journal', 'agence', 'page', 'url', 'heure_utc', 'empreinte_texte', 'resultat'], lect)
    if reg is not None:
        write(d, 'relectures-exceptionnelles.csv', ['id_lecture', 'date_decision', 'inscription', 'type', 'motif', 'perimetre'], reg)


L = [['r1', 'j', 'a', 'mentions', 'u', '2026-12-01T10:00:00Z', 'ab', 'ok'], ['r1', 'j', 'b', 'mentions', 'u', '2026-12-01T10:01:00Z', 'cd', 'ok']]
R = [['r1', '2026-12-01', 'avant le lancement', 'regle_nouvelle', 'motif publié', 'toutes']]


class Readings(unittest.TestCase):
    def run_with(self, **kw):
        with tempfile.TemporaryDirectory() as t:
            build(Path(t), **kw)
            return {f['code']: f for f in readings(Path(t), ['a'])}

    def test_consistent_journal_passes(self):
        f = self.run_with(lect=L, reg=R)
        self.assertTrue(all(x['severity'] == 'info' for x in f.values()), f)

    def test_identifier_without_journal_entry(self):
        f = self.run_with(lect=L[:1], reg=R)                # b porte r1 mais n'a aucune lecture au journal
        self.assertEqual((f['V-15a']['severity'], f['V-15a']['count']), ('majeur', 1))
        self.assertEqual(f['V-15e']['severity'], 'majeur')  # et la relecture « toutes » ne couvre pas b

    def test_undeclared_or_unmotivated_reread(self):
        self.assertEqual(self.run_with(lect=L, reg=[])['V-15b']['severity'], 'majeur')
        self.assertEqual(self.run_with(lect=L, reg=[R[0][:4] + ['', 'toutes']])['V-15b']['severity'], 'majeur')

    def test_missing_timestamp_and_late_registration_are_reported(self):
        f = self.run_with(lect=[L[0], L[1][:5] + ['', '', 'ok']], reg=[R[0][:2] + ['après coup'] + R[0][3:]])
        self.assertEqual(f['V-15d']['count'], 1)
        self.assertEqual(f['V-15c']['count'], 1)

    def test_missing_files_is_not_a_pass(self):
        f = self.run_with()
        self.assertEqual(f['V-15']['severity'], 'mineur')


if __name__ == '__main__':
    unittest.main()

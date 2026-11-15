"""Conformité au texte : une règle n'est « documentée » que si sa description figure dans le texte archivé."""
import json
import unittest

from auditor.textcheck import text_conformity
from tests.helpers import CFG, REFERENCE, ROOT, needs_snapshot, restored

INTERP = json.loads((ROOT / 'config' / 'interpretations.json').read_text(encoding='utf-8'))
PUBLISHER = ['immovendu', 'gestion-cassini']


@needs_snapshot
class TextConformity(unittest.TestCase):
    def test_reference_text_has_contradictions(self):
        tmp, d = restored(REFERENCE)
        with tmp:
            r = text_conformity(d, CFG, INTERP, PUBLISHER)
        self.assertEqual(r['status'], 'ecarts')
        self.assertEqual(r['contradictions'], ['I-4', 'I-7'])
        self.assertEqual(r['ambiguities'], ['I-6', 'I-11'])
        self.assertEqual(r['effects']['ensemble']['agences_suivies']['immovendu']['rang_production'], 2)

    def test_rule_documented_only_when_its_description_is_in_the_text(self):
        tmp, d = restored(REFERENCE)
        with tmp:
            page = d / 'methode-details.html'
            extra = ' '.join(i['documented_by'] for i in INTERP if i.get('documented_by'))
            page.write_text(page.read_text(encoding='utf-8') + f'<p>{extra}</p>', encoding='utf-8')
            r = text_conformity(d, CFG, INTERP, PUBLISHER)
            self.assertEqual(r['status'], 'conforme')
            self.assertIn('I-4', r['documented_in_archived_text'])
            # une phrase tronquée ne suffit pas
            page.write_text('<p>puis arrondie</p>', encoding='utf-8')
            r = text_conformity(d, CFG, INTERP, PUBLISHER)
            self.assertIn('I-7', r['contradictions'])

    def test_missing_text_is_a_failure_not_a_pass(self):
        tmp, d = restored(REFERENCE)
        with tmp:
            (d / 'methode-details.html').unlink()
            self.assertEqual(text_conformity(d, CFG, INTERP, PUBLISHER)['status'], 'echec')


if __name__ == '__main__':
    unittest.main()

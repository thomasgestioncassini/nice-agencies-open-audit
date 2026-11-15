"""Texte de la méthode : règles décrites, contradictions encore présentes, écarts des versions antérieures conservés."""
import json
import unittest

from auditor.textcheck import page_text, read_text_rules, text_conformity
from tests.helpers import CFG, REFERENCE, ROOT, needs_snapshot, restored

INTERP = json.loads((ROOT / 'config' / 'interpretations.json').read_text(encoding='utf-8'))
PUBLISHER = ['immovendu', 'gestion-cassini']
ALL_DOC = ' '.join(i['documented_by'] for i in INTERP if i.get('documented_by'))


class PhraseRules(unittest.TestCase):
    def test_description_alone_is_documented(self):
        r = read_text_rules(f'<p>{ALL_DOC}</p>', INTERP)
        self.assertEqual(r['contradictions'], [])
        self.assertEqual(r['residual_contradictions'], [])

    def test_description_does_not_hide_a_contrary_sentence_still_present(self):
        """Critique de ChatGPT : « puis arrondie au centième » ne suffit pas si « note exacte » reste dans le texte."""
        r = read_text_rules(f"{ALL_DOC} Les agences sont rangées selon leur note exacte.", INTERP)
        self.assertIn('I-7', r['residual_contradictions'])
        self.assertIn('I-7', r['contradictions'])

    def test_truncated_phrase_is_not_enough(self):
        self.assertIn('I-7', read_text_rules('puis arrondie', INTERP)['contradictions'])


@needs_snapshot
class TextConformity(unittest.TestCase):
    def test_reference_text_has_contradictions(self):
        tmp, d = restored(REFERENCE)
        with tmp:
            r = text_conformity(d, CFG, INTERP, PUBLISHER)
        self.assertEqual(r['current']['contradictions'], ['I-4', 'I-7'])
        self.assertEqual(r['current']['ambiguities'], ['I-6', 'I-11'])
        self.assertEqual(r['coherence'], 'contradictions_residuelles')
        self.assertEqual(r['documentation'], 'partielle')

    def test_corrected_text_keeps_the_history_of_past_contradictions(self):
        tmp, d = restored(REFERENCE)
        with tmp:
            old = d.parent / (d.name + '_ancien.html')
            old.write_bytes((d / 'methode-details.html').read_bytes())
            (d / 'methode-details.html').write_text(f'<p>{ALL_DOC}</p>', encoding='utf-8')
            r = text_conformity(d, CFG, INTERP, PUBLISHER, [('ancien', old)])
            old.unlink()
        self.assertEqual(r['documentation'], 'complete')
        self.assertEqual(r['coherence'], 'aucune_contradiction_repertoriee')
        self.assertEqual(r['history'], 'ecarts_anterieurs')
        self.assertEqual(r['past'][0]['contradictions'], ['I-4', 'I-7'])

    def test_missing_text_is_a_failure_not_a_pass(self):
        tmp, d = restored(REFERENCE)
        with tmp:
            (d / 'methode-details.html').unlink()
            r = text_conformity(d, CFG, INTERP, PUBLISHER)
        self.assertEqual((r['documentation'], r['coherence']), ('echec', 'echec'))


if __name__ == '__main__':
    unittest.main()

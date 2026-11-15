"""Formules publiées (cas simples construits à la main) et test 1 : reproduction complète d'un relevé archivé."""
import datetime as dt
import unittest

from auditor.recalculate import (Method, PILLARS, nice_average, pillar_points, pillar_seniority, pillar_service,
                                 star_to_100)
from tests.helpers import CFG, audit, latest_snapshot, restored

M = Method(CFG)
REF = dt.date(2026, 11, 15)


def review(**kw):
    base = {'agence': 'a', 'plateforme': 'google', 'id': 'x', 'date': '2026-10-01', 'note': '5', 'profil': 'vendeur',
            'compte_vente_achat': '1', 'releve_complet': '1', 'retenu_qualite': '1', 'retenu_service': '1',
            'nb_agences_partageant': '1', 'reponse_agence': '', 'probleme': ''}
    base.update(kw)
    return base


class Formulas(unittest.TestCase):
    def test_worked_example_of_the_method(self):
        ex = CFG['worked_example']
        note = sum(ex['pillars'][p] * CFG['weights'][p] for p in PILLARS) / sum(CFG['weights'].values())
        self.assertAlmostEqual(round(note, 1), ex['note'])

    def test_weights_sum_to_100(self):
        self.assertEqual(sum(CFG['weights'].values()), 100)
        self.assertEqual(sum(CFG['criteria_count'].values()), 23)

    def test_star_conversion(self):
        self.assertEqual(star_to_100(3), 0)
        self.assertEqual(star_to_100(4), 50)
        self.assertEqual(star_to_100(5), 100)
        self.assertEqual(star_to_100(2), 0)

    def test_seniority(self):
        self.assertEqual(pillar_seniority('2016-11-01', M, REF), 50.0)
        self.assertEqual(pillar_seniority('1995-05-02', M, REF), 100.0)
        self.assertEqual(pillar_seniority('2026-11-01', M, REF), 0.0)
        self.assertIsNone(pillar_seniority('', M, REF))

    def test_points_not_applicable_criterion_is_ignored(self):
        rows = [{'points': '1', 'max': '1'}, {'points': '0', 'max': '1'}, {'points': '', 'max': ''}]
        self.assertEqual(pillar_points(rows), 50.0)
        self.assertIsNone(pillar_points([{'points': '', 'max': ''}]))

    def test_service_rules(self):
        s, d = pillar_service([], M)
        self.assertEqual(d['response'], 75.0)          # aucun avis négatif
        self.assertEqual(d['problems'], 50.0)          # moins de 10 avis avec texte
        neg = [review(note='2', reponse_agence='1'), review(note='1', reponse_agence='0')]
        texts = [review(probleme='ok')] * 8 + [review(probleme='probleme')] * 2
        s, d = pillar_service(neg + texts, M)
        self.assertEqual(d['response'], round(100 * (1 + 2) / (2 + 4), 1))
        # 2 problèmes sur 10 avis avec texte = 20 % → 100 × (1 − 0,20 / 0,25) = 20
        self.assertEqual(d['texts'], 10)
        self.assertEqual(d['problems'], 20.0)
        self.assertEqual(s, round(0.4 * d['response'] + 0.6 * 20.0, 1))

    def test_nice_average(self):
        aggs = [{'agence': 'a', 'note': '4', 'nombre': '10'}, {'agence': 'a', 'note': '5', 'nombre': '10'},
                {'agence': 'b', 'note': '3', 'nombre': '1'}]
        self.assertEqual(nice_average(aggs), round((4.5 + 3) / 2, 3))


@unittest.skipIf(latest_snapshot() is None, 'aucun relevé archivé')
class Test1Reproduction(unittest.TestCase):
    """Test 1 : à partir du dépôt et d'un relevé archivé, sans clé d'API ni réseau, toutes les notes sont recalculées."""

    def test_full_snapshot(self):
        tmp, d = restored()
        with tmp:
            res, cmp_ = audit(d)
        self.assertGreater(cmp_['examined'], 500)
        self.assertEqual(cmp_['notes']['divergente'], 0, cmp_['anomalies'][:5])
        self.assertEqual(cmp_['ranks_divergent'], 0)


if __name__ == '__main__':
    unittest.main()

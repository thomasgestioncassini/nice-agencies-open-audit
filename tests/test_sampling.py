"""Tirage des agences contrôlées : échéance fixe, aucun repli sans balise, balise contrôlée, règle reproductible."""
import datetime as dt
import hashlib
import unittest

from auditor.sampling import CHAIN_HASH, check_beacon, draw_time, round_at, seed_of, select
from tests.helpers import POLICY


def utc(*a):
    return dt.datetime(*a, tzinfo=dt.timezone.utc).timestamp()


def beacon(rnd):
    sig = hashlib.sha256(str(rnd).encode()).hexdigest() * 3
    return {'chain': CHAIN_HASH, 'round': rnd, 'signature': sig, 'randomness': hashlib.sha256(bytes.fromhex(sig)).hexdigest()}


class Sampling(unittest.TestCase):
    def test_draw_time_is_fixed_whatever_the_rerun(self):
        a = draw_time(utc(2026, 11, 15, 11, 38))
        b = draw_time(utc(2026, 11, 15, 23, 59))        # archivage relancé le soir : même échéance
        self.assertEqual(a, b)
        self.assertEqual(a, utc(2026, 11, 16, 6, 0))
        self.assertEqual(draw_time(utc(2026, 11, 16, 5, 0)), utc(2026, 11, 16, 6, 0))
        self.assertEqual(round_at(utc(2026, 11, 15, 11, 38, 16)), 33979778)   # tour réellement publié à cet instant

    def test_no_fallback_without_beacon(self):
        with self.assertRaises(ValueError):
            seed_of({'a.csv': '00'}, None)
        with self.assertRaises(ValueError):
            seed_of({'a.csv': '00'}, {'error': 'indisponible'})

    def test_beacon_checks(self):
        b = beacon(42)
        self.assertEqual(check_beacon(b, 42), [])
        self.assertTrue(check_beacon(b, 43))                                   # mauvais tour
        self.assertTrue(check_beacon({**b, 'randomness': '00' * 32}, 42))       # valeur aléatoire falsifiée
        self.assertTrue(check_beacon({**b, 'chain': 'autre'}, 42))              # autre chaîne

    def test_selection_is_reproducible_and_includes_publisher(self):
        ag = [{'agence': f'a{i:03d}', 'rang_publie': str(i + 1)} for i in range(300)]
        ag[1]['agence'] = 'immovendu'
        ag[123]['agence'] = 'gestion-cassini'
        seed = seed_of({'a.csv': 'ff'}, beacon(7))
        s1, s2 = select(ag, {}, POLICY, seed), select(ag, {}, POLICY, seed)
        self.assertEqual(s1, s2)
        self.assertEqual(s1['agencies']['immovendu'], 'editeur')
        self.assertEqual(s1['agencies']['gestion-cassini'], 'editeur')
        self.assertEqual(sum(1 for v in s1['agencies'].values() if v == 'tirage_aleatoire'), 20)
        other = select(ag, {}, POLICY, seed_of({'a.csv': 'ff'}, beacon(8)))
        self.assertNotEqual(s1['agencies'], other['agencies'])


if __name__ == '__main__':
    unittest.main()

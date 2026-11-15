"""Tirage des agences contrôlées : échéance fixe, aucun repli sans balise, balise contrôlée, règle reproductible."""
import datetime as dt
import hashlib
import unittest

import json
import os

from auditor.drandverify import verify
from auditor.sampling import CHAIN_HASH, check_beacon, committed_snapshot, draw_deadline, round_at, seed_of, select
from tests.helpers import POLICY, REFERENCE

REAL = json.loads((REFERENCE / 'manifest.json').read_text(encoding='utf-8')).get('drand') if (REFERENCE / 'manifest.json').exists() else None
try:
    import py_ecc  # noqa: F401
    HAS_BLS = True
except ImportError:
    HAS_BLS = False
if not HAS_BLS and os.environ.get('AUDIT_REQUIRE_BLS') == '1':
    raise RuntimeError('py_ecc absent alors que AUDIT_REQUIRE_BLS=1')


def utc(*a):
    return dt.datetime(*a, tzinfo=dt.timezone.utc).timestamp()


def beacon(rnd):
    sig = hashlib.sha256(str(rnd).encode()).hexdigest() * 3
    return {'chain': CHAIN_HASH, 'round': rnd, 'signature': sig, 'randomness': hashlib.sha256(bytes.fromhex(sig)).hexdigest()}


class Sampling(unittest.TestCase):
    def test_deadline_is_fixed_per_releve(self):
        self.assertEqual(draw_deadline('2026-11-15'), utc(2026, 11, 17, 6, 0))   # dimanche → mardi suivant
        self.assertEqual(draw_deadline('2026-11-16'), utc(2026, 11, 17, 6, 0))   # lundi → mardi
        self.assertEqual(draw_deadline('2026-11-17'), utc(2026, 11, 24, 6, 0))   # mardi → mardi suivant
        self.assertEqual(round_at(utc(2026, 11, 15, 11, 38, 16)), 33979778)       # tour réellement publié à cet instant

    def test_committed_snapshot_is_the_last_archived_before_deadline(self):
        m = [{'date_releve': '2026-11-15', 'archived_utc': '2026-11-15T11:38:16+00:00', 'n': 1},
             {'date_releve': '2026-11-15', 'archived_utc': '2026-11-16T22:00:00+00:00', 'n': 2},
             {'date_releve': '2026-11-15', 'archived_utc': '2026-11-17T06:00:01+00:00', 'n': 3}]   # après l'échéance
        self.assertEqual(committed_snapshot(m, '2026-11-15')['n'], 2)
        self.assertIsNone(committed_snapshot(m[2:], '2026-11-15'))

    def test_no_fallback_without_beacon(self):
        with self.assertRaises(ValueError):
            seed_of({'a.csv': '00'}, None)
        with self.assertRaises(ValueError):
            seed_of({'a.csv': '00'}, {'error': 'indisponible'})

    @unittest.skipUnless(HAS_BLS and REAL, 'py_ecc ou balise réelle absente')
    def test_real_beacon_is_authenticated(self):
        b = {**REAL, 'chain': CHAIN_HASH}
        self.assertTrue(verify(b['round'], b['signature']))
        self.assertEqual(check_beacon(b, b['round']), [])
        self.assertFalse(verify(b['round'] + 1, b['signature']))              # signature d'un autre tour

    @unittest.skipUnless(HAS_BLS, 'py_ecc absent')
    def test_forged_but_consistent_beacon_is_refused(self):
        """Critique de ChatGPT : une fausse signature avec son SHA-256 recalculé doit être refusée."""
        b = beacon(42)
        errs = check_beacon(b, 42)
        self.assertTrue(any('BLS' in e for e in errs))

    def test_beacon_checks(self):
        b = beacon(42)
        self.assertEqual([e for e in check_beacon(b, 42, require_bls=False) if 'BLS' not in e], [])
        self.assertTrue(check_beacon(b, 43, require_bls=False))                # mauvais tour
        self.assertTrue(check_beacon({**b, 'randomness': '00' * 32}, 42, require_bls=False))
        self.assertTrue(check_beacon({**b, 'chain': 'autre'}, 42, require_bls=False))

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

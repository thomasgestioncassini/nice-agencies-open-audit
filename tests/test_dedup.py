"""V-14 : dédoublonnage refait par l'auditeur sur des données anonymisées synthétiques."""
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from auditor.dedupcheck import check, same

COLS = ['agence', 'plateforme', 'id', 'date', 'note', 'profil', 'compte_vente_achat', 'releve_complet', 'retenu_qualite',
        'retenu_service', 'nb_agences_partageant', 'reponse_agence', 'probleme']
TOK = [f't{i}' for i in range(12)]


def item(i, r, toks, key=None, kind='vendeur', aut=('a1', 'b')):
    return {'id': i, 'date': '2026-10-01', 'r': r, 'kind': kind, 'tok': toks, 'aut': list(aut), 'key': key}


def build(d: Path, rows):
    agencies = [{'id': 'A', 'slug': 'alpha'}, {'id': 'B', 'slug': 'beta'}]
    reviews = {
        'A': {'google': {'complete': True, 'items': [item('g1', 5, TOK, 'k1'), item('g2', 4, TOK[:3], None, 'locataire')]},
              'opinionsystem': {'complete': True, 'items': [item('o1', 5, TOK[1:], 'k1x')]}},
        'B': {'google': {'complete': True, 'items': [item('g9', 5, TOK, 'k1')]}},
    }
    with zipfile.ZipFile(d / 'calcul.zip', 'w') as z:
        z.writestr('data/agencies.json', json.dumps({'agencies': agencies}))
        for k, v in reviews.items():
            z.writestr(f'data/reviews/{k}.json', json.dumps(v))
    (d / 'parametres.json').write_text(json.dumps({'profils_ecartes': ['locataire', 'bailleur', 'syndic']}))
    (d / 'agences.csv').write_text('agence;rang_publie\nalpha;1\nbeta;2\n')
    lines = [';'.join(COLS)] + [';'.join(str(r.get(c, '')) for c in COLS) for r in rows]
    (d / 'avis-elementaires.csv').write_text('\n'.join(lines) + '\n')


OK_ROWS = [
    # alpha : google g1 = opinionsystem o1 (doublon : la copie Opinion System est conservée) ; g2 de locataire écarté
    {'agence': 'alpha', 'plateforme': 'opinionsystem', 'id': 'o1', 'retenu_qualite': 1, 'retenu_service': 1, 'nb_agences_partageant': 1},
    {'agence': 'alpha', 'plateforme': 'google', 'id': 'g1', 'retenu_qualite': 0, 'retenu_service': 0, 'nb_agences_partageant': 2},
    {'agence': 'alpha', 'plateforme': 'google', 'id': 'g2', 'retenu_qualite': 0, 'retenu_service': 0, 'nb_agences_partageant': 1},
    {'agence': 'beta', 'plateforme': 'google', 'id': 'g9', 'retenu_qualite': 1, 'retenu_service': 1, 'nb_agences_partageant': 2},
]


class Dedup(unittest.TestCase):
    def run_with(self, rows):
        with tempfile.TemporaryDirectory() as t:
            build(Path(t), rows)
            return check(Path(t))

    def test_rule(self):
        a = {'tok': set(TOK), 'r': 5, 'aut': ('x', None), 'date': '2026-01-01'}
        b = {'tok': set(TOK[1:]), 'r': 5, 'aut': ('y', None), 'date': '2026-01-01'}
        self.assertTrue(same(a, b))                       # 11 mots sur 12 en commun
        c = {'tok': set(), 'r': 4.5, 'aut': ('x', 'b'), 'date': '2026-02-10'}
        d = {'tok': set(), 'r': 5, 'aut': ('x', None), 'date': '2026-01-01'}
        self.assertTrue(same(c, d))                       # sans texte : même prénom, note et dates proches
        self.assertFalse(same(c, {**d, 'date': '2025-11-01'}))

    def test_consistent_files_pass(self):
        r = self.run_with(OK_ROWS)
        self.assertEqual(r['status'], 'conforme', r)

    def test_duplicate_counted_twice_is_detected(self):
        rows = [dict(x) for x in OK_ROWS]
        rows[1]['retenu_qualite'] = 1                      # le doublon google serait compté en plus
        r = self.run_with(rows)
        self.assertEqual(r['status'], 'ecarts')
        self.assertEqual([x['agence'] for x in r['ecarts_qualite']], ['alpha'])

    def test_hidden_sharing_is_detected(self):
        rows = [dict(x) for x in OK_ROWS]
        rows[3]['nb_agences_partageant'] = 1               # avis partagé présenté comme propre à beta
        r = self.run_with(rows)
        self.assertEqual([x['agence'] for x in r['ecarts_partage']], ['beta'])

    def test_missing_package_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(check(Path(t))['status'], 'non_verifie')


if __name__ == '__main__':
    unittest.main()


class Categories(unittest.TestCase):
    def test_categories_from_exports(self):
        from auditor.bias import categories
        ag = {'orpi-agence-x': {}, 'cabinet-y': {}, 'agence-z': {}}
        src = {'cabinet-y': {'url_site': 'https://www.century21-y.com/', 'activites': 'vente'},
               'agence-z': {'url_site': 'https://z.fr', 'activites': 'vente,gestion'}, 'orpi-agence-x': {'activites': ''}}
        crit = {'agence-z': [{'critere': 'Estimation en ligne du prix de vente', 'points': '1', 'max': '1'}],
                'cabinet-y': [{'critere': 'Estimation en ligne du prix de vente', 'points': '0', 'max': '1'}]}
        c = categories(ag, src, crit, ['orpi', 'century21'])
        self.assertEqual(sorted(c['groups']['reseau']), ['cabinet-y', 'orpi-agence-x'])
        self.assertEqual(c['groups']['vente_seule'], ['cabinet-y'])
        self.assertEqual(c['groups']['vente_et_location_ou_gestion'], ['agence-z'])
        self.assertEqual(c['groups']['estimation_en_ligne'], ['agence-z'])
        self.assertEqual(c['groups']['sans_estimation_en_ligne'], ['cabinet-y'])

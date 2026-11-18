"""Comparateur gestion locative (méthode G1.2) : recalcul indépendant sur un jeu de données construit à la main."""
import json
import tempfile
import unittest
from pathlib import Path

from auditor import gestion as G
from tests.helpers import ROOT, write_rows

CFG = json.loads((ROOT / 'config' / 'methodology-gestion-g12.json').read_text(encoding='utf-8'))
AG_HEAD = ['agence_id', 'slug', 'nom', 'editeur', 'groupe_publie', 'rang_publie', 'rang_indicatif_publie', 'note_publiee', 'avis',
           'service', 'transparence', 'mentions_legales', 'information', 'anciennete', 'avis_comptes_publies',
           'semestres_actifs_publies', 'date_anciennete']
AV_HEAD = ['agence_id', 'plateforme', 'id', 'date', 'note', 'poids_partage', 'retenu', 'service', 'reponse']
CR_HEAD = ['agence_id', 'pilier', 'famille', 'critere', 'points', 'max']


def dataset(d: Path, ag, av, cr, m_ref):
    (d / 'gestion-parametres.json').write_text(json.dumps({'date_releve': '2026-11-18', 'moyenne_reference_M_REF': m_ref}))
    write_rows(d / 'gestion-agences.csv', AG_HEAD, ag)
    write_rows(d / 'gestion-avis.csv', AV_HEAD, av)
    write_rows(d / 'gestion-criteres.csv', CR_HEAD, cr)


def review(i, n, date='2026-10-01', note='5', k='1.0000', retenu='1', service='ok', reponse='', pf='google'):
    return {'agence_id': i, 'plateforme': pf, 'id': f'{i}-{n}', 'date': date, 'note': note, 'poids_partage': k,
            'retenu': retenu, 'service': service, 'reponse': reponse}


class Gestion(unittest.TestCase):
    def build(self):
        """Agence 1 : 16 avis sur 3 semestres (évaluée) ; agence 2 : 2 avis (peu évaluée) ; agence 3 : aucun avis."""
        av = [review('1', n, date=d) for n, d in enumerate(['2026-10-01'] * 6 + ['2026-03-01'] * 5 + ['2025-07-01'] * 5)]
        av += [review('1', 99, date='2026-09-01', note='2', reponse='1', service='probleme')]
        av += [review('1', 98, date='2026-09-01', note='2', retenu='0', reponse='0', service='')]   # doublon d'une autre plateforme
        av += [review('2', 1, note='4'), review('2', 2, note='5', k='0.5000')]
        cr = [{'agence_id': i, 'pilier': p, 'famille': '', 'critere': c, 'points': pts, 'max': mx}
              for i in '123' for p, c, pts, mx in (('hono', 'a', '25', '25'), ('hono', 'b', '0', '75'), ('conf', 'c', '10', '20'),
                                                   ('info', 'd', '1', '1'), ('info', 'e', '', ''))]
        notes = [float(x['note']) for x in av]
        m_ref = round(sum(notes) / len(notes), 3)
        res = None
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            ag = [{'agence_id': i, 'slug': f'a{i}', 'nom': f'Agence {i}', 'date_anciennete': '2006-11-01'} for i in '123']
            dataset(d, [{**a, **{k: '' for k in AG_HEAD if k not in a}} for a in ag], av, cr, m_ref)
            res = G.recalculate(d, CFG)
        return res, av, cr, m_ref

    def test_formulas(self):
        res, _, _, m_ref = self.build()
        a = res['agencies']
        self.assertEqual(res['m_ref'], m_ref)
        self.assertEqual(a['1']['group'], 'évaluée')
        self.assertEqual(a['1']['semesters'], 3)
        self.assertEqual(a['1']['n'], 17.0)
        self.assertEqual(a['2']['group'], 'peu évaluée')
        self.assertEqual(a['2']['n'], 1.5)
        self.assertEqual(a['3']['group'], 'données insuffisantes')
        self.assertEqual(a['3']['pillars']['avis'], 50)
        self.assertEqual(a['3']['pillars']['serv'], 50)
        # réponses : 2 avis Google négatifs (doublon compris), 1 réponse -> (1 + 2) / (2 + 4)
        self.assertEqual(a['1']['detail']['response'], 50.0)
        # agence 2 : aucun avis négatif -> 75 ; moins de 10 avis lus -> 50
        self.assertEqual(a['2']['detail']['response'], 75)
        self.assertEqual(a['2']['pillars']['serv'], round((75 * 40 + 50 * 60) / 100, 1))
        self.assertEqual(a['1']['pillars']['hono'], 25.0)
        self.assertEqual(a['1']['pillars']['info'], 100.0)          # critère sans maximum : non applicable
        self.assertEqual(a['1']['pillars']['anc'], 100.0)
        self.assertEqual(a['1']['rank'], 1)
        self.assertEqual(a['2']['rank_ind'], 1)

    def test_detects_altered_publication(self):
        res, av, cr, m_ref = self.build()
        a = res['agencies']
        ag = []
        for i, r in a.items():
            row = {'agence_id': i, 'slug': f'a{i}', 'nom': r['nom'], 'editeur': 'non', 'groupe_publie': r['group'],
                   'rang_publie': r.get('rank', ''), 'rang_indicatif_publie': r.get('rank_ind', ''), 'note_publiee': f"{r['note']:.2f}",
                   'avis_comptes_publies': f"{r['n']:.2f}", 'semestres_actifs_publies': r['semesters'], 'date_anciennete': '2006-11-01'}
            for p, c in G.PUB_COL.items():
                row[c] = '' if r['pillars'][p] is None else f"{r['pillars'][p]:.1f}"
            ag.append(row)
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            dataset(d, ag, av, cr, m_ref)
            self.assertEqual(G.check(d, CFG)['status'], 'conforme')
            ag[1]['note_publiee'] = f"{float(ag[1]['note_publiee']) + 0.5:.2f}"       # note publiée plus haute que les données
            ag[0]['groupe_publie'] = 'peu évaluée'
            dataset(d, ag, av, cr, m_ref)
            c = G.check(d, CFG)
            self.assertEqual(c['status'], 'divergences')
            self.assertEqual({x['agence'] for x in c['divergent']}, {'a1', 'a2'})

    def test_absent_files(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(G.check(Path(t), CFG)['status'], 'non_execute')

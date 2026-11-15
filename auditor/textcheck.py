"""Conformité au TEXTE de la méthode, distincte de la reproduction du calcul de production.

Reproduire le site prouve que ses notes découlent de ses données selon SES règles. Cela ne prouve pas que ces règles
sont celles que le texte public annonce. Ce module recalcule le classement en remplaçant chaque règle qui contredit le
texte, ou que le texte laisse ambiguë, par sa lecture la plus littérale, et mesure l'effet sur les notes et les rangs.
Ces variantes sont des diagnostics : elles ne remplacent jamais les notes officielles.
"""
from __future__ import annotations

import html
import re
import statistics
from pathlib import Path

from .recalculate import TEXT_VARIANTS, recalculate


def _diff(base: dict, var: dict, watch: list[str]) -> dict:
    moved = {s: var[s]['rank'] - base[s]['rank'] for s in base if var[s]['rank'] != base[s]['rank']}
    notes = sum(1 for s in base if abs(var[s]['note_exact'] - base[s]['note_exact']) >= 0.005)
    top10 = len({s for s in base if base[s]['rank'] <= 10} & {s for s in var if var[s]['rank'] <= 10})
    return {'notes_changees': notes, 'rangs_changes': len(moved),
            'deplacement_median': statistics.median(abs(v) for v in moved.values()) if moved else 0,
            'deplacement_max': max((abs(v) for v in moved.values()), default=0), 'top10_inchanges': top10,
            'agences_suivies': {s: {'rang_production': base[s]['rank'], 'rang_variante': var[s]['rank']}
                                for s in watch if s in base}}


def page_text(path: Path) -> str | None:
    if not path.exists():
        return None
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', path.read_text(encoding='utf-8'), flags=re.S)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t)).replace('\u2019', "'")
    return ' '.join(t.split())


def _norm(x: str) -> str:
    return ' '.join(x.replace('\u2019', "'").split())


def read_text_rules(page: str | None, interpretations: list[dict]) -> dict:
    """Pour un texte de méthode archivé : règles décrites (phrase descriptive présente) et contradictions résiduelles
    (phrase contraire encore présente). Ce contrôle par phrases ne vaut pas relecture complète du texte : il ne détecte
    que les contradictions déjà répertoriées dans config/interpretations.json."""
    if page is None:
        return {'archived': False}
    documented = sorted(i['id'] for i in interpretations if i.get('documented_by') and _norm(i['documented_by']) in page)
    residual = sorted(i['id'] for i in interpretations for c in i.get('contradicted_by', []) if _norm(c) in page)
    open_ = [i for i in interpretations if i['id'] not in documented or i['id'] in residual]
    return {'archived': True, 'documented': documented, 'residual_contradictions': residual,
            'contradictions': [i['id'] for i in open_ if i['kind'] == 'contradiction'],
            'ambiguities': [i['id'] for i in open_ if i['kind'] == 'ambiguite'],
            'undocumented': [i['id'] for i in open_ if i['kind'] == 'non_documente']}


def text_conformity(data_dir, cfg: dict, interpretations: list[dict], watch: list[str], history: list[tuple] = ()) -> dict:
    """history : [(nom du relevé, chemin du texte archivé)] des relevés ANTÉRIEURS. Une contradiction passée reste
    publiée même quand le texte a été corrigé depuis."""
    page = page_text(Path(data_dir) / 'methode-details.html')
    cur = read_text_rules(page, interpretations)
    base = recalculate(data_dir, cfg)['agencies']
    effects = {}
    for v in TEXT_VARIANTS:
        effects[v] = _diff(base, recalculate(data_dir, cfg, {v})['agencies'], watch)
    effects['ensemble'] = _diff(base, recalculate(data_dir, cfg, set(TEXT_VARIANTS))['agencies'], watch)
    past = []
    for name, path in history:
        r = read_text_rules(page_text(Path(path)), interpretations)
        if r['archived'] and (r['contradictions'] or r['ambiguities']):
            past.append({'snapshot': name, 'contradictions': r['contradictions'], 'ambiguities': r['ambiguities']})
    if not cur['archived']:
        doc = coh = 'echec'
    else:
        doc = 'complete' if not cur['undocumented'] and not cur['contradictions'] and not cur['ambiguities'] else 'partielle'
        coh = 'contradictions_residuelles' if cur['contradictions'] or cur['residual_contradictions'] else \
            'aucune_contradiction_repertoriee'
    return {'documentation': doc, 'coherence': coh, 'history': 'ecarts_anterieurs' if past else 'aucun_ecart_anterieur',
            'current': cur, 'past': past, 'effects': effects}

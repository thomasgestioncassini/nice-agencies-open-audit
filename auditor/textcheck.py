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


def text_conformity(data_dir, cfg: dict, interpretations: list[dict], watch: list[str]) -> dict:
    """Le texte de la méthode archivé avec le relevé (methode-details.html) est lu : une règle dont la phrase
    descriptive y figure est « documentée » ; sinon elle garde son classement d'origine."""
    page = page_text(Path(data_dir) / 'methode-details.html')
    documented = {i['id'] for i in interpretations if page and i.get('documented_by')
                  and ' '.join(i['documented_by'].split()) in page}
    base = recalculate(data_dir, cfg)['agencies']
    effects = {}
    for v in TEXT_VARIANTS:
        effects[v] = _diff(base, recalculate(data_dir, cfg, {v})['agencies'], watch)
    effects['ensemble'] = _diff(base, recalculate(data_dir, cfg, set(TEXT_VARIANTS))['agencies'], watch)
    open_ = [i for i in interpretations if i['id'] not in documented]
    contradictions = [i['id'] for i in open_ if i['kind'] == 'contradiction']
    ambiguities = [i['id'] for i in open_ if i['kind'] == 'ambiguite']
    undocumented = [i['id'] for i in open_ if i['kind'] == 'non_documente']
    status = 'ecarts' if contradictions or ambiguities else ('incomplet' if undocumented else 'conforme')
    if page is None:
        status = 'echec'
    return {'status': status, 'text_archived': page is not None, 'documented_in_archived_text': sorted(documented),
            'contradictions': contradictions, 'ambiguities': ambiguities, 'undocumented': undocumented,
            'effects': effects}

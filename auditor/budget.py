"""Compteur de dépenses des IA, conservé dans le dépôt (budget/<AAAA-MM>.json).

Avant chaque appel, le coût est estimé de façon PRUDENTE (sortie maximale, ~3 caractères par jeton) ; si la dépense du
mois plus cette estimation dépasse le seuil d'arrêt (12 $ par fournisseur, sous les plafonds de 15 $ des fournisseurs),
l'appel n'est pas fait et le rapport l'indique. Après l'appel, le coût réel (jetons facturés) est enregistré.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


class BudgetExceeded(RuntimeError):
    pass


def price(cfg: dict, tokens_in: int, tokens_out: int) -> float:
    long = cfg.get('long_context_threshold') and tokens_in > cfg['long_context_threshold']
    pin = cfg['usd_per_m_input_long'] if long else cfg['usd_per_m_input']
    pout = cfg['usd_per_m_output_long'] if long else cfg['usd_per_m_output']
    return tokens_in / 1e6 * pin + tokens_out / 1e6 * pout


class Ledger:
    def __init__(self, root: Path, models: dict, month: str | None = None):
        self.models = models
        self.month = month or dt.date.today().strftime('%Y-%m')
        self.path = root / 'budget' / f'{self.month}.json'
        self.data = json.loads(self.path.read_text(encoding='utf-8')) if self.path.exists() else {'month': self.month, 'providers': {}}

    def spent(self, slot: str) -> float:
        return sum(c['usd'] for c in self.data['providers'].get(slot, {}).get('calls', []))

    def estimate(self, slot: str, prompt_chars: int) -> tuple[int, float]:
        b = self.models['budget']
        cfg = self.models['providers'][slot]
        tin = int(prompt_chars / b['chars_per_token_estimate']) + 1
        return tin, price(cfg, tin, cfg['max_output_tokens'])

    def check(self, slot: str, prompt_chars: int) -> float:
        b = self.models['budget']
        tin, est = self.estimate(slot, prompt_chars)
        if tin > b['max_input_tokens']:
            raise BudgetExceeded(f'entrée estimée à {tin} jetons, au-delà de la limite de {b["max_input_tokens"]}')
        if self.spent(slot) + est > b['monthly_stop_usd_per_provider']:
            raise BudgetExceeded(f'IA {slot} : dépense du mois {self.spent(slot):.2f} $ + estimation {est:.2f} $ '
                                 f'> seuil d’arrêt {b["monthly_stop_usd_per_provider"]:.2f} $')
        return est

    def record(self, slot: str, purpose: str, tokens_in: int, tokens_out: int, report_id: str) -> float:
        usd = price(self.models['providers'][slot], tokens_in, tokens_out)
        p = self.data['providers'].setdefault(slot, {'model': self.models['providers'][slot]['model'], 'calls': []})
        p['calls'].append({'utc': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'), 'report': report_id,
                           'purpose': purpose, 'tokens_in': tokens_in, 'tokens_out': tokens_out, 'usd': round(usd, 4)})
        self.save()
        return usd

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

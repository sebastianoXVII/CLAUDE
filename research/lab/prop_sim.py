"""Simulatore di challenge prop. Regole Topstep 50K verificate il 2026-11-10 su help.topstep.com:
- Maximum Loss Limit 2.000 $, trailing sul saldo di fine giornata; violazione anche intraday sul P&L non realizzato;
  smette di salire quando raggiunge il saldo iniziale.
- Consistency: il giorno migliore deve stare sotto il 55% del target, altrimenti il target sale a giorno_migliore / 0,55.
- Profit target 3.000 $ (da fonte secondaria, NON verificato sul sito ufficiale).
Input: lista di giorni (P&L del giorno in $, minimo intraday del P&L cumulato del giorno in $, <= 0)."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Rules:
    start: float = 50_000.0
    target: float = 3_000.0
    mll: float = 2_000.0
    consistency: float = 0.55   # 0 = nessuna regola di consistency
    trailing: bool = True       # False = pavimento statico a start - mll
    daily_loss: float = 0.0     # 0 = nessun limite giornaliero; altrimenti perdita intraday massima del giorno


def run_challenge(days, rules: Rules) -> dict:
    bal, hwm = rules.start, rules.start
    floor = rules.start - rules.mll
    best = 0.0
    for i, (pnl, intra_min) in enumerate(days, start=1):
        if bal + min(intra_min, 0.0) <= floor or bal + pnl <= floor:
            return {"outcome": "fail", "days": i}
        if rules.daily_loss and min(intra_min, pnl, 0.0) <= -rules.daily_loss:
            return {"outcome": "fail", "days": i}
        bal += pnl
        best = max(best, pnl)
        need = max(rules.target, best / rules.consistency) if rules.consistency else rules.target
        if bal - rules.start >= need:
            return {"outcome": "pass", "days": i}
        if rules.trailing:
            hwm = max(hwm, bal)
            floor = min(hwm - rules.mll, rules.start)
    return {"outcome": "open", "days": len(days)}


def scale(pool, n: float):
    return [(p * n, m * n) for p, m in pool]


def monte_carlo(pool, rules: Rules, n_sims: int = 5000, max_days: int = 120, block: int = 5, seed: int = 0) -> dict:
    """Block bootstrap dei giorni storici (blocchi consecutivi per preservare la dipendenza fra giorni)."""
    rng = np.random.default_rng(seed)
    n = len(pool)
    res = {"pass": [], "fail": [], "open": []}
    for _ in range(n_sims):
        seq = []
        while len(seq) < max_days:
            s = int(rng.integers(0, max(n - block, 1)))
            seq.extend(pool[s:s + block])
        r = run_challenge(seq[:max_days], rules)
        res[r["outcome"]].append(r["days"])
    tot = float(n_sims)
    return {"p_pass": len(res["pass"]) / tot, "p_fail": len(res["fail"]) / tot, "p_open": len(res["open"]) / tot,
            "median_days_pass": float(np.median(res["pass"])) if res["pass"] else float("nan"),
            "median_days_fail": float(np.median(res["fail"])) if res["fail"] else float("nan")}


@dataclass(frozen=True)
class FundedRules:
    """Conto funded FundedNext Stellar (verificato su help.fundednext.com il 2026-11-10): perdita max 10% e giornaliera 5%
    statiche sul saldo iniziale; payout a fine ciclo se in profitto (primo ciclo 21 giorni, poi 14), quota trader 80%.
    Modello: al payout il saldo torna al valore iniziale (si preleva tutto il profitto)."""
    start: float = 100_000.0
    mll: float = 10_000.0
    daily_loss: float = 5_000.0
    first_cycle: int = 21
    cycle: int = 14
    split: float = 0.8


def run_funded(days, r: FundedRules) -> dict:
    bal, floor = r.start, r.start - r.mll
    payouts, next_end = [], r.first_cycle
    for i, (pnl, intra_min) in enumerate(days, start=1):
        if bal + min(intra_min, 0.0) <= floor or bal + pnl <= floor or min(intra_min, pnl, 0.0) <= -r.daily_loss:
            return {"payouts": payouts, "breached": True, "days": i}
        bal += pnl
        if i == next_end:
            if bal > r.start:
                payouts.append(r.split * (bal - r.start))
                bal = r.start
            next_end += r.cycle
    return {"payouts": payouts, "breached": False, "days": len(days)}


def monte_carlo_funded(pool, r: FundedRules, n_sims: int = 3000, horizon: int = 252, block: int = 5, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    tot, br, first = [], 0, []
    for _ in range(n_sims):
        seq = []
        while len(seq) < horizon:
            s = int(rng.integers(0, max(len(pool) - block, 1)))
            seq.extend(pool[s:s + block])
        out = run_funded(seq[:horizon], r)
        tot.append(sum(out["payouts"]))
        br += out["breached"]
    tot = np.array(tot)
    return {"payout_medio_anno": float(tot.mean()), "payout_mediano_anno": float(np.median(tot)),
            "p_zero_payout": float((tot == 0).mean()), "p_conto_perso_entro_anno": br / n_sims,
            "p10": float(np.percentile(tot, 10)), "p90": float(np.percentile(tot, 90))}

"""Confronto di programmi prop sul candidato Noise Area NQ (condizionato: NON e' evidenza di edge).
Parametri da research_notes/Gap di mercato testabili/05_prop_firm_regole_2026.md (Topstep verificato; FTMO da sintesi/secondario)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_t6 as R6  # noqa: E402
from lab import prop_sim as P  # noqa: E402

K = 41.0


def pool_with_costs(cost_pts: float) -> list[tuple[float, float]]:
    """Giorni (P&L, minimo intraday) in PUNTI NQ con il costo per trade indicato; ricalcolato dalle serie di T6."""
    base = pd.read_parquet(R6.ROOT / "data" / "nq_noise_area_daily_pool.parquet")  # costruito con costo MNQ 0,85
    tr, armed, _d, _ = R6.trades_for("QQQ", K, 0.85)
    n = tr.groupby("date").size().reindex(base.index, fill_value=0)
    extra = (cost_pts - 0.85) * n
    return list(zip(base["pnl_pts"] - extra, base["intra_min_pts"] - extra))


def two_phase(pool, r1: P.Rules, r2: P.Rules, usd_per_pt: float, n_sims=3000, max_days=250, seed=5) -> dict:
    rng = np.random.default_rng(seed)
    scaled = P.scale(pool, usd_per_pt)
    ok = 0
    days = []
    for _ in range(n_sims):
        seq = []
        while len(seq) < 2 * max_days:
            s = int(rng.integers(0, len(scaled) - 5))
            seq.extend(scaled[s:s + 5])
        a = P.run_challenge(seq[:max_days], r1)
        if a["outcome"] != "pass":
            continue
        b = P.run_challenge(seq[a["days"]:a["days"] + max_days], r2)
        if b["outcome"] == "pass":
            ok += 1
            days.append(a["days"] + b["days"])
    return {"p_pass": ok / n_sims, "median_days_pass": float(np.median(days)) if days else float("nan")}


def main() -> None:
    out = {}
    fut = pool_with_costs(0.85)   # MNQ
    cfd = pool_with_costs(2.0)    # US100 CFD, spread ~1-2 pt round trip (secondario): si usa 2
    cfd_s = pool_with_costs(4.0)  # stress 2x
    halfmean = lambda pl: [(p - 0.5 * np.mean([x for x, _ in pl]), m) for p, m in pl]
    progs = {
        "Topstep 50K (trailing 2K EOD, cons 55%)": ("1", fut, P.Rules(50_000, 3_000, 2_000, 0.55, True, 0.0), [2, 4, 6, 8]),
        "FTMO Futures Pro 50K (trailing 3K EOD, DLL 1K, cons 40%)": ("1", fut, P.Rules(50_000, 3_000, 3_000, 0.40, True, 1_000), [2, 4, 6, 8]),
    }
    for name, (_, pl, rules, sizes) in progs.items():
        for tag, p in (("edge storico", pl), ("edge dimezzato", halfmean(pl))):
            for n in sizes:
                r = P.monte_carlo(P.scale(p, 2.0 * n), rules, n_sims=3000, max_days=120, seed=5)  # n MNQ = 2$/pt ciascuno
                out[f"{name}|{tag}|{n} MNQ"] = r
                print(f"{name} | {tag} | {n} MNQ: passa {r['p_pass']:.0%} brucia {r['p_fail']:.0%} | gg mediani {r['median_days_pass']:.0f}")
    f1 = P.Rules(100_000, 10_000, 10_000, 0.0, False, 5_000)
    f2 = P.Rules(100_000, 5_000, 10_000, 0.0, False, 5_000)
    for tag, p in (("edge storico", cfd), ("edge dimezzato", halfmean(cfd)), ("dimezzato + spread 2x", halfmean(cfd_s))):
        for usd in (4, 8, 12, 16, 24):  # $ per punto indice (equivalente a usd/2 MNQ)
            r = two_phase(p, f1, f2, usd)
            out[f"FTMO 2-Step 100K CFD|{tag}|{usd}$/pt"] = r
            print(f"FTMO 2-Step 100K CFD (statico 10%, daily 5%) | {tag} | {usd}$/pt (= {usd/2:.0f} MNQ): supera ENTRAMBE le fasi {r['p_pass']:.0%} | gg mediani {r['median_days_pass']:.0f}")
    (R6.OUT / "prop_compare_noise_area_nq.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

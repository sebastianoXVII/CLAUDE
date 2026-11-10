"""Test del forward test giornaliero (codice congelato di T6, applicato ai giorni nuovi). Scritti prima del codice."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forward import noise_area_forward as F  # noqa: E402


def synth(days=25, seed=0, trend_last=True):
    rng = np.random.default_rng(seed)
    frames, p = [], 400.0
    for d in pd.bdate_range("2026-09-01", periods=days):
        idx = pd.date_range(f"{d.date()} 09:30", f"{d.date()} 15:59", freq="1min", tz="America/New_York")
        steps = rng.normal(0, 0.05, len(idx))
        if trend_last and d == pd.bdate_range("2026-09-01", periods=days)[-1]:
            steps += 0.03  # ultimo giorno in forte trend rialzista
        px = p + np.cumsum(steps)
        frames.append(pd.DataFrame({"open": px, "high": px + 0.02, "low": px - 0.02, "close": px, "volume": 1000.0}, index=idx))
        p = px[-1]
    b = pd.concat(frames)
    b.index = b.index.tz_convert("UTC")
    return b


def test_new_rows_only_after_warmup_and_not_duplicated():
    b = synth()
    rows = F.forward_rows(b, b, already=set(), k=41.0, cost=0.85)
    days = sorted({r["date"] for r in rows})
    assert all(d >= "2026-09-21" for d in days)  # servono 14 giorni completi + giorno precedente
    again = F.forward_rows(b, b, already=set(days), k=41.0, cost=0.85)
    assert again == []


def test_trend_day_produces_long_and_row_fields():
    b = synth()
    rows = F.forward_rows(b, b, already=set(), k=41.0, cost=0.85)
    last = [r for r in rows if r["date"] == "2026-10-05"]
    assert last and last[0]["side"] == 1
    assert {"date", "side", "entry_time", "exit_time", "entry", "exit", "reason", "net_pts_nq", "code_version"} <= set(last[0])


def test_no_trade_days_are_logged_as_flat():
    b = synth(trend_last=False)
    rows = F.forward_rows(b, b, already=set(), k=41.0, cost=0.85)
    days = {r["date"] for r in rows}
    assert "2026-10-05" in days  # ogni giorno valido viene registrato, anche senza trade (riga 'flat')

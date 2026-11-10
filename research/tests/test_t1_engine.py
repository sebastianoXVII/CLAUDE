"""Test del motore T1 (pre-registrazione: research/preregistration/T1_momentum_ultima_mezzora.md).
Scritti PRIMA dell'implementazione (TDD). Dati sintetici a 1 minuto in UTC, come quelli di Dukascopy."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import t1_engine as E  # noqa: E402

TZ = "America/New_York"


def make_bars(days: dict[str, dict[str, float]]) -> pd.DataFrame:
    """days: {'2024-03-11': {'09:59': p, '15:29': p, ...}} con orari ET = minuto d'inizio barra; close = p."""
    rows = []
    for d, pts in days.items():
        for hhmm, p in pts.items():
            ts = pd.Timestamp(f"{d} {hhmm}", tz=TZ).tz_convert("UTC")
            rows.append((ts, p, p, p, p, 1.0))
    df = pd.DataFrame(rows, columns=["ts_utc", "open", "high", "low", "close", "volume"]).set_index("ts_utc")
    return df.sort_index()


def day(p10, p1500, p1530, p1600):
    # il prezzo AL tempo t e' il close della barra che inizia a t-1m
    return {"09:59": p10, "14:59": p1500, "15:29": p1530, "15:59": p1600}


# ---------- price_at ----------

def test_price_at_uses_close_of_bar_starting_one_minute_before():
    b = make_bars({"2024-03-11": {"09:58": 99.0, "09:59": 100.0, "10:00": 555.0}})
    b.index = b.index.tz_convert(TZ)
    assert E.price_at(b, pd.Timestamp("2024-03-11 10:00", tz=TZ)) == 100.0  # mai la barra delle 10:00 (futuro)


def test_price_at_falls_back_within_two_minutes_else_nan():
    b = make_bars({"2024-03-11": {"09:57": 100.0}})
    b.index = b.index.tz_convert(TZ)
    assert E.price_at(b, pd.Timestamp("2024-03-11 10:00", tz=TZ)) == 100.0  # 2 minuti di buco: ok
    b2 = make_bars({"2024-03-11": {"09:56": 100.0}})
    b2.index = b2.index.tz_convert(TZ)
    assert np.isnan(E.price_at(b2, pd.Timestamp("2024-03-11 10:00", tz=TZ)))  # 3 minuti: NaN


# ---------- daily_points ----------

def test_daily_points_r1_uses_previous_close_and_last_pts():
    b = make_bars({"2024-03-11": day(100, 100, 100, 100), "2024-03-12": day(102, 101, 103, 104)})
    d = E.daily_points(b, window=1)
    row = d.loc["2024-03-12"]
    assert row["r1"] == pytest.approx(np.log(102 / 100))
    assert row["r12"] == pytest.approx(np.log(103 / 101))
    assert row["last_pts"] == pytest.approx(1.0)


def test_daily_points_handles_dst_summer_day():
    # luglio = EDT (UTC-4): gli orari ET devono restare corretti
    b = make_bars({"2024-07-09": day(100, 100, 100, 100), "2024-07-10": day(101, 101, 101, 99)})
    d = E.daily_points(b, window=1)
    assert d.loc["2024-07-10", "last_pts"] == pytest.approx(-2.0)


def test_half_day_without_1600_bar_is_dropped_and_not_used_as_prev_close():
    b = make_bars({
        "2024-11-27": day(100, 100, 100, 100),
        "2024-11-29": {"09:59": 50, "12:59": 50},  # mezza sessione: niente 15:00/15:30/16:00
        "2024-12-02": day(110, 110, 110, 110),
    })
    d = E.daily_points(b, window=1)
    assert pd.Timestamp("2024-11-29") not in d.index
    assert d.loc["2024-12-02", "r1"] == pytest.approx(np.log(110 / 100))


def test_threshold_has_no_lookahead():
    days = {f"2024-01-{i:02d}": day(100 + i, 100, 100, 100) for i in range(2, 31) if pd.Timestamp(f"2024-01-{i:02d}").weekday() < 5}
    b = make_bars(days)
    d1 = E.daily_points(b, window=5)
    last = list(days)[-1]
    days[last] = day(10_000, 100, 100, 100)  # cambia SOLO il r1 dell'ultimo giorno
    d2 = E.daily_points(make_bars(days), window=5)
    assert d1.loc[last, "thr"] == pytest.approx(d2.loc[last, "thr"])


# ---------- varianti e costi ----------

def synthetic_daily(n=300, seed=0):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2017-01-02", periods=n)
    r1 = rng.normal(0, 0.01, n)
    return pd.DataFrame({"r1": r1, "r12": np.zeros(n), "last_pts": np.sign(r1) * 2.0, "thr": np.full(n, 0.005)}, index=idx)


def test_v1_pnl_is_sign_times_move_minus_cost():
    d = synthetic_daily()
    v = E.run_variants(d, cost=0.5)
    pnl, traded = v["V1"]
    assert traded.all()
    assert np.allclose(pnl, 1.5)


def test_v2_trades_only_above_threshold_and_zero_otherwise():
    d = synthetic_daily()
    pnl, traded = E.run_variants(d, cost=0.5)["V2"]
    assert (traded == (d["r1"].abs() > d["thr"])).all()
    assert (pnl[~traded] == 0).all()


def test_benchmark_is_always_long():
    d = synthetic_daily()
    pnl, traded = E.run_variants(d, cost=0.5)["BENCH_long"]
    assert traded.all()
    assert np.allclose(pnl, d["last_pts"] - 0.5)


# ---------- statistica ----------

def test_holm_matches_textbook_example():
    adj = E.holm({"a": 0.01, "b": 0.04, "c": 0.03})
    assert adj["a"] == pytest.approx(0.03)
    assert adj["c"] == pytest.approx(0.06)
    assert adj["b"] == pytest.approx(0.06)  # monotonicita'


def test_nw_t_positive_for_strong_positive_mean_and_near_zero_for_noise():
    rng = np.random.default_rng(1)
    assert E.nw_t(rng.normal(1.0, 1.0, 1000)) > 10
    assert abs(E.nw_t(rng.normal(0.0, 1.0, 1000))) < 4


def test_metrics_basic_values():
    pnl = pd.Series([2.0, -1.0, 2.0, 0.0], index=pd.bdate_range("2020-01-01", periods=4))
    traded = pd.Series([True, True, True, False], index=pnl.index)
    m = E.metrics(pnl, traded, usd_per_pt=50)
    assert m["trade"] == 3
    assert m["win_rate"] == pytest.approx(2 / 3)
    assert m["payoff"] == pytest.approx(2.0)
    assert m["profit_factor"] == pytest.approx(4.0)
    assert m["max_dd_usd"] == pytest.approx(-50.0)
    assert m["expectancy_usd_per_trade"] == pytest.approx(50.0)


def test_verdict_in_sample_requires_all_criteria():
    ok = {"t_nw": 3.5, "media_pt_stress2x": 0.1, "p_holm": 0.01, "anni_positivi": "6/7", "diff_vs_bench_pt_medio": 0.2}
    assert E.verdict(ok, "in_sample")[1] is True
    for k, bad in [("t_nw", 2.9), ("media_pt_stress2x", -0.01), ("p_holm", 0.06), ("anni_positivi", "4/7"), ("diff_vs_bench_pt_medio", -0.1)]:
        assert E.verdict({**ok, k: bad}, "in_sample")[1] is False, k


def test_verdict_holdout_needs_t_above_1_5():
    assert E.verdict({"t_nw": 1.6}, "holdout")[1] is True
    assert E.verdict({"t_nw": 1.4}, "holdout")[1] is False

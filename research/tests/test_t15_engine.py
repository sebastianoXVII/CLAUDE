import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import t15_engine as E  # noqa: E402


def daily(closes, n_bars=1000, start="2015-01-01"):
    idx = pd.bdate_range(start, periods=len(closes))
    return pd.DataFrame({"close": np.asarray(closes, float), "n_bars": n_bars}, index=idx)


def test_returns_skip_days_with_few_bars():
    d = daily([100, 110, 121, 133.1])
    d.iloc[2, d.columns.get_loc("n_bars")] = 50
    r = E.returns(d)
    assert list(r.index) == [d.index[1], d.index[3]]
    assert np.isclose(r.iloc[0], 0.10) and np.isclose(r.iloc[1], 133.1 / 110 - 1)


def test_signal_v1_sign_of_252_day_return_and_nan_before():
    c = pd.Series(np.r_[np.full(252, 100.0), 101.0, 99.0], index=pd.bdate_range("2015-01-01", periods=254))
    s = E.signal(c, "V1")
    assert s.iloc[:252].isna().all()
    assert s.iloc[252] == 1 and s.iloc[253] == -1


def test_signal_v2_mean_of_three_signs():
    c = pd.Series(np.linspace(100, 200, 300), index=pd.bdate_range("2015-01-01", periods=300))
    c.iloc[-1] = c.iloc[-22] - 1  # 21-day return negative, 63 and 252 positive
    s = E.signal(c, "V2")
    assert np.isclose(s.iloc[-1], 1 / 3)


def test_vol_is_ewma_com60_annualised():
    r = pd.Series(0.01, index=pd.bdate_range("2015-01-01", periods=200))
    assert np.isclose(E.ewma_vol(r).iloc[-1], 0.01 * np.sqrt(261))


def test_positions_scale_and_cap():
    sig = pd.Series([1.0, -1.0, 1.0])
    vol = pd.Series([0.20, 0.40, 0.05])
    p = E.positions(sig, vol)
    assert list(p) == [2.0, -1.0, 4.0]


def test_instrument_pnl_uses_previous_position_costs_on_change_and_financing():
    idx = pd.bdate_range("2015-01-01", periods=4)
    pos = pd.Series([np.nan, 1.0, 1.0, -1.0], index=idx)
    r = pd.Series([0.0, 0.02, 0.01, -0.03], index=idx)
    out = E.instrument_pnl(pos, r, cost=0.0002, fin=0.03)
    # day 2: held 1.0 from day 1 -> +0.01 minus financing; day 3: +0.03 (short from day 3 applies from day 4)
    assert np.isclose(out["gross"].iloc[2], 0.01) and np.isclose(out["gross"].iloc[3], -0.03)
    assert np.isclose(out["tcost"].iloc[1], 1.0 * 0.0001) and np.isclose(out["tcost"].iloc[3], 2.0 * 0.0001)
    assert np.isclose(out["fcost"].iloc[2], 0.03 / 252)


def test_portfolio_equal_weight_over_available_instruments():
    idx = pd.bdate_range("2015-01-01", periods=3)
    a = pd.DataFrame({"gross": [0.0, 0.02, 0.02], "tcost": 0.0, "fcost": 0.0, "avail": [True, True, True]}, index=idx)
    b = pd.DataFrame({"gross": [0.0, 0.0, 0.04], "tcost": 0.0, "fcost": 0.0, "avail": [False, False, True]}, index=idx)
    p = E.portfolio({"A": a, "B": b}, cost_mult=1.0)
    assert np.isclose(p.iloc[1], 0.02) and np.isclose(p.iloc[2], 0.03)


def test_instrument_leaves_portfolio_after_its_last_data_day():
    idx = pd.bdate_range("2015-01-01", periods=4)
    a = pd.DataFrame({"gross": [0.0, 0.01, 0.01, 0.01], "tcost": 0.0, "fcost": 0.0, "avail": True}, index=idx)
    b = pd.DataFrame({"gross": [0.0, 0.03], "tcost": 0.0, "fcost": 0.0, "avail": True}, index=idx[:2])
    p = E.portfolio({"A": a, "B": b})
    assert np.isclose(p.iloc[1], 0.02) and np.isclose(p.iloc[3], 0.01)


def test_entry_cost_from_flat_reaches_portfolio():
    idx = pd.bdate_range("2015-01-01", periods=3)
    pos = pd.Series([np.nan, 2.0, 2.0], index=idx)
    r = pd.Series([0.0, 0.0, 0.0], index=idx)
    part = E.instrument_pnl(pos, r, cost=1e-4, fin=0.0)
    p = E.portfolio({"A": part})
    assert np.isclose(p.loc[idx[1]], -2.0 * 1e-4 / 2)


# --- Emendamento 2: rotture del dato ---
def _bd(n, start="2015-01-01"):
    return pd.bdate_range(start, periods=n)


def test_segments_no_break_single_segment():
    c = pd.Series(np.linspace(100, 120, 50), index=_bd(50))
    segs = E.segments(c)
    assert len(segs) == 1 and segs[0].equals(c)


def test_segments_split_on_halving_or_doubling():
    v = [100.0] * 10 + [30.0] * 10 + [100.0] * 10   # -70% e +233%
    c = pd.Series(v, index=_bd(30))
    segs = E.segments(c)
    assert [len(s) for s in segs] == [10, 10, 10]


def test_segments_keep_large_but_real_move():
    v = [1.0] * 10 + [0.84] * 10                      # -16% (tipo SNB): nessuna rottura
    segs = E.segments(pd.Series(v, index=_bd(20)))
    assert len(segs) == 1


def test_segments_nonpositive_close_removed_and_breaks():
    v = [20.0] * 5 + [-37.0] + [19.0] * 5            # -5% fra i due lati: senza la regola non spezzerebbe
    c = pd.Series(v, index=_bd(11))
    segs = E.segments(c)
    assert [len(s) for s in segs] == [5, 5]
    assert all((s > 0).all() for s in segs)


def test_segments_exclusion_window_removed_and_breaks():
    c = pd.Series(np.linspace(100, 110, 30), index=_bd(30))
    a, b = c.index[10], c.index[19]
    segs = E.segments(c, exclude=[(str(a.date()), str(b.date()))])
    assert [len(s) for s in segs] == [10, 10]
    assert segs[1].index[0] == c.index[20]


def test_instrument_parts_no_pnl_across_break_and_reentry_after_252():
    rng = np.random.default_rng(0)
    n1, n2 = 400, 400
    p1 = 100 * np.exp(np.cumsum(rng.normal(0.001, 0.01, n1)))
    p2 = p1[-1] * 0.25 * np.exp(np.cumsum(rng.normal(0.001, 0.01, n2)))   # dimezzamento: rottura
    c = pd.Series(np.r_[p1, p2], index=_bd(n1 + n2))
    out = E.instrument_parts(c, "V1", cost=0.0002, fin=0.03)
    assert out.index.equals(c.index)
    k = n1  # primo giorno del secondo segmento
    assert out["gross"].iloc[k] == 0.0                     # nessun P&L a cavallo della rottura
    assert not out["avail"].iloc[k: k + 252].any()         # fuori dal portafoglio durante i 252 giorni di nuova storia
    assert out["avail"].iloc[k + 252:].all()               # posizione dal 253esimo giorno del segmento (come senza rotture)
    # il primo segmento è identico al calcolo senza rotture sul solo primo tratto
    s1 = c.iloc[:n1]; r1 = s1 / s1.shift(1) - 1
    ref = E.instrument_pnl(E.positions(E.signal(s1, "V1"), E.ewma_vol(r1)), r1, 0.0002, 0.03)
    pd.testing.assert_frame_equal(out.iloc[:n1], ref)


def test_portfolio_counts_instrument_out_during_new_segment_history():
    idx = _bd(600)
    rng = np.random.default_rng(1)
    a = pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, 600))), index=idx)
    b = a.copy(); b.iloc[300:] *= 0.3
    pa, pb = E.instrument_parts(a, "V1", 0.0, 0.0), E.instrument_parts(b, "V1", 0.0, 0.0)
    port = E.portfolio({"A": pa, "B": pb})
    day = idx[320]   # B nel nuovo segmento, ancora senza storia: N_t = 1
    assert port.loc[day] == pytest.approx(pa.loc[day, "gross"])


def test_excluded_window_instrument_not_counted_in_portfolio():
    idx = _bd(700)
    rng = np.random.default_rng(2)
    a = pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, 700))), index=idx)
    b = pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, 700))), index=idx)
    pa = E.instrument_parts(a, "V1", 0.0, 0.0)
    pb = E.instrument_parts(b, "V1", 0.0, 0.0, exclude=[(str(idx[300].date()), str(idx[400].date()))])
    port = E.portfolio({"A": pa, "B": pb})
    for day in (idx[350], idx[450]):   # dentro la finestra esclusa e nella nuova storia di B: N_t = 1
        assert port.loc[day] == pytest.approx(pa.loc[day, "gross"])

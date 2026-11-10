"""Test del motore T6 (Noise Area). Specifica: research/preregistration/T6_noise_area_momentum.md. Scritti prima del codice."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import t6_engine as E  # noqa: E402

DEC = E.DECISION_TIMES


def test_decision_times_are_semi_hourly_from_1000_to_1530():
    assert DEC[0] == "10:00" and DEC[-1] == "15:30" and len(DEC) == 12


def test_sigma_is_mean_abs_move_over_previous_14_days_only():
    n = 20
    idx = pd.bdate_range("2024-01-02", periods=n)
    opens = pd.Series(100.0, index=idx)
    p = pd.DataFrame({t: 100.0 for t in DEC}, index=idx)
    p.iloc[:, 0] = [100 + (i % 3) for i in range(n)]  # move a 10:00: 0, 1%, 2%, ...
    sig = E.sigma_table(p, opens)
    day15 = idx[14]
    expected = np.mean([abs((100 + (i % 3)) / 100 - 1) for i in range(14)])
    assert sig.loc[day15, "10:00"] == pytest.approx(expected)
    assert sig.iloc[:14].isna().all().all()  # servono 14 giorni di storia
    p.iloc[14, 0] = 500.0  # il giorno stesso non entra nella sua sigma
    assert E.sigma_table(p, opens).loc[day15, "10:00"] == pytest.approx(expected)


def test_bounds_use_gap_adjusted_reference():
    ub, lb = E.bounds(open_=101.0, prev_close=100.0, sigma=0.01)
    assert ub == pytest.approx(101.0 * 1.01) and lb == pytest.approx(100.0 * 0.99)


def run(prices, vwap, ub, lb, close=100.0):
    return E.simulate_day(dict(zip(DEC, prices)), dict(zip(DEC, vwap)), dict(zip(DEC, ub)), dict(zip(DEC, lb)), close)


def flat(x):
    return [x] * 12


def test_long_entry_held_to_close():
    pr = [102.0] + [103.0] * 11
    tr = run(pr, flat(100.0), flat(101.0), flat(99.0), close=104.0)
    assert len(tr) == 1 and tr[0]["side"] == 1 and tr[0]["entry_time"] == "10:00"
    assert tr[0]["entry"] == 102.0 and tr[0]["exit"] == 104.0 and tr[0]["reason"] == "close"


def test_trailing_stop_max_of_band_and_vwap_only_at_decision_times():
    pr = [102.0, 103.0, 102.5] + [103.0] * 9
    vw = [100.0, 100.0, 102.8] + [102.8] * 9  # alle 11:00 il VWAP sale sopra il prezzo -> stop
    tr = run(pr, vw, flat(101.0), flat(99.0), close=110.0)
    assert tr[0]["exit_time"] == "11:00" and tr[0]["exit"] == 102.5 and tr[0]["reason"] == "stop"


def test_no_reentry_at_same_decision_time_after_stop_but_allowed_later():
    pr = [102.0, 102.5, 104.0] + [104.0] * 9
    vw = [100.0, 103.0, 103.0] + [103.0] * 9  # 10:30 stop (102.5 < 103); 11:00 prezzo 104 > max(UB, VWAP)
    tr = run(pr, vw, flat(101.0), flat(99.0), close=105.0)
    assert [t["entry_time"] for t in tr] == ["10:00", "11:00"]
    assert tr[0]["exit_time"] == "10:30"


def test_reversal_on_opposite_band():
    pr = [102.0, 98.0] + [97.0] * 10
    tr = run(pr, flat(100.0), flat(101.0), flat(99.0), close=96.0)
    assert [(t["side"], t["entry_time"], t["exit_time"]) for t in tr] == [(1, "10:00", "10:30"), (-1, "10:30", "16:00")]
    assert tr[0]["reason"] == "reversal"


def test_no_trade_inside_noise_area():
    assert run(flat(100.0), flat(100.0), flat(101.0), flat(99.0)) == []


def test_day_inputs_from_bars_vwap_excludes_decision_bar():
    idx = pd.date_range("2024-03-12 09:30", "2024-03-12 15:59", freq="1min", tz="America/New_York")
    b = pd.DataFrame({"open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0, "volume": 1.0}, index=idx)
    b.loc[pd.Timestamp("2024-03-12 10:00", tz="America/New_York"), ["high", "low", "close", "volume"]] = [200, 200, 200, 1e6]
    d = E.day_inputs(b)
    assert d["open"] == 100.0
    assert d["vwap"]["10:00"] == pytest.approx(100.0)  # la barra delle 10:00 non e' ancora nota alle 10:00
    assert d["prices"]["10:00"] == pytest.approx(100.0)  # P(10:00) = close della barra 09:59
    assert d["vwap"]["10:30"] > 150  # dopo, entra


# ---------- emendamento 2: regola ufficiale degli autori ----------

def test_no_entry_above_band_but_below_vwap():
    assert run(flat(102.0), flat(103.0), flat(101.0), flat(99.0)) == []  # sopra UB ma sotto VWAP: segnale 0


def test_no_churn_between_band_and_vwap():
    pr = [104.0] + [102.0] * 11  # long alle 10:00, poi il prezzo resta fra UB (101) e VWAP (103)
    vw = [100.0] + [103.0] * 11
    tr = run(pr, vw, flat(101.0), flat(99.0), close=102.0)
    assert len(tr) == 1 and tr[0]["exit_time"] == "10:30" and tr[0]["reason"] == "stop"


def test_short_side_stop_is_min_of_lb_and_vwap():
    pr = [98.0, 97.0, 97.5] + [97.5] * 9
    vw = [100.0, 100.0, 97.2] + [97.2] * 9  # alle 11:00 il prezzo sale sopra il VWAP (97.2) -> fine short
    tr = run(pr, vw, flat(101.0), flat(99.0), close=90.0)
    assert len(tr) == 1 and tr[0]["side"] == -1 and tr[0]["exit_time"] == "11:00"


def test_sigma_skips_incomplete_days_without_poisoning_next_14():
    n = 30
    idx = pd.bdate_range("2024-01-02", periods=n)
    opens = pd.Series(100.0, index=idx)
    p = pd.DataFrame({t: 101.0 for t in DEC}, index=idx)
    p.iloc[10, 3] = np.nan  # un giorno incompleto
    sig = E.sigma_table(p, opens)
    assert sig.iloc[20:].notna().all().all()  # i giorni dopo non restano senza sigma
    assert sig.loc[idx[16], "10:00"] == pytest.approx(0.01)  # usa i 14 giorni completi precedenti


def test_dividend_from_adjusted_vs_raw_closes():
    idx = pd.bdate_range("2024-03-14", periods=3)
    raw = pd.Series([500.0, 498.0, 499.0], index=idx)
    # rettifica moltiplicativa: prima dello stacco i prezzi rettificati sono scalati di (1 - D/close_prec)
    D = 1.6
    f_before = 1 - D / 500.0
    adj = pd.Series([500.0 * f_before, 498.0, 499.0], index=idx)
    div = E.dividends_from_closes(adj, raw)
    assert div.loc[idx[1]] == pytest.approx(D, rel=1e-6) and div.loc[idx[0]] == 0 and div.loc[idx[2]] == 0

"""Test del motore T4 (pre-registrazione: research/preregistration/T4_concetti_retail.md). Scritti prima del codice."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import t4_engine as E  # noqa: E402

TZ = "America/New_York"
D = "2024-03-12"


def day(over=None, base=100.0, vol=1.0):
    """RTH 09:30-15:59 piatta a `base`; over = {'HH:MM': (open, high, low, close[, volume])}."""
    idx = pd.date_range(f"{D} 09:30", f"{D} 15:59", freq="1min", tz=TZ)
    df = pd.DataFrame({"open": base, "high": base, "low": base, "close": base, "volume": vol}, index=idx)
    for hhmm, v in (over or {}).items():
        t = pd.Timestamp(f"{D} {hhmm}", tz=TZ)
        df.loc[t, ["open", "high", "low", "close"]] = v[:4]
        if len(v) > 4:
            df.loc[t, "volume"] = v[4]
    return df


# ---------- simulatore ----------

def test_simulate_stop_wins_when_bar_touches_both():
    b = day({"10:00": (100, 103, 97, 100)})
    r = E.simulate(b, start="09:35", side=1, p_in=100, stop=98, target=102)
    assert r["p_out"] == 98 and r["reason"] == "stop"


def test_simulate_target_then_time_exit():
    b = day({"10:00": (100, 102.5, 99.5, 102)})
    assert E.simulate(b, "09:35", 1, 100, stop=98, target=102)["p_out"] == 102
    b2 = day({"15:55": (100, 100, 100, 101)})
    r = E.simulate(b2, "09:35", 1, 100, stop=None, target=None)
    assert r["p_out"] == 101 and r["reason"] == "time"


def test_simulate_short_side_and_custom_last_bar():
    b = day({"11:59": (100, 100, 100, 99), "13:00": (100, 100, 90, 95)})
    r = E.simulate(b, "09:35", -1, 100, stop=None, target=None, last_bar="11:59")
    assert r["p_out"] == 99  # il crollo delle 13:00 non conta


# ---------- C1 ORB ----------

def test_orb_long_with_stop_at_range_low():
    b = day({"09:30": (100, 100.5, 99.0, 100.2), "09:34": (100.2, 101, 100, 100.8)})
    t = E.orb(b)
    assert t["side"] == 1 and t["p_in"] == 100.8 and t["stop"] == 99.0 and t["target"] is None
    assert t["start"] == "09:35"


def test_orb_no_trade_on_doji():
    b = day({"09:30": (100, 101, 99, 100), "09:34": (100, 100, 100, 100)})
    assert E.orb(b) is None


# ---------- C2 gap ----------

def test_gap_fill_short_on_gap_up_with_target_prev_close():
    over = {f"09:3{m}": (100.5, 100.6, 100.4, 100.5) for m in range(0, 4)}  # gap non toccato nei primi 5 minuti
    over["09:34"] = (100.5, 100.5, 100.4, 100.4)
    t = E.gap_fill(day(over), prev_close=100.0)
    assert t["side"] == -1 and t["target"] == 100.0 and t["p_in"] == 100.4 and t["last_bar"] == "11:59"


def test_gap_outside_band_is_skipped():
    assert E.gap_fill(day({"09:30": (100.05, 100.05, 100.05, 100.05)}), prev_close=100.0) is None  # 0,05%
    assert E.gap_fill(day({"09:30": (102, 102, 102, 102)}), prev_close=100.0) is None  # 2%


# ---------- C3 VWAP ----------

def test_vwap_first_deviation_after_1000_trades_back_to_vwap():
    b = day({"09:40": (100, 100, 100, 100, 1000.0), "10:05": (100.5, 100.5, 100.4, 100.4)})
    t = E.vwap_magnet(b)
    assert t["side"] == -1 and t["p_in"] == 100.4 and t["start"] == "10:06"
    assert t["target"] == pytest.approx(100.0, abs=0.01)


def test_vwap_ignores_deviation_before_1000():
    b = day({"09:45": (101, 101, 101, 101)})
    assert E.vwap_magnet(b) is None


# ---------- C4 FVG ----------

def test_fvg_bullish_entry_on_retrace_with_2r_target():
    over = {}
    for m in range(30, 45):
        over[f"09:{m}"] = (100.1, 100.1, 100.1, 100.1)  # apertura piatta: nessun FVG spurio
    for m in range(45, 50):
        over[f"09:{m}"] = (100.0, 100.2, 99.8, 100.1)  # barra 5m #1: high 100.2, low 99.8
    for m in range(50, 55):
        over[f"09:{m}"] = (100.3, 100.8, 100.1, 100.7)  # barra 5m #2: spinta
    for m in range(55, 60):
        over[f"09:{m}"] = (100.7, 101.0, 100.6, 100.9)  # barra 5m #3: low 100.6 > 100.2 -> FVG rialzista
    over["10:10"] = (100.5, 100.5, 100.15, 100.3)  # primo ritorno nel gap
    t = E.fvg(day(over, base=100.9))
    assert t["side"] == 1 and t["p_in"] == pytest.approx(100.2) and t["stop"] == pytest.approx(99.8)
    assert t["target"] == pytest.approx(100.2 + 2 * 0.4) and t["start"] == "10:10" and t["entry_bar_stop"] is True


def test_fvg_none_when_no_gap():
    assert E.fvg(day()) is None


# ---------- emendamento 2 (da code review) ----------

def test_gap_already_touched_in_first_five_minutes_is_skipped():
    b = day({"09:30": (100.5, 100.6, 99.95, 100.4), "09:34": (100.45, 100.5, 100.4, 100.45)})
    assert E.gap_fill(b, prev_close=100.0) is None


def test_fvg_requires_contiguous_5m_bars():
    over = {f"09:{m}": (100.0, 100.2, 99.8, 100.1) for m in range(45, 50)}  # barra 1
    over.update({f"{h}:{m:02d}": (100.7, 101.0, 100.6, 100.9) for h, ms in (("09", range(55, 60)), ("10", range(0, 10))) for m in ms})
    over["10:10"] = (100.5, 100.5, 100.15, 100.3)
    b = day(over, base=100.1)
    b = b.drop(index=[pd.Timestamp(f"{D} 09:{m}", tz=TZ) for m in range(50, 55)])  # halt: manca la barra 5m 09:50
    assert E.fvg(b) is None  # senza contiguita' nascerebbe un FVG fra 09:45 e 10:00 attraverso il buco


def test_fvg_zero_risk_is_skipped():
    over = {f"09:{m}": (100.0, 100.0, 100.0, 100.0) for m in range(45, 50)}
    over.update({f"09:{m}": (100.5, 100.5, 100.5, 100.5) for m in range(50, 55)})
    b = day(over, base=101.0)  # tutte barre piatte: ogni FVG ha rischio nullo
    assert E.fvg(b) is None


def test_stop_gap_through_exits_at_open():
    b = day({"10:00": (97.0, 97.5, 96.5, 97.2)})
    r = E.simulate(b, "09:35", 1, 100, stop=98, target=None)
    assert r["p_out"] == 97.0 and r["reason"] == "stop"
    rs = E.simulate(day({"10:00": (103.0, 103.5, 102.5, 103.2)}), "09:35", -1, 100, stop=102, target=None)
    assert rs["p_out"] == 103.0


def test_entry_bar_checks_stop_only_and_exits_at_stop_price():
    b = day({"10:10": (101.0, 103, 99.0, 100.5)})  # la barra d'ingresso tocca lo stop (99.5) e il target (102)
    r = E.simulate(b, "10:10", 1, 100.2, stop=99.5, target=102, entry_bar_stop=True)
    assert r["p_out"] == 99.5 and r["reason"] == "stop"


def test_short_orb():
    b = day({"09:30": (100, 100.5, 99.5, 99.8), "09:34": (99.8, 99.9, 99.2, 99.3)})
    t = E.orb(b)
    assert t["side"] == -1 and t["stop"] == 100.5

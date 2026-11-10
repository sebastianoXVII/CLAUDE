"""Test del motore T8 (pre-registrazione: research/preregistration/T8_sessioni_liquidita.md). Scritti prima del codice.
Giornata sintetica 24h: dalle 18:00 ET del giorno precedente alle 15:59 del giorno D, barre a 1 minuto."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import t8_engine as E  # noqa: E402

TZ = "America/New_York"
D = pd.Timestamp("2024-03-12")
PREV = "2024-03-11"


def ts(hhmm, prev=False):
    return pd.Timestamp(f"{PREV if prev else D.date()} {hhmm}", tz=TZ)


def day(base=100.0, over=None, prev_over=None):
    idx = pd.date_range(ts("18:00", True), ts("15:59"), freq="1min")
    df = pd.DataFrame({"open": base, "high": base, "low": base, "close": base, "volume": 1.0}, index=idx)
    for o, prev in ((prev_over or {}, True), (over or {}, False)):
        for hhmm, v in o.items():
            df.loc[ts(hhmm, prev), ["open", "high", "low", "close"]] = v
    return df


def setv(over, start, end, v, prev=False):
    for t in pd.date_range(ts(start, prev), ts(end, prev), freq="1min"):
        over[t.strftime("%H:%M")] = v


# ---------- livelli di sessione ----------

def test_asia_range_is_prev_evening_2000_2359():
    b = day(prev_over={"20:10": (100, 103, 99, 100), "19:00": (100, 999, 1, 100)})
    hi, lo = E.asia_range(b, D)
    assert (hi, lo) == (103, 99)  # le 19:00 sono fuori dalla finestra


def test_london_range_0200_0829():
    b = day(over={"02:30": (100, 104, 98, 100), "08:45": (100, 120, 80, 100)})
    assert E.london_range(b, D) == (104, 98)


def test_htf_trend_from_prev_closes():
    closes = pd.Series([100.0] * 19 + [110.0], index=pd.bdate_range("2024-02-12", periods=20))
    assert E.htf_trend(closes) == 1
    assert E.htf_trend(pd.Series([100.0] * 19 + [90.0], index=closes.index)) == -1


# ---------- H8a sweep di Londra dell'Asia ----------

def test_h8a_short_after_asia_high_sweep_and_close_back_inside():
    po = {}
    setv(po, "20:00", "23:59", (100, 101, 99, 100), prev=True)  # Asia 99-101
    ov = {}
    setv(ov, "02:10", "02:14", (101, 102, 100.5, 101.5))  # sweep sopra 101 (barra 5m 02:10)
    setv(ov, "02:15", "02:19", (101.5, 101.5, 100.2, 100.5))  # barra 5m 02:15 chiude dentro (100.5)
    t = E.h8a(day(over=ov, prev_over=po), D, (101, 99))
    assert t["side"] == -1 and t["p_in"] == pytest.approx(100.5) and t["stop"] == pytest.approx(102)
    assert t["target"] == pytest.approx(99) and t["start"] == ts("02:20") and t["last"] == ts("10:59")


def test_h8a_no_trade_if_no_return_within_30_minutes():
    ov = {}
    setv(ov, "02:10", "04:59", (101.5, 102, 101.2, 101.5))  # resta sopra
    assert E.h8a(day(over=ov), D, (101, 99)) is None


# ---------- H8b rottura del box Asia ----------

def test_h8b_acceptance_long_with_mid_stop_and_2r_target():
    ov = {}
    setv(ov, "03:00", "03:04", (100.5, 101.6, 100.5, 101.5))  # prima chiusura 5m oltre 101
    setv(ov, "03:05", "03:19", (101.5, 102, 101.3, 101.8))  # 3 chiusure oltre: accettazione
    t = E.h8b(day(over=ov), D, (101, 99))
    assert t["side"] == 1 and t["p_in"] == pytest.approx(101.8) and t["stop"] == pytest.approx(100)
    assert t["target"] == pytest.approx(101.8 + 2 * 1.8)


def test_h8b_reabsorption_reverses_toward_opposite_side():
    ov = {}
    setv(ov, "03:00", "03:04", (100.5, 101.6, 100.5, 101.5))
    setv(ov, "03:05", "03:09", (101.5, 101.7, 100.4, 100.6))  # rientra nel box
    t = E.h8b(day(over=ov), D, (101, 99))
    assert t["side"] == -1 and t["p_in"] == pytest.approx(100.6) and t["stop"] == pytest.approx(101.7)
    assert t["target"] == pytest.approx(99)


# ---------- H8c sweep del POI di Londra a NY ----------

def test_h8c_long_after_london_low_sweep_at_ny():
    ov = {}
    setv(ov, "02:00", "08:29", (100, 102, 98, 100))  # Londra 98-102
    setv(ov, "09:40", "09:44", (99, 99, 97.5, 97.8))  # sweep sotto 98
    setv(ov, "09:45", "09:49", (97.8, 98.6, 97.8, 98.5))  # chiude dentro
    b = day(over=ov)
    t = E.h8c(b, D, E.london_range(b, D))
    assert t["side"] == 1 and t["p_in"] == pytest.approx(98.5) and t["stop"] == pytest.approx(97.5)
    assert t["target"] == pytest.approx(98.5 + 2 * 1.0)


# ---------- H8d IFVG ----------

def test_h8d_bullish_fvg_invalidated_then_short_on_retest():
    ov = {}
    setv(ov, "08:30", "08:34", (100, 100.2, 99.9, 100.1))  # 5m #1 high 100.2
    setv(ov, "08:35", "08:39", (100.2, 100.9, 100.2, 100.8))
    setv(ov, "08:40", "08:44", (100.8, 101.0, 100.6, 100.9))  # 5m #3 low 100.6 > 100.2: FVG rialzista
    setv(ov, "08:45", "08:49", (100.9, 100.9, 99.8, 100.0))  # chiude sotto 100.2: invalidato -> IFVG
    setv(ov, "08:50", "09:09", (100.0, 100.05, 99.9, 100.0))
    ov["09:10"] = (100.0, 100.25, 100.0, 100.1)  # ritorno al bordo 100.2
    t = E.h8d(day(over=ov), D)
    assert t["side"] == -1 and t["p_in"] == pytest.approx(100.2) and t["stop"] == pytest.approx(100.6)
    assert t["target"] == pytest.approx(100.2 - 2 * 0.4) and t["entry_bar_stop"] is True


# ---------- H8e order block ----------

def test_h8e_bullish_order_block_retest():
    ov = {}
    setv(ov, "06:50", "08:39", (100, 100.2, 99.8, 100.1))  # range 5m 0.4: media delle 20 precedenti
    setv(ov, "08:40", "08:44", (100.1, 100.15, 99.7, 99.8))  # ultima barra ribassista = order block (high 100.15, low 99.7)
    setv(ov, "08:45", "08:49", (99.8, 101.2, 99.8, 101.1))  # displacement: range 1.4 >= 2*0.4, corpo 1.3/1.4
    setv(ov, "08:50", "09:19", (101.1, 101.2, 100.9, 101.0))
    ov["09:20"] = (101.0, 101.0, 100.1, 100.4)  # ritorno nell'OB (low <= 100.15)
    t = E.h8e(day(over=ov), D)
    assert t["side"] == 1 and t["p_in"] == pytest.approx(100.15) and t["stop"] == pytest.approx(99.7)
    assert t["target"] == pytest.approx(100.15 + 2 * 0.45)


# ---------- simulatore con orari assoluti ----------

def test_simulate_abs_stop_first_and_time_exit():
    b = day(over={"10:00": (100, 103, 97, 100), "15:55": (100, 100, 100, 101)})
    assert E.simulate(b, ts("09:35"), 1, 100, 98, 102, ts("15:55"))["p_out"] == 98
    assert E.simulate(b, ts("10:01"), 1, 100, None, None, ts("15:55"))["p_out"] == 101

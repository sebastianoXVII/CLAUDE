"""Test del motore T2 (pre-registrazione: research/preregistration/T2_livelli_di_stop.md). Scritti prima del codice."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import t2_engine as E  # noqa: E402

TZ = "America/New_York"


def bars(spec: dict[str, list[tuple[str, float, float, float]]]) -> pd.DataFrame:
    """spec: {'2024-03-11': [('09:30', high, low, close), ...]} orari ET = inizio barra."""
    rows = []
    for d, items in spec.items():
        for hhmm, h, l, c in items:
            ts = pd.Timestamp(f"{d} {hhmm}", tz=TZ).tz_convert("UTC")
            rows.append((ts, c, h, l, c, 1.0))
    df = pd.DataFrame(rows, columns=["ts_utc", "open", "high", "low", "close", "volume"]).set_index("ts_utc")
    return df.sort_index()


def flat(d, start, end, p):
    """barre piatte a prezzo p da start a end inclusi (ET)."""
    idx = pd.date_range(f"{d} {start}", f"{d} {end}", freq="1min")
    return [(t.strftime("%H:%M"), p, p, p) for t in idx]


# ---------- livelli ----------

def test_day_levels_previous_rth_high_low_ignore_after_hours_and_premarket_from_0400():
    spec = {
        "2024-03-11": [("08:00", 500, 500, 500)] + flat("2024-03-11", "09:30", "15:59", 100)
                      + [("12:00", 110, 95, 100), ("17:00", 999, 1, 100)],
        "2024-03-12": [("03:59", 300, 300, 300), ("04:00", 104, 101, 102), ("09:29", 103, 99, 100)]
                      + flat("2024-03-12", "09:30", "15:59", 100),
    }
    lv = E.day_levels(bars(spec))
    row = lv.loc["2024-03-12"]
    assert row["pd_high"] == 110 and row["pd_low"] == 95  # after-hours 999/1 e pre-market 500 ignorati
    assert row["pm_high"] == 104 and row["pm_low"] == 99  # 03:59 ignorata
    assert row["prev_range"] == 15


def test_candidate_levels_include_two_placebos_per_true_level():
    row = pd.Series({"pd_high": 110.0, "pd_low": 95.0, "pm_high": 104.0, "pm_low": 99.0, "prev_range": 10.0})
    c = E.candidate_levels(row, "PD")
    assert sorted(c) == sorted([("true", 1, 110.0), ("placebo", 1, 113.0), ("placebo", 1, 107.0),
                                ("true", -1, 95.0), ("placebo", -1, 98.0), ("placebo", -1, 92.0)])


# ---------- attraversamento ----------

def day_rth(d, items):
    b = bars({d: flat(d, "09:30", "15:59", 100) })
    b = b.drop(index=[pd.Timestamp(f"{d} {h}", tz=TZ).tz_convert("UTC") for h, *_ in items], errors="ignore")
    return pd.concat([b, bars({d: items})]).sort_index()


def test_first_cross_up_measures_continuation_in_points():
    d = "2024-03-12"
    b = day_rth(d, [("10:00", 101, 99, 100.5), ("10:15", 102, 102, 102)])
    b.index = b.index.tz_convert(TZ)
    ev = E.first_cross(b, level=101.0, s=1, H=15, k=10.0)
    assert ev["t_in"] == pd.Timestamp(f"{d} 10:00", tz=TZ)
    assert ev["y"] == pytest.approx((102 - 100.5) * 10)  # P[10:16] = close barra 10:15
    assert ev["swept"] is True  # la barra 10:01.. torna a 100 < 101 entro 15 minuti


def test_first_cross_down_sign_and_no_sweep():
    d = "2024-03-12"
    items = [("10:00", 100, 98, 98.5)] + [(t, 98, 97, 97.5) for t, *_ in flat(d, "10:01", "15:59", 0)]
    b = day_rth(d, items)
    b.index = b.index.tz_convert(TZ)
    ev = E.first_cross(b, level=99.0, s=-1, H=15, k=10.0)
    assert ev["y"] == pytest.approx(-1 * (97.5 - 98.5) * 10)
    assert ev["swept"] is False


def test_cross_before_0935_or_too_late_is_ignored():
    d = "2024-03-12"
    b = day_rth(d, [("09:32", 105, 99, 100), ("15:50", 105, 99, 100)])
    b.index = b.index.tz_convert(TZ)
    assert E.first_cross(b, level=101.0, s=1, H=15, k=10.0) is None  # 09:32 troppo presto, 15:50 > 15:44


def test_level_already_beyond_at_0935_is_not_admitted():
    d = "2024-03-12"
    b = day_rth(d, [])
    b.index = b.index.tz_convert(TZ)
    assert E.admitted(b, level=99.0, s=1) is False  # prezzo 100 gia' sopra un livello superiore a 99
    assert E.admitted(b, level=101.0, s=1) is True
    assert E.admitted(b, level=101.0, s=-1) is False


# ---------- statistica ----------

def test_stage1_detects_true_vs_placebo_difference_with_day_clusters():
    rng = np.random.default_rng(0)
    rows = []
    for i, d in enumerate(pd.bdate_range("2017-01-02", periods=800)):
        rows.append({"date": d, "kind": "true", "y": 1.0 + rng.normal(0, 3)})
        rows.append({"date": d, "kind": "placebo", "y": rng.normal(0, 3)})
        rows.append({"date": d, "kind": "placebo", "y": rng.normal(0, 3)})
    r = E.stage1(pd.DataFrame(rows))
    assert r["coef"] == pytest.approx(1.0, abs=0.35)
    assert r["t"] > 3
    assert r["n_true"] == 800 and r["n_placebo"] == 1600


def test_stage1_no_effect_on_noise():
    rng = np.random.default_rng(1)
    df = pd.DataFrame({"date": np.repeat(pd.bdate_range("2017-01-02", periods=500), 3),
                       "kind": ["true", "placebo", "placebo"] * 500, "y": rng.normal(0, 3, 1500)})
    assert abs(E.stage1(df)["t"]) < 3


def test_holm_two_sided_p():
    assert E.p_two_sided(3.0) == pytest.approx(0.0027, abs=1e-4)


def test_stage1_survivors_need_holm_t3_and_same_sign_across_instruments():
    r = {
        ("ES", "PD", 15): {"t": 4.0, "p": 6e-5, "coef": 1.0},
        ("NQ", "PD", 15): {"t": 3.5, "p": 4e-4, "coef": 2.0},
        ("ES", "PM", 15): {"t": 4.0, "p": 6e-5, "coef": 1.0},
        ("NQ", "PM", 15): {"t": -3.5, "p": 4e-4, "coef": -2.0},  # segno opposto -> muore
        ("ES", "PD", 30): {"t": 2.5, "p": 0.012, "coef": 1.0},  # |t|<3 -> muore
        ("NQ", "PD", 30): {"t": 3.2, "p": 0.0014, "coef": 1.0},
    }
    s = E.stage1_survivors(r)
    assert set(s) == {("ES", "PD", 15), ("NQ", "PD", 15)}
    assert all(k in r[key] for key in r for k in ("p_holm",))

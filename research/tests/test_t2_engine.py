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
    for v in r.values():  # emendamento 1: serve anche la regressione con controlli
        v["t_adj"], v["coef_adj"] = v["t"], v["coef"]
    s = E.stage1_survivors(r)
    assert set(s) == {("ES", "PD", 15), ("NQ", "PD", 15)}
    assert all(k in r[key] for key in r for k in ("p_holm",))


# ---------- emendamento 1 (da code review) ----------

def full_day(d, extra=(), pm=()):
    """giornata con pre-market opzionale + RTH piatta a 100, con barre sovrascritte da `extra`."""
    base = {h: (p, p, p) for h, p, _, _ in [(t, 100, 100, 100) for t, *_ in flat(d, "09:30", "15:59", 100)]}
    for h, hi, lo, c in list(pm) + list(extra):
        base[h] = (hi, lo, c)
    b = bars({d: [(h, *v) for h, v in base.items()]})
    b.index = b.index.tz_convert(TZ)
    return b


def test_level_touched_between_0930_and_0934_is_not_admitted():
    b = full_day("2024-03-12", extra=[("09:31", 101.5, 99, 100)])
    assert E.admitted(b, level=101.0, s=1, family="PM") is False
    assert E.admitted(full_day("2024-03-12"), level=101.0, s=1, family="PM") is True


def test_pd_level_touched_in_premarket_is_not_admitted_but_pm_level_is():
    b = full_day("2024-03-12", pm=[("08:00", 101.5, 99, 100)])
    assert E.admitted(b, level=101.0, s=1, family="PD") is False
    assert E.admitted(b, level=101.0, s=1, family="PM") is True


def test_second_crossing_is_ignored():
    b = full_day("2024-03-12", extra=[("10:00", 101, 99, 100.5), ("11:00", 101, 99, 100.9)])
    ev = E.first_cross(b, level=101.0, s=1, H=15, k=10.0)
    assert ev["t_in"] == pd.Timestamp("2024-03-12 10:00", tz=TZ)


def test_window_boundary_for_h30():
    ok = full_day("2024-03-12", extra=[("15:29", 101, 99, 100.5), ("15:59", 100, 100, 103)])
    ev = E.first_cross(ok, level=101.0, s=1, H=30, k=10.0)
    assert ev is not None and ev["y"] == pytest.approx((103 - 100.5) * 10)  # uscita = close 15:59
    late = full_day("2024-03-12", extra=[("15:30", 101, 99, 100.5)])
    assert E.first_cross(late, level=101.0, s=1, H=30, k=10.0) is None


def two_days(pm2=True):
    d1 = full_day("2024-03-11", extra=[("12:00", 110, 95, 100)])
    d2 = full_day("2024-03-12", pm=[("08:00", 104, 99, 100)] if pm2 else [],
                  extra=[("10:00", 111, 99, 110.5), ("10:15", 112, 112, 112)])
    b = pd.concat([d1, d2])
    b.index = b.index.tz_convert("UTC")
    return b


def test_events_integration_has_controls_and_true_pd_event():
    ev = E.events(two_days(), "PD", H=15, k=10.0)
    tr = ev[(ev["kind"] == "true") & (ev["s"] == 1)]
    assert len(tr) == 1 and tr["y"].iloc[0] == pytest.approx((112 - 110.5) * 10)
    assert {"dist", "bucket", "side"} <= set(ev.columns)
    assert tr["dist"].iloc[0] == pytest.approx((110 - 100) / 15)
    assert tr["bucket"].iloc[0] == 0  # 10:00 cade nella prima fascia di 30 minuti dalle 09:35


def test_day_without_premarket_keeps_pd_levels():
    ev = E.events(two_days(pm2=False), "PD", H=15, k=10.0)
    assert ((ev["kind"] == "true") & (ev["s"] == 1)).sum() == 1
    assert E.events(two_days(pm2=False), "PM", H=15, k=10.0).empty


def test_stage1_adjusted_removes_pure_distance_confound():
    rng = np.random.default_rng(2)
    rows = []
    for d in pd.bdate_range("2017-01-02", periods=900):
        for kind, dist in (("true", 0.2), ("placebo", 0.5), ("placebo", 0.5)):
            rows.append({"date": d, "kind": kind, "dist": dist + rng.uniform(-0.1, 0.1), "bucket": int(rng.integers(0, 12)),
                         "side": int(rng.choice([1, -1])), "swept": False})
    df = pd.DataFrame(rows)
    df["y"] = -4.0 * df["dist"] + rng.normal(0, 1, len(df))  # y dipende SOLO dalla distanza
    assert E.stage1(df)["t"] > 3  # la regressione semplice vede un falso effetto
    assert abs(E.stage1(df)["t_adj"]) < 3  # quella con controlli no


def test_survivors_require_adjusted_t_with_same_sign():
    base = {"t": 4.0, "p": 6e-5, "coef": 1.0, "t_adj": 3.5, "coef_adj": 0.8}
    r = {("ES", "PD", 15): dict(base), ("NQ", "PD", 15): dict(base),
         ("ES", "PM", 15): dict(base), ("NQ", "PM", 15): {**base, "t_adj": 1.0}}
    assert E.stage1_survivors(r) == [("ES", "PD", 15), ("NQ", "PD", 15)]


def test_stage2_per_trade_metrics_and_valid_days_only():
    days = pd.DatetimeIndex(["2024-03-11", "2024-03-12", "2024-03-13"])
    ev = pd.DataFrame({"date": pd.to_datetime(["2024-03-11", "2024-03-11", "2024-03-13"]),
                       "kind": "true", "y": [2.0, -1.0, 3.0]})
    m = E.stage2(ev, direction=1, cost=0.5, valid_days=days, usd_per_pt=50.0)
    assert m["n_trades"] == 3
    assert m["per_trade_pt"] == pytest.approx((1.5 - 1.5 + 2.5) / 3)
    assert m["giorni"] == 3  # solo giorni validi, nessun festivo riempito a zero
    assert m["trade_win_rate"] == pytest.approx(2 / 3)


def test_events_empty_frame_has_columns():
    b = full_day("2024-03-12")
    b.index = b.index.tz_convert("UTC")
    ev = E.events(b, "PD", H=15, k=10.0)
    assert ev.empty and "kind" in ev.columns

"""Test del simulatore di challenge prop (regole Topstep 50K verificate 2026-11-10 su help.topstep.com). Scritti prima del codice."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab import prop_sim as P  # noqa: E402

R = P.Rules(start=50_000, target=3_000, mll=2_000, consistency=0.55)


def test_pass_when_target_reached_without_big_single_day():
    days = [(1000, 0), (1000, 0), (1100, 0)]  # (P&L del giorno, minimo intraday del P&L del giorno)
    r = P.run_challenge(days, R)
    assert r["outcome"] == "pass" and r["days"] == 3


def test_consistency_raises_target_after_big_day():
    # giorno migliore 2000 > 55% di 3000 -> il target diventa 2000/0.55 = 3636.4
    days = [(2000, 0), (1200, 0), (500, 0)]
    r = P.run_challenge(days, R)
    assert r["outcome"] == "pass" and r["days"] == 3
    assert P.run_challenge(days[:2], R)["outcome"] == "open"  # 3200 < 3636: non ancora passato


def test_fail_on_intraday_breach_even_if_day_closes_positive():
    days = [(500, 0), (100, -2600)]  # MLL a 48.500 dopo il giorno 1; intraday 50.500-2.600 = 47.900 -> violato
    r = P.run_challenge(days, R)
    assert r["outcome"] == "fail" and r["days"] == 2


def test_mll_trails_on_eod_high_and_stops_at_start_balance():
    # dopo +2.500 il MLL sale fino a 50.000 e si ferma: un crollo a 50.100 non viola, a 49.900 si'
    assert P.run_challenge([(2500, 0), (0, -2400)], R)["outcome"] == "open"
    assert P.run_challenge([(2500, 0), (0, -2600)], R)["outcome"] == "fail"


def test_monte_carlo_returns_probabilities_that_sum_to_one():
    rng = np.random.default_rng(0)
    pool = [(float(x), float(min(0, x) - 50)) for x in rng.normal(30, 400, 500)]
    out = P.monte_carlo(pool, R, n_sims=400, max_days=120, block=5, seed=1)
    assert out["p_pass"] + out["p_fail"] + out["p_open"] == pytest.approx(1.0)
    assert 0 <= out["p_pass"] <= 1 and out["median_days_pass"] > 0


def test_scaling_multiplies_pnl_and_intraday_min():
    pool = [(100.0, -50.0)]
    scaled = P.scale(pool, 3)
    assert scaled == [(300.0, -150.0)]


# ---------- drawdown statico e limite giornaliero (prop CFD) ----------

STATIC = P.Rules(start=50_000, target=4_000, mll=5_000, consistency=0.0, trailing=False, daily_loss=2_500)


def test_static_floor_never_moves():
    # dopo +3.000 il pavimento statico resta a 45.000: un crollo a 47.500 non viola
    assert P.run_challenge([(3000, 0), (-2400, -2400)], STATIC)["outcome"] == "open"


def test_daily_loss_limit_breach_fails_even_with_room_on_max_loss():
    assert P.run_challenge([(0, -2600)], STATIC)["outcome"] == "fail"


def test_consistency_zero_disables_rule():
    assert P.run_challenge([(4000, 0)], STATIC)["outcome"] == "pass"


# ---------- fase funded (FundedNext: statico 10%, giornaliero 5%, payout ogni 14 giorni, 80%) ----------

FUNDED = P.FundedRules(start=100_000, mll=10_000, daily_loss=5_000, first_cycle=21, cycle=14, split=0.8)


def test_funded_pays_profit_at_cycle_end_and_resets_balance():
    days = [(500, 0)] * 21 + [(0, 0)] * 14
    r = P.run_funded(days, FUNDED)
    assert r["payouts"] == [pytest.approx(0.8 * 10_500)] and r["breached"] is False


def test_funded_no_payout_if_cycle_not_in_profit():
    r = P.run_funded([(-100, -100)] * 21, FUNDED)
    assert r["payouts"] == [] and r["breached"] is False


def test_funded_breach_on_static_floor():
    r = P.run_funded([(-4000, -4000), (-4000, -4000), (-2100, -2100)], FUNDED)  # pavimento statico a 90.000
    assert r["breached"] is True and r["days"] == 3


def test_funded_breach_on_daily_loss():
    assert P.run_funded([(-5100, -5100)], FUNDED)["breached"] is True

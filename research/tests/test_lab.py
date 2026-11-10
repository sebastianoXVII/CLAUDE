"""Test del laboratorio di backtest: statistiche di percorso, diario dei trade e screenshot. Scritti prima del codice."""
import sqlite3
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab import charts, journal, pathstats  # noqa: E402

TZ = "America/New_York"


def bars(vals):
    """vals: lista di (high, low, close) a partire dalle 10:00 ET."""
    idx = pd.date_range("2024-03-12 10:00", periods=len(vals), freq="1min", tz=TZ)
    return pd.DataFrame({"open": [v[2] for v in vals], "high": [v[0] for v in vals],
                         "low": [v[1] for v in vals], "close": [v[2] for v in vals], "volume": 1.0}, index=idx)


def test_mfe_mae_in_r_for_long():
    b = bars([(101, 99.5, 100.5), (103, 100, 102), (102, 98.5, 99)])
    s = pathstats.path_stats(b, side=1, entry=100.0, stop=98.0)
    assert s["mfe_r"] == pytest.approx(1.5)   # massimo 103 -> +3 punti / rischio 2
    assert s["mae_r"] == pytest.approx(-0.75)  # minimo 98.5 -> -1.5 punti / rischio 2


def test_mfe_mae_for_short_and_no_stop_uses_points():
    b = bars([(101, 99, 100), (100.5, 97, 98)])
    s = pathstats.path_stats(b, side=-1, entry=100.0, stop=None)
    assert s["mfe_pts"] == pytest.approx(3.0) and s["mae_pts"] == pytest.approx(-1.0)
    assert s["mfe_r"] is None


def test_journal_roundtrip_and_query(tmp_path):
    db = tmp_path / "j.sqlite"
    j = journal.Journal(db)
    tid = j.add({"strategy": "S1", "instrument": "NQ", "date": "2024-03-12", "side": 1,
                 "entry_time": "2024-03-12 10:00", "entry": 100.0, "stop": 98.0, "target": 104.0,
                 "exit_time": "2024-03-12 10:30", "exit": 104.0, "reason": "target", "r_multiple": 2.0,
                 "pnl_pts": 4.0, "context": {"htf_trend": "up", "asia_range_pts": 55.0}})
    rows = j.query("SELECT strategy, r_multiple, context FROM trades WHERE id = ?", (tid,))
    assert rows[0][0] == "S1" and rows[0][1] == 2.0 and '"htf_trend": "up"' in rows[0][2]
    assert sqlite3.connect(db).execute("SELECT COUNT(*) FROM trades").fetchone()[0] == 1


def test_chart_renders_png_with_annotations(tmp_path):
    b = bars([(101 + i % 3, 99 + i % 2, 100 + (i % 4) / 2) for i in range(60)])
    out = charts.trade_chart(b, tmp_path / "t.png", title="S1 NQ 2024-03-12",
                             entry=("2024-03-12 10:10", 100.5), stop=98.0, target=104.0,
                             exit=("2024-03-12 10:40", 101.0),
                             boxes=[("Asia", "2024-03-12 10:00", "2024-03-12 10:20", 99.0, 103.0)],
                             levels={"PDH": 102.5})
    assert out.exists() and out.stat().st_size > 5000
    assert out.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_chart_accepts_side_and_marks_short_with_down_triangle(tmp_path):
    b = bars([(101, 99, 100)] * 30)
    assert charts.entry_marker(1) == "^" and charts.entry_marker(-1) == "v"
    out = charts.trade_chart(b, tmp_path / "s.png", title="short", entry=("2024-03-12 10:05", 100.0), side=-1)
    assert out.exists()

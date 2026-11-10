"""Diario dei trade su SQLite: ogni trade del backtest e' tracciato e ricercabile (con contesto e screenshot)."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

SCHEMA = """CREATE TABLE IF NOT EXISTS trades (
  id INTEGER PRIMARY KEY AUTOINCREMENT, strategy TEXT, instrument TEXT, date TEXT, side INTEGER,
  entry_time TEXT, entry REAL, stop REAL, target REAL, exit_time TEXT, exit REAL, reason TEXT,
  r_multiple REAL, pnl_pts REAL, pnl_net_pts REAL, mfe_pts REAL, mae_pts REAL, mfe_r REAL, mae_r REAL,
  minutes INTEGER, sample TEXT, context TEXT, chart TEXT)"""
COLS = ["strategy", "instrument", "date", "side", "entry_time", "entry", "stop", "target", "exit_time", "exit",
        "reason", "r_multiple", "pnl_pts", "pnl_net_pts", "mfe_pts", "mae_pts", "mfe_r", "mae_r", "minutes",
        "sample", "context", "chart"]


class Journal:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as c:
            c.execute(SCHEMA)

    def add(self, t: dict) -> int:
        row = {k: t.get(k) for k in COLS}
        row["context"] = json.dumps(t.get("context") or {}, ensure_ascii=False)
        with sqlite3.connect(self.path) as c:
            cur = c.execute(f"INSERT INTO trades ({','.join(COLS)}) VALUES ({','.join('?' * len(COLS))})",
                            [row[k] for k in COLS])
            return int(cur.lastrowid)

    def query(self, sql: str, params: tuple = ()) -> list[tuple]:
        with sqlite3.connect(self.path) as c:
            return c.execute(sql, params).fetchall()

    def clear_strategy(self, strategy: str) -> None:
        with sqlite3.connect(self.path) as c:
            c.execute("DELETE FROM trades WHERE strategy = ?", (strategy,))

"""Forward test giornaliero del candidato Noise Area su NQ (proxy QQQ), con il CODICE CONGELATO di T6 (t6_engine.py).
Ogni sera: scarica le ultime ~40 sessioni da Alpaca (raw + rettificate), calcola i segnali dei giorni non ancora registrati
e li aggiunge a research/forward/noise_area_nq_forward.csv. I giorni senza trade sono registrati come 'flat'.
Credenziali Alpaca: variabili d'ambiente APCA_API_KEY_ID / APCA_API_SECRET_KEY (segreti di GitHub Actions)."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import t1_engine as T1  # noqa: E402
import t6_engine as E  # noqa: E402

LOG = HERE / "noise_area_nq_forward.csv"
FIELDS = ["date", "side", "entry_time", "exit_time", "entry", "exit", "reason", "gross_pts_nq", "net_pts_nq", "code_version"]
CODE_VERSION = hashlib.sha256((HERE.parent / "t6_engine.py").read_bytes()).hexdigest()[:12]


def _daily_close(b: pd.DataFrame) -> pd.Series:
    x = b.copy()
    x.index = x.index.tz_convert(E.TZ)
    x = x.between_time("09:30", "15:59")
    return x.groupby(pd.to_datetime(x.index.date))["close"].last()


def forward_rows(raw: pd.DataFrame, adj: pd.DataFrame, already: set, k: float = 41.0, cost: float = 0.85) -> list[dict]:
    div = E.dividends_from_closes(_daily_close(adj), _daily_close(raw))
    b = raw.copy()
    b.index = b.index.tz_convert(E.TZ)
    rth = b[~b.index.duplicated()].sort_index().between_time("09:30", "15:59")
    days, rows, prev_ok = {}, [], False
    for d, g in rth.groupby(rth.index.date):
        ts = pd.Timestamp(d)
        if ts.weekday() >= 5 or ts in T1.EARLY_CLOSES or len(g) < 300:
            prev_ok = False
            continue
        inp = E.day_inputs(g)
        days[ts] = inp
        rows.append({"date": ts, "open": inp["open"], "prev_valid": prev_ok,
                     **{t: inp["prices"][t] for t in E.DECISION_TIMES}, "p1600": inp["prices"]["16:00"]})
        prev_ok = True
    if not rows:
        return []
    tab = pd.DataFrame(rows).set_index("date")
    tab = tab[tab["p1600"].notna() & tab["open"].notna()]
    tab["prev_close"] = tab["p1600"].shift(1).where(tab["prev_valid"]) - div.reindex(tab.index).fillna(0.0)
    sig = E.sigma_table(tab[E.DECISION_TIMES], tab["open"])
    out = []
    for ts, row in tab.iterrows():
        ds = str(ts.date())
        if ds in already or np.isnan(row["prev_close"]) or sig.loc[ts].isna().any():
            continue
        ub, lb = {}, {}
        for t in E.DECISION_TIMES:
            ub[t], lb[t] = E.bounds(row["open"], row["prev_close"], sig.loc[ts, t])
        inp = days[ts]
        trades = E.simulate_day(inp["prices"], inp["vwap"], ub, lb, row["p1600"])
        if not trades:
            out.append({"date": ds, "side": 0, "entry_time": "", "exit_time": "", "entry": "", "exit": "", "reason": "flat",
                        "gross_pts_nq": 0.0, "net_pts_nq": 0.0, "code_version": CODE_VERSION})
        for tr in trades:
            gross = tr["side"] * (tr["exit"] - tr["entry"]) * k
            out.append({"date": ds, "side": tr["side"], "entry_time": tr["entry_time"], "exit_time": tr["exit_time"],
                        "entry": round(tr["entry"], 4), "exit": round(tr["exit"], 4), "reason": tr["reason"],
                        "gross_pts_nq": round(gross, 2), "net_pts_nq": round(gross - cost, 2), "code_version": CODE_VERSION})
    return out


def _alpaca(sym: str, start: str, adjustment: str) -> pd.DataFrame:
    # in GitHub Actions le chiavi arrivano dai segreti; in questa sessione cloud il proxy inietta l'autenticazione da solo
    hdr = ({"APCA-API-KEY-ID": os.environ["APCA_API_KEY_ID"], "APCA-API-SECRET-KEY": os.environ["APCA_API_SECRET_KEY"]}
           if os.environ.get("APCA_API_KEY_ID") else {})
    params = {"symbols": sym, "timeframe": "1Min", "start": start, "feed": "sip", "adjustment": adjustment, "limit": 10000, "sort": "asc"}
    bars = []
    while True:
        url = "https://data.alpaca.markets/v2/stocks/bars?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=60) as r:
            j = json.load(r)
        bars += (j.get("bars") or {}).get(sym) or []
        if not j.get("next_page_token"):
            break
        params["page_token"] = j["next_page_token"]
    df = pd.DataFrame(bars)
    df.index = pd.to_datetime(df.pop("t"), utc=True)
    return df.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"})[["open", "high", "low", "close", "volume"]]


def main() -> None:
    start = (pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=70)).strftime("%Y-%m-%dT00:00:00Z")
    raw, adj = _alpaca("QQQ", start, "raw"), _alpaca("QQQ", start, "all")
    already = set()
    if LOG.exists():
        with LOG.open() as f:
            already = {r["date"] for r in csv.DictReader(f)}
    floor = "2026-11-10"  # il forward test parte dal giorno del congelamento del codice
    new = [r for r in forward_rows(raw, adj, already) if r["date"] >= floor]
    write_header = not LOG.exists()
    with LOG.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if write_header:
            w.writeheader()
        w.writerows(new)
    print(f"aggiunte {len(new)} righe ({len({r['date'] for r in new})} giorni) | versione codice {CODE_VERSION}")


if __name__ == "__main__":
    main()

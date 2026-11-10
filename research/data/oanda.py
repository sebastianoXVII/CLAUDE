"""Downloader delle candele M1 (prezzo mid) dall'API OANDA v20, conto practice.
Il token NON sta nel codice: il proxy della sessione lo inietta come 'Authorization: Bearer' verso api-fxpractice.oanda.com.

Uso:
    python3 research/data/oanda.py NAS100_USD 2008-01-01 2016-12-31
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "bars"
BASE = "https://api-fxpractice.oanda.com/v3/instruments/{inst}/candles"


def http_get_factory(inst: str) -> Callable[[dict], dict]:
    def get(params: dict) -> dict:
        url = BASE.format(inst=inst) + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": "Bearer proxy-injected"})
        for attempt in range(6):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    return json.load(r)
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503, 504):
                    time.sleep(2 ** attempt)
                    continue
                raise
        raise RuntimeError(f"richiesta fallita: {url}")
    return get


def parse(payload: dict) -> pd.DataFrame:
    rows = [{"ts_utc": c["time"], "open": float(c["mid"]["o"]), "high": float(c["mid"]["h"]),
             "low": float(c["mid"]["l"]), "close": float(c["mid"]["c"]), "volume": float(c["volume"])}
            for c in payload.get("candles", []) if c.get("complete", True)]
    if not rows:
        return pd.DataFrame(columns=["open", "high", "low", "close", "volume"],
                            index=pd.DatetimeIndex([], tz="UTC", name="ts_utc"))
    df = pd.DataFrame(rows)
    df.index = pd.to_datetime(df.pop("ts_utc"), utc=True, format="ISO8601")
    df.index.name = "ts_utc"
    return df


def fetch(inst: str, start: str, end: str, get: Callable[[dict], dict] | None = None, count: int = 5000) -> pd.DataFrame:
    get = get or http_get_factory(inst)
    frames, frm = [], start
    end_ts = pd.Timestamp(end).tz_convert("UTC") if pd.Timestamp(end).tzinfo else pd.Timestamp(end, tz="UTC")
    while True:
        df = parse(get({"granularity": "M1", "price": "M", "from": frm, "count": count}))
        df = df[df.index < end_ts]
        if df.empty:
            break
        frames.append(df)
        last = df.index[-1]
        if len(df) < 2 and frames and len(frames) > 1 and frames[-2].index[-1] == last:
            break
        nxt = (last).strftime("%Y-%m-%dT%H:%M:%S.000000000Z")
        if nxt == frm:
            break
        frm = nxt
        time.sleep(0.05)
    if not frames:
        return parse({})
    out = pd.concat(frames)
    return out[~out.index.duplicated()].sort_index()


def main(inst: str, start: str, end: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = fetch(inst, f"{start}T00:00:00Z", f"{end}T23:59:59Z")
    out = OUT / f"{inst}_M1_oanda.parquet"
    df.to_parquet(out)
    print(f"FATTO {inst}: {len(df)} barre {df.index[0] if len(df) else '-'} -> {df.index[-1] if len(df) else '-'} -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])

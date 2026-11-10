"""Downloader delle barre storiche a 1 minuto di Alpaca (piano gratuito: storia dal 2016, 200 chiamate/min).

La credenziale NON sta nel codice: il proxy della sessione la inietta in automatico come autenticazione Basic
(username = API Key ID, password = Secret Key) nelle richieste verso data.alpaca.markets.

Uso:
    python3 research/data/alpaca.py SPY 2016-01-01 2026-11-06        # rettificato (dividendi)
    python3 research/data/alpaca.py SPY 2016-01-01 2026-11-06 raw    # non rettificato
"""
from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "bars"
BASE = "https://data.alpaca.markets/v2/stocks/bars"
COLS = {"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"}


def http_get(params: dict) -> dict:
    url = BASE + "?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 ** attempt)
                continue
            raise
    raise RuntimeError(f"richiesta fallita: {url}")


def parse_page(payload: dict, sym: str) -> pd.DataFrame:
    bars = (payload.get("bars") or {}).get(sym) or []
    if not bars:
        return pd.DataFrame(columns=list(COLS.values()), index=pd.DatetimeIndex([], tz="UTC", name="ts_utc"))
    df = pd.DataFrame(bars)
    df.index = pd.to_datetime(df.pop("t"), utc=True)
    df.index.name = "ts_utc"
    return df.rename(columns=COLS)[list(COLS.values())]


def fetch(sym: str, start: str, end: str, get: Callable[[dict], dict] = http_get, adjustment: str = "all") -> pd.DataFrame:
    params = {"symbols": sym, "timeframe": "1Min", "start": start, "end": end,
              "feed": "sip", "adjustment": adjustment, "limit": 10000, "sort": "asc"}
    frames = []
    while True:
        payload = get(params)
        frames.append(parse_page(payload, sym))
        token = payload.get("next_page_token")
        if not token:
            break
        params = {**params, "page_token": token}
        time.sleep(0.35)  # ~170 chiamate/min, sotto il limite di 200
    df = pd.concat(frames)
    return df[~df.index.duplicated()].sort_index()


def main(sym: str, start: str, end: str, adjustment: str = "all") -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    years = range(int(start[:4]), int(end[:4]) + 1)
    frames = []
    for y in years:
        s = max(start, f"{y}-01-01")
        e = min(end, f"{y}-12-31")
        df = fetch(sym, s, e, adjustment=adjustment)
        print(f"{sym} {y}: {len(df)} barre", flush=True)
        frames.append(df)
    bars = pd.concat(frames)
    bars = bars[~bars.index.duplicated()].sort_index()
    out = OUT / (f"{sym}_1m.parquet" if adjustment == "all" else f"{sym}_1m_{adjustment}.parquet")
    bars.to_parquet(out)
    print(f"FATTO {sym}: {len(bars)} barre {bars.index[0]} -> {bars.index[-1]} -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:5])

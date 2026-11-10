"""Downloader rallentato delle barre a 1 minuto di Dukascopy (gratuite, senza account).

Fonte: https://datafeed.dukascopy.com/datafeed/{SYMBOL}/{YYYY}/{MM-1}/{DD}/BID_candles_min_1.bi5
Formato (verificato a mano il 2026-11-10): LZMA, record da 24 byte big-endian
    uint32 secondi dalla mezzanotte UTC, uint32 open, uint32 close, uint32 low, uint32 high, float32 volume
Prezzo = intero / 1000 per gli indici (USA500IDXUSD 2016-06-14 14:30 UTC -> 2071.65).

Il server risponde 429 se si va troppo veloci: pausa fissa tra richieste + backoff esponenziale.
Ogni giorno viene salvato in cache come file .bi5 grezzo, quindi il download e' riprendibile.

Uso:
    python3 research/data/dukascopy.py USA500IDXUSD 2016-01-01 2026-11-06
"""
from __future__ import annotations

import datetime as dt
import lzma
import struct
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "dukascopy"
OUT = ROOT / "data" / "bars"
URL = "https://datafeed.dukascopy.com/datafeed/{sym}/{y:04d}/{m:02d}/{d:02d}/BID_candles_min_1.bi5"
import os
PAUSE_S = float(os.environ.get("DUKA_PAUSE", "6.0"))  # il feed e' fortemente limitato: sotto ~5 s/richiesta arrivano 429 a raffica
SCALE = 1000.0


def fetch_day(sym: str, day: dt.date) -> bytes | None:
    """Scarica (o legge dalla cache) il file grezzo di un giorno. None = giorno vuoto/assente."""
    path = RAW / sym / f"{day.isoformat()}.bi5"
    if path.exists():
        data = path.read_bytes()
        return data or None
    url = URL.format(sym=sym, y=day.year, m=day.month - 1, d=day.day)
    wait = PAUSE_S
    for attempt in range(40):
        time.sleep(wait)
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                data = r.read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                data = b""
                break
            if e.code in (429, 500, 502, 503):
                wait = min(wait * 2, 600)
                continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            wait = min(wait * 2, 600)
    else:
        raise RuntimeError(f"download fallito dopo i tentativi: {url}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data or None


def decode(day: dt.date, raw: bytes) -> pd.DataFrame:
    d = lzma.decompress(raw)
    n = len(d) // 24
    rows = struct.iter_unpack(">5If", d[: n * 24])
    df = pd.DataFrame(rows, columns=["sec", "open", "close", "low", "high", "volume"])
    df = df[df["volume"] > 0]  # minuti senza tick: Dukascopy ripete l'ultimo prezzo con volume 0
    base = pd.Timestamp(day, tz="UTC")
    df.index = base + pd.to_timedelta(df.pop("sec"), unit="s")
    df.index.name = "ts_utc"
    for c in ("open", "close", "low", "high"):
        df[c] = df[c] / SCALE
    return df[["open", "high", "low", "close", "volume"]]


def main(sym: str, start: str, end: str, out_name: str | None = None) -> None:
    d0, d1 = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    frames, day, n_req = [], d0, 0
    while day <= d1:
        if day.weekday() != 5:  # tutti i giorni tranne il sabato: la domenica sera apre la sessione asiatica
            cached = (RAW / sym / f"{day.isoformat()}.bi5").exists()
            raw = fetch_day(sym, day)
            n_req += not cached
            if raw:
                frames.append(decode(day, raw))
            if day.day == 1:
                print(f"{sym} {day} giorni={len(frames)} richieste={n_req}", flush=True)
        day += dt.timedelta(days=1)
    if not frames:
        print(f"{sym} {start}->{end}: nessun dato disponibile")
        return
    bars = pd.concat(frames).sort_index()
    bars = bars[~bars.index.duplicated()]
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / (out_name or f"{sym}_1m.parquet")
    bars.to_parquet(out)
    print(f"FATTO {sym}: {len(bars)} barre, {bars.index[0]} -> {bars.index[-1]} -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:5])

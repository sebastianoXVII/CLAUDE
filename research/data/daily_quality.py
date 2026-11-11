"""Controllo descrittivo dei dati giornalieri (T15, prima di qualsiasi P&L di strategia):
copertura, giorni validi per anno, buchi, rendimenti anomali rispetto alla volatilita' precedente.
Uso: python research/data/daily_quality.py DIR_DAILY OUT.json"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

MIN_BARS = 120


def gaps(idx: pd.DatetimeIndex, min_bdays: int = 5) -> list[tuple]:
    out = []
    for a, b in zip(idx[:-1], idx[1:]):
        if len(pd.bdate_range(a, b)) - 2 >= min_bdays:
            out.append((a, b))
    return out


def top_outliers(close: pd.Series, k: int = 10) -> list[dict]:
    r = close / close.shift(1) - 1
    sig = np.sqrt((r**2).ewm(com=60).mean()).shift(1)
    z = (r / sig).dropna()
    big = z.abs().sort_values(ascending=False).head(k)
    return [{"date": str(d.date()), "r": round(float(r.loc[d]), 5), "z": round(float(abs(z.loc[d])), 1)} for d in big.index]


def report(d: pd.DataFrame) -> dict:
    v = d[d["n_bars"] >= MIN_BARS]
    return {"prima": str(v.index.min().date()), "ultima": str(v.index.max().date()),
            "giorni_validi_per_anno": {int(y): int(n) for y, n in v.groupby(v.index.year).size().items()},
            "n_bars_mediana": int(v["n_bars"].median()),
            "buchi_oltre_5_gg": [(str(a.date()), str(b.date())) for a, b in gaps(v.index)],
            "top10_anomali": top_outliers(v["close"])}


def main(src: str, out: str) -> None:
    res = {f.stem.replace("_1d", ""): report(pd.read_parquet(f)) for f in sorted(Path(src).glob("*_1d.parquet"))}
    Path(out).write_text(json.dumps(res, indent=1))
    print(f"{len(res)} strumenti -> {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

"""Costruisce il diario consultabile (pagina HTML + screenshot WebP) dal journal SQLite.
Uso: python3 research/journal_site/build.py <cartella_uscita> [strategia] [strumento]"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def main(out: str, strategy: str = "T6_noise_area", instrument: str = "NQ") -> None:
    out = Path(out)
    (out / "img").mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(ROOT / "research" / "results" / "journal.sqlite")
    cols = [d[1] for d in c.execute("PRAGMA table_info(trades)")]
    rows = [dict(zip(cols, r)) for r in c.execute(
        "SELECT * FROM trades WHERE strategy=? AND instrument=? ORDER BY entry_time", (strategy, instrument))]
    trades = []
    for r in rows:
        ctx = json.loads(r["context"] or "{}")
        src = ROOT / r["chart"]
        name = src.stem + ".webp"
        if src.exists() and not (out / "img" / name).exists():
            im = Image.open(src).convert("RGB")
            im.thumbnail((1100, 1100))
            im.save(out / "img" / name, "WEBP", quality=70, method=6)
        e = r["entry"]
        width = (ctx.get("ub", e) - ctx.get("lb", e)) / e if e else 0
        dist = (e - ctx["ub"]) / e if r["side"] == 1 else (ctx["lb"] - e) / e
        trades.append({
            "id": r["id"], "date": r["date"], "side": r["side"], "t_in": r["entry_time"][11:16], "t_out": r["exit_time"][11:16],
            "entry": round(e, 2), "exit": round(r["exit"], 2), "reason": r["reason"],
            "gross": round(r["pnl_pts"], 1), "net": round(r["pnl_net_pts"], 1),
            "mfe": round(r["mfe_pts"], 1), "mae": round(r["mae_pts"], 1), "min": r["minutes"],
            "band_pct": round(width * 100, 3), "dist_pct": round(dist * 100, 3), "img": f"img/{name}",
        })
    # trade simili: solo informazioni note PRIMA dell'ingresso (lato, ora, ampiezza della Noise Area, distanza dalla banda)
    X = np.array([[int(t["t_in"][:2]) * 60 + int(t["t_in"][3:]), t["band_pct"], t["dist_pct"]] for t in trades], float)
    sd = X.std(0)
    sd[sd == 0] = 1
    Z = (X - X.mean(0)) / sd
    for i, t in enumerate(trades):
        d = np.sqrt(((Z - Z[i]) ** 2).sum(1))
        d[[j for j, u in enumerate(trades) if u["side"] != t["side"] or j == i]] = np.inf
        t["similar"] = [trades[j]["id"] for j in np.argsort(d)[:6] if np.isfinite(d[j])]
    tpl = (Path(__file__).parent / "template.html").read_text()
    meta = {"strategy": strategy, "instrument": instrument, "usd_per_pt": 20.0, "usd_per_pt_micro": 2.0,
            "sample": rows[0]["sample"] if rows else "", "n": len(trades)}
    html = tpl.replace("/*__DATA__*/null", json.dumps({"meta": meta, "trades": trades}, ensure_ascii=False))
    (out / "index.html").write_text(html)
    print(f"{len(trades)} trade, {len(list((out / 'img').glob('*.webp')))} immagini -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])

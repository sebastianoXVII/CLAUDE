"""Esegue T8 (concetti di sessione) secondo research/preregistration/T8_sessioni_liquidita.md.
    python3 research/run_t8.py              # in-sample (inizio dati -> 2023-12-31), salva il verdetto
    python3 research/run_t8.py --holdout    # hold-out 2024+, SOLO per i sopravvissuti in-sample
Dati attesi: data/bars/NAS100_USD_M1_oanda.parquet (e SPX500_USD_M1_oanda.parquet, solo riportato)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import t1_engine as T1  # noqa: E402
import t8_engine as E  # noqa: E402
from lab import charts, journal, pathstats  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BARS, OUT = ROOT / "data" / "bars", ROOT / "research" / "results"
CHARTS = ROOT / "data" / "charts" / "T8"
INSTR = {"NQ": ("USATECHIDXUSD", 20.0, 0.45), "ES": ("USA500IDXUSD", 50.0, 0.5)}  # emendamento 3: Dukascopy  # file, $/pt pieno, costo DECISIONALE pt (emend. 2)
COST_MNQ, COST_CFD = 0.85, 2.0  # controllo MNQ (decisionale per NQ) e CFD (solo riportato)
IS_END, HO_START = "2023-12-31", "2024-01-01"
HYP = ("H8a", "H8b", "H8c", "H8d", "H8e")


def days_of(sym: str):
    b = pd.read_parquet(BARS / f"{sym}_1m_24h.parquet")
    b.index = b.index.tz_convert(E.TZ)
    b = b[~b.index.duplicated()].sort_index()
    rth_close = b.between_time("15:59", "15:59")["close"]
    closes = rth_close.groupby(pd.to_datetime(rth_close.index.date)).last()
    for D in closes.index:
        if D.weekday() >= 5 or D in T1.EARLY_CLOSES:
            continue
        frame = b.loc[E._ts(D, "18:00", True):E._ts(D, "15:59")]
        if len(frame.loc[E._ts(D, "09:30"):]) < 300 or frame.loc[E._ts(D, "20:00", True):E._ts(D, "23:59", True)].empty:
            continue
        prev = closes.loc[:D - pd.Timedelta(days=1)]
        if len(prev) < 20:
            continue
        yield D, frame, E.htf_trend(prev)


def signals(frame, D):
    asia = E.asia_range(frame, D)
    lon = E.london_range(frame, D)
    return {"H8a": E.h8a(frame, D, asia), "H8b": E.h8b(frame, D, asia), "H8c": E.h8c(frame, D, lon),
            "H8d": E.h8d(frame, D), "H8e": E.h8e(frame, D)}, asia, lon


def run(inst: str, period: str, keep=None, jr=None):
    sym, usd, cost = INSTR[inst]
    rows, valid = [], []
    for D, frame, trend in days_of(sym):
        if (period == "IS" and D > pd.Timestamp(IS_END)) or (period == "HO" and D < pd.Timestamp(HO_START)):
            continue
        valid.append(D)
        sig, asia, lon = signals(frame, D)
        for h, t in sig.items():
            if t is None:
                continue
            r = E.simulate(frame, t["start"], t["side"], t["p_in"], t["stop"], t["target"], t["last"], t["entry_bar_stop"])
            gross = t["side"] * (r["p_out"] - t["p_in"])
            for variant in ("base", "HTF"):
                if variant == "HTF" and t["side"] != trend:
                    continue
                key = f"{inst}_{h}_{variant}"
                if keep is not None and key not in keep:
                    continue
                rows.append({"key": key, "date": D, "gross_pts": gross, "net_pts": gross - cost, "reason": r["reason"]})
                if jr is not None and variant == "base":
                    g = frame.loc[t["start"]:r["t_out"]]
                    ps = pathstats.path_stats(g, t["side"], t["p_in"], t["stop"])
                    png = CHARTS / period / f"{inst}_{h}_{D.date()}.png"
                    view = frame.loc[E._ts(D, "19:30", True):E._ts(D, "15:59")]
                    charts.trade_chart(view.resample("5min").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna(),
                                       png, title=f"T8 {h} {inst} {D.date()} {'LONG' if t['side'] == 1 else 'SHORT'} {r['reason']} {gross - cost:+.1f} pt",
                                       entry=(t["start"], t["p_in"]), side=t["side"], stop=t["stop"], target=t["target"], exit=(r["t_out"], r["p_out"]),
                                       boxes=[("Asia", E._ts(D, "20:00", True), E._ts(D, "23:59", True), asia[1], asia[0]),
                                              ("London", E._ts(D, "02:00"), E._ts(D, "08:29"), lon[1], lon[0]),
                                              ("NY", E._ts(D, "09:30"), E._ts(D, "15:59"),
                                               float(frame.loc[E._ts(D, "09:30"):, "low"].min()), float(frame.loc[E._ts(D, "09:30"):, "high"].max()))])
                    jr.add({"strategy": f"T8_{h}", "instrument": inst, "date": str(D.date()), "side": t["side"],
                            "entry_time": str(t["start"]), "entry": t["p_in"], "stop": t["stop"], "target": t["target"],
                            "exit_time": str(r["t_out"]), "exit": r["p_out"], "reason": r["reason"],
                            "r_multiple": (gross / abs(t["p_in"] - t["stop"])) if t["stop"] else None,
                            "pnl_pts": gross, "pnl_net_pts": gross - cost, "mfe_pts": ps["mfe_pts"], "mae_pts": ps["mae_pts"],
                            "mfe_r": ps["mfe_r"], "mae_r": ps["mae_r"], "minutes": ps["minutes"], "sample": period,
                            "chart": (str(png.relative_to(ROOT)) if png.is_relative_to(ROOT) else str(png)), "context": {"htf_trend": trend, "asia": asia, "london": lon}})
    return pd.DataFrame(rows), pd.DatetimeIndex(valid)


def stats(df, valid, usd, cost):
    daily = df.groupby("date")["net_pts"].sum().reindex(valid, fill_value=0.0)
    m = T1.metrics(daily, daily.index.isin(df["date"]), usd)
    m["n_trades"] = int(len(df))
    m["gross_pt_per_trade"] = float(df["gross_pts"].mean()) if len(df) else np.nan
    m["stress2x_media_pt"] = float((df["gross_pts"] - 2 * cost).groupby(df["date"]).sum().reindex(valid, fill_value=0.0).mean())
    for name, c in (("media_pt_costo_MNQ", COST_MNQ), ("media_pt_costo_CFD", COST_CFD)):
        m[name] = float((df["gross_pts"] - c).groupby(df["date"]).sum().reindex(valid, fill_value=0.0).mean()) if len(df) else np.nan
    m["uscite"] = df["reason"].value_counts(normalize=True).round(3).to_dict() if len(df) else {}
    yr = daily.groupby(daily.index.year).sum()
    m["anni_positivi"] = f"{int((yr > 0).sum())}/{len(yr)}"
    return m


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    jr = journal.Journal(OUT / "journal.sqlite")
    is_file = OUT / "T8_in_sample.json"
    if "--holdout" not in sys.argv:
        if is_file.exists():
            sys.exit("T8 in-sample gia' eseguito.")
        for h in HYP:
            jr.clear_strategy(f"T8_{h}")
        res, pv = {}, {}
        for inst in INSTR:
            if not (BARS / f"{INSTR[inst][0]}_1m_24h.parquet").exists():
                print(f"{inst}: dati assenti, saltato (solo riportato)")
                continue
            df, valid = run(inst, "IS", jr=jr if inst == "NQ" else None)
            for h in HYP:
                for v in ("base", "HTF"):
                    key = f"{inst}_{h}_{v}"
                    m = stats(df[df["key"] == key], valid, INSTR[inst][1], INSTR[inst][2])
                    res[key] = m
                    if inst == "NQ":
                        pv[key] = m["p_unilaterale"]
        for key, p in T1.holm(pv).items():
            m = res[key]
            pos, yrs = map(int, m["anni_positivi"].split("/"))
            m["p_holm"] = p
            m["SOPRAVVIVE"] = bool(m["t_nw"] > 3 and p < 0.05 and m["stress2x_media_pt"] > 0 and m["media_pt_costo_MNQ"] > 0
                                   and pos * 3 >= 2 * yrs and m["n_trades"] >= 150)
        is_file.write_text(json.dumps(res, indent=2, default=str, ensure_ascii=False))
        cols = ["n_trades", "win_rate", "gross_pt_per_trade", "expectancy_pt_per_trade", "profit_factor", "sharpe_ann",
                "max_dd_usd", "t_nw", "p_holm", "stress2x_media_pt", "media_pt_costo_MNQ", "media_pt_costo_CFD", "anni_positivi", "SOPRAVVIVE"]
        print(pd.DataFrame(res).T.reindex(columns=cols).to_string(float_format=lambda v: f"{v:,.3f}"))
        surv = [k for k, m in res.items() if m.get("SOPRAVVIVE")]
        print("Sopravvissuti NQ:", surv or "NESSUNO -> T8 MORTO")
        return
    surv = [k for k, m in json.loads(is_file.read_text()).items() if m.get("SOPRAVVIVE")]
    if not surv:
        sys.exit("T8 MORTO in-sample: hold-out non calcolato.")
    import sqlite3
    with sqlite3.connect(OUT / "journal.sqlite") as c:
        c.execute("DELETE FROM trades WHERE strategy LIKE 'T8_%' AND sample = 'HO'")
    df, valid = run("NQ", "HO", keep=set(surv), jr=jr)
    res = {k: stats(df[df["key"] == k], valid, INSTR["NQ"][1], INSTR["NQ"][2]) for k in surv}
    for k, m in res.items():
        m["SOPRAVVIVE_HO"] = bool(m["t_nw"] > 2 and m["stress2x_media_pt"] > 0 and m["media_pt_costo_MNQ"] > 0)
    (OUT / "T8_holdout.json").write_text(json.dumps(res, indent=2, default=str, ensure_ascii=False))
    print(pd.DataFrame(res).T.to_string())


if __name__ == "__main__":
    main()

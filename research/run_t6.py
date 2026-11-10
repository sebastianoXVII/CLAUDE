"""Esegue T6 (Noise Area) secondo research/preregistration/T6_noise_area_momentum.md."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import t1_engine as T1  # noqa: E402
import t6_engine as E  # noqa: E402
from lab import charts, journal, pathstats  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BARS, OUT = ROOT / "data" / "bars", ROOT / "research" / "results"
CHARTS = ROOT / "data" / "charts" / "T6"
INSTR = {"ES": ("SPY", 10.0, 50.0, 0.33), "NQ": ("QQQ", 41.0, 20.0, 0.45)}
PERIODS = {"info_in_sample_autori_2017_2024": ("2017-01-01", "2024-12-31"), "OOS_2025": ("2025-01-02", "2026-12-31")}


def daily_last_close(sym_file: str) -> pd.Series:
    b = pd.read_parquet(BARS / sym_file)
    b.index = b.index.tz_convert(E.TZ)
    b = b.between_time("09:30", "15:59")
    return b.groupby(pd.to_datetime(b.index.date))["close"].last()


def build(sym: str, volume_fn=None):
    div = E.dividends_from_closes(daily_last_close(f"{sym}_1m.parquet"), daily_last_close(f"{sym}_1m_raw.parquet"))
    raw = pd.read_parquet(BARS / f"{sym}_1m_raw.parquet")
    raw.index = raw.index.tz_convert(E.TZ)
    rth = raw.between_time("09:30", "15:59")
    if volume_fn is not None:  # T7 emendamento 2: VWAP da profilo di volume
        rth = volume_fn(rth)
    days, rows, prev_ok = {}, [], False
    for d, g in rth.groupby(rth.index.date):
        ts = pd.Timestamp(d)
        if ts.weekday() >= 5 or ts in T1.EARLY_CLOSES or len(g) < 300:
            prev_ok = False
            continue
        inp = E.day_inputs(g)
        days[ts] = (g, inp)
        rows.append({"date": ts, "open": inp["open"], "prev_valid": prev_ok, **{t: inp["prices"][t] for t in E.DECISION_TIMES},
                     "p1600": inp["prices"]["16:00"]})
        prev_ok = True
    tab = pd.DataFrame(rows).set_index("date")
    tab = tab[tab["p1600"].notna() & tab["open"].notna()]  # emendamento 2: giorni senza 16:00 o open esclusi
    tab["prev_close"] = tab["p1600"].shift(1).where(tab["prev_valid"])
    tab["dividend"] = div.reindex(tab.index).fillna(0.0)
    tab["prev_close"] = tab["prev_close"] - tab["dividend"]  # emendamento 2 (codice degli autori)
    sig = E.sigma_table(tab[E.DECISION_TIMES], tab["open"])
    return tab, sig, days


def trades_for(sym: str, k: float, cost: float, volume_fn=None):
    tab, sig, days = build(sym, volume_fn)
    out, armed = [], []
    for ts, row in tab.iterrows():
        if np.isnan(row["prev_close"]) or sig.loc[ts].isna().any() or np.isnan(row["open"]):
            continue
        armed.append(ts)
        ub, lb = {}, {}
        for t in E.DECISION_TIMES:
            ub[t], lb[t] = E.bounds(row["open"], row["prev_close"], sig.loc[ts, t])
        g, inp = days[ts]
        for tr in E.simulate_day(inp["prices"], inp["vwap"], ub, lb, row["p1600"]):
            gross = tr["side"] * (tr["exit"] - tr["entry"]) * k
            out.append({"date": ts, **tr, "gross_pts": gross, "net_pts": gross - cost,
                        "ub_entry": ub[tr["entry_time"]], "lb_entry": lb[tr["entry_time"]]})
    return pd.DataFrame(out), pd.DatetimeIndex(armed), days, int((tab["dividend"] > 0).sum())


def evaluate(tr: pd.DataFrame, valid_days: pd.DatetimeIndex, usd: float, cost: float) -> dict:
    daily = tr.groupby("date")["net_pts"].sum().reindex(valid_days, fill_value=0.0)
    m = T1.metrics(daily, daily.index.isin(tr["date"]), usd)
    m["n_trades"] = int(len(tr))
    m["trade_win_rate"] = float((tr["net_pts"] > 0).mean()) if len(tr) else np.nan
    m["gross_pt_per_trade"] = float(tr["gross_pts"].mean()) if len(tr) else np.nan
    m["net_usd_per_trade"] = float(tr["net_pts"].mean() * usd) if len(tr) else np.nan
    stress = (tr["gross_pts"] - 2 * cost).groupby(tr["date"]).sum().reindex(valid_days, fill_value=0.0)
    m["stress2x_media_pt"] = float(stress.mean())
    m["uscite"] = tr["reason"].value_counts(normalize=True).round(3).to_dict() if len(tr) else {}
    yr = daily.groupby(daily.index.year).sum()
    m["pnl_pt_per_anno"] = {int(a): round(float(b), 1) for a, b in yr.items()}
    return m


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "T6_risultati.json").exists():
        sys.exit("T6 e' gia' stato eseguito: il fuori campione e' consumato, non si riesegue.")
    jr = journal.Journal(OUT / "journal.sqlite")
    jr.clear_strategy("T6_noise_area")
    res = {}
    pending = []
    for inst, (sym, k, usd, cost) in INSTR.items():
        tr, armed, days, n_div = trades_for(sym, k, cost)
        print(f"{inst}: {len(armed)} giorni operativi, {n_div} giorni ex-dividendo rilevati, {len(tr)} trade totali", flush=True)
        for per, (s_, e_) in PERIODS.items():
            valid = armed[(armed >= s_) & (armed <= e_)]
            sub = tr[(tr["date"] >= s_) & (tr["date"] <= e_)]
            res[f"{per}|{inst}"] = evaluate(sub, valid, usd, cost)
            if per == "OOS_2025":
                pending.append((inst, sym, k, sub, days))
    # emendamento 2: sequenza fissa SPY -> QQQ
    for inst in ("ES", "NQ"):
        m = res[f"OOS_2025|{inst}"]
        m["passa_singolo"] = bool(m["t_nw"] > 1.65 and m["stress2x_media_pt"] > 0)
    es_ok = res["OOS_2025|ES"]["passa_singolo"]
    nq_ok = es_ok and res["OOS_2025|NQ"]["passa_singolo"]
    esito = "CANDIDATO FORTE" if nq_ok else "CANDIDATO DEBOLE (solo SPY/ES)" if es_ok else "T6 MORTO"
    res["ESITO"] = esito
    (OUT / "T6_risultati.json").write_text(json.dumps(res, indent=2, default=str, ensure_ascii=False))  # prima dei grafici
    for inst, sym, k, sub, days in pending:
        for _, t in sub.iterrows():
            g, _inp = days[t["date"]]
            d = t["date"].date()
            t0, t1 = pd.Timestamp(f"{d} {t['entry_time']}", tz=E.TZ), pd.Timestamp(f"{d} {t['exit_time']}", tz=E.TZ)
            ps = pathstats.path_stats(g.loc[t0:t1 - pd.Timedelta(minutes=1)], t["side"], t["entry"], None)
            png = CHARTS / f"{inst}_{d}_{t['entry_time'].replace(':', '')}.png"
            charts.trade_chart(g, png, title=f"T6 Noise Area {inst} ({sym}) {d} {'LONG' if t['side'] == 1 else 'SHORT'} "
                               f"{t['reason']} netto {t['net_pts']:+.2f} pt",
                               entry=(t0, t["entry"]), exit=(t1, t["exit"]), side=int(t["side"]),
                               levels={"UB@entry": t["ub_entry"], "LB@entry": t["lb_entry"]})
            jr.add({"strategy": "T6_noise_area", "instrument": inst, "date": str(d), "side": int(t["side"]),
                    "entry_time": str(t0), "entry": t["entry"], "exit_time": str(t1), "exit": t["exit"],
                    "reason": t["reason"], "pnl_pts": t["gross_pts"], "pnl_net_pts": t["net_pts"],
                    "mfe_pts": ps["mfe_pts"] * k, "mae_pts": ps["mae_pts"] * k, "minutes": ps["minutes"],
                    "sample": "OOS_2025", "chart": str(png.relative_to(ROOT)),
                    "context": {"sym": sym, "k": k, "ub": t["ub_entry"], "lb": t["lb_entry"]}})
    cols = ["n_trades", "trade_win_rate", "gross_pt_per_trade", "net_usd_per_trade", "profit_factor", "sharpe_ann",
            "max_dd_usd", "t_nw", "p_unilaterale", "stress2x_media_pt", "passa_singolo"]
    print(pd.DataFrame({k: v for k, v in res.items() if k != "ESITO"}).T.reindex(columns=cols).to_string(float_format=lambda v: f"{v:,.3f}"))
    for key, m in res.items():
        if key == "ESITO":
            continue
        print(f"  {key}: uscite {m['uscite']} | P&L pt/anno {m['pnl_pt_per_anno']}")
    print("\nESITO:", esito)


if __name__ == "__main__":
    main()

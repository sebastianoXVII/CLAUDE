"""Screenshot di ogni trade: candele, box di sessione, livelli, entry/stop/target/uscita."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

TZ = "America/New_York"
BOX_COLORS = {"Asia": "#7c9cbf", "London": "#c9a86a", "NY": "#8fbf8f"}


def _ts(x):
    t = pd.Timestamp(x)
    return t.tz_localize(TZ) if t.tzinfo is None else t.tz_convert(TZ)


def entry_marker(side: int) -> str:
    return "^" if side >= 0 else "v"


def trade_chart(bars: pd.DataFrame, out: Path, title: str, entry: tuple, stop=None, target=None, exit=None,
                boxes=(), levels=None, side: int = 1) -> Path:
    """bars: OHLC con indice ET. entry/exit: (orario, prezzo). boxes: (nome, inizio, fine, low, high)."""
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    b = bars.copy()
    b.index = b.index.tz_convert(TZ)
    x = range(len(b))
    pos = {t: i for i, t in enumerate(b.index)}

    def xi(t):
        t = _ts(t)
        return pos.get(t, b.index.searchsorted(t))

    fig, ax = plt.subplots(figsize=(12, 5.5), dpi=110)
    up = b["close"] >= b["open"]
    ax.vlines(list(x), b["low"], b["high"], color="#555", linewidth=0.6)
    ax.bar([i for i, u in zip(x, up) if u], (b["close"] - b["open"])[up], bottom=b["open"][up], color="#2e8b57", width=0.7)
    ax.bar([i for i, u in zip(x, up) if not u], (b["close"] - b["open"])[~up], bottom=b["open"][~up], color="#c0392b", width=0.7)
    for name, t0, t1, lo, hi in boxes:
        ax.add_patch(plt.Rectangle((xi(t0), lo), max(xi(t1) - xi(t0), 1), hi - lo, alpha=0.15,
                                   color=BOX_COLORS.get(name, "#999"), label=f"box {name}"))
    for name, lvl in (levels or {}).items():
        ax.axhline(lvl, color="#8e44ad", linestyle=":", linewidth=1)
        ax.text(0, lvl, f" {name} {lvl:,.2f}", color="#8e44ad", fontsize=8, va="bottom")
    ei = xi(entry[0])
    ax.scatter([ei], [entry[1]], marker=entry_marker(side), s=90, color="#1f6feb", zorder=5, label=f"entry {entry[1]:,.2f}")
    if stop is not None:
        ax.axhline(stop, color="#c0392b", linestyle="--", linewidth=1, label=f"stop {stop:,.2f}")
    if target is not None:
        ax.axhline(target, color="#2e8b57", linestyle="--", linewidth=1, label=f"target {target:,.2f}")
    if exit is not None:
        ax.scatter([xi(exit[0])], [exit[1]], marker="X", s=90, color="black", zorder=5, label=f"uscita {exit[1]:,.2f}")
    step = max(len(b) // 12, 1)
    ax.set_xticks(list(x)[::step])
    ax.set_xticklabels([t.strftime("%m-%d %H:%M") for t in b.index[::step]], rotation=30, fontsize=7)
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=7, loc="upper left")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out

"""Optional reproducible research charts. Requires matplotlib and pandas."""
from pathlib import Path
from typing import Any

AUTHOR_SIGNATURE = "Created by Jairo Alonso González"


def _plt():
    try:
        import matplotlib.pyplot as plt
        return plt
    except ImportError as exc:
        raise RuntimeError("Install the optional chart dependencies to generate charts") from exc


def football_field(ranges: dict[str, dict[str, float]], current_price: float, output_path: str) -> str:
    plt = _plt(); fig, ax = plt.subplots(figsize=(10, max(3.5, .65 * len(ranges))))
    for i, (name, values) in enumerate(ranges.items()):
        low, base, high = (float(values[k]) for k in ("Bear", "Base", "Bull"))
        if not low <= base <= high: raise ValueError(f"Invalid scenario range for {name}")
        ax.barh(i, high-low, left=low, height=.42)
        ax.plot(base, i, "D", label="Base case" if i == 0 else "")
    ax.axvline(float(current_price), linestyle="--", label="Current price")
    ax.set_yticks(range(len(ranges)), list(ranges)); ax.set_xlabel("Implied value per share")
    ax.set_title("Valuation football field"); ax.grid(axis="x", alpha=.2); ax.legend()
    fig.tight_layout(); path=Path(output_path); path.parent.mkdir(parents=True,exist_ok=True); fig.savefig(path,dpi=180); plt.close(fig); return str(path)


def dcf_sensitivity_heatmap(sensitivity: dict[str, Any], output_path: str) -> str:
    import numpy as np
    plt = _plt(); ws=sensitivity["wacc_values"]; gs=sensitivity["terminal_growth_values"]
    grid=sensitivity["grid_per_share"]
    values=np.array([[grid[str(w)][str(g)] if grid[str(w)][str(g)] is not None else np.nan for g in gs] for w in ws],dtype=float)
    fig,ax=plt.subplots(figsize=(8,5)); im=ax.imshow(values,aspect="auto",origin="lower")
    ax.set_xticks(range(len(gs)),[f"{x:.1%}" for x in gs]); ax.set_yticks(range(len(ws)),[f"{x:.1%}" for x in ws])
    ax.set_xlabel("Terminal growth"); ax.set_ylabel("WACC"); ax.set_title("DCF sensitivity — value per share")
    fig.colorbar(im,ax=ax,label="Value per share"); fig.tight_layout()
    path=Path(output_path); path.parent.mkdir(parents=True,exist_ok=True); fig.savefig(path,dpi=180); plt.close(fig); return str(path)


def price_technical_chart(indicators, ticker: str, output_path: str) -> str:
    plt=_plt(); fig,ax=plt.subplots(figsize=(11,5)); ax.plot(indicators["Date"],indicators["Close"],label="Close")
    for col in ("SMA_50","SMA_200"):
        if col in indicators: ax.plot(indicators["Date"],indicators[col],label=col)
    if {"BB_Upper","BB_Lower"}.issubset(indicators.columns): ax.fill_between(indicators["Date"],indicators["BB_Lower"],indicators["BB_Upper"],alpha=.12,label="Bollinger 20,2")
    ax.set_title(f"{ticker} — Price and technical context"); ax.set_ylabel("Price"); ax.grid(alpha=.2); ax.legend()
    fig.tight_layout(); path=Path(output_path); path.parent.mkdir(parents=True,exist_ok=True); fig.savefig(path,dpi=180); plt.close(fig); return str(path)

"""Optional reproducible research charts."""
from pathlib import Path
from typing import Any
def _plt():
    try:
        import matplotlib.pyplot as plt
        return plt
    except ImportError as exc:
        raise RuntimeError("Install optional chart dependencies to generate charts") from exc
def _save(fig, output_path):
    p=Path(output_path); p.parent.mkdir(parents=True,exist_ok=True); fig.savefig(p,dpi=180,bbox_inches="tight"); _plt().close(fig); return str(p)
def football_field(ranges: dict[str,dict[str,float]], current_price: float, output_path: str)->str:
    plt=_plt(); fig,ax=plt.subplots(figsize=(10,max(3.5,.65*len(ranges))))
    for i,(name,v) in enumerate(ranges.items()):
        low,base,high=(float(v[k]) for k in ("Bear","Base","Bull"))
        if not low<=base<=high: raise ValueError(f"Invalid scenario range for {name}")
        ax.barh(i,high-low,left=low,height=.42); ax.plot(base,i,"D",label="Base case" if i==0 else "")
    ax.axvline(float(current_price),linestyle="--",label="Current price"); ax.set_yticks(range(len(ranges)),list(ranges)); ax.set_xlabel("Implied value per share"); ax.set_title("Valuation football field"); ax.grid(axis="x",alpha=.2); ax.legend(); fig.tight_layout(); return _save(fig,output_path)
def dcf_sensitivity_heatmap(*args)->str:
    import numpy as np
    plt=_plt()
    if len(args)==2 and isinstance(args[0],dict):
        sensitivity,output_path=args; ws=sensitivity["wacc_values"]; gs=sensitivity["terminal_growth_values"]; grid=sensitivity["grid_per_share"]
    elif len(args)==5:
        fcff,wacc_values,growth_values,net_debt,diluted_shares=args
        from .valuation import dcf_sensitivity
        sensitivity=dcf_sensitivity(fcff,wacc_values,growth_values,net_debt,diluted_shares)
        output_path=args[4] if isinstance(args[4],str) else args[-1]
        ws=sensitivity["wacc_values"]; gs=sensitivity["terminal_growth_values"]; grid=sensitivity["grid_per_share"]
    else:
        raise TypeError("Expected (sensitivity, output_path) or legacy five-argument chart call")
    vals=np.array([[grid[str(w)][str(g)] if grid[str(w)][str(g)] is not None else np.nan for g in gs] for w in ws],dtype=float)
    fig,ax=plt.subplots(figsize=(8,5)); im=ax.imshow(vals,aspect="auto",origin="lower"); ax.set_xticks(range(len(gs)),[f"{x:.1%}" for x in gs]); ax.set_yticks(range(len(ws)),[f"{x:.1%}" for x in ws]); ax.set_xlabel("Terminal growth"); ax.set_ylabel("WACC"); ax.set_title("DCF sensitivity — value per share"); fig.colorbar(im,ax=ax,label="Value per share"); fig.tight_layout(); return _save(fig,output_path)
def price_technical_chart(indicators,ticker: str,output_path: str)->str:
    plt=_plt(); fig,ax=plt.subplots(figsize=(11,5)); ax.plot(indicators["Date"],indicators["Close"],label="Close")
    for c in ("SMA_50","SMA_200"):
        if c in indicators: ax.plot(indicators["Date"],indicators[c],label=c)
    if {"BB_Upper","BB_Lower"}.issubset(indicators.columns): ax.fill_between(indicators["Date"],indicators["BB_Lower"],indicators["BB_Upper"],alpha=.12,label="Bollinger 20,2")
    ax.set_title(f"{ticker} — Price and technical context"); ax.set_ylabel("Price"); ax.grid(alpha=.2); ax.legend(); fig.tight_layout(); return _save(fig,output_path)

"""Price-series indicators with explicit lookbacks and Wilder RSI convention."""
from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = {"Date", "Close"}


def compute_technical_indicators(prices: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(prices.columns)
    if missing: raise ValueError(f"Missing price columns: {sorted(missing)}")
    df = prices.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="raise", utc=True)
    df = df.sort_values("Date").drop_duplicates("Date", keep="last").reset_index(drop=True)
    df["Close"] = pd.to_numeric(df["Close"], errors="raise")
    if df["Close"].isna().any() or (df["Close"] <= 0).any():
        raise ValueError("Close prices must be positive and non-missing")
    close = df["Close"].astype(float)
    df["SMA_50"] = close.rolling(50, min_periods=50).mean()
    df["SMA_200"] = close.rolling(200, min_periods=200).mean()
    df["EMA_20"] = close.ewm(span=20, adjust=False, min_periods=20).mean()
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    # Wilder initialization: seed with the arithmetic mean of the first 14 changes,
    # then apply the recursive Wilder smoothing (previous * 13 + current) / 14.
    avg_gain = pd.Series(float("nan"), index=df.index, dtype=float)
    avg_loss = pd.Series(float("nan"), index=df.index, dtype=float)
    if len(df) > 14:
        avg_gain.iloc[14] = gain.iloc[1:15].mean()
        avg_loss.iloc[14] = loss.iloc[1:15].mean()
        for i in range(15, len(df)):
            avg_gain.iloc[i] = (avg_gain.iloc[i-1] * 13 + gain.iloc[i]) / 14
            avg_loss.iloc[i] = (avg_loss.iloc[i-1] * 13 + loss.iloc[i]) / 14
    rs = avg_gain / avg_loss.where(avg_loss != 0)
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.mask((avg_loss == 0) & (avg_gain > 0), 100)
    rsi = rsi.mask((avg_loss > 0) & (avg_gain == 0), 0)
    rsi = rsi.mask((avg_loss == 0) & (avg_gain == 0), 50)
    df["RSI_14"] = rsi
    ema12 = close.ewm(span=12, adjust=False, min_periods=12).mean()
    ema26 = close.ewm(span=26, adjust=False, min_periods=26).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False, min_periods=9).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
    mid = close.rolling(20, min_periods=20).mean()
    std = close.rolling(20, min_periods=20).std(ddof=0)
    df["BB_Middle"] = mid
    df["BB_Upper"] = mid + 2 * std
    df["BB_Lower"] = mid - 2 * std
    df["Daily_Return"] = close.pct_change(fill_method=None)
    return df


def relative_performance(asset_prices: pd.Series, benchmark_prices: pd.Series) -> dict[str, float | int]:
    """Compare aligned price returns. Total-return treatment requires adjusted prices."""
    aligned = pd.concat([asset_prices.rename("asset"), benchmark_prices.rename("benchmark")], axis=1).sort_index().dropna()
    if len(aligned) < 2: raise ValueError("At least two aligned observations are required")
    if (aligned <= 0).any().any(): raise ValueError("Prices must be positive")
    asset = float(aligned.asset.iloc[-1] / aligned.asset.iloc[0] - 1)
    benchmark = float(aligned.benchmark.iloc[-1] / aligned.benchmark.iloc[0] - 1)
    return {"observations": len(aligned), "asset_return": asset,
            "benchmark_return": benchmark, "relative_return": asset - benchmark}

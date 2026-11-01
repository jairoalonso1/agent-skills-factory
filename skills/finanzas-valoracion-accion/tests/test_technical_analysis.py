import numpy as np
import pandas as pd
import pytest
from scripts.technical_analysis import compute_technical_indicators, relative_performance


def test_sma_requires_full_lookback_and_rsi_bounded():
    prices = pd.DataFrame({"Date":pd.date_range("2024-01-01", periods=220), "Close":np.arange(100,320,dtype=float)})
    out = compute_technical_indicators(prices)
    assert pd.isna(out.loc[48,"SMA_50"])
    assert out.loc[49,"SMA_50"] == pytest.approx(np.mean(np.arange(100,150)))
    assert out["RSI_14"].dropna().between(0,100).all()
    assert out.loc[199,"SMA_200"] == pytest.approx(np.mean(np.arange(100,300)))


def test_relative_performance_aligns_dates():
    a = pd.Series([100, 110, 120], index=[1,2,3])
    b = pd.Series([100, 105, 110], index=[1,2,3])
    r = relative_performance(a,b)
    assert r["relative_return"] == pytest.approx(.2 - .1)

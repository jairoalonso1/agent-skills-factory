"""Deterministic financial-statement analytics for institutional equity research.

Inputs are normalized issuer data supplied by an authorized provider or analyst.
All monetary values must use the same currency and scale unless stated otherwise.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from math import isfinite
from typing import Any


def _number(data: Mapping[str, Any], key: str, *, positive: bool = False) -> float:
    if key not in data or data[key] is None:
        raise ValueError(f"Required input '{key}' is missing; no default is inferred.")
    value = float(data[key])
    if not isfinite(value):
        raise ValueError(f"Input '{key}' must be finite.")
    if positive and value <= 0:
        raise ValueError(f"Input '{key}' must be greater than zero.")
    return value


def safe_divide(numerator: float, denominator: float) -> float | None:
    if denominator == 0 or not isfinite(numerator) or not isfinite(denominator):
        return None
    return numerator / denominator


def calculate_financial_ratios(data: Mapping[str, Any]) -> dict[str, Any]:
    """Calculate ratios without silently imputing missing accounting inputs.

    Required keys: revenue, gross_profit, ebit, ebitda, ebt, net_income,
    total_assets, average_assets, total_equity, average_equity, invested_capital,
    diluted_shares, current_price, cash, total_debt, operating_cash_flow,
    capex, dividends_paid, net_buybacks, tax_rate.

    `net_buybacks` means repurchases less equity issuance, and may be negative
    when issuance exceeds repurchases. `tax_rate` must be an explicitly
    sourced/approved effective or normalized cash tax assumption in decimal
    form. Capex is entered as a positive outflow.
    """
    required = ["revenue", "gross_profit", "ebit", "ebitda", "ebt", "net_income",
                "total_assets", "average_assets", "total_equity", "average_equity",
                "invested_capital", "diluted_shares", "current_price", "cash",
                "total_debt", "operating_cash_flow", "capex", "dividends_paid",
                "net_buybacks", "tax_rate"]
    v = {k: _number(data, k, positive=(k in {"diluted_shares", "current_price"})) for k in required}
    if not 0 <= v["tax_rate"] <= 1:
        raise ValueError("tax_rate must be between 0 and 1 (decimal form).")
    net_debt = v["total_debt"] - v["cash"]
    fcf = v["operating_cash_flow"] - v["capex"]
    eps = v["net_income"] / v["diluted_shares"]
    market_cap = v["current_price"] * v["diluted_shares"]
    ev = market_cap + net_debt
    nopat = v["ebit"] * (1 - v["tax_rate"])
    ratios = {
        "gross_margin": safe_divide(v["gross_profit"], v["revenue"]),
        "ebit_margin": safe_divide(v["ebit"], v["revenue"]),
        "ebitda_margin": safe_divide(v["ebitda"], v["revenue"]),
        "net_margin": safe_divide(v["net_income"], v["revenue"]),
        "roa": safe_divide(v["net_income"], v["average_assets"]),
        "roe": safe_divide(v["net_income"], v["average_equity"]),
        "roic": safe_divide(nopat, v["invested_capital"]),
        "interest_burden": safe_divide(v["ebt"], v["ebit"]),
        "tax_burden": safe_divide(v["net_income"], v["ebt"]),
        "asset_turnover": safe_divide(v["revenue"], v["average_assets"]),
        "equity_multiplier": safe_divide(v["average_assets"], v["average_equity"]),
        "eps_diluted": eps,
        "book_value_per_share": safe_divide(v["total_equity"], v["diluted_shares"]),
        "p_to_book": safe_divide(v["current_price"], v["total_equity"] / v["diluted_shares"]) if v["total_equity"] > 0 else None,
        "dividend_payout_ratio": safe_divide(v["dividends_paid"], v["net_income"]) if v["net_income"] > 0 else None,
        "total_payout_ratio": safe_divide(v["dividends_paid"] + v["net_buybacks"], v["net_income"]) if v["net_income"] > 0 else None,
        "fcf": fcf,
        "fcf_margin": safe_divide(fcf, v["revenue"]),
        "fcf_conversion": safe_divide(fcf, v["net_income"]),
        "net_debt": net_debt,
        "net_debt_to_ebitda": safe_divide(net_debt, v["ebitda"]),
        "market_cap": market_cap,
        "enterprise_value": ev,
        "pe_ttm": safe_divide(v["current_price"], eps) if eps > 0 else None,
        "ev_to_ebitda": safe_divide(ev, v["ebitda"]) if v["ebitda"] > 0 else None,
        "p_to_fcf": safe_divide(market_cap, fcf) if fcf > 0 else None,
        "dividend_yield": safe_divide(v["dividends_paid"], market_cap),
        "buyback_yield": safe_divide(v["net_buybacks"], market_cap),
        "total_shareholder_yield": safe_divide(v["dividends_paid"] + v["net_buybacks"], market_cap),
        "nopat": nopat,
        "tax_rate_input": v["tax_rate"],
    }
    ratios["dupont_5_step_roe"] = _product_or_none([
        ratios["interest_burden"], ratios["tax_burden"], ratios["ebit_margin"],
        ratios["asset_turnover"], ratios["equity_multiplier"]])
    ratios["duPont_roe_reconciliation_difference"] = (
        ratios["roe"] - ratios["dupont_5_step_roe"]
        if ratios["roe"] is not None and ratios["dupont_5_step_roe"] is not None else None)
    return ratios


def _product_or_none(values: Sequence[float | None]) -> float | None:
    if any(x is None for x in values):
        return None
    result = 1.0
    for x in values:
        result *= float(x)
    return result


def growth_rate(current: float, prior: float) -> float | None:
    """Growth rate; undefined when prior is zero or sign changes make it misleading."""
    if prior == 0 or current * prior < 0:
        return None
    return current / prior - 1


def calculate_eva_spread(roic: float | None, wacc: float | None) -> float | None:
    if roic is None or wacc is None:
        return None
    if not (isfinite(roic) and isfinite(wacc)):
        return None
    return roic - wacc

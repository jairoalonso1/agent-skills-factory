"""Explicit-input equity valuation models. Monetary units must be consistent."""
from __future__ import annotations
from collections.abc import Mapping, Sequence
from math import isfinite
from typing import Any


def _finite(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _positive(name: str, value: float) -> float:
    x = _finite(name, value)
    if x <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return x


def _validate_forecast(values: Sequence[float], name: str) -> list[float]:
    if len(values) == 0:
        raise ValueError(f"{name} must contain at least one forecast period")
    return [_finite(f"{name}[{i}]", x) for i, x in enumerate(values)]


def dcf_fcff(fcff_forecast: Sequence[float], wacc: float, terminal_growth: float,
             net_debt: float, diluted_shares: float, non_operating_assets: float = 0.0,
             other_senior_claims: float = 0.0, mid_year: bool = False) -> dict[str, Any]:
    """Unlevered DCF. FCFF forecast must be an explicit sequence, not an inferred growth rate."""
    flows = _validate_forecast(fcff_forecast, "fcff_forecast")
    wacc, g = _finite("wacc", wacc), _finite("terminal_growth", terminal_growth)
    shares = _positive("diluted_shares", diluted_shares)
    if wacc <= g:
        raise ValueError("WACC must exceed terminal growth")
    if g <= -1:
        raise ValueError("Terminal growth must exceed -100%")
    if wacc <= -1:
        raise ValueError("WACC must exceed -100%")
    periods = [i + (0.5 if mid_year else 1.0) for i in range(len(flows))]
    pv_explicit = sum(cf / ((1 + wacc) ** t) for cf, t in zip(flows, periods))
    terminal_value = flows[-1] * (1 + g) / (wacc - g)
    terminal_period = len(flows) - (0.5 if mid_year else 0.0)
    pv_terminal = terminal_value / ((1 + wacc) ** terminal_period)
    ev = pv_explicit + pv_terminal
    equity = ev - _finite("net_debt", net_debt) + _finite("non_operating_assets", non_operating_assets) - _finite("other_senior_claims", other_senior_claims)
    return {"method": "DCF_FCFF", "pv_explicit_fcff": pv_explicit,
            "terminal_value": terminal_value, "pv_terminal_value": pv_terminal,
            "terminal_value_share_of_ev": pv_terminal / ev if ev else None,
            "enterprise_value": ev, "equity_value": equity,
            "intrinsic_value_per_share": equity / shares, "periods": periods,
            "assumptions": {"wacc": wacc, "terminal_growth": g, "mid_year": mid_year}}


def dcf_fcfe(fcfe_forecast: Sequence[float], cost_of_equity: float, terminal_growth: float,
             diluted_shares: float, mid_year: bool = False) -> dict[str, Any]:
    """Levered DCF: discounts FCFE at cost of equity; no second net-debt subtraction."""
    flows = _validate_forecast(fcfe_forecast, "fcfe_forecast")
    ke, g = _finite("cost_of_equity", cost_of_equity), _finite("terminal_growth", terminal_growth)
    shares = _positive("diluted_shares", diluted_shares)
    if ke <= g:
        raise ValueError("Cost of equity must exceed terminal growth")
    if ke <= -1 or g <= -1:
        raise ValueError("Discount rate and terminal growth must exceed -100%")
    periods = [i + (0.5 if mid_year else 1.0) for i in range(len(flows))]
    pv_explicit = sum(cf / ((1 + ke) ** t) for cf, t in zip(flows, periods))
    tv = flows[-1] * (1 + g) / (ke - g)
    terminal_period = len(flows) - (0.5 if mid_year else 0.0)
    pv_tv = tv / ((1 + ke) ** terminal_period)
    equity = pv_explicit + pv_tv
    return {"method": "DCF_FCFE", "pv_explicit_fcfe": pv_explicit,
            "terminal_value": tv, "pv_terminal_value": pv_tv,
            "equity_value": equity, "intrinsic_value_per_share": equity / shares,
            "periods": periods, "assumptions": {"cost_of_equity": ke, "terminal_growth": g, "mid_year": mid_year}}


def ddm_multistage(dividend_per_share_0: float, cost_of_equity: float,
                   high_growth: float, high_growth_years: int, terminal_growth: float,
                   transition_growth: float | None = None, transition_years: int = 0) -> dict[str, Any]:
    """Multi-stage dividend discount model with an explicit transition path.

    `transition_growth` is the first transition-year growth rate. Subsequent
    transition years converge linearly to `terminal_growth`; with one
    transition year, that year uses `transition_growth` and the terminal
    stage begins in the following period.
    """
    d0 = _finite("dividend_per_share_0", dividend_per_share_0)
    ke = _finite("cost_of_equity", cost_of_equity)
    g1 = _finite("high_growth", high_growth)
    gt = _finite("terminal_growth", terminal_growth)
    if ke <= gt or ke <= -1 or gt <= -1: raise ValueError("Cost of equity must exceed terminal growth; both must exceed -100%")
    if g1 <= -1: raise ValueError("High growth must exceed -100%")
    if high_growth_years < 1 or transition_years < 0: raise ValueError("Invalid stage length")
    if transition_years and transition_growth is None: raise ValueError("transition_growth required when transition_years > 0")
    growths = [g1] * high_growth_years
    if transition_years:
        tg = _finite("transition_growth", transition_growth)
        if tg <= -1: raise ValueError("Transition growth must exceed -100%")
        if transition_years == 1:
            transition_path = [tg]
        else:
            transition_path = [tg + (gt - tg) * i / (transition_years - 1)
                               for i in range(transition_years)]
        growths.extend(transition_path)
    pv, dividend = 0.0, d0
    for t, growth in enumerate(growths, 1):
        dividend *= 1 + growth
        pv += dividend / ((1 + ke) ** t)
    tv = dividend * (1 + gt) / (ke - gt)
    pv_tv = tv / ((1 + ke) ** len(growths))
    return {"method": "DDM_MULTISTAGE", "intrinsic_value_per_share": pv + pv_tv,
            "pv_explicit_dividends": pv, "terminal_value": tv, "pv_terminal_value": pv_tv,
            "forecast_dividends": [d0 * __import__('functools').reduce(lambda a,b:a*(1+b), growths[:i+1], 1.0) for i in range(len(growths))],
            "assumptions": {"cost_of_equity": ke, "high_growth": g1, "high_growth_years": high_growth_years, "transition_growth": transition_growth, "transition_years": transition_years, "terminal_growth": gt}}


def total_payout_model(total_payout_forecast: Sequence[float], cost_of_equity: float,
                       terminal_growth: float, diluted_shares: float) -> dict[str, Any]:
    """Equity-level total payout valuation (dividends + net repurchases).

    Forecasts must be total cash returned to equity holders. Use net repurchases
    (repurchases less equity issuance) and avoid separately adding buyback yield.
    """
    payouts = _validate_forecast(total_payout_forecast, "total_payout_forecast")
    ke, g = _finite("cost_of_equity", cost_of_equity), _finite("terminal_growth", terminal_growth)
    shares = _positive("diluted_shares", diluted_shares)
    if ke <= g or ke <= -1 or g <= -1: raise ValueError("Cost of equity must exceed terminal growth; both must exceed -100%")
    pv = sum(x / ((1 + ke) ** (i + 1)) for i, x in enumerate(payouts))
    tv = payouts[-1] * (1 + g) / (ke - g)
    pv_tv = tv / ((1 + ke) ** len(payouts))
    equity = pv + pv_tv
    return {"method": "TOTAL_PAYOUT", "equity_value": equity,
            "intrinsic_value_per_share": equity / shares, "pv_explicit_payouts": pv,
            "terminal_value": tv, "pv_terminal_value": pv_tv,
            "assumptions": {"cost_of_equity": ke, "terminal_growth": g}}


def comparable_valuation(peers: Sequence[Mapping[str, Any]], subject_metric: float,
                         metric: str, diluted_shares: float | None = None,
                         net_debt: float | None = None, non_operating_assets: float = 0.0,
                         other_senior_claims: float = 0.0) -> dict[str, Any]:
    """Median/range peer valuation. Peer values must be consistently trailing or forward."""
    if metric not in {"pe", "ev_ebitda", "ev_ebit", "ev_sales", "p_fcf", "pb"}:
        raise ValueError("Unsupported comparable metric")
    _positive("subject_metric", subject_metric)
    if len(peers) < 3: raise ValueError("At least three defensible peers are required")
    multiples = []
    for peer in peers:
        value = _finite("peer multiple", peer[metric])
        if value > 0: multiples.append(value)
    if len(multiples) < 3: raise ValueError("At least three positive peer multiples are required")
    multiples.sort()
    median = multiples[len(multiples)//2] if len(multiples)%2 else (multiples[len(multiples)//2-1]+multiples[len(multiples)//2])/2
    low, high = multiples[0], multiples[-1]
    implied = {"bear": subject_metric * low, "base": subject_metric * median, "bull": subject_metric * high}
    if metric.startswith("ev_"):
        if net_debt is None or diluted_shares is None: raise ValueError("EV multiples require net_debt and diluted_shares")
        shares = _positive("diluted_shares", diluted_shares)
        debt = _finite("net_debt", net_debt)
        noa = _finite("non_operating_assets", non_operating_assets)
        claims = _finite("other_senior_claims", other_senior_claims)
        implied = {k: (v - debt + noa - claims) / shares for k,v in implied.items()}
        unit = "per_share"
    elif metric in {"pe", "p_fcf", "pb"}:
        unit = "per_share"
    else: unit = "multiple"
    return {"method": f"COMPARABLE_{metric.upper()}", "peer_count": len(multiples),
            "peer_multiples": multiples, "median_multiple": median,
            "implied_values": implied, "unit": unit}


def sum_of_the_parts(segments: Sequence[Mapping[str, Any]], net_debt: float,
                     diluted_shares: float, non_operating_assets: float = 0.0,
                     other_senior_claims: float = 0.0, holding_discount: float = 0.0) -> dict[str, Any]:
    """SOTP using segment enterprise values and an explicit holding-company discount."""
    shares = _positive("diluted_shares", diluted_shares)
    discount = _finite("holding_discount", holding_discount)
    if not 0 <= discount < 1: raise ValueError("holding_discount must be in [0, 1)")
    if not segments: raise ValueError("At least one segment is required")
    segment_values = []
    for s in segments:
        name = str(s["name"])
        ev = _positive(f"{name}.enterprise_value", s["enterprise_value"])
        segment_values.append({"name": name, "enterprise_value": ev})
    gross_ev = sum(s["enterprise_value"] for s in segment_values)
    discounted_ev = gross_ev * (1 - discount)
    equity = discounted_ev - _finite("net_debt", net_debt) + _finite("non_operating_assets", non_operating_assets) - _finite("other_senior_claims", other_senior_claims)
    return {"method": "SOTP", "segments": segment_values, "gross_segment_ev": gross_ev,
            "holding_discount": discount, "adjusted_segment_ev": discounted_ev,
            "equity_value": equity, "intrinsic_value_per_share": equity / shares}


def dcf_sensitivity(fcff_forecast: Sequence[float], wacc_values: Sequence[float],
                    terminal_growth_values: Sequence[float], net_debt: float,
                    diluted_shares: float) -> dict[str, Any]:
    """Return a WACC × terminal-growth grid; invalid cells are None, never hidden."""
    if len(wacc_values) == 0 or len(terminal_growth_values) == 0:
        raise ValueError("Sensitivity axes must not be empty")
    grid: dict[str, dict[str, float | None]] = {}
    for w in wacc_values:
        row = {}
        for g in terminal_growth_values:
            try:
                result = dcf_fcff(fcff_forecast, w, g, net_debt, diluted_shares)
                row[str(g)] = result["intrinsic_value_per_share"]
            except (ValueError, ZeroDivisionError):
                row[str(g)] = None
        grid[str(w)] = row
    return {"wacc_values": list(wacc_values), "terminal_growth_values": list(terminal_growth_values), "grid_per_share": grid}


def blended_valuation(method_results: Mapping[str, Mapping[str, float]],
                       weights: Mapping[str, float], current_price: float,
                       expected_dividend_per_share: float = 0.0,
                       roic: float | None = None, wacc: float | None = None,
                       buy_threshold: float = 0.12, sell_threshold: float = -0.05) -> dict[str, Any]:
    """Transparent weighted valuation. Rating is withheld if critical evidence is absent."""
    price = _positive("current_price", current_price)
    if not weights or set(weights) != set(method_results): raise ValueError("Weights must match exactly the included valuation methods")
    w = {k: _finite(f"weight.{k}", v) for k,v in weights.items()}
    if any(x < 0 for x in w.values()) or abs(sum(w.values()) - 1.0) > 1e-8:
        raise ValueError("Valuation weights must be non-negative and sum to 1.0")
    for name, values in method_results.items():
        if not {"Bear", "Base", "Bull"}.issubset(values): raise ValueError(f"{name} requires Bear, Base and Bull values")
        scenario_values = {case: _finite(f"{name}.{case}", values[case]) for case in ("Bear", "Base", "Bull")}
        if not scenario_values["Bear"] <= scenario_values["Base"] <= scenario_values["Bull"]: raise ValueError(f"{name} scenario ordering is invalid")
    targets = {case: sum(_finite(f"{m}.{case}", method_results[m][case]) * w[m] for m in w) for case in ("Bear","Base","Bull")}
    dividend = _finite("expected_dividend_per_share", expected_dividend_per_share)
    if dividend < 0: raise ValueError("expected_dividend_per_share cannot be negative")
    div_yield = dividend / price
    etr = targets["Base"] / price - 1 + div_yield
    if roic is None or wacc is None:
        rating = "NOT_RATED"
        reason = "ROIC and WACC evidence is incomplete; rating withheld."
    elif not (isfinite(float(roic)) and isfinite(float(wacc))):
        rating, reason = "NOT_RATED", "ROIC or WACC is not finite; rating withheld."
    elif etr >= buy_threshold and roic >= wacc:
        rating, reason = "BUY / OVERWEIGHT", "Expected total return exceeds the configured threshold and ROIC is at least WACC."
    elif etr < sell_threshold:
        rating, reason = "SELL / UNDERWEIGHT", "Expected total return is below the configured downside threshold."
    else:
        rating, reason = "HOLD / NEUTRAL", "Expected return or value-creation evidence does not meet the configured BUY/SELL conditions."
    return {"targets": targets, "current_price": price, "expected_dividend_yield": div_yield,
            "expected_total_return": etr, "rating": rating, "rating_rationale": reason,
            "weights": w, "roic": roic, "wacc": wacc}

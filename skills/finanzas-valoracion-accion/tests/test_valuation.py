import pytest
from scripts.valuation import (dcf_fcff, dcf_fcfe, ddm_multistage,
    total_payout_model, comparable_valuation, sum_of_the_parts,
    dcf_sensitivity, blended_valuation)


def test_fcff_dcf_equity_bridge_and_per_share():
    r = dcf_fcff([100, 110, 121], .10, .03, 200, 50)
    assert r["equity_value"] == pytest.approx(r["enterprise_value"] - 200)
    assert r["intrinsic_value_per_share"] == pytest.approx(r["equity_value"] / 50)


def test_fcff_rejects_invalid_terminal_spread():
    with pytest.raises(ValueError): dcf_fcff([100], .05, .05, 0, 10)


def test_fcfe_does_not_subtract_debt_again():
    r = dcf_fcfe([100, 110], .12, .03, 10)
    assert r["equity_value"] == pytest.approx(r["pv_explicit_fcfe"] + r["pv_terminal_value"])


def test_ddm_multistage_returns_positive_value():
    r = ddm_multistage(2.0, .10, .08, 3, .03, .05, 2)
    assert r["intrinsic_value_per_share"] > 0
    assert len(r["forecast_dividends"]) == 5
    # The first transition-year growth rate must use the explicit input.
    assert r["forecast_dividends"][3] == pytest.approx(r["forecast_dividends"][2] * 1.05)
    alternative = ddm_multistage(2.0, .10, .08, 3, .03, .02, 2)
    assert alternative["forecast_dividends"][3] != pytest.approx(r["forecast_dividends"][3])


def test_total_payout_model_is_equity_level():
    r = total_payout_model([100, 110, 120], .10, .03, 10)
    assert r["intrinsic_value_per_share"] == pytest.approx(r["equity_value"] / 10)


def test_comparables_use_median_and_ev_bridge():
    peers = [{"ev_ebitda": x} for x in [8, 10, 12, 14, 16]]
    r = comparable_valuation(peers, 100, "ev_ebitda", diluted_shares=10, net_debt=50)
    assert r["median_multiple"] == 12
    assert r["implied_values"]["base"] == pytest.approx((1200 - 50) / 10)


def test_comparables_require_three_peers():
    with pytest.raises(ValueError): comparable_valuation([{"pe": 10}], 2, "pe")


def test_sotp_applies_holding_discount_and_bridge():
    r = sum_of_the_parts([{"name": "A", "enterprise_value": 500}, {"name": "B", "enterprise_value": 300}], 100, 20, holding_discount=.10)
    assert r["equity_value"] == pytest.approx(620)


def test_sensitivity_marks_invalid_cells():
    r = dcf_sensitivity([100, 110], [.08, .10], [.02, .09], 0, 10)
    assert r["grid_per_share"]["0.08"]["0.09"] is None
    assert r["grid_per_share"]["0.1"]["0.02"] is not None


def test_blend_requires_weights_sum_to_one_and_withholds_rating():
    methods = {"DCF": {"Bear": 80, "Base": 100, "Bull": 120}}
    with pytest.raises(ValueError): blended_valuation(methods, {"DCF": .8}, 90)
    r = blended_valuation(methods, {"DCF": 1.0}, 90)
    assert r["rating"] == "NOT_RATED"


def test_discount_rates_and_scenario_values_must_be_finite():
    with pytest.raises(ValueError): dcf_fcff([100], .10, -1.0, 0, 10)
    with pytest.raises(ValueError): blended_valuation({"DCF":{"Bear":80,"Base":float("nan"),"Bull":120}}, {"DCF":1.0}, 90, roic=.2, wacc=.1)


def test_blended_valuation_does_not_mutate_inputs():
    methods={"DCF":{"Bear":80,"Base":100,"Bull":120}}
    before={k:dict(v) for k,v in methods.items()}
    blended_valuation(methods,{"DCF":1.0},90,roic=.2,wacc=.1)
    assert methods == before

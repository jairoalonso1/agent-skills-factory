import pytest
from scripts.financial_analysis import calculate_financial_ratios, safe_divide, growth_rate

BASE = {"revenue":1000,"gross_profit":600,"ebit":200,"ebitda":250,"ebt":180,
"net_income":140,"total_assets":2000,"average_assets":1900,"total_equity":900,
"average_equity":850,"invested_capital":1200,"diluted_shares":100,"current_price":20,
"cash":100,"total_debt":300,"operating_cash_flow":180,"capex":50,
"dividends_paid":30,"net_buybacks":20,"tax_rate":0.22}


def test_ratios_reconcile_du_pont_and_equity_value():
    r = calculate_financial_ratios(BASE)
    assert r["net_debt"] == 200
    assert r["market_cap"] == 2000
    assert r["roe"] == pytest.approx(r["dupont_5_step_roe"])
    assert r["fcf"] == 130


def test_missing_input_is_not_silently_imputed():
    data = dict(BASE); del data["ebt"]
    with pytest.raises(ValueError, match="missing"): calculate_financial_ratios(data)


def test_invalid_tax_rate_rejected():
    data = dict(BASE); data["tax_rate"] = 18
    with pytest.raises(ValueError): calculate_financial_ratios(data)


def test_safe_divide_and_growth_edge_cases():
    assert safe_divide(1, 0) is None
    assert growth_rate(10, 0) is None
    assert growth_rate(-2, 4) is None
    assert growth_rate(12, 10) == pytest.approx(.2)

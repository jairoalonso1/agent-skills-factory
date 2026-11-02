"""End-to-end profile tests use synthetic data, not real issuer research."""
import json
from pathlib import Path
import pytest
from scripts.run_research import run


def _package(issuer, ticker, sector, methods, financials, scenarios=True):
    return {
        "issuer": f"{issuer} (synthetic test profile)", "ticker": ticker, "exchange": "NYSE/NASDAQ",
        "valuation_date": "2026-10-31", "current_price": 100.0,
        "security_currency": "USD", "financial_reporting_currency": "USD", "valuation_currency": "USD",
        "reporting_currency": "USD", "rating": "NOT_RATED",
        "investment_thesis": {"summary": "Synthetic fixture to test issuer-archetype handling; not a real investment view."},
        "industry": {"sector": sector, "business_model": "Synthetic profile", "peer_selection_basis": "Illustrative peers only", "peers": ["Peer A", "Peer B"]},
        "financials": financials,
        "valuation": {"methods_used": methods, "method_selection_rationale": f"Synthetic profile tests suitability disclosure for {sector}.", "intrinsic_value_per_share": 105.0},
        "scenarios": ({
            "bear": {"target_price": 80.0, "drivers": ["Synthetic downside assumptions"]},
            "base": {"target_price": 105.0, "drivers": ["Synthetic central assumptions"]},
            "bull": {"target_price": 125.0, "drivers": ["Synthetic upside assumptions"]},
        } if scenarios else {key: {"status": "not_estimated"} for key in ("bear", "base", "bull")}),
        "risks": ["Synthetic test risk; not issuer-specific research."],
        "sources": [{"source_id": "TEST-SYNTHETIC-1", "publisher": "Test fixture", "title": "Synthetic test data — not a factual issuer source", "url": "https://example.com/synthetic-test-fixture", "published_at": "2026-10-31", "retrieved_at": "2026-10-31T16:00:00Z", "evidence_type": "analyst_assumption", "notes": "Only used to exercise the reporting pipeline."}],
        "assumptions": ["All values are synthetic and must not be interpreted as real issuer data."],
        "data_gaps": [],
    }


@pytest.mark.parametrize("package", [
    _package("Intel", "INTC", "Semiconductors / manufacturing", ["FCFF DCF", "EV/EBITDA", "EV/Sales"], {"revenue": 50000, "ebitda": 10000, "free_cash_flow": 5000, "net_income": 2000, "capex": 7000}),
    _package("JPMorgan Chase", "JPM", "Banking / financial services", ["DDM", "P/B", "P/E"], {"net_interest_income": 60000, "net_income": 50000, "book_value": 300000, "tangible_book_value": 250000, "roe": 0.15, "capital_adequacy_ratio": 0.14}),
    _package("NVIDIA", "NVDA", "Semiconductors / accelerated computing", ["FCFF DCF", "EV/Sales", "EV/EBITDA"], {"revenue": 100000, "ebitda": 60000, "free_cash_flow": 45000, "net_income": 50000, "research_and_development": 10000}),
])
def test_company_archetype_generates_all_four_formats(package, tmp_path):
    source = tmp_path / f"{package['ticker']}.json"
    source.write_text(json.dumps(package), encoding="utf-8")
    result = run(source, tmp_path / "out", package["ticker"])
    assert result["schema_validation"] == "passed"
    assert result["quality_check"]["passed"] is True
    assert set(result["artifacts"]) == {"html", "xlsx", "docx", "pptx"}
    assert all(Path(path).is_file() and Path(path).stat().st_size > 500 for path in result["artifacts"].values())


def test_insufficient_data_generates_transparent_not_rated_reports(tmp_path):
    package = _package("Insufficient Data Co", "IDCO", "Unclassified", [], {"revenue": None}, scenarios=False)
    package["valuation"] = {"method": "Not estimated", "reason": "Insufficient verified financial history to support a defensible valuation."}
    package["rating"] = "NOT_RATED"
    source = tmp_path / "insufficient.json"
    source.write_text(json.dumps(package), encoding="utf-8")
    result = run(source, tmp_path / "out", "insufficient")
    assert result["quality_check"]["passed"] is True
    html = Path(result["artifacts"]["html"]).read_text(encoding="utf-8")
    assert "NOT_RATED" in html and "No estimado" in html
    assert all(Path(path).is_file() for path in result["artifacts"].values())

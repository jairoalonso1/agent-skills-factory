from scripts.research_quality import validate_research_package


def test_package_quality_flags_missing_sources_and_scenario_order():
    p={"issuer":"Example plc","valuation_date":"2026-10-31","reporting_currency":"USD",
       "financials":{"revenue":1},"valuation":{"method":"DCF"},
       "scenarios":{"bear":{"target_price":12},"base":{"target_price":10},"bull":{"target_price":15}},
       "risks":["execution"],"sources":[]}
    r=validate_research_package(p)
    assert not r["passed"]
    assert "invalid:scenario_order" in r["issues"]
    assert "missing:evidence_sources" in r["issues"]


def test_research_package_example_matches_json_schema():
    import json
    from pathlib import Path
    from jsonschema import Draft202012Validator, FormatChecker
    root = Path(__file__).resolve().parents[1]
    schema = json.loads((root / "schemas/research-package.schema.json").read_text())
    example = json.loads((root / "examples/research-package.example.json").read_text())
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(example))
    assert not errors, [e.message for e in errors]


def test_valid_source_dates_and_duplicate_ids_are_checked():
    from scripts.research_quality import validate_research_package
    p={"issuer":"Example","valuation_date":"2026-10-31","reporting_currency":"USD",
       "financials":{"revenue":1},"valuation":{"method":"DCF"},"risks":["risk"],
       "scenarios":{"bear":{"target_price":8},"base":{"target_price":10},"bull":{"target_price":12}},
       "sources":[{"source_id":"S1","publisher":"Issuer","title":"Filing","url":"https://example.com",
                   "published_at":"not-a-date","retrieved_at":"2026-10-31T10:00:00Z","evidence_type":"reported"},
                  {"source_id":"S1","publisher":"Issuer","title":"Filing 2","url":"https://example.com/2",
                   "published_at":"2026-10-31","retrieved_at":"2026-10-31T10:00:00Z","evidence_type":"reported"}]}
    result=validate_research_package(p)
    assert "source[0]:invalid:published_at" in result["issues"]
    assert "source[1]:duplicate:source_id" in result["issues"]



def test_disclosed_non_estimated_scenarios_are_valid_but_unknown_status_is_not():
    package = {
        "issuer": "Insufficient plc", "valuation_date": "2026-10-31", "reporting_currency": "USD",
        "financials": {"revenue": 100}, "valuation": {"method": "Not estimated", "reason": "Insufficient evidence to support a defensible valuation."},
        "scenarios": {key: {"status": "not_estimated"} for key in ("bear", "base", "bull")},
        "risks": ["Insufficient data"],
        "sources": [{"source_id": "S1", "publisher": "Issuer", "title": "Filing", "url": "https://example.com", "published_at": "2026-10-30", "retrieved_at": "2026-10-31T12:00:00Z", "evidence_type": "reported"}],
    }
    assert validate_research_package(package)["passed"] is True
    package["scenarios"]["base"]["status"] = "guess"
    result = validate_research_package(package)
    assert result["passed"] is False
    assert "invalid:scenario_status:base" in result["issues"]

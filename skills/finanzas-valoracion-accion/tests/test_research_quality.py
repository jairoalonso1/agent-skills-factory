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


def _ledger_package():
    return {"issuer":"Example", "valuation_date":"2026-10-31", "reporting_currency":"USD", "financials":{"revenue":100,"roic":0.12}, "valuation":{"method":"DCF"}, "scenarios":{"bear":{"target_price":8},"base":{"target_price":10},"bull":{"target_price":12}}, "risks":["risk"], "sources":[{"source_id":"S1","publisher":"Issuer","title":"Filing","url":"https://example.com/filing","published_at":"2026-10-30","retrieved_at":"2026-10-31T10:00:00Z","evidence_type":"reported"}]}

def test_observation_ledger_validates_source_and_calculation_lineage():
    p=_ledger_package(); p["data_observations"]=[{"observation_id":"O1","field":"revenue","value":100,"unit":"USD millions","evidence_type":"reported","source_ids":["S1"]},{"observation_id":"O2","field":"growth","value":0.1,"unit":"ratio","evidence_type":"calculated","input_observation_ids":["O1"],"transformation":"(current/prior)-1"}]
    assert validate_research_package(p)["passed"] is True
    p["data_observations"][1]["input_observation_ids"]=["MISSING"]
    assert "observation[1]:unresolved:input_observation_id:MISSING" in validate_research_package(p)["issues"]

def test_observation_ledger_rejects_duplicate_ids_and_unknown_sources():
    p=_ledger_package(); p["data_observations"]=[{"observation_id":"O1","field":"revenue","value":100,"unit":"USD millions","evidence_type":"reported","source_ids":["NOPE"]},{"observation_id":"O1","field":"cost","value":50,"unit":"USD millions","evidence_type":"reported","source_ids":["S1"]}]
    issues=validate_research_package(p)["issues"]
    assert "observation[1]:duplicate:observation_id" in issues
    assert "observation[0]:unresolved:source_id:NOPE" in issues

def test_roic_methodology_is_a_warning_not_a_forced_formula():
    p=_ledger_package(); r=validate_research_package(p)
    assert r["passed"] and "missing:roic_methodology_definition" in r["warnings"]
    p["roic_definition"]={"formula":"NOPAT / Average Invested Capital","denominator_definition":"Average operating capital excluding excess cash","tax_rate_basis":"normalized"}
    assert "missing:roic_methodology_definition" not in validate_research_package(p)["warnings"]

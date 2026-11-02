import json
from pathlib import Path
from scripts.run_research import run


def test_cli_runner_generates_and_verifies_all_deliverables(tmp_path):
    root=Path(__file__).resolve().parents[1]
    source=root/"examples/research-package.example.json"
    result=run(source,tmp_path,"synthetic-example")
    assert result["schema_validation"] == "passed"
    assert result["quality_check"]["passed"] is True
    assert set(result["artifacts"]) == {"html","xlsx","docx","pptx"}
    assert Path(result["manifest"]).is_file()
    assert all(Path(path).is_file() and Path(path).stat().st_size > 0 for path in result["artifacts"].values())


def test_cli_runner_rejects_incomplete_package(tmp_path):
    bad=tmp_path/"bad.json"; bad.write_text(json.dumps({"issuer":"Missing data"}))
    try:
        run(bad,tmp_path/"out")
    except ValueError as exc:
        assert "schema_errors" in str(exc)
    else:
        raise AssertionError("incomplete research package must not generate reports")



def test_schema_accepts_explicit_non_estimated_scenario_statuses():
    from scripts.run_research import validate_schema
    import json
    skill_root = Path(__file__).resolve().parents[1]
    package = json.loads((skill_root / "examples" / "research-package.example.json").read_text())
    package["scenarios"] = {key: {"status": "not_estimated"} for key in ("bear", "base", "bull")}
    errors = validate_schema(package, skill_root / "schemas" / "research-package.schema.json")
    assert errors == []
    package["scenarios"]["base"]["status"] = "speculative"
    errors = validate_schema(package, skill_root / "schemas" / "research-package.schema.json")
    assert errors

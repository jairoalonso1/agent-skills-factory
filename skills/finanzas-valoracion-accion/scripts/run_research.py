"""CLI runner for schema-checked, standardized Equity Research deliverables."""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from .reporting import generate_research_deliverables
from .research_quality import validate_research_package


def validate_schema(package: dict, schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{'/'.join(str(x) for x in e.path) or '<root>'}: {e.message}" for e in validator.iter_errors(package)]


def run(input_path: Path, output_dir: Path, basename: str | None = None) -> dict:
    package = json.loads(input_path.read_text(encoding="utf-8"))
    skill_root = Path(__file__).resolve().parents[1]
    schema_errors = validate_schema(package, skill_root / "schemas" / "research-package.schema.json")
    quality = validate_research_package(package)
    if schema_errors or not quality["passed"]:
        raise ValueError(json.dumps({"schema_errors": schema_errors, "quality": quality}, ensure_ascii=False, indent=2))
    artifacts = generate_research_deliverables(package, output_dir, basename)
    for kind, filename in artifacts.items():
        path = Path(filename)
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"Artifact verification failed: {kind} ({filename})")
    manifest = {
        "issuer": package["issuer"], "valuation_date": package["valuation_date"],
        "reporting_currency": package["reporting_currency"], "quality_check": quality,
        "schema_validation": "passed", "artifacts": artifacts,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "Artifact creation and structural checks do not certify financial accuracy or investment suitability."
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / f"{basename or 'equity-research'}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest["manifest"] = str(manifest_path)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate standardized Equity Research deliverables from a validated JSON package.")
    parser.add_argument("input", type=Path, help="Path to a populated research-package JSON file")
    parser.add_argument("--out", type=Path, default=Path("artifacts"), help="Output directory")
    parser.add_argument("--name", default=None, help="Output file basename")
    args = parser.parse_args(argv)
    try:
        result = run(args.input, args.out, args.name)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

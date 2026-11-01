#!/usr/bin/env python3
"""Validate the Skill registry, package structure, AX schemas and release metadata."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "skills.json"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RELEASE_STATUSES = {
    "draft", "candidate", "validated", "runtime-tested",
    "evaluated", "managed-service", "deprecated",
}
EVALUATION_STATUSES = {"not-run", "in-progress", "passed", "failed", "partial"}
RUNTIME_STATUSES = {"documented", "declared", "tested", "not-tested", "failed"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} is invalid JSON: {exc}")


def validate_schemas_and_examples() -> None:
    pairs = [
        ("schemas/ax-workflow.schema.json", "examples/equity-research-workflow.json"),
        ("schemas/skill-invocation.schema.json", "examples/skill-invocation.json"),
        ("schemas/skill-result.schema.json", "examples/skill-result.json"),
        ("schemas/skill-release.schema.json", "examples/skill-release.example.json"),
    ]
    for schema_name, example_name in pairs:
        schema_path = ROOT / schema_name
        example_path = ROOT / example_name
        if not schema_path.is_file() or not example_path.is_file():
            fail(f"missing schema/example pair: {schema_name}, {example_name}")
        schema = read_json(schema_path)
        example = read_json(example_path)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(example), key=lambda error: list(error.path))
        if errors:
            details = "; ".join(
                f"{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
                for error in errors
            )
            fail(f"{example_name} does not satisfy {schema_name}: {details}")
        print(f"OK: {example_name} validates against {schema_name}")


def validate_release_metadata(manifest: dict, skill_id: str) -> None:
    status = manifest.get("status")
    if status not in RELEASE_STATUSES:
        fail(f"{skill_id}: unsupported or missing release status: {status!r}")

    evaluation = manifest.get("evaluation")
    if not isinstance(evaluation, dict) or evaluation.get("status") not in EVALUATION_STATUSES:
        fail(f"{skill_id}: evaluation.status must be explicit and valid")

    runtime_items = manifest.get("runtime_compatibility")
    if not isinstance(runtime_items, list) or not runtime_items:
        fail(f"{skill_id}: runtime_compatibility must be a non-empty list")
    for item in runtime_items:
        if item.get("status") not in RUNTIME_STATUSES:
            fail(f"{skill_id}: invalid runtime compatibility status: {item.get('status')!r}")
        if item.get("status") == "tested" and not item.get("tested_at"):
            fail(f"{skill_id}: tested runtime entries must include tested_at")

    data_dependencies = manifest.get("data_dependencies")
    if not isinstance(data_dependencies, list):
        fail(f"{skill_id}: data_dependencies must be an explicit list")
    for dependency in data_dependencies:
        for field in ("name", "access_mode", "license_status", "provenance_required"):
            if field not in dependency:
                fail(f"{skill_id}: data dependency is missing {field}")


def main() -> None:
    if not REGISTRY.is_file():
        fail("registry/skills.json is missing")

    registry = read_json(REGISTRY)
    if registry.get("schema_version") != "1.0.0":
        fail("unsupported or missing registry schema_version")

    skills = registry.get("skills")
    if not isinstance(skills, list) or not skills:
        fail("registry must contain a non-empty skills array")

    seen: set[str] = set()
    for entry in skills:
        skill_id = entry.get("id", "")
        if not NAME_RE.fullmatch(skill_id):
            fail(f"invalid skill id: {skill_id!r}")
        if skill_id in seen:
            fail(f"duplicate skill id: {skill_id}")
        seen.add(skill_id)

        paths = [
            ROOT / entry.get("path", ""),
            ROOT / entry.get("skill_file", ""),
            ROOT / entry.get("manifest", ""),
        ]
        for path in paths:
            if not path.exists():
                fail(f"missing registered path: {path.relative_to(ROOT)}")

        skill_file = paths[1]
        content = skill_file.read_text(encoding="utf-8")
        if not content.startswith("---\n"):
            fail(f"{skill_file.relative_to(ROOT)} must start with YAML frontmatter")
        parts = content.split("---", 2)
        if len(parts) < 3:
            fail(f"{skill_file.relative_to(ROOT)} has unclosed YAML frontmatter")
        frontmatter = parts[1]
        if not re.search(r"(?m)^name:\\s*" + re.escape(skill_id) + r"\\s*$", frontmatter):
            fail(f"{skill_file.relative_to(ROOT)} name does not match registry id")
        if not re.search(r"(?m)^description:\\s*.+$", frontmatter):
            fail(f"{skill_file.relative_to(ROOT)} is missing description")

        manifest = read_json(paths[2])
        if manifest.get("id") != skill_id:
            fail(f"{paths[2].relative_to(ROOT)} id does not match registry")
        if manifest.get("version") != entry.get("version"):
            fail(f"version mismatch for {skill_id}")
        validate_release_metadata(manifest, skill_id)

        if entry.get("evaluation", {}).get("status") != manifest["evaluation"]["status"]:
            fail(f"evaluation status mismatch for {skill_id}")

    validate_schemas_and_examples()
    print(f"OK: validated {len(skills)} Skill package(s), release metadata and AX contracts.")


if __name__ == "__main__":
    main()

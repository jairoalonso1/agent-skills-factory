#!/usr/bin/env python3
"""Validate the registry and basic Agent Skill package structure."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "skills.json"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not REGISTRY.is_file():
        fail("registry/skills.json is missing")

    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"registry/skills.json is invalid JSON: {exc}")

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
        if not re.search(r"(?m)^name:\s*" + re.escape(skill_id) + r"\s*$", frontmatter):
            fail(f"{skill_file.relative_to(ROOT)} name does not match registry id")
        if not re.search(r"(?m)^description:\s*.+$", frontmatter):
            fail(f"{skill_file.relative_to(ROOT)} is missing description")

        manifest = json.loads(paths[2].read_text(encoding="utf-8"))
        if manifest.get("id") != skill_id:
            fail(f"{paths[2].relative_to(ROOT)} id does not match registry")
        if manifest.get("version") != entry.get("version"):
            fail(f"version mismatch for {skill_id}")

    print(f"OK: validated {len(skills)} Skill package(s).")


if __name__ == "__main__":
    main()

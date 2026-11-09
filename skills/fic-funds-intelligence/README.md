# FIC Funds Intelligence

Portable specialist service for analysis and institutional HTML reporting of Colombian FICs.

## Primary deliverables

- Fund factsheet HTML (`factsheet` profile).
- Fund peer-comparison HTML (`comparative` profile).
- Structured result with fund IDs, cutoff, metrics, category snapshot, evidence, warnings and artifact provenance.

Frontera Funds supplies two reference report designs. It is not a dependency. The skill can run with other authorized sources and tools, and can still produce the same defined report profiles.

## Package

- `SKILL.md`: service specification, workflow and quality gates.
- `manifest.json`: machine-readable service metadata, integrations and portability.
- `references/report-profiles.md`: required contents and layout standards for both HTML profiles.
- `references/source-and-methodology.md`: SFC, MCP, category snapshot and interpretation policy.
- `schemas/fic-report.schema.json`: domain report payload.
- `scripts/validate_html_report.py`: lightweight HTML artifact validation (Python standard library only).
- `examples/`: factsheet and comparative result fixtures.
- `tests/`: deterministic validation tests.

The package does not copy the Frontera app, the FIC classifier or the MCP implementation.

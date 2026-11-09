# Frontera Funds SKaaS — FIC Funds Intelligence

FIC Funds Intelligence is a portable specialist Skill in the Frontera Funds product family. It standardizes institutional analysis and branded HTML reporting for Colombian collective investment funds (FICs).

## Primary deliverables

- Fund factsheet HTML (`factsheet` profile).
- Peer-comparison HTML (`comparative` profile).
- Structured result with fund identifiers, cutoff, metrics, category snapshot, evidence, warnings and artifact provenance.

## Independent product components

Frontera Funds may be offered through three separately packageable components:

1. **Skill:** portable methodology, analytical workflow, report contract, templates, brand rules and quality checks.
2. **Data access:** separately authorized access to regulatory and other permitted data through capabilities exposed by the host environment.
3. **Managed service:** an integrated service combining the Skill, data access and managed execution/support under separate commercial terms.

The Skill does not bundle, install or require a particular MCP, connector, API vendor, endpoint, private SaaS codebase or infrastructure. The host agent/runtime supplies authorized data and artifact capabilities.

## Package

- `SKILL.md`: service specification, workflow and quality gates.
- `manifest.json`: machine-readable service metadata, portability and commercial component model.
- `references/report-profiles.md`: required analytical contents and chart standards.
- `references/brand-identity.md`: brand identity and reference-mark provenance.
- `references/design-tokens.json`: light institutional palette, typography and layout tokens.
- `references/html-rendering-contract.md`: mandatory HTML template, portability and preflight contract.
- `templates/`: canonical factsheet and comparative report templates.
- `references/source-and-methodology.md`: regulatory source, data-access contract, category snapshot and interpretation policy.
- `schemas/fic-report.schema.json`: structured report payload.
- `scripts/validate_html_report.py`: lightweight HTML artifact validation (Python standard library only).
- `examples/` and `tests/`: illustrative payloads and deterministic checks.

The bundled Frontera Funds reference mark was extracted from a user-supplied factsheet HTML reference (`user_supplied_reference`); it is not independently trademark-verified. The mark and brand identity are excluded from the package's MIT code license and may be used only for authorized Frontera Funds distribution.

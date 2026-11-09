# Frontera Funds SKaaS — FIC Funds Intelligence

FIC Funds Intelligence is a specialist SKaaS product in the Frontera Funds ecosystem. It delivers institutional analysis and branded HTML reporting for Colombian FICs.

## Primary deliverables

- Fund factsheet HTML (`factsheet` profile).
- Fund peer-comparison HTML (`comparative` profile).
- Structured result with fund IDs, cutoff, metrics, category snapshot, evidence, warnings and artifact provenance.

Frontera Funds is the product brand and quality standard. Generated reports are Frontera Funds SKaaS deliverables and must follow the canonical light institutional design system and templates. The bundled mark is extracted from the user-supplied factsheet HTML reference (`user_supplied_reference`); it is not independently trademark-verified. The service is implementation-independent from the private Frontera SaaS: it does not import its code, APIs, infrastructure, credentials or runtime.

## Package

- `SKILL.md`: service specification, workflow and quality gates.
- `manifest.json`: machine-readable service metadata, integrations and portability.
- `references/report-profiles.md`: required contents and layout standards for both HTML profiles.
- `references/brand-identity.md`: Frontera Funds SKaaS identity, reference-mark provenance and visual-quality requirements.
- `references/design-tokens.json`: machine-readable light institutional palette, typography and layout tokens.
- `references/html-rendering-contract.md`: mandatory HTML template, portability and preflight contract.
- `templates/factsheet.html` and `templates/comparative.html`: canonical report templates.
- `references/source-and-methodology.md`: SFC, MCP, category snapshot and interpretation policy.
- `schemas/fic-report.schema.json`: domain report payload.
- `scripts/validate_html_report.py`: lightweight HTML artifact validation (Python standard library only).
- `examples/`: factsheet and comparative result fixtures.
- `tests/`: deterministic validation tests.

The package does not copy or depend on the private Frontera SaaS implementation, the FIC classifier or the MCP implementation. The reference mark extracted from the user-supplied factsheet HTML is included at `assets/frontera-funds-mark.svg`; do not redraw or infer a replacement. A newer mark should be supplied and approved by the brand owner.


Brand asset notice: the Frontera Funds name, mark and visual identity are brand assets and are not relicensed under MIT. Use them only for authorized Frontera Funds product distribution. See references/brand-identity.md.

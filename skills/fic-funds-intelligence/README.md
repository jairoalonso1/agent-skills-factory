# Frontera Funds SKaaS — FIC Funds Intelligence

FIC Funds Intelligence is a portable specialist Skill in the Frontera Funds product family. It standardizes institutional analysis and branded HTML reporting for Colombian collective investment funds (FICs).

## Primary deliverables

- Fund factsheet HTML (`factsheet` profile).
- Peer-comparison HTML: `analitico_completo` and `tabla_ejecutiva` (or `ambos`) profiles, generated from the same data snapshot.
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

## Golden masters and canonical executable distribution

This Skill includes the two original Frontera Funds comparative HTML artifacts in `references/golden-masters/`, with SHA-256 tests, plus the TypeScript renderer copied without independent modifications from the specialized source repository.

- Source of truth: `jairoalonso1/frontera-funds-intelligence-skills`.
- Factory is a packaged distribution; changes to `src/` must come from the specialized source repository.
- Node.js >=22, run `node --experimental-strip-types scripts/render-report.ts input.json output.html`.
- Original HTML reference tests: `node --experimental-strip-types --test tests/golden-masters.test.ts`.
- **Current limit:** the renderer produces both profiles deterministically; it is not yet certified visually identical to the original SaaS examples. The `templates/` directory is an older noncanonical representation.

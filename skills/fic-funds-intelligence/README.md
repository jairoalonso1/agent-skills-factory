# Frontera Funds SKaaS — FIC Funds Intelligence

Portable specialist Skill for evidence-led institutional reporting on Colombian collective investment funds (FICs). The initial report standard contains exactly two standardized deliverables: **Fund Factsheet** and **Comparative Report**.

## Standardized deliverables

- `factsheet` — one fund, one business code, one reporting cutoff; A4 portrait.
- `comparative` — two to eight funds with aligned cutoff and comparable periods; A4 landscape.
- HTML is the primary artifact; a structured JSON result accompanies the report contract.

Fund discovery and other data-intelligence operations may support report intake, but they are not additional standardized report profiles.

## Report standard and configuration

- `standards/report-standard.yaml` — scope, principles, product boundaries and conformance dimensions.
- `standards/metric-definitions.yaml` — metric semantics, formulas, prerequisites and display rules.
- `standards/data-contract.yaml` — entity identity, data granularity, provenance and comparison rules.
- `standards/quality-gates.yaml` — blocking and disclosure quality checks.
- `profiles/` — versioned factsheet and comparative section specifications.
- `themes/frontera-funds.yaml` — default light institutional Frontera theme.
- `themes/neutral-institutional.yaml` — unbranded fallback theme.
- `configuration/defaults.yaml` and `configuration/client-overrides.schema.json` — defaults and validated client customization.
- `compatibility/` — capability requirements and model/runtime execution profiles.

Branding is configurable, but overrides cannot change metric formulas, required report sections, source provenance, entity keys, comparability rules or quality gates. Only authorized logos and brand assets may be used.

## Independent product components

1. **Skill:** portable methodology, report profiles, templates, brand configuration and quality checks.
2. **Data access:** separately authorized data services exposed by the host.
3. **Managed service:** an integrated offer combining Skill, data access and managed execution under separate commercial terms.

The Skill does not bundle, install or require a particular MCP, connector, API vendor, endpoint, private SaaS codebase or infrastructure. The host agent/runtime maps available tools to the abstract data capabilities.

## Model compatibility

Execution is selected by capabilities rather than model names. Orchestration, analytical reasoning, deterministic computation, document generation and visual QA may be performed by one model, several specialized models or a model plus deterministic runtime. Cross-model equivalence is not claimed until empirically tested.

## Package map

- `SKILL.md`: service specification and workflow.
- `standards/`: report, metric, data and quality contracts.
- `profiles/`: factsheet and comparative report specifications.
- `themes/` and `configuration/`: default brand and authorized overrides.
- `compatibility/`: host capability requirements and execution profiles.
- `templates/`: canonical HTML scaffolds.
- `references/`: source, methodology, identity and rendering guidance.
- `schemas/`, `examples/`, `scripts/`, `tests/`: output validation and package tests.

The bundled Frontera reference mark is a user-supplied asset, not independently trademark-verified. It is excluded from the package's MIT code license and may be used only for authorized Frontera Funds distribution.

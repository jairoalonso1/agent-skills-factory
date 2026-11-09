---
name: fic-funds-intelligence
description: Delivers Frontera Funds-branded institutional analysis and HTML reports for Colombian collective investment funds (FICs) as a portable SKaaS service. Supports factsheets, peer comparisons, fund discovery and industry analysis using authorized SFC data, optional MCP tools and optional categorization snapshots.
---

# FIC Funds Intelligence

**Created by Jairo Alonso González**

## Mandatory HTML rendering contract

HTML generation is deterministic, not an invitation to improvise a dashboard. Before generating any report, read:
- `references/brand-identity.md`
- `references/design-tokens.json`
- `references/html-rendering-contract.md`
- `references/report-profiles.md`

Select and populate the canonical template:
- One fund: `templates/factsheet.html`
- Two or more funds: `templates/comparative.html`

Do not start from a generic dashboard, create a new visual system, or switch to a dark theme. The mandatory default is the light institutional style of the user-supplied Frontera Funds SaaS factsheet: white page, soft gray panels, dark slate text, subtle neutral borders, restrained green accent, Roboto/system sans-serif, centered report header, KPI cards, analytical sections, legible tables and institutional footer.

Use the bundled reference mark at `assets/frontera-funds-mark.svg` exactly as supplied, paired with the “Frontera Funds” wordmark. This SVG was extracted from a user-supplied factsheet reference; do not claim independent trademark verification. Do not redraw, approximate, recolor or replace it with an invented mark. If it cannot be packaged, use text-only wordmark and emit `reference_mark_unavailable`.

Produce a portable single HTML file: embed CSS, inline SVG charts and the reference mark where practical. Do not require Tailwind CDN, remote chart libraries, network fonts or a proprietary runtime. Preserve every required section in the selected report profile. If data is unavailable, retain the section and state why; never silently delete it. Resolve every template placeholder, escape untrusted text, and never insert source HTML as markup.

Before delivery, run structural and brand tests where Python is available. Render/inspect in a browser when available; if not, state that visual rendering was not performed. A passing structural test is not pixel-level visual validation.

## Service promise

Deliver a consistent, evidence-led institutional report about a Colombian FIC, a peer group or a defined segment of the FIC industry. The primary artifact is a readable, portable HTML report using one of two report profiles:
1. **Fund factsheet** — one fund's identity, performance, risk, history and diagnostics.
2. **Comparative report** — consistent side-by-side comparison of two or more funds, with common-period metrics and ranking context.

This Skill is implementation-independent from the private Frontera Funds SaaS. It does not import its application code, services, APIs, infrastructure, credentials or proprietary runtime. The report renderer is independent; product identity and report quality are consistent.

The Skill provides methodology, orchestration guidance, report specifications, lightweight validation and a portable output contract. It does not bundle or duplicate the classifier, MCP implementation or a large analytics library.

## Scope

**Supported operations**
- `fund_factsheet`: institutional report for one fund/business code.
- `peer_comparison`: comparison of 2–8 funds, aligned to one cutoff and comparable horizons.
- `fund_discovery`: discover funds by name, manager, SFC business code, subtype or category.
- `category_universe`: inspect taxonomy and category membership from an authorized snapshot.
- `industry_snapshot`: manager AUM, market shares, flows, rankings and liquidity indicators.
- `custom_analysis`: model-led analysis using authorized data, with the same provenance and report contract.

**Out of scope**
- Personalized investment recommendations or suitability determinations.
- Trade execution, subscription/redemption processing or custody.
- Regulatory certification, credit rating or comprehensive risk rating.
- Recreating the official classifier inside this Skill.
- Treating a volatility cluster as a complete risk assessment.

## First interaction and intake

Infer the operation from the user's request; do not ask them to select it when intent is clear. Resolve funds to SFC `codigo_negocio` where possible. For comparisons, resolve each candidate to a unique business code. Use the latest available cutoff by default and disclose it. Ask one focused question only when a material ambiguity blocks a reliable report.

## Sources and integration policy

### Source priority
1. SFC open-data dataset `qhpu-8ixx` via datos.gov.co or authorized MCP; preserve cutoff, source URL and retrieval timestamp.
2. Versioned classification output from the external FIC categorization project; treat as a dated snapshot.
3. Other authorized sources: user files, licensed vendors or corporate datasets.
4. Model interpretation may contextualize retrieved data but must not be represented as source facts.

Frontera Funds is the product brand, not a required data source. The private SaaS is not an execution dependency.

### Optional SFC MCP integration
When an authorized MCP connection is available, use its tools only after verifying the connection and permissions. Relevant operations may include dataset freshness, fund search, fund snapshot, peer comparison, historical NAV/returns, quantitative risk metrics, rankings, market share, flows and liquidity alerts. Never invent tool results or claim a request was performed if it was not.

### Optional categorization integration
The repository `jairoalonso1/categorizacion-fic-colombia` is an external provider. Its documented outputs are:
- `outputs/latest/fondos_clasificados.csv`
- `outputs/latest/resumen_clasificacion.json`
- `outputs/latest/clasificacion_fic.xlsx`

Read the snapshot metadata, cutoff, source and version. Join on `codigo_negocio`, not fund name. If unavailable, disclose that and continue without it. Follow the methodology version accompanying the actual snapshot. Volatility categories are descriptive groupings, not a comprehensive risk rating.

## Workflow and methodology

### 1. Resolve scope and entity
Resolve operation, funds, managers, business codes, participation classes, cutoff and requested output. Distinguish fund (`codigo_negocio`) from participation class (`tipo_participacion`). State whether metrics are class-specific, fund aggregates or representative-class measures.

### 2. Verify freshness and scope
Record source dataset, latest available date, selected cutoff, date range, retrieval time and tool identifiers when available. Do not silently substitute a different date for a requested historical cutoff.

### 3. Collect evidence
For a factsheet, collect identity, manager, subtype, category (if available), AUM, investors, unit value, EA returns, historical series, risk metrics, monthly returns and drawdown information when available. For comparisons, align cutoff, horizons, units, participation classes and definitions. Disclose missing/stale values.

### 4. Analyze with bounded judgment
Separate source facts, deterministic calculations and qualitative interpretation. Explain material performance differences with evidence. Higher return is not automatically better after risk, horizon, category, liquidity and comparability. Do not recalculate metrics unless series, definitions, sampling and assumptions are available. Distinguish SFC-reported EA returns from NAV-derived returns and model calculations.

### 5. Generate the report
Follow `references/report-profiles.md` for required analytical content and `references/html-rendering-contract.md` for HTML structure and presentation. HTML is primary; also return a concise structured summary and optional JSON. Generate other formats only when requested and supported.

### 6. Quality control
- Confirm resolved fund identifiers and applicable participation classes.
- Confirm cutoff and period are explicit and supported.
- Align compared periods and metric definitions.
- Preserve source units and distinguish reported EA return from NAV-derived return.
- Flag missing, stale, inconsistent or extreme observations.
- Check required report sections, title, language, brand mark, responsive CSS, print CSS, tables, charts, sources and disclaimers.
- Resolve all placeholders; confirm HTML opens and is non-empty.
- Reconcile visible report values with structured output.
- Disclose what was retrieved, calculated or inferred.

A passing HTML validator is not evidence of suitability or complete risk assessment.

## Output contract

Return a JSON object or equivalent host-native structure with:
- `service_id`: `fic-funds-intelligence`
- `service_version`, `operation`, `status`
- `report_profile`, `title`, `cutoff_date`, `period_start`, `period_end`
- `funds`: identifiers, names, manager, subtype, participation class and category when available
- `summary`, `metrics`, `category_snapshot`
- `artifacts`: name, media type, URI/path, SHA-256 when available, provenance
- `evidence`, `assumptions`, `warnings`, `errors`, `execution`, `next_actions`

Generated reports use provenance `frontera_skaas_generated`; user-provided artifacts use `user_supplied`. Follow the Factory's Universal Skill Invocation Contract 1.0.0; domain fields belong inside `outputs`.

## Runtime and security

The portable core works as instructions alone. Discover approved tools, MCP, Python, browser and artifact capabilities at invocation time. Do not embed secrets, assume private repository access, execute untrusted code/HTML, or transmit confidential data to unapproved services. Ask for approval when required for external connections, data transfer, package installation or external writes.

## Execution and completion

If no runtime is available, reason over supplied data but return `partial` or `blocked` when a required artifact cannot be generated or validated. Never fabricate a download link. The workflow orchestrator owns multi-step AX progress and approvals; this Skill owns the bounded FIC intelligence service and report quality gates.

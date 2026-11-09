---
name: fic-funds-intelligence
description: Produces standardized institutional analysis and HTML reports for Colombian collective investment funds (FICs) using a portable service contract. Supports single-fund factsheets, peer-group comparative reports, fund discovery and industry analysis. May use authorized SFC data, optional MCP tools and optional external categorization snapshots; Frontera Funds is a reference design, not a runtime dependency.
---

# FIC Funds Intelligence

**Created by Jairo Alonso González**

## Service promise

Deliver a consistent, evidence-led institutional report about a Colombian FIC, a peer group or a defined segment of the FIC industry. The primary artifact is a readable, portable HTML report using one of two report profiles:

1. **Fund factsheet** — a single fund's identity, performance, risk, history and relevant diagnostics.
2. **Comparative report** — a consistent side-by-side comparison of two or more funds, with common-period metrics and ranking context.

The skill is independent of Frontera Funds, any particular model, MCP server, browser, frontend, runtime or data vendor. Frontera's two report designs are reference patterns for the report profiles, not dependencies, required assets or authoritative data sources. The model may use any authorized data source that satisfies the source policy and output contract.

The Skill provides methodology, orchestration guidance, report specifications, lightweight validation and a portable output contract. It does not bundle or duplicate the classifier, MCP implementation, a large analytics library or a SaaS frontend.

## Scope

**Supported service operations**

- `fund_factsheet`: institutional report for one fund/business code, with a selected participation class or all classes where meaningful.
- `peer_comparison`: comparison of 2–8 funds, aligned to one cutoff and comparable horizons.
- `fund_discovery`: discover funds by name, manager, SFC business code, subtype or commercial category.
- `category_universe`: inspect the current classification taxonomy and category membership from an authorized, versioned classification snapshot.
- `industry_snapshot`: manager AUM, market shares, flows, rankings and liquidity indicators.
- `custom_analysis`: model-led analysis using any authorized dataset/tools, while retaining the same provenance and report contract.

**Out of scope**

- Personalized investment recommendations or suitability determinations.
- Trade execution, subscription/redemption processing or custody.
- Regulatory certification, credit rating or comprehensive risk rating.
- Reclassifying funds by recreating the official project classifier inside this Skill.
- Representing a volatility cluster as a complete risk assessment.

## First interaction and intake

Infer the operation from the user's request. Do not ask the user to select an operation when intent is clear.

For a single fund, identify it by SFC `codigo_negocio` where possible. If only a name is supplied, search first and resolve ambiguous matches by manager, subtype or other identifier. For a comparative report, resolve each candidate to a unique business code and use between 2 and 8 funds if the SFC peer-group operation is selected.

Use the latest available SFC cutoff by default and disclose the exact cutoff. Accept a user-specified historical cutoff when the source supports it. The default report profile is `factsheet` for one fund and `comparative` for two or more funds.

Ask one focused question only when a material ambiguity blocks a reliable report (for example, two funds with similar names or an unclear historical cutoff). Do not ask for details already present in context.

## Sources and integration policy

### Source priority

1. **Primary regulator dataset**: SFC open-data dataset `qhpu-8ixx` via datos.gov.co or an authorized MCP/connector. Preserve the source cutoff, source URL and retrieval timestamp.
2. **Versioned classification output**: the latest authorized output of the external FIC classification project. Treat it as a dated snapshot, never as a live query unless the source explicitly confirms that.
3. **Other authorized sources**: user files, licensed data vendors or corporate datasets. Identify the source and applicable rights.
4. **Model interpretation**: may explain or contextualize retrieved data, but must not be represented as source facts.

Do not treat Frontera's UI as a required or authoritative data source. Frontera is used as a design reference for its factsheet and comparative HTML reports.

### Optional SFC MCP integration

When an authorized MCP connection is available, the MCP server `mcp-sfc-fics-colombia` may supply current data through these tools:

| Tool | Use |
|---|---|
| `obtener_estado_dataset` | Verify dataset freshness, latest cutoff and data coverage before current analyses. |
| `listar_entidades_administradoras` | Manager universe, fund counts, investors and AUM. |
| `buscar_fondos_fic` | Resolve funds by name, manager, business code or subtype. |
| `radiografia_fondo` | Full fund snapshot, participation classes, AUM, unit value, investors, daily flows and EA returns. Requires `codigo_negocio`. |
| `ranking_rentabilidades_fics` | Top/bottom by daily, monthly, semiannual or annual EA return. |
| `cuota_mercado_aum_entidades` | Market share and AUM by manager, subtype or entity type. |
| `flujos_netos_captacion` | Contributions, redemptions, cancellations and net flows over a date range. Requires `fecha_inicio`. |
| `radar_corridas_y_alertas_liquidez` | Potential liquidity stress based on redemptions versus prior-close assets. |
| `serie_historica_nav_y_tasas` | Historical unit NAV, assets, investors, flows and reported returns. Requires `codigo_negocio` and `fecha_inicio`. |
| `metricas_riesgo_cuantitativo` | Quantitative metrics on unit NAV. Requires `codigo_negocio` and `fecha_inicio`. |
| `comparar_peer_group_fics` | Cross-fund snapshot for 2–8 business codes. |
| `ejecutar_soql_avanzado` | Bounded custom query over official columns. Use only when dedicated tools do not provide the required data. |

MCP availability is optional. The host must verify that the tool is actually connected and authorized before invoking it. Never invent tool results or claim an MCP request was performed if it was not.

Use `obtener_estado_dataset` before current industry or fund reports when the MCP is available. Use `buscar_fondos_fic` to resolve names, then `radiografia_fondo` or `comparar_peer_group_fics` for profile data. Use history and risk tools only when the requested report period and required observations exist. Use rankings and flows as supplementary context, not as substitutes for fund-level analysis.

### Optional categorization integration

The repository `jairoalonso1/categorizacion-fic-colombia` is an external, replaceable analytical provider. Its current project output contract is:

- `outputs/latest/fondos_clasificados.csv`
- `outputs/latest/resumen_clasificacion.json`
- `outputs/latest/clasificacion_fic.xlsx`

When a snapshot is available, read its own metadata, cutoff, source and version before using it. Join on `codigo_negocio`; preserve category dimension, category name, classification status and reason. Do not join on fund name alone. If no current snapshot is accessible, state that categorization was unavailable and continue without it.

The currently documented classification methodology uses a 365-calendar-day window and daily log returns on unit value; sample standard deviation annualized by √365; K-means with K=12, seed 42 and 50 initializations on log annualized volatility for eligible SFC subtypes 1 and 2 with strictly more than 180 valid returns; and nature-based classes for subtypes 3 (Inmobiliarios), 6 (Bursátiles) and 7 (Fondos de Capital Privado). Remaining records receive the residual status `Sin Clasificar`, which is not a risk category. Always follow the methodology version accompanying the actual snapshot; do not assume this description remains current if the project has changed.

Volatility categories are descriptive grouping labels, not a comprehensive risk rating, recommendation or guarantee. Disclose that volatility alone does not capture credit, liquidity, concentration, duration, leverage or operational risk.

## Workflow and methodology

### 1. Resolve scope and entity

Resolve the operation, funds, manager, business codes, participation type(s), cutoff and requested output. Retain the distinction between fund (`codigo_negocio`) and participation class (`tipo_participacion`). When multiple classes exist, make clear whether metrics are class-specific, fund-level aggregates or representative-class measures.

### 2. Verify source freshness and scope

Record source dataset, latest available date, selected cutoff, date range, data retrieval time and query/tool identifiers when available. For historical cutoff requests, verify that data is actually available for that date. Do not silently substitute the latest date for a requested historical date.

### 3. Collect evidence

For a factsheet, collect fund identity, manager, SFC subtype, category (if available), AUM, investors, unit value, EA returns, historical series, relevant risk metrics, monthly returns and drawdown information when available.

For comparisons, use a common cutoff and aligned metrics/horizons. Check that participation classes are comparable, currency and units match, periods overlap, and any missing or stale values are disclosed. Do not mix daily observed returns with annual EA returns without explaining the basis.

For industry analysis, obtain AUM/market share, flows, return rankings and liquidity flags only when relevant to the user's question.

### 4. Analyze with bounded model judgment

Separate source facts, deterministic calculations and qualitative interpretation. Explain material performance differences using evidence. Present upside and downside observations where relevant; do not make every analysis a ranking of winners. A fund's higher return is not automatically better after considering risk, horizon, category, liquidity and comparability.

If the available data supports it, consider absolute and annualized returns; realized volatility, maximum drawdown and recovery; Sharpe/Sortino and other provider metrics, with assumptions and risk-free rate; assets under management, investors and average ticket; daily, monthly, 180-day and 365-day EA returns reported by the regulator; monthly return distribution and worst drawdown windows; flows and liquidity warnings; and category and peer position.

Do not recalculate provider metrics unless source series, definitions, sampling and assumptions are available. If recalculated, distinguish them from SFC-reported return fields and MCP-computed measures.

### 5. Select the HTML report profile

Use one of the report profiles in `references/report-profiles.md`.

- `factsheet`: one fund, institutional factsheet.
- `comparative`: at least two funds, side-by-side comparison.

Both profiles must be readable on desktop and mobile, printable, in Spanish (Colombia), and portable as a single HTML file wherever practical. Embed styles and chart assets when feasible; avoid requiring a proprietary frontend or client-side runtime. External resources must be declared. Include report title, date generated, cutoff, period, fund identifiers, data provenance, methodology and limitations.

The HTML is the primary artifact. Also return a concise structured summary and optional machine-readable JSON. Generate XLSX or other formats only when requested or materially useful and the runtime supports them.

### 6. Deliverable provenance: Frontera reference vs original source

Frontera Funds has two relevant browser-generated HTML report types:
- Factsheet: the `factsheet` report type, with selected KPIs, cumulative return, drawdown, period/annualized returns, risk-return universe, monthly return heatmaps and worst drawdowns as configured.
- Comparative table report: the `comparative` report type, with selected comparative metrics and table columns.

These are reference designs. The original Frontera HTML is exported from a browser preview; the reviewed source code does not expose a backend HTML-rendering API. Therefore:

- If a user/host supplies an actual Frontera-exported HTML file, preserve it as an **original source artifact**, validate it and link it separately.
- If an authorized Frontera session or browser tool can export the actual report, use that exact mechanism; record which options, funds and date range were selected.
- If neither is available, create a skill-produced HTML that follows the relevant report profile using authorized data. Label it **Skill-generated report — Frontera-inspired profile**, not as a Frontera original or Frontera export.
- Never claim to have downloaded an original Frontera report without verifying the file.

This separation protects the main product promise and avoids false claims about integration.

### 7. Quality control and acceptance

Before completing:
- Ensure every fund has a resolved business code and, where applicable, participation class.
- Confirm the cutoff and date range are explicit and supported by the data.
- Confirm all compared funds use aligned periods and definitions.
- Preserve source field names/units and distinguish reported EA return from return calculated from NAV.
- Ensure category labels carry their dimension and snapshot date.
- Flag missing, stale, inconsistent or extreme observations without silently deleting them.
- Check HTML structure, title, language, links, charts, tables and local asset references.
- Verify the HTML opens as a file and that the artifact is non-empty.
- Confirm that structured outputs reconcile with the visible report.
- Disclose what the model inferred and what was calculated or retrieved.

A passing HTML validator is not evidence of investment suitability or complete risk assessment.

## Output contract

Return the following structure as a JSON object or equivalent host-native structured result:

- `service_id`: `fic-funds-intelligence`
- `service_version`
- `operation`
- `status`: succeeded, partial, needs_input, blocked, failed or cancelled
- `report_profile`: factsheet, comparative or null
- `title`
- `cutoff_date`
- `period_start`, `period_end`
- `funds`: identifiers, names, manager, subtype, participation class and category when available
- `summary`: key findings, comparisons and interpretation
- `metrics`: values, units, period, definition and source for each metric
- `category_snapshot`: source, version, cutoff, category dimension and status where available
- `artifacts`: name, media type, URI/path, SHA-256 when available, and provenance label (`frontera_original` or `skill_generated`)
- `evidence`: source, locator, access time and claim/output supported
- `assumptions`
- `warnings`
- `errors`
- `execution`: whether code/network/tools were actually used, runtime and tool references
- `next_actions`

The service must follow the Factory's Universal Skill Invocation Contract 1.0.0. Keep its request/response envelope unchanged; domain-specific fields above belong inside `outputs`.

## Runtime and security

The Skill's portable core must be usable as instructions alone. A compatible host may supply tools, MCP, browser automation, a Python runtime, HTML files or a managed artifact store. Discover those capabilities at invocation time.

Do not embed tokens, credentials or secrets. Do not assume private repository access. Do not execute untrusted code or HTML from source artifacts. Do not transmit confidential fund, customer or account data to unapproved services. Ask for approval when host policy requires external connection, data transfer, package installation or external writes.

## Execution and completion

A Skill may reason over user-supplied data even when no runtime is available, but it must return `partial` or `blocked` when a required report artifact cannot be generated or validated. Do not fabricate a download link.

The workflow orchestrator owns the multi-step AX experience, user-visible progress, approval capture and final workflow closure. This Skill owns the bounded FIC intelligence service and its report quality gates.

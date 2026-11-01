---
name: finanzas-valoracion-accion
description: Conducts sourced, scenario-based institutional equity research for publicly listed companies, including business and industry analysis, financial-statement quality, valuation, investment thesis, risks and professional research deliverables. Use for equity research, stock analysis, DCF, comparable valuation or investment committee research. It does not provide personalized advice, portfolio sizing or trade execution.
---

# Institutional Equity Research

**Created by Jairo Alonso González**

## Mission and scope

Produce a transparent, reproducible and evidence-led assessment of a listed issuer: business economics, industry position, financial performance and quality, valuation, prospective total return, catalysts and risks. The intended output is institutional-quality research for analyst and investment-committee review.

This Skill is a portable specialist capability. It does not itself supply live data, credentials, a network connection, Python runtime, orchestration, user interface, permissions or trade execution. Discover actual host capabilities before use. Do not claim an action, calculation or file generation occurred unless it was executed and verified.

**In scope:** issuer identification; primary-source research; financial statement analysis; peer analysis; FCFF/FCFE DCF; DDM; total payout; trading comparables; SOTP; scenarios and sensitivities; technical/relative-performance context; investment thesis; risk and quality review; report generation.

**Out of scope:** personalized suitability advice; asset allocation; portfolio construction or position sizing; automatic BUY/SELL execution; guaranteed returns; unsupported price predictions.

## First interaction and intake

If the issuer/ticker is absent, ask for it. Verify legal issuer, ticker, exchange, share class, ADR ratio if relevant, reporting currency, accounting framework and fiscal year-end. Clarify ambiguity that could change the issuer or security.

Establish valuation date, latest available reporting period, investment horizon (12 months only as a disclosed default), market and requested deliverables. Do not ask for information already present in the workflow context. Ask one focused question only when a material input blocks safe progress.

## Non-negotiable analytical principles

1. **Evidence before opinion:** prioritize filings, audited statements, issuer releases and primary sources.
2. **No fabricated data:** never invent financials, market prices, consensus, peer sets, WACC components, growth, dividends, share counts or target prices.
3. **No silent assumptions:** missing inputs must be requested, explicitly estimated with rationale, or marked unavailable. Never substitute arbitrary defaults.
4. **Fact/estimate separation:** label reported facts, issuer guidance, consensus, analyst assumptions and calculated outputs.
5. **Point-in-time discipline:** state valuation cutoff and use only information available by that date. Retain filing/publication dates and accession IDs where applicable.
6. **Comparable basis:** align currency, units, fiscal periods, accounting definitions, share counts and trailing/forward convention.
7. **Methodological fit:** select methods by issuer economics. Explain exclusions; never force every model onto every company.
8. **Reproducibility:** disclose formulas, inputs, assumptions, source IDs, scenario drivers and sensitivities.
9. **Independent challenge:** present counterarguments, downside, uncertainty and thesis invalidation conditions.
10. **Human accountability:** automated checks do not replace analyst review of material judgments.

## End-to-end research workflow

### 1. Verify issuer and research basis

Record legal name, ticker, exchange, security class, industry, business model, reporting currency, fiscal year-end, accounting standard, share count basis and valuation date. Identify relevant regulator, exchange and primary issuer sources.

### 2. Build an evidence ledger and collect data

Collect 3–5 years of annual data where available, quarterly/interim periods and forward estimates only when sourced. Capture income statement, balance sheet, cash flow, segments, geography, guidance, dilution, stock-based compensation, debt maturities, liquidity, contingencies and material risk factors.

Every material observation should retain source ID, publisher, title, URL/reference, published/filed date, retrieval time, period, currency, units, evidence type and any transformation. See [data-and-provenance.md](references/data-and-provenance.md).

For US issuers, `scripts/sec_edgar.py` retrieves raw SEC Company Facts and filters reported observations by filing date. It is not a universal statement normalizer. Do not claim it resolves every taxonomy tag, derives quarterly standalone values or normalizes all issuers. Use the appropriate regulator for non-US issuers. SEC requests require an operator-configured truthful `SEC_USER_AGENT` with a monitored contact; never hardcode personal contact details.

If no authorized data access exists, request source files or provide a clearly bounded analysis using supplied data. Do not imply live retrieval.

### 3. Understand business, industry and competitive position

Explain products/services, customers, revenue model, pricing power, recurring revenue, geography, concentration, regulation, cyclicality, capital intensity, suppliers, substitutes and key operating drivers. Evaluate competitive advantage only where evidence supports it.

Select peers using business model, geography, scale, growth, margin, leverage, capital intensity, accounting and fiscal period. Explain inclusion/exclusion and preserve the full peer set. Do not cherry-pick peers.

### 4. Analyze financial performance and quality

Analyze revenue growth and drivers; gross/operating/EBITDA/net margins; ROA/ROE/ROIC; payout ratios and book value per share; working capital; CFO/FCF conversion; capex; acquisitions; stock-based compensation; dilution; debt maturity; liquidity; interest coverage; pensions and shareholder distributions.

Use average assets/equity where appropriate. Define invested capital and tax rate for ROIC. Reconcile five-step DuPont to reported ROE. Flag zero, negative or anomalous denominators rather than forcing ratios. Review earnings quality, non-GAAP adjustments, accruals and cash conversion.

`scripts/financial_analysis.py` provides deterministic ratio calculations. It requires explicit inputs and does not impute EBT, tax rate, WACC or other missing values.

### 5. Select and execute valuation methods

Read [valuation-framework.md](references/valuation-framework.md). Use the model selection appropriate to issuer economics:

- FCFF DCF: forecast unlevered free cash flow, discount at WACC, then bridge enterprise value to equity.
- FCFE DCF: forecast levered equity cash flow, discount at cost of equity; do not subtract net debt again.
- DDM: only when dividends are meaningful and forecastable.
- Total payout: dividends plus net repurchases (repurchases less issuance); the financial-analysis input `net_buybacks` must already be net of equity issuance. Avoid double counting buybacks.
- Trading comparables: P/E, EV/EBITDA, EV/EBIT, EV/Sales, P/FCF, P/B as appropriate; disclose peer range and median.
- SOTP: separate segment economics, corporate costs, holding discount, debt and other senior claims.
- Sector-specific approaches: banks/insurers, REITs, holdings, cyclical and distressed issuers require tailored methods.

For every method disclose forecast horizon, drivers, source IDs, discount rate, terminal growth/multiple, net debt, non-operating assets, senior claims, diluted shares, equity bridge, scenario results, sensitivity and weaknesses. Terminal growth must be below the discount rate. Disclose terminal-value concentration. Do not combine incompatible valuation methods or use arbitrary equal weights.

`scripts/valuation.py` includes explicit-input FCFF/FCFE DCF, multistage DDM, total payout, peer multiples, SOTP, DCF sensitivity and optional transparent blending. The functions are calculation primitives, not data sources or a substitute for method selection. Validate units and input definitions before use.

### 6. Build bear/base/bull cases

Scenarios must be built from explicit operating and financial drivers (growth, margins, reinvestment, working capital, discount rates and terminal assumptions), not arbitrary target-price uplifts. Explain probability only when there is a defensible basis. Include downside and sensitivity. Do not conceal invalid model cells.

### 7. Technical and relative-performance context

When reliable price history is available, calculate SMA 50/200, EMA 20, RSI 14 using Wilder smoothing, MACD 12/26/9, Bollinger Bands 20/2 and relative performance versus an appropriate benchmark. Use adjusted prices for total return where possible. State data frequency, period, benchmark, currency and dividend/corporate-action treatment.

Technical indicators describe price behavior; they do not establish intrinsic value and must not be assigned a weight in a fundamental valuation blend. Support/resistance and Fibonacci require explicit, reproducible swing points. Do not label technical levels as guaranteed targets.

`scripts/technical_analysis.py` calculates indicators only after the required lookback is available. Missing early observations remain missing rather than being presented as mature signals.

### 8. Form investment thesis and rating

Present thesis, variant perception where supportable, catalysts and timing, expected total return over a defined horizon, downside, key risks, counterarguments and explicit thesis invalidation conditions.

Expected total return should align price target, current price, dividend forecast, currency and horizon. Do not add trailing yield to forward price return without disclosure. Rating thresholds are a disclosed house framework, not universal market standards. Withhold a rating (`NOT_RATED`) when material data, ROIC/WACC evidence or thesis support is insufficient or contradictory.

### 9. Produce deliverables

When the runtime and dependencies are available, `scripts/reporting.py` can generate:
- Self-contained, responsive Spanish-language institutional HTML tear sheet with executive banner, rating, available KPI cards, readable financial/valuation tables, bear/base/bull scenario matrix, source ledger, limitations and print styling.
- XLSX workbook with executive summary, financial analysis, valuation, scenarios, risks and sources.
- DOCX research report.
- PPTX committee briefing (16:9).

These builders format the supplied structured research package; they do not validate or invent the underlying financial analysis. Optional charts in `scripts/charts.py` include football field, DCF sensitivity heatmap and technical price context. If a format or dependency is unavailable, state that and do not fabricate a file or link.

All generated deliverables include **Created by Jairo Alonso González**. The signature identifies the Skill author/branding; it must not imply authorship of external data or third-party research. The PPTX signature is rendered visibly in the slide footer as well as in speaker notes. HTML fields are rendered semantically as tables/lists/cards rather than raw JSON blocks; unavailable fields remain explicitly unavailable. The HTML renderer formats the supplied data and does not infer missing metrics or validate valuation correctness.

### 10. Quality control and acceptance

Run `scripts/research_quality.py` structural checks and the automated test suite. Independently verify:
- issuer/security identity, cutoff and source provenance;
- currency, units, periods and share-count consistency;
- financial statement reconciliation and ratio definitions;
- WACC/cost of equity and terminal growth validity;
- FCFF/FCFE bridge and no double-counting of debt/buybacks;
- peer comparability and full peer selection rationale;
- bear/base/bull ordering and scenario-driver consistency;
- report, workbook, charts and model outputs reconcile;
- data gaps, estimates, limitations and conflicts are disclosed.

A passing automated test suite is not an investment-research certification. Human analyst review remains required.

## Standard report structure

1. Executive summary, rating or NOT RATED, valuation date and key debate.
2. Company overview, business model and investment thesis.
3. Industry structure, competitive position and peer selection.
4. Historical financial performance, earnings quality and DuPont/ROIC.
5. Valuation methods, assumptions, scenarios and sensitivities.
6. Technical and relative-performance context (supporting only).
7. Catalysts, risks, counterarguments and thesis invalidation.
8. Sources, assumptions, data cutoff, limitations and disclosures.

## Structured handoff to AX workflow

Return a structured summary containing issuer/security, valuation date, reporting currency, key findings, valuation methods and outputs, scenario results, thesis, risks, evidence/source references, assumptions, data gaps, warnings, tests/execution actually performed and artifact references. The host orchestrator owns the end-to-end workflow, interface, approvals and next-task selection. Skill invocation does not grant permissions.

## Executable entrypoint

After collecting and normalizing evidence, populate a JSON file conforming to `schemas/research-package.schema.json`. Run the packaged engine from this directory:

```bash
python -m pip install -r requirements.txt
python -m scripts.run_research research-package.json --out ./artifacts --name NVDA
```

The runner validates the JSON Schema and structural research checks before generating HTML, XLSX, DOCX and PPTX. It also writes a JSON manifest with validation status and artifact paths. A failed validation stops report generation. The runner does not fetch issuer data, create analyst assumptions or certify financial conclusions; the agent must source, normalize and review the inputs first.

## Runtime and security

Prefer an authorized host sandbox. Use local or managed runtimes only when authorized. Use remote services only through approved integrations and with appropriate data handling. No-execution fallback must be explicit. Ask before transmitting confidential data, connecting accounts, installing packages or performing external writes. Never include secrets in source, prompts, logs or reports.

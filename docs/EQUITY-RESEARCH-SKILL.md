# Equity Research Skill — Implementation and Acceptance Plan

## Product definition

`finanzas-valoracion-accion` is an institutional equity-research specialist capability. It covers issuer and industry research, financial statement quality, applicable valuation, scenarios, investment thesis, risk analysis and report formatting. It does not provide personalized advice, portfolio sizing or execution.

## Implementation status (v0.2.0)

| Capability | Current implementation | Validation boundary |
|---|---|---|
| Financial ratios / DuPont / ROIC | `financial_analysis.py` | Explicit normalized inputs; missing values are not imputed |
| FCFF / FCFE DCF | `valuation.py` | Forecast cash flows supplied explicitly |
| Multistage DDM / total payout | `valuation.py` | Explicit dividends/payouts and discount-rate assumptions |
| Trading comparables | `valuation.py` | Requires at least three positive peer multiples and a comparable subject metric |
| SOTP | `valuation.py` | Segment EVs and holding discount supplied explicitly |
| DCF sensitivity | `valuation.py` | Invalid discount/growth combinations return null cells |
| Technical indicators | `technical_analysis.py` | SMA lookback and Wilder RSI; price data must be supplied |
| SEC Company Facts | `sec_edgar.py` | Raw facts + filing-date filter; not a universal statement normalizer |
| Research QA | `research_quality.py` | Structural checks only; no semantic audit or investment certification |
| HTML / XLSX / DOCX / PPTX | `reporting.py` | Standardized multi-section output from one structured package; does not validate its financial truth |
| Executable report runner | `run_research.py` | Validates JSON Schema + structural QA, generates four formats and a verification manifest; no report if validation fails |
| Optional charts | `charts.py` | matplotlib required; functions require prepared inputs |
| Business/industry research | Methodology in `SKILL.md` and references | Evidence gathering depends on authorized host tools/provider |

## Acceptance gates for a production release

1. Unit tests pass for calculations, edge cases, chart generation and deliverable generation; CLI smoke test verifies all four files and the manifest.
2. Integration test with a complete sourced issuer dataset and one non-US issuer.
3. Point-in-time test: later filings/restatements are excluded from an earlier cutoff.
4. Reconciliation test against an independently checked model for FCFF, FCFE, DDM, comparables and SOTP.
5. Sector suitability tests for at least an industrial company, bank/insurer, REIT and holding company.
6. Workbook/report/chart reconciliation and visible source/assumption references.
7. Dependency, security and package portability review.
8. Manual analyst review of the final research package and disclosures.
9. Runtime tests on at least two compatible host environments before claiming cross-platform validation.

The current suite has 29 passing tests in Python 3.13.18, including a CLI run that creates and verifies HTML, XLSX, DOCX, PPTX and a JSON manifest from a synthetic example. This is partial package-level evidence, not a financial-domain evaluation or a cross-host compatibility claim. A green unit-test suite does not pass the remaining acceptance gates by itself. v0.2.0 is an implementation candidate, not a production certification.

## Factory release governance

This package is a candidate release. Its manifest declares data dependencies, evaluation status and host compatibility separately. The local test suite and CLI smoke test are evidence of package behavior only; they do not certify financial-domain accuracy or a managed service. See the Factory [release governance](SKILL-QUALITY-AND-RELEASES.md) and [Skills as a Service model](SKILL-AS-A-SERVICE.md).


## HTML report presentation — candidate 0.2.1

The HTML exporter now renders a responsive institutional tear sheet rather than serializing each package section as a JSON code block. The layout includes an executive header, rating panel, data-driven KPI cards, readable nested tables and lists, a Bear/Base/Bull scenario matrix when scenario inputs exist, source links, mobile breakpoints, print styles and explicit limitations. Missing metrics are omitted from KPI cards and shown as unavailable in detail sections; the renderer does not estimate missing values.

The PPTX author signature is visible in slide footers and remains in speaker notes. Regression tests cover semantic HTML structure, escaping, KPI percentage formatting, scenario presentation and visible PPTX branding. This is a presentation-quality improvement, not a financial-model validation or production certification.

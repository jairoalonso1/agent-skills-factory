# Data and Provenance Contract

## Required data record

Each material observation should be represented with: `field`, `value`, `unit`, `currency`, `period_start`, `period_end`, `period_type` (instant/duration), `as_of_date`, `published_or_filed_at`, `retrieved_at`, `source_id`, `source_url`, `evidence_type`, `reported_or_adjusted`, `transformation`, and `confidence_or_limitation`.

## Evidence labels

- `reported`: regulator-filed or issuer-reported historical fact.
- `company_guidance`: issuer forecast or target.
- `consensus`: third-party analyst estimate; include provider and timestamp.
- `analyst_assumption`: explicit modeling assumption.
- `calculated`: reproducible calculation from identified inputs.
- `market_data`: price, volume, shares or corporate-action observation from a named provider.

## Point-in-time rules

For historical backtests or as-of research, only use information public by the selected cutoff. SEC `filed` date is a practical availability proxy, not an intraday timestamp. Retain accession number and filing date. Do not use a later amendment, restatement, consensus snapshot or corporate action before its actual publication/availability date.

## SEC Company Facts limitations

The included SEC helper retrieves raw Company Facts and can filter observations by filing date. It does not universally normalize GAAP/non-GAAP statements, infer quarterly standalone flows from year-to-date facts, resolve every issuer-specific XBRL tag, or guarantee comparability across taxonomies. Mapping and period derivation must be separately reviewed and tested.

## Data-provider policy

Use only authorized APIs/connectors or user-supplied datasets. Respect licenses, rate limits and terms. Do not scrape authenticated or restricted sources without permission. Never put API keys, passwords, private email addresses or access tokens in source files, prompts, artifacts or logs.


## Structured observation ledger (0.3.0)

The package may include `data_observations`, an observation-level ledger linking material inputs to source records or calculation inputs. Each record identifies `observation_id`, `field`, `value`, `unit`, and `evidence_type`. Reported, guidance, consensus and market observations link to `source_ids`; calculated observations identify `input_observation_ids` and a reproducible `transformation`; analyst assumptions include a `rationale`. The quality checker validates unique IDs and resolves source/input references. The ledger remains optional for backward compatibility, but its absence is reported as a warning.

## ROIC methodology disclosure

The engine calculates ROIC as NOPAT divided by supplied `invested_capital`. This is a calculation convention, not a universal accounting definition. Analysts should disclose denominator perimeter, cash treatment, debt/lease treatment where relevant, period basis and tax-rate basis in `roic_definition`. No single invested-capital formula is forced because conventions differ by provider, company and industry. ROIC without a methodology definition triggers a warning. For banks and other financial institutions, ROIC may be less decision-useful; use sector-appropriate return and capital measures.

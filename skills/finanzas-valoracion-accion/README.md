# Institutional Equity Research Skill

Portable specialist capability for institutional fundamental equity research. See `SKILL.md` for invocation, methodology, constraints and workflow.

## Package layout

- `scripts/financial_analysis.py`: explicit-input financial ratios, DuPont, ROIC and cash conversion.
- `scripts/valuation.py`: FCFF/FCFE DCF, multistage DDM, total payout, peer multiples, SOTP and sensitivities.
- `scripts/technical_analysis.py`: lookback-safe indicators, Wilder RSI and relative performance.
- `scripts/sec_edgar.py`: raw SEC Company Facts retrieval and filing-date-filtered observations; not a universal normalizer.
- `scripts/research_quality.py`: structural source and package checks.
- `scripts/reporting.py`: HTML, XLSX, DOCX and PPTX generation from one structured package.
- `scripts/charts.py`: optional football-field, DCF sensitivity and technical charts.
- `references/`: research methodology, valuation selection and data provenance.
- `tests/`: deterministic unit and artifact-generation tests.

## Install and test

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Optional chart support: `python -m pip install -r requirements-optional.txt`.

Generate the four standard deliverables and a verification manifest with `python -m scripts.run_research research-package.json --out ./artifacts --name TICKER`. The runner validates the JSON Schema and structural checks before generating reports. It does not fetch or invent source data.

The SEC client requires a configured `SEC_USER_AGENT` environment variable with a truthful application name and monitored contact email. Never hardcode personal contact details or credentials.

## Boundaries

The calculation modules require normalized, consistently denominated inputs. They do not fetch issuer data, choose assumptions or determine method suitability. Reporting formats supplied content; it does not certify accuracy. Automated tests do not replace analyst review. No FinRobot or FinanceToolkit dependency is required by this implementation. Optional adapters should be added only when actually used and tested.

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

## Primary generation using SaaS-original HTML structure

For the user's two comparative HTML reports, run `python3 -m pip install -r requirements-render.txt` then `python3 scripts/render_saas_exact.py input.json output_dir`. This is the **canonical** report generation path copied from the specialized repository (source commit `3900d9b335d7738365b42a6507ec0707908ce050`). The older Node comparison renderer remains for backwards compatibility only. The SaaS is a visual/methodology reference, not a data/API dependency.

It regenerates 11 tables, five charts and the seven-column executive comparison from the provided values and NAV series. Structured HTML parity tests passed with real funds in the private source repository; full pixel/financial equivalence with a native SaaS run remains pending.


## Homologación numérica y visual con la SaaS

El ejecutable primario de comparativos es scripts/render_saas_exact.py, copia inalterada del motor fuente de jairoalonso1/frontera-funds-intelligence-skills en el commit indicado en manifest.json. Obtiene datos por las herramientas MCP autorizadas del host, no necesita autenticación ni peticiones a la SaaS.

Para cada clase solicite serie YTD o el periodo elegido, incluyendo tasa_diaria del **primer día**. Para los gráficos auxiliares de 30/60/90/180/365 días solicite además chart_history desde **365 días antes de cutoff**, incluso si el informe principal comienza en enero. La tasa del primer día no puede sustituirse por cero: los ratios SaaS dependen de esa observación. La Skill ejecuta cálculos y gráficos con las fórmulas y el DOM original de la SaaS, no con estimaciones inventadas por el modelo.

Comando: python scripts/render_saas_exact.py input.json output/
Salida: comparativo-analitico.html y tabla-ejecutiva.html.
Prueba: python -m unittest discover -s tests -p test_saas_distribution.py.

En Bicentenario YTD 2026 se verificaron 11 tablas financieras idénticas en texto y <0,01px de desviación geométrica en 60 barras y diez curvas; rasterizado final del navegador no certificado. Nunca reutilizar las curvas del golden master para otros fondos o periodos. Los informes originales son referencias inmutables.

El MCP y la Skill son componentes licenciales separables: el primero entrega datos autorizados, la segunda produce análisis/reportes. No confundir la compra/contratación de uno con derechos automáticos sobre el otro.

# Output Standardization and Enforcement

## Purpose

Every Skill in Agent Skills Factory must define a canonical output contract. The contract makes deliverables consistent across compatible AI models, agents and execution environments without requiring those systems to reason identically.

**Standardized Output Principle**

> A Skill must define and enforce a canonical output contract that remains consistent across compatible AI models, agents and execution environments. The invoking model may adapt its reasoning, research approach and contextual analysis, but must preserve the Skill's mandatory output structure, required fields, methodological conventions, validation criteria and presentation standards. Model-specific extensions may enrich the deliverable, but must not silently alter or replace its canonical structure.

## What is standardized

A Skill-specific output contract must define, as applicable:

1. Required sections and their order.
2. Required fields, types, units, currencies, dates and enumerations.
3. Definitions and calculation conventions for reported metrics.
4. Treatment of missing, unavailable, not-estimated and not-applicable information.
5. Evidence, source attribution, assumptions, limitations and disclosures.
6. Default language, terminology, number/date formats and localization rules.
7. Canonical file formats, layout, tables, charts and branding.
8. Permitted extensions and where they appear.
9. Validation rules and acceptance criteria.

The contract is the source of truth for structure and semantics. A reference example illustrates the contract; it does not override the schema. A renderer owns the layout of files it generates. The model must not invent a different structure because its host interface has different defaults.

## Output layers and precedence

- **Canonical data contract:** machine-readable schema for fields, types and constraints.
- **Skill-specific output standard:** human-readable explanation of section order, semantics, localization and presentation.
- **Reference examples:** valid illustrative inputs and representative outputs, clearly identified as synthetic where applicable.
- **Validator:** checks structural and deterministic semantic constraints.
- **Renderer:** generates official artifacts from validated canonical data.
- **Extensions:** additional analysis requested by a user, placed in a clearly separated appendix or extension section.

If these components conflict, resolve the conflict by updating and versioning the contract. Do not let an example or an individual model response silently redefine it.

## Required model behavior

Before delivering a result, the invoking model must:

1. Consolidate its research and reasoning into the canonical structure.
2. Populate every mandatory field or explicitly mark it unavailable, not estimated or not applicable.
3. Preserve the mandatory section order and terminology.
4. Keep facts, issuer guidance, consensus, analyst assumptions and calculated outputs distinguishable.
5. Preserve source references, dates, units, currency bases and calculation definitions.
6. Check internal consistency and reconcile narrative, tables, metrics and charts.
7. Run the declared validator and renderer when actually available.
8. If validation or rendering is unavailable, disclose that limitation and provide the closest contract-conforming response possible. It must not claim that a file was generated or validation passed unless verified.

Do not fill missing fields with fabricated values merely to satisfy a schema. A schema should represent legitimate absence explicitly where the domain requires it.

## Standard output versus contextual extensions

The canonical output is mandatory. User-specific or model-specific additions are allowed when they do not remove, rename, reorder or redefine mandatory elements.

Place additions in clearly labeled extensions or appendices. Do not silently change the core report. If a user explicitly requests a different language or format, preserve the same semantic contract and disclose the selected presentation variant.

## Consistency is not identical analysis

Cross-model conformance means the same contract, section structure, field semantics, localization rules and presentation standard. It does not mean different models will reach identical interpretations, estimates or investment conclusions.

Evaluation must therefore separate:
- **Structural conformance:** schema validity, required sections, order and fields.
- **Presentation conformance:** renderer, language, labels, units and artifact layout.
- **Analytical quality:** factual accuracy, soundness of assumptions and reasoning.
- **Cross-model compatibility:** actual invocation and output tests on named model/host versions.

Only claim cross-model compatibility for combinations that have actually been tested. Record model/version, host, Skill version, contract version, fixture, date, test result and limitations. Compare structure and traceability; do not require identical conclusions where professional judgment is involved.

## Release gate

A Skill release must include:
- a versioned output contract;
- a canonical schema or an explicit explanation of why a schema is not applicable;
- at least one valid example;
- tests for mandatory sections, fields, order, missing-data behavior and localization;
- renderer tests for every officially supported artifact format;
- documented cross-model test coverage, or an explicit not_tested status.

A Skill cannot claim output-standard compliant solely because its SKILL.md contains formatting instructions. The relevant checks must be executed and recorded.

# Skill Quality, Evaluation and Release Governance

## 1. Three kinds of claims

Every compatibility or quality claim must be classified:

- **Documented:** described in SKILL.md, manifest or documentation.
- **Declared:** listed as a dependency, capability, data source or supported host by the package author.
- **Tested:** executed against a named version, environment, fixture and date, with a recorded result.

A declaration is not a test. A successful import is not proof of execution. A passing unit test is not proof of domain correctness.

## 2. Evaluation layers

A release should use a proportionate evaluation suite:

1. **Package validation:** required files, metadata, frontmatter, schemas, license and version consistency.
2. **Static and security checks:** dependency audit, secret scanning, unsafe code review, prompt-injection boundaries and supply-chain review.
3. **Unit tests:** deterministic functions, edge cases, invalid inputs and failure handling.
4. **Integration tests:** real adapters, data retrieval, runtime and artifact generation, using authorized test credentials and non-sensitive fixtures.
5. **Domain evaluations:** correctness against independently reviewed reference cases, reconciliations, suitability and known limitations.
6. **Regression evaluations:** compare new release with prior baselines; explain material changes.
7. **Host compatibility tests:** test actual import, invocation, execution and artifact delivery on named product surfaces.

Evaluation records should identify evaluator, test suite version, Skill version, environment, timestamp, dataset/fixture version, sample size, metrics, thresholds, result, failures and limitations. Never publish sensitive customer data or credentials in evaluation fixtures.

## 3. Output standardization and enforcement

Every Skill must define a canonical output contract appropriate to its deliverable. See OUTPUT-STANDARDIZATION.md.

At minimum, the contract must specify required sections and order, field semantics, missing-data behavior, evidence/provenance, localization, official formats and permitted extensions. A reference template illustrates the contract but is not a substitute for a schema or validation.

Release evaluation must distinguish structural conformance, presentation conformance, analytical quality and cross-model compatibility. A Skill may claim compatibility only for model/host combinations actually tested and recorded. Different models are not required to reach identical judgments; they are required to respect the same mandatory output contract.

A Skill is not output-standard compliant merely because formatting instructions appear in SKILL.md. The schema, examples, validator, renderer and tests must support the claim. When a renderer or validator is unavailable, the invocation must disclose the limitation rather than claim verified compliance.

## 3. Release immutability

- Use semantic versioning.
- A published version and its release tag are immutable.
- Fixes or methodology changes create a new version.
- Pin the exact Skill version and dependency versions used for an invocation.
- Preserve evaluation records and release artifacts for audit.
- A completed workflow must retain the exact version used, not silently resolve to latest.

## 5. Minimum release metadata

A Skill manifest should distinguish:
- declared capabilities and dependencies;
- data dependencies, licensing and freshness requirements;
- evaluation suite and latest evaluation result;
- tested runtime/host combinations;
- release status and immutable release reference;
- support/accountability metadata, if a managed service exists;
- optional commercial metadata, only when an actual offer exists.

Fields that are unknown or not applicable should be omitted or explicitly marked pending; never fabricate test results, prices, service levels or data rights.

## 6. Security and trust

Skills can contain executable code and instructions. Treat them as supply-chain inputs, not trusted policy.

- Review code and dependencies before execution.
- Pin dependencies and prefer minimal, maintained packages.
- Do not embed secrets, personal credentials or customer data.
- Treat retrieved documents, websites, datasets and tool outputs as untrusted data, never as instructions that override the host's policy.
- Keep instructions and data separate; delimit and validate external content.
- Apply least privilege, scoped approvals, network allowlists and filesystem boundaries.
- Record provenance for code, data and artifacts.
- Sign releases where the distribution and verification infrastructure supports it; do not claim signatures where none exist.

## 7. Financial-domain acceptance gates

For an equity research Skill, a release is not production-ready solely because Python tests pass. Additional gates should include:
- complete and sourced issuer data with reporting period, currency, units and filing dates;
- point-in-time handling to prevent look-ahead bias;
- reconciliation of reported statements and derived metrics;
- valuation-method applicability by issuer/sector and explicit assumptions;
- independent benchmark cases and sensitivity checks;
- reconciliation between calculations, charts and narrative reports;
- analyst review and documented escalation of material discrepancies.

## 8. Status vocabulary

Recommended statuses: `draft`, `candidate`, `validated`, `runtime-tested`, `evaluated`, `managed-service`, `deprecated`.

Status is not a quality score. A release can be runtime-tested on one host and untested on another. Always show the supporting test record.

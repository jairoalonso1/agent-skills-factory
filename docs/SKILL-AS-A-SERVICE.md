# Skills as a Service: value, operating model and accountability

## Thesis

A Skill package is a portable capability description: specialist instructions, methodology, references and optional executable resources. The package alone is easy to copy and is not, by itself, a defensible managed service or a substitute for SaaS.

A commercial Skill service becomes valuable when it is backed by one or more durable capabilities that are difficult to reproduce responsibly:

- **Authorized data access:** proprietary, licensed or curated datasets with documented rights, coverage, freshness and lineage.
- **Managed execution:** controlled runtimes, dependency pinning, observability, isolation, artifact retention and predictable delivery.
- **Demonstrated quality:** public or customer-accessible evaluations, reproducible test fixtures, benchmark results and regression history.
- **Accountability:** named service owner, support process, incident handling, limitations, escalation and contractual responsibility.
- **Workflow integration:** reliable orchestration, approvals, state, audit trail and integration with the customer's systems.

The value proposition must identify which of these are actually supplied. Do not market a text-only Skill as if it includes licensed data, managed execution or a service-level commitment.

## Relationship to SaaS

Skills as a Service is complementary to SaaS, not a blanket replacement. Existing SaaS products and APIs continue to own authoritative data, business state, identity, access control, compliance and transactional operations. Skills provide an agent-facing capability layer that can coordinate work across those systems.

An agent becoming a common user of software does not remove the need for the underlying systems of record.

## Service maturity levels

| Level | Offer | Minimum evidence |
|---|---|---|
| 0 — Portable instructions | SKILL.md, methodology and references | Package validation and clear scope |
| 1 — Reproducible capability | Versioned scripts, pinned dependencies and fixtures | Automated tests and repeatable outputs |
| 2 — Evaluated capability | Quality, accuracy, safety and regression evaluations | Published evaluation protocol and dated results |
| 3 — Managed execution | Controlled runtime, authorized data, monitoring and artifact delivery | Runtime tests, operational controls and incident process |
| 4 — Contracted service | Defined support, service objectives, accountability and customer integration | Service terms, measurable SLO/SLA and named owner |

A Skill may be distributed at one level while the factory supports others. Do not infer a higher level from a manifest declaration.

## Pricing and responsibility

Potential pricing dimensions include per invocation, usage volume, managed compute, licensed data, workflow outcome or enterprise support. Pricing metadata must be optional and must not imply a guarantee of investment or business outcomes.

Before charging for a capability, define:
- what is included and excluded;
- who supplies and licenses each data source;
- what is executed versus reasoned by the model;
- how results are evaluated and what thresholds apply;
- what happens on stale data, missing dependencies, failed execution or incorrect output;
- retention, privacy, security and incident responsibilities;
- which decisions remain with the customer and require human review.

For consequential domains such as finance, legal and health, a disclaimer is not a substitute for competent review, controls or accountability.

## Factory position

The Agent Skills Factory is an open distribution and governance layer. It does not claim to be a hosted execution service, data licensor, certification body or guarantor of outputs. A third-party provider may offer managed services around a Skill, but those commitments must be separately identified and evidenced.

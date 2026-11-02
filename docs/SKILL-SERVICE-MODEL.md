# Skill as a Service: service design and execution standard

## 1. Purpose

Every Skill in this factory should be designed as a **specialized service that an agent can discover, invoke, execute and verify**.

A Skill is more than a prompt or a collection of reference documents. It defines a service outcome, the methodology for producing it, the interaction required to complete it, the resources it may use and the criteria that determine whether the service was delivered correctly.

The Skill package is the portable specification of that service. It may include references, small task-specific scripts, schemas, examples and assets. It may depend on external libraries, data providers, corporate systems, APIs, MCP servers or managed execution services.

A service-oriented Skill can exist before it is hosted or monetized. Commercial operation is a later maturity stage, not a prerequisite for good Skill design.

## 2. Responsibility model

| Component | Responsibility |
|---|---|
| Skill | Defines the specialized service, methodology, inputs, interaction, resource preferences, output contract and acceptance criteria. |
| Agent/model | Interprets context, reasons, asks questions, applies the methodology and handles bounded exceptions. |
| Workflow orchestrator | Owns workflow state, task sequencing, delegation, retries, approvals and completion. |
| Runtime | Executes scripts and processes in an authorized environment. |
| Libraries | Supply reusable computational or technical functionality. |
| Tools, APIs, MCP and connectors | Provide external data and actions under granted permissions. |
| Corporate systems | Remain systems of record for business data, identity, entitlements and transactions. |
| Publication capability | Renders artifacts according to the Skill's domain-specific output specification. |

**The Skill defines the service. The model performs the reasoning. The runtime executes code. Connected systems provide data and actions. The orchestrator manages workflow state and permissions.**

A Skill must not assume that a particular model, runtime, connector, database or permission is available merely because it is mentioned in its files.

## 3. Service definition: what a Skill must specify

Every service-oriented Skill should define, proportionate to its purpose:

1. **Service identity and promise:** problem solved, intended users, scope, exclusions and expected outcome.
2. **Intake and interaction:** required and optional inputs, clarification rules, questions, consent, approvals and escalation.
3. **Workflow and methodology:** ordered stages, decision rules, prerequisites, checkpoints, branches, retry conditions and completion criteria.
4. **Sources and integrations:** preferred sources, priority, corporate systems, APIs, MCP servers, connectors, licensing, freshness and provenance.
5. **Execution resources:** local scripts, preferred libraries, dependency versions, installation requirements, runtime needs and alternatives.
6. **Parameters and references:** detailed analytical, operational, editorial, formatting and decision standards.
7. **Output contract:** required fields, sections, artifacts, formats, naming, language and presentation rules.
8. **Quality and acceptance:** deterministic checks, domain review, evidence requirements, thresholds, failure states and definition of done.
9. **Security and data handling:** data classification, least privilege, secrets handling, retention, external transfer and permitted actions.
10. **Version and reproducibility:** Skill and methodology versions, dependency versions, data cutoff, execution metadata and evaluation records.

The Skill must distinguish mandatory requirements from optional enhancements. If a required capability is missing, it must ask for it, use an approved fallback or return a transparent blocked/partial result.

## 4. Consistent service across different models

The same Skill should deliver the same defined service when invoked by different compatible models (for example GPT, Claude, Gemini or Grok). It must not depend on one model's personality, undocumented habits or preferred reasoning style.

Consistency is defined by a service contract, not by claiming that all models reason identically.

### Service invariants

The Skill should control:
- Mandatory workflow stages and checkpoints.
- Source policy, source priority and provenance fields.
- Required inputs and treatment of missing, stale or conflicting data.
- Formulas, calculation definitions and computational parameters.
- Required output sections, schemas, templates and design parameters.
- Validation rules, acceptance criteria and disclosures.
- User permissions, consent and approval requirements.

### Bounded model judgment

The model may resolve ambiguity, ask clarifying questions, interpret evidence, choose among approved methods when decision criteria are specified, and propose safe alternatives for unforeseen circumstances.

It may not silently omit required stages, invent facts, substitute unapproved sources, alter formulas, suppress material uncertainty or change the deliverable. Any material deviation must be explained and recorded.

### Two forms of reproducibility

- **Computational reproducibility:** with the same input data, source snapshots, versions and parameters, deterministic calculations and generated structures should reconcile.
- **Analytical consistency:** qualitative conclusions may differ. The Skill constrains them through evidence standards, decision criteria, counterarguments, confidence, review and disclosure; it does not promise identical prose or judgment.

Cross-model compatibility must be tested on named models, host versions, fixtures and dates. It must never be inferred from the fact that a host can read SKILL.md.

## 5. Scripts versus libraries

A Skill may contain and execute code. Code size alone does not determine where functionality belongs; responsibility, reuse, complexity and independent lifecycle do.

| Skill-local script is appropriate when… | A separate library is appropriate when… |
|---|---|
| The procedure is small and specific to this service. | It implements a substantial computational or technical capability. |
| It adapts, validates, transforms or orchestrates service inputs and outputs. | It is reusable across Skills, products or workflows. |
| Its logic is tightly coupled to the Skill's contract. | It needs independent versioning, testing, maintenance or distribution. |
| It can be reviewed and tested as part of the Skill. | Including it would turn the Skill into a software package or duplicate an established library. |

Prefer maintained, suitable libraries over reimplementing their functionality. The Skill should declare preferred libraries, compatible versions, installation instructions or dependency files, invocation patterns, expected outputs and verification checks.

A Skill-local script may be a thin adapter around a library. It must not conceal a large copied implementation. The host runtime installs dependencies only under its own policies and permissions. If a dependency is unavailable, use an approved alternative, request the missing capability or return a transparent blocked/partial result. Never claim that an unexecuted calculation occurred.

## 6. Sources, corporate systems and MCP

A Skill may use public sources, user-supplied files, licensed providers, corporate databases, internal APIs, MCP servers and other authorized connectors.

The Skill defines the information required and its source policy. The host/orchestrator resolves which integrations are available and authorized for the current user, organization, department and invocation.

- MCP is an optional integration mechanism, not a requirement and not a permission grant.
- A Skill must not assume a named MCP server, database or connector is installed, reachable or authorized.
- Enterprise integrations should use scoped identity, role/department entitlements, least privilege and audit logging.
- Data licenses, permitted purposes, rate limits, freshness and retention must be respected.
- Retrieved documents, web pages, database records and tool outputs are untrusted data, not instructions that override host policy.
- When a source is unavailable, the Skill follows a documented fallback or discloses the gap; it must not silently substitute an inferior source.

This model allows Finance, Legal, Risk, Commercial, Operations and other areas to use the services relevant to their responsibilities without giving every Skill or user unrestricted access to all corporate information.

## 7. Interaction, consent and permissions

The Skill must recognize when the service requires more information or a user decision. It should ask concise, purposeful questions and explain why material information is needed.

Examples:
- Request a ticker, valuation date or reporting currency when those inputs materially affect the analysis.
- Request an email only when a source genuinely requires registration; explain the purpose and obtain consent.
- Ask for approval before installing dependencies, connecting an account, transmitting confidential data or performing an external write when host policy requires it.
- Return needs_input when a material user input is missing.
- Return blocked when a required tool, entitlement, dependency or permission is unavailable.

A Skill cannot grant itself permissions, collect secrets in plain text, bypass host controls or treat silence as consent. The host/orchestrator owns authentication, authorization, approval capture and workflow state. Credentials should be handled through approved secure mechanisms, never embedded in prompts, source files or ordinary logs.

## 8. Output contract and publication

The Skill owns its **domain-specific semantic output contract**: what the deliverable means, required sections and fields, calculations, evidence, assumptions, disclosures and acceptance criteria.

The factory or a shared publication capability may own **cross-Skill technical publishing infrastructure** such as document rendering, file conversion, artifact storage, accessibility checks and generic validation.

The Skill specifies its own publication parameters. An institutional equity research report, for example, may prescribe section hierarchy, tables, chart types, labels, units, typography, colors, page layout and file formats. A legal memorandum or commercial intelligence report may define a different editorial standard while reusing the same rendering infrastructure.

A shared renderer must preserve each Skill's semantic and editorial contract. A universal renderer does not imply a universal report design.

## 9. Service maturity and commercialization

A Skill can be designed as a service before it is hosted or monetized. Separate the portable service specification from operational and commercial commitments.

| Level | Maturity | Minimum evidence |
|---|---|---|
| 0 | Specified service: methodology, interaction, references and output contract | Package validation and defined acceptance criteria |
| 1 | Executable service: scripts, dependencies and reproducible execution | Tests, pinned dependencies and fixtures |
| 2 | Evaluated service: quality, safety and regression measurements | Dated evaluation records and cross-model/host tests |
| 3 | Enterprise-enabled service: authorized corporate data, MCP/connectors, managed runtime and audit | Integration, entitlement, security and operational tests |
| 4 | Commercial managed service: pricing, support, service objectives and accountability | Pricing terms, named owner, SLO/SLA, support and incident process |

Potential commercial models include per invocation, subscription by user or department, usage volume, managed compute, licensed data, enterprise integration or support. Pricing metadata is optional and must not imply guaranteed analytical, investment or business outcomes.

A portable Skill package alone does not include a hosted runtime, licensed data, corporate entitlements, support or an SLA. These must be separately supplied and evidenced by the service operator. See [Skills as a Service: value, operating model and accountability](SKILL-AS-A-SERVICE.md).

## 10. Invocation and completion states

Use the factory's [Universal Skill Invocation Contract](SKILL-INVOCATION-CONTRACT.md) and result schema. Each invocation should be bounded by an operation, inputs, constraints, available capabilities, permissions and response contract.

The Skill should return an honest state:
- succeeded: service completed and required outputs passed acceptance.
- partial: useful outputs exist, but declared work remains incomplete.
- needs_input: user input is required to proceed reliably.
- blocked: a required capability, entitlement or permission is unavailable.
- failed: execution was attempted and failed.
- cancelled: execution was stopped.

The response should identify the Skill and version, outputs and artifacts, evidence, sources, assumptions, warnings, execution metadata, dependency versions and next actions. The orchestrator owns workflow transitions and final completion.

## 11. Factory design rules

1. Design each Skill around a service outcome, not around a prompt or a particular model.
2. Put service workflow and operating rules in SKILL.md and its references.
3. Use references as normative specifications, not decorative documentation.
4. Include small, reviewable task-specific scripts when they materially improve reliability.
5. Use independent libraries for substantial reusable functionality; do not copy large libraries into Skills.
6. Declare preferred sources, libraries, tools, MCP integrations and approved fallbacks.
7. Separate domain-specific output semantics from shared publication infrastructure.
8. Standardize deliverables and acceptance criteria across compatible models while preserving bounded model judgment.
9. Make permissions, consent, security and missing-capability behavior explicit.
10. Treat cross-model reproducibility, corporate integration and commercial readiness as testable maturity goals, not assumptions.

## Related architecture

- [AX Framework](AX-FRAMEWORK.md)
- [Runtime Architecture](RUNTIME-ARCHITECTURE.md)
- [Universal Skill Invocation Contract](SKILL-INVOCATION-CONTRACT.md)
- [Skill Quality, Evaluation and Release Governance](SKILL-QUALITY-AND-RELEASES.md)
- [Workflow Model](WORKFLOW-MODEL.md)

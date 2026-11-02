# Architecture

## Goal

Maintain portable, reusable Skills while designing for complete Agent Experience (AX). A Skill is a specialized service capability within a broader person–agent workflow; it is not the workflow, orchestrator, interface or runtime.

The factory's service-design principle is defined in [SKILL-SERVICE-MODEL.md](SKILL-SERVICE-MODEL.md). Commercial and managed-service considerations are defined separately in [SKILL-AS-A-SERVICE.md](SKILL-AS-A-SERVICE.md).

See [AX-FRAMEWORK.md](AX-FRAMEWORK.md) and [RUNTIME-ARCHITECTURE.md](RUNTIME-ARCHITECTURE.md).

## Layers and responsibilities

1. **AX experience:** workflow experience, agent behavior & orchestration, conversational & multimodal interface, and human–agent coordination.
2. **Agent/orchestrator:** interprets goals, plans work, selects Skills/tools/runtimes, delegates and manages state.
3. **Skill service package:** SKILL.md, references, optional scripts, schemas and assets; defines a specialized service outcome, method, interaction, resource requirements, output contract and acceptance criteria.
4. **Registry:** registry/skills.json and each manifest describe identifiers, versions, paths, license, service profile and requirements.
5. **Distribution:** GitHub is source of truth; compatible installers distribute packages to supported agent directories.
6. **Runtime:** native sandbox, local execution or authorized remote service runs code and processes.
7. **Tools/data:** APIs, MCP servers, connectors, corporate databases and providers supply external data or actions.
8. **Publication:** shared rendering and artifact infrastructure produces files according to each Skill's domain-specific output specification.
9. **Host interface:** chat, voice, visualizations, files and controls.

These layers can be deployed together or separately. Their logical responsibilities must remain explicit.

## Workflow and invocation contracts

The AX workflow record is the durable representation of the user's goal, constraints, tasks, approvals, evidence, artifacts, events and checkpoint. The orchestrator owns this state; the chat transcript is not its source of truth.

A Skill invocation is a bounded request/response exchange correlated to a workflow task. The invocation contract does not grant permissions or imply that runtime capabilities exist. See [WORKFLOW-MODEL.md](WORKFLOW-MODEL.md), [SKILL-INVOCATION-CONTRACT.md](SKILL-INVOCATION-CONTRACT.md) and the JSON Schemas under schemas/.

## Service package responsibilities

A Skill defines:
- the service promise, target user, scope and exclusions;
- intake questions, required inputs, consent and approval points;
- workflow stages, methodology, decision rules and exception handling;
- preferred sources, integrations, libraries and execution dependencies;
- domain-specific output structure, parameters, formats and quality gates;
- provenance, limitations, reproducibility and handoff information.

A Skill may contain small, reviewable scripts that are specific to its service. Substantial reusable functionality should be provided by independent libraries or services. The Skill should declare preferred libraries and how to invoke and verify them; the runtime installs and executes them under host policy.

A Skill can use corporate data, internal APIs, licensed providers or MCP integrations when available and authorized. It cannot grant itself access. The orchestrator resolves identity, entitlements, approvals and available capabilities.

## What a Skill is not

A Skill is not an AI model, orchestrator, user interface, Python interpreter, package manager, data provider, API/MCP server or permission grant. Including a script does not guarantee the host can execute it.

## Execution modes

- Native sandbox when available and suitable.
- Local runtime when accessible and authorized.
- Remote runtime through an agent-callable interface, when authorized.
- No-execution fallback with transparent limits.

A web compiler is not automatically an agent-callable runtime and should not receive confidential data.

## Important separation

A Skill does not need MCP. MCP exposes tools to an agent; it is one optional integration path. A Skill does not grant access to paid data, corporate systems, network, filesystem, Python or document-generation libraries. The consuming environment must provide and authorize these capabilities.

The Skill owns its domain-specific semantic and editorial output contract. Shared factory infrastructure may own generic validation, document rendering, file conversion and artifact storage, but it must preserve each Skill's required sections, calculations, visual parameters and disclosures.

## Distribution lifecycle

Design service -> Specify workflow and contracts -> Implement resources -> Validate package -> Evaluate -> Version -> Publish -> Discover -> Install -> Invoke -> Resolve permissions, data and runtime -> Execute -> Verify -> Review -> Deliver -> Record outcome.

Use semantic versioning, keep published tags immutable, record tested agent/product versions and never silently change a methodology used in a completed analysis.

## Initial choices

- Public GitHub repository under owner's personal account.
- MIT license for factory code and documentation.
- Standard Agent Skills package layout.
- Vercel Skills CLI as first installer, not a custom installer.
- No Composio dependency in the portable core; Composio may be an optional remote-runtime adapter.
- No mandatory MCP server.
- No universal hosted runtime or custom agent UI in the initial scope.

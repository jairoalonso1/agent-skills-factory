# Universal Skill Invocation Contract

## Purpose

Define a vendor-neutral request/response envelope for invoking a specialist Skill from an AX workflow.

The contract separates **what capability is requested** from **how a particular agent host executes it**. It is designed for an agent to call an instruction-only Skill, a Skill with local scripts, or a Skill that uses authorized tools. It does not require MCP, Composio, a particular model, Python or a hosted execution service.

## Roles

- **Workflow orchestrator:** owns workflow state, plans work, selects a Skill, resolves permissions and handles retries/handoffs.
- **Skill:** applies specialist instructions and resources to the bounded operation.
- **Runtime:** executes scripts or processes when available.
- **Tools/data providers:** supply external data or actions under the host's permissions.
- **Requester/reviewer:** provides context, approvals and acceptance.

The Skill must not assume it owns the workflow, can grant itself permissions, or can discover arbitrary host resources.

## Request envelope

The request contains:

1. `protocol_version`: version of this invocation contract.
2. `invocation_id`: unique identifier for this attempt.
3. `workflow_ref`: workflow and task correlation.
4. `skill_ref`: stable Skill ID, requested version and entrypoint.
5. `operation`: bounded capability requested.
6. `request`: goal, structured inputs and relevant context references.
7. `constraints`: scope, deadline, source policy and output expectations.
8. `capabilities`: capabilities the host actually makes available for this invocation.
9. `permissions`: explicitly granted actions and approval requirements.
10. `response_contract`: expected response format and provenance requirements.

The orchestrator must describe only capabilities that are actually available in the current session. An empty or absent capability is not permission to invent a fallback.

### Capability discovery

The host should inspect its active tools and runtime before invoking a Skill. It may declare:
- runtime mode and language;
- installed packages and versions;
- filesystem/artifact support;
- network availability and allowed domains;
- named tools or connectors;
- available data sources.

This is a snapshot of the invocation context, not a promise that all capabilities will remain available. A Skill should check requirements and return `blocked` or `needs_input` if an essential capability is missing.

### Permissions and secrets

Permissions are explicit and scoped. Never place API keys, passwords, access tokens or secret values in the request. Pass an opaque credential handle only if the host's secure tool contract explicitly supports it. A Skill cannot elevate its own permissions.

## Response envelope

A Skill returns one of these statuses:

- `succeeded`: requested operation completed and its outputs were produced.
- `partial`: useful outputs exist, but some requested work remains incomplete.
- `needs_input`: a specific missing input prevents reliable progress.
- `blocked`: a required capability, permission or dependency is unavailable.
- `failed`: execution was attempted and failed.
- `cancelled`: execution was stopped.

The response includes:
- the same invocation ID and workflow/task references;
- Skill ID and version actually used;
- concise summary;
- structured outputs;
- artifact references;
- evidence/provenance;
- warnings and errors;
- execution metadata;
- next actions and approval requests where relevant.

The Skill must distinguish calculations actually executed from conceptual estimates or model-generated reasoning. It must not claim network access, code execution, package installation or file creation unless those actions occurred and were verified.

## Retry and idempotency

- A new attempt gets a new `invocation_id`.
- Preserve a stable `workflow_ref.task_id` across retries of the same task.
- Use an idempotency key when a host tool supports it, especially for external writes.
- Do not automatically retry non-idempotent actions.
- Include failure codes and whether a retry is likely to help.
- Preserve partial outputs when safe and useful.

The invocation ID is a correlation identifier; it does not itself guarantee exactly-once execution.

## Output and handoff rules

- Return machine-readable structured outputs where possible, with human-readable summaries.
- Return file references rather than embedding large binary files in JSON.
- Include source URLs or stable source identifiers, retrieval timestamps and relevant date ranges.
- Identify assumptions, unavailable data, stale data and model limitations.
- Use `needs_input` for a material question to the requester; use `blocked` when the host must supply a capability or permission.
- Approval requests describe the action but do not execute it.
- The orchestrator owns workflow state transitions, user communication, approvals and task completion.

## Versioning and compatibility

The contract version is independent of Skill versions and agent product versions. Breaking changes require a new major contract version. Skills may support more than one contract version through adapters.

A host may support the Skill package format but not support this invocation envelope natively. In that case, an adapter maps the host's native call/return format to this contract. Compatibility must be tested, not inferred.

## Schemas and examples

- Request schema: `schemas/skill-invocation.schema.json`
- Response schema: `schemas/skill-result.schema.json`
- Request example: `examples/skill-invocation.json`
- Response example: `examples/skill-result.json`

## Initial implementation recommendation

Implement this contract first as a documented JSON boundary and schema validation suite. Do not build a universal runtime or network service yet. Prove it with one workflow and one Skill, then write thin adapters for specific agent hosts only when their native interfaces are known and tested.

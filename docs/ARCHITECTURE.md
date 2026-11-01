# Architecture

## Goal

Maintain portable, reusable Skills while designing for complete Agent Experience (AX). A Skill is one capability within a broader person–agent workflow; it is not the workflow, orchestrator, interface or runtime.

See [AX-FRAMEWORK.md](AX-FRAMEWORK.md) and [RUNTIME-ARCHITECTURE.md](RUNTIME-ARCHITECTURE.md).

## Layers and responsibilities

1. **AX experience:** workflow experience, agent behavior & orchestration, conversational & multimodal interface, and human–agent coordination.
2. **Agent/orchestrator:** interprets goals, plans work, selects Skills/tools/runtimes, delegates and manages state.
3. **Skill package:** SKILL.md, references, optional scripts and assets; contains portable domain methodology and a capability contract.
4. **Registry:** registry/skills.json and each manifest describe identifiers, versions, paths, license and requirements.
5. **Distribution:** GitHub is source of truth; compatible installers distribute packages to supported agent directories.
6. **Runtime:** native sandbox, local execution or authorized remote service runs code and processes.
7. **Tools/data:** APIs, MCP servers, connectors and providers supply external actions and information.
8. **Host interface:** chat, voice, visualizations, files and controls.

These layers can be deployed together or separately. Their logical responsibilities must remain explicit.

## Workflow and invocation contracts

The AX workflow record is the durable representation of the user's goal, constraints, tasks, approvals, evidence, artifacts, events and checkpoint. The orchestrator owns this state; the chat transcript is not its source of truth.

A Skill invocation is a bounded request/response exchange correlated to a workflow task. The invocation contract does not grant permissions or imply that runtime capabilities exist. See [WORKFLOW-MODEL.md](WORKFLOW-MODEL.md), [SKILL-INVOCATION-CONTRACT.md](SKILL-INVOCATION-CONTRACT.md) and the JSON Schemas under `schemas/`.

## What a Skill is not

A Skill is not an AI model, orchestrator, user interface, Python interpreter, package manager, data provider, API/MCP server or permission grant. Including a script does not guarantee the host can execute it.

## Execution modes

- Native sandbox when available and suitable.
- Local runtime when accessible and authorized.
- Remote runtime through an agent-callable interface, when authorized.
- No-execution fallback with transparent limits.

A web compiler is not automatically an agent-callable runtime and should not receive confidential inputs.

## Important separation

A Skill does not need MCP. MCP exposes tools to an agent; it is one optional integration path. A Skill does not grant access to paid data, network, filesystem, Python or document-generation libraries. The consuming environment must provide and authorize these capabilities.

## Distribution lifecycle

```text
Author -> Validate -> Review -> Version -> Publish
                                      |
                                      v
                           Discover -> Install -> Invoke
                                      |
                                      v
                         Select runtime/tools -> Verify
                                      |
                                      v
                         Human review -> Complete
```

Use semantic versioning, keep published tags immutable, record tested agent/product versions and never silently change a methodology used in a completed analysis.

## Initial choices

- Public GitHub repository under owner's personal account.
- MIT license for factory code and documentation.
- Standard Agent Skills package layout.
- Vercel Skills CLI as first installer, not a custom installer.
- No Composio dependency in the portable core; Composio may be an optional remote-runtime adapter.
- No mandatory MCP server.
- No universal hosted runtime or custom agent UI in the initial scope.

# Agent Skills Factory

Open, vendor-neutral repository for reusable AI Agent Skills and their optional execution resources.

Owner: Jairo Alonso González  
Factory license: MIT. Each Skill may specify its own license.

## Purpose

GitHub is the source of truth. Each Skill is a portable package centered on a standard `SKILL.md`, with optional references, scripts and assets. The package describes a specialized capability; it does not assume every host has the same model, interface, orchestration, runtime, network access or tools.

**AX (Agent Experience)** is the broader design discipline for the complete person–agent work experience. The factory supplies reusable capabilities that agents can invoke inside AX workflows.

Read:
- [AX — Agent Experience](docs/AX-FRAMEWORK.md)
- [Skill, Capability and Runtime Architecture](docs/RUNTIME-ARCHITECTURE.md)
- [Execution Capability Matrix](docs/EXECUTION-CAPABILITY-MATRIX.md)
- [Platform compatibility](docs/PLATFORM-COMPATIBILITY.md)

## Available Skills

| Skill | Purpose | Version | Status |
|---|---|---:|---|
| [finanzas-valoracion-accion](skills/finanzas-valoracion-accion/SKILL.md) | Institutional equity research and valuation | 0.1.0 | Initial port; runtime validation pending |

Machine-readable catalogue: [registry/skills.json](registry/skills.json).

## Discover and install

Recommended general installer: the open-source Vercel Skills CLI. It detects supported agent directories and installs from GitHub.

```bash
npx skills add jairoalonso1/agent-skills-factory --list
npx skills add jairoalonso1/agent-skills-factory --skill finanzas-valoracion-accion
npx skills check
npx skills update finanzas-valoracion-accion
```

Consult the [CLI documentation](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) for current agent identifiers and capabilities.

## What is a Skill?

A Skill is a portable, discoverable package of procedural knowledge, methodology and task-specific resources. It defines when to use a capability, inputs, procedure, constraints, outputs and verification.

A Skill is not a model, orchestrator, UI, runtime, package manager, data provider, API/MCP server or permission grant. It may contain scripts, but the host must provide a compatible execution environment.

## AX relationship

- AX designs the end-to-end person–agent workflow and interaction.
- The agent/orchestrator plans, reasons and selects capabilities.
- A Skill provides a specialized, reusable capability.
- A runtime executes code when available.
- Tools/connectors provide external data and actions.
- The host interface presents progress, evidence and results.

A workflow can invoke multiple Skills, tools and runtimes. A Skill can be reused by many workflows and agents.

## Execution and dependencies

Python and third-party libraries are optional runtime dependencies, not prerequisites for understanding or loading a Skill. A dependency declaration does not install a package. The host/runtime must provide and verify it.

Execution preference: host sandbox, authorized local/managed runtime, authorized remote runtime, then a bounded no-execution fallback. Public online compilers are suitable only for isolated non-sensitive experiments; do not send confidential data or secrets.

MCP is optional. Use it only when the workflow needs an external tool exposed through MCP and the host supports it.

## Workflow and invocation contracts

AX workflows and Skill calls use vendor-neutral data contracts:
- [AX Workflow Experience model](docs/WORKFLOW-MODEL.md)
- [Universal Skill Invocation Contract](docs/SKILL-INVOCATION-CONTRACT.md)
- JSON Schemas: `schemas/`
- Interoperability examples: `examples/`

These schemas define portable data boundaries; they are not a runtime, scheduler or agent framework.

## Principles

- Vendor-neutral portable core.
- Progressive disclosure and explicit capability contracts.
- Honest distinction between documented, declared and runtime-tested compatibility.
- Reproducible outputs with sources, assumptions, dates and versions.
- Secure execution; never bundle secrets.
- Human accountability and explicit approvals for consequential actions.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

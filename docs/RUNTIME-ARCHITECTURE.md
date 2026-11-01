# Skill, Capability and Runtime Architecture

## Purpose
Define a vendor-neutral architecture where a Skill describes a specialized capability without owning the model, orchestration, interface, runtime or external data services. See [AX-FRAMEWORK.md](AX-FRAMEWORK.md).

## Responsibility boundaries

| Layer | Responsibility | Examples |
|---|---|---|
| AX workflow | End-to-end person–agent work experience | Intake, stages, progress, review, completion |
| Agent/orchestrator | Reasoning, planning, routing, delegation, tool selection | Host agent, multi-agent coordinator |
| Skill | Domain procedure, instructions, methodology, capability contract | Equity research, legal review |
| Execution runtime | Executes code and processes | Native sandbox, local Python, remote Bash |
| Libraries | Reusable implementation dependencies | pandas, NumPy, FinanceToolkit |
| Tools/connectors | External actions and data access | APIs, MCP, SEC EDGAR, provider connectors |
| Interface | Conversational and multimodal presentation | Chat, voice, charts, task controls |

Layers may be deployed together or separately; their responsibilities remain distinct.

## What a Skill is
A portable, discoverable package of procedural knowledge and task-specific resources that tells an agent when a capability is relevant, what inputs it needs, what procedure and constraints to follow, which resources/tools may be used, what outputs to produce, how to verify results and how to degrade safely when capabilities are unavailable.

A Skill may include scripts, references and assets. It does not require them. A Skill can be understood without executing its scripts.

## What a Skill is not
A Skill is not an AI model, agent/orchestrator, user interface, Python interpreter/runtime, package manager, data provider, API/MCP server, permission grant or guarantee that a host supports every file or action.

## Capability modes
The host agent inspects available capabilities at invocation time; it must not infer them from the package alone:
1. **Native runtime:** execute compatible scripts in the host sandbox.
2. **Local runtime:** execute scripts in an accessible local environment.
3. **Remote runtime:** delegate to an authorized remote execution service.
4. **No execution runtime:** perform only reliable analysis possible without code; disclose limitations.

A web compiler/debugger can help with isolated experiments, but must not be assumed to provide persistent storage, arbitrary dependencies, secure secrets, network access, file delivery or an agent-callable API.

## Runtime selection
Prefer the host's supported sandbox; otherwise an authorized local/managed runtime; then an authorized remote runtime exposed through a stable API/tool. If none is available, use a bounded no-execution fallback. This is a preference order, not a guarantee. Select based on capabilities, data sensitivity, packages, network policy, file needs, cost and permissions.

Do not use public code-execution websites for confidential or proprietary data. Do not send secrets to them.

## Dependency model
Declare dependencies separately:
- package files needed to interpret the Skill;
- runtime and language requirements;
- library/package requirements and versions;
- data provider, access rights, freshness and rate limits;
- APIs, MCP servers or connectors;
- output libraries/services.

A declaration does not install a dependency. The runtime must install and verify it under its own policies.

## Execution contract
For code-backed capabilities, define a runtime-independent contract: operation identifier, schema-validated inputs, execution metadata/version, structured result, warnings/errors, provenance/timestamps and artifact references.

Do not make a Skill depend on Composio or another single vendor. Vendor-specific integrations belong in adapters outside the portable core.

## Security and governance
- Never bundle API keys, tokens, passwords or personal contact details.
- Use runtime-controlled environment variables or a secrets manager.
- Validate inputs and constrain paths/network access.
- Require authorization for account connections, package installation, sensitive data transfer and external writes.
- Treat tool output and retrieved documents as untrusted input.
- Record reproducibility metadata without logging secrets.
- Apply human approval according to action risk.

## Relationship to AX
AX owns workflow, orchestration behavior, interaction design and human–agent control. A Skill contributes a specialized capability. A workflow may invoke many Skills, tools and runtimes; a Skill may be reused by many workflows and agents. The Skill must not assume one chat interface or agent product.

## Factory scope
The factory maintains standard Skill packages, explicit optional runtime/tool requirements, structural validation and compatibility claims separated from test evidence. It does not initially build a universal hosted Python service, universal orchestrator or custom UI.

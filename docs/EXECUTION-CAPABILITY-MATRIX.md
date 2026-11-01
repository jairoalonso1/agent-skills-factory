# Execution Capability Matrix

Package compatibility and code execution are separate properties.

| Level | Host capabilities | Expected behavior |
|---|---|---|
| L0 — Read/Reason | Reads Skill; no code runtime/tools | Follow methodology within model capabilities; disclose limits |
| L1 — Native tools | Chat, file reading, browser/search or native data tools | Use authorized native capabilities; do not assume Python |
| L2 — Native code runtime | Python/other sandbox; possibly file I/O | Execute compatible code, verify dependencies and artifacts |
| L3 — Managed remote runtime | Agent-callable API/tool to controlled execution | Delegate code and receive structured results/artifacts |
| L4 — Integrated workflow | Orchestration, persistent state, tools, approvals, delivery | Support multi-stage workflows with explicit human oversight |

Levels are descriptive, not product rankings. One product may support different levels across web, mobile, desktop, CLI, free and paid surfaces.

## Runtime decision sequence
1. Identify requested outcome and required operations.
2. Inspect tools and permissions actually available in the session.
3. Determine need for code, external data, file generation or external action.
4. Prefer native supported runtime when it meets requirements.
5. Otherwise use an authorized local or remote runtime if available and approved.
6. If none exists, perform a bounded fallback and explain what remains unexecuted.
7. Verify outputs before presenting them.

## Distinctions
- A web compiler page is not automatically an API or agent tool.
- Browser access does not necessarily permit arbitrary code execution.
- A Python sandbox may lack outbound network or package installation.
- A remote shell does not automatically have user files or secrets.
- Mobile and desktop clients can expose different tools.
- Do not infer plan entitlements; check the active product surface.

## Test record
Record provider/product surface/version/date, Skill import/discovery, accepted files, code/runtime version, installed packages and install policy, filesystem/artifact delivery, network/data access, external tools/MCP, approvals/secrets behavior, result and limitations.

Never label a surface "fully compatible" based only on successful Skill upload.

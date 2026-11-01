# Agent Skills Factory

Open, vendor-neutral repository for reusable AI Agent Skills.

Owner: Jairo Alonso González  
Factory license: MIT. Each Skill may specify its own license in its manifest.

## What this is

GitHub is the source of truth. Each Skill is a folder containing a standard SKILL.md plus optional references, scripts and assets. The same portable core can be installed into compatible agent environments; platform-specific import and discovery methods are documented separately.

This repository does not assume every AI product has the same discovery mechanism, execution tools, network access or runtime.

## Available Skills

| Skill | Purpose | Version | Status |
|---|---|---:|---|
| [finanzas-valoracion-accion](skills/finanzas-valoracion-accion/SKILL.md) | Institutional equity research and valuation | 0.1.0 | Initial port; runtime validation pending |

Machine-readable catalogue: [registry/skills.json](registry/skills.json).

## Discover and install

Recommended general installer: the open-source Vercel Skills CLI. It detects supported agent directories and installs from GitHub.

List Skills:
~~~bash
npx skills add jairoalonso1/agent-skills-factory --list
~~~

Install the equity research Skill:
~~~bash
npx skills add jairoalonso1/agent-skills-factory --skill finanzas-valoracion-accion
~~~

Install for a specific supported agent:
~~~bash
npx skills add jairoalonso1/agent-skills-factory --skill finanzas-valoracion-accion --agent claude-code
~~~

Install globally where supported:
~~~bash
npx skills add jairoalonso1/agent-skills-factory --skill finanzas-valoracion-accion -g
~~~

Check and update:
~~~bash
npx skills check
npx skills update finanzas-valoracion-accion
~~~

The CLI's supported agent identifiers evolve independently. Consult its [CLI documentation](https://github.com/vercel-labs/skills/blob/main/docs/commands.md).

## Manual installation

If an environment is not detected, copy the complete Skill directory—not only SKILL.md—to the location documented by that agent. Standard package:

~~~text
skills/finanzas-valoracion-accion/
├── SKILL.md
├── manifest.json
└── references/
    └── valuation-framework.md
~~~

A compatible agent must be able to read Skill files. For products without native discovery, use the platform's supported import/upload mechanism or attach the package and explicitly ask the agent to follow it. This is not equivalent to native automatic discovery.

## Does a Skill need MCP?

No. A Skill defines a workflow and domain instructions. MCP servers, APIs, local scripts and other tools are optional dependencies. The equity research Skill can guide analysis without MCP. Live data access or external actions require an authorized data source, connector, API or MCP tool. Reproducible calculations and file generation require a suitable Python/runtime environment and packages.

## Principles

- Portable core: standard SKILL.md, relative references and optional scripts.
- Honest compatibility: do not claim support until tested.
- Progressive disclosure: keep detailed methodology in references.
- Reproducibility: record sources, as-of dates, assumptions and versions.
- Safety: review executable code, pin dependencies where practical, never bundle secrets.
- Human accountability: research outputs are not personalized investment advice.

## Structure

~~~text
.
├── registry/skills.json
├── skills/<skill-name>/
│   ├── SKILL.md
│   ├── manifest.json
│   ├── references/
│   ├── scripts/
│   └── assets/
├── docs/
├── scripts/
└── .github/workflows/
~~~

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

## Status

First public MVP. The initial Skill is a careful port of the supplied source file, not a claim that every valuation method, data provider or deliverable has been integration-tested in every agent runtime.

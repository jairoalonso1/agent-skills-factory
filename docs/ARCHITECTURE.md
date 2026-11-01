# Architecture

## Goal

Maintain one canonical, vendor-neutral Skill package and distribute it into different agent environments without assuming identical capabilities.

## Layers

1. **Skill package:** SKILL.md, references, optional scripts and assets. This is the portable methodology.
2. **Registry:** registry/skills.json and each Skill's manifest.json describe identifiers, versions, paths, licenses and requirements.
3. **Distribution:** GitHub is the source repository. The open Vercel skills CLI installs compatible Skills into supported agent directories and checks/updates installations.
4. **Platform adapters:** documentation or packaging metadata for environments with different import, plugin or discovery mechanisms.
5. **Runtime dependencies:** Python, data providers, APIs, MCP servers and credentials are external dependencies, not implicitly bundled with a Skill.

## Important separation

A Skill does not need MCP. The Skill describes a workflow; MCP exposes tools to an agent. Use MCP only when a workflow needs a tool the agent does not otherwise have.

A Skill does not automatically grant access to paid data, network, filesystem, Python or document-generation libraries. The consuming environment must provide and authorize those capabilities.

## Distribution lifecycle

~~~text
Author -> Validate -> Review -> Version -> Publish on GitHub
                                      |
                                      v
                         Discover -> Install -> Invoke
                                      |
                                      v
                               Check -> Update
~~~

Use semantic versioning, keep published tags immutable, update registry metadata with each release, record tested agent/product versions and never silently change a methodology used in a completed analysis.

## Initial choices

- Public GitHub repository under owner's personal account.
- MIT license for factory code and documentation.
- Standard Agent Skills package layout.
- Vercel Skills CLI as first installer, not a new custom installer.
- No Composio dependency in core architecture; Composio may later be an integration adapter.
- No mandatory MCP server.

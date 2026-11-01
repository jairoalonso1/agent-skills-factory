# Contributing

Thank you for helping improve the Agent Skills Factory.

## Add or update a Skill

1. Create or update a directory under skills/<skill-name>/.
2. Include SKILL.md with YAML frontmatter containing name and description.
3. Use lowercase kebab-case names. Describe both what the Skill does and when to use it.
4. Put detailed methodology in references/, executable helpers in scripts/, templates in assets/.
5. Add or update manifest.json and registry/skills.json.
6. Update platform compatibility only after testing.
7. Run python scripts/validate_registry.py.
8. Submit a pull request describing behavior changes, dependencies, security implications and validation.

## Authoring rules

- Write instructions for more than one model vendor.
- Do not assume tools, internet access, Python, packages or file-generation support exist.
- State required capabilities and provide graceful fallbacks.
- Never hardcode API keys, passwords, personal access tokens or private credentials.
- Source and timestamp external data.
- Separate facts, assumptions, estimates and analyst judgments.
- Do not force a valuation method when it is unsuitable.
- Treat scripts as software: document dependencies and test where practical.
- Use semantic versions: patch for corrections, minor for backward-compatible capabilities, major for breaking changes.

A platform is documented when official documentation describes support. It is tested only after an installation and invocation test on that product/version. Markdown readability alone does not prove compatibility.

# Platform compatibility

Compatibility is product-surface-specific. A vendor may support Skills in its coding CLI or API without supporting native discovery in its consumer chat interface.

"Documented" means official documentation describes a compatible mechanism. It does not mean this Skill has been runtime-tested on that product.

| Platform / surface | Integration path | Status for this repository |
|---|---|---|
| OpenAI Codex | Standard Skill folder in .agents/skills/ | Documented; runtime test pending |
| ChatGPT desktop / Work / web | Standalone Skill availability depends on product surface; Chat/Work distribution may require a ChatGPT plugin package | Surface-specific; native installation not yet packaged |
| Claude Code | .claude/skills/ or supported Agent Skills location | Documented; runtime test pending |
| claude.ai | Upload custom Skill package through supported settings and plan features | Manual import; runtime test pending |
| Gemini CLI | .gemini/skills/ or .agents/skills/ | Documented; runtime test pending |
| Muse Code | Supports project/user Skills including .agents/skills/ and compatible roots | Documented; runtime test pending |
| Grok / xAI | No verified native Agent Skills import/discovery path recorded in this MVP | Not yet validated; manual prompt/file workflow only if supported |

## Installer

The Vercel Skills CLI supports many coding-agent tools and detects installation directories. Its supported agent identifiers evolve independently. Check its current documentation:

https://github.com/vercel-labs/skills/blob/main/docs/commands.md

Typical commands:

~~~bash
npx skills add jairoalonso1/agent-skills-factory --list
npx skills add jairoalonso1/agent-skills-factory --skill finanzas-valoracion-accion
npx skills check
npx skills update finanzas-valoracion-accion
~~~

## ChatGPT distinction

A GitHub Skill folder is not automatically installed into ChatGPT web/mobile Chat. OpenAI documentation distinguishes standalone Skills for supported desktop/Codex surfaces from plugin packaging for distribution in Chat and Work. A future ChatGPT adapter may package a Skill as a plugin, but must be implemented and tested separately.

## Grok distinction

Do not claim Grok supports native SKILL.md discovery until an official xAI product surface and import mechanism are verified. A Markdown upload or prompt may provide instructions for one session but is not persistent Skill installation.

## Testing checklist

For each platform adapter, record product/version, installation path/import workflow, automatic or explicit discovery, whether scripts run, network access, external tools/MCP access, file-generation capability, limitations and test date.

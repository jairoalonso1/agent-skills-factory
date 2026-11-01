# Security policy

## Reporting a vulnerability

Do not publish secrets, exploit details or sensitive financial data in a public issue. Use a private GitHub Security Advisory where available.

## Skill trust model

A Skill is executable guidance. Its instructions can cause an agent to read files, call tools, access network resources or run scripts. Install only from trusted sources and review changes before updating.

## Requirements

- Never commit API keys, OAuth tokens, passwords, private keys, personal access tokens or environment files.
- Do not embed private user data or credentials in a Skill.
- Scripts must document what they read, write and transmit.
- Avoid destructive operations and external writes unless explicitly requested and authorized.
- Prefer least-privilege credentials and read-only access.
- Pin or constrain third-party dependencies and review supply-chain changes.
- Do not execute downloaded code automatically during installation.
- Verify release tags and package integrity where checksums are provided.

## Financial data

Market and financial data may be licensed, delayed, incomplete or subject to provider terms. Users must ensure they have rights to access and redistribute data. Never publish confidential financial information in public repository issues or commits.

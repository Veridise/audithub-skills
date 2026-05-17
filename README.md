# AuditHub Skills

This repository contains skills for AI agents (e.g., Codex/Claude code) useful for setting up and using AuditHub tools.

## Repository layout
- Each skill lives in its own folder at the repo root.
- Each skill folder must include:
  - `README.md` (purpose + author)
  - `SKILL.md`
  - Optional `assets/`, `references/`, or helpers

For multiple related skills, create a single directory with a single `README.md`, and a sub-directory for each skill.

## Using the skills locally
If your agent supports installing skills directly from a repository, prefer that flow first.

If you are using codex locally, symlink a skill folder into your local `~/.codex/skills` directory so Codex can load it.

If you are using Claude Code, symlink a skill folder into your local Claude skills directory so Claude Code can load it. For many setups, that directory is `~/.claude/skills`.

Example (from repo root):

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/" ~/.codex/skills/audithub-skills
```

Claude Code example:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/" ~/.claude/skills/audithub-skills
```

## Contribution guidelines
- Keep changes minimal and DRY.
- Every skill must have `SKILL.md` and `README.md`. The `README.md` must include the purpose and author.
- If you add templates, place them in `assets/` and keep them small.
- If you add references, place them in `references/` and keep them scoped.
- Prefer ASCII in files unless the skill requires Unicode.
- Add or update tests/examples when behavior changes.

## Skills
- [`orca`](./orca/README.md): Set of skills for setting up OrCa fuzzing campaigns and analyzing OrCa results.
- [`defi-vanguard`](./defi-vanguard/README.md): Set of skills for setting up DeFi Vanguard scans and analyzing their results.

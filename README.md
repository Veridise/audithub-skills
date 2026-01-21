# Auditing Skills

This repository contains skills for AI agents (e.g., Codex/Claude code) useful for setting up and using AuditHub tools.

## Repository layout
- Each skill lives in its own folder at the repo root.
- Each skill folder must include:
  - `README.md` (purpose + author)
  - `SKILL.md`
  - Optional `assets/`, `references/`, or helpers

For multiple related skills, create a single directory with a single `README.md`, and a sub-directory for each skill.

## Using the skills locally
If you are using codex, symlink a skill folder into your local `~/.codex/skills` directory so Codex can load it.

Example (from repo root):

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/write-issue" ~/.codex/skills/write-issue
```

## Contribution guidelines
- Keep changes minimal and DRY.
- Every skill must have `SKILL.md` and `README.md`. The `README.md` must include the purpose and author.
- If you add templates, place them in `assets/` and keep them small.
- If you add references, place them in `references/` and keep them scoped.
- Prefer ASCII in files unless the skill requires Unicode.
- Add or update tests/examples when behavior changes.

## Skills
- `orca`: Set of skills for setting up OrCa fuzzing campaigns and analyze OrCa results.


# AGENTS.md

This repository publishes Agent Skills written from real work. Conventions here are brief on purpose; detail lives in the linked documents.

## Layout

- `skills/<name>/SKILL.md` — one skill per directory. The frontmatter `name` matches the directory name.
- Bundled scripts live in the skill's `scripts/` directory and are part of the skill.
- `README.md` / `README.ja.md` — the short index (skills table).
- `CATALOG.md` / `CATALOG.ja.md` — the per-skill catalog for first-time readers.

## Conventions

- SKILL.md files are written in English. README and the catalog are maintained in English and Japanese, in sync, in the same commit.
- A skill is generalized before it lands here: no machine names, personal paths beyond the layouts the skill itself documents, account details, or tokens. Environment-specific variants stay in the author's own dotfiles.
- Bundled scripts are tested before they are published — at minimum a dry-run against a fixture that exercises the destructive paths safely — and the test is described in the change that adds them.
- Nothing in this repository is published on someone else's behalf: skills adopted from other authors are credited and linked, not copied in.
- Some skills here are generalized editions of working originals the author maintains elsewhere for daily use. The two editions are expected to differ — the original keeps its environment-specific wiring, this edition drops it. When behavior changes or a bug is fixed in one edition, port the change to the other in the same round of work; never let fixes accumulate on one side only. The original records which published skill it corresponds to.

## Routing

- Adding, changing, or removing a skill → update the README tables and the catalog in the same commit. **Read [docs/catalog-guide.md](docs/catalog-guide.md) first** and follow its template and rules for the catalog entry.
- Changing a bundled script's behavior → check whether the skill's SKILL.md and catalog entry still describe it accurately, and update them in the same commit.

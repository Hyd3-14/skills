# Writing the catalog

The catalog ([CATALOG.md](../CATALOG.md) / [CATALOG.ja.md](../CATALOG.ja.md)) is the outsider-facing index of this repository: one entry per skill, written for someone who has never seen the repo and is deciding whether a skill solves their problem. The README table is the short index; the catalog is the per-skill story. This guide is the template and the rules for keeping it current.

## When to update

In the **same commit** that adds, changes, or removes a skill:

- New skill → add a catalog entry and a README table row.
- Behavior change → update the entry if anything it says is affected (what it does, requirements, limits).
- Removal → remove the entry and the row.

## Entry template

Entries appear in the same order as the README table, separated by `---`.

```markdown
## <skill-name>

<One sentence: what the reader can do with it, in their terms.>

**The problem.** <What goes wrong without this skill. Concrete failure modes,
not adjectives. Two to four sentences.>

**What it does.** <The mechanism, in plain terms. Name the concrete techniques,
formats, and safeguards — the things a reader could verify in the SKILL.md.>

**When to use it.** <The situations that should make a reader reach for it.>

**Requirements.** <Tools, versions, and optional integrations. Only what is
actually required; mark optional things as optional.>

→ [skills/<skill-name>/SKILL.md](skills/<skill-name>/SKILL.md)
```

## Rules

- **Problem first.** Every entry earns its place by naming a real failure mode. If you cannot state what goes wrong without the skill, the entry is not ready.
- **Write for a first-time reader.** No repository-internal history, no machine or account specifics, no unexplained local jargon. Terms a general agent user would not know get a half-sentence of explanation or a link.
- **Claims must be checkable.** Numbers (line counts, day counts, version requirements) are copied from the skill or the code at writing time, never from memory. If a number changes, the entry changes in the same commit.
- **Both languages, same commit.** CATALOG.md (English) and CATALOG.ja.md (Japanese) carry the same entries in the same order with the same facts. Neither is a summary of the other.
- **The catalog describes; the SKILL.md instructs.** Do not copy procedure steps into the catalog. If a reader needs the how, the entry links to the SKILL.md.

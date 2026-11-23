---
name: write-readme
description: Create or update a project README from evidence in the repository. Use when a project has no README, when a README has drifted from the code, when the user asks to write, rewrite, or improve a README, or before publishing a repository. Reads the manifest, entry points, docs, and tests first, classifies the project type, builds a centered header with verified badges only, and runs the documented Quick Start before calling the README done.
---

# Write a README

A README is the first page of a repository. A reader who lands on it needs three answers fast. What is this. Is it for me. How do I try it. Everything after the first screen serves one of those answers, in the order a new reader needs it.

Every claim in the README comes from the repository itself. If the code does not confirm a feature, a flag, or a command, the README does not state it.

## Read before you write

Gather the facts first. Read what exists, in this order:

1. The manifest. `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or the equivalent for the stack. It gives the name, the one-line description, the version, the entry points, the scripts, and the runtime versions.
2. The entry points and the public surface. The main module, the exported functions, the routes, or the CLI. Run the CLI with `--help` when it runs, and document the flags it prints, not the flags you expect.
3. The existing README and docs. Note what is still true and what has drifted. Keep wording that works.
4. `CONTRIBUTING.md`, `LICENSE`, and the CI configuration. The README links to the first two and takes its CI badge from the third.
5. The examples and the tests. Tests show real usage with real inputs. An example that already runs is a better Quick Start than a new one written from memory.

## Classify the project

Pick one type. The type sets the section order, because each reader looks for a different first success.

| Type | Section order after the header |
| --- | --- |
| CLI tool | What it does, Quick Start (install, then one command that produces visible output), Usage (the common commands, a flags table), Configuration, How it works, Development, Contributing, License |
| Library | What it does, Quick Start (install, then the smallest working code example), Usage (one example per common task, a link to the full API reference when one exists), Configuration, Development, Contributing, License |
| Web app or service | What it does, Screenshot or demo, Features, Quick Start (run it locally), Configuration (environment variables in a table), How it works, Development, Contributing, License |
| Agent Skill collection | What the collection is, the skill index (a table that links each `SKILL.md`), Install (where to copy a skill for each agent), License. Per-skill detail belongs in a catalog, not in the README |
| Repository template | What the template generates, Quick Start (the generate command), What a generated repository contains, Customization (the questions or answers the generator asks), Updating a generated repository, License |
| Other | The canonical order below, with the sections that have no real content removed |

## Build the header

Center the header. Keep it to the name, one line of description, the badges, and the language switch when the repository has one.

```markdown
<div align="center">

# project-name

One line that says what the project does and who it is for.

[![CI](https://github.com/owner/project/actions/workflows/ci.yml/badge.svg)](https://github.com/owner/project/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

English | [日本語](README.ja.md)

</div>
```

Header rules:

- The description is one line. It names the thing and the reader, not a feature list.
- Badges must be verified in the repository. The CI badge names a workflow file that exists. The license badge matches the `LICENSE` file. The version badge matches the manifest or a release. Four badges at most.
- Never copy a badge URL from another project and change only the name. A badge that points at a workflow the repository does not have is a false claim.
- The language switch appears only when the repository maintains the README in two languages. Center it and separate the names with a vertical bar, as in the example.

## Write the sections

Use this order. Omit a section when the repository gives it nothing true to say. An omitted section costs nothing. A filler section teaches the reader to skip the rest.

- **What it does.** Two or three sentences. The problem it solves, who it is for, and the one thing that sets it apart. No feature list here.
- **Screenshot or demo.** Only when a real asset exists in the repository. A screenshot for an app, a short terminal recording or the real output for a CLI, the output of the smallest example for a library. Never a placeholder image.
- **Features.** A short list, and only when each item is grounded in code you read. Each item names what the reader can do, in one line.
- **Quick Start.** The shortest path to a visible result. Prerequisites in one line (runtime version, account, key). Copy-pasteable commands, with nothing optional mixed in. End with what the reader sees when it worked.
- **Usage.** The common tasks, three to five. Each task gets one sentence, one code block, and one sentence on the result. Link to the full reference for the rest.
- **Configuration.** A table with the option, the flag or environment variable, the default, and what it does. List only options a user will actually set, and only options the code reads.
- **How it works.** Optional. A short paragraph or one diagram for a reader who is deciding whether to trust or extend the project. Skip it when the project is small enough to read.
- **Development.** Clone, install, test, and lint, in as few commands as the repository supports. Link to `CONTRIBUTING.md` for anything longer.
- **Contributing.** Two or three lines and a link to `CONTRIBUTING.md` when it exists. Do not copy its content into the README. When no file exists, say where to open an issue or a pull request.
- **License.** The license name and a link to `LICENSE`.

Omit Roadmap, Contact, and Acknowledgments by default. Add one only when the repository already maintains it and a reader would look for it.

## Keep bilingual READMEs in sync

When a repository maintains the README in two languages, one change updates both files in the same commit. The two files carry the same sections in the same order with the same facts. Neither file is a summary of the other. A section added to one and not the other is drift, and it starts with the next edit.

## Verify before you finish

1. Run the Quick Start commands exactly as written, when they can run in your environment. Fix the README or report the failure. Do not document a path that does not work.
2. Check every command, flag, option, and file path the README names against the code. Remove anything you cannot confirm.
3. Check that every link resolves to a file or a page that exists, and that every badge points at a real workflow, license, or release.
4. Re-read the finished file top to bottom. The first screen must still answer the three questions from the top of this skill.

## Sources

The shape combines three published references. The header and section layout follow [Best-README-Template](https://github.com/othneildrew/Best-README-Template). The section discipline follows [standard-readme](https://github.com/RichardLitt/standard-readme). The read-first and verify-the-Quick-Start procedure follows [readme-writing](https://dotclaude.khaledsaeed.tech/skill/readme-writing/) from the dotclaude collection. This skill adds the project-type orders, the verified-badge rule, and the bilingual sync rule on top of them.

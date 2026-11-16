# skills

English | [日本語](README.ja.md)

Agent Skills I wrote from real work, published as open source.

Each skill lives in `skills/<name>/SKILL.md` and follows the [Agent Skills](https://agentskills.io) format, so it works across Claude Code, Codex, GitHub Copilot, and other compatible agents.

For what each skill solves and when to use it, see the [catalog](CATALOG.md).

## Skills

| Skill | What it does |
| --- | --- |
| [github-issue-artifacts](skills/github-issue-artifacts/SKILL.md) | Create and update HTML artifacts (`embedded_html`) on GitHub Issues that actually render in GitHub's sandboxed preview: inline SVG icons, CSS-only theme toggles, paired light/dark colors with checked contrast, tables that stay readable in the narrow preview pane, and read-back verification through the API. GitHub's official `issue-artifacts` skill covers basic API access; this one covers the HTML authoring side it leaves out. |
| [temp-workspace-hygiene](skills/temp-workspace-hygiene/SKILL.md) | Keep agent scratch work from piling up untracked: separate homes for throwaway files (`~/agent-tmp`) and human-facing deliverables (`~/artifacts`), a manifest recording owner, purpose, and retention for everything created, safe end-of-task cleanup, and a two-stage lifecycle — expired or idle units move to `.trash` and are deleted 7 days later. Includes a reference pruner script. |
| [prune-merged-branches](skills/prune-merged-branches/SKILL.md) | Delete local branches whose GitHub PRs are merged — squash merges included, which `git branch --merged` cannot detect — together with their worktrees and remote branches. Dirty worktrees are moved to the agent-tmp trash instead of deleted, closed-but-unmerged PRs get strict local-only cleanup, and every destructive step re-verifies a state snapshot first. Dry-run by default. |

## Install

Copy the skill directory into the location your agent reads:

| Agent | Repository path | Personal path |
| --- | --- | --- |
| Claude Code | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` |
| Codex | `.agents/skills/<name>/` | `~/.agents/skills/<name>/` |
| GitHub Copilot CLI | `.github/skills/<name>/` | `~/.copilot/skills/<name>/` |
| GitHub Copilot in VS Code | `.github/skills/<name>/` | `~/.copilot/skills/<name>/` |

```bash
git clone https://github.com/Hyd3-14/skills.git
cp -r skills/skills/github-issue-artifacts ~/.claude/skills/
```

## License

MIT — see [LICENSE](LICENSE).

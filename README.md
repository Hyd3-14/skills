# skills

English | [日本語](README.ja.md)

Agent Skills I wrote from real work, published as open source.

Each skill lives in `skills/<name>/SKILL.md` and follows the [Agent Skills](https://agentskills.io) format, so it works across Claude Code, Codex, GitHub Copilot, and other compatible agents.

## Skills

| Skill | What it does |
| --- | --- |
| [github-issue-artifacts](skills/github-issue-artifacts/SKILL.md) | Create and update HTML artifacts (`embedded_html`) on GitHub Issues that actually render in GitHub's sandboxed preview: inline SVG icons, CSS-only theme toggles, paired light/dark colors with checked contrast, tables that stay readable in the narrow preview pane, and read-back verification through the API. GitHub's official `issue-artifacts` skill covers basic API access; this one covers the HTML authoring side it leaves out. |

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

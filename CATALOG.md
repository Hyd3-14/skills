# Catalog

English | [日本語](CATALOG.ja.md)

Every skill in this repository, written for people seeing it for the first time: the problem each one solves, what it actually does, and when to reach for it. The short index is in the [README](README.md).

---

## github-issue-artifacts

Attach an HTML summary to a GitHub Issue so it renders in place — diagrams and all — instead of burying it in a comment.

**The problem.** GitHub Issue Artifacts (public preview) can render an HTML document right next to an issue, which makes it the best place for an investigation summary or a decision brief. But the preview is a sandboxed iframe: scripts may not run, icon libraries that swap in SVGs at runtime show nothing, a JavaScript theme toggle silently does nothing, and a table that looks fine on a wide screen can collapse in the narrow preview pane — one character per line. GitHub's official `issue-artifacts` skill covers basic API access and does not touch any of this.

**What it does.** A field guide to authoring `embedded_html` artifacts that survive the preview: inline SVG icons instead of runtime icon libraries, CSS-only toggles via `:has()`, light/dark color pairs defined per filled element with contrast ratios checked to at least 4.5:1, tables that stay readable at 390px, and an API workflow that updates artifacts in place with PATCH and verifies the result by reading it back.

**When to use it.** Whenever you save a summary, report, plan, or diagram-heavy write-up to a GitHub Issue — or when an existing HTML artifact renders broken in the preview.

**Requirements.** GitHub CLI (`gh`). The dedicated artifact commands need 2.103.0+; the skill includes the REST route for older versions.

→ [skills/github-issue-artifacts/SKILL.md](skills/github-issue-artifacts/SKILL.md)

---

## temp-workspace-hygiene

Stop agent scratch work from piling up in `/tmp` and your home directory with no record of what it is or when it can go.

**The problem.** Agents create temporary files constantly — scratch clones, caches, verification output, drafts. They scatter across `/tmp` and `~` with names that say nothing about who made them, why, or whether deleting them is safe. Cleanup becomes archaeology, so nobody cleans up.

**What it does.** A discipline plus a small pruner script. Two homes with the same layout: `~/agent-tmp/<host>/<owner>/<repo>/<date>-<task>/` for throwaway work, `~/artifacts/…` for deliverables a human will review. `/tmp` work gets one session root and a `manifest.tsv` recording kind, path, purpose, owner, retention, and status for everything created. Scratch units declare `expires=YYYY-MM-DD` in a `MANIFEST`; the pruner moves expired units — and units idle for 7 days — into `.trash`, and deletes them 7 days later, so every deletion is reversible for a week. Deleting anything requires five conditions to hold at once (yours, unused, clean, unneeded, retention met).

**When to use it.** When setting up how an agent should handle temporary files, when a scratch tree has already become a pile, or when you want cleanup to be a routine instead of an excavation.

**Requirements.** Python 3 for the pruner script (Linux; its in-use check reads `/proc`).

→ [skills/temp-workspace-hygiene/SKILL.md](skills/temp-workspace-hygiene/SKILL.md)

---

## prune-merged-branches

Delete local branches whose pull requests are merged — squash merges included — without ever deleting a branch that still matters.

**The problem.** `git branch --merged` cannot see squash merges, so finished branches pile up. The common workaround, force-deleting branches that look merged, is how an unmerged branch with real work gets eaten. Worktrees make it worse: a merged branch's worktree may still hold uncommitted files you cannot afford to lose.

**What it does.** A 900-line bash tool, `gprune-merged`, that decides from GitHub's PR state rather than git ancestry. A branch is a candidate only when its merged PR head contains it (exact SHA match, or ancestry for the squash case). Closed-but-unmerged PRs get local-only cleanup under a strict three-way SHA match, and their remote branches are never deleted. Clean worktrees are removed; dirty ones have their regenerable directories (`node_modules`, `dist`, …) dropped and the rest moved to the `~/agent-tmp/.trash` lifecycle. Before anything destructive happens, the tool re-reads PR states, worktree registrations, and local and remote OIDs and compares them with the snapshot it collected — any change aborts the run. Dry-run is the default.

**When to use it.** When merged branches and their worktrees pile up, especially in a squash-merge workflow with heavy worktree use.

**Requirements.** `git` and an authenticated `gh`. Optional: `gwq` for worktree removal (plain `git worktree remove` otherwise), `ghq` for the cross-repository `--all` sweep, `mise` for trust cleanup.

→ [skills/prune-merged-branches/SKILL.md](skills/prune-merged-branches/SKILL.md)

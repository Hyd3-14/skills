---
name: temp-workspace-hygiene
description: Keep temporary files created during agent work from piling up untracked — fixed homes for scratch work vs deliverables, a manifest recording owner, purpose, and retention for everything created, safe end-of-task cleanup, and a two-stage trash lifecycle (expired or idle units move to .trash, then are deleted 7 days later) run by a small pruner script. Use when creating scratch directories, verification clones, caches, or work artifacts in /tmp or a home scratch tree, when cleaning them up, or when setting up the lifecycle for a scratch tree.
---

# Temp workspace hygiene

Agents create temporary files constantly: scratch clones, caches, verification output, draft notes. Left unmanaged, they scatter across `/tmp` and the home directory with names that say nothing about who made them, why, or when they can go. This skill ties every temporary path to a unit of work, an owner, a reason to keep it, and a deletion condition — and gives the scratch tree a lifecycle, so cleanup is a routine instead of an excavation.

## Two homes: scratch vs deliverables

Keep two trees, both laid out by repository so related work is findable:

- **Scratch** — `~/agent-tmp/<host>/<owner>/<repo>/<YYYYMMDD>-<task>/`. Drafts, investigation notes, verification output: anything created for the work itself and safe to lose. This tree is pruned automatically (below).
- **Deliverables** — `~/artifacts/<host>/<owner>/<repo>/<YYYYMMDD>-<task>/`. Output a human will review: reports, screenshots, files attached to a PR. This tree is **not** pruned.

The `<host>/<owner>/<repo>` part mirrors how repository managers (ghq and similar) lay out clones, e.g. `github.com/you/project`. For work not tied to a repository, use a descriptive top-level name instead.

Rules that apply to both trees:

- Never put per-task directories at the repository root (`./.tmp/`, `./.artifacts/`). Formatters, linters, and CSS tooling that ignore `.gitignore` will walk them and can stall on symlinks pointing outside the repository.
- Never start an agent session *at* the root of either tree. Some sandboxes materialize protected empty directories (`.git`, `.aws`, tool config dirs) in the session's working directory; start inside a per-task directory instead.
- At the end of a task, promote only what a PR, review, or reproduction actually needs from scratch into deliverables (or into the repository), and record the move.

## /tmp work: one session root, one manifest

Worktrees belong under your worktree manager, not in `/tmp`. When a tool constraint forces `/tmp`, use exactly one session root and track everything in it:

```bash
session_root="$(mktemp -d "/tmp/agent-work/$(date +%Y%m%d-%H%M%S)-XXXXXX")"
mkdir -p "$session_root"/{worktrees,caches,artifacts,logs}
printf 'kind\tpath\tpurpose\towner\tcreated_at\tretention\tstatus\n' > "$session_root/manifest.tsv"
```

- `kind` is one of `worktree`, `cache`, `artifact`, `log`, `other`; `path` is absolute; `created_at` is ISO 8601.
- `owner` for agent-created paths is the session id (the session root's name).
- `retention` is one of `until-end`, `until-pr-review`, `until-date:YYYY-MM-DD`, `keep`.
- `status` is one of `active`, `moved`, `kept`, `deleted`, `blocked`.
- Add a row the moment you create a path, not at cleanup time. Never record secrets or tokens in the manifest.

## Boundaries while working

- Files you create explicitly stay inside the session root, or in the two trees above. Nothing else gets improvised locations.
- When a tool generates its own temp paths, point it at the session root if it accepts one; otherwise record the paths it reports in the manifest.
- Never copy credentials, tokens, session data, or personal logs into temporary artifacts. Record verification results in a form that excludes secrets.
- System runtime areas of `/tmp` (sockets, `systemd-private-*`, SSH agent files, anything whose owner you cannot identify) are not work space. Do not touch them.
- Measuring, moving, or deleting trees that may contain symlinks pointing outside (tool state dirs are prone to this) must not follow symlinks: `du -P`, `cp -P`, and explicit target checks before `rm -r`.
- Never delete a path that is dirty, in use, or of unknown ownership. Check branch, processes, related PRs, and the recorded retention first.

## Closing a task: the inventory

1. Check `git status`, `git worktree list`, and which processes are using the paths (`lsof +D <path>` or equivalent). If you cannot confirm a path is unused, leave it.
2. Promote deliverables (above) and record the moves in the manifest.
3. Delete only paths that meet **all five** conditions:
   - your session created it,
   - no process is using it,
   - no uncommitted changes and no unpushed commits,
   - it is not needed for a PR, review, or recovery,
   - its recorded retention or end condition is met.
4. Leave everything else in place and report it with the reason.
5. Reconcile: surviving paths match the manifest, deleted paths are marked `deleted`. If nothing survives, remove the manifest and session root too; if something survives, keep the manifest and report the survivors as `kept` or `blocked`.
6. Never bulk-delete `/tmp` or anything outside your session root. A session root with no manifest is not yours to judge — report it, don't remove it.

## The lifecycle: two-stage trash for the scratch tree

Scratch units under `~/agent-tmp/` carry their retention in a `MANIFEST` (or `MANIFEST.md`) file inside the unit, as a single line:

```
expires=2027-01-31
```

A pruner — `scripts/agent-tmp-prune.py` in this skill is a reference implementation — runs daily (a systemd user timer or cron) and applies these rules per unit (a unit is one `<host>/<owner>/<repo>/<task>` directory, or a non-host entry directly under `~/agent-tmp/`):

| Unit state | Action |
| --- | --- |
| `expires=` date has passed | move to `.trash` |
| `expires=` date is in the future | keep, regardless of age |
| no `expires=` line, and nothing inside modified for 7 days | move to `.trash` |
| a process has its cwd or an open file inside | keep, and report as in use |

Moved units land in `~/agent-tmp/.trash/<YYYYMMDD>/<original path>`. Date directories in `.trash` are deleted once they are 7 days old, so every deletion is reversible for a week: restore by moving the unit back (and give it an `expires=` line, or it will be moved again). Run the pruner daily, not weekly — a weekly run can add up to 7 days of delay to both stages. Default to `--dry-run`; the script changes nothing without `--apply`.

To keep something long-term, write a future `expires=` date. To keep it forever, move it out of the scratch tree — permanence by neglect is how the pile forms.

## Resuming after an interruption

If a previous session root or scratch unit survives, start by reading its manifest, ownership, Git state, and process use. Anything whose records and reality disagree, or whose retention cannot be determined, is held — never deleted on a guess.

---
name: prune-merged-branches
description: Safely delete local branches whose GitHub pull requests are merged — including squash merges that `git branch --merged` cannot detect — together with their worktrees and remote branches. Dirty worktrees are moved to the agent-tmp trash instead of being deleted, and every destructive step re-verifies a state snapshot first. Use when merged branches and their worktrees pile up, when cleaning up after a merged PR, or when a cleanup script based on git ancestry alone would miss squash merges or delete too much.
---

# Prune merged branches

`git branch --merged` cannot see squash merges: the branch's commits never become ancestors of the base branch, so finished branches pile up — and the usual fix, force-deleting anything that "looks merged", eventually eats a branch that was never merged at all. The bundled script, `scripts/gprune-merged`, decides from the source of truth instead: **GitHub's pull request state**, fetched through `gh`.

## What it does

For every local branch (except the current one and `main` / `master` / `production`), the script looks up the branch's pull requests and classifies it:

- **Merged PR** → cleanup candidate. The local branch must be *contained* in the merged PR head: an exact head-SHA match, or the local branch is an ancestor of the PR head (the squash-merge case, where later commits exist only on the PR side). A local branch with commits the PR head does not contain is skipped.
- **Closed without merging** → local cleanup only, and only when the PR head, the local branch, and the origin branch all point at the same commit. The remote branch is **never** deleted for an unmerged PR.
- **Open PR, or no PR** → skipped.

For each candidate it also handles:

- **Worktrees.** A clean worktree is removed. A worktree with uncommitted changes or ignored files is not deleted: regenerable directories (`node_modules`, `dist`, `build`, … — extendable per repository via `git config --add gprune.disposable <name>`) are removed, and everything else is moved to `~/agent-tmp/.trash/<date>/worktrees/…`, where the [temp-workspace-hygiene](../temp-workspace-hygiene/SKILL.md) lifecycle deletes it after 7 days. The main worktree is never trashed, and a worktree a process is currently using is skipped.
- **Remote branches.** Deleted in one push per remote, each ref pinned with `--force-with-lease` to the OID observed during checks. If a remote branch cannot be deleted, its local branch is kept too. A remote branch that moved past the PR head, or whose name differs from the PR branch, is never deleted.

## The safety model

Deletion is the last step, not the first:

1. **Dry-run by default.** Nothing changes without `--apply`.
2. **Snapshot, then re-verify.** Candidates are collected with their PR states, worktree registrations, local OIDs, and remote OIDs (read from the remote itself via `ls-remote`, not from tracking refs). Immediately before the destructive phase — and again before the local branch deletion — everything is re-read and compared. Any change aborts the run instead of deleting on stale information.
3. **Trash before delete.** Anything with content that might matter goes to `.trash` first and becomes recoverable for 7 days.
4. **Fail closed.** When a PR head commit cannot be fetched, a remote OID cannot be verified, or a worktree's state cannot be checked, the branch is skipped with the reason printed.

## Usage

```bash
# Inside a repository: show candidates only
gprune-merged

# Delete the candidates that pass every check
gprune-merged --apply

# Skip the initial `git fetch --prune` (e.g. when a wrapper already fetched)
gprune-merged --no-fetch

# Dry-run across every repository managed by ghq
gprune-merged --all
```

## Requirements

- `git` and an authenticated `gh` (the PR lookups go through `gh api graphql`).
- Optional: `gwq` — when installed, worktree removal goes through it; otherwise plain `git worktree remove` is used.
- Optional: `ghq` — only for `--all`.
- Optional: `mise` — when installed, a worktree's mise trust entry is removed just before the worktree is deleted (after deletion it can no longer be untrusted by path).
- Environment: `GPRUNE_TRASH_ROOT` overrides the trash location (default `~/agent-tmp/.trash`); `GH_REPO` overrides repository detection.

Copy `scripts/gprune-merged` somewhere on your `PATH` and make it executable.

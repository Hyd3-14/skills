#!/usr/bin/env python3
"""Move expired or idle work units in ~/agent-tmp to .trash, and delete old .trash entries.

A unit is one <host>/<owner>/<repo>/<task> directory, or a non-host entry
directly under the root. A unit with an `expires=YYYY-MM-DD` line in its
MANIFEST (or MANIFEST.md) is trashed once that date has passed; a unit with
no expiry is trashed after 7 days without modification. Trashed units land
in <root>/.trash/<YYYYMMDD>/<original path> and are deleted 7 days later.
Units in use by a process are kept. Default mode is --dry-run.
"""
import argparse
from datetime import date, datetime
import os
from pathlib import Path
import re
import shutil
import stat
import sys

IDLE_DAYS = 7
TRASH_DAYS = 7
TRASH = ".trash"
SKIP_TOP = {TRASH}
EXPIRES = re.compile(r"^expires=(\d{4}-\d{2}-\d{2})\s*$", re.M)
# Require an alphabetic TLD so names like `extract-1.2` are not mistaken for
# hosts, and exclude bare clones via their HEAD file.
HOST = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}$")


def real_dirs(path):
    return sorted(p for p in path.iterdir() if p.is_dir() and not p.is_symlink())


def is_host(path):
    # Files sitting in the host/owner layers are not units; never move a
    # whole host tree as one unit.
    return bool(HOST.match(path.name)) and path.is_dir() and not path.is_symlink() and not (path / "HEAD").exists()


def units(root):
    """Yield work units: <host>/<owner>/<repo>/<task>, plus non-host entries
    directly under root. Symlinks in the owner/repo layers are not followed."""
    for top in sorted(root.iterdir()):
        if top.name in SKIP_TOP:
            continue
        if is_host(top):
            for owner in real_dirs(top):
                for repo in real_dirs(owner):
                    yield from sorted(repo.iterdir())
        else:
            yield top


def expires(path):
    for name in ("MANIFEST", "MANIFEST.md"):
        f = path / name
        if path.is_dir() and not path.is_symlink() and f.is_file():
            m = EXPIRES.search(f.read_text(errors="replace"))
            if m:
                return date.fromisoformat(m.group(1))
    return None


def last_modified(path):
    newest = path.lstat().st_mtime
    if path.is_dir() and not path.is_symlink():
        for d, dirs, files in os.walk(path):
            for n in dirs + files:
                try:
                    newest = max(newest, os.lstat(os.path.join(d, n)).st_mtime)
                except FileNotFoundError:
                    pass
    return datetime.fromtimestamp(newest)


def paths_in_use():
    """Process cwds and open files. Processes whose /proc entries cannot be
    read (other users') are ignored."""
    used = []
    for pid in Path("/proc").glob("[0-9]*"):
        links = [pid / "cwd"]
        try:
            links += list((pid / "fd").iterdir())
        except OSError:
            pass
        for link in links:
            try:
                used.append(os.readlink(link))
            except OSError:
                pass
    return used


def in_use(path, used):
    p = str(path)
    return any(u == p or u.startswith(p + "/") for u in used)


def remove(path):
    # Read-only directories (Go module caches and the like) make rmtree fail;
    # restore write permission first.
    if path.is_dir() and not path.is_symlink():
        for d, dirs, _ in os.walk(path):
            for n in dirs:
                q = os.path.join(d, n)
                if not os.path.islink(q):
                    os.chmod(q, os.lstat(q).st_mode | stat.S_IRWXU)
        os.chmod(path, path.lstat().st_mode | stat.S_IRWXU)
        shutil.rmtree(path)
    else:
        path.unlink()


def plan(root, now, used):
    actions = []
    today = now.date()
    for u in units(root):
        rel = u.relative_to(root)
        exp = expires(u)
        if exp is not None:
            reason = f"expires={exp}" if exp < today else None
        else:
            age = (now - last_modified(u)).days
            reason = f"no expiry set, untouched for {age} days" if age >= IDLE_DAYS else None
        if reason is None:
            continue
        if in_use(u, used):
            actions.append(("keep", rel, f"{reason}, but in use"))
        else:
            actions.append(("trash", rel, reason))
    trash = root / TRASH
    if trash.is_dir():
        for day in sorted(trash.iterdir()):
            try:
                moved = datetime.strptime(day.name, "%Y%m%d").date()
            except ValueError:
                actions.append(("keep", day.relative_to(root), "non-date name directly under .trash"))
                continue
            if (today - moved).days >= TRASH_DAYS:
                actions.append(("delete", day.relative_to(root), f"moved to .trash on {moved}"))
    return actions


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.home() / "agent-tmp")
    parser.add_argument("--now", type=datetime.fromisoformat, default=None, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    now = args.now or datetime.now()
    used = paths_in_use()
    day = now.strftime("%Y%m%d")
    root = args.root.resolve()
    if not root.is_dir():
        print(f"[agent-tmp-prune] {root} does not exist; nothing to do")
        return 0
    # (kind, source, reason, destination when trashing)
    jobs = [(kind, root / rel, reason, root / TRASH / day / rel) for kind, rel, reason in plan(root, now, used)]
    failed = 0
    for kind, src, reason, dest in jobs:
        print(f"[{kind}] {src.relative_to(root)} ({reason})")
        if not args.apply or kind == "keep":
            continue
        try:
            if kind == "trash":
                if dest.exists() or dest.is_symlink():
                    raise FileExistsError(dest)
                dest.parent.mkdir(parents=True, exist_ok=True)
                if src.is_dir() and not src.is_symlink():
                    # Moving across directories rewrites `..`, so a read-only
                    # directory needs its write bit back first.
                    os.chmod(src, src.lstat().st_mode | stat.S_IWUSR)
                os.rename(src, dest)
            else:
                remove(src)
        except OSError as e:
            failed += 1
            print(f"[error] {src}: {e}", file=sys.stderr)
    if not args.apply:
        print("[DRY-RUN] nothing was moved or deleted")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

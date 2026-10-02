#!/usr/bin/env python3
"""What has been done to this repo, read from git itself -- not from any model's account of it.

    python3 tools/repo_status.py          # last 10 commits
    python3 tools/repo_status.py 30

Prints: current branch; whether it is ahead of / behind its remote copy;
which branch commits went to (main or not); the last N commits with author,
time and files touched; uncommitted changes. Run `git fetch` first to compare
against the latest remote state. Plain Python 3, no packages; runs on Termux.
"""
import subprocess
import sys


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    n = int(argv[0]) if argv else 10
    if git("rev-parse", "--git-dir") is None:
        print("not inside a git repository")
        return 2
    branch = git("branch", "--show-current") or "(detached)"
    print(f"branch:   {branch}")
    up = git("rev-parse", "--abbrev-ref", "@{u}")
    if up:
        ahead, behind = (git("rev-list", "--left-right", "--count", f"HEAD...{up}") or "0 0").split()
        print(f"remote:   {up}  ({ahead} local commits not pushed, {behind} remote commits not pulled)")
    else:
        print("remote:   no upstream set; nothing on this branch is known to be pushed")
    main_ref = next((r for r in ("origin/main", "main") if git("rev-parse", "--verify", "-q", r)), None)
    if main_ref and branch != "main":
        k = git("rev-list", "--count", f"{main_ref}..HEAD")
        print(f"vs main:  {k} commits on {branch} that are not in {main_ref}")
    dirty = git("status", "--short")
    print("uncommitted: " + ("none" if not dirty else f"{len(dirty.splitlines())} files"))
    if dirty:
        print("  " + dirty.replace("\n", "\n  "))
    print(f"\nlast {n} commits:")
    log = git("log", f"-{n}", "--date=format-local:%Y-%m-%d %H:%M UTC",
              "--pretty=format:@@%h  %ad  author: %an <%ae>  committer: %cn <%ce>%n    %s", "--name-only") or ""
    for line in log.splitlines():
        print(line[2:] if line.startswith("@@") else ("      " + line if line and not line.startswith("    ") else line))
    return 0


if __name__ == "__main__":
    sys.exit(main())

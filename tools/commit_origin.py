#!/usr/bin/env python3
"""Sort every commit on a branch by who made it, from what git records.

    python3 tools/commit_origin.py              # all-work, summary
    python3 tools/commit_origin.py --list       # also one line per commit

Classes, decided in this order:
  claude-name      author or committer is Claude <noreply@anthropic.com>
  claude-tagged    owner's name, but the message carries a Claude-Session or
                   claude.ai/code/session line -- made in a Claude session
  claude-window    owner's name (Michael Song <red3rdeye@gmail.com>), no tag,
                   after 2026-09-22 16:36:49 UTC: the session container's
                   .git/config set that name, so Claude sessions committed
                   under it. Inferred from that config, not from a tag.
  github           committed through GitHub itself (web edits, PR merges)
  owner-or-unknown everything else: the owner's own name with no marker before
                   that date. Git alone cannot say who made these.
"""
import subprocess
import sys

CUT = "2026-09-22T16:36:49+00:00"


def commits(ref):
    out = subprocess.run(["git", "log", ref, "--format=%h%x1f%an%x1f%ae%x1f%cn%x1f%ce%x1f%cI%x1f%s%x1f%B%x1e"],
                         capture_output=True, text=True, check=True).stdout
    for rec in out.split("\x1e"):
        f = rec.strip("\n").split("\x1f")
        if len(f) == 8:
            yield dict(zip(("h", "an", "ae", "cn", "ce", "date", "subj", "body"), f))


def classify(c, cut=CUT):
    if "noreply@anthropic.com" in (c["ae"].lower(), c["ce"].lower()):
        return "claude-name"
    if "Claude-Session:" in c["body"] or "claude.ai/code/session" in c["body"]:
        return "claude-tagged"
    if c["ce"].lower() == "noreply@github.com":
        return "github"
    from datetime import datetime
    if c["an"] == "Michael Song" and datetime.fromisoformat(c["date"]) > datetime.fromisoformat(cut):
        return "claude-window"
    return "owner-or-unknown"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    ref = next((a for a in argv if not a.startswith("-")), "all-work")
    rows = [(classify(c), c) for c in commits(ref)]
    counts = {}
    for k, _ in rows:
        counts[k] = counts.get(k, 0) + 1
    print(f"{ref}: {len(rows)} commits")
    for k in ("claude-name", "claude-tagged", "claude-window", "github", "owner-or-unknown"):
        print(f"  {k:17s} {counts.get(k, 0)}")
    if "--list" in argv:
        for k, c in rows:
            print(f"{c['h']}  {c['date'][:16]}  {k:17s} {c['an']:14s} {c['subj'][:90]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

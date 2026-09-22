"""
theorem_index.py -- one index across every branch.

The repository's failure mode is not loss. Nothing has ever been deleted:
`git fsck` reports no dangling blobs and a deleted-path search across all
branches returns empty. The failure is DISCOVERY. A file written as T237
is renumbered to T374 and the old number now points at something else;
work lands on a branch that never merges, so the next session cannot see
it; `main` is frozen, so a fresh clone shows none of it.

This walks every branch tip, extracts every theorem number it can find,
and reports four things:

  INVENTORY    every theorem file, its number, title, and which branches
               carry it
  RENUMBERED   files that record having moved from one number to another,
               so the old number is searchable
  COLLISIONS   one number claimed by two or more different files
  ORPHANS      files present on some branch but absent from main

Run:  python3 tools/theorem_index.py [--write INDEX_ALL.md]
"""

import re
import subprocess
import sys
from collections import defaultdict


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True,
                          text=True, errors="replace").stdout


def branches():
    out = []
    for line in git("for-each-ref", "--format=%(refname:short)",
                    "refs/heads/scan/").splitlines():
        line = line.strip()
        if line:
            out.append(line)
    return out or ["HEAD"]


NUM_IN_NAME = re.compile(r"theorem[_-]?(\d+)", re.I)
NUM_IN_BODY = re.compile(r"^\s*(?:#\s*)?(?:THEOREM|Theorem)\s+(\d+)\s*[:\-]", re.M)
TITLE = re.compile(r"^\s*(?:#\s*)?(?:THEOREM|Theorem)\s+\d+\s*[:\-]\s*(.+)$", re.M)
RENUM = re.compile(r"RENUMBERED[^\n]*?from\s+T?(\d+)", re.I)
CLASS = re.compile(r"^#\s*CLASS:\s*(\w+)", re.M)


def scan():
    files = defaultdict(set)            # path -> {branches}
    for b in branches():
        for path in git("ls-tree", "-r", "--name-only", b).splitlines():
            if path.endswith((".py", ".md")) and (
                    "theorem" in path.lower() or path.startswith("math/")):
                files[path].add(b.replace("scan/", ""))

    records = []
    for path, brs in sorted(files.items()):
        ref = sorted(brs)[0]
        body = git("show", f"scan/{ref}:{path}")
        if not body:
            continue
        head = body[:4000]
        nums = set(int(n) for n in NUM_IN_NAME.findall(path))
        nums |= set(int(n) for n in NUM_IN_BODY.findall(head))
        if not nums:
            continue
        t = TITLE.search(head)
        c = CLASS.search(head)
        r = RENUM.search(head)
        records.append({
            "path": path,
            "numbers": sorted(nums),
            "title": (t.group(1).strip() if t else "")[:78],
            "klass": c.group(1) if c else "",
            "renumbered_from": int(r.group(1)) if r else None,
            "branches": sorted(brs),
        })
    return records


def report(records, out=sys.stdout):
    by_num = defaultdict(list)
    for r in records:
        for n in r["numbers"]:
            by_num[n].append(r)

    p = lambda *a: print(*a, file=out)
    p("# Theorem index — all branches\n")
    p(f"{len(records)} numbered files, {len(by_num)} distinct numbers, "
      f"across {len(branches())} branches.\n")

    renum = [r for r in records if r["renumbered_from"] is not None]
    p(f"## Renumbered ({len(renum)})\n")
    p("The old number is what you would search for and would not find.\n")
    if renum:
        p("| looked-for | now | file |")
        p("|---|---|---|")
        for r in sorted(renum, key=lambda x: x["renumbered_from"]):
            p(f"| T{r['renumbered_from']} | T{r['numbers'][0]} | `{r['path']}` |")
    p("")

    coll = {n: rs for n, rs in by_num.items() if len({x["path"] for x in rs}) > 1}
    p(f"## Collisions ({len(coll)})\n")
    p("One number, more than one file. Searching the number finds the wrong one.\n")
    if coll:
        for n in sorted(coll):
            p(f"- **T{n}**")
            for r in coll[n]:
                p(f"  - `{r['path']}`")
    p("")

    main_files = {r["path"] for r in records if "main" in r["branches"]}
    orphans = [r for r in records if r["path"] not in main_files]
    p(f"## Not on main ({len(orphans)} of {len(records)})\n")
    p("Invisible to a fresh clone.\n")
    p("| T | file | branches |")
    p("|---|---|---|")
    for r in sorted(orphans, key=lambda x: x["numbers"][0]):
        bs = ", ".join(b.replace("claude/", "") for b in r["branches"][:2])
        p(f"| {r['numbers'][0]} | `{r['path']}` | {bs} |")
    p("")

    p(f"## Full inventory ({len(records)})\n")
    p("| T | title | file |")
    p("|---|---|---|")
    for r in sorted(records, key=lambda x: x["numbers"][0]):
        p(f"| {r['numbers'][0]} | {r['title'] or '—'} | `{r['path']}` |")


if __name__ == "__main__":
    recs = scan()
    if "--write" in sys.argv:
        dest = sys.argv[sys.argv.index("--write") + 1]
        with open(dest, "w") as f:
            report(recs, f)
        print(f"wrote {dest}: {len(recs)} numbered files")
    else:
        report(recs)

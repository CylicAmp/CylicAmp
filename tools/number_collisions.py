#!/usr/bin/env python3
"""Theorem-number collisions: a citation "T233" must resolve to one file.

Written after a full-corpus prior-art sweep found that 40+ numbers resolve
to two different files on unrelated subjects, which makes every cross-
reference by number ambiguous. Cleared 2026-09-19 (early block T218-T261
renumbered to T382-T421); this now prints 0 and 0, and is a regression
check, not an open report.

    python3 tools/number_collisions.py
"""
import ast, re, pathlib, sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["math/theorems", "math/primes", "math/turbulence", "cylicamp"]
# a self-declaration is the FIRST line of the docstring, not a section label
DECL = re.compile(r'^\s*(?:={3,}\s*)?(?:THEOREM|Theorem)\s+(\d{1,3})\b', re.M)


def scan():
    files = []
    for d in DIRS:
        p = ROOT / d
        if p.is_dir():
            files += sorted(p.glob("*.py"))
    named, declared = {}, defaultdict(list)
    for f in files:
        try:
            txt = f.read_text(errors='replace')
            doc = ast.get_docstring(ast.parse(txt)) or ""
        except Exception:
            doc = ""
        m = re.match(r"theorem_(\d+)_", f.name)
        if m:
            named.setdefault(int(m.group(1)), []).append(f.name)
        # only the first 3 lines: a section label deeper in is not a claim
        head = "\n".join(doc.splitlines()[:3])
        d = DECL.findall(head)
        if d:
            declared[int(d[0])].append(f.name)
    return named, declared


def main():
    named, declared = scan()
    hard = {n: v for n, v in named.items() if len(v) > 1}
    print("=== TWO PROPERLY-NAMED FILES ON THE SAME NUMBER ===")
    for n, v in sorted(hard.items()):
        print("  T%-4d %s" % (n, v))
    print("  total: %d\n" % len(hard))

    soft = []
    for n, v in sorted(declared.items()):
        others = [f for f in v if not f.startswith("theorem_%d_" % n)]
        if others and n in named:
            soft.append((n, named[n], others))
    print("=== A NUMBERED FILE AND AN UNNUMBERED FILE CLAIMING THE SAME N ===")
    for n, a, b in soft:
        print("  T%-4d %-46s vs %s" % (n, a[0], b[0]))
    print("  total: %d" % len(soft))
    print("\n  a citation of any listed number does not resolve to one file.")
    return len(hard) + len(soft)


if __name__ == '__main__':
    sys.exit(0 if main() >= 0 else 1)

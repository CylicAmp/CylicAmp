#!/usr/bin/env python3
"""
Detect syntactically redundant assertions in math/theorems/.

  D1  exact duplicate assertions within one scope
  D2  tautologies: assert X == (the exact source X was assigned)
  D3  conjunct subsumption: assert A, then later assert A and B

All three mean the check could not have been red, so it is not evidence.

NOT DETECTED: semantic entailment between sibling checks -- the T316 case,
where `m2*s == seed%37` already forces the two orbit checks and the DR check.
That needs a parameter to sweep and is not reachable by static analysis.
See notes/theorem_corpus_audit.md.

Usage:  python3 tools/redundancy_audit.py [--json OUT.json]
"""
import argparse
import ast
import collections
import glob
import json
import os
import sys

D = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "math", "theorems")) + os.sep


def norm(node):
    try:
        return ast.unparse(node)
    except Exception:
        return None


def scan(files):
    dup, tauto, subsume = [], [], []
    for path in files:
        name = os.path.basename(path)
        try:
            tree = ast.parse(open(path).read())
        except Exception:
            continue
        scopes = [tree] + [n for n in ast.walk(tree)
                           if isinstance(n, ast.FunctionDef)]
        for scope in scopes:
            assigned, seen = {}, {}
            for stmt in getattr(scope, "body", []):
                if isinstance(stmt, ast.Assign):
                    rhs = norm(stmt.value)
                    for t in stmt.targets:
                        if isinstance(t, ast.Name):
                            assigned[t.id] = rhs
                        elif isinstance(t, ast.Tuple):
                            for e in t.elts:
                                if isinstance(e, ast.Name):
                                    assigned[e.id] = None
                elif isinstance(stmt, ast.Assert):
                    s = norm(stmt.test)
                    if s is None:
                        continue
                    if s in seen:
                        dup.append((name, stmt.lineno, seen[s], s[:70]))
                    else:
                        seen[s] = stmt.lineno
                    t = stmt.test
                    if (isinstance(t, ast.Compare) and len(t.ops) == 1
                            and isinstance(t.ops[0], ast.Eq)):
                        l, r = norm(t.left), norm(t.comparators[0])
                        for a, b in ((l, r), (r, l)):
                            if assigned.get(a) is not None and assigned[a] == b:
                                tauto.append((name, stmt.lineno,
                                              f"{a} = {b}  then  assert {s[:52]}"))
                                break
                    if isinstance(t, ast.BoolOp) and isinstance(t.op, ast.And):
                        for v in t.values:
                            vs = norm(v)
                            if vs in seen and seen[vs] != stmt.lineno:
                                subsume.append((name, seen[vs], stmt.lineno,
                                                vs[:60]))
    return dup, tauto, subsume


def report(files, dup, tauto, subsume):
    total = 0
    for path in files:
        try:
            total += sum(1 for n in ast.walk(ast.parse(open(path).read()))
                         if isinstance(n, ast.Assert))
        except Exception:
            pass
    n = len(dup) + len(tauto) + len(subsume)
    print(f"scanned {len(files)} files, {total} assertions\n")
    print(f"D1  exact duplicate assertions (same scope)        : {len(dup):>5}")
    print(f"D2  tautologies: assert X == (X's own RHS)         : {len(tauto):>5}")
    print(f"D3  conjunct subsumption (assert A; assert A and B): {len(subsume):>5}")
    if total:
        print(f"\n    {n} of {total} = {100*n/total:.1f}% could not have been red")
    for label, rows in (("D1 duplicates", dup), ("D2 tautologies", tauto),
                        ("D3 subsumed", subsume)):
        if not rows:
            continue
        by = collections.Counter(r[0] for r in rows)
        print(f"\n=== {label}: top files ===")
        for f, c in by.most_common(8):
            print(f"  {c:>4}  {f}")
        print("  examples:")
        for r in rows[:4]:
            print(f"    {r[0]}:{r[1]}  {r[-1]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="also write raw findings here")
    a = ap.parse_args()
    files = sorted(glob.glob(D + "*.py"))
    dup, tauto, subsume = scan(files)
    if a.json:
        json.dump(dict(dup=dup, tauto=tauto, subsume=subsume),
                  open(a.json, "w"))
    try:
        report(files, dup, tauto, subsume)
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        os._exit(0)


if __name__ == "__main__":
    main()

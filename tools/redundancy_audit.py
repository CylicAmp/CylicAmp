#!/usr/bin/env python3
"""Detect syntactically redundant assertions in math/theorems/.

D1 exact duplicates in one scope; D2 tautologies (assert X == X's own RHS);
D3 conjunct subsumption (assert A, later assert A and B). All three mean the
check could not have been red.

Does NOT detect semantic entailment between sibling checks -- the T316 case.
That needs a parameter to sweep and is not reachable statically.
"""
import ast, glob, os, json, collections

D = "/home/user/CylicAmp/math/theorems/"
files = sorted(glob.glob(D + "*.py"))

def norm(node):
    try: return ast.unparse(node)
    except Exception: return None

dup_rows, tauto_rows, subsume_rows = [], [], []

for path in files:
    name = os.path.basename(path)
    try: tree = ast.parse(open(path).read())
    except Exception: continue

    # walk function bodies and module body, tracking assignments in order
    for scope in [tree] + [n for n in ast.walk(tree)
                           if isinstance(n, (ast.FunctionDef,))]:
        body = getattr(scope, "body", [])
        assigned = {}          # varname -> source of RHS
        seen_tests = {}        # normalized test -> first lineno
        for stmt in body:
            if isinstance(stmt, ast.Assign):
                rhs = norm(stmt.value)
                for t in stmt.targets:
                    if isinstance(t, ast.Name): assigned[t.id] = rhs
                    elif isinstance(t, ast.Tuple):
                        for e in t.elts:
                            if isinstance(e, ast.Name): assigned[e.id] = None
            elif isinstance(stmt, ast.Assert):
                s = norm(stmt.test)
                if s is None: continue
                # D1 exact duplicate within scope
                if s in seen_tests:
                    dup_rows.append((name, stmt.lineno, seen_tests[s], s[:70]))
                else:
                    seen_tests[s] = stmt.lineno
                # D2 tautology: assert X == <exact source X was assigned>
                t = stmt.test
                if (isinstance(t, ast.Compare) and len(t.ops) == 1
                        and isinstance(t.ops[0], ast.Eq)):
                    l, r = norm(t.left), norm(t.comparators[0])
                    for a, b in ((l, r), (r, l)):
                        if a in assigned and assigned[a] is not None \
                           and assigned[a] == b:
                            tauto_rows.append((name, stmt.lineno,
                                               f"{a} = {b}  then  assert {s[:52]}"))
                            break
                # D3 conjunct subsumption: assert A, later assert A and B
                if isinstance(t, ast.BoolOp) and isinstance(t.op, ast.And):
                    for v in t.values:
                        vs = norm(v)
                        if vs in seen_tests and seen_tests[vs] != stmt.lineno:
                            subsume_rows.append((name, seen_tests[vs],
                                                 stmt.lineno, vs[:60]))

json.dump(dict(dup=dup_rows, tauto=tauto_rows, subsume=subsume_rows),
          open("/tmp/claude-0/-home-user-CylicAmp/98ad5857-685b-52cf-858d-0ceafb944d3b/scratchpad/redundancy.json","w"))

print(f"scanned {len(files)} files\n")
print(f"D1  exact duplicate assertions (same scope)   : {len(dup_rows):>5}")
print(f"D2  tautologies: assert X == (X's own RHS)    : {len(tauto_rows):>5}")
print(f"D3  conjunct subsumption (assert A; assert A and B): {len(subsume_rows):>5}")
for lbl, rows in (("D1 duplicates", dup_rows), ("D2 tautologies", tauto_rows),
                  ("D3 subsumed", subsume_rows)):
    if not rows: continue
    by = collections.Counter(r[0] for r in rows)
    print(f"\n=== {lbl}: top files ===")
    for f, n in by.most_common(8): print(f"  {n:>4}  {f}")
    print(f"  examples:")
    for r in rows[:5]: print(f"    {r[0]}:{r[1]}  {r[-1]}")

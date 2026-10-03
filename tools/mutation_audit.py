#!/usr/bin/env python3
"""
Mutation audit for math/theorems/ — which theorems actually depend on 37?

METHOD. A theorem claiming something about GF(37) should break if 37 is
replaced by another prime. Two passes:

  pass 1  rewrite the module-level `P = 37` to 43, then to 73
  pass 2  for files that survive pass 1, rewrite EVERY standalone literal 37

Classification, following the repo's forced-check taxonomy:

  fails 43 and 73          TIER C -- specific to 37
  fails 43, passes 73      TIER B -- the {7, 37, 73} family
  passes both              TIER A -- true for other primes; the 37 is decorative
  crashes                  inconclusive -- mutation broke it structurally

TWO FALSE-NEGATIVE MODES, both hit on the first run of this tool and both
corrected here; keep them in mind when reading output:

  1. A file can pass pass-1 simply because no assertion references `P` --
     it hardcodes the literal instead. Pass 2 exists for exactly this.
  2. A slow theorem looks like a failure under too short a timeout. Two
     files needed 29s and 65s. TIMEOUT is reported separately from ASSERT.

A PASS is the finding: it means the theorem's assertions hold for a prime
that is not 37, so 37 is not doing work in them.

Usage:  python3 tools/mutation_audit.py [--timeout SECONDS]
"""
import argparse, os, re, subprocess, sys, collections
from concurrent.futures import ProcessPoolExecutor

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                 "math", "theorems")
D = os.path.normpath(D) + os.sep
TIMEOUT = 150


def _run(path, timeout):
    try:
        r = subprocess.run([sys.executable, path], capture_output=True,
                           timeout=timeout)
        if r.returncode == 0:
            return "PASS"
        return "ASSERT" if b"AssertionError" in r.stderr[-600:] else "ERROR"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def _sites(src):
    """Every standalone integer literal 37, as (lineno, col, end_col), plus
    whether it sits in modulus position (RHS of %, or the modulus arg of pow).
    Positions come from the AST, so a 37 inside a string or a float is never
    a site."""
    import ast
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    modpos = set()
    for n in ast.walk(tree):
        c = None
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mod):
            c = n.right
        elif (isinstance(n, ast.Call) and getattr(n.func, "id", "") == "pow"
              and len(n.args) == 3):
            c = n.args[2]
        elif (isinstance(n, ast.Call) and getattr(n.func, "id", "") == "divmod"
              and len(n.args) == 2):
            c = n.args[1]
        if isinstance(c, ast.Constant) and c.value == 37:
            modpos.add((c.lineno, c.col_offset))
    out = []
    for n in ast.walk(tree):
        if (isinstance(n, ast.Constant) and n.value == 37
                and isinstance(n.value, int) and not isinstance(n.value, bool)):
            out.append((n.lineno, n.col_offset, n.end_col_offset,
                        (n.lineno, n.col_offset) in modpos))
    return sorted(set(out))


def _splice(src, site, newP):
    lines = src.split("\n")
    ln, c0, c1, _ = site
    line = lines[ln - 1]
    lines[ln - 1] = line[:c0] + str(newP) + line[c1:]
    return "\n".join(lines)


def _mutate(args):
    """mode 'P'    -> rewrite the module-level P = 37
       mode 'SITE' -> rewrite ONE literal 37, given as args[4]

    Per-site is what makes pass 2 trustworthy. A blanket rewrite of every 37
    cannot tell a field characteristic from an ordinary constant -- it broke
    theorem_272_easter_dates_gf37 by rewriting a 37 inside Gregorian date
    arithmetic, producing a crash that says nothing about 37-dependence.
    One site at a time keeps those separable."""
    name, newP, mode, timeout = args[:4]
    src = open(D + name).read()
    if mode == "P":
        mut = re.sub(r'^P = 37\s*$', f'P = {newP}', src, count=1, flags=re.M)
    else:
        mut = _splice(src, args[4], newP)
    tmp = D + f"_zzmut_{mode}{newP}_{os.getpid()}_{abs(hash(str(args[4:])))%99999}_{name}"
    open(tmp, "w").write(mut)
    try:
        return _run(tmp, timeout)
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass


def _literal_verdict(args):
    """Mutate each literal 37 alone. Verdict rules:
         any site -> ASSERT   => 37 is load-bearing (an assertion depends on it)
         no ASSERT, some PASS => those sites carry no assertion weight
         all sites -> crash   => structural dependence only, weak evidence
    Returns (verdict, detail)."""
    name, newP, timeout = args
    src = open(D + name).read()
    sites = _sites(src)
    if not sites:
        return ("NOSITES", "")
    res = [(_mutate((name, newP, "SITE", timeout, s)), s) for s in sites]
    kinds = [r for r, _ in res]
    nmod = sum(1 for s in sites if s[3])
    detail = (f"{len(sites)} sites ({nmod} in %/pow); "
              + " ".join(sorted({k for k in kinds})))
    if "ASSERT" in kinds:
        return ("ASSERT", detail)
    if "PASS" in kinds:
        return ("PASS", detail)
    return ("ERROR", detail)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=TIMEOUT)
    a = ap.parse_args()
    import ast
    cand = sorted(f for f in os.listdir(D)
                  if f.endswith(".py") and not f.startswith("_zz")
                  and re.search(r'^P = 37\s*$', open(D + f).read(), re.M))
    # A file with no assertions passes EVERY mutation trivially -- nothing in
    # it can fail. Counting those as "Tier A / 37 is decorative" is a false
    # positive; this was the tool's own first-run error. Excluded and reported.
    files, noassert = [], []
    for f in cand:
        try:
            n = sum(1 for x in ast.walk(ast.parse(open(D + f).read()))
                    if isinstance(x, ast.Assert))
        except Exception:
            n = 0
        (files if n else noassert).append(f)
    print(f"{len(cand)} theorem files define a module-level P = 37")
    if noassert:
        print(f"  {len(noassert)} excluded: NO ASSERTIONS, so no mutation can "
              f"fail them (not a finding)")
        for f in noassert:
            print(f"    {f}")
    print(f"  {len(files)} carry at least one assertion and are testable\n")
    with ProcessPoolExecutor(4) as ex:
        base = list(ex.map(_run, [D + f for f in files],
                           [a.timeout] * len(files)))
        live = [f for f, b in zip(files, base) if b == "PASS"]
        print(f"{len(live)} run clean at timeout={a.timeout}s "
              f"({len(files)-len(live)} did not -- see below)\n")
        r43 = list(ex.map(_mutate, [(f, 43, "P", a.timeout) for f in live]))
        r73 = list(ex.map(_mutate, [(f, 73, "P", a.timeout) for f in live]))
        surv = [f for f, x in zip(live, r43) if x == "PASS"]
        lit = list(ex.map(_literal_verdict, [(f, 43, a.timeout) for f in surv]))

    litmap = {f: v[0] for f, v in zip(surv, lit)}
    litdetail = {f: v[1] for f, v in zip(surv, lit)}
    tally = collections.Counter()
    decorative, inconclusive = [], []
    for f, x43, x73 in zip(live, r43, r73):
        if x43 != "PASS":
            if x43 == "ASSERT" and x73 == "PASS":
                tally["TIER B {7,37,73}"] += 1
            elif x43 in ("ASSERT",):
                tally["TIER C specific to 37"] += 1
            else:
                tally["inconclusive (crash on P-mutation)"] += 1
                inconclusive.append(f)
        else:
            L = litmap[f]
            if L == "ASSERT":
                tally["TIER C (caught only by literal mutation)"] += 1
            elif L == "PASS":
                tally["TIER A -- 37 IS DECORATIVE"] += 1
                decorative.append(f)
            elif L == "NOSITES":
                tally["TIER A -- no literal 37 to mutate either"] += 1
                decorative.append(f)
            else:
                tally["structural only (every site crashes)"] += 1
                inconclusive.append(f)

    print("RESULT")
    for k, v in tally.most_common():
        print(f"  {v:>4}  {k}")
    load = sum(v for k, v in tally.items() if k.startswith("TIER C")
               or k.startswith("TIER B"))
    print(f"\n  {load}/{len(live)} demonstrably depend on 37 "
          f"({100*load/max(len(live),1):.0f}%)")
    if decorative:
        print(f"\n  THE FINDING -- {len(decorative)} theorems whose assertions all")
        print(f"  still hold with every 37 replaced by 43:")
        for f in decorative:
            print(f"    {f}")
    if inconclusive:
        print(f"\n  structural only ({len(inconclusive)}): no single-site "
              f"mutation reaches an assertion -- the file cannot RUN at another")
        print(f"  prime because it indexes 37-derived tables. Weak evidence of")
        print(f"  dependence, not proof: a table merely BUILT from 37 crashes")
        print(f"  identically to one a claim rests on.")
        for f in inconclusive:
            d = litdetail.get(f, "")
            print(f"    {f}" + (f"   [{d}]" if d else ""))
    slow = [f for f, b in zip(files, base) if b != "PASS"]
    if slow:
        print(f"\n  did not complete at timeout={a.timeout}s "
              f"({len(slow)}) -- raise --timeout, do not assume broken:")
        for f in slow:
            print(f"    {f}")


if __name__ == "__main__":
    main()

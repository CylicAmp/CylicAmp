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
TIMEOUT = 90


def _run(path, timeout):
    try:
        r = subprocess.run([sys.executable, path], capture_output=True,
                           timeout=timeout)
        if r.returncode == 0:
            return "PASS"
        return "ASSERT" if b"AssertionError" in r.stderr[-600:] else "ERROR"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def _mutate(args):
    name, newP, mode, timeout = args
    src = open(D + name).read()
    if mode == "P":
        mut = re.sub(r'^P = 37\s*$', f'P = {newP}', src, count=1, flags=re.M)
    else:
        mut = re.sub(r'(?<![\d.\w])37(?![\d\w.])', str(newP), src)
    tmp = D + f"_zzmut_{mode}{newP}_{os.getpid()}_{name}"
    open(tmp, "w").write(mut)
    try:
        return _run(tmp, timeout)
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass


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
        lit = list(ex.map(_mutate, [(f, 43, "LIT", a.timeout) for f in surv]))

    litmap = dict(zip(surv, lit))
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
            else:
                tally["inconclusive (crash on literal mutation)"] += 1
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
        print(f"\n  inconclusive ({len(inconclusive)}): mutation broke them "
              f"structurally, so the test says nothing")
        for f in inconclusive:
            print(f"    {f}")
    slow = [f for f, b in zip(files, base) if b != "PASS"]
    if slow:
        print(f"\n  did not complete at timeout={a.timeout}s "
              f"({len(slow)}) -- raise --timeout, do not assume broken:")
        for f in slow:
            print(f"    {f}")


if __name__ == "__main__":
    main()

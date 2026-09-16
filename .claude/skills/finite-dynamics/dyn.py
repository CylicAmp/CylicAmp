#!/usr/bin/env python3
"""Complete audit of a self-map of a finite set. Usage:
   dyn.py "x**3+33" 37          cycle type, transients, sources, in-degrees
   dyn.py "2*x+1" 37
   dyn.py "3*x+1" 37 --quotient  also test descent to the cubing quotient
"""
import sys
from collections import Counter

def analyse(f, states):
    per = set()
    for s in states:
        seen, y, i = {}, s, 0
        while y not in seen:
            seen[y] = i; y = f(y); i += 1
        z, cy = y, [y]
        while f(z) != y:
            z = f(z); cy.append(z)
        per |= set(cy)
    cycles, done = [], set()
    for s in states:
        if s in per and s not in done:
            cy, y = [s], f(s)
            while y != s:
                cy.append(y); y = f(y)
            done |= set(cy); cycles.append(cy)
    tails = {}
    for s in states:
        y, t = s, 0
        while y not in per:
            y = f(y); t += 1
        tails[s] = t
    img = {f(s) for s in states}
    ind = Counter(f(s) for s in states)
    src = [s for s in states if s not in img]
    ev = set(states)
    steps = 0
    while True:
        nxt = {f(s) for s in ev}
        if nxt == ev: break
        ev = nxt; steps += 1
    return dict(cycles=cycles, periodic=len(per), transient=len(states)-len(per),
                tails=tails, sources=src, indeg=ind, image=len(img),
                eventual=len(ev), depth=steps)

def report(name, f, states):
    a = analyse(f, states)
    n = len(states)
    print(f"{name}   |X| = {n}")
    print(f"  cycles        {[len(c) for c in a['cycles']]}  {a['cycles']}")
    print(f"  periodic      {a['periodic']}      transient {a['transient']}")
    print(f"  fixed points  {[c[0] for c in a['cycles'] if len(c)==1]}")
    print(f"  image size    {a['image']}   in-degrees {dict(Counter(a['indeg'].values()))}")
    print(f"  sources       {a['sources']}")
    print(f"  max tail      {max(a['tails'].values())}")
    print(f"  eventual image {a['eventual']} after {a['depth']} steps")
    perm = a['image'] == n
    print(f"  permutation?  {perm}")
    if not perm:
        print(f"  -> NOT invertible: information is lost each step.")
        print(f"  -> no surjective semiconjugacy onto any permutation of")
        print(f"     more than {a['eventual']} states (eventual image bound).")
    return a

def main():
    if len(sys.argv) < 3:
        print(__doc__); return
    expr, p = sys.argv[1], int(sys.argv[2])
    f = lambda x: eval(expr, {"x": x, "pow": pow}) % p
    a = report(f"{expr} mod {p}", f, list(range(p)))
    if "--quotient" in sys.argv:
        cls = {}
        for x in range(p):
            cls.setdefault(pow(x, 3, p), []).append(x)
        const = all(len({f(x) for x in c}) == 1 for c in cls.values())
        pres = all(len({pow(f(x), 3, p) for x in c}) == 1 for c in cls.values())
        print(f"\n  descent to the cubing quotient ({len(cls)} classes):")
        print(f"    class-preserving  x~y => f(x)~f(y)   {pres}")
        print(f"    CONSTANT          x~y => f(x)=f(y)   {const}")
        if const:
            rep = {k: c[0] for k, c in cls.items()}
            keys = sorted(cls)
            phi = {k: pow(f(rep[k]), 3, p) for k in keys}
            print(f"    descends. induced map on {len(keys)} classes:")
            report("    phi", lambda k: phi[k], keys)
        elif pres:
            print("    descends (preservation only) -- in-degree structure")
            print("    does NOT follow; that needs constancy.")
        else:
            print("    does NOT descend.")

if __name__ == "__main__":
    main()

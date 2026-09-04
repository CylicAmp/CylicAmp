#!/usr/bin/env python3
"""
Runs METHOD.md's fixed sequence plus CLAUDE.md's standing analysis on any
number. Reports everything without filtering.

    python3 audit.py 246 [more numbers...]
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import gf37 as G


def audit(n):
    r = n % G.P
    o = G.orbit(n)
    L = []
    A = L.append

    A(f"{'='*66}")
    A(f"n = {n}")
    A(f"{'='*66}")

    # Steps 1-3
    A(f"  [1] n mod 37          = {r}")
    A(f"  [2] named sets        = {G.named_sets(n) or 'UNNAMED'}")
    A(f"  [3] orbit             = {o}  {G.orbit_triple(n) if r else ''}")
    if r:
        t = G.orbit_triple(n)
        A(f"      position in orbit = {t.index(r)}")
        A(f"      Z/12Z class       = {G.cls(n)}")
        A(f"      antipodal orbit   = {G.antipode(o)}")
        A(f"      decimal block     = {G.block(r)}  (block of {r}/37)")

    # Step 4
    A(f"  [4] DR                = {G.dr(n)}   basin = {G.dr_basin(n)}")
    A(f"      DR mod 3 = {G.dr(n)%3}, n mod 3 = {n%3}  (equal: {G.dr(n)%3==n%3})")

    # Step 5
    A(f"  [5] mod 2,3,6,9       = {n%2}, {n%3}, {n%6}, {n%9}")

    # Step 6
    p = G.prime_profile(n)
    if p['prime']:
        A(f"  [6] prime             = True  twin={p['twin']} cousin={p['cousin']} "
          f"sexy={p['sexy']}")
        A(f"      Sophie Germain    = {p['sophie_germain']} (2n+1={2*n+1})   "
          f"safe={p['safe']}")
        A(f"      chamber (n mod 6) = {p['chamber']}")
    else:
        A(f"  [6] prime             = False   factorization = {G.factor(n)}")

    # Standing analysis (CLAUDE.md)
    A(f"  --- standing analysis ---")
    if r:
        A(f"  RH   floor(gamma_n) = {r} at n = {G.rh_hits(r) or 'none in first 30'}")
        A(f"  137  n x137 = {(n*137)%G.P} ({G.orbit(n*137)}),  "
          f"n /137 = {(r*pow(26,-1,G.P))%G.P} ({G.orbit(r*pow(26,-1,G.P))})")
        A(f"       n mod 137 = {n%137}")
        r30 = G.rule30(n)
        A(f"  R30  {n%256:08b} -> {r30:08b} = {r30}, mod 37 = {r30%G.P} "
          f"({G.orbit(r30)})")
    else:
        A(f"  SEAM: 37 | {n}. No orbit, no class. It is the rotation axis (T302).")

    # Forced-fact warnings
    A(f"  --- forced facts (carry no information; T282) ---")
    A(f"  * every residue lands in exactly one orbit — membership is never news")
    A(f"  * the 137-map preserves every orbit by definition")
    if r:
        A(f"  * class(a)+class(b) = class(ab) for EVERY factorization (T285)")
        A(f"  * DR(a)*DR(b) = DR(ab) mod 9 for EVERY factorization")
        A(f"  * block({r}) is a function of {r} alone — decimal route adds nothing")
    return "\n".join(L)


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    for a in args:
        print(audit(int(a)))
        print()

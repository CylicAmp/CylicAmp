# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 245: All-Prime Grids -- Full Structural Analysis
================================================================================

Extends T238 (master coset theorem) and T240 (cyclic permutation) with the
complete structural picture of the three all-prime grids:

  G(3,1): 311, 131, 113  -> C_2  = {2, 15, 20}
  G(1,9): 199, 919, 991  -> C_9  = {14, 29, 31}
  G(7,3): 733, 373, 337  -> C_3  = {3, 4, 30}

STRUCTURE:

A. DR CONSTANCY (all rows share one DR):
  Cyclic permutations of digits {b,s,s} always have digit sum b+2s.
  Every row therefore has DR = DR(b+2s).

  G(3,1): b+2s = 5       DR = 5  (prime seed)  for all 3 rows
  G(1,9): b+2s = 19      DR = 1  in H          for all 3 rows
  G(7,3): b+2s = 13      DR = 4  in SA         for all 3 rows

  The three DR values {5, 1, 4} classify as: prime seed, H-identity, SA.

B. ROW PRODUCT = (b-s)^3 mod 37:
  The product of the three row residues:
    N_1 * N_2 * N_3 = (b-s)*26 * (b-s)*10 * (b-s)*1  (mod 37)
                     = (b-s)^3 * (26*10*1) mod 37
                     = (b-s)^3 * 260 mod 37
                     = (b-s)^3 * 1  mod 37
  (since prod(H) = 1*10*26 = 260 = 7*37+1 = 1 mod 37)

  G(3,1): 2^3 = 8        mod 37 = 8   (first prime cubed)
  G(1,9): (-8)^3 = -512  mod 37 = 6   = IMAGINARY UNIT of GF(37)
  G(7,3): 4^3 = 64       mod 37 = 27  in C_8={11,27,36} (the -1/repunit coset)

  The product of G(1,9)'s rows is the imaginary unit 6 (6^2=-1 mod 37).

C. PRODUCT OF H IS IDENTITY:
  prod(H) = 1 * 10 * 26 = 260 = 7*37 + 1 = 1 (mod 37).
  The product of all elements of the sovereign kernel is the identity.
  This makes N_1*N_2*N_3 = (b-s)^3 mod 37 exact.

D. TWO-DIGIT READINGS OF EACH PAIR:
  G(3,1): [b,s]=[3,1] -> 31 and 13. Both DR=4 in SA. 31 in C_9={14,29,31}.
  G(1,9): [b,s]=[1,9] -> 19 and 91. Both DR=1 in H. 19=twin prime; 91 mod 37=17=twin prime.
  G(7,3): [b,s]=[7,3] -> 73 and 37.
    73 mod 37 = 36 = -1 = ANTIPODE.
    37 mod 37 = 0 = SEAM.
    Both DR=1 in H.
    The digit pair (7,3) read as two-digit numbers gives exactly the
    seam-antipode pair {37, 73} from T239 (Mirror Seam-Antipode theorem).

E. THE (b+s) SOVEREIGN PATTERN:
  G(3,1): b+s = 4  in SA.
  G(1,9): b+s = 10 in H.
  G(7,3): b+s = 10 in H.
  The two H-generating grids share b+s=10 (the first H element after 1).
  G(3,1) uniquely has b+s in SA.

F. DIGIT OPERATIONS ON ALL THREE (b,s) PAIRS:
  G(3,1): b+s=4[SA]  b-s=2  bxs=3[ST]  b/s=3[ST]
  G(1,9): b+s=10[H]  b-s=29  bxs=9[SA]  b/s=33
  G(7,3): b+s=10[H]  b-s=4[SA]  bxs=21[ST]  b/s=27[C_8]

G. ROW SUMS AND COSET QUOTIENTS:
  G(3,1): 311+131+113=555=15*37.  Quotient 15 mod37=15.  15 in C_2 (same coset as grid).
  G(1,9): 199+919+991=2109=57*37. Quotient 57 mod37=20.  20 in C_2.
  G(7,3): 733+373+337=1443=39*37. Quotient 39 mod37=2.   2 is the primitive root.

H. THE ALL-PRIME DR TRIPLET {5, 1, 4}:
  DR(prime seed) = 5.
  DR(H identity) = 1.
  DR(SA element) = 4.
  5+1+4 = 10 in H. The sum of the three grid DRs is in H.
  5*1*4 = 20 mod 37 = 20 in C_2 (the coset of G(3,1)).
================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H_SET = {1, 10, 26}
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED_ORBIT = {18, 24, 32}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True


def build_cosets():
    used, cosets = set(), []
    for g in range(1, P):
        if g in used: continue
        c = sorted((g * h) % P for h in H_SET)
        for x in c: used.add(x)
        cosets.append(c)
    return cosets


def coset_of(x, cosets):
    r = x % P
    for i, c in enumerate(cosets):
        if r in c: return i+1, c
    return None, None


def run():
    print("=" * 70)
    print("THEOREM 245: ALL-PRIME GRIDS -- FULL STRUCTURAL ANALYSIS")
    print("=" * 70)

    cosets = build_cosets()

    grids = [
        (3, 1, [311, 131, 113]),
        (1, 9, [199, 919, 991]),
        (7, 3, [733, 373, 337]),
    ]

    # A: DR constancy
    print("\nA. DR CONSTANCY (all rows share one DR = DR(b+2s)):")
    dr_vals = []
    for b, s, rows in grids:
        ds = b + 2*s
        d = dr(ds)
        dr_vals.append(d)
        flags = []
        if d in H_SET: flags.append("H")
        if d in SA:    flags.append("SA")
        print(f"  G({b},{s}): b+2s={ds}  DR={d}  [{','.join(flags) or 'prime seed'}]")
        for row in rows:
            assert dr(row) == d
        print(f"    All rows confirmed DR={d}: {[dr(r) for r in rows]}")
    assert dr_vals == [5, 1, 4]
    print(f"  DRs: {{5=prime seed, 1=H, 4=SA}}  check")

    # B: Row product = (b-s)^3
    print(f"\nB. ROW PRODUCT = (b-s)^3 mod {P}:")
    for b, s, rows in grids:
        prod_r = 1
        for row in rows:
            prod_r = (prod_r * (row % P)) % P
        key = (b - s) % P
        theory = pow(key, 3, P)
        flags = []
        if prod_r in H_SET: flags.append("H")
        if prod_r in SA:    flags.append("SA")
        if prod_r == 6:     flags.append("IMAG_UNIT")
        print(f"  G({b},{s}): (b-s={b-s})^3 mod{P} = {key}^3 = {theory}  "
              f"actual={prod_r}  match:{theory==prod_r}  [{','.join(flags) or '-'}]")
        assert prod_r == theory
    print(f"  G(1,9) product = 6 = imaginary unit (6^2=-1 mod {P})  check")
    assert ((-8)**3) % P == 6

    # C: Product of H = 1
    print(f"\nC. PRODUCT OF H IS IDENTITY:")
    prod_h = 1
    for h in H_SET:
        prod_h = (prod_h * h) % P
    print(f"  prod(H) = 1x10x26 = 260 mod {P} = {prod_h} (identity)  check")
    assert prod_h == 1
    print(f"  This makes N_1*N_2*N_3 = (b-s)^3 mod {P} exact  check")

    # D: Two-digit readings
    print(f"\nD. TWO-DIGIT READINGS OF EACH (b,s) PAIR:")
    for b, s, rows in grids:
        bs = 10*b + s
        sb = 10*s + b
        print(f"  G({b},{s}): [{b}{s}]={bs} mod{P}={bs%P} DR={dr(bs)}  "
              f"[{s}{b}]={sb} mod{P}={sb%P} DR={dr(sb)}")
    # G(7,3) special case
    assert 73 % P == P-1 and 37 % P == 0
    assert dr(73) == 1 and dr(37) == 1
    print(f"  G(7,3): 73 mod{P}={73%P}=ANTIPODE, 37 mod{P}={37%P}=SEAM  check")
    print(f"  The digit pair (7,3) contains the seam-antipode pair from T239  check")

    # E: b+s pattern
    print(f"\nE. THE (b+s) SOVEREIGN PATTERN:")
    for b, s, rows in grids:
        add = (b+s)%P
        flags = []
        if add in H_SET: flags.append("H")
        if add in SA:    flags.append("SA")
        print(f"  G({b},{s}): b+s={b+s} mod{P}={add}  [{','.join(flags) or '-'}]")
    assert (1+9)%P in H_SET and (7+3)%P in H_SET and (3+1)%P in SA
    print(f"  G(1,9) and G(7,3): b+s=10 in H.  G(3,1): b+s=4 in SA.  check")

    # F: Full digit operations
    print(f"\nF. DIGIT OPERATIONS:")
    for b, s, rows in grids:
        inv_s = pow(s, -1, P)
        ops = [(b+s)%P, (b-s)%P, (b*s)%P, (b*inv_s)%P]
        labels = ['+','-','x','/']
        parts = []
        for op, lab in zip(ops, labels):
            fl = []
            if op in H_SET: fl.append("H")
            if op in SA:    fl.append("SA")
            if op in ST:    fl.append("ST")
            parts.append(f"b{lab}s={op}[{','.join(fl) or '-'}]")
        joined = "  ".join(parts)
        print(f"  G({b},{s}): {joined}")

    # G: Row sums and quotients
    print(f"\nG. ROW SUMS AND COSET QUOTIENTS:")
    for b, s, rows in grids:
        rs = sum(rows)
        q = rs // P
        ci, c = coset_of(q, cosets)
        print(f"  G({b},{s}): sum={rs}={q}x{P}  quotient={q} mod{P}={q%P}  coset C_{ci}={c}")
    assert sum([311,131,113])//P == 15 and 15 in [2,15,20]
    assert sum([199,919,991])//P == 57 and 57%P == 20 and 20 in [2,15,20]
    assert sum([733,373,337])//P == 39 and 39%P == 2

    # H: DR triplet
    print(f"\nH. THE ALL-PRIME DR TRIPLET {{5, 1, 4}}:")
    dr_sum = 5+1+4
    dr_prod = 5*1*4
    print(f"  5+1+4 = {dr_sum} in H:{dr_sum in H_SET}  check")
    print(f"  5x1x4 = {dr_prod} mod{P}={dr_prod%P}  in C_2:{dr_prod%P in [2,15,20]}  check")
    assert dr_sum in H_SET and dr_prod % P == 20

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()

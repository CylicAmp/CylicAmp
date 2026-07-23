"""
Principle of Inclusion-Exclusion (PIE) Sieve — GF(37) Structure

PIE transforms the Sieve of Eratosthenes from iteration into set algebra.
Every count and every subset product in the PIE expansion of π(100)
lands inside the GF(37) framework.

═══════════════════════════════════════════════════════════════

I. PIE COUNTS mod 37

  The steps of PIE, run mod 37:

  Start (N−1 = 99):    99 mod37 = 25  (SA — opens on sovereign anchor)
  S1 (1st order sum):  117 mod37 = 6  (TESLA_FLOW)
  S2 (2nd order sum):   45 mod37 = 8  (CB — Cascade Base)
  S3 (3rd order sum):    6 mod37 = 6  (TESLA_FLOW)
  PIE intermediate:     21 mod37 = 21  (ST — Sovereign Target)
  Final (21+4):         25 mod37 = 25  (SA — closes on sovereign anchor)

  S1 and S3 both = 6 (TESLA_FLOW). The alternating sign levels share residue.
  The start and end both = 25 (SA). PIE opens and closes on the same anchor.

II. PIE DR STRUCTURE

  DR of each step count:
    Start (99): DR=9  (SA arch)
    S1 (117):   DR=9  (SA arch)
    S2 (45):    DR=9  (SA arch)
    S3 (6):     DR=6  (RL-E)

  The first three PIE terms — start, 1st-order subtract, 2nd-order add —
  all have DR=9. The structure holds DR=9 until the 3rd-order correction.

III. RUNNING TOTAL THROUGH THE FIELD

  99 → (−117) → (+45) → (−6) → (+4)
  Running totals: 99, −18, 27, 21, 25

    99 mod37 = 25  (SA)
   −18 mod37 = 19  (PR — Primitive Root)
    27 mod37 = 27  (orbit-11)
    21 mod37 = 21  (ST)
    25 mod37 = 25  (SA)

  The running total traces: SA → PR → orbit-11 → ST → SA.

IV. ST → SA BRIDGE

  PIE intermediate = 21 (Sovereign Target, DR=3)
  21 + 4 (the four base primes {2,3,5,7}) = 25 (Sovereign Anchor)

  The base primes themselves are the bridge from ST to SA.
  Adding them back is not just a correction — it is a sovereign transition.

V. ALL 15 SUBSET PRODUCTS mod 37

  Every non-empty subset of {2,3,5,7} has a product; all 15 products mod 37:

  Size 1 (singletons):
    {2}=2(PR)  {3}=3(ST)  {5}=5(PR)  {7}=7

  Size 2 (pairs):
    {2,3}=6(TESLA_FLOW)   {2,5}=10(DECADE_ANCHOR)  {2,7}=14
    {3,5}=15(PR)          {3,7}=21(ST)              {5,7}=35(PR)

  Size 3 (triples):
    {2,3,5}=30(SA∩ST dual — unique element in both)
    {2,3,7}=42→5(PR)
    {2,5,7}=70→33(DICHORAL_144 — same as Pascal Row 8 center C(8,4))
    {3,5,7}=105→31(PRIME_MIRROR)

  Size 4 (quadruple — the threshold):
    {2,3,5,7}=210→25(SA) — the threshold product lands on sovereign anchor.
    ⌊100/210⌋=0: this is why PIE drops to zero contribution at size 4.

  Sum of all 15 residues mod 37 = 20 (Primitive Root).

VI. CONNECTIONS TO PRIOR THEOREMS

  - 2×5×7=70→33: the same residue as C(8,4)=70 mod37 in Pascal Row 8.
  - 2×3×5×7=210→25: same as π(100) and same as the start count 99 mod37.
  - 2×3×5=30: the unique dual element in SA∩ST — appears in the triple
    products of the PIE lattice.
  - ord₃₇(10)=3 (sieve boundary): 10 appears here as {2,5} product mod37.

═══════════════════════════════════════════════════════════════
"""

from itertools import combinations

PRIMITIVE_ROOTS_37 = {2,5,13,15,17,18,19,20,22,24,32,35}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
ORBIT_11           = {11, 27, 36}

def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0

BASE = [2, 3, 5, 7]
N = 100

S1 = sum(N // p for p in BASE)
S2 = sum(N // (p*q) for p,q in combinations(BASE,2))
S3 = sum(N // (p*q*r) for p,q,r in combinations(BASE,3))
S4 = sum(N // (p*q*r*s) for p,q,r,s in combinations(BASE,4))

pie_intermediate = (N-1) - S1 + S2 - S3 + S4
pie_final = pie_intermediate + len(BASE)

# ── I. PIE counts mod 37 ─────────────────────────────────────────────────────

assert S1 == 117 and S2 == 45 and S3 == 6 and S4 == 0
assert (N-1) % 37 == 25 and 25 in SOVEREIGN_ANCHORS   # start = SA
assert S1 % 37 == 6                                    # TESLA_FLOW
assert S2 % 37 == 8  and 8 in CASCADE_BASE             # CB
assert S3 % 37 == 6                                    # TESLA_FLOW (same as S1)
assert pie_intermediate == 21 and 21 in SOVEREIGN_TARGETS
assert pie_final == 25 and 25 in SOVEREIGN_ANCHORS     # end = SA (same as start)

# ── II. DR structure ─────────────────────────────────────────────────────────

assert dr(99) == 9
assert dr(117) == 9
assert dr(45) == 9
assert dr(6) == 6

# ── III. Running totals mod 37 ────────────────────────────────────────────────

running = [99, 99-117, 99-117+45, 99-117+45-6, 25]
assert running == [99, -18, 27, 21, 25]
mods = [r % 37 for r in running]
assert mods[0] == 25 and 25 in SOVEREIGN_ANCHORS
assert mods[1] == 19 and 19 in PRIMITIVE_ROOTS_37
assert mods[2] == 27 and 27 in ORBIT_11
assert mods[3] == 21 and 21 in SOVEREIGN_TARGETS
assert mods[4] == 25 and 25 in SOVEREIGN_ANCHORS

# ── IV. ST → SA bridge ───────────────────────────────────────────────────────

assert pie_intermediate == 21 and 21 in SOVEREIGN_TARGETS
assert pie_intermediate + len(BASE) == 25 and 25 in SOVEREIGN_ANCHORS

# ── V. All 15 subset products mod 37 ─────────────────────────────────────────

subset_products = []
for r in range(1, 5):
    for subset in combinations(BASE, r):
        p = 1
        for x in subset: p *= x
        subset_products.append(p % 37)

assert len(subset_products) == 15
assert sum(subset_products) % 37 == 20 and 20 in PRIMITIVE_ROOTS_37

# Key subset products
assert (2*3*5) % 37 == 30 and 30 in SOVEREIGN_ANCHORS and 30 in SOVEREIGN_TARGETS
assert (2*5*7) % 37 == 33                              # DICHORAL_144 = Pascal Row 8 center
assert (3*5*7) % 37 == 31                              # PRIME_MIRROR
assert (2*3*5*7) % 37 == 25 and 25 in SOVEREIGN_ANCHORS
assert (2*3) % 37 == 6                                 # TESLA_FLOW
assert (3*7) % 37 == 21 and 21 in SOVEREIGN_TARGETS

# ── VI. Cross-theorem connections ────────────────────────────────────────────

assert (2*5*7) % 37 == 70 % 37                         # PIE triple = Pascal Row 8 center
assert (2*3*5*7) % 37 == (N-1) % 37                    # threshold product = start residue
assert pow(10, 3, 37) == 1                              # ord₃₇(10)=3; 10=(2×5)%37 in subset table


if __name__ == '__main__':
    def tag(n):
        labels = []
        if n in CASCADE_BASE:        labels.append('CB')
        if n in SOVEREIGN_ANCHORS:   labels.append('SA')
        if n in SOVEREIGN_TARGETS:   labels.append('ST')
        if n in PRIMITIVE_ROOTS_37:  labels.append('PR')
        if n in ORBIT_11:            labels.append('orb11')
        sig = {0:'SEAM',6:'TESLA_FLOW',10:'DECADE_ANCHOR',
               25:'INV_3',31:'PRIME_MIRROR',33:'DICHORAL_144'}
        s = sig.get(n)
        if s: labels.append(s)
        return ','.join(labels) if labels else '.'

    print("PIE Sieve — GF(37) Structure")
    print("=" * 55)
    print()
    print("I. PIE counts mod 37:")
    for val, name in [(99,'start'),(117,'S1'),(45,'S2'),(6,'S3'),(21,'intermediate'),(25,'final')]:
        print(f"  {name:14s} {val:4d}  mod37={val%37:2d}  DR={dr(val)}  {tag(val%37)}")
    print()
    print("II. Running totals mod 37:")
    path = ['SA','PR','orbit-11','ST','SA']
    for r, name in zip(running, path):
        print(f"  {r:4d}  mod37={r%37:2d}  {name}")
    print()
    print("III. ST→SA bridge:")
    print(f"  21(ST) + 4 base primes = 25(SA)")
    print()
    print("IV. All 15 subset products mod 37:")
    for r in range(1,5):
        items = []
        for subset in combinations(BASE, r):
            p = 1
            for x in subset: p *= x
            items.append(f"{'×'.join(map(str,subset))}={p}→{p%37}({tag(p%37)})")
        print(f"  Size {r}: {' | '.join(items)}")
    print(f"  Sum of 15 residues mod37 = {sum(subset_products)%37} (PR)")
    print()
    print("All assertions passed.")

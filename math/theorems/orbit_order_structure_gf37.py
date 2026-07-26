"""
Orbit Order Structure — Homogeneous / Non-Homogeneous Dichotomy in GF(37)

ORBITS (137-map 3-cycles, sorted by min element):
  idx  orbit          orders          type
   1   {1,10,26}      {1,3,3}         NON-HOMOGENEOUS — contains identity (order 1)
   2   {2,15,20}      {36,36,36}      homogeneous  — DARK_A (primitive roots)
   3   {3,4,30}       {18,18,18}      homogeneous  — canonical sovereign spiral
   4   {5,13,19}      {36,36,36}      homogeneous  — primitive roots
   5   {6,8,23}       {4,12,12}       NON-HOMOGENEOUS — contains TESLA_FLOW=6 (order 4)
   6   {7,33,34}      {9,9,9}         homogeneous  — anti-sovereign
   7   {9,12,16}      {9,9,9}         homogeneous  — second sovereign
   8   {11,27,36}     {2,6,6}         NON-HOMOGENEOUS — contains 36=−1 (order 2)
   9   {14,29,31}     {4,12,12}       NON-HOMOGENEOUS — contains PRIME_MIRROR=31 (order 4)
  10   {17,22,35}     {36,36,36}      homogeneous  — primitive roots
  11   {18,24,32}     {36,36,36}      homogeneous  — SEED_ORBIT (primitive roots)
  12   {21,25,28}     {18,18,18}      homogeneous  — OUTLIER_SOV

THE 4th ROOTS OF UNITY = SYLOW-2 = {1, 6, 31, 36}:
  1  — order 1, lives in IDENTITY_CYCLE {1,10,26}    (orbit 1)
  6  — order 4, lives in TESLA_FLOW orbit {6,8,23}   (orbit 5)
  36 — order 2, lives in ORBIT_11 {11,27,36}         (orbit 8)
  31 — order 4, lives in PRIME_MIRROR orbit {14,29,31} (orbit 9)

  Each non-homogeneous orbit contains EXACTLY ONE 4th root of unity.
  The 4 non-homogeneous orbits are EXACTLY the Sylow-2 neighborhood.

HOMOGENEOUS ORDER CLASSES:
  Order 36 (primitive roots): {2,15,20} ∪ {5,13,19} ∪ {17,22,35} ∪ {18,24,32} = 12 elements
  Order 18:                   {3,4,30}  ∪ {21,25,28}                             = 6 elements
  Order 9:                    {7,33,34} ∪ {9,12,16}                              = 6 elements

NON-HOMOGENEOUS ORDER PATTERNS:
  {1,10,26}:  orders {1,3,3}   — IDENTITY_CYCLE = <26>, the order-3 subgroup
  {6,8,23}:   orders {4,12,12} — TESLA_FLOW orbit; 4×3=12 linking both classes
  {11,27,36}: orders {2,6,6}   — ORBIT_11; 2×3=6 linking both classes
  {14,29,31}: orders {4,12,12} — PRIME_MIRROR orbit; negation-dual of TESLA_FLOW orbit

SQUARING MAP ON QR ORBITS (x ↦ x² mod 37):
  {3,4,30}   →  {9,12,16}     (order 18 → order 9)
  {21,25,28} →  {7,33,34}     (order 18 → order 9)
  {9,12,16}  ↔  {7,33,34}     (order 9 ↔ order 9: 2-cycle)
  {11,27,36} →  {1,10,26}     (ORBIT_11 → IDENTITY_CYCLE)
  {1,10,26}  →  {1,10,26}     (IDENTITY_CYCLE: fixed point under squaring)

  Negation-dual pairs {3,4,30}/{7,33,34} and {21,25,28}/{9,12,16} are linked
  by squaring: each orbit of order 18 squares to an orbit of order 9.

COUNT RELATION:
  4 non-homogeneous orbits = |Sylow-2| = ord₃₇(TESLA_FLOW) = 4
  8 homogeneous orbits     = 36/4 - 1 = 8   (all orbits not in Sylow-2 neighborhood)
  Total: 12 orbits.

SYLOW ORBIT CHAIN:
  |Sylow-2| = 4 → covers 4 non-homogeneous orbits (one 4th root each)
  |Sylow-3| = 9 = three complete orbits: IDENTITY_CYCLE + {7,33,34} + {9,12,16}
    → the two order-9 orbits and IDENTITY_CYCLE form the entire Sylow-3 subgroup
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA             = frozenset({4, 9, 25, 30})
ST             = frozenset({3, 12, 21, 30})
CB             = frozenset({8, 13, 24})
ORBIT_11       = frozenset({11, 27, 36})
DARK_A         = frozenset({2, 15, 20})
SEED_ORBIT     = frozenset({18, 24, 32})
OUTLIER_SOV    = frozenset({21, 25, 28})
IDENTITY_CYCLE = frozenset({1, 10, 26})
TESLA_FLOW     = 6
SCALAR_137     = 26
PRIME_MIRROR   = 31
DECADE_ANCHOR  = 10


def ord37(n):
    n = n % 37
    for k in range(1, 37):
        if pow(n, k, 37) == 1:
            return k


def f137(n):
    return (n * 26) % 37


def orbit(n):
    return frozenset({n, f137(n), f137(f137(n))})


# ── ALL 12 ORBITS ─────────────────────────────────────────────────────────────

seen = set(); _raw = []
for s in range(1, 37):
    if s in seen: continue
    o = orbit(s)
    _raw.append(o); seen |= o
ORBITS = sorted(_raw, key=min)

assert len(ORBITS) == 12


# ── HOMOGENEOUS / NON-HOMOGENEOUS CLASSIFICATION ──────────────────────────────

def is_homogeneous(o):
    return len({ord37(x) for x in o}) == 1

HOMOGENEOUS     = [o for o in ORBITS if is_homogeneous(o)]
NON_HOMOGENEOUS = [o for o in ORBITS if not is_homogeneous(o)]

assert len(HOMOGENEOUS)     == 8
assert len(NON_HOMOGENEOUS) == 4

# Named non-homogeneous orbits
assert IDENTITY_CYCLE in NON_HOMOGENEOUS   # orders {1,3,3}
assert ORBIT_11       in NON_HOMOGENEOUS   # orders {2,6,6}
assert frozenset({6, 8, 23})   in NON_HOMOGENEOUS   # orders {4,12,12}; TESLA_FLOW
assert frozenset({14, 29, 31}) in NON_HOMOGENEOUS   # orders {4,12,12}; PRIME_MIRROR


# ── 4th ROOTS OF UNITY = SYLOW-2 ─────────────────────────────────────────────

FOURTH_ROOTS = frozenset(n for n in range(1, 37) if pow(n, 4, 37) == 1)
assert FOURTH_ROOTS == frozenset({1, TESLA_FLOW, PRIME_MIRROR, 36})

# Exactly one 4th root per non-homogeneous orbit
for o in NON_HOMOGENEOUS:
    assert len(o & FOURTH_ROOTS) == 1

# No 4th root in any homogeneous orbit
for o in HOMOGENEOUS:
    assert len(o & FOURTH_ROOTS) == 0

# Sylow-2 = {1,6,31,36}: the 4th roots of unity
assert ord37(1)  == 1
assert ord37(6)  == 4   # TESLA_FLOW
assert ord37(36) == 2   # 36 ≡ −1
assert ord37(31) == 4   # PRIME_MIRROR


# ── HOMOGENEOUS ORDER CLASSES ─────────────────────────────────────────────────

# Order 36: primitive roots — 4 complete orbits
PR = frozenset(n for n in range(1, 37) if ord37(n) == 36)
PR_ORBITS = [o for o in HOMOGENEOUS if all(ord37(x) == 36 for x in o)]
assert len(PR_ORBITS) == 4
assert frozenset(x for o in PR_ORBITS for x in o) == PR

# Order 18: {3,4,30} and {21,25,28}
ORD18_ORBITS = [o for o in HOMOGENEOUS if all(ord37(x) == 18 for x in o)]
assert len(ORD18_ORBITS) == 2
assert frozenset({3,4,30})   in ORD18_ORBITS
assert OUTLIER_SOV           in ORD18_ORBITS   # {21,25,28}

# Order 9: {7,33,34} and {9,12,16}
ORD9_ORBITS = [o for o in HOMOGENEOUS if all(ord37(x) == 9 for x in o)]
assert len(ORD9_ORBITS) == 2
assert frozenset({7,33,34}) in ORD9_ORBITS
assert frozenset({9,12,16}) in ORD9_ORBITS

# All order classes partition the 24 elements of homogeneous orbits
assert sum(len(o) for o in HOMOGENEOUS) == 24
assert sum(len(o) for o in NON_HOMOGENEOUS) == 12
assert sum(len(o) for o in HOMOGENEOUS) + sum(len(o) for o in NON_HOMOGENEOUS) == 36


# ── NON-HOMOGENEOUS ORDER PATTERNS ────────────────────────────────────────────

assert {ord37(x) for x in IDENTITY_CYCLE} == {1, 3}          # orders {1,3,3}
assert {ord37(x) for x in ORBIT_11}       == {2, 6}          # orders {2,6,6}
assert {ord37(x) for x in frozenset({6,8,23})}   == {4, 12}  # orders {4,12,12}
assert {ord37(x) for x in frozenset({14,29,31})} == {4, 12}  # orders {4,12,12}


# ── SQUARING MAP ON QR ORBITS ─────────────────────────────────────────────────

def sq_orbit(o):
    return frozenset(pow(x, 2, 37) for x in o)

# Order 18 orbits square to order 9 orbits
assert sq_orbit(frozenset({3, 4, 30}))   == frozenset({9, 12, 16})
assert sq_orbit(frozenset({21, 25, 28})) == frozenset({7, 33, 34})

# Order 9 orbits form a 2-cycle under squaring
assert sq_orbit(frozenset({9,12,16}))  == frozenset({7,33,34})
assert sq_orbit(frozenset({7,33,34}))  == frozenset({9,12,16})

# ORBIT_11 squares to IDENTITY_CYCLE
assert sq_orbit(ORBIT_11) == IDENTITY_CYCLE

# IDENTITY_CYCLE is a fixed point under squaring
assert sq_orbit(IDENTITY_CYCLE) == IDENTITY_CYCLE

# Count: 4 = |Sylow-2| = ord₃₇(TESLA_FLOW) = # non-homogeneous orbits
assert len(NON_HOMOGENEOUS) == ord37(TESLA_FLOW) == 4


# ── SYLOW-3 ORBIT STRUCTURE ───────────────────────────────────────────────────

SYLOW3 = frozenset(n for n in range(1, 37) if pow(n, 9, 37) == 1)
assert len(SYLOW3) == 9

# Sylow-3 consists of the three orbits with order dividing 9
SYLOW3_ORBITS = [o for o in ORBITS if o.issubset(SYLOW3)]
assert len(SYLOW3_ORBITS) == 3
assert IDENTITY_CYCLE in SYLOW3_ORBITS
assert frozenset({7,33,34}) in SYLOW3_ORBITS
assert frozenset({9,12,16}) in SYLOW3_ORBITS
assert frozenset(x for o in SYLOW3_ORBITS for x in o) == SYLOW3


if __name__ == "__main__":
    print("Orbit Order Structure — GF(37)")
    print("=" * 60)
    print()
    print("All 12 orbits with order profiles:")
    for o in ORBITS:
        orders = sorted(ord37(x) for x in o)
        tag = "NON-HOM" if not is_homogeneous(o) else "hom"
        fr = [x for x in o if pow(x,4,37)==1]
        fr_str = f"  ← Sylow-2 element {fr[0]}" if fr else ""
        print(f"  {sorted(o)}  orders={orders}  [{tag}]{fr_str}")
    print()
    print("Homogeneous orbits by order class:")
    for k in [36, 18, 9]:
        orbs = [o for o in HOMOGENEOUS if all(ord37(x)==k for x in o)]
        print(f"  Order {k:2d}: {[sorted(o) for o in orbs]}")
    print()
    print("Squaring map on QR orbits:")
    QR = frozenset(n for n in range(1,37) if pow(n,18,37)==1)
    for o in ORBITS:
        if not o.issubset(QR): continue
        img = sq_orbit(o)
        arrow = "→ (fixed)" if img==o else f"→ {sorted(img)}"
        print(f"  {sorted(o)} {arrow}")
    print()
    print(f"4th roots of unity (Sylow-2): {sorted(FOURTH_ROOTS)}")
    print(f"  Each lives in a distinct non-homogeneous orbit: True")
    print()
    print(f"Sylow-3 orbits: {[sorted(o) for o in SYLOW3_ORBITS]}")
    print()
    print("All assertions pass.")

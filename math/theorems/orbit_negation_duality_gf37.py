"""
Orbit Negation Duality — GF(37)

FOUNDATION: chi(−1) = chi(36) = +1 for GF(37).
  37 ≡ 1 mod 4 → (−1)^((37−1)/2) = (−1)^18 = 1. Negation is a QR.
  Therefore: chi(−n) = chi(−1)·chi(n) = chi(n). Negation preserves QR/NQR.

NEGATION COMMUTES WITH THE 137-MAP:
  f(−n) = 26·(−n) = −26n = −f(n) (mod 37).
  If {n, 26n, 26²n} is an orbit, so is {−n, −26n, −26²n}.
  The negation map sends orbits to orbits.

NO SELF-DUAL ORBITS:
  An orbit {n,26n,26²n} is self-negating iff −n ∈ {n,26n,26²n},
  i.e., iff −1 ∈ {1, 26, 26²} = {1, 26, 10} = IDENTITY_CYCLE.
  −1 ≡ 36 ∉ {1,10,26}. Therefore no orbit is self-negating.
  All 12 orbits pair into 6 genuine negation-dual pairs.

SIX NEGATION-DUAL PAIRS (each summing to 111 = R(3) = 3×37 ≡ SEAM):
  [1,10,26] (sum=37)  ↔  [11,27,36] (sum=74)  — IDENTITY_CYCLE  ↔  ORBIT_11
  [2,15,20] (sum=37)  ↔  [17,22,35] (sum=74)  — DARK_A          ↔  {17,22,35}
  [3, 4,30] (sum=37)  ↔  [ 7,33,34] (sum=74)  — SOVEREIGN_SPIRAL ↔ ANTI-SOVEREIGN
  [5,13,19] (sum=37)  ↔  [18,24,32] (sum=74)  — {5,13,19}       ↔  SEED_ORBIT
  [6, 8,23] (sum=37)  ↔  [14,29,31] (sum=74)  — {6,8,23}        ↔  {14,29,31}
  [9,12,16] (sum=37)  ↔  [21,25,28] (sum=74)  — SOVEREIGN_2     ↔  OUTLIER_SOV

THEOREM: every pair sums (integer) to exactly 111 = R(3) = 3×37.
  Proof: {n, a, b} and {37−n, 37−a, 37−b}. Pairwise sums each equal 37. 3 pairs × 37 = 111. □

ORBIT_11 = NEGATION OF IDENTITY_CYCLE:
   1 + 36 = 37 ≡ SEAM.    (1 ↔ 36 = −1)
  10 + 27 = 37 ≡ SEAM.    (DECADE_ANCHOR ↔ 27 = −DECADE_ANCHOR)
  26 + 11 = 37 ≡ SEAM.    (SCALAR_137 ↔ 11 = −SCALAR_137)
  ORBIT_11 = {−1, −DECADE_ANCHOR, −SCALAR_137}.

ANTI-SOVEREIGN SPIRAL {7, 33, 34} = NEGATION OF {3, 4, 30}:
  −(SA∩ST=30) = 7.  −(SA=4) = 33.  −(ST=3) = 34.
  The orbit {7,33,34} is the additive mirror of the canonical sovereign spiral.
  Element-wise: {7,33,34} = {−SA∩ST, −SA_anchor, −ST_anchor}.

SOVEREIGN NEGATION PAIR — {9,12,16} ↔ {21,25,28}:
  SA(9) ↔ 28 (outlier).    9 + 28 = 37 ≡ SEAM.
  ST(12) ↔ 25 ∈ SA.        12 + 25 = 37 ≡ SEAM.
  ?(16) ↔ 21 ∈ ST.         16 + 21 = 37 ≡ SEAM.
  The two "incomplete" sovereign orbits are negation duals.
  Within the pair: SA↔outlier, ST↔SA, interior↔ST.

2×2 STRUCTURE — QR/NQR × sum37/sum74:
  QR  sum=37: {1,10,26}, {3,4,30},  {9,12,16}   — 3 orbits
  QR  sum=74: {7,33,34}, {11,27,36}, {21,25,28}  — 3 orbits
  NQR sum=37: {2,15,20}, {5,13,19},  {6,8,23}    — 3 orbits
  NQR sum=74: {14,29,31},{17,22,35}, {18,24,32}  — 3 orbits
  Each cell contains exactly 3 orbits. Each row is a negation-dual pair.

TOTAL RESIDUE SUM:
  1+2+…+36 = 36×37/2 = 666 = 18×37.
  By 2×2 structure: 6 orbits×37 + 6 orbits×74 = 222 + 444 = 666. ✓
  DR(666) = 6+6+6 = 18 → DR(18) = 9 ∈ SA.
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA           = frozenset({4, 9, 25, 30})
ST           = frozenset({3, 12, 21, 30})
CB           = frozenset({8, 13, 24})
PR           = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})
ORBIT_11     = frozenset({11, 27, 36})
DARK_A       = frozenset({2, 15, 20})
SEED_ORBIT   = frozenset({18, 24, 32})
OUTLIER_SOV  = frozenset({21, 25, 28})
TESLA_FLOW   = 6
SCALAR_137   = 26
DECADE_ANCHOR = 10
PRIME_MIRROR  = 31


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def f137(n):
    return (n * 26) % 37


def chi(n, p=37):
    n = n % p
    if n == 0: return 0
    return 1 if pow(n, (p - 1) // 2, p) == 1 else -1


# ── FOUNDATION: chi(-1) = 1 ──────────────────────────────────────────────────

assert chi(36) == 1      # chi(-1) = 1: negation is a QR
assert 37 % 4 == 1       # 37 ≡ 1 mod 4 is why

# Negation commutes with 137-map
for n in range(1, 37):
    assert f137(37 - n) == (37 - f137(n)) % 37


# ── BUILD ORBITS ──────────────────────────────────────────────────────────────

seen = set(); ORBITS = []
for s in range(1, 37):
    if s in seen: continue
    o = frozenset({s, f137(s), f137(f137(s))})
    assert f137(f137(f137(s))) == s
    ORBITS.append(o); seen |= o

assert len(ORBITS) == 12


# ── NO SELF-DUAL ORBITS ───────────────────────────────────────────────────────

IDENTITY_CYCLE = frozenset({1, 10, 26})
assert 36 not in IDENTITY_CYCLE   # −1 ∉ IDENTITY_CYCLE → no self-duals
for o in ORBITS:
    neg_o = frozenset((37 - x) % 37 for x in o)
    assert neg_o != o              # no orbit equals its own negation


# ── SIX NEGATION-DUAL PAIRS, EACH SUMMING TO 111 ─────────────────────────────

def neg_orbit(o):
    return frozenset((37 - x) % 37 for x in o)

paired = set()
PAIRS = []
for o in ORBITS:
    fo = frozenset(o)
    if fo in paired: continue
    no = neg_orbit(o)
    paired.add(fo); paired.add(no)
    PAIRS.append((fo, no))

assert len(PAIRS) == 6

for a, b in PAIRS:
    assert sum(a) + sum(b) == 111    # each pair sums to R(3) = 3×37
    assert (sum(a) + sum(b)) % 37 == 0


# ── SPECIFIC NAMED PAIRS ──────────────────────────────────────────────────────

# ORBIT_11 = negation of IDENTITY_CYCLE
assert neg_orbit(IDENTITY_CYCLE) == ORBIT_11
assert 1 + 36 == 37 and 10 + 27 == 37 and 26 + 11 == 37   # element-wise SEAM

# Anti-sovereign {7,33,34} = negation of canonical sovereign {3,4,30}
ANTI_SOVEREIGN = frozenset({7, 33, 34})
assert neg_orbit(frozenset({3, 4, 30})) == ANTI_SOVEREIGN
assert (37 - 30) == 7   # −SA∩ST
assert (37 -  4) == 33  # −SA_anchor
assert (37 -  3) == 34  # −ST_anchor

# Sovereign-2 {9,12,16} ↔ OUTLIER_SOV {21,25,28}
assert neg_orbit(frozenset({9, 12, 16})) == OUTLIER_SOV
assert 9 + 28 == 37 and 12 + 25 == 37 and 16 + 21 == 37

# DARK_A ↔ {17,22,35}
assert neg_orbit(DARK_A) == frozenset({17, 22, 35})

# SEED_ORBIT ↔ {5,13,19}
assert neg_orbit(SEED_ORBIT) == frozenset({5, 13, 19})

# {6,8,23} ↔ {14,29,31}
assert neg_orbit(frozenset({6, 8, 23})) == frozenset({14, 29, 31})


# ── 2×2 STRUCTURE: QR/NQR × SUM37/SUM74 ─────────────────────────────────────

for qr_val in [1, -1]:
    for sum_target in [37, 74]:
        cell = [o for o in ORBITS if chi(min(o)) == qr_val and sum(o) == sum_target]
        assert len(cell) == 3   # exactly 3 orbits in each cell

# QR sum-37 orbits are exactly IDENTITY_CYCLE, {3,4,30}, {9,12,16}
qr37 = [frozenset(o) for o in ORBITS if chi(min(o))==1 and sum(o)==37]
assert frozenset({1,10,26}) in qr37
assert frozenset({3,4,30})  in qr37
assert frozenset({9,12,16}) in qr37

# QR sum-74 = negations of QR sum-37
for o in qr37:
    assert neg_orbit(o) in [frozenset(x) for x in ORBITS if chi(min(x))==1 and sum(x)==74]


# ── TOTAL RESIDUE SUM ─────────────────────────────────────────────────────────

assert sum(range(1, 37)) == 666
assert 666 == 18 * 37
assert dr(666) == 9 and 9 in SA   # DR of total = SA element

# By 2×2: 6 orbits×37 + 6 orbits×74 = 666
assert 6 * 37 + 6 * 74 == 666


if __name__ == "__main__":
    print("Orbit Negation Duality — GF(37)")
    print("=" * 60)
    print(f"\nchi(−1) = chi(36) = {chi(36)}  (37≡1 mod 4)")
    print(f"Negation commutes with 137-map: f(−n)=−f(n) for all n")
    print(f"No self-dual orbits: −1=36 ∉ IDENTITY_CYCLE")
    print()
    print("SIX NEGATION-DUAL PAIRS (each → 111 = R(3) = 3×37):")
    for a, b in sorted(PAIRS, key=lambda p: min(min(p[0]),min(p[1]))):
        print(f"  {sorted(a)} sum={sum(a)}  ↔  {sorted(b)} sum={sum(b)}  total={sum(a)+sum(b)}")
    print()
    print("KEY PAIRINGS:")
    print(f"  IDENTITY_CYCLE → ORBIT_11 via negation")
    print(f"    1+36=37, 10+27=37, 26+11=37  (each ≡ SEAM)")
    print(f"  Canonical sovereign {{3,4,30}} → anti-sovereign {{7,33,34}}")
    print(f"    −(SA∩ST=30)=7,  −(SA=4)=33,  −(ST=3)=34")
    print(f"  Sovereign {{9,12,16}} ↔ OUTLIER {{21,25,28}}")
    print(f"    SA(9)↔28,  ST(12)↔SA(25),  16↔ST(21)")
    print()
    print("2×2 STRUCTURE (3 orbits per cell):")
    for qr_label, qr_val in [("QR ", 1), ("NQR", -1)]:
        for st in [37, 74]:
            cell = sorted([sorted(o) for o in ORBITS if chi(min(o))==qr_val and sum(o)==st])
            print(f"  {qr_label} sum={st}: {cell}")
    print()
    print(f"TOTAL: 1+2+…+36 = 666 = 18×37;  DR(666)={dr(666)}∈SA")
    print(f"  6×37 + 6×74 = {6*37}+{6*74} = 666 ✓")
    print()
    print("All assertions pass.")

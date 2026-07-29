"""
Kervaire Dimension Arithmetic on GF(37) and the Ghost Equation — THEOREM 81

KERVAIRE INVARIANT ONE: SETUP.
  Browder (1969): smooth framed manifolds with Kervaire invariant one can only
  exist in dimensions n = 2^j − 2 for integer j ≥ 2.
  Hill-Hopkins-Ravenel (2016): no such manifold exists for j ≥ 8 (i.e., n ≥ 254).
  Lin-Wang-Xu (2025): existence confirmed for j = 7 (n = 126), completing the picture.
  The complete existence set: n ∈ {2, 6, 14, 30, 62, 126} = {2^j − 2 : j = 2,...,7}.

GF(37) MOD-37 TABLE.
  j | 2^j mod 37 | framework   | n=2^j−2 mod 37 | framework | exists
  ──────────────────────────────────────────────────────────────────────
  2 |  4         | SA          |  2             | PR(base)  | YES
  3 |  8         | CB          |  6  TESLA_FLOW | T4        | YES
  4 | 16         | —           | 14             | 8^{−1}∈CB | YES
  5 | 32         | SEED_ORBIT  | 30             | SA∩ST jxn | YES
  6 | 27         | ORBIT_11    | 25             | SA        | YES
  7 | 17         | PR          | 15             | PR        | YES
  8 | 34         | —           | 32             | SEED_ORBIT| NO (excluded)

  Three of the six included exponents give 2^j ∈ named framework sets:
    j=3 → 2^3 = 8 ∈ CB          (cascade base)
    j=5 → 2^5 = 32 ∈ SEED_ORBIT (pipeline seed orbit)
    j=6 → 2^6 ≡ 27 ∈ ORBIT_11  (orbit-11 subgroup)
  The first excluded exponent (j=8) gives 2^8 ≡ 34 — non-framework.

FOUR ARITHMETIC STATISTICS (all hitting framework nodes mod 37).
  Sum of exponents:    2+3+4+5+6+7        = 27  ∈ ORBIT_11 = {11,27,36}
  Sum of dimensions:   2+6+14+30+62+126   = 240 ≡ 18 ∈ SEED_ORBIT = {18,24,32}
  Product of exponents: 2×3×4×5×6×7      = 7!  ≡  8 ∈ CB = {8,13,24}
  Product of dimensions: 2×6×14×30×62×126 mod 37 ≡  3 ∈ ST = {3,12,21,30}

  Mnemonic: the six Kervaire exponents (in their sum×product) encode ORBIT_11 and CB;
  the six dimensions (in their sum×product) encode SEED_ORBIT and ST.

7! ≡ 8 ∈ CB (mod 37).
  7! = 5040 = 136×37 + 8. The factorial of the largest Kervaire exponent (7)
  equals the smallest Cascade Base element (8) modulo the prime 37.
  This is consistent with Wilson's theorem (36! ≡ −1): the factorial 7!
  reduces to the CB anchor that generates the TESLA_FLOW orbit.

MUTUAL INVERSE: 8 ↔ 14 IN GF(37).
  8 ∈ CB (cascade base, first Kervaire exponent to hit a framework node via 2^3=8).
  14 = n at j=4 (the Kervaire dimension 14).
  8 × 14 = 112 = 3×37 + 1 ≡ 1 (mod 37):  8 and 14 are mutual inverses in GF(37)*.
  Every CB element (8,13,24) has a GF(37)-inverse. The inverse of 8 is the dimension 14.

FIRST EXCLUDED DIMENSION.
  j=8: n = 2^8 − 2 = 254. 254 mod 37 = 32 ∈ SEED_ORBIT.
  2^8 mod 37 = 34. ord(34) = 9 (order 9 in GF(37)*).
  The shift: at j=7 (last included), 2^7 ≡ 17 ∈ PR (order 36 = full primitive root).
  At j=8 (first excluded), 2^8 ≡ 34 (order 9, not in PR, not in any framework set).
  The SEED_ORBIT "transfer": 2^5 = 32 ∈ SEED_ORBIT (dimension j=5 exists);
  at j=8, the DIMENSION 254 ≡ 32 ∈ SEED_ORBIT (while 2^8 is non-framework).

GHOST EQUATION — GF(37) INTERPRETATION.
  From non-uniformly elliptic PDE theory (De Filippis-Mingioni): a "ghost equation"
  is an auxiliary linear constraint appended to the main equation to control
  unstable gradients — the part the main equation cannot bound alone.
  In GF(37), the THEOREM 79 solvability condition IS this ghost equation:

  Main equation:    (I−A)·x = b   [3-cycle process; det(I−A)=uvw−rst]
  Degenerate at:    uvw ≡ rst (mod 37)  [det=0; usual inverse fails]
  Ghost equation:   st·b_A + ut·b_B + uv·b_C ≡ 0 (mod 37)  [control the RHS b]

  When the ghost equation holds: the gradient b lies in a stable codimension-1
  hyperplane → a fixed line x(λ)=x₀+λ·v exists (the process stabilizes).
  When not: the gradient is UNSTABLE — no solution exists.

  The ghost equation selects exactly p² = 37² = 1369 stable b-vectors out of
  p³ = 37³ = 50,653 total — a fraction of 1/p = 1/37.
  The non-uniform ellipticity ratio: 1 in 37 right-hand sides is controllable.

SPECTRAL DIMENSION CHAIN.
  The sum of Kervaire dimensions 240 ≡ 18 ∈ SEED_ORBIT connects to THEOREM 77:
    666 = 18×37 = SEED_node × PRIME.
  The six-dimensional total (sum ≡ 18) echoes the role of 18 in the SEAM factorization:
  18 is the multiplier that generates the prime 37 from the triple-repdigit 666.
  The six allowed Kervaire dimensions collectively encode the SEED anchor of the pipeline.
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
IC         = frozenset({1, 10, 26})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
P          = 37
TESLA_FLOW = 6

# ── Kervaire dimensions ─────────────────────────────────────────────────────────

KERVAIRE_DIMS = [2**j - 2 for j in range(2, 8)]   # [2, 6, 14, 30, 62, 126]
KERVAIRE_EXPS = list(range(2, 8))                   # [2, 3, 4, 5, 6, 7]

assert KERVAIRE_DIMS == [2, 6, 14, 30, 62, 126]

# All dimensions are 2^j − 2 form (n+2 is a power of 2)
assert all((d + 2) & (d + 2 - 1) == 0 for d in KERVAIRE_DIMS)   # n+2 is power of 2

# ── Mod-37 table ────────────────────────────────────────────────────────────────

# j=2: 2^2=4∈SA, n=2∈PR
assert pow(2, 2, P) == 4 and 4 in SA
assert 2 % P == 2 and 2 in PR

# j=3: 2^3=8∈CB, n=6=TESLA_FLOW∈T4
assert pow(2, 3, P) == 8 and 8 in CB
assert (8 - 2) % P == 6 and 6 == TESLA_FLOW and TESLA_FLOW in TESLA_4

# j=4: 2^4=16 (non-framework), n=14; 14 is mutual inverse of 8∈CB
assert pow(2, 4, P) == 16 and 16 not in SA | ST | CB | ORBIT_11 | IC | SEED_ORBIT | TESLA_4 | PR
assert (16 - 2) % P == 14
assert (8 * 14) % P == 1   # 8∈CB and 14 are mutual inverses

# j=5: 2^5=32∈SEED_ORBIT, n=30∈SA∩ST
assert pow(2, 5, P) == 32 and 32 in SEED_ORBIT
assert (32 - 2) % P == 30 and 30 in SA and 30 in ST   # SA∩ST junction

# j=6: 2^6≡27∈ORBIT_11, n=25∈SA
assert pow(2, 6, P) == 27 and 27 in ORBIT_11
assert (27 - 2) % P == 25 and 25 in SA

# j=7: 2^7≡17∈PR, n=15∈PR
assert pow(2, 7, P) == 17 and 17 in PR
assert (17 - 2) % P == 15 and 15 in PR

# First excluded (j=8): 2^8≡34 (non-framework), n≡32∈SEED_ORBIT
assert pow(2, 8, P) == 34
assert 34 not in SA | ST | CB | ORBIT_11 | IC | SEED_ORBIT | TESLA_4 | PR
assert (34 - 2) % P == 32 and 32 in SEED_ORBIT

# ── Four arithmetic statistics ───────────────────────────────────────────────────

# Sum of exponents = 27 ∈ ORBIT_11
assert sum(KERVAIRE_EXPS) == 27 and 27 in ORBIT_11

# Sum of dimensions ≡ 18 ∈ SEED_ORBIT
assert sum(KERVAIRE_DIMS) == 240 and 240 % P == 18 and 18 in SEED_ORBIT

# Product of exponents = 7! ≡ 8 ∈ CB
import math
assert math.prod(KERVAIRE_EXPS) == math.factorial(7) == 5040
assert 5040 % P == 8 and 8 in CB

# Product of dimensions ≡ 3 ∈ ST
_prod_dims = math.prod(d % P for d in KERVAIRE_DIMS) % P
assert _prod_dims == 3 and 3 in ST

# ── Mutual inverse: 8 ↔ 14 ─────────────────────────────────────────────────────

assert (8 * 14) % P == 1     # mutual inverses in GF(37)*
assert 8 in CB               # 8 is cascade base
assert 14 == KERVAIRE_DIMS[2]  # 14 is the j=4 Kervaire dimension

# ── Orders of 2^j ──────────────────────────────────────────────────────────────

# ord(2^7=17) = 36 (primitive root) — last included
_ord17 = next(o for o in range(1, P) if pow(17, o, P) == 1)
assert _ord17 == 36 and 17 in PR

# ord(2^8=34) = 9 (drops from primitive root) — first excluded
_ord34 = next(o for o in range(1, P) if pow(34, o, P) == 1)
assert _ord34 == 9

# The order drop at j=8: primitive root (36) → order 9
assert _ord17 == 36 > 9 == _ord34

# ── Ghost equation (THEOREM 79 solvability) ────────────────────────────────────

# Ghost equation: st·b_A + ut·b_B + uv·b_C ≡ 0 (mod 37)
# Exactly 37² stable b-vectors; fraction = 1/37
assert P ** 2 == 1369                   # ghost-stable count
assert P ** 3 == 50653                  # total b-vectors
# Fraction 1/37: for each fixed (s,t,u,v), exactly p^2 of p^3 b-vectors are stable
_s, _t, _u, _v = 3, 5, 2, 4
_stable = sum(
    1 for bA in range(P) for bB in range(P) for bC in range(P)
    if (_s*_t*bA + _u*_t*bB + _u*_v*bC) % P == 0
)
assert _stable == P ** 2

# ── SEED connection: 18×37 = 666 = SEAM-generator ──────────────────────────────

assert sum(KERVAIRE_DIMS) % P == 18
assert 18 * P == 666      # 18 is SEED_ORBIT node; 666 = SEED×PRIME (THEOREM 77)
assert 666 % P == 0       # SEAM
assert 18 in SEED_ORBIT


if __name__ == "__main__":
    print("Kervaire Dimension Arithmetic on GF(37) and the Ghost Equation — THEOREM 81")
    print("=" * 72)
    print()
    print("KERVAIRE DIMENSIONS: {2^j − 2 : j = 2,...,7}")
    print()
    print(f"{'j':>2} | {'2^j mod 37':>10} | {'framework':>10} | {'n mod 37':>8} | {'framework':>10} | exists")
    print(f"{'─'*2}-+-{'─'*10}-+-{'─'*10}-+-{'─'*8}-+-{'─'*10}-+-------")
    def fw(n):
        for s,name in [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),
                       (IC,'IC'),(SEED_ORBIT,'SEED'),(TESLA_4,'T4'),(PR,'PR')]:
            if n in s: return name
        return '—'
    for j in range(2, 9):
        p2 = pow(2, j, P)
        n = (p2 - 2) % P
        ex = 'YES' if j <= 7 else 'NO (excl.)'
        print(f"{j:>2} | {p2:>10} | {fw(p2):>10} | {n:>8} | {fw(n):>10} | {ex}")
    print()
    print("FOUR ARITHMETIC STATISTICS:")
    print(f"  Sum of exponents   (2+3+4+5+6+7)       = {sum(KERVAIRE_EXPS):5} ∈ ORBIT_11")
    print(f"  Sum of dimensions  (2+6+14+30+62+126)   = {sum(KERVAIRE_DIMS):5} ≡ 18 ∈ SEED_ORBIT (mod 37)")
    print(f"  Product of exponents (2×3×4×5×6×7 = 7!) = {5040:5} ≡  8 ∈ CB (mod 37)")
    print(f"  Product of dimensions                    = ... ≡  3 ∈ ST (mod 37)")
    print()
    print("MUTUAL INVERSE: 8∈CB × 14(dim) ≡ 1 (mod 37)")
    print()
    print("GHOST EQUATION (THEOREM 79 solvability):")
    print(f"  Stable b-vectors: p² = {P**2} out of p³ = {P**3}  (fraction = 1/{P})")
    print(f"  Constraint: st·b_A + ut·b_B + uv·b_C ≡ 0 (mod {P})")
    print()
    print("SEED CONNECTION:")
    print(f"  Sum(Kervaire dims) = 240 ≡ 18 ∈ SEED_ORBIT (mod {P})")
    print(f"  18 × {P} = {18*P} = 666 = SEAM-generator (THEOREM 77)")
    print()
    print("All assertions pass.")

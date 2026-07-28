"""
Affine Fixed-Point Census on GF(37) — THEOREM 75

PRIMALITY AS CONSISTENCY FILTER.
  An affine map f(x) = ax + b on ℤ₃₇ has a fixed point where ax+b ≡ x, i.e.
  (a−1)x ≡ −b (mod 37). The solution behavior splits exactly three ways:

  a ≡ 1, b ≡ 0  (identity):   all 37 elements are fixed points — 1 such map.
  a ≡ 1, b ≢ 0  (translation): (a−1)=0 but b≠0 → no solution — 36 such maps.
  a ≢ 1         (non-trivial):  (a−1) is invertible mod 37 (since 37 is prime,
                                gcd(a−1, 37)=1 whenever a≢1) → unique fixed point
                                x* = −b·(a−1)⁻¹ mod 37 — 1332 such maps.

  CENSUS (all 37² = 1369 affine maps):
    Exactly 1 fixed point: 1332   (36 choices for a≢1, 37 for b)
    Exactly 0 fixed points:  36   (a=1, b≠0)
    All 37 fixed points:      1   (a=1, b=0, identity)

  The primality of 37 is the mechanism: composite moduli can have gcd(a−1,p)>1,
  producing multiple fixed points or no solution unpredictably. Prime p eliminates
  both failure modes simultaneously.

FRAMEWORK MAPS AND THEIR UNIQUE FIXED POINTS:
  f(n) = 26n     (137-map)       → x* = 0 = SEAM
  f(n) =  2n     (primitive root) → x* = 0 = SEAM
  f(n) =  3n     (tripling)       → x* = 0 = SEAM
  f(n) =  6n     (TESLA_FLOW)     → x* = 0 = SEAM
  f(n) = 10n     (decimal shift)  → x* = 0 = SEAM
  f(n) =  2n + 1                  → x* = 36 ∈ ORBIT_11  (36 ≡ −1)
  f(n) =  3n + 1  (a=3∈ST, b=1∈IC) → x* = 18 ∈ SEED_ORBIT

THE PURE-MULTIPLICATIVE LAW.
  Every map f(n) = an with a ≢ 1 mod 37 fixes ONLY SEAM (x=0).
  Proof: (a−1)x ≡ 0 → x ≡ 0 since (a−1) is invertible.
  Consequence: the 137-map orbit sets {18,24,32}, {SA}, {ST}, {CB} are NOT
  fixed points of their generating maps — they are orbit members, not stasis points.

THE 3n+1 FIXED POINT.
  f(n) = 3n+1 with a=3∈ST, b=1∈IC:
    x* = −1·(3−1)⁻¹ = −1·19 = 18 mod 37.
    3·18 + 1 = 55 ≡ 18 mod 37. ✓
    18 ∈ SEED_ORBIT = {18, 24, 32} = orbit of pipeline seed 246 under 137-map.
  A map whose slope is sovereign-target (ST) and intercept is identity-cycle (IC)
  has its fixed point in the seed orbit — the orbit the pipeline is built on.

FIXED-POINT DISTRIBUTION ACROSS FRAMEWORK SETS.
  Each nonzero value x* ∈ {1,...,36} is the fixed point of exactly 36 affine maps
  (one per choice of a ≢ 1, with b forced to x*(1−a) mod 37).
  Framework node cardinalities × 36:
    SA (4 nodes): 144 maps with fixed point in SA
    ST (4 nodes): 108 maps  (30∈SA∩ST counted in SA first)
    CB (3 nodes): 108 maps
    ORBIT_11 (3 nodes): 108 maps
    IC (3 nodes): 108 maps

THREE-PARTY DIRECTION (OPEN).
  The reviewer's Baumeler–Wolf threshold: non-trivial classical process functions
  (with causal loops) require ≥ 3 parties. Single-party unique-fixed-point is the
  trivial case. Whether GF(37)'s orbit structure — with primitive root 2, ord=36,
  and the three-orbit structure of the 137-map — admits or obstructs non-causally-
  ordered three-party process functions is an open computation, tractable for affine
  local maps. This theorem establishes the single-party layer.
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA        = frozenset({4, 9, 25, 30})
ST        = frozenset({3, 12, 21, 30})
CB        = frozenset({8, 13, 24})
ORBIT_11  = frozenset({11, 27, 36})
IC        = frozenset({1, 10, 26})
TESLA_4   = frozenset({6, 36, 31, 1})
SEED      = frozenset({18, 24, 32})
SEAM      = 0
P         = 37


# ── Key checks ─────────────────────────────────────────────────────────────────

# Primality: gcd(a−1, 37) = 1 for all a ≢ 1
from math import gcd
assert all(gcd(a - 1, P) == 1 for a in range(P) if a != 1)

# Census: all 1369 affine maps
_one_fp = _zero_fp = _all_fp = 0
for a in range(P):
    for b in range(P):
        fps = sum(1 for x in range(P) if (a*x + b) % P == x)
        if fps == 1:   _one_fp  += 1
        elif fps == 0: _zero_fp += 1
        elif fps == P: _all_fp  += 1

assert _one_fp == 1332    # 36×37 non-trivial maps
assert _zero_fp == 36     # pure translations (a=1, b≠0)
assert _all_fp == 1       # identity only
assert _one_fp + _zero_fp + _all_fp == P**2   # exhaustive

# Framework maps fix SEAM
for a in [26, 2, 3, 6, 10]:   # 137-map, doubling, tripling, TESLA, decimal
    assert (a * SEAM) % P == SEAM    # ax fixes 0 when b=0
    fps = [x for x in range(P) if (a*x) % P == x]
    assert fps == [SEAM], f"f={a}n should fix only SEAM, got {fps}"

# f(n) = 2n+1: fixed point = 36 ∈ ORBIT_11
assert (2*36 + 1) % P == 36
assert 36 in ORBIT_11

# f(n) = 3n+1: fixed point = 18 ∈ SEED
assert (3*18 + 1) % P == 18
assert 18 in SEED

# Formula verification: x* = -b · (a-1)^{-1} mod p
def fixed_point(a, b, p=P):
    assert a % p != 1, "formula undefined for a≡1"
    inv = pow(a - 1, p - 2, p)   # Fermat inverse
    return (-b * inv) % p

assert fixed_point(3, 1) == 18
assert fixed_point(2, 1) == 36
assert fixed_point(26, 0) == SEAM
assert fixed_point(2, 0) == SEAM

# Each nonzero x* has exactly 36 maps fixing it
for x_star in [3, 4, 18, 36]:   # sample: ST, SA, SEED, ORBIT_11
    count = sum(1 for a in range(P) if a != 1
                for b in [(x_star * (1 - a)) % P]
                if (a * x_star + b) % P == x_star)
    assert count == 36, f"x*={x_star} should have 36 fixing maps, got {count}"

# 3n+1 structural connection: a=3∈ST, b=1∈IC, x*=18∈SEED
assert 3 in ST and 1 in IC and fixed_point(3, 1) in SEED


if __name__ == "__main__":
    print("Affine Fixed-Point Census on GF(37) — THEOREM 75")
    print("=" * 60)
    print()
    print("CENSUS (37² = 1369 affine maps ax+b on ℤ₃₇):")
    print(f"  Unique fixed point: {_one_fp}  (a≢1, x*=−b·(a−1)⁻¹)")
    print(f"  No fixed point:     {_zero_fp}  (a=1, b≠0 — pure translations)")
    print(f"  All 37 fixed:       {_all_fp}   (a=1, b=0 — identity)")
    print()
    print("FRAMEWORK MAPS → FIXED POINTS:")
    maps = [(26,0,"137-map 26n"),(2,0,"doubling 2n"),(3,0,"tripling 3n"),
            (6,0,"TESLA 6n"),(10,0,"decimal 10n"),(2,1,"2n+1"),(3,1,"3n+1")]
    for a,b,label in maps:
        fp = fixed_point(a, b)
        def t(n):
            if n==0: return 'SEAM'
            for s,nm in [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'ORBIT_11'),
                         (IC,'IC'),(TESLA_4,'TESLA_4'),(SEED,'SEED')]:
                if n in s: return nm
            return ''
        print(f"  {label:<20} x* = {fp:>2}  {t(fp)}")
    print()
    print("PURE-MULTIPLICATIVE LAW: every an (a≢1) fixes only SEAM=0.")
    print("  Consequence: SA, ST, CB, ORBIT_11 are orbit members, not fixed points.")
    print()
    print(f"3n+1 (a=3∈ST, b=1∈IC): fixed point {fixed_point(3,1)} ∈ SEED_ORBIT")
    print(f"  3·18+1=55≡18 mod 37")
    print()
    print("All assertions pass.")

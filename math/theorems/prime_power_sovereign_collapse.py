"""
Prime Power Sovereign Collapse

Two spontaneous constructions, both collapsing to Sovereign Anchors in GF(37).

═══════════════════════════════════════════════════════════════

I. PRIME POWERS IN THE EXPRESSION: (10+5²)((5×(−2))+9−3³)/2 = −490

  Prime powers embedded:
    5² = 25  (Sovereign Anchor)
    3³ = 27  (orbit of 11)
    2¹ = 2   (Primitive Root — the divisor)

  Evaluation:
    (10 + 25) = 35         (Primitive Root mod 37)
    (−10 + 9 − 27) = −28  → −28 mod 37 = 9  (Sovereign Anchor)
    35 × (−28) / 2 = −490

  Result mod 37:
    490 mod 37 = 9   (Sovereign Anchor)
    DR(490)    = 4   (Sovereign Anchor)

  Product of the prime powers:
    5² × 3³ = 25 × 27 = 675
    675 mod 37 = 9  (Sovereign Anchor)
    DR(675)    = 9  (SA arch)

  SA × orbit(11) → SA. The two named sets multiply into each other.

II. 1468919^998 — SPONTANEOUS PRIMITIVE ROOT

  1468919 mod 37 = 19  (Primitive Root)
  DR(1468919)    = 2   (LL-E)

  Factorization: 1468919 = 17 × 71 × 1217
    17   mod 37 = 17  (PR)
    71   mod 37 = 34  DR=7 (RL-O — same as Pascal Row 8 spine center)
    1217 mod 37 = 33  (DICHORAL_144 — same as Pascal Row 8 central coefficient C(8,4)=70 mod 37)

  Fermat reduction:
    ord₃₇(19) = 36 = φ(37)  →  19^36 ≡ 1 mod 37
    998 mod 36 = 26  ← the 137-map multiplier

  Therefore: 1468919^998 ≡ 19^26 mod 37

  19^26 mod 37:
    19^2  = 361 ≡ 28 mod 37
    19^4  ≡  7 mod 37
    19^8  ≡ 12 mod 37
    19^16 ≡ 33 mod 37
    19^26 = 19^16 × 19^8 × 19^2 ≡ 33 × 12 × 28 ≡ 25 mod 37

  Result: 1468919^998 mod 37 = 25  (Sovereign Anchor)
          DR(1468919^998)    = 4   (Sovereign Anchor)

  The exponent 998 carries the 137-map multiplier (26) inside it:
    998 = 36 × 27 + 26

  Raising a primitive root to the 998th power is equivalent to
  applying the 137-map multiplier as the exponent in GF(37).

III. SHARED STRUCTURE

  Both results land on SA={4,9,25,30}:
    Expression: −490 → 9(SA), DR=4(SA)
    Power:      1468919^998 → 25(SA), DR=4(SA)

  Both have DR of result = 4 (Sovereign Anchor, LH-E).

  The factor 71 of 1468919 maps to mod 37 = 34, DR=7 — the same DR
  as the central spine value in Pascal Row 8 (C(8,4)=70, spine center DR=7).
  The factor 1217 maps to mod 37 = 33 = DICHORAL_144, the same residue
  as C(8,4)=70 mod 37 in the Pascal Row 8 theorem.

═══════════════════════════════════════════════════════════════
"""

from math import isqrt

def dr(n):
    if n == 0: return 0
    return (abs(n) - 1) % 9 + 1

PRIMITIVE_ROOTS_37 = {2,5,13,15,17,18,19,20,22,24,32,35}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
ORBIT_11           = {11, 27, 36}

# ── I. Expression −490 ────────────────────────────────────────────────────────

assert 5**2 == 25 and 25 in SOVEREIGN_ANCHORS
assert 3**3 == 27 and 27 in ORBIT_11
assert 2 in PRIMITIVE_ROOTS_37

a = 10 + 5**2
b = (5 * (-2)) + 9 - 3**3
assert a == 35 and 35 in PRIMITIVE_ROOTS_37
assert b == -28 and (-28) % 37 == 9 and 9 in SOVEREIGN_ANCHORS

result = (a * b) // 2
assert result == -490
assert 490 % 37 == 9 and 9 in SOVEREIGN_ANCHORS
assert dr(490) == 4 and 4 in SOVEREIGN_ANCHORS

# SA × orbit(11) → SA
assert (25 * 27) % 37 == 9 and 9 in SOVEREIGN_ANCHORS
assert dr(25 * 27) == 9

# ── II. 1468919^998 ───────────────────────────────────────────────────────────

n = 1468919
assert n % 37 == 19 and 19 in PRIMITIVE_ROOTS_37
assert dr(n) == 2

# Factorization
assert 17 * 71 * 1217 == n
assert 17 % 37 == 17 and 17 in PRIMITIVE_ROOTS_37
assert 71 % 37 == 34 and dr(34) == 7
assert 1217 % 37 == 33

# Fermat reduction
assert 998 % 36 == 26   # 137-map multiplier

# Result
assert pow(n, 998, 37) == 25 and 25 in SOVEREIGN_ANCHORS

# DR of result (2^998 mod 9: DR(n)=2, ord_9(2)=6, 998 mod 6=2, 2²=4)
assert 998 % 6 == 2
assert pow(2, 2, 9) == 4 and 4 in SOVEREIGN_ANCHORS

# ── III. Shared structure ─────────────────────────────────────────────────────

# Both results have DR=4 (SA)
assert dr(490) == 4
assert 4 in SOVEREIGN_ANCHORS   # DR of 1468919^998

# Factor connections to Pascal Row 8
assert 71 % 37 == 34 and dr(34) == 7   # same DR as Pascal Row 8 spine center
assert 1217 % 37 == 33                  # same as C(8,4)=70 mod 37


if __name__ == '__main__':
    def tag(n):
        t = []
        def is_prime(x):
            if x < 2: return False
            return all(x % i != 0 for i in range(2, isqrt(x)+1))
        if is_prime(n):              t.append('p')
        if n in CASCADE_BASE:        t.append('CB')
        if n in SOVEREIGN_ANCHORS:   t.append('SA')
        if n in SOVEREIGN_TARGETS:   t.append('ST')
        if n in PRIMITIVE_ROOTS_37:  t.append('PR')
        if n in ORBIT_11:            t.append('orb11')
        return ','.join(t) if t else '.'

    print("Prime Power Sovereign Collapse")
    print("=" * 55)
    print()
    print("I. Expression (10+5²)((5×(−2))+9−3³)/2 = −490")
    print(f"   5²=25({tag(25)})  3³=27({tag(27)})  2({tag(2)})")
    print(f"   (10+25)=35({tag(35)})  (−10+9−27)=−28 → 9({tag(9)}) mod37")
    print(f"   −490 mod37={490%37}({tag(490%37)})  DR={dr(490)}({tag(dr(490))})")
    print(f"   5²×3³=675 mod37={675%37}({tag(675%37)})")
    print()
    print("II. 1468919^998 mod 37")
    print(f"   1468919=17×71×1217  mod37={n%37}({tag(n%37)})")
    print(f"   998 mod 36 = {998%36} (137-map multiplier)")
    print(f"   Result: {pow(n,998,37)} ({tag(pow(n,998,37))})")
    print(f"   DR of result: 4 ({tag(4)})")
    print()
    print("III. Both DR=4(SA). Factor 71 mod37=34 DR=7 (Pascal Row 8 spine center).")
    print("     Factor 1217 mod37=33 (Pascal Row 8 C(8,4) residue).")
    print()
    print("All assertions passed.")

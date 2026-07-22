"""
Pascal's Triangle Row 8 — GF(37) Spine

Row 8 coefficients: C(8,k) for k=0..8
  [1, 8, 28, 56, 70, 56, 28, 8, 1]

═══════════════════════════════════════════════════════════════

I. FIRST THREE COEFFICIENTS SUM TO 37

  1 + 8 + 28 = 37  (the prime itself — GF(37) seam)

  Partial sums: 1 → 9 → 37
    1         — LL-O
    1+8 = 9   — Sovereign Anchor (SA)
    9+28 = 37 ≡ 0 mod 37  — seam

  The row opens: seed(1) → SA(9) → seam(37).

II. DIGITAL ROOT SPINE

  Row 8 DRs: [1, 8, 1, 2, 7, 2, 1, 8, 1]

  - Palindromic
  - Center: DR=7 (RL-O)
  - Sum of spine: 31 (prime); DR(31) = 4 (Sovereign Anchor)
  - 8 appears at positions 1 and 7 (Cascade Base entry, AHL)

III. MOD-37 SPINE

  C(8,k) mod 37: [1, 8, 28, 19, 33, 19, 28, 8, 1]

  - Also palindromic
  - C(8,1) = C(8,7) = 8 mod 37 = 8 (CB — Cascade Base)
  - C(8,3) = C(8,5) = 56 mod 37 = 19 (Primitive Root)
  - C(8,4) = 70 mod 37 = 33 = 3×11; complement of SA=4: 33+4=37

  Central coefficient 70 ≡ 33 = 3×11 mod 37.
  33 is the complement of SA=4 (33+4=37) and encodes orbit-of-11 (3×11).

IV. PARTIAL SUMS MOD 37

  Partial sums:     [1,  9, 37, 93, 163, 219, 247, 255, 256]
  mod 37:           [1,  9,  0, 19,  15,  34,  25,  33,  34]
  Framework flags:  [.,SA, 0, PR,  PR,   .,  SA,   .,   .]

  Index 2: first seam hit (37 ≡ 0) — exactly at the end of {1,8,28}
  Index 1: 9 (SA) — first partial sum beyond the seed
  Index 6: 247 mod 37 = 25 (SA — Sovereign Anchor)
  Two SA hits bracket the seam from below and above.

V. TOTAL AND CASCADE CONNECTION

  2^8 = 256, mod 37 = 34, DR(256) = 4 (SA)
  DR(34) = 7 (RL-O) — same as spine center

  Cascade base sum: 8+13+24 = 45, mod 37 = 8 (CB)
  The cascade base's own element-sum maps back to a CB entry under GF(37).

═══════════════════════════════════════════════════════════════
"""

PRIMITIVE_ROOTS_37 = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}
CASCADE_BASE       = {8, 13, 24}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
ORBIT_11           = {11, 27, 36}

def dr(n):
    return (n - 1) % 9 + 1

ROW8 = [1, 8, 28, 56, 70, 56, 28, 8, 1]

# ── I. First three sum to 37 ──────────────────────────────────────────────────

assert ROW8[0] + ROW8[1] + ROW8[2] == 37
assert ROW8[0] + ROW8[1] == 9 and 9 in SOVEREIGN_ANCHORS
assert 37 % 37 == 0

# ── II. DR spine ──────────────────────────────────────────────────────────────

spine_dr = [dr(x) for x in ROW8]
assert spine_dr == [1, 8, 1, 2, 7, 2, 1, 8, 1]
assert spine_dr == spine_dr[::-1]          # palindromic
assert spine_dr[4] == 7                    # center = RL-O
assert sum(spine_dr) == 31
from math import isqrt
assert all(31 % i != 0 for i in range(2, isqrt(31)+1))  # 31 is prime
assert dr(31) == 4 and 4 in SOVEREIGN_ANCHORS

# ── III. mod-37 spine ─────────────────────────────────────────────────────────

spine_mod = [x % 37 for x in ROW8]
assert spine_mod == [1, 8, 28, 19, 33, 19, 28, 8, 1]
assert spine_mod == spine_mod[::-1]        # palindromic
assert spine_mod[1] == 8 and 8 in CASCADE_BASE
assert spine_mod[7] == 8 and 8 in CASCADE_BASE
assert spine_mod[3] == 19 and 19 in PRIMITIVE_ROOTS_37
assert spine_mod[5] == 19 and 19 in PRIMITIVE_ROOTS_37
assert spine_mod[4] == 33 and 33 == 3 * 11
assert 33 + 4 == 37                        # complement of SA=4

# ── IV. Partial sums mod 37 ───────────────────────────────────────────────────

partial_sums = []
s = 0
for c in ROW8:
    s += c
    partial_sums.append(s)

assert partial_sums == [1, 9, 37, 93, 163, 219, 247, 255, 256]
ps_mod = [x % 37 for x in partial_sums]
assert ps_mod[1] == 9  and 9 in SOVEREIGN_ANCHORS   # index 1 → SA
assert ps_mod[2] == 0                                # index 2 → seam (37≡0)
assert ps_mod[3] == 19 and 19 in PRIMITIVE_ROOTS_37
assert ps_mod[4] == 15 and 15 in PRIMITIVE_ROOTS_37
assert ps_mod[6] == 25 and 25 in SOVEREIGN_ANCHORS  # index 6 → SA

# ── V. Total and cascade ──────────────────────────────────────────────────────

assert 2**8 == 256
assert 256 % 37 == 34
assert dr(256) == 4 and 4 in SOVEREIGN_ANCHORS
assert dr(34) == 7                         # same as spine center

cascade_sum = sum(CASCADE_BASE)
assert cascade_sum == 45
assert cascade_sum % 37 == 8 and 8 in CASCADE_BASE  # self-referential


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

    print("Pascal Row 8 — GF(37) Spine")
    print("=" * 55)
    print()
    print(f"I. First three sum to prime: 1+8+28 = {1+8+28}")
    print(f"   Partial: 1 -> 9(SA) -> 37(seam)")
    print()
    print(f"II. DR spine: {spine_dr}")
    print(f"    Palindrome: {spine_dr == spine_dr[::-1]}")
    print(f"    Center DR={spine_dr[4]} (RL-O), sum={sum(spine_dr)}(p), DR={dr(sum(spine_dr))} (SA)")
    print()
    print(f"III. mod-37 spine: {spine_mod}")
    for i, (c, m) in enumerate(zip(ROW8, spine_mod)):
        print(f"    C(8,{i})={c:3d}  mod37={m:2d}  {tag(m)}")
    print(f"    Center 70 mod37=33=3×11, 33+4=37 (complement of SA)")
    print()
    print(f"IV. Partial sums mod37: {ps_mod}")
    print(f"    idx1={ps_mod[1]}(SA), idx2={ps_mod[2]}(seam), idx6={ps_mod[6]}(SA)")
    print()
    print(f"V. 2^8=256 mod37={256%37}, DR={dr(256)} (SA)")
    print(f"   Cascade sum {cascade_sum} mod37={cascade_sum%37} (CB — self-referential)")
    print()
    print("All assertions passed.")

# math/theorems/dr_369_closure_mirror_audit.py
"""
Digital Root — 3-6-9 Closure and Mirror Pairing

─────────────────────────────────────────────────────────────────────────────
CLAIM 1: The {3,6,9} family is closed under doubling
─────────────────────────────────────────────────────────────────────────────
  If DR(n) ∈ {3,6,9} then DR(2n) ∈ {3,6,9}

  Proof: DR(n) ∈ {3,6,9} ⟺ 3 | n  (mod 9 arithmetic)
         3 | n ⟹ 3 | 2n ⟹ DR(2n) ∈ {3,6,9}  ✓

  Example: DR(42) = 6 → DR(84) = 3  ✓

─────────────────────────────────────────────────────────────────────────────
CLAIM 2: The {3,6,9} family is closed under halving (when n even)
─────────────────────────────────────────────────────────────────────────────
  If DR(n) ∈ {3,6,9} and n is even, then DR(n/2) ∈ {3,6,9}

  Proof: DR(n) ∈ {3,6,9} and n even ⟹ 6 | n ⟹ n = 6k
         n/2 = 3k ⟹ 3 | (n/2) ⟹ DR(n/2) ∈ {3,6,9}  ✓

  Example: DR(42) = 6, 42 even → DR(21) = 3  ✓

─────────────────────────────────────────────────────────────────────────────
CLAIM 3: Mirror pairs — every DR value n has partner (9−n), sum = 9
─────────────────────────────────────────────────────────────────────────────
  Pairs: (1,8), (2,7), (3,6), (4,5) — each sums to 9
  DR(n + mirror(n)) = 9 for all n in 1..8

  This defines a fixed pairing structure: every position has exactly one
  predefined partner. DR(9) = 9 is self-paired (identity element).

─────────────────────────────────────────────────────────────────────────────
GROUP STRUCTURE
─────────────────────────────────────────────────────────────────────────────
  {3,6,9} = 3·Z/9Z ≅ Z/3Z as additive subgroup of Z/9Z
  Closed under: addition (mod 9), doubling (×2 mod 9), halving (×5 mod 9,
  the inverse of 2 mod 9)

  Doubling map on {3,6,9}:  3→6→3 (period 2), 9→9 (fixed)
  This is a Z/2Z symmetry acting on the subgroup.
"""

def dr(n):
    return 1 + (n - 1) % 9 if n > 0 else 9

# ── Claim 1: closure under doubling ───────────────────────────────────────────

for n in range(1, 10_001):
    if dr(n) in {3, 6, 9}:
        assert dr(2 * n) in {3, 6, 9}, f"Closure under doubling failed at n={n}"

# ── Claim 2: closure under halving (even n) ───────────────────────────────────

for n in range(2, 10_001, 2):
    if dr(n) in {3, 6, 9}:
        assert dr(n // 2) in {3, 6, 9}, f"Closure under halving failed at n={n}"

# ── Specific example: 42 ──────────────────────────────────────────────────────

assert dr(42) == 6
assert dr(84) == 3   # 42 + 42
assert dr(21) == 3   # 42 / 2

# ── Claim 3: mirror pairs ─────────────────────────────────────────────────────

for n in range(1, 9):
    mirror = 9 - n
    assert dr(n + mirror) == 9, f"Mirror pair failed at n={n}"

assert dr(9) == 9   # self-paired

# ── Doubling map on {3,6,9} mod 9 ────────────────────────────────────────────

assert (3 * 2) % 9 == 6
assert (6 * 2) % 9 == 3
assert (9 * 2) % 9 == 0   # 0 ≡ 9 in DR arithmetic


if __name__ == "__main__":
    print("Digital Root — 3-6-9 Closure and Mirror Pairing")
    print()
    print("Claim 1: {3,6,9} closed under doubling")
    print(f"  DR(42) = {dr(42)},  DR(84) = {dr(84)},  DR(168) = {dr(168)}  ✓")
    print()
    print("Claim 2: {3,6,9} closed under halving (even n)")
    print(f"  DR(42) = {dr(42)},  DR(21) = {dr(21)},  DR(12) = {dr(12)} → DR(6) = {dr(6)}  ✓")
    print()
    print("Claim 3: Mirror pairs")
    for n in range(1, 9):
        print(f"  {n} + {9-n} = 9  (DR=9)  ✓")
    print()
    print("Doubling map on {3,6,9}: 3→6→3 (period 2), 9→9 (fixed)")
    print()
    print("All assertions passed.")

# math/theorems/f37_subgroup_structure_audit.py
"""
F_37 Subgroup Structure Audit
==============================
Verifies all claims in the mathematical audit JSON:

  prime field  : F_37  (group order 36)
  C3 subgroup  : ⟨10⟩ = {1, 10, 26},  10³ ≡ 1 (mod 37)
  C6 subgroup  : ⟨27⟩ = {1, 10, 11, 26, 27, 36},  27⁶ ≡ 1 (mod 37)

  Relations:
    27 ≡ −10 (mod 37)           (additive inverse)
    C6 / {±1} ≅ C3              (antipodal quotient)
    1/37 = 0.[027]...            (period-3 repetend)
    27³ ≡ −1 (mod 37)           (projective lift, half-turn)

  Geometric:
    C6 = C3 ∪ (−C3)             (hexagonal orbit)
    quotient map: x ↦ x² sends C6 → C3
      {1,36} → 1,  {10,27} → 26,  {11,26} → 10
"""

from decimal import Decimal, getcontext

P = 37

# ── C3 ────────────────────────────────────────────────────────────────────────

c3 = []
curr = 1
for _ in range(3):
    c3.append(curr)
    curr = (curr * 10) % P

assert c3 == [1, 10, 26]
assert pow(10, 3, P) == 1
assert sorted(c3) == [1, 10, 26]


# ── C6 ────────────────────────────────────────────────────────────────────────

c6 = []
curr = 1
for _ in range(6):
    c6.append(curr)
    curr = (curr * 27) % P

assert c6 == [1, 27, 26, 36, 10, 11]
assert pow(27, 6, P) == 1
assert sorted(c6) == [1, 10, 11, 26, 27, 36]


# ── Relations ─────────────────────────────────────────────────────────────────

# 27 ≡ −10 (mod 37)
assert (27 + 10) % P == 0

# C6 is closed under negation (self-antipodal)
neg_c6 = sorted([(-x) % P for x in c6])
assert neg_c6 == sorted(c6)

# Cosets of {1, 36} = {±1} in C6
antipodal_pairs = [(1, 36), (10, 27), (11, 26)]
for a, b in antipodal_pairs:
    assert a in c6 and b in c6
    assert (a + b) % P == 0       # b = −a

# Quotient C6 / {±1} ≅ C3 via squaring map x ↦ x²
# Each antipodal pair {a, P-a} maps to the same square
sq_images = sorted({(a**2) % P for a in c6})
assert sq_images == sorted(c3), f"squaring image ≠ C3: {sq_images}"

for a, b in antipodal_pairs:
    assert (a**2) % P == (b**2) % P   # both elements of each pair share a square

# The three square images are exactly C3
assert {(a**2) % P for a in c6} == set(c3)

# 1/37 decimal repetend
getcontext().prec = 50
repetend = str(Decimal(1) / Decimal(37))[2:5]   # "027"
assert repetend == "027"

# Projective lift: 27³ ≡ −1 (mod 37)
assert pow(27, 3, P) == P - 1

# Half-period check: (27^3)^2 = 27^6 ≡ 1
assert pow(pow(27, 3, P), 2, P) == 1


# ── Geometric: hexagonal orbit ────────────────────────────────────────────────

neg_c3 = [(-x) % P for x in c3]
assert sorted(set(c3) | set(neg_c3)) == sorted(c6)   # C3 ∪ (−C3) = C6

# C3 and −C3 are disjoint (no element equals its own negative in this group)
assert set(c3).isdisjoint(set(neg_c3))


# ── Report ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("F_37 Subgroup Structure Audit")
    print()
    print(f"  Group order: {P-1}  (F_{P}×)")
    print()
    print(f"  C3 = ⟨10⟩ = {c3}  ✓  (10³={pow(10,3,P)})")
    print(f"  C6 = ⟨27⟩ = {c6}  ✓  (27⁶={pow(27,6,P)})")
    print()
    print("  Relations:")
    print(f"    27 ≡ −10 (mod 37):        {(27+10)%P==0}  ✓")
    print(f"    1/37 repetend:             {repetend}  ✓  (period 3)")
    print(f"    27³ ≡ −1 (mod 37):         {pow(27,3,P)}  ✓")
    print()
    print("  Antipodal pairs {a,−a} in C6:")
    for a, b in antipodal_pairs:
        sq = (a**2) % P
        print(f"    {{{a:2d},{b:2d}}}  →  {sq:2d}  (squaring image in C3)")
    print()
    print(f"  C6 / {{±1}} ≅ C3 via x↦x²:  image = {sq_images}  ✓")
    print()
    print("  Hexagonal orbit:")
    print(f"    C3       = {sorted(c3)}")
    print(f"    −C3      = {sorted(neg_c3)}")
    print(f"    C3∪(−C3) = {sorted(set(c3)|set(neg_c3))} = C6  ✓")
    print()
    print("All assertions passed.")

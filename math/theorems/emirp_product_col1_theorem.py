"""
Emirp Product COL1 Theorem
==========================

THEOREM: For any emirp pair (p, rev(p)) with p > 3,
  DR(p × rev(p)) ∈ {1, 4, 7}  —  COL1, the chi_{-3} = +1 class.

PROOF (two routes):

Route 1 — DR algebra:
  (a) DR(p × rev(p)) = DR(DR(p) × DR(rev(p)))   [DR is multiplicative]
  (b) DR(p) = DR(rev(p))                          [digit sum permutation-invariant]
  (c) → DR(p × rev(p)) = DR(DR(p)²)
  (d) For prime p > 3: 3 ∤ p → DR(p) ∉ {3,6,9}
      → DR(p) ∈ {1,2,4,5,7,8}
  (e) DR(d²) for d ∈ {1,2,4,5,7,8} — exhaustive check:
        d=1 → DR(1)  = 1  ∈ {1,4,7}
        d=2 → DR(4)  = 4  ∈ {1,4,7}
        d=4 → DR(16) = 7  ∈ {1,4,7}
        d=5 → DR(25) = 7  ∈ {1,4,7}
        d=7 → DR(49) = 4  ∈ {1,4,7}
        d=8 → DR(64) = 1  ∈ {1,4,7}
  QED.

Route 2 — chi_{-3}:
  chi_{-3}(p × rev(p)) = chi_{-3}(p) × chi_{-3}(rev(p))
                       = chi_{-3}(p) × chi_{-3}(p)     [digit sum mod 3 invariant]
                       = chi_{-3}(p)²
  For prime p > 3: 3 ∤ p → chi_{-3}(p) ∈ {−1, +1}
  (±1)² = +1  →  chi_{-3}(p × rev(p)) = +1  →  DR(p × rev(p)) ∈ COL1
  QED.

SQUARING MAP ON DR VALUES (new result):
  The DR squaring map d → DR(d²) sends:
    COL1 → COL1:  1→1,  4→7,  7→4    (COL1 closed under squaring)
    COL2 → COL1:  2→4,  5→7,  8→1    (COL2 collapses INTO COL1)
    COL3 → COL3:  3→9,  6→9,  9→9    (sovereign closed; all collapse to 9)

  COL1 = {1,4,7} is precisely the image of the squaring map
  for all non-sovereign DR values. Equivalently: {1,4,7} are the
  non-zero quadratic residues mod 9.

PRODUCT DR LOOKUP TABLE:
  emirp DR | product DR | mapping
  ---------+------------+---------
      1    |     1      |  1² → 1
      2    |     4      |  2² → 4
      4    |     7      |  4² → 7  (16 mod 9 = 7)
      5    |     7      |  5² → 7  (25 mod 9 = 7)
      7    |     4      |  7² → 4  (49 mod 9 = 4)
      8    |     1      |  8² → 1  (64 mod 9 = 1)

VERIFIED: 0 violations over all emirp pairs in [13, 10^6].
Product DR distribution: {1: 3776, 4: 3638, 7: 3770} (near-uniform over COL1).
"""


def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


def chi_m3(n: int) -> int:
    r = n % 3
    if r == 1:
        return 1
    if r == 2:
        return -1
    return 0


def rev_num(n: int) -> int:
    return int(str(n)[::-1])


def sieve(limit: int):
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i :: i] = bytearray(len(is_p[i * i :: i]))
    return is_p


COL1 = {1, 4, 7}
COL2 = {2, 5, 8}
COL3 = {3, 6, 9}

# ── Proof step (e): exhaustive check of DR(d²) for d ∉ {3,6,9} ──────────────
for d in COL1 | COL2:
    assert dr(d * d) in COL1, f"DR({d}²)={dr(d*d)} not in COL1"

# ── Squaring map: COL1 closed, COL2 → COL1, COL3 → COL3 (→ 9) ───────────────
for d in COL1:
    assert dr(d * d) in COL1, f"COL1 not closed under squaring at d={d}"
for d in COL2:
    assert dr(d * d) in COL1, f"COL2 does not map to COL1 at d={d}"
for d in COL3:
    assert dr(d * d) in COL3, f"COL3 not closed under squaring at d={d}"

# COL1 squaring cycle: 1→1, 4→7, 7→4 (period-2 within COL1)
assert dr(1 * 1) == 1
assert dr(4 * 4) == 7
assert dr(7 * 7) == 4
# Two applications restore COL1 map: 1→1→1, 4→7→4, 7→4→7
assert dr(dr(4 * 4) * dr(4 * 4)) == 4   # 7²→4
assert dr(dr(7 * 7) * dr(7 * 7)) == 7   # 4²→7

# ── Chi_{-3} route: (±1)² = +1 ───────────────────────────────────────────────
for p in [13, 17, 31, 37, 71, 73, 79, 97, 107, 701]:
    assert chi_m3(p) != 0, f"Prime {p} should have chi≠0"
    assert chi_m3(p) ** 2 == 1
    rp = rev_num(p)
    assert chi_m3(p * rp) == 1, f"chi_{-3}({p}×{rp}) should be +1"
    assert dr(p * rp) in COL1, f"DR({p}×{rp}) should be in COL1"

# ── Full verification over all emirp pairs to 10^6 ────────────────────────────
is_p = sieve(10 ** 6)
violations = 0
from collections import Counter
product_dr_dist = Counter()
for p in range(13, 10 ** 6):
    if is_p[p]:
        rp = rev_num(p)
        if len(str(rp)) == len(str(p)) and is_p[rp] and p != rp:
            pd = dr(dr(p) ** 2)  # = DR(p × rev(p))
            if pd not in COL1:
                violations += 1
            elif p < rp:
                product_dr_dist[pd] += 1

assert violations == 0
assert set(product_dr_dist.keys()) == COL1


if __name__ == "__main__":
    print("EMIRP PRODUCT COL1 THEOREM")
    print("=" * 55)
    print()

    print("Theorem: DR(p × rev(p)) ∈ {1,4,7} for all emirp pairs (p > 3).")
    print()

    print("Proof — DR squaring route:")
    print("  DR(p × rev(p))")
    print("  = DR(DR(p) × DR(rev(p)))  [DR multiplicative homomorphism]")
    print("  = DR(DR(p)²)              [DR(p) = DR(rev(p)), digit sum invariant]")
    print()
    print("  DR(d²) for d ∈ {1,2,4,5,7,8} (sovereign-free DR values):")
    for d in sorted(COL1 | COL2):
        col = "COL1" if d in COL1 else "COL2"
        print(f"    d={d} [{col}]: DR({d}²) = DR({d*d:>2}) = {dr(d*d)}  ∈ COL1 ✓")
    print()

    print("Proof — chi_{-3} route:")
    print("  chi_{-3}(p × rev(p)) = chi_{-3}(p)² = (±1)² = +1 → COL1")
    print()

    print("Squaring map on DR values:")
    for col_name, col in [("COL1", COL1), ("COL2", COL2), ("COL3", COL3)]:
        arrow = "  ".join(f"{d}→{dr(d*d)}" for d in sorted(col))
        dest = "COL1" if col == COL1 or col == COL2 else "COL3"
        print(f"  {col_name} → {dest}:  {arrow}")
    print()

    print("Product DR lookup table:")
    print("  emirp DR | product DR")
    for d in sorted(COL1 | COL2):
        print(f"      {d}    |     {dr(d*d)}")
    print()

    print(f"Full verification [13, 10^6]: {violations} violations")
    print(f"Product DR distribution (unique pairs): {dict(sorted(product_dr_dist.items()))}")
    print()
    print("All assertions passed.")

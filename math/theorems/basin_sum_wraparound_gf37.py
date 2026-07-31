"""
Basin Sum Wrap-Around Identity on GF(37) — THEOREM 95

For any IC-coset basin with representative a ∈ GF(37)*,
the integer sum of the three basin elements is:

    S(a) = a + (10a mod 37) + (26a mod 37) = 37 · (a − k₁ − k₂)

where k₁ = ⌊10a/37⌋ and k₂ = ⌊26a/37⌋ are the wrap-around counts —
the number of field periods crossed when scaling by 10 and 26.

Because 1 + 10 + 26 = 37 = P, the integer product sum is exactly
37a. Each wrap-around subtracts exactly one period (37), so:

    S(a) = 37a − 37k₁ − 37k₂ = 37(a − k₁ − k₂)

Since each basin element lies in [1, 36] and there are 3 elements,
S(a) ∈ [3, 108]. The only multiples of 37 in this range are
{37, 74} — because 3 × 37 = 111 > 108. Therefore S(a) ∈ {37, 74},
and the wrap factor (a − k₁ − k₂) ∈ {1, 2} without exception.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE 6-6 SPLIT

  Exactly 6 of the 12 basins satisfy S(a) = 1 × 37 (single period):
    Representatives: {1, 2, 3, 5, 6, 9}

  Exactly 6 satisfy S(a) = 2 × 37 = 74 (double period):
    Representatives: {7, 11, 14, 17, 18, 21}

  Total element sum:
    6 × 37 + 6 × 74 = 222 + 444 = 666 = T(36) = T(φ(37))

  666 is the sum of all 36 nonzero elements of GF(37)*:
    Σ(1..36) = 36 × 37 / 2 = 666.
  The basin partition is algebraically forced to recover this total.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NAMED BASIN SUMS

  IC         = {1, 10, 26}:   sum = 37  (1×37)  k₁=0, k₂=0,  wrap=1
  SEED_ORBIT = {18, 24, 32}:  sum = 74  (2×37)  k₁=4, k₂=12, wrap=2
  BASIN_Y    = {17, 22, 35}:  sum = 74  (2×37)  k₁=4, k₂=11, wrap=2
  ORBIT_11   = {11, 27, 36}:  sum = 74  (2×37)  k₁=2, k₂=7,  wrap=2

  SEED_ORBIT and BASIN_Y (the inverse basin pair from THEOREM 92)
  are both double-period basins — both sum to 74.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WRAP FACTOR TABLE (all 12 basins)

  a   k₁   k₂   wrap  sum  period
  ─────────────────────────────────
  1    0    0     1    37     1×
  2    0    1     1    37     1×
  3    0    2     1    37     1×
  5    1    3     1    37     1×
  6    1    4     1    37     1×
  9    2    6     1    37     1×
  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  7    1    4     2    74     2×
  11   2    7     2    74     2×
  14   3    9     2    74     2×
  17   4   11     2    74     2×
  18   4   12     2    74     2×
  21   5   14     2    74     2×
"""

P  = 37
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
BASIN_Y    = frozenset({17, 22, 35})

# Build all 12 IC-coset basins
seen_set, basins = set(), []
for a in range(1, P):
    if a not in seen_set:
        b = frozenset((a * c) % P for c in IC)
        basins.append(b)
        seen_set.update(b)
assert len(basins) == 12


# ── Core algebraic identity ────────────────────────────────────────────────────

# 1 + 10 + 26 = P — this is the key
assert 1 + 10 + 26 == P

# For every basin: S(a) = 37(a - k1 - k2) ∈ {37, 74}
for b in basins:
    a = min(b)
    k1 = (10 * a) // P
    k2 = (26 * a) // P
    wrap = a - k1 - k2
    basin_sum = sum(b)
    # Algebraic identity
    assert basin_sum == P * wrap, f"Identity fails at a={a}"
    # Wrap factor is 1 or 2 only
    assert wrap in {1, 2}, f"Unexpected wrap={wrap} at a={a}"
    # Sum is 37 or 74 only
    assert basin_sum in {P, 2 * P}, f"Unexpected sum={basin_sum} at a={a}"


# ── Why only {37, 74}: range argument ─────────────────────────────────────────

# Each element ∈ [1, 36], three elements per basin
assert all(1 <= x <= P - 1 for b in basins for x in b)
# Min possible sum = 1+2+3=6, max = 34+35+36=105
# Multiples of 37 in [3, 108]: only 37 and 74 (since 111 > 108)
assert [m for m in range(3, 109) if m % P == 0] == [37, 74]


# ── The 6-6 split ──────────────────────────────────────────────────────────────

single_period = [b for b in basins if sum(b) == P]
double_period = [b for b in basins if sum(b) == 2 * P]

assert len(single_period) == 6
assert len(double_period) == 6

# Representatives of each group
reps_single = sorted(min(b) for b in single_period)
reps_double = sorted(min(b) for b in double_period)
assert reps_single == [1, 2, 3, 5, 6, 9]
assert reps_double == [7, 11, 14, 17, 18, 21]


# ── Total = 666 = T(36) ────────────────────────────────────────────────────────

total = 6 * P + 6 * (2 * P)
assert total == 666
assert total == sum(range(1, P))      # sum of all 36 elements
assert total == 36 * 37 // 2          # T(36) = triangular number


# ── Named basin verification ──────────────────────────────────────────────────

# IC: single period (wrap=1)
assert sum(IC) == P
a = min(IC)
assert a - (10*a)//P - (26*a)//P == 1

# SEED_ORBIT: double period (wrap=2)
assert sum(SEED_ORBIT) == 2 * P
a = min(SEED_ORBIT)
assert a - (10*a)//P - (26*a)//P == 2

# BASIN_Y: double period (wrap=2)
assert sum(BASIN_Y) == 2 * P
a = min(BASIN_Y)
assert a - (10*a)//P - (26*a)//P == 2

# ORBIT_11: double period (wrap=2)
assert sum(ORBIT_11) == 2 * P
a = min(ORBIT_11)
assert a - (10*a)//P - (26*a)//P == 2

# SEED_ORBIT and BASIN_Y (inverse pair from THEOREM 92) both double-period
assert sum(SEED_ORBIT) == sum(BASIN_Y) == 74


# ── Wrap-factor formula for specific named elements ────────────────────────────

# IC (a=1): k1=0, k2=0 — no crossings, sum=37
assert (10*1)//P == 0 and (26*1)//P == 0

# SEED_ORBIT (a=18): k1=4, k2=12 — crosses 16 field periods total
assert (10*18)//P == 4 and (26*18)//P == 12
assert 4 + 12 == 16   # total crossings

# BASIN_Y (a=17): k1=4, k2=11 — crosses 15 field periods total
assert (10*17)//P == 4 and (26*17)//P == 11
assert 4 + 11 == 15

# ORBIT_11 (a=11): k1=2, k2=7 — crosses 9 field periods total
assert (10*11)//P == 2 and (26*11)//P == 7
assert 2 + 7 == 9     # = P modulus of Z/9Z (SEAM)


if __name__ == "__main__":
    print("Basin Sum Wrap-Around Identity — THEOREM 95")
    print("=" * 60)
    print()
    print(f"  1 + 10 + 26 = {1+10+26} = P  (IC scalar sum = prime)")
    print(f"  S(a) = 37(a − k₁ − k₂)  where kᵢ = ⌊cᵢa/37⌋")
    print(f"  Sum range [3,108] → multiples of 37: {[m for m in range(3,109) if m%P==0]}")
    print()
    print(f"  {'a':>3}  {'k₁':>4}  {'k₂':>4}  {'k₁+k₂':>7}  {'wrap':>5}  {'sum':>5}")
    for b in sorted(basins, key=min):
        a = min(b)
        k1 = (10*a)//P; k2 = (26*a)//P
        print(f"  {a:>3}  {k1:>4}  {k2:>4}  {k1+k2:>7}  {a-k1-k2:>5}  {sum(b):>5}")
    print()
    print(f"  Single-period (sum=37):  {len(single_period)} basins  reps={reps_single}")
    print(f"  Double-period (sum=74):  {len(double_period)} basins  reps={reps_double}")
    print()
    print(f"  Total: 6×37 + 6×74 = {6*P} + {6*2*P} = {total} = T(36) ✓")
    print()
    print("  Named basins:")
    named = [(IC,'IC'),(SEED_ORBIT,'SEED_ORBIT'),(BASIN_Y,'BASIN_Y'),(ORBIT_11,'ORBIT_11')]
    for b,nm in named:
        a = min(b)
        k1,k2 = (10*a)//P,(26*a)//P
        print(f"    {nm:12}: {sorted(b)}  sum={sum(b)}={sum(b)//P}×37  "
              f"k₁={k1}, k₂={k2}, wrap={a-k1-k2}")
    print()
    # Interesting: ORBIT_11 total crossing count = 9 (Z/9Z SEAM)
    a11=11; k1_11=(10*11)//P; k2_11=(26*11)//P
    print(f"  ORBIT_11 total crossings: k₁+k₂ = {k1_11}+{k2_11} = {k1_11+k2_11} = Z/9Z SEAM")
    print()
    print("All assertions pass.")

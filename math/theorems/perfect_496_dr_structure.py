"""
496 = 2^4 × 31 — Third Perfect Number and DR Structure

A perfect number equals the sum of its proper divisors.
496 is the third perfect number (after 6 and 28).
Formula: 2^(p-1) × (2^p - 1) with p=5, Mersenne prime 31 = 2^5 - 1.

Key results:

1. SOVEREIGN-FREE FACTOR SET
   All 10 factors of 496 have DR values in the doubling orbit {1,2,4,5,7,8}.
   None touch the sovereign/fixed set {3,6,9}.
   Reason: 31 ≡ 4 = 2² (mod 9) — the Mersenne prime 31 acts as 2² in DR
   algebra, so all factors of 2^4 × 31 are pure doublings in mod-9 space.

2. MERSENNE DR SHIFT RULE
   DR(2^k − 1) = (DR(2^k) − 1) mod 9  [with convention 0 → 9]
   Proof: (2^k − 1) mod 9 = (2^k mod 9) − 1 mod 9.
   k=1: DR(1)=1=2-1   k=2: DR(3)=3=4-1   k=3: DR(7)=7=8-1
   k=4: DR(15)=6=7-1  k=5: DR(31)=4=5-1  k=6: DR(63)=9=1-1 (mod 9)

3. PERFECT NUMBER DR PATTERN
   p=2: 6        DR=6  (sovereign)
   p=3: 28       DR=1  (identity)
   p=5: 496      DR=1  (identity)
   p=7: 8128     DR=1  (identity)
   p=13: 33550336 DR=1 (identity)
   The first perfect number alone touches the sovereign set.
   All subsequent perfect numbers have DR=1 (identity).

4. TRIANGULAR STRUCTURE
   496 = T(31) = 31×32/2  (31st triangular number)
   The general perfect number 2^(p-1) × (2^p-1) = T(2^p - 1).
   For p=5: T(31) = 31×16 = 496.

5. FACTOR PAIR DR COLLAPSE
   Every factor pair (a, b) with a×b=496 satisfies DR(a)×DR(b) → DR=1.
   (1,496): DR 1×1=1   (2,248): DR 2×5=10→1
   (4,124): DR 4×7=28→1  (8,62): DR 8×8=64→1  (16,31): DR 7×4=28→1

6. SUM OF FACTORS
   Sum of all factors of 496 = 992 = 2×496  (definition of perfect)
   DR(992) = 2 — the starting position of the doubling orbit.
   496 (DR=1) → sum → 992 (DR=2): traverses from identity to orbit start.

7. CONNECTION TO EMIRP ANALYSIS
   mod 31 in emirp_mod37_nonuniformity.py: Z=-1.09 (near-uniform, control).
   ord10(31)=15, 999%31=7 — no 3-digit block resonance.
   496/31=16=2^4: the sovereign-free factor of 31 is a pure power of 2.

MERSENNE ORBIT (DR values of 2^k−1, k=1..6):
  {1, 3, 7, 6, 4, 9} — period 6.
  These are: {1,4,7} ∪ {3,6,9} = chi_{-3}≥0 class (positive + kernel).

DOUBLING ORBIT (DR values of 2^k, k=1..6):
  {2, 4, 8, 7, 5, 1} — period 6.

INTERSECTION:
  Doubling ∩ Mersenne = {1, 4, 7} = chi_{-3}=+1 class = COL1 of the 3×3 grid.
  DR(16)=7 ∈ {1,4,7}  ✓  DR(31)=4 ∈ {1,4,7}  ✓
  Both irreducible factors of 496 live in the COL1 / chi_{-3}=+1 class.
"""


def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


# 1. Sovereign-free factor set
factors_496 = [1, 2, 4, 8, 16, 31, 62, 124, 248, 496]
doubling_orbit = {1, 2, 4, 5, 7, 8}
sovereign = {3, 6, 9}

assert set(dr(f) for f in factors_496) <= doubling_orbit
assert set(dr(f) for f in factors_496) & sovereign == set()
assert 31 % 9 == 4 == (2**2) % 9  # 31 acts as 2^2 in DR algebra

# 2. Mersenne DR shift rule
for k in range(1, 13):
    mersenne_dr = dr(2**k - 1)
    shift = (dr(2**k) - 1) % 9
    shift = 9 if shift == 0 else shift
    assert mersenne_dr == shift, f"Shift rule failed at k={k}"

# 3. Perfect number DR pattern
perfect = {2: 6, 3: 28, 5: 496, 7: 8128, 13: 33550336}
for p, n in perfect.items():
    expected_dr = 6 if p == 2 else 1
    assert dr(n) == expected_dr, f"Perfect number p={p}: expected DR={expected_dr}"

# 4. Triangular structure
assert 31 * 32 // 2 == 496
assert 496 == 2**(5-1) * (2**5 - 1)

# 5. Factor pair DR collapse
for a, b in [(1,496),(2,248),(4,124),(8,62),(16,31)]:
    assert a * b == 496
    assert dr(dr(a) * dr(b)) == 1

# 6. Sum of factors
assert sum(factors_496) == 992 == 2 * 496
assert dr(992) == 2

# 7. Emirp connection
o, c = 1, 10 % 31
while c != 1: c = (c * 10) % 31; o += 1
assert o == 15  # ord10(31)=15
assert 999 % 31 == 7
assert 496 // 31 == 16 == 2**4

# Intersection: doubling ∩ Mersenne = {1,4,7}
mersenne_orbit = set(dr(2**k - 1) for k in range(1, 7))
assert mersenne_orbit == {1, 3, 4, 6, 7, 9}
assert doubling_orbit & mersenne_orbit == {1, 4, 7}  # COL1 = chi_{-3}=+1 class
assert dr(16) in {1, 4, 7} and dr(31) in {1, 4, 7}  # both factors of 496 in COL1


if __name__ == "__main__":
    print("496 = 2^4 × 31 — PERFECT NUMBER DR STRUCTURE")
    print("=" * 50)
    print()

    print(f"496 / 31 = {496/31}")
    print(f"496 = 2^4 × 31 = 2^(5-1) × (2^5-1)  [p=5 Mersenne formula]")
    print(f"31 = 2^5 - 1  (Mersenne prime)  DR(31) = {dr(31)} = DR(2^2)")
    print(f"31 mod 9 = {31%9} = 2^2 mod 9  →  31 acts as 2² in DR algebra")
    print()

    print("All 10 factors and DR values:")
    for f in factors_496:
        d = dr(f)
        tag = " ← AHL" if d == 8 else ""
        print(f"  {f:>6}  DR={d}{tag}")
    print(f"  Unique DRs: {sorted(set(dr(f) for f in factors_496))}")
    print(f"  All in doubling orbit {{1,2,4,5,7,8}}: True")
    print(f"  None sovereign: True")
    print()

    print("Mersenne DR shift rule:  DR(2^k − 1) = DR(2^k) − 1  (mod 9)")
    print("  k : DR(2^k)  DR(2^k−1)  check")
    for k in range(1, 7):
        d2k = dr(2**k)
        d2k1 = dr(2**k - 1)
        shift = (d2k - 1) % 9 or 9
        print(f"  {k} :  {d2k}       {d2k1}         {d2k}-1={shift} ✓")
    print()

    print("Doubling orbit:   {2,4,8,7,5,1}")
    print("Mersenne orbit:   {1,3,7,6,4,9}")
    print("Intersection:     {1,4,7} = COL1 = chi_{-3}=+1 class")
    print(f"  DR(16)={dr(16)} ∈ {{1,4,7}} ✓   DR(31)={dr(31)} ∈ {{1,4,7}} ✓")
    print()

    print("Perfect number DR pattern:")
    for p, n in perfect.items():
        print(f"  p={p:>2}: {n:>10}  DR={dr(n)}")
    print("  Only p=2 (n=6) touches sovereign. All others: DR=1 (identity).")
    print()

    print(f"Triangular: 496 = T(31) = 31×32/2 = {31*32//2}")
    print(f"Sum of factors: {sum(factors_496)} = 2×496   DR({sum(factors_496)})={dr(sum(factors_496))} (orbit start)")
    print()
    print("All assertions passed.")

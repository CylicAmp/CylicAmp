"""
Sovereign Bridge 30
DR(30) = 3 — 30 is sovereign.

Results:

1. SOVEREIGN RANGE
   {3, 12, 21, 30} — arithmetic progression, step 9, all DR=3.
   These are the four sovereign sentinels below 36.

2. CUMULATIVE SOVEREIGN SUMS
   Partial sums: 3, 3+12=15, 15+21=36, 36+30=66
   DR cycle:    {3,  6,      9,        3}   — one full sovereign cycle.

3. 30 AS BRIDGE: CONSTELLATIONS (11,12,13) → (41,42,43)
   Gap = 30 = sovereign number.
   30 + 11 = 41   (first twin prime target in Euler's polynomial)
   30 + 12 = 42   (sovereign middle: DR(42)=6)
   30 + 13 = 43   (second twin prime target)
   DR(30) = 3 connects both constellations without ambiguity.

4. EULER POLYNOMIAL HOOK
   p(n) = n² + n + 41 starts at p(0)=41, p(1)=43 — a twin prime pair.
   The gap between the twin-prime seed pair: 43 - 41 = 2 (primordial twin gap).
   The gap from constellation (11,12,13) to (41,42,43): 30 (sovereign).
   DR(2) = 2,  DR(30) = 3,  DR(32) = 5.  All distinct — no collision.

5. 3-6-9 PROGRESSION FROM SOVEREIGN SUM
   3 + 3 = 6
   6 + 3 = 9
   Cumulative sums of sovereign range encode this: 3 → 6 → 9 → 3.
"""

def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


# 1. Sovereign range
sovereign = [3, 12, 21, 30]
assert all(dr(x) == 3 for x in sovereign), "All sovereign sentinels must have DR=3"
diffs = [sovereign[i+1] - sovereign[i] for i in range(len(sovereign)-1)]
assert all(d == 9 for d in diffs), "Sovereign range must have step 9"

# 2. Cumulative sums
cumsum = []
running = 0
for x in sovereign:
    running += x
    cumsum.append(running)
assert cumsum == [3, 15, 36, 66]
cumsum_dr = [dr(s) for s in cumsum]
assert cumsum_dr == [3, 6, 9, 3], "Cumulative sum DR cycle must be {3,6,9,3}"

# 3. Bridge
assert 30 + 11 == 41
assert 30 + 12 == 42
assert 30 + 13 == 43
assert dr(30) == 3

# 4. Euler polynomial hook
def euler_poly(n):
    return n * n + n + 41

assert euler_poly(0) == 41
assert euler_poly(1) == 43
assert 43 - 41 == 2
assert 41 - 11 == 30 and 43 - 13 == 30

# 5. 3-6-9 progression
assert 3 + 3 == 6
assert 6 + 3 == 9
assert dr(3) == 3 and dr(6) == 6 and dr(9) == 9


if __name__ == "__main__":
    print("SOVEREIGN BRIDGE 30")
    print("=" * 40)
    print(f"Sovereign range: {sovereign}")
    print(f"  DRs: {[dr(x) for x in sovereign]}")
    print(f"  Step: 9 (fixed point of DR)")
    print()
    print("Cumulative sums:")
    for i, (s, r) in enumerate(zip(cumsum, cumsum_dr)):
        print(f"  Σ{i+1} = {s:>3}   DR = {r}")
    print(f"  Cycle: {cumsum_dr} → period 4 collapses to {{3,6,9,3}}")
    print()
    print("30 as bridge between twin prime constellations:")
    for base in [11, 12, 13]:
        target = 30 + base
        print(f"  30 + {base} = {target}   DR({base})={dr(base)}, DR({target})={dr(target)}")
    print()
    print("Euler polynomial seed pair:")
    print(f"  p(0) = {euler_poly(0)}   p(1) = {euler_poly(1)}")
    print(f"  Gap = {euler_poly(1) - euler_poly(0)} (primordial twin gap)")
    print(f"  Constellation shift: 41-11 = {41-11} = sovereign bridge")
    print()
    print("3-6-9 progression:")
    print(f"  3 + 3 = 6,  6 + 3 = 9,  9 + 3 → DR = {dr(12)} (back to 3)")
    print()
    print("All assertions passed.")

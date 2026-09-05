"""
LaneGenerator: Execution Lanes from Divisors of Seed 246 — THEOREM 97

The seed 246 has exactly 8 divisors: {1, 2, 3, 6, 41, 82, 123, 246}.
Each divisor defines an execution lane in GF(37). Their mod-37
residues map directly to named named sets.

Divisor → mod 37 → class:
  1   → 1   ∈ IC ∩ TESLA_4
  2   → 2   ∈ PR  (canonical primitive root)
  3   → 3   ∈ ST
  6   → 6   ∈ TESLA_4
  41  → 4   ∈ SA  (sovereign anchor)
  82  → 8   ∈ CB  (cascade base)
  123 → 12  ∈ ST
  246 → 24  ∈ CB ∩ SEED_ORBIT

The 8 lanes span: IC, PR, ST, TESLA_4, SA, CB, SEED_ORBIT.
Every named named set is represented except ORBIT_11 and BASIN_Y.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COUNT PROPERTIES

  8 divisors: DR(8) = 8 ∈ CB  (cascade base element)
  Sum of divisors: 1+2+3+6+41+82+123+246 = 504
    504 mod 37 = 504 - 13×37 = 504 - 481 = 23
    DR(504) = 9  (Z/9Z SEAM)

  Product of mod-37 residues: 1×2×3×6×4×8×12×24 mod 37
    = (1×2×3×6) × (4×8×12×24) mod 37
    = 36 × 9216 mod 37
    36 mod 37 = 36
    9216 mod 37 = 9216 - 249×37 = 9216 - 9213 = 3
    36 × 3 = 108 mod 37 = 108 - 2×37 = 34

  The two half-products:
    Small divisors {1,2,3,6}: product mod 37 = 36 ≡ -1 (additive near-identity)
    Large divisors {41,82,123,246}: residues {4,8,12,24}; product mod 37 = 3 ∈ ST

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SEED 246 ORBIT

  246 mod 37 = 24 ∈ SEED_ORBIT = {18, 24, 32}
  137-map: 24 → 32 → 18 → 24  (heartbeat 3-cycle)

  Lane 8 (divisor 246) lands at the seed's own orbit entry.
  Lane 5 (divisor 41) lands at sovereign anchor 4.
  Lane 6 (divisor 82) lands at cascade base 8.
"""

P          = 37
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
BASIN_Y    = frozenset({17, 22, 35})

SEED = 246


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 9


def divisors(n):
    return sorted(d for d in range(1, n + 1) if n % d == 0)


# ── Divisors of 246 ───────────────────────────────────────────────────────────

divs = divisors(SEED)
assert divs == [1, 2, 3, 6, 41, 82, 123, 246]
assert len(divs) == 8

# ── mod-37 residues of each lane ──────────────────────────────────────────────

residues = [d % P for d in divs]
assert residues == [1, 2, 3, 6, 4, 8, 12, 24]

# Lane membership
assert residues[0] == 1  and 1  in IC and 1  in TESLA_4
assert residues[1] == 2  and 2  in PR
assert residues[2] == 3  and 3  in ST
assert residues[3] == 6  and 6  in TESLA_4
assert residues[4] == 4  and 4  in SA
assert residues[5] == 8  and 8  in CB
assert residues[6] == 12 and 12 in ST
assert residues[7] == 24 and 24 in CB and 24 in SEED_ORBIT

# ── Count properties ──────────────────────────────────────────────────────────

assert len(divs) == 8 and 8 in CB        # count ∈ cascade base
assert dr(len(divs)) == 8

div_sum = sum(divs)
assert div_sum == 504
assert div_sum % P == 23
assert dr(div_sum) == 9                  # Z/9Z SEAM

# Half-product residues
small = [d % P for d in [1, 2, 3, 6]]
large = [d % P for d in [41, 82, 123, 246]]

prod_small = 1
for r in small:
    prod_small = (prod_small * r) % P
assert prod_small == 36                  # ≡ -1 mod 37

prod_large = 1
for r in large:
    prod_large = (prod_large * r) % P
assert prod_large == 3 and 3 in ST      # ∈ sovereign target

# ── Seed orbit connection ─────────────────────────────────────────────────────

assert SEED % P == 24 and 24 in SEED_ORBIT
# 137-map heartbeat
assert (26 * 24) % P == 32 and 32 in SEED_ORBIT
assert (26 * 32) % P == 18 and 18 in SEED_ORBIT
assert (26 * 18) % P == 24              # completes the 3-cycle


if __name__ == "__main__":
    def fw(r):
        classes = []
        for name, s in [('IC',IC),('SA',SA),('ST',ST),('CB',CB),
                        ('ORBIT_11',ORBIT_11),('SEED_ORBIT',SEED_ORBIT),
                        ('TESLA_4',TESLA_4),('PR',PR),('BASIN_Y',BASIN_Y)]:
            if r in s:
                classes.append(name)
        return classes or ['—']

    print("LaneGenerator: Execution Lanes from Divisors of Seed 246 — THEOREM 97")
    print("=" * 68)
    print()
    print(f"  Seed: {SEED}  mod37={SEED%P}  DR={dr(SEED)}")
    print(f"  Divisors ({len(divs)}): {divs}")
    print()
    print(f"  {'Lane':>4}  {'Divisor':>8}  {'mod37':>5}  {'DR':>3}  Classes")
    for i, (d, r) in enumerate(zip(divs, residues), 1):
        print(f"  {i:>4}  {d:>8}  {r:>5}  {dr(d):>3}  {fw(r)}")
    print()
    print(f"  Divisor count: {len(divs)}  DR={dr(len(divs))} ∈ CB")
    print(f"  Divisor sum:   {div_sum}  mod37={div_sum%P}  DR={dr(div_sum)} (SEAM)")
    print(f"  Small-divisor product mod37: {prod_small} ≡ -1")
    print(f"  Large-divisor product mod37: {prod_large} ∈ ST")
    print()
    print("All assertions pass.")

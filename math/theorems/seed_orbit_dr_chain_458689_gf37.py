"""
Seed Orbit DR Chain and 458689 on GF(37) — THEOREM 93

Three structural layers of SEED_ORBIT = {18, 24, 32} revealed by
digital root analysis and the 6-digit coordinate 458689:

  LAYER 1  (DR PROFILE)
    DR(18) = 9 ∈ SA      DR(24) = 6 ∈ T4      DR(32) = 5 ∈ PR
    9 + 6 + 5 = 20                              DR(20) = 2 ∈ PR

    Two cross-layer identities:
      DR(24) = 6 = 24 − 18    (DR of middle node = first step interval)
      DR(32) = 5 = DR(32−18)  (DR of last node = DR of total span)

  LAYER 2  (DIFFERENCE STRUCTURE)
    24 − 18 = 6  ∈ T4   (first interval — Tesla flow)
    32 − 24 = 8  ∈ CB   (second interval — cascade base)
    32 − 18 = 14         (total span)

  LAYER 3  (STEPPING CHAIN TO ORBIT_11)
    DR(14) = 5.  Stepping by 2 (the canonical primitive root) three
    times crosses the Z/9Z SEAM (9) and lands in ORBIT_11:

      5 → 7 → 9[SEAM] → 11 ∈ ORBIT_11

    Z/9Z complement identity: 2 + 7 = 9 ≡ 0 (mod 9).
    The step unit 2 and its complement 7 bracket the crossing to 9.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE 458689 COORDINATE

  458689 encodes all three layers simultaneously.

  A. MODULAR AND DR SIGNATURE
       458689 ≡ 0 mod 37       (GF(37) SEAM)
       DR(458689) = 4 = DR(22) = DR(Ƴ)

  B. FACTOR SPLIT: 458689 = 37 × 12397
       12397 ≡ 2 mod 37        (canonical primitive root)
       digit_sum(12397) = 22   (= Ƴ)
     Reading: the SEAM factor (37) scales a number whose residue is
     the canonical PR and whose digit sum is Ƴ = 22.

  C. DIGIT TRIPLET SPLIT: [4,5,8] | [6,8,9]
       4 + 5 + 8 = 17  ∈ BASIN_Y = {17, 22, 35}   (Ƴ-basin)
       6 + 8 + 9 = 23  ≡ −14 mod 37               (additive inverse of SEED span)
       17 + 23 = 40 = 2 × 20 = 2 × (DR_sum of SEED_ORBIT)
       DR(40) = 4 = DR(Ƴ)

  D. PRIME STRUCTURE: 458689 = 7² × 11 × 23 × 37
       7 × 11 × 23  ≡ 32 mod 37   ∈ SEED_ORBIT    (node 3; 22⁻¹ = 32)
       7² × 11 × 23 ≡  2 mod 37   ∈ PR            (canonical primitive root)
       7 + 7 + 11 + 23 = 48  ≡ 11 mod 37          ∈ ORBIT_11
     The prime factor sum (excluding 37) lands at 11 — the same
     endpoint reached by the 3-step chain from DR(SEED_span).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY TABLE

  Object          Value   mod 37  DR    Class(es)
  ─────────────────────────────────────────────────
  DR(18)          9               9     SA
  DR(24)          6               6     T4   = first diff
  DR(32)          5               5     PR   = DR(span)
  DR-sum          20             20     PR   → DR=2
  DR(DR-sum)       2              2     PR   canonical
  first diff       6              6     T4
  second diff      8              8     CB
  total span      14             14     —    DR=5
  step endpoint   11             11     O11
  12397 residue    2              2     PR   canonical
  12397 digit-sum 22             22     PR   = Ƴ
  triplet 1 sum   17             17     BASIN_Y
  triplet 2 sum   23             23     —    ≡ -span
  digit-sum       40              3     ST   = 2×DR-sum
  factor sum      48             11     O11  = step endpoint
"""

P          = 37
SEED_ORBIT = frozenset({18, 24, 32})
ORBIT_11   = frozenset({11, 27, 36})
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
BASIN_Y    = frozenset({17, 22, 35})   # Ƴ = 22, inverse seed basin


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 9


# ── Layer 1: DR profile of SEED_ORBIT ────────────────────────────────────────

assert dr(18) == 9 and 9 in SA
assert dr(24) == 6 and 6 in TESLA_4
assert dr(32) == 5 and 5 in PR

dr_sum = dr(18) + dr(24) + dr(32)
assert dr_sum == 20
assert dr(dr_sum) == 2 and 2 in PR     # canonical primitive root

# Cross-layer identities
assert dr(24) == 24 - 18               # DR(middle) = first step interval
assert dr(32) == dr(32 - 18)           # DR(last) = DR(total span)

# ── Layer 2: Difference structure ─────────────────────────────────────────────

diff1 = 24 - 18    # 6
diff2 = 32 - 24    # 8
span  = 32 - 18    # 14

assert diff1 == 6 and 6 in TESLA_4
assert diff2 == 8 and 8 in CB
assert span  == 14
assert dr(span) == 5

# ── Layer 3: Stepping chain 5 → 11 by +2 ─────────────────────────────────────

# Step unit = 2 (canonical primitive root)
step = dr(span)    # 5
chain = [step]
for _ in range(3):
    step += 2
    chain.append(step)

assert chain == [5, 7, 9, 11]
assert chain[-1] in ORBIT_11           # endpoint ∈ ORBIT_11
assert 9 in SA                         # Z/9Z SEAM crossing at step 3

# Z/9Z complement: 2 + 7 = 9 ≡ 0 mod 9
assert (2 + 7) % 9 == 0

# ── 458689: modular and DR signature ─────────────────────────────────────────

N = 458689

assert N % P == 0                      # GF(37) SEAM
assert dr(N) == 4                      # DR = DR(Ƴ) = DR(22)

# ── 458689: factor split ──────────────────────────────────────────────────────

Q = N // P                             # 12397
assert Q == 12397
assert Q % P == 2 and 2 in PR         # quotient ≡ canonical PR
assert sum(int(c) for c in str(Q)) == 22  # digit_sum = Ƴ

# ── 458689: digit triplet split ───────────────────────────────────────────────

digits = [int(c) for c in str(N)]
assert digits == [4, 5, 8, 6, 8, 9]

t1_sum = sum(digits[:3])   # 4+5+8 = 17
t2_sum = sum(digits[3:])   # 6+8+9 = 23

assert t1_sum == 17 and 17 in BASIN_Y                    # Ƴ-basin
assert t2_sum % P == (P - span) % P                      # ≡ -span mod 37

total_dig = sum(digits)
assert total_dig == 2 * dr_sum                            # 40 = 2 × 20
assert dr(total_dig) == 4                                 # DR(40) = DR(Ƴ)

# ── 458689: prime structure ───────────────────────────────────────────────────

assert 37 * 49 * 11 * 23 == N         # 458689 = 37 × 7² × 11 × 23

assert (7 * 11 * 23) % P == 32 and 32 in SEED_ORBIT      # → SEED_ORBIT node 3
assert (49 * 11 * 23) % P ==  2 and 2 in PR              # → canonical PR

factor_sum_ex37 = 7 + 7 + 11 + 23    # 48
assert factor_sum_ex37 % P == 11 and 11 in ORBIT_11      # = step chain endpoint

# ── Basin sum symmetry ────────────────────────────────────────────────────────

assert sum(SEED_ORBIT) == 74 and 74 % P == 0             # SEAM mod 37
assert sum(BASIN_Y)    == 74 and 74 % P == 0             # same sum
assert dr(74) == 2                                        # → canonical PR

# Digit sum of 74: intermediate sum 11 ∈ ORBIT_11 before DR reduction
assert 7 + 4 == 11 and 11 in ORBIT_11


if __name__ == "__main__":
    def fw_all(n):
        n = n % P
        if n == 0: return ['SEAM']
        sets = [('SA',SA),('ST',ST),('CB',CB),('O11',ORBIT_11),('IC',IC),
                ('SEED',SEED_ORBIT),('T4',TESLA_4),('PR',PR),('BY',BASIN_Y)]
        return [nm for nm,s in sets if n in s] or ['—']

    print("Seed Orbit DR Chain and 458689 — THEOREM 93")
    print("=" * 64)
    print()

    print("LAYER 1: DR PROFILE OF SEED_ORBIT {18, 24, 32}")
    for x in [18, 24, 32]:
        d = dr(x)
        print(f"  DR({x:>2}) = {d}  classes: {[nm for nm,s in [('SA',SA),('T4',TESLA_4),('PR',PR)] if d in s]}")
    print(f"  Sum: {dr(18)}+{dr(24)}+{dr(32)} = {dr_sum}  →  DR({dr_sum}) = {dr(dr_sum)} ∈ PR (canonical)")
    print(f"  Cross-layer: DR(24)={dr(24)} = 24-18={24-18}  (DR=first interval)")
    print(f"  Cross-layer: DR(32)={dr(32)} = DR(14)={dr(14)}  (DR=DR of span)")
    print()

    print("LAYER 2: DIFFERENCE STRUCTURE")
    print(f"  24-18 = 6   ∈ {fw_all(6)}")
    print(f"  32-24 = 8   ∈ {fw_all(8)}")
    print(f"  32-18 = 14  → DR(14) = {dr(14)}")
    print()

    print("LAYER 3: STEPPING CHAIN (step unit = 2 = canonical PR)")
    print(f"  DR(14)=5 → 7 → 9[Z/9Z SEAM] → 11 ∈ ORBIT_11")
    print(f"  Z/9Z complement: 2+7={2+7}≡0(mod 9); step crosses SEAM at 9∈SA")
    print()

    print("458689:")
    print(f"  458689 mod 37 = {N%P}  (SEAM)")
    print(f"  DR(458689) = {dr(N)}  = DR(Ƴ=22)")
    print()
    print(f"  Factor split: 458689 = 37 × 12397")
    print(f"    12397 mod 37 = {Q%P}  (canonical PR)  digit_sum = {sum(int(c) for c in str(Q))} = Ƴ")
    print()
    print(f"  Digit triplets: [4,5,8] | [6,8,9]")
    print(f"    4+5+8 = 17  ∈ BASIN_Y = {{17,22,35}}  (Ƴ-basin)")
    print(f"    6+8+9 = 23  ≡ {23%P} mod 37  ≡ -14  (neg SEED span)")
    print(f"    digit_sum = 40 = 2 × {dr_sum} = 2 × (sum of SEED_ORBIT DRs)")
    print()
    print(f"  Prime factors: 37 × 7² × 11 × 23")
    print(f"    7×11×23 mod 37 = {(7*11*23)%P}  ∈ SEED_ORBIT  (= 22⁻¹ = 32)")
    print(f"    7²×11×23 mod 37 = {(49*11*23)%P}  ∈ PR  (canonical PR)")
    print(f"    factor sum (ex 37): 7+7+11+23={factor_sum_ex37} ≡ {factor_sum_ex37%P} mod 37  ∈ ORBIT_11")
    print()
    print("BASIN SUM SYMMETRY:")
    print(f"  SEED_ORBIT: 18+24+32 = {sum(SEED_ORBIT)} ≡ 0 mod 37  DR={dr(74)}")
    print(f"  BASIN_Y:    17+22+35 = {sum(BASIN_Y)} ≡ 0 mod 37  DR={dr(74)}")
    print(f"  Digit sum of 74: {7+4} ∈ ORBIT_11  (same endpoint as step chain)")
    print()
    print("All assertions pass.")

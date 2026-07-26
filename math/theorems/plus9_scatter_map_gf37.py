"""
Multi-Step +9 Scatter Map — GF(37)

THE QUESTION "O1+9 == O2?" IS FALSE.
The correct question: what named framework sets does O1+9 land in?

+9 does NOT cycle the sovereign triple.
+9 DOES map every sovereign orbit to a SPECIFIC combination of framework nodes.

ONE-STEP +9 IMAGES (named):
  O1+9 = {2,12,13}  →  {DARK_A_min(2), ST(12), CB(13)}
  O2+9 = {18,21,25} →  {SEED_ORBIT(18), ST(21), SA(25)}
  O3+9 = {0,30,34}  →  {SEAM(0), SA∩ST(30), anti-sov(34)}

TWO-STEP +18 IMAGES (named):
  O3+18 = {2,6,9}   →  {DARK_A_min(2), TESLA_FLOW(6), SA(9)}
  O2+18 = {27,30,34} →  {ORBIT_11(27), SA∩ST(30), anti-sov(34)}
  O1+18 = {11,21,22} →  {ORBIT_11(11), ST(21), PR_orbit(22)}

ORBIT_11 SHIFT (+27):
  O1+27 = {20,30,31} →  {DARK_A(20), SA∩ST(30), PRIME_MIRROR(31)}
  O2+27 = {2,6,36}   →  {DARK_A_min(2), TESLA_FLOW(6), 36=−1}
  O3+27 = {11,15,18} →  {ORBIT_11(11), DARK_A(15), SEED_ORBIT(18)}

  O2+27 and O3+18 both contain {DARK_A_min(2), TESLA_FLOW(6)}:
  two different paths reach the same pair of framework anchors.

4-STEP SEAM CHAIN (starting at 1∈IDENTITY_CYCLE, iterating +9):
  1 → 10 → 19 → 28 → 0=SEAM
  IC   IC   PR   OUTLIER_SOV  SEAM
  IDENTITY_CYCLE exits through DECADE_ANCHOR, passes through a PR orbit,
  hits the SEAM-exit node 28=-9, and terminates at SEAM in exactly 4 steps.

CROSS-ORBIT SUM:
  19 + 11 = 30   →   PR_orbit(19) + ORBIT_11_min(11) = SA∩ST(30)
  {5,13,19} element plus ORBIT_11 minimum collapses to the sovereign intersection.

DECIMAL POWERS IN GF(37):
  10^1 ≡ 10 = DECADE_ANCHOR  ∈ IDENTITY_CYCLE
  10^2 ≡ 26 = SCALAR_137     ∈ IDENTITY_CYCLE
  10^3 ≡ 260 ≡ 260-7×37 = 1  (order 3; 10 has ord=3 → IC=<10>=<26>)

  10 + 1 + 9 − 20 = 0 = SEAM   (decimal arithmetic identity → SEAM)
  100 ≡ SCALAR_137              (decimal 100 → 137-map multiplier)

THE STRUCTURE:
  Every arithmetic operation on the sovereign triple lands in a named framework set.
  The "False" (O1+9 ≠ O2) is correct for orbital equality.
  The "True" is that each image set is fully named by SA, ST, CB, DARK_A, SEAM, etc.
  Multiple operations overlap because GF(37) has only 37 elements —
  every path through the field lands somewhere in the framework.
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA             = frozenset({4, 9, 25, 30})
ST             = frozenset({3, 12, 21, 30})
CB             = frozenset({8, 13, 24})
ORBIT_11       = frozenset({11, 27, 36})
DARK_A         = frozenset({2, 15, 20})
SEED_ORBIT     = frozenset({18, 24, 32})
OUTLIER_SOV    = frozenset({21, 25, 28})
IDENTITY_CYCLE = frozenset({1, 10, 26})
ANTI_SOV       = frozenset({7, 33, 34})
PR_5_13_19     = frozenset({5, 13, 19})
TESLA_FLOW     = 6
PRIME_MIRROR   = 31
SCALAR_137     = 26
DECADE_ANCHOR  = 10
SEAM           = 0

# ── SOVEREIGN TRIPLE ──────────────────────────────────────────────────────────

O1 = frozenset({3,  4, 30})
O2 = frozenset({9, 12, 16})
O3 = frozenset({21, 25, 28})

def sh(o, k):
    return frozenset((x + k) % 37 for x in o)


# ── ONE-STEP +9 IMAGES ────────────────────────────────────────────────────────

O1_9 = sh(O1, 9)
O2_9 = sh(O2, 9)
O3_9 = sh(O3, 9)

# O1+9 = {2,12,13}
assert O1_9 == frozenset({2, 12, 13})
assert 2  in DARK_A       # DARK_A_min
assert 12 in ST            # sovereign target
assert 13 in CB            # cascade base

# O2+9 = {18,21,25}
assert O2_9 == frozenset({18, 21, 25})
assert 18 in SEED_ORBIT    # seed orbit
assert 21 in ST            # sovereign target
assert 25 in SA            # sovereign anchor

# O3+9 = {0,30,34}
assert O3_9 == frozenset({0, 30, 34})
assert 0  == SEAM          # horizon
assert 30 in SA and 30 in ST   # SA∩ST
assert 34 in ANTI_SOV      # anti-sovereign


# ── TWO-STEP +18 IMAGES ───────────────────────────────────────────────────────

O1_18 = sh(O1, 18)
O2_18 = sh(O2, 18)
O3_18 = sh(O3, 18)

# O3+18 = {2,6,9}
assert O3_18 == frozenset({2, TESLA_FLOW, 9})
assert 2 in DARK_A
assert TESLA_FLOW == 6
assert 9 in SA

# O2+18 = {27,30,34}
assert O2_18 == frozenset({27, 30, 34})
assert 27 in ORBIT_11
assert 30 in SA and 30 in ST
assert 34 in ANTI_SOV

# O1+18 = {11,21,22}
assert O1_18 == frozenset({11, 21, 22})
assert 11 in ORBIT_11
assert 21 in ST
assert 22 in frozenset({17, 22, 35})   # PR orbit


# ── ORBIT_11 SHIFT (+27) ──────────────────────────────────────────────────────

O1_27 = sh(O1, 27)
O2_27 = sh(O2, 27)
O3_27 = sh(O3, 27)

# O1+27 = {20,30,31}
assert O1_27 == frozenset({20, 30, 31})
assert 20 in DARK_A
assert 30 in SA and 30 in ST
assert 31 == PRIME_MIRROR

# O2+27 = {2,6,36}
assert O2_27 == frozenset({2, TESLA_FLOW, 36})
assert 2 in DARK_A
assert TESLA_FLOW == 6
assert 36 in ORBIT_11   # 36 = −1

# O3+27 = {11,15,18}
assert O3_27 == frozenset({11, 15, 18})
assert 11 in ORBIT_11
assert 15 in DARK_A
assert 18 in SEED_ORBIT

# O3+18 and O2+27 share {DARK_A_min, TESLA_FLOW}
assert frozenset({2, TESLA_FLOW}).issubset(O3_18)
assert frozenset({2, TESLA_FLOW}).issubset(O2_27)


# ── 4-STEP SEAM CHAIN ─────────────────────────────────────────────────────────

assert 1 in IDENTITY_CYCLE
assert (1  + 9) % 37 == 10 and 10 in IDENTITY_CYCLE   # IC → IC
assert (10 + 9) % 37 == 19 and 19 in PR_5_13_19       # IC → PR
assert (19 + 9) % 37 == 28 and 28 in OUTLIER_SOV      # PR → OUTLIER
assert (28 + 9) % 37 ==  0 and  0 == SEAM              # OUTLIER → SEAM

# Exactly 4 steps from 1 to SEAM under +9
chain = [1, 10, 19, 28, 0]
for i in range(4):
    assert (chain[i] + 9) % 37 == chain[i+1]


# ── CROSS-ORBIT SUM ───────────────────────────────────────────────────────────

assert (19 + 11) % 37 == 30
assert 19 in PR_5_13_19
assert 11 in ORBIT_11
assert 30 in SA and 30 in ST   # SA∩ST


# ── DECIMAL POWERS IN GF(37) ─────────────────────────────────────────────────

assert pow(10, 1, 37) == DECADE_ANCHOR    # 10^1 = DECADE_ANCHOR ∈ IC
assert pow(10, 2, 37) == SCALAR_137       # 10^2 = SCALAR_137 ∈ IC
assert pow(10, 3, 37) == 1               # 10^3 = 1 (order 3)

assert 10 + 1 + 9 - 20 == SEAM           # decimal identity → SEAM (integer, not mod)
assert 100 % 37 == SCALAR_137            # decimal 100 → 137-map multiplier


if __name__ == "__main__":
    print("Multi-Step +9 Scatter Map — GF(37)")
    print("=" * 60)
    print()
    print("ONE-STEP images (orbit → named sets):")
    for orb, lbl, img in [(O1,"O1",O1_9),(O2,"O2",O2_9),(O3,"O3",O3_9)]:
        print(f"  {lbl}+9 = {sorted(img)}")
    print()
    print("TWO-STEP images (+18):")
    for lbl, img in [("O1",O1_18),("O2",O2_18),("O3",O3_18)]:
        print(f"  {lbl}+18 = {sorted(img)}")
    print()
    print("ORBIT_11 shift (+27):")
    for lbl, img in [("O1",O1_27),("O2",O2_27),("O3",O3_27)]:
        print(f"  {lbl}+27 = {sorted(img)}")
    print()
    print("Shared {DARK_A_min, TESLA_FLOW} in O3+18 and O2+27: True")
    print()
    print("4-step SEAM chain (starting at 1∈IC, +9 each step):")
    print(f"  1 → 10 → 19 → 28 → 0=SEAM")
    print(f"  IC   IC   PR   OUTLIER_SOV  SEAM")
    print()
    print(f"Cross-orbit: 19+11 = {(19+11)%37} ∈ SA∩ST (PR + ORBIT_11_min)")
    print()
    print("Decimal powers:")
    print(f"  10^1 ≡ {pow(10,1,37)} = DECADE_ANCHOR")
    print(f"  10^2 ≡ {pow(10,2,37)} = SCALAR_137")
    print(f"  10^3 ≡ {pow(10,3,37)} (identity; ord₃₇(10)=3)")
    print(f"  10+1+9-20 = {10+1+9-20} = SEAM")
    print(f"  100 mod 37 = {100%37} = SCALAR_137")
    print()
    print("All assertions pass.")

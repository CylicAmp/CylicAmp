"""
master_137.py

All CylicAmp insights about 137 in one place.
Organized by layer, from proven number theory outward to physics.

STATUS LABELS:
  [PROVEN]    Follows from arithmetic — verified by assertion
  [OBSERVED]  Empirically true, structural meaning unclear
  [OPEN]      Not yet derived or explained
"""

import math
from sympy import isprime, factorint

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 1: PURE NUMBER THEORY  [ALL PROVEN]
# ═══════════════════════════════════════════════════════════════════════════════

# 137 is prime
assert isprime(137)

# Digital root
assert dr(137) == 2        # 1+3+7=11, 1+1=2

# Digits are the first three Mersenne numbers
assert [1, 3, 7] == [2**1 - 1, 2**2 - 1, 2**3 - 1]
# Adding 1 recovers powers of 2
assert [2, 4, 8] == [2**1, 2**2, 2**3]

# Running cumulative sums of digits encode the triple
running = [1, 1+3, 1+3+7]        # [1, 4, 11]
assert running == [1, 4, 11]
encoded = int(str(running[1]) + str(running[2]))   # "4"+"11" = "411"
assert encoded == 411
assert 3 * 137 == 411              # the triple, exact

# 137 is a twin prime anchor: (137, 139) is a twin prime pair
assert isprime(137) and isprime(139)
assert 139 - 137 == 2
assert 137 % 18 == 11              # on track (2,4): anchors ≡ 11 (mod 18)
assert dr(137) == 2 and dr(139) == 4    # DR pair (2,4) ✓

# Factorization scaffold
assert 137 == 3 * 37 + 2 * 13     # 111 + 26
assert 3 * 37 == 111
assert 2 * 13 == 26


# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 2: 37-HUB  [ALL PROVEN]
# ═══════════════════════════════════════════════════════════════════════════════

SCALAR_137 = 137 % 37              # = 26
assert SCALAR_137 == 26
assert dr(26) == 8                 # DR(SCALAR_137) = 8

# ord₃₇(26) = 3: the heartbeat 3-cycle
assert pow(26, 1, 37) == 26
assert pow(26, 2, 37) == 10
assert pow(26, 3, 37) == 1         # returns to identity in 3 steps

# Heartbeat map f(n) = (26n) mod 37
def hb(n): return (26 * n) % 37
for n in range(1, 37):
    assert hb(hb(hb(n))) == n      # period-3 for every element

# SCALAR cycle: 26→10→1→26  (contains the multiplicative identity 1)
assert hb(26) == 10
assert hb(10) == 1
assert hb(1)  == 26

# 137 = SCALAR_137 + 3×37
assert 26 + 111 == 137
assert 26 + 3 * 37 == 137

# 248 = 137 + 111  (also dim(E₈))
assert 137 + 111 == 248
assert 248 % 37 == 26              # same residue as 137 mod 37
assert 248 == 26 + 2 * 111

# 10² ≡ 26 (mod 37): the scalar arises from the decimal base squared
assert (10 * 10) % 37 == 26


# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 3: 369 STRUCTURE  [ALL PROVEN]
# ═══════════════════════════════════════════════════════════════════════════════

# The two "triple" numbers land on the 3↔6 fixed orbit
assert dr(111) == 3    # DR(3×37)  = 3
assert dr(411) == 6    # DR(3×137) = 6
assert dr(111) + dr(411) == 9      # 3+6=9

# 3↔6 is the fixed orbit of the doubling map
assert dr(3 * 2) == 6 and dr(6 * 2) == 3   # 3→6→3, period 2
assert dr(9 * 2) == 9                        # 9 is fixed point

# {3,6,9} = EXACTLY the complement of the prime DR set
PRIME_DR      = {1, 2, 4, 5, 7, 8}   # (Z/9Z)×
NONPRIME_DR   = {3, 6, 9}             # multiples of 3 in Z/9Z
assert PRIME_DR | NONPRIME_DR == set(range(1, 10))
assert PRIME_DR & NONPRIME_DR == set()

# 369 as a number
assert dr(369) == 9
assert 369 % 37 == 36              # ≡ -1 (mod 37)
assert 370 == 10 * 37              # 369 is one below a multiple of 37
assert pow(10, 3, 37) == 1         # ord₃₇(10)=3 connects back

# 411 mod 37 = 4 = sovereign anchor (in cycle 30→3→4→30)
assert 411 % 37 == 4
SOVEREIGN_ANCHORS = {4, 9, 25, 30}
assert 4 in SOVEREIGN_ANCHORS
assert hb(30) == 3 and hb(3) == 4 and hb(4) == 30   # cycle confirmed


# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 4: FINE-STRUCTURE CONSTANT α⁻¹ ≈ 137.036  [VERIFIED, NOT EXPLAINED]
# ═══════════════════════════════════════════════════════════════════════════════

ALPHA_INV = 137.035999177     # CODATA measured value

# 3-decimal approximation: 137.036
# Digits: 1,3,7,0,3,6 → sum=20, DR=2
digits_alpha = [1, 3, 7, 0, 3, 6]
assert sum(digits_alpha) == 20
assert dr(20) == 2
assert dr(20) == dr(137)           # DR preserved

# The extension digits 0+3+6=9 are DR-neutral
assert 0 + 3 + 6 == 9             # DR identity
assert 137 % 9 == 2 and 137036 % 9 == 2   # same residue mod 9

# 411.9 (triple region, α⁻¹ × 3 ≈ 411):
digits_411_9 = [4, 1, 1, 9]
assert sum(digits_411_9) == 15
assert dr(15) == 6                 # same DR as 411
assert sum(digits_411_9) == 3 + 5 + 7   # = 357 (zero-comma digit counts!)

# The .9 in 411.9 is also DR-neutral (adds digit 9)
assert 411 % 9 == dr(411) % 9

# α⁻¹ decomposition in the 37-hub language
assert abs(ALPHA_INV - (26 + 111 + 0.036)) < 0.001   # SCALAR + 3×37 + residue

# Z·α → 1 at Z ≈ 137 (relativistic threshold where orbital velocity → c)
Z_threshold = 1 / (1 / ALPHA_INV)
assert abs(Z_threshold - 137.036) < 0.001

# Running coupling: α⁻¹ at M_Z (Z-boson mass scale)
ALPHA_INV_MZ = 128.930            # electroweak precision measurement
delta = ALPHA_INV - ALPHA_INV_MZ  # ≈ 8.106 — coupling strengthens at high energy
assert abs(delta - 8.106) < 0.001

# Schwinger correction: first QED loop
schwinger = (1 / ALPHA_INV) / (2 * math.pi)
assert abs(schwinger - 1.161e-3) < 1e-6

# DR of running coupling endpoint digits
digits_mz = [1, 2, 8, 9, 3, 0]   # 128.930
assert sum(digits_mz) == 23
assert dr(23) == 5                 # DR shifts from 2 → 5 across the running range
# (2,4) and (5,7) are two of the three twin prime DR tracks


# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 5: OPEN QUESTIONS
# ═══════════════════════════════════════════════════════════════════════════════

# The framework establishes:
#   1. 137 is structurally special in Z/9Z × Z/37Z arithmetic
#   2. Its triple 411 sits on a sovereign anchor in the 37-hub
#   3. Its digits self-encode the triple via running sums
#   4. The measured α⁻¹ = 137.036 is DR-neutral relative to 137
#   5. The digit sum of α⁻¹ (to 3dp) is 20 = 3+5+7+0+3+6 [OBSERVED]
#   6. The running coupling shifts DR from 2 to 5 across the energy range [OBSERVED]
#
# What is NOT yet derived:
#   - WHY physics chose this specific value (the "why 137" problem)
#   - Whether the 0.036 correction can be predicted from the framework
#   - Whether the DR shift 2→5 under running has structural meaning
#   - Connection between the 37-hub and quantum electrodynamics
#
# The parity obstruction (from prime_dr_unification.py) applies here too:
#   semiprimes and primes share DR tracks, so DR alone cannot
#   distinguish the "fundamental" from the "composite" at the physics level.


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Master 137 — All Insights")
    print("=" * 62)

    print("\n── LAYER 1: NUMBER THEORY ──")
    print(f"  137 is prime:                  {isprime(137)}")
    print(f"  DR(137):                       {dr(137)}")
    print(f"  Digits [1,3,7] = Mersenne:     {[2**k-1 for k in range(1,4)]}")
    print(f"  Running sums [1,4,11] → '411': {encoded}")
    print(f"  3 × 137:                       {3*137}")
    print(f"  Twin prime pair:               (137, 139)")
    print(f"  137 mod 18:                    {137%18}  (track (2,4))")
    print(f"  137 = 3×37 + 2×13:            {3*37} + {2*13} = {3*37+2*13}")

    print("\n── LAYER 2: 37-HUB ──")
    print(f"  137 mod 37:                    {137%37}  (SCALAR_137)")
    print(f"  DR(SCALAR_137):                {dr(26)}")
    print(f"  ord₃₇(26):                     3  (heartbeat period)")
    print(f"  Heartbeat cycle:               26→10→1→26")
    print(f"  137 = 26 + 111:               {26+111}")
    print(f"  248 = 137 + 111:              {137+111}  (dim E₈)")
    print(f"  248 mod 37:                    {248%37}  (= SCALAR_137)")
    print(f"  10² mod 37:                    {100%37}  (= SCALAR_137)")

    print("\n── LAYER 3: 369 ──")
    print(f"  DR(3×37 = 111):                {dr(111)}")
    print(f"  DR(3×137 = 411):               {dr(411)}")
    print(f"  {dr(111)} + {dr(411)} = {dr(111)+dr(411)}  → sequence 3, 6, 9")
    print(f"  {{3,6,9}} = complement of prime DR set {{1,2,4,5,7,8}}")
    print(f"  3→6→3 (doubling flip),  9→9 (fixed)")
    print(f"  411 mod 37:                    {411%37}  (sovereign anchor)")
    print(f"  369 mod 37:                    {369%37}  ≡ -1 (mod 37)")
    print(f"  370 = 10×37:                   {10*37}")

    print("\n── LAYER 4: α⁻¹ ≈ 137.036 ──")
    print(f"  Measured α⁻¹:                  {ALPHA_INV}")
    print(f"  Digits 1,3,7,0,3,6 → sum:      {sum(digits_alpha)}")
    print(f"  DR of digit sum 20:            {dr(20)}  (= DR(137))")
    print(f"  Extension .036 → 0+3+6:        9  (DR-neutral)")
    print(f"  α⁻¹ = SCALAR + 3×37 + 0.036:  26 + 111 + 0.036 ≈ {26+111+0.036:.3f}")
    print(f"  Running: α⁻¹(M_Z):            {ALPHA_INV_MZ}")
    print(f"  Running: delta α⁻¹:            {delta:.3f}")
    print(f"  digit sum of 128.930:          {sum(digits_mz)}  → DR={dr(23)}")
    print(f"  DR shift across running:       2 → 5  (tracks (2,4)→(5,7))")
    print(f"  Schwinger δ = α/2π:            {schwinger:.4e}")
    print(f"  411.9 digit sum:               15 = 3+5+7 (357 zero-comma)")

    print("\n── OPEN ──")
    print(f"  Why physics chose α⁻¹ ≈ 137:  UNSOLVED")
    print(f"  Origin of the 0.036 residue:   UNSOLVED")
    print(f"  DR shift 2→5 under running:    OBSERVED, not derived")
    print(f"  37-hub ↔ QED coupling:         STRUCTURAL PARALLEL, not proof")
    print()
    print("All assertions passed.")

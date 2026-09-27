# math/theorems/sequence_30303_doubling.py
"""
Doubling Sequence: 30,303 × 2^k

─────────────────────────────────────────────────────────────────────────────
SEED FACTORIZATION
─────────────────────────────────────────────────────────────────────────────
  30,303 = 3² × 7 × 13 × 37
         = 333 × 91          (333 = 37×9,  91 = 7×13)
         = 3 × 10,101        (10101 = 3 × 7 × 13 × 37)

  Every term 30,303 × 2^k is divisible by 37.
  Every term has DR = 9  (since 9 | 30,303 → 9 | 30,303×2^k for all k).

─────────────────────────────────────────────────────────────────────────────
ALTERNATING-DIGIT WINDOW: k = 2..5
─────────────────────────────────────────────────────────────────────────────
  30,303 × 2^k = (2^(k−3) × 24) × 10,101

  For 2-digit multiplier xy:  xy × 10,101 = xyxyxy  (repeating xy, no carry)
  Because: xy × (10⁴ + 10² + 1) = xy0000 + xy00 + xy

  k=2: 12 × 10101 =  121,212  [1,2] alternating
  k=3: 24 × 10101 =  242,424  [2,4] alternating
  k=4: 48 × 10101 =  484,848  [4,8] alternating
  k=5: 96 × 10101 =  969,696  [9,6] alternating   ← last clean pair (96 < 100)
  k=6: 192 × 10101 = 1,939,392  BREAKS (192 is 3-digit → carries corrupt pattern)

  The alternating pairs double: [1,2]→[2,4]→[4,8]→[9,6].
  After [9,6]×2=[18,12]→192 (3-digit): pattern cannot continue.

─────────────────────────────────────────────────────────────────────────────
RETURN TO 3.33... AT k=40
─────────────────────────────────────────────────────────────────────────────
  Leading digits determined by frac(k·log₁₀(2) + log₁₀(30303)).
  At k=40: frac = 0.5227  →  10^0.5227 = 3.332  (leading digits "3.33")
  At k=41: ×2 of k=40     →  leading digits "6.66"

  k=40: 33,318,500,856,496,128  =  3.33185009E+16
  k=41: 66,637,001,712,992,256  =  6.66370017E+16

─────────────────────────────────────────────────────────────────────────────
333 = 37 × 9  ACROSS SCALES
─────────────────────────────────────────────────────────────────────────────
  3,330  = 333 × 10   (top anchor, "3.33" scale)
  6,660  = 333 × 20
  30,303 = 333 × 91   (seed)
  121,212 = 333 × 364 = 4 × 30,303
  Leading "3.33" at k=40 is the same digit pattern, 13 orders of magnitude up.

─────────────────────────────────────────────────────────────────────────────
"787" APPEARANCES: gap of 26
─────────────────────────────────────────────────────────────────────────────
  k= 7: 3,878,784          contains digits ...7,8,7... (positions 3,4,5)
  k=33: 260,300,787,941,376  contains "787"
  Gap: 33 − 7 = 26  (Z/26Z modulus from AML(248; 26, 37))
"""

import math

SEED = 30_303


def dr(n): return (n - 1) % 9 + 1 if n > 0 else 9


# ── Seed factorization ─────────────────────────────────────────────────────────

assert SEED == 9 * 7 * 13 * 37
assert SEED == 333 * 91
assert SEED == 3 * 10_101
assert 10_101 == 3 * 7 * 13 * 37
assert 333 == 37 * 9
assert 91 == 7 * 13

# ── DR = 9 for all terms ───────────────────────────────────────────────────────

assert SEED % 9 == 0
for k in range(45):
    assert dr(SEED * 2**k) == 9

# ── All terms divisible by 37 ──────────────────────────────────────────────────

for k in range(45):
    assert (SEED * 2**k) % 37 == 0

# ── Alternating-digit property ─────────────────────────────────────────────────

# xy × 10101 = xyxyxy when xy is a 2-digit number (10 ≤ xy ≤ 99)
def is_alternating_6digit(n):
    s = str(n)
    return len(s) == 6 and s[0] == s[2] == s[4] and s[1] == s[3] == s[5]

# General: xy × 10101 for 2-digit xy
for xy in range(10, 100):
    val = xy * 10_101
    s = str(val)
    assert s == str(xy) * 3, f"Pattern fails for xy={xy}"

# Specific values in the sequence
assert SEED * 4  == 12 * 10_101 == 121_212
assert SEED * 8  == 24 * 10_101 == 242_424
assert SEED * 16 == 48 * 10_101 == 484_848
assert SEED * 32 == 96 * 10_101 == 969_696

assert is_alternating_6digit(121_212)
assert is_alternating_6digit(242_424)
assert is_alternating_6digit(484_848)
assert is_alternating_6digit(969_696)

# k=2..5 all pass; k=6 breaks
for k in (2, 3, 4, 5):
    assert is_alternating_6digit(SEED * 2**k)
assert not is_alternating_6digit(SEED * 2**6)   # 192 × 10101 = 1939392 ≠ 6-digit

# Alternating pairs double: [1,2]→[2,4]→[4,8]→[9,6]
pairs = [12, 24, 48, 96]
assert all(pairs[i] * 2 == pairs[i + 1] for i in range(3))
assert pairs[-1] * 2 == 192   # 3-digit → breaks pattern

# ── Return to 3.33... at k=40 ─────────────────────────────────────────────────

k40 = SEED * 2**40
k41 = SEED * 2**41

assert k40 == 33_318_500_856_496_128
assert k41 == 66_637_001_712_992_256

assert str(k40)[:3] == '333'
assert str(k41)[:3] == '666'

# Fractional part analysis
frac40 = math.modf(40 * math.log10(2) + math.log10(SEED))[0]
assert abs(10**frac40 - 3.332) < 0.01   # leading value ≈ 3.332

# ── 333 across scales ──────────────────────────────────────────────────────────

assert 3_330 == 333 * 10
assert 6_660 == 333 * 20
assert SEED  == 333 * 91
assert SEED * 4 == 333 * 364      # 121,212 = 333 × 364

# All are multiples of 333 = 37 × 9
for val in [3_330, 6_660, SEED, SEED * 4, SEED * 8]:
    assert val % 333 == 0

# ── "787" appearances 26 steps apart ──────────────────────────────────────────

assert '787' in str(SEED * 2**7)     # k=7:  3,878,784
assert '787' in str(SEED * 2**33)    # k=33: 260,300,787,941,376
assert 33 - 7 == 26                  # gap = 26 = AML Z/26Z modulus

# ── User sequence verification ─────────────────────────────────────────────────

SEQUENCE = {
    2:  121_212,
    3:  242_424,
    4:  484_848,
    5:  969_696,
    6:  1_939_392,
    7:  3_878_784,
    8:  7_757_568,
    9:  15_515_136,
    10: 31_030_272,
    11: 62_060_544,
    12: 124_121_088,
    13: 248_242_176,
    14: 496_484_352,
    15: 992_968_704,
    33: 260_300_787_941_376,
    40: 33_318_500_856_496_128,
    41: 66_637_001_712_992_256,
}
for k, expected in SEQUENCE.items():
    assert SEED * 2**k == expected, f"k={k}: {SEED * 2**k} ≠ {expected}"


if __name__ == "__main__":
    print("Doubling Sequence: 30,303 × 2^k")
    print()
    print(f"Seed: {SEED:,d} = 333×91 = 37×9×7×13")
    print(f"      10101 = 3×7×13×37  (alternating-digit generator)")
    print(f"      All terms: DR=9, divisible by 37")
    print()
    print("Alternating-digit window k=2..5:")
    for k in range(2, 7):
        val = SEED * 2**k
        xy = val // 10_101
        ok = is_alternating_6digit(val) if len(str(val)) == 6 else False
        status = f"xy={xy:3d}  [{str(xy)[0]},{str(xy)[1]}]×3  HOLDS" if ok else f"xy={xy:3d}  BREAKS"
        print(f"  k={k}: {val:>12,d}  {status}")
    print()
    print(f"Leading-digit return at k=40:")
    print(f"  k=40: {k40:,d}  ({k40:.8E})  →  '3.33'")
    print(f"  k=41: {k41:,d}  ({k41:.8E})  →  '6.66'")
    print()
    print("333 = 37×9 across scales:")
    for label, val in [("3,330",3330),("6,660",6660),("30,303",30303),("121,212",121212)]:
        print(f"  {label:>8s} = 333 × {val//333}")
    print()
    print(f"'787' at k=7 and k=33 (gap=26=AML modulus):")
    print(f"  k= 7: {SEED*2**7:>25,d}  ({str(SEED*2**7)[2:5]}...)")
    print(f"  k=33: {SEED*2**33:>25,d}  (...{str(SEED*2**33)[6:9]}...)")
    print()
    print("All assertions passed.")

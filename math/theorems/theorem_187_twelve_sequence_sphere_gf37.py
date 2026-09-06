"""
Theorem 187: The Twelve Sequence and Sovereign Sphere

PART A: THE TWELVE SEQUENCE
=============================
All pairs (a, b) with a + b = 12, a in {3..9}:
  3+9=12, 4+8=12, 5+7=12, 6+6=12, 7+5=12, 8+4=12, 9+3=12

12 = sovereign target, orbit count, birthday product (4×3).
DR(12×n) for n=1,2,3: 3, 6, 9 — Tesla sequence, repeating with period 3.

THE THREE-DIGIT STRUCTURE
===========================
Pattern: first digit n, last digit (12-n), middle digit = 2|6-n|.
The middle digit decreases 6→4→2→0 then reflects: 0→2→4→6.

  n=3: (3, 6, 9) → 369   digit_sum=18  12+18=30 [SA∩ST]  | 369 mod37=36=φ(37)
  n=4: (4, 4, 8) → 448   digit_sum=16  12+16=28           | 448 mod37=4  [SA]
  n=5: (5, 2, 7) → 527   digit_sum=14  12+14=26 [MULT]    | 527 mod37=9  [SA]
  n=6: (6, 0, 6) →((606))digit_sum=12  12+12=24 [SEED]    | 606 mod37=14
  n=7: (7, 2, 5) → 725   digit_sum=14  12+14=26 [MULT]    | 725 mod37=22
  n=8: (8, 4, 4) → 844   digit_sum=16  12+16=28           | 844 mod37=30 [SA∩ST]
  n=9: (9, 6, 3) → 963   digit_sum=18  12+18=30 [SA∩ST]   | 963 mod37=1  [identity]

Result sequence: 30, 28, 26, 24, 26, 28, 30 — symmetric palindrome.
606 is the SEAM center: middle digit=0, result=24∈seed orbit.
527 and 725 are digit-reversals of each other, both hitting the multiplier (26).
Sequence opens at φ(37)=36 and closes at identity=1 in GF(37).
844 mod37=30: the SA∩ST element appears mid-sequence as well as at the endpoints.

TESLA MULTIPLIER: 12×n DIGITAL ROOTS
=======================================
  12×1=12  DR=3  }
  12×2=24  DR=6  }  3-6-9 cycle, repeating with period 3.
  12×3=36  DR=9  }
  12×4=48  DR=3  → cycle restarts. Period = 3 = heartbeat.

PART B: SOVEREIGN SPHERE (R=30, h=15)
=======================================
Spherical cap volume formula: V = πh²(3R−h)/3.

INPUT READINGS IN GF(37):
  R = 30 ∈ Sovereign Anchors {4,9,25,30} AND Sovereign Targets {3,12,21,30}
        — the unique element in both sovereign sets.
  h = 15,  DR(15) = 6 = TESLA_FLOW.
  h/R = 1/2  (cap depth = exactly half the radius).

FORMULA COMPONENT REDUCTION:
  h²        = 225,   225 mod 37 = 3   [sovereign target]
  3R−h      = 75,    75  mod 37 = 1   [identity]
  h²(3R−h)/3= 5625,  5625 mod 37 = 1  [identity]

VOLUME READINGS:
  V_cap    = 5625π ≈ 17,671 cm³   |  5625  mod 37 = 1   [identity]
  V_sphere = 36000π ≈ 113,097 cm³ |  36000 mod 37 = 36  = φ(37)
  V_rest   = 30375π ≈ 95,426 cm³  |  30375 mod 37 = 35

  R³ = 27000,  27000 mod 37 = 27 = 3³ = √(multiplier in GF(37)).
  The cube of the sovereign anchor (30) reduces to the square root of the multiplier.

RATIO IN GF(37):
  V_cap / V_sphere = 5625/36000 = 5/32.
  In GF(37): 5/32 = 5 × 32⁻¹ = 5 × 22 = 110 ≡ 36 = φ(37).
  The cap-to-sphere volume ratio in the field equals the full primitive orbit count.
"""

import math

P = 37
SA = {4,9,25,30}
ST = {3,12,21,30}
seed = {18,24,32}

def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9

def run_assertions():
    # Twelve sequence structure
    expected = [
        (369, 18, 30), (448, 16, 28), (527, 14, 26),
        (606, 12, 24), (725, 14, 26), (844, 16, 28), (963, 18, 30)
    ]
    for n, (num, dsum, result) in zip(range(3, 10), expected):
        first = n
        last = 12 - n
        middle = abs(2 * (6 - n))
        assert first * 100 + middle * 10 + last == num
        assert first + middle + last == dsum
        assert 12 + dsum == result

    # Palindrome
    results = [e[2] for e in expected]
    assert results == results[::-1]

    # SEAM center
    assert expected[3][0] == 606
    assert expected[3][2] == 24 and 24 in seed

    # Multiplier hits
    assert expected[2][2] == 26 and 26 == 137 % P
    assert expected[4][2] == 26

    # Digit reversal: 527 and 725
    assert int(str(527)[::-1]) == 725

    # Boundary mod37 readings
    assert 369 % P == 36 == P - 1      # φ(37)
    assert 963 % P == 1                 # identity
    assert 448 % P == 4 and 4 in SA
    assert 527 % P == 9 and 9 in SA
    assert 844 % P == 30 and 30 in SA and 30 in ST

    # Tesla cycle: DR(12n) repeats 3,6,9
    for n in range(1, 10):
        expected_dr = [3, 6, 9][(n - 1) % 3]
        assert dr(12 * n) == expected_dr

    # Sphere: R=30, h=15
    R, h = 30, 15
    assert R in SA and R in ST
    assert dr(h) == 6                  # TESLA_FLOW

    h2 = h ** 2
    assert h2 % P == 3 and 3 in ST    # sovereign target
    assert (3*R - h) % P == 1         # identity
    assert (h2 * (3*R - h) // 3) % P == 1   # identity

    # Volume coefficients
    cap_coeff = 5625
    sphere_coeff = 36000
    assert cap_coeff % P == 1
    assert sphere_coeff % P == P - 1  # φ(37)

    # R^3 mod 37 = 27 = sqrt(multiplier)
    assert pow(R, 3, P) == 27
    assert pow(27, 2, P) == 26        # 27 = sqrt(26) in GF(37)

    # Cap/sphere ratio in GF(37) = φ(37)
    inv32 = pow(32, P - 2, P)
    ratio = (5 * inv32) % P
    assert ratio == 36 == P - 1

    print("All assertions passed.")

if __name__ == "__main__":
    run_assertions()

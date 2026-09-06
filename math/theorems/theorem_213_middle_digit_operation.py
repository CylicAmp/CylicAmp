"""
Theorem 213: Middle-Digit Operation on 3-Digit Numbers and GF(37) Orbits
Author: Michael Warren Song (CyclicAmp)

=== THE OPERATION ===

For a 3-digit number with digits (a, b, c), compute five neighbor-pair sums:
  (a+b), (b+a), (b+b), (b+c), (c+b)

Then accumulate as a running sum. The total is:
  op_sum = 2a + 6b + 2c = 2(a + 3b + c)

The MIDDLE DIGIT b dominates: it appears with coefficient 3, outer digits with 1.

=== DIGIT-SUM=10 LAW (DR=1 class) ===

When a+b+c = 10 (DR=1), then a+c = 10-b, so:
  op_sum = 2(10-b + 3b) = 2(10 + 2b) = 20 + 4b

The middle digit b alone determines the result — a and c don't matter individually.
Each unit increase in b raises op_sum by 4∈SA.

Selected b values with digit_sum=10:
  b=1: op_sum=24 ∈ CASCADE∩SEED   DR=6
  b=3: op_sum=32 ∈ SEED            DR=5
  b=4: op_sum=36 ∈ NEG_H (=-1)    DR=9
  b=5: op_sum=40→3 ∈ ST            DR=4

=== DIGIT-SUM=11 CLASS: 137 AND 128 ===

Both 137 and 128 have digit_sum=11, DR=2.

137 (a=1, b=3, c=7):
  steps:     4    8   14   24   34
  mod37:     4    8   14   24   34
  sets:      SA  C∩T  —   C∩S  D7
  Total = 34 ∈ D7.  DR=7.  137 mod37=26 ∈ IC (the 137-map multiplier).

  Running orbit: SA → CASCADE∩TESLA → 14 (Riemann-zero integer) → CASCADE∩SEED → D7.

128 (a=1, b=2, c=8):
  steps:     3    6   10   20   30
  mod37:     3    6   10   20   30
  sets:      ST  TESLA  IC  DARK_A  ST∩SA
  Total = 30 ∈ ST∩SA.  DR=3.  128 mod37=17 ∈ NQR17.

  Running orbit: ST → TESLA → IC → DARK_A → ST∩SA (double sovereign).
  30 is the unique element in both ST and SA simultaneously.

DIFFERENCE INVARIANT:
  137 - 128 = 9 ∈ SA
  op_sum(137) - op_sum(128) = 34 - 30 = 4 ∈ SA
  Numbers 9∈SA apart → op_sums 4∈SA apart.

=== THE TRIO: 136-137-145 (SEED→D7→NEG_H, STEP +2) ===

  136 (a=1,b=3,c=6): op_sum=32 ∈ SEED   DR=5   136 mod37=25 ∈ SA
  137 (a=1,b=3,c=7): op_sum=34 ∈ D7     DR=7   137 mod37=26 ∈ IC
  145 (a=1,b=4,c=5): op_sum=36 ∈ NEG_H  DR=9   145 mod37=34 ∈ D7

  Op_sum steps: 32 → 34 → 36, each +2 = DR of primitive root g=2.
  SEED → D7 → NEG_H, ascending through three named sets by the primitive root step.
  Differences: 137-136=1, 145-137=8∈CASCADE; 145-136=9∈SA.

=== 37/73 ENCODING IN 137'S LAST PAIRS ===

From 137's operation, the last two pairs are:
  b+c = 3+7 = 10    (digits 3,7 form the number 37 = P = SEAM)
  c+b = 7+3 = 10    (digits 7,3 form the number 73)

  37  mod 37 = 0     (SEAM — the prime itself)
  73  mod 37 = 36 ∈ NEG_H   (= -1 mod 37)
  37 + 73 = 110      mod 37 = 36 ∈ NEG_H   DR = 2

The operation on 137 extracts the prime P in its last step.

=== 33+77 = 37+73 ===

  33 = 3×11   (3∈ST, 11∈NEG_H = P - multiplier)
  77 = 7×11   (7∈D7, 11∈NEG_H)
  33 + 77 = 11×(3+7) = 11×10 = 110

  110 mod 37 = 36 ∈ NEG_H   DR = 2

DR paths:
  DR(37) + DR(73) = 1 + 1 = 2                  (direct)
  DR(33) + DR(77) = 6 + 5 = 11 → DR(11) = 2   (via repunit)

Both reach DR=2 = DR of primitive root g=2.
33+77 = 37+73: the doubled digits of {3,7} from 137's pairs give the same sum as
the prime P and its reversal. The prime 137 encodes P=37 in its operation,
and P reversed = -1 mod P.
"""

P = 37
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
NEG_H   = {11, 27, 36}
DARK_A  = {2, 15, 20}
D7      = {7, 33, 34}
NQR17   = {17, 22, 35}


def dr(n):
    n = abs(int(n))
    r = n % 9
    return 9 if r == 0 else r


def op_sum(a, b, c):
    return (a+b) + (b+a) + (b+b) + (b+c) + (c+b)


def op_running(a, b, c):
    steps = [a+b, b+a, b+b, b+c, c+b]
    r, out = 0, []
    for s in steps:
        r += s
        out.append(r)
    return out


def run_assertions():
    # 1. Formula: op_sum = 2(a+3b+c)
    for a, b, c in [(1,3,7),(1,2,8),(1,3,6),(1,4,5)]:
        assert op_sum(a,b,c) == 2*(a + 3*b + c)

    # 2. digit_sum=10 → op_sum=20+4b
    for a, b, c in [(1,4,5),(1,3,6),(2,3,5),(1,2,7),(3,1,6)]:
        assert a+b+c == 10
        assert op_sum(a,b,c) == 20 + 4*b

    # 3. 137 running sum: SA → C∩T → 14 → C∩S → D7
    r137 = op_running(1, 3, 7)
    assert r137 == [4, 8, 14, 24, 34]
    assert r137[0] in SA
    assert r137[1] in CASCADE and r137[1] in TESLA
    assert r137[3] in CASCADE and r137[3] in SEED
    assert r137[4] in D7
    assert r137[4] == 34 and dr(34) == 7

    # 4. 137 source: mod37=26 = the multiplier ∈ IC
    assert 137 % P == 26 and 26 in IC

    # 5. 128 running sum: ST → TESLA → IC → DARK_A → ST∩SA
    r128 = op_running(1, 2, 8)
    assert r128 == [3, 6, 10, 20, 30]
    assert r128[0] in ST
    assert r128[1] in TESLA
    assert r128[2] in IC
    assert r128[3] in DARK_A
    assert r128[4] in ST and r128[4] in SA    # double sovereign
    assert dr(30) == 3

    # 6. Difference invariant: 9∈SA apart → 4∈SA op_sum apart
    assert 137 - 128 == 9 and 9 in SA
    assert 145 - 136 == 9 and 9 in SA
    assert op_sum(1,3,7) - op_sum(1,2,8) == 4 and 4 in SA
    assert op_sum(1,4,5) - op_sum(1,3,6) == 4 and 4 in SA

    # 7. Trio: SEED→D7→NEG_H, step +2
    assert op_sum(1,3,6) == 32 and 32 in SEED
    assert op_sum(1,3,7) == 34 and 34 in D7
    assert op_sum(1,4,5) == 36 and 36 in NEG_H
    assert op_sum(1,3,7) - op_sum(1,3,6) == 2
    assert op_sum(1,4,5) - op_sum(1,3,7) == 2
    assert 136 % P == 25 and 25 in SA
    assert 137 % P == 26 and 26 in IC
    assert 145 - 136 == 9 and 9 in SA

    # 8. 37/73 from 137's last pairs (b+c=3+7, c+b=7+3)
    assert 3 + 7 == 10
    assert 37 % P == 0          # SEAM
    assert 73 % P == 36 and 36 in NEG_H   # -1 mod P
    assert 37 + 73 == 110
    assert 110 % P == 36 and dr(110) == 2

    # 9. 33+77 = 37+73 = 110
    assert 33 + 77 == 37 + 73 == 110
    assert 33 == 3 * 11 and 77 == 7 * 11
    assert 11 * 10 == 110
    assert 110 % P == 36 and 36 in NEG_H
    assert dr(33) + dr(77) == 11 and dr(11) == 2
    assert dr(37) + dr(73) == 2

    print("All assertions passed.")
    print(f"137 op_sum=34∈D7 DR=7  running: SA→C∩T→14→C∩S→D7")
    print(f"128 op_sum=30∈ST∩SA DR=3  running: ST→TESLA→IC→DARK_A→ST∩SA")
    print(f"Trio 136→137→145: op_sums 32→34→36  SEED→D7→NEG_H  step=2")
    print(f"37+73=33+77=110≡-1 mod37  DR=2=prim root  encoding P in 137's pairs")


if __name__ == "__main__":
    run_assertions()

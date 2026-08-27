"""
Theorem 231: {2, 3, 6} Permutations — All Splits Under Basic Arithmetic
Author: Michael Warren Song (CyclicAmp)

From T230: the counts of the three representations of 6 are (6, 3, 2) → number 632.
Reversed: 236. "236 — new beginning."

The six permutations of digits {2, 3, 6}:
  236  263  326  362  623  632

For each permutation, two two-part splits (left-1-digit + right-2-digits, and left-2-digits + right-1-digit).
Total: 12 splits. Apply each of the four basic arithmetic operations.

=== ADDITION ===

  2+36=38   23+6=29
  2+63=65   26+3=29
  3+26=29   32+6=38
  3+62=65   36+2=38
  6+23=29   62+3=65
  6+32=38   63+2=65

Distinct sums: {29, 38, 65}

  Every single sum has DR = 2.
  DR(29) = DR(38) = DR(65) = 2.

  29 + 38 + 65 = 132.  DR(132) = 6.  Returns to 6.

  Spacing between sums:
    38 − 29 = 9  = 3²
    65 − 38 = 27 = 3³

GF(37):
  29 mod 37 = 29  ∈ C9 = {14, 29, 31}
  38 mod 37 =  1  ∈ IC = {1, 10, 26}
  65 mod 37 = 28  ∈ SA_ST_B = {21, 25, 28}

=== SUBTRACTION (absolute differences) ===

Distinct |differences|: {17, 23, 26, 34, 59, 61}

GF(37):
  17 mod 37 = 17  ∈ NQR17 = {17, 22, 35}
  23 mod 37 = 23  ∈ TESLA = {6, 8, 23}
  26 mod 37 = 26  ∈ IC = {1, 10, 26}
  34 mod 37 = 34  ∈ D7 = {7, 33, 34}
  59 mod 37 = 22  ∈ NQR17 = {17, 22, 35}
  61 mod 37 = 24  ∈ SEED = {18, 24, 32}

Sum of distinct differences: 220.  DR(220) = 4.

=== MULTIPLICATION ===

  2×36=72    23×6=138
  2×63=126   26×3=78
  3×26=78    32×6=192
  3×62=186   36×2=72
  6×23=138   62×3=186
  6×32=192   63×2=126

Distinct products: {72, 78, 126, 138, 186, 192}

  DR(72)  = 9
  DR(78)  = 6
  DR(126) = 9
  DR(138) = 3
  DR(186) = 6
  DR(192) = 3

All DRs are in {3, 6, 9}.

Sum of distinct products: 792.  DR(792) = 9.

GF(37):
  72  mod 37 = 35  ∈ NQR17
  78  mod 37 =  4  ∈ C3 = {3, 4, 30}
  126 mod 37 = 15  ∈ DARK_A = {2, 15, 20}
  138 mod 37 = 27  ∈ NEG_H = {11, 27, 36}
  186 mod 37 =  1  ∈ IC
  192 mod 37 =  7  ∈ D7 = {7, 33, 34}

=== DIVISION (exact integer results only) ===

Only one exact integer division exists across all 12 splits:

  36 / 2 = 18  ∈ SEED = {18, 24, 32}

DR(18) = 9.  18 ∈ SEED = orbit of seed 246 mod 37.

=== SUMMARY ===

Operation     Distinct values         DR pattern        Return to 6?
Addition      {29, 38, 65}            all DR=2          yes: 29+38+65=132, DR=6
Subtraction   {17,23,26,34,59,61}     {8,5,8,7,5,7}    —
Multiplication {72,78,126,138,186,192} all in {3,6,9}   yes: sum=792, DR=9
Division      {18}  (one exact)        DR=9             —
"""

from itertools import permutations as _permutations

P    = 37
MULT = 26

IC      = {1, 10, 26}
DARK_A  = {2, 15, 20}
C3      = {3, 4, 30}
CAS_EXT = {5, 13, 19}
TESLA   = {6, 8, 23}
D7      = {7, 33, 34}
SA_ST_A = {9, 12, 16}
NEG_H   = {11, 27, 36}
C9      = {14, 29, 31}
NQR17   = {17, 22, 35}
SEED    = {18, 24, 32}
SA_ST_B = {21, 25, 28}


def dr(n: int) -> int:
    n = abs(int(n))
    if n == 0:
        return 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def splits(perm: str):
    """Two two-part splits of a 3-digit string: (d1, d23) and (d12, d3)."""
    return [(int(perm[0]), int(perm[1:])), (int(perm[:2]), int(perm[2]))]


def all_splits():
    """All 12 two-part splits of the six permutations of {2,3,6}."""
    perms = [''.join(map(str, p)) for p in _permutations([2, 3, 6])]
    result = []
    for p in perms:
        for a, b in splits(p):
            result.append((a, b))
    return result


def run_assertions():
    pairs = all_splits()
    assert len(pairs) == 12

    # ── Addition ──────────────────────────────────────────────────────────────
    add_vals = sorted(set(a + b for a, b in pairs))
    assert add_vals == [29, 38, 65]
    assert all(dr(s) == 2 for s in add_vals)
    assert sum(add_vals) == 132 and dr(132) == 6

    # Spacing: 9 = 3², 27 = 3³
    assert add_vals[1] - add_vals[0] == 9
    assert add_vals[2] - add_vals[1] == 27

    # GF(37)
    assert 29 % P == 29 and 29 in C9
    assert 38 % P == 1  and 1  in IC
    assert 65 % P == 28 and 28 in SA_ST_B

    # ── Subtraction ───────────────────────────────────────────────────────────
    sub_vals = sorted(set(abs(a - b) for a, b in pairs))
    assert sub_vals == [17, 23, 26, 34, 59, 61]
    assert 17 % P == 17 and 17 in NQR17
    assert 23 % P == 23 and 23 in TESLA
    assert 26 % P == 26 and 26 in IC
    assert 34 % P == 34 and 34 in D7
    assert 59 % P == 22 and 22 in NQR17
    assert 61 % P == 24 and 24 in SEED
    assert sum(sub_vals) == 220 and dr(220) == 4

    # ── Multiplication ────────────────────────────────────────────────────────
    mul_vals = sorted(set(a * b for a, b in pairs))
    assert mul_vals == [72, 78, 126, 138, 186, 192]
    assert all(dr(p) in {3, 6, 9} for p in mul_vals)
    assert sum(mul_vals) == 792 and dr(792) == 9
    assert 72  % P == 35 and 35 in NQR17
    assert 78  % P == 4  and 4  in C3
    assert 126 % P == 15 and 15 in DARK_A
    assert 138 % P == 27 and 27 in NEG_H
    assert 186 % P == 1  and 1  in IC
    assert 192 % P == 7  and 7  in D7

    # ── Division (exact integers) ─────────────────────────────────────────────
    div_exact = [(a, b, a // b) for a, b in pairs if b != 0 and a % b == 0]
    div_exact += [(a, b, b // a) for a, b in pairs if a != 0 and b % a == 0]
    div_vals = sorted(set(v for _, _, v in div_exact if v > 1))
    assert div_vals == [18], f"exact integer divisions: {div_vals}"
    assert 18 in SEED and dr(18) == 9

    print("All assertions passed.")
    print()
    print("PERMUTATIONS OF {2, 3, 6} — T231")
    print()
    print("236  263  326  362  623  632")
    print()
    print("ADDITION — distinct sums: {29, 38, 65}")
    print(f"  DR(29)=DR(38)=DR(65) = 2")
    print(f"  29+38+65 = 132  DR=6  (returns to 6)")
    print(f"  Gaps: 38-29=9=3²  65-38=27=3³")
    print(f"  GF(37): 29∈C9  38→1∈IC  65→28∈SA_ST_B")
    print()
    print("SUBTRACTION — distinct |differences|: {17,23,26,34,59,61}")
    print(f"  GF(37): 17∈NQR17  23∈TESLA  26∈IC  34∈D7  59→22∈NQR17  61→24∈SEED")
    print(f"  Sum=220  DR=4")
    print()
    print("MULTIPLICATION — distinct products: {72,78,126,138,186,192}")
    print(f"  All DRs ∈ {{3,6,9}}")
    print(f"  GF(37): 72→35∈NQR17  78→4∈C3  126→15∈DARK_A  138→27∈NEG_H  186→1∈IC  192→7∈D7")
    print(f"  Sum=792  DR=9")
    print()
    print("DIVISION — one exact integer result: 36/2=18∈SEED  DR=9")


if __name__ == "__main__":
    run_assertions()

"""
Theorem 158: The Counting Palindrome — 11213141514131211 Hits SEAM

THE NUMBER
===========

    N = 11213141514131211

A 17-digit palindrome. It encodes counting from 1 to 5 and back:

    1 | 1,2 | 1,3 | 1,4 | 1,5 | 1,4 | 1,3 | 1,2 | 1

Each segment is the pair (1, current count): the 1 is the "+1 step," the
count is the arrival. The count rises 1→2→3→4→5, pivots at 5, then falls
5→4→3→2→1. The start and end 1s are the boundary markers.

    Digits: 1, 1, 2, 1, 3, 1, 4, 1, 5, 1, 4, 1, 3, 1, 2, 1, 1
    Count: 17

IT IS SEAM
===========

    11213141514131211 ≡ 0  (mod 37)

The palindrome is an exact multiple of 37:

    11213141514131211 = 303057878760303 × 37

Not divisible by 37²:  N mod (37²) = 259 = 7 × 37

This means N = 37 × k where k mod 37 = 7 ∈ D7.

The palindrome hits SEAM. Its first factor above the prime is in D7.

PARALLEL TO THEOREM 151
=========================

Theorem 151: 1221 = 33 × 37  (4-digit palindrome → SEAM)
Theorem 158: 11213141514131211 = 303057878760303 × 37  (17-digit palindrome → SEAM)

Both palindromes — the 4-digit palindrome of simple reversal and the
17-digit palindrome of counting — hit SEAM. The palindrome structure forces
divisibility by 37 in both cases.

THE D7 CLUSTER: {7, 33, 34}
==============================

Three quantities associated with this palindrome all land in D7 = {7, 33, 34}:

    33 = digit sum     (actual: 1+1+2+1+3+1+4+1+5+1+4+1+3+1+2+1+1 = 33)
    34 = 2 × 17        (digit count × 2)
     7 = (N/37) mod 37 (the quotient above the prime)

D7 is the 414-orbit (Theorem 147). All three values — the digit sum, the count
doubled, and the prime quotient residue — are in the same D7 orbit.

Note: DR(33) = 6 ∈ TESLA_ORB. DR(34) = 7 ∈ D7. DR(7) = 7 ∈ D7.
The digit sum DR does not itself land in D7 — only the raw value 33 does.

THE CENTER: 5
==============

The palindrome pivots at position 9 of 17. The center digit is 5.

    5 ∈ NQR_5 = {5, 13, 19}

From Theorem 153: 5 + 32 = 37 = SEAM. The center digit is the NQR_5 complement
of 32 (SEED_ORB node), and their sum is the prime itself.

The counting process reaches 5 — then must reverse. 5 is the pivot. In GF(37),
5 cannot reach the seed without crossing the prime boundary.

THE 17 DIGITS
==============

    17 ∈ NQR_17 = {17, 22, 35}

The palindrome length is a non-quadratic residue. The NQR_17 orbit is the orbit
of 17, which is itself prime.

    2 × 17 = 34 ∈ D7    (digit count doubled lands in D7)

THE DIGIT SUM CORRECTION
==========================

The digit sum is 33, not 34. The discrepancy is 1.

    33 ∈ D7 (actual digit sum)
    34 ∈ D7 (digit count × 2)
    Both are in D7.

The claim "sum = 34 → 7" conflates two different D7 routes:
  - 34 = 2 × 17 is a D7 element (via digit count)
  - 7 appears as (N/37) mod 37 (via the prime quotient)
The digit sum DR is DR(33) = 6, not 7. The 7 comes from the quotient, not the DR.

STRUCTURE SUMMARY
==================

    N = 11213141514131211  (counting palindrome, 1→5→1)
    N mod 37 = 0           (SEAM — exact multiple of 37)
    N / 37 mod 37 = 7      (D7)
    Digit sum = 33         (D7)
    Digit count = 17       (NQR_17); 2×17=34 (D7)
    Center digit = 5       (NQR_5; 5+32=37=SEAM)
    D7 = {7, 33, 34}: quotient residue, digit sum, and count-doubled all in D7
    Palindrome → SEAM: same pattern as 1221 (Theorem 151)
"""

P = 37

ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}

N = 11213141514131211


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def run_assertions():
    digits = [int(d) for d in str(N)]

    # Structure
    assert digits == [1, 1, 2, 1, 3, 1, 4, 1, 5, 1, 4, 1, 3, 1, 2, 1, 1]
    assert len(digits) == 17
    assert digits == digits[::-1]   # palindrome

    # Center digit is 5
    assert digits[8] == 5           # position 9 of 17 (0-indexed: 8)
    assert 5 in ORBITS['NQR_5']
    assert 5 + 32 == P              # complement to 37 (Theorem 153)

    # SEAM
    assert N % P == 0

    # Exact divisibility: once by 37, not twice
    k = N // P
    assert N % (P * P) == 7 * P    # N mod 37² = 7×37
    assert k % P == 7              # (N/37) mod 37 = 7
    assert 7 in ORBITS['D7']

    # Digit sum = 33
    digit_sum = sum(digits)
    assert digit_sum == 33
    assert 33 in ORBITS['D7']
    assert dr(33) == 6
    assert 6 in ORBITS['TESLA_ORB']

    # Digit count: 17 ∈ NQR_17
    assert len(digits) == 17
    assert 17 in ORBITS['NQR_17']
    assert 2 * 17 == 34
    assert 34 in ORBITS['D7']

    # D7 contains all three: 7, 33, 34
    assert {7, 33, 34} == ORBITS['D7']
    assert 7 in ORBITS['D7']
    assert 33 in ORBITS['D7']
    assert 34 in ORBITS['D7']

    # Theorem 151 parallel: 1221 = 33×37
    assert 1221 % P == 0
    assert 1221 == 33 * P

    print("All assertions passed.")


def summarise():
    digits = [int(d) for d in str(N)]
    k = N // P

    print("=" * 62)
    print("Theorem 158: Counting Palindrome → SEAM")
    print("=" * 62)
    print()
    print(f"  N = {N}")
    print(f"  Digits: {digits}")
    print(f"  Count: {len(digits)}, palindrome: {digits == digits[::-1]}")
    print()
    print(f"  N mod 37 = {N % P}  →  {orbit_of(N)}")
    print(f"  N / 37 = {k}")
    print(f"  (N/37) mod 37 = {k % P}  →  {orbit_of(k)}")
    print()
    print(f"  Digit sum = {sum(digits)}  →  {orbit_of(sum(digits))}")
    print(f"  DR({sum(digits)}) = {dr(sum(digits))}  →  {orbit_of(dr(sum(digits)))}")
    print(f"  2 × 17 = 34  →  {orbit_of(34)}")
    print()
    print(f"  D7 = {{7, 33, 34}}:")
    print(f"    7   = (N/37) mod 37")
    print(f"    33  = digit sum")
    print(f"    34  = 2 × digit_count")
    print()
    print(f"  Center digit: {digits[8]} ∈ {orbit_of(5)}")
    print(f"  5 + 32 = 37 = SEAM  (Theorem 153 complement)")
    print()
    print(f"  Parallel: 1221 = 33×37  (4-digit palindrome → SEAM, Theorem 151)")


if __name__ == "__main__":
    run_assertions()
    summarise()

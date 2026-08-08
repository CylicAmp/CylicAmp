"""
Theorem 144: The Loop Cipher — Negation mod 37 via ord₃₇(10) = 3

THE CIPHER
===========

loop_cipher: each digit d ↦ 9 − d. Non-digit characters are skipped.

This is negation in ℤ/9ℤ: d + (9−d) = 9 ≡ 0 (mod 9). It is the
9-complement operation. In digital root arithmetic it swaps:

    DR=1 ↔ DR=8,   DR=2 ↔ DR=7,   DR=4 ↔ DR=5
    DR=3 ↔ DR=6    (3-6-9 elements swap within the pair)
    DR=9 ↦ DR=0    (digit 9 maps to 0, the SEAM digit)

THE STRUCTURAL REASON: ord₃₇(10) = 3
========================================

10 ∈ IC = {1, 10, 26} = μ₃   (the cube roots of unity in GF(37))

The 10-system and the 37-system are connected:
    10¹ ≡ 10 (mod 37)
    10² ≡ 26 (mod 37)
    10³ ≡  1 (mod 37)

The three elements of IC are exactly the three powers of 10 mod 37.
The positional base of decimal arithmetic sits inside μ₃ of GF(37).

CIPHER = NEGATION MOD 37 FOR STRINGS OF LENGTH DIVISIBLE BY 3
================================================================

For an n-digit integer N with cipher output N′:
    N + N′ = 9 × (10^{n-1} + 10^{n-2} + ... + 10 + 1)
           = 10^n − 1

10^n − 1 ≡ 0 (mod 37)  iff  3 | n     [since ord₃₇(10) = 3]

Therefore:
    N′ ≡ −N (mod 37)   for any n-digit string with 3 | n

The cipher is exact negation mod 37 on 3-, 6-, 9-, 12-, ...-digit strings.

COROLLARY: SEAM IS FIXED
==========================

If N ≡ 0 (mod 37) and len(N) is divisible by 3:
    cipher(N) ≡ −N ≡ 0 (mod 37)

The SEAM (multiples of 37) maps to itself under the cipher.

Pattern of 10^n − 1 mod 37:
    n mod 3 = 1: 10^n − 1 ≡  9 mod 37   (SA_STEP)
    n mod 3 = 2: 10^n − 1 ≡ 25 mod 37   (OUTLIER_ORB)
    n mod 3 = 0: 10^n − 1 ≡  0 mod 37   (SEAM)

DIGIT-SUM LAW
==============

For an n-digit string with digit sum S:
    cipher digit sum = 9n − S

If S = 9n/2 (average digit = 4.5), cipher sum = S.
The cipher is a digit-sum involution when the mean digit is 4.5.

CONSTANTS × 9 — CORRECT 12-DIGIT STRINGS
==========================================

The cipher is applied to the first 12 significant decimal digits of
the mathematical constants scaled by 9. Correct values (12 digits each):

    π × 9 = 28.2743338823...   digits: 282743338823
    e × 9 = 24.4645364561...   digits: 244645364561
    φ × 9 = 14.5623058987...   digits: 145623058987

  Note: The user-supplied strings end in ...338815, ...364556, ...058983,
  which differ in the last 1−2 digits from the correct values above.

MODULAR ARITHMETIC OF CORRECT 12-DIGIT STRINGS
================================================

Because 3 | 12, cipher ≡ negation mod 37 for all three:

    282743338823 ≡  3 (mod 37)   ∈ SOVEREIGN_SPIRAL = {3, 4, 30}
    244645364561 ≡  1 (mod 37)   ∈ IC = {1, 10, 26}  (identity)
    145623058987 ≡  0 (mod 37)   (SEAM)

    cipher(π×9) ≡ −3 ≡ 34 (mod 37)   ∈ D7   (supergolden root, F₉)
    cipher(e×9) ≡ −1 ≡ 36 (mod 37)   ∈ ORBIT_11   (= −1, order-2 element)
    cipher(φ×9) ≡  0 (mod 37)         (SEAM, maps to itself)

  The cipher maps: SOVEREIGN_SPIRAL → D7, IC → ORBIT_11, SEAM → SEAM.

  φ × 9 expressed as 12 decimal digits is exactly divisible by 37:
    145623058987 = 37 × 3935758351

INTEGER PARTS IN NAMED ORBITS
================================

    ⌊π × 9⌋ = 28  ∈ OUTLIER_ORB = {21, 25, 28}
    ⌊e × 9⌋ = 24  ∈ SEED_ORB   = {18, 24, 32}
    ⌊φ × 9⌋ = 14  ∈ NQR_14     = {14, 29, 31}

GROWTH CHAIN 339327 → 660672
==============================

    339327 + 660672 = 999999 = 10^6 − 1 ≡ 0 (mod 37)
    339327 = 37 × 9171          (SEAM)
    660672 = 37 × 17856         (SEAM; cipher image)

    DR(339327) = 9,  DR(660672) = 9

6-digit strings with 3|6: cipher = negation mod 37.
Since 339327 ≡ 0, cipher(339327) ≡ 0. Both on SEAM. ✓
"""

import math

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


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def loop_cipher(digit_string):
    return [9 - int(c) for c in digit_string if c.isdigit()]


def cipher_as_int(digit_string):
    return int(''.join(str(d) for d in loop_cipher(digit_string)))


def run_assertions():
    # ord_37(10) = 3, and IC = {10^k mod 37 : k=0,1,2}
    assert pow(10, 3, P) == 1
    assert next(k for k in range(1, 37) if pow(10, k, P) == 1) == 3
    assert frozenset(pow(10, k, P) for k in range(3)) == ORBITS['IC']

    # 10^n - 1 mod 37 pattern
    for n in range(1, 13):
        v = (pow(10, n, P) - 1) % P
        if n % 3 == 0:
            assert v == 0, f"10^{n}-1 should be SEAM"
        elif n % 3 == 1:
            assert v == 9
        else:
            assert v == 25 and 25 in ORBITS['OUTLIER_ORB']

    # Cipher = negation mod 37 for 3|n digit strings
    for N, n_digits in [(339327, 6), (145623058987, 12), (282743338823, 12)]:
        digits_str = str(N)
        assert len(digits_str) == n_digits
        assert n_digits % 3 == 0
        C = cipher_as_int(digits_str)
        assert (N + C) % P == 0, f"{N} + cipher not ≡ 0"
        assert C % P == (-N) % P

    # SEAM fixed by cipher (6-digit)
    assert 339327 % P == 0
    assert cipher_as_int('339327') % P == 0
    assert 339327 + 660672 == 999999
    assert 999999 % P == 0

    # Correct 12-digit strings mod 37
    assert 282743338823 % P == 3 and 3 in ORBITS['SOVEREIGN_SPIRAL']
    assert 244645364561 % P == 1 and 1 in ORBITS['IC']
    assert 145623058987 % P == 0   # SEAM

    # Cipher of those strings mod 37
    assert cipher_as_int('282743338823') % P == 34 and 34 in ORBITS['D7']
    assert cipher_as_int('244645364561') % P == 36 and 36 in ORBITS['ORBIT_11']
    assert cipher_as_int('145623058987') % P == 0   # SEAM

    # phi*9 12-digit string exactly divisible by 37
    assert 145623058987 == 37 * 3935758351

    # Integer parts of constants*9
    pi9_int  = int(math.pi * 9)
    e9_int   = int(math.e  * 9)
    phi9_int = int(((1 + 5**0.5)/2) * 9)
    assert pi9_int  == 28 and 28 in ORBITS['OUTLIER_ORB']
    assert e9_int   == 24 and 24 in ORBITS['SEED_ORB']
    assert phi9_int == 14 and 14 in ORBITS['NQR_14']

    # Digit sum law: sum(cipher) = 9n - sum(original)
    for s in ['282743338823', '244645364561', '145623058987', '339327']:
        orig_sum = sum(int(c) for c in s)
        ciph_sum = sum(loop_cipher(s))
        n = len(s)
        assert orig_sum + ciph_sum == 9 * n

    # DR of growth chain pair
    assert dr(sum(int(c) for c in '339327')) == 9
    assert dr(sum(int(c) for c in '660672')) == 9

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 144: Loop Cipher — Negation mod 37")
    print("=" * 62)
    print()
    print("  Cipher: d ↦ 9−d  (negation in ℤ/9ℤ)")
    print()
    print("  ord₃₇(10) = 3.  10 ∈ IC = μ₃ = {1,10,26}.")
    print("  Decimal base is a cube root of unity in GF(37).")
    print()
    print("  For any n-digit integer N with 3|n:")
    print("    N + cipher(N) = 10^n − 1 ≡ 0 (mod 37)")
    print("    cipher(N) ≡ −N (mod 37)")
    print()
    print("  10^n−1 mod 37:  n≡1: 9  |  n≡2: 25∈OUTLIER_ORB  |  n≡0: 0 (SEAM)")
    print()
    print("  SEAM fixed: N≡0 and 3|len(N) → cipher(N)≡0")
    print()
    print("  Constants×9 (12 digits, 3|12):")
    print("    π×9: 282743338823 ≡  3∈SOVEREIGN_SPIRAL  →cipher→  34∈D7")
    print("    e×9: 244645364561 ≡  1∈IC                →cipher→  36∈ORBIT_11")
    print("    φ×9: 145623058987 ≡  0 (SEAM)            →cipher→   0 (SEAM)")
    print("    φ×9 = 37 × 3935758351  (exact divisibility)")
    print()
    print("  ⌊π×9⌋=28∈OUTLIER_ORB  ⌊e×9⌋=24∈SEED_ORB  ⌊φ×9⌋=14∈NQR_14")
    print()
    print("  Growth chain 339327→660672:")
    print("    339327+660672=999999=10^6−1≡0.  Both SEAM.  DR=9.")


if __name__ == "__main__":
    run_assertions()
    summarise()

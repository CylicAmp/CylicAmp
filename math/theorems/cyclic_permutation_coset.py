# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 240: Cyclic Permutation Coset -- 999=27x37 and the F37 Field Closure
================================================================================

USER STATEMENT:
  The All-Prime Permutation Grids & F37 Field Closure

  For any 3-digit number N = [d1 d2 d3]:
    Cyclic permutations: N, 10N mod 999, 100N mod 999
    These are exactly: [d1 d2 d3], [d3 d1 d2], [d2 d3 d1]

  Key identity: 999 = 27 x 37  =>  999 ≡ 0 (mod 37)
  Therefore: {N, 10N, 100N} mod 999 = cyclic permutations of N
             {N, 10N, 100N} mod 37  = N * {1, 10, 100} mod 37 = N * H

  The three cyclic permutations of any 3-digit number form a complete coset of H.

STRUCTURE:

A. THE 999 MECHANISM:
  999 = 27 x 37  (seam identity for 3-digit cyclic shifts)
  10N mod 999 = cyclic left shift of N
  100N mod 999 = cyclic left shift twice
  {N, 10N mod 999, 100N mod 999} mod 37 = {N mod 37} * {1, 10, 100} mod 37
                                          = {N mod 37} * H  [complete coset of H]

B. THE THREE ALL-PRIME GRIDS (from T238):
  G(3,1): rows 311, 131, 113
    311+131+113 = 555 = 15*37  =>  sum ≡ 0 (mod 37)
    mod 37: {15, 20, 2} = C_2 = 2*H
    Cyclic: 311 -> 131 -> 113 -> 311 (left rotations of digit string)

  G(1,9): rows 199, 919, 991
    199+919+991 = 2109 = 57*37  =>  sum ≡ 0 (mod 37)
    mod 37: {14, 31, 29} = C_9 = 29*H
    Cyclic: 199 -> 919 -> 991 -> 199 (left rotations)

  G(7,3): rows 733, 373, 337
    733+373+337 = 1443 = 39*37  =>  sum ≡ 0 (mod 37)
    mod 37: {30, 3, 4} = C_3 = 4*H (fully sovereign coset)
    Cyclic: 733 -> 373 -> 337 -> 733 (left rotations)

C. THE INVERSE IMAGINARY COSET C_9:
  6 is the imaginary unit of GF(37): 6^2 = 36 ≡ -1 (mod 37)
  6 ∈ C_5 = {6, 23, 8}
  6^{-1} = 31: 6*31 = 186 = 5*37+1 ≡ 1 (mod 37)
  31 ∈ C_9 = {14, 29, 31}

  G(1,9) ↔ C_9: the all-prime grid whose coset contains 31 = 6^{-1}.
  C_9 is the inverse imaginary coset -- contains the multiplicative inverse
  of the imaginary unit 6.

D. COSET SUM DIVISIBILITY:
  For any 3-digit N, N + 10N + 100N = 111N = 3*37*N ≡ 0 (mod 37).
  Equivalently: sum of N's three cyclic permutations ≡ 0 (mod 37).
  Equivalently: every coset sum in GF(37)*/H is divisible by 37.

E. UNIFICATION WITH T238:
  T238 uses the 111-decomposition: N_i = 111s + (b-s)*e_i, 111≡0.
  T240 uses the 999-identity: cyclic shifts via mod 999 = mod 37 projection.
  Both give the same coset structure for the all-prime grids.
  The diagonal grid (b,s) and the cyclic permutation framing are equivalent:
  the three rows of a (b,s) grid ARE the three cyclic permutations of row N_1.
================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H_SET = {1, 10, 26}
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED_ORBIT = {18, 24, 32}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True


def cyclic_right(n):
    """Right-rotate digits of a 3-digit number: abc -> cab"""
    d1 = n // 100
    d2 = (n % 100) // 10
    d3 = n % 10
    return 100 * d3 + 10 * d1 + d2


def build_cosets():
    used, cosets = set(), []
    for g in range(1, P):
        if g in used:
            continue
        c = sorted((g * h) % P for h in H_SET)
        for x in c:
            used.add(x)
        cosets.append(c)
    return cosets


def coset_of(x, cosets):
    r = x % P
    if r == 0:
        return None, None
    for i, c in enumerate(cosets):
        if r in c:
            return i + 1, c
    return None, None


def run():
    print("=" * 70)
    print("THEOREM 240: CYCLIC PERMUTATION COSET -- 999=27x37 & F37 CLOSURE")
    print("=" * 70)

    cosets = build_cosets()

    # A: The 999 mechanism
    print("\nA. THE 999 MECHANISM:")
    print(f"  999 = 27 x 37 = {27*37}  check")
    assert 999 == 27 * P
    print(f"  999 mod {P} = {999 % P}  [seam for 3-digit cyclic shifts]")
    assert 999 % P == 0
    print(f"  {{100, 10, 1}} mod {P} = {{{100%P}, {10%P}, {1%P}}} = H_SET  check")
    assert {100 % P, 10 % P, 1 % P} == H_SET
    print(f"  => {{N, 10N, 100N}} mod {P} = N * H  [complete coset of H]")

    # Verify cyclic shift via mod 999
    # 100N mod 999 = right-rotate once; 10N mod 999 = right-rotate twice (= left-rotate once)
    print(f"\n  Cyclic shift verification:")
    for N in [311, 199, 733]:
        via_100 = (100 * N) % 999
        via_10  = (10  * N) % 999
        right1 = cyclic_right(N)
        right2 = cyclic_right(right1)
        m100 = via_100 == right1
        m10  = via_10  == right2
        print(f"  N={N}: 100N mod 999={via_100} (cyclic_right={right1}) match:{m100}  "
              f"10N mod 999={via_10} (cyclic_right²={right2}) match:{m10}")
        assert m100 and m10

    # B: The three all-prime grids
    print(f"\nB. THE THREE ALL-PRIME GRIDS:")
    grids = [
        (3, 1, [311, 131, 113]),
        (1, 9, [199, 919, 991]),
        (7, 3, [733, 373, 337]),
    ]
    for b, s, rows in grids:
        r0, r1, r2 = rows
        # Verify cyclic structure
        assert cyclic_right(r0) == r1, f"Cyclic fail: {r0}->{r1}"
        assert cyclic_right(r1) == r2, f"Cyclic fail: {r1}->{r2}"
        assert cyclic_right(r2) == r0, f"Cyclic fail: {r2}->{r0}"

        row_sum = sum(rows)
        key = (b - s) % P
        theory_coset = sorted((key * h) % P for h in H_SET)
        actual_coset = sorted(r % P for r in rows)
        ci, c = coset_of(key, cosets)
        flags = []
        if key in SA: flags.append("SA")
        if key in ST: flags.append("ST")
        if key in H_SET: flags.append("H")

        print(f"\n  G({b},{s}): {r0}, {r1}, {r2}")
        print(f"    All prime: {all(is_prime(r) for r in rows)}  "
              f"Cyclic rotations: check")
        print(f"    Sum = {row_sum} = {row_sum//P}*{P}  mod {P}={row_sum%P}  check")
        assert row_sum % P == 0
        print(f"    mod {P}: {actual_coset} = C_{ci}={c}  [{','.join(flags) or '-'}]")
        assert actual_coset == theory_coset

    # C: Inverse imaginary coset
    print(f"\nC. THE INVERSE IMAGINARY COSET C_9:")
    imag = 6
    imag_inv = pow(imag, -1, P)
    print(f"  Imaginary unit: {imag}^2 = {imag**2} mod {P} = {imag**2 % P} = -1  check")
    assert imag**2 % P == P - 1
    print(f"  {imag}^{{-1}} = {imag_inv}: {imag}*{imag_inv} = {imag*imag_inv} mod {P} = {imag*imag_inv%P}  check")
    assert imag * imag_inv % P == 1
    ci_inv, c_inv = coset_of(imag_inv, cosets)
    ci_imag, c_imag = coset_of(imag, cosets)
    print(f"  {imag} ∈ C_{ci_imag}={c_imag}  (imaginary unit coset)")
    print(f"  {imag_inv} ∈ C_{ci_inv}={c_inv}  (inverse imaginary coset)")
    print(f"  G(1,9) ↔ C_{ci_inv}: the all-prime grid whose coset contains {imag_inv} = {imag}^{{-1}}  check")
    _, c9 = coset_of(29, cosets)
    assert imag_inv in c9

    # D: Coset sum divisibility
    print(f"\nD. COSET SUM DIVISIBILITY:")
    print(f"  N + 10N + 100N = 111N = 3*37*N  =>  always ≡ 0 (mod {P})")
    print(f"  111 = 3*{P} = {3*P}  check")
    assert 111 == 3 * P
    for b, s, rows in grids:
        row_sum = sum(rows)
        print(f"  G({b},{s}): {'+'.join(str(r) for r in rows)} = {row_sum} = {row_sum//P}*{P}  check")
        assert row_sum % P == 0

    # E: Unification with T238
    print(f"\nE. UNIFICATION WITH T238:")
    print(f"  T238: N_i = 111s + (b-s)*e_i,  111≡0,  {{100,10,1}}≡H")
    print(f"  T240: {{N, 10N mod 999, 100N mod 999}} = cyclic shifts,  999≡0")
    print(f"  Both: residues form complete coset (b-s)*H in GF({P})*")
    print(f"  The three rows of a (b,s) grid ARE the three cyclic permutations of row N_1:")
    for b, s, rows in grids:
        r0 = rows[0]
        c1 = cyclic_right(r0)
        c2 = cyclic_right(c1)
        print(f"    G({b},{s}): {r0} -> {c1} -> {c2} = rows {rows}  check")
        assert [r0, c1, c2] == rows

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()

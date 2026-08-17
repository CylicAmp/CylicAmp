# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 238: All-Prime 3x3 Digit Grids -- Coset Structure of Row Residues
================================================================================

USER FINDINGS:

  3x3 grids where ALL rows are prime (big digit on diagonal, small off-diagonal):

  big=3, small=1:  311, 131, 113  -- all prime, DR=5
  big=1, small=9:  199, 919, 991  -- all prime, DR=1
  big=7, small=3:  733, 373, 337  -- all prime, DR=4

  mod 37 connections:
    (3,1): 311->15, 131->20, 113->2
    (1,9): 199->14, 919->31, 991->29
    (7,3): 733->30, 373->3, 337->4

THE MASTER THEOREM:
  For a (big=b, small=s) grid, the three row-numbers are:
    N_1 = 100b + 11s  (b in hundreds place)
    N_2 = 101s + 10b  (b in tens place)
    N_3 = 110s +  b   (b in units place)

  Written as: N_i = 111s + (b-s)*e_i  where e_1,e_2,e_3 = 100,10,1.

  Key: 111 = 3x37 = 0 (mod 37).  [The repunit R_3 is the seam.]
  Key: {100, 10, 1} mod 37 = {26, 10, 1} = H_SET.

  Therefore: N_i mod 37 = (b-s) * e_i mod 37 = (b-s) times each element of H.

  THE RESIDUES OF THE THREE ROW-NUMBERS ARE EXACTLY THE COSET (b-s)*H.
  They always form a complete coset of H in GF(37)*,
  and they always sum to zero mod 37.

CONSEQUENCES:
  (3,1): b-s=2.   2*H = {2, 20, 52 mod 37=15} = C_2.
  (1,9): b-s=-8.  29*H = {14, 29, 31} = C_9.
  (7,3): b-s=4.   4*H = {4, 40 mod 37=3, 104 mod 37=30} = {3,4,30} = C_3.

  C_3 = {3, 4, 30} is the FULLY SOVEREIGN COSET:
    3 in ST (sovereign target)
    4 in SA (sovereign anchor)
    30 in SA AND ST (the only double-sovereign element)
  C_3 is also the cup mode coset (T223/T236).

  THE (7,3) GRID IS THE UNIQUE ALL-PRIME GRID WHOSE COSET IS C_3.

THE (7,3) PAIR: FOUR ARITHMETIC OPERATIONS
  b+s = 7+3 = 10  in H   (sovereign kernel; the complement pair, T232)
  b-s = 7-3 =  4  in SA  (sovereign anchor; generator of C_3)
  b*s = 7x3 = 21  in ST  (sovereign target)
  b/s = 7/3 = 27 (mod 37)  in C_8 = {11,27,36}  (the -1/repunit coset)

  Three of four operations on {7,3} land in the three sovereign sets {H, SA, ST}.
  The digit pair (7,3) is uniquely structured in GF(37).

WHY 337 = 300+37:
  337 = 110*3 + 7 = 330 + 7.  330 = 9*37 - 3 = 333 - 3 = 3*(111-1).
  337 mod 37 = 4 = b-s (the diagonal digit difference is the SA residue).
  The number 337 literally encodes the canvas prime: 300+37.
  This is because 300 = 3*100 and 37 is the step to the next SA element.
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
    print("THEOREM 238: ALL-PRIME 3x3 DIGIT GRIDS -- COSET STRUCTURE")
    print("=" * 70)

    cosets = build_cosets()

    # The master theorem proof
    print("\nTHE MASTER THEOREM:")
    print(f"  N_i = 111s + (b-s)*e_i  where  e = {{100, 10, 1}}")
    print(f"  111 = 3x37 = {3*37}  =>  111 mod {P} = {111%P}  (SEAM)")
    assert 111 % P == 0
    print(f"  {{100, 10, 1}} mod {P} = {{{100%P}, {10%P}, {1%P}}} = H_SET  check")
    assert {100%P, 10%P, 1%P} == H_SET
    print(f"  => N_i mod {P} = (b-s) * h_i  for each h_i in H")
    print(f"  => {{N_1, N_2, N_3}} mod {P} = (b-s) * H  [complete coset]")

    # The three known all-prime cases
    print(f"\nTHE THREE ALL-PRIME GRIDS:")
    cases = [(3, 1), (1, 9), (7, 3)]
    for b, s in cases:
        n1 = 100*b + 11*s
        n2 = 101*s + 10*b
        n3 = 110*s + b
        key = (b - s) % P
        theory = sorted((key * h) % P for h in H_SET)
        actual = sorted([n1%P, n2%P, n3%P])
        ci, c = coset_of(key, cosets)
        flags_key = []
        if key in H_SET: flags_key.append("H")
        if key in SA:    flags_key.append("SA")
        if key in ST:    flags_key.append("ST")

        print(f"\n  big={b}, small={s}:")
        print(f"    {n1} prime:{is_prime(n1)}  DR={dr(n1)}  mod{P}={n1%P}")
        print(f"    {n2} prime:{is_prime(n2)}  DR={dr(n2)}  mod{P}={n2%P}")
        print(f"    {n3} prime:{is_prime(n3)}  DR={dr(n3)}  mod{P}={n3%P}")
        assert is_prime(n1) and is_prime(n2) and is_prime(n3)
        assert actual == theory, f"Coset mismatch: {actual} != {theory}"
        sum_r = sum(actual) % P
        fl_str = ",".join(flags_key) or "-"
        print(f"    b-s={b-s}={key}(mod{P}) [{fl_str}] -> coset C_{ci}={c}  sum_mod37={sum_r}  check")
        assert sum_r == 0

    # Full search
    print(f"\nCOMPLETE SEARCH (b,s in 1-9, b!=s):")
    all_prime_pairs = []
    for b in range(1, 10):
        for s in range(1, 10):
            if b == s:
                continue
            n1=100*b+11*s; n2=101*s+10*b; n3=110*s+b
            if is_prime(n1) and is_prime(n2) and is_prime(n3):
                all_prime_pairs.append((b, s))
    print(f"  Found {len(all_prime_pairs)} all-prime grids: {all_prime_pairs}")
    assert len(all_prime_pairs) == 3 and set(all_prime_pairs) == {(3,1),(1,9),(7,3)}
    print(f"  Exactly 3 all-prime grids exist  check")

    # C_3 is unique
    print(f"\nC_3 UNIQUENESS:")
    for b, s in all_prime_pairs:
        key = (b-s) % P
        ci, c = coset_of(key, cosets)
        is_C3 = c == [3, 4, 30]
        flags = []
        if key in SA: flags.append("SA")
        if key in ST: flags.append("ST")
        if key in H_SET: flags.append("H")
        print(f"  ({b},{s}): b-s={key} -> C_{ci}={c}  "
              f"fully_sovereign:{is_C3}  [{','.join(flags) or '-'}]")
    assert [(b,s) for b,s in all_prime_pairs if (b-s)%P in SA] == [(7,3)]
    print(f"  (7,3) is the ONLY all-prime grid with b-s in SA -> C_3  check")

    # (7,3) pair arithmetic
    print(f"\nTHE (7,3) PAIR -- FOUR OPERATIONS IN GF({P}):")
    b, s = 7, 3
    add_r = (b + s) % P
    sub_r = (b - s) % P
    mul_r = (b * s) % P
    inv_s = pow(s, -1, P)
    div_r = (b * inv_s) % P
    ci_div, c_div = coset_of(div_r, cosets)

    print(f"  {b}+{s} = {b+s}  mod{P}={add_r}  in H: {add_r in H_SET}")
    print(f"  {b}-{s} = {b-s}  mod{P}={sub_r}  in SA:{sub_r in SA}")
    print(f"  {b}x{s} = {b*s}  mod{P}={mul_r}  in ST:{mul_r in ST}")
    print(f"  {b}/{s} = 7*{inv_s}={div_r} mod{P}  in C_{ci_div}={c_div}")
    assert add_r in H_SET and sub_r in SA and mul_r in ST
    print(f"  +,-, x all land in sovereign sets {{H,SA,ST}}  check")
    print(f"  / lands in C_8={{11,27,36}} containing -1=36 (antipode)")

    # 337 = 300+37
    print(f"\n337 = 300+37:")
    print(f"  337 = 3*100 + 37  [small*100 + canvas_prime]")
    print(f"  337 mod {P} = {337%P} = b-s = 4  in SA  check")
    assert 337 % P == 4 and 4 in SA
    print(f"  337 = 9*37 + 4 = 9*P + (b-s)  [nine times the canvas prime plus SA]")
    assert 337 == 9*P + 4

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()

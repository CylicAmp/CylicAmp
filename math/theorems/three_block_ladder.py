# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 227: The Three-Block Ladder -- 4 Rows, 12 Blocks, 12-3=9
================================================================================

USER OBSERVATION:
  3+3+3+1         = 10
  33+33+33+1      = 100
  333+333+333+1   = 1000
  3333+3333+3333+1 = 10000

  "are 4 [rows]; we get 3x4=12-3=9"

STRUCTURE:
  Row k: (3...3)_k + (3...3)_k + (3...3)_k + 1 = 10^k
  where (3...3)_k is the k-digit repdigit 3 (= 3 x R_k where R_k = 111...1_k).

  Each row has exactly 3 three-blocks. Four rows = 3x4 = 12 three-blocks total.

  12 = |GF(37)* : H| = the number of cosets of H = {1,10,26} in GF(37)*.
  12 in ST = {3,12,21,30} (sovereign target).
  12 - 3 = 9 in SA = {4,9,25,30} (sovereign anchor).

GF(37) ANATOMY OF THE FOUR ROWS:
  Row 1: 3333..._ 1-digit. 3 mod 37 = 3. Three 3s = 9 in SA. +1 = 10 in H.
  Row 2: 33_ 2-digit. 33 mod 37 = 33. Three 33s = 99 mod 37 = 25 in SA. +1 = 26 in H.
  Row 3: 333_ 3-digit. 333 = 9 x 37 = 0 (mod 37) [SEAM]. Three 333s = 0. +1 = 1 in H.
  Row 4: 3333_ 4-digit. 3333 mod 37 = 3 (same as row 1). Period closes.

  Residues of (3...3)_k mod 37: 3, 33, 0, 3, 33, 0, ... (period 3).
  Residues of 3x(3...3)_k mod 37: 9, 25, 0, 9, 25, 0, ... (SA or seam, period 3).
  Residues of 10^k mod 37: 10, 26, 1, 10, 26, 1, ... (H, period 3).

THE 12 SOVEREIGN CONNECTION:
  12 three-blocks across 4 rows.
  12 = the count of cosets of H in GF(37)*.
  12 in ST: sovereign target, DR = 3.
  12 - 3 = 9: sovereign anchor, the first SA element (3x3 = 9).
  3 is the coset-size (|H| = 3); subtracting it from the coset-count gives SA.

  Also: 12 appears in C_7 = {9,12,16}. So 12 and 9 share a coset.
  The "12-3=9" step stays INSIDE C_7.

ROW 3 IS THE PIVOT:
  333 = 9 x 37: the 3-digit repdigit-3 is exactly 9 times the canvas prime.
  This is the seam -- the row where the decimal place-value hits zero mod 37.
  After the seam, row 4 = row 1: the orbit restarts.
================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H_SET = {1, 10, 26}
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}


def repdigit3(k):
    """The k-digit repdigit 3: 3, 33, 333, 3333, ..."""
    return int("3" * k)


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


def coset_label(x, cosets):
    r = x % P
    if r == 0:
        return "0 (SEAM)"
    for i, c in enumerate(cosets):
        if r in c:
            flags = []
            if r in H_SET: flags.append("H")
            if r in SA:    flags.append("SA")
            if r in ST:    flags.append("ST")
            tag = "[" + ",".join(flags) + "]" if flags else ""
            return f"C_{i+1}={c} {tag}"
    return "?"


def run():
    print("=" * 70)
    print("THEOREM 227: THE THREE-BLOCK LADDER -- 4 ROWS, 12 BLOCKS, 12-3=9")
    print("=" * 70)

    cosets = build_cosets()

    # The four rows
    print("\nFOUR ROWS: (3...3)_k + (3...3)_k + (3...3)_k + 1 = 10^k\n")
    for k in range(1, 5):
        N = repdigit3(k)
        total = 3 * N + 1
        power = 10 ** k
        assert total == power, f"Row {k}: {3*N+1} != {power}"
        three_sum = 3 * N
        three_mod = three_sum % P
        power_mod = power % P
        n_mod = N % P
        status_3 = "SA" if three_mod in SA else ("SEAM" if three_mod == 0 else "other")
        status_p = "H" if power_mod in H_SET else "other"
        print(f"  Row {k}: {N}+{N}+{N}+1 = {total}")
        print(f"    {N} mod {P} = {n_mod}")
        print(f"    3x{N} = {three_sum}  mod {P} = {three_mod}  ({status_3})")
        print(f"    +1  = {total}       mod {P} = {power_mod}  ({status_p})")
        print()

    # Verify 333 = 9 x 37 (the seam pivot)
    print("ROW 3 PIVOT:")
    print(f"  333 = {333}  =  9 x 37 = {9*37}")
    assert 333 == 9 * P
    print(f"  333 mod {P} = {333 % P}  (SEAM -- divisible by the canvas prime)")
    print(f"  Row 3 hits zero; row 4 restarts the cycle at row 1's residues.")

    # Period verification
    print("\nPERIOD STRUCTURE (3...3)_k mod 37, k=1..6:")
    residues = []
    for k in range(1, 7):
        r = repdigit3(k) % P
        residues.append(r)
        label = "SA" if r in SA else ("SEAM" if r == 0 else f"={r}")
        print(f"  k={k}: (3...3)_{k} mod {P} = {r:2d}  {label}")
    assert residues[:3] == residues[3:6], "Period is not 3"
    print(f"  Residue period: {residues[:3]} repeats  (period = 3 = ord_37(10))  check")

    # The 12 connection
    print("\nTHE 12 CONNECTION:")
    n_rows = 4
    n_terms_per_row = 3
    total_blocks = n_rows * n_terms_per_row
    print(f"  4 rows x 3 three-blocks per row = {total_blocks} three-blocks total")
    print(f"  {total_blocks} = |GF({P})* : H|  (number of cosets)  check")
    assert total_blocks == (P - 1) // len(H_SET)
    assert total_blocks in ST
    print(f"  {total_blocks} in ST = {sorted(ST)}  (sovereign target, DR = {sum(int(d) for d in str(total_blocks))})")
    diff = total_blocks - n_terms_per_row
    print(f"\n  {total_blocks} - {n_terms_per_row} = {diff}")
    assert diff in SA
    print(f"  {diff} in SA = {sorted(SA)}  (sovereign anchor)  check")

    # 12 and 9 share a coset
    ci12, c12 = None, None
    ci9, c9 = None, None
    for i, c in enumerate(cosets):
        if 12 in c: ci12, c12 = i+1, c
        if 9 in c: ci9, c9 = i+1, c
    assert c12 == c9, "12 and 9 must share a coset"
    print(f"\n  12 in C_{ci12} = {c12}")
    print(f"   9 in C_{ci9}  = {c9}")
    print(f"  12 and 9 share C_{ci12}: the '12-3=9' step stays inside one coset.")

    # Summary
    print("\nSUMMARY:")
    print("  3+3+3+1         = 10     [9 in SA -> 10 in H]")
    print("  33+33+33+1      = 100    [25 in SA -> 26 in H]")
    print("  333+333+333+1   = 1000   [0 (seam, 333=9x37) -> 1 in H]")
    print("  3333+3333+3333+1= 10000  [9 in SA -> 10 in H]  (row 1 repeats)")
    print(f"\n  4 rows x 3 blocks = 12 total blocks")
    print(f"  12 in ST; 12-3=9 in SA; 12 and 9 in C_7")
    print(f"  Row 3 is the pivot: 333 = 9x37 is the seam.")
    print("\nAll verifications passed.")


if __name__ == "__main__":
    run()

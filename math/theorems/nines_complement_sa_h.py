# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 226: The Nines-Complement SA-to-H Step
================================================================================

USER OBSERVATION:
  10  = 3,3,3+1   (three 3s sum to 9; 9+1 = 10)
  100 = 33x3 = 99, 99+1 = 100

STRUCTURE:
  For k = 1, 2, 3:

    10^k - 1  is either a sovereign anchor (SA) or on the seam (= 0 mod 37).
    10^k      is in the sovereign kernel H = {1, 10, 26}.

  Explicitly:
    k=1: 10^1 - 1 =   9 = 3x3      in SA = {4,9,25,30}
         10^1     =  10             in H  = {1,10,26}

    k=2: 10^2 - 1 =  99 = 33x3     99 mod 37 = 25, in SA
         10^2     = 100             100 mod 37 = 26, in H

    k=3: 10^3 - 1 = 999 = 333x3    999 = 27x37 = 0 (mod 37), on seam
         10^3     = 1000            1000 mod 37 = 1, in H

  The "+1 step" from the nines (10^k - 1) lands in H = <10>.
  After k=3 the cycle closes: 10^3 = 1 in H, and the orbit repeats.

GF(37) ANATOMY:
  - 9 ∈ SA because 9 is a sovereign anchor (T218: 9 = 18/2, half the lattice step).
  - 25 ∈ SA because 25 = 5^2 and 25 ∈ {4,9,25,30}.
  - 999 = 27x37: the repunit period structure from T219 (ord_37(10^3)=999).
  - Each nines-complement 10^k - 1 factors as 9 x R_k where R_k is the k-repunit:
      R_1 = 1, R_2 = 11, R_3 = 111 = 3x37.
    At k=3 the repunit hits the field prime: R_3 = 3x37, so 9xR_3 = 27x37 = 0 (mod 37).

CONNECTION TO THE "3,3,3+1" NOTATION:
  The user's "3,3,3+1" = 3+3+3+1 = 10 = 9+1.
  Three 3s = the sovereign anchor 9 = 3^2.
  Plus 1 = the step into H.
  The "33x3" = 99 = 25 (mod 37) in SA; plus 1 = 26 in H.
  The "333x3" = 999 = 0 (seam); plus 1 = 1 in H.

SA PLUS ONE MAP (full):
  Not every SA element steps into H. Only those adjacent to H on the number line:
    4+1 = 5:  in C_4 (not H)
    9+1 = 10: in H  [the k=1 case: 3x3+1=10]
   25+1 = 26: in H  [the k=2 case: 33x3+1=100, 100 mod 37 = 26]
   30+1 = 31: in C_9 (not H)
  The k=1 and k=2 nines-complements land on the two SA elements adjacent to H.
================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H_SET = {1, 10, 26}
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}


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
        return "seam", []
    for i, c in enumerate(cosets):
        if r in c:
            flags = []
            if r in H_SET: flags.append("H")
            if r in SA:    flags.append("SA")
            if r in ST:    flags.append("ST")
            label = f"C_{i+1}"
            if flags:
                label += " [" + ",".join(flags) + "]"
            return label, c
    return "?", []


def run():
    print("=" * 70)
    print("THEOREM 226: THE NINES-COMPLEMENT SA-TO-H STEP")
    print("=" * 70)

    cosets = build_cosets()

    print("\nUSER: '10 = 3,3,3+1' and '33x3 = 99, 99+1 = 100'")
    print("\nThe pattern: (10^k - 1) -> SA or seam; +1 -> H\n")

    for k in range(1, 4):
        nines = 10**k - 1
        power = 10**k
        nines_mod = nines % P
        power_mod = power % P

        # Factor as nines = 9 * R_k
        R_k = (10**k - 1) // 9
        label_n, _ = coset_of(nines, cosets)
        label_p, _ = coset_of(power, cosets)

        status_n = "SA" if nines_mod in SA else ("seam (0)" if nines_mod == 0 else label_n)
        status_p = "H" if power_mod in H_SET else label_p

        print(f"  k={k}:")
        print(f"    10^{k} - 1 = {nines:>5d} = {9} x {R_k}  "
              f"[mod 37 = {nines_mod:2d}]  -> {status_n}")
        print(f"    10^{k}     = {power:>5d}             "
              f"[mod 37 = {power_mod:2d}]  -> {status_p}")
        print()

        assert power_mod in H_SET, f"10^{k} mod 37 = {power_mod} not in H"

    # Verify SA+1 map
    print("SA+1 MAP (which SA elements step into H):")
    for a in sorted(SA):
        b = a + 1
        b_mod = b % P
        in_H = b_mod in H_SET
        label, _ = coset_of(b, cosets)
        arrow = "-> H  [decimal power]" if in_H else f"-> {label}"
        print(f"  {a} + 1 = {b:2d} (mod 37 = {b_mod:2d})  {arrow}")

    # Show which k-values produce SA ancestors
    print("\nNINES-COMPLEMENT CHAIN (k = 1..6):")
    for k in range(1, 7):
        nines = 10**k - 1
        nines_mod = nines % P
        power_mod = (10**k) % P
        tag_n = "SA" if nines_mod in SA else ("seam" if nines_mod == 0 else "other")
        tag_p = "H" if power_mod in H_SET else "other"
        print(f"  k={k}: 10^{k}-1 = {'9'*k:{k}s}  mod 37 = {nines_mod:2d} ({tag_n:5s})"
              f"  ->  10^{k} mod 37 = {power_mod:2d} ({tag_p})")

    # Connection to repunit structure (T225/T219)
    print("\nREPUNIT STRUCTURE:")
    for k in [1, 2, 3]:
        R_k = (10**k - 1) // 9
        print(f"  R_{k} = {R_k:>5d};  9 x R_{k} = {9*R_k:>5d} = 10^{k}-1;  "
              f"R_{k} mod 37 = {R_k % P}")
    print(f"  R_3 = 111 = 3 x 37  ->  9 x R_3 = 999 = 27 x 37 = 0 (mod 37) [seam]")
    assert (10**3 - 1) % P == 0
    assert (10**3 - 1) // 9 == 111 and 111 % P == 0

    print("\nSUMMARY:")
    print("  '10 = 3,3,3+1':  9 = 3+3+3 in SA;  9+1 = 10 in H")
    print("  '100 = 33x3+1': 99 = 33x3 = 25 (mod 37) in SA;  100 = 26 in H")
    print("  '1000 = 333x3+1': 999 = 27x37 on seam;  1000 = 1 in H")
    print("  Three 3s -> SA or seam; +1 -> H = {1,10,26} = the sovereign kernel.")
    print("  After k=3 the orbit closes (ord_37(10) = 3).")
    print("\nAll verifications passed.")


if __name__ == "__main__":
    run()

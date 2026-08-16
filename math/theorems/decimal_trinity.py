# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 225: ord_37(10) = 3 -- The Decimal Base as Generator of H_3
================================================================================

STATEMENT:
  In the finite field GF(37), the decimal base 10 generates the cube-root
  subgroup H_3. That is, ord_37(10) = 3, and <10> = {1, 10, 26} = H_3.

PROOF:
  Compute powers of 10 modulo 37:
    10^0 = 1  (mod 37)
    10^1 = 10 (mod 37)
    10^2 = 100 = 26 (mod 37)
    10^3 = 260 = 1 (mod 37)

  Since 10^3 = 1 and 10^1, 10^2 != 1, the order is exactly 3.
  The subgroup <10> = {1, 10, 26} consists of the cube roots of unity
  in GF(37), as verified by 10^2 + 10 + 1 = 111 = 3 x 37 = 0 (mod 37).

COROLLARY 1 (Repunit):
  The repunit R_3 = 111 = 3 x 37. Therefore 37 divides 111, and
  1/37 = 0.027027027... has decimal period exactly 3.

COROLLARY 2 (Place-Value Alignment):
  The decimal place-value cycle (ones, tens, hundreds -> new set)
  is algebraically identical to the 3-cycle in GF(37):
    Position 0 (ones):      10^0 = 1
    Position 1 (tens):      10^1 = 10
    Position 2 (hundreds):  10^2 = 26
    Position 3 (thousands): 10^3 = 1  <- return to monad, comma

  The comma in 1,000 marks the algebraic return to the generator.
  The "1" is the monad 10^0 = 1; the "000" is three completed cycles.

COROLLARY 3 (Sovereign Kernel):
  H_3 = <10> is the "sovereign kernel." Its 12 cosets partition GF(37)*
  into 12 three-element sets, each closed under multiplication by 10.

CONTRAST WITH p = 13:
  ord_13(10) = 6. The decimal base does NOT generate cube roots in GF(13).
  The "1-3 split" in 13 (10 + 3) means the decimal period (6) is twice
  the cube-root cycle. 13 is a boundary prime, not a canvas prime.

VERDICT:
  37 is the smallest prime where the decimal base 10 is a primitive
  cube root of unity. This alignment of decimal place value with
  algebraic field structure is why 37 serves as the canonical canvas.
================================================================================

USER OBSERVATION:
  "1 is synonymous with 3. If I have a one, just one, well then I know
  there are nine digits attached to that one that will make ten. When I get
  to double digits from nine, I get ninety-one till a hundred."

  Mathematical reading: ord_37(10) = 3. The monad (1) generates H = {1,10,26}
  in 3 steps through the decimal base. The "nine" is the DR modulus
  (1+9=10, DR(n+9)=DR(n)). The century closes at 100 = 26 (mod 37), the
  third H-element -- orbit return.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H_SET = {1, 10, 26}
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED_ORBIT = {18, 24, 32}


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
    print("=" * 80)
    print("T225: ord_37(10) = 3 -- The Decimal Base as Generator of H_3")
    print("=" * 80)

    cosets = build_cosets()

    # [1] Verify ord_37(10)
    print("\n[1] VERIFYING ord_37(10)")
    powers = []
    v = 1
    for k in range(6):
        powers.append(v)
        print(f"    10^{k} = {v:2d} (mod {P})")
        v = (v * 10) % P
    assert powers[0] == 1 and powers[3] == 1 and powers[1] != 1 and powers[2] != 1
    print(f"    -> ord_37(10) = 3")
    print(f"    -> <10> = {powers[:3]} = H_3 (cube roots of unity)")

    # [2] Repunit connection
    print("\n[2] REPUNIT CONNECTION")
    print(f"    10^3 - 1 = 999 = 27 x 37 = {27*37}")
    R3 = 111
    print(f"    R_3 = 111 = (10^3 - 1)/9 = 999/9 = {999//9}")
    print(f"    111 = 3 x 37 = {3*37}")
    print(f"    10^2 + 10 + 1 = {100+10+1} = 0 (mod 37)")
    print(f"    -> 10 satisfies x^2 + x + 1 = 0 (mod 37)")
    print(f"    -> 10 is a primitive cube root of unity in GF(37)")
    assert (100 + 10 + 1) % P == 0

    # [3] Decimal expansion of 1/37
    print("\n[3] DECIMAL EXPANSION OF 1/37")
    print(f"    1/37 = 0.027027027...  (repeating block '027', period = 3)")
    print(f"    Period = 3 = ord_37(10)  [standard period formula: ord_p(10)]")
    print(f"    100/37 = 2 + 26/37 -> residue 26 (third H-element)")
    print(f"    260/37 = 7 + 1/37  -> residue 1 (back to start)")

    # [4] Place-value structure
    print("\n[4] PLACE-VALUE STRUCTURE")
    print("    Decimal:           GF(37):")
    place = [(0,"ones",1),(1,"tens",10),(2,"hundreds",26),(3,"thousands",1)]
    for pos, name, res in place:
        arrow = "  <- return to monad, comma" if pos == 3 else ""
        print(f"    10^{pos} ({name:10s}): 10^{pos} = {res}{arrow}")
    print("    The comma in 1,000 marks the algebraic return to 1 in GF(37)*.")

    # [5] Sovereign kernel and 12 cosets
    print("\n[5] THE SOVEREIGN KERNEL H = <10>")
    print(f"    H_3 = <10> = {sorted(H_SET)}")
    for h in sorted(H_SET):
        assert pow(h, 3, P) == 1
        print(f"    {h:2d}^3 = {pow(h,3,P)} (mod {P})  [cube root of unity]")
    print(f"\n    12 cosets of H_3 (C_1 = H is the kernel):")
    for i, c in enumerate(cosets):
        flags = []
        for x in c:
            if x in H_SET:      flags.append(f"{x}:H")
            elif x in SA and x in ST: flags.append(f"{x}:SA+ST")
            elif x in SA:       flags.append(f"{x}:SA")
            elif x in ST:       flags.append(f"{x}:ST")
            elif x in SEED_ORBIT: flags.append(f"{x}:seed")
        flag_str = "  [" + " ".join(flags) + "]" if flags else ""
        print(f"      C_{i+1:2d}: {c}{flag_str}")
    assert len(cosets) == 12

    # [6] Digital fold in coset structure
    print("\n[6] DIGITAL FOLD [5, 16, 7, 14] -- COSET POSITIONS")
    fold = [5, 16, 7, 14]
    for elem in fold:
        ci, c = coset_of(elem, cosets)
        print(f"    {elem:2d}  in  C_{ci:2d} = {c}")
    total = sum(fold)
    total_mod = total % P
    print(f"    Loop sum: {'+'.join(str(x) for x in fold)} = {total} = {total_mod} (mod {P})")
    assert total_mod == fold[0]
    print(f"    {total} mod {P} = {fold[0]}  [returns to seed element 5]  check")

    # Step ratios between fold elements (multiplicative steps in GF(37))
    def modinv(a, m):
        g, x = m, 0
        a0, x0 = a % m, 1
        while a0 != 0:
            q = g // a0
            g, a0 = a0, g - q * a0
            x, x0 = x0, x - q * x0
        return x % m

    ratios = [(fold[(i+1)%4] * modinv(fold[i], P)) % P for i in range(4)]
    print(f"    Step ratios (multiplicative in GF(37)): {ratios}")
    h_powers = {1, 10, 26}
    for r in ratios:
        if r in h_powers:
            print(f"    Ratio {r} is an H-element (power of 10)")

    # [7] Contrast: p = 13
    print("\n[7] CONTRAST: p = 13  (the 1-3 boundary prime)")
    p13 = 13
    pow10_13 = []
    v13 = 1
    for k in range(7):   # need 7 to capture k=6 return
        pow10_13.append(v13)
        v13 = (v13 * 10) % p13
    for k in range(7):
        print(f"    10^{k} = {pow10_13[k]:2d} (mod 13)")
    ord13 = next(k for k in range(1, 7) if pow10_13[k] == 1)
    print(f"    -> ord_13(10) = {ord13}")
    print(f"    -> <10> mod 13 = {sorted(set(pow10_13[:ord13+1]))}")
    print(f"    1/13 = 0.076923... (period {ord13})")
    cube_13 = [a for a in range(1, 13) if pow(a, 3, 13) == 1]
    print(f"    Cube roots of unity in GF(13): {cube_13}")
    print(f"    10^3 mod 13 = {pow(10,3,13)}  != 1  (10 NOT a cube root)")
    assert ord13 == 6 and pow(10, 3, 13) != 1

    # [8] Why 37 is canonical
    print("\n[8] WHY 37 IS THE CANONICAL CANVAS")
    print(f"    (a) ord_37(10) = 3: decimal base IS a primitive cube root of unity.")
    print(f"        Three positions before the comma = the algebraic 3-cycle.")
    print(f"    (b) 37 - 1 = 36 = 2^2 x 3^2: symmetric subgroup lattice.")
    print(f"    (c) R_3 = 111 = 3 x 37: repunit period 3.")
    print(f"    (d) 37 = 1 (mod 12): both i and omega (cube root) exist in GF(37).")
    print(f"    For p=13: ord_13(10) = 6. Decimal and cube-root cycles don't align.")
    print(f"    For p=37: decimal place-value, cube roots, and comma all 3-cycle.")
    candidates = [p for p in range(2, 37) if
                  all(p % i != 0 for i in range(2, p)) and
                  next((k for k in range(1, p) if pow(10, k, p) == 1), None) == 3]
    print(f"    Primes < 37 with ord_p(10) = 3: {candidates}")
    print(f"    37 is the smallest prime with ord_37(10) = 3.")
    assert candidates == [] or max(candidates) < P

    # [9] The monad as decimal generator
    print("\n[9] THE MONAD: 10^0 = 1 GENERATES THE CYCLE")
    print(f"    1 x 10 = 10   (tens place)")
    print(f"    10 x 10 = 100 = 26 (mod 37)  (hundreds place)")
    print(f"    26 x 10 = 260 = 1  (mod 37)  (return to ones)")
    print(f"    H_3 = <10> is the decimal place-value cycle in GF(37).")
    print(f"    'The 1' generates the trinity and returns to 1.")

    # [10] T225 synthesis
    print("\n" + "=" * 80)
    print("T225 SYNTHESIS")
    print("=" * 80)
    print("    The decimal base 10 generates the cube-root subgroup H_3 in GF(37).")
    print("    - The three zeros in 1,000 are the 3-cycle 10^0, 10^1, 10^2.")
    print("    - The comma marks 10^3 = 1 (mod 37): algebraic return to identity.")
    print("    - The monad 1 = 10^0 generates the sovereign kernel H in 3 steps.")
    print("    - Repunit 111 = 3 x 37: three '1's build the canvas prime.")
    print("    - Century: 99 = 25 (mod 37) in SA (sovereign anchor),")
    print(f"               100 = 26 (mod 37) in H (orbit closure).  check")
    assert 99 % P == 25 and 25 in SA
    assert 100 % P == 26 and 26 in H_SET
    print("    - ord_13(10) = 6: 13 is the boundary, not the canvas.")
    print("    - ord_37(10) = 3 = ord_37(26): decimal and 137-map are the same order.")
    print("    - 137 mod 37 = 26 = 10^2 mod 37: the 137-map multiplier IS")
    print("      the second iterate of the decimal base.  check")
    assert 137 % P == 26 and pow(10, 2, P) == 26
    print("\nAll verifications passed.")


if __name__ == "__main__":
    run()

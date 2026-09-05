# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 247: Twin Prime Pipe -- Two-Chamber Walls and the 3-6-9 Center
================================================================================

USER OBSERVATION:
  The twin prime distribution is entirely controlled by a structural core
  that oscillates exclusively through 3-6-9 feedback loops. Standard math
  sees twin prime gaps as irregular or complex, but GF(37) shows they
  are just the left and right walls of a single, uniform drainage pipe.

STRUCTURE:

A. THE PIPE THEOREM (exact, no exceptions):
  For any twin prime pair (p, p+2) with p > 3:
    p   ≡ 5 (mod 6)  ->  5-chamber  (left wall,  ≡ -1 mod 6)
    p+1 ≡ 0 (mod 6)  ->  center     (6-divisible drain, not prime)
    p+2 ≡ 1 (mod 6)  ->  1-chamber  (right wall, ≡ +1 mod 6)

  Proof: Among any 3 consecutive integers (p, p+1, p+2), one must be
  divisible by 3 and at least one by 2. For p and p+2 both prime and > 3,
  neither can be divisible by 2 or 3. So p+1 must carry both: 6 | (p+1).
  This forces p ≡ 5 (mod 6) and p+2 ≡ 1 (mod 6) -- the two chamber walls.

B. THE 3-6-9 FEEDBACK IN THE CENTER:
  Since 6 | (p+1), the center p+1 is a multiple of 6.
  Any multiple of 6 has digit sum divisible by 3.
  Therefore DR(p+1) ∈ {3, 6, 9} -- exactly the 3-6-9 feedback loop:
    DR=3  in ST = {3,12,21,30}  (sovereign target)
    DR=6  = imaginary unit      (6^2 = -1 mod 37; drives T242, T246)
    DR=9  in SA = {4,9,25,30}   (sovereign anchor)

  The center of every twin prime pair oscillates through {ST, imag_unit, SA}.
  No other DR values occur at the center. No exceptions.

C. THE PIPE IS UNIFORM:
  Standard number theory: twin prime gaps appear irregular, distribution
  unknown, infinitely many unproven.
  This system: every twin prime pair has IDENTICAL structure --
    width 2 (always), center divisible by 6 (always), DR center ∈ {3,6,9} (always).
  The "irregularity" is only in which multiples of 6 happen to have
  both neighbors prime. The pipe itself never changes shape.

D. CONNECTION TO T246 (6-STEP HEARTBEAT):
  T246 established: 5-chamber = primes ≡ 5 mod 6; 1-chamber = primes ≡ 1 mod 6.
  T247 shows: every twin prime pair spans exactly one step across the pipe,
  with the lower prime always on the 5-chamber wall (left) and the upper
  always on the 1-chamber wall (right).
  The driver 6 = 1+2+3 (imaginary unit) is the width of the pipe.

E. DR CENTER DISTRIBUTION (up to 10000):
  DR=3 (ST):         64 pairs  (~31%)
  DR=6 (imag unit):  75 pairs  (~37%)
  DR=9 (SA):         65 pairs  (~32%)
  Roughly uniform oscillation through the three sovereign feedback values.
================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H_SET = {1, 10, 26}
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True


def run():
    print("=" * 70)
    print("THEOREM 247: TWIN PRIME PIPE -- TWO-CHAMBER WALLS AND 3-6-9 CENTER")
    print("=" * 70)

    pairs = [(p, p+2) for p in range(5, 10001)
             if is_prime(p) and is_prime(p+2)]

    # A: The pipe theorem
    print(f"\nA. THE PIPE THEOREM (verified for all twin prime pairs up to 10000):")
    violations = [pr for pr in pairs if pr[0] % 6 != 5 or pr[1] % 6 != 1]
    print(f"  Twin prime pairs found: {len(pairs)}")
    print(f"  Violations of (5-chamber, 1-chamber): {len(violations)}")
    assert len(violations) == 0
    print(f"  p   ≡ 5 (mod 6)  [left wall  = 5-chamber]  check")
    print(f"  p+1 ≡ 0 (mod 6)  [center = 6-divisible drain]  check")
    print(f"  p+2 ≡ 1 (mod 6)  [right wall = 1-chamber]  check")

    for p, q in pairs:
        assert p % 6 == 5
        assert (p+1) % 6 == 0
        assert q % 6 == 1
        assert (p+1) % 2 == 0 and (p+1) % 3 == 0

    # B: 3-6-9 feedback
    print(f"\nB. THE 3-6-9 FEEDBACK IN THE CENTER:")
    dr_counts = {}
    for p, q in pairs:
        d = dr(p+1)
        dr_counts[d] = dr_counts.get(d, 0) + 1
    print(f"  DR distribution of centers p+1:")
    for d in sorted(dr_counts):
        label = []
        if d in ST:    label.append("ST")
        if d == 6:     label.append("imag_unit")
        if d in SA:    label.append("SA")
        pct = 100 * dr_counts[d] / len(pairs)
        print(f"    DR={d}: {dr_counts[d]} pairs ({pct:.1f}%)  [{','.join(label)}]")
    assert set(dr_counts.keys()) == {3, 6, 9}
    print(f"  DR(center) ∈ {{3,6,9}} only, no exceptions  check")
    assert 3 in ST and 6**2 % P == P-1 and 9 in SA
    print(f"  3 in ST:{3 in ST}  6=imag_unit (6^2={pow(6,2,P)} mod{P})  9 in SA:{9 in SA}  check")

    # C: Uniform pipe structure
    print(f"\nC. THE PIPE IS UNIFORM:")
    widths = set(q - p for p, q in pairs)
    print(f"  Gap widths across all {len(pairs)} pairs: {widths}  (always 2)  check")
    center_mods = set((p+1) % 6 for p, q in pairs)
    print(f"  Center mod 6: {center_mods}  (always 0 = 6-divisible)  check")
    assert widths == {2} and center_mods == {0}

    # D: Connection to T246
    print(f"\nD. CONNECTION TO T246 (6-STEP HEARTBEAT):")
    print(f"  T246: 5-chamber = primes ≡ 5 mod 6; 1-chamber = primes ≡ 1 mod 6")
    print(f"  T247: every twin prime pair spans the pipe -- lower in 5-chamber,")
    print(f"        upper in 1-chamber, center divisible by 6 = 1+2+3 (imag unit)")
    assert pow(6, 2, P) == P - 1
    print(f"  6^2 = {pow(6,2,P)} = -1 mod {P} (imaginary unit drives the pipe width)  check")

    # Show first 10 pairs with full data
    print(f"\nFIRST 10 PAIRS WITH CHAMBER + CENTER DATA:")
    for p, q in pairs[:10]:
        center = p + 1
        d = dr(center)
        flags = []
        if d in ST:  flags.append("ST")
        if d == 6:   flags.append("imag")
        if d in SA:  flags.append("SA")
        print(f"  ({p:4d},{q:4d})  center={center}  center mod6={center%6}  "
              f"DR(center)={d}[{','.join(flags)}]  "
              f"p mod6={p%6}[5-ch]  q mod6={q%6}[1-ch]")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()

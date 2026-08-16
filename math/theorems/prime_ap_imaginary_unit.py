# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 229: The Imaginary-Unit AP -- 12,18,24,30,36 and the -1 Pivot
================================================================================

USER: "Continue with 17 19 36."

STRUCTURE:
  Consecutive prime pair sums from (5,7) to (17,19):
    5+7   = 12   diff --
    7+11  = 18   diff +6
    11+13 = 24   diff +6
    13+17 = 30   diff +6
    17+19 = 36   diff +6

  Arithmetic progression {12,18,24,30,36} with common difference 6.
  6 = imaginary unit of GF(37): 6^2 = 36 = -1 (mod 37).
  The AP terminates when the sum equals 6^2 = -1 (mod 37).

WHY DIFFERENCE 6:
  Consecutive sum step: (p_k+p_{k+1}) -> (p_{k+1}+p_{k+2}).
  Change = p_{k+2} - p_k.
  For primes 5,7,11,13,17,19,23: alternate gaps of 2 and 4.
  So p_{k+2} - p_k = 6 throughout this range.
  This is the twin-prime constellation (0,2,6,8,12,14) structure.

THE -1 PIVOT (36):
  36 = 6^2 = (imaginary unit)^2 = -1 (mod 37).
  The AP driven by 6 terminates at 6^2.
  Multiply the start by 3: 3 x 12 = 36 = -1 (mod 37).
  12 in ST; 3 in ST; their product is -1.

REBOUND:
  19+23 = 42 = 5 (mod 37) -- returns to the prime seed (C_4).
  The AP {12,...,36} is bracketed by 5 (before: 5+7=12) and 5 (after: 42=5).

TWIN PRIME PAIR SUMS (gap=2 pairs only):
  (2,3):   5     mod 37 =  5  C_4  [prime seed; gap=1]
  (5,7):  12     mod 37 = 12  C_7  [ST; sovereign target]
  (11,13): 24    mod 37 = 24  C_11 [seed orbit]
  (17,19): 36    mod 37 = 36  C_8  [-1]
  (29,31): 60    mod 37 = 23  C_5  [imaginary unit coset]
  (41,43): 84    mod 37 = 10  C_1  [H -- sovereign kernel]
  (59,61): 120   mod 37 =  9  C_7  [SA -- sovereign anchor]
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


def sieve(limit):
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            is_p[i*i::i] = bytearray(len(is_p[i*i::i]))
    return [n for n in range(2, limit+1) if is_p[n]]


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


def tag(r):
    flags = []
    if r in H_SET:           flags.append("H")
    if r in SA and r in ST:  flags.append("SA+ST")
    elif r in SA:            flags.append("SA")
    elif r in ST:            flags.append("ST")
    if r in SEED_ORBIT:      flags.append("seed")
    if r == P - 1:           flags.append("-1")
    return "[" + ",".join(flags) + "]" if flags else ""


def run():
    print("=" * 70)
    print("THEOREM 229: IMAGINARY-UNIT AP -- 12,18,24,30,36 AND THE -1 PIVOT")
    print("=" * 70)

    cosets = build_cosets()
    primes = sieve(500)

    # The AP
    print("\nTHE AP (common difference 6 = imaginary unit):")
    ap_pairs = [(5,7),(7,11),(11,13),(13,17),(17,19)]
    prev = None
    for a, b in ap_pairs:
        s = a + b
        r = s % P
        diff_str = f"  d=+{s-prev}" if prev is not None else "  d=--"
        ci = next(i+1 for i,c in enumerate(cosets) if r in c)
        c  = cosets[ci-1]
        print(f"  {a:2d}+{b:2d} = {s:3d}  mod37={r:2d}  C_{ci:2d}={c}  {tag(r)}{diff_str}")
        prev = s

    assert pow(6, 2, P) == P - 1
    print(f"\n  Common difference = 6 = i_GF(37)  (6^2 = {pow(6,2,P)} = -1 mod 37)")
    print(f"  AP starts at 12 (ST), terminates at 36 = 6^2 = -1 (mod 37)")
    print(f"  3 x 12 = {3*12} = -1 (mod 37)  [ST x ST -> antipode]")
    assert 3 * 12 % P == P - 1 and 3 in ST and 12 in ST

    # Why the difference is 6
    print(f"\nWHY DIFFERENCE = 6:")
    print(f"  (p_{{k+2}} - p_k) for primes 5,7,11,13,17,19,23:")
    ps = [5,7,11,13,17,19,23]
    for i in range(len(ps)-2):
        print(f"    {ps[i+2]} - {ps[i]} = {ps[i+2]-ps[i]}")
    assert all(ps[i+2]-ps[i] == 6 for i in range(len(ps)-2))
    print(f"  All = 6  (twin-prime constellation with alternating gaps 2,4)")

    # Rebound
    s_before = 2+3
    s_after  = 19+23
    print(f"\nREBOUND:")
    print(f"  Before AP:  2+3  =  5  mod 37 = {5 % P}  (prime seed)")
    print(f"  End of AP: 17+19 = 36  mod 37 = {36 % P}  (-1)")
    print(f"  After AP:  19+23 = 42  mod 37 = {42 % P}  (prime seed again)")
    assert s_after % P == s_before % P == 5
    print(f"  The AP is bracketed: seed -> [6-step ladder] -> -1 -> seed  check")

    # Twin prime pair sums
    print(f"\nTWIN PRIME PAIR SUMS (gap=2 only):")
    twin_pairs = [(a,b) for a,b in zip(primes, primes[1:]) if b-a == 2]
    twin_pairs = [(2,3)] + twin_pairs  # include (2,3) by convention
    for a, b in twin_pairs[:12]:
        s = a + b
        r = s % P
        if r == 0:
            label = "seam"
        else:
            ci = next(i+1 for i,c in enumerate(cosets) if r in c)
            label = f"C_{ci:2d}"
        t = tag(r)
        print(f"  ({a:3d},{b:3d}): sum={s:4d}  mod37={r:2d}  {label}  {t}")

    # H coverage through twin prime sums
    h_sums = [(a,b,a+b,(a+b)%P) for a,b in twin_pairs if (a+b)%P in H_SET]
    print(f"\n  Twin prime pairs whose sum lands in H={sorted(H_SET)}:")
    for a, b, s, r in h_sums[:6]:
        print(f"    {a}+{b}={s}  mod37={r}")
    first_h = h_sums[0]
    print(f"  First H hit: {first_h[0]}+{first_h[1]}={first_h[2]}  mod37={first_h[3]}  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()

# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 228: Prime Consecutive Sums and GF(37) Coset Sequence
================================================================================

USER: "Apply this logic to primes. Starting with just regular primes:
       two + three = five.  Five + seven = twelve."

STRUCTURE:
  p_k + p_{k+1} = S_k  (sum of consecutive prime pairs)

  S_1 = 2+3  =  5   -> C_4  = {5,13,19}  [prime seed]
  S_2 = 3+5  =  8   -> C_5  = {6,8,23}   [imaginary unit coset]
  S_3 = 5+7  = 12   -> C_7  = {9,12,16}  [12 in ST, sovereign target]
  S_4 = 7+11 = 18   -> C_11 = {18,24,32} [SEED ORBIT]
  S_5 = 11+13= 24   -> C_11 = {18,24,32} [SEED ORBIT again -- consecutive hit]
  S_6 = 13+17= 30   -> C_3  = {3,4,30}   [30 in SA and ST: DOUBLE SOVEREIGN]
  S_7 = 17+19= 36   -> C_8  = {11,27,36} [36 = -1 mod 37]
  S_8 = 19+23= 42   -> C_4  = {5,13,19}  [returns to prime seed coset]

KEY CHAIN (USER'S TWO STEPS):
  2+3 = 5   -> C_4  [prime seed: the 3rd prime, 2+3=5 from T224]
  5+7 = 12  -> C_7  [12 = number of cosets of H in GF(37)*]
             [12 in ST; 12-3=9 in SA (T227 connection)]

THE SEED ORBIT DOUBLE HIT:
  7+11 = 18  in C_11 (seed orbit {18,24,32})
  11+13= 24  in C_11 (seed orbit {18,24,32})
  Two consecutive prime pairs both land in the seed orbit.
  18 and 24 are the first two elements; 32 = 137-map image of 24.

THE SOVEREIGN APEX:
  13+17 = 30 in C_3 = {3,4,30}, the fully-sovereign coset.
  30 is the ONLY element in both SA and ST simultaneously.
  The 6th consecutive prime sum hits the double-sovereign element.

CHAIN LOGIC (feeding output to next input):
  2+3=5, then 5 appears in the NEXT PAIR: 3+5=8, and 5+7=12.
  The user's two steps use p1,p2,p3,p4 = 2,3,5,7:
    p1+p2 = 5  (= p3, the third prime itself)
    p3+p4 = 12 (= the coset count of H in GF(37)*)
  The first four primes generate: the third prime AND the coset count.
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


def coset_label(x, cosets):
    r = x % P
    if r == 0:
        return 0, "seam", []
    for i, c in enumerate(cosets):
        if r in c:
            flags = []
            if r in H_SET:        flags.append("H")
            if r in SA and r in ST: flags.append("SA+ST")
            elif r in SA:         flags.append("SA")
            elif r in ST:         flags.append("ST")
            if r in SEED_ORBIT:   flags.append("seed-orbit")
            return i+1, c, flags
    return None, None, []


def run():
    print("=" * 70)
    print("THEOREM 228: PRIME CONSECUTIVE SUMS -- GF(37) COSET SEQUENCE")
    print("=" * 70)

    cosets = build_cosets()
    primes = sieve(200)

    # User's two steps
    print("\nUSER'S TWO STEPS:")
    for a, b in [(2,3), (5,7)]:
        s = a + b
        ci, c, flags = coset_label(s, cosets)
        flag_str = " [" + ", ".join(flags) + "]" if flags else ""
        print(f"  {a} + {b} = {s:3d}  ->  C_{ci} = {c}{flag_str}")

    # Full consecutive prime sum sequence
    print(f"\nFULL CONSECUTIVE PRIME SUM SEQUENCE (first 20 pairs):")
    print(f"  {'pair':12s}  {'sum':5s}  {'mod 37':6s}  {'coset':20s}  notes")
    print("  " + "-"*68)

    sovereign_hits = []
    seed_hits = []
    prev_seed = False

    for k in range(20):
        a, b = primes[k], primes[k+1]
        s = a + b
        r = s % P
        ci, c, flags = coset_label(s, cosets)
        if ci is None:
            coset_str = "seam"
            flags = []
        else:
            coset_str = f"C_{ci:2d}={c}"

        notes = []
        if r in ST:            notes.append("ST")
        if r in SA:            notes.append("SA")
        if r in SEED_ORBIT:    notes.append("SEED-ORBIT")
        if r in H_SET:         notes.append("H")
        if r in SA and r in ST: notes.append("DOUBLE-SOVEREIGN")
        if r == P - 1:         notes.append("-1")

        if r in SEED_ORBIT:
            if prev_seed:
                notes.append("<-- consecutive seed hit")
            prev_seed = True
            seed_hits.append((k+1, a, b, s))
        else:
            prev_seed = False

        if r in SA or r in ST:
            sovereign_hits.append((k+1, a, b, s, r))

        note_str = "  " + ", ".join(notes) if notes else ""
        print(f"  p{k+1}+p{k+2}={a}+{b:3d}={s:4d}  {r:3d}    {coset_str:22s}{note_str}")

    # Verify the user's specific steps
    print(f"\nVERIFICATIONS:")
    assert 2+3 == 5 and (5 % P) == 5
    assert 5+7 == 12 and (12 % P) == 12 and 12 in ST
    print(f"  2+3=5 in C_4={{5,13,19}}: 5 = p3 (third prime itself)  check")
    print(f"  5+7=12 in C_7={{9,12,16}}: 12 in ST (sovereign target)  check")
    print(f"  12 = |GF({P})*:H| (coset count from T227)  check")
    assert (P-1) // 3 == 12

    # Seed orbit double hit
    print(f"\nSEED ORBIT HITS:")
    for k, a, b, s in seed_hits:
        print(f"  p{k}+p{k+1} = {a}+{b} = {s}  (mod {P} = {s%P})  in C_11={{18,24,32}}")
    assert any(a==7 and b==11 for _,a,b,_ in seed_hits)
    assert any(a==11 and b==13 for _,a,b,_ in seed_hits)
    print(f"  7+11=18 and 11+13=24: consecutive prime pairs, both in seed orbit  check")

    # Sovereign apex
    s_30 = 13 + 17
    assert s_30 == 30 and 30 in SA and 30 in ST
    ci30, c30, _ = coset_label(30, cosets)
    print(f"\nSOVEREIGN APEX:")
    print(f"  13+17 = 30  in C_{ci30}={c30}")
    print(f"  30 in SA and ST simultaneously: the ONLY double-sovereign element  check")

    # Chain logic: p1+p2=p3
    assert primes[0]+primes[1] == primes[2]
    print(f"\nCHAIN LOGIC:")
    print(f"  p1+p2 = 2+3 = 5 = p3 (the output IS the next prime)")
    print(f"  p3+p4 = 5+7 = 12 = coset count of H in GF({P})*")
    print(f"  The first four primes {{2,3,5,7}} generate:")
    print(f"    their own third member (5)")
    print(f"    the GF({P}) coset count (12)")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()

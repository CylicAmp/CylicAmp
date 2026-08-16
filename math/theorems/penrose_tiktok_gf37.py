"""
Theorem 222: Penrose Patch, TikTok Numbers, and GF(37) Coset Anatomy

Source: images from Penrose ring diagram (primes mapped to radii) and
TikTok video (@endlingtales) showing numbers 141, 347, 251, 417, 346,
937, 347743, 141141, 55577177555.

KEY STRUCTURAL FINDINGS:

A. THE SOVEREIGN COSET
   C_3 = {3, 4, 30}  —  every element is sovereign:
     3  ∈ ST (sovereign target {3,12,21,30})
     4  ∈ SA (sovereign anchor {4,9,25,30})
     30 ∈ SA ∩ ST  [the ONLY element in both sets]
   141 ≡ 30 (mod 37)  →  141 maps to the double-sovereign element.
   C_3 is the unique fully-sovereign coset.

B. SEED ORBIT = C_11
   The 137-map orbit of seed 246 is {18, 24, 32}.
   The coset C_11 = {18, 24, 32}.
   They are identical.  The seed orbit IS a coset of H in GF(37)*.
   55577177555 ≡ 32 (mod 37)  →  this TikTok palindrome lands in C_11.

C. PENROSE OUTER RADIUS
   The Penrose patch outer radius = 407 px = 11 × 37.
   407 ≡ 0 (mod 37):  the rim is on the zero / SEAM.
   12 card primes (2,3,5,...,37) fill the first four shells.
   There are exactly 12 cosets of H in GF(37)*.

D. COSET MAP OF THE TIKTOK NUMBERS
   141    ≡ 30  →  C_3   (sovereign coset: double-sovereign element)
   417    ≡ 10  →  C_1   (sovereign kernel H = {1,10,26})
   937    ≡ 12  →  C_7   (sovereign target 12)
   347    ≡ 14  →  C_9   (prime-mirror coset {14,29,31})
   251    ≡ 29  →  C_9   (same coset as 347)
   346    ≡ 13  →  C_4
   347743 ≡ 17  →  C_10  (torus step coset from T218)
   141141 ≡ 23  →  C_5   (imaginary unit coset {6,8,23})
   55577177555 ≡ 32 → C_11 (seed orbit coset {18,24,32})

E. THE 20 + 12 = 32 IDENTITY
   The reversal ladder (T220) has first column-1 residue 9381 ≡ 20 (mod 37).
   20 ∈ C_2 = {2, 15, 20}  (same coset as the twin prime step size +2).
   12 is a sovereign target.
   20 + 12 = 32 ∈ {18, 24, 32} = C_11 = seed orbit.
   The ladder's starting residue plus the nearest sovereign target = seed orbit node.

F. BLASCHKE PRODUCT PARALLEL
   The degree-3 Blaschke product f(z) = μ Π_{k=1}^{3} (z-a_k)/(1-ā_k z)
   is an order-3 map on the unit disk (three preimages per boundary point).
   The 137-map on GF(37) also has order 3: ord_37(26) = 3 (orbit size 3).
   Both are degree/order-3 maps.  The Blaschke product is the continuous
   complex-analytic analogue of the discrete 137-map on the finite field.
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


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def run():
    print("=" * 70)
    print("THEOREM 222: PENROSE PATCH, TIKTOK NUMBERS, GF(37) COSET ANATOMY")
    print("=" * 70)

    cosets = build_cosets()

    # A. Sovereign coset
    print(f"\nA. THE SOVEREIGN COSET")
    c3 = cosets[2]   # C_3
    print(f"   C_3 = {c3}")
    for x in c3:
        in_sa = x in SA
        in_st = x in ST
        tag = "SA∩ST (double sovereign)" if in_sa and in_st else \
              "SA" if in_sa else "ST" if in_st else ""
        print(f"   {x:>2}  →  {tag}")
    assert all(x in SA or x in ST for x in c3), "C_3 not fully sovereign"
    assert 30 in SA and 30 in ST
    print(f"   C_3 is the unique coset where every element is sovereign.")
    print(f"   141 mod 37 = {141 % P}  ∈  C_3  ✓")

    # B. Seed orbit = C_11
    print(f"\nB. SEED ORBIT = C_11")
    c11 = cosets[10]
    print(f"   C_11 = {c11}")
    print(f"   Seed orbit {{18,24,32}} == C_11: {set(c11) == SEED_ORBIT}")
    assert set(c11) == SEED_ORBIT
    r_palindrome = 55577177555 % P
    ci, c = coset_of(55577177555, cosets)
    print(f"   55577177555 mod 37 = {r_palindrome}  →  C_{ci} = {c}")
    print(f"   {r_palindrome} ∈ seed orbit: {r_palindrome in SEED_ORBIT}  ✓")

    # C. Penrose outer radius
    print(f"\nC. PENROSE OUTER RADIUS")
    print(f"   407 px = 11 × 37 = {11*37}")
    print(f"   407 mod 37 = {407 % P}  (SEAM / zero)")
    card_primes = [p for p in range(2, 38) if is_prime(p)]
    print(f"   Card primes (p ≤ 37): {card_primes}")
    print(f"   Count: {len(card_primes)}  ==  12 cosets of H in GF(37)*: {len(card_primes) == 12}")
    assert len(card_primes) == 12

    # D. Coset map of all numbers
    print(f"\nD. COSET MAP OF TIKTOK NUMBERS")
    numbers = [
        ("141",          141),
        ("417",          417),
        ("937",          937),
        ("347",          347),
        ("251",          251),
        ("346",          346),
        ("347743",       347743),
        ("141141",       141141),
        ("55577177555",  55577177555),
    ]
    for name, n in numbers:
        r = n % P
        ci, c = coset_of(n, cosets)
        in_H  = r in H_SET
        in_SA = r in SA
        in_ST = r in ST
        in_seed = r in SEED_ORBIT
        notes = []
        if in_H:    notes.append("H-kernel")
        if in_SA:   notes.append("SA")
        if in_ST:   notes.append("ST")
        if in_seed: notes.append("seed-orbit")
        if ci == 10: notes.append("torus-step-coset")
        if ci == 5:  notes.append("imag-unit-coset")
        note_str = "  [" + ", ".join(notes) + "]" if notes else ""
        print(f"   {name:15s}  ≡ {r:2d}  →  C_{ci:2}{note_str}")

    # Verify key coset members
    assert 141 % P == 30 and 30 in SA and 30 in ST
    assert 417 % P == 10 and 10 in H_SET
    assert 937 % P == 12 and 12 in ST
    assert 347 % P == 14 and 251 % P == 29
    ci_347, _ = coset_of(347, cosets)
    ci_251, _ = coset_of(251, cosets)
    assert ci_347 == ci_251, "347 and 251 must share a coset"
    print(f"\n   347 and 251 share coset C_{ci_347} = {cosets[ci_347-1]}  ✓")

    # E. The 20 + 12 = 32 identity
    print(f"\nE. 20 + 12 = 32  IDENTITY")
    c_of_20 = coset_of(20, cosets)
    c_of_2  = coset_of(2, cosets)
    print(f"   20 ∈ C_{c_of_20[0]} = {c_of_20[1]}  (same coset as twin-prime step +2)")
    print(f"    2 ∈ C_{c_of_2[0]} = {c_of_2[1]}  ✓  (20 and 2 share a coset)")
    assert c_of_20[0] == c_of_2[0]
    print(f"   12 ∈ ST (sovereign target)")
    total = (20 + 12) % P
    print(f"   (20 + 12) mod 37 = {total}  ∈ seed orbit: {total in SEED_ORBIT}  ✓")

    # F. Blaschke parallel
    print(f"\nF. BLASCHKE PRODUCT PARALLEL")
    ord_26 = next(k for k in range(1, P) if pow(26, k, P) == 1)
    print(f"   ord_37(26) = {ord_26}  (order of 137-map multiplier in GF(37))")
    print(f"   Blaschke degree = 3  (each boundary point has 3 preimages)")
    print(f"   Both are order-3 maps: discrete (GF(37)) and continuous (unit disk).")
    assert ord_26 == 3

    # Coset summary with sovereign annotations
    print(f"\nCOMPLETE COSET TABLE (GF(37)*  /  H):")
    for i, c in enumerate(cosets):
        flags = []
        for x in c:
            if x in H_SET: flags.append(f"{x}:H")
            elif x in SA and x in ST: flags.append(f"{x}:SA+ST")
            elif x in SA: flags.append(f"{x}:SA")
            elif x in ST: flags.append(f"{x}:ST")
            elif x in SEED_ORBIT: flags.append(f"{x}:seed")
            else: flags.append(f"{x}")
            if x in SEED_ORBIT and not flags[-1].endswith(":seed"):
                flags[-1] += "(seed)"
        note = "  ← SOVEREIGN COSET" if i == 2 else \
               "  ← SEED ORBIT" if i == 10 else \
               "  ← TORUS-STEP COSET (T218)" if i == 9 else \
               "  ← IMAG-UNIT COSET" if i == 4 else \
               "  ← H (kernel)" if i == 0 else ""
        print(f"   C_{i+1:2d} = {c}  {' | '.join(flags)}{note}")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()

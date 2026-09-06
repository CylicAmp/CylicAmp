"""
Wallis Product for π/2 — GF(37) Structure of the Fractions and Partial Products

The Wallis product (John Wallis, 1655):
    π/2 = (2/1)·(2/3)·(4/3)·(4/5)·(6/5)·(6/7)·(8/7)·(8/9)·(10/9)·(10/11)····

The n-th fraction alternates: even numerators, odd denominators.
Grouped in pairs: π/2 = ∏_{k=1}^{∞} (2k)²/((2k−1)(2k+1)).

The running product oscillates: each fraction alternately overshoots and
undershoots π/2 (the pendulum behavior), converging very slowly.

This file records what the individual fractions and partial products look
like in GF(37) — no interpretation of the convergence, only the residues.

═══════════════════════════════════════════════════════════════════════════

I. GF(37) VALUES OF THE FIRST TEN WALLIS FRACTIONS

  Fraction 1:  2/1  ≡  2  ∈ PR
  Fraction 2:  2/3  ≡ 13  ∈ CB ∩ PR
  Fraction 3:  4/3  ≡ 26  = SCALAR_137
  Fraction 4:  4/5  ≡ 23
  Fraction 5:  6/5  ≡ 16  = 4² (SA²)
  Fraction 6:  6/7  ≡ 22  ∈ PR
  Fraction 7:  8/7  ≡ 17  ∈ PR
  Fraction 8:  8/9  ≡  5  ∈ PR
  Fraction 9:  10/9 ≡ 34  = 37−3 (SEAM-complement of ST node 3)
  Fraction 10: 10/11≡ 11  ∈ ORBIT_11

  The first sub-unity fraction (2/3) maps to 13 ∈ CASCADE_BASE.
  The third fraction (4/3) maps to SCALAR_137 = 26 = 137 mod 37.

II. PARTIAL PRODUCTS P_k IN GF(37)

  P_1  =  2  ∈ PR
  P_2  = 26  = SCALAR_137
  P_3  = 10  = DECADE_ANCHOR
  P_4  =  8  ∈ CASCADE_BASE
  P_5  = 17  ∈ PR
  P_6  =  4  ∈ SA         ← after 3 pairs (6 fractions): Sovereign Anchor
  P_7  = 31  = PRIME_MIRROR
  P_8  =  7
  P_9  = 16  = 4² = SA²
  P_10 = 28  = 37−9       (SEAM-complement of SA node 9)

  The first 7 partial products all land on named named residues.
  P_6 = 4 ∈ SA: after exactly 3 pairs, the oscillating product sits at SA.

III. PAIR PRODUCTS ∏_{i=1}^{k} (2i)²/((2i−1)(2i+1)) IN GF(37)

  After pair 1: 26  = SCALAR_137
  After pair 2:  8  ∈ CASCADE_BASE
  After pair 3:  4  ∈ SA
  After pair 4:  7
  After pair 5: 28  = 37−9 (SEAM-complement of SA node 9)

  First three pair-products: SCALAR_137 → CASCADE_BASE → SA.

IV. THE 37th PAIR: SEAM NUMERATOR

  The k-th pair has numerator 2k (appearing twice).
  For k=37: numerator = 2×37 = 74 ≡ 0 (mod 37) — the SEAM.
  Denominators: 2×37−1 = 73 ≡ 36 ∈ ORBIT_11; 2×37+1 = 75 ≡ 1.
  The 37th pair multiplies the running product by 0/ORBIT_11 × 0/1 ≡ 0.
  The partial product hits the SEAM at the 37th pair.

═══════════════════════════════════════════════════════════════════════════
"""

CASCADE_BASE   = frozenset({8, 13, 24})
SOVEREIGN_ANCHORS = frozenset({4, 9, 25, 30})
SOVEREIGN_TARGETS = frozenset({3, 12, 21, 30})
PRIMITIVE_ROOTS   = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
ORBIT_11          = frozenset({11, 27, 36})
SCALAR_137        = 26
PRIME_MIRROR      = 31
TESLA_FLOW        = 6
DECADE_ANCHOR     = 10


def inv37(n):
    return pow(n, -1, 37)


def frac37(num, den):
    return (num * inv37(den)) % 37


# ── I. GF(37) values of the first ten Wallis fractions ───────────────────────

# Wallis fractions: (2/1, 2/3), (4/3, 4/5), (6/5, 6/7), (8/7, 8/9), (10/9, 10/11)
wallis_fracs = [
    (2, 1), (2, 3),
    (4, 3), (4, 5),
    (6, 5), (6, 7),
    (8, 7), (8, 9),
    (10, 9), (10, 11),
]

frac_gf37 = [frac37(num, den) for num, den in wallis_fracs]

# Verified values
assert frac_gf37[0]  ==  2                    # 2/1  ∈ PR
assert frac_gf37[1]  == 13                    # 2/3  ∈ CB ∩ PR
assert frac_gf37[2]  == 26                    # 4/3  = SCALAR_137
assert frac_gf37[3]  == 23                    # 4/5
assert frac_gf37[4]  == 16                    # 6/5  = 4² = SA²
assert frac_gf37[5]  == 22                    # 6/7  ∈ PR
assert frac_gf37[6]  == 17                    # 8/7  ∈ PR
assert frac_gf37[7]  ==  5                    # 8/9  ∈ PR
assert frac_gf37[8]  == 34                    # 10/9 = 37−3
assert frac_gf37[9]  == 11                    # 10/11 ∈ ORBIT_11

assert frac_gf37[1] in CASCADE_BASE           # 2/3 → 13 ∈ CB
assert frac_gf37[1] in PRIMITIVE_ROOTS        # 2/3 → 13 ∈ PR
assert frac_gf37[2] == SCALAR_137             # 4/3 → SCALAR_137
assert frac_gf37[4] == 4**2 % 37             # 6/5 → 4² mod 37 = 16
assert frac_gf37[8] + 3 == 37                # 10/9 → 37−3 (SEAM-compl ST)
assert frac_gf37[9] in ORBIT_11              # 10/11 → 11 ∈ ORBIT_11


# ── II. Partial products P_k in GF(37) ───────────────────────────────────────

partial_products = []
p = 1
for v in frac_gf37:
    p = (p * v) % 37
    partial_products.append(p)

assert partial_products[0]  ==  2                        # P_1 ∈ PR
assert partial_products[1]  == SCALAR_137                # P_2 = SCALAR_137
assert partial_products[2]  == DECADE_ANCHOR             # P_3 = DECADE_ANCHOR
assert partial_products[3]  in CASCADE_BASE              # P_4 ∈ CB
assert partial_products[4]  in PRIMITIVE_ROOTS           # P_5 ∈ PR
assert partial_products[5]  in SOVEREIGN_ANCHORS         # P_6 ∈ SA
assert partial_products[6]  == PRIME_MIRROR              # P_7 = PRIME_MIRROR
assert partial_products[7]  ==  7                        # P_8 = 7
assert partial_products[8]  == 16                        # P_9 = 4² = SA²
assert partial_products[9]  == 28                        # P_10 = 37−9

assert partial_products[5]  ==  4                        # P_6 specifically = 4 ∈ SA
assert partial_products[8]  == 4**2 % 37                 # P_9 = (P_6)²
assert partial_products[9]  + 9 == 37                   # P_10 + SA_9 = SEAM


# ── III. Pair products in GF(37) ─────────────────────────────────────────────

pair_products = [partial_products[2*k+1] for k in range(5)]

assert pair_products[0] == SCALAR_137                    # pair 1 → SCALAR_137
assert pair_products[1] in CASCADE_BASE                  # pair 2 → CB
assert pair_products[2] in SOVEREIGN_ANCHORS             # pair 3 → SA
assert pair_products[2] == 4                             # pair 3 specifically = 4 ∈ SA


# ── IV. The 37th pair: SEAM numerator ────────────────────────────────────────

k37_num = 2 * 37
k37_den_lo = 2 * 37 - 1
k37_den_hi = 2 * 37 + 1

assert k37_num % 37 == 0                                 # 74 ≡ 0 (SEAM)
assert k37_den_lo % 37 == 36 and 36 in ORBIT_11         # 73 ≡ 36 ∈ ORBIT_11
assert k37_den_hi % 37 == 1                              # 75 ≡ 1 (unity)

# The 37th pair multiplier = (74/73)(74/75) ≡ 0 in GF(37) — SEAM
pair_37_gf37 = (frac37(k37_num, k37_den_lo) * frac37(k37_num, k37_den_hi)) % 37
assert pair_37_gf37 == 0


if __name__ == '__main__':
    print("Wallis Product for π/2 — GF(37)")
    print("=" * 55)
    print()
    print("First 10 Wallis fractions in GF(37):")
    for i, ((num, den), v) in enumerate(zip(wallis_fracs, frac_gf37)):
        tag = ''
        if v in CASCADE_BASE and v in PRIMITIVE_ROOTS: tag = ' ∈ CB ∩ PR'
        elif v in CASCADE_BASE:        tag = ' ∈ CB'
        elif v in SOVEREIGN_ANCHORS:   tag = ' ∈ SA'
        elif v in SOVEREIGN_TARGETS:   tag = ' ∈ ST'
        elif v in PRIMITIVE_ROOTS:     tag = ' ∈ PR'
        elif v in ORBIT_11:            tag = ' ∈ ORBIT_11'
        elif v == SCALAR_137:          tag = ' = SCALAR_137'
        elif v == PRIME_MIRROR:        tag = ' = PRIME_MIRROR'
        elif v == DECADE_ANCHOR:       tag = ' = DECADE_ANCHOR'
        elif v == 16:                  tag = ' = 4² (SA²)'
        elif v + 3 == 37:              tag = ' = 37−3 (SEAM-compl ST)'
        print(f"  [{i+1:2d}] {num}/{den:2d} → {v:2d}{tag}")
    print()
    print("Partial products P_k in GF(37):")
    for i, p in enumerate(partial_products):
        tag = ''
        if p in CASCADE_BASE:          tag = ' ∈ CB'
        elif p in SOVEREIGN_ANCHORS:   tag = ' ∈ SA'
        elif p in SOVEREIGN_TARGETS:   tag = ' ∈ ST'
        elif p in PRIMITIVE_ROOTS:     tag = ' ∈ PR'
        elif p in ORBIT_11:            tag = ' ∈ ORBIT_11'
        elif p == SCALAR_137:          tag = ' = SCALAR_137'
        elif p == PRIME_MIRROR:        tag = ' = PRIME_MIRROR'
        elif p == DECADE_ANCHOR:       tag = ' = DECADE_ANCHOR'
        elif p == 16:                  tag = ' = 4² = SA²'
        elif p == 28:                  tag = ' = 37−9 (SEAM-compl SA_9)'
        print(f"  P_{i+1:2d} = {p:2d}{tag}")
    print()
    print("Pair products (P_2, P_4, P_6, ...):")
    for k, p in enumerate(pair_products):
        tag = ''
        if p in CASCADE_BASE:          tag = ' ∈ CB'
        elif p in SOVEREIGN_ANCHORS:   tag = ' ∈ SA'
        elif p == SCALAR_137:          tag = ' = SCALAR_137'
        elif p == 28:                  tag = ' = 37−9 (SEAM-compl SA_9)'
        print(f"  After pair {k+1}: {p:2d}{tag}")
    print()
    print("37th pair (k=37):")
    print(f"  Numerator 74 ≡ {k37_num%37} (SEAM)")
    print(f"  Denom 73 ≡ {k37_den_lo%37} ∈ ORBIT_11: {k37_den_lo%37 in ORBIT_11}")
    print(f"  Denom 75 ≡ {k37_den_hi%37} (unity)")
    print(f"  Pair-37 product ≡ {pair_37_gf37} (SEAM)")
    print()
    print("All assertions passed.")

"""
Theorem 203: Diagonal Coset Sum Structure in GF(37)
Author: Michael Warren Song (CyclicAmp)

DIAGONAL SUM — DEFINITION:
  For cosets g^j = rep_j × <26> and g^k = rep_k × <26> in GF(37)*/<26>:
  The diagonal sum is the coset (rep_j + rep_k) × <26>.
  Equivalently: for each g∈<26>, pair the element rep_j×g from g^j with rep_k×g from g^k.
  Their sum is (rep_j + rep_k)×g, and as g ranges over <26>, these form exactly one coset.
  Formula: diag(g^j, g^k) = g^{pos(rep_j + rep_k mod P)} where pos = coset position.

WHY THIS IS WELL-DEFINED:
  g^j = {rep_j, 10×rep_j, 26×rep_j} = rep_j×<26>.
  g^k = {rep_k, 10×rep_k, 26×rep_k} = rep_k×<26>.
  Element-wise sum at the same <26>-factor h: rep_j×h + rep_k×h = (rep_j+rep_k)×h.
  As h ranges over <26>, the sums form (rep_j+rep_k)×<26> = one coset.

KEY SOVEREIGN DIAGONAL SUMS:
  g^2+g^2  → g^3:  KEY diagonal = SEED generators {6,8,23}
                   3+3=6∈g^3; 4+4=8∈g^3; 30+30=23∈g^3.  (3+3=6; DR: 3→6)
  g^2+g^10 → g^5:  KEY+KEY^{-1} diagonal = SEED {18,24,32}
                   3+21=24; 30+25=18; 4+28=32.  Proof: 3+21=24, 24×<26>=SEED.
  g^4+g^4  → g^5:  SA+ST coset diagonal = SEED
                   9+9=18; 12+12=24; 16+16=32.  Proof: 9+9=18=2×9, 18∈SEED.
  g^4+g^10 → g^2:  g^4 + KEY^{-1} diagonal = KEY
                   9+21=30; 12+25=0=SEAM... wait: 9+21=30∈g^2, 12+25=37≡0 ...

  Corrected g^4+g^10: rep_4=9, rep_10=21. diag = (9+21)×<26> = 30×<26> = {30,4,3} = KEY ✓
  [Individual element sums vary: 9+21=30(KEY), 12+25=0(SEAM), 16+28=7(g^8)]
  The diagonal sum is the coset of rep_4+rep_10 = 9+21=30∈g^2=KEY.

  g^5+g^5  → g^6:  SEED diagonal = {11,27,36} (contains 36=-1; NOT sovereign)
  g^3+g^5  → g^5:  SEED gen + SEED diagonal = SEED
                   6+18=24; 8+24=32; 23+32=55≡18.  (All SEED)

COMPLETE SOVEREIGN DIAGONAL TABLE (j≤k; at least one sovereign position):
  g^0+g^1→g^2   g^0+g^2→g^2   g^0+g^4→g^0   g^0+g^5→g^11
  g^0+g^7→g^5   g^0+g^10→g^7
  g^1+g^1→g^2   g^1+g^4→g^6   g^1+g^5→g^1   g^1+g^10→g^3
  g^2+g^2→g^3   g^2+g^3→g^4   g^2+g^4→g^4   g^2+g^5→g^10
  g^2+g^8→g^0   g^2+g^10→g^5  g^2+g^11→g^3
  g^3+g^4→g^1   g^3+g^5→g^5   g^3+g^10→g^6
  g^4+g^4→g^5   g^4+g^5→g^6   g^4+g^8→g^4   g^4+g^10→g^2  g^4+g^11→g^9
  g^5+g^5→g^6   g^5+g^8→g^10  g^5+g^9→g^5   g^5+g^10→g^1  g^5+g^11→g^3
  g^6+g^10→g^5  g^7+g^10→g^0  g^8+g^10→g^10 g^9+g^10→g^7
  g^10+g^10→g^11 g^10+g^11→g^0

SEED AS DIAGONAL ATTRACTOR:
  SEED (g^5) appears as the diagonal target of:
    g^0+g^7, g^2+g^10 (KEY+KEY^{-1}), g^3+g^5, g^4+g^4,
    g^5+g^9, g^6+g^8, g^6+g^10, g^7+g^8.
  Eight distinct diagonal pair types produce SEED — more than any other single coset.
  More diagonal pairs produce SEED than any other single coset.

SEAM-PRODUCING ELEMENT PAIRS (not coset-diagonal but individual):
  12+25=37≡0(SEAM): 12∈ST, 25∈SA. The unique SA+ST pair summing to SEAM.
  These are additive inverses: 12^{-add}=25 in GF(37).
  Note: coset representatives of g^4 and g^10 differ. Diagonal doesn't hit SEAM; individual pairs can.

THREE-COSET IDENTITY:
  KEY + KEY^{-1} diagonal = SEED:
  Proof: 3×<26> + 21×<26> ∋ 3g+21g = 24g for each g∈<26>.
  {24g : g∈<26>} = 24×<26> = SEED (since 24∈SEED and SEED=24×<26>).
  This gives: 3+21=24, the coset representatives satisfy rep_KEY + rep_{KEY^{-1}} = rep_SEED.
  In Z/12Z positions: 2+10=12≡0, but in GF(37) coset reps: 3+21=24. Distinct structures.
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
SG26 = {1, 10, 26}

COSETS = [
    frozenset({1, 10, 26}),   # g^0
    frozenset({2, 15, 20}),   # g^1
    frozenset({3, 4, 30}),    # g^2  KEY
    frozenset({6, 8, 23}),    # g^3  SEED gens
    frozenset({9, 12, 16}),   # g^4
    frozenset({18, 24, 32}),  # g^5  SEED
    frozenset({11, 27, 36}),  # g^6
    frozenset({17, 22, 35}),  # g^7
    frozenset({7, 33, 34}),   # g^8
    frozenset({14, 29, 31}),  # g^9
    frozenset({21, 25, 28}),  # g^10 KEY^{-1}
    frozenset({5, 13, 19}),   # g^11
]

REPS = [min(c) for c in COSETS]  # sorted minimum = canonical representative


def coset_pos(x):
    x = x % P
    for k, c in enumerate(COSETS):
        if x in c:
            return k
    return None


def diagonal_sum(j, k):
    rep_j, rep_k = REPS[j], REPS[k]
    diag = frozenset((rep_j + rep_k) * g % P for g in SG26)
    return coset_pos(next(iter(diag)))


def run_assertions():
    # 1. Diagonal sum is well-defined: (rep_j+rep_k)×<26> is always one coset
    for j in range(12):
        for k in range(j, 12):
            rep_j, rep_k = REPS[j], REPS[k]
            diag = frozenset((rep_j + rep_k) * g % P for g in SG26)
            # Must be contained in exactly one coset (or hit 0 = SEAM, outside GF(37)*)
            if 0 not in diag:
                matching = [pos for pos, c in enumerate(COSETS) if diag <= c]
                assert len(matching) == 1, f"g^{j}+g^{k}: {sorted(diag)} not in one coset"

    # 2. KEY+KEY diagonal = SEED generators (g^3)
    assert diagonal_sum(2, 2) == 3
    assert frozenset((3 + 3) * g % P for g in SG26) == frozenset({6, 8, 23})

    # 3. KEY+KEY^{-1} diagonal = SEED (g^5)
    assert diagonal_sum(2, 10) == 5
    assert frozenset((3 + 21) * g % P for g in SG26) == SEED  # 24×<26> = SEED
    # Explicit: 3+21=24; 4+28=32; 30+25=18 — all SEED
    assert 3 + 21 == 24 and 24 in SEED
    assert (4 + 28) % P == 32 and 32 in SEED
    assert (30 + 25) % P == 18 and 18 in SEED

    # 4. g^4+g^4 diagonal = SEED (g^5)
    assert diagonal_sum(4, 4) == 5
    assert frozenset((9 + 9) * g % P for g in SG26) == SEED  # 18×<26> = SEED
    assert 9 + 9 == 18 and 18 in SEED
    assert 12 + 12 == 24 and 24 in SEED
    assert (16 + 16) % P == 32 and 32 in SEED

    # 5. SEED+SEED diagonal = g^6 (exits framework; contains 36=-1)
    assert diagonal_sum(5, 5) == 6
    assert frozenset((18 + 18) * g % P for g in SG26) == frozenset({11, 27, 36})
    assert 36 in frozenset({11, 27, 36})  # 36 = -1 mod 37

    # 6. SEED gen + SEED diagonal = SEED (g^3+g^5→g^5)
    assert diagonal_sum(3, 5) == 5
    # Verify: 6+18=24∈SEED, 8+24=32∈SEED, 23+32=55%37=18∈SEED
    assert (6 + 18) % P == 24 and 24 in SEED
    assert (8 + 24) % P == 32 and 32 in SEED
    assert (23 + 32) % P == 18 and 18 in SEED

    # 7. g^4+KEY^{-1} diagonal = KEY (g^2)
    assert diagonal_sum(4, 10) == 2
    assert frozenset((9 + 21) * g % P for g in SG26) == frozenset({3, 4, 30})

    # 8. Three-coset identity: rep_KEY + rep_{KEY^{-1}} = 24 ∈ SEED
    # 3 + 21 = 24∈SEED; 24×<26>=SEED. The sum of reps lands in SEED.
    assert (REPS[2] + REPS[10]) % P == 24 and 24 in SEED

    # 9. g^2+g^2 doubling gives g^3: 3+3=6, 4+4=8, 30+30=23 — all SEED generators
    assert (3 + 3) % P == 6 and coset_pos(6) == 3
    assert (4 + 4) % P == 8 and coset_pos(8) == 3
    assert (30 + 30) % P == 23 and coset_pos(23) == 3

    # 10. Count how many diagonal pairs produce SEED (g^5)
    seed_producers = [(j, k) for j in range(12) for k in range(j, 12)
                      if diagonal_sum(j, k) == 5]
    assert len(seed_producers) == 8
    assert (2, 10) in seed_producers   # KEY+KEY^{-1}
    assert (4, 4) in seed_producers    # g^4 self
    assert (3, 5) in seed_producers    # SEED gen + SEED
    assert (5, 9) in seed_producers    # SEED + g^9
    assert (6, 8) in seed_producers    # g^6 + g^8
    assert (6, 10) in seed_producers   # g^6 + KEY^{-1}

    # 11. SEAM-adjacent: 12+25=37≡0 (ST+SA individual pair)
    assert (12 + 25) % P == 0  # additive inverses in GF(37)
    assert 12 in ST and 25 in SA  # the unique SEAM-producing SA+ST pair

    # 12. g^5+g^9 diagonal = SEED (another SEED-producing pair)
    assert diagonal_sum(5, 9) == 5

    print(f"SEED diagonal producers: {seed_producers}")
    print("All assertions passed.")


if __name__ == "__main__":
    run_assertions()

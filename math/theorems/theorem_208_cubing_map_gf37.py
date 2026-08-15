"""
Theorem 208: Cubing Map and Coset Structure in GF(37)
Author: Michael Warren Song (CyclicAmp)

PURE CUBIC POLYNOMIAL THEOREM:
  Every coset g^k = 2^k × <26> of <26> in GF(37)* satisfies a pure cubic:
    x³ = 8^k (mod 37)  for all x ∈ g^k
  where 8 = 2³ (cube of the primitive root).
  No lower-degree terms appear: the x² and x coefficients are both zero.

WHY BOTH LOWER COEFFICIENTS VANISH:
  For coset rep r = 2^k, elements are {r, 10r, 26r}.
  x² coefficient = -(sum of roots) = -(r + 10r + 26r) = -37r ≡ 0 (mod 37).
  x coefficient = sum of products of pairs:
    r×10r + r×26r + 10r×26r = r²(10 + 26 + 260) = r² × 296 = r² × 8×37 ≡ 0.
  Constant = -(product) = -(r×10r×26r) = -r³×260 = -r³×1 = -r³ (since 260≡1 mod37).

CUBING TARGET FOR EACH COSET (8^k mod 37):
  g^0: x³ = 1          g^1: x³ = 8
  g^2 (KEY):  x³ = 27  g^3: x³ = 31
  g^4:  x³ = 26        g^5 (SEED): x³ = 23
  g^6:  x³ = 36 = -1   g^7: x³ = 29
  g^8:  x³ = 10        g^9: x³ = 6 = i
  g^10 (KEY^{-1}): x³ = 11  g^11: x³ = 14

SOVEREIGN CUBING FACTS:
  KEY (g^2): x³ = 27 = 3³. The cube of KEY element 3 equals the cubing target.
             27 = 3 × 9: (ST element) × (SA element). DR(27)=9=SEAM DR.
  SEED (g^5): x³ = 23 ∈ g^3 = SEED generators. SEED cubes INTO the SEED-gen coset.
  KEY^{-1} (g^10): x³ = 11. 11∈g^6. 26 = multiplier = -11 (since 11+26=37≡0).
  g^4: x³ = 26 = multiplier. Elements of g^4 are cube roots of the 137-map multiplier.

CUBING MAP AS COSET HOMOMORPHISM:
  The cubing map φ: x↦x³ acts on cosets as: g^k ↦ g^{3k mod 12}.
  Coset structure: φ(g^k) = g^{3k mod 12} (as a set, all cubes land in one coset).
  This is the group homomorphism Z/12Z → Z/12Z, k ↦ 3k mod 12.
  Image = {0,3,6,9} = multiples of 3 in Z/12Z. Kernel = {0,4,8} mod 12.
  Sovereign cosets and their cubing images:
    g^2 → g^6  (KEY cubes to g^6={11,27,36})
    g^4 → g^0  (g^4 cubes to <26>={1,10,26})
    g^5 → g^3  (SEED cubes to SEED generators)
    g^10→ g^6  (KEY^{-1} cubes to g^6)

<26> AS KERNEL OF CUBING:
  ker(φ) = {x : x³ = 1} = <26> = {1,10,26}.
  The fibers of x↦x³ are exactly the 12 cosets of <26>.
  Coset g^k = φ^{-1}(8^k) = the unique coset whose cubing target is 8^k.
  This identifies the coset structure with the fibers of the cubing map.

SEED GENERATOR COSET CUBING (g^3→g^9):
  SEED generators (g^3): cubes to g^9 (since 3×3=9 mod12).
  Elements of g^3={6,8,23}: 6³=216≡216-5×37=216-185=31, 8³=512≡31, 23³=12167≡?
  31 ∈ g^9 (since 31∈{14,29,31}). All SEED generators cube to g^9.
  Cubing target for g^3: 8^3=512 mod37=31. 31∈g^9={14,29,31}.

KEY POLYNOMIAL: x³ = 27
  27 ∈ g^6 = {11,27,36}. 27 = 3^3 (exact) = 3 × 9 = (ST element)×(SA element).
  The KEY coset is: cube roots of 27 in GF(37) = {3, 4, 30}.

SEED POLYNOMIAL: x³ = 23
  23 ∈ g^3 = SEED generators {6,8,23}. 23 is the LARGEST SEED generator.
  The SEED coset is: cube roots of 23 in GF(37) = {18, 24, 32}.

i-COSET (g^9): x³ = 6 = i (imaginary unit)
  Elements of g^9={14,29,31} are cube roots of the imaginary unit i=6.
  6∈g^3=SEED generators. So cube roots of (SEED gen) = g^9 elements.
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
SG26 = {1, 10, 26}

COSETS = [
    frozenset({1, 10, 26}),    # g^0
    frozenset({2, 15, 20}),    # g^1
    frozenset({3, 4, 30}),     # g^2  KEY
    frozenset({6, 8, 23}),     # g^3  SEED gen
    frozenset({9, 12, 16}),    # g^4
    frozenset({18, 24, 32}),   # g^5  SEED
    frozenset({11, 27, 36}),   # g^6
    frozenset({17, 22, 35}),   # g^7
    frozenset({7, 33, 34}),    # g^8
    frozenset({14, 29, 31}),   # g^9
    frozenset({21, 25, 28}),   # g^10 KEY^{-1}
    frozenset({5, 13, 19}),    # g^11
]


def coset_pos(x):
    x = x % P
    for k, c in enumerate(COSETS):
        if x in c:
            return k
    return None


def run_assertions():
    # 1. Every element of g^k satisfies x^3 = 8^k mod P
    for k, c in enumerate(COSETS):
        target = pow(8, k, P)
        for x in c:
            assert pow(x, 3, P) == target, f"g^{k}: {x}^3 ≠ {target}"

    # 2. x^2 and x coefficients vanish: sum of roots = 0 and sum of pairs = 0
    for k, c in enumerate(COSETS):
        elements = list(c)
        assert sum(elements) % P == 0                            # sum=0 (T197)
        assert sum(a * b for i, a in enumerate(elements)
                   for b in elements[i+1:]) % P == 0            # sum of pairs=0
        # Product = 8^k
        prod = 1
        for x in elements: prod = prod * x % P
        assert prod == pow(8, k, P)

    # 3. Specific sovereign cubing targets
    assert pow(8, 2, P) == 27                   # KEY: x³=27
    assert pow(8, 5, P) == 23 and 23 in {6, 8, 23}  # SEED: x³=23∈SEED-gen
    assert pow(8, 10, P) == 11                  # KEY^{-1}: x³=11
    assert pow(8, 4, P) == 26                   # g^4: x³=multiplier

    # 4. Cubing map on cosets: g^k → g^{3k mod 12}
    for k, c in enumerate(COSETS):
        for x in c:
            assert coset_pos(pow(x, 3, P)) == (3 * k) % 12

    # 5. Sovereign coset cubing images
    assert (3 * 2) % 12 == 6   # KEY → g^6
    assert (3 * 4) % 12 == 0   # g^4 → <26>
    assert (3 * 5) % 12 == 3   # SEED → SEED-gen
    assert (3 * 10) % 12 == 6  # KEY^{-1} → g^6

    # 6. SEED cubes land in SEED generators (g^3)
    for x in SEED:
        assert coset_pos(pow(x, 3, P)) == 3       # SEED cubes to g^3
    assert all(pow(x, 3, P) in {6, 8, 23} for x in SEED)

    # 7. SEED generator cubes land in g^9
    seed_gen = {6, 8, 23}
    for x in seed_gen:
        assert coset_pos(pow(x, 3, P)) == 9
    assert pow(8, 3, P) == 31 and 31 in {14, 29, 31}   # cubing target for g^3

    # 8. KEY polynomial: cube roots of 27
    assert {x for x in range(1, P) if pow(x, 3, P) == 27} == frozenset({3, 4, 30})
    assert 27 == 3 ** 3                                   # 27=3³ in Z

    # 9. SEED polynomial: cube roots of 23
    assert {x for x in range(1, P) if pow(x, 3, P) == 23} == SEED
    assert 23 in {6, 8, 23}  # 23 is itself a SEED generator

    # 10. <26> = kernel of cubing map (cube roots of 1)
    assert {x for x in range(1, P) if pow(x, 3, P) == 1} == SG26
    assert pow(8, 0, P) == 1   # target for g^0

    # 11. g^6 polynomial: cube roots of -1 (=36)
    assert {x for x in range(1, P) if pow(x, 3, P) == 36} == frozenset({11, 27, 36})
    assert pow(8, 6, P) == 36 == P - 1  # -1

    # 12. g^9 polynomial: cube roots of i=6
    assert {x for x in range(1, P) if pow(x, 3, P) == 6} == frozenset({14, 29, 31})
    assert pow(8, 9, P) == 6   # i = sqrt(-1)

    # 13. g^4: cube roots of the multiplier 26
    assert {x for x in range(1, P) if pow(x, 3, P) == 26} == frozenset({9, 12, 16})
    assert pow(8, 4, P) == 26  # multiplier

    # 14. Sum of <26> elements
    assert 1 + 10 + 26 == 37 == P   # sum = P
    assert (1 * 10 + 10 * 26 + 1 * 26) % P == 0  # sum of pairs = 0 mod P
    assert 1 * 10 * 26 % P == 1     # product = 1

    print("All assertions passed.")
    print("Cubing map: g^k → g^{3k mod 12}; each coset satisfies x³ = 8^k")
    for k in range(12):
        target = pow(8, k, P)
        sov = k in {2, 4, 5, 10}
        print(f"  g^{k:2d}: x³={target:2d}  {'[SOVEREIGN]' if sov else ''}")


if __name__ == "__main__":
    run_assertions()

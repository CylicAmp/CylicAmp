"""
Theorem 215: 246 = 2 × 123 — Seed as Primitive Root × Lucas Number in GF(37)
Author: Michael Warren Song (CyclicAmp)

THE IDENTITY: 246 = 2 × 123

  2   = the primitive root of GF(37)* (ord_37(2) = 36; generator of all cosets).
  123 = L(10): the exact 10th Lucas number.
  246 = the pipeline seed; 246 mod 37 = 24 ∈ SEED = {18,24,32}.

  The seed is the primitive root times the 10th Lucas number.

COSET ARITHMETIC (T201 MULTIPLICATION DISPLACEMENT LAW):
  In Z/12Z ≅ GF(37)*/<26>, coset positions add under multiplication.
    pos(2)  = 1  (g^1 = {2,15,20}: primitive root coset)
    pos(12) = 4  (g^4 = {9,12,16}: 12 ∈ g^4 AND 12 ∈ ST)
    pos(2) + pos(12) = 1 + 4 = 5 = pos(24)  ✓  (g^5 = SEED)
  Doubling L(10) mod37: 2 × 12 = 24. One step forward in the coset lattice.

SECOND DECOMPOSITION: 246 = 6 × 41
  6  ∈ g^3 = {6,8,23} = SEED-gen (imaginary unit i: 6²≡-1 mod37).
  41 mod 37 = 4 ∈ g^2 = {3,4,30} = KEY coset.
    pos(6) + pos(41) = 3 + 2 = 5 = pos(24) ∈ g^5 = SEED  ✓
  (41, 43) is a twin prime pair; 41 is the lower twin (T107: π₂(246)=17).
  SEED-gen × KEY = SEED in coset arithmetic: g^3 × g^2 = g^5.

THIRD DECOMPOSITION: 246 = 2 × 3 × 41
  pos(2) + pos(3) + pos(41) = 1 + 2 + 2 = 5 = SEED  ✓
  2 ∈ g^1 (primitive root), 3 ∈ g^2 (KEY, ST), 41≡4 ∈ g^2 (KEY, SA).
  All three factorizations of 246 give coset-position sums of 5 = SEED.

LUCAS STRUCTURE OF 123:
  123 = 3 × 41.
  3 ∈ g^2 = KEY = {3,4,30}; 3 ∈ ST; 3 = L(2) (2nd Lucas number, exact).
  41 mod 37 = 4 ∈ g^2 = KEY; 4 ∈ SA.
  KEY × KEY = g^4: pos(3)+pos(4) = 2+2 = 4 → 3×4=12 ∈ g^4 ✓.
  (T205: ST×SA = ST or SA; here 3×4=12∈ST ✓)
  123 mod 37 = 12 ∈ g^4 ∩ ST: the Pell fundamental element,
    the CF period of √37, the Fibonacci pre-period element.

DIGIT ANALYSIS OF 123:
  Digits: 1, 2, 3.
    1 ∈ <26> = {1,10,26}: the identity, kernel of cubing, first element of the 137-map subgroup.
    2 = primitive root mod 37.
    3 ∈ ST: L(2), the ST generator.
  Digit sum: 1+2+3 = 6 ∈ SEED-gen: the imaginary unit i.
  DR(123) = DR(6) = 6.
  The three digits {1,2,3} = {<26> identity, primitive root, ST generator}
  — the three most fundamental single-element roles in the framework.

DIGIT ANALYSIS OF 246:
  Digits: 2, 4, 6.
    2 = primitive root.
    4 ∈ SA.
    6 ∈ SEED-gen (imaginary unit).
  Digit sum: 2+4+6 = 12 ∈ ST ∩ g^4: Pell fundamental, CF period, ST element.
  DR(246) = DR(12) = 3 = the ST DR signature (T210: all ST elements have DR=3).

DR CHAIN — DOUBLING LAW (T210):
  DR(123) = 6.
  DR(246) = DR(2×123) = 3.
  DR(2×6) = DR(12) = 3: doubling the DR-6 value gives DR-3. (T210 table: 6+6=3)
  So 246 = 2 × 123 doubles both the number AND its DR-character shifts
  from the i-DR (6) to the ST-DR (3).

THE COMPLETE IDENTITY CHAIN:
  246 = 2 × 123 = 2 × L(10) = 6 × 41 = 2 × 3 × 41
  ↓ mod37
  24 = 2 × 12 = 6 × 4 = 2 × 3 × 4   (all ∈ g^5 = SEED)
  ↓ coset pos
  5  = 1+4 = 3+2 = 1+2+2            (all sum to 5)
  ↓ DR
  3  = DR(24) = DR of all ST elements
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
SEED_GEN = {6, 8, 23}
SG26 = {1, 10, 26}

COSETS = [
    frozenset({1,10,26}), frozenset({2,15,20}),  frozenset({3,4,30}),
    frozenset({6,8,23}),  frozenset({9,12,16}),   frozenset({18,24,32}),
    frozenset({11,27,36}),frozenset({17,22,35}),  frozenset({7,33,34}),
    frozenset({14,29,31}),frozenset({21,25,28}),  frozenset({5,13,19}),
]


def coset_pos(x):
    x = x % P
    for k, c in enumerate(COSETS):
        if x in c: return k


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def lucas(n):
    a, b = 2, 1
    for _ in range(n): a, b = b, a + b
    return a


def run_assertions():
    # 1. Core identity
    assert 246 == 2 * 123
    assert lucas(10) == 123

    # 2. Mod37 positions
    assert 246 % P == 24 and 24 in SEED
    assert 123 % P == 12 and 12 in ST

    # 3. Coset displacement: pos(2)+pos(12)=5=pos(24)
    assert coset_pos(2) == 1
    assert coset_pos(12) == 4
    assert coset_pos(24) == 5
    assert coset_pos(2) + coset_pos(12) == coset_pos(24)

    # 4. Second decomposition: 6 × 41
    assert 6 * 41 == 246
    assert 6 in SEED_GEN
    assert 41 % P == 4 and 4 in SA
    assert coset_pos(6) + coset_pos(41 % P) == coset_pos(24)  # 3+2=5

    # 5. Third decomposition: 2 × 3 × 41
    assert 2 * 3 * 41 == 246
    pos_sum = coset_pos(2) + coset_pos(3) + coset_pos(41 % P)
    assert pos_sum == 5 == coset_pos(24)  # 1+2+2=5

    # 6. KEY × KEY = g^4: 3 and 4 both in g^2, product 12 in g^4
    assert coset_pos(3) == 2 and coset_pos(4) == 2    # both KEY
    assert coset_pos(12) == 4                          # KEY×KEY→g^4
    assert 3 * 4 % P == 12 and 12 in ST               # T205: ST×SA→ST

    # 7. 123 = 3 × 41; both in KEY coset (g^2)
    assert 3 * 41 == 123
    assert coset_pos(3) == coset_pos(41 % P) == 2     # both in KEY

    # 8. Digit analysis of 123
    assert 1 + 2 + 3 == 6 and 6 in SEED_GEN
    assert dr(123) == 6
    assert 1 in SG26
    assert pow(2, 36, P) == 1 and all(pow(2, k, P) != 1 for k in range(1, 36))  # primitive root
    assert 3 in ST

    # 9. Digit analysis of 246
    assert 2 + 4 + 6 == 12 and 12 in ST
    assert dr(246) == 3
    assert all(dr(x) == 3 for x in ST)  # universal ST signature

    # 10. DR doubling law (T210): DR(2×DR-6) = 3
    assert dr(2 * 6) == dr(12) == 3

    # 11. Primitive root: 2 generates GF(37)*
    assert pow(2, 36, P) == 1
    assert all(pow(2, k, P) != 1 for k in range(1, 36))
    assert coset_pos(2) == 1   # g^1

    # 12. All three coset decompositions give pos=5
    assert coset_pos(2) + coset_pos(12) == 5            # 1+4
    assert coset_pos(6) + coset_pos(4) == 5             # 3+2
    assert coset_pos(2) + coset_pos(3) + coset_pos(4) == 5  # 1+2+2

    print("All assertions passed.")
    print("246 = 2 × L(10) = 6 × 41 = 2 × 3 × 41")
    print("All factorizations → coset pos sums = 5 = SEED (g^5)")
    print(f"  2×123: pos {coset_pos(2)}+{coset_pos(12)}=5 → {2*123%P} ∈ SEED")
    print(f"  6×41:  pos {coset_pos(6)}+{coset_pos(41%P)}=5 → {6*41%P} ∈ SEED")
    print(f"  2×3×41:pos {coset_pos(2)}+{coset_pos(3)}+{coset_pos(41%P)}=5 → {2*3*41%P} ∈ SEED")
    print(f"Digit sum(123)=6∈SEED-gen, DR=6; digit sum(246)=12∈ST, DR=3")
    print(f"246 doubles 123 in value and shifts DR from 6 to 3 (T210 doubling rule)")


if __name__ == "__main__":
    run_assertions()

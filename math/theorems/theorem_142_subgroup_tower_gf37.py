"""
Theorem 142: The Subgroup Tower μ₃ < H₉ < QR < F₃₇×

TOWER STRUCTURE
================

(ℤ/37ℤ)× has order 36 = 2² × 3².  Four nested subgroups:

    μ₃  <  H₉  <  QR  <  F₃₇×

    |μ₃| = 3,   [H₉ : μ₃] = 3
    |H₉| = 9,   [QR : H₉] = 2
    |QR| = 18,  [F₃₇× : QR] = 2

μ₃ = {1, 10, 26}  — cube roots of unity (the 137-map identity orbit, IC)
H₉ = ⟨16⟩        — unique Sylow 3-subgroup, order 9
QR  = quadratic residues mod 37, order 18
F₃₇× = (ℤ/37ℤ)×, order 36

μ₃ ⊂ H₉: the cube roots of unity are contained in the Sylow 3-subgroup.
This is the critical containment that determines the two-level refinement below.

TWO INDEPENDENT QUOTIENT STRUCTURES
======================================

The 12 named orbits (cosets of μ₃) and the 4 H₉-cosets are two different
partitions of F₃₇×.  They are not the same partition.

    H₉-cosets: 4 cosets of size 9   — index 4
    μ₃-cosets: 12 cosets of size 3  — index 12

Because μ₃ ⊂ H₉, every H₉-coset decomposes into exactly 3 μ₃-cosets:

    1·H₉  = IC  ∪  D7  ∪  SA_ORB
    2·H₉  = DARK_A  ∪  NQR_14  ∪  SEED_ORB
    4·H₉  = SOVEREIGN_SPIRAL  ∪  ORBIT_11  ∪  OUTLIER_ORB
    8·H₉  = NQR_5  ∪  TESLA_ORB  ∪  NQR_17

The 12-orbit structure is the finer partition; the 4-coset H₉-structure is
the coarser one.  The 137-map uses the finer partition.

QR/NQR DETERMINED BY H₉-COSET
=================================

A μ₃-coset (named orbit) is QR if and only if it lies in a QR H₉-coset.

    H₉-coset    QR/NQR    μ₃-cosets (named orbits)
    1·H₉        QR        IC, D7, SA_ORB
    4·H₉        QR        SOVEREIGN_SPIRAL, ORBIT_11, OUTLIER_ORB
    2·H₉        NQR       DARK_A, NQR_14, SEED_ORB
    8·H₉        NQR       NQR_5, TESLA_ORB, NQR_17

Every element of a QR H₉-coset is a quadratic residue; every element of an
NQR H₉-coset is a non-residue.  The 12/12 orbit QR/NQR match is exact.

Consequence: the QR/NQR split of orbits is not an independent classification.
It is read off directly from the index-2 quotient QR/H₉.

H₉-COSET GROUP ≅ ℤ/4ℤ
========================

The four H₉-cosets form a cyclic group of order 4 under multiplication:

  Position 0: 1·H₉  (QR)
  Position 1: 2·H₉  (NQR)
  Position 2: 4·H₉  (QR)
  Position 3: 8·H₉  (NQR)

Full multiplication table: i+j (mod 4).

NQR×NQR products (positions 1 and 3):
  2·H₉ × 2·H₉ = 4·H₉  (position 2, QR)
  8·H₉ × 8·H₉ = 4·H₉  (position 6≡2, QR)
  2·H₉ × 8·H₉ = 1·H₉  (position 4≡0, QR)

All NQR×NQR products land in QR cosets, which is why NQR×NQR→QR holds.

COSET-OF-μ₃ REPRESENTATION OF EACH ORBIT
==========================================

Every named orbit is a·μ₃ for a representative a:

    Orbit            Representative a    a·μ₃
    IC               1                  {1, 10, 26}
    D7               7                  {7, 33, 34}
    SA_ORB           9                  {9, 12, 16}
    SOVEREIGN_SPIRAL 3                  {3, 4, 30}
    ORBIT_11         11                 {11, 27, 36}
    OUTLIER_ORB      21                 {21, 25, 28}
    DARK_A           2                  {2, 15, 20}
    NQR_14           14                 {14, 29, 31}
    SEED_ORB         18                 {18, 24, 32}
    NQR_5            5                  {5, 13, 19}
    TESLA_ORB        6                  {6, 8, 23}
    NQR_17           17                 {17, 22, 35}

Note: 8·μ₃ = {6, 8, 23} = TESLA_ORB.  The element 8 = 2³ generates TESLA_ORB
as a coset representative, not DARK_A.  8 has dlog = 3, order 4 in F₃₇×/μ₃.

DARK_A = 2·μ₃ generates F₃₇×/μ₃ ≅ C₁₂ (dlog(2) = 1, order 12 in quotient).

STRUCTURAL CONSEQUENCE: NQR × NQR → QR
=========================================

In the H₉-coset group (ℤ/4ℤ):
  2·H₉ is position 1, 8·H₉ is position 3.  1+3 = 4 ≡ 0 → H₉ (QR).
  2·H₉ × 2·H₉ → 4·H₉ (QR).  8·H₉ × 8·H₉ → 64·H₉ = H₉ (QR).

The NQR×NQR→QR rule (Theorem 138) follows directly from the H₉-coset arithmetic.
The orbit product table is a refinement of the H₉-coset multiplication table.
"""

P = 37

mu3 = frozenset({1, 10, 26})
H9  = frozenset({1, 7, 9, 10, 12, 16, 26, 33, 34})
QR  = frozenset(pow(a, 2, P) for a in range(1, P))

ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_14':           frozenset({14, 29, 31}),
    'SEED_ORB':         frozenset({18, 24, 32}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_17':           frozenset({17, 22, 35}),
}

QR_ORBITS  = {'IC', 'D7', 'SA_ORB', 'SOVEREIGN_SPIRAL', 'ORBIT_11', 'OUTLIER_ORB'}
NQR_ORBITS = {'DARK_A', 'NQR_14', 'SEED_ORB', 'NQR_5', 'TESLA_ORB', 'NQR_17'}

H9_COSETS = {
    '1*H9': frozenset(1 * x % P for x in H9),
    '2*H9': frozenset(2 * x % P for x in H9),
    '4*H9': frozenset(4 * x % P for x in H9),
    '8*H9': frozenset(8 * x % P for x in H9),
}

QR_H9_COSETS  = frozenset().union(H9_COSETS['1*H9'], H9_COSETS['4*H9'])
NQR_H9_COSETS = frozenset().union(H9_COSETS['2*H9'], H9_COSETS['8*H9'])

COSET_REPS = {
    'IC': 1, 'D7': 7, 'SA_ORB': 9,
    'SOVEREIGN_SPIRAL': 3, 'ORBIT_11': 11, 'OUTLIER_ORB': 21,
    'DARK_A': 2, 'NQR_14': 14, 'SEED_ORB': 18,
    'NQR_5': 5, 'TESLA_ORB': 6, 'NQR_17': 17,
}


def run_assertions():
    import math

    # Tower containment
    assert mu3 <= H9
    assert H9 <= QR
    assert QR <= frozenset(range(1, P))

    # Orders and indices
    assert len(mu3) == 3
    assert len(H9)  == 9
    assert len(QR)  == 18
    assert len(H9) // len(mu3) == 3
    assert len(QR) // len(H9) == 2

    # H9 = ⟨16⟩
    h9_gen = frozenset(pow(16, k, P) for k in range(9))
    assert h9_gen == H9

    # Each H9-coset decomposes into exactly 3 mu3-cosets
    for hc in H9_COSETS.values():
        contained = [name for name, orb in ORBITS.items() if orb <= hc]
        assert len(contained) == 3, f"H9-coset {hc} contains {len(contained)} mu3-cosets"

    # H9-coset decomposition matches the named groups exactly
    assert ORBITS['IC'] | ORBITS['D7'] | ORBITS['SA_ORB']           == H9_COSETS['1*H9']
    assert ORBITS['DARK_A'] | ORBITS['NQR_14'] | ORBITS['SEED_ORB'] == H9_COSETS['2*H9']
    assert ORBITS['SOVEREIGN_SPIRAL'] | ORBITS['ORBIT_11'] | ORBITS['OUTLIER_ORB'] == H9_COSETS['4*H9']
    assert ORBITS['NQR_5'] | ORBITS['TESLA_ORB'] | ORBITS['NQR_17'] == H9_COSETS['8*H9']

    # Each H9-coset is entirely QR or entirely NQR
    assert all(x in QR for x in H9_COSETS['1*H9'])
    assert all(x in QR for x in H9_COSETS['4*H9'])
    assert all(x not in QR for x in H9_COSETS['2*H9'])
    assert all(x not in QR for x in H9_COSETS['8*H9'])

    # QR/NQR of named orbits determined entirely by H9-coset membership
    for name, orb in ORBITS.items():
        in_qr_h9 = orb <= QR_H9_COSETS
        labeled_qr = name in QR_ORBITS
        assert in_qr_h9 == labeled_qr, f"{name}: H9-coset QR={in_qr_h9} but labeled QR={labeled_qr}"

    # Coset-of-mu3 representation
    for name, rep in COSET_REPS.items():
        assert frozenset(rep * m % P for m in mu3) == ORBITS[name], \
            f"{name}: {rep}*mu3 != {sorted(ORBITS[name])}"

    # 8*mu3 = TESLA_ORB (not DARK_A)
    assert frozenset(8 * m % P for m in mu3) == ORBITS['TESLA_ORB']
    assert 8 not in ORBITS['DARK_A']

    # DARK_A = 2*mu3 generates quotient: dlog(2) mod 12 = 1
    dlp = {}
    x = 1
    for k in range(36):
        dlp[x] = k
        x = x * 2 % P
    assert dlp[2] % 12 == 1
    assert all(dlp[a] % 12 == 1 for a in ORBITS['DARK_A'])

    # 8 has order 4 in quotient
    assert dlp[8] == 3
    assert 12 // math.gcd(3, 12) == 4

    # H9-coset group ≅ ℤ/4ℤ (positions: 1*H9=0, 2*H9=1, 4*H9=2, 8*H9=3)
    # NQR x NQR -> QR: positions 1+1=2, 3+3=2 (both land in 4*H9, QR)
    assert frozenset(a * b % P for a in H9_COSETS['2*H9'] for b in H9_COSETS['2*H9']) == H9_COSETS['4*H9']
    assert frozenset(a * b % P for a in H9_COSETS['8*H9'] for b in H9_COSETS['8*H9']) == H9_COSETS['4*H9']
    assert frozenset(a * b % P for a in H9_COSETS['2*H9'] for b in H9_COSETS['8*H9']) == H9_COSETS['1*H9']

    # 12 orbits cover F37x, pairwise disjoint
    union = frozenset().union(*ORBITS.values())
    assert union == frozenset(range(1, P))
    pairs = [(a, b) for i, a in enumerate(ORBITS.values())
                    for j, b in enumerate(ORBITS.values()) if i < j]
    assert all(len(a & b) == 0 for a, b in pairs)

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 142: Subgroup Tower μ₃ < H₉ < QR < F₃₇×")
    print("=" * 62)
    print()
    print("  Tower:  μ₃ (order 3) < H₉ (order 9) < QR (order 18) < F₃₇×")
    print("  Indices: [H₉:μ₃]=3,  [QR:H₉]=2,  [F₃₇×:QR]=2")
    print()
    print("  μ₃ ⊂ H₉: each H₉-coset splits into exactly 3 μ₃-cosets.")
    print()
    print("  H₉-coset decomposition:")
    print("    1·H₉ (QR):  IC  |  D7  |  SA_ORB")
    print("    4·H₉ (QR):  SOVEREIGN_SPIRAL  |  ORBIT_11  |  OUTLIER_ORB")
    print("    2·H₉ (NQR): DARK_A  |  NQR_14  |  SEED_ORB")
    print("    8·H₉ (NQR): NQR_5   |  TESLA_ORB  |  NQR_17")
    print()
    print("  QR/NQR of named orbits = QR/NQR of their H₉-coset (12/12 match).")
    print()
    print("  8·μ₃ = TESLA_ORB = {6,8,23}.  8 ∉ DARK_A.")
    print("  DARK_A = 2·μ₃, dlog ≡ 1 mod 12, generates F₃₇×/μ₃ ≅ C₁₂.")
    print()
    print("  H₉-coset group ≅ ℤ/4ℤ (positions 0-3).  NQR = positions 1,3.")
    print("  2·H₉×2·H₉=4·H₉ (QR),  8·H₉×8·H₉=4·H₉ (QR),  2·H₉×8·H₉=H₉ (QR).")
    print("  NQR×NQR→QR (Theorem 138) follows directly. ✓")


if __name__ == "__main__":
    run_assertions()
    summarise()

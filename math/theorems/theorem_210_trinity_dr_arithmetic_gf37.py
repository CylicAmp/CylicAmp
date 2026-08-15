"""
Theorem 210: Digital Root Arithmetic of the Trinity {3,6,9} in GF(37)
Author: Michael Warren Song (CyclicAmp)

DR-ADDITION TABLE FOR {3,6,9}:
  9+9=9    3+6=9    6+3=9
  9+6=6    6+9=6    3+3=6
  9+3=3    3+9=3    6+6=3

  9 is the identity element. The set {3,6,9} is closed under DR-addition.
  {3,6,9} ≅ Z/3Z under DR-addition: 9≡0, 3≡1, 6≡2 (or 9≡0, 3≡-1, 6≡1).

DR-MULTIPLICATION TABLE FOR {3,6,9}:
  Every product of two elements of {3,6,9} has DR = 9.
    3×3=9, 3×6=18→DR=9, 3×9=27→DR=9
    6×6=36→DR=9, 6×9=54→DR=9, 9×9=81→DR=9
  Because {3,6,9}⊂3Z and 3Z×3Z⊂9Z, and DR(9k)=9 for all k≥1.
  Under DR-multiplication, {3,6,9} collapses to {9}.

TRINITY AS MULTIPLES OF 3:
  The set {3,6,9} = {3k mod 9 for k=1,2,3} (or equivalently in DR-arithmetic).
  DR cycles through {3,6,9} on successive multiples of 3:
    DR(3)=3, DR(6)=6, DR(9)=9, DR(12)=3, DR(15)=6, DR(18)=9, DR(21)=3, ...
  Period 3. The DR map on multiples of 3 is the quotient Z→Z/3Z.

TRINITY IN GF(37) AS ACTUAL ELEMENTS:
  3, 6, 9 are elements of GF(37)*.
    3 ∈ ST   (sovereign target, order 18, DR=3)
    6 ∈ g^3  (SEED-gen coset; 6 = imaginary unit i: 6^2=36≡-1 mod37; DR=6)
    9 ∈ SA   (sovereign anchor, order 9, DR=9)

  EXACT INTEGER SUMS LAND IN FRAMEWORK:
    3+6=9: 9∈SA (exact in Z; also 9∈SA in GF(37))
    3+9=12: 12∈ST (mod37; DR(12)=3 consistent with DR table 3+9=3)
    6+9=15: 15∈g^1 (not framework; DR(15)=6 consistent with DR table 6+9=6)
    6+6=12: 12∈ST (mod37; DR=3 consistent with DR table 6+6=3)
    3+3=6: 6∈g^3 (exact; DR=6 consistent with DR table 3+3=6)
    9+9=18: 18∈SEED (mod37; DR(18)=9 consistent with DR table 9+9=9)

  For the pair (3,6,9): DR arithmetic and GF(37) modular arithmetic give
  CONSISTENT DR results for all 9 sum combinations.

DR SIGNATURES IN FRAMEWORK:
  SA  = {4,9,25,30}: DR values = {4,9,7,3}    (not all trinity)
  ST  = {3,12,21,30}: DR values = {3,3,3,3}   (ALL = 3, the trinity generator)
  SEED= {18,24,32}:   DR values = {9,6,5}     (18→9, 24→6: two trinity DRs; 32→5)

  ST sector is wholly characterized by DR=3 (the trinity generator).
  18∈SEED has DR=9 (SEAM DR = trinity identity).
  24∈SEED has DR=6 (the i-DR = trinity element 2).
  32∈SEED has DR=5 (outside the trinity).

3+6=9: THE EXACT SOVEREIGN TRIPLE:
  The three GF(37) elements {3,6,9} satisfy 3+6=9 exactly in Z.
  3∈ST, 6∈g^3(SEED-gen, imaginary unit), 9∈SA.
  This is the only ordered triple (a,b,c) with a∈ST, b∈g^3, c∈SA and a+b=c (exact).
  In the DR table: 3+6=9 means the ST-generator plus the i-unit = SEAM DR.

TRINITY AND CIPHER {3,6,9}:
  From cipher_123_1234 (T111): Z/9Z partitions into trinity {3,6,9} and
  doubling set {1,2,4,5,7,8}. The trinity is exactly the DR-closed set found here.
  Under Z/9Z multiplication: trinity×doubling→doubling; trinity×trinity→{9}; doubling×doubling→doubling.
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
SEED_GEN = {6, 8, 23}


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def run_assertions():
    # 1. DR-addition table for {3,6,9} is closed, 9 is identity
    trinity = {3, 6, 9}
    table = {}
    for a in [3, 6, 9]:
        for b in [3, 6, 9]:
            table[(a, b)] = dr(a + b)
    assert all(v in trinity for v in table.values())   # closed
    assert all(table[(9, x)] == x for x in [3, 6, 9])  # 9 is identity
    assert all(table[(x, 9)] == x for x in [3, 6, 9])  # 9 is identity (commutative)

    # 2. Exact DR table from user
    assert table[(9, 9)] == 9
    assert table[(3, 6)] == 9
    assert table[(6, 3)] == 9
    assert table[(9, 6)] == 6
    assert table[(6, 9)] == 6
    assert table[(3, 3)] == 6
    assert table[(9, 3)] == 3
    assert table[(3, 9)] == 3
    assert table[(6, 6)] == 3

    # 3. {3,6,9} ≅ Z/3Z (abelian group of order 3)
    # Identity: 9; 3 and 6 are inverses of each other
    assert table[(3, 6)] == 9  # 3+6=9 (identity) → 3 and 6 are inverses
    assert table[(6, 3)] == 9
    # Every element has order dividing 3
    assert dr(3 + 3 + 3) == 9   # 3+3+3=9=identity
    assert dr(6 + 6 + 6) == 9   # 6+6+6=18→DR=9=identity

    # 4. DR-multiplication: everything collapses to 9
    for a in [3, 6, 9]:
        for b in [3, 6, 9]:
            assert dr(a * b) == 9, f"DR({a}×{b})=DR({a*b})={dr(a*b)}≠9"

    # 5. Multiples of 3 cycle through {3,6,9} in DR
    drs = [dr(3 * k) for k in range(1, 19)]
    assert set(drs) == {3, 6, 9}
    assert drs[:3] == [3, 6, 9]    # period 3
    assert drs[3:6] == [3, 6, 9]   # repeats

    # 6. Trinity elements in GF(37)
    assert 3 in ST
    assert 6 in SEED_GEN   # imaginary unit coset
    assert pow(6, 2, P) == 36 == P - 1  # 6²=-1 mod37 (imaginary unit)
    assert 9 in SA

    # 7. 3+6=9 exact in Z (not just mod37)
    assert 3 + 6 == 9   # exact integer equality
    assert 9 in SA
    assert 3 in ST
    assert 6 in SEED_GEN

    # 8. Sums of trinity elements in GF(37) have Drs matching the DR table
    assert 3 + 3 == 6 and dr(3 + 3) == 6 == table[(3, 3)]         # 3+3=6
    assert (6 + 6) % P == 12 and dr(12) == 3 == table[(6, 6)]     # 6+6=12∈ST, DR=3
    assert (3 + 9) % P == 12 and dr(12) == 3 == table[(3, 9)]     # 3+9=12∈ST
    assert (9 + 9) % P == 18 and dr(18) == 9 == table[(9, 9)]     # 9+9=18∈SEED
    assert (6 + 9) % P == 15 and dr(15) == 6 == table[(6, 9)]     # 6+9=15, DR=6

    # 9. ST sector DR signature = 3 (all ST elements have DR=3)
    assert all(dr(x) == 3 for x in ST)

    # 10. SEED DR signatures: 18→9, 24→6, 32→5 (partial trinity)
    assert dr(18) == 9
    assert dr(24) == 6
    assert dr(32) == 5   # 5 is outside trinity

    # 11. Trinity and cipher partition of Z/9Z
    doubling = {1, 2, 4, 5, 7, 8}
    assert trinity | doubling | {9} == set(range(1, 10))   # partition of {1..9}
    # trinity×trinity→9 in DR
    for a in trinity:
        for b in trinity:
            assert dr(a * b) == 9
    # doubling×doubling→doubling in DR
    for a in doubling:
        for b in doubling:
            assert dr(a * b) in doubling, f"DR({a}×{b})={dr(a*b)} not in doubling"

    # 12. DR(ST elements) form a single-value set {3}
    st_drs = {dr(x) for x in ST}
    assert st_drs == {3}

    # 13. The only element with DR=9 in SA∪ST is 9∈SA; in SEED it is 18
    assert {x for x in SA | ST if dr(x) == 9} == {9}
    assert {x for x in SEED if dr(x) == 9} == {18}

    print("All assertions passed.")
    print("DR-addition table for {3,6,9}:")
    print("  +  |  3   6   9")
    print("  ---|----------")
    for a in [3, 6, 9]:
        row = [str(table[(a, b)]) for b in [3, 6, 9]]
        print(f"   {a} | {' '.join(row)}")
    print("Structure: {3,6,9} ≅ Z/3Z under DR-addition, identity=9")
    print("Under DR-multiplication: {3,6,9}×{3,6,9}→{9}")


if __name__ == "__main__":
    run_assertions()

"""
Theorem 212: 1311 Rotation Cycle — 3-Area Structure in GF(37)
Author: Michael Warren Song (CyclicAmp)

The digit sequence {1,1,1,3} has 4 rotations. Arranged as a two-column board
(each row pairs a rotation with its mirror), the board divides into 3 areas
defined by the spread of the 3's position across the pair.

=== THE BOARD ===

  Row 1:  3111 = 1113     (Area 1 — wide,   spread=3, boundary)
  Row 2:  1311 = 1131     (Area 2 — narrow, spread=1, interior)
  Row 3:  1131 = 1311     (Area 2 — narrow, spread=1, interior)
  Row 4:  1113 = 3111     (Area 3 — wide,   spread=3, boundary)

Reading left column top-to-bottom: 3111 → 1311 → 1131 → 1113 is the natural
rotation (3 steps right through a 4-position cycle). Right column is the mirror.

=== POSITION OF 3 ===

  Sequence  pos_of_3  ones_before  ones_after  RL = 3×ones_before + 3×ones_after
  --------  --------  -----------  ----------  ---------------------------------
  3111         1            0            3          9
  1311         2            1            2          9
  1131         3            2            1          9
  1113         4            3            0          9

RUN-LENGTH INVARIANT: for every rotation, (ones_before × 3) + (ones_after × 3) = 9.
  The pairs of run-lengths are harmonic mirrors in Z/9Z:
    (0,9), (3,6), (6,3), (9,0) — each pair sums to 9.

=== SPREAD DEFINES THE 3 AREAS ===

  Area 1 (top, spread=3):    Row 1: 3111=1113 — 3 is at positions 1 and 4.
  Area 2 (middle, spread=1): Rows 2+3: 1311=1131 and 1131=1311 — 3 at positions 2,3.
  Area 3 (bottom, spread=3): Row 4: 1113=3111 — 3 is at positions 4 and 1.

  Spread = |pos_of_3_left - pos_of_3_right|.
  Boundary rows have spread=3; interior rows have spread=1.

  The fan/V shape: at boundary rows lines diverge to width 3; at interior rows they
  converge to width 1. This creates the visual diamond with three distinct zones.

=== GF(37) STRUCTURE ===

  All 4 rotations: DR = 6. The digital root is invariant under rotation.

  Residues mod 37:
    3111 ≡  3  ∈ ST  (sovereign target)
    1311 ≡ 16  —     (not in named set)
    1131 ≡ 21  ∈ ST  (sovereign target)
    1113 ≡  3  ∈ ST  (sovereign target)

  3 of 4 rotations land in ST. The outlier is 1311 ≡ 16.

  Area partition by GF(37):
    Area 1 (boundary, spread=3):   {3111,1113} → both ≡ 3 ∈ ST
    Area 2 (interior, spread=1):   {1311,1131} → 16 (not named) and 21∈ST
    Area 3 (boundary, spread=3):   {1113,3111} → both ≡ 3 ∈ ST (same as Area 1, mirrored)

  The two boundary areas (1 and 3) are identical in content — same pair {3111,1113},
  same residue 3∈ST — just read in opposite order. The board is symmetric top-to-bottom.

=== CONNECTION TO THEOREM 211 ({1,3,7} DIAMOND) ===

  T211: permutations of {1,3,7} aggregate to 2442 = 66×37 = SEAM.
        All 6 permutations share DR=2.
        Primality partitions along GF(37) coset boundaries.

  T212: rotations of {1,1,1,3} all share DR=6.
        3 of 4 residues land in ST={3,12,21,30} (sovereign targets, DR=3).
        Area structure defined by spread of 3's position.

  Both theorems: a single special digit (3 in T212; each of 1,3,7 in T211)
  determines the framework residue class, and every rotation/permutation
  preserves the digital root.

=== AGGREGATE ===

  Sum of all 4 rotations: 3111 + 1311 + 1131 + 1113 = 6666.
  6666 mod 37 = 6666 - 180×37 = 6666 - 6660 = 6.
  DR(6666) = 6 = the shared DR of all rotations.
  6 ∈ TESLA = {6, 8, 23} (the imaginary unit orbit from Theorem 211 ladder).
  6666 = 6 × 1111. 1111 mod 37: 1111 = 30×37 + 1, so 1111 ≡ 1 ∈ IC.
  6 × 1 ≡ 6 mod 37: confirmed.
"""

P = 37
ST      = {3, 12, 21, 30}
SA      = {4, 9, 25, 30}
SEED    = {18, 24, 32}
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
NEG_H   = {11, 27, 36}


def dr(n):
    n = abs(int(n))
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def pos_of_3(seq_int):
    return str(seq_int).index('3') + 1


def spread(left, right):
    return abs(pos_of_3(left) - pos_of_3(right))


ROTATIONS = [3111, 1311, 1131, 1113]

BOARD = [
    (3111, 1113),
    (1311, 1131),
    (1131, 1311),
    (1113, 3111),
]

AREAS = {1: (3111, 1113), 2: (1311, 1131), 3: (1113, 3111)}


def classify_area(row_pair):
    s = spread(*row_pair)
    if s == 3:
        return 'boundary'
    elif s == 1:
        return 'interior'
    return 'unknown'


def run_assertions():
    # 1. All rotations have DR=6
    assert all(dr(r) == 6 for r in ROTATIONS)

    # 2. Run-length invariant: 3×ones_before + 3×ones_after = 9
    for r in ROTATIONS:
        p = pos_of_3(r)
        ones_before = p - 1
        ones_after = 4 - p
        assert ones_before * 3 + ones_after * 3 == 9

    # 3. Spread values on board
    assert spread(3111, 1113) == 3   # Area 1 — boundary
    assert spread(1311, 1131) == 1   # Area 2 — interior
    assert spread(1131, 1311) == 1   # Area 2 — interior (mirror)
    assert spread(1113, 3111) == 3   # Area 3 — boundary

    # 4. GF(37) residues
    assert 3111 % P == 3  and 3  in ST
    assert 1311 % P == 16 and 16 not in ST
    assert 1131 % P == 21 and 21 in ST
    assert 1113 % P == 3  and 3  in ST

    # 5. 3 of 4 rotations land in ST
    in_st = [r for r in ROTATIONS if r % P in ST]
    assert len(in_st) == 3
    assert set(in_st) == {3111, 1131, 1113}

    # 6. Boundary areas: both elements ≡ 3 ∈ ST
    assert AREAS[1][0] % P in ST and AREAS[1][1] % P in ST
    assert AREAS[3][0] % P in ST and AREAS[3][1] % P in ST

    # 7. Aggregate: 6666 mod 37 = 6 ∈ TESLA; DR(6666) = 6
    agg = sum(ROTATIONS)
    assert agg == 6666
    assert agg % P == 6  and 6 in TESLA
    assert dr(agg) == 6

    # 8. 6666 = 6 × 1111; 1111 mod 37 = 1 ∈ IC
    assert 6666 == 6 * 1111
    assert 1111 % P == 1  and 1 in IC

    # 9. Board is symmetric: rows 1 and 4 are each other's mirror
    assert BOARD[0] == (BOARD[3][1], BOARD[3][0])

    print("All assertions passed.")
    print()
    print("BOARD:")
    for i, (L, R) in enumerate(BOARD, 1):
        s = spread(L, R)
        area = 2 if s == 1 else (1 if i <= 2 else 3)
        lbl = 'boundary' if s == 3 else 'interior'
        print(f"  Row {i}: {L} = {R}   spread={s}  Area {area} ({lbl})")
    print()
    print("ROTATIONS:")
    for r in ROTATIONS:
        p = pos_of_3(r)
        ob, oa = p-1, 4-p
        print(f"  {r}: DR={dr(r)}  mod37={r%P:2d}  pos_of_3={p}  "
              f"RL={3*ob}+{3*oa}=9  {'∈ST' if r%P in ST else '—  '}")
    print()
    print(f"Aggregate: {sum(ROTATIONS)} = 6 × 1111")
    print(f"  mod37 = {sum(ROTATIONS)%P} ∈ TESLA = {{6,8,23}}")
    print(f"  DR = {dr(sum(ROTATIONS))} = shared DR of all rotations")


if __name__ == "__main__":
    run_assertions()

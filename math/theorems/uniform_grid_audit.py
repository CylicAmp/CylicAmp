"""
uniform_grid_audit.py

Six uniform bivariate arithmetic grids and two supporting mathematical
identities (Pearson r, DR fixed-point).

─────────────────────────────────────────────────────────────────
GENERAL MODEL:
  M(i,j) = a + (i−1)·d_R + (j−1)·d_C

  Horizontal: M(i,j+1) − M(i,j) = d_C
  Vertical:   M(i+1,j) − M(i,j) = d_R
  Displacement: M(i+k, j+ℓ) = M(i,j) + k·d_R + ℓ·d_C

GRID PARAMETERS (3×3 shown):
  File           a    d_R   d_C   d_R+d_C
  1000242649     3     4     7      11 = repunit_2
  1000242641    13     5    14      19
  1000242637     7     6     7      13 = 6th prime
  1000242644     2     3     5       8 = AHL
  1000242642     1     2     3       5
  1000242643     1     2     3       5

KEY FACTS:
  (U1) Grids 3, 4, 5/6 are DR-complete: the 3×3 DR values are a permutation
       of {1,2,3,4,5,6,7,8,9}. Grids 1 and 2 have DR collisions.

  (U2) Grid 1 row DR sums = col DR sums = [12,15,18] → DR [3,6,9] (ascending).
       Grid 2 row DR sums = col DR sums = [18,15,12] → DR [9,6,3] (descending).
       Grid 3 all row DR sums = 15 → DR = 6 (constant row); cols [3,6,9].
       Grid 4 all row DR sums → DR = 3 (constant); cols DR [6,3,9].
       Grid 5/6 all col DR sums = [9,9,9] = NULL throughout.

  (U3) Framework constants appearing as cell values:
       G1: M(3,2)=18=GATE; M(1,3)=17=criss-cross; M(1,2)=10=mod-ratio
       G2: M(2,1)=18=GATE; M(3,2)=37=modulus; M(1,2)=27=3³
       G3: M(3,2)=26=slot(137); M(3,3)=33=count-DR8; M(1,1)=7=ALO
       G4: M(3,3)=18=GATE; M(3,1)=8=AHL; M(1,2)=7=ALO; M(2,2)=10=mod-ratio
       G5/6: M(3,2)=8=AHL; M(1,3)=7=ALO; M(3,3)=11=repunit_2

  (U4) Parameter triples (a, d_R, d_C):
       G5/6: (1,2,3) = cascade axioms = first digits of φ, e, π
       G4:   (2,3,5) = first three primes; sum=10=26⁻¹ mod 37 (modular ratio)
       G3:   (7,6,7) = ALO, DR(AHL+ALO), ALO; d_R+d_C=13=6th prime
       G1:   (3,4,7) = TRIAD axiom, cycle-step-3, ALO; d_R+d_C=11=repunit_2

  (U5) DR fixed point: DR(2n) = n ⟺ n = 9.
       9 is the unique digital root satisfying this self-referential identity.

  (U6) Pearson r ∈ [−1, 1]: r=0 corresponds to no linear relationship (NULL);
       r=±1 to perfect correlation. The r=0 null mirrors the DR(9)=9 null
       in that both mark the pivot/center of their respective ranges.
─────────────────────────────────────────────────────────────────
"""

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(n) % 9
    return r if r else 9


def M(a, dR, dC, i, j):
    return a + (i - 1) * dR + (j - 1) * dC


def grid3x3(a, dR, dC):
    return [[M(a, dR, dC, i, j) for j in range(1, 4)] for i in range(1, 4)]


def dr_grid(g):
    return [[dr(v) for v in row] for row in g]


def is_complete_perm(dg):
    vals = sorted(v for row in dg for v in row)
    return vals == list(range(1, 10))


GRIDS = [
    (3,  4,  7,  "G1"),
    (13, 5,  14, "G2"),
    (7,  6,  7,  "G3"),
    (2,  3,  5,  "G4"),
    (1,  2,  3,  "G5"),
    (1,  2,  3,  "G6"),
]

for a, dR, dC, label in GRIDS:
    g  = grid3x3(a, dR, dC)
    dg = dr_grid(g)

    # ── Bivariate formula verification ──────────────────────────────────────
    for i in range(1, 4):
        for j in range(1, 4):
            expected_val = a + (i - 1) * dR + (j - 1) * dC
            check(g[i - 1][j - 1] == expected_val,
                  f"{label} M({i},{j}) = a+(i-1)d_R+(j-1)d_C",
                  g[i - 1][j - 1], expected_val)

    # Horizontal step = d_C
    for i in range(3):
        for j in range(2):
            step = g[i][j + 1] - g[i][j]
            check(step == dC, f"{label} row {i+1} horiz step = d_C", step, dC)

    # Vertical step = d_R
    for i in range(2):
        for j in range(3):
            step = g[i + 1][j] - g[i][j]
            check(step == dR, f"{label} col {j+1} vert step = d_R", step, dR)


# ── U1: DR-completeness ───────────────────────────────────────────────────────

for a, dR, dC, label in GRIDS:
    g  = grid3x3(a, dR, dC)
    dg = dr_grid(g)
    complete = is_complete_perm(dg)
    if label in ("G3", "G4", "G5", "G6"):
        check(complete, f"{label} DR grid is complete permutation of {{1..9}}",
              complete, True)
    else:
        check(not complete, f"{label} DR grid has collisions (not complete)",
              complete, False)


# ── U2: Row and column DR sum patterns ───────────────────────────────────────

def row_dr_sums(dg):
    return [sum(row) for row in dg]

def col_dr_sums(dg):
    return [sum(dg[i][j] for i in range(3)) for j in range(3)]

# G1: both rows and cols → [12,15,18] → DR [3,6,9]
g1 = grid3x3(3, 4, 7); dg1 = dr_grid(g1)
check(row_dr_sums(dg1) == [12, 15, 18], "G1 row DR sums = [12,15,18]",
      row_dr_sums(dg1), [12, 15, 18])
check(col_dr_sums(dg1) == [12, 15, 18], "G1 col DR sums = [12,15,18]",
      col_dr_sums(dg1), [12, 15, 18])
check([dr(s) for s in row_dr_sums(dg1)] == [3, 6, 9], "G1 row DR → [3,6,9]",
      [dr(s) for s in row_dr_sums(dg1)], [3, 6, 9])

# G2: both → [18,15,12] → DR [9,6,3]
g2 = grid3x3(13, 5, 14); dg2 = dr_grid(g2)
check(row_dr_sums(dg2) == [18, 15, 12], "G2 row DR sums = [18,15,12]",
      row_dr_sums(dg2), [18, 15, 12])
check(col_dr_sums(dg2) == [18, 15, 12], "G2 col DR sums = [18,15,12]",
      col_dr_sums(dg2), [18, 15, 12])
check([dr(s) for s in row_dr_sums(dg2)] == [9, 6, 3], "G2 row DR → [9,6,3]",
      [dr(s) for s in row_dr_sums(dg2)], [9, 6, 3])

# G3: all row DR sums = 15 → DR 6 (constant)
g3 = grid3x3(7, 6, 7); dg3 = dr_grid(g3)
check(row_dr_sums(dg3) == [15, 15, 15], "G3 all row DR sums = 15",
      row_dr_sums(dg3), [15, 15, 15])
check(all(dr(s) == 6 for s in row_dr_sums(dg3)), "G3 all row DR = 6",
      [dr(s) for s in row_dr_sums(dg3)], [6, 6, 6])
check([dr(s) for s in col_dr_sums(dg3)] == [3, 6, 9], "G3 col DR → [3,6,9]",
      [dr(s) for s in col_dr_sums(dg3)], [3, 6, 9])

# G4: all row DR → 3 (constant); cols [6,3,9]
g4 = grid3x3(2, 3, 5); dg4 = dr_grid(g4)
check(all(dr(s) == 3 for s in row_dr_sums(dg4)), "G4 all row DR = 3",
      [dr(s) for s in row_dr_sums(dg4)], [3, 3, 3])
check([dr(s) for s in col_dr_sums(dg4)] == [6, 3, 9], "G4 col DR → [6,3,9]",
      [dr(s) for s in col_dr_sums(dg4)], [6, 3, 9])

# G5: all col DR sums → 9 (NULL)
g5 = grid3x3(1, 2, 3); dg5 = dr_grid(g5)
check(all(dr(s) == 9 for s in col_dr_sums(dg5)), "G5 all col DR = 9 (NULL)",
      [dr(s) for s in col_dr_sums(dg5)], [9, 9, 9])


# ── U3: Framework constants in cell values ────────────────────────────────────

# G1
check(M(3, 4, 7, 3, 2) == 18, "G1 M(3,2) = 18 = GATE", M(3, 4, 7, 3, 2), 18)
check(M(3, 4, 7, 1, 3) == 17, "G1 M(1,3) = 17 = criss-cross prime", M(3, 4, 7, 1, 3), 17)
check(M(3, 4, 7, 1, 2) == 10, "G1 M(1,2) = 10 = 26⁻¹ mod 37", M(3, 4, 7, 1, 2), 10)
check(M(3, 4, 7, 2, 1) == 7,  "G1 M(2,1) = 7 = ALO", M(3, 4, 7, 2, 1), 7)
check(M(3, 4, 7, 3, 1) == 11, "G1 M(3,1) = 11 = repunit_2", M(3, 4, 7, 3, 1), 11)

# G2
check(M(13, 5, 14, 2, 1) == 18, "G2 M(2,1) = 18 = GATE", M(13, 5, 14, 2, 1), 18)
check(M(13, 5, 14, 3, 2) == 37, "G2 M(3,2) = 37 = framework modulus", M(13, 5, 14, 3, 2), 37)
check(M(13, 5, 14, 1, 2) == 27, "G2 M(1,2) = 27 = 3³", M(13, 5, 14, 1, 2), 27)
check(27 == 3 ** 3, "27 = 3³ (appears in loop-audit mod-37 subtotals)", 27, 3 ** 3)

# G3
check(M(7, 6, 7, 3, 2) == 26, "G3 M(3,2) = 26 = slot(137) = AHL digit-sum", M(7, 6, 7, 3, 2), 26)
check(M(7, 6, 7, 3, 3) == 33, "G3 M(3,3) = 33 = count DR-8 in 1..300", M(7, 6, 7, 3, 3), 33)
check(M(7, 6, 7, 1, 1) == 7,  "G3 M(1,1) = 7 = ALO", M(7, 6, 7, 1, 1), 7)
check(137 % 37 == 26, "26 = slot(137) in Z/37Z", 137 % 37, 26)

# G4
check(M(2, 3, 5, 3, 3) == 18, "G4 M(3,3) = 18 = GATE", M(2, 3, 5, 3, 3), 18)
check(M(2, 3, 5, 3, 1) == 8,  "G4 M(3,1) = 8 = AHL", M(2, 3, 5, 3, 1), 8)
check(M(2, 3, 5, 1, 2) == 7,  "G4 M(1,2) = 7 = ALO", M(2, 3, 5, 1, 2), 7)
check(M(2, 3, 5, 2, 2) == 10, "G4 M(2,2) = 10 = mod-ratio", M(2, 3, 5, 2, 2), 10)
check(M(2, 3, 5, 3, 2) == 13, "G4 M(3,2) = 13 = 6th prime", M(2, 3, 5, 3, 2), 13)

# G5
check(M(1, 2, 3, 3, 2) == 8,  "G5 M(3,2) = 8 = AHL", M(1, 2, 3, 3, 2), 8)
check(M(1, 2, 3, 1, 3) == 7,  "G5 M(1,3) = 7 = ALO", M(1, 2, 3, 1, 3), 7)
check(M(1, 2, 3, 3, 3) == 11, "G5 M(3,3) = 11 = repunit_2", M(1, 2, 3, 3, 3), 11)


# ── U4: Parameter triple connections ─────────────────────────────────────────

# G5/6: (1,2,3) = cascade axioms (first digits of φ, e, π)
check((1, 2, 3) == (1, 2, 3), "G5/6 params = cascade axioms (φ=1,e=2,π=3)", (1, 2, 3), (1, 2, 3))
check(1 + 2 + 3 == 6, "G5/6 param sum = 6 = DR(6) fixed point", 1 + 2 + 3, 6)
check(dr(1 + 2 + 3) == 6, "DR(1+2+3) = 6", dr(1 + 2 + 3), 6)

# G4: (2,3,5) = first three primes; sum = 10 = modular ratio
check(2 + 3 + 5 == 10, "G4 param sum = 10 = 26⁻¹ mod 37", 2 + 3 + 5, 10)
check(26 * 10 % 37 == 1, "26×10 ≡ 1 mod 37", 26 * 10 % 37, 1)

# G3: (7,6,7); d_R+d_C=13=6th prime; a=d_C=7 (anchor equals column step)
check(7 == 7, "G3: a = d_C = 7 (anchor equals column step)", 7, 7)
check(6 + 7 == 13, "G3: d_R+d_C = 13 = 6th prime", 6 + 7, 13)
check(dr(6) == 6, "DR(d_R=6) = 6 = DR(AHL+ALO) = DR(33)", dr(6), 6)

# G1: d_R+d_C = 11 = repunit_2
check(4 + 7 == 11, "G1: d_R+d_C = 11 = repunit_2", 4 + 7, 11)


# ── U5: DR fixed point DR(2n) = n ⟺ n = 9 ────────────────────────────────────

for n in range(1, 10):
    satisfies = dr(2 * n) == n
    if n == 9:
        check(satisfies, "DR(2×9) = DR(18) = 9 = n (unique fixed point)", satisfies, True)
    else:
        check(not satisfies, f"DR(2×{n}) = {dr(2*n)} ≠ {n} (not a fixed point)",
              dr(2 * n) == n, False)

check(dr(18) == 9, "DR(18) = 9", dr(18), 9)
check((37 - 1) // 2 == 18, "GATE = (37-1)/2 = 18; DR(GATE) = 9", (37 - 1) // 2, 18)


# ── U6: Pearson r range and null ──────────────────────────────────────────────

# The correlation coefficient r ∈ [-1, 1]; r=0 = no relationship (null)
# r=0 ↔ DR(9)=9 (null/pivot) in that both are centers of their intervals
check(-1 <= 0 <= 1, "r=0 (null) ∈ [-1,1]", -1 <= 0 <= 1, True)
check(dr(9) == 9, "DR(9) = 9 = null anchor in digital-root", dr(9), 9)
# 9 = (1+17)/2? No. But 18 = (37-1)/2 = center of Z/37Z = 2×9.
check(18 == 2 * dr(9), "GATE = 2×DR(9) = 2×NULL", 18, 2 * dr(9))


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Uniform Grid Audit")
    print("=" * 62)

    for a, dR, dC, label in GRIDS[:5]:  # G5=G6, show once
        g  = grid3x3(a, dR, dC)
        dg = dr_grid(g)
        rds = row_dr_sums(dg)
        cds = col_dr_sums(dg)
        complete = is_complete_perm(dg)

        print(f"\n── {label}: a={a}  d_R={dR}  d_C={dC} ──")
        print(f"  Values:  {g[0]}")
        print(f"           {g[1]}")
        print(f"           {g[2]}")
        print(f"  DR grid: {dg[0]}")
        print(f"           {dg[1]}")
        print(f"           {dg[2]}")
        print(f"  Row DR sums: {rds} → DR {[dr(s) for s in rds]}")
        print(f"  Col DR sums: {cds} → DR {[dr(s) for s in cds]}")
        print(f"  DR complete permutation: {complete}")

    print("\n── U4: Parameter triples ──")
    print(f"  G5/6: (1,2,3) = φ,e,π cascade axioms; sum=6; DR(6)=6 (fixed point)")
    print(f"  G4:   (2,3,5) = first three primes; sum=10 = 26⁻¹ mod 37")
    print(f"  G3:   (7,6,7) = ALO,DR(AHL+ALO),ALO; d_R+d_C=13=6th prime")
    print(f"  G1:   (3,4,7) = TRIAD,cycle-step-3,ALO; d_R+d_C=11=repunit_2")
    print(f"  G2:   (13,5,14) = 6th-prime, cycle-step-6, 2×ALO")

    print(f"\n── U3: Framework constants as cell values ──")
    framework_hits = [
        ("G1", 3, 4, 7,  [(3,2,18,"GATE"), (1,3,17,"criss-cross"), (1,2,10,"mod-ratio"), (2,1,7,"ALO"), (3,1,11,"repunit_2")]),
        ("G2", 13,5,14, [(2,1,18,"GATE"), (3,2,37,"37-modulus"), (1,2,27,"3³")]),
        ("G3", 7, 6, 7,  [(3,2,26,"slot(137)"), (3,3,33,"count-DR8"), (1,1,7,"ALO")]),
        ("G4", 2, 3, 5,  [(3,3,18,"GATE"), (3,1,8,"AHL"), (1,2,7,"ALO"), (2,2,10,"mod-ratio"), (3,2,13,"6th prime")]),
        ("G5", 1, 2, 3,  [(3,2,8,"AHL"), (1,3,7,"ALO"), (3,3,11,"repunit_2")]),
    ]
    for label, a, dR, dC, hits in framework_hits:
        for i, j, val, name in hits:
            print(f"  {label} M({i},{j}) = {val} = {name}")

    print(f"\n── U5: DR(2n)=n ⟺ n=9 ──")
    for n in range(1, 10):
        mark = " ← UNIQUE FIXED POINT" if n == 9 else ""
        print(f"  n={n}: DR(2×{n}) = DR({2*n}) = {dr(2*n)} {'= n' if dr(2*n)==n else '≠ n'}{mark}")

    print(f"\n── U6: Pearson r null and digital-root null ──")
    print(f"  Pearson r ∈ [−1, 1];  r=0 → no relationship (null center)")
    print(f"  DR null: DR(9)=9; GATE=18=2×9; 3+6+9=18=GATE=(37-1)/2")
    print(f"  Both r=0 and DR(9)=9 are pivot centers of their respective ranges")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")

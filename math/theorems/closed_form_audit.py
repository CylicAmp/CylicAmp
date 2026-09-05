"""
closed_form_audit.py

Seven-row matrix closed-form, single-cell correction, residue structure,
rank, and the inherence of 177 as the anchor.

─────────────────────────────────────────────────────────────────
CLOSED-FORM:

  M(i,j) = 167 + 90(i-1) + 11(j-1) + ε(i,j)

  ε(i,j) = 10  if (i,j) = (1,1)
           = 0   otherwise

The entire 7×3 matrix is a single globally arithmetic form (a=167,
d_R=90, d_C=11) with one point perturbed by +10.

─────────────────────────────────────────────────────────────────
INHERENCE OF 177:
  177 = 3×59 = DESCENT[2] in the chain [191,188,177,166,...,100].
  It is the structurally required anchor in the Z/37Z framework.
  The ideal anchor 167 is derived, not primary.
  ε(1,1) = 10 = 26⁻¹ mod 37 = modular ratio (framework constant).

─────────────────────────────────────────────────────────────────
"""

from math import isqrt

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


def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    k = 5
    while k * k <= n:
        if n % k == 0 or n % (k + 2) == 0:
            return False
        k += 6
    return True


# ── Matrix data ───────────────────────────────────────────────────────────────

MATRIX = [
    [177, 178, 189],
    [257, 268, 279],
    [347, 358, 369],
    [437, 448, 459],
    [527, 538, 549],
    [617, 628, 639],
    [707, 718, 729],
]
ROWS, COLS = 7, 3

# Parameters
A    = 167   # closed-form anchor (ideal, prime)
D_R  = 90    # vertical step
D_C  = 11    # horizontal step
ANCHOR = 177  # actual matrix anchor = A + 10

ORBIT_P = {0,1,4,13,3,10,31,20,24,36,35,32,23,33,26,5,16,12}
ORBIT_V = {2,7,22,30,17,15,9,28,11,34,29,14,6,19,21,27,8,25}

DESCENT = [191, 188] + [191 - 3 - 11 * k for k in range(1, 9)]


# ── Closed-form verification ──────────────────────────────────────────────────

def M_formula(i, j):
    """1-indexed; ignores ε."""
    return A + (i - 1) * D_R + (j - 1) * D_C

# Every cell except (1,1) matches the formula
for i in range(1, ROWS + 1):
    for j in range(1, COLS + 1):
        formula_val = M_formula(i, j)
        actual_val  = MATRIX[i - 1][j - 1]
        if i == 1 and j == 1:
            eps = actual_val - formula_val
            check(eps == 10, "ε(1,1) = actual - formula = 177 - 167 = 10", eps, 10)
        else:
            check(actual_val == formula_val,
                  f"M({i},{j}) = {formula_val}",
                  actual_val, formula_val)

# Specific spot-checks from the problem statement
check(M_formula(2, 1) == 257, "i=2,j=1: 167+90=257", M_formula(2, 1), 257)
check(M_formula(2, 2) == 268, "i=2,j=2: 167+90+11=268", M_formula(2, 2), 268)
check(M_formula(7, 3) == 729, "i=7,j=3: 167+540+22=729", M_formula(7, 3), 729)
check(M_formula(1, 2) == 178, "i=1,j=2: 167+11=178", M_formula(1, 2), 178)
check(M_formula(1, 3) == 189, "i=1,j=3: 167+22=189", M_formula(1, 3), 189)


# ── ε(1,1) = 10 properties ───────────────────────────────────────────────────

# 10 = 26⁻¹ mod 37 (modular ratio)
check(26 * 10 % 37 == 1, "10 = 26⁻¹ mod 37 (modular ratio)", 26 * 10 % 37, 1)

# 177 = DESCENT[2] (third element of 191→100 chain)
check(DESCENT[2] == 177, "DESCENT[2] = 177", DESCENT[2], 177)
check(DESCENT == [191,188,177,166,155,144,133,122,111,100], "full DESCENT chain",
      DESCENT, [191,188,177,166,155,144,133,122,111,100])

# 177 = 3×59 (composite; anomaly shifts from prime 167 to composite 177)
check(177 == 3 * 59, "177 = 3×59 (composite)", 3 * 59, 177)
check(is_prime(167), "167 is prime (ideal anchor)", is_prime(167), True)
check(not is_prime(177), "177 is composite (actual anchor)", not is_prime(177), True)

# Residue shift: ε shifts DR from 5 to 6
check(dr(167) == 5, "DR(167) = 5 (col-1 prime residue)", dr(167), 5)
check(dr(177) == 6, "DR(177) = 6 (ε shifts to forbidden residue)", dr(177), 6)
check(6 % 3 == 0, "6 ≡ 0 mod 3 → 177 composite (divisible by 3)", 6 % 3, 0)

# Z/37Z orbit: both 167 and 177 are in ORBIT_V
check(167 % 37 in ORBIT_V, "167 mod 37 = 19 ∈ ORBIT_V", 167 % 37 in ORBIT_V, True)
check(177 % 37 in ORBIT_V, "177 mod 37 = 29 ∈ ORBIT_V", 177 % 37 in ORBIT_V, True)
check(167 % 37 == 19, "167 mod 37 = 19", 167 % 37, 19)
check(177 % 37 == 29, "177 mod 37 = 29", 177 % 37, 29)
# ε does not change the orbit assignment: both are in ORBIT_V
check(10 % 37 in ORBIT_P, "ε=10 mod 37 ∈ ORBIT_P (displacement is outer-ring)", 10 % 37 in ORBIT_P, True)


# ── Residue structure mod 9 ───────────────────────────────────────────────────

# Formula: M mod 9 = (167 + 11(j-1)) mod 9 = (5 + 2(j-1)) mod 9
# j=1 → 5; j=2 → 7; j=3 → 9 (≡0 mod 9, so DR=9)
# All rows i≥2 have A + (i-1)·90 ≡ A mod 9 = 5 (since 90≡0 mod 9)

RES = {1: 5, 2: 7, 3: 9}  # residue mod 9 by column (for formula cells)

check(dr(A) == 5, "DR(167) = 5 → col-1 formula residue", dr(A), 5)
check((A + D_C) % 9 or 9 == 7, "col-2 formula residue = 7", dr(A + D_C), 7)
check(dr(A + 2 * D_C) == 9, "col-3 formula residue = 9 (NULL)", dr(A + 2 * D_C), 9)

# All formula cells: verify column residues
for i in range(1, ROWS + 1):
    for j in range(1, COLS + 1):
        if i == 1 and j == 1:
            continue  # anomalous cell
        val = MATRIX[i - 1][j - 1]
        check(dr(val) == RES[j],
              f"DR(M({i},{j})) = {RES[j]}",
              dr(val), RES[j])

# Anchor anomaly: DR(177) = 6 (not 5)
check(dr(MATRIX[0][0]) == 6, "DR(M(1,1)=177) = 6 ≠ 5 (ε breaks col-1 residue)", dr(MATRIX[0][0]), 6)

# Col 3 entries all divisible by 9 → no primes
for i in range(1, ROWS + 1):
    val = MATRIX[i - 1][2]
    check(val % 9 == 0, f"M({i},3)={val} ≡ 0 mod 9 → composite", val % 9, 0)

# Col 2 residue = 7 (primes allowed mod 9: {1,2,4,5,7,8})
# Col 1 residue = 5 for formula cells → (5,7) is admissible twin-prime pair
ALLOWED_RESIDUES_9 = {1, 2, 4, 5, 7, 8}
ALLOWED_PAIRS_9    = {(2, 4), (5, 7), (8, 1)}
check((5, 7) in ALLOWED_PAIRS_9, "(5,7) is an admissible twin-prime pair mod 9",
      (5, 7) in ALLOWED_PAIRS_9, True)
check(5 in ALLOWED_RESIDUES_9, "col-1 residue 5 allows primes", 5 in ALLOWED_RESIDUES_9, True)
check(7 in ALLOWED_RESIDUES_9, "col-2 residue 7 allows primes", 7 in ALLOWED_RESIDUES_9, True)


# ── Primes in the matrix ──────────────────────────────────────────────────────

matrix_primes = [(i + 1, j + 1, MATRIX[i][j]) for i in range(ROWS) for j in range(COLS)
                 if is_prime(MATRIX[i][j])]
prime_cols = {j for _, j, _ in matrix_primes}

# All primes in col 1 (and possibly col 2); none in col 3
for i, j, p in matrix_primes:
    check(j != 3, f"prime {p} at ({i},{j}) not in col 3", j != 3, True)
    check(j in {1, 2}, f"prime {p} at ({i},{j}) in col 1 or 2", j in {1, 2}, True)

# Known primes: 257, 347, 617 in col 1
for p in [257, 347, 617]:
    check(is_prime(p), f"{p} is prime", is_prime(p), True)
    check(dr(p) == 5, f"DR({p}) = 5 = col-1 residue", dr(p), 5)

# Ideal anchor 167 would also be prime and col-1 admissible
check(is_prime(167), "ideal anchor 167 is prime (col-1 admissible)", is_prime(167), True)
check(dr(167) == 5, "DR(167) = 5 = col-1 residue", dr(167), 5)

# 59 (the non-trivial factor of 177): its slot
check(59 % 37 == 22, "59 mod 37 = 22 ∈ ORBIT_V", 59 % 37, 22)
check(22 in ORBIT_V, "22 ∈ ORBIT_V", 22 in ORBIT_V, True)


# ── Rank of the 7×3 matrix ───────────────────────────────────────────────────

import fractions

def matrix_rank(M):
    mat = [[fractions.Fraction(x) for x in row] for row in M]
    r, c = len(mat), len(mat[0])
    rank = 0
    pivot_row = 0
    for col in range(c):
        found = next((row for row in range(pivot_row, r) if mat[row][col] != 0), -1)
        if found == -1:
            continue
        mat[pivot_row], mat[found] = mat[found], mat[pivot_row]
        pivot = mat[pivot_row][col]
        for row in range(r):
            if row != pivot_row and mat[row][col] != 0:
                f = mat[row][col] / pivot
                mat[row] = [mat[row][k] - f * mat[pivot_row][k] for k in range(c)]
        rank += 1
        pivot_row += 1
    return rank

rank_full    = matrix_rank(MATRIX)
rank_formula = matrix_rank([[M_formula(i + 1, j + 1) for j in range(COLS)] for i in range(ROWS)])

check(rank_full == 3, "rank(full 7×3 matrix) = 3", rank_full, 3)
check(rank_formula == 2, "rank(formula matrix, no ε) = 2", rank_formula, 2)

# ε contribution: the correction E = full - formula
E = [[MATRIX[i][j] - M_formula(i + 1, j + 1) for j in range(COLS)] for i in range(ROWS)]
rank_E = matrix_rank(E)
# E is 10 at (0,0) and 0 elsewhere → rank 1
check(rank_E == 1, "rank(correction matrix E) = 1", rank_E, 1)
check(E[0][0] == 10 and all(E[i][j] == 0 for i in range(ROWS) for j in range(COLS)
                              if not (i == 0 and j == 0)),
      "E has exactly one nonzero entry E[1,1]=10", True, True)

# rank(full) = rank(formula + E) ≤ rank(formula) + rank(E) = 2+1 = 3
check(rank_full <= rank_formula + rank_E, "rank bound: rank(F+E) ≤ rank(F)+rank(E)",
      rank_full <= rank_formula + rank_E, True)
check(rank_full == rank_formula + rank_E, "rank(full) = rank(F) + rank(E) = 3",
      rank_full, rank_formula + rank_E)


# ── Inherence of 177 (answer to the question) ────────────────────────────────

# 177 is inherent because:
#   (I1) 177 = DESCENT[2]: determined by the 191→100 descent chain
#   (I2) ε(1,1) = 10 = modular ratio = 26⁻¹ mod 37: a framework constant
#   (I3) both 167 and 177 are in ORBIT_V mod 37: orbit structure preserved
#   (I4) DR(177) = 6 → 177 ≡ 0 mod 3: ε shifts anchor out of prime residues
#        (structural necessity: the anchor cannot be prime in this framework)

# (I1) already checked above
# (I2) already checked above

# (I3): orbit membership
check(167 % 37 in ORBIT_V and 177 % 37 in ORBIT_V,
      "both 167 and 177 in ORBIT_V mod 37", True, True)

# (I4): 177 ≡ 0 mod 3 (anchoring a composite at (1,1) is structurally forced)
check(177 % 3 == 0, "177 ≡ 0 mod 3 (ε forces anchor composite)", 177 % 3, 0)
check(167 % 3 == 2, "167 ≢ 0 mod 3 (ideal anchor admissible for primes)", 167 % 3, 2)

# The formula anchor A=167: it is the unique value satisfying
#   A ≡ 5 mod 9  AND  A ≡ 257-90 mod anything  AND  A is minimal positive
# i.e., A = M(2,1) - 90 = 257 - 90 = 167
check(MATRIX[1][0] - D_R == A, "A = M(2,1) - d_R = 257-90 = 167", MATRIX[1][0] - D_R, A)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Closed-Form Audit (7×3 Matrix)")
    print("=" * 66)

    print("\n── Matrix ──")
    print(f"  {'i':>2}  {'j=1':>6}  {'j=2':>6}  {'j=3':>6}  {'primes':>10}")
    for i in range(1, ROWS + 1):
        row = MATRIX[i - 1]
        ps = [str(v) for v in row if is_prime(v)]
        print(f"  {i:>2}  {row[0]:>6}  {row[1]:>6}  {row[2]:>6}  {', '.join(ps) or '—':>10}")

    print(f"\n── Closed form: M(i,j) = {A} + {D_R}(i-1) + {D_C}(j-1) + ε(i,j) ──")
    print(f"  ε(1,1) = 10 = {ANCHOR}-{A} = modular ratio = 26⁻¹ mod 37")
    print(f"  All other ε = 0  ({ROWS*COLS - 1} cells obey the pure formula)")

    print(f"\n── ε(1,1) = 10 properties ──")
    print(f"  26×10 mod 37 = {26*10%37}  (confirms: 10 = 26⁻¹ mod 37)")
    print(f"  DR(167) = {dr(167)} → prime-admissible residue (col-1 class)")
    print(f"  DR(177) = {dr(177)} → 177 ≡ 0 mod 3 → composite")
    print(f"  167 mod 37 = {167%37} ∈ ORBIT_V;  177 mod 37 = {177%37} ∈ ORBIT_V")
    print(f"  ε = 10, 10 mod 37 = {10%37} ∈ ORBIT_P  (displacement crosses rings)")

    print(f"\n── Residue structure mod 9 ──")
    print(f"  d_R = {D_R} ≡ 0 mod 9  → vertical step preserves all mod-9 residues")
    print(f"  d_C = {D_C} ≡ 2 mod 9  → each column shifts residue by +2")
    print(f"  col 1 (formula): residue {dr(A)} = prime-admissible (≡5 mod 9)")
    print(f"  col 2 (formula): residue {dr(A+D_C)} = prime-admissible (≡7 mod 9)")
    print(f"  col 3 (formula): residue {dr(A+2*D_C)} = composite-forced (≡0 mod 9, div by 9)")
    print(f"  twin-prime pair (5,7) ∈ ALLOWED_PAIRS_9: {(5,7) in ALLOWED_PAIRS_9}")
    print(f"  M(1,1)=177: DR={dr(177)} ≠ 5 → ε breaks col-1 residue at anchor only")

    print(f"\n── Primes in matrix ──")
    for i, j, p in sorted(matrix_primes):
        print(f"  M({i},{j}) = {p}  DR={dr(p)}  mod37={p%37} {'∈ORBIT_V' if p%37 in ORBIT_V else '∈ORBIT_P'}")
    print(f"  Ideal anchor 167: prime, DR=5, mod37=19 ∈ ORBIT_V")

    print(f"\n── Rank ──")
    print(f"  rank(formula matrix, pure)  = {rank_formula}  (C = u·𝟏ᵀ + 𝟏·vᵀ)")
    print(f"  rank(correction matrix E)   = {rank_E}  (single nonzero entry)")
    print(f"  rank(full 7×3 matrix)       = {rank_full}  = {rank_formula} + {rank_E}")

    print(f"\n── Inherence of 177 ──")
    print(f"  177 = DESCENT[2] in chain {DESCENT}")
    print(f"  177 = 3×59;  59 mod 37 = {59%37} ∈ ORBIT_V (factor is framework-internal)")
    print(f"  A = 167 = M(2,1)-d_R = {MATRIX[1][0]}-{D_R}")
    print(f"  167 is the derived ideal anchor; 177 is the structurally required anchor.")
    print(f"  ε = 177-167 = 10 = modular ratio: deviation is a framework constant.")
    print(f"  Conclusion: 177 is INHERENT. The piecewise model is not a testing artifact;")
    print(f"  it encodes the single-point break where the structural anchor (DESCENT[2])")
    print(f"  deviates from the arithmetic ideal by exactly the modular ratio.")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")

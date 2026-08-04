"""
Matrix Configurations A and B: Linear Algebra over GF(37)

M_A = [[5, 9, 7],   M_B = [[5, 9, 7],
        [4, 8, 6],           [4, 8, 6],
        [3, 1, 2]]           [3, 4, 2]]

M_B = M_A + 3·e₃·e₂ᵀ  (rank-one perturbation at entry (3,2))

Null space:
  ker(M_A) = span{(1, 1, -2)ᵀ}  enforces c₁ + c₂ = 2c₃ on every row:
    5 + 9 = 2(7) = 14
    4 + 8 = 2(6) = 12
    3 + 1 = 2(2) = 4

Determinants:
  det(M_A) = 0              rank 2
  det(M_B) = 3 × C_{3,2}(M_A) = 3 × (-2) = -6

Permanents:
  perm(M_A) = 540
  perm(M_B) = 714
  Δperm     = 174

GF(37) connections:
  111 = V(r₁) - V(r₂) = 3 × 37       invariant under any row-3 perturbation
  174 mod 37 = 26                      Δperm lands on the 137-map multiplier
  perm(M_B) mod 37 = 11 ∈ ORBIT_11    {11, 27, 36}

Entry-class map — M_A contains all nine non-zero digits {1,...,9}:
  1 ∈ IC      orbit (1, 26, 10)
  2 ∈ PR37    orbit (2, 15, 20)   primitive root
  3 ∈ ST      orbit (3, 4, 30)    sovereign target
  4 ∈ SA      orbit (4, 30, 3)    sovereign anchor
  5 ∈ PR37    orbit (5, 19, 13)   primitive root
  6 → orbit(8)[2] = DR(7+8)       connects to Theorem 120
  7 ∈ D7      orbit (7, 34, 33)
  8 ∈ CB      orbit (8, 23, 6)    cascade base
  9 ∈ SA      orbit (9, 12, 16)   sovereign anchor

Cyclic row permutations preserve ker(M) and rank(M); trace varies across S₃ orbit.
"""

import itertools

P = 37

MA = [[5, 9, 7], [4, 8, 6], [3, 1, 2]]
MB = [[5, 9, 7], [4, 8, 6], [3, 4, 2]]


def det3(M):
    a, b, c = M[0]; d, e, f = M[1]; g, h, i = M[2]
    return a * (e*i - f*h) - b * (d*i - f*g) + c * (d*h - e*g)


def perm3(M):
    return sum(
        M[0][s[0]] * M[1][s[1]] * M[2][s[2]]
        for s in itertools.permutations([0, 1, 2])
    )


def cofactor(M, r, c):
    minor = [[M[i][j] for j in range(3) if j != c] for i in range(3) if i != r]
    return ((-1) ** (r + c)) * (minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0])


def orbit137(n):
    x, path = n % P, []
    for _ in range(3):
        path.append(x); x = (26 * x) % P
    return tuple(path)


def primitive_root_37(g):
    return all(pow(g, 36 // q, P) != 1 for q in [2, 3])


IC = frozenset({1, 10, 26})
SA = frozenset({4, 9, 25, 30})
ST = frozenset({3, 12, 21})
CB = frozenset({8, 13, 24})
ORBIT_11 = frozenset({11, 27, 36})
D7 = frozenset({7, 33, 34})
PR37 = frozenset(g for g in range(2, P) if primitive_root_37(g))


def run_assertions():
    # Determinants
    assert det3(MA) == 0,  f"det(M_A) = {det3(MA)}"
    assert det3(MB) == -6, f"det(M_B) = {det3(MB)}"

    # Null space
    v = [1, 1, -2]
    for row in MA:
        assert sum(row[j] * v[j] for j in range(3)) == 0

    # Cofactor and determinant lemma
    c32 = cofactor(MA, 2, 1)
    assert c32 == -2,              f"C_{{3,2}} = {c32}"
    assert 3 * c32 == det3(MB),   f"3 × C_{{3,2}} ≠ det(M_B)"

    # Row null-space condition
    for row in MA:
        assert row[0] + row[1] == 2 * row[2]

    # Permanents
    pA, pB = perm3(MA), perm3(MB)
    assert pA == 540, f"perm(M_A) = {pA}"
    assert pB == 714, f"perm(M_B) = {pB}"
    dperm = pB - pA
    assert dperm == 174, f"Δperm = {dperm}"

    # GF(37) permanent connection
    assert dperm % P == 26, f"Δperm mod 37 = {dperm % P}  (expected 26 = 137-map multiplier)"
    assert pB % P == 11,    f"perm(M_B) mod 37 = {pB % P}  (expected 11 ∈ ORBIT_11)"
    assert 11 in ORBIT_11

    # 111 invariant
    V = lambda row: 100 * row[0] + 10 * row[1] + row[2]
    diff = V(MA[0]) - V(MA[1])
    assert diff == 111,      f"V(r1)-V(r2) = {diff}"
    assert diff == 3 * P,    f"111 ≠ 3 × 37"
    assert V(MB[0]) - V(MB[1]) == 111  # invariant: row 3 perturbation doesn't affect it

    # M_A contains exactly {1,...,9}
    entries = sorted(e for row in MA for e in row)
    assert entries == list(range(1, 10)), f"entries = {entries}"

    # Entry-class map
    assert 1 in IC
    assert 2 in PR37
    assert 3 in ST
    assert 4 in SA
    assert 5 in PR37
    assert orbit137(8)[2] == 6   # 6 = orbit(8)[2]
    assert 7 in D7
    assert 8 in CB
    assert 9 in SA

    # Cyclic row permutation preserves ker and rank (singular iff det = 0)
    for perm in itertools.permutations([0, 1, 2]):
        MP = [MA[i] for i in perm]
        assert det3(MP) == 0  # still singular

    print("All assertions passed.")


def summarise():
    pA, pB = perm3(MA), perm3(MB)
    print("=" * 56)
    print("Matrix Configurations A and B over GF(37)")
    print("=" * 56)
    print(f"  det(M_A) = 0     rank 2     ker = span{{(1,1,-2)ᵀ}}")
    print(f"  det(M_B) = {det3(MB)}    3 × C_{{3,2}}(M_A) = 3 × (-2)")
    print(f"  perm(M_A) = {pA}   perm(M_B) = {pB}   Δ = {pB-pA}")
    print(f"  Δperm mod 37 = {(pB-pA) % P}  (137-map multiplier)")
    print(f"  perm(M_B) mod 37 = {pB % P}  ∈ ORBIT_11")
    print(f"  V(r1) - V(r2) = 111 = 3 × 37  (invariant)")


if __name__ == "__main__":
    run_assertions()
    summarise()

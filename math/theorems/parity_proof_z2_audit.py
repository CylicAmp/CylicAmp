# math/theorems/parity_proof_z2_audit.py
"""
Refined Parity Proof — σ_p vs σ_a on Mat_3(Z₂)
================================================
σ_p(i,j) = (2-i, 2-j)  — 180° point reflection
σ_a(i,j) = (i,   2-j)  — vertical axial flip

Three distinct cases:

  1. Constant matrix M=1: fixed by EVERY permutation → σ_p(M)=σ_a(M)=M.
     Collapse is an artifact of the matrix being a fixed point of the full
     symmetric group, not a property of the pair (σ_p, σ_a).

  2. X-pattern N (sequential-parity / Z₂ checkerboard [[1,0,1],[0,1,0],[1,0,1]]):
     Fixed by σ_p because N is centrosymmetric.
     Fixed by σ_a because every row of N is a palindrome.
     Both operations fix N for INDEPENDENT structural reasons.
     σ_p = σ_a is still false as transformations — N just happens to satisfy both.

  3. Generic Z₂ counterexample: a matrix fixed by neither, showing σ_p ≠ σ_a
     as distinct elements of the dihedral action on Mat_3(Z₂).
"""


def sigma_p(M: list) -> list:
    n = len(M)
    return [[M[n - 1 - i][n - 1 - j] for j in range(n)] for i in range(n)]


def sigma_a(M: list) -> list:
    n = len(M)
    return [[M[i][n - 1 - j] for j in range(n)] for i in range(n)]


def parity_grid(seq_matrix: list) -> list:
    return [[v % 2 for v in row] for row in seq_matrix]


def verify():
    print("Refined Parity Proof — σ_p vs σ_a on Mat_3(Z₂)\n")

    # ── 1. Constant matrix ────────────────────────────────────────────────────
    M1 = [[1, 1, 1],
          [1, 1, 1],
          [1, 1, 1]]

    sp1 = sigma_p(M1)
    sa1 = sigma_a(M1)

    assert sp1 == M1 and sa1 == M1   # both fix it
    assert sp1 == sa1                # images coincide

    print("1. Constant matrix M = 1 (all entries 1)")
    print(f"   σ_p(M) = σ_a(M) = M  ✓")
    print(f"   M is fixed by the full symmetric group on 9 positions.")
    print(f"   Collapse is trivial — artifact of M being a global fixed point.")

    # ── 2. X-pattern N (the sequential parity grid) ───────────────────────────
    # N[i][j] = (i+j+1) mod 2  ≡  parity of (3i+j+1)
    N = [[1, 0, 1],
         [0, 1, 0],
         [1, 0, 1]]

    # Confirm N is the parity image of the sequential 1-9 matrix
    seq = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert parity_grid(seq) == N

    spN = sigma_p(N)
    saN = sigma_a(N)

    assert spN == N   # centrosymmetry: N[i][j] = N[2-i][2-j]
    assert saN == N   # row-palindrome: N[i][j] = N[i][2-j]

    # Verify centrosymmetry explicitly: (i+j+1)%2 == (2-i+2-j+1)%2
    for i in range(3):
        for j in range(3):
            assert N[i][j] == N[2 - i][2 - j], "centrosymmetry broken"
            assert N[i][j] == N[i][2 - j],     "row-palindrome broken"

    # But σ_p ≠ σ_a as maps — they merely agree on this particular input
    print("\n2. X-pattern N = [[1,0,1],[0,1,0],[1,0,1]]  (sequential parity grid)")
    print(f"   σ_p(N) = N  ✓  because N is centrosymmetric")
    print(f"   σ_a(N) = N  ✓  because every row of N is a palindrome")
    print(f"   Both fix N for INDEPENDENT structural reasons.")
    print(f"   Agreement on this matrix does NOT imply σ_p = σ_a as transformations.")

    # ── 3. Generic Z₂ counterexample: σ_p(M) ≠ σ_a(M) ───────────────────────
    # Take M with a single 1 in the top-left corner
    M2 = [[1, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]

    sp2 = sigma_p(M2)   # 1 rotates to bottom-right
    sa2 = sigma_a(M2)   # 1 flips to top-right

    expected_sp2 = [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 1]]

    expected_sa2 = [[0, 0, 1],
                    [0, 0, 0],
                    [0, 0, 0]]

    assert sp2 == expected_sp2
    assert sa2 == expected_sa2
    assert sp2 != sa2   # σ_p and σ_a are distinct on this input

    print("\n3. Generic Z₂ counterexample: M = e_{00}  (1 at top-left only)")
    print(f"   σ_p(M): 1 maps to position (2,2)  →  bottom-right")
    print(f"   σ_a(M): 1 maps to position (0,2)  →  top-right")
    print(f"   σ_p(M) ≠ σ_a(M)  ✓  — distinct transformations on Mat_3(Z₂)")

    # ── 4. Formal scope statement ─────────────────────────────────────────────
    print("\n4. Precise scope of 'symmetry collapse'")
    print("   σ_p(M) = σ_a(M) = M  holds for:")
    print("     (a) M = 1 (all-1s): fixed by every map → trivial")
    print("     (b) M = N (X-pattern): fixed by each for independent reasons")
    print("     (c) Any M simultaneously centrosymmetric AND row-palindromic")
    print("   σ_p ≠ σ_a as elements of the symmetry group of Mat_3(Z₂).")
    print("   The pair coincides only on the intersection of their fixed-point sets.")

    # Verify: the intersection of Fix(σ_p) and Fix(σ_a) in Z₂^{3×3}
    # Fix(σ_p): centrosymmetric matrices; Fix(σ_a): row-palindromic matrices
    # Count centrosymmetric Z₂ 3×3 matrices: free entries are 5 → 2^5 = 32
    # Count row-palindromic: each row [a,b,a] → 2^2=4 choices/row → 4^3=64
    # Intersection: both centrosymmetric AND row-palindromic
    count_intersection = 0
    for bits in range(2 ** 9):
        M = [[(bits >> (3 * i + j)) & 1 for j in range(3)] for i in range(3)]
        if sigma_p(M) == M and sigma_a(M) == M:
            count_intersection += 1
    # These are matrices with M[i][j]=M[2-i][2-j] AND M[i][j]=M[i][2-j]
    # Free entries: (0,0),(0,1),(1,0),(1,1) → 4 free → 2^4=16
    assert count_intersection == 16

    print(f"\n   |Fix(σ_p) ∩ Fix(σ_a)| in Z₂^{{3×3}} = {count_intersection}  (2^4 free entries)")
    print(f"   M=1 and N are two of these 16 matrices.")
    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()

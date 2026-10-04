# math/theorems/dim6_kernel_role_audit.py
"""
Dimension-Six Kernel Role — Rigorous Audit
==========================================
Audits the claim that Fix(φ) ⊂ Mat_3(F_2), where φ = σ_p ∘ σ_a^{-1},
is the maximal linear subspace on which σ_p and σ_a agree.

Definitions recalled:
  σ_p(M)[i][j] = M[2-i][2-j]  (180° point reflection / central inversion)
  σ_a(M)[i][j] = M[i][2-j]    (vertical axial flip)
  φ             = σ_p ∘ σ_a^{-1}

Key algebraic facts established here:
  (A) σ_a is an involution: σ_a ∘ σ_a = id  →  σ_a^{-1} = σ_a
  (B) φ = σ_p ∘ σ_a  (i.e., σ_pa, the third non-identity Klein element)
  (C) φ(M)[i][j] = M[2-i][j]  (row-swap: rows 0 ↔ 2)
  (D) Fix(φ) = {M : row 0 = row 2}  — 64 matrices, dim 6
  (E) {M : σ_p(M) = σ_a(M)} = {M : row 0 = row 2} = Fix(φ)
      → these are NOT two different sets; both conditions reduce identically.
  (F) Fix(φ) is a linear subspace (kernel of σ_p + σ_a over F_2)
  (G) Fix(φ) is the UNIQUE MAXIMAL subspace on which σ_p = σ_a
  (H) All-1s matrix ∈ Fix(φ); spans a 1-dimensional ray inside it
  (I) Fix(σ_p) ∩ Fix(σ_a) ⊊ Fix(φ)  (16 ⊊ 64: strictly smaller)

Flagged as unverifiable (definition of 'MWS Sovereign Kernel K' not provided):
  — "symmetry anchor" role inside K
  — "constant component stabilizer" inside K
  — "Law-of-12 closure" connection to Fix(φ)
  — "reduces modulo parity" (not formally defined)
"""


def sigma_p(M: list) -> list:
    n = len(M)
    return [[M[n - 1 - i][n - 1 - j] for j in range(n)] for i in range(n)]


def sigma_a(M: list) -> list:
    n = len(M)
    return [[M[i][n - 1 - j] for j in range(n)] for i in range(n)]


def phi(M: list) -> list:
    """φ = σ_p ∘ σ_a^{-1} = σ_p ∘ σ_a (since σ_a is involutory)."""
    return sigma_p(sigma_a(M))


def mat_add_f2(A: list, B: list) -> list:
    """Componentwise XOR (addition in F_2)."""
    return [[(A[i][j] + B[i][j]) % 2 for j in range(3)] for i in range(3)]


def all_3x3_f2():
    for bits in range(512):
        yield [[(bits >> (3 * i + j)) & 1 for j in range(3)] for i in range(3)]


def verify():
    print("Dimension-Six Kernel Role — Rigorous Audit\n")

    # ── (A) σ_a is an involution ───────────────────────────────────────────────
    print("(A) σ_a is an involution: σ_a ∘ σ_a = id")
    for M in all_3x3_f2():
        assert sigma_a(sigma_a(M)) == M, "σ_a² ≠ id"
    print("  σ_a(σ_a(M)) = M  for all 512 matrices  ✓")
    print("  Therefore σ_a^{-1} = σ_a  ✓")

    # σ_p also an involution (recorded for completeness)
    for M in all_3x3_f2():
        assert sigma_p(sigma_p(M)) == M, "σ_p² ≠ id"
    print("  σ_p(σ_p(M)) = M  for all 512 matrices  ✓  (both generators are involutions)")

    # ── (B) φ = σ_p ∘ σ_a^{-1} = σ_p ∘ σ_a ──────────────────────────────────
    print("\n(B) φ = σ_p ∘ σ_a^{-1} = σ_p ∘ σ_a")
    for M in all_3x3_f2():
        assert phi(M) == sigma_p(sigma_a(M)), "φ definition mismatch"
    print("  Confirmed: φ(M) = σ_p(σ_a(M))  for all 512 matrices  ✓")
    # φ is itself an involution
    for M in all_3x3_f2():
        assert phi(phi(M)) == M, "φ² ≠ id"
    print("  φ is also an involution: φ ∘ φ = id  ✓")

    # ── (C) Explicit action of φ ───────────────────────────────────────────────
    print("\n(C) φ(M)[i][j] = M[2-i][j]  (row-swap: row 0 ↔ row 2)")
    for M in all_3x3_f2():
        pM = phi(M)
        for i in range(3):
            for j in range(3):
                assert pM[i][j] == M[2 - i][j], f"Row-swap formula failed at ({i},{j})"
    print("  φ(M)[i][j] = M[2-i][j]  verified for all 512 matrices  ✓")
    print("  Derivation: φ(M)[i][j] = σ_p(σ_a(M))[i][j]")
    print("            = σ_a(M)[2-i][2-j]  = M[2-i][2-(2-j)]  = M[2-i][j]  ✓")

    # ── (D) Fix(φ) = {M : row 0 = row 2}, size 64, dim 6 ────────────────────
    print("\n(D) Fix(φ) = {M ∈ Mat_3(F_2) : φ(M) = M}")
    fix_phi = [M for M in all_3x3_f2() if phi(M) == M]
    assert len(fix_phi) == 64
    # Characterisation: row 0 = row 2
    for M in fix_phi:
        assert M[0] == M[2], "Fix(φ) matrix does not satisfy row0=row2"
    # Converse
    for M in all_3x3_f2():
        if M[0] == M[2]:
            assert phi(M) == M, "row0=row2 should imply φ(M)=M"
    print(f"  |Fix(φ)| = {len(fix_phi)}  ✓")
    print(f"  Fix(φ) = {{M : row 0 = row 2}} verified (both directions)  ✓")
    print(f"  Free parameters: row 0 (3 bits) + row 1 (3 bits) = 6 → 2^6 = 64  ✓")
    print(f"  dim Fix(φ) = 6  ✓")

    # ── (E) {M : σ_p(M) = σ_a(M)} = Fix(φ) ──────────────────────────────────
    print("\n(E) {M : σ_p(M) = σ_a(M)} = Fix(φ)  (same set, not just same size)")
    agree_set = [M for M in all_3x3_f2() if sigma_p(M) == sigma_a(M)]
    assert len(agree_set) == 64
    # Verify exact equality as sets
    fix_phi_keys  = {tuple(tuple(r) for r in M) for M in fix_phi}
    agree_keys    = {tuple(tuple(r) for r in M) for M in agree_set}
    assert fix_phi_keys == agree_keys, "Fix(φ) ≠ {M:σ_p(M)=σ_a(M)} as sets"
    print(f"  {{M:σ_p(M)=σ_a(M)}} has {len(agree_set)} elements")
    print(f"  Identical to Fix(φ) as sets  ✓")
    print(f"  Algebraic reason: σ_p(M)=σ_a(M) ↔ M[2-i][2-j]=M[i][2-j]")
    print(f"    ↔ M[2-i][k]=M[i][k] (k=2-j)  ↔  row 0 = row 2  = Fix(φ)  ✓")

    # ── (F) Fix(φ) is a linear subspace over F_2 ──────────────────────────────
    print("\n(F) Fix(φ) is a linear subspace of Mat_3(F_2)")
    zero = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert zero in fix_phi or any(M == zero for M in fix_phi), "0 ∉ Fix(φ)"
    # Closure under addition (XOR)
    violations = 0
    for M in fix_phi:
        for N in fix_phi:
            S = mat_add_f2(M, N)
            if not any(S == X for X in fix_phi):
                violations += 1
    assert violations == 0
    print(f"  Zero matrix ∈ Fix(φ)  ✓")
    print(f"  Closed under F_2 addition: {violations} violations  ✓")
    print(f"  Fix(φ) = ker(σ_p + σ_a) over F_2  (kernel of a linear map → subspace)  ✓")

    # ── (G) Fix(φ) is the UNIQUE MAXIMAL subspace where σ_p = σ_a ─────────────
    print("\n(G) Fix(φ) is the unique maximal linear subspace on which σ_p = σ_a")
    # Any M where σ_p(M) = σ_a(M) is already IN Fix(φ) (shown in E).
    # So no linear subspace outside Fix(φ) can satisfy σ_p = σ_a.
    # Equivalently: if V is any set where σ_p|_V = σ_a|_V, then V ⊆ Fix(φ).
    for M in all_3x3_f2():
        agrees = (sigma_p(M) == sigma_a(M))
        in_fix = any(M == X for X in fix_phi)
        assert agrees == in_fix, "Membership mismatch"
    print(f"  Verified: σ_p(M)=σ_a(M) ↔ M ∈ Fix(φ) for all 512 matrices  ✓")
    print(f"  Corollary: any V with σ_p|_V = σ_a|_V satisfies V ⊆ Fix(φ)")
    print(f"  Fix(φ) is the UNIQUE maximal such subspace  ✓")

    # ── (H) All-1s matrix ─────────────────────────────────────────────────────
    print("\n(H) The all-1s matrix and its role in Fix(φ)")
    ones = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    assert any(M == ones for M in fix_phi), "All-1s ∉ Fix(φ)"
    assert sigma_p(ones) == ones    # fixed by σ_p
    assert sigma_a(ones) == ones    # fixed by σ_a
    assert phi(ones) == ones        # fixed by φ
    print(f"  All-1s ∈ Fix(φ)  ✓")
    print(f"  All-1s is fixed by σ_p, σ_a, and φ individually  ✓")
    # Span{all-1s} is 1-dimensional over F_2
    span_ones = [ones, zero]        # {0, 1} in the vector space
    print(f"  span{{all-1s}} = {{0,1}} inside Fix(φ): 1-dimensional ray  ✓")
    # But all-1s is NOT the ONLY element of Fix(φ) — Fix(φ) has 64 elements
    assert len(fix_phi) == 64
    print(f"  |Fix(φ)| = 64: the ray span{{all-1s}} (dim 1) is a proper subspace of Fix(φ) (dim 6)  ✓")

    # ── (I) Fix(σ_p) ∩ Fix(σ_a) ⊊ Fix(φ) ────────────────────────────────────
    print("\n(I) Strict containment: Fix(σ_p) ∩ Fix(σ_a) ⊊ Fix(φ)")
    fix_p  = [M for M in all_3x3_f2() if sigma_p(M) == M]
    fix_a  = [M for M in all_3x3_f2() if sigma_a(M) == M]
    fix_p_keys = {tuple(tuple(r) for r in M) for M in fix_p}
    fix_a_keys = {tuple(tuple(r) for r in M) for M in fix_a}
    intersection = fix_p_keys & fix_a_keys
    assert len(fix_p)  == 32
    assert len(fix_a)  == 64
    assert len(intersection) == 16
    # Every element of the intersection is in Fix(φ)
    for key in intersection:
        assert key in fix_phi_keys, "Fix(σ_p)∩Fix(σ_a) not contained in Fix(φ)"
    # But Fix(φ) is larger
    assert len(intersection) < len(fix_phi)
    print(f"  |Fix(σ_p)|          = {len(fix_p)}")
    print(f"  |Fix(σ_a)|          = {len(fix_a)}")
    print(f"  |Fix(σ_p) ∩ Fix(σ_a)| = {len(intersection)}  (both fixed individually)")
    print(f"  |Fix(φ)|             = {len(fix_phi_keys)}  (σ_p and σ_a merely agree)")
    print(f"  Fix(σ_p) ∩ Fix(σ_a) ⊆ Fix(φ): verified  ✓")
    print(f"  Strict: {len(intersection)} < {len(fix_phi_keys)}  ✓")
    print(f"  Key distinction: Fix(φ) requires σ_p(M)=σ_a(M), NOT σ_p(M)=M AND σ_a(M)=M")

    # ── Correction: misleading language in exposition ─────────────────────────
    print("\n--- Precision note ---")
    print("The exposition says Fix(φ) is 'fixed by the composition of the reflection")
    print("generators.' This is ambiguous. Clarification:")
    print("  Fix(φ) = {M : φ(M) = M} where φ = σ_p ∘ σ_a.")
    print("  Elements of Fix(φ) are NOT simultaneously fixed by σ_p and σ_a;")
    print(f"  only {len(intersection)} of the 64 are fixed by both individually.")
    print("  Fix(φ) is the set where σ_p and σ_a produce the SAME OUTPUT,")
    print("  not where each produces the INPUT back.")

    # ── Flagged claims (unauditable without formal definition of K) ─────────────
    print("\n--- Unauditable claims (require formal definition of K) ---")
    print("  1. 'Symmetry anchor inside MWS Sovereign Kernel K'")
    print("     → K is not defined in this codebase. Cannot audit.")
    print("  2. 'Constant component stabilizer: constant direction of K")
    print("      mapped isomorphically onto 1-dimensional ray'")
    print("     → 'Isomorphically mapped' is imprecise without specifying the map.")
    print("     → Auditable part: all-1s ∈ Fix(φ) ✓; span is 1-dimensional ✓.")
    print("  3. 'Law-of-12 closure enforced by this 6-dimensional direction'")
    print("     → No established link between Fix(φ) and Law-of-12 DR sequences.")
    print("  4. 'Reduces modulo parity must land inside this subspace'")
    print("     → 'Reduces modulo parity' not formally defined.")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n--- Audit summary ---")
    print("  VERIFIED:")
    print("    σ_a^{-1} = σ_a (involution)  ✓")
    print("    φ = σ_p ∘ σ_a; φ(M)[i][j] = M[2-i][j]  ✓")
    print("    Fix(φ) = {M:σ_p(M)=σ_a(M)} = {M:row0=row2}: size 64, dim 6  ✓")
    print("    Fix(φ) is a linear subspace (kernel of σ_p+σ_a)  ✓")
    print("    Fix(φ) is the unique maximal subspace where σ_p=σ_a  ✓")
    print("    All-1s ∈ Fix(φ), spanning a 1-dimensional ray  ✓")
    print("    Fix(σ_p) ∩ Fix(σ_a) ⊊ Fix(φ)  (16 ⊊ 64)  ✓")
    print("  UNVERIFIABLE: claims requiring definition of K")
    print("  IMPRECISE: 'fixed by the composition' should read 'φ(M)=M'")

    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()

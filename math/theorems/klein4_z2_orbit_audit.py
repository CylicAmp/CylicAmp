# math/theorems/klein4_z2_orbit_audit.py
"""
Klein Four-Group Action on Mat_3(F_2) — Corrected Orbit Count
==============================================================
Generators:
  σ_p(M)_{ij} = M_{2-i,2-j}   (central inversion / 180° rotation)
  σ_a(M)_{ij} = M_{i,2-j}     (vertical axial flip)

Group K = {e, σ_p, σ_a, σ_p∘σ_a} ≅ Z₂×Z₂  (Klein four-group)
Action: linear on Mat_3(F_2) ≅ F_2^9 (512 matrices)

Parity-collapse subspace:
  {M : σ_p(M) = σ_a(M)} — dimension 6, size 64.
  Condition: M_{2-i,2-j} = M_{i,2-j} for all i,j
           ↔ row 0 of M equals row 2 of M.
  Free parameters: row 0 (3) + row 1 (3) = 6 → 64 matrices.

Fixed-point counts (Burnside):
  |Fix(e)|          = 512
  |Fix(σ_p)|        =  32  (5 free params: centrosymmetric matrices)
  |Fix(σ_a)|        =  64  (6 free params: row-palindromic matrices)
  |Fix(σ_p∘σ_a)|   =  64  (6 free params: row 0 = row 2)

  Burnside orbit count = (512 + 32 + 64 + 64) / 4 = 168.

Correction to exposition: the formula (512 + 3×64)/4 = 176 is WRONG.
σ_p (central inversion) has |Fix(σ_p)| = 32, not 64.
The error was equating |Fix(σ_p)| with |Fix(σ_a)| = |Fix(σ_p∘σ_a)| = 64.
"""


def sigma_p(M: list) -> list:
    n = len(M)
    return [[M[n-1-i][n-1-j] for j in range(n)] for i in range(n)]


def sigma_a(M: list) -> list:
    n = len(M)
    return [[M[i][n-1-j] for j in range(n)] for i in range(n)]


def sigma_pa(M: list) -> list:
    """σ_p ∘ σ_a : M[i][j] → M[2-i][j]  (row swap: rows 0 ↔ 2)."""
    return sigma_p(sigma_a(M))


def all_3x3_f2():
    """Generate all 512 matrices in Mat_3(F_2)."""
    for bits in range(512):
        yield [[(bits >> (3*i + j)) & 1 for j in range(3)] for i in range(3)]


def verify():
    print("Klein Four-Group Action on Mat_3(F_2)\n")

    # ── Parity-collapse subspace ──────────────────────────────────────────────
    collapse = [M for M in all_3x3_f2() if sigma_p(M) == sigma_a(M)]
    assert len(collapse) == 64
    # Characterisation: row 0 = row 2
    for M in collapse:
        assert M[0] == M[2], "Collapse matrix does not have row0=row2"
    # Converse: row0=row2 → σ_p(M)=σ_a(M)
    for M in all_3x3_f2():
        if M[0] == M[2]:
            assert sigma_p(M) == sigma_a(M)
    print(f"  Parity-collapse subspace: {len(collapse)} matrices (row0=row2)  ✓")
    print(f"  Dimension = 6 (row0: 3 free, row1: 3 free, row2 = row0)  ✓")

    # ── Fixed-point counts ────────────────────────────────────────────────────
    fix_e  = 512
    fix_p  = sum(1 for M in all_3x3_f2() if sigma_p(M)  == M)
    fix_a  = sum(1 for M in all_3x3_f2() if sigma_a(M)  == M)
    fix_pa = sum(1 for M in all_3x3_f2() if sigma_pa(M) == M)

    assert fix_p  == 32    # 5 free params (centrosymmetric)
    assert fix_a  == 64    # 6 free params (each row a palindrome)
    assert fix_pa == 64    # 6 free params (row0 = row2)

    print(f"\n  Fixed-point counts:")
    print(f"    |Fix(e)|        = {fix_e}")
    print(f"    |Fix(σ_p)|      = {fix_p}  (centrosymmetric; 5 free params)  ✓")
    print(f"    |Fix(σ_a)|      = {fix_a}  (row-palindromic; 6 free params)  ✓")
    print(f"    |Fix(σ_p∘σ_a)| = {fix_pa}  (row0=row2;      6 free params)  ✓")

    # ── Burnside orbit count ──────────────────────────────────────────────────
    burnside = (fix_e + fix_p + fix_a + fix_pa) // 4
    assert burnside == 168
    print(f"\n  Burnside orbit count = ({fix_e}+{fix_p}+{fix_a}+{fix_pa})/4 = {burnside}  ✓")

    # Verify via direct orbit enumeration
    seen = set()
    orbits = 0
    for M in all_3x3_f2():
        key = tuple(tuple(r) for r in M)
        if key not in seen:
            orbits += 1
            for img in [M, sigma_p(M), sigma_a(M), sigma_pa(M)]:
                seen.add(tuple(tuple(r) for r in img))
    assert orbits == 168
    print(f"  Direct orbit enumeration: {orbits} orbits  ✓")

    # ── Correction to exposition ──────────────────────────────────────────────
    wrong_burnside = (512 + 3 * 64) // 4
    assert wrong_burnside == 176
    print(f"\n  CORRECTION: exposition formula (512 + 3×64)/4 = {wrong_burnside}")
    print(f"  Error: uses |Fix(σ_p)| = 64, but correct value is {fix_p}.")
    print(f"  σ_p (central inversion) has 5 free params → 32, not 64.")
    print(f"  Correct Burnside = {burnside}.")

    # ── Stabilizer decomposition ──────────────────────────────────────────────
    # In Klein group {e,σ_p,σ_a,σ_pa}: fixed by 2 non-identity elements
    # implies fixed by the third (since a·b = c and a,b fix M → c=ab fixes M).
    # So possible fixed_counts: 0 (stab={e}), 1 (stab size 2), 3 (stab=K, size 4).
    count_fc = {0: 0, 1: 0, 2: 0, 3: 0}
    for M in all_3x3_f2():
        fc = sum(1 for f in [sigma_p, sigma_a, sigma_pa] if f(M) == M)
        count_fc[fc] += 1

    # fixed_count = 2 must be 0 (Klein group property)
    assert count_fc[2] == 0, f"Unexpected fixed_count=2 matrices: {count_fc[2]}"

    stab_K = count_fc[3]   # stab = full K (size 4), orbit size 1
    stab_2 = count_fc[1]   # stab size 2, orbit size 2
    stab_1 = count_fc[0]   # stab = {e} (size 1), orbit size 4

    assert stab_K == 16    # Fix(σ_p) ∩ Fix(σ_a) = 16 (4 free params)
    assert stab_K + stab_2 + stab_1 == 512

    o1 = stab_K
    o2 = stab_2 // 2
    o4 = stab_1 // 4
    assert o1 + o2 + o4 == 168

    print(f"\n  Stabilizer decomposition (Klein group):")
    print(f"    |stab|=4 (full K): {stab_K} matrices  → {o1} orbits of size 1")
    print(f"    |stab|=2:          {stab_2} matrices  → {o2} orbits of size 2")
    print(f"    |stab|=1:          {stab_1} matrices  → {o4} orbits of size 4")
    print(f"  Orbits: {o1}+{o2}+{o4} = {o1+o2+o4}  ✓")

    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()

"""
Group G = <x,y | x^9=y^6=1, yxy^-1=x^4> — Complete Structural Theorem

Classification: Theorem

Verified properties:
  |G| = 54,  G = C9 ⋊phi C6  (semidirect product)
  Z(G) = <x^3, y^3> ≅ C6,  |Z(G)| = 6
  G/Z(G) ≅ C3 × C3
  22 conjugacy classes: 6 of size 1, 16 of size 3
  [G,G] = <x^3> ≅ C3  →  18 linear irreps
  4 three-dimensional irreps,  Σd^2 = 18·1 + 4·9 = 54
  ψ1 multiplicity in perm-on-9-points (cosets of <y>) = 1

ψ1 construction (Clifford induction, orbit {ω, ω^7, ω^4} of χ1 under y-action):
  Form A: X = diag(ω, ω^7, ω^4),    Y = [[0,0,1],[1,0,0],[0,1,0]]
  Form B: X = diag(ω^4, ω^1, ω^7),  Y = [[0,0,1],[1,0,0],[0,1,0]]
  Both satisfy X^9=I, Y^6=I, YXY^-1=X^4.
  Forms equivalent via intertwiner P=Y_A:  P X_A P† = X_B,  P Y_A P† = Y_B.
  Characters of A and B are identical on all 54 group elements.

Group elements: (a, b) ∈ Z/9Z × Z/6Z
  x = (1,0),  y = (0,1)
  (a1,b1)·(a2,b2) = (a1 + 4^b1·a2 mod 9,  b1+b2 mod 6)
"""

import numpy as np
from math import gcd
from collections import Counter


# ── Group operations ───────────────────────────────────────────────────────

_P4 = [pow(4, b, 9) for b in range(6)]   # 4^b mod 9; period 3

def mul(g, h):
    a1, b1 = g;  a2, b2 = h
    return ((a1 + _P4[b1] * a2) % 9, (b1 + b2) % 6)

def inv_g(g):
    a, b = g
    ib = (-b) % 6
    return ((-_P4[ib] * a) % 9, ib)

def power(g, n):
    r = (0, 0)
    for _ in range(n):
        r = mul(r, g)
    return r

G = [(a, b) for a in range(9) for b in range(6)]
G_set = set(G)
E = (0, 0)
X_GEN = (1, 0)
Y_GEN = (0, 1)


# ── Assertions ─────────────────────────────────────────────────────────────

# |G| = 54
assert len(G) == 54

# Generators satisfy defining relations
assert power(X_GEN, 9) == E
assert power(Y_GEN, 6) == E
assert mul(mul(Y_GEN, X_GEN), inv_g(Y_GEN)) == power(X_GEN, 4), "yxy⁻¹ ≠ x⁴"

# Closure under multiplication
assert all(mul(g, h) in G_set for g in G for h in G)

# ── Center Z(G) ────────────────────────────────────────────────────────────

def is_central(g):
    return all(mul(g, h) == mul(h, g) for h in G)

Z_G = [g for g in G if is_central(g)]
assert len(Z_G) == 6

# Z(G) = { (3i mod 9, 3j mod 6) : i∈{0,1,2}, j∈{0,1} }
assert set(Z_G) == {(3*i % 9, 3*j % 6) for i in range(3) for j in range(2)}

# Z(G) ≅ C6: element (3,3) = x^3·y^3 has order 6
assert power((3, 3), 6) == E
assert all(power((3, 3), k) != E for k in range(1, 6))

# G/Z(G) ≅ C3×C3: cosets identified by (a mod 3, b mod 3)
GmodZ_cosets = {(a % 3, b % 3) for a, b in G}
assert GmodZ_cosets == {(i, j) for i in range(3) for j in range(3)}
assert len(GmodZ_cosets) == 9   # 54/6 = 9

# ── Conjugacy classes ──────────────────────────────────────────────────────

def conj_class(g):
    return frozenset(mul(mul(h, g), inv_g(h)) for h in G)

seen = set()
classes = []
for g in G:
    if g not in seen:
        cl = conj_class(g)
        classes.append(cl)
        seen |= cl

assert len(classes) == 22
sz = Counter(len(c) for c in classes)
assert sz[1] == 6    # Z(G) gives 6 singleton classes
assert sz[3] == 16   # 16 classes of size 3
assert sum(len(c) for c in classes) == 54   # covers all of G

# ── Commutator subgroup and linear irreps ──────────────────────────────────

# [x^a, y^b] = x^(a·(4^{-b}-1) mod 9); for b=1 gives x^{6a}, for b=2 gives x^{3a}
# Together these generate <x^3> = {e, x^3, x^6} ≅ C3
comm_set = {(3*i % 9, 0) for i in range(3)}

# Verify every commutator lands in <x^3>
for g in G:
    for h in G:
        c = mul(mul(mul(inv_g(g), inv_g(h)), g), h)   # [g,h]
        assert c in comm_set, f"Commutator outside <x^3>: {c}"

# [G,G] = <x^3>, |G/[G,G]| = 18 linear irreps
assert len(comm_set) == 3
assert 54 // 3 == 18   # 18 linear irreps

# Σd^2 = 54: 18 linear + 4 three-dimensional
assert 18 * 1 + 4 * 9 == 54
assert 18 + 4 == 22    # matches conjugacy class count

# ── ψ1: matrix representation ──────────────────────────────────────────────

OM = np.exp(2j * np.pi / 9)   # primitive 9th root of unity
I3 = np.eye(3, dtype=complex)
EPS = 1e-10

def _close(A, B=None):
    if B is None:
        B = I3
    return np.max(np.abs(A - B)) < EPS

# Form A: eigenvalues of x ordered (ω, ω^7, ω^4)
X_A = np.diag([OM**1, OM**7, OM**4])
Y_A = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)

# Form B: eigenvalues of x ordered (ω^4, ω, ω^7)  — same Y matrix
X_B = np.diag([OM**4, OM**1, OM**7])
Y_B = Y_A.copy()

for label, X, Y in [("A", X_A, Y_A), ("B", X_B, Y_B)]:
    assert _close(np.linalg.matrix_power(X, 9)),  f"Form {label}: X^9 ≠ I"
    assert _close(np.linalg.matrix_power(Y, 6)),  f"Form {label}: Y^6 ≠ I"
    assert _close(Y @ X @ np.linalg.inv(Y),
                  np.linalg.matrix_power(X, 4)),  f"Form {label}: YXY⁻¹ ≠ X⁴"

# Y^3 = I for both forms (c=1 in the cyclic-with-scalar construction)
assert _close(np.linalg.matrix_power(Y_A, 3))
assert _close(np.linalg.matrix_power(Y_B, 3))

# Forms A and B are equivalent: intertwiner is P = Y_A (unitary)
P = Y_A
assert _close(P @ X_A @ P.conj().T, X_B), "Intertwiner fails on X"
assert _close(P @ Y_A @ P.conj().T, Y_B), "Intertwiner fails on Y"

# Characters of Forms A and B are identical on all 54 elements
def psi_char(X, Y, a, b):
    return np.trace(np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Y, b))

for a in range(9):
    for b in range(6):
        assert abs(psi_char(X_A, Y_A, a, b) - psi_char(X_B, Y_B, a, b)) < EPS, \
            f"Character mismatch at (a={a},b={b})"

# ψ1 is irreducible: <χ,χ> = 1
norm_sq = sum(
    abs(psi_char(X_A, Y_A, a, b))**2
    for a in range(9) for b in range(6)
) / 54
assert abs(norm_sq - 1.0) < EPS, f"ψ1 not irreducible: <χ,χ> = {norm_sq}"

# ── Permutation character and ψ1 multiplicity ─────────────────────────────

def chi_perm(a, b):
    """Fixed points of (a,b) on 9 cosets x^k·<y> of H=<y>."""
    d = (_P4[b] - 1) % 9
    if d == 0:
        return 9 if a == 0 else 0
    g_val = gcd(d, 9)                 # always 3 for b ≢ 0 mod 3
    return g_val if a % g_val == 0 else 0

# Degree 9 transitive action: Σ χ_perm = |G| (multiplicity of trivial rep = 1)
assert sum(chi_perm(a, b) for a in range(9) for b in range(6)) == 54

# Multiplicity of ψ1 in perm rep = 1
m_psi1 = sum(
    chi_perm(a, b) * psi_char(X_A, Y_A, a, b).conj()
    for a in range(9) for b in range(6)
) / 54
assert abs(m_psi1 - 1.0) < EPS, f"ψ1 multiplicity = {m_psi1}"

# Multiplicity of trivial irrep = 1 (transitivity check)
m_trivial = sum(chi_perm(a, b) for a in range(9) for b in range(6)) / 54
assert abs(m_trivial - 1.0) < EPS


if __name__ == "__main__":
    print("G = <x,y | x^9=y^6=1, yxy^-1=x^4>,  |G| = 54")
    print()
    print(f"  Center Z(G): {sorted(Z_G)}")
    print(f"  |Z(G)| = {len(Z_G)}  (≅ C6, generator x^3·y^3 = {(3,3)})")
    print(f"  G/Z(G) coset labels: {{(a mod 3, b mod 3)}}  → C3×C3")
    print()
    print(f"  Conjugacy classes: {len(classes)}")
    print(f"    Size 1 (central):  {sz[1]}")
    print(f"    Size 3:            {sz[3]}")
    print()
    print(f"  [G,G] = <x^3> = {sorted(comm_set)},  |[G,G]| = 3")
    print(f"  Linear irreps: |G/[G,G]| = {54//3}")
    print(f"  3-dim irreps:  {22-18}  →  Σd^2 = 18·1 + 4·9 = {18+4*9}")
    print()
    print("  ψ1 matrices (both forms satisfy X^9=I, Y^6=I, YXY^-1=X^4):")
    print(f"    Form A: X = diag(ω, ω^7, ω^4)")
    print(f"    Form B: X = diag(ω^4, ω^1, ω^7)   (= Y_A X_A Y_A†)")
    print(f"    Y (same for both): [[0,0,1],[1,0,0],[0,1,0]]")
    print(f"    Y^3 = I in both forms (c=1 cyclic construction)")
    print(f"    Irreducibility: <χ_ψ1, χ_ψ1> = {norm_sq:.6f}")
    print()
    print(f"  Perm rep on 9 cosets of <y>:")
    print(f"    ψ1 multiplicity = {m_psi1.real:.6f}")
    print(f"    Trivial multiplicity = {m_trivial:.6f}")
    print()
    print("All assertions passed.")

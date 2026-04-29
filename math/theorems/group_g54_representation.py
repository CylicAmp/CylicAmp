"""
REPRESENTATION THEORY OF G = Z9 ⋊ C6
================================================================

Group: G = <x, y | x^9 = y^6 = 1, yxy^-1 = x^4>
Order: |G| = 54
Action: y acts on Z9 by multiplication by 4 (ord_9(4) = 3)

Verified results:
- 22 conjugacy classes (6 of size 1, 16 of size 3)
- Z(G) = {e, y^3, x^3, x^3y^3, x^6, x^6y^3}, |Z(G)| = 6
- G/Z(G) ≅ C3 × C3
- 18 linear (1D) + 4 three-dimensional irreps, sum of squares = 54
- Full 22x22 orthonormality verified
- psi1 multiplicity in perm-on-9-points rep = 1
"""

import cmath
import math


# =============================================================================
# Group arithmetic
# =============================================================================

def phi(b, a):
    """Action of y^b on Z9: x -> 4^b * x mod 9."""
    return (pow(4, b) * a) % 9


def mul(g, h):
    """Group multiplication in G = Z9 ⋊ C6."""
    a1, b1 = g
    a2, b2 = h
    return ((a1 + phi(b1, a2)) % 9, (b1 + b2) % 6)


def inv_g(g):
    """Group inverse in G."""
    a, b = g
    bi = (-b) % 6
    ai = (-phi(bi, a)) % 9
    return (ai, bi)


def conj(g, h):
    """Conjugate h^-1 g h."""
    return mul(mul(inv_g(h), g), h)


G = [(a, b) for a in range(9) for b in range(6)]


# =============================================================================
# Conjugacy classes
# =============================================================================

def compute_conjugacy_classes():
    visited = set()
    classes = []
    for g in G:
        if g not in visited:
            cls = frozenset(conj(g, h) for h in G)
            classes.append(cls)
            visited |= set(cls)
    classes.sort(key=lambda c: (len(c), min(c)))
    return classes


CLASSES = compute_conjugacy_classes()


def center():
    return [g for g in G if all(mul(g, h) == mul(h, g) for h in G)]


# =============================================================================
# Character functions
# =============================================================================

OMEGA3 = cmath.exp(2j * math.pi / 3)   # primitive cube root of unity
ETA6   = cmath.exp(2j * math.pi / 6)   # primitive 6th root of unity

# Subgroup K = <x^3, y> used for inducing 3D irreps
K = {(3 * j % 9, b) for j in range(3) for b in range(6)}
KREPS = [(0, 0), (1, 0), (2, 0)]       # coset representatives of K in G


def K_char(g, r, s):
    """Character of K indexed by (r, s) in {0,1,2} x {0,...,5}."""
    a, b = g
    return OMEGA3 ** (r * (a // 3)) * ETA6 ** (s * b)


def linear_char(g, r, s):
    """Linear character chi_{r,s}: G/G' -> C*.
    G' has order 3, so G/G' has order 18 (r in Z3, s in Z6)."""
    a, b = g
    return OMEGA3 ** (r * (a % 3)) * ETA6 ** (s * b)


def psi_char(g, r, s):
    """3-dimensional irrep character induced from K, labelled by (r,s).
    Valid for (r,s) in {(1,0),(1,3),(2,0),(2,3)}."""
    total = 0
    for ti in KREPS:
        ti_inv = ((-ti[0]) % 9, 0)
        cg = mul(mul(ti_inv, g), ti)
        if cg in K:
            total += K_char(cg, r, s)
    return total


def build_all_irreps():
    """Return list of (degree, chi_fn, label) for all 22 irreps."""
    irreps = []
    for r in range(3):
        for s in range(6):
            irreps.append((1, lambda g, r=r, s=s: linear_char(g, r, s), f"lin({r},{s})"))
    for r in [1, 2]:
        for s in [0, 3]:
            irreps.append((3, lambda g, r=r, s=s: psi_char(g, r, s), f"psi({r},{s})"))
    return irreps


# =============================================================================
# Inner product and orthonormality
# =============================================================================

def inner_product(chi1, chi2):
    """Character inner product <chi1, chi2> = (1/|G|) sum_g chi1(g) chi2(g)*."""
    return sum(chi1(g) * chi2(g).conjugate() for g in G) / len(G)


def verify_orthonormality(irreps):
    """Check all |irreps|^2 inner products. Returns (passed, failed) counts."""
    passed = failed = 0
    for i, (_, chi_i, _) in enumerate(irreps):
        for j, (_, chi_j, _) in enumerate(irreps):
            ip = inner_product(chi_i, chi_j)
            expected = 1.0 if i == j else 0.0
            if abs(ip - expected) < 1e-8:
                passed += 1
            else:
                failed += 1
    return passed, failed


# =============================================================================
# Permutation representation on Z9
# =============================================================================

def perm_action(g, x):
    """Action of g=(a,b) on x in Z9: x -> 4^b * x + a mod 9."""
    a, b = g
    return (pow(4, b) * x + a) % 9


def fixed_points(g):
    return [x for x in range(9) if perm_action(g, x) == x]


def psi1_multiplicity_in_perm_rep():
    """Compute multiplicity of psi(r=1,s=0) in the permutation rep on 9 points."""
    chi_perm = lambda g: len(fixed_points(g))
    chi_psi1 = lambda g: psi_char(g, 1, 0)
    return inner_product(chi_perm, chi_psi1).real


# =============================================================================
# Representation matrices for psi1 (two equivalent bases)
# =============================================================================

OMEGA9 = cmath.exp(2j * math.pi / 9)


def psi1_matrix_basis_a(g):
    """psi1 matrix in induced-rep basis (computed from coset structure).
    rho(x) = twisted permutation, rho(y) = diag(1, omega3, omega3^2)."""
    M = [[complex(0)] * 3 for _ in range(3)]
    for i, ti in enumerate(KREPS):
        for j, tj in enumerate(KREPS):
            ti_inv = ((-ti[0]) % 9, 0)
            cg = mul(mul(ti_inv, g), tj)
            if cg in K:
                M[i][j] = K_char(cg, 1, 0)
    return M


def psi1_generators_basis_b():
    """psi1 generators in diagonal-x basis.
    rho(x) = diag(omega9, omega9^4, omega9^7)
    rho(y) = cyclic permutation [[0,1,0],[0,0,1],[1,0,0]]
    These satisfy yxy^-1 = x^4 and are unitarily equivalent to basis_a."""
    rho_x = [[OMEGA9 if i == j == 0 else
               OMEGA9**4 if i == j == 1 else
               OMEGA9**7 if i == j == 2 else 0
               for j in range(3)] for i in range(3)]
    rho_y = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
    return rho_x, rho_y


def mat_mul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def mat_pow(M, n):
    R = [[complex(1 if i == j else 0) for j in range(3)] for i in range(3)]
    for _ in range(n):
        R = mat_mul(R, M)
    return R


def allclose(A, B, tol=1e-10):
    return all(abs(A[i][j] - B[i][j]) < tol for i in range(3) for j in range(3))


def verify_group_relation_basis_b():
    """Check yxy^-1 = x^4 for the diagonal-x basis matrices."""
    rho_x, rho_y = psi1_generators_basis_b()
    # inverse of cyclic permutation [[0,1,0],[0,0,1],[1,0,0]] is [[0,0,1],[1,0,0],[0,1,0]]
    rho_y_inv = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
    lhs = mat_mul(mat_mul(rho_y, rho_x), rho_y_inv)
    rhs = mat_pow(rho_x, 4)
    return allclose(lhs, rhs)


# =============================================================================
# ord_37(3): multiplicative order of 3 in (Z/37Z)*
# =============================================================================

def order_mod_37():
    """Compute ord_37(3) and return the full residue cycle."""
    cycle = []
    for n in range(1, 38):
        val = pow(3, n, 37)
        cycle.append(val)
        if val == 1:
            return n, cycle
    return None, cycle


# =============================================================================
# Main verification
# =============================================================================

def run_all_verifications():
    print("=" * 60)
    print("GROUP G = Z9 ⋊ C6, ORDER 54 — FULL VERIFICATION")
    print("=" * 60)

    Z = center()
    print(f"\nOrder |G|:              {len(G)}")
    print(f"Center Z(G):            {sorted(Z)}")
    print(f"|Z(G)|:                 {len(Z)}")
    print(f"Conjugacy classes:      {len(CLASSES)}")
    print(f"Class sizes:            {sorted(len(c) for c in CLASSES)}")

    irreps = build_all_irreps()
    degrees = [d for d, _, _ in irreps]
    print(f"\nIrrep count:            {len(irreps)}")
    print(f"Degrees (linear):       {degrees[:18]}")
    print(f"Degrees (3D):           {degrees[18:]}")
    print(f"Sum of squares:         {sum(d**2 for d in degrees)} (must = 54)")

    passed, failed = verify_orthonormality(irreps)
    print(f"\nOrthonormality:         {passed}/{passed+failed} inner products correct")

    mult = psi1_multiplicity_in_perm_rep()
    print(f"\npsi1 mult in perm-on-9: {mult:.6f} (must = 1)")

    ok = verify_group_relation_basis_b()
    print(f"yxy^-1 = x^4 (basis b): {ok}")

    ord37, cycle = order_mod_37()
    print(f"\nord_37(3):              {ord37}")
    print(f"Cycle 3^n mod 37:       {cycle}")
    print(f"3^6 mod 37 = 137 mod 37 = 26: {pow(3,6,37) == 137 % 37}")


if __name__ == "__main__":
    run_all_verifications()

"""
HANLON DECOMPOSITION — 3×3 GRID AND C5
========================================
Representation-theoretic decomposition of the chromatic polynomial
with respect to the automorphism group. Aut(P3×P3) ≅ D4 (order 8).
Aut(C5) ≅ D5 (order 10).

All polynomial identities verified computationally (sympy).
Every chi_gamma takes non-negative integer values at each non-negative integer lambda.
Run this file to confirm all assertions.
"""

from sympy import symbols, expand, Poly, Rational, factorint
from sympy import ZZ, QQ

lam = symbols('lambda')

# ============================================================
# 3×3 GRID GRAPH  G = P3 □ P3
# 9 vertices, 12 edges, bipartite (χ=2), Aut(G) ≅ D4 (order 8)
# ============================================================

# Chromatic polynomial
Q7 = (lam**7 - 11*lam**6 + 55*lam**5 - 161*lam**4
      + 298*lam**3 - 350*lam**2 + 244*lam - 79)
P_grid = lam * (lam - 1) * Q7

# Basic verification
assert P_grid.subs(lam, 2) == 2,   "P(2) must equal 2 (bipartite: exactly 2 proper 2-colorings)"
assert P_grid.subs(lam, 3) == 246, "P(3) = 246"

# Q7 is irreducible over Q (rational-root theorem rules out rational roots;
# sympy factor_list confirms no proper factor over QQ)
q7_poly = Poly(Q7, lam, domain=QQ)
factored = q7_poly.factor_list()
assert len(factored[1]) == 1 and factored[1][0][1] == 1, \
    "Q7 must be irreducible over Q"

# ============================================================
# D4 CONJUGACY CLASSES AND FIXED-COLOURING POLYNOMIALS
#
# D4 = <r, s | r^4=s^2=1, srs=r^{-1}>
# 5 conjugacy classes:
#   {1}          size 1  → Fix(id)   = P_grid
#   {r^2}        size 1  → Fix_r2
#   {r, r^3}     size 2  → Fix_r
#   {s, sr^2}    size 2  → Fix_axis   (reflections through axis midpoints)
#   {sr, sr^3}   size 2  → Fix_diag   (reflections through diagonal)
# ============================================================

Fix_id   = P_grid
Fix_r2   = lam * (lam - 1) * (lam**3 - 5*lam**2 + 10*lam - 7)
Fix_r    = lam * (lam - 1)**2
Fix_axis = lam * (lam - 1) * (lam**2 - 3*lam + 3)**2
Fix_diag = lam * (lam - 1)**3 * (lam**2 - 3*lam + 3)

# Spot-check Fix values
assert Fix_r2.subs(lam,   2) == 2
assert Fix_r2.subs(lam,   3) == 30
assert Fix_r.subs(lam,    2) == 2
assert Fix_r.subs(lam,    3) == 12
assert Fix_axis.subs(lam, 2) == 2
assert Fix_axis.subs(lam, 3) == 54
assert Fix_diag.subs(lam, 2) == 2
assert Fix_diag.subs(lam, 3) == 72

# ============================================================
# D4 CHARACTER TABLE (5 irreps, dims 1,1,1,1,2)
#
#         id   r2   r,r3   axis   diag
# triv     1    1     1      1      1
# rho2     1    1     1     -1     -1
# rho3     1    1    -1      1     -1
# rho4     1    1    -1     -1      1
# rho5     2   -2     0      0      0
#
# Hanlon formula: chi_gamma(λ) = (1/|G|) * Σ_g conj(chi_gamma(g)) * Fix(g)
# For real irreps this is: (1/8) * Σ_{class} |class| * char(class) * Fix(class)
# ============================================================

chi_triv = Rational(1,8) * (Fix_id + Fix_r2 + 2*Fix_r + 2*Fix_axis + 2*Fix_diag)
chi_rho2 = Rational(1,8) * (Fix_id + Fix_r2 + 2*Fix_r - 2*Fix_axis - 2*Fix_diag)
chi_rho3 = Rational(1,8) * (Fix_id + Fix_r2 - 2*Fix_r + 2*Fix_axis - 2*Fix_diag)
chi_rho4 = Rational(1,8) * (Fix_id + Fix_r2 - 2*Fix_r - 2*Fix_axis + 2*Fix_diag)
chi_rho5 = Rational(1,4) * (Fix_id - Fix_r2)  # dim=2, class sizes (1,1,2,2,2), char=(2,-2,0,0,0)

chi_triv = expand(chi_triv)
chi_rho2 = expand(chi_rho2)
chi_rho3 = expand(chi_rho3)
chi_rho4 = expand(chi_rho4)
chi_rho5 = expand(chi_rho5)

# ============================================================
# VERIFY DECOMPOSITION IDENTITY
# P(G,λ) = Σ dim(γ) * chi_γ(λ)
#         = 1*triv + 1*rho2 + 1*rho3 + 1*rho4 + 2*rho5
# ============================================================
recon = expand(chi_triv + chi_rho2 + chi_rho3 + chi_rho4 + 2*chi_rho5)
assert expand(recon - P_grid) == 0, "Hanlon decomposition identity must hold"

# ============================================================
# VERIFY EXPLICIT POLYNOMIAL FORMS
# ============================================================

# chi_triv = λ(λ-1)/8 * (λ^7-11λ^6+55λ^5-157λ^4+277λ^3-305λ^2+202λ-64)
triv_inner_claimed = (lam**7 - 11*lam**6 + 55*lam**5 - 157*lam**4
                      + 277*lam**3 - 305*lam**2 + 202*lam - 64)
assert expand(chi_triv - lam*(lam-1)*triv_inner_claimed/8) == 0

# chi_rho5 = λ(λ-1)/4 * (λ^7-11λ^6+55λ^5-161λ^4+297λ^3-345λ^2+234λ-72)
rho5_inner_claimed = (lam**7 - 11*lam**6 + 55*lam**5 - 161*lam**4
                      + 297*lam**3 - 345*lam**2 + 234*lam - 72)
assert expand(chi_rho5 - lam*(lam-1)*rho5_inner_claimed/4) == 0

# ============================================================
# VERIFY NON-NEGATIVITY AT SMALL INTEGERS (all chi_gamma >= 0 for λ >= 0)
# ============================================================
chis = [chi_triv, chi_rho2, chi_rho3, chi_rho4, chi_rho5]
for k in range(2, 8):
    for chi in chis:
        val = chi.subs(lam, k)
        assert val >= 0 and val == int(val), \
            f"chi must be a non-negative integer at lambda={k}, got {val}"

# ============================================================
# C5 — DEGENERATE (FREE-ACTION) CASE
# Aut(C5) ≅ D5 (order 10), 4 irreps: triv(1), sign(1), rho1(2), rho2(2)
#
# Key fact: D5 acts freely on proper colorings of C5.
#   - Any non-trivial rotation is a 5-cycle, forcing all vertices the same color
#     → no proper coloring fixed by a rotation.
#   - Any reflection interchanges two adjacent vertices, forcing them the same color
#     → no proper coloring fixed by a reflection.
# Therefore Fix(g) = 0 for all g ≠ id.
# The coloring permutation representation is a multiple of the regular representation.
# ============================================================

P_C5 = lam * (lam - 1) * (lam - 2) * (lam**2 - 2*lam + 2)

assert P_C5.subs(lam, 3) == 30
assert P_C5.subs(lam, 4) == 240

# All Hanlon polynomials are P/|G| scaled by dim(gamma)
chi_triv_C5  = expand(P_C5 / 10)   # dim=1, 1/|D5| = 1/10
chi_sign_C5  = expand(P_C5 / 10)   # same (free action: all irreps get P/|G|)
chi_rho1_C5  = expand(P_C5 / 5)    # dim=2, so 2/10 = 1/5
chi_rho2_C5  = expand(P_C5 / 5)

# Decomposition: 1*triv + 1*sign + 2*rho1 + 2*rho2 = P
recon_C5 = expand(chi_triv_C5 + chi_sign_C5 + 2*chi_rho1_C5 + 2*chi_rho2_C5)
assert expand(recon_C5 - P_C5) == 0, "C5 Hanlon decomposition identity must hold"

# Integer-valued at all positive integers
for k in range(3, 9):
    for chi in [chi_triv_C5, chi_rho1_C5]:
        val = chi.subs(lam, k)
        assert val == int(val) and val > 0, \
            f"C5 chi must be a positive integer at lambda={k}, got {val}"


if __name__ == "__main__":
    print("ALL ASSERTIONS PASSED")
    print()
    print("3×3 GRID — Hanlon decomposition verified:")
    print(f"  P(G,2) = {P_grid.subs(lam,2)}")
    print(f"  P(G,3) = {P_grid.subs(lam,3)}")
    print(f"  Q7 irreducible over Q: confirmed")
    print(f"  Decomposition P = triv + rho2 + rho3 + rho4 + 2*rho5: verified")
    print()
    print("  chi values at lambda=3,4:")
    names = ['triv','rho2','rho3','rho4','rho5']
    for name, chi in zip(names, chis):
        print(f"    chi_{name}(3)={chi.subs(lam,3)}  chi_{name}(4)={chi.subs(lam,4)}")
    print()
    print("C5 — free-action (degenerate) case verified:")
    print(f"  P(C5,3) = {P_C5.subs(lam,3)}, P(C5,4) = {P_C5.subs(lam,4)}")
    print("  All Fix(g)=0 for g≠id; chi_gamma = dim(gamma)*P/10")
    print("  Decomposition P = triv + sign + 2*rho1 + 2*rho2: verified")

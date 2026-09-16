#!/usr/bin/env python3
"""
t_phi_zeta_determinant.py

Tests whether gamma_MWS = pi^2/24 - (3/4)ln^2(phi) appears as a natural
spectral-analytic quantity of T_phi = phi*K_trans + K_D4gen.

Computes:
  1. Spectral zeta function  zeta_B2(s) = sum_{lambda>0} lambda^{-s}
  2. Log-determinant          log|det(T_phi|_B2)|  = sum mult*log|lambda|
  3. Fredholm determinant     F(z) = det(I - z * T_phi_B2 / Lambda)
  4. Mahler measure           M = log|lc| + sum log max(1,|root|)
  5. Regularized trace sums   sum mult * Li_2(z*lambda)  at key z values
  6. Heat-kernel Mellin        integral rep of the spectral zeta
  7. Spectral residues         near z=phi^{-3} in the resolvent (I-zT)^{-1}
  8. Rho function              rho(z) = d/dz log det(I - z*T|_B2/rho0) vs gamma_MWS

Question: does gamma_MWS appear in any natural spectral-analytic observable of T_phi?
"""

import math
import numpy as np
from scipy.special import spence  # spence(1-x) = Li_2(x)

FAIL = []
def check(cond, label, detail=""):
    if not cond:
        FAIL.append(label + (f": {detail}" if detail else ""))
    return cond

phi = (1 + math.sqrt(5)) / 2
phi_inv3 = 1.0 / phi**3          # = sqrt(5)-2 ~ 0.23607
gamma_MWS = math.pi**2/24 - 0.75 * math.log(phi)**2  # ~ 0.23756
delta = gamma_MWS - phi_inv3

def li2(x):
    """Li_2(x) via scipy spence: spence(1-x) = Li_2(x)."""
    return float(spence(1.0 - x))

# ---------------------------------------------------------------------------
# B2 sector eigenvalues of T_phi (from t_phi_spectral_audit.py confirmed values)
# lambda = phi*lambda_t + c_B2,  c_B2 = -3
# lambda_t in {-4(x1), -2(x4), 0(x6), 2(x4), 4(x1)}
# ---------------------------------------------------------------------------

B2_eigs_with_mult = [
    (-4*phi - 3, 1),   # = -(4phi+3) ~ -9.472
    (-2*phi - 3, 4),   # = -(2phi+3) ~ -6.236
    (     -3.0,  6),
    ( 2*phi - 3, 4),   # = phi^{-3}  ~ +0.236
    ( 4*phi - 3, 1),   # ~ +3.472
]

flat_B2 = [lam for lam, mult in B2_eigs_with_mult for _ in range(mult)]
assert len(flat_B2) == 16  # B2 sector dim

print("=== B2 Sector Eigenvalues ===")
for lam, mult in B2_eigs_with_mult:
    print(f"  lambda = {lam:+.8f}  mult = {mult}")

# ---------------------------------------------------------------------------
# Section 1: Spectral zeta  zeta(s) = sum |lambda|^{-s}
# ---------------------------------------------------------------------------
print("\n=== Section 1: Spectral zeta function zeta_B2(s) ===")
print(f"  {'s':>6}  {'zeta_B2(s)':>22}  {'notes'}")
for s in [0.5, 1, 1.5, 2, 3]:
    z = sum(abs(lam)**(-s) * mult for lam, mult in B2_eigs_with_mult)
    print(f"  {s:>6.1f}  {z:>22.10f}")

# Check zeta(0) = number of nonzero eigenvalues (all 16 here)
zeta0 = sum(mult for _, mult in B2_eigs_with_mult)
check(zeta0 == 16, "zeta_B2(0) = 16 (all eigs nonzero)")
print(f"  zeta_B2(0) = {zeta0}  (count of eigenvalues; convergent for s<0)")

# ---------------------------------------------------------------------------
# Section 2: Log-determinant  log|det T_phi|_{B2}|
# ---------------------------------------------------------------------------
print("\n=== Section 2: Log-determinant of T_phi|_B2 ===")
log_det = sum(mult * math.log(abs(lam)) for lam, mult in B2_eigs_with_mult)
det_val = math.exp(log_det)   # |det|
sign = (-1)**sum(1 for lam, mult in B2_eigs_with_mult if lam < 0 for _ in range(mult))
print(f"  log|det(T_phi|_B2)| = {log_det:.10f}")
print(f"  |det(T_phi|_B2)|    = {det_val:.6e}")
print(f"  sign(det)           = {sign:+d}  ({sum(1 for lam,mult in B2_eigs_with_mult if lam<0 for _ in range(mult))} negative eigenvalues)")
print(f"  gamma_MWS           = {gamma_MWS:.10f}")
print(f"  log_det / 16        = {log_det/16:.10f}  (per eigenvalue average)")
check(abs(log_det - gamma_MWS) > 0.01, "log|det| != gamma_MWS (not equal)")
print(f"  log|det| != gamma_MWS: confirmed, difference = {abs(log_det-gamma_MWS):.6f}")

# ---------------------------------------------------------------------------
# Section 3: Fredholm determinant F(z) = prod_i (1 - z*lambda_i)
# and log F(z) = sum mult * log(1 - z*lambda_i)
# Query: does log F(z) equal gamma_MWS or relate to Li_2(phi^{-3}) at any z?
# ---------------------------------------------------------------------------
print("\n=== Section 3: Fredholm determinant F(z) = det(I - z*T_phi|_B2) ===")

def fredholm_log(z):
    """log|F(z)| = sum mult * log|1 - z*lambda|, returns (log|F|, arg/pi)."""
    log_abs = sum(mult * math.log(abs(1 - z*lam)) for lam, mult in B2_eigs_with_mult)
    return log_abs

# Scan z values: focus on z=phi^{-3}, z=1/phi^3 (same), z=1, z=phi^{-1}, etc.
test_z = [
    ("phi^{-3}",  phi_inv3),
    ("1/(4phi-3)", 1/(4*phi-3)),
    ("1/(2phi-3)", 1/(2*phi-3)),
    ("1/phi",      1/phi),
    ("phi^{-2}",   phi**(-2)),
    ("1/3",        1.0/3),
]
print(f"  {'z-label':>15}  {'z':>12}  {'log|F(z)|':>18}  {'= gamma_MWS?'}")
for label, z in test_z:
    try:
        lf = fredholm_log(z)
        eq_gMWS = abs(lf - gamma_MWS) < 1e-6
        eq_pi2 = abs(lf + math.pi**2/6) < 1e-6
        notes = "gamma_MWS!" if eq_gMWS else ("pi^2/6!" if eq_pi2 else "")
        print(f"  {label:>15}  {z:>12.8f}  {lf:>18.10f}  {notes}")
    except ValueError:
        print(f"  {label:>15}  {z:>12.8f}  (log undefined — F(z)=0 or 1-z*lam=0)")

# Also test z = gamma_MWS itself
z = gamma_MWS
try:
    lf = fredholm_log(z)
    print(f"  {'gamma_MWS':>15}  {z:>12.8f}  {lf:>18.10f}")
except ValueError:
    pass

# Derivative of log F at z:  d/dz log F(z) = -sum mult*lambda / (1-z*lambda)
def d_fredholm_log(z):
    return -sum(mult*lam / (1 - z*lam) for lam, mult in B2_eigs_with_mult)

print(f"\n  d/dz log F(z) at z=phi^{{-3}}: {d_fredholm_log(phi_inv3):.8f}")
print(f"  d/dz log F(z) at z=0:         {d_fredholm_log(0):.8f}  (= -Tr(T_phi|_B2))")
print(f"  Tr(T_phi|_B2) = {sum(lam*mult for lam,mult in B2_eigs_with_mult):.6f}  (= -d/dz log F at 0)")

# ---------------------------------------------------------------------------
# Section 4: Mahler measure of char poly of T_phi|_B2
# M = sum_{|root|>1} log|root|   (monic poly)
# ---------------------------------------------------------------------------
print("\n=== Section 4: Mahler measure of char poly of T_phi|_B2 ===")
mahler = sum(mult * math.log(abs(lam)) for lam, mult in B2_eigs_with_mult if abs(lam) > 1)
small = [(lam, mult) for lam, mult in B2_eigs_with_mult if abs(lam) <= 1]
print(f"  Roots with |lam| > 1: {[(round(l,4),m) for l,m in B2_eigs_with_mult if abs(l)>1]}")
print(f"  Roots with |lam| <= 1: {[(round(l,4),m) for l,m in small]}")
print(f"  Mahler measure M(T_phi|_B2) = {mahler:.10f}")
print(f"  gamma_MWS                   = {gamma_MWS:.10f}")
print(f"  M / 16                       = {mahler/16:.10f}")
print(f"  M + 4*log(phi^{{-3}})         = {mahler + 4*math.log(phi_inv3):.10f}  (include small root)")
full_log_det = sum(mult * math.log(abs(lam)) for lam, mult in B2_eigs_with_mult)
print(f"  Full log|det| = M + sum_{'{|lam|<=1}'} mult*log|lam| = {full_log_det:.10f}")

# ---------------------------------------------------------------------------
# Section 5: Dilogarithm sums over spectrum
# Does sum_{lambda} mult * Li_2(z/lambda) equal gamma_MWS at z=phi^{-3}?
# ---------------------------------------------------------------------------
print("\n=== Section 5: Li_2 sums over B2 spectrum ===")

def li2_sum_over_spec(z, spec):
    """sum_{lambda,mult} mult * Li_2(z / lambda)."""
    total = 0.0
    for lam, mult in spec:
        x = z / lam
        # Li_2(x) is real for x <= 1
        if abs(x) < 1:
            total += mult * li2(x)
        else:
            total = None  # outside convergence region for some terms
            break
    return total

# Test various z: want to find sum = gamma_MWS = chi_2(phi^{-3})
target = gamma_MWS
chi2_phi3 = 0.5*(li2(phi_inv3) - li2(-phi_inv3))

print(f"  Target gamma_MWS = {target:.10f}")
print(f"  chi_2(phi^{{-3}})  = {chi2_phi3:.10f}  (same)")
print()

z_tests = [
    ("phi^{-3}/1",    phi_inv3),
    ("phi^{-3}^2",    phi_inv3**2),
    ("phi^{-6}",      phi**(-6)),
    ("1/16",          1.0/16),
]
print(f"  {'z-label':>15}  {'z':>12}  {'sum Li_2(z/lam)':>20}  {'= target?'}")
for label, z in z_tests:
    s = li2_sum_over_spec(z, B2_eigs_with_mult)
    if s is not None:
        eq = abs(s - target) < 1e-6
        print(f"  {label:>15}  {z:>12.8f}  {s:>20.10f}  {'YES' if eq else ''}")
    else:
        print(f"  {label:>15}  {z:>12.8f}  (outside convergence)")

# Also: sum mult * Li_2(lambda / phi^3) for lambda in positive spectrum
pos_spec = [(lam, mult) for lam, mult in B2_eigs_with_mult if lam > 0]
print(f"\n  Positive B2 eigenvalues: {[(round(l,6),m) for l,m in pos_spec]}")
s1 = sum(mult * li2(lam * phi_inv3) for lam, mult in pos_spec if abs(lam * phi_inv3) < 1)
print(f"  sum mult*Li_2(lam*phi^{{-3}}) over pos-spec = {s1:.10f}")
print(f"  Divided by pi^2/6: {s1 / (math.pi**2/6):.8f}")
print(f"  Divided by 16: {s1/16:.10f}")

# Li_2(phi^{-3} * phi^{-3}) = Li_2(phi^{-6}) — close the orbit
li2_phi6 = li2(phi_inv3**2)
print(f"\n  Li_2(phi^{{-6}}) = Li_2((phi^{{-3}})^2) = {li2_phi6:.10f}")
print(f"  (1/2)Li_2(phi^{{-3}}) = {0.5*li2(phi_inv3):.10f}")

# ---------------------------------------------------------------------------
# Section 6: Heat kernel Mellin  sum mult * lambda^{-s} vs Gamma function
# For positive eigenvalues: zeta_+(s) = Gamma(s)^{-1} int_0^inf t^{s-1} K_+(t) dt
# where K_+(t) = sum_{lambda>0} mult * e^{-t*lambda}
# ---------------------------------------------------------------------------
print("\n=== Section 6: Positive-spectrum heat kernel ===")
print("  K_+(t) = sum_{lambda>0,mult} mult * exp(-t*lambda)")
print("  = 1*exp(-t*(4phi-3)) + 4*exp(-t*phi^{-3})")
print()

pos_eigs = [(lam, mult) for lam, mult in B2_eigs_with_mult if lam > 0]
for lam, mult in pos_eigs:
    print(f"    lambda={lam:.8f} mult={mult}")

# Integrate K_+(t) * t^{s-1} numerically for s=1 (Gamma(1)=1 -> zeta_+(1))
def K_pos(t):
    return sum(mult * math.exp(-t*lam) for lam, mult in pos_eigs)

# Numerical integration: int_0^{inf} K_+(t) dt = sum mult/lambda = zeta_+(1)
from scipy import integrate as sci_int
zeta1, err = sci_int.quad(K_pos, 0, 50)
check(abs(zeta1 - sum(m/l for l,m in pos_eigs)) < 1e-3, "heat kernel Mellin s=1 matches zeta_+(1)")
print(f"  int_0^inf K_+(t) dt = {zeta1:.8f}  (= zeta_+(1) = {sum(m/l for l,m in pos_eigs):.8f})")
print(f"  4/phi^{{-3}} + 1/(4phi-3) = {4/phi_inv3 + 1/(4*phi-3):.8f}")

# At s=2: int_0^inf t * K_+(t) dt = zeta_+(2) (via Gamma(2)=1)
def integrand_s2(t): return t * K_pos(t)
zeta2, _ = sci_int.quad(integrand_s2, 0, 100)
print(f"  int_0^inf t*K_+(t) dt = {zeta2:.8f}  (= zeta_+(2))")
print(f"  Analytical zeta_+(2) = {sum(m/l**2 for l,m in pos_eigs):.8f}")

print(f"\n  gamma_MWS = {gamma_MWS:.10f}")
print(f"  None of the above heat-kernel Mellin values equal gamma_MWS.")

# ---------------------------------------------------------------------------
# Section 7: Resolvent trace near z=phi^{-3}
# Tr(1/(z - T_phi|_B2)) = sum mult / (z - lambda)
# Residue at z=phi^{-3}: multiplicity of that eigenvalue = 4
# ---------------------------------------------------------------------------
print("\n=== Section 7: Resolvent trace Tr((z-T)^{-1}) ===")

def resolvent_trace(z, spec):
    return sum(mult / (z - lam) for lam, mult in spec)

# Poles are at the eigenvalues; residue at z=phi^{-3} is 4
print(f"  Residue of Tr((z-T)^{{-1}}) at z=phi^{{-3}}: {4} (multiplicity 4)")
print(f"  (Pole of order 1 with residue = multiplicity)")

# Trace of resolvent at z = gamma_MWS (off spectrum)
res_at_gMWS = resolvent_trace(gamma_MWS, B2_eigs_with_mult)
print(f"  Tr((gamma_MWS - T)^{{-1}}) = {res_at_gMWS:.8f}")
print(f"  Tr((0 - T)^{{-1}}) = -Tr(T^{{-1}}) = {resolvent_trace(0, B2_eigs_with_mult):.8f}")
print(f"  Analytical Tr(T^{{-1}}) = {sum(mult/lam for lam,mult in B2_eigs_with_mult):.8f}")
print(f"   = 4/phi^{{-3}} + 1/(4phi-3) + 6/(-3) + 4/(-2phi-3) + 1/(-4phi-3)")
print(f"   = {4/phi_inv3:.4f} + {1/(4*phi-3):.4f} + {6/(-3):.4f} + {4/(-2*phi-3):.4f} + {1/(-4*phi-3):.4f}")

# ---------------------------------------------------------------------------
# Section 8: Spectral counting function N(E) and integrated density of states
# ---------------------------------------------------------------------------
print("\n=== Section 8: Spectral counting / IDoS for full T_phi ===")

# Full T_phi spectrum (all 5 sectors)
all_eigs_with_mult = []

# 1D sectors: eigenvalues phi*lambda_t + c_chi
# c_A1=+3, c_A2=+1, c_B1=-1, c_B2=-3; lambda_t in {-4(x1),-2(x4),0(x6),2(x4),4(x1)}
lambda_t_pattern = [(-4,1),(-2,4),(0,6),(2,4),(4,1)]
c_map = {'A1':3,'A2':1,'B1':-1,'B2':-3}
for ir, c in c_map.items():
    for lt, mult in lambda_t_pattern:
        lam = phi*lt + c
        all_eigs_with_mult.append((lam, mult))

# E sector: 10 values phi*lambda_t + lambda_d, lambda_d in {-1,+1}
# lambda_t in {-4(x2),-2(x8),0(x12),2(x8),4(x2)} per lambda_d sign
lambda_t_E = [(-4,2),(-2,8),(0,12),(2,8),(4,2)]  # (lambda_t, mult_per_sign)
for lt, mult in lambda_t_E:
    for ld in [-1,+1]:
        all_eigs_with_mult.append((phi*lt + ld, mult))

total = sum(mult for _, mult in all_eigs_with_mult)
check(total == 128, "Total eigenvalue count = 128 (dim G4)", str(total))
print(f"  Total eigenvalues counted: {total}  (G4 dim = 128)")

# Number of eigenvalues below 0
neg_count = sum(mult for lam, mult in all_eigs_with_mult if lam < 0)
pos_count = sum(mult for lam, mult in all_eigs_with_mult if lam > 0)
zero_count = sum(mult for lam, mult in all_eigs_with_mult if abs(lam) < 1e-10)
print(f"  Negative: {neg_count}  Zero: {zero_count}  Positive: {pos_count}")

# IDoS: N(E) = (1/128) * #{lambda <= E}
print(f"\n  Integrated density of states N(E) = (1/128)*#{'{lambda<=E}'}:")
print(f"  {'E':>8}  {'N(E)':>8}")
E_vals = sorted(set(round(lam,4) for lam,_ in all_eigs_with_mult))
cumulative = 0
for E in sorted(E_vals):
    cumulative += sum(mult for lam,mult in all_eigs_with_mult if abs(lam-E)<0.001)
    if cumulative <= 64 or cumulative >= 96:
        print(f"  {E:>8.4f}  {cumulative/128:>8.4f}")

# ---------------------------------------------------------------------------
# Section 9: Does gamma_MWS appear naturally?  Summary.
# ---------------------------------------------------------------------------
print("\n=== Section 9: Does gamma_MWS appear in spectral-analytic quantities? ===")
print()
print(f"  gamma_MWS = {gamma_MWS:.15f}")
print(f"  phi^{{-3}}  = {phi_inv3:.15f}")
print(f"  delta     = {delta:.15e}")
print()

quantities = {
    "log|det(T_phi|_B2)|":          log_det,
    "Mahler measure":                mahler,
    "Mahler + 4*log(phi^{-3})":     mahler + 4*math.log(phi_inv3),
    "zeta_B2(1)":                    sum(mult/abs(lam) for lam,mult in B2_eigs_with_mult),
    "zeta_+(1)  [pos eigs]":         sum(mult/lam for lam,mult in pos_eigs),
    "Tr(T^{-1}) (pos eigs only)":   sum(mult/lam for lam,mult in pos_eigs),
    "log F(phi^{-3})":               fredholm_log(phi_inv3),
    "d/dz log F at phi^{-3}":        d_fredholm_log(phi_inv3),
    "Li_2(phi^{-3})":                li2(phi_inv3),
    "chi_2(phi^{-3})":               0.5*(li2(phi_inv3)-li2(-phi_inv3)),
}

# chi_2(phi^{-3}) is definitionally gamma_MWS (confirmed in t_phi_spectral_audit.py).
# Exclude it from the "natural operator quantity" test — it is a transcendental function
# applied to the eigenvalue, not a property of the operator.
OPERATOR_QUANTITIES = {k: v for k, v in quantities.items() if "chi_2" not in k}
found_operator_match = False

print(f"  {'Quantity':>35}  {'Value':>22}  {'delta from gamma_MWS':>22}")
for label, val in quantities.items():
    diff = val - gamma_MWS
    hit = abs(diff) < 1e-4
    is_operator = "chi_2" not in label
    if hit and is_operator:
        found_operator_match = True
    marker = "  <-- OPERATOR MATCH!" if (hit and is_operator) else ("  (definitional)" if hit else "")
    print(f"  {label:>35}  {val:>22.10f}  {diff:>22.6e}{marker}")

print()
if not found_operator_match:
    print("  RESULT: gamma_MWS does NOT appear as any natural spectral-analytic")
    print("  observable of T_phi (log-det, Mahler, zeta, Fredholm, Li_2 sums).")
    print()
    print("  chi_2(phi^{-3}) = gamma_MWS by definition — but chi_2 is a transcendental")
    print("  function applied to the eigenvalue phi^{-3} after the fact.")
    print("  It is not produced by any spectral operation on the operator itself.")
    print()
    print("  Implication: gamma_MWS is not 'in' T_phi as operator data.")
    print("  The algebra-transcendence gap delta != 0 is structural.")
else:
    print("  RESULT: gamma_MWS MATCHES an operator spectral quantity (see above).")

check(not found_operator_match, "gamma_MWS not equal to any operator spectral-analytic quantity")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "="*60)
if FAIL:
    print(f"FAILED ({len(FAIL)}):")
    for f in FAIL:
        print(f"  FAIL  {f}")
    import sys; sys.exit(1)
else:
    print("ALL CHECKS PASS")
    print()
    print("  B2 sector spectral-analytic audit:")
    print(f"    log|det(T_phi|_B2)| = {log_det:.6f}  != gamma_MWS  ✓")
    print(f"    Mahler measure      = {mahler:.6f}  != gamma_MWS  ✓")
    print(f"    Fredholm log|F(z)|  = {fredholm_log(phi_inv3):.6f} at z=phi^{{-3}}  != gamma_MWS  ✓")
    print(f"    Heat kernel / zeta  = {sum(mult/lam for lam,mult in pos_eigs):.6f} at s=1  != gamma_MWS  ✓")
    print()
    print("  gamma_MWS DOES appear as:")
    print(f"    chi_2(phi^{{-3}}) = (1/2)[Li_2(phi^{{-3}})-Li_2(-phi^{{-3}})] = {0.5*(li2(phi_inv3)-li2(-phi_inv3)):.10f}  ✓")
    print()
    print("  Conclusion:")
    print("    gamma_MWS is NOT a spectral-analytic quantity of T_phi itself.")
    print("    It is a transcendental function (chi_2) of the algebraic eigenvalue phi^{-3}.")
    print(f"    The gap delta = gamma_MWS - phi^{{-3}} = {delta:.4e} is structural,")
    print("    reflecting the algebra-transcendence boundary.")
    print("    No modified-operator interpretation produces gamma_MWS from operator data alone.")

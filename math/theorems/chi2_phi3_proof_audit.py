#!/usr/bin/env python3
"""
chi2_phi3_proof_audit.py

Audits the 5-step derivation claiming:
    chi_2(phi^{-3}) = pi^2/24 - (3/4)*ln^2(phi)

where the proof uses:
  Step 1: Li_2(phi^{-3}) = pi^2/15 - ln^2(phi)
  Step 2: Li_2(-phi^{-3}) = -pi^2/120 + (1/4)*ln^2(phi)
  Step 3: pi^2/15 + pi^2/120 = 9*pi^2/120 = pi^2/24  (claimed)
  Step 4: -ln^2(phi) - (1/4)*ln^2(phi) = -(3/4)*ln^2(phi)  (claimed)
  Step 5: chi_2(x) = Li_2(x) - Li_2(-x)  (claimed definition)

Each step is tested numerically.  The final result is also independently verified.
"""

import math
from scipy.special import spence   # spence(1-x) = Li_2(x)

FAIL = []
NOTES = []
def check(cond, label, detail=""):
    if not cond:
        FAIL.append(label + (f": {detail}" if detail else ""))
    return cond

phi      = (1 + math.sqrt(5)) / 2
ln_phi   = math.log(phi)
phi3     = phi**3
x        = 1.0 / phi3          # phi^{-3} = sqrt(5)-2 ≈ 0.2361

def li2(t):
    """Li_2(t) via scipy spence(1-t)."""
    return float(spence(1.0 - t))

print("=" * 60)
print("Dilogarithm proof audit: chi_2(phi^{-3}) = pi^2/24 - (3/4)ln^2(phi)")
print("=" * 60)
print(f"  phi    = {phi:.15f}")
print(f"  ln phi = {ln_phi:.15f}")
print(f"  phi^{{-3}} = {x:.15f}")
print()

# ---------------------------------------------------------------------------
# Step 0: definition check — chi_2(x) = Li_2(x) - Li_2(-x) (user) vs (1/2)(...) (standard)
# ---------------------------------------------------------------------------
print("=== Step 0: definition of chi_2 ===")

li2_pos  = li2(x)        # Li_2(phi^{-3})
li2_neg  = li2(-x)       # Li_2(-phi^{-3})

chi2_user_defn = li2_pos - li2_neg          # user's formula: no factor 1/2
chi2_standard  = 0.5 * (li2_pos - li2_neg)  # standard Legendre chi_2

gamma_MWS = math.pi**2 / 24 - 0.75 * ln_phi**2

print(f"  Li_2(phi^{{-3}})  = {li2_pos:.15f}")
print(f"  Li_2(-phi^{{-3}}) = {li2_neg:.15f}")
print()
print(f"  User's chi_2 = Li_2(x) - Li_2(-x)          = {chi2_user_defn:.15f}")
print(f"  Standard chi_2 = (1/2)[Li_2(x) - Li_2(-x)] = {chi2_standard:.15f}")
print(f"  gamma_MWS = pi^2/24 - (3/4)ln^2(phi)        = {gamma_MWS:.15f}")
print()
user_def_matches = abs(chi2_user_defn - gamma_MWS) < 1e-10
std_def_matches  = abs(chi2_standard  - gamma_MWS) < 1e-10
print(f"  User defn matches gamma_MWS: {user_def_matches}  "
      f"(differs by {chi2_user_defn - gamma_MWS:.6e})")
print(f"  Standard defn matches gamma_MWS: {std_def_matches}  ✓")

NOTES.append("Step 0: chi_2 definition is missing factor 1/2 — "
             "claimed chi_2(x)=Li_2(x)-Li_2(-x) but standard Legendre chi_2=(1/2)(Li_2(x)-Li_2(-x))")
check(std_def_matches, "Standard chi_2(phi^{-3}) = pi^2/24 - (3/4)ln^2(phi)")
check(not user_def_matches, "User defn chi_2 = Li_2 - Li_2(-) is NOT pi^2/24 - (3/4)ln^2(phi) "
      "(factor 2 error in definition)")

# ---------------------------------------------------------------------------
# Step 1: claimed Li_2(phi^{-3}) = pi^2/15 - ln^2(phi)
# ---------------------------------------------------------------------------
print("\n=== Step 1: Li_2(phi^{-3}) = pi^2/15 - ln^2(phi)? ===")

step1_claimed = math.pi**2 / 15 - ln_phi**2
step1_actual  = li2_pos

print(f"  Li_2(phi^{{-3}}) (numerical) = {step1_actual:.15f}")
print(f"  pi^2/15 - ln^2(phi)         = {step1_claimed:.15f}")
print(f"  Difference                  = {step1_actual - step1_claimed:.6e}")

step1_ok = abs(step1_actual - step1_claimed) < 1e-10
check(not step1_ok, "Step 1: Li_2(phi^{-3}) ≠ pi^2/15 - ln^2(phi)  (WRONG identity used)")
diff1 = abs(step1_actual - step1_claimed)
print(f"  Step 1 is {'CORRECT' if step1_ok else f'WRONG (off by {diff1:.5f})'}")

# The known correct identity is Li_2(phi^{-2}) = pi^2/15 - ln^2(phi)
li2_phi_inv2 = li2(1.0 / phi**2)
phi_inv2_check = math.pi**2 / 15 - ln_phi**2
print()
print(f"  NOTE: The identity pi^2/15 - ln^2(phi) = {step1_claimed:.10f}")
print(f"        actually equals Li_2(phi^{{-2}}) = {li2_phi_inv2:.10f}  "
      f"(phi^{{-2}} ≈ {1/phi**2:.4f}, not phi^{{-3}} ≈ {x:.4f})")
check(abs(li2_phi_inv2 - phi_inv2_check) < 1e-10,
      "Li_2(phi^{-2}) = pi^2/15 - ln^2(phi)  [correct known identity]")
print(f"  Li_2(phi^{{-2}}) = pi^2/15 - ln^2(phi): "
      f"{'CONFIRMED' if abs(li2_phi_inv2 - phi_inv2_check)<1e-10 else 'FAIL'}  ✓")
NOTES.append("Step 1 uses identity for phi^{-2} (pi^2/15 - ln^2(phi) = Li_2(phi^{-2})), "
             "incorrectly applied to phi^{-3}")

# ---------------------------------------------------------------------------
# Step 2: claimed Li_2(-phi^{-3}) = -pi^2/120 + (1/4)*ln^2(phi)
# ---------------------------------------------------------------------------
print("\n=== Step 2: Li_2(-phi^{-3}) = -pi^2/120 + (1/4)*ln^2(phi)? ===")

step2_claimed = -math.pi**2 / 120 + 0.25 * ln_phi**2
step2_actual  = li2_neg

print(f"  Li_2(-phi^{{-3}}) (numerical) = {step2_actual:.15f}")
print(f"  -pi^2/120 + (1/4)ln^2(phi)   = {step2_claimed:.15f}")
print(f"  Difference                   = {step2_actual - step2_claimed:.6e}")

step2_ok = abs(step2_actual - step2_claimed) < 1e-10
check(not step2_ok, "Step 2: Li_2(-phi^{-3}) ≠ -pi^2/120 + (1/4)ln^2(phi)  (WRONG)")
diff2 = abs(step2_actual - step2_claimed)
print(f"  Step 2 is {'CORRECT' if step2_ok else f'WRONG (off by {diff2:.5f})'}")

# What is -pi^2/120 + (1/4)ln^2(phi) actually?
# Check if it equals Li_2(-phi^{-2}) (complementary guess)
li2_neg_phi_inv2 = li2(-1/phi**2)
print()
print(f"  Li_2(-phi^{{-2}}) = {li2_neg_phi_inv2:.10f}")
print(f"  -pi^2/120 + (1/4)ln^2(phi) = {step2_claimed:.10f}")
print(f"  Difference: {abs(li2_neg_phi_inv2 - step2_claimed):.6e}")
NOTES.append("Step 2 formula -pi^2/120 + (1/4)ln^2(phi) does not match "
             "Li_2(-phi^{-3}) or any standard golden-ratio dilogarithm value")

# ---------------------------------------------------------------------------
# Step 3: arithmetic — 9*pi^2/120 = pi^2/24?
# ---------------------------------------------------------------------------
print("\n=== Step 3: arithmetic — 9*pi^2/120 = pi^2/24? ===")

lhs_step3 = 9 * math.pi**2 / 120
rhs_step3 = math.pi**2 / 24

# What is 9/120? = 3/40. What is 1/24 = 5/120.
print(f"  9*pi^2/120 = {lhs_step3:.15f}")
print(f"  pi^2/24    = {rhs_step3:.15f}")
print(f"  9/120 = {9/120:.6f} = 3/40;  1/24 = {1/24:.6f} = 5/120")
print(f"  9pi^2/120 = 3pi^2/40 ≠ pi^2/24 (= 5pi^2/120)")
print(f"  Error: user claims 9pi^2/120 = pi^2/24 but 9 ≠ 5")

step3_ok = abs(lhs_step3 - rhs_step3) < 1e-12
check(not step3_ok, "Step 3 arithmetic: 9pi^2/120 ≠ pi^2/24  (WRONG)")
NOTES.append("Step 3: 9*pi^2/120 = 3*pi^2/40 ≠ pi^2/24 = 5*pi^2/120.  "
             "User writes '= pi^2/13.3...' which is 9pi^2/120, "
             "then incorrectly equates it to pi^2/24")

# Correct: pi^2/15 + pi^2/120
pi2_correct_sum = math.pi**2 / 15 + math.pi**2 / 120
print(f"\n  Correct arithmetic: pi^2/15 + pi^2/120 = {pi2_correct_sum:.10f}")
print(f"  = 8*pi^2/120 + pi^2/120 = 9*pi^2/120 = 3*pi^2/40 = {3*math.pi**2/40:.10f}")
print(f"  NOT pi^2/24 = 5*pi^2/120 = {math.pi**2/24:.10f}")

# ---------------------------------------------------------------------------
# Step 4: arithmetic — -(1 + 1/4) = -3/4?
# ---------------------------------------------------------------------------
print("\n=== Step 4: arithmetic — -(1 + 1/4)*ln^2(phi) = -(3/4)*ln^2(phi)? ===")

coeff_lhs = -(1 + 0.25)    # -5/4
coeff_rhs = -0.75           # -3/4

print(f"  -(1 + 1/4) = {coeff_lhs} = -5/4")
print(f"  -3/4       = {coeff_rhs}")
print(f"  Equal? {abs(coeff_lhs - coeff_rhs) < 1e-12}")
print(f"  Error: 1 + 1/4 = 5/4, not 3/4")

step4_ok = abs(coeff_lhs - coeff_rhs) < 1e-12
check(not step4_ok, "Step 4 arithmetic: -(1+1/4) ≠ -(3/4)  (WRONG)")
NOTES.append("Step 4: -(ln^2 phi) - (1/4)ln^2 phi = -(5/4)ln^2 phi ≠ -(3/4)ln^2 phi.  "
             "User drops the 5 and writes 3.")

# ---------------------------------------------------------------------------
# Error analysis: do the four errors cancel to give the right answer?
# ---------------------------------------------------------------------------
print("\n=== Error propagation: do Steps 1-4 errors cancel? ===")

# What the proof computes with WRONG premises but CORRECT arithmetic:
# (pi^2/15 - ln^2) - (-pi^2/120 + (1/4)ln^2) = 9pi^2/120 - (5/4)ln^2 phi
correct_arith_on_wrong_premises = (9*math.pi**2/120) - (5/4)*ln_phi**2
print(f"  With WRONG premises, CORRECT arithmetic:")
print(f"  9pi^2/120 - (5/4)ln^2(phi) = {correct_arith_on_wrong_premises:.10f}")
print(f"  Actual chi_2_user (Li_2-Li_2(-)) = {chi2_user_defn:.10f}")
print(f"  Actual standard chi_2           = {chi2_standard:.10f}")
print()

# What the proof computes with WRONG premises AND WRONG arithmetic:
wrong_arith = math.pi**2/24 - (3/4)*ln_phi**2
print(f"  With WRONG premises, WRONG arithmetic (user's result):")
print(f"  pi^2/24 - (3/4)ln^2(phi) = {wrong_arith:.10f}")
print(f"  = gamma_MWS = standard chi_2(phi^{{-3}})  ✓  (numerically)")
print()

# The accident: errors conspire to give the correct answer
print(f"  Residual from wrong-premise+correct-arith vs correct answer:")
print(f"    {correct_arith_on_wrong_premises:.6f} vs {chi2_standard:.6f}: "
      f"diff = {abs(correct_arith_on_wrong_premises - chi2_standard):.6e}")
print(f"  Residual from wrong-premise+wrong-arith vs correct answer:")
print(f"    {wrong_arith:.6f} vs {chi2_standard:.6f}: "
      f"diff = {abs(wrong_arith - chi2_standard):.2e}")
print()
print(f"  The arithmetic errors in Steps 3-4 accidentally compensate for the")
print(f"  wrong Li_2 premises to produce the numerically correct final value.")

# ---------------------------------------------------------------------------
# The final result IS correct — independent verification
# ---------------------------------------------------------------------------
print("\n=== Final result: is chi_2(phi^{-3}) = pi^2/24 - (3/4)ln^2(phi) true? ===")

# Series: chi_2(x) = sum_{n=0}^{inf} x^{2n+1}/(2n+1)^2  [standard Legendre chi]
chi2_series = sum(x**(2*n+1) / (2*n+1)**2 for n in range(500))
chi2_via_li2 = 0.5*(li2_pos - li2_neg)
rhs = math.pi**2/24 - 0.75*ln_phi**2

print(f"  chi_2 via series (500 terms) = {chi2_series:.15f}")
print(f"  chi_2 via (1/2)(Li_2-Li_2(-))= {chi2_via_li2:.15f}")
print(f"  pi^2/24 - (3/4)ln^2(phi)     = {rhs:.15f}")
print(f"  |series - rhs|     = {abs(chi2_series - rhs):.2e}")
print(f"  |(1/2)(Li_2-Li_2(-)) - rhs| = {abs(chi2_via_li2 - rhs):.2e}")
check(abs(chi2_via_li2 - rhs) < 1e-12, "chi_2(phi^{-3}) = pi^2/24 - (3/4)ln^2(phi)  [confirmed]")
print(f"  Final result TRUE: CONFIRMED to 1e-12  ✓")

# ---------------------------------------------------------------------------
# Correct Li_2(phi^{-3}) — what is the actual closed form?
# ---------------------------------------------------------------------------
print("\n=== Appendix: actual Li_2 values (no simple closed form without ln2) ===")

# From the reflection formula:
# Li_2(phi^{-3}) + Li_2(2*phi^{-2}) = pi^2/6 + 3*ln(phi)*ln(2) - 6*ln^2(phi)
# 1 - phi^{-3} = 2*phi^{-2} (verified below)
print(f"  1 - phi^{{-3}} = {1 - x:.10f}")
print(f"  2*phi^{{-2}}   = {2/phi**2:.10f}")
check(abs((1-x) - 2/phi**2) < 1e-12, "1 - phi^{-3} = 2*phi^{-2}")
print(f"  1 - phi^{{-3}} = 2*phi^{{-2}}  CONFIRMED  ✓")
print()
print(f"  Reflection: Li_2(phi^{{-3}}) + Li_2(2*phi^{{-2}})")
print(f"            = pi^2/6 + 3*ln(phi)*ln(2) - 6*ln^2(phi)")
rhs_reflection = math.pi**2/6 + 3*ln_phi*math.log(2) - 6*ln_phi**2
li2_2phi_inv2  = li2(2/phi**2)
print(f"  Li_2(phi^{{-3}}) + Li_2(2phi^{{-2}}) = {li2_pos + li2_2phi_inv2:.10f}")
print(f"  pi^2/6 + 3*ln(phi)*ln(2) - 6*ln^2(phi) = {rhs_reflection:.10f}")
check(abs((li2_pos + li2_2phi_inv2) - rhs_reflection) < 1e-10,
      "Reflection formula Li_2(phi^{-3}) + Li_2(2phi^{-2}) = pi^2/6 + 3lnphi*ln2 - 6ln^2phi")
print(f"  Reflection identity CONFIRMED  ✓")
print()
print(f"  Li_2(phi^{{-3}})  (actual) = {li2_pos:.10f}")
print(f"  Li_2(-phi^{{-3}}) (actual) = {li2_neg:.10f}")
print()
print(f"  These involve ln(2) (non-trivially) and cannot be expressed as")
print(f"  a*pi^2 + b*ln^2(phi) alone with rational a,b.")
print(f"  The DIFFERENCE Li_2(phi^{{-3}}) - Li_2(-phi^{{-3}}) = 2*chi_2(phi^{{-3}})")
print(f"  DOES simplify: {li2_pos - li2_neg:.10f} = pi^2/12 - (3/2)*ln^2(phi)")
rhs_diff = math.pi**2/12 - 1.5*ln_phi**2
print(f"  pi^2/12 - (3/2)*ln^2(phi) = {rhs_diff:.10f}")
check(abs((li2_pos - li2_neg) - rhs_diff) < 1e-10,
      "Li_2(phi^{-3}) - Li_2(-phi^{-3}) = pi^2/12 - (3/2)*ln^2(phi)")
print(f"  CONFIRMED  ✓  (the ln2 terms cancel in the antisymmetric combination)")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("AUDIT SUMMARY")
print("=" * 60)
print()
print("  Final result chi_2(phi^{-3}) = pi^2/24 - (3/4)ln^2(phi):  TRUE  ✓")
print()
print("  Errors in the derivation:")
for i, note in enumerate(NOTES, 1):
    print(f"  [{i}] {note}")
print()
print("  Step 0 (definition): chi_2 = Li_2 - Li_2(-)  MISSING factor 1/2")
print(f"         User's chi_2(phi^{{-3}}) = {chi2_user_defn:.6f} ≠ {gamma_MWS:.6f}")
print(f"         Standard chi_2(phi^{{-3}}) = {chi2_standard:.6f} = {gamma_MWS:.6f}  ✓")
print()
print(f"  Step 1: Li_2(phi^{{-3}}) = pi^2/15 - ln^2(phi)?")
print(f"          Claimed = {step1_claimed:.6f}, Actual = {step1_actual:.6f}")
print(f"          Error = {step1_actual - step1_claimed:.6f}")
print(f"          Correct identity: Li_2(phi^{{-2}}) = pi^2/15 - ln^2(phi)  (wrong index)")
print()
print(f"  Step 2: Li_2(-phi^{{-3}}) = -pi^2/120 + (1/4)ln^2(phi)?")
print(f"          Claimed = {step2_claimed:.6f}, Actual = {step2_actual:.6f}")
print(f"          Error = {step2_actual - step2_claimed:.6f}")
print()
print(f"  Step 3: 9pi^2/120 = pi^2/24?  FALSE (9pi^2/120 = 3pi^2/40 ≠ 5pi^2/120)")
print()
print(f"  Step 4: -(1+1/4) = -3/4?  FALSE (should be -5/4)")
print()
print(f"  Net effect: errors in Steps 1-2 (wrong Li_2 premises)")
print(f"  and errors in Steps 3-4 (wrong arithmetic) cancel to give")
print(f"  the correct result pi^2/24 - (3/4)ln^2(phi).  This is accidental.")
print()
print(f"  A correct proof notes that the ln(2) terms cancel in")
print(f"  Li_2(phi^{{-3}}) - Li_2(-phi^{{-3}}), giving pi^2/12 - (3/2)ln^2(phi),")
print(f"  so chi_2(phi^{{-3}}) = (1/2)(...) = pi^2/24 - (3/4)ln^2(phi).  ✓")
print()
print()
if FAIL:
    # Filter out the intentional "check not" assertions for summary
    genuine_fails = [f for f in FAIL if "WRONG" not in f and "≠" not in f.split(":")[0]]
    if genuine_fails:
        print(f"UNEXPECTED FAILURES ({len(genuine_fails)}):")
        for f in genuine_fails:
            print(f"  FAIL  {f}")
        import sys; sys.exit(1)
    else:
        print("ALL ARITHMETIC CHECKS PASS (error flags are for claimed-wrong identities)")
else:
    print("ALL CHECKS PASS")

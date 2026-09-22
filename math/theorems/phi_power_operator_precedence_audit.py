# math/theorems/phi_power_operator_precedence_audit.py
"""
φ Power Calculations — Operator Precedence Audit

Audits two submitted Python scripts computing φ-based values.

─────────────────────────────────────────────────────────────────────────────
SCRIPT 1 — THREE COMPUTATIONS (submitted for audit)
─────────────────────────────────────────────────────────────────────────────
  Line 1: print("PHI cubed:", (1 + math.sqrt(5))/2 ** 3)
  Line 2: print("108 degrees to radians:", 108 * math.pi / 180)
  Line 3: print("log_phi of 3.12 approx:", math.log(3.12) / math.log((1 + math.sqrt(5))/2))

  Line 1 — BUG (operator precedence):
    Python evaluates ** before /
    Parsed as: (1 + sqrt(5)) / (2**3) = (1 + sqrt(5)) / 8 ≈ 0.4045
    Label says "PHI cubed"; φ³ = 4.2361
    Off by factor of 10.47
    Fix: ((1 + math.sqrt(5)) / 2) ** 3

  Line 2 — CORRECT:
    108 * π / 180 = 3π/5 ≈ 1.8850 radians
    Interior angle of a regular pentagon. Standard result.

  Line 3 — CORRECT:
    log_φ(3.12) = ln(3.12)/ln(φ) — change-of-base formula applied properly.
    Parentheses protect the φ computation: (1 + sqrt(5))/2 = φ correctly.
    Result ≈ 2.365 (consistent: φ² = 2.618 < 3.12 < 4.236 = φ³, so 2 < log < 3)

─────────────────────────────────────────────────────────────────────────────
SCRIPT 2 — φ^20 CALCULATION (submitted for audit)
─────────────────────────────────────────────────────────────────────────────
  phi = (1 + math.sqrt(5)) / 2
  print(phi ** 20)

  Status: CORRECT.
  Parentheses placed properly; φ is computed before exponentiation.
  Expected output: 15126.999999... (≈ L(20) − ψ^20 where L(20)=15127)

─────────────────────────────────────────────────────────────────────────────
LUCAS NUMBER VERIFICATION
─────────────────────────────────────────────────────────────────────────────
  φ^n + ψ^n = L(n)  where ψ = (1−√5)/2 ≈ −0.6180, L(n) = Lucas sequence
  |ψ| < 1 → ψ^20 is small and positive (even exponent)
  φ^20 = L(20) − ψ^20 = 15127 − ψ^20
  ψ^20 ≈ 0.618^20 ≈ 6.6 × 10⁻⁵
  → φ^20 ≈ 15126.9999339
"""

import math

phi = (1 + math.sqrt(5)) / 2
psi = (1 - math.sqrt(5)) / 2

# ── Script 1 audit ────────────────────────────────────────────────────────────

# Line 1: what the submitted code actually computes
submitted_line1 = (1 + math.sqrt(5)) / 2 ** 3      # operator precedence bug
correct_phi_cubed = ((1 + math.sqrt(5)) / 2) ** 3  # correct

assert abs(submitted_line1 - 0.4045) < 0.001, f"Unexpected: {submitted_line1}"
assert abs(correct_phi_cubed - 4.2361) < 0.001, f"Unexpected: {correct_phi_cubed}"
assert correct_phi_cubed / submitted_line1 > 10  # >10x difference

# Line 2: 108 degrees in radians
val_108_rad = 108 * math.pi / 180
assert abs(val_108_rad - 3 * math.pi / 5) < 1e-12   # = 3π/5 exactly
assert abs(val_108_rad - 1.8849556) < 1e-6

# Line 3: log_phi(3.12)
log_phi_312 = math.log(3.12) / math.log(phi)
assert 2.0 < log_phi_312 < 3.0      # must be between 2 and 3 (φ²<3.12<φ³)
assert abs(log_phi_312 - 2.365) < 0.001

# ── Script 2 audit ────────────────────────────────────────────────────────────

phi20 = phi ** 20
psi20 = psi ** 20   # positive: even exponent, psi negative

# Lucas numbers up to L(20)
L = [0, 2, 1]
for i in range(3, 21):
    L.append(L[-1] + L[-2])
# L[1]=2 (convention: L(1)=1 in some sources; using L[0]=2,L[1]=1 recurrence)
# Use Fibonacci-based identity instead:
# φ^n = F(n)·φ + F(n-1)
F = [0, 1, 1]
for i in range(3, 22):
    F.append(F[-1] + F[-2])

phi20_exact_approx = F[20] * phi + F[19]   # = 6765φ + 4181
assert abs(phi20 - phi20_exact_approx) < 1e-6

# Lucas sequence (correct definition: L(1)=1, L(2)=3)
lucas = [0, 1, 3]
for i in range(3, 21):
    lucas.append(lucas[-1] + lucas[-2])

L20 = lucas[20]   # = 15127
assert L20 == 15127

# φ^20 + ψ^20 = L(20)
assert abs(phi20 + psi20 - L20) < 1e-6

# φ^20 is just below 15127
assert 15126.999 < phi20 < 15127.0
assert psi20 > 0       # even power
assert psi20 < 1e-3    # small because |ψ| < 1


if __name__ == "__main__":
    print("φ Power Calculations — Operator Precedence Audit")
    print()
    print("Script 1 — Line 1 (PHI cubed):")
    print(f"  Submitted code computes: (1+√5)/8 = {submitted_line1:.6f}")
    print(f"  Label says 'PHI cubed':  φ³       = {correct_phi_cubed:.6f}")
    print(f"  Ratio:                             = {correct_phi_cubed/submitted_line1:.4f}×  ← bug")
    print(f"  Cause: ** binds tighter than /; need extra parentheses")
    print()
    print("Script 1 — Line 2 (108° to radians):")
    print(f"  108 × π/180 = 3π/5 = {val_108_rad:.7f}  ✓")
    print()
    print("Script 1 — Line 3 (log_φ 3.12):")
    print(f"  log_φ(3.12) = {log_phi_312:.6f}  (between 2 and 3, consistent with φ²<3.12<φ³)  ✓")
    print()
    print("Script 2 — φ^20:")
    print(f"  φ^20 = {phi20:.10f}")
    print(f"  ψ^20 = {psi20:.10f}")
    print(f"  φ^20 + ψ^20 = {phi20 + psi20:.6f}  (= L(20) = {L20})  ✓")
    print(f"  Code is correct; parentheses placed properly.")
    print()
    print("All assertions passed.")

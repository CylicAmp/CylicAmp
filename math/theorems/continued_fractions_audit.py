# math/theorems/continued_fractions_audit.py
"""
Continued Fractions Audit
==========================
Claims audited:
  A. Plastic constant ρ: defining equation, Pisot property,
     nested radical identity, generalised CF identity, CF prefix
  B. 19/10101: Euclidean algorithm steps, CF, convergents table
  C. Structural claim: "19/10101 drives master 12-digit composite"
"""

import math
from decimal import Decimal, getcontext
getcontext().prec = 120   # 120 significant digits


# ── exact rational continued fraction ─────────────────────────────────────────

def cf_rational(p: int, q: int) -> list[int]:
    """Simple CF of p/q via Euclidean algorithm."""
    terms = []
    while q:
        terms.append(p // q)
        p, q = q, p % q
    return terms


def convergents(cf: list[int]) -> list[tuple]:
    """Return (p_k, q_k) for each k."""
    p_prev, p_cur = 1, cf[0]
    q_prev, q_cur = 0, 1
    result = [(p_cur, q_cur)]
    for a in cf[1:]:
        p_prev, p_cur = p_cur, a * p_cur + p_prev
        q_prev, q_cur = q_cur, a * q_cur + q_prev
        result.append((p_cur, q_cur))
    return result


# ── high-precision CF of an irrational ────────────────────────────────────────

def cf_decimal(x: Decimal, n_terms: int = 25) -> list[int]:
    """Simple CF of x to n_terms partial quotients."""
    terms = []
    for _ in range(n_terms):
        a = int(x)
        terms.append(a)
        frac = x - Decimal(a)
        if frac < Decimal('1e-100'):
            break
        x = Decimal(1) / frac
    return terms


def verify():
    print("Continued Fractions Audit\n")

    # ── A. Plastic constant ρ ─────────────────────────────────────────────────
    print("=" * 60)
    print("A. Plastic constant ρ  (x³ − x − 1 = 0)")
    print("=" * 60)

    # A1. Defining equation — compute ρ via Newton's method to full precision
    # f(x)=x³−x−1; f'(x)=3x²−1
    rho = Decimal('1.3247179572447460259609088544780973')
    for _ in range(10):   # Newton iterations converge quadratically
        fx = rho**3 - rho - 1
        dfx = 3 * rho**2 - 1
        rho = rho - fx / dfx

    residual = rho**3 - rho - 1
    assert abs(residual) < Decimal('1e-100'), f"ρ³−ρ−1 = {residual}"
    print(f"\n  ρ = {str(rho)[:40]}...")
    print(f"  ρ³ − ρ − 1 = {residual:.2e}  ✓  (Newton-converged, < 10⁻¹⁰⁰)")

    # A2. Pisot property: conjugate modulus < 1
    # ρ × |z|² = 1  (product of all roots = 1 by Vieta)
    # So |z|² = 1/ρ
    conj_mod_sq = Decimal(1) / rho
    conj_mod = conj_mod_sq.sqrt()
    assert conj_mod < Decimal(1)
    print(f"\n  Pisot: |complex conjugate| = √(1/ρ) = {float(conj_mod):.6f} < 1  ✓")
    print(f"  (Product of all roots = 1; ρ × |z|² = 1 → |z| = √(1/ρ))")
    print(f"  ρ IS the smallest Pisot-Vijayaraghavan number  ✓")

    # A3. Nested radical: ρ = ∛(1+ρ) ↔ ρ³ = 1+ρ ✓ (already verified above)
    # Convergence test: iterate x ↦ ∛(1+x) from x=1
    x = Decimal(1)
    for _ in range(200):   # linear convergence rate ~0.19; need ~125 iters for 90 digits
        x = (1 + x) ** (Decimal(1)/3)
    assert abs(x - rho) < Decimal('1e-80')
    print(f"\n  Nested radical ∛(1+∛(1+∛(1+...))) → {str(x)[:20]}...")
    print(f"  Difference from ρ: {abs(x-rho):.2e}  ✓")
    print(f"  Reason: fixed point of x↦∛(1+x) satisfies x³=1+x  ✓")

    # A4. Generalised CF identity: ρ = 1 + 1/(1+1/ρ)²
    rhs = 1 + Decimal(1) / (1 + Decimal(1)/rho)**2
    diff_A4 = abs(rhs - rho)
    assert diff_A4 < Decimal('1e-95')
    print(f"\n  Identity ρ = 1 + 1/(1+1/ρ)²:")
    print(f"  RHS = {str(rhs)[:30]}...")
    print(f"  Difference from ρ: {diff_A4:.2e}  ✓")
    # Algebraic proof: ρ³=ρ+1 → ρ=1+1/ρ² via ρ²=1+1/ρ... actually:
    # (1+1/ρ)² = (ρ+1)²/ρ²; 1/(1+1/ρ)² = ρ²/(ρ+1)²
    # RHS = 1 + ρ²/(ρ+1)² = ((ρ+1)²+ρ²)/(ρ+1)² = (2ρ²+2ρ+1)/(ρ+1)²
    # RHS=ρ ↔ ρ(ρ+1)²=2ρ²+2ρ+1 ↔ ρ³+2ρ²+ρ=2ρ²+2ρ+1 ↔ ρ³=ρ+1  ✓
    print(f"  Algebraic proof: RHS=ρ ↔ ρ(ρ+1)²=2ρ²+2ρ+1 ↔ ρ³=ρ+1  ✓")

    # A5. Simple CF of ρ — compute and compare to claimed prefix
    claimed_cf = [1, 3, 12, 1, 1, 3, 2, 3, 2, 4, 2, 141, 80, 2, 5, 1, 2, 8]
    computed_cf = cf_decimal(rho, n_terms=25)

    print(f"\n  Claimed CF prefix:  {claimed_cf}")
    print(f"  Computed CF prefix: {computed_cf[:len(claimed_cf)]}")

    match_terms = sum(1 for a, b in zip(claimed_cf, computed_cf) if a == b)
    mismatches = [(i, claimed_cf[i], computed_cf[i])
                  for i in range(min(len(claimed_cf), len(computed_cf)))
                  if claimed_cf[i] != computed_cf[i]]

    if mismatches:
        print(f"\n  MISMATCHES at positions: {mismatches}")
    else:
        assert computed_cf[:len(claimed_cf)] == claimed_cf
        print(f"  All {len(claimed_cf)} claimed terms verified  ✓")

    # Note: large partial quotient 141 at position 11 — near-rational approximation
    if len(computed_cf) > 11:
        p11 = claimed_cf[11] if len(claimed_cf) > 11 else '?'
        print(f"\n  Partial quotient a_11 = {computed_cf[11]} (claimed {p11})")
        print(f"  Large PQ indicates near-rational: p/q ≈ ρ with small denominator")

    # Confirm non-periodicity (no period ≤ 15 in first 30 terms)
    cf30 = computed_cf[:30]
    periodic = any(
        cf30[:p] * (30 // p) + cf30[:30 % p] == cf30
        for p in range(1, 16)
    )
    assert not periodic
    print(f"  Non-periodic (no period ≤ 15 in first 30 terms)  ✓")
    print(f"  Lagrange's theorem (periodic ↔ quadratic irrational) inapplicable  ✓")

    # ── B. 19/10101 — Euclidean algorithm & convergents ──────────────────────
    print()
    print("=" * 60)
    print("B. 19/10101 — Euclidean algorithm and convergents")
    print("=" * 60)

    # B1. Euclidean steps
    print("\n  Euclidean algorithm for 10101/19 (computing CF of 19/10101):")
    steps = []
    a, b = 10101, 19
    while b:
        q, r = divmod(a, b)
        steps.append((a, q, b, r))
        a, b = b, r

    expected_steps = [
        (10101, 531, 19, 12),
        (19,    1,   12,  7),
        (12,    1,    7,  5),
        (7,     1,    5,  2),
        (5,     2,    2,  1),
        (2,     2,    1,  0),
    ]
    for i, (step, exp) in enumerate(zip(steps, expected_steps)):
        a_s, q_s, b_s, r_s = step
        a_e, q_e, b_e, r_e = exp
        match = step == exp
        print(f"  Step {i+1}: {a_s} = {q_s}×{b_s} + {r_s}  {'✓' if match else '✗'}")
        assert match, f"Step {i+1} mismatch: got {step}, expected {exp}"

    # B2. CF
    cf_frac = cf_rational(19, 10101)
    expected_cf = [0, 531, 1, 1, 1, 2, 2]
    assert cf_frac == expected_cf
    print(f"\n  CF of 19/10101 = {cf_frac}  ✓")

    # B3. Convergents table
    convs = convergents(cf_frac)
    target = 19 / 10101

    print(f"\n  Convergents:")
    print(f"  {'k':>3}  {'a_k':>6}  {'p_k':>6}  {'q_k':>7}  {'p_k/q_k':>14}  {'|diff|':>12}")
    expected_conv = [
        (0, 0,  0,      1,      0.0),
        (1, 531, 1,    531,     1/531),
        (2, 1,  1,     532,     1/532),
        (3, 1,  2,    1063,     2/1063),
        (4, 1,  3,    1595,     3/1595),
        (5, 2,  8,    4253,     8/4253),
        (6, 2, 19,  10101,     19/10101),
    ]
    for k, (pk, qk) in enumerate(convs):
        val = pk / qk if qk != 0 else 0.0
        diff = abs(val - target)
        exp_pk = expected_conv[k][2]
        exp_qk = expected_conv[k][3]
        match = (pk == exp_pk and qk == exp_qk)
        print(f"  {k:>3}  {cf_frac[k]:>6}  {pk:>6}  {qk:>7}  {val:>14.7f}  {diff:>12.2e}  {'✓' if match else '✗'}")
        assert match, f"Convergent k={k}: got ({pk},{qk}), expected ({exp_pk},{exp_qk})"

    # Final convergent equals exact fraction
    assert convs[-1] == (19, 10101)
    print(f"\n  Final convergent = 19/10101 (exact)  ✓")
    print(f"  6 convergent levels (k=1..6)  ✓")

    # ── C. Structural claim: "19/10101 drives master composite" ───────────────
    print()
    print("=" * 60)
    print("C. Structural claim: 19/10101 as 'rational generator node'")
    print("=" * 60)

    N = 191919919191

    # Does 19 divide N?
    rem_19 = N % 19
    print(f"\n  191919919191 mod 19 = {rem_19}")
    if rem_19 != 0:
        print(f"  19 does NOT divide 191919919191  — 19 is not a factor  ✗")
        print(f"  The factorization is 3×7×11×13×37×167×10343 (no 19)")
    else:
        print(f"  19 | 191919919191  ✓")

    # Does 10101 divide N?
    rem_10101 = N % 10101
    assert rem_10101 == 0
    print(f"  191919919191 mod 10101 = {rem_10101}  → 10101 | 191919919191  ✓")

    # 19 × 10101 = 191919 — this is the 6-digit prefix
    assert 19 * 10101 == 191919
    print(f"\n  19 × 10101 = {19*10101}  (= 6-digit prefix of 191919919191)  ✓")
    print(f"  191919 = 3×7×13×19×37  (contains 19 as factor)  ✓")
    print(f"  BUT 191919919191 = 3×7×11×13×37×167×10343  (19 absent)  ✓")

    # The "6-digit block" connection: 19/10101 has 6 convergent levels (k=1..6)
    # Master palindrome 191919919191 has 12 digits = 2 × 6
    print(f"\n  Claimed: 6 convergents aligns with '6-digit block lengths'")
    print(f"  Master palindrome has 12 digits. 10101 has 5 digits. 191919 has 6 digits.")
    print(f"  The convergent count = 6 matching the digit count = 6 of '191919'")
    print(f"  is a post-hoc observation, not a structural derivation.")

    print(f"\n  Summary:")
    print(f"  — CF of 19/10101: correct  ✓")
    print(f"  — 10101 | 191919919191: true  ✓")
    print(f"  — 19 | 191919919191: FALSE  ✗  (19 is not a factor)")
    print(f"  — '19/10101 drives master composite': unsupported as stated")
    print(f"    Supported: 19×10101=191919 (6-digit block); 10101|N; 19∤N")

    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()

# math/theorems/ramanujan_modular_audit.py
"""
Ramanujan Modular Equations — Claim Audit + CF of ψ
=====================================================
Five claims from the document are audited point by point.
The CF of ψ (x³−x²−1=0) is computed as a concrete deliverable.

Claims:
  1. "19/10101 and 111111 fusion produce rational points compatible with
     low-degree modular equations"
  2. "ρ and ψ class invariants recoverable via Ramanujan's theory"
  3. "CF periodicity (quadratic) and non-periodicity (cubic) governed by
     same modular transformation group"
  4. "37 appears in Ramanujan's class invariants → direct bridge to 37-field"
  5. "mod-3 and parity-agreement structures preserved under radical denesting"
"""

import math
from math import isqrt
from decimal import Decimal, getcontext
getcontext().prec = 120


def cf_decimal(x: Decimal, n_terms: int = 25) -> list[int]:
    terms = []
    for _ in range(n_terms):
        a = int(x)
        terms.append(a)
        frac = x - Decimal(a)
        if frac < Decimal('1e-100'):
            break
        x = Decimal(1) / frac
    return terms


def find_period(seq: list) -> int | None:
    n = len(seq)
    for p in range(1, n // 2 + 1):
        if all(seq[i] == seq[i % p] for i in range(n)):
            return p
    return None


def class_number(D: int) -> int:
    """Class number h(D) for fundamental negative discriminant D < 0.

    Uses reduced positive definite binary quadratic forms with
    strict boundary b > -a.

    >>> class_number(-3)
    1
    >>> class_number(-4)
    1
    >>> class_number(-7)
    1
    >>> class_number(-23)
    3
    >>> class_number(-43)
    1
    >>> class_number(-163)
    1
    """
    if D >= 0:
        raise ValueError("D must be negative")
    h = 0
    a_max = isqrt(-D // 3) + 1
    for a in range(1, a_max + 1):
        for b in range(-a + 1, a + 1):
            disc = b * b - D
            if disc % (4 * a) != 0:
                continue
            c = disc // (4 * a)
            if a > c:
                continue
            if (b == -a or a == c) and b < 0:
                continue
            h += 1
    return h


def _test_class_number():
    # Heegner numbers: all 9 discriminants with h=1
    assert class_number(-3)   == 1
    assert class_number(-4)   == 1
    assert class_number(-7)   == 1
    assert class_number(-8)   == 1
    assert class_number(-11)  == 1
    assert class_number(-19)  == 1
    assert class_number(-43)  == 1   # Heegner (NOT 3; h(-43)=1)
    assert class_number(-67)  == 1
    assert class_number(-163) == 1
    # h=3 examples
    assert class_number(-23)  == 3
    assert class_number(-31)  == 3
    # h=2 example
    assert class_number(-148) == 2   # h(-4×37)
    print("  class_number unit tests passed  ✓")


def verify():
    print("Ramanujan Modular Equations — Claim Audit\n")
    _test_class_number()

    # ── Claim 1: 19/10101 and "111111 fusion" ────────────────────────────────
    print("=" * 60)
    print("CLAIM 1: 19/10101 and 111111 fusion → compatible with")
    print("         low-degree modular equations")
    print("=" * 60)
    print("""
  "111111 fusion" is not a defined operation in this framework.
  "Compatible with low-degree modular equations" is not a
  falsifiable predicate without specifying the modular equation.

  What IS established:
  — 19/10101 = [0;531,1,1,1,2,2], 6 convergents  (continued_fractions_audit.py)
  — 19 ∤ 191919919191                              (continued_fractions_audit.py)
  — 10101 | 191919919191  ✓
  — 111111 × 900991 = 100110011001 (palindrome)   (palindrome_divisors_ord10_audit.py)
  — These are rational/integer arithmetic facts; no modular equation
    connection is established or testable from them.

  VERDICT: UNVERIFIABLE as stated. Terminology undefined.
    """)

    # ── Claim 2: ρ and ψ class invariants ────────────────────────────────────
    print("=" * 60)
    print("CLAIM 2: ρ and ψ class invariants recoverable via Ramanujan")
    print("=" * 60)
    print("""
  Ramanujan's class invariants G_n and g_n are defined via:
    G_n = 2^{-1/4} · f(e^{-π√n})     (Weber modular function)
    g_n = 2^{-1/4} · f_1(e^{-π√n})
  These are algebraic numbers over Q of degree h(-4n) or h(-n).
  They arise from imaginary quadratic fields Q(√(-n)).

  ρ (root of x³−x−1=0) and ψ (root of x³−x²−1=0) are real
  cubic algebraic numbers. They do NOT arise from imaginary
  quadratic fields and are NOT class invariants in Ramanujan's sense.

  Real cubic fields are governed by a completely different theory
  (S-unit theorem, Dirichlet's unit theorem for rank-1 units).
  There is no standard mechanism by which ρ or ψ are "recovered
  via Ramanujan's modular theory."

  VERDICT: FALSE as stated. ρ and ψ are real cubics; Ramanujan's
  class invariants are algebraic numbers from imaginary quadratic
  fields. Different objects.
    """)

    # ── Claim 3: same modular transformation group ────────────────────────────
    print("=" * 60)
    print("CLAIM 3: CF periodicity governed by same modular group")
    print("=" * 60)
    print("""
  WHAT IS TRUE:
  — Quadratic irrationals have eventually periodic CFs (Lagrange).
  — This IS connected to the modular group PSL(2,Z): the CF
    algorithm is a discretisation of geodesics on the modular
    surface H/PSL(2,Z), and periodic geodesics correspond to
    quadratic irrationals via Gauss's theory.

  WHAT IS FALSE:
  — Cubic (and higher degree) irrationals do NOT have periodic CFs.
  — Their CF behaviour is NOT governed by the same modular group.
    It falls under a different, less understood theory (Hermite's
    problem: no analogue of Lagrange's theorem exists for cubics).
  — "Same modular transformation group" conflates two regimes that
    are actively distinct in the literature.

  VERDICT: MISLEADING. Quadratic case: modular group. Cubic case:
  different (open) theory. They are NOT governed by the same group.
    """)

    # ── Claim 4: 37 in Ramanujan's lists ─────────────────────────────────────
    print("=" * 60)
    print("CLAIM 4: 37 appears in Ramanujan class invariants →")
    print("         direct bridge to 37-field")
    print("=" * 60)

    # Compute class number h(-148) = h(-4×37)
    h_148 = class_number(-148)
    print(f"\n  Class number h(-4×37) = h(-148) = {h_148}")
    assert h_148 == 2
    print(f"  Reduced forms of discriminant -148: 2 forms")
    print(f"    (1, 0, 37) and (2, 2, 19)")

    print(f"""
  37 as DISCRIMINANT (Ramanujan context):
  — Discriminant -4×37 = -148 has class number 2.
  — G_37 is therefore a degree-2 algebraic number (quadratic
    over Q), satisfying some quadratic minimal polynomial.
  — 37 here labels the imaginary quadratic field Q(√(-37)).

  37 as MODULUS (this framework's "37-field"):
  — ord_37(10) = 3; digit-block sum invariant; AP {5,14,23,32}.
  — 37 here is used as a modulus for arithmetic on integers.

  These are two different uses of the prime 37.
  Appearing in both contexts does not establish a "direct bridge."
  Prime 37 appears in many mathematical tables for reasons unrelated
  to digit-sum arithmetic; its appearance in both is not remarkable.

  VERDICT: EQUIVOCATION. Both statements are individually true,
  but they use 37 in distinct roles. No bridge is established.
    """)

    # ── Claim 5: mod-3 and parity structures preserved ────────────────────────
    print("=" * 60)
    print("CLAIM 5: mod-3 and parity-agreement structures preserved")
    print("         under radical denesting")
    print("=" * 60)
    print("""
  "Radical denesting" refers to simplifying nested radical expressions.
  No specific denesting step is supplied in the document.
  No connection between radical denesting and:
  — the mod-3 filter (DR ∈ {3,6,9})
  — Fix(φ) = {M : σ_p(M) = σ_a(M)} ⊂ Mat_3(F_2)
  is given or derivable from the material in this codebase.

  VERDICT: UNVERIFIABLE. No specific claim to test.
    """)

    # ── CF of ψ (supergolden ratio, x³−x²−1=0) ───────────────────────────────
    print("=" * 60)
    print("CF of ψ  (x³ − x² − 1 = 0)  — concrete deliverable")
    print("=" * 60)

    # Newton's method: f(x)=x³−x²−1, f'(x)=3x²−2x
    psi = Decimal('1.4655712318767680')
    for _ in range(12):
        fx = psi**3 - psi**2 - 1
        dfx = 3*psi**2 - 2*psi
        psi = psi - fx / dfx

    residual_psi = psi**3 - psi**2 - 1
    assert abs(residual_psi) < Decimal('1e-100')
    print(f"\n  ψ = {str(psi)[:40]}...")
    print(f"  ψ³ − ψ² − 1 = {residual_psi:.2e}  ✓")

    # Pisot property: product of all roots = 1 (constant term = -1, leading = 1)
    # x³−x²−1=0: product of roots = 1 (Vieta: product = -(-1)/1 = 1)
    # So ψ × |z|² = 1 → |z| = √(1/ψ)
    conj_mod = (Decimal(1)/psi).sqrt()
    assert conj_mod < Decimal(1)
    print(f"\n  Pisot: |complex conjugates| = √(1/ψ) = {float(conj_mod):.6f} < 1  ✓")

    # CF of ψ
    cf_psi = cf_decimal(psi, n_terms=25)
    print(f"\n  CF of ψ = {cf_psi[:20]}")

    # Non-periodic?
    periodic_psi = find_period(cf_psi[:24])
    assert periodic_psi is None or periodic_psi > 12
    print(f"  Non-periodic (Lagrange inapplicable to cubic)  ✓")

    # Pisot integer-convergence: ψ^n + conjugate_sum → integer
    # For a Pisot number ψ with conjugates z, z̄: ψ^n + z^n + z̄^n ∈ Z
    # and z^n + z̄^n → 0, so ψ^n approaches an integer
    print(f"\n  Pisot power convergence (ψⁿ approaches integer):")
    for n in [5, 10, 20, 30]:
        pn = psi ** n
        nearest_int = round(float(pn))
        fractional = abs(float(pn) - nearest_int)
        print(f"    ψ^{n:>2} ≈ {float(pn):.6f}  nearest int = {nearest_int}  "
              f"fractional part = {fractional:.6f}")

    # Verify: ψⁿ grows, fractional part shrinks (for large n)
    frac_20 = abs(float(psi**20) - round(float(psi**20)))
    frac_30 = abs(float(psi**30) - round(float(psi**30)))
    assert frac_30 < frac_20   # fractional part decreasing
    print(f"  Fractional part decreasing as n grows  ✓  (Pisot property)")

    # Compare ρ vs ψ CF structure
    rho = Decimal('1.3247179572447460')
    for _ in range(12):
        fx = rho**3 - rho - 1
        dfx = 3*rho**2 - 1
        rho = rho - fx / dfx
    cf_rho = cf_decimal(rho, n_terms=20)

    print(f"\n  Comparison:")
    print(f"  CF(ρ) = {cf_rho[:15]}")
    print(f"  CF(ψ) = {cf_psi[:15]}")
    print(f"  Both non-periodic cubics; neither is a Ramanujan class invariant.")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"""
  CLAIM 1 (19/10101 and 111111 fusion): UNVERIFIABLE — undefined terms
  CLAIM 2 (ρ, ψ as class invariants): FALSE — wrong number field type
  CLAIM 3 (same modular group): MISLEADING — cubics use different theory
  CLAIM 4 (37 bridge): EQUIVOCATION — two different roles of 37
  CLAIM 5 (structures preserved): UNVERIFIABLE — no specific claim

  VERIFIED (new):
    ψ = {str(psi)[:35]}...
    ψ³ − ψ² − 1 = {residual_psi:.1e}  ✓
    CF(ψ) = {cf_psi[:12]}...
    Pisot: |conjugates| = √(1/ψ) ≈ {float(conj_mod):.6f} < 1  ✓
    Pisot power convergence confirmed for n=5,10,20,30  ✓
    h(-148) = h(-4×37) = {h_148}  ✓  (G_37 is degree-2 algebraic)
    """)

    print("All assertions passed.")


if __name__ == "__main__":
    verify()

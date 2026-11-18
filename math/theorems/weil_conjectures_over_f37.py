# CLASS: THEOREM
"""
The Weil conjectures over F_37: the Riemann Hypothesis that is a theorem
Author: Michael Warren Song (CyclicAmp)

The corpus works over a finite field.  Over finite fields the Riemann
Hypothesis is not open -- it is proved.  That is what the Weil conjectures say,
and F_37 is where this repository already lives.  This file states them, checks
the relevant one exhaustively over F_37, and marks exactly where the boundary
to the classical Riemann Hypothesis is, so the two are not conflated.

Orbits, dr and is_prime come from the repository core `functions.py`.  146 files
in this corpus carry their own hardcoded ORBITS dict; this one does not.

=== THE WEIL CONJECTURES (Weil, 1949) ===

For X a smooth projective variety of dimension n over F_q, define

    Z(X, t) = exp( sum_{m>=1} #X(F_{q^m}) t^m / m )

W1  RATIONALITY.      Z(X, t) is a rational function of t.
                      Proved by Dwork, 1960, p-adic analysis.
W2  FUNCTIONAL EQN.   Z(1/(q^n t)) = +- q^{n*chi/2} t^chi Z(t).
                      Proved by Grothendieck, etale cohomology, 1960s.
W3  RIEMANN HYPOTHESIS.
                      Z(X,t) = P_1 P_3 ... P_{2n-1} / (P_0 P_2 ... P_{2n}),
                      with P_i(t) = prod_j (1 - alpha_ij t) and
                      EVERY |alpha_ij| = q^{i/2}.
                      Proved by Deligne, 1974.  Fields Medal, 1978.
W4  BETTI NUMBERS.    deg P_i equals the i-th Betti number of a lift to
                      characteristic zero.  Grothendieck / Deligne.

All four are theorems.  None is open.

=== W3 FOR CURVES, WHICH IS THE CASE F_37 GIVES DIRECTLY ===

For an elliptic curve E / F_q the zeta function is

    Z(E, t) = (1 - a t + q t^2) / ((1 - t)(1 - q t)),    a = q + 1 - #E(F_q)

and W3 reduces to: the two roots of the numerator, written
(1 - alpha t)(1 - beta t), satisfy |alpha| = |beta| = sqrt(q).  Equivalently
the Hasse bound |a| <= 2 sqrt(q), proved by Hasse in 1933 for elliptic curves,
before Weil stated the general conjectures.

VERIFIED EXHAUSTIVELY OVER F_37.  All 1332 non-singular curves
y^2 = x^3 + Ax + B with A, B in F_37 and 4A^3 + 27B^2 nonzero:

    largest |a| found            12
    2 sqrt(37)                   12.1655...
    floor(2 sqrt(37))            12          -- so the bound is TIGHT
    curves attaining |a| = 12    18 of 1332
    curves with |alpha| = sqrt37 1332 of 1332

AND IT IS EXACT, NOT NUMERICAL.  alpha beta = q = 37, and a^2 - 4q < 0 for
every curve (that is the Hasse bound), so alpha and beta are a complex
conjugate pair.  Then

    |alpha|^2 = alpha * conj(alpha) = alpha * beta = q = 37.

Two lines.  All 1332 curves have a^2 < 4q, checked, so none is an exception.

=== A CURVE ALREADY IN THIS CORPUS SITS ON THE BOUND ===

T254 names three curves over F_37.  All three re-verified here:

    ANOM   y^2 = x^3 + 5x       #E = 26   a = 12
    TWIN   y^2 = x^3 + 2x + 1   #E = 36   a =  2
    PRIME  y^2 = x^3 + 2x + 9   #E = 43   a = -5

ANOM's trace is 12, which is floor(2 sqrt 37) exactly.  ANOM is one of the 18
curves out of 1332 sitting ON the Weil bound -- the extremal case, not a
typical one.  T254 records #E = 26 = MULT and the trace 12 in SA_ST_A; what is
added here is that 12 is the maximum the Weil RH permits over F_37, so ANOM is
pinned by the theorem rather than merely landing somewhere.

=== THE BOUNDARY, STATED SO IT IS NOT CROSSED BY ACCIDENT ===

W3 is the Riemann Hypothesis for zeta functions OF VARIETIES OVER FINITE
FIELDS.  It is not the classical Riemann Hypothesis.

    classical RH    zeta(s) = sum 1/n^s over the integers; the zeros in the
                    critical strip lie on Re(s) = 1/2.  OPEN.
    Weil W3         Z(X,t) for X/F_q; the reciprocal roots have |alpha| = q^{i/2}.
                    PROVED (Deligne 1974).

They are analogues, not instances of one another.  No proof of W3 gives the
classical statement, and nothing in this file does either.  The repo's own
files already say the classical one is open -- master_framework_audit.py line
180, prime_dr_unification.py line 20, fixed_point_sieve_audit.py line 261 -- and
this file does not change that.

What IS true, and is the reason this file exists: the proved version lives over
finite fields, and this corpus is already over one.  Work here is not reaching
for an analogy to RH.  It is in the setting where the analogue is a theorem,
with its objects computable by hand -- 1332 of them enumerated below.

=== WHAT THIS FILE DOES NOT CLAIM ===

It does not claim 37 is distinguished.  Every statement here holds for every
prime power q; q = 37 is substituted because that is this repo's modulus.  The
tier-test is run below over q in {5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43}
and the bound is tight for all of them, so tightness is a fact about finite
fields, not about 37.

It does not rest on T253's motivic correspondence table.  Nothing above needs
it; the Weil statements are used in their standard form.

=== FALSIFICATION ===

An elliptic curve over F_37 with |a| > 12; a curve whose alpha has modulus
other than sqrt(37); a curve with a^2 >= 4q; or a prime q where
floor(2 sqrt q) is not attained by some curve over F_q.  Each is asserted
below by exhaustive enumeration, not by sampling.

=== PRIOR ART IN THIS CORPUS ===

theorem_254_elliptic_curves_gf37.py   ANOM / TWIN / PRIME and their traces,
                                      re-verified here; ANOM shown extremal
theorem_287_anomalous_curve_orbit_partition.py   anomalous curves over F_37
theorem_288_j0_isomorphism_classes_gf37.py       j = 0 classes
theorem_298_j1728_gaussian_cm.py                 j = 1728, CM
theorem_253_gf37_motive_framework.py             motivic correspondence table;
                                                 cited, not relied on
theorem_192_hilbert_polya_delta_critique.py      the Hilbert-Polya side
functions.py                                     ORBITS, dr, is_prime
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from functions import ORBITS, dr  # noqa: E402

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")


P = 37


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def curve_order(A, B, p=P):
    """#E(F_p) for y^2 = x^3 + Ax + B, including the point at infinity."""
    n = 1
    for x in range(p):
        n += 1 + legendre(x ** 3 + A * x + B, p)
    return n


def trace_of_frobenius(A, B, p=P):
    return p + 1 - curve_order(A, B, p)


def nonsingular_curves(p=P):
    for A in range(p):
        for B in range(p):
            if (4 * A ** 3 + 27 * B ** 2) % p:
                yield A, B


# ── W3 for curves: the Hasse-Weil bound, exhaustively over F_37 ───────────
def test_hasse_weil_bound_over_f37():
    import math
    bound = 2 * math.sqrt(P)
    n = 0
    worst = 0
    extremal = []
    for A, B in nonsingular_curves():
        a = trace_of_frobenius(A, B)
        n += 1
        check(abs(a) <= bound, f"|a| <= 2sqrt(37) for ({A},{B})", abs(a), f"<= {bound:.4f}")
        if abs(a) > worst:
            worst = abs(a)
        if abs(a) == 12:
            extremal.append((A, B, a))
    check(n == 1332, "non-singular curves over F_37", n, 1332)
    check(worst == 12, "largest |a|", worst, 12)
    check(worst == int(bound), "the bound is tight", worst, int(bound))
    check(len(extremal) == 18, "curves on the bound", len(extremal), 18)


# ── W3 exactly: |alpha| = sqrt(q), by conjugacy not by floating point ────
def test_alpha_modulus_is_exactly_sqrt_q():
    """alpha*beta = q and a^2 < 4q, so alpha,beta conjugate and |alpha|^2 = q."""
    n = 0
    for A, B in nonsingular_curves():
        a = trace_of_frobenius(A, B)
        # the discriminant is negative for every curve -- that IS the Hasse bound
        check(a * a < 4 * P, f"a^2 < 4q for ({A},{B})", a * a, f"< {4*P}")
        # so the roots are conjugate with product exactly q
        # alpha = (a + i sqrt(4q - a^2))/2 ; |alpha|^2 = (a^2 + 4q - a^2)/4 = q
        mod_sq_times_4 = a * a + (4 * P - a * a)
        check(mod_sq_times_4 == 4 * P, f"4|alpha|^2 = 4q for ({A},{B})",
              mod_sq_times_4, 4 * P)
        n += 1
    check(n == 1332, "curves checked", n, 1332)
    # done in exact integers above; confirm once in floating point too
    import cmath
    a = trace_of_frobenius(1, 1)
    al = (a + cmath.sqrt(complex(a * a - 4 * P, 0))) / 2
    check(abs(abs(al) - P ** 0.5) < 1e-12, "numeric agreement",
          abs(al), P ** 0.5)


# ── the zeta prediction, checked against an INDEPENDENT count in F_{37^2} ─
def _f2_mul(u, v, ns, p=P):
    """(a+b*s)(c+d*s) in F_p[s]/(s^2 - ns), ns a non-residue."""
    a, b = u
    c, d = v
    return ((a * c + b * d * ns) % p, (a * d + b * c) % p)


def _count_over_f_p2(A, B, p=P):
    """#E(F_{p^2}) by brute force over all p^2 values of x, no zeta used."""
    ns = next(n for n in range(2, p) if pow(n, (p - 1) // 2, p) == p - 1)
    elems = [(a, b) for a in range(p) for b in range(p)]
    squares = set()
    for e in elems:
        squares.add(_f2_mul(e, e, ns))
    n = 1  # point at infinity
    for x in elems:
        x2 = _f2_mul(x, x, ns)
        x3 = _f2_mul(x2, x, ns)
        rhs = ((x3[0] + A * x[0] + B) % p, (x3[1] + A * x[1]) % p)
        if rhs == (0, 0):
            n += 1
        elif rhs in squares:
            n += 2
    return n


def test_zeta_predicts_the_extension_count():
    """W1/W3: #E(F_{q^m}) = q^m + 1 - (alpha^m + beta^m), with alpha+beta = a.

    The m = 2 count below is obtained by brute force over all 37^2 points of
    F_{37^2}, with no reference to the zeta function, then compared against the
    recurrence s_m = a s_{m-1} - q s_{m-2}.  An earlier version of this test
    compared the recurrence against itself and could not fail; this one can.
    """
    for A, B in [(1, 1), (5, 0), (2, 1), (2, 9), (13, 19)]:
        a = trace_of_frobenius(A, B)
        s = [2, a]
        for m in (2, 3):
            s.append(a * s[m - 1] - P * s[m - 2])
        # m = 1, direct
        check(P + 1 - s[1] == curve_order(A, B), f"m=1 ({A},{B})",
              P + 1 - s[1], curve_order(A, B))
        # m = 2, independent brute-force count over F_{37^2}
        predicted = P ** 2 + 1 - s[2]
        actual = _count_over_f_p2(A, B)
        check(predicted == actual, f"m=2 ({A},{B}) zeta vs brute force",
              predicted, actual)
        # the group order over the extension must be divisible by the base one
        check(actual % curve_order(A, B) == 0,
              f"#E(F_37) divides #E(F_37^2) for ({A},{B})",
              actual % curve_order(A, B), 0)
    # and the test must notice a wrong trace
    a_wrong = trace_of_frobenius(1, 1) + 1
    s2_wrong = a_wrong * a_wrong - 2 * P
    check(P ** 2 + 1 - s2_wrong != _count_over_f_p2(1, 1),
          "a deliberately wrong trace is rejected",
          P ** 2 + 1 - s2_wrong, f"!= {_count_over_f_p2(1,1)}")


# ── T254's three curves, re-verified, and ANOM shown extremal ────────────
def test_t254_curves():
    named = {"ANOM": ((5, 0), 26, 12), "TWIN": ((2, 1), 36, 2),
             "PRIME": ((2, 9), 43, -5)}
    for name, ((A, B), order, tr) in named.items():
        check(curve_order(A, B) == order, f"{name} #E", curve_order(A, B), order)
        check(trace_of_frobenius(A, B) == tr, f"{name} trace",
              trace_of_frobenius(A, B), tr)
    import math
    check(abs(named["ANOM"][2]) == int(2 * math.sqrt(P)),
          "ANOM is on the Weil bound", abs(named["ANOM"][2]), int(2 * math.sqrt(P)))
    # and it is one of only 18
    extremal = [(A, B) for A, B in nonsingular_curves()
                if abs(trace_of_frobenius(A, B)) == 12]
    check((5, 0) in extremal, "ANOM among the extremal curves", (5, 0), "present")
    check(len(extremal) == 18, "extremal count", len(extremal), 18)
    # placement read from the core, not a retyped table
    check(12 in ORBITS["SA_ST_A"], "trace 12 in SA_ST_A", 12, ORBITS["SA_ST_A"])
    check(26 in ORBITS["IC"], "order 26 in IC", 26, ORBITS["IC"])


# ── TIER TEST: this is finite fields, not 37 ─────────────────────────────
def test_tightness_is_not_about_37():
    """floor(2 sqrt q) is attained over F_q for every prime q tested."""
    import math
    for q in (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
        worst = 0
        for A in range(q):
            for B in range(q):
                if (4 * A ** 3 + 27 * B ** 2) % q == 0:
                    continue
                n = 1
                for x in range(q):
                    n += 1 + legendre(x ** 3 + A * x + B, q)
                worst = max(worst, abs(q + 1 - n))
        check(worst == int(2 * math.sqrt(q)), f"bound tight over F_{q}",
              worst, int(2 * math.sqrt(q)))
        check(worst <= 2 * math.sqrt(q), f"bound holds over F_{q}",
              worst, f"<= {2*math.sqrt(q):.3f}")


# ── the boundary to the classical RH, asserted as a fact about the repo ──
def test_the_repo_already_marks_classical_rh_open():
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    marks = {
        "math/theorems/master_framework_audit.py": "does NOT prove RH",
        "math/theorems/prime_dr_unification.py": "OPEN",
        "math/theorems/fixed_point_sieve_audit.py": "OPEN",
    }
    for rel, needle in marks.items():
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            FAIL.append(f"missing prior-art file {rel}")
            continue
        txt = open(p, encoding="utf-8", errors="replace").read()
        check(needle in txt, f"{rel} marks it open", needle in txt, True)


def self_test():
    tests = [test_hasse_weil_bound_over_f37,
             test_alpha_modulus_is_exactly_sqrt_q,
             test_zeta_predicts_the_extension_count,
             test_t254_curves,
             test_tightness_is_not_about_37,
             test_the_repo_already_marks_classical_rh_open]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    if FAIL:
        for x in FAIL[:20]:
            print(f"  FAIL  {x}")
        raise AssertionError(f"{len(FAIL)} check(s) failed")

    print()
    print("THE WEIL CONJECTURES OVER F_37")
    print()
    print("  W1 rationality        Dwork 1960")
    print("  W2 functional eqn     Grothendieck, 1960s")
    print("  W3 RIEMANN HYPOTHESIS Deligne 1974")
    print("  W4 Betti numbers      Grothendieck / Deligne")
    print("  All four are theorems.  None is open.")
    print()
    print("  W3 for curves over F_37, checked on ALL 1332 non-singular curves:")
    print("    largest |a|                 12")
    print("    2 sqrt(37)                  12.1655...")
    print("    bound tight                 yes, floor(2 sqrt 37) = 12 attained")
    print("    curves on the bound         18 of 1332")
    print("    |alpha| = sqrt(37)          1332 of 1332, exactly")
    print()
    print("  EXACT, not numerical: alpha*beta = 37 and a^2 < 4q for every curve,")
    print("  so alpha and beta are conjugate and |alpha|^2 = alpha*beta = 37.")
    print()
    print("  T254's ANOM (y^2 = x^3 + 5x) has trace 12 = floor(2 sqrt 37).")
    print("  It is one of the 18 curves ON the Weil bound -- extremal, not")
    print("  typical.  T254 recorded the trace; the theorem says 12 is the most")
    print("  F_37 permits.")
    print()
    print("  TIER TEST: the bound is tight over F_q for q = 5,7,11,...,43 as")
    print("  well.  This is a fact about finite fields, not about 37.")
    print()
    print("  BOUNDARY.  W3 is RH for zeta functions of varieties over finite")
    print("  fields.  It is not the classical RH for zeta(s), which is open and")
    print("  which this repo already marks open in three files.  They are")
    print("  analogues; neither gives the other.  What is true is that the")
    print("  proved version lives over finite fields, and this corpus is")
    print("  already over one.")


if __name__ == "__main__":
    self_test()

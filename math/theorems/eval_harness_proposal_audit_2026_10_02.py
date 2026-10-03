# CLASS: AUDIT
"""
Audit of a supplied proposal (2026-10-02): "scale toy monoid and Diophantine
checks into frontier-grade evaluations" -- three status tiers mapped to
proof layers, a toy-to-Millennium table, and an "epistemic clamping"
pipeline.  Checkable parts are asserted; the rest is recorded as unchecked.

CORRECT
 - Barrier names are right: relativization (Baker-Gill-Solovay 1975), natural
   proofs (Razborov-Rudich), algebrization (Aaronson-Wigderson 2008).
 - Tracking a premise DAG so a failed step lowers everything downstream is
   sound; cylicamp/provenance.py already has Claim/Derivation/Evidence for it.

INCORRECT OR OVERSTATED (asserted below where computable)
 1. The example shape ['1','p','pq','q'] is not a divisor prefix: pq > q for
    every prime p, so pq cannot precede q.  As a SET it is the divisor set of
    pq; as an ordered prefix it must be 1 p q pq.
 2. "[MEASURED] -> computationally refuted" merges two different things. One
    counterexample is a PROOF of the negation, not a measurement:
    psi_12 = 318665857834031151167461 refutes "witnesses 2..37 are exact below
    3.3e24" outright (mr_witness_audit_2026_10_02.py).
 3. An exhaustive check of a FINITE statement is a proof of that statement,
    not a bounded measurement.  The k=8 case B p = 3 step
    (k8_case_b_complete.py) is finite and therefore proved; the repo's own
    split is PROVED vs SEARCH (a bounded sweep of an infinite family), which
    is the distinction that matters.
 4. "Fails in a finite model -> clamp to REFUTED" holds only for a statement
    whose intended domain IS that model, or a universal statement that the
    model is an instance of.  "There is x with x^2 = 2" fails in Z/8 and holds
    in Z/7.
 5. The table's links are named, not shown: divisor-prefix shapes have no
    known relation to P vs NP circuit lower bounds; Legendre three-square is a
    theorem and Markov triples are not BSD objects (the real bridge to BSD on
    that row is congruent numbers / Tunnell's theorem, itself conditional on
    BSD for one direction).
 6. "Toy": the T245 layers in this repo are proofs (k = 2, 3, 4, 6, 8
    impossible), not string checks.

LIBRARY CLAIMS, CHECKED 2026-10-02
Lean 4 mathlib -- read from source, commit 014e37aeb813 (2026-10-02):
 - Elliptic curve L-function: DEFINED only, AlgebraicGeometry/EllipticCurve/
   LFunction.lean (89 lines): the Euler product as a formal Dirichlet series
   (ArithmeticFunction Z) and its LSeries.  No analytic continuation, no
   value at s = 1, no rank.  "Formally compute L-function values at s = 1"
   is NOT available.  Mordell-Weil: absent; only the naive height and the
   approximate parallelogram law (NumberTheory/Height/EllipticCurve.lean).
 - Dirichlet L-functions: L(chi, s) != 0 for Re s >= 1
   (LFunction_ne_zero_of_one_le_re), incl. s = 1, and zeta != 0 on Re s >= 1.
   The file calls these PNT prerequisites; the PNT itself is not in mathlib
   (it is in the separate PrimeNumberTheoremAnd project).  Zeta zeros:
   only closed and discrete (LSeries/ZetaZeros.lean).  No zero-free region
   beyond Re s >= 1.
 - Sobolev: Gagliardo-Nirenberg-Sobolev inequality PROVED for compactly
   supported C^1 functions (FunctionalSpaces/SobolevInequality.lean), and
   Sobolev spaces H^{s,p} DEFINED via the Bessel potential
   (Distribution/Sobolev.lean).  So "verified Sobolev embedding lemmas" is
   partly true.  Navier-Stokes: no file mentions it.
 - Computability: Turing machines, partial recursive functions, halting,
   automata.  No circuits, no P, no NP, no AC^0.  The P vs NP row's
   "circuit complexity libraries" do not exist in mathlib.
Isabelle AFP -- read from the AFP topic pages:
 - Prime Number Theorem, Eberl and Paulson 2018 (with Mertens' theorems);
   Dirichlet L-functions and Dirichlet's theorem (Eberl 2017); Hurwitz and
   Riemann zeta (Eberl 2017); General Weierstrass Equations (2026).
 - Analysis topic: "Lp spaces"; nothing on Sobolev, Navier-Stokes or PDE.
Coq/Rocq -- web search only (weaker): an elliptic-curve group-law library
   (SSReflect) and MathComp-Analysis exist; no L-function, Sobolev or
   zero-free-region formalization was found.

FALSIFICATION: any assertion failing.
"""
from sympy import primerange

for p in primerange(2, 200):
    for q in primerange(p + 1, 200):
        v = [1, p, p * q, q]
        assert v != sorted(v)                                   # 1
        assert sorted(v) == [1, p, q, p * q]

PSI12 = 318665857834031151167461                                # 2
assert PSI12 == 399165290221 * 798330580441

assert not any(x * x % 8 == 2 for x in range(8))                # 4: fails in Z/8
assert any(x * x % 7 == 2 for x in range(7))                    #    holds in Z/7

if __name__ == "__main__":
    print("eval-harness proposal audit 2026-10-02: all assertions pass")

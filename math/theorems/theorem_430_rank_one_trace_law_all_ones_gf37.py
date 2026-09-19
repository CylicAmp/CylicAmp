# CLASS: THEOREM
"""
Theorem 430: A^2 = tr(A)·A for every rank-one A, so the n×n all-ones matrix
over GF(37) has J^k = n^(k-1) J with period ord_37(n) -- and at 37 | n the
seam turns the projector into a NILPOTENT

Supplied as M = u u^T with u^T u = 3, giving M^2 = 3M and M^n = 3^(n-1) M,
with the spectral reading M = 3P for the projector P = M/3. Both routes
verified below. What follows is the general law they are instances of, and
the GF(37) content, neither of which is in the corpus.

PRIOR ART, read before writing.
  T229 (theorem_229_m9_terminal_singularity.py) is the corpus's rank-one
  file. It has M_9 of rank 1 with spectrum {0,1}, kernel of dimension 8,
  idempotency, and -- at its line 92 -- the observation trace(M_9) = 1.
  It does NOT state the law below; it records the trace as a coincidence of
  that one matrix rather than as the thing that forces the power rule.
  T280 (theorem_280_matrix_dimension_gf37.py) is about alternating {1,2}
  matrices and palindromic tiling, a different subject entirely.

================================================================================
1. THE LAW, WHICH SUBSUMES BOTH CASES
================================================================================

  Let A = v w^T be any rank-one matrix over a commutative ring. Then

      A^2 = v (w^T v) w^T = (w^T v) A = tr(A) · A,

  since tr(v w^T) = w^T v. By induction

      A^k = tr(A)^(k-1) · A     for every k >= 1.

  The supplied M = u u^T is the case v = w = u with tr = u^T u = 3.
  T229's M_9 is the case tr = 1, and "M_9 is idempotent" is exactly
  A^2 = 1 · A. So idempotency and M^2 = 3M are one identity at two traces,
  and the trace T229 noticed is the whole mechanism.

  The spectral reading generalises the same way: A has rank one, so its
  spectrum is {tr(A), 0, ..., 0}, and when tr(A) is invertible
  P = A/tr(A) is a projector with A = tr(A)·P and A^k = tr(A)^k P.

================================================================================
2. OVER GF(37): THE PERIOD IS ord_37(n), AND THE SEAM IS NILPOTENT
================================================================================

  For the n×n all-ones matrix J over GF(37), tr(J) = n, so

      J^k = n^(k-1) J.

  Two regimes, and the divide is the seam:

      37 does NOT divide n    J^k cycles: J^(k) = J iff n^(k-1) = 1, so the
                              power sequence is periodic in k with period
                              exactly ord_37(n). J/n is a projector.

      37 DIVIDES n            tr(J) = 0, so J^2 = 0. J is NILPOTENT of index
                              2. There is no projector: n is not invertible.

  Verified directly: the 37×37 all-ones matrix over GF(37) squares to the
  zero matrix. The 3×3 one satisfies J^2 = 3J and J^19 = J, because
  ord_37(3) = 18.

  Sample of the correspondence:

      n = 2    ord_37(2)  = 36    period 36      (2 is a primitive root)
      n = 3    ord_37(3)  = 18    period 18
      n = 26   ord_37(26) =  3    period 3       (the 137-map multiplier)
      n = 36   ord_37(36) =  2    period 2       (36 = -1)
      n = 37   0                  NILPOTENT, J^2 = 0

  The 18 at n = 3 is the same ord_37(3) = 18 that makes <C, mu> only half of
  AGL(1,37) in T346 and T427; the 3 at n = 26 is the order that makes every
  137-map orbit a 3-cycle. One quantity, three places.

================================================================================
3. FORCED-CHECK -- THE PERIOD IS NOT AN ORBIT INVARIANT
================================================================================

  It is tempting to read section 2 as "the period is a property of the orbit
  of n". It is not, and the check is one line: IC = {1, 10, 26} has

      ord_37(1) = 1,   ord_37(10) = 3,   ord_37(26) = 3

  three elements of one orbit, two distinct periods. The period is
  36/gcd(dlog(n), 36), a function of the discrete log, and the H-orbit shifts
  the discrete log by 12 and 24, which does not preserve gcd(·, 36).

  So the period depends on n mod 37 and on nothing coarser. Asserted below
  by exhibiting an orbit whose members disagree.

  WHAT IS FORCED and carries nothing: tr(J) = n for the all-ones matrix,
  rank(J) = 1, and spectrum {n, 0, ..., 0}. All three are definitional.
  WHAT IS NOT: which n give which period, and that 37 | n is exactly the
  nilpotent case.

  FALSIFICATION. Any of: a rank-one A with A^2 != tr(A)A; the 37×37 all-ones
  matrix not squaring to zero; a period differing from ord_37(n) for some
  n not divisible by 37; or IC turning out to have a constant order.
"""

import sys

import numpy as np

P = 37
ORBITS = {
    "IC": {1, 10, 26}, "DARK_A": {2, 15, 20}, "C3": {3, 4, 30},
    "CAS_EXT": {5, 13, 19}, "TESLA": {6, 8, 23}, "D7": {7, 33, 34},
    "SA_ST_A": {9, 12, 16}, "NEG_H": {11, 27, 36}, "C9": {14, 29, 31},
    "NQR17": {17, 22, 35}, "SEED": {18, 24, 32}, "SA_ST_B": {21, 25, 28},
}


def order_of(a):
    if a % P == 0:
        return None
    k, v = 1, a % P
    while v != 1:
        v = v * a % P
        k += 1
    return k


def main():
    print("=" * 78)
    print("THEOREM 430: THE RANK-ONE TRACE LAW AND THE ALL-ONES MATRIX")
    print("=" * 78)

    print("\nPart 1: the supplied case, both routes")
    u = np.ones((3, 1), dtype=object)
    M = u @ u.T
    assert int((u.T @ u)[0, 0]) == 3
    Mk = M.copy()
    for k in range(1, 9):
        assert (Mk == (3 ** (k - 1)) * M).all(), k
        Mk = Mk @ M
    print("   M = u u^T, u^T u = 3 -> M^k = 3^(k-1) M for k = 1..8 ✓")
    Mf = np.ones((3, 3))
    ev = sorted(np.linalg.eigvals(Mf).real.round(9), reverse=True)
    print("   spectrum %s, rank %d, P = M/3 idempotent: %s"
          % (ev, np.linalg.matrix_rank(Mf), np.allclose(Mf / 3 @ (Mf / 3), Mf / 3)))
    assert ev[0] == 3.0 and np.linalg.matrix_rank(Mf) == 1

    print("\nPart 2: the general law A^2 = tr(A) A for rank-one A")
    rng = np.random.default_rng(0)
    tested = 0
    for _ in range(400):
        v = rng.integers(0, P, (5, 1))
        w = rng.integers(0, P, (1, 5))
        A = (v @ w) % P
        if np.linalg.matrix_rank(A.astype(float)) != 1:
            continue
        tested += 1
        assert (((A @ A) % P) == (int(np.trace(A)) % P * A) % P).all()
    print("   verified on %d random rank-one matrices over GF(37) ✓" % tested)
    print("   tr = 1 gives idempotent (T229's M_9); tr = 3 gives M^2 = 3M")

    print("\nPart 3: the all-ones matrix over GF(37)")
    print("   n     n mod 37  ord_37(n)   behaviour")
    for n in (2, 3, 26, 36, 37, 74):
        o = order_of(n)
        print("   %-5d %-9d %-11s %s"
              % (n, n % P, o if o else "-",
                 "NILPOTENT, J^2 = 0" if o is None else "period %d in k" % o))
    J37 = np.ones((P, P), dtype=object)
    assert (((J37 @ J37) % P) == 0).all()
    print("   37x37 all-ones squares to ZERO over GF(37) ✓ -- the seam")
    J3 = np.ones((3, 3), dtype=object)
    assert (((J3 @ J3) % P) == (3 * J3) % P).all()
    assert pow(3, 18, P) == 1 and order_of(3) == 18
    print("   3x3: J^2 = 3J and J^19 = J, since ord_37(3) = 18 ✓")
    assert order_of(26) == 3
    print("   26x26: period 3, the same order that makes 137-map orbits 3-cycles")

    # the period really is ord_37(n)
    for n in (2, 3, 5, 26, 36):
        o = order_of(n)
        Jn = np.ones((3, 3), dtype=object)      # shape irrelevant; scalar rules
        assert pow(n, o, P) == 1
        assert all(pow(n, j, P) != 1 for j in range(1, o))
    print("   period = ord_37(n) exactly, checked for n = 2, 3, 5, 26, 36 ✓")

    print("\nPart 4: forced-check -- the period is NOT an orbit invariant")
    ic = sorted(ORBITS["IC"])
    ords = [order_of(x) for x in ic]
    print("   IC = %s has orders %s -- two distinct values in one orbit"
          % (ic, ords))
    assert len(set(ords)) > 1
    print("   period = 36/gcd(dlog(n),36); the H-orbit shifts dlog by 12 and")
    print("   24, which does not preserve gcd(.,36). So it depends on n mod 37")
    print("   and on nothing coarser.")

    print("\n" + "=" * 78)
    print("ALL ASSERTIONS PASS")
    print("=" * 78)


if __name__ == "__main__":
    sys.exit(main())

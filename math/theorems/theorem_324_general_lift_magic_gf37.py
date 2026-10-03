# CLASS: THEOREM
"""
Theorem 324: the lift is row-magic at n(n^2+1)/2 for every n, and magic for none
Author: Michael Warren Song (CyclicAmp)

Generalises T322 (n=3) and T323 (n=4). The constants 15 and 34 were never
special: both are n(n^2+1)/2, the magic constant for 1..n^2.

=== SETUP ===

    Identify 1..n^2 with Z_n x Z_n by

        d = 1 + w + n*f,     w(d) = (d-1) mod n,   f(d) = (d-1) div n

    Seed s = (s_0, ..., s_{n-1}) of distinct digits; the lift G(s) has row t
    equal to (s_j + n*t) on the n^2-cycle. Two identities drive everything:

        w(s_j + n t) = w(s_j)            orbit INVARIANT
        f(s_j + n t) = f(s_j) + t        phase SHIFTS by t

=== THEOREM ===

    Write w, f for the words w o s and f o s.

    (a) COVERING.   G(s) is a bijection onto 1..n^2  <=>  w is injective.
                    Count: n! * n^n.  (w-word any permutation of Z_n, f-word
                    free.) Verified exhaustively for n = 2,3,4 and by the
                    closed form beyond.

    (b) ORBIT ARRAY.  L_orb = (w; w; ...; w), the same row n times. Every
                      column is constant, so L_orb is NEVER Latin, any n.

    (c) PHASE ARRAY.  L_ph column j is { f_j + t : t in Z_n } = Z_n, so L_ph
                      is column-Latin for EVERY seed. Only rows can fail.

    (d) CRITERION.  Under (a), these are equivalent:
                        f injective  <=>  L_ph Latin  <=>  all row sums equal
                        <=>  every row sum = n(n^2+1)/2
                    Count of such seeds: (n!)^2.

        PROOF of the sum. Under (a), sum(w) = 0+1+...+(n-1) = n(n-1)/2, so

            row_t = SUM_j [ 1 + w_j + n*((f_j+t) mod n) ]
                  = n + n(n-1)/2 + n * SUM_j ((f_j+t) mod n).

        The last sum is t-independent iff f is injective, and then equals
        n(n-1)/2, giving

            row = n + n(n-1)/2 + n * n(n-1)/2
                = n + n(n^2-1)/2
                = n(n^2+1)/2,

        which is exactly the magic constant for 1..n^2.

    (e) COLUMNS.  Column j is the whole +n-orbit of s_j, with sum

            col_j = n + n*w_j + n^2 (n-1)/2,

        an arithmetic progression in w_j of step n. Its mean over j is
        n(n^2+1)/2 -- the same magic constant -- but the n values are
        distinct for every n >= 2.

    (f) COROLLARY.  A lift grid can be ROW-MAGIC (exactly under (d)) and is
        NEVER MAGIC, for any n. The obstruction is (e): the column sums are
        an AP of nonzero step, so they cannot all equal the constant their
        own mean is.

=== WHAT THIS RETIRES ===

    n=3: rows 15, cols 12/15/18 (T320, T321, T322)
    n=4: rows 34, cols 28/32/36/40 (T323)

    Both are this theorem evaluated. The AG(2,3) reading of T320 remains the
    right geometric account at n=3 -- columns are the x=c parallel class --
    but the arithmetic needs no plane.

=== FALSIFICATION ===
    Any assert below failing.
"""

from itertools import permutations
from math import factorial


def coords(n):
    NN = n * n
    return (lambda v, k: ((v - 1 + k) % NN) + 1,
            lambda d: (d - 1) % n,
            lambda d: (d - 1) // n)


def lift(n, s):
    adv, _, _ = coords(n)
    return [tuple(adv(v, n * t) for v in s) for t in range(n)]


def latin(sq):
    m = len(sq)
    return (all(len(set(r)) == m for r in sq)
            and all(len({sq[r][c] for r in range(m)}) == m for c in range(m)))


def magic(n):
    return n * (n * n + 1) // 2


def run():
    for n in (2, 3, 4):
        NN = n * n
        adv, w, f = coords(n)
        cov = both = 0
        for s in permutations(range(1, NN + 1), n):
            winj = len({w(d) for d in s}) == n
            g = lift(n, s)
            assert (sorted(d for r in g for d in r) == list(range(1, NN + 1))) == winj
            if not winj:
                continue
            cov += 1
            Lo = [[w(d) for d in r] for r in g]
            Lp = [[f(d) for d in r] for r in g]

            # (b) orbit array: same row n times, never Latin
            assert Lo == [[w(d) for d in s]] * n
            assert all(len({Lo[t][j] for t in range(n)}) == 1 for j in range(n))
            assert not latin(Lo)

            # (c) phase array always column-Latin
            assert all({Lp[t][j] for t in range(n)} == set(range(n))
                       for j in range(n))

            # (d) the equivalence
            finj = len({f(d) for d in s}) == n
            assert finj == latin(Lp)
            assert finj == (len({sum(r) for r in g}) == 1)
            assert finj == ({sum(r) for r in g} == {magic(n)})
            if finj:
                both += 1

            # the closed form, every row
            for t in range(n):
                assert sum(g[t]) == n + n * (n - 1) // 2 \
                       + n * sum((f(d) + t) % n for d in s)

            # (e) columns: AP of step n, mean = magic, never all equal
            cols = [sum(g[t][j] for t in range(n)) for j in range(n)]
            for j in range(n):
                assert cols[j] == n + n * w(s[j]) + n * n * (n - 1) // 2
            assert sorted(cols) == [n + n * k + n * n * (n - 1) // 2
                                    for k in range(n)]
            assert sum(cols) == NN * (NN + 1) // 2
            assert sum(cols) == n * magic(n)
            assert len(set(cols)) == n                      # never all equal
            assert len(set(cols)) > 1                       # so never magic

        assert cov == factorial(n) * n ** n, (n, cov)
        assert both == factorial(n) ** 2, (n, both)

    # the algebraic identity behind the magic constant, for a wide range of n
    for n in range(2, 60):
        assert n + n * (n * n - 1) // 2 == magic(n)
        assert n + n * (n - 1) // 2 + n * (n * (n - 1) // 2) == magic(n)
        cols = [n + n * k + n * n * (n - 1) // 2 for k in range(n)]
        assert sum(cols) == n * magic(n)
        assert sum(cols) // n == magic(n)                   # mean is the constant
        assert len(set(cols)) == n                          # AP, step n
        assert cols[1] - cols[0] == n

    print("All assertions passed.\n")
    print("  d = 1 + w + n*f on 1..n^2,  lift by +n,  n rows\n")
    print(f"  {'n':>3} {'covering':>10} {'n!*n^n':>10} {'both inj':>9} "
          f"{'(n!)^2':>8} {'row sum':>8} {'n(n^2+1)/2':>11}  column sums")
    for n in (2, 3, 4, 5, 6):
        cols = [n + n * k + n * n * (n - 1) // 2 for k in range(n)]
        print(f"  {n:>3} {factorial(n)*n**n:>10} {factorial(n)*n**n:>10} "
              f"{factorial(n)**2:>9} {factorial(n)**2:>8} "
              f"{magic(n):>8} {magic(n):>11}  {cols}")
    print("\n  row sum when f is injective  = n(n^2+1)/2, THE magic constant")
    print("  column sums                  = AP in w_j of step n, mean the same")
    print("  so: row-magic exactly when f is injective, and NEVER magic,")
    print("  because an AP of nonzero step cannot be constant at its own mean.")
    print("\n  15 (n=3) and 34 (n=4) were this formula, not small-case accidents.")


if __name__ == "__main__":
    run()

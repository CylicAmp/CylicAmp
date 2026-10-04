# CLASS: AUDIT
"""
Audit of supplied record AUD-WAV-CHEEGER-42 (2026-10-04): Dirichlet Laplacian L = 4I - A on a
42-cell domain Omega of the 8x8 torus (the complement of the 26-node wave's support), with
lambda_1 = 0.781498 and Cheeger constant h = 5/7. Mathematics only.

INTERNALLY CONTRADICTORY -- decidable from the record alone
  C1 For any nonempty S in Omega, the indicator vector 1_S has Rayleigh quotient
        <1_S, L 1_S> / <1_S, 1_S> = (4|S| - 2 e(S)) / |S| = |cut edges of S| / |S|,
     counting edges to Omega \ S and to the absorbing boundary (every cell has degree 4 on the
     torus). Since lambda_1 is the MINIMUM Rayleigh quotient, lambda_1 <= |cut(S)| / |S| for every
     S, hence lambda_1 <= h(Omega).
     The record states lambda_1 = 0.781498 and h = 5/7 = 0.714286 from a set S* with 10 cut edges
     on 14 cells. Then 1_{S*} has quotient 0.714 < 0.781 -- impossible. At least one of the two
     numbers is wrong. (Checked below on a real domain: lambda_1 <= |cut(S)|/|S| for 20,000 random
     S, and the identity <1_S, L 1_S> = |cut(S)| for each.)
  C2 The quoted window "h^2 / 8 <= lambda_1 <= 2h" uses the upper bound 2h; for this Dirichlet
     Laplacian the indicator argument gives the sharper lambda_1 <= h, which the record's own
     numbers violate.

NOT REPRODUCIBLE / MISLABELLED
  C3 The domain is defined in AUD-WAV-BG-8DIR and AUD-WAV-EIG-A42, which were not supplied. The
     natural placements of the 26-node wave on the 8x8 (digits mod 8, or digit - 1 mod 8) cover
     23 cells and leave 41, not 42; on that 41-cell domain rho(A) = 3.480276, lambda_1 = 0.519724,
     and 0 is an eigenvalue of A eleven times (not six). So the spectrum cannot be checked as
     given.
  C4 "A4 EXHAUSTIVE FINITE ... exhaustive cut minimization": the Cheeger constant minimizes over
     all 2^42 (about 4.4 x 10^12) subsets; checking 42 cells is not an exhaustive search of that
     domain. Per the owner's protocol (PROTOCOL.md, sections 5 and 7) the A4 label and the
     THEOREM / PROVED status do not apply; the record is at most a COMPUTATIONAL RESULT, and C1
     shows it is inconsistent.
FALSIFICATION: any assertion failing.
"""
import numpy as np

wave = [77, 78, 87, 88, 89, 98, 99, 91, 19, 11, 12, 21, 22, 23, 32, 33, 34, 43, 44, 45, 54, 55, 56, 65, 66, 67]
lam1_claim, h_claim = 0.781498, 10 / 14
assert h_claim < lam1_claim                                                             # C1: the contradiction

supp = {(x // 10 % 8, x % 10 % 8) for x in wave}
om = [(i, j) for i in range(8) for j in range(8) if (i, j) not in supp]
idx = {c: k for k, c in enumerate(om)}
n = len(om)
A = np.zeros((n, n))
for (i, j), k in idx.items():
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        c = ((i + di) % 8, (j + dj) % 8)
        if c in idx:
            A[k, idx[c]] = 1
L = 4 * np.eye(n) - A
ev = np.linalg.eigvalsh(L)
assert (len(supp), n) == (23, 41)                                                       # C3
assert abs(ev.min() - 0.519724) < 1e-6 and sum(abs(np.linalg.eigvalsh(A)) < 1e-9) == 11
assert abs(np.trace(L) - 4 * n) < 1e-9

rng = np.random.default_rng(0)
for _ in range(20000):                                                                  # C1 check
    m = rng.integers(1, n + 1)
    S = rng.choice(n, size=m, replace=False)
    f = np.zeros(n); f[S] = 1
    cut = 0
    for k in S:
        i, j = om[k]
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c = ((i + di) % 8, (j + dj) % 8)
            if c not in idx or idx[c] not in set(S):
                cut += 1
    assert abs(f @ L @ f - cut) < 1e-9
    assert ev.min() <= cut / m + 1e-12
assert 2 ** 42 > 4.39e12                                                                # C4

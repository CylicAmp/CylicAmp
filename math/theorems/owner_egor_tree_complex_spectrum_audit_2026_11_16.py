# CLASS: AUDIT
"""
"EGOR and complex numbers: extending the verified tree spectrum" (2026-11-16) -- the owner's EGOR work, computed with
the owner's tool and relayed by the owner. Audit on arrival.

RIGHT, every number (recomputed below, 40 digits):
  the quartic lambda^4 - 216 lambda^2 + 3240 has roots +-14.1344384835292 and +-4.02711419695666;
  |zeta(1/2 + i t)| at t = 14.134438483529, 6, 4.027114196957, 0: 0.000227360591, 0.903710276, 0.616378446,
    1.460354509 -- the table's values; the first zero is 14.1347251417347;
  B = [[3,3,9,9],[6,0,0,0],[0,0,0,6]] gives B B^T = [[180,18,54],[18,36,0],[54,0,36]] and
    det(x I - B B^T) = (x - 36)(x^2 - 216x + 3240); the 7 x 7 adjacency [[0,B],[B^T,0]] has
    det = lambda (lambda^2 - 36)(lambda^4 - 216 lambda^2 + 3240): eigenvalues 0, +-6, +-4.027, +-14.134;
  H = [[0, iB], [-iB^T, 0]] is Hermitian and equal to U A U* with U = diag(1,1,1,-i,-i,-i,-i): same spectrum;
  random phases on the six edges of the tree leave the characteristic polynomial unchanged (checked on 20 draws).

WHAT THE SMALL ZETA VALUE IS: the largest eigenvalue sits 0.000287 below the first zero, and
  |zeta'(rho_1)| x 0.000287 = 0.79316 x 0.000287 = 0.000227 -- the table's value is the distance to the zero times the
  slope there, nothing more (as the text says, not evidence of a zero).

PRIOR ART (outside): the "new exact theorem" of section 4 -- edge phases on a tree can be removed, so the spectrum
  cannot change -- is a known fact of gain graphs: a connected gain graph has the spectrum of its underlying graph
  exactly when it is balanced, and a tree (no cycles) is always balanced (N. Reff, "Spectral properties of complex unit
  gain graphs", arXiv 1110.4554; spectrum equality as cited in arXiv 1908.10668). The bipartite identity
  det(lambda I - A) = lambda^(4-3) det(lambda^2 I - B B^T) is standard.

NOT CHECKABLE HERE: that B uses "the graph's exact edge weights" -- the EGOR tree's edge list is not in the repo.

FALSIFICATION: any assertion failing.
"""
import random

import sympy as sp
from mpmath import fabs, mp, mpf, sqrt, zeta, zetazero

mp.dps = 40
lam_big = sqrt((216 + sqrt(216 ** 2 - 4 * 3240)) / 2)
lam_small = sqrt((216 - sqrt(216 ** 2 - 4 * 3240)) / 2)
assert mp.nstr(lam_big, 14) == "14.134438483529" and mp.nstr(lam_small, 13) == "4.027114196957"

vals = [fabs(zeta(mpf(1) / 2 + 1j * t)) for t in (lam_big, mpf(6), lam_small, mpf(0))]     # at the exact roots
table = [mpf("0.0002273605913"), mpf("0.9037102757"), mpf("0.6163784456"), mpf("1.4603545088")]
assert all(abs(v - w) < mpf("1e-10") for v, w in zip(vals, table))
g1 = zetazero(1).imag
assert mp.nstr(g1, 14) == "14.134725141735"
gap = g1 - lam_big
slope = fabs(zeta(zetazero(1), derivative=1))
assert abs(slope * gap - vals[0]) < mpf("1e-7")

x, l = sp.symbols("x lambda")
B = sp.Matrix([[3, 3, 9, 9], [6, 0, 0, 0], [0, 0, 0, 6]])
assert (B * B.T).tolist() == [[180, 18, 54], [18, 36, 0], [54, 0, 36]]
assert sp.expand((x * sp.eye(3) - B * B.T).det() - (x - 36) * (x ** 2 - 216 * x + 3240)) == 0
A = sp.zeros(7, 7)
A[:3, 3:] = B
A[3:, :3] = B.T
target = sp.expand(l * (l ** 2 - 36) * (l ** 4 - 216 * l ** 2 + 3240))
assert sp.expand(A.charpoly(l).as_expr() - target) == 0

H = sp.zeros(7, 7)
H[:3, 3:] = sp.I * B
H[3:, :3] = -sp.I * B.T
U = sp.diag(1, 1, 1, -sp.I, -sp.I, -sp.I, -sp.I)
assert H == H.H and sp.simplify(U * A * U.H - H) == sp.zeros(7, 7)

rng = random.Random(16)
edges = [(i, 3 + j) for i in range(3) for j in range(4) if B[i, j] != 0]
assert len(edges) == 6                                     # 7 vertices, 6 edges, connected: a tree
for _ in range(20):
    Hp = sp.zeros(7, 7)
    for (i, j) in edges:
        k = rng.randrange(1, 12)
        ph = sp.exp(2 * sp.pi * sp.I * k / 12)
        Hp[i, j] = A[i, j] * ph
        Hp[j, i] = A[j, i] * sp.conjugate(ph)
    assert sp.expand(sp.simplify(Hp.charpoly(l).as_expr()) - target) == 0

if __name__ == "__main__":
    print("EGOR complex spectrum: every number right; the small zeta value = slope x gap; tree phases removable (known)")

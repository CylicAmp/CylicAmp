# CLASS: COMPUTATION
"""
Hejhal's algorithm on SL_2(Z), implemented and run here
Author: Michael Warren Song (CyclicAmp)

This file exists because selberg_maass_montgomery.py carried two [U] flags
justified by "producing r_j requires Hejhal's algorithm, which is a
substantial numerical program not present in this repo".  That was true.
It is no longer true at level 1.

WHAT IT DOES.  A Maass cusp form on SL_2(Z)\\H with spectral parameter r has

    f(x+iy) = sqrt(y) sum_{n>=1} a_n K_{ir}(2 pi n y) cs(2 pi n x)

with cs = cos (even) or sin (odd), a_1 = 1.  K_{ir}(x) decays like e^{-x},
so at a fixed horocycle height Y only |n| <= M survive and the system is
finite.  Sample 2Q points z_m = x_m + iY, pull each back into the standard
fundamental domain (translate Re into [-1/2,1/2]; invert if |z| < 1; repeat),
and use automorphy f(z_m) = f(z_m*).  Inverting the DFT on the horocycle:

    a_n sqrt(Y) K_ir(2 pi n Y) = sum_k V_nk(r,Y) a_k
    V_nk = (1/Q) sum_m sqrt(y_m*) K_ir(2 pi k y_m*) cs(2 pi k x_m*) cs(2 pi n x_m)

Fix a_1 = 1, solve for the rest, repeat at a second height Y', and score

    g(r) = sum_n | a_n(Y) - a_n(Y') |.

g(r) is small only at an eigenvalue.  The search in r is one-dimensional.

RESULT, 2026-09-16.  Against the known first odd eigenvalue
r_1 = 9.53369526135 (Booker-Strombergsson-Venkatesh, 100 decimals):

    r = 9.0               g = 3.6e+02
    r = 9.3               g = 1.1e+02
    r = 9.53369526135     g = 1.3e-09     <-- eleven orders down
    r = 9.8               g = 7.3e+01
    r = 10.2              g = 9.3e+01

and a BLIND scan over r in [9.2, 14.1] at step 0.1, told nothing, produced
a local minimum in the 12.17 neighbourhood (known r_2 = 12.17300832468).
The 0.1 grid is too coarse to catch every dip -- they are narrow -- so a
coarse scan must be followed by local refinement.

SCOPE, so this is not read as more than it is.
  * This is the ONE-CUSP algorithm.  Gamma_0(4) has three cusps and needs
    Stromberg's block extension; that is not implemented here.
  * The solve is HEURISTIC.  A dip in g(r) is a candidate, not a proof.
    Certification is Booker-Strombergsson-Venkatesh, a separate argument.
  * So this does NOT lift the two [U] flags in selberg_maass_montgomery.py,
    which are about Gamma_0(4).  It removes their stated REASON -- "no such
    program is present" -- and replaces it with a narrower one: the
    multi-cusp extension is not written.

FALSIFICATION.  g(r) failing to dip at a known eigenvalue, or dipping at a
value that is not one.
"""
import mpmath as mp


def pullback(x, y, iters=200):
    """Pull z = x+iy into the standard fundamental domain for SL_2(Z)."""
    z = mp.mpc(x, y)
    for _ in range(iters):
        z -= mp.floor(mp.re(z) + mp.mpf(1) / 2)
        if abs(z) < 1:
            z = -1 / z
        else:
            return mp.re(z), mp.im(z)
    return mp.re(z), mp.im(z)


def Kir(r, x):
    """K_{ir}(x), rescaled by e^{pi r/2} to keep it off the underflow floor."""
    return mp.besselk(mp.mpc(0, r), x) * mp.exp(mp.pi * r / 2)


def coeffs(r, Y, M, Q, odd=True):
    """Fourier coefficients a_1..a_M at horocycle height Y, with a_1 = 1."""
    cs = mp.sin if odd else mp.cos
    xs = [(mp.mpf(m) - mp.mpf(1) / 2) / (2 * Q) for m in range(1, 2 * Q + 1)]
    pb = [pullback(x, Y) for x in xs]
    V = mp.zeros(M, M)
    for m, (xst, yst) in enumerate(pb):
        sq = mp.sqrt(yst)
        kk = [sq * Kir(r, 2 * mp.pi * k * yst) * cs(2 * mp.pi * k * xst)
              for k in range(1, M + 1)]
        for n in range(1, M + 1):
            c = cs(2 * mp.pi * n * xs[m])
            for k in range(1, M + 1):
                V[n - 1, k - 1] += kk[k - 1] * c / Q
    A = mp.zeros(M, M)
    for n in range(1, M + 1):
        A[n - 1, n - 1] = mp.sqrt(Y) * Kir(r, 2 * mp.pi * n * Y)
    A = A - V
    rhs = mp.matrix([-A[n, 0] for n in range(1, M)])
    B = mp.matrix(M - 1, M - 1)
    for i in range(M - 1):
        for j in range(M - 1):
            B[i, j] = A[i + 1, j + 1]
    sol = mp.lu_solve(B, rhs)
    return [mp.mpf(1)] + [sol[i] for i in range(M - 1)]


def residual(r, M=22, Q=28, Y1=None, Y2=None, odd=True, ncomp=8):
    """g(r): disagreement between coefficient vectors at two heights."""
    Y1 = mp.mpf('0.38') if Y1 is None else Y1
    Y2 = mp.mpf('0.30') if Y2 is None else Y2
    a1 = coeffs(r, Y1, M, Q, odd)
    a2 = coeffs(r, Y2, M, Q, odd)
    return sum(abs(a1[i] - a2[i]) for i in range(1, min(ncomp, M)))


R1 = mp.mpf('9.53369526135')      # first odd level-1 eigenvalue (BSV)


def run():
    mp.mp.dps = 30
    print("Hejhal on SL_2(Z), one cusp, two heights\n")
    print("  r                     g(r)")
    vals = {}
    for s in ('9.0', '9.3', '9.53369526135', '9.8'):
        g = residual(mp.mpf(s))
        vals[s] = g
        print("  %-18s  %.3e" % (s, float(g)))

    # the eigenvalue must beat every neighbour by many orders
    hit = vals['9.53369526135']
    assert hit < mp.mpf('1e-6'), hit
    for s in ('9.0', '9.3', '9.8'):
        assert vals[s] > 1, (s, vals[s])
        assert vals[s] / hit > mp.mpf('1e6'), (s, vals[s] / hit)

    print("\n  g(r_1) = %.2e, every neighbour > 1 and at least 1e6 larger."
          % float(hit))
    print("  The dip locates the known eigenvalue. Machinery validated.\n")
    print("  NOT a certificate (BSV is separate), and NOT Gamma_0(4)")
    print("  (three cusps, needs Stromberg's block extension, not written).")
    print("\n  ALL ASSERTIONS PASS")


if __name__ == '__main__':
    run()

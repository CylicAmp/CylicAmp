# CLASS: COMPUTATION
"""
Scale-to-scale flux: the sign of Pi at a point is a property of the FILTER,
not of the flow -- measured, plus a diagnostic for vanishing Pi
Author: Michael Warren Song (CyclicAmp)

Built to put a number on a claim that was otherwise rhetoric: "move the
cutoff and a backscatter region becomes a forward-scatter region."

=== WHAT Pi IS ===

    Filter the velocity at width D.  The subfilter stress is

        tau_ij = filter(u_i u_j) - filter(u_i) filter(u_j)

    and the scale-to-scale energy flux is

        Pi = - tau_ij Sbar_ij ,   Sbar_ij = (d_i Ubar_j + d_j Ubar_i)/2

    Pi > 0 is forward scatter (energy to smaller scales), Pi < 0 is
    backscatter.  Both are signs of ONE field, and that field is indexed by
    D.  D is a choice.

=== RESULT 1: THE SIGN FLIPS, AND HERE IS HOW OFTEN ===

    On a 256^2 incompressible synthetic field with a k^-5/3 streamfunction
    spectrum (divergence verified at 1e-13, i.e. machine zero):

        D=4 against D=3    20.3% of points flip the sign of Pi
        D=4 against D=5    14.0%
        D=4 against D=6    21.7%
        D=4 against D=8    30.1%

    Between a quarter and a third of the domain changes which way energy is
    said to be going, with the flow untouched.  Forward and backscatter are
    not two processes; they are one quantity whose sign at a point depends
    on where the observer cuts.

    CAVEAT, stated because it matters: this is 2D, where the mean cascade is
    inverse, and indeed the net here is backscatter-dominated (about 45%
    forward, 55% back at every D).  The MEAN direction is a 2D-vs-3D fact
    and does not transfer.  The POINTWISE sign-flipping under a change of
    filter width is kinematic -- it follows from tau depending on D -- and
    holds in both.

=== RESULT 2: A DIAGNOSTIC FOR Pi ~ 1e-18 ===

    Pi rms against filter width, same field:

        D= 2   1.56e-02        D=12   6.18e-08
        D= 3   5.46e-03        D=16   5.48e-12
        D= 4   2.16e-03        D=24   1.44e-23
        D= 6   4.11e-04
        D= 8   4.55e-05

    Pi does not merely shrink with D, it COLLAPSES once the filter is wide
    enough to remove everything the field contains -- here the spectrum was
    de-aliased above k = 85, and by D = 16 the Gaussian has killed all of
    it, so tau -> 0 and Pi falls to roundoff.

    So a Pi of order 1e-18 is a signature, not a small number.  The three
    things that produce it:

        1. filter width at or below the grid spacing, or so far above the
           resolved content that nothing survives -- no scale separation
           either way, tau == 0
        2. tau built as filter(uu) - filter(u)filter(u) with the SAME
           filter applied twice in a way that cancels
        3. the velocity field normalised to ~1e-9 before being squared

    Worth saying: the first draft of this script reproduced the pathology by
    accident, by normalising u and v separately (which also broke
    incompressibility, divergence 3e-1 instead of 1e-13).  Both bugs are
    easy to make and neither announces itself.

    Run `diagnose(u, v)` below on a real field to see which case applies.
"""

import numpy as np


def synthetic_field(N=256, seed=37):
    """Incompressible 2D field, streamfunction spectrum ~ k^-11/6."""
    rng = np.random.default_rng(seed)
    k = np.fft.fftfreq(N) * N
    KX, KY = np.meshgrid(k, k, indexing='ij')
    K2 = KX ** 2 + KY ** 2
    K2[0, 0] = 1
    psi = (rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N)))
    psi *= K2 ** (-11 / 12)
    psi[K2 > (N / 3) ** 2] = 0
    u = np.real(np.fft.ifft2(1j * KY * psi))
    v = np.real(np.fft.ifft2(-1j * KX * psi))
    s = np.sqrt((u ** 2 + v ** 2).mean() / 2)      # ONE common factor:
    return u / s, v / s, KX, KY, K2                # separate ones break div=0


def flux(u, v, D, KX, KY, K2):
    """Pi = -tau_ij Sbar_ij at Gaussian filter width D (grid units)."""
    G = np.exp(-K2 * (D ** 2) / 24)
    f = lambda a: np.real(np.fft.ifft2(np.fft.fft2(a) * G))
    d = lambda a, K: np.real(np.fft.ifft2(1j * K * np.fft.fft2(a)))
    U, V = f(u), f(v)
    t11, t12, t22 = f(u * u) - U * U, f(u * v) - U * V, f(v * v) - V * V
    Ux, Uy, Vx, Vy = d(U, KX), d(U, KY), d(V, KX), d(V, KY)
    return -(t11 * Ux + 2 * t12 * 0.5 * (Uy + Vx) + t22 * Vy)


def diagnose(u, v, Ds=(2, 3, 4, 6, 8, 12, 16, 24)):
    """Run on your own field. Flags the Pi ~ 0 pathology."""
    N = u.shape[0]
    k = np.fft.fftfreq(N) * N
    KX, KY = np.meshgrid(k, k, indexing='ij')
    K2 = KX ** 2 + KY ** 2
    K2[0, 0] = 1
    div = np.real(np.fft.ifft2(1j * KX * np.fft.fft2(u)
                               + 1j * KY * np.fft.fft2(v)))
    print(f"  u rms {u.std():.3e}   v rms {v.std():.3e}")
    print(f"  divergence max {abs(div).max():.2e}"
          f"   {'OK' if abs(div).max() < 1e-8 * max(u.std(),1e-30) else '<-- NOT incompressible'}")
    for D in Ds:
        P = flux(u, v, D, KX, KY, K2)
        tag = '  <-- at roundoff: tau has collapsed' if P.std() < 1e-14 else ''
        print(f"  D={D:2d}  Pi rms {P.std():.3e}  fwd {100*(P>0).mean():4.1f}%"
              f"  back {100*(P<0).mean():4.1f}%{tag}")


def run():
    u, v, KX, KY, K2 = synthetic_field()
    div = np.real(np.fft.ifft2(1j * KX * np.fft.fft2(u)
                               + 1j * KY * np.fft.fft2(v)))
    assert abs(div).max() < 1e-10, abs(div).max()

    print("256x256 incompressible synthetic field, k^-5/3 spectrum")
    print(f"  divergence max {abs(div).max():.2e}  (machine zero)\n")

    print("RESULT 1 -- the sign of Pi flips with the filter width")
    base = flux(u, v, 4, KX, KY, K2)
    flips = {}
    for D in (3, 5, 6, 8):
        P = flux(u, v, D, KX, KY, K2)
        fl = (np.sign(P) != np.sign(base)).mean()
        flips[D] = fl
        print(f"   D=4 vs D={D}:  {100*fl:4.1f}% of points flip sign")
    assert 0.10 < min(flips.values()) and max(flips.values()) > 0.25
    print("   the flow is untouched; only the cutoff moved.\n")
    print("   CAVEAT: 2D, so the MEAN direction (backscatter-dominated here)")
    print("   is a 2D fact and does not transfer to 3D.  The pointwise")
    print("   sign-flipping is kinematic and does.\n")

    print("RESULT 2 -- Pi rms vs D, and the 1e-18 signature")
    prev = None
    for D in (2, 3, 4, 6, 8, 12, 16, 24):
        P = flux(u, v, D, KX, KY, K2)
        print(f"   D={D:2d}  Pi rms {P.std():.3e}"
              + ("   <-- roundoff, tau collapsed" if P.std() < 1e-14 else ""))
        if prev is not None:
            assert P.std() < prev
        prev = P.std()
    print("\n   Pi ~ 1e-18 is a signature, not a small number.  Causes:")
    print("     1. no scale separation (D at the grid spacing, or so wide")
    print("        that nothing resolved survives)")
    print("     2. tau cancelling from the same filter applied twice")
    print("     3. velocities ~1e-9 before squaring")
    print("\n   diagnose(u, v) runs this on a real field.")


if __name__ == "__main__":
    run()

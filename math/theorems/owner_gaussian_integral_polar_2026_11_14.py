# CLASS: COMPUTATION
"""
The owner's lines (2026-11-14), the Gaussian integral by polar coordinates:

    "∫₀^∞ e^(−x²) dx = √π / 2 ≈ 0.886
     Square it: I² = ¼ ∬ e^(−(x²+y²)) dx dy over the whole plane, the volume under a bell surface.
     In polar form, dx dy = r dr dθ. Let u = r² and the radial part becomes 1, so I² = ⅛ ∫₀^2π dθ = π/4.."

CLEANED, each step checked:
    I = integral from 0 to infinity of e^(-x^2) dx
    I^2 = (integral over x > 0) x (integral over y > 0) = the quarter-plane volume under e^(-(x^2 + y^2))
        = 1/4 x (the whole-plane volume)                          right: the bell is the same in all four quarters
    polar: dx dy -> r dr dtheta                                   right
    radial part: integral of e^(-r^2) r dr, with u = r^2, du = 2r dr
        = 1/2 x integral of e^(-u) du = 1/2 x 1                   right: the 1/2 goes out front, the rest is 1
    so I^2 = 1/4 x 1/2 x (integral of dtheta over 0 .. 2 pi) = 1/8 x 2 pi = pi/4   right
    I = sqrt(pi/4) = sqrt(pi)/2 = 0.886 226 925 ...                right (I is positive, so the + root)

THE WHOLE PLANE: the same steps without the 1/4 give pi, so the full-line integral is sqrt(pi) = 1.772 453 85 ...

FALSIFICATION: any assertion failing.
"""
import math

from mpmath import inf, mp, mpf, pi, quad, exp, sqrt

mp.dps = 30

I = quad(lambda x: exp(-x * x), [0, inf])
assert abs(I - sqrt(pi) / 2) < mpf(10) ** -25
assert f"{float(I):.3f}" == "0.886"

# the quarter-plane volume is I^2, and it is 1/4 of the whole plane
quarter = quad(lambda x, y: exp(-(x * x + y * y)), [0, inf], [0, inf])
whole = quad(lambda x, y: exp(-(x * x + y * y)), [-inf, inf], [-inf, inf])
assert abs(quarter - I ** 2) < mpf(10) ** -20 and abs(whole / 4 - quarter) < mpf(10) ** -20

# polar: radial part = 1/2, with u = r^2 the u-integral = 1
radial = quad(lambda r: exp(-r * r) * r, [0, inf])
assert abs(radial - mpf(1) / 2) < mpf(10) ** -25
assert abs(quad(lambda u: exp(-u), [0, inf]) - 1) < mpf(10) ** -25

# I^2 = 1/4 x 1/2 x 2 pi = pi/4
assert abs(mpf(1) / 8 * 2 * pi - pi / 4) < mpf(10) ** -28 and abs(I ** 2 - pi / 4) < mpf(10) ** -25
assert abs(math.sqrt(math.pi) / 2 - 0.886226925452758) < 1e-15

if __name__ == "__main__":
    print("I = sqrt(pi)/2 = 0.88623; quarter plane = pi/4; radial part 1/2 x 1; 1/4 x 1/2 x 2pi = pi/4: all right")

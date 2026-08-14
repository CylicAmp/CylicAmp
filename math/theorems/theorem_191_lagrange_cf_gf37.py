"""
Theorem 191: Lagrange Spectrum, Periodic Continued Fractions, and GF(37)

PERIODIC CONTINUED FRACTION [0; a, b, a, b, ...]
===================================================
The quadratic equation is: a·x² + a·b·x − b = 0
Positive root: x = (−ab + √(ab(ab + 4))) / (2a)

LAGRANGE SPECTRUM CONSTANTS IN GF(37)
=======================================
L₁ = √5 ≈ 2.2360:   5 ∈ NQR (Legendre(5,37) = −1). First isolated peak
                      arises from the NQR sector. Floor = 2 = primitive root.

L₂ = √8 ≈ 2.8284:   √8 = 2√2. Coefficient 4 = 2² ∈ SA. The second isolated
                      peak encodes the sovereign anchor (4) and primitive root (2).

Freiman = 4.52782956: floor = 4 ∈ SA = {4,9,25,30}.
                      Above this value the Lagrange spectrum becomes dense
                      (no more isolated peaks). The density transition is
                      gated by a sovereign anchor.

TOTIENT-BALANCED PERIOD PAIRS
===============================
Any period pair (a, b) with a·b = 36 = φ(37) generates a
"totient-balanced" periodic continued fraction.

All GF(37) framework pairs with a·b = φ(37):
  (3, 12): ST × ST   [sovereign target × sovereign target]
  (4,  9): SA × SA   [sovereign anchor × sovereign anchor]
  (6,  6): TESLA²    [TESLA_FLOW squared]
  (9,  4): SA × SA
  (12, 3): ST × ST

For all these pairs:
  discriminant = 36 × 40 = 1440
  1440 mod 37 = 34 = P − 3

SILVER RATIO
=============
[2; 2, 2, 2, ...]: a = b = 2, a·b = 4 ∈ SA.
Silver ratio = 1 + √2 ≈ 2.4142.
The silver ratio arises from the sovereign anchor period pair.

GOLDEN RATIO
=============
[1; 1, 1, 1, ...]: x² − x − 1 = 0, root = φ = (1 + √5)/2.
Pisano period π(37) = 76.  76 mod 37 = 2 = primitive root.
F₇₆ ≡ 0 mod 37 (SEAM), F₇₇ ≡ 1 mod 37 (identity).

LAGRANGE FLOOR
===============
L₁ = √5: Hurwitz theorem states every irrational has infinitely many
rational approximations p/q with |α − p/q| < 1/(√5 · q²).
The floor constant is √5. In GF(37): 5 is NQR, the unexplained sector.
The hardest-to-approximate numbers (like φ) live at the NQR boundary.

STRUCTURE OF THE QUADRATIC COEFFICIENTS
=========================================
a·x² + a·b·x − b = 0
Coefficient of x²: a
Coefficient of x:  a·b = a × b
Constant term:     −b

For (a,b) = (4,9):  4x² + 36x − 9 = 0   (4∈SA, 36=φ(37), 9∈SA)
For (a,b) = (3,12): 3x² + 36x − 12 = 0  (3∈ST, 36=φ(37), 12∈ST)
For (a,b) = (6,6):  6x² + 36x − 6 = 0   (6=TESLA_FLOW, 36=φ(37))
  → simplifies to x² + 6x − 1 = 0, positive root = −3 + √10.
"""

import math
import cmath
from typing import NamedTuple, List

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
seed_orbit = {18, 24, 32}


class QuadraticSolution(NamedTuple):
    a: float
    b: float
    c: float
    discriminant: float
    roots: List[complex]


def solve_quadratic(a: float, b: float, c: float) -> QuadraticSolution:
    disc = b * b - 4 * a * c
    if disc >= 0:
        r1 = (-b + math.sqrt(disc)) / (2 * a)
        r2 = (-b - math.sqrt(disc)) / (2 * a)
        roots = [complex(r1), complex(r2)]
    else:
        r1 = complex(-b, math.sqrt(-disc)) / (2 * a)
        r2 = complex(-b, -math.sqrt(-disc)) / (2 * a)
        roots = [r1, r2]
    return QuadraticSolution(a=a, b=b, c=c, discriminant=disc, roots=roots)


def solve_periodic_fraction_2(a: int, b: int) -> QuadraticSolution:
    """
    [0; a, b, a, b, ...]  with  x = 1 / (a + 1 / (b + x))
    =>  a*x^2 + a*b*x - b = 0
    """
    if a == 0:
        raise ValueError("a must be positive")
    return solve_quadratic(float(a), float(a * b), float(-b))


def positive_quadratic_root(q: QuadraticSolution) -> float:
    reals = [r.real for r in q.roots if abs(r.imag) < 1e-12]
    return max(reals)


def get_lagrange_bounds() -> dict:
    golden = solve_quadratic(1.0, -1.0, -1.0)    # [1;1,1,1,...]
    phi_val = positive_quadratic_root(golden)

    silver = solve_quadratic(1.0, -2.0, -1.0)    # [2;2,2,2,...]
    silver_val = positive_quadratic_root(silver)

    return {
        "phi": phi_val,
        "silver_ratio": silver_val,
        "Lagrange Floor (Base Delta)": math.sqrt(5),
        "Second Isolated Peak (sqrt(8))": math.sqrt(8),
        "Freiman's Constant Barrier": 4.52782956,
    }


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def run_assertions():
    # --- Lagrange bounds ---
    bounds = get_lagrange_bounds()
    phi = bounds["phi"]
    assert abs(phi - (1 + math.sqrt(5)) / 2) < 1e-10
    assert abs(bounds["silver_ratio"] - (1 + math.sqrt(2))) < 1e-10
    assert abs(bounds["Lagrange Floor (Base Delta)"] - math.sqrt(5)) < 1e-12
    assert abs(bounds["Second Isolated Peak (sqrt(8))"] - math.sqrt(8)) < 1e-12
    assert abs(bounds["Freiman's Constant Barrier"] - 4.52782956) < 1e-8

    # --- GF(37): √5 → 5 is NQR ---
    assert legendre(5, P) == P - 1   # 5 is NQR

    # --- √8 = 2√2: 4 ∈ SA, 2 = primitive root ---
    assert abs(math.sqrt(8) - 2 * math.sqrt(2)) < 1e-12
    assert 4 in SA
    assert pow(2, 36, P) == 1

    # --- Freiman floor = 4 ∈ SA ---
    assert int(4.52782956) == 4 and 4 in SA

    # --- Silver ratio: a=b=2, ab=4 ∈ SA ---
    silver_q = solve_periodic_fraction_2(2, 2)
    silver_root = positive_quadratic_root(silver_q)
    assert abs(silver_root - (math.sqrt(2) - 1)) < 1e-10
    assert 2 * 2 == 4 and 4 in SA

    # --- Totient-balanced pairs: ab = 36 = φ(37) ---
    totient_pairs = [(3, 12), (4, 9), (6, 6), (9, 4), (12, 3)]
    for a, b in totient_pairs:
        assert a * b == P - 1, f"({a},{b}): ab={a*b} ≠ 36"

    # Discriminant for ab=36
    ab = 36
    disc = ab * (ab + 4)
    assert disc == 1440
    assert disc % P == 34 == P - 3

    # Specific pair quadratics
    q_4_9 = solve_periodic_fraction_2(4, 9)
    # equation is 4x² + 36x - 9 = 0; coefficients: a=4, b=36, c=-9
    assert q_4_9.a == 4.0 and q_4_9.b == 36.0 and q_4_9.c == -9.0

    q_6_6 = solve_periodic_fraction_2(6, 6)
    root_6_6 = positive_quadratic_root(q_6_6)
    assert abs(root_6_6 - (-3 + math.sqrt(10))) < 1e-10   # x²+6x-1=0 → x=-3+√10

    # --- Golden ratio and Pisano period ---
    assert abs(phi - (1 + math.sqrt(5)) / 2) < 1e-10
    fib = [0, 1]
    for _ in range(76):
        fib.append((fib[-1] + fib[-2]) % P)
    assert fib[76] == 0    # F_76 ≡ 0 mod 37 = SEAM
    assert fib[77] == 1    # F_77 ≡ 1 mod 37 = identity
    assert 76 % P == 2     # Pisano period mod 37 = primitive root

    # --- solve_periodic_fraction_2 satisfies its own equation ---
    for a, b in [(1, 1), (2, 2), (3, 12), (4, 9)]:
        q = solve_periodic_fraction_2(a, b)
        x = positive_quadratic_root(q)
        residual = a * x**2 + a * b * x - b
        assert abs(residual) < 1e-8, f"({a},{b}): residual={residual}"

    print("All assertions passed.")


if __name__ == "__main__":
    bounds = get_lagrange_bounds()
    print("=== LAGRANGE SPECTRUM BOUNDS ===")
    for k, v in bounds.items():
        print(f"  {k:40s}: {v:.10f}")
    print()
    print("=== TOTIENT-BALANCED PERIODS (ab = 36 = φ(37)) ===")
    for a, b in [(3, 12), (4, 9), (6, 6), (9, 4), (12, 3)]:
        q = solve_periodic_fraction_2(a, b)
        x = positive_quadratic_root(q)
        label = ("SA×SA" if a in SA and b in SA else
                 "ST×ST" if a in ST and b in ST else
                 "TESLA²" if a == 6 else "mixed")
        print(f"  ({a:2d},{b:2d}) {label:6s}: root = {x:.8f}")
    print()
    run_assertions()

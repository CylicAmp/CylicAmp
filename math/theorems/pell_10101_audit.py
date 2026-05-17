# math/theorems/pell_10101_audit.py
"""
Pell Equation x² - 10101·y² = 1: Fundamental Unit Audit
=========================================================
Claims verified:
  1. 10101 = 3 × 7 × 13 × 37  (squarefree; 13 and 37 appear in Kyber/Pisot context)
  2. CF expansion: √10101 = [100; 1, 1, 66, 1, 1, 200̄],  period = 6 (even)
  3. Fundamental unit: ε = 26935 + 268√10101,  ε² - 10101 = 1
  4. Even period ⟹ fundamental solution comes from p_{ℓ-1}/q_{ℓ-1} (ℓ = 6)
  5. All solutions: x_n + y_n·√10101 = εⁿ  (n ≥ 1)
  6. Norm identity: N(ε) = ε·ε̄ = 1  (ε is a unit of Z[√10101])

Connection to prior audits:
  10101 = 3 × 7 × 13 × 37
  — 13  is the NTT cofactor in 3329 = 13 × 256 + 1  (ML-KEM)
  — 37  is the Pisot prime for x³ - x - 1  (F_37 framework)
  — 13 × 37 = 481;  3 × 7 = 21;  21 × 481 = 10101
  The product 13 × 37 lands in this Pell discriminant via standard arithmetic,
  not by any deep coincidence — 10101 is the repunit-like number 1·10⁴+0·10³+1·10²+0·10+1.
"""

from math import isqrt


# ── helpers ───────────────────────────────────────────────────────────────────

def factorize(n: int) -> dict:
    f: dict = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def cf_sqrt(N: int):
    """Return (a0, period) for CF expansion of √N (N squarefree)."""
    a0 = isqrt(N)
    assert a0 * a0 < N < (a0 + 1) * (a0 + 1), "N must not be a perfect square"
    period = []
    m, d, a = 0, 1, a0
    while True:
        m = d * a - m
        d = (N - m * m) // d
        a = (a0 + m) // d
        period.append(a)
        if a == 2 * a0:
            break
    return a0, period


def convergent(a0: int, period: list, steps: int):
    """Compute (p, q) for the convergent after `steps` period terms."""
    seq = [a0] + period[:steps]
    h_prev, h_curr = 1, seq[0]
    k_prev, k_curr = 0, 1
    for ai in seq[1:]:
        h_prev, h_curr = h_curr, ai * h_curr + h_prev
        k_prev, k_curr = k_curr, ai * k_curr + k_prev
    return h_curr, k_curr


def pell_solutions(x1: int, y1: int, N: int, count: int):
    """Generate first `count` positive solutions via (x1+y1√N)^n."""
    solutions = []
    xn, yn = x1, y1
    for _ in range(count):
        solutions.append((xn, yn))
        # (xn + yn√N)(x1 + y1√N) = xn*x1 + yn*y1*N + (xn*y1 + yn*x1)√N
        xn, yn = xn * x1 + yn * y1 * N, xn * y1 + yn * x1
    return solutions


# ── main verification ─────────────────────────────────────────────────────────

def verify():
    print("Pell Equation x² - 10101·y² = 1: Fundamental Unit Audit\n")

    N = 10101

    # ── Claim 1: factorization ─────────────────────────────────────────────────
    print("=" * 60)
    print("CLAIM 1: 10101 = 3 × 7 × 13 × 37")
    print("=" * 60)

    factors = factorize(N)
    assert factors == {3: 1, 7: 1, 13: 1, 37: 1}
    assert 3 * 7 * 13 * 37 == N
    assert all(e == 1 for e in factors.values())   # squarefree

    print(f"\n  10101 = 3 × 7 × 13 × 37  ✓  (squarefree)")
    print(f"  13 × 37 = {13 * 37}  (NTT cofactor × Pisot prime)")
    print(f"   3 ×  7 = {3 * 7}  (complementary factor)")
    print(f"  21 × 481 = {21 * 481}")

    # ── Claim 2: CF expansion ──────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("CLAIM 2: √10101 = [100; 1, 1, 66, 1, 1, 200̄],  period 6")
    print("=" * 60)

    a0, period = cf_sqrt(N)

    assert a0 == 100
    assert period == [1, 1, 66, 1, 1, 200]
    assert len(period) == 6
    assert len(period) % 2 == 0        # even period
    assert period[-1] == 2 * a0        # always 2·a0 for last term

    print(f"\n  a₀ = {a0}")
    print(f"  period = {period}")
    print(f"  period length = {len(period)}  (even)  ✓")
    print(f"  last term = {period[-1]} = 2×{a0}  ✓")
    print(f"  √10101 = [100; overline{{1, 1, 66, 1, 1, 200}}]")

    # ── Claim 3 & 4: fundamental unit from p_{ℓ-1}/q_{ℓ-1} ───────────────────
    print()
    print("=" * 60)
    print("CLAIM 3 & 4: Fundamental unit ε = 26935 + 268√10101")
    print("=" * 60)

    ell = len(period)
    x1, y1 = convergent(a0, period, ell - 1)   # steps through first ℓ-1 period terms

    assert x1 == 26935
    assert y1 == 268
    assert x1 * x1 - N * y1 * y1 == 1

    print(f"\n  Even period length ℓ={ell}: fundamental solution from p_{{ℓ-1}}/q_{{ℓ-1}}")
    print(f"  x₁ = {x1},  y₁ = {y1}")
    print(f"  x₁² - 10101·y₁² = {x1}² - 10101×{y1}²")
    print(f"                   = {x1**2} - {N * y1**2}")
    print(f"                   = {x1**2 - N * y1**2}  ✓")
    print(f"\n  ε = 26935 + 268√10101  is the fundamental unit of Z[√10101]")

    # ── Claim 5: all solutions via powers of ε ────────────────────────────────
    print()
    print("=" * 60)
    print("CLAIM 5: All solutions xₙ + yₙ·√10101 = εⁿ")
    print("=" * 60)

    solutions = pell_solutions(x1, y1, N, 6)
    print()
    for n, (xn, yn) in enumerate(solutions, 1):
        residual = xn * xn - N * yn * yn
        assert residual == 1, f"n={n}: x²-Ny²={residual}≠1"
        print(f"  n={n}: ({xn}, {yn})  →  {xn}² - 10101×{yn}² = {residual}  ✓")

    # ── Claim 6: norm identity N(ε) = 1 ──────────────────────────────────────
    print()
    print("=" * 60)
    print("CLAIM 6: Norm N(ε) = ε·ε̄ = 1")
    print("=" * 60)

    ebar_x, ebar_y = x1, -y1             # conjugate: 26935 - 268√10101
    # product (x1 + y1√N)(x1 - y1√N) = x1² - N·y1²
    norm = x1 * x1 - N * y1 * y1
    assert norm == 1

    print(f"\n  ε  = {x1} + {y1}√10101")
    print(f"  ε̄  = {ebar_x} - {y1}√10101")
    print(f"  N(ε) = ε·ε̄ = {x1}² - 10101×{y1}² = {norm}  ✓")
    print(f"  ε is a unit of Z[√10101]; all εⁿ are also units with norm 1.")

    # ── Period structure note ─────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("PERIOD STRUCTURE")
    print("=" * 60)
    print(f"""
  Period [1, 1, 66, 1, 1, 200] is palindromic up to the final 200:
    [1, 1, 66, 1, 1] is a palindrome  ✓
  This is the standard symmetry of √N continued fractions.

  The large partial quotient 66 at index 3 is the centre of the palindrome.
  Large partial quotients correspond to good rational approximations;
  66 = 2×33 = 2×3×11, not directly related to the Kyber/Pisot context.

  Period 5 partial quotients [1, 1, 66, 1, 1] are consistent with
  index ℓ/2 = 3 in the convergent table — the "index 5" reference in
  the period structure means the 5th partial quotient (a₅=1) completes
  the palindrome before the terminal 2·a₀=200.
    """)

    # ── Summary ───────────────────────────────────────────────────────────────
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print("""
  VERIFIED:
    10101 = 3 x 7 x 13 x 37  (squarefree)                    OK
    sqrt(10101) = [100; 1,1,66,1,1,200],  period = 6 (even)  OK
    Fundamental unit: e = 26935 + 268*sqrt(10101)             OK
    x1^2 - 10101*y1^2 = 1                                     OK
    All solutions xn + yn*sqrt(10101) = e^n,  n=1..6 checked  OK
    N(e) = e*e_bar = 1  (e is a genuine unit)                  OK

  NO EXOTIC MACHINERY:
    Standard Pell theory: CF expansion -> p_{l-1}/q_{l-1} for even l.
    The fundamental unit is unique (up to sign and conjugate).
    x + y*sqrt(10101) = e^n generates every positive solution.

  FACTORIZATION NOTE:
    13 (NTT cofactor, ML-KEM) and 37 (Pisot prime, F_37) both divide 10101.
    This is arithmetic coincidence: 10101 is the repunit-pattern integer
    10101 = 10^4 + 10^2 + 1 = (10^2+10+1)(10^2-10+1) = 111 x 91 = 3x37 x 7x13.
    The factorization is determined by cyclotomic divisibility of 10101,
    not by any structural link between the Pell equation and Kyber/Pisot.
    """)

    print("All assertions passed.")


if __name__ == "__main__":
    verify()

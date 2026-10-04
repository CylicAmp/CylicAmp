#!/usr/bin/env python3
"""
Verification for the unit-circle Method of Exhaustion test family
n = 6*2^k.

Checks:
- exact n=6 anchor formulas
- enclosure L_n < pi < U_n
- monotonicity L_n < L_2n and U_2n < U_n through n=1536
- gap identity U_n-L_n = n*sin(x)^3/cos(x), x=pi/n
- bound g_n <= 2*pi^3/n^2 for n>=6
- first-passing selection for epsilon=1e-4
- predecessor failure
- invalid tolerance rejection
"""
import math

STAGES = [6 * (2**k) for k in range(9)]  # through 1536

def L(n: int) -> float:
    if n < 3:
        raise ValueError("n must be >= 3")
    return (n / 2.0) * math.sin(2.0 * math.pi / n)

def U(n: int) -> float:
    if n < 3:
        raise ValueError("n must be >= 3")
    return n * math.tan(math.pi / n)

def gap(n: int) -> float:
    return U(n) - L(n)

def gap_identity(n: int) -> float:
    x = math.pi / n
    return n * (math.sin(x) ** 3) / math.cos(x)

def gap_bound(n: int) -> float:
    return 2.0 * math.pi**3 / n**2

def select_first_passing(epsilon: float) -> int:
    if not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("epsilon must be finite and > 0")
    n = 6
    # g_n -> 0 and strictly decreases under doubling.
    for _ in range(64):
        if gap(n) <= epsilon:
            return n
        n *= 2
    raise RuntimeError("selection failed within 64 doublings")

def run():
    # Anchor at n=6.
    assert math.isclose(L(6), 3.0 * math.sqrt(3.0) / 2.0,
                        rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(U(6), 2.0 * math.sqrt(3.0),
                        rel_tol=0.0, abs_tol=1e-14)

    rows = []
    for n in STAGES:
        ln, un = L(n), U(n)
        gn, gi = gap(n), gap_identity(n)
        bn = gap_bound(n)

        assert ln < math.pi < un
        assert math.isclose(gn, gi, rel_tol=2e-12, abs_tol=2e-15)
        assert gn <= bn + 2e-15

        rows.append((n, ln, un, gn, bn, gn <= 1e-4))

    for n in STAGES[:-1]:
        assert L(n) < L(2*n) < math.pi
        assert math.pi < U(2*n) < U(n)
        assert gap(2*n) < gap(n)

    epsilon = 1e-4
    selected = select_first_passing(epsilon)
    assert selected == 768
    assert gap(selected) <= epsilon
    assert gap(selected // 2) > epsilon

    for bad in (0.0, -1e-4, float("inf"), float("-inf"), float("nan")):
        try:
            select_first_passing(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid epsilon accepted: {bad!r}")

    print("ALL ASSERTIONS PASSED")
    print(f"epsilon={epsilon:.1e}")
    print(f"first_passing_n={selected}")
    print(f"g_384={gap(384):.15e}")
    print(f"g_768={gap(768):.15e}")
    print()
    print("n,L_n,U_n,g_n,bound_2pi3_over_n2,passes_1e-4")
    for row in rows:
        print(f"{row[0]},{row[1]:.15f},{row[2]:.15f},"
              f"{row[3]:.15e},{row[4]:.15e},{row[5]}")

if __name__ == "__main__":
    run()

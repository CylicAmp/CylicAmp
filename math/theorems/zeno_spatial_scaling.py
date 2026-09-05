"""
Zeno Spatial-Temporal Scaling Law
f(n) = 100 · (0.5)^(n-1)

GF(37): Each step halves the previous value. The system never reaches zero
but converges to a finite total — a Zeno architecture encoding a finite
information horizon despite infinite steps.

Results:

1. FINITE HORIZON
   Sum_{n=1}^{∞} f(n) = 100 / (1 - 0.5) = 200 = 2 × 100
   Total distance from all steps = exactly twice the first step.
   This is the system's absolute bound — it cannot exceed 200.

2. ENTROPY CROSSOVER AT n=7
   f(7) = 100 · (0.5)^6 = 100/64 ≈ 1.5625
   f(8) = 100 · (0.5)^7 = 100/128 ≈ 0.7813
   n=7 is the last step where f(n) > 1 (still integer-capable in the sense of >1).
   n=8 is the first step where f(n) < 1 — the sub-unity threshold.
   This is the entropy crossover: the system crosses from macro to micro.

3. PIVOT AT n=28 (Sovereign Pivot)
   f(28) = 100 · (0.5)^27
   DR(28) = 1 — identity element.
   2^28 mod 37 = 12 — sovereign target in GF(37).
   n=28 is the pivot: identity in DR algebra, sovereign in GF(37).

4. SUMMATION PAIRS (pairs totaling 110 in the index space 1..99)
   For n + m = 100: f(n) · f(m) = 100^2 · (0.5)^(n-1) · (0.5)^(m-1)
                                 = 10000 · (0.5)^(n+m-2) = 10000 · (0.5)^98
   All such pairs have the same product — constant across the pair orbit.

5. CONNECTION TO EXTINCTION RATES AND ABSOLUTE ZERO
   The finite horizon 200 represents a hard ceiling on total observable extent.
   Below n=7 (entropy crossover): measurable, integer-regime behavior.
   Below n=28 (pivot): sub-threshold, residual trace behavior.
   The limit f(n)→0 is structural absolute zero — unreachable but asymptotically approached.
   This mirrors thermodynamic 0K: the system approaches but never reaches it.
"""


def f(n: float) -> float:
    return 100.0 * (0.5) ** (n - 1)


def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


# 1. Finite horizon
total = sum(f(n) for n in range(1, 1001))
assert abs(total - 200.0) < 1e-9, "Finite horizon must approach 200"

# 2. Entropy crossover at n=7
assert f(7) > 1.0,  "f(7) must be > 1"
assert f(8) < 1.0,  "f(8) must be < 1"

# 3. Pivot at n=28
assert dr(28) == 1,         "DR(28) must be 1 (identity)"
assert pow(2, 28, 37) == 12, "2^28 mod 37 must be 12 (sovereign target)"

# 4. Summation pair product constant
def pair_product(n):
    m = 100 - n
    return f(n) * f(m)

pair_products = [pair_product(n) for n in range(1, 50)]
assert all(abs(p - pair_products[0]) < 1e-6 for p in pair_products), \
    "All summation pair products must be equal"


if __name__ == "__main__":
    print("ZENO SPATIAL-TEMPORAL SCALING LAW")
    print("=" * 40)
    print("f(n) = 100 · (0.5)^(n-1)")
    print()
    print("First 10 steps:")
    for n in range(1, 11):
        marker = ""
        if n == 7:
            marker = "  ← entropy crossover (last step > 1)"
        elif n == 8:
            marker = "  ← first sub-unity step"
        print(f"  f({n:>2}) = {f(n):>12.6f}{marker}")
    print()
    print(f"Finite horizon: Σf(n) → {200.0} = 2 × 100")
    print(f"Entropy crossover: n=7  [f(7)={f(7):.4f} > 1, f(8)={f(8):.4f} < 1]")
    print()
    print("Pivot n=28:")
    print(f"  DR(28)      = {dr(28)} (identity element)")
    print(f"  2^28 mod 37 = {pow(2,28,37)} (sovereign target in GF(37))")
    print(f"  f(28)       = {f(28):.2e}")
    print()
    print("Summation pair product (n + m = 100):")
    print(f"  f(1)·f(99) = {f(1)*f(99):.6e}")
    print(f"  f(7)·f(93) = {f(7)*f(93):.6e}  (same)")
    print(f"  f(28)·f(72)= {f(28)*f(72):.6e}  (same)")
    print()
    print("Absolute zero analogy:")
    print("  f(n)→0 as n→∞: unreachable limit = structural absolute zero")
    print("  Total horizon 200: finite, approached from below")
    print()
    print("All assertions passed.")

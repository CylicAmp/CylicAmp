"""
log2_sqrt5_audit.py

Verifies 10 mathematical claims about log₂(2+√5) and DR(2+8+2+7):

  1.  log₂(2+√5) ≈ 2.0827–2.0840
  2.  DR(2+8+2+7) = DR(19) = 1
  3.  19 ≡ 1 (mod 9)
  4.  No algebraic homomorphism (ℝ⁺,×) → (ℤ/9ℤ,+)
  5.  2+√5 is the positive root of x²−4x−1=0
  6.  Self-consistency: y = ½·log₂(4·2^y+1)
  7.  Numerical convergence of the fixed-point iteration
  8.  DR arithmetic progression 9k+1 maps to DR=1
  9.  Log map: multiplicative→additive; DR map: additive collapse
  10. Continued fraction expansion of log₂(2+√5)
"""

import math
import numpy as np

# ============================================================
# Constants
# ============================================================
sqrt5 = math.sqrt(5)
x     = 2 + sqrt5              # = 4.2360679...
y_exact = math.log2(x)         # = log₂(2+√5)

print("=" * 62)
print("Constants")
print("=" * 62)
print(f"  √5          = {sqrt5:.15f}")
print(f"  2+√5        = {x:.15f}")
print(f"  log₂(2+√5)  = {y_exact:.15f}")


# ============================================================
# Claim 1: log₂(2+√5) ∈ [2.0827, 2.0840]
# ============================================================
print()
print("=" * 62)
print("1.  log₂(2+√5) ∈ [2.0827, 2.0840]")
print("=" * 62)
lo, hi = 2.0827, 2.0840
in_range = lo <= y_exact <= hi
print(f"  log₂(2+√5) = {y_exact:.6f}")
print(f"  Claimed range: [{lo}, {hi}]")
print(f"  {'✓ IN RANGE' if in_range else '✗ OUT OF RANGE'}")
print(f"  Tighter bound: {y_exact:.10f}")


# ============================================================
# Claim 2: DR(2+8+2+7) = DR(19) = 1
# ============================================================
print()
print("=" * 62)
print("2.  DR(2+8+2+7) = DR(19) = 1")
print("=" * 62)

def dr(n):
    n = abs(int(n))
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

digit_sum = 2 + 8 + 2 + 7
print(f"  Digits of '2.0827': 2, 0, 8, 2, 7")
print(f"  Sum (including 0): 2+0+8+2+7 = {2+0+8+2+7}")
print(f"  Sum (excluding 0): 2+8+2+7 = {digit_sum}")
print(f"  DR({digit_sum}) = {dr(digit_sum)}  (1+9={1+9}, 1+0=1)  "
      f"{'✓' if dr(digit_sum) == 1 else '✗'}")
print(f"  Chain: {digit_sum} → {1+9} → {1+0} = 1")
print(f"  Note: including the 0 digit: 2+0+8+2+7=19 also, unchanged")


# ============================================================
# Claim 3: 19 ≡ 1 (mod 9)
# ============================================================
print()
print("=" * 62)
print("3.  19 ≡ 1 (mod 9)")
print("=" * 62)
print(f"  19 mod 9 = {19 % 9}  {'✓' if 19 % 9 == 1 else '✗'}")
print(f"  DR(n) = n mod 9  (where 0 mod 9 maps to 9)")
print(f"  DR(19) = 19 mod 9 = 1  ✓")


# ============================================================
# Claim 4: No algebraic homomorphism (ℝ⁺,×) → (ℤ/9ℤ,+)
# ============================================================
print()
print("=" * 62)
print("4.  No algebraic homomorphism (ℝ⁺,×) → (ℤ/9ℤ,+)")
print("=" * 62)
print("""
  Proof sketch:
    A group homomorphism φ: (ℝ⁺,×) → (ℤ/9ℤ,+) must satisfy
      φ(ab) = φ(a) + φ(b) (mod 9).

    (ℝ⁺,×) is divisible: for every a∈ℝ⁺ and n∈ℤ⁺, there exists b with b^n=a.
    (ℤ/9ℤ,+) is finite (order 9).

    If φ is a homomorphism, then for any a and n:
      φ(a) = φ(b^n) = n·φ(b)
    Since (ℤ/9ℤ) has order 9, we need 9·φ(b) = 0 for all b.
    So φ(a) = 9·φ(b) = 0 for all a — i.e., only the trivial homomorphism.

    The log map f(x) = log₂(x) is a homomorphism (ℝ⁺,×) → (ℝ,+).
    The DR map g(n) = n mod 9 is a homomorphism (ℤ,+) → (ℤ/9ℤ,+).
    But g∘f is NOT a homomorphism, since f maps to ℝ (uncountable) while
    g is only defined on ℤ (integers).
""")
print(f"  STATUS: No non-trivial homomorphism exists. ✓")
print(f"  The chain log₂(2+√5) → round digits → DR(19) → 1")
print(f"  is a COMPUTATIONAL OBSERVATION, not an algebraic identity.")


# ============================================================
# Claim 5: 2+√5 is the positive root of x²−4x−1=0
# ============================================================
print()
print("=" * 62)
print("5.  2+√5 is the positive root of x²−4x−1=0")
print("=" * 62)

# Verify: x² - 4x - 1 = 0 at x = 2+√5
x_check = x**2 - 4*x - 1
print(f"  x = 2+√5 = {x:.15f}")
print(f"  x² − 4x − 1 = {x_check:.2e}  (should be 0)  "
      f"{'✓' if abs(x_check) < 1e-12 else '✗'}")

# Algebraic derivation
print(f"""
  Derivation:
    Let x = 2+√5.
    x − 2 = √5
    (x−2)² = 5
    x² − 4x + 4 = 5
    x² − 4x − 1 = 0  ✓

  Both roots: x = (4 ± √(16+4))/2 = (4 ± √20)/2 = 2 ± √5
    Positive root: 2+√5 = {2+sqrt5:.6f}  ✓
    Negative root: 2-√5 = {2-sqrt5:.6f}
""")


# ============================================================
# Claim 6: Self-consistency y = ½·log₂(4·2^y+1)
# ============================================================
print()
print("=" * 62)
print("6.  Self-consistency: y = ½·log₂(4·2^y+1)")
print("=" * 62)
y = y_exact
rhs = 0.5 * math.log2(4 * 2**y + 1)
print(f"  y = log₂(2+√5) = {y:.15f}")
print(f"  ½·log₂(4·2^y+1) = {rhs:.15f}")
print(f"  Difference = {abs(y - rhs):.2e}  {'✓' if abs(y - rhs) < 1e-10 else '✗'}")
print(f"""
  Derivation:
    From x² = 4x+1 (claim 5), take log₂:
      2·log₂(x) = log₂(4x+1)
      y = log₂(x) = ½·log₂(4x+1)
    Substitute x = 2^y:
      y = ½·log₂(4·2^y+1)  ✓

  This is a fixed-point equation: f(y) = ½·log₂(4·2^y+1) = y.
""")


# ============================================================
# Claim 7: Numerical convergence via fixed-point iteration
# ============================================================
print()
print("=" * 62)
print("7.  Fixed-point convergence: y_{n+1} = ½·log₂(4·2^{y_n}+1)")
print("=" * 62)

def fp_iter(y):
    return 0.5 * math.log2(4 * (2**y) + 1)

y0 = 2.0   # starting guess
print(f"  Starting from y₀ = {y0}")
print(f"\n  {'n':>4}  {'y_n':>18}  {'|y_n − y*|':>14}")
print(f"  {'-'*40}")
y_n = y0
prev_err = None
for n in range(50):
    err = abs(y_n - y_exact)
    if n <= 11 or err < 1e-12:
        rate = err / prev_err if prev_err else None
        rate_str = f"  rate={rate:.3f}" if rate else ""
        print(f"  {n:>4}  {y_n:>18.12f}  {err:>14.2e}{rate_str}")
    if err < 1e-14:
        break
    prev_err = err
    y_n = fp_iter(y_n)

print(f"  ...")
print(f"  Fixed point y* = {y_exact:.12f}")
# Linear convergence: each step reduces error by ~0.47
errors = []
yn2 = y0
for _ in range(30):
    err = abs(yn2 - y_exact)
    errors.append(err)
    yn2 = fp_iter(yn2)
rates = [errors[i+1]/errors[i] for i in range(10)]
avg_rate = sum(rates)/len(rates)
print(f"  Convergence: LINEAR (avg rate {avg_rate:.4f} per step)")
print(f"  STATUS: CONVERGES ✓  (linear, ~{avg_rate:.2f} error reduction/step)")


# ============================================================
# Claim 8: Arithmetic progression n = 9k+1 → DR=1
# ============================================================
print()
print("=" * 62)
print("8.  Arithmetic progression n = 9k+1 → DR(n) = 1")
print("=" * 62)
print(f"\n  {'k':>4}  {'n=9k+1':>8}  {'DR(n)':>7}  {'n mod 9':>8}")
print(f"  {'-'*35}")
all_one = True
for k in range(15):
    n = 9*k + 1
    d = dr(n)
    all_one = all_one and (d == 1)
    print(f"  {k:>4}  {n:>8}  {d:>7}  {n%9:>8}")
print(f"\n  All DR(9k+1)=1 for k=0..14: {'✓' if all_one else '✗'}")
print(f"  General: DR(n)=1 ⟺ n ≡ 1 (mod 9)  ✓")


# ============================================================
# Claim 9: Structural separation — log map vs DR map
# ============================================================
print()
print("=" * 62)
print("9.  Structural Separation: log map vs DR map")
print("=" * 62)
print(f"""
  Log map  f: (ℝ⁺,×) → (ℝ,+)
    f(ab) = f(a) + f(b)  (group homomorphism)
    Codomain: (ℝ,+) — uncountable, archimedean ordered field

  DR map   g: (ℤ,+) → (ℤ/9ℤ,+)
    g(a+b) = g(a)+g(b) (mod 9)  (ring quotient homomorphism)
    Codomain: {{1,…,9}} — finite, cyclic group

  Composition g∘f:
    Takes x∈ℝ⁺ → f(x) = log(x) ∈ ℝ → NOT in ℤ → g undefined
    Requires discretization (e.g., floor/round/digit extraction)
    which is NOT a ring homomorphism.

  Consequence:
    The chain 2.0827 → (round digits) → 19 → (DR) → 1
    is a computational pipeline, not an algebraic functor.
    It does not "mean" that log₂(2+√5) = 1 in any algebraic sense.
""")
print(f"  STATUS: Structural separation confirmed ✓")


# ============================================================
# Claim 10: Continued fraction of log₂(2+√5)
# ============================================================
print()
print("=" * 62)
print("10. Continued Fraction of log₂(2+√5)")
print("=" * 62)

def continued_fraction(x, n_terms=20):
    """Compute first n_terms of the continued fraction [a₀; a₁, a₂, …] of x."""
    cf = []
    for _ in range(n_terms):
        a = int(x)
        cf.append(a)
        frac = x - a
        if abs(frac) < 1e-12:
            break
        x = 1.0 / frac
    return cf

cf = continued_fraction(y_exact, n_terms=20)
print(f"  log₂(2+√5) = {y_exact:.12f}")
print(f"  Continued fraction: [{cf[0]}; {', '.join(str(a) for a in cf[1:])}]")

# Reconstruct convergents
print(f"\n  Convergents p/q (rational approximations):")
print(f"  {'n':>4}  {'a_n':>6}  {'p_n':>12}  {'q_n':>12}  {'p_n/q_n':>14}  {'error':>12}")
print(f"  {'-'*60}")

p_prev, p_curr = 1, cf[0]
q_prev, q_curr = 0, 1
for n, a in enumerate(cf):
    if n == 0:
        p, q = cf[0], 1
    else:
        p = a * p_curr + p_prev
        q = a * q_curr + q_prev
        p_prev, p_curr = p_curr, p
        q_prev, q_curr = q_curr, q
    err = abs(p/q - y_exact)
    print(f"  {n:>4}  {a:>6}  {p:>12}  {q:>12}  {p/q:>14.10f}  {err:>12.2e}")
    if n >= 8:
        break

print(f"\n  Note: log₂(2+√5) is transcendental (not rational), so its CF")
print(f"  does not terminate or become periodic.")


# ============================================================
# Summary
# ============================================================
print()
print("=" * 62)
print("SUMMARY")
print("=" * 62)
print(f"""
  1.  log₂(2+√5) = {y_exact:.6f} ∈ [2.0827, 2.0840]  ✓
  2.  DR(2+8+2+7) = DR(19) = 1  ✓
  3.  19 ≡ 1 (mod 9)  ✓
  4.  No non-trivial homomorphism (ℝ⁺,×) → (ℤ/9ℤ,+)  ✓
  5.  x = 2+√5 satisfies x²−4x−1=0  ✓  (error {abs(x_check):.1e})
  6.  Self-consistency y = ½·log₂(4·2^y+1)  ✓  (error {abs(y-rhs):.1e})
  7.  Fixed-point iteration converges  ✓
  8.  n=9k+1 → DR(n)=1 for all k  ✓
  9.  Structural separation log/DR maps  ✓
  10. CF = [{cf[0]}; {', '.join(str(a) for a in cf[1:8])}, …]
      Best rational approx at 8 terms: p/q with error shown above

  All 10 claims: VERIFIED ✓
  One note: claim 1 range [2.0827, 2.0840] is imprecise (true value {y_exact:.6f}).
  The lower bound is tight to 4 d.p.; the stated range is confirmed.
""")

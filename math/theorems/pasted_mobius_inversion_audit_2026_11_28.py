# CLASS: AUDIT
"""
Pasted statement and proof of Möbius inversion (2026-11-28), written as a reading of an image that did not come with it.
Audit on arrival.

RIGHT: the statement (g = sum of f over divisors  <=>  f(n) = sum of mu(d) g(n/d), for f, g valued in any abelian group);
  the Möbius function; Dirichlet convolution, its associativity, commutativity and identity epsilon; the key lemma
  sum over d | n of mu(d) = epsilon(n) -- for n > 1 with k distinct primes, the squarefree divisors with j primes number
  C(k, j), and sum (-1)^j C(k, j) = (1 - 1)^k = 0; both directions of the proof. Checked below for n up to 2000, with f
  valued in the integers, in Z/37 and in pairs of integers.
WRONG (changes a result): section 5 ends "recovering f(n) via the identity mu * zeta = 1". mu * zeta is epsilon (1 at
  n = 1, 0 after), as section 3 itself proves; it is not the constant function 1 (that is zeta).
NOT CHECKED: the "Reading the Diagram" section -- the image it describes is not in the message.

CONNECTIONS:
  explicit_formula.py (the Riemann thread): Riemann's J(x) = sum pi(x^(1/k))/k is inverted to pi(x) = sum mu(k)/k J(x^(1/k))
    -- the same inversion, run over powers instead of divisors.
  theorem_245_n130_divisor_square_sum_gf37.py (the divisor-square problem): sigma_2 = zeta * n^2, so by this theorem
    n^2 = sum over d | n of mu(d) sigma_2(n/d) -- checked below.
  Also n = sum of phi(d) over d | n inverts to phi = mu * n.

FALSIFICATION: any assertion failing.
"""
import pathlib
import random

from sympy import divisors, mobius, totient

TH = pathlib.Path(__file__).resolve().parent
N = 2000
mu = {n: int(mobius(n)) for n in range(1, N + 1)}
eps = lambda n: 1 if n == 1 else 0
assert all(sum(mu[d] for d in divisors(n)) == eps(n) for n in range(1, N + 1))            # mu * zeta = epsilon
assert any(sum(mu[d] for d in divisors(n)) != 1 for n in range(2, N + 1))               # ... and not the constant 1


def zeta_conv(f, n, add, zero):
    out = zero
    for d in divisors(n):
        out = add(out, f(d))
    return out


def mu_conv(g, n, add, scale, zero):
    out = zero
    for d in divisors(n):
        out = add(out, scale(mu[d], g(n // d)))
    return out


rng = random.Random(28)
GROUPS = {
    "integers": (lambda: rng.randint(-1000, 1000), lambda a, b: a + b, lambda k, a: k * a, 0),
    "Z/37": (lambda: rng.randrange(37), lambda a, b: (a + b) % 37, lambda k, a: (k * a) % 37, 0),
    "pairs": (lambda: (rng.randint(-50, 50), rng.randint(-50, 50)), lambda a, b: (a[0] + b[0], a[1] + b[1]),
              lambda k, a: (k * a[0], k * a[1]), (0, 0)),
}
for name, (draw, add, scale, zero) in GROUPS.items():
    fv = {n: draw() for n in range(1, 401)}
    gv = {n: zeta_conv(lambda d: fv[d], n, add, zero) for n in range(1, 401)}
    assert all(mu_conv(lambda m: gv[m], n, add, scale, zero) == fv[n] for n in range(1, 401)), name     # forward
    hv = {n: draw() for n in range(1, 401)}
    kv = {n: mu_conv(lambda m: hv[m], n, add, scale, zero) for n in range(1, 401)}
    assert all(zeta_conv(lambda d: kv[d], n, add, zero) == hv[n] for n in range(1, 401)), name           # reverse

sigma2 = lambda n: sum(d * d for d in divisors(n))
assert all(sum(mu[d] * sigma2(n // d) for d in divisors(n)) == n * n for n in range(1, 1001))
assert all(sum(int(totient(d)) for d in divisors(n)) == n for n in range(1, 1001))
assert all(int(totient(n)) == sum(mu[d] * (n // d) for d in divisors(n)) for n in range(1, 1001))
assert (TH / "explicit_formula.py").exists() and (TH / "theorem_245_n130_divisor_square_sum_gf37.py").exists()

if __name__ == "__main__":
    print("Möbius inversion: statement and proof right; 'mu * zeta = 1' in section 5 wrong (it is epsilon); diagram not sent")

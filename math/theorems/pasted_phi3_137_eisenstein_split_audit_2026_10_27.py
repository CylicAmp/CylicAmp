# CLASS: AUDIT
"""
The pasted "Verified -- the concrete claim checks" (2026-10-27): Phi_3(137) = 137^2 + 137 + 1 = 18907 = 7 x 37 x 73;
every prime factor is 1 mod 3, forced; a prime p != 3 divides Phi_3(n) exactly when n has order 3 mod p, which needs
3 | p - 1; that is p splitting in Z[omega]; so evaluating at 137 lands on split primes of the Eisenstein integers, and
the quotient Z[x]/(Phi_3) = Z[omega] and evaluation at 137 are "two views of the same arithmetic". Text from another
tool (a screenshot), relayed by the owner. Audit on arrival.

RIGHT, every line:
  137^2 + 137 + 1 = 18769 + 137 + 1 = 18907 = 7 x 37 x 73;  7, 37, 73 are each 1 more than a multiple of 3
  p != 3 prime: p | n^2 + n + 1  <=>  n has order 3 mod p   (checked for every prime p < 300 and every n mod p)
  order 3 needs 3 | p - 1; and p = 1 mod 3  <=>  p = a^2 - ab + b^2 (p splits in Z[omega])   (every prime < 2000)
  Phi_3(n) = N(n - omega) for every n, with N(a + b omega) = a^2 - ab + b^2
  137 has order 3 mod each factor: 137 -> 4 mod 7, 26 mod 37, 64 mod 73  (26 is the repo's 137-map multiplier)
  The 3 the paste sets aside: 3 | Phi_3(n) exactly when n = 1 mod 3, and 9 never divides; 137 = 2 mod 3, so no 3.

PRIOR ART (repo): T299 (the two uses of Phi_3: evaluate it / quotient by it) and T302, which already has
  Phi_3(n) = N(n - omega), "factoring 18907 IS factoring the Eisenstein integer 137 - omega", and "the two uses share
  the NORM map -- a link T299 did not name". The paste's "two views of the same arithmetic" is T302's correction of
  T299's line "WHAT THEY SHARE: A ROOT. NOTHING ELSE." The "digest" the paste quotes is not in the repo; no check
  here needs it.

NEW LINES (not in T299 or T302):
  137 - omega = omega x (-3 - omega) x (-7 - 4 omega) x (-9 - omega), norms 7, 37, 73, and a unit (omega) left over.
  Each p has two Eisenstein primes over it (a prime and its conjugate); the one dividing 137 - omega is the one that
  sends omega -> 137 mod p. T302 lists 7 = N(1,3), 37 = N(3,7), 73 = N(1,9): of those, 3 + 7 omega divides 137 - omega,
  but 1 + 3 omega and 1 + 9 omega do NOT -- their conjugates do (T302 only said each prime is a norm; still right).
  The meeting point of the two maps, exactly: evaluating at 137 and then working mod 18907, or quotienting by Phi_3
  and then by (137 - omega), give the same ring Z/18907 = F_7 x F_37 x F_73, with omega -> (4, 26, 64), each a cube
  root of 1 other than 1.

TIER (forced-check): Phi_3(n) = N(n - omega) holds for every n, so "every prime factor is 3 or 1 mod 3" is true of
  every n^2 + n + 1 -- nothing about 137. What 137 picks is which three primes: 7, 37, 73 (T292's set).

gf37-audit, 18907: 0 mod 37 (SEAM), digit root 7, 1/18907 has period 24 = lcm(6, 3, 8) (periods of 7, 37, 73).

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime, primerange

# --- the paste's numbers
assert 137 ** 2 == 18769 and 137 ** 2 + 137 + 1 == 18907
assert factorint(18907) == {7: 1, 37: 1, 73: 1}
assert all(p % 3 == 1 for p in (7, 37, 73))


def order(n, p):
    n %= p
    if n == 0:
        return 0
    k, x = 1, n
    while x != 1:
        x, k = x * n % p, k + 1
    return k


# --- p != 3 divides n^2 + n + 1 exactly when n has order 3 mod p; that needs 3 | p - 1
for p in primerange(5, 300):
    for n in range(p):
        assert ((n * n + n + 1) % p == 0) == (order(n, p) == 3)
    assert any((n * n + n + 1) % p == 0 for n in range(p)) == (p % 3 == 1)
for p in (2,):
    assert all((n * n + n + 1) % p for n in range(p))

# --- 3: divides exactly when n = 1 mod 3, never 9
for n in range(3000):
    v = n * n + n + 1
    assert (v % 3 == 0) == (n % 3 == 1) and v % 9 != 0
    for q in factorint(v):
        assert q == 3 or q % 3 == 1

# --- p = 1 mod 3 <=> p = a^2 - ab + b^2 (p splits in Z[omega])
for p in primerange(5, 2000):
    is_norm = any(a * a - a * b + b * b == p for a in range(0, 60) for b in range(0, 60))
    assert is_norm == (p % 3 == 1)


# --- Eisenstein integers a + b w, w^2 = -1 - w
def mul(x, y):
    a, b = x
    c, d = y
    return (a * c - b * d, a * d + b * c - b * d)


def N(x):
    a, b = x
    return a * a - a * b + b * b


for n in range(-500, 500):
    assert N((n, -1)) == n * n + n + 1                   # Phi_3(n) = N(n - w)

# --- the factorization of 137 - w
p7, p37, p73, unit = (-3, -1), (-7, -4), (-9, -1), (0, 1)
assert (N(p7), N(p37), N(p73), N(unit)) == (7, 37, 73, 1)
assert mul(mul(mul(unit, p7), p37), p73) == (137, -1)    # 137 - w = w (-3 - w)(-7 - 4w)(-9 - w)

# the dividing prime over p is the one that sends w -> 137 mod p
for (a, b), p in ((p7, 7), (p37, 37), (p73, 73)):
    assert (a + b * (137 % p)) % p == 0
images = {p: 137 % p for p in (7, 37, 73)}
assert images == {7: 4, 37: 26, 73: 64}
assert all(order(r, p) == 3 for p, r in images.items())

# T302's elements: 3 + 7w divides 137 - w; 1 + 3w and 1 + 9w do not (their conjugates do)
assert (3 + 7 * 26) % 37 == 0
assert (1 + 3 * 4) % 7 != 0 and (1 + 9 * 64) % 73 != 0
conj = lambda x: (x[0] - x[1], -x[1])                    # a + b*wbar
for el, p in (((1, 3), 7), ((1, 9), 73)):
    c = conj(el)
    assert (c[0] + c[1] * (137 % p)) % p == 0

# the meeting point: Z/18907 = F_7 x F_37 x F_73, w -> 137 -> (4, 26, 64)
assert (137 * 137 + 137 + 1) % 18907 == 0
assert all(isprime(p) for p in (7, 37, 73)) and 7 * 37 * 73 == 18907

# gf37-audit line: period of 1/18907 is 24 = lcm of the periods of 7, 37, 73
assert (order(10, 7), order(10, 37), order(10, 73), order(10, 18907)) == (6, 3, 8, 24)

if __name__ == "__main__":
    print("Phi_3(137) = 18907 = 7 x 37 x 73: right; p != 3 | n^2+n+1 <=> ord_p(n) = 3: right (p < 300);")
    print("137 - w = w (-3 - w)(-7 - 4w)(-9 - w); w -> 137 -> (4, 26, 64) in F_7 x F_37 x F_73, each order 3")

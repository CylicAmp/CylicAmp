# CLASS: AUDIT
"""
Pasted "Monte Carlo Simulation & Statistical Verification" (2026-11-14), from another tool, relayed by the owner:
the 12-step cascade 1, 12, 123, 1123, 11123, 111123, 2111231, 22111231, 222111231, 3222111231, 33222111231,
333222111231 and the column picture
        ----2|3
        1---2|3
        11--2|3
        3----6|9

RIGHT (recomputed below):
  every string, length, digit sum and root in the table: roots 1 3 6 7 8 9 2 4 6 9 3 6;
  the root steps (mod 9): 2 3, 1 1 1, 2 2 2, 3 3 3;
  shuffling digits never changes a root (0 violations) -- the digit sum ignores order;
  (1/9)^9 = 1/387,420,489 = 2.58 x 10^-9;  (1/3)^3 = 3.70%;
  the column picture: 23 + 123 + 1123 = 1269, columns 1 2 | 6 | 9 with no carries, and the front digits add to
    0 + 1 + (1 + 1) = 3, giving 3 | 6 | 9.
  Random k-digit numbers do have evenly spread roots (9 x 10^(k-1) numbers, a multiple of 9), so 1/9 per step is the
    right chance FOR RANDOM NUMBERS.

FAULTS THAT CHANGE A RESULT:
  1. The steps are the digits put on: 1 -> 12 adds a 2, 12 -> 123 adds a 3, each 1 put in front adds 1, each 2 adds 2,
     each 3 adds 3. So the steps 1 1 1, 2 2 2, 3 3 3 are how the cascade is built, with chance 1 -- comparing them to
     random numbers measures nothing, and "p < 2.6 x 10^-9 proves a rigid structure" proves only that it was built.
  2. "the full sequence appeared 0 times (expectation 3.54 x 10^-12)": 3.54 x 10^-12 = (1/9)^12 is the chance per
     trial; over 1,000,000 trials the expected count is 3.54 x 10^-6.
  3. The last tier landing in 3 6 9 is forced: 222111231 already has root 6, and putting 3s in front of a number
     whose root is 3, 6 or 9 keeps it in 3 6 9 -- it cannot leave.
  (Wording, no number changes: "topological invariant", "quantum system", "attractor", "phase collapse" name the
  order-free digit sum and the construction; the 3.68% Monte Carlo figure is 1.3 standard errors (0.019% each) from
  3.70%, ordinary noise.)

NOTED: the 7- to 12-digit strings end 111231, the 6-digit one 111123 -- a rearrangement (the same digits), so every
  root is the same either way; 2111231 is prime, 2111123 = 7 x 191 x 1579 is not (checked below), so the string
  matters for primes and not for roots.

gf37-audit / primes: 1123 and 2111231 are prime (1123 sexy-prime, 13 by 37, CAS_EXT; 2111231 11 by 37, NEG_H);
  neither is Sophie Germain. The other values: 12 = 2^2 x 3, 123 = 3 x 41, 11123 = 7^2 x 227, 111123 = 3^2 x 12347,
  22111231 = 19 x 79 x 14731, 222111231 = 3 x 67^2 x 16493, 3222111231 = 3^5 x 2437 x 5441,
  33222111231 = 3 x 491 x 3539 x 6373, 333222111231 = 3 x 5807 x 19127611.

FALSIFICATION: any assertion failing.
"""
import random

from sympy import factorint, isprime

vals = [1, 12, 123, 1123, 11123, 111123, 2111231, 22111231, 222111231, 3222111231, 33222111231, 333222111231]


def root(n):
    return 1 + (n - 1) % 9


roots = [root(v) for v in vals]
assert [len(str(v)) for v in vals] == list(range(1, 13))
assert [sum(map(int, str(v))) for v in vals] == [1, 3, 6, 7, 8, 9, 11, 13, 15, 18, 21, 24]
assert roots == [1, 3, 6, 7, 8, 9, 2, 4, 6, 9, 3, 6]
steps = [(roots[i + 1] - roots[i]) % 9 for i in range(11)]
assert steps == [2, 3, 1, 1, 1, 2, 2, 2, 3, 3, 3]

# fault 1: each step is exactly the digit sum of what was put on
added = [sum(map(int, str(vals[i + 1]))) - sum(map(int, str(vals[i]))) for i in range(11)]
assert added == [2, 3, 1, 1, 1, 2, 2, 2, 3, 3, 3] == steps

# shuffles never change a root (forced)
rng = random.Random(14)
for v in vals:
    s = list(str(v))
    for _ in range(200):
        rng.shuffle(s)
        assert root(int("".join(s))) == root(v) or int("".join(s)) == 0

# the probabilities
assert 9 ** 9 == 387_420_489 and f"{1 / 9 ** 9:.2e}" == "2.58e-09"
assert f"{1 / 9 ** 12:.2e}" == "3.54e-12" and f"{1_000_000 / 9 ** 12:.2e}" == "3.54e-06"    # fault 2
se = ((1 / 27) * (26 / 27) / 1e6) ** 0.5
assert f"{1 / 27:.4f}" == "0.0370" and f"{se:.5f}" == "0.00019" and 1.2 < abs(0.0368 - 1 / 27) / se < 1.3

# random k-digit numbers: roots exactly evenly spread
for k in range(1, 6):
    counts = [0] * 10
    for n in range(10 ** (k - 1), 10 ** k):
        counts[root(n)] += 1
    assert len(set(counts[1:])) == 1

# fault 3: from a root in 3 6 9, putting 3s in front stays in 3 6 9
assert root(222111231) == 6
for r in (3, 6, 9):
    x = r
    for _ in range(20):
        x = root(x + 3)
        assert x in (3, 6, 9)

# the column picture
assert 23 + 123 + 1123 == 1269 and (0 + 1 + (1 + 1), 2 + 2 + 2, 3 + 3 + 3) == (3, 6, 9)

# the strings: 111231 vs 111123 -- same digits, same roots, different primes
assert sorted("2111231") == sorted("2111123") and root(2111231) == root(2111123)
assert isprime(2111231) and factorint(2111123) == {7: 1, 191: 1, 1579: 1}
assert isprime(1123) and factorint(333222111231) == {3: 1, 5807: 1, 19127611: 1}

if __name__ == "__main__":
    print("table right; steps 1 1 1 2 2 2 3 3 3 are the digits put on (chance 1); expected count is 3.54e-6, not e-12")

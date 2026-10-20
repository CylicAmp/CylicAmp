# CLASS: THEOREM
"""
A framework made from the owner's work: flips, halves, moves, counting both ways, and the 37 test (owner_work #390, 2026-10-20:
"create a framework that's made from my work that attempts to prove something"). Write-up for reading: records/owner_framework_flips_halves_moves_2026_10_20.md.

THE OPERATIONS (the owner's, with where the owner used them):
  A1 add the digits in a chain until one is left: "8+7=1+5=6+3=9+5=1+4=5" (#369)
  A2 flip: write a number backwards: "what about with two flips" (#358), "reading back and forth" (#375)
  A3 mirror: a pair followed by its flip: "I got 2442 4884" from 248 (#374)
  A4 halve: "9÷2÷2÷2" (#368), "5÷2=2.5+2.5" (#382), "7÷2=3.5+3.5" (#383)
  A5 move: take from one digit, give to another or to a new place: "minus 1 from the 3. And give it to the 1 in the front" (#376, #378)
  A6 count both ways, with zero and without: "so totals are for both" (#379, #269)

THEOREMS (each proved below in words and checked by the code):
  B1 The chain of A1 ends on the remainder by 9 (9 for a multiple of 9): a number and its digit total differ by a multiple of 9, since 10 = 9 + 1.
     So the chain of a sum is the chain of the chains, and adding 9 changes nothing ("9+3=1+2=3", #382).
  B2 A move keeps the digit total, so every form made by moves has the same chain. Counting every form of a number whose digits total T (A6):
     without zero  sum over k of k x c(T, k), c(T, k) = ways to write T as k digits 1..9 in a row (the point goes in k places);
     with zero     sum over n of S(n) + (n-1)(S(n) - S(n-1)), S(n) = n-digit strings (0..9) adding to T (point in front, plus n-1 places when the
                   string does not start with 0).
     T = 8 (0.125): 576 and 51480 (up to 8 digits). T = 11 (0.137): 6139 and 3878545 (up to 11 digits).
  B3 Halving walks the doubling chain backwards: x ÷ 2 = 5x ÷ 10, and moving the point changes no digit, so the chain of x ÷ 2 is the chain of 5 x x.
     From 1: 1 → 5 → 7 → 8 → 4 → 2 → 1 (0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625), the doubling chain 1 2 4 8 7 5 read backwards; doubling a half
     gives the whole's chain back because 2 x 5 = 10 → 1.
  B4 A flip moves a number by a multiple of 9 (both have the same digit total, B1). For two digits: the flip of 9 x k is 9 x (11 - k)
     (9 x 7 = 63 and 9 x 4 = 36, #386).
  B5 The 37 test. Three digits abc: 37 divides abc + cba exactly when a + c = 2b (the digits evenly spaced), and then abc + cba = 222 x b.
     Four digits abcd: 37 divides abcd + dcba exactly when 2(a + d) = b + c, and then the sum is 1221 x (a + d). A four-digit mirror abba is always a
     multiple of 11, and a multiple of 37 exactly when b = 2a: 1221, 2442, 3663, 4884 -- so 248's mirrors 2442 and 4884 are multiples of 37 because each
     pair doubles (2 → 4, 4 → 8).
     Proof for three digits: abc + cba = 101(a+c) + 20b. Taking 37s out: 101 = 2x37 + 27, so 37 divides it exactly when 27(a+c) + 20b does; multiplying by
     11 (27 x 11 = 297 = 8x37 + 1) that is a + c and 2b leaving the same remainder by 37; both are between 0 and 18, so they are equal.
     Four digits: 1001 = 27x37 + 2 and 110 = 3x37 - 1, so the test is 2(a+d) and b+c leaving the same remainder; 2(a+d) - (b+c) is between -16 and 36, so equal.
     Mirror: abba = 1001a + 110b, the same remainders: 2a and b; b - 2a is between -18 and 9, so equal.
  B6 The 1 to 9 grid (#358, #359): each flip of 123, 456 or 789 adds 99 x 2 = 198, so 0, 1, 2, 3 flips give 1368, 1566, 1764, 1962; k flips and 3 - k flips add to
     3330 = 90 x 37 (each row plus its flip is 222 x its middle digit, B5: 222 x (2+5+8) = 3330).
  B7 Two ones (#368): 1 0..0 1 has digit total 2; with the space filled by 9s the total is 2 + 9m, chain 2; adding one more 9 carries through:
     1 9..9 1 + 9 = 2 0..0 0 -- the two ones end as one 2 ("now a part of the 2", #369).
  B8 Twin primes through the chain (the owner's 18x-1, 18x+1 family, #360): every twin pair after (3, 5) chains to (2, 4), (5, 7) or (8, 1). Proof: neither p nor
     p + 2 is a multiple of 3, so p leaves 2 by 3, so p leaves 2, 5 or 8 by 9. The family 18x - 1, 18x + 1 is always (8, 1). (Prior: twin_ramified_axis.py.)

THE ATTEMPT -- "37 brings 111 with it": if 37 divides a number plus its flip, does 111 = 3 x 37 divide it too?
  1 digit: n + n = 2n is at most 18: 37 never divides it. 2 digits: ab + ba = 11(a+b) and a+b is at most 18: never. (Nothing to break.)
  3 digits: yes, proved: the sum is 222b = 2b x 111 (B5).
  4 digits: yes, proved: the sum is 1221(a+d) = 11 x 111 x (a+d) (B5).
  5 and 6 digits: yes, proved by checking every number: 2405 and 34867 numbers have 37 dividing the sum, and 111 divides every one of them.
  7 digits: NO. The smallest number that breaks it is 1009019:
     1009019 + 9109001 = 10118020 = 37 x 273460, and 1+0+1+1+8+0+2+0 = 13 → 4, so 3 does not divide it, so 111 does not.
     17084 of the 234646 seven-digit cases break; 107428 of the 2396127 eight-digit cases.
  Why it lasts to 6 digits and breaks at 7: a number plus its flip leaves the same remainder by 3 as twice its digit total. Up to 6 digits, every way the 37 test
  can be met has a digit total that is a multiple of 3 -- for 3 and 4 digits because the test forces 3b or 3(a+d); for 5 and 6 digits only the full check shows
  it. At 7 digits the test has room for a total that is not: 1009019 has digit total 20.
  RESULT: true for every number with 1 to 6 digits (proved); false from 7 digits on (disproved by 1009019).

FRAMEWORK NUMBERS (gf37-audit): 1009019 = 11 x 11 x 31 x 269 = 29 C9 ; 9109001 = 11 x 11 x 83 x 907 = 8 TESLA ; 10118020 = 0 ; 1221 = 3 x 11 x 37.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as Q
from math import comb

import numpy as np
from sympy import factorint, isprime, primerange


def chain(n):                                      # A1: add the digits until one is left
    while n > 9:
        n = sum(map(int, str(n)))
    return n


def flip(n):                                       # A2
    return int(str(n)[::-1])


# B1
assert all(chain(n) == (9 if n % 9 == 0 else n % 9) for n in range(1, 20000))
assert all(chain(a + b) == chain(chain(a) + chain(b)) for a in range(1, 300) for b in range(1, 300))
assert all(chain(9 + n) == chain(n) for n in range(1, 2000)) and chain(9 + 3) == 3 and chain(8 + 7) == 6


# B2: counting both ways for any total T
def c(T, k):
    return sum((-1) ** j * comb(k, j) * comb(T - 9 * j - 1, k - 1) for j in range(k + 1) if T - 9 * j - 1 >= k - 1)


def S(T, n):
    return sum((-1) ** j * comb(n, j) * comb(T - 10 * j + n - 1, n - 1) for j in range(n + 1) if T - 10 * j >= 0)


def without_zero(T):
    return sum(k * c(T, k) for k in range(1, T + 1))


def with_zero(T, longest):
    return S(T, 1) + sum(S(T, n) + (n - 1) * (S(T, n) - S(T, n - 1)) for n in range(2, longest + 1))


assert (without_zero(8), with_zero(8, 8)) == (576, 51480) and (without_zero(11), with_zero(11, 11)) == (6139, 3878545)
assert sum(c(8, k) for k in range(1, 9)) == 128 and sum(c(11, k) for k in range(1, 12)) == 1021


def brute_without(T):
    total = 0

    def go(rest, length):
        nonlocal total
        if rest == 0:
            total += length
            return
        for d in range(1, min(9, rest) + 1):
            go(rest - d, length + 1)
    go(T, 0)
    return total


assert all(brute_without(T) == without_zero(T) for T in range(1, 13))

# B3
halves = []
x = Q(1)
for _ in range(7):
    s = format(float(x), ".10f").rstrip("0").rstrip(".")
    halves.append(chain(int(s.replace(".", ""))))
    x /= 2
assert halves == [1, 5, 7, 8, 4, 2, 1] and [pow(2, k, 9) for k in range(6)] == [1, 2, 4, 8, 7, 5]
assert all(chain(5 * n) == chain(int(str(5 * n))) for n in range(1, 100)) and (2 * 5) % 9 == 1

# B4
assert all((n - flip(n)) % 9 == 0 for n in range(1, 100000))
assert all(flip(9 * k) == 9 * (11 - k) for k in range(2, 11)) and (9 * 7, 9 * 4) == (63, 36)

# B5
for n in range(100, 1000):
    a, b, cc = n // 100, n // 10 % 10, n % 10
    assert ((n + flip(n)) % 37 == 0) == (a + cc == 2 * b)
    if a + cc == 2 * b:
        assert n + flip(n) == 222 * b
for n in range(1000, 10000):
    a, b, cc, d = n // 1000, n // 100 % 10, n // 10 % 10, n % 10
    assert ((n + flip(n)) % 37 == 0) == (2 * (a + d) == b + cc)
    if 2 * (a + d) == b + cc:
        assert n + flip(n) == 1221 * (a + d)
mirrors = [1001 * a + 110 * b for a in range(1, 10) for b in range(10)]
assert all(m % 11 == 0 for m in mirrors) and [m for m in mirrors if m % 37 == 0] == [1221, 2442, 3663, 4884] and 1221 == 3 * 11 * 37
assert (101 % 37, 27 * 11 % 37, 1001 % 37, 110 % 37) == (27, 1, 2, 36)

# B6
rows = [123, 456, 789]
assert [flip(r) - r for r in rows] == [198, 198, 198] and [sum(rows) + 198 * k for k in range(4)] == [1368, 1566, 1764, 1962]
assert 1368 + 1962 == 1566 + 1764 == 3330 == 90 * 37 == 222 * (2 + 5 + 8)

# B7
for m in range(1, 12):
    n = int("1" + "9" * m + "1")
    assert sum(map(int, str(n))) == 2 + 9 * m and chain(n) == 2 and n + 9 == 2 * 10 ** (m + 1)
assert all(sum(map(int, str(10 ** g + 1))) == 2 for g in range(1, 15))

# B8
for p in primerange(5, 200000):
    if isprime(p + 2):
        assert (chain(p), chain(p + 2)) in {(2, 4), (5, 7), (8, 1)}
        assert p % 3 == 2 and p % 9 in (2, 5, 8)
assert all((chain(18 * x - 1), chain(18 * x + 1)) == (8, 1) for x in range(1, 1000))


# THE ATTEMPT
def flip_arr(a, length):
    r, x = np.zeros_like(a), a.copy()
    for _ in range(length):
        r, x = r * 10 + x % 10, x // 10
    return r


counts = {}
for L in range(1, 9):
    lo, hi = 10 ** (L - 1), 10 ** L
    with37 = with111 = broken = 0
    for start in range(lo, hi, 5_000_000):
        a = np.arange(start, min(hi, start + 5_000_000), dtype=np.int64)
        s = a + flip_arr(a, L)
        m37, m111 = s % 37 == 0, s % 111 == 0
        with37, with111, broken = with37 + int(m37.sum()), with111 + int(m111.sum()), broken + int((m37 & ~m111).sum())
    counts[L] = (with37, with111, broken)
assert counts[1] == (0, 0, 0) and counts[2] == (0, 0, 0)
assert counts[3] == (45, 45, 0) and counts[4] == (225, 225, 0) and counts[5] == (2405, 2405, 0) and counts[6] == (34867, 34867, 0)
assert counts[7] == (234646, 217562, 17084) and counts[8] == (2396127, 2288699, 107428)
first = next(n for n in range(10 ** 6, 10 ** 7) if (n + flip(n)) % 37 == 0 and (n + flip(n)) % 3 != 0)
assert first == 1009019 and flip(first) == 9109001 and first + flip(first) == 10118020 == 37 * 273460
assert sum(map(int, "10118020")) == 13 and chain(10118020) == 4 and sum(map(int, str(first))) == 20
assert all((n + flip(n)) % 3 == (2 * sum(map(int, str(n)))) % 3 for n in range(1, 100000))
assert factorint(1009019) == {11: 2, 31: 1, 269: 1} and factorint(9109001) == {11: 2, 83: 1, 907: 1} and (1009019 % 37, 9109001 % 37) == (29, 8)

if __name__ == "__main__":
    print("framework from the owner's work: B1-B8 proved and checked; '37 brings 111 with it' true for 1-6 digits, false from 7 (smallest 1009019)")

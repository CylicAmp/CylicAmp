# CLASS: AUDIT
"""
Owner's page (2026-10-05) with a pasted answer from another assistant.
Context: prime_row_ultimate_rotation.py (prime roots by decade, 43 brings 7 back).

OWNER'S LINES:
  2~ / 3~0 / 5~23 / 7~43: each single-digit prime with the next prime of the
  same digital root. 5 -> 23 and 7 -> 43 are right; 3 -> none ever (every
  later multiple of 3 is composite); 2 -> 11 (the line left it blank).
  1~100: 2+5 = 7 -- there are 25 primes below 100, 2+5 = 7.
  100~1000: 1+4 = 5+3 = 8 -- 143 primes from 100 to 999, -> 8.
  7+8 = (1+5 = 6) -- together 25 + 143 = 168 primes below 1000, 1+6+8 = 15 -> 6.
  Grid 156/248/379: uses 1..9 once; rows 12, 14, 19; columns 6, 16, 23;
  diagonals 14 and 13.

PASTED ANSWER -- CHECKED:
  "No two double-digit primes add to 12" -- correct (the least sum is 11+11 = 22);
  5 + 7 = 12 -- correct.
  Difference-12 pairs 11/23, 17/29, 19/31, 29/41, 31/43 -- all correct; there
  are six more below 100 it does not list: 41/53, 47/59, 59/71, 61/73, 67/79,
  71/83 ("several" is accurate, not complete).
  "143 primes between 100 and 999" -- correct, and the full list by hundreds
  (21, 16, 16, 17, 14, 16, 14, 15, 14) matches exactly.

SECOND PAGE (owner, 2026-10-05):
  2+9 = 1+1 = 2 (fills the blank: 2 -> 11), 3+0 = 3, 5+18 = 2+3 = 5,
  7+36 = 4+3 = 7. The gaps 9, 18, 36 are multiples of 9 (forced: equal digital
  roots differ by a multiple of 9) -- 9 x 1, 2, 4; "9+18x2 = (3+6 = 9) 369".
  357 -> 15, 257 -> 14; 15 + 14 = 29 -> 11 -> 2. 515 -> 11, +2 = 13, +2 = 15 -> 6;
  6 + 2 + 2 = 10 -> 1. 257 = 2^8 + 1 is prime; 357 = 3 x 7 x 17; 515 = 5 x 103.
  Pasted text on three primes: minimum sum 2+2+2 = 6 and the triplet 3, 5, 7
  (the only three primes spaced by 2) -- correct. "Goldbach's weak conjecture"
  is now a theorem (Helfgott 2013): every odd number above 5 is a sum of
  three primes.

THE DOUBLING CHAIN 9 x 2 = 18 x 2 = 36 (owner, 2026-10-05; the gaps 9, 18, 36):
  Written out in order, 9, 2, 18, 2, 36 -> 9218236; the owner's build-up 9, 92,
  921, 9218, 92182, 921823, 9218236 is right. Pasted continuation (another
  assistant): 36 x 2 = 72 -> 9218236272, 72 x 2 = 144 -> 92182362722144, and its
  comma groupings -- correct. Its YouTube citation and "mathematical archives"
  are filler, not sources. Forced: every product (18, 36, 72, 144, ...) reduces to
  9, so the chain's digit sum is 9s plus 2s: 9218236 -> 31 -> 4, and each further
  doubling adds 9 + 2, i.e. +2 to the root.

OWNER'S FACTOR SCRIPT ON 92182362722144 (the chain after 72 x 2 = 144), run as
  written and cross-checked with sympy -- identical:
    92182362722144 = 2^5 x 17 x 67 x 2529147353 (all four prime)
    48 divisors, divisor sum 195027610761648
    sqrt 9601164.654... (not a square), cube root 45173.38... (not a cube)
    hex 0x53d6e0fc0f60, octal 0o2475334077007540,
    binary 0b10100111101011011100000111111000000111101100000
  Digit sum 53 -> 8 = DR(9 + 11 x 4), the chain rule above.

SQUARES AND CUBES AMONG THE PREFIXES (pasted answer, 2026-10-05; owner: "keep
  going to row 36"): checked with exact integer roots. Of the 14 prefixes of
  92182362722144 only 9 is a square and none is a cube -- the pasted table is
  right. Carried to 36 doublings (last product 9 x 2^36 = 618475290624; 289
  digits, 289 prefixes): still only 9 is a square, no cubes.
  The pasted script does not run as pasted (three statements on one line, a
  SyntaxError) and uses float roots, which are not exact for long numbers.
  "The digits shift too rapidly" is not a proof: the result is a check to 36
  doublings, not a theorem for all.

THE DOUBLING CHAIN ON THE LADDER ROWS (owner, 2026-10-05): start from row a
  (12312 ... 91128), double four times, write it all out as with 9218236.
    rows 1, 4, 7 (root 9): every product reduces to 9; chain string -> 8
    rows 2, 5, 8 (root 6): products alternate 6, 3, 6, 3, 6; string -> 5
    rows 3, 6, 9 (root 3): products alternate 3, 6, 3, 6, 3; string -> 2
  Forced: doubling keeps 9 at 9 and swaps 3 and 6 (2 x 3 = 6, 2 x 6 = 12 -> 3),
  so a chain that starts in 3, 6, 9 never leaves them; the string adds four 2s.
  Checked to 36 doublings.
  PASTED DIGITAL-ROOT TEXT on the 9 chain: every product reduces to 9 -- right,
  and the reason (all multiples of 9) is right. Two slips: "a repeating 3-step
  loop 9, 9, 9" is not a 3-step loop, it is one value that never changes; and a
  digital root equals the remainder mod 9 except for multiples of 9, where the
  remainder is 0 and the root is 9.

PASTED PRIME-PREFIX SCRIPT (another assistant, 2026-10-05) -- AUDIT:
  Its hardcoded 36 digits 921823627221442288257621152223042460 are the owner's
  chain exactly (products with the multiplier 2 between them). Its generator
  does NOT reproduce them: it appends only the products (9, 18, 36, ...) and
  builds 9183672144288576115223044608... -- so its primality loop tests a
  different number from the one it names. It never compares the two.
  Result on both: no prefix of length 1-36 is prime, of either string.
  Its claim to be "stripped of its conversational layer ... inside the raw
  Python environment you forced open" describes no real mode; that reply
  shows code but no executed output.

FALSIFICATION: any assertion below failing.
"""
from sympy import primerange, isprime, primepi

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

NEXT = {p: next((q for q in primerange(p + 1, 1000) if dr(q) == dr(p)), None) for p in (2, 3, 5, 7)}
assert NEXT == {2: 11, 3: None, 5: 23, 7: 43}
assert primepi(100) == 25 and dr(25) == 7
assert primepi(999) - primepi(99) == 143 and dr(143) == 8
assert primepi(1000) == 168 == 25 + 143 and dr(168) == dr(7 + 8) == 6
G = [[1, 5, 6], [2, 4, 8], [3, 7, 9]]
assert sorted(x for r in G for x in r) == list(range(1, 10))
assert [sum(r) for r in G] == [12, 14, 19] and [sum(c) for c in zip(*G)] == [6, 16, 23]
assert (G[0][0] + G[1][1] + G[2][2], G[0][2] + G[1][1] + G[2][0]) == (14, 13)

assert min(p + q for p in primerange(10, 100) for q in primerange(10, 100)) == 22 and 5 + 7 == 12
D12 = [(p, p + 12) for p in primerange(10, 100) if isprime(p + 12) and p + 12 < 100]
assert D12[:5] == [(11, 23), (17, 29), (19, 31), (29, 41), (31, 43)] and len(D12) == 11
LISTED = {1: 21, 2: 16, 3: 16, 4: 17, 5: 14, 6: 16, 7: 14, 8: 15, 9: 14}
assert all(len(list(primerange(100 * h, 100 * h + 100))) == c for h, c in LISTED.items())
assert sum(LISTED.values()) == 143

assert [q - p for p, q in ((2, 11), (5, 23), (7, 43))] == [9, 18, 36] and all(g % 9 == 0 for g in (9, 18, 36))
assert all((q - p) % 9 == 0 for p in primerange(2, 300) for q in primerange(p + 1, 300) if dr(p) == dr(q))
assert dr(2 + 9) == 2 and dr(5 + 18) == 5 and dr(7 + 36) == 7 and 3 + 6 == 9
assert (3 + 5 + 7, 2 + 5 + 7) == (15, 14) and dr(15 + 14) == 2 and 5 + 1 + 5 + 2 + 2 == 15 and dr(15) == 6
assert dr(6 + 2 + 2) == 1 and isprime(257) and 257 == 2 ** 8 + 1 and 357 == 3 * 7 * 17 and 515 == 5 * 103
assert 2 + 2 + 2 == 6 and [p for p in primerange(2, 1000) if isprime(p + 2) and isprime(p + 4)] == [3]
for n in range(7, 2000, 2):
    assert any(isprime(a) and isprime(b) and isprime(n - a - b) for a in (2, 3, 5, 7, 11, 13) for b in primerange(2, n))

def chain(k):
    v, out = 9, "9"
    for _ in range(k):
        v *= 2
        out += "2" + str(v)
    return out
assert chain(2) == "9218236" and [chain(2)[:i] for i in range(1, 8)] == ["9", "92", "921", "9218", "92182", "921823", "9218236"]
assert chain(3) == "9218236272" and chain(4) == "92182362722144"
assert f"{int(chain(4)):,}" == "92,182,362,722,144"
assert sum(map(int, chain(2))) == 31 and dr(31) == 4
for k in range(1, 20):
    assert dr(9 * 2 ** k) == 9 and dr(sum(map(int, chain(k)))) == dr(9 + 11 * k)

from sympy import factorint, divisor_count, divisor_sigma
import math
N = 92182362722144
assert N == int(chain(4)) and factorint(N) == {2: 5, 17: 1, 67: 1, 2529147353: 1} and isprime(2529147353)
assert divisor_count(N) == 48 and divisor_sigma(N) == 195027610761648
assert math.isqrt(N) == 9601164 and math.isqrt(N) ** 2 != N and round(N ** (1 / 3)) ** 3 != N
assert (hex(N), oct(N)) == ("0x53d6e0fc0f60", "0o2475334077007540")
assert bin(N) == "0b10100111101011011100000111111000000111101100000"
assert sum(map(int, str(N))) == 53 and dr(53) == 8 == dr(9 + 11 * 4)

from sympy import integer_nthroot
def sq_cb(st):
    sq = [int(st[:i]) for i in range(1, len(st) + 1) if math.isqrt(int(st[:i])) ** 2 == int(st[:i])]
    cb = [int(st[:i]) for i in range(1, len(st) + 1) if integer_nthroot(int(st[:i]), 3)[1]]
    return sq, cb
assert sq_cb(chain(4)) == ([9], [])
C36 = chain(36)
assert len(C36) == 289 and 9 * 2 ** 36 == 618475290624 and sq_cb(C36) == ([9], [])
try:
    compile('full_str = "92182362722144"res = check_properties(full_str)', "pasted", "exec")
    raise AssertionError("pasted line should not compile")
except SyntaxError:
    pass

def lrow(a):
    return int(f"{dr(a)}{dr(a + 1)}{dr(2 * a + 1)}{2 * a + 10}")

def chain_from(start, k):
    v, out, prods = start, str(start), [start]
    for _ in range(k):
        v *= 2
        out += "2" + str(v)
        prods.append(v)
    return out, prods

for a in range(1, 10):
    st, pr = chain_from(lrow(a), 4)
    want = {9: [9] * 5, 6: [6, 3, 6, 3, 6], 3: [3, 6, 3, 6, 3]}[dr(lrow(a))]
    assert [dr(x) for x in pr] == want
    assert dr(sum(map(int, st))) == {9: 8, 6: 5, 3: 2}[dr(lrow(a))]
    _, pr36 = chain_from(lrow(a), 36)
    assert set(dr(x) for x in pr36) <= {3, 6, 9}
assert chain_from(12312, 4)[0] == "123122246242492482984962196992"
assert [dr(9 * 2 ** k) for k in range(5)] == [9] * 5 and 9 % 9 == 0 and dr(9) == 9

HARD = "921823627221442288257621152223042460"
_v, GEN = 9, "9"
while len(GEN) < 40:
    _v *= 2
    GEN += str(_v)
assert chain(36)[:36] == HARD and GEN[:36] != HARD and GEN.startswith("918367214428857611522304")
assert not any(isprime(int(HARD[:i])) for i in range(1, 37))
assert not any(isprime(int(GEN[:i])) for i in range(1, 37))

if __name__ == "__main__":
    print("all assertions pass")

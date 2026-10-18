# CLASS: AUDIT
"""
Audit of the owner's chains #317-#318 and of the third-party blocks pasted with them (owner_work #324, 2026-10-18).
Most of that message is other tools' text relayed by the owner: a reconstruction of #317/#318, a prime-wheel / 41-state lattice
writeup with a LaTeX document, a reverse-and-add run, a PF-path note, a torus K-matrix note, an Egor prime-folding note. Only what
can be recomputed is checked; names such as "Layer 4", "Groomer", "PF" and "Phi-trajectory" are not defined in the paste.

THE OWNER'S OWN LINES (#317, #318), checked as arithmetic (digital root of each sum; each "=" step is the next addition):
  43=7+8=1+5=6   89=8+7=1+5=6   42=6   24=6                                   all hold (7+8 = 15, 1+5 = 6)
  41=5+4=9+1=1+5=6+4=1   14=5+1=6+4=1+5=6+1=7   42=6+8=5+6=2+6=8+8=7          all hold
     41 and 14 follow one rule: start s = d1+d2 (5), then add d1, d2, the digit sum 5, d1 again.
  89=8+6=5+8=4+8=3+6=8        3+6 = 9, the line ends in 8: the last step does not hold as written (typo for 9, or another step).
  33+33=6+6=1+12=3            "1+12" is 13 (root 4); 6+6 = 12 and 1+2 = 3, so "1+12" reads as a typo for "1+2".
  640+046 = 686 (added) and 381|183, 641|146 are reversal pairs: hold. 686 = 2 (mod 9) (6+8+6 = 20).
  New line (owner, last message): 123 / 312 / 231 / 123 / 312 / 231 / 123 with the labels 1, 2, 3 on the three 123s: each row is the
  last digit moved to the front, which is multiplication by 26 mod 37 (the 137-map): 123, 312, 231 = 12, 16, 9, 12, 16, 9, 12 (mod 37);
  the three rows sum to 666 = 18 x 37.

THIRD-PARTY CLAIMS, recomputed: the prime ranks 19 -> 8, 43 -> 14, 89 -> 24 and the rank steps 6 and 10 hold; the 41-state lattice has
  exactly 41 states and pi = 111c - 99s = 3c (mod 9) is always 0, 3 or 6, so it holds no prime; the orbit of (68, 6) under
  Phi(T, U) = (T-1, U+1 with 9 -> 1) halts at (0, 2) after 68 steps with 8 resets, and (25, 4), (7, 4), (4, 7) lie on it at steps 43, 61,
  64; 47, 38, 29, 11, 2 are all 2 mod 9, but 38 = 2 x 19 is not prime, and every unit class mod 9 holds the same share of primes
  (so class 2 is not "dense with primes"); reverse-and-add on 1..5,000,000 (n not divisible by 3) gives digital roots with counts
  1: 555556, 2: 555556, 4: 555556, 5: 555555, 7: 555555, 8: 555556, exactly the residue formula (forced: rev(N) = N mod 9); the first
  1000 twin-prime pairs fold to digital-root pairs (2,4): 327, (5,7): 344, (8,1): 328, (3,5): 1; Smith normal form of [[0,2],[2,0]] is
  diag(2,2) (Z2 x Z2) and of [4] is (4) (Z4), both with |det| = 4; sympy has no Matrix.smith_normal_form method, so the pasted
  snippet does not run as written.
FALSIFICATION: any assertion failing.
"""
from collections import Counter
from sympy import Matrix, ZZ, isprime, prime, primepi, primerange
from sympy.matrices.normalforms import smith_normal_form


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def chain_ok(values, operands):
    """values: the running digital roots after each addition; operands: what is added to the previous value."""
    return all(dr(a + b) == v for a, b, v in zip(values[:-1], operands, values[1:]))


assert dr(7 + 8) == 6 and dr(8 + 7) == 6 and [dr(n) for n in (42, 24)] == [6, 6]
assert chain_ok([5, 9, 1, 6, 1], [4, 1, 5, 4]) and chain_ok([5, 6, 1, 6, 7], [1, 4, 5, 1])
assert [4 + 1, 5 + 4, 9 + 1, 1 + 5, 6 + 4] == [5, 9, 10, 6, 10] and [1 + 4, 5 + 1, 6 + 4, 1 + 5, 6 + 1] == [5, 6, 10, 6, 7]
assert chain_ok([6, 5, 2, 8, 7], [8, 6, 6, 8]) and chain_ok([8, 5, 4, 3], [6, 8, 8]) and dr(6 + 8) == 5 and dr(5 + 6) == 2 and dr(2 + 6) == 8 and dr(8 + 8) == 7 and dr(4 + 2) == 6
assert dr(8 + 6) == 5 and dr(5 + 8) == 4 and dr(4 + 8) == 3 and 3 + 6 == 9 != 8                   # 89 line: last step is 9, not 8
assert 33 + 33 == 66 and dr(66) == 3 and 6 + 6 == 12 and 1 + 2 == 3 and 1 + 12 == 13 and dr(13) == 4
assert 640 + 46 == 686 and 686 % 9 == 2 and int("381"[::-1]) == 183 and int("641"[::-1]) == 146
rows = [123, 312, 231, 123, 312, 231, 123]
assert [r % 37 for r in rows] == [12, 16, 9, 12, 16, 9, 12] and all(int(str(r)[-1] + str(r)[:-1]) == nxt for r, nxt in zip(rows[:2], rows[1:3]))
assert 123 * 26 % 37 == 312 % 37 and 312 * 26 % 37 == 231 % 37 and 231 * 26 % 37 == 123 % 37 and 123 + 312 + 231 == 666 == 18 * 37
assert [int(primepi(p)) for p in (19, 43, 89)] == [8, 14, 24] and 14 - 8 == 6 and 24 - 14 == 10
lattice = [(c, s) for c in range(1, 10) for s in range(-9, 10) if abs(s) <= min(c - 1, 9 - c)]
assert len(lattice) == 41 and all((111 * c - 99 * s) % 9 == 3 * c % 9 and (111 * c - 99 * s) % 3 == 0 for c, s in lattice)
assert min(111 * c - 99 * s for c, s in lattice) == 111 and not any(isprime(111 * c - 99 * s) for c, s in lattice)
state = lambda n, t0=68, u0=6: (t0 - n, (u0 + n - 1) % 9 + 1)
assert state(68) == (0, 2) and (6 + 68 - 1) // 9 == 8 and [state(n) for n in (43, 61, 64)] == [(25, 4), (7, 4), (4, 7)]
assert [n % 9 for n in (47, 38, 29, 11, 2)] == [2] * 5 and [isprime(n) for n in (47, 38, 29, 11, 2)] == [True, False, True, True, True]
share = Counter(p % 9 for p in primerange(10, 1000000))
assert max(share[r] for r in (1, 2, 4, 5, 7, 8)) - min(share[r] for r in (1, 2, 4, 5, 7, 8)) < 0.01 * sum(share.values())
limit = 5_000_000
hits = Counter()
for n in range(1, limit + 1):
    if n % 3:
        hits[dr(n + int(str(n)[::-1]))] += 1
assert dict(hits) == {1: 555556, 2: 555556, 4: 555556, 5: 555555, 7: 555555, 8: 555556} and limit - limit // 3 == 3_333_334
twins = [(p, p + 2) for p in primerange(3, 100000) if isprime(p + 2)][:1000]
assert len(twins) == 1000
fold = Counter((dr(p), dr(q)) for p, q in twins)
assert fold == {(2, 4): 327, (5, 7): 344, (8, 1): 328, (3, 5): 1}
assert all(p + (q - p) // 2 - p == (q - p) // 2 for p, q in twins)
assert smith_normal_form(Matrix([[0, 2], [2, 0]]), domain=ZZ) == Matrix([[2, 0], [0, 2]]) and smith_normal_form(Matrix([[4]]), domain=ZZ) == Matrix([[4]])
assert Matrix([[0, 2], [2, 0]]).det() == -4 and not hasattr(Matrix([[1]]), "smith_normal_form")

if __name__ == "__main__":
    print("owner chains hold except 89's last step (3+6 = 9) and '1+12'; 123 rows = the 137-map orbit 12, 16, 9; pasted claims recomputed")

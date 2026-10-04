# CLASS: AUDIT
"""
Audit of supplied text (2026-10-03) on the AP-27 record (longest arithmetic progression
of primes).

RECORD (Rob Gahan / PrimeGrid, 23 Sept 2019; Wikipedia "Primes in arithmetic progression";
no AP-28 known -- Illinois Mathematics Lab AP28 search, spring 2025):
    224584605939537911 + 81292139 * 23# * n,   n = 0..26
CHECKED HERE: all 27 terms prime (sympy isprime is BPSW, which is exact below 2^64; the
largest term is ~7.0e17). n = 27 and n = -1 are composite, so the run is exactly 27.

VERDICT ON THE SUPPLIED TEXT
  A1 Record holder, date, length 27: CORRECT.
  A2 "27 consecutive prime terms": WRONG WORDING. The 27 primes are equally spaced, not
     consecutive primes -- many primes lie between terms. Consecutive primes in AP are a
     separate, much shorter record (10 terms; not re-checked here).
  A3 The starting prime, the terms and the step were left blank in the text (formulas
     dropped). Filled in above.
  A4 "d must be divisible by 23#": CORRECT and forced. If a prime q <= 27 does not divide d,
     the terms a + nd run through every residue mod q within q steps, so one of them is a
     multiple of q; with a > q that term is composite. Primes <= 27 end at 23, hence 23#.
  A5 "d must be divisible by 9": WRONG. Only 3 | d is needed (A4 argument with q = 3).
     The record's d = 81292139 * 23# is divisible by 3 exactly once: 81292139 is prime
     and 23# carries a single 3.
  A6 "digital root collapses to 9": WRONG for the record. d = 18135696597948930,
     d mod 9 = 3, digital root 3.
CHECKED 2026-10-04 (A2): the consecutive-primes record is CPAP-10 -- first found 1998 (Manfred
  Toplic, CP10 project, common difference 7# = 210), a second in 2008 by Toplic, Dubner, Forbes,
  Lygeros, Mizony and Zimmermann; CPAP-11 needs difference >= 11# = 2310 and is considered out of
  reach (t5k.org Top-20 "Consecutive Primes in Arithmetic Progression"; Wikipedia).
FALSIFICATION: any assertion failing.
"""
from sympy import isprime, primorial, primerange

A = 224584605939537911
M = 81292139
P23 = primorial(9)                     # 2*3*5*7*11*13*17*19*23
D = M * P23

assert P23 == 223092870 == 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23
assert D == 18135696597948930
terms = [A + D * n for n in range(27)]
assert max(terms) < 2 ** 64
assert all(isprime(t) for t in terms)                         # A1
assert not isprime(A + 27 * D) and not isprime(A - D)
assert all(D % q == 0 for q in primerange(2, 28))             # A4
assert isprime(M) and D % 3 == 0 and D % 9 != 0               # A5
assert D % 9 == 3 and 1 + (D - 1) % 9 == 3                    # A6

if __name__ == "__main__":
    print(f"d = {M} x 23# = {D}; digital root {1 + (D - 1) % 9}; 3 divides d once")
    print(f"27 terms prime, {terms[0]} .. {terms[-1]}; n=27 and n=-1 composite")

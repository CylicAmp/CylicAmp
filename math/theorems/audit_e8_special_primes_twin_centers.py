# CLASS: AUDIT
"""
Audit of supplied Datasets 39-45 ("special primes as predictor of E8 zeroes").

SPECIAL PRIME = p with p^3 = -1 (mod 37), i.e. p mod 37 in {11, 27, 36}.
E8 ZERO (inferred, then REPRODUCED EXACTLY) = 37 | sigma_3(c), c the twin-prime
centre (E8 theta coefficients are 240 sigma_3). Twin centres: first 2000, (5,7) on.

VERDICT: FORCED BY DEFINITION, not predictive.
  sigma_3(p^e) = sum_{i<=e} (p^3)^i = sum (-1)^i (mod 37) = 0 if e odd, 1 if e even.
  So a special prime to an ODD power makes c a zero automatically.
  * Confusion matrix with special primes < 1000: TP 287, FP 21, TN 1586, FN 106 --
    identical to the supplied Dataset 39.
  * All 21 FP are special primes SQUARED (11^2, 73^2): sigma_3 = 1 - 1 + 1 = 1.
  * FN: special primes >= 1000 missing from the list (to 1e5: TP 334, FN 59), plus
    other routes to 37 | sigma_3 (e.g. p^3 of order 3 at exponent 2).
  * Datasets 40-41 match the twin-centre sieve baseline 1/(q - 2): q = 11: 231 vs
    222.2; 73: 28 vs 28.2; 101: 21 vs 20.2; 307: 8 vs 6.6. 11's 91% zero rate is
    the 11^2 share (about 1/11).
  * Dataset 42: 94 special primes < 1e4 vs Dirichlet 1229 * 3/36 = 102.4, split
    32/32/30 across the three classes -- uniform, as Dirichlet predicts.
  * Dataset 43 label "first 20 each" lists all such primes below 1000.
  * Arithmetic checks: 73^3 + 1 = 37 * 10514, 101^3 + 1 = 37 * 27846 (correct).
"""
from sympy import factorint, isprime, primerange


def sig3(n):
    r = 1
    for p, e in factorint(n).items():
        r *= (p ** (3 * (e + 1)) - 1) // (p**3 - 1)
    return r


centers, p = [], 5
while len(centers) < 2000:
    if isprime(p) and isprime(p + 2):
        centers.append(p + 1)
    p += 2
F = [factorint(c) for c in centers]
Z = [sig3(c) % 37 == 0 for c in centers]
SP = lambda f, B: any(q % 37 in (11, 27, 36) and q < B for q in f)

cm = lambda B: (sum(SP(f, B) and z for f, z in zip(F, Z)), sum(SP(f, B) and not z for f, z in zip(F, Z)),
                sum(not SP(f, B) and not z for f, z in zip(F, Z)), sum(not SP(f, B) and z for f, z in zip(F, Z)))
assert cm(1000) == (287, 21, 1586, 106)                        # the supplied matrix, exactly
assert cm(100000) == (334, 21, 1586, 59)
for f, z in zip(F, Z):                                          # every FP is a squared special prime
    if SP(f, 10**9) and not z:
        assert all(e % 2 == 0 for q, e in f.items() if q % 37 in (11, 27, 36))
for q in (11, 27, 36):
    for pp in primerange(q, 3000):
        if pp % 37 == q:
            assert all((sum(pow(pp, 3 * i, 37) for i in range(e + 1)) % 37 == 0) == (e % 2 == 1) for e in range(1, 7))
assert [sum(c % q == 0 for c in centers) for q in (11, 73, 101, 307)] == [231, 28, 21, 8]
sp = [q for q in primerange(2, 10000) if q % 37 in (11, 27, 36)]
assert len(sp) == 94
assert 73**3 + 1 == 37 * 10514 and 101**3 + 1 == 37 * 27846

if __name__ == "__main__":
    print("E8-zero audit: supplied matrix reproduced exactly from 37 | sigma_3(c); forced by p^3 = -1.")

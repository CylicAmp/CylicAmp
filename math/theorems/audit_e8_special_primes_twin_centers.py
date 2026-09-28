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

COMPLETE CRITERION (supersedes the supplied "(A) odd special exponent, (B) p = 7,
e = 2 mod 3", which covers 69.3% and misses e.g. 243 = 3^5). sigma_3 is
multiplicative, so 37 | sigma_3(n) iff some p^e || n has 37 | sigma_3(p^e). For
p != 37 let d = ord_37(p^3) (d | 12, the cubes form the order-12 subgroup):
    d > 1:  37 | sigma_3(p^e)  iff  d | e + 1
    d = 1 (p = 1, 10, 26 mod 37):  iff  37 | e + 1
    p = 37: sigma_3 = 1, never.
(A) is d = 2; (B) is d = 3 for p = 7 -- but EVERY prime with p^3 in {10, 26}
(7, 53, 71, 83, 107, 127, ...) behaves like 7. 3^5 is d = 6 (ord(3) = 18,
ord(27) = 6, 6 | 5 + 1). Verified for every n <= 1e5: zeros certified by
d = 2: 15428, d = 3: 1838, d = 4: 16, d = 6: 274, d = 12: 24.
Dataset 50 "twin elevation" 20.0% vs 18.6% on n = 2000 each: z = 1.12, not
significant.
The d = 3 primes are exactly p = 7, 9, 12, 16, 33, 34 (mod 37) -- the elements of
order 9 (p^3 in {10, 26}); a supplied decomposition listed only 9, 16, 34.
SUPPLIED 1e6 SCAN, REPRODUCED independently (sieve, 2026-09-27): zeros <= 1e6:
188 742 (18.874%); twin centres c = p+1 <= 1e6: 8168, of which 1652 zeros
(20.225%); elevation 1.072. Criterion vs direct sigma_3: no mismatch.

WHY TWIN CENTRES ARE ELEVATED -- the local sieve, quantitatively (proved model).
A twin centre has c = 0 mod 6 and c != +-1 mod p, so P(p | c) = 1/(p-2) instead of
1/p; given p | c, higher powers are as for random integers. Hence
    P(annihilated by p) = P(p | c) * sum_{e in class} (1 - 1/p) p^-(e-1).
  p = 11, e odd:        twin 11/108 = 10.185%, mult-6 11/132 = 8.333%, delta 1.852 pp
                        (supplied smallest-annihilator table: 1.819)
  p = 7,  e = 2 mod 3:  twin 2.456%, mult-6 1.754%, delta 0.702 pp (supplied 0.697)
FAIR CONTROL (N = 4e6): twin centres 21.25% zeros; multiples of 6 with c +- 1 free
of all primes 5..47: 21.13%; plain multiples of 6: 19.15%. The elevation vanishes
under the fair control: it is entirely the local sieve at small primes.
SUPPLIED-CODE NOTE: np.arange(N+1, dtype=int64)**3 overflows int64 for n > 2.1e6
(N^3 = 8e21 > 9.2e18), which produced the spurious 4.35% density; reducing mod 37
before multiplying gives the correct 20.24% at N = 2e7.
A supplied 2e7 re-run (2026-09-28) confirms: range-matched by decade, twin excess
z ~ +10, entirely in the p = 11 (odd e) and p = 7 (e = 2 mod 3) classes; fair
control 21.82% vs twin 21.84%. Its model predictions (+1.63, +0.54 pp) omitted
higher powers; the exact values are 1.852 and 0.702 pp (above).
STATUS: TWIN-CENTRE THREAD RETIRED -- mechanism is residue conditioning
(P(p | c) = 1/(p-2)); no residual link between 37 | sigma_3 and twin primality.

ASYMPTOTIC DENSITY OF THE ZERO SET (Selberg-Delange, standard). n is a NON-zero
only if every d = 2 prime (p^3 = -1 mod 37, i.e. p in 3 of the 36 unit classes,
relative density 1/12) divides n to an EVEN power; the d = 3,4,6,12 classes need
exponent >= 2 and change only the constant. Hence
    #{n <= x : 37 does not divide sigma_3(n)} ~ C x (log x)^(-1/12),
so the zero density tends to 1, as slowly as 1 - C (log x)^(-1/12). This IS the
observed drift 18.87% (1e6) -> 20.24% (2e7): fitted C = 1.0097 at 1e6 and
1.0091 at 2e7 (stable to 0.06%); predicted non-zero ratio 0.98378 vs observed
0.98315. No earlier twin-vs-baseline comparison is valid unless range-matched.

THE CONSTANT, TO SECOND ORDER (supplied 2026-09-28, both routes reproduced here).
Selberg-Delange with f(p^e) = [37 does not divide sigma_3(p^e)], z = 11/12:
    C = Gamma(11/12)^-1 prod_p (1-1/p)^(11/12) sum_e f(p^e) p^-e,
Gamma(11/12) = 1.055547; the p = 37 factor is (1-1/37)^(-1/12). Euler product
truncated at B: 1.003861 (1e3), 1.006594 (1e4), 1.006105 (1e5), 1.006216 (1e6),
1.006253 (3e6). Independently, a linear fit of the sieve's C_fit(x) =
A(x)(log x)^(1/12)/x at x = 1e5, 1e6, 3e6, 1e7, 2e7 against 1/log x gives
C = 1.006266, c1 = 0.04679. The two agree to 1.3e-5. So
    #{n <= x : 37 does not divide sigma_3(n)}
        = 1.00627 x (log x)^(-1/12) (1 + 0.0468/log x + ...),
and the finite-x fits near 1.009 are this expansion at finite x.
(Counting note: cumsum(~is_zero) with is_zero[0] = False counts index 0 as a
non-zero; the 1/x error changes only the fifth decimal of C_fit.)

EXTENSION TO 3e8 (supplied 2026-09-28). Non-zero density 0.787396693 at 3e8,
C_fit(3e8) = 1.008631, decreasing toward C; the Euler product oscillates at
1.00627 (C_{3e8} = 1.006270719; numerical stabilisation, not a rigorous bound).
Overlap check: the supplied 2e7 value 0.797592200 equals this file's 0.7975922.
a(37n) = a(n) is EXACT (sigma_3(37^e) = 1 mod 37); 8,108,108 pairs checked. The
supplied citation (Bordelles, Aug 2026, v_q(sigma_k(n))) is not verified here and
is not needed: the local rule follows from sigma_3(p^e) = (r^(e+1)-1)/(r-1),
r = p^3.
25% zeros needs log10 x = 14.78 (x ~ 6e14) at leading order: confirmed.

RESIDUE-CLASS DENSITIES AND WHY THEY FACTOR THROUGH F_37*/H_3 (proved here).
Local obstruction depends on p^3 only, and (ph)^3 = p^3 for h in H_3 = {1,10,26}:
EXACT. The densities of n in each residue class come from the twists
sum a(n) chi(n); Selberg-Delange gives each size x (log x)^(z_chi - 1) with
    z_chi = (1/36) sum_r a_r chi(r),   a_r = 0 iff r^3 = -1, i.e. r in -H_3.
  chi trivial on H_3: z_chi = -chi(-1)/12  -> x (log x)^(-11/12) (odd chi) or
                      x (log x)^(-13/12) (even chi);
  chi nontrivial on H_3: z_chi = 0         -> x / log x.
So WITHIN an H_3-coset densities differ at order 1/log x, BETWEEN cosets at order
(log x)^(-11/12): this is why the supplied within-coset spread is 3.8e-5. All
classes share the same limit; the near-constancy on cosets is an asymptotic
hierarchy, not an exact identity.
FOURIER TEST on C_12 = <2 H_3> (the supplied 12 densities, rows = 2^j H_3):
-1 = 2^18 -> 2^6 H_3, so psi_k is odd iff k is odd; odd twists should dominate.
|rho^(k)|, k = 1..6: 0.01188 (odd), 0.00402, 0.00406 (odd), 0.00219, 0.00296
(odd), 0.00299. The largest harmonic is odd; beyond it the odd/even separation
is only the factor (log x)^(1/6) = 1.64 at 3e8, so L-value constants still
dominate. PREDICTION: the odd/even amplitude ratio grows like (log x)^(1/6).

SIEVE-SCRIPT AUDIT (2026-09-28). A supplied vectorised sieve multiplied sig by
(1 + r + ... + r^k) at EVERY division step k, i.e. by the product of partial
sums instead of the single sigma_3(p^e) = 1 + r + ... + r^e (r = p^3 mod 37); it
is wrong whenever e >= 2 and gave 199857 zeros <= 1e6 instead of 188742. Also:
checkpoint subtraction nz[c-lo:] drops n = c (use nz[c-lo+1:]); the residue
snapshot counted the whole segment. Corrected tool: tools/sigma3_mod37_sieve.py.
Its 1e8 run (30 s): nonzero 82420 (1e5), 811258 (1e6), 2417653 (3e6), 8005039
(1e7), 15951844 (2e7), 23878649 (3e7), 79132815 (1e8); C_fit 1.010333,
1.009694, 1.009421, 1.009190, 1.009054, 1.008984, 1.008785 -- matching the
supplied 3e8-run values at 2e7 and 1e8.
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

def _ord37(y):
    k, x = 1, y % 37
    while x != 1:
        x = x * y % 37
        k += 1
    return k


def _crit(n):
    for q, e in factorint(n).items():
        if q == 37:
            continue
        d = _ord37(pow(q, 3, 37))
        if (d > 1 and (e + 1) % d == 0) or (d == 1 and (e + 1) % 37 == 0):
            return True
    return False


assert all((sig3(n) % 37 == 0) == _crit(n) for n in range(1, 20001))
assert [x for x in range(1, 37) if pow(x, 3, 37) in (10, 26)] == [7, 9, 12, 16, 33, 34]
from fractions import Fraction as _Fr
_P = lambda p, base, ecls: sum(_Fr(1, base) * _Fr(p - 1, p) * _Fr(1, p) ** (e - 1) for e in ecls)
_e11 = [e for e in range(1, 80) if e % 2]
assert abs(float(_P(11, 9, _e11)) - 11 / 108) < 1e-12 and abs(float(_P(11, 11, _e11)) - 11 / 132) < 1e-12
assert round(float(_P(7, 5, [e for e in range(1, 80) if e % 3 == 2]) - _P(7, 7, [e for e in range(1, 80) if e % 3 == 2])) * 100, 3) == 0.702
assert (2 * 10**6) ** 3 < 2**63 < (21 * 10**5) ** 3
from math import log as _log
_C1, _C2 = (1 - 188742 / 10**6) / _log(1e6) ** (-1 / 12), (1 - 0.2024078) / _log(2e7) ** (-1 / 12)
assert abs(_C1 - _C2) < 1e-3 and 1.0 < _C2 < 1.02
assert sum(1 for r in range(1, 37) if pow(r, 3, 37) == 36) == 3                    # 3 of 36 classes: 1/12
from math import lgamma as _lg, exp as _ex
assert abs(_ex(_lg(11 / 12)) - 1.055547) < 1e-6
assert abs((1 - 1 / 37) ** (-1 / 12) - 1.002286) < 1e-6
assert sorted(r for r in range(1, 37) if pow(r, 3, 37) == 36) == [11, 27, 36] == sorted(36 * h % 37 for h in (1, 10, 26))
assert pow(2, 18, 37) == 36
assert sig3(243) % 37 == 0 and _ord37(27) == 6 and _ord37(pow(7, 3, 37)) == 3

if __name__ == "__main__":
    print("E8-zero audit: supplied matrix reproduced exactly from 37 | sigma_3(c); forced by p^3 = -1.")

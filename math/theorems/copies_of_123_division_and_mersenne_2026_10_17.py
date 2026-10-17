# CLASS: AUDIT
"""
123123123123123123123123123123, 123 / 10 and Mersenne primes (owner_work #309, 2026-10-17).

THE OWNER'S LINES, verbatim:
    123123123123123123123123123123


    123÷10

    Mersenne primes
No operation is given with them; each is run through the frameworks and the repository is searched for earlier work.

1. 123 written ten times (30 digits).
   = 123 x (10^30 - 1) / 999 = 3 x 7 x 11 x 13 x 31 x 41^2 x 211 x 241 x 271 x 2161 x 9091 x 2906161.
   Digit sum 60, root 6 (ten blocks of 6). Mod 37: 1000 = 1, so k copies of 123 are k x 123 = 12k (mod 37): the owner's
   ABCABC = 2 x ABC (cylicamp pipeline step 9, math/lemmas/abcabc_mod37_orbit.py) is the k = 2 case. Ten copies = 9
   -> SA_ST_A. Mod 999 it is 231 (1230 - 999).
2. 123 / 10 = 12.3 (digits 1, 2, 3, root 6, as 123). Mod 37, 10^-1 = 26, so dividing by 10 IS the 137-map f(n) = 26n:
   123 = 12, 123/10 = 16, 123/100 = 9, 123/1000 = 12 again -- the cycle 12 -> 16 -> 9 -> 12 of SA_ST_A. Ten copies of 123
   = 123 x 10 = 123/100: the same residue, 9. All three (12, 16, 9) lie in SA_ST_A = {9, 12, 16}. FORCED: 10 = 26^2 and
   26 are in the subgroup {1, 10, 26}; this is T302 (26 = 100 mod 37, the decimal shift), not a new finding.
3. Mersenne primes. Lucas-Lehmer on every prime below 4500 (this run) gives the 20 exponents
   2 3 5 7 13 17 19 31 61 89 107 127 521 607 1279 2203 2281 3217 4253 4423.
   Digital root of the exponent: 2 3 5 7 4 8 1 4 7 8 8 1 8 4 1 7 4 4 5 4.
   Digital root of M_p = 2^p - 1: only 1 or 4 for p >= 5 (1 when p = 1 mod 6, 4 when p = 5 mod 6); 3 for p = 2, 7 for p = 3.
   9 never occurs: 3 | 2^p - 1 only for even p. Last digit 1 (p = 1 mod 4) or 7 (p = 3 mod 4). Forced, by p mod 6 and mod 4.
   Even perfect numbers 2^(p-1) x M_p: root 6 for p = 2, root 1 for every other exponent found.
   Mod 37: M_p = 2^(p mod 36) - 1, so 37 never divides a Mersenne prime (36 does not divide a prime). Residues and orbits of the
   20 values: 3 C3, 7 D7, 31 C9, 16 SA_ST_A, 14 C9, 17 NQR17, 34 D7, 21 SA_ST_B, 19 CAS_EXT, 18 SEED (M_89 = 17, M_107 = 18).
   M_17 = 131071 = 17 (mod 37): the only exponent of the 20 for which (2^p - 1) mod 37 = p mod 37 (the MWS dashboard's
   "alignment" test, #272).
   Digital roots of the exponents against 1/6 each (primes above 3 are equally spread over the six units mod 9):
   counts for 1 2 4 5 7 8 are 3 0 6 2 3 4 among 18; chi-square 6.67 on 5 degrees of freedom, p = 0.25. Not significant;
   recorded, not claimed.

THE REPOSITORY ALREADY HAS the owner's Mersenne work: cylicamp/euclid_euler_theorem.md, euler_converse_expanded.md,
lucas_lehmer_proof.md, ll_sequence_sympy.py (Michael Warren Song, added 2026-10-02); math/theorems/mersenne_seam_kervaire_gf37.py
(T84); theorem_258_rule30_mersenne_gf37.py (T258, Rule 30 records at times 2^k - 1). LOSS_DOCUMENTATION.md (2026-08-02) records
the loss of the owner's "Mersenne Exponents -- DR patterns vs 7-4-9 triad" (directory mersenne_exponents_role_7_4_9_2026_04/:
README, statement.tex, analysis.tex, verification.py). That work is not in the repository and what the 7-4-9 triad was is not
recorded here. NOT SETTLED. The computations above are new runs, not a rebuild of it.

FALSIFICATION: any assertion failing.
"""
import math
from sympy import factorint, isprime, primerange

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# 1. ten copies of 123
n = int("123" * 10)
assert str(n) == "123123123123123123123123123123" and len(str(n)) == 30
assert n == 123 * (10 ** 30 - 1) // 999
assert factorint(n) == {3: 1, 7: 1, 11: 1, 13: 1, 31: 1, 41: 2, 211: 1, 241: 1, 271: 1, 2161: 1, 9091: 1, 2906161: 1}
assert sum(map(int, str(n))) == 60 and dr(n) == 6 and n % 999 == 231 and n % 37 == 9
assert all(int("123" * k) % 37 == 12 * k % 37 for k in range(1, 60)) and int("123123") % 37 == 2 * 123 % 37
# 2. 123 / 10
assert pow(10, -1, 37) == 26 and 26 * 26 % 37 == 10 and 10 * 26 % 37 == 1 and 123 % 37 == 12
chain = [123 % 37]
for _ in range(3):
    chain.append(26 * chain[-1] % 37)
assert chain == [12, 16, 9, 12] and n % 37 == 123 * 10 % 37 == chain[2] and 123 % 37 in (9, 12, 16)
assert dr(123) == 6 and sum(map(int, "123")) == 6 == sum(map(int, "12.3".replace(".", "")))
# 3. Mersenne primes, Lucas-Lehmer


def lucas_lehmer(p):
    if p == 2:
        return True
    M = (1 << p) - 1
    s = 4
    for _ in range(p - 2):
        s = s * s - 2
        s = (s & M) + (s >> p)
        if s >= M:
            s -= M
    return s == 0


EXP = [p for p in primerange(2, 4500) if lucas_lehmer(p)]
assert EXP == [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423]
assert [dr(p) for p in EXP] == [2, 3, 5, 7, 4, 8, 1, 4, 7, 8, 8, 1, 8, 4, 1, 7, 4, 4, 5, 4]
assert [dr((1 << p) - 1) for p in EXP] == [3, 7, 4, 1, 1, 4, 1, 1, 1, 4, 4, 1, 4, 1, 1, 1, 1, 1, 4, 1]
assert all(dr((1 << p) - 1) == (1 if p % 6 == 1 else 4) for p in EXP[2:])
assert all(((1 << p) - 1) % 10 == (1 if p % 4 == 1 else 7) for p in EXP[1:])
perfect = [(1 << (p - 1)) * ((1 << p) - 1) for p in EXP]
assert dr(perfect[0]) == 6 and all(dr(x) == 1 for x in perfect[1:])
assert [((1 << p) - 1) % 37 for p in EXP] == [3, 7, 31, 16, 14, 17, 34, 21, 19, 17, 18, 34, 17, 21, 34, 16, 14, 14, 31, 21]
assert all(((1 << p) - 1) % 37 == (pow(2, p % 36, 37) - 1) % 37 != 0 for p in EXP)
assert [p for p in EXP if (pow(2, p, 37) - 1) % 37 == p % 37] == [17] and (1 << 17) - 1 == 131071 and 131071 % 37 == 17
assert isprime(131071)
counts = [sum(1 for p in EXP[2:] if dr(p) == r) for r in (1, 2, 4, 5, 7, 8)]
assert counts == [3, 0, 6, 2, 3, 4] and sum(counts) == 18
chi2 = sum((c - 3) ** 2 / 3 for c in counts)
assert abs(chi2 - 20 / 3) < 1e-12


def chi_square_tail_5(x):
    return math.erfc(math.sqrt(x / 2)) + math.sqrt(2 * x / math.pi) * math.exp(-x / 2) * (1 + x / 3)


assert abs(chi_square_tail_5(11.0705) - 0.05) < 1e-4 and 0.24 < chi_square_tail_5(chi2) < 0.25

if __name__ == "__main__":
    print("ten copies of 123 = 9 mod 37; 123/10 = 16 (the 137-map is division by 10); 20 Mersenne exponents below 4500 by Lucas-Lehmer;")
    print("dr(M_p) is 1 or 4; M_17 = 17 mod 37; the digital roots of the exponents are not significantly uneven (p = 0.25)")

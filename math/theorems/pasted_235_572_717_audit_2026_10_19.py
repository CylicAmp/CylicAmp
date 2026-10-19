# CLASS: AUDIT
"""
The pasted table and invariants for {235, 572, 717} (owner_work #355, 2026-10-19). Third-party text (LaTeX, another
tool's style); nothing below is put in the owner's mouth. Several displayed equations are blank in the paste
(rendering dropped them); those were recomputed from the sentence around each blank.

RIGHT (every cell and sentence re-run):
  235 = 5x47 ; 235 = 6x37+13 ; 235 = 21x11+4 ; 2+3+5=10=1 ; 235 = 25 mod 30, gcd 5
  572 = 2x2x11x13 ; 572 = 15x37+17 ; 572 = 52x11+0 ; 5+7+2=14=5 ; 572 = 2 mod 30, gcd 2
  717 = 3x239 ; 717 = 19x37+14 ; 717 = 65x11+2 ; 7+1+7=15=6 ; 717 = 27 mod 30, gcd 3
  235 = 13+37x6 ; 235+717 = 952 = 25x37+27, and 13+14 = 27 < 37 ; 27x27 = 26, 27x27x27 = 36 = -1 mod 37, so 27 has order 6
  337 = 572-235, prime, 337 = 9x37+4, 3+3+7=13=4 ; 145 = 717-572 = 5x29, 145 = 3x37+34 = -3, 1+4+5=10=1
  476 = (235+717)/2 = 2x2x7x17 ; its four smallest divisors 1, 2, 4, 7 ; 1+4+16+49 = 70 (not 476)
  1524 = 235+572+717 = 2x2x3x127, 127 = 2^7-1 prime ; 1524 = 41x37+7, and 13+17+14 = 44 = 7 ; 1+5+2+4=12=3 = 1+5+6=12
WRONG:
  "241 is the 52nd prime": 241 is the 53rd (the 52nd is 239; there are 53 primes up to 246).
  "the Maynard-Tao bound 246": 246 is the Polymath8b bound for bounded prime gaps (it uses the Maynard-Tao method; Maynard's
    own bound was 600). 241 is the largest prime below 246 (242 to 246 are composite).
TYPO  sqrt(337) is 18.36 (18.3576), the paste has 18.35.
I CAN'T CHECK  where the three numbers come from, and which difference the paste's third bullet ("241 ...") is taken from:
  the line is blank. 241 = (717-235)/2 = 482/2, so that is the reading used.

CONNECTIONS (the owner's lines and files):
  13+37k : 235 = 13+37x6, as 679 = 13+37x18 in the earlier review (dashboards/egor_checks/check_egor_checks.py).
  337 = 4 mod 37 is in C3 and 145 = 34 mod 37 is in D7: the birthday pair (C3, D7); 337+145 = 482 = 13x37+1.
  235 = 13, 572 = 17, 717 = 14 mod 37 (CAS_EXT, NQR17, C9); the midpoint 476 = 32 mod 37 is in SEED; 241 = 19 mod 37 is in
    CAS_EXT with 235 ; 1524 = 7 mod 37 (D7).
  246 is the reference seed of the pipeline (CLAUDE.md); 53 primes up to 246 (the Egor Checks page); 241 is the 53rd.
  127 = 7x7x7-6x6x6 is the cuban number C6 (repetend_998001_audit_2026_10_19.py); 1524 = 12 x 127.
  Divisor probe (T245, n = sum of the squares of its k smallest divisors): none of 235, 476, 572, 717, 1524 is a
  solution at k = 4 (only 130 is); the four-divisor sums are 57460, 70, 142, 571220.

FALSIFICATION: any assertion failing.
"""
from sympy import divisors, factorint, gcd, isprime, prime, primepi


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


S = [235, 572, 717]
assert [factorint(n) for n in S] == [{5: 1, 47: 1}, {2: 2, 11: 1, 13: 1}, {3: 1, 239: 1}]
assert [(n // 37, n % 37) for n in S] == [(6, 13), (15, 17), (19, 14)]
assert [(n // 11, n % 11) for n in S] == [(21, 4), (52, 0), (65, 2)]
assert [dr(n) for n in S] == [1, 5, 6] and [sum(map(int, str(n))) for n in S] == [10, 14, 15]
assert [(n % 30, int(gcd(n, 30))) for n in S] == [(25, 5), (2, 2), (27, 3)]
assert 235 == 13 + 37 * 6 and 235 + 717 == 952 == 25 * 37 + 27 and 13 + 14 == 27 < 37
assert pow(27, 2, 37) == 26 and pow(27, 3, 37) == 36 and all(pow(27, k, 37) != 1 for k in (1, 2, 3)) and pow(27, 6, 37) == 1

assert 572 - 235 == 337 and 717 - 572 == 145 and 717 - 235 == 482 and isprime(337) and 337 % 37 == 4 == 9 * 37 + 4 - 333
assert dr(337) == 4 and 3 + 3 + 7 == 13 and abs(337 ** 0.5 - 18.3576) < 1e-4 and round(337 ** 0.5, 2) == 18.36
assert factorint(145) == {5: 1, 29: 1} and 145 == 3 * 37 + 34 and 34 == 37 - 3 and dr(145) == 1

assert (235 + 717) // 2 == 476 == 4 * 7 * 17 and divisors(476)[:4] == [1, 2, 4, 7] and 1 + 4 + 16 + 49 == 70 != 476
assert sum(S) == 1524 == 4 * 3 * 127 and isprime(127) and 127 == 2 ** 7 - 1
assert 1524 % 37 == 7 == (13 + 17 + 14) % 37 and 1524 == 41 * 37 + 7 and dr(1524) == 3 == dr(1 + 5 + 6)

# wrong: the 52nd prime
assert prime(52) == 239 and prime(53) == 241 and primepi(241) == 53 == primepi(246)
assert [n for n in range(242, 247) if isprime(n)] == [] and 482 // 2 == 241

# connections
assert 679 == 13 + 37 * 18 and 235 % 37 == 679 % 37 == 13
assert 337 % 37 in {3, 4, 30} and 145 % 37 in {7, 33, 34} and 337 + 145 == 482 == 13 * 37 + 1
assert 476 % 37 == 32 and 32 in {18, 24, 32} and 241 % 37 == 19 and 19 in {5, 13, 19} and 17 in {17, 22, 35} and 14 in {14, 29, 31}
assert 127 == 7 ** 3 - 6 ** 3 and 1524 == 12 * 127
for n in (235, 476, 572, 717, 1524):
    d = divisors(n)
    assert sum(x * x for x in d[:4]) != n
assert [sum(x * x for x in divisors(n)[:4]) for n in (235, 476, 572, 717)] == [57460, 70, 142, 571220]

if __name__ == "__main__":
    print("235, 572, 717: table and sums right; 241 is the 53rd prime, not the 52nd; 246 is the Polymath8b bound; "
          "337 in C3 and 145 in D7; 476 in SEED; 1524 = 12x127")

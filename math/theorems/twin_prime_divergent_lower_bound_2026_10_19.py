# CLASS: AUDIT
"""
"Derivation of a divergent lower bound for twin prime" (owner_work #360, 2026-10-19). The message is that title only.

ANSWER IN ONE LINE: a proved lower bound for the number of twin primes that grows without limit is the twin prime conjecture
itself. It is open. I can't derive one, and no one has. What can be derived, and what is proved, is below, with every number
computed here.

1. THE DERIVATION THAT EXISTS (Hardy-Littlewood, a heuristic, not a proof). A number n near x is prime with probability 1/ln x.
   For a prime p, the residues of n mod p that keep both n and n+2 away from a multiple of p: p = 2 allows 1 of 2 (n odd),
   an odd p allows p-2 of p. Dividing by the independent model (1 - 1/p)^2 for each prime:
       p = 2: (1/2)/(1/2)^2 = 2          odd p: (1 - 2/p)/(1 - 1/p)^2 = 1 - 1/(p-1)^2
   so the density of n with n and n+2 both prime is  2 C2 / ln^2 n,  C2 = product over odd primes of (1 - 1/(p-1)^2) = 0.6601618158...
       pi_2(x) ~ 2 C2 * integral from 2 to x of dt / ln^2 t  ~ 2 C2 x / ln^2 x,   which grows without limit (diverges).
   Checked against the count of pairs (p, p+2) with p <= x:
       x       10^3   10^4   10^5    10^6    10^7     10^8
       count   35     205    1224    8169    58980    440312
       count / prediction   0.764  0.957  0.980  0.990  1.004  0.9999
   The prediction is a conjecture. It matches the data to 0.01 percent at 10^8; it proves nothing about x beyond.

2. WHAT IS PROVED, in the other directions:
   - Upper bound (Brun 1919): pi_2(x) <= C x / ln^2 x, and the sum of 1/p + 1/(p+2) over twin pairs CONVERGES, to Brun's constant
     1.9021605831...; the partial sum to 10^8 is 1.7588. So no divergent lower bound can exist for that sum; the bound has to be
     on the count pi_2(x).
   - Divergent lower bound, proved but for a larger set (Chen 1973, cited, not reproved here): the number of primes p <= x with
     p + 2 prime OR a product of two primes is >> x / ln^2 x. Counted: p <= 10^7 gives 225630 such p, of which 58980 have p+2 prime
     (3.83 times as many); 225630 = 5.86 x/ln^2 x (the ratio is 5.37, 5.61, 5.72, 5.86 at 10^4 .. 10^7).
   - Bounded gaps (Zhang 2013, Maynard and Tao 2013, Polymath8b 2014): infinitely many pairs of primes p, q with q - p <= 246
     (not 2). Under the Elliott-Halberstam family of conjectures the bound drops to 12 and 6; 2 is not reached.
   - Why sieves stop short of 2 (Selberg's parity problem): a sieve cannot tell a number with an even number of prime factors from one with
     an odd number, so it cannot separate "p + 2 is prime" from "p + 2 is a product of two primes". Chen's theorem is exactly that wall.

3. THE OWNER'S FAMILY (18x-1, 18x+1): twin primes have middle 6k; middles divide evenly over 0, 6, 12 mod 18, each 1/3
   (0.3326, 0.3342, 0.3332 up to 10^8), so the family is a third of the twin primes and its count diverges exactly when the
   conjecture holds; 61 pairs for x <= 500 (dashboards/egor_checks/check_egor_checks.py).

FALSIFICATION: any assertion failing.
"""
import math

import numpy as np
from mpmath import li, log, mp, mpf
from sympy import primerange

mp.dps = 30
N = 10 ** 8
s = np.ones(N + 3, dtype=bool)
s[:2] = False
for i in range(2, int(N ** 0.5) + 2):
    if s[i]:
        s[i * i::i] = False
tw = np.nonzero(s[:-2] & s[2:])[0]                          # p with p and p+2 prime

C2 = mpf(1)
for p in primerange(3, 10 ** 6):
    C2 *= 1 - mpf(1) / (p - 1) ** 2
assert abs(C2 - mpf("0.6601618158")) < 1e-6 and abs(2 * C2 - mpf("1.3203236316")) < 1e-5

# the density factors
assert all(abs((1 - 2 / p) / (1 - 1 / p) ** 2 - (1 - 1 / (p - 1) ** 2)) < 1e-12 for p in (3, 5, 7, 11, 13, 101))
assert (1 / 2) / (1 / 2) ** 2 == 2


def predicted(x):
    x = mpf(x)
    return 2 * C2 * (li(x) - li(2) - x / log(x) + 2 / log(2))


counts = {k: int(np.searchsorted(tw, 10 ** k, side="right")) for k in range(3, 9)}
assert counts == {3: 35, 4: 205, 5: 1224, 6: 8169, 7: 58980, 8: 440312}
ratio = {k: float(counts[k] / predicted(10 ** k)) for k in counts}
assert [round(ratio[k], 3) for k in range(3, 9)] == [0.764, 0.957, 0.980, 0.990, 1.004, 1.000]
assert abs(ratio[8] - 1) < 1e-3 and abs(counts[8] - float(predicted(10 ** 8))) < 100
growth = [float(predicted(10 ** (k + 1)) / predicted(10 ** k)) for k in range(3, 8)]
assert all(4 < g < 10 for g in growth) and growth == sorted(growth)        # each step of x by 10 multiplies it by less than 10, nearing 10: x / ln^2 x

# Brun: the reciprocal sum converges; partial sum to 10^8
brun = float(np.sum(1 / tw[1:] + 1 / (tw[1:] + 2.0)) + 1 / 3 + 1 / 5)
assert abs(brun - 1.7588) < 1e-3 and brun < 1.9021605831

# the owner's family: a third of the twin primes
mid = tw + 1
assert [round(float(np.mean(mid % 18 == r)), 4) for r in (0, 6, 12)] == [0.3326, 0.3342, 0.3332]
assert sum(1 for x in range(1, 501) if s[18 * x - 1] and s[18 * x + 1]) == 61

# Chen's set, counted to 10^7
M = 10 ** 7 + 2
Om = np.zeros(M + 1, dtype=np.int8)
for p in np.nonzero(s[:M + 1])[0]:
    q = int(p)
    while q <= M:
        Om[q::q] += 1
        q *= int(p)
chen = {}
for k in range(4, 8):
    ps = np.nonzero(s[:10 ** k + 1])[0]
    chen[k] = (int(np.sum(Om[ps + 2] <= 2)), int(np.sum(s[ps + 2])))
assert chen == {4: (633, 205), 5: (4234, 1224), 6: (29949, 8169), 7: (225630, 58980)}
assert [round(chen[k][0] / (10 ** k / math.log(10 ** k) ** 2), 2) for k in range(4, 8)] == [5.37, 5.61, 5.72, 5.86]
assert round(chen[7][0] / chen[7][1], 2) == 3.83

if __name__ == "__main__":
    print("twin primes: no proved divergent lower bound exists (it is the twin prime conjecture); Hardy-Littlewood 2*C2*x/ln^2 x "
          "matches the count to 10^8 (440312); Chen's divergent bound is for p+2 prime or semiprime (225630 up to 10^7)")

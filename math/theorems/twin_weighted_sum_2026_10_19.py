# CLASS: AUDIT
"""
The weighted twin sum, the third target named in the pasted clarification (owner_work #361, 2026-10-19).

THE PASTE (another tool's text, relayed without comment): "One clarification: If by 'divergent lower bound' you mean a lower bound
for a different quantity -- such as Chen primes, bounded-gap pairs, or a weighted sum -- specify that quantity. Those are distinct
mathematical targets, and some already have proved results."
RIGHT: the three are different targets and some have proved results (Chen primes: a divergent lower bound, proved; bounded-gap pairs:
infinitely many pairs of primes with gap <= 246, proved). Nothing is asked here: the reply to #360 already covers Chen primes and
bounded gaps; this file adds the weighted sum so all three named targets are in the repository.

THE WEIGHTED SUM: psi_2(x) = sum over n <= x of Lambda(n) Lambda(n+2), Lambda(n) = ln p if n is a power of the prime p, else 0.
  Hardy-Littlewood conjecture: psi_2(x) ~ 2 C2 x   (C2 = 0.6601618..., 2 C2 = 1.3203236...). It is the twin count with each
  prime weighted by its logarithm, which removes the ln^2 x and turns "diverges" into "grows like x".
  A proved lower bound  psi_2(x) >> x  would give infinitely many twin primes: the terms where n or n+2 is a power p^a with a >= 2
  number at most about 2 sqrt(x) / ln x and each weighs at most ln^2 x, so they add O(sqrt(x) ln x) = o(x), and what is left is
  the sum over twin primes. So a divergent lower bound for psi_2 IS the twin prime conjecture. Proved: only upper bounds,
  psi_2(x) << x by Selberg's sieve (cited, not reproved here). I CAN'T CHECK the exact upper constant: 8 C2 (four times the
  conjecture) is what I remember; a web search (2026-10-19) found the constant 8 in Halberstam-Richert's Theorem 3.13 for the
  sieve, and the twin-prime papers it listed (arXiv 2504.15658, section 2) were not opened, so 8 C2 is not confirmed.
  Counted here, psi_2(x) / (2 C2 x) at x = 10^4, 10^5, 10^6, 10^7:  1.0076, 0.9961, 0.9943, 1.0052.
  The weighted sum in the bounded-gap proofs (Goldston-Pintz-Yildirim, Maynard-Tao) is a different sum, S = sum over n of
  (number of primes among n+h_1..n+h_k, minus 1) times a sieve weight w_n; showing S > 0 for k = 50 (admissible tuple of diameter 246)
  is how 246 is reached. That is a proved positivity, not a lower bound that grows for the pair (p, p+2).

FALSIFICATION: any assertion failing.
"""
import numpy as np
from sympy import primerange

N = 10 ** 7 + 2
s = np.ones(N + 1, dtype=bool)
s[:2] = False
for i in range(2, int(N ** 0.5) + 2):
    if s[i]:
        s[i * i::i] = False
lam = np.zeros(N + 1)
for p in np.nonzero(s)[0]:
    q, lp = int(p), float(np.log(p))
    while q <= N:
        lam[q] = lp
        q *= int(p)

C2 = 1.0
for p in primerange(3, 10 ** 6):
    C2 *= 1 - 1 / (p - 1) ** 2
assert abs(C2 - 0.6601618158) < 1e-6
res = {}
for k in (4, 5, 6, 7):
    x = 10 ** k
    res[k] = float(np.sum(lam[2:x + 1] * lam[4:x + 3])) / (2 * C2 * x)
assert [round(res[k], 4) for k in (4, 5, 6, 7)] == [1.0076, 0.9961, 0.9943, 1.0052]

# the terms with a proper prime power are a negligible part of the sum
lam_p = np.where(s, lam, 0.0)
for k in (5, 6, 7):
    x = 10 ** k
    full = float(np.sum(lam[2:x + 1] * lam[4:x + 3]))
    primes_only = float(np.sum(lam_p[2:x + 1] * lam_p[4:x + 3]))
    assert 0 <= full - primes_only < 0.02 * full and (full - primes_only) / full < (0.02 if k == 5 else 0.01 if k == 6 else 0.005)

if __name__ == "__main__":
    print({k: round(v, 4) for k, v in res.items()})

# CLASS: THEOREM
"""
T245, k = 8, case B (4 | n, a = 3): seven of the thirteen open shapes are
impossible.  Added 2026-10-02.  Settles the question left at
theorem_245_n130_divisor_square_sum_gf37.py, "(a) The cand 0 rows ... Whether
that is provable rather than range-limited is worth asking": all four are
provable, and three more fall with them.

Setting: n = d_1^2 + ... + d_8^2, d_1 < ... < d_8 the eight smallest divisors
of n, written as tokens in 2 and odd primes p < q < r.

LEMMA (shape-level mod 8).  Odd^2 = 1, (2*odd)^2 = 4, (4m)^2 = 0 (mod 8), so a
shape FIXES n mod 8.  A shape also fixes whether 8 | n:
  - if 8 is a token, 8 | n;
  - if 4 is the largest power of 2 listed, 8 does not divide n, because
    8 < d_8 in every shape here (d_8 >= 2q >= 14 or d_8 is a prime > 8, or
    a multiple of p >= 5 exceeding 8; in general d_4..d_8 are five distinct
    integers above d_3 = 4, so d_8 >= 9), so 8 | n would put 8 in the list.
The file's earlier remark "Mod 8 does not close it ... both are reachable"
is correct for PARITY shapes, which do not say whether 8 is listed; it does
not hold shape by shape.

  shape                       n mod 8   8 listed   verdict
  1 2 4 p q r 2p 2q              0         no      IMPOSSIBLE  (cand 0 row)
  1 2 4 p q 2p r 2q              0         no      IMPOSSIBLE  (cand 0 row)
  1 2 4 p q 2p 2q r              0         no      IMPOSSIBLE
  1 2 4 8 p q 2p r               4         yes     IMPOSSIBLE
  1 2 4 8 p 2p q r               4         yes     IMPOSSIBLE
  1 2 4 8 p q r 2p               4         yes     IMPOSSIBLE  (cand 0 row)

SIZE LEMMA, shape 1 2 4 p 2p q r 4p (the fourth cand 0 row).  q, r lie in
(2p, 4p) and 4, p, q, r all divide n, so n >= 4pqr > 16 p^3, while
n = 21 + 21 p^2 + q^2 + r^2 < 21 + 53 p^2.  16 p^3 < 53 p^2 + 21 fails for
every p >= 4, and p >= 5 (p > 4 in the ordering).  IMPOSSIBLE.         QED

Remaining open in case B: six shapes,
  1 2 4 p 2p 4p q r     1 2 4 p 2p q 4p r     1 2 4 p 2p q 4p p^2
  1 2 4 p 2p 4p p^2 q   1 2 4 p 2p 4p q p^2   1 2 4 8 16 p q r
mod 8 is consistent for all six; the last one passes mod 16 too
(341 + three odd squares is 0 or 8 mod 16).

FALSIFICATION: any assertion failing.
"""
import random
import re
from sympy import randprime

OPEN13 = """1 2 2^2 p 2p 2^2p q r
1 2 2^2 p 2p q r 2^2p
1 2 2^2 p 2p q 2^2p r
1 2 2^2 p 2p q 2^2p p^2
1 2 2^2 p q r 2p 2q
1 2 2^2 p q 2p r 2q
1 2 2^2 p q 2p 2q r
1 2 2^2 p 2p 2^2p p^2 q
1 2 2^2 p 2p 2^2p q p^2
1 2 2^2 2^3 p q 2p r
1 2 2^2 2^3 p 2p q r
1 2 2^2 2^3 p q r 2p
1 2 2^2 2^3 2^4 p q r""".splitlines()


def value(tok, P):
    if tok == "1":
        return 1
    v = 1
    m = re.match(r"2(?:\^(\d+))?", tok)
    if m:
        v = 2 ** int(m.group(1) or 1)
        tok = tok[m.end():]
    for s, e in re.findall(r"([pqr])(?:\^(\d+))?", tok):
        v *= P[s] ** int(e or 1)
    return v


def n_mod8_symbolic(shape):
    tot = 0
    for t in shape.split():
        m = re.match(r"2(?:\^(\d+))?", t) if t != "1" else None
        k = int(m.group(1) or 1) if m else 0
        tot += {0: 1, 1: 4}.get(k, 0)
    return tot % 8


R = random.Random(1)
for sh in OPEN13:                                   # symbolic value = actual, random odd primes
    for _ in range(200):
        p, q, r = sorted(randprime(5, 10 ** 6) for _ in range(3))
        if len({p, q, r}) < 3:
            continue
        P = {"p": p, "q": q, "r": r}
        assert sum(value(t, P) ** 2 for t in sh.split()) % 8 == n_mod8_symbolic(sh)

verdict = {}
for sh in OPEN13:
    toks = sh.split()
    eight_listed = "2^3" in toks
    m8 = n_mod8_symbolic(sh)
    verdict[sh] = (m8 == 0) != eight_listed      # contradiction
dead = [s for s, v in verdict.items() if v]
assert dead == ["1 2 2^2 p q r 2p 2q", "1 2 2^2 p q 2p r 2q", "1 2 2^2 p q 2p 2q r",
                "1 2 2^2 2^3 p q 2p r", "1 2 2^2 2^3 p 2p q r", "1 2 2^2 2^3 p q r 2p"]

# 8 < d_8 in every shape: d_3 = 4, and d_4..d_8 are five distinct integers > 4
assert all(sh.split()[2] == "2^2" and len(sh.split()) == 8 for sh in OPEN13) and 4 + 5 > 8

# size lemma for 1 2 4 p 2p q r 4p
assert all(16 * p ** 3 >= 53 * p ** 2 + 21 for p in range(4, 10 ** 4))

# 1 2 4 8 16 p q r survives mod 16
assert {(341 + a + b + c) % 16 for a in (1, 9) for b in (1, 9) for c in (1, 9)} == {0, 8}

CAND0 = ["1 2 2^2 2^3 p q r 2p", "1 2 2^2 p q 2p r 2q", "1 2 2^2 p 2p q r 2^2p", "1 2 2^2 p q r 2p 2q"]
assert all(s in dead for s in CAND0 if s != "1 2 2^2 p 2p q r 2^2p")
assert len(dead) + 1 == 7 and 13 - 7 == 6

if __name__ == "__main__":
    for s in OPEN13:
        tag = "mod 8" if s in dead else ("size" if s == "1 2 2^2 p 2p q r 2^2p" else "open")
        print(f"{s:28s} n = {n_mod8_symbolic(s)} mod 8   {tag}")

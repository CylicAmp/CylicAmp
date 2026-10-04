# CLASS: THEOREM
"""
T245, k = 7, n EVEN IS IMPOSSIBLE.  Added 2026-10-02.  No even n equals the
sum of the squares of its 7 smallest divisors.

n even: d_2 = 2, and n = 1 + a (mod 4) with a the number of odd entries among
d_3..d_7 (theorem_245, "k=7: THE 4-DOES-NOT-DIVIDE-n HALF").  So a is odd:
  a in {1, 5}  <=>  n = 2 (mod 4)   PROVED impossible 2026-09-20 (T245)
  a = 3        <=>  4 | n           PROVED here.

Method: the one that closed k = 8 case B (k8_case_b_complete.py).
STEP 1  tools/k8_caseb_shape_enumerator.py with K = 7: order ideals of size 7
        with four odd members (1 and three more; so at most three odd primes)
        containing 4 (4 | n and d_7 >= 7 > 4), orders and in-box ghosts by LP
        in log space, non-strict: a SUPERSET of the possible shapes.
        67 labelled, 22 with primes labelled by size.  Negative control: the
        census of n < 400000 realizes 10 case-B shapes, all inside.
STEP 2  mod 8 removes nothing at k = 7: four odd squares (4) + 2^2 (4) +
        4^2 (0) + a third even square (4 if it is 2 mod 4, else 0) is 0 or 4
        mod 8, consistent with 8 listed or not in every shape.  Recorded.
STEP 3  size LP: lcm(listed) <= n <= 7 d_7^2, p >= 5 (q >= 7, r >= 11) if p
        follows 4, p = 3 (q >= 5, r >= 7) if p precedes 4.  22 -> 5.
STEP 4  the five have p = 3 and LP upper bounds on q, r (asserted < 100);
        exhaustive over primes q < r < 100: none is a solution.      QED

So k = 7 is impossible for every even n.  k = 7, n odd: still OPEN.

FALSIFICATION: any assertion failing.
"""
import itertools
import math
import os
import re
import sys

import numpy as np
from scipy.optimize import linprog
from sympy import divisors, factorint, primerange

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import k8_caseb_shape_enumerator as EN  # noqa: E402

K = 7
L2 = math.log(2)


def canon(s):
    seen = ""
    for c in s:
        if c in "pqr" and c not in seen:
            seen += c
    return seen == "pqr"[:len(seen)]


def parse(t):
    e = [0, 0, 0, 0]
    if t == "1":
        return tuple(e)
    m = re.match(r"2(?:\^(\d+))?", t)
    if m:
        e[0] = int(m.group(1) or 1); t = t[m.end():]
    for s, k in re.findall(r"([pqr])(?:\^(\d+))?", t):
        e[" pqr".index(s)] += int(k or 1)
    return tuple(e)


def size_lp(shape, obj=None):
    S = [parse(t) for t in shape.split()]
    t = 1 + max(i for a in S for i in range(4) if a[i])
    S = [a[:t] for a in S]
    E = [max(a[i] for a in S) for i in range(t)]
    nv = t - 1
    A, b = [], []

    def le(x, y):
        A.append([float(x[i] - y[i]) for i in range(1, t)]); b.append(float(y[0] - x[0]) * L2)
    for i in range(len(S) - 1):
        le(S[i], S[i + 1])
    for g in itertools.product(*[range(e + 1) for e in E]):
        if g not in S:
            le(S[-1], g)
    D2 = tuple(2 * x for x in S[-1])
    A.append([float(E[i] - D2[i]) for i in range(1, t)]); b.append(float(D2[0] - E[0]) * L2 + math.log(K))
    toks = shape.split()
    after4 = toks.index("2^2") < toks.index("p")
    lo = [math.log(x) for x in ((5, 7, 11) if after4 else (3, 5, 7))]
    for i in range(nv):
        e = [0.0] * nv; e[i] = -1; A.append(e); b.append(-lo[i])
    if not after4:
        e = [0.0] * nv; e[0] = 1; A.append(e); b.append(math.log(3))
    for i in range(nv - 1):
        e = [0.0] * nv; e[i] = 1; e[i + 1] = -1; A.append(e); b.append(0.0)
    c = [0.0] * nv
    if obj is not None:
        c[obj] = -1.0
    return linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=[(None, None)] * nv, method="highs")


def lp_max(shape, j):
    r = size_lp(shape, j)
    return math.inf if r.status == 3 else math.exp(r.x[j])


def n_mod8(s):
    return sum({0: 1, 1: 4}.get(parse(t)[0] if t != "1" else 0, 0) for t in s.split()) % 8


EN.K = K
ALL = set()
for t in range(2, 5):
    ALL |= EN.enumerate_shapes(t)
EN.K = 8
assert len(ALL) == 67
C = sorted(s for s in ALL if canon(s))
assert len(C) == 22

realized = set()                                                      # negative control
for n in range(4, 400000, 4):
    d = divisors(n)
    if len(d) < K:
        continue
    d = d[:K]
    if sum(x % 2 for x in d[2:]) != 3:
        continue
    pr = sorted({q for x in d for q in factorint(x) if q > 2})
    sym = dict(zip(pr, "pqr"))
    toks = []
    for x in d:
        f = factorint(x)
        tk = "" if 2 not in f else ("2" if f[2] == 1 else "2^%d" % f[2])
        for q in pr:
            if q in f:
                tk += sym[q] if f[q] == 1 else "%s^%d" % (sym[q], f[q])
        toks.append(tk or "1")
    realized.add(" ".join(toks))
assert len(realized) == 10 and realized <= set(C)

# STEP 2: the three even entries are 2, 4 and one more; n = 0 (mod 8) exactly
# when that one is 8, i.e. exactly when 8 is listed -- so mod 8 never contradicts
for s in C:
    evens = [parse(t)[0] for t in s.split() if parse(t)[0] >= 1]
    assert len(evens) == 3 and "2" in s.split() and "2^2" in s.split()
    third = sorted(evens); third.remove(1); third.remove(2); third = third[0]   # exponent of the third even entry
    assert (n_mod8(s) == 0) == ("2^3" in s.split()) == (third >= 2)

LIVE = sorted(s for s in C if size_lp(s).status == 0)
assert LIVE == ["1 2 p 2^2 2p p^2 q", "1 2 p 2^2 2p q p^2", "1 2 p 2^2 2p q r",
                "1 2 p 2^2 q 2p p^2", "1 2 p 2^2 q 2p r"]
assert all(s.split()[2] == "p" for s in LIVE)                          # all have p = 3


def val(tok, P):
    e = parse(tok)
    return 2 ** e[0] * P[0] ** e[1] * P[1] ** e[2] * P[2] ** e[3]


for s in LIVE:
    nq = len({c for c in s if c in "qr"})
    for j in range(1, 1 + nq):
        assert lp_max(s, j) < 100, (s, j)
    for q in primerange(5, 100):
        for r in ([1] if "r" not in s else primerange(q + 1, 100)):
            v = [val(t, (3, q, r)) for t in s.split()]
            if v != sorted(v) or len(set(v)) != K:
                continue
            n = sum(x * x for x in v)
            assert divisors(n)[:K] != v, (s, q, r, n)

if __name__ == "__main__":
    print("k=7 n even impossible: superset 67 -> 22 -> 22 (mod 8: no kill) -> %d (size) -> 0;" % len(LIVE),
          "census realizes", len(realized), "shapes, all inside")

# CLASS: THEOREM
"""
T245, k = 8, CASE B IS IMPOSSIBLE.  With case A (proved 2026-09-19) this makes
k = 8 IMPOSSIBLE: no n equals the sum of the squares of its 8 smallest
divisors.  Added 2026-10-02.

Case B: 4 | n and exactly 3 odd entries among d_3..d_8.

STEP 1  COMPLETE SHAPE LIST.  tools/k8_caseb_shape_enumerator.py enumerates
        a SUPERSET of the possible shapes: order ideals of size 8 (2 and at
        most three odd primes; four odd members), orders and in-box ghosts
        tested by LP in log space with non-strict inequalities.  304 labeled
        shapes; 122 after fixing labels by size (p < q < r).  The 13 shapes
        the 2026-09-19 tree left open are all in it (asserted).
STEP 2  SHAPE-LEVEL MOD 8 (k8_case_b_shape_mod8.py): 8 | n iff 8 is listed,
        since d_8 > 8 whenever 8 is not listed.  122 -> 38.
STEP 3  SIZE LP: lcm(listed) <= n < 8 d_8^2, p >= 5 if p follows 4, p = 3 if
        p precedes 4.  38 -> 12.
STEP 4  the twelve:
   proved in k8_case_b_last_six.py / k8_case_b_shape_mod8.py (size lemma):
        1 2 4 p 2p 4p p^2 q   1 2 4 p 2p 4p q p^2   1 2 4 p 2p q 4p p^2
        1 2 4 p 2p q r 4p
   STRICTNESS (the LP met them only at a tie q = 2p, odd = even):
        1 2 4 p q 2p r 4p     1 2 4 p q r 2p 4p
        both need q < 2p and, since the in-box ghost 2q is unlisted, 2q > 4p.
   p = 3, by hand:  1 2 3 4 6 12 q r.  2q unlisted so r < 2q; 12qr | n, so
        12 q^2 < n = 210 + q^2 + r^2 < 210 + 5 q^2, q^2 < 30, but q > 12.
   p = 3, FINITE (LP gives q <= 18, r <= 24; checked to 100):
        1 2 3 4 6 9 12 q    1 2 3 4 6 9 q 12    1 2 3 4 6 q 12 r
        1 2 3 4 6 q 9 12    1 2 3 4 6 q r 12
Every shape is empty, so case B has no solution.                        QED

Scope: STEP 1 is the load-bearing step.  Its soundness argument is in the
enumerator's docstring (non-strict real LP admits every ordering actual
primes produce), the same as the k=9 enumerator, which was validated
against a census.  Here it is validated against the earlier 33-shape tree.

FALSIFICATION: any assertion failing.
"""
import math
import os
import re
import sys

import numpy as np
from scipy.optimize import linprog
from sympy import divisors, primerange

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import k8_caseb_shape_enumerator as EN  # noqa: E402

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


def mod8_ok(s):
    T = s.split()
    v = [parse(t)[0] if t != "1" else 0 for t in T]
    m8 = sum({0: 1, 1: 4}.get(x, 0) for x in v) % 8
    a = max(parse(t)[0] for t in T if re.fullmatch(r"1|2(\^\d+)?", t))
    return (m8 == 0) if a >= 3 else (m8 == 4)


def size_ok(shape):
    import itertools
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
    A.append([float(E[i] - D2[i]) for i in range(1, t)]); b.append(float(D2[0] - E[0]) * L2 + math.log(8))
    toks = shape.split()
    after4 = toks.index("2^2") < toks.index("p")
    lo = [math.log(5 if after4 else 3), math.log(7), math.log(11)]
    for i in range(nv):
        e = [0.0] * nv; e[i] = -1; A.append(e); b.append(-lo[i])
    if not after4:
        e = [0.0] * nv; e[0] = 1; A.append(e); b.append(math.log(3))
    for i in range(nv - 1):
        e = [0.0] * nv; e[i] = 1; e[i + 1] = -1; A.append(e); b.append(0.0)
    return linprog([0] * nv, A_ub=np.array(A), b_ub=np.array(b), bounds=[(None, None)] * nv,
                   method="highs").status == 0


ALL = set()
for t in range(2, 5):
    ALL |= EN.enumerate_shapes(t)
assert len(ALL) == 304
C = sorted(s for s in ALL if canon(s))
assert len(C) == 122
OPEN13 = """1 2 2^2 p 2p 2^2p q r|1 2 2^2 p 2p q r 2^2p|1 2 2^2 p 2p q 2^2p r|1 2 2^2 p 2p q 2^2p p^2|
1 2 2^2 p q r 2p 2q|1 2 2^2 p q 2p r 2q|1 2 2^2 p q 2p 2q r|1 2 2^2 p 2p 2^2p p^2 q|1 2 2^2 p 2p 2^2p q p^2|
1 2 2^2 2^3 p q 2p r|1 2 2^2 2^3 p 2p q r|1 2 2^2 2^3 p q r 2p|1 2 2^2 2^3 2^4 p q r""".replace("\n", "").split("|")
assert set(OPEN13) <= set(C)
M8 = [s for s in C if mod8_ok(s)]
assert len(M8) == 38
LIVE = sorted(s for s in M8 if size_ok(s))
PROVED = {"1 2 2^2 p 2p 2^2p p^2 q", "1 2 2^2 p 2p 2^2p q p^2", "1 2 2^2 p 2p q 2^2p p^2",
          "1 2 2^2 p 2p q r 2^2p"}
STRICT = {"1 2 2^2 p q 2p r 2^2p", "1 2 2^2 p q r 2p 2^2p"}
HAND3 = {"1 2 p 2^2 2p 2^2p q r"}
FIN3 = {"1 2 p 2^2 2p p^2 2^2p q", "1 2 p 2^2 2p p^2 q 2^2p", "1 2 p 2^2 2p q 2^2p r",
        "1 2 p 2^2 2p q p^2 2^2p", "1 2 p 2^2 2p q r 2^2p"}
assert set(LIVE) == PROVED | STRICT | HAND3 | FIN3

# strictness: q < 2p and 2q > 4p are incompatible
assert all(not (q < 2 * p and 2 * q > 4 * p) for p in range(1, 500) for q in range(1, 1000))
# hand p = 3
assert 1 + 4 + 9 + 16 + 36 + 144 == 210 and all(12 * q * q >= 210 + 5 * q * q for q in range(13, 10 ** 4))


def val(tok, P):
    e = parse(tok)
    return 2 ** e[0] * P["p"] ** e[1] * P["q"] ** e[2] * P["r"] ** e[3]


for s in FIN3:
    hits = 0
    for q in primerange(5, 100):
        for r in ([1] if "r" not in s else primerange(q + 1, 100)):
            P = {"p": 3, "q": q, "r": r}
            v = [val(t, P) for t in s.split()]
            if v != sorted(v):
                continue
            n = sum(x * x for x in v)
            if divisors(n)[:8] == v:
                hits += 1
    assert hits == 0, s

# negative control: every case-B shape realized by an actual n < 400000 is in C
from sympy import factorint  # noqa: E402
realized = set()
for n in range(4, 400000, 4):
    d = divisors(n)
    if len(d) < 8:
        continue
    d = d[:8]
    if sum(x % 2 for x in d[2:]) != 3:
        continue
    pr = sorted({q for x in d for q in factorint(x) if q > 2})
    sym = dict(zip(pr, "pqr"))
    toks = []
    for x in d:
        f = factorint(x)
        t = "" if 2 not in f else ("2" if f[2] == 1 else "2^%d" % f[2])
        for q in pr:
            if q in f:
                t += sym[q] if f[q] == 1 else "%s^%d" % (sym[q], f[q])
        toks.append(t or "1")
    realized.add(" ".join(toks))
assert realized <= set(C), sorted(realized - set(C))[:5]
NREAL = len(realized)

if __name__ == "__main__":
    print("realized case-B shapes below 400000:", NREAL, "all inside the enumerated superset")
    print("k=8 case B complete: 304 -> 122 -> 38 (mod 8) -> 12 (size) -> 0; all assertions pass")

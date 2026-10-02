"""k=7, n ODD: a PROVABLE SUPERSET of divisor-prefix shapes, with the size
bound applied per order, and per-branch LP bounds on every prime.

Every divisor is odd; the seven smallest are an order ideal of size 7 in N^t
(t distinct odd primes p < q < ...), t <= 6.  Orders and in-box ghosts are
tested in log space over the reals with NON-STRICT inequalities (so the output
is a superset of what actual primes can produce, same argument as
k8_caseb_shape_enumerator.py).  Size: lcm(listed) <= n <= 7 d_7^2.
Branches: p = 3 (q >= 5, r >= 7, ...) and p >= 5 (q >= 7, r >= 11, ...).
"""
import itertools
import math
import re

import numpy as np
from scipy.optimize import linprog

K = 7
SYM = "pqrsuv"


def ideals(t):
    base = [tuple(0 for _ in range(t))] + [tuple(1 if j == i else 0 for j in range(t)) for i in range(t)]
    start = frozenset(base)
    if len(start) > K:
        return []
    frontier = {start}
    for _ in range(K - len(start)):
        nxt = set()
        for S in frontier:
            for a in S:
                for i in range(t):
                    b = list(a); b[i] += 1; b = tuple(b)
                    if b in S:
                        continue
                    if all(tuple(b[:j] + (b[j] - 1,) + b[j + 1:]) in S for j in range(t) if b[j] > 0):
                        nxt.add(S | {b})
        frontier = nxt
    return [S for S in frontier if len(S) == K]


def tok(a):
    if sum(a) == 0:
        return "1"
    return "".join(s if k == 1 else f"{s}^{k}" for s, k in zip(SYM, a) if k)


def parse(t):
    e = [0] * 6
    if t == "1":
        return tuple(e)
    for s, k in re.findall(r"([pqrsuv])(?:\^(\d+))?", t):
        e[SYM.index(s)] += int(k or 1)
    return tuple(e)


def canon(s):
    seen = ""
    for c in s:
        if c in SYM and c not in seen:
            seen += c
    return seen == SYM[:len(seen)]


def _lp(t, A, b, lo, fix3=False, obj=None):
    A = [list(x) for x in A]; b = list(b)
    for i in range(t):
        e = [0.0] * t; e[i] = -1.0; A.append(e); b.append(-math.log(lo[i]))
    if fix3:
        e = [0.0] * t; e[0] = 1.0; A.append(e); b.append(math.log(3))
    for i in range(t - 1):
        e = [0.0] * t; e[i] = 1.0; e[i + 1] = -1.0; A.append(e); b.append(0.0)
    c = [0.0] * t
    if obj is not None:
        c[obj] = -1.0
    return linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=[(None, None)] * t, method="highs")


LO_ANY = (3, 5, 7, 11, 13, 17)


def superset():
    """{shape: t} for every shape (labelled by size) consistent with order + ghosts."""
    res = {}
    for t in range(1, 7):
        for S in ideals(t):
            E = [max(a[i] for a in S) for i in range(t)]
            ghosts = [g for g in itertools.product(*[range(e + 1) for e in E]) if g not in S]
            A = [[float(x[i] - g[i]) for i in range(t)] for g in ghosts for x in S]
            b = [0.0] * len(A)
            if _lp(t, A, b, LO_ANY).status != 0:
                continue

            def rec(order, rem, A, b):
                if not rem:
                    s = " ".join(tok(a) for a in order)
                    if canon(s):
                        res[s] = t
                    return
                for x in sorted(rem):
                    if any(all(z[i] <= x[i] for i in range(t)) and z != x for z in rem):
                        continue
                    A2 = A + [[float(x[i] - z[i]) for i in range(t)] for z in rem if z != x]
                    b2 = b + [0.0] * (len(A2) - len(A))
                    if _lp(t, A2, b2, LO_ANY).status == 0:
                        rec(order + [x], rem - {x}, A2, b2)
            rec([], set(S), A, b)
    return res


def branch_lp(shape, branch, obj=None):
    S = [parse(x) for x in shape.split()]
    t = 1 + max(i for a in S for i in range(6) if a[i])
    S = [a[:t] for a in S]
    E = [max(a[i] for a in S) for i in range(t)]
    A = []
    for i in range(K - 1):
        A.append([float(S[i][j] - S[i + 1][j]) for j in range(t)])
    for g in itertools.product(*[range(e + 1) for e in E]):
        if g not in S:
            A.append([float(S[-1][j] - g[j]) for j in range(t)])
    b = [0.0] * len(A)
    A.append([float(E[j] - 2 * S[-1][j]) for j in range(t)]); b.append(math.log(K))     # size
    lo = (3, 5, 7, 11, 13, 17) if branch == "p=3" else (5, 7, 11, 13, 17, 19)
    return _lp(t, A, b, lo, fix3=(branch == "p=3"), obj=obj), t


def bounds(shape, branch):
    r, t = branch_lp(shape, branch)
    if r.status != 0:
        return None
    out = []
    for j in range(t):
        rj, _ = branch_lp(shape, branch, j)
        out.append(math.inf if rj.status == 3 else math.exp(rj.x[j]))
    return out

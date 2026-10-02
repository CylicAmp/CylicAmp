"""k=8, case B (4 | n, exactly 3 odd entries among d_3..d_8): enumerate a
PROVABLE SUPERSET of divisor-prefix shapes.  Same method as
k9_odd_shape_enumerator.py, with base prime 2.

The eight are 1, 2 and six more; case B makes exactly four of the eight odd
(1 and three others), so at most three odd primes appear.  4 | n and 4 < 8th
divisor (d_4..d_8 are five distinct integers above d_3 <= 4), so 4 is listed.
The exponent set is an order ideal of size 8 in N^t, t = 1 + #odd primes,
containing the unit, every generator and (2,0,..,0).  Ghosts inside the
exponent box must exceed d_8; ghosts outside it are excluded by n's exponent
caps.  Orders are tested in log space over the reals with non-strict
inequalities, odd primes >= 3, 5, 7 in increasing order: the output is a
SUPERSET of the realizable shapes.
"""
import itertools
import math
import sys

import numpy as np
from scipy.optimize import linprog

L2 = math.log(2.0)
PLO = [math.log(x) for x in (3, 5, 7)]
K = 8


def ideals(t):
    base = [tuple(0 for _ in range(t))] + [tuple(1 if j == i else 0 for j in range(t)) for i in range(t)]
    base.append(tuple(2 if j == 0 else 0 for j in range(t)))
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


def lp_feasible(t, cons):
    nv = t - 1
    if nv == 0:
        return all(r >= -1e-9 for v, r in cons)
    A = [list(v) for v, r in cons]; b = [r for v, r in cons]
    for i in range(nv):
        e = [0.0] * nv; e[i] = -1.0; A.append(e); b.append(-PLO[i])
    for i in range(nv - 1):
        e = [0.0] * nv; e[i] = 1.0; e[i + 1] = -1.0; A.append(e); b.append(0.0)
    r = linprog(c=[0.0] * nv, A_ub=np.array(A), b_ub=np.array(b), bounds=[(None, None)] * nv, method="highs")
    return r.status == 0


def le_cons(a, b, t):
    return ([float(a[i] - b[i]) for i in range(1, t)], float(b[0] - a[0]) * L2)


def tok(a, t):
    if sum(a) == 0:
        return "1"
    s = "" if a[0] == 0 else ("2" if a[0] == 1 else "2^%d" % a[0])
    for i, sym in zip(range(1, t), "pqr"):
        if a[i]:
            s += sym if a[i] == 1 else "%s^%d" % (sym, a[i])
    return s


def enumerate_shapes(t):
    res = set()
    for S in ideals(t):
        if sum(1 for a in S if a[0] == 0) != 4:
            continue
        E = [max(a[i] for a in S) for i in range(t)]
        ghosts = [g for g in itertools.product(*[range(E[i] + 1) for i in range(t)]) if g not in S]
        base = [le_cons(x, g, t) for g in ghosts for x in S]
        if not lp_feasible(t, base):
            continue

        def rec(order, rem, cons):
            if not rem:
                res.add(" ".join(tok(a, t) for a in order)); return
            for x in sorted(rem):
                if any(all(z[i] <= x[i] for i in range(t)) and z != x for z in rem):
                    continue
                c2 = cons + [le_cons(x, z, t) for z in rem if z != x]
                if lp_feasible(t, c2):
                    rec(order + [x], rem - {x}, c2)
        rec([], set(S), base)
    return res


if __name__ == "__main__":
    allsh = set()
    for t in range(2, 5):
        sh = enumerate_shapes(t)
        print("t=%d: %d shapes" % (t, len(sh)))
        allsh |= sh
    out = sys.argv[1] if len(sys.argv) > 1 else "k8_caseb_shapes.txt"
    open(out, "w").write("\n".join(sorted(allsh)) + "\n")
    print("total", len(allsh), "->", out)

"""k=9, n odd: enumerate a PROVABLE SUPERSET of divisor-prefix shapes.

Written because the CENSUS APPROACH FAILED on this branch (T245): the shape
list found by scanning n <= 600000 gives 83 shapes, but 95 appear by 800000
and 101 by 1200000, so no census bound certifies the list.  Many-prime
shapes cannot be realized below roughly the product of their primes -- the
shape 1 3 p q r s t 3*p 3*q first occurs at 969969 = 3*7*11*13*17*19 -- so
a bound on n is not a bound on the shape set.

WHAT MAKES THE SET FINITE is the count lemma of T245.  With
c = #{i : 3 | d_i} and t the number of distinct primes among d_1..d_9:

    n = k - c (mod 3) and 3|n  =>  c = k (mod 3)  =>  c in {3,6} at k=9
    the nine are 1, t primes and 8-t composites, and 3 is the only PRIME
    multiple of 3, so c-1 <= 8-t, i.e.  t <= 9 - c  =>  t <= 6.

So at most six distinct primes and at most five free ones.

METHOD.  The nine smallest divisors of such an n are the nine smallest
divisors of 3^E1 * v2^E2 * ... * vt^Et with 3 = v1 < v2 < ... < vt and every
other prime of n above d_9.  Divisor-closure forces every prime appearing to
BE in the list, so the exponent set is an order ideal of size 9 containing
the unit and all t generators.  Monomials not in the ideal ("ghosts") must
exceed d_9, or they would themselves be among the nine.

SOUNDNESS.  An ordering is tested in LOG SPACE, where every comparison
between monomials is linear in (log v2 .. log vt).  Testing over the REALS
with NON-STRICT inequalities admits every ordering that actual primes could
produce, and more: the output is a SUPERSET.  That is the direction that
makes it valid as a search domain -- sweeping a superset and finding it
empty proves the true set empty.  It is NOT a tight enumeration, and the
7180 shapes it returns are far more than the 101 a census to 1.2e6 finds.

VALIDATED: the output contains all 101 census shapes, including all 18 that
the 600000 census missed.
"""

import sys, math, itertools
import numpy as np
from scipy.optimize import linprog

L3 = math.log(3.0)
PLO = [math.log(x) for x in (5, 7, 11, 13, 17)]   # v2..v6 lower bounds
MAXT = 6; K = 9

def ideals(t):
    """order ideals of size K in N^t containing 0 and every generator e_i"""
    base = [tuple(0 for _ in range(t))] + [tuple(1 if j == i else 0 for j in range(t))
                                           for i in range(t)]
    start = frozenset(base)
    if len(start) > K: return []
    frontier = {start}
    for _ in range(K - len(start)):
        nxt = set()
        for S in frontier:
            cand = set()
            for a in S:
                for i in range(t):
                    b = list(a); b[i] += 1; b = tuple(b)
                    if b in S: continue
                    ok = all(tuple(b[:j] + (b[j]-1,) + b[j+1:]) in S
                             for j in range(t) if b[j] > 0)
                    if ok: cand.add(b)
            for b in cand: nxt.add(S | {b})
        frontier = nxt
        if not frontier: break
    return [S for S in frontier if len(S) == K]

def lp_feasible(t, cons):
    """cons: list of (vec, rhs) meaning sum_i vec[i]*y_i <= rhs, i indexes v2..vt"""
    nv = t - 1
    if nv == 0:
        return all(r >= -1e-9 for v, r in cons)
    A = [list(v) for v, r in cons]; b = [r for v, r in cons]
    # y_2 >= log5  ->  -y_2 <= -log5 ; y_{i+1} >= y_i -> y_i - y_{i+1} <= 0
    for i in range(nv):
        e = [0.0]*nv; e[i] = -1.0; A.append(e); b.append(-PLO[i])
    for i in range(nv - 1):
        e = [0.0]*nv; e[i] = 1.0; e[i+1] = -1.0; A.append(e); b.append(0.0)
    r = linprog(c=[0.0]*nv, A_ub=np.array(A), b_ub=np.array(b),
                bounds=[(None, None)]*nv, method="highs")
    return r.status == 0

def le_cons(a, b, t):
    """constraint  monomial a <= monomial b"""
    vec = [float(a[i] - b[i]) for i in range(1, t)]
    rhs = float(b[0] - a[0]) * L3
    return (vec, rhs)

def shape_str(order, t):
    syms = ["3"] + list("pqrst")[:t-1]
    out = []
    for a in order:
        if sum(a) == 0: out.append("1"); continue
        out.append("*".join(syms[i] if a[i] == 1 else "%s^%d" % (syms[i], a[i])
                            for i in range(t) if a[i] > 0))
    return "  ".join(out)

def enumerate_shapes(t, cap=None):
    res = set()
    for S in ideals(t):
        c = sum(1 for a in S if a[0] >= 1)
        if c not in (3, 6): continue          # count lemma, ideal-level
        if t > 9 - c: continue                # t <= 9 - c
        E = [max(a[i] for a in S) for i in range(t)]
        ghosts = [g for g in itertools.product(*[range(E[i]+1) for i in range(t)])
                  if g not in S]
        base = [le_cons(x, g, t) for g in ghosts for x in S]      # g >= every x in S
        if not lp_feasible(t, base): continue
        def rec(order, rem, cons):
            if not rem:
                res.add(shape_str(order, t)); return
            for x in sorted(rem):
                if any(all(z[i] <= x[i] for i in range(t)) and z != x for z in rem):
                    continue                                       # not minimal: divides
                extra = [le_cons(x, z, t) for z in rem if z != x]
                c2 = cons + extra
                if lp_feasible(t, c2): rec(order + [x], rem - {x}, c2)
        rec([], set(S), base)
        if cap and len(res) > cap: break
    return res

if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    allsh = set()
    for t in range(lo, hi+1):
        sh = enumerate_shapes(t)
        print("t=%d : %d ideals, %d shapes" % (t, len(ideals(t)), len(sh)))
        sys.stdout.flush()
        allsh |= sh
    with open(sys.argv[3], "w") as f:
        f.write("\n".join(sorted(allsh)) + "\n")
    print("total", len(allsh), "->", sys.argv[3])

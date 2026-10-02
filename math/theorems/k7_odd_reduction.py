# CLASS: THEOREM
"""
T245, k = 7, n ODD: reduced to 224 unbounded branches; everything else PROVED
empty.  Added 2026-10-02.  This is a reduction, not a closure: k = 7, n odd
stays OPEN.  (k = 7, n even is proved impossible: k7_even_complete.py.)

STEP 1  COMPLETE SHAPE LIST.  tools/k7_odd_shape_enumerator.py: every order
        ideal of size 7 over t <= 6 odd primes, orders and in-box ghosts by LP
        in log space, non-strict (a superset of what primes can realize).
        512 shapes with primes labelled by size.  Negative control: every
        shape realized by an odd n < 1200000 is inside (asserted).
STEP 2  BRANCHES p = 3 and p >= 5 for each shape.
        p = 3: squares of divisors coprime to 3 are 1 (mod 3), so
        n = 7 - c (mod 3), c = number of listed divisors divisible by 3;
        3 | n forces c = 1 (mod 3).  Branches with c = 0, 2 (mod 3) die.
        Residue rule: if, for a listed prime x, the only listed divisor
        coprime to x is 1, then n = 1 (mod x) against x | n: dead.
STEP 3  SIZE: lcm(listed) <= n <= 7 d_7^2 in the LP of each branch.  All
        shapes with 5 or 6 primes die here (in-box ghosts such as pq cap d_7,
        and then the product of the primes exceeds 7 d_7^2).
STEP 4  BOUNDED BRANCHES (the LP caps every prime; all have p <= 7):
        exhausted over all primes up to the caps.  No solution.
OPEN    224 branches in which the LP leaves some prime unbounded, over
        2, 3 or 4 primes (55 / 127 / 42).  They are listed in
        math/theorems/k7_odd_open_branches.txt.  Their conditions are of the
        two-prime-system type T245 already records as open (Theorem C,
        Wieferich-type).

FALSIFICATION: any assertion failing.
"""
import math
import os
import sys

from sympy import divisors, primerange

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import k7_odd_shape_enumerator as E  # noqa: E402

K = 7
SUP = E.superset()
assert len(SUP) == 512
assert all(t <= 6 for t in SUP.values())

# negative control: census of odd n
N = 1_200_000
spf = list(range(N + 1))
for i in range(2, int(N ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, N + 1, i):
            if spf[j] == j:
                spf[j] = i


def small_divs(n, k):
    f = {}
    m = n
    while m > 1:
        p = spf[m]; f[p] = f.get(p, 0) + 1; m //= p
    ds = [1]
    for p, e in f.items():
        ds = [d * p ** i for d in ds for i in range(e + 1)]
    ds.sort()
    return ds[:k], sorted(f)


realized = set()
for n in range(3, N + 1, 2):
    d, ps = small_divs(n, K)
    if len(d) < K:
        continue
    used = sorted({p for p in ps if any(x % p == 0 for x in d)})
    toks = []
    for x in d:
        e = [0] * 6
        for i, p in enumerate(used):
            while x % p == 0:
                x //= p; e[i] += 1
        toks.append(E.tok(tuple(e)))
    realized.add(" ".join(toks))
assert realized <= set(SUP), sorted(realized - set(SUP))[:3]
NREAL = len(realized)


def unit_dead(s):
    T = [E.parse(x) for x in s.split()]
    t = 1 + max(i for a in T for i in range(6) if a[i])
    return any(sum(1 for a in T if a[x] == 0) == 1 for x in range(t))


branches = []
for s in sorted(SUP):
    if unit_dead(s):
        continue
    for br in ("p=3", "p>=5"):
        if br == "p=3" and sum(1 for x in s.split() if E.parse(x)[0] > 0) % 3 != 1:
            continue
        b = E.bounds(s, br)
        if b is not None:
            branches.append((s, br, b))
assert all(SUP[s] <= 4 for s, _, _ in branches)                 # 5 and 6 primes die on size

bounded = [x for x in branches if all(v < math.inf for v in x[2])]
openb = [x for x in branches if any(v == math.inf for v in x[2])]
assert len(bounded) == 65 and len(openb) == 224
assert all(x[2][0] <= 7 + 1e-9 for x in bounded)


def val(tk, P):
    e = E.parse(tk)
    v = 1
    for i, k in enumerate(e):
        if k:
            v *= P[i] ** k
    return v


checked = 0
for s, br, cap in bounded:
    t = len(cap)
    pools = [list(primerange(3, 4)) if (i == 0 and br == "p=3") else
             list(primerange(5 if br == "p>=5" else 3, int(cap[i] + 1e-6) + 1)) for i in range(t)]

    def go(i, P):
        global checked
        if i == t:
            v = [val(x, P) for x in s.split()]
            if v != sorted(v) or len(set(v)) != K:
                return
            n = sum(x * x for x in v)
            checked += 1
            if all(n % x == 0 for x in v):
                assert divisors(n)[:K] != v, (s, P, n)
            return
        for x in pools[i]:
            if i == 0 or x > P[-1]:
                go(i + 1, P + [x])
    go(0, [])

with open(os.path.join(HERE, "k7_odd_open_branches.txt"), "w") as f:
    f.write("# k=7, n odd: branches with an unbounded prime (shape | branch | LP caps)\n")
    for s, br, cap in openb:
        f.write(f"{s} | {br} | {['inf' if v == math.inf else round(v, 1) for v in cap]}\n")

if __name__ == "__main__":
    print(f"k=7 odd: superset {len(SUP)} (census of odd n < {N}: {NREAL} shapes, all inside); "
          f"{len(branches)} live branches = {len(bounded)} bounded (exhausted, {checked} tuples, none) "
          f"+ {len(openb)} unbounded (OPEN)")

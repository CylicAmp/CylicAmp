# CLASS: AUDIT
"""
Audit of a supplied monomial_universe.py (pasted 2026-10-01/02) against the
repo version math/theorems/monomial_universe.py (702 lines).

FINDINGS
 1. The repo version already contains every review fix the supplied version
    describes: canonical() and is_order_ideal() are independent; the empty set
    is vacuously an order ideal; "1 in F" is not a hypothesis (it follows for
    nonempty F).
 2. BUG in the supplied version, fixed in the repo version: the supplied
    generate() caches by k only, so generate(k, "ODD") after generate(k) returns
    the EVEN-tagged family. The repo keys the cache on (k, parity). Asserted.
 3. Design difference: the supplied is_downset pads mixed-length exponent
    vectors into a common N^n ({(0,), (1,0)} is accepted); the repo rejects
    vectors not of the generator's dimension. Repo behaviour kept: the generator
    works in one fixed dimension. Asserted as current behaviour.
 4. Beyond its own tests, the repo generator matches published counts:
    n=1: 1 each; n=2: partition numbers p(k), k <= 11; n=3: plane partitions
    A000219, k <= 10; n=4: solid partitions A000293, k <= 8.

CONNECTION (connect-theorems): T245 / divisor_prefix_ledger.py. The k smallest
divisors of any n form a divisor-closed set, so their exponent vectors (over the
primes dividing them) are an order ideal of size k: the F_k universe is the set
of all possible prefix shapes. Checked on the known solutions 130 (k=4),
1860 (k=11), 148480 (k=19), 3039520 (k=31).

FALSIFICATION: any assertion failing.
"""
import os
import sys

from sympy import divisors, factorint

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import monomial_universe as M  # noqa: E402

G2 = M.UniverseGenerator(2)
assert {s.parity for s in G2.generate(4, "EVEN")} == {"EVEN"}
assert {s.parity for s in G2.generate(4, "ODD")} == {"ODD"}                       # finding 2
assert G2.is_order_ideal(frozenset()) is True                                     # finding 1
o, x, xx = M.Monomial((0, 0)), M.Monomial((1, 0)), M.Monomial((2, 0))
assert M.MonomialShape((x, o), "EVEN", 2).is_order_ideal() and not M.MonomialShape((x, o), "EVEN", 2).canonical()
assert M.MonomialShape((o, xx), "EVEN", 2).canonical() and not M.MonomialShape((o, xx), "EVEN", 2).is_order_ideal()
assert G2.is_order_ideal(frozenset({M.Monomial((0,)), M.Monomial((1, 0))})) is False   # finding 3

A219 = [1, 3, 6, 13, 24, 48, 86, 160, 282, 500]
A293 = [1, 4, 10, 26, 59, 140, 307, 684]
P = [1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56]
assert [len(M.UniverseGenerator(2).generate(k)) for k in range(1, 12)] == P       # finding 4
assert [len(M.UniverseGenerator(3).generate(k)) for k in range(1, 11)] == A219
assert [len(M.UniverseGenerator(4).generate(k)) for k in range(1, 9)] == A293


def prefix_ideal(n, k):
    ds = divisors(n)[:k]
    primes = sorted({p for d in ds for p in factorint(d)})
    vecs = [tuple(factorint(d).get(p, 0) for p in primes) for d in ds]
    return M.UniverseGenerator(len(primes) or 1), [M.Monomial(v) for v in vecs]


for n, k in [(130, 4), (1860, 11), (148480, 19), (3039520, 31)]:
    assert sum(d * d for d in divisors(n)[:k]) == n
    gen, ms = prefix_ideal(n, k)
    assert len(ms) == k and gen.is_order_ideal(frozenset(ms))                     # connection

if __name__ == "__main__":
    print("monomial_universe audit 2026-10-02: all assertions pass")

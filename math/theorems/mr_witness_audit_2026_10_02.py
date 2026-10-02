# CLASS: AUDIT
"""
Miller-Rabin witness audit, 2026-10-02.

Witnesses = the first 12 primes (2..37) are exact only below
psi_12 = 318665857834031151167461 = 399165290221 * 798330580441, which passes
all twelve. Witnesses 2..41 (13 primes) are exact below
psi_13 = 3317044064679887385961981. Several modules used 2..37 while stating
"deterministic below 3.3e24", the psi_13 bound. prime_engine.py was fixed on
2026-09-30 (grid81_operators_applied.py); the same defect remained in:

  k5_odd_shapes.is_prime                          psi_12 -> True (fixed)
  monte_carlo_prime_streams.is_prime_miller_rabin psi_12 -> True (fixed)
  data_ledger_audit.is_prime_miller_rabin         psi_12 -> True (fixed)
  goldilocks_prime.is_prime_deterministic         psi_12 -> True (fixed); also
      returned False for primes 2..41 (witness = n). Fixed with a
      small-prime guard. Its only callers test the Goldilocks prime.

Effect on recorded results: k5_odd_shapes, data_ledger_audit and
goldilocks_prime produce byte-identical output before and after the fix, so
no search in them met psi_12. monte_carlo_prime_streams is unseeded and
differs run to run regardless.

FALSIFICATION: any assertion failing.
"""
import ast
import os
from sympy import isprime, factorint

ROOT = os.path.dirname(os.path.abspath(__file__))
PSI12 = 318665857834031151167461
PSI13 = 3317044064679887385961981
assert factorint(PSI12) == {399165290221: 1, 798330580441: 1}
assert not isprime(PSI13)


def _strong(n, a):
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


W12 = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
assert all(_strong(PSI12, a) for a in W12) and not _strong(PSI12, 41)
assert all(_strong(PSI13, a) for a in W12 + (41,))


def load(fname, fn):
    tree = ast.parse(open(os.path.join(ROOT, fname)).read())
    ns = {}
    exec("import random\nfrom math import gcd\nfrom typing import *", ns)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            exec(ast.unparse(node), ns)
    return ns[fn]


TARGETS = [("k5_odd_shapes.py", "is_prime"),
           ("monte_carlo_prime_streams.py", "is_prime_miller_rabin"),
           ("data_ledger_audit.py", "is_prime_miller_rabin"),
           ("goldilocks_prime.py", "is_prime_deterministic")]
for fname, fn in TARGETS:
    f = load(fname, fn)
    assert f(PSI12) is False, (fname, "psi_12")
    assert all(f(n) == isprime(n) for n in range(2, 20000)), fname
    assert f(2 ** 64 - 2 ** 32 + 1) is True

if __name__ == "__main__":
    print("MR witness audit 2026-10-02: all assertions pass")

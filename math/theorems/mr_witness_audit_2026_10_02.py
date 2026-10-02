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
  cylicamp/rsa_dr_engine.miller_rabin_primality  witnesses 2..11 only; accepted
      2152302898747, 3474749660383, 341550071728321, 3825123056546413051 and
      psi_12. It gates RSA p, q in VerifiedRSAEngine.rsa_key_roundtrip.
      Now 2..41.

Effect on recorded results: k5_odd_shapes, data_ledger_audit and
goldilocks_prime produce byte-identical output before and after the fix, so
no search in them met psi_12. monte_carlo_prime_streams is unseeded and
differs run to run regardless.

FULL SWEEP (2026-10-02): 57 files define a function named *is_prime*, *miller*,
*rabin* or *isprime*. 51 top-level functions in 48 files were run against sympy
on n = -2..4999 and, if they use pow() (Miller-Rabin), on 12 known strong
pseudoprimes up to psi_12: all 51 agree after the fixes above. The other 9
files: 7 nested trial-division functions (eisenstein_prime_split,
board_row_col_numbers_mod37, fps37_scanner, pascal_row8_mod37,
prime_power_sovereign_collapse, T143, T326) -- correct by inspection, divisors
checked up to the square root; 2 name matches that are not primality tests
(api.get_rabinowitsch, gf37_engine.rabinowitsch_residues).

SUPPLIED REVIEW OF THE GOLDILOCKS PATCH (2026-10-02), audited
  1. "The fix is correct: removes witness = n false negatives for primes <= 41
     and handles n < 2."  CORRECT; asserted below.
  2. "The 13-witness set is only conjecturally deterministic above 3e23."
     INCORRECT. Sorenson and Webster (Math. Comp. 86, 2017) computed
     psi_12 = 318665857834031151167461 and psi_13 = 3317044064679887385961981.
     So witnesses 2..41 are PROVEN exact for n < psi_13 ~ 3.3e24, which is the
     range the docstring states. 3e23 is the 12-witness bound, not the 13. Above
     psi_13 the set is not conjectural: it fails at psi_13 itself (asserted).
  3. "The sibling is_prime census matters."  Agreed, and it was run: every
     function named is_prime / miller / rabin in the repo was tested against a
     sieve and the known strong pseudoprimes; the defective ones are listed above.

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
assert all(_strong(PSI13, a) for a in W12 + (41,)) and not _strong(PSI13, 43)   # 13 witnesses fail at psi_13


def load(fname, fn):
    tree = ast.parse(open(os.path.join(ROOT, fname)).read())
    ns = {}
    exec("import random\nfrom math import gcd\nfrom typing import *", ns)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            exec(ast.unparse(node), ns)
    return ns[fn]


TARGETS = [("../../cylicamp/rsa_dr_engine.py", "miller_rabin_primality"),
           ("k5_odd_shapes.py", "is_prime"),
           ("monte_carlo_prime_streams.py", "is_prime_miller_rabin"),
           ("data_ledger_audit.py", "is_prime_miller_rabin"),
           ("goldilocks_prime.py", "is_prime_deterministic")]
for fname, fn in TARGETS:
    f = load(fname, fn)
    assert f(PSI12) is False, (fname, "psi_12")
    assert not any(f(c) for c in (2152302898747, 3474749660383, 341550071728321, 3825123056546413051))
    assert all(f(n) == isprime(n) for n in range(2, 20000)), fname
    assert f(2 ** 64 - 2 ** 32 + 1) is True

_g = load("goldilocks_prime.py", "is_prime_deterministic")
assert [n for n in range(-5, 50) if _g(n)] == [p for p in range(50) if isprime(p)]   # supplied point 1

if __name__ == "__main__":
    print("MR witness audit 2026-10-02: all assertions pass")

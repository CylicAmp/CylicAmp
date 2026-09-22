"""
divisor_prefix_ledger.py

Mechanized ledger for n = sum of the squares of its k smallest divisors.

    n = d_1^2 + d_2^2 + ... + d_k^2,   d_1 < d_2 < ... < d_k
    the k smallest divisors of n.

Why the prefix is an order ideal
--------------------------------
If d | d_i and d_i is among the k smallest divisors, then d <= d_i, so d is
also among them. The prefix is therefore divisor-closed, and the shapes it
can take are exactly the order ideals of size k enumerated by
monomial_universe.UniverseGenerator. That module supplies the universe; this
one supplies the arithmetic.

Known anchor: k = 4 admits n = 130 = 1 + 2^2 + 5^2 + 10^2, divisors
1, 2, 5, 10. Every oracle below is tested against it: an oracle that closes
the shape of 130 is unsound, and self_test() fails.

Coordinates and orbits
----------------------
Coordinate 0 is the prime 2 and is NOT interchangeable; coordinates 1..n-1
are generic odd primes and may be permuted. Shapes are therefore reduced
modulo S_{n-1} acting on coordinates 1.. only.

Admissibility
-------------
An order ideal is realizable as a divisor PREFIX only if nothing is forced
below its largest element. If a, b are coprime and both divide n, then
ab | n; so if ab < max(V) then ab is a divisor below the top and must
already be in V. Note this applies to coprime pairs only: 2 | n does not
force 4 | n, so prime powers are not forced.

ORACLES AND THEIR EPISTEMIC LEVEL
---------------------------------
LEVEL 1 (proved, parameter-free, shape-level -- hold for every realization):

  modular       2^a | n for the largest 2-power 2^a in the prefix, so
                n = 0 mod 2^b for any b <= a. Writing d_i = 2^(a_i) m_i
                with m_i odd, d_i^2 = 2^(2 a_i) m_i^2 and m_i^2 = 1 mod 8.
                That last congruence is a theorem only up to 8, and 1 is
                always in the prefix (a_i = 0), so b <= 3 ALWAYS. The
                modulus is capped at 8 for this reason; using 2^a for
                a >= 4 is unsound (3^2 = 5^2 = 9 mod 16, not 1).

  parity        Every divisor of an odd n is odd, and a sum of k odd
                squares has the parity of k. For EVEN k that sum is even
                and cannot equal an odd n, so the whole odd sector dies.
                Silent at k = 5, where the sum is 5 mod 8 and odd.

  count_mod3    Michael Song's count lemma (commit 02ae900). Divisors
                coprime to 3 square to 1 mod 3, so n = k - c (mod 3) with
                c the count of prefix entries divisible by 3. When 3 | n
                this forces c = k (mod 3), and 3 is then the least prime
                present. Kills the 3 | n branch of any shape failing it.
                NOTE: it closes a BRANCH, not a shape, so it is recorded
                separately and never used as a closing certificate.

  prime_power   For the chain 1, q, q^2, ..., q^(k-1): q | n forces
                n = 0 mod q, while n = 1 + q^2 + ... = 1 mod q. Parameter
                free, so it closes the shape outright.

LEVEL 2 (verified over a bounded prime pool, NOT proved for all primes):

  cofactor_size Every d_i divides n, so lcm(d_1..d_k) | n and hence
                n >= lcm. When n = sum d_i^2 < lcm the shape is impossible.
                Sound for each realization it is checked on, but closing a
                SHAPE this way asserts the inequality for all realizations,
                which is checked here only up to the pool bound.
"""

from dataclasses import dataclass
from typing import Tuple, Optional, List, Dict, Iterable
from math import gcd, lcm
import itertools
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from monomial_universe import UniverseGenerator  # verified order-ideal universe

Shape = Tuple[Tuple[int, ...], ...]

# =====================================================================
# 1. UNIVERSE, ORBITS, ADMISSIBILITY
# =====================================================================

def labeled_universe(k: int, n_vars: Optional[int] = None) -> List[Shape]:
    """All order ideals of size k, from the verified generator."""
    gen = UniverseGenerator(max_variables=n_vars or k)
    return [tuple(m.exponents for m in s.monomials) for s in gen.generate(k)]

def orbit_reps(shapes: Iterable[Shape], n_vars: int) -> Dict[Shape, List[Shape]]:
    """Reduce modulo permutations of the ODD coordinates only (0 is the prime 2)."""
    perms = [(0,) + p for p in itertools.permutations(range(1, n_vars))]
    out: Dict[Shape, List[Shape]] = {}
    for sh in shapes:
        rep = min(tuple(sorted(tuple(v[p] for p in perm) for v in sh)) for perm in perms)
        out.setdefault(rep, []).append(sh)
    return out

def small_primes(count: int) -> List[int]:
    ps, x = [], 2
    while len(ps) < count:
        if all(x % p for p in ps if p * p <= x):
            ps.append(x)
        x += 1
    return ps

def realize(rep: Shape, pmap: Dict[int, int]) -> Tuple[int, ...]:
    """Evaluate a shape at a prime assignment, sorted ascending."""
    vals = []
    for v in rep:
        x = 1
        for i, e in enumerate(v):
            if e:
                x *= pmap[i] ** e
        vals.append(x)
    return tuple(sorted(vals))

def prefix_admissible(vals: Tuple[int, ...]) -> bool:
    """Coprime-product closure: nothing is forced below the largest element."""
    if len(set(vals)) != len(vals):
        return False
    top, S = max(vals), set(vals)
    for a, b in itertools.combinations(sorted(S), 2):
        if gcd(a, b) == 1 and a * b < top and a * b not in S:
            return False
    return True

def realizations(rep: Shape, pool: List[int]) -> List[Tuple[int, ...]]:
    """Every admissible prefix this shape takes over the prime pool."""
    used = sorted({i for v in rep for i, e in enumerate(v) if e > 0})
    odd_slots = [i for i in used if i != 0]
    odd_pool = [p for p in pool if p != 2]
    out = []
    for assign in itertools.permutations(odd_pool, len(odd_slots)):
        pmap = dict(zip(odd_slots, assign))
        if 0 in used:
            pmap[0] = 2
        vals = realize(rep, pmap)
        if prefix_admissible(vals):
            out.append(vals)
    return out

# =====================================================================
# 2. ORACLES
# =====================================================================

@dataclass(frozen=True)
class Certificate:
    strategy: str
    level: int          # 1 = proved for all realizations, 2 = checked on a pool
    detail: str

def oracle_modular(rep: Shape) -> Optional[Certificate]:
    """LEVEL 1. Modulus capped at 8; see the module docstring for why."""
    a = max(v[0] for v in rep)
    for b in range(1, min(a, 3) + 1):
        modulus = 2 ** b
        derived = sum(0 if 2 * v[0] >= b else 2 ** (2 * v[0]) for v in rep) % modulus
        if derived != 0:
            return Certificate(
                "MODULAR_PARITY", 1,
                f"2^{a} | n so n = 0 mod {modulus}, but sum d_i^2 = {derived} mod {modulus}")
    return None

def oracle_prime_power(rep: Shape, k: int) -> Optional[Certificate]:
    """LEVEL 1. The single-prime chain 1, q, ..., q^(k-1)."""
    active = {i for v in rep for i, e in enumerate(v) if e > 0}
    if len(active) != 1:
        return None
    i = next(iter(active))
    if sorted(v[i] for v in rep) != list(range(k)):
        return None
    return Certificate("SINGLE_PRIME_POWER", 1,
                       "q | n forces n = 0 mod q, but n = 1 mod q")

def oracle_cofactor_size(rep: Shape, pool: List[int]) -> Optional[Certificate]:
    """LEVEL 2. lcm(prefix) | n forces n >= lcm; checked over the pool only."""
    reals = realizations(rep, pool)
    if not reals:
        return None
    for vals in reals:
        if sum(v * v for v in vals) >= lcm(*vals):
            return None
    return Certificate("COFACTOR_SIZE", 2,
                       f"n = sum d_i^2 < lcm(d_i) | n on all {len(reals)} "
                       f"realizations over primes <= {pool[-1]}")

def oracle_parity(rep: Shape, k: int) -> Optional[Certificate]:
    """LEVEL 1. Closes the entire ODD sector whenever k is even.

    Every divisor of an odd n is odd, so an odd n forces all k of the
    d_i odd. A sum of k odd squares has the parity of k, hence is even
    when k is even, and cannot equal an odd n.

    Each odd square is 1 mod 8, which sharpens the sum to k mod 8, but
    parity alone is what closes it. At k = 5 the sum is 5 mod 8, odd, so
    the lemma is silent -- which is why the k=5 odd sector needs work.

    The lemma is parameter-free and inherits nothing from any other
    verdict: it reads only k and whether the shape uses the prime 2.
    """
    if k % 2 != 0:
        return None
    if any(v[0] > 0 for v in rep):
        return None                      # even sector; lemma does not apply
    return Certificate(
        "PARITY_EVEN_K", 1,
        f"n odd => all d_i odd => sum d_i^2 = {k} mod 8, even, != odd n")

def oracle_count_mod3(rep: Shape, k: int) -> Optional[Certificate]:
    """LEVEL 1, but closes a BRANCH, not a shape. Never a closing certificate.

    Michael Song's count lemma (commit 02ae900). Every divisor coprime to
    3 squares to 1 mod 3, so with c = #{i <= k : 3 | d_i},

        n = k - c   (mod 3),   and   3 | n  forces  c = k (mod 3).

    If 3 | n then 3 is a divisor, and since only 1 and 2 are smaller, 3
    lies in the prefix for every k >= 3 -- so some slot of the shape holds
    it. Which slot is not determined by the exponent pattern alone (for
    even n the least prime is 2, not 3), so every slot is tried and the
    branch is declared empty only if EVERY placement fails the congruence.
    That is the conservative direction.

    The surviving 3 does-not-divide n branch is untouched, which is why
    this never closes a shape on its own. n = 130 lives in exactly that
    branch, and the k=4 anchor test pins the distinction.
    """
    if k < 3:
        return None
    support = sorted({i for v in rep for i, e in enumerate(v) if e > 0})
    if not support:
        return None
    counts = []
    for slot in support:
        c = sum(1 for v in rep if v[slot] > 0)
        if c % 3 == k % 3:
            return None               # some placement is consistent
        counts.append(c)
    return Certificate(
        "MOD3_CONTENT", 1,
        f"3 | n forces c = {k % 3} (mod 3); no placement of the prime 3 "
        f"achieves it (c in {counts}). The 3 | n branch is empty; "
        f"3 does not divide n is untouched")

def close_shape(rep: Shape, k: int, pool: List[int]) -> Optional[Certificate]:
    return (oracle_parity(rep, k)
            or oracle_modular(rep)
            or oracle_prime_power(rep, k)
            or oracle_cofactor_size(rep, pool))

# =====================================================================
# 3. WITNESS SEARCH (the independent oracle)
# =====================================================================

def first_k_divisors(n: int, k: int, cap: int) -> List[int]:
    out = []
    for d in range(1, cap + 1):
        if n % d == 0:
            out.append(d)
            if len(out) == k:
                return out
    return out

def witnesses(k: int, pool: List[int], n_vars: Optional[int] = None):
    """All n <= pool-bound with n = sum of squares of its k smallest divisors."""
    nv = n_vars or k
    found = []
    for rep in orbit_reps(labeled_universe(k, nv), nv):
        for vals in realizations(rep, pool):
            n = sum(v * v for v in vals)
            if any(n % v for v in vals):
                continue
            if tuple(first_k_divisors(n, k, max(vals))) == vals:
                found.append((n, vals, rep))
    return sorted(set((n, v) for n, v, _ in found))

# =====================================================================
# 4. LEDGER
# =====================================================================

def ledger(k: int, pool: List[int], n_vars: Optional[int] = None) -> Dict:
    nv = n_vars or k
    reps = orbit_reps(labeled_universe(k, nv), nv)
    admissible = [r for r in reps if realizations(r, pool)]
    closed, open_ = [], []
    for rep in admissible:
        cert = close_shape(rep, k, pool)
        (closed if cert else open_).append((rep, cert))
    return {
        "k": k,
        "labeled_ideals": len(labeled_universe(k, nv)),
        "orbits_prime_2_fixed": len(reps),
        "admissible_as_prefix": len(admissible),
        "closed": closed,
        "open": open_,
        "global_status": "PROVED_IMPOSSIBLE" if not open_ else "OPEN",
        "level_1_closures": sum(1 for _, c in closed if c.level == 1),
        "level_2_closures": sum(1 for _, c in closed if c.level == 2),
    }

_NAMES = "2qrst"

def render(rep: Shape) -> str:
    out = []
    for v in sorted(rep, key=lambda v: (sum(v), v)):
        if sum(v) == 0:
            out.append("1")
            continue
        out.append("".join(_NAMES[i] + ("" if e == 1 else f"^{e}")
                           for i, e in enumerate(v) if e))
    return "{" + ", ".join(out) + "}"

# =====================================================================
# 5. SELF-TESTS
# =====================================================================

def test_k4_anchor() -> None:
    """The known solution must be FOUND, and no oracle may close its shape."""
    pool = small_primes(25)
    w = witnesses(4, pool)
    assert (130, (1, 2, 5, 10)) in w, f"lost the k=4 anchor: {w}"
    assert len(w) == 1, f"unexpected extra k=4 witnesses: {w}"

    # Falsification test: the shape of 130 must survive every oracle.
    target = None
    for rep in orbit_reps(labeled_universe(4, 4), 4):
        if (1, 2, 5, 10) in realizations(rep, pool):
            target = rep
    assert target is not None
    cert = close_shape(target, 4, pool)
    assert cert is None, f"UNSOUND: oracle {cert} closed the shape of n=130"
    print("[ok] k=4 anchor: n=130 found; no oracle closes its shape")

def test_modular_soundness_cap() -> None:
    """The modulus must never exceed 8, since odd^2 = 1 is false mod 16."""
    assert 3 ** 2 % 16 == 9 and 5 ** 2 % 16 == 9
    chain = tuple((i, 0, 0, 0, 0) for i in range(5))      # 1,2,4,8,16
    cert = oracle_modular(chain)
    assert cert is not None
    assert "mod 16" not in cert.detail, f"unsound modulus used: {cert.detail}"
    print("[ok] modular oracle capped at 8, still closes the 2-adic chain")

def test_admissibility_rule() -> None:
    """Coprime products are forced; prime powers are not."""
    assert prefix_admissible((1, 2, 3, 6, 9))        # 4 not forced
    assert not prefix_admissible((1, 2, 3, 5, 10))   # 6 < 10 is forced, absent
    assert prefix_admissible((1, 2, 4, 5, 8))
    print("[ok] admissibility: coprime products forced, prime powers not")

def test_k5_ledger() -> None:
    pool = small_primes(40)
    L = ledger(5, pool)
    assert L["labeled_ideals"] == 120
    assert L["orbits_prime_2_fixed"] == 18
    assert L["admissible_as_prefix"] == 13
    assert witnesses(5, pool) == [], "a k=5 witness exists"
    assert L["global_status"] == "OPEN", "ledger must not overclaim"
    print(f"[ok] k=5 ledger: 120 labeled -> 18 orbits -> 13 admissible; "
          f"{len(L['closed'])} closed, {len(L['open'])} open")

def test_parity_lemma() -> None:
    """Even k kills the odd sector; odd k must leave it alone."""
    odd_chain  = tuple((0, i, 0, 0, 0, 0) for i in range(6))   # 1,q,..,q^5
    even_chain = tuple((i, 0, 0, 0, 0, 0) for i in range(6))   # 1,2,..,2^5
    assert oracle_parity(odd_chain, 6) is not None
    assert oracle_parity(even_chain, 6) is None, "lemma must not touch even n"
    assert oracle_parity(odd_chain, 5) is None, "sum of 5 odd squares is odd"
    for k in range(1, 9):
        fires = oracle_parity(tuple((0,) * 6 for _ in range(k)), k) is not None
        assert fires == (k % 2 == 0), k
    print("[ok] parity lemma: fires exactly on even k, odd sector only")

def test_parity_kills_k6_odd_sector() -> None:
    pool = small_primes(12)
    reps = orbit_reps(labeled_universe(6, 6), 6)
    odd = [r for r in reps if all(v[0] == 0 for v in r)]
    assert odd, "no odd k=6 shapes to kill"
    for rep in odd:
        cert = oracle_parity(rep, 6)
        assert cert is not None and cert.level == 1, rep
    print(f"[ok] k=6: all {len(odd)} odd-sector shapes closed at Level 1")

def test_count_mod3_lemma() -> None:
    """Song's count lemma: kills 3|n branches, and never closes a shape."""
    A = ((0,0,0,0,0),(1,0,0,0,0),(2,0,0,0,0),(3,0,0,0,0),(0,1,0,0,0))
    assert oracle_count_mod3(A, 5) is not None, "should kill A's 3|n branch"
    C = ((0,0,0,0,0),(1,0,0,0,0),(0,1,0,0,0),(0,0,1,0,0),(1,1,0,0,0))
    assert oracle_count_mod3(C, 5) is None, "C's 3|n branch survives"

    # The lemma may fire on the n=130 shape -- and what it says is TRUE,
    # since 3 does not divide 130. What must never happen is the shape
    # being CLOSED by it, because 130 lives in the surviving branch.
    anchor = ((0,0,0,0),(1,0,0,0),(0,1,0,0),(1,1,0,0))
    assert 130 % 3 != 0
    pool = small_primes(25)
    assert close_shape(anchor, 4, pool) is None, "UNSOUND: n=130 closed"

    # and it must not be wired into close_shape at all
    import inspect
    assert "oracle_count_mod3" not in inspect.getsource(close_shape), \
        "branch-level lemma must not be a closing certificate"
    print("[ok] count lemma (Song): kills A's 3|n branch, spares C, "
          "never closes n=130")

def self_test() -> None:
    test_admissibility_rule()
    test_parity_lemma()
    test_count_mod3_lemma()
    test_modular_soundness_cap()
    test_k4_anchor()
    test_k5_ledger()
    test_parity_kills_k6_odd_sector()
    print("\nAll self-tests passed.")

if __name__ == "__main__":
    self_test()
    print("\n" + "=" * 62)
    pool = small_primes(40)
    L = ledger(5, pool)
    print(f"k = {L['k']}   global_status = {L['global_status']}")
    print(f"  labeled order ideals      {L['labeled_ideals']}")
    print(f"  orbits (prime 2 fixed)    {L['orbits_prime_2_fixed']}")
    print(f"  admissible as prefix      {L['admissible_as_prefix']}")
    print(f"  closed {len(L['closed'])}  (Level 1: {L['level_1_closures']}, "
          f"Level 2: {L['level_2_closures']})   open {len(L['open'])}")
    print("\nCLOSED")
    for rep, cert in sorted(L["closed"], key=lambda x: (x[1].level, x[1].strategy)):
        print(f"  L{cert.level} {render(rep):<26} {cert.strategy}")
        print(f"        {cert.detail}")
    print("\nOPEN -- no sound argument in this module")
    for rep, _ in L["open"]:
        print(f"     {render(rep)}")

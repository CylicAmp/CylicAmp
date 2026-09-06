"""
Theorem 228: Affine Doubling Topology on Z_{B-1} — General Base GF(37)
Author: Michael Warren Song (CyclicAmp)

For any base B, let m = B-1.  The doubling map T(x) = 2x mod m partitions Z_m
into cycles and transients.  The decisive quantity is the 2-adic valuation v₂(m).

=== CORE THEOREM ===

Factor m = 2^k * q,  q odd  (k = v₂(m) ≥ 0).

CASE k = 0 (m odd, B even):
  gcd(2, m) = 1 — multiplication by 2 is a permutation.
  ALL m states lie on cycles.  No transients exist.

CASE k > 0 (m even, B odd):
  gcd(2, m) = 2 — multiplication by 2 destroys information.
  Exactly q states lie on cycles.
  Exactly m - q states are transient.
  Max transient depth = k.

The cycle structure on cyclic states = cycles of T(x) = 2x mod q,
  which is equivalent to orbits of multiplication by 2 in Z_q*.

=== UNIT / ZERO-DIVISOR DECOMPOSITION ===

For modulus m, Z_m splits into:
  Units:        gcd(x, m) = 1   — count = φ(m) (Euler's totient)
  Zero divisors: gcd(x, m) > 1  — count = m - φ(m) - 1
  Zero:         x = 0           — count = 1

Total = φ(m) + (m - φ(m) - 1) + 1 = m.  ✓

Algebraic strata ≠ dynamical strata when k > 0:
  Units cycle iff gcd(x, q) = 1 (unit in Z_q).
  Zero divisors may orbit (if gcd(x, m) | q) or be transient.

=== FOUR CANONICAL BASES ===

Base  m = B-1  Factorization     v₂  q   Topology
 8    7        prime              0   7   permutation: 1 fixed(0) + 3-cycle + 3-cycle
10    9        3²                 0   9   permutation: 1 fixed(0) + 6-cycle + 2-cycle = 6+2+1
26   25        5²                 0  25   permutation: 1 fixed(0) + 20-cycle + 4-cycle = 20+4+1
 9    8        2³                 3   1   destructive: 1 cyclic state (0), 7 transients

=== GF(37) CONNECTION ===

Base B = 38:  m = 37 (prime).
v₂(37) = 0 — T is a PERMUTATION on Z_37.
All 37 states lie on cycles.
Specifically: T(x) = 2x mod 37 has ord_37(2) = 36 (2 is a primitive root mod 37).
Every nonzero state lies on one 36-cycle.
Plus the fixed point x = 0.

This is the foundational reason the GF(37) has clean cyclic structure:
the base B = 38 doubling map is a complete permutation — nothing collapses,
everything orbits.  All the 3-cycles under the 137-map (MULT = 26 = 137 mod 37)
inherit this non-destructive topology.

=== PRIME-SQUARE IDENTITY ===

For m = p² (p odd prime):
  Units:        p² - p  = p(p-1)
  Nonzero ZDs:  p - 1
  Zero:         1
  Total:        p² - p + p - 1 + 1 = p²  ✓

p = 3 (decimal, m=9):   6 + 2 + 1 = 9
p = 5 (base 26, m=25): 20 + 4 + 1 = 25

The 3-6-9 structure of decimal digital roots is the p=3 instance of p² dynamics.

=== GENERAL THEOREM (FORMAL) ===

For base B, map T(x) = 2x mod (B-1), factorize B-1 = 2^k * q (q odd):

  cyclic_count   = q               (states on eventual cycles)
  transient_count = (B-1) - q      (states that eventually enter cycles)
  max_depth      = k               (maximum transient chain length)
  cycle_lengths  = orbits of x↦2x on Z_q* ∪ {0}

Corollary: decimal (B=10, m=9, k=0) has q=9; all states cyclic.
           base-9 (B=9, m=8, k=3) has q=1; only 0 is cyclic.
"""

import math
from collections import defaultdict


# ── Utilities ────────────────────────────────────────────────────────────────

def v2(n: int) -> int:
    """2-adic valuation of n (largest k with 2^k | n)."""
    if n == 0:
        return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def phi(n: int) -> int:
    """Euler's totient φ(n)."""
    result, p, m = n, 2, n
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            result -= result // p
        p += 1
    if m > 1:
        result -= result // m
    return result


def factor_v2(n: int):
    """Return (k, q) where n = 2^k * q, q odd."""
    k = v2(n)
    q = n >> k
    return k, q


def doubling_topology(m: int) -> dict:
    """
    Analyze T(x) = 2x mod m on Z_m = {0, ..., m-1}.

    Returns dict with:
      factorization     : (k, q)   — m = 2^k * q, q odd
      v2                : k
      unit_count        : φ(m)
      zero_divisor_count: m - φ(m) - 1
      cyclic_states     : list of states on eventual cycles
      transient_states  : list of states NOT on eventual cycles
      cycles            : list of cycles (each a tuple of states)
      cycle_lengths     : sorted list of cycle lengths
      max_transient_depth: longest transient chain
      topology_str      : human-readable summary
    """
    if m == 0:
        raise ValueError("m must be positive")

    k, q = factor_v2(m)

    # Build successor map and find cycles via standard algorithm
    T = {x: (2 * x) % m for x in range(m)}

    # Floyd-Warshall-style: mark all states reachable then on cycles
    on_cycle = set()
    visited = {}
    for start in range(m):
        if start in visited:
            continue
        path = []
        x = start
        while x not in visited and x not in on_cycle:
            visited[x] = len(path)
            path.append(x)
            x = T[x]
        if x in on_cycle:
            pass  # path leads into known cycle
        else:
            # x is revisited from this path — cycle found
            cycle_start_idx = visited[x]
            for node in path[cycle_start_idx:]:
                on_cycle.add(node)

    cyclic = sorted(on_cycle)
    transient = sorted(set(range(m)) - on_cycle)

    # Extract all cycles
    cycles = []
    seen_in_cycle = set()
    for x in cyclic:
        if x in seen_in_cycle:
            continue
        cycle = []
        cur = x
        while cur not in seen_in_cycle:
            seen_in_cycle.add(cur)
            cycle.append(cur)
            cur = T[cur]
        cycles.append(tuple(cycle))

    cycle_lengths = sorted(len(c) for c in cycles)

    # Max transient depth: longest chain before hitting a cycle
    depth_cache = {}

    def depth(x):
        if x in on_cycle:
            return 0
        if x in depth_cache:
            return depth_cache[x]
        d = 1 + depth(T[x])
        depth_cache[x] = d
        return d

    max_depth = max((depth(x) for x in transient), default=0)

    # Topology string: cycle lengths descending + transient info
    cl_str = "+".join(str(l) for l in sorted(cycle_lengths, reverse=True))
    if transient:
        topo = f"{cl_str} [+{len(transient)} transient, depth≤{max_depth}]"
    else:
        topo = cl_str

    return {
        "m": m,
        "factorization": (k, q),
        "v2": k,
        "q": q,
        "unit_count": phi(m),
        "zero_divisor_count": m - phi(m) - 1,
        "cyclic_count": len(cyclic),
        "transient_count": len(transient),
        "cycles": cycles,
        "cycle_lengths": cycle_lengths,
        "max_transient_depth": max_depth,
        "topology_str": topo,
    }


def sweep(base_min: int = 2, base_max: int = 100) -> list:
    """Run the doubling topology analysis over all bases B in [base_min, base_max]."""
    results = []
    for B in range(base_min, base_max + 1):
        m = B - 1
        if m == 0:
            continue
        r = doubling_topology(m)
        r["base"] = B
        results.append(r)
    return results


# ── GF(37) constants ──────────────────────────────────────────────────────────
P    = 37
MULT = 26

SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
D7      = {7, 33, 34}


def run_assertions():
    # ── v₂ utility ────────────────────────────────────────────────────────────
    assert v2(8) == 3
    assert v2(9) == 0
    assert v2(12) == 2
    assert v2(37) == 0   # 37 is odd → prime
    assert v2(25) == 0   # 25 = 5², odd

    # ── Factor theorem ─────────────────────────────────────────────────────────
    assert factor_v2(8) == (3, 1)
    assert factor_v2(9) == (0, 9)
    assert factor_v2(25) == (0, 25)
    assert factor_v2(37) == (0, 37)
    assert factor_v2(12) == (2, 3)

    # ── Four canonical bases ───────────────────────────────────────────────────
    # Base 8 (m=7, prime, k=0): permutation — all 7 states cyclic
    t7 = doubling_topology(7)
    assert t7["v2"] == 0
    assert t7["transient_count"] == 0
    assert t7["cyclic_count"] == 7
    # ord_7(2) = 3 → two 3-cycles + fixed 0
    assert sorted(t7["cycle_lengths"]) == [1, 3, 3]

    # Base 10 (m=9, k=0): permutation — all 9 states cyclic
    t9 = doubling_topology(9)
    assert t9["v2"] == 0
    assert t9["transient_count"] == 0
    assert t9["cyclic_count"] == 9
    # 6-cycle (units) + 2-cycle (multiples of 3) + 1-cycle (0)
    assert sorted(t9["cycle_lengths"]) == [1, 2, 6]

    # Base 26 (m=25, k=0): permutation — all 25 states cyclic
    t25 = doubling_topology(25)
    assert t25["v2"] == 0
    assert t25["transient_count"] == 0
    assert t25["cyclic_count"] == 25
    # ord_25(2) = 20 → 20-cycle (units) + 4-cycle (mult of 5) + 1-cycle (0)
    assert sorted(t25["cycle_lengths"]) == [1, 4, 20]

    # Base 9 (m=8, k=3, q=1): destructive — only 0 is cyclic, 7 transients
    t8 = doubling_topology(8)
    assert t8["v2"] == 3
    assert t8["q"] == 1
    assert t8["cyclic_count"] == 1
    assert t8["transient_count"] == 7
    assert t8["max_transient_depth"] == 3   # depth = v₂(m)

    # ── GF(37) base: B=38, m=37 ───────────────────────────────────────────────
    t37 = doubling_topology(37)
    assert t37["v2"] == 0      # 37 is prime → odd → complete permutation
    assert t37["transient_count"] == 0
    assert t37["cyclic_count"] == 37
    # ord_37(2) = 36 (2 is primitive root mod 37)
    assert pow(2, 36, 37) == 1
    assert pow(2, 18, 37) != 1   # order is exactly 36
    assert sorted(t37["cycle_lengths"]) == [1, 36]   # fixed 0 + 36-cycle
    assert t37["unit_count"] == phi(37) == 36
    assert t37["zero_divisor_count"] == 0   # 37 is prime

    # ── Prime-square identity ─────────────────────────────────────────────────
    for p in [3, 5, 7, 11]:
        m = p * p
        u = phi(m)           # = p² - p = p(p-1)
        z = m - u - 1        # zero divisors
        assert u == p * p - p
        assert z == p - 1
        assert u + z + 1 == m

    # ── General theorem: cyclic_count = q ─────────────────────────────────────
    for m in [4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 36]:
        k, q = factor_v2(m)
        t = doubling_topology(m)
        assert t["cyclic_count"] == q, f"m={m}: cyclic={t['cyclic_count']} ≠ q={q}"
        assert t["transient_count"] == m - q
        assert t["max_transient_depth"] == k if k > 0 else 0

    # ── k=0 means permutation ─────────────────────────────────────────────────
    for m in [1, 3, 5, 7, 9, 11, 15, 21, 25, 35, 37, 45]:
        assert v2(m) == 0
        t = doubling_topology(m)
        assert t["transient_count"] == 0
        assert t["cyclic_count"] == m

    # ── Sweep: theorem holds universally for B=2..50 ─────────────────────────
    results = sweep(2, 50)
    for r in results:
        m = r["m"]
        k, q = factor_v2(m)
        assert r["cyclic_count"] == q, f"B={r['base']}: cyclic={r['cyclic_count']} ≠ q={q}"
        assert r["transient_count"] == m - q

    print("All assertions passed.")
    print()
    print("AFFINE DOUBLING TOPOLOGY — T228")
    print()

    # ── Four canonical bases ──────────────────────────────────────────────────
    print("Four canonical bases:")
    print(f"  {'Base':>5}  {'m=B-1':>6}  {'k=v₂':>5}  {'q':>4}  {'cyclic':>7}  {'transient':>10}  topology")
    for B, label in [(8,"prime"), (10,"3²"), (26,"5²"), (9,"2³")]:
        m = B - 1
        r = doubling_topology(m)
        print(f"  {B:>5}  {m:>6}  {r['v2']:>5}  {r['q']:>4}  {r['cyclic_count']:>7}  {r['transient_count']:>10}  {r['topology_str']}")

    # ── GF(37) base ───────────────────────────────────────────────────────────
    print()
    print("GF(37) base (B=38, m=37):")
    r37 = doubling_topology(37)
    print(f"  v₂(37) = {r37['v2']}  (37 is prime → complete permutation)")
    print(f"  Cyclic: {r37['cyclic_count']}  Transient: {r37['transient_count']}")
    print(f"  ord_37(2) = 36  (2 is primitive root mod 37)")
    print(f"  Topology: {r37['topology_str']}")
    print(f"  This is WHY the GF(37) has clean cyclic structure.")

    # ── Prime-square table ────────────────────────────────────────────────────
    print()
    print("Prime-square topology (m = p²):")
    print(f"  {'p':>4}  {'m=p²':>5}  {'units φ(m)':>10}  {'ZDs m-φ-1':>10}  cycle lengths")
    for p in [3, 5, 7, 11, 13]:
        m = p * p
        r = doubling_topology(m)
        print(f"  {p:>4}  {m:>5}  {r['unit_count']:>10}  {r['zero_divisor_count']:>10}  {r['topology_str']}")

    # ── Full sweep 2..100: summary by v₂ class ────────────────────────────────
    print()
    print("Sweep B=2..100 — count by 2-adic class:")
    results = sweep(2, 100)
    by_k = defaultdict(list)
    for r in results:
        by_k[r["v2"]].append(r["base"])
    for k in sorted(by_k.keys()):
        bases = by_k[k]
        print(f"  v₂(m)={k}: {len(bases)} bases: {bases[:8]}{'...' if len(bases)>8 else ''}")

    # ── Notable: bases where B-1 = p² (prime square) ─────────────────────────
    print()
    print("Bases where B-1 is an odd prime square (reversible + stratified):")
    ps_bases = []
    for r in results:
        m = r["m"]
        k, q = factor_v2(m)
        if k == 0:
            # check if m = p² for some prime p
            sq = int(math.isqrt(m))
            if sq * sq == m and all(m % p != 0 for p in range(2, sq)):
                ps_bases.append((r["base"], m, sq))
    for B, m, p in ps_bases:
        print(f"  B={B:>3}  m={m:>4} = {p}²")


if __name__ == "__main__":
    run_assertions()

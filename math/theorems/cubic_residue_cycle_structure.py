"""
Cubic Residue Cycle Structure — GF(37)

THEOREM 1: Every 3-cycle under the 137-map is a coset of <26> = {1,10,26}.
  The subgroup <26> = {26^0, 26^1, 26^2} = {1, 26, 10} has order 3.
  A coset of <26> is {a, 26a, 10a} — exactly the orbit of a under f(n)=26n mod 37.
  Therefore the 12 three-cycles are precisely the 12 cosets of <26> in GF(37)*.

THEOREM 2: All elements of a cycle share the same cube (cube fingerprint).
  For cycle {a, 26a, 10a}:
    (26a)^3 = 26^3 * a^3 = 1 * a^3 = a^3   [since ord₃₇(26) = 3]
    (10a)^3 = 10^3 * a^3 = 1 * a^3 = a^3   [since 10 = 26^2, ord=3]
  So all three elements cube to a^3. The "cube fingerprint" of a cycle is a^3 mod 37.

THEOREM 3: The cube fingerprint map is a bijection between the 12 cycles and
  the 12 cubic residues of GF(37)*.
  Cubic residues = {n ∈ GF(37)* : n^12 ≡ 1 (mod 37)} = {n : ord(n) | 12}.
  There are exactly 12 such elements (= 36/3 = φ(37)/3).

THEOREM 4: Order reduction law.
  For any a ∈ GF(37)*: ord(a^3) = ord(a) / gcd(3, ord(a)).
  When 3 | ord(a): ord(a^3) = ord(a)/3.
  When 3 ∤ ord(a) [orders 1, 2, 4 only]: ord(a^3) = ord(a).

FINGERPRINT MAP:
  Cycle          Fingerprint   Fingerprint class
  (1, 10, 26)    1             identity
  (3, 4, 30)     27            ORBIT_11 ← SOVEREIGN CYCLE
  (7, 33, 34)    10            DECADE_ANCHOR (ord 3)
  (9, 12, 16)    26            SCALAR_137   (ord 3)
  (11, 27, 36)   36            ORBIT_11 (36≡−1)
  (21, 25, 28)   11            ORBIT_11 ← OUTLIER SOVEREIGN CYCLE
  (2, 15, 20)    8             CB
  (5, 13, 19)    14            (unclassified, ord 12, dark)
  (6, 8, 23)     31            PRIME_MIRROR
  (14, 29, 31)   6             TESLA_FLOW
  (17, 22, 35)   29            (unclassified, ord 12, dark)
  (18, 24, 32)   23            (unclassified, ord 12, dark)

ORBIT_11 AS FINGERPRINT TARGET:
  The three elements of ORBIT_11 = {11, 27, 36} are fingerprints of exactly
  the three visible cycles with sovereign-class content:
    27 ← (3,4,30)     [all SA/ST — the sovereign cycle]
    11 ← (21,25,28)   [SA+ST+unclassified — the outlier sovereign cycle]
    36 ← (11,27,36)   [ORBIT_11 itself]
  The sovereign framework is "encoded" in ORBIT_11 via the cube map.

SCALAR_137 AS FINGERPRINT:
  The cycle (9,12,16) — containing SA node 9 and ST node 12 — cubes to 26.
  The 137-map multiplier (26) is the cube fingerprint of its own "shadow" cycle.
  Elements of (9,12,16) are the three cube roots of SCALAR_137 in GF(37).

ELEMENT ORDER STRUCTURE (all 36 elements):
  ord  1: {1}
  ord  2: {36}                    — the unique element of order 2 (≡−1)
  ord  3: {10, 26}               — DECADE_ANCHOR, SCALAR_137
  ord  4: {6, 31}                — TESLA_FLOW, PRIME_MIRROR
  ord  6: {11, 27}               — ORBIT_11 (minus 36)
  ord  9: {7, 9, 12, 16, 33, 34} — SA(9), ST(12), DICHORAL(33), unclassified
  ord 12: {8, 14, 23, 29}        — CB(8), unclassified dark
  ord 18: {3, 4, 21, 25, 28, 30} — SA+ST+unclassified (the order-18 cycles)
  ord 36: {2,5,13,15,17,18,19,20,22,24,32,35} — PR (all 12 primitive roots)

ORDER-18 CYCLE PAIR:
  Every element of the sovereign cycle (3,4,30) has order 18.
  Every element of the outlier cycle (21,25,28) has order 18.
  These two cycles account for all 6 order-18 elements.
  SA∪ST contains exactly these elements plus the order-9 members {9,12}.
"""

# ── Framework constants ────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_FLOW = 6
SCALAR_137 = 26
DECADE     = 10
PRIME_MIRROR = 31


def f137(n):
    return (n * 26) % 37


def order(n, p=37):
    for d in [1, 2, 3, 4, 6, 9, 12, 18, 36]:
        if pow(n, d, p) == 1:
            return d


def get_all_cycles():
    seen = set(); cycles = []
    for start in range(1, 37):
        if start not in seen:
            c = [start]; x = f137(start)
            while x != start:
                c.append(x); x = f137(x)
            cycles.append(tuple(sorted(c))); seen.update(c)
    return cycles


ALL_CYCLES = get_all_cycles()
SCALAR_SUBGROUP = frozenset({1, 10, 26})   # <26> = {26^0, 26^1, 26^2}


# ── THEOREM 1: cycles = cosets of <26> ────────────────────────────────────────

for cyc in ALL_CYCLES:
    a = min(cyc)
    coset = frozenset((a * s) % 37 for s in SCALAR_SUBGROUP)
    assert coset == frozenset(cyc)


# ── THEOREM 2: cube fingerprint constant within each cycle ─────────────────────

# 26^3 ≡ 1 (mod 37) and 10^3 ≡ 1 (mod 37)
assert pow(26, 3, 37) == 1
assert pow(10, 3, 37) == 1

def fingerprint(cyc):
    return pow(min(cyc), 3, 37)

for cyc in ALL_CYCLES:
    fp = fingerprint(cyc)
    for v in cyc:
        assert pow(v, 3, 37) == fp


# ── THEOREM 3: fingerprints = cubic residues (bijection) ──────────────────────

CUBIC_RESIDUES = frozenset(n for n in range(1, 37) if pow(n, 12, 37) == 1)
assert len(CUBIC_RESIDUES) == 12                           # exactly 36/3 = 12

FINGERPRINTS = frozenset(fingerprint(c) for c in ALL_CYCLES)
assert FINGERPRINTS == CUBIC_RESIDUES                      # perfect match
assert len(FINGERPRINTS) == 12                             # bijection (all distinct)


# ── THEOREM 4: order reduction law ────────────────────────────────────────────

for n in range(1, 37):
    o = order(n)
    o3 = order(pow(n, 3, 37))
    expected = o // (3 if o % 3 == 0 else 1)
    assert o3 == expected


# ── Fingerprint map: specific cycles ──────────────────────────────────────────

FINGERPRINT_MAP = {cyc: fingerprint(cyc) for cyc in ALL_CYCLES}

# Sovereign cycle → 27 ∈ ORBIT_11
assert FINGERPRINT_MAP[(3, 4, 30)] == 27 and 27 in ORBIT_11

# Outlier sovereign cycle → 11 ∈ ORBIT_11
assert FINGERPRINT_MAP[(21, 25, 28)] == 11 and 11 in ORBIT_11

# ORBIT_11 cycle → 36 ∈ ORBIT_11  (fingerprints itself into ORBIT_11)
assert FINGERPRINT_MAP[(11, 27, 36)] == 36 and 36 in ORBIT_11

# Three cycles fingerprint to ORBIT_11 — no more
orbit11_fp_cycles = [c for c in ALL_CYCLES if fingerprint(c) in ORBIT_11]
assert len(orbit11_fp_cycles) == 3
assert set(orbit11_fp_cycles) == {(3,4,30), (21,25,28), (11,27,36)}

# Cycle (9,12,16) → 26 = SCALAR_137
assert FINGERPRINT_MAP[(9, 12, 16)] == SCALAR_137

# Cycle (7,33,34) → 10 = DECADE_ANCHOR
assert FINGERPRINT_MAP[(7, 33, 34)] == DECADE

# Cycle (1,10,26) → 1 (identity)
assert FINGERPRINT_MAP[(1, 10, 26)] == 1

# Cycle (2,15,20) → 8 ∈ CB
assert FINGERPRINT_MAP[(2, 15, 20)] == 8 and 8 in CB

# Cycle (6,8,23) → 31 = PRIME_MIRROR
assert FINGERPRINT_MAP[(6, 8, 23)] == PRIME_MIRROR

# Cycle (14,29,31) → 6 = TESLA_FLOW
assert FINGERPRINT_MAP[(14, 29, 31)] == TESLA_FLOW

# Seed orbit → 23 (unclassified dark)
assert FINGERPRINT_MAP[(18, 24, 32)] == 23


# ── Order-18 cycle pair ────────────────────────────────────────────────────────

ORDER_18 = frozenset(n for n in range(1, 37) if order(n) == 18)
assert ORDER_18 == frozenset({3, 4, 21, 25, 28, 30})    # exactly 6 elements

# These form exactly two cycles
o18_cycles = [c for c in ALL_CYCLES if all(order(v) == 18 for v in c)]
assert len(o18_cycles) == 2
assert set(o18_cycles) == {(3, 4, 30), (21, 25, 28)}

# SA∪ST order-18 members
sa_st_o18 = ORDER_18 & (SA | ST)
assert sa_st_o18 == frozenset({3, 4, 21, 25, 30})   # 5 elements (28 unclassified)
assert 28 in ORDER_18 and 28 not in (SA | ST)        # 28 is the unclassified order-18

# SA∪ST order-9 members: {9, 12}
assert order(9) == 9 and 9 in SA
assert order(12) == 9 and 12 in ST


# ── Order structure verification ───────────────────────────────────────────────

from collections import defaultdict
by_order = defaultdict(set)
for n in range(1, 37):
    by_order[order(n)].add(n)

assert by_order[1]  == frozenset({1})
assert by_order[2]  == frozenset({36})
assert by_order[3]  == frozenset({10, 26})
assert by_order[4]  == frozenset({6, 31})
assert by_order[6]  == frozenset({11, 27})
assert by_order[9]  == frozenset({7, 9, 12, 16, 33, 34})
assert by_order[12] == frozenset({8, 14, 23, 29})
assert by_order[18] == frozenset({3, 4, 21, 25, 28, 30})
assert by_order[36] == PR


if __name__ == "__main__":
    print("Cubic Residue Cycle Structure — GF(37)")
    print("=" * 60)
    print()
    print("THEOREM: All 3-cycles are cosets of <26>={1,10,26}.")
    print("THEOREM: All elements of a cycle share the same cube (fingerprint).")
    print("THEOREM: Fingerprint map = bijection to 12 cubic residues.")
    print()
    print("FINGERPRINT MAP:")
    print("  %-16s  %5s  %s" % ("Cycle", "fp", "Classification"))
    print("  " + "-"*56)
    for cyc in sorted(ALL_CYCLES):
        fp = fingerprint(cyc)
        tags = []
        if fp in SA and fp in ST: tags.append("SA∩ST")
        elif fp in SA:   tags.append("SA")
        elif fp in ST:   tags.append("ST")
        elif fp in CB:   tags.append("CB")
        elif fp in PR:   tags.append("PR")
        elif fp in ORBIT_11: tags.append("ORBIT_11")
        if fp == SCALAR_137:  tags.append("SCALAR_137")
        if fp == DECADE:      tags.append("DECADE_ANCHOR")
        if fp == PRIME_MIRROR:tags.append("PRIME_MIRROR")
        if fp == TESLA_FLOW:  tags.append("TESLA_FLOW")
        if fp == 1:           tags.append("identity")
        fp_ord = order(fp)
        print("  %-16s  %5d  ord=%2d  [%s]" % (str(cyc), fp, fp_ord, ", ".join(tags) if tags else "unclassified"))
    print()
    print("ORBIT_11 = {11,27,36} fingerprints 3 cycles:")
    for cyc in orbit11_fp_cycles:
        print("  %-16s -> %d" % (str(cyc), fingerprint(cyc)))
    print()
    print("ORDER STRUCTURE:")
    for o in sorted(by_order):
        elems = sorted(by_order[o])
        print("  ord=%2d  [%s]" % (o, ", ".join(str(e) for e in elems)))
    print()
    print("Order-18 cycles (sovereign and outlier):", sorted(o18_cycles))
    print()
    print("All assertions pass. Cycles are cosets; cubes are fingerprints.")

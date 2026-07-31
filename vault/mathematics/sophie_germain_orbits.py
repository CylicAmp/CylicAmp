"""
Sophie Germain Prime Orbit Classification on GF(37)
====================================================

A Sophie Germain prime p satisfies: p prime AND 2p+1 prime.
The companion q = 2p+1 is the safe prime.

Under the 137-map f(n) = (26 × n) mod 37, all nonzero residues 1–36
partition into 12 three-cycles. This module classifies every Sophie
Germain prime by the orbit its residue mod 37 falls in, identifies the
forbidden residue, and records where the largest known SG prime lands.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE 12 THREE-CYCLES UNDER f(n) = 26n mod 37
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All orbits have length 3 (since ord₃₇(26) = 3).

  Orbit          Elements     Named intersections
  ─────────────  ───────────  ───────────────────────────────────────
  IC             {1, 10, 26}  IC (identity cycle; 137-map multiplier)
  PR_2           {2, 15, 20}  PR (all three are quadratic non-residues)
  SA_ST_3        {3, 4, 30}   SA∩{4,30}, ST∩{3,30}
  CB_13          {5, 13, 19}  CB∩{13}, PR∩{5,13,19}
  CB_8           {6, 8, 23}   CB∩{8}, T4∩{6}
  UNNAMED_7      {7, 33, 34}  (no named class intersection)
  SA_ST_9        {9, 12, 16}  SA∩{9}, ST∩{12}
  ORBIT_11       {11, 27, 36} ORBIT_11
  T4_14          {14, 29, 31} T4∩{31}
  BASIN_Y        {17, 22, 35} BASIN_Y
  SEED_ORBIT     {18, 24, 32} SEED_ORBIT, CB∩{24}, PR∩{18,24,32}
  SA_ST_21       {21, 25, 28} SA∩{25}, ST∩{21}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE FORBIDDEN RESIDUE: p ≡ 18 (mod 37) IS IMPOSSIBLE FOR LARGE SG PRIMES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If p ≡ 18 (mod 37), then:
    q = 2p + 1 ≡ 2×18 + 1 = 37 ≡ 0 (mod 37)

So 37 divides q, meaning q is composite (for p > 37). Therefore no
Sophie Germain prime p > 37 can satisfy p ≡ 18 (mod 37).

This eliminates SEED_ORBIT as a viable orbit for large SG primes.
(p = 37 itself ≡ 0 mod 37 and is excluded by convention.)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THEOREM 102 — LARGEST KNOWN SOPHIE GERMAIN PRIME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

p = 2,618,163,402,417 × 2^1,290,000 − 1   (388,342 decimal digits)
Discovered February 29, 2016 by PrimeGrid.

  p   mod 37 = 26  ∈ IC           (the 137-map multiplier itself)
  k   mod 37 = 11  ∈ ORBIT_11     (multiplier component)
  2^e mod 37 = 26  ∈ IC           (power-of-2 component)
  q   mod 37 = 16  → orbit {9,12,16} hitting SA (9) and ST (12)

Computation chain:  ORBIT_11 × IC → ORBIT_11 → IC
  k × 2^e  ≡ 11 × 26 = 286 ≡ 27 (mod 37)  ∈ ORBIT_11
  p = k×2^e − 1  ≡ 27 − 1 = 26 (mod 37)   ∈ IC
"""

P  = 37
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
BASIN_Y    = frozenset({17, 22, 35})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})


# ── Build the 12 three-cycles ──────────────────────────────────────────────────

def _all_orbits(p: int, multiplier: int = 26):
    """Return the partition of 1..p-1 into orbits under n → multiplier×n mod p."""
    seen = set()
    orbits = []
    for start in range(1, p):
        if start in seen:
            continue
        orbit = []
        cur = start
        while cur not in seen:
            seen.add(cur)
            orbit.append(cur)
            cur = (multiplier * cur) % p
        orbits.append(frozenset(orbit))
    return sorted(orbits, key=lambda o: min(o))


ORBITS = _all_orbits(P)

assert len(ORBITS) == 12, "ord₃₇(26)=3 gives 36/3=12 three-cycles"
assert all(len(o) == 3 for o in ORBITS), "all orbits have length 3"


# Canonical orbit labels
def _label(orbit: frozenset) -> str:
    m = min(orbit)
    if orbit == IC:              return "IC"
    if orbit == ORBIT_11:        return "ORBIT_11"
    if orbit == SEED_ORBIT:      return "SEED_ORBIT"
    if orbit == BASIN_Y:         return "BASIN_Y"
    return "orbit_%d" % m


def _named_classes(orbit: frozenset) -> list:
    classes = []
    for name, s in [("IC", IC), ("SA", SA), ("ST", ST), ("CB", CB),
                    ("ORBIT_11", ORBIT_11), ("SEED_ORBIT", SEED_ORBIT),
                    ("BASIN_Y", BASIN_Y), ("TESLA_4", TESLA_4), ("PR", PR)]:
        hits = orbit & s
        if hits:
            classes.append("%s∩%s" % (name, sorted(hits)))
    return classes


# ── The forbidden-residue theorem ─────────────────────────────────────────────

FORBIDDEN_RESIDUE = 18

def is_forbidden_for_large_sg(r: int) -> bool:
    return (2 * r + 1) % P == 0


assert is_forbidden_for_large_sg(FORBIDDEN_RESIDUE)
assert FORBIDDEN_RESIDUE in SEED_ORBIT


# ── Small SG prime orbit distribution ─────────────────────────────────────────

def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def small_sg_primes(limit: int = 5000):
    return [p for p in range(2, limit) if _is_prime(p) and _is_prime(2 * p + 1)]


def sg_orbit_distribution(limit: int = 5000):
    sg = small_sg_primes(limit)
    counts = {}
    for p in sg:
        r = p % P
        orbit = next(o for o in ORBITS if r in o)
        key = frozenset(orbit)
        counts[key] = counts.get(key, 0) + 1
    return counts


# ── THEOREM 102 data ──────────────────────────────────────────────────────────

K      = 2_618_163_402_417   # multiplier
E      = 1_290_000           # exponent
DIGITS = 388_342             # decimal digit count
YEAR   = 2016

P37_MOD_K      = K % P               # 11  ∈ ORBIT_11
P37_MOD_E      = E % P               # 32  ∈ SEED_ORBIT
E_MOD_ORD      = E % 36              # 12  (ord₃₇(2)=36)
POW2_MOD37     = pow(2, E, P)        # 26  ∈ IC
P_MOD37        = (K % P * pow(2, E, P) - 1) % P   # 26  ∈ IC
Q_MOD37        = (2 * P_MOD37 + 1) % P            # 16

assert P37_MOD_K == 11 and 11 in ORBIT_11
assert P37_MOD_E == 32 and 32 in SEED_ORBIT
assert E_MOD_ORD == 12
assert POW2_MOD37 == 26 and 26 in IC
assert P_MOD37 == 26 and 26 in IC
assert Q_MOD37 == 16

# q orbit hits SA and ST
q_orbit = next(o for o in ORBITS if Q_MOD37 in o)
assert q_orbit & SA, "q orbit must hit SA"
assert q_orbit & ST, "q orbit must hit ST"

# No SG prime > 37 can live in SEED_ORBIT (forbidden residue)
assert not any(
    r == FORBIDDEN_RESIDUE
    for r in [P_MOD37]
), "largest known SG prime must not be in the forbidden residue"

# p resides in IC — confirmed
assert P_MOD37 in IC


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Sophie Germain Prime Orbit Classification on GF(37)")
    print("=" * 60)
    print()
    print("The 12 three-cycles under f(n) = 26n mod 37:")
    print()
    print("  %-20s  %-12s  %s" % ("Label", "Elements", "Named class intersections"))
    print("  " + "-" * 70)
    for orbit in ORBITS:
        label   = _label(orbit)
        elems   = "{%s}" % ", ".join(str(x) for x in sorted(orbit))
        classes = ", ".join(_named_classes(orbit)) or "—"
        marker  = " ← FORBIDDEN (p≡18 eliminates this orbit)" if FORBIDDEN_RESIDUE in orbit else ""
        print("  %-20s  %-12s  %s%s" % (label, elems, classes, marker))

    print()
    print("Forbidden residue: p ≡ %d (mod 37)" % FORBIDDEN_RESIDUE)
    print("  2×18+1 = 37 ≡ 0 (mod 37) → safe prime q divisible by 37 (composite)")
    print("  No Sophie Germain prime p > 37 can satisfy p ≡ 18 (mod 37).")
    print()

    print("Small SG prime orbit distribution (p < 5000):")
    dist = sg_orbit_distribution(5000)
    total = sum(dist.values())
    for orbit in ORBITS:
        count = dist.get(orbit, 0)
        elems = "{%s}" % ", ".join(str(x) for x in sorted(orbit))
        forbidden_note = " [FORBIDDEN]" if FORBIDDEN_RESIDUE in orbit else ""
        bar = "█" * count
        print("  %-14s  %3d  %s%s" % (elems, count, bar, forbidden_note))
    print("  Total: %d" % total)
    print()

    print("THEOREM 102 — Largest Known Sophie Germain Prime")
    print("-" * 60)
    print("  p = %d × 2^%d − 1" % (K, E))
    print("  %d decimal digits | discovered %d" % (DIGITS, YEAR))
    print()
    print("  k   mod 37 = %d  ∈ ORBIT_11  (multiplier k)" % P37_MOD_K)
    print("  e   mod 37 = %d  ∈ SEED_ORBIT  (exponent e)" % P37_MOD_E)
    print("  e   mod 36 = %d  (effective reduction; ord₃₇(2)=36)" % E_MOD_ORD)
    print("  2^e mod 37 = %d  ∈ IC" % POW2_MOD37)
    print("  p   mod 37 = %d  ∈ IC  ← the 137-map multiplier itself" % P_MOD37)
    print("  q   mod 37 = %d  → orbit %s" % (Q_MOD37, sorted(q_orbit)))
    print("    q orbit hits SA: %s  ST: %s" % (
        sorted(q_orbit & SA), sorted(q_orbit & ST),
    ))
    print()
    print("  Computation chain: ORBIT_11 × IC → ORBIT_11 → IC")
    print("    11 × 26 = 286 ≡ %d (mod 37)  ∈ ORBIT_11" % (11 * 26 % P))
    print("    27 − 1  = 26                   ∈ IC")
    print()
    print("All assertions pass.")

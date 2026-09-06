"""
T293 — p=37 Is the Unique Admissible Prime with an Orbit-Aligned Anomalous Curve

T292 proved {7, 37, 73} is the COMPLETE set of primes with ord_p(137)=3.
This theorem pushes T288/T289 across all three and finds a uniqueness.

The T288 structure requires TWO independent conditions. Each fails at a
DIFFERENT prime, and only p=37 satisfies both.

════════════════════════════════════════════════════════════════════════════
CONDITION 1 — orbit must sit inside the 6th powers
════════════════════════════════════════════════════════════════════════════
Two curves y^2=x^3+a and y^2=x^3+a' are isomorphic iff a'/a is a 6th power.
So #E is constant on a set S iff S lies in one coset of (F_p*)^6.
The 137-map orbit is <mult>, of order 3. Point counts are constant on orbits
iff <mult> is contained in (F_p*)^6, i.e. iff 3 | (p-1)/gcd(6, p-1).

    p= 7: |(F_p*)^6| = 6/6  =  1   <4> = {1,2,4}  NOT inside   -> FAILS
    p=37: |(F_p*)^6| = 36/6 =  6   <26>={1,10,26} inside {1,10,11,26,27,36}
    p=73: |(F_p*)^6| = 72/6 = 12   <64>={1,8,64}  inside       -> holds

At p=7 the 6th powers are trivial (x^6 = 1 for every x, by Fermat), so every
a is its own isomorphism class. Point counts vary WITHIN an orbit:
    a in {1,2,4}: #E = 3, 9, 12    a in {3,5,6}: #E = 4, 7, 13
The orbit structure carries no information about curve counts at p=7.

════════════════════════════════════════════════════════════════════════════
CONDITION 2 — trace 1 must occur (anomalous curve must exist at all)
════════════════════════════════════════════════════════════════════════════
For j=0 curves over F_p with p = 1 mod 3, CM theory gives 4p = L^2 + 27M^2,
and the six traces are {+-L, +-(L+9M)/2, +-(L-9M)/2}.

    p= 7: 4p= 28 =  1 + 27      L=1,  M=1 -> traces {+-1, +-4, +-5}   1 present
    p=37: 4p=148 =121 + 27      L=11, M=1 -> traces {+-1, +-10,+-11}  1 present
    p=73: 4p=292 = 49 + 243     L=7,  M=3 -> traces {+-7, +-10,+-17}  NO 1

At p=73 there is NO anomalous j=0 curve at all — trace 1 simply is not in the
attainable set. The orbit structure is perfect there (24 orbits, counts
constant, 12 antipodal pairs), but the anomalous class does not exist.

════════════════════════════════════════════════════════════════════════════
RESULT
════════════════════════════════════════════════════════════════════════════
       p    cond 1 (orbit<=6th)   cond 2 (1 in traces)   both
       7          False                  True            No
      37          True                   True            YES
      73          True                   False           No

p=37 is the UNIQUE prime in the complete admissible set where an anomalous
j=0 curve exists AND the point count is constant on 137-map orbits — which is
what makes T288's "anomalous class = one antipodal orbit pair" statement
possible. At p=7 the alignment fails; at p=73 the anomaly fails.

The two failures are for unrelated reasons — one is about 6th-power index,
the other about a quadratic form representation. They are not two symptoms of
one cause, which is what makes the p=37 coincidence non-trivial.

Verified counts at p=73 (orbit structure holds, no anomaly):
    traces present: -17, -10, -7, +7, +10, +17;  #E in {57,64,67,81,84,91}
    p+1 = 74 is never attained as #E - t = 74 with t=1 (i.e. #E=73 absent).
"""

from math import gcd, isqrt

ADMISSIBLE = [7, 37, 73]


def count_points(a, p):
    n = 1
    for x in range(p):
        rhs = (x ** 3 + a) % p
        for y in range(p):
            if (y * y) % p == rhs:
                n += 1
    return n


def orbits_of(p):
    mult = 137 % p
    seen, orbs = set(), []
    for x in range(1, p):
        if x in seen:
            continue
        o = frozenset({x, (x * mult) % p, (x * mult * mult) % p})
        seen |= o
        orbs.append(o)
    return orbs


def cm_traces(p):
    """4p = L^2 + 27M^2 -> the six j=0 traces."""
    M = 1
    while 27 * M * M < 4 * p:
        r = 4 * p - 27 * M * M
        s = isqrt(r)
        if s * s == r:
            L = s
            half1 = (L + 9 * M) // 2
            half2 = (L - 9 * M) // 2
            return L, M, sorted({L, -L, half1, -half1, half2, -half2})
        M += 1
    raise ValueError(f"no representation for p={p}")


# ─── Condition 1 ─────────────────────────────────────────────────────────────

def condition_1(p):
    """Orbit <mult> contained in the 6th powers?"""
    mult = 137 % p
    sixth = {pow(x, 6, p) for x in range(1, p)}
    om = {pow(mult, i, p) for i in range(3)}
    inside = om <= sixth
    # equivalent arithmetic test
    assert inside == ((p - 1) // gcd(6, p - 1) % 3 == 0), \
        f"p={p}: set test and divisibility test disagree"
    return inside, sorted(sixth), sorted(om)


# ─── Condition 2 ─────────────────────────────────────────────────────────────

def condition_2(p):
    L, M, traces = cm_traces(p)
    return (1 in traces), L, M, traces


# ─── Verification ────────────────────────────────────────────────────────────

def verify_counts_constant(p, expected):
    """Check empirically whether #E is constant on every orbit."""
    for o in orbits_of(p):
        counts = {count_points(a, p) for a in o}
        if expected:
            assert len(counts) == 1, f"p={p}: orbit {sorted(o)} varies {counts}"
        else:
            if len(counts) > 1:
                return False
    return True


def verify_traces_match(p):
    """Empirical traces must equal the CM prediction."""
    _, _, predicted = cm_traces(p)
    seen = {p + 1 - count_points(a, p) for a in range(1, p)}
    assert seen == set(predicted), f"p={p}: {sorted(seen)} != {predicted}"
    return sorted(seen)


def verify_anomalous_set(p):
    anom = sorted(a for a in range(1, p) if count_points(a, p) == p)
    orbs = orbits_of(p)
    if not anom:
        return anom, None
    touched = [o for o in orbs if o & set(anom)]
    whole = set(anom) == set().union(*[set(o) for o in touched])
    return anom, whole


def run():
    print("=" * 76)
    print("T293 — p=37 Is the Unique Admissible Prime with an Orbit-Aligned")
    print("       Anomalous j=0 Curve")
    print("=" * 76)
    print(f"\n  Admissible set (T292, complete): {ADMISSIBLE}")

    results = {}
    for p in ADMISSIBLE:
        c1, sixth, om = condition_1(p)
        c2, L, M, traces = condition_2(p)
        results[p] = (c1, c2)

        print(f"\n--- p = {p} ---")
        print(f"  CONDITION 1 (orbit inside 6th powers):")
        print(f"    |(F_p*)^6| = {p-1}/gcd(6,{p-1}) = {len(sixth)};  6th powers = {sixth}")
        print(f"    <mult {137%p}> = {om}")
        print(f"    3 | (p-1)/gcd(6,p-1) = {(p-1)//gcd(6,p-1)}  ->  {c1}")

        print(f"  CONDITION 2 (trace 1 attainable):")
        print(f"    4p = {4*p} = {L}^2 + 27*{M}^2 = {L*L} + {27*M*M}")
        print(f"    traces = {traces}  ->  1 present: {c2}")

        emp = verify_traces_match(p)
        print(f"    empirical traces = {emp}  (matches CM: True)")

        const = verify_counts_constant(p, c1)
        print(f"  #E constant on all orbits: {const}")

        anom, whole = verify_anomalous_set(p)
        if anom:
            print(f"  anomalous a-values: {anom};  forms whole orbits: {whole}")
        else:
            print(f"  anomalous a-values: NONE — no anomalous j=0 curve exists at p={p}")

    print("\n" + "=" * 76)
    print(f"  {'p':>4}  {'cond1 orbit<=6th':>18}  {'cond2 trace 1':>15}  {'BOTH':>6}")
    for p in ADMISSIBLE:
        c1, c2 = results[p]
        print(f"  {p:>4}  {str(c1):>18}  {str(c2):>15}  {str(c1 and c2):>6}")

    both = [p for p in ADMISSIBLE if all(results[p])]
    assert both == [37], f"Expected only 37, got {both}"
    print(f"\n  ===> UNIQUE: p = {both[0]}")
    print("  p=7  fails condition 1 — 6th powers are trivial, orbits carry no")
    print("       curve information; #E varies within an orbit.")
    print("  p=73 fails condition 2 — orbit structure is perfect (24 orbits,")
    print("       counts constant, 12 antipodal pairs) but trace 1 is not")
    print("       attainable, so no anomalous curve exists at all.")
    print("\n  The two failures have unrelated causes (6th-power index vs a")
    print("  quadratic-form representation), so the p=37 alignment is not one")
    print("  phenomenon seen twice.")
    print("\nAll T293 assertions passed.")


if __name__ == '__main__':
    run()

"""
T297 — Block Separation: the Curve Results Are Not Corollaries of the Group

The framework's results split into two blocks. Block 1 is self-contained in
F_37* = Z/36Z. Block 2 requires Weierstrass and CM input that Z/36Z does not
supply. This theorem fixes the boundary and gives a falsification test showing
the boundary is real rather than stylistic.

════════════════════════════════════════════════════════════════════════════
BLOCK 1 — derivable from F_37* ≅ Z/36Z alone
════════════════════════════════════════════════════════════════════════════
    2 is a primitive root; log_2 gives F_37* ≅ Z/36Z, and x2^k is +k.
    x26 = 2^12 has order 3; orbits are cosets of <12>, twelve of them.
    x36 = -1 = 2^18 has order 2 (antipodal, T283).
    x27 = 2^6  has order 6 (operator group, T284).
    Subgroups containing mu_3 have order 3d for d | 12 — six of the nine
      subgroups of C_36 (the excluded three have orders 1, 2, 4).   (T286)
    |P^1(F_37)| = 38 = 2 fixed points {0, inf} + 12 cosets x 3.       (T296)
    Antipodal closure = contains the order-2 element = even order.

Everything above follows from "C_36, and 12 | 36". Nothing is special to 37
beyond 37 - 1 = 36.

════════════════════════════════════════════════════════════════════════════
BLOCK 2 — requires input from outside Z/36Z
════════════════════════════════════════════════════════════════════════════
    (a) y^2=x^3+a  ≅  y^2=x^3+a'   iff  a'/a is a sixth power.
        A fact about Weierstrass models. Z/36Z supplies the sixth-power
        subgroup as a lattice element (<27> = H_2) but says nothing about
        it classifying curves.
    (b) 4p = L^2 + 27M^2  determines the six traces {±L, ±(L±9M)/2}.
        Complex multiplication by Z[omega]. Verified against brute-force
        point counts at p = 7,13,31,37,43,61,73.
    (c) The anomalous class exists iff 1 is among those traces.     (T293)

════════════════════════════════════════════════════════════════════════════
THE SEAM, AND WHY IT MISLEADS
════════════════════════════════════════════════════════════════════════════
At p=37 the trace absolute values are {1, 10, 11}, and the sixth-power
subgroup is <11> = {1, 10, 11, 26, 27, 36}. All three traces lie inside it.
That reads as though block 2 were a corollary of block 1.

FALSIFICATION TEST. The framework's admissible set is {7, 37, 73} (T292) —
all three carry the identical block-1 structure. Their trace behaviour:

    p= 7:  |traces| = {1, 4, 5}     inside sixth powers: 1/3
    p=37:  |traces| = {1, 10, 11}   inside sixth powers: 3/3
    p=73:  |traces| = {7, 10, 17}   inside sixth powers: 0/3

Block 1 is identical in kind across all three. Block 2 gives 1/3, 3/3, 0/3.
Reading the p=37 containment as structural predicts containment at p=73.
It fails there completely. The blocks are therefore independent.

════════════════════════════════════════════════════════════════════════════
THE CONTAINMENT RATE IS ELEVATED, BUT FOR A CM REASON
════════════════════════════════════════════════════════════════════════════
Measured over all 1124 primes p = 1 mod 3 below 20000:

    all three traces inside the sixth powers:  89/1124 = 7.92%
      naive expectation (index 6, independent): (1/6)^3 = 0.46%
    per-trace containment:                     945/3372 = 28.0%
      naive expectation:                        1/6     = 16.7%

So the containment is NOT a pure coincidence — it runs ~17x above chance.
Source of the excess, decomposed:
    traces equal to 1:   36/36 inside (100%)  — 1 is always a sixth power,
                         and t=1 occurs exactly for the anomalous primes
    all other traces:   909/3336 inside (27.2%) vs 16.7% naive
    trace residues mod 3: {1: 1712, 2: 1660} — NOT uniform, and never 0
Sixth powers are in particular cubic residues, so a mod-3 constraint on the
traces couples directly to sixth-power membership.

That constraint comes from 4p = L^2 + 27M^2, i.e. from CM. It is a block-2
fact explaining a block-2 observation. It does not make block 2 derivable
from block 1, and the p=73 failure stands regardless.

════════════════════════════════════════════════════════════════════════════
STATEMENT
════════════════════════════════════════════════════════════════════════════
Block 1 is complete, self-contained, and identical in kind at 7, 37, 73.
Block 2 requires CM input, varies across those same three primes, and is
where the framework connects to anything outside itself (GLV, T295).
No result in block 2 may be presented as a corollary of block 1.
"""

from math import isqrt

ADMISSIBLE = [7, 37, 73]


def cm_traces(p):
    """4p = L^2+27M^2 -> the six j=0 traces. Returns (L, M, sorted traces)."""
    M = 1
    while 27 * M * M < 4 * p:
        r = 4 * p - 27 * M * M
        s = isqrt(r)
        if s * s == r:
            L = s
            h1, h2 = (L + 9 * M) // 2, (L - 9 * M) // 2
            return L, M, sorted({L, -L, h1, -h1, h2, -h2})
        M += 1
    raise ValueError(f"no representation for p={p}")


def brute_traces(p):
    tr = set()
    for a in range(1, p):
        n = 1
        for x in range(p):
            r = (x ** 3 + a) % p
            for y in range(p):
                if (y * y) % p == r:
                    n += 1
        tr.add(p + 1 - n)
    return sorted(tr)


def sixth_powers(p):
    return {pow(x, 6, p) for x in range(1, p)}


def sieve(n):
    b = [True] * (n + 1)
    b[0] = b[1] = False
    for i in range(2, isqrt(n) + 1):
        if b[i]:
            for j in range(i * i, n + 1, i):
                b[j] = False
    return [i for i in range(n + 1) if b[i]]


# ─── Block 1: everything follows from C_36 ──────────────────────────────────

def verify_block1():
    dlog = {pow(2, k, 37): k for k in range(36)}
    assert len(dlog) == 36, "2 must be a primitive root"
    assert dlog[26] == 12 and dlog[36] == 18 and dlog[27] == 6
    # orders
    import math
    for mult, order in ((26, 3), (36, 2), (27, 6)):
        assert 36 // math.gcd(dlog[mult], 36) == order
    # subgroups containing mu_3
    divs = [d for d in range(1, 37) if 36 % d == 0]
    assert len(divs) == 9
    contain = [d for d in divs if d % 3 == 0]
    assert contain == [3, 6, 9, 12, 18, 36]
    assert contain == [3 * d for d in divs if 12 % d == 0]
    assert [d for d in divs if d % 3] == [1, 2, 4]
    # P^1
    assert [x for x in range(37) if (26 * x) % 37 == x] == [0]
    assert 37 + 1 == 2 + 12 * 3
    return contain


# ─── Block 2: CM formula, validated ─────────────────────────────────────────

def verify_cm_formula():
    for p in (7, 13, 31, 37, 43, 61, 73):
        _, _, tr = cm_traces(p)
        assert tr == brute_traces(p), f"p={p}: CM != brute force"
    return True


# ─── The falsification test ─────────────────────────────────────────────────

def falsification_test():
    rows = []
    for p in ADMISSIBLE:
        _, _, tr = cm_traces(p)
        ab = sorted({abs(t) for t in tr if t != 0})
        sp = sixth_powers(p)
        inside = [t for t in ab if t in sp]
        rows.append((p, ab, len(inside), len(ab)))
    # p=37 all in, p=73 none in -> not a corollary
    d = {p: (i, n) for p, ab, i, n in rows}
    assert d[37][0] == d[37][1], "p=37 should be 3/3"
    assert d[73][0] == 0, "p=73 should be 0/3"
    return rows


# ─── Rate measurement ───────────────────────────────────────────────────────

def containment_rate(limit=20000):
    ps = [p for p in sieve(limit) if p % 3 == 1]
    joint = tot = 0
    ins_t = tot_t = 0
    one_in = one_n = rest_in = rest_n = 0
    mod3 = {}
    for p in ps:
        _, _, tr = cm_traces(p)
        ab = sorted({abs(t) for t in tr if t != 0})
        sp = sixth_powers(p)
        k = sum(1 for t in ab if t in sp)
        tot += 1
        joint += (k == len(ab))
        ins_t += k
        tot_t += len(ab)
        for t in ab:
            mod3[t % 3] = mod3.get(t % 3, 0) + 1
            if t == 1:
                one_n += 1
                one_in += (1 in sp)
            else:
                rest_n += 1
                rest_in += (t in sp)
    return dict(primes=tot, joint=joint, ins_t=ins_t, tot_t=tot_t,
                one=(one_in, one_n), rest=(rest_in, rest_n), mod3=mod3)


def run():
    print("=" * 74)
    print("T297 — Block Separation: Curve Results Are Not Group Corollaries")
    print("=" * 74)

    contain = verify_block1()
    print("\n--- BLOCK 1: self-contained in F_37* = Z/36Z ---")
    print("  x26 = 2^12 order 3 | x36 = 2^18 order 2 | x27 = 2^6 order 6")
    print(f"  subgroups containing mu_3: orders {contain} = 3d for d | 12")
    print("  six of the nine subgroups of C_36 (excluded: orders 1, 2, 4)")
    print("  |P^1(F_37)| = 38 = 2 fixed + 12 x 3")
    print("  Follows from 'C_36 and 12 | 36'. Nothing special to 37 beyond 36.")

    verify_cm_formula()
    print("\n--- BLOCK 2: needs Weierstrass + CM ---")
    print("  (a) iso iff a'/a is a sixth power     [curve fact, not group fact]")
    print("  (b) 4p = L^2+27M^2 -> six traces      [CM by Z[omega]]")
    print("      validated against brute force at p = 7,13,31,37,43,61,73")
    print("  (c) anomalous class exists iff 1 is a trace   (T293)")

    rows = falsification_test()
    print("\n--- THE FALSIFICATION TEST ---")
    print("  At p=37, |traces| = {1,10,11} all lie in the sixth powers <11>.")
    print("  If that were structural it would hold across the admissible set.")
    print(f"  {'p':>5} {'|traces|':>16} {'inside sixth powers':>22}")
    for p, ab, i, n in rows:
        print(f"  {p:>5} {str(ab):>16} {f'{i}/{n}':>22}")
    print("  Block 1 identical in kind at all three. Block 2 gives 1/3, 3/3, 0/3.")
    print("  The p=73 failure is complete. The blocks are independent.")

    st = containment_rate()
    print("\n--- CONTAINMENT RATE (all p = 1 mod 3 below 20000) ---")
    print(f"  all three traces inside:  {st['joint']}/{st['primes']} = "
          f"{100*st['joint']/st['primes']:.2f}%   (naive (1/6)^3 = 0.46%)")
    print(f"  per-trace containment:    {st['ins_t']}/{st['tot_t']} = "
          f"{100*st['ins_t']/st['tot_t']:.1f}%   (naive 1/6 = 16.7%)")
    print("  Elevated ~17x above chance, so not a pure coincidence. Source:")
    oi, on = st['one']
    ri, rn = st['rest']
    print(f"    traces equal to 1: {oi}/{on} inside (100%) — 1 is always a")
    print(f"      sixth power, and t=1 marks exactly the anomalous primes")
    print(f"    all other traces:  {ri}/{rn} inside ({100*ri/rn:.1f}%)")
    print(f"    trace residues mod 3: {dict(sorted(st['mod3'].items()))} — never 0")
    print("  Sixth powers are cubic residues, so the mod-3 constraint on")
    print("  traces couples to sixth-power membership. That constraint comes")
    print("  from 4p = L^2+27M^2 — a block-2 fact explaining a block-2")
    print("  observation. It does not make block 2 follow from block 1.")

    print("\n" + "=" * 74)
    print("  Block 1: complete, self-contained, identical at 7, 37, 73.")
    print("  Block 2: needs CM, varies across those primes, and is where the")
    print("           framework connects outward (GLV / secp256k1, T295).")
    print("  No block-2 result may be presented as a corollary of block 1.")
    print("=" * 74)
    print("\nAll T297 assertions passed.")


if __name__ == '__main__':
    run()

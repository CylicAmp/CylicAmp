# CLASS: THEOREM
"""
Theorem 337: the Sophie Germain map is multiplication by 2 in shifted
coordinates, twelve of its steps equal one 137-step plus 25 -- and the
primes see none of it
Author: Michael Warren Song (CyclicAmp)

T336 closed the twin-prime direction: the +2 gap is additive, the orbits are
multiplicative, and T329's CRT independence predicted the null in advance.
The Sophie Germain map p -> 2p+1 is the case that direction could NOT
settle, because it is multiplicative in disguise.  It is settled here.

=== SIGMA IS MULTIPLICATION BY 2 ===

    sigma(x) = 2x + 1 on GF(37).  Its fixed point is x = -1 = 36, in NEG_H.
    Shift to y = x + 1:

        sigma(x) + 1 = 2x + 2 = 2(x + 1)     i.e.   y -> 2y

    So sigma is conjugate to multiplication by 2 -- exactly, not loosely.
    And 2 is a primitive root mod 37 (ord = 36, already in CLAUDE.md), so
    sigma is a SINGLE 36-CYCLE on the 36 points other than its fixed point.
    A Sophie Germain chain p -> 2p+1 -> 4p+3 -> ... is a walk along
    consecutive powers of the generator.

=== TWELVE SG STEPS = ONE 137-STEP, PLUS 25 ===

    26 = 2^12, so the 137-multiplier is the 12th power of the generator, and
    ord(26) = 36/gcd(12,36) = 3, which is where the 3-cycles come from.
    Pushing the conjugation through:

        sigma^12(x) = 26x + 25          exact, verified for all x

    So twelve Sophie Germain steps are one 137-map step followed by a shift
    of 25 -- and 25 is a sovereign ANCHOR.  sigma^36 = identity.

    This is the bridge T336 could not build for twins: the SG map and the
    137-map are powers of the same generator, differing only by that shift.

=== BUT THE SHIFT MATTERS: THE TWO TRIPLE SYSTEMS AGREE ON NOTHING ===

    sigma^12 has multiplier 26 of order 3, so it cuts 36 points into 12
    triples, exactly as the 137-map does.  They are not the same 12.

    The systems partition DIFFERENT 36-sets: sigma fixes 36 and moves 0,
    while the 137-map fixes 0 and moves 36.  So at most 11 triples could
    ever coincide.  The number that do is ZERO.

        sigma^12 triple      137-orbits of its members
        [0, 9, 25]           SEAM, SA_ST_A, SA_ST_B
        [1, 14, 19]          IC, C9, CAS_EXT
        [10, 26, 35]         IC, IC, NQR17      <- the only repeat
        ... (12 in all, none equal to a 137-orbit)

    The additive 25 is the whole obstruction.  Conjugate maps with different
    fixed points generate different orbit systems on the same points.

=== THE SEAM TRIPLE, GRADED ===

    sigma^12 through the seam gives {0, 25, 9}: the seam plus TWO of the
    four sovereign anchors {4, 9, 25, 30}.

        selectivity     (4/36)(3/35) = 1/105,  6.71 bits
        sample size     n = 1
        pre-registered  NO -- read off after the triples were computed

    Suggestive, NOT established.  The triple is forced once sigma is, so
    this is one draw, not a pattern.  Recorded at that grade.

=== THE PRIMES SEE NONE OF IT ===

    Pre-registered before the sieve: admissible residues are p != 0 and
    2p+1 != 0 (i.e. p != 18), 35 of 37, giving SEED two admissible members
    instead of three.  MISS if chi-square over the 12 orbits is
    insignificant at alpha = 0.01 (df 11, crit 24.72).

    RESULT: 56,031 Sophie Germain primes p < 10^7.  chi-square = 5.60.
    MISS.  Every per-orbit ratio within 1.7% of 1.

    So the map carries real structure and the primes carry none of it.
    Unlike T336, this null is MEASURED rather than predicted: T329's
    independence does not cover it, precisely because sigma is
    multiplicative in shifted coordinates.  The reason is ordinary --
    Dirichlet / prime k-tuples equidistribution -- not the CRT argument.

=== FALSIFICATION ===
    sigma^12(x) != 26x + 25 for some x; a coincidence between the two
    triple systems; or a Sophie Germain orbit statistic beating 24.72.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY = {r: n for n, o in ORBITS.items() for r in o}
ANCHORS = {4, 9, 25, 30}


def orbit_of(n):
    return 'SEAM' if n % P == 0 else BY[n % P]


def sigma(x, k=1):
    return (pow(2, k, P) * (x + 1) - 1) % P


def sophie_germain(N):
    s = bytearray([1]) * (2 * N + 3)
    s[0:2] = b'\0\0'
    for i in range(2, int((2 * N + 2) ** .5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [p for p in range(3, N) if s[p] and s[2 * p + 1]]


def run():
    import math
    from collections import Counter

    # --- sigma is multiplication by 2 in y = x+1 ---
    for x in range(P):
        assert (2 * x + 1) % P == sigma(x)
        assert (sigma(x) + 1) % P == (2 * (x + 1)) % P
    assert sigma(36) == 36 and orbit_of(36) == 'NEG_H'       # fixed point
    assert pow(2, 36, P) == 1 and all(pow(2, k, P) != 1 for k in range(1, 36))
    cyc, x = 0, 0
    while True:
        x = sigma(x)
        cyc += 1
        if x == 0:
            break
    assert cyc == 36                                          # a single 36-cycle

    # --- sigma^12 = the 137-map plus 25 ---
    k = next(k for k in range(1, 37) if pow(2, k, P) == 26)
    assert k == 12 and 36 // math.gcd(12, 36) == 3
    for x in range(P):
        assert sigma(x, 12) == (26 * x + 25) % P
        assert sigma(x, 36) == x
    assert 25 in ANCHORS

    # --- the two triple systems agree on nothing ---
    sg12 = sorted({frozenset({x, sigma(x, 12), sigma(x, 24)})
                   for x in range(P) if x != 36}, key=lambda s: min(s))
    assert len(sg12) == 12 and all(len(t) == 3 for t in sg12)
    orb137 = {frozenset(v) for v in ORBITS.values()}
    assert len(orb137) == 12
    eligible = [t for t in sg12 if 0 not in t]
    assert len(eligible) == 11                       # at most 11 could match
    assert [t for t in sg12 if t in orb137] == []    # none do
    # the systems partition different 36-sets
    assert sigma(36) == 36 and (26 * 0) % P == 0
    assert 0 in set().union(*sg12) and 0 not in set().union(*orb137)
    assert 36 in set().union(*orb137)

    # --- the seam triple, and its grade ---
    seam = next(t for t in sg12 if 0 in t)
    assert seam == frozenset({0, 9, 25})
    assert (seam - {0}) <= ANCHORS and len(seam - {0}) == 2
    assert abs(math.log2(1 / ((4 / 36) * (3 / 35))) - 6.71) < 0.02
    # exactly one triple has two members sharing a 137-orbit
    rep = [t for t in sg12
           if len({orbit_of(v) for v in t}) < 3 and 0 not in t]
    assert rep == [frozenset({10, 26, 35})]

    # --- the primes: pre-registered null ---
    adm = [r for r in range(P) if r % P and (2 * r + 1) % P]
    assert len(adm) == 35 and 18 not in adm and 0 not in adm
    w = Counter(BY[r] for r in adm)
    assert w['SEED'] == 2 and all(w[o] == 3 for o in ORBITS if o != 'SEED')
    sg = sophie_germain(10 ** 7)
    n = len(sg)
    assert n == 56031, n
    c = Counter(BY[p % P] for p in sg)
    chi = sum((c[o] - n * w[o] / 35) ** 2 / (n * w[o] / 35) for o in ORBITS)
    assert chi < 24.72, chi                                   # MISS
    for o in ORBITS:
        assert abs(c[o] / (n * w[o] / 35) - 1) < 0.02, o

    print("All assertions passed.\n")
    print("THEOREM 337.  sigma(x) = 2x+1 is multiplication by 2.\n")
    print("   y = x+1  =>  sigma: y -> 2y.   fixed point x = -1 = 36 (NEG_H)")
    print("   ord_37(2) = 36, a primitive root, so sigma is ONE 36-cycle.")
    print("   an SG chain walks consecutive powers of the generator.\n")
    print(f"   26 = 2^{k}, ord(26) = 3, and pushing the conjugation through:")
    print( "       sigma^12(x) = 26x + 25       exact, all x")
    print( "   TWELVE SG STEPS = ONE 137-STEP PLUS 25, a sovereign anchor.")
    print( "   sigma^36 = identity.\n")
    print("  BUT THE TWO TRIPLE SYSTEMS AGREE ON NOTHING")
    print( "   sigma fixes 36 and moves 0; the 137-map fixes 0 and moves 36,")
    print(f"   so at most {len(eligible)} triples could coincide.  Zero do.\n")
    print("    sigma^12 triple     137-orbits of its members")
    for t in sg12:
        print(f"    {str(sorted(t)):15s}  {[orbit_of(v) for v in sorted(t)]}")
    print("\n   the additive 25 is the whole obstruction: conjugate maps with")
    print("   different fixed points generate different orbit systems.\n")
    print("  THE SEAM TRIPLE, GRADED")
    print(f"   {sorted(seam)} -- the seam plus two of the four anchors"
          f" {sorted(ANCHORS)}")
    print(f"   selectivity (4/36)(3/35) = 1/105 = {math.log2(105):.2f} bits,"
          f" n = 1, not pre-registered")
    print( "   SUGGESTIVE, NOT ESTABLISHED -- the triple is forced, one draw.\n")
    print("  THE PRIMES SEE NONE OF IT  (pre-registered, alpha = 0.01)")
    print(f"   {n:,} Sophie Germain primes p < 10^7")
    print(f"   chi-square {chi:.2f} on df 11 against 24.72   MISS")
    print( "    orbit      count   expected   ratio")
    for o in ORBITS:
        e = n * w[o] / 35
        print(f"     {o:9s} {c[o]:6d} {e:10.1f}   {c[o]/e:.4f}")
    print("\n   the map carries structure; the primes carry none of it.")
    print("   Unlike T336 this null is MEASURED, not predicted -- T329's")
    print("   independence does not cover a map that is multiplicative in")
    print("   shifted coordinates.  The reason is ordinary equidistribution.")


if __name__ == "__main__":
    run()

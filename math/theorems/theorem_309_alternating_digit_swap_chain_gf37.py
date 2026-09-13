# CLASS: COMPUTATION
"""
Theorem 309: The alternating-digit-swap chain is period-6 mod 37 by a
rendering mechanism, for every digit pair -- screened, and correctly
downgraded, by miss-test and forced-check
Author: Michael Warren Song (CyclicAmp)

THE CONSTRUCTION
    term_k = 10^k + digit_swap(term_{k-1}), seeded term_3 = "aba" for a
    digit pair (a,b), a in 1..9, b in 0..9, a != b, where digit_swap
    exchanges every occurrence of a and b in the decimal string. Because
    every term stays built from exactly the two digits {a,b}, digit_swap
    never becomes undefined -- unlike the general reversal-build chain
    (digit-protocols protocol 9, theorem_308) which usually breaks after
    1-2 steps once a third digit appears. For (a,b)=(1,9) this is exactly
    the sequence the user wrote by hand: 191, 1919, 19191, 191919, ...

MISS-TEST (run BEFORE the full sweep, via .claude/skills/miss-test)
    Claim: eventually periodic mod 37 with period exactly 6, for every
    (a,b) pair. Miss condition: any pair giving a period other than 6,
    a nonzero transient, or no period within bounds (transient<=10,
    period<=15).
    HONESTY NOTE: the (a,b)=(1,9) instance was seen FIRST (it is what the
    user wrote out), so that single case is not a blind trial. The other
    80 pairs were genuinely untested when the miss condition was declared
    -- they are the real out-of-sample test. Result: 0 misses in all 81
    pairs (including the seed pair). See run() for the sweep.

FORCED-CHECK VERDICT: RENDERING, not new structure
    .claude/skills/forced-check's own `digits` audit on 191919 shows the
    general mechanism directly: a period-2 digit alternation of EVEN
    length has a DFT supported only at the DC and Nyquist bins (all other
    frequencies exactly zero) -- FORCED by the arrangement, not the
    values. Combined with ord_37(10) = 3 (theorem_265, theorem_303,
    theorem_308), which is the known fact that only 37 (among primes
    dividing 999 = 3^3 x 37) has ord_p(10) = 3, the period-2 digit shape
    interacting with a period-3 power-of-10 cycle forces every period to
    divide lcm(2,3) = 6.
    Per forced-check's own rule ("a digit fact must survive a digit
    substitution... the conclusion is about the arrangement, not the
    value"): this DOES survive substitution -- all 81 (a,b) pairs behave
    identically (period exactly 6, zero transient) -- which by that same
    rule means the period-6 result is a RENDERING fact about the
    alternating-pair SHAPE, not new information about 37 beyond the
    already-established ord_37(10)=3. It is recorded here as a verified,
    exhaustively-checked corollary, not oversold as a new mechanism.
    Tier: does not fit forced-check's three canonical tiers (mu_3-orbit
    facts / Phi_3(137) facts / n^2+1 CM facts) -- it is a distinct,
    already-catalogued ord_p(10)=3 fact, unique to 37 among primes
    dividing 999 (verified: ord_7(10)=6, ord_73(10)=/=3 since
    10^3 mod 73 = 51).

WHAT IS NOT FORCED: which orbits the (1,9) cycle actually touches
    Which specific residues appear in a given pair's period-6 cycle is
    ordinary arithmetic on that pair's actual digit values, not forced by
    the arrangement. For (1,9), starting from term_3=191:
        6(TESLA) -> 32(SEED) -> 25(SA_ST_B) -> 0(SEAM) -> 1(IC) -> 19(CAS_EXT) -> (repeats)
    "the cycle touches SEED" is not by itself notable -- every non-SEAM
    residue is in some orbit (partition is complete, forced-check's own
    first vacuous pattern), so touching *some* orbit is guaranteed; only
    a claim about *which* orbit, checked against a null, would carry
    information.

OPEN, UNEXPLAINED OBSERVATION (recorded, not claimed)
    Pooling which orbits appear across all 81 pairs' period-6 cycles and
    chi-squaring against uniform gives chi^2/df = 7.73 (n=467, 11 df) --
    a real deviation from uniform (SA_ST_B and C9 overrepresented,
    SA_ST_A and CAS_EXT underrepresented). Per miss-test's own caution,
    this is NOT claimed as structure: the (a,b) sample itself is
    asymmetric (a in 1..9, b in 0..9, so a=0 is excluded but b=0 is not),
    and the map is a fixed deterministic arithmetic function, not a
    random draw, so nonuniformity over an artificial 81-point domain is
    not automatically meaningful. Left open.

FALSIFICATION
    Any assert below failing.
"""

from collections import Counter

P = 37
ORBITS = {
    'IC': {1, 10, 26}, 'DARK_A': {2, 15, 20}, 'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23}, 'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36}, 'C9': {14, 29, 31},
    'NQR17': {17, 22, 35}, 'SEED': {18, 24, 32}, 'SA_ST_B': {21, 25, 28},
}


def orbit_of(r):
    if r == 0:
        return 'SEAM'
    for name, s in ORBITS.items():
        if r in s:
            return name
    raise AssertionError(r)


def digit_swap_pair(n, a, b):
    return int(str(n).translate(str.maketrans(a + b, b + a)))


def build_chain(a, b, n_steps=6):
    """a,b are single-char digit strings. Returns residues mod 37 for k=3..3+n_steps-1."""
    prior = int(f"{a}{b}{a}")
    residues = [prior % P]
    for k in range(4, 3 + n_steps):
        s = digit_swap_pair(prior, a, b)
        prior = 10 ** (k - 1) + s
        residues.append(prior % P)
    return residues


def eventual_period(residues, max_period=15):
    for p in range(1, max_period + 1):
        if all(residues[i] == residues[i + p] for i in range(len(residues) - p)):
            return p
    return None


def run():
    assert pow(10, 3, P) == 1                       # ord_37(10) = 3
    assert pow(10, 3, 7) != 1 and pow(10, 3, 73) != 1  # unique to 37 among {7,37,73}

    all_pairs = [(a, b) for a in range(1, 10) for b in range(0, 10) if a != b]
    assert len(all_pairs) == 81

    periods = {}
    orbit_hits = Counter()
    for a, b in all_pairs:
        residues = build_chain(str(a), str(b), n_steps=12)
        p = eventual_period(residues)
        assert p == 6, f"(a,b)=({a},{b}) gave period {p}, expected 6"
        periods[(a, b)] = p
        for r in set(residues[:6]):
            orbit_hits[orbit_of(r)] += 1

    assert all(p == 6 for p in periods.values())
    assert len(periods) == 81

    # the (1,9) worked example -- exactly what the user wrote by hand
    # (starts at term_3=191; the cycle is the same rotation reported in the
    # docstring, which starts its listing at term_4=1919=32=SEED instead)
    cyc_19 = build_chain("1", "9", n_steps=6)
    assert cyc_19 == [6, 32, 25, 0, 1, 19]
    assert [orbit_of(r) for r in cyc_19] == \
        ['TESLA', 'SEED', 'SA_ST_B', 'SEAM', 'IC', 'CAS_EXT']

    # chi-square of pooled orbit-hit counts against uniform over the 12 named orbits
    named = {k: v for k, v in orbit_hits.items() if k != 'SEAM'}
    n = sum(named.values())
    expected = n / 12
    chi2 = sum((c - expected) ** 2 / expected for c in named.values())
    df = 11
    assert len(named) == 12
    assert n == 467
    assert abs(chi2 - 84.97) < 0.1
    ratio = chi2 / df

    print("All assertions passed.\n")
    print(f"81/81 (a,b) pairs give eventual period exactly 6, zero transient\n")
    print(f"Worked example (a,b)=(1,9):")
    for k, r in enumerate(cyc_19, start=3):
        print(f"  term_{k} mod 37 = {r:2d}  orbit={orbit_of(r)}")
    print()
    print(f"Pooled orbit-hit counts across all 81 pairs' period-6 cycles:")
    for name in sorted(named, key=lambda x: -named[x]):
        print(f"  {name:<9} {named[name]:3d}")
    print(f"SEAM hits: {orbit_hits['SEAM']}")
    print(f"\nchi^2 = {chi2:.2f}, df={df}, chi^2/df = {ratio:.3f}"
          f"  (deviates from uniform; mechanism NOT identified, left open)")


if __name__ == "__main__":
    run()

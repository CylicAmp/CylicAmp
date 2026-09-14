# CLASS: THEOREM
"""
Theorem 316: the pipeline's T120/121 gate is exactly the class 246 mod 333,
and 8 of CLAUDE.md's 16 reference values are seed-independent
Author: Michael Warren Song (CyclicAmp)

=== THE RESULT ===

    A sweep of cylicamp/engine_integration.py over seeds 1..1110 (30 full
    cycles mod 37) separates the reference block in CLAUDE.md into three
    tiers:

    TIER 1 -- CONSTANT for every seed (8 of 16 fields). These carry ZERO
    information about seed 246:

        multiplier = 8          field_threshold = 0.95
        insight_score = 104832  spectrum_status = FAIL
        stability_ratio = 0.0   g5 all_checks_pass = False
        g5 aggregate_mod_p = 11 cage integrity = FAIL

    They are regression checks -- a code change moves them -- but they say
    nothing about which seed was supplied.

    TIER 2 -- pure functions of seed mod 37 (or mod 9). Properties of the
    RESIDUE CLASS, not of 246. All 30 swept seeds = 24 (mod 37) give
    byte-identical values:

        seed_mod37, seed_sovereign, cascade_orbit_hits_count,
        sovereign_status, abcabc_orbit_position, orbit_all_nonqr,
        seed_orbit, heartbeat_3cycle       (all mod 37)
        seed_dr                            (mod 9)

    TIER 3 -- the only field where 246 is rare:

        t120_t121 all-true: 3 of 1110 seeds (0.27%), and a function of
        NEITHER mod 37 alone NOR mod 9 alone.

    The three are 246, 579, 912 -- an arithmetic progression of common
    difference 333 = 9 x 37 = lcm(9, 37).

        T120/121 passes  <=>  seed = 246 (mod 333)

=== MECHANISM -- derived, and the five checks reduce to two ===

    m1 = 7, m2 = 8, s = 3 are CONSTANTS (theorem_120_digit_algebra_007_008),
    not seed-dependent. So the five checks are:

      1. s_eq_seed_dr              3 == dr(seed)        -> seed = 3 (mod 9)
      2. m2_times_s_eq_seed_mod37  8*3 = 24 == seed%37  -> seed = 24 (mod 37)
      3. orbit_18_check            7+8+3 = 18 in orbit  -> IMPLIED by 2
      4. orbit_32_check            8*(3+1) = 32 in orbit-> IMPLIED by 2
      5. dr_matches_t120           dr(24) == dr(15) = 6 -> IMPLIED by 2

    Checks 3, 4 and 5 are forced once check 2 fixes the residue: the
    137-orbit of 24 is {18, 24, 32}, which contains both 18 and 32, and
    dr(24) = 6 = dr(15) is arithmetic on the residue alone.

    So "all five pass" is really TWO independent conditions. gcd(9,37) = 1,
    so by CRT their intersection is a single class modulo 9 x 37 = 333, and
    246 is in it (246 = 3 mod 9, 246 = 24 mod 37).

    This is why Tier 3 is a function of neither modulus alone -- it needs
    both.

=== WHY 333 ===

    333 = 9 x 37 is forced here as lcm(9, 37): the digital root lives mod 9
    and the field lives mod 37, and the gate constrains one of each.

    Recorded, NOT claimed as a second occurrence: 333 is also T311's
    sub-grid forward difference (333 = 37 x 9). Same factorisation, and in
    both places it arises as "the 9 and the 37 together". That is one fact
    about 9 x 37, not two independent sightings of 333.

=== VERIFIED PREDICTION ===

    Stated before testing, then checked outside the swept range:
      - 7 of 7 seeds 246 + k*333 for k = 3..9 pass
      - 10 of 10 near-misses (+-1, +-9, +-37 off the class) fail
      - exhaustive over 1111..2220: the actual pass set equals the
        predicted set exactly, {1245, 1578, 1911}

=== WHAT THIS MEANS FOR THE REFERENCE BLOCK ===

    Of 16 documented reference values, 8 are seed-independent and 7 are
    residue-class properties shared by 1 seed in 37. Exactly one field
    distinguishes 246 from its own residue class, and that field is
    satisfied by 1 seed in 333 -- every one of which reproduces the entire
    reference block identically.

    Seed 246 is therefore not unique in anything the pipeline reports. It
    is the smallest member of the class 246 mod 333. This is recorded so
    the reference block is read as a regression fixture, which it is, and
    not as evidence that 246 is distinguished, which it is not.

=== FALSIFICATION ===
    Any assert below failing. In particular: a seed = 246 (mod 333) that
    fails the T120/121 gate, or a seed outside that class that passes.
"""

P = 37
M1, M2, S = 7, 8, 3          # from theorem_120_digit_algebra_007_008
MOD = 333                    # 9 * 37


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def orbit_triple(x):
    x %= P
    return {x, 26 * x % P, 26 * 26 * x % P}


def t120_gate(seed):
    """The five checks as the pipeline computes them."""
    m37 = seed % P
    orb = orbit_triple(seed)
    return {
        "s_eq_seed_dr": S == dr(seed),
        "m2_times_s_eq_seed_mod37": M2 * S == m37,
        "orbit_18_check": M1 + M2 + S in orb,
        "orbit_32_check": M2 * (S + 1) in orb,
        "dr_matches_t120": dr(m37) == dr(M1 + M2),
    }


def run():
    # --- the constants are constants ---
    assert (M1, M2, S) == (7, 8, 3)
    assert M2 * S == 24 and M1 + M2 + S == 18 and M2 * (S + 1) == 32
    assert dr(M1 + M2) == dr(15) == 6

    # --- checks 3,4,5 are implied by check 2 ---
    for seed in range(1, 4000):
        g = t120_gate(seed)
        if g["m2_times_s_eq_seed_mod37"]:
            assert g["orbit_18_check"], seed
            assert g["orbit_32_check"], seed
            assert g["dr_matches_t120"], seed
    assert orbit_triple(24) == {18, 24, 32}
    assert 18 in orbit_triple(24) and 32 in orbit_triple(24)
    assert dr(24) == 6

    # --- so the gate is exactly two conditions ---
    for seed in range(1, 4000):
        g = t120_gate(seed)
        allfive = all(g.values())
        two = (dr(seed) == S) and (seed % P == M2 * S)
        assert allfive == two, seed

    # --- and those two are seed = 3 (mod 9) and seed = 24 (mod 37) ---
    for seed in range(1, 4000):
        assert (dr(seed) == 3) == (seed % 9 == 3), seed
    # CRT: intersection is one class mod 333
    passers = [n for n in range(1, 4000) if all(t120_gate(n).values())]
    assert passers == [n for n in range(1, 4000) if n % MOD == 246 % MOD]
    assert 246 % MOD == 246
    assert MOD == 9 * P == 333
    import math
    assert math.gcd(9, P) == 1 and math.lcm(9, P) == MOD

    # --- the three in the swept range, step 333 ---
    in1110 = [n for n in range(1, 1111) if all(t120_gate(n).values())]
    assert in1110 == [246, 579, 912]
    assert [in1110[i + 1] - in1110[i] for i in (0, 1)] == [333, 333]
    assert all(n % P == 24 and dr(n) == 3 for n in in1110)

    # --- the prediction that was checked against the live pipeline ---
    assert all(all(t120_gate(246 + k * MOD).values()) for k in range(0, 12))
    for off in (1, -1, 9, -9, 37, -37):
        assert not all(t120_gate(246 + off).values()), off
    assert [n for n in range(1111, 2221) if all(t120_gate(n).values())] \
        == [1245, 1578, 1911]

    # --- density ---
    dens = len([n for n in range(1, 3331) if all(t120_gate(n).values())])
    assert dens == 10                      # 3330 / 333

    print("All assertions passed.\n")
    print("THE GATE, REDUCED")
    print(f"  m1={M1} m2={M2} s={S} are constants, not seed-dependent")
    print(f"    1. s == dr(seed)          -> dr(seed) = {S}  <=> seed = 3 (mod 9)")
    print(f"    2. m2*s == seed%37        -> seed = {M2*S} (mod 37)")
    print(f"    3. m1+m2+s = {M1+M2+S} in orbit    -> IMPLIED by 2")
    print(f"    4. m2*(s+1) = {M2*(S+1)} in orbit  -> IMPLIED by 2")
    print(f"    5. dr(seed%37) == dr(m1+m2) -> IMPLIED by 2")
    print(f"  orbit(24) = {sorted(orbit_triple(24))}, contains 18 and 32")
    print(f"  so five checks = two conditions, on coprime moduli 9 and 37\n")
    print("THE CLASS")
    print(f"  CRT -> one class mod lcm(9,37) = {MOD}")
    print(f"  passers in 1..1110: {in1110}   step "
          f"{in1110[1]-in1110[0]}")
    print(f"  passers in 1111..2220: "
          f"{[n for n in range(1111,2221) if all(t120_gate(n).values())]}")
    print(f"  density: 1 seed in {MOD}\n")
    print("READ THE REFERENCE BLOCK ACCORDINGLY")
    print("  8 of 16 documented values are seed-INDEPENDENT (constant)")
    print("  7 are functions of seed mod 37 (or mod 9) -- residue-class facts")
    print("  1 (the T120/121 gate) distinguishes 246 from its residue class,")
    print("  and is shared by every seed = 246 (mod 333).")
    print("  246 is the smallest member of that class, not a unique seed.")


if __name__ == "__main__":
    run()

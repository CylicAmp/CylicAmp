"""
THEOREM 117 — Discrete Logarithm Base 2 and the 137-Map in GF(37)

Since ord₃₇(2) = 36, every non-zero residue a mod 37 can be written
uniquely as 2^k for k ∈ {1, 2, …, 36} (with 2^36 ≡ 1 playing the role
of the identity).

COMPLETE POWER TABLE (step-by-step, each row = 2×previous mod 37)

  k   2^k mod 37  |  k   2^k mod 37  |  k   2^k mod 37
  1      2        | 13     15        | 25     20
  2      4        | 14     30        | 26      3
  3      8        | 15     23        | 27      6
  4     16        | 16      9        | 28     12
  5     32        | 17     18        | 29     24
  6     27        | 18     36 ≡ -1   | 30     11
  7     17        | 19     35        | 31     22
  8     34        | 20     33        | 32      7
  9     31        | 21     29        | 33     14
 10     25        | 22     21        | 34     28
 11     13        | 23      5        | 35     19
 12     26        | 24     10        | 36      1

This gives the discrete logarithm: dlog₂(a) = k  iff  2^k ≡ a (mod 37).

CORE THEOREM — THE 137-MAP IS A SHIFT BY 12 IN LOG-SPACE

  26 ≡ 2^12 (mod 37).

  For any a, write a = 2^k. Then:
      f(a) = 26a ≡ 2^12 · 2^k = 2^(k+12)  (mod 37, exponent mod 36).

  The 137-map f(a) = 26a in GF(37) corresponds to  k ↦ k+12  in ℤ/36ℤ.

COROLLARY — EVERY ORBIT HAS ARITHMETIC-PROGRESSION DISCRETE LOGS

  Every 137-map orbit {a, f(a), f²(a)} = {2^k, 2^(k+12), 2^(k+24)} for
  some k. The discrete logs {k, k+12, k+24} form an arithmetic progression
  with common difference 12 in ℤ/36ℤ. This holds for all 12 orbits.

THE 12 ORBITS AND THEIR DISCRETE LOGS

  Orbit               Discrete logs (sorted)  Named class
  {1, 10, 26}         {12, 24, 36}            IC
  {2, 15, 20}         { 1, 13, 25}            —
  {3, 4, 30}          { 2, 14, 26}            —  (contains SA∩ST = 30)
  {5, 13, 19}         {11, 23, 35}            —  (CB element 13 here)
  {6, 8, 23}          { 3, 15, 27}            —  (CB element 8 here)
  {7, 33, 34}         { 8, 20, 32}            D7
  {9, 12, 16}         { 4, 16, 28}            —
  {11, 27, 36}        { 6, 18, 30}            ORBIT_11
  {14, 29, 31}        { 9, 21, 33}            —
  {17, 22, 35}        { 7, 19, 31}            BASIN_Y
  {18, 24, 32}        { 5, 17, 29}            SEED_ORBIT
  {21, 25, 28}        {10, 22, 34}            —

  Minimum exponents: {1,2,3,4,5,6,7,8,9,10,11,12} — one per orbit.
  The 12 orbits partition the 36 exponents into 12 cosets of ⟨12⟩={0,12,24}
  in ℤ/36ℤ (writing 36 as 0 for the identity element).

HALFWAY SYMMETRY
  2^18 ≡ 36 ≡ -1 (mod 37).
  Therefore 2^(k+18) ≡ -2^k (mod 37) for all k.
  The power sequence is negation-symmetric at the midpoint k=18.

CB = {8, 13, 24} IS NOT A SINGLE ORBIT
  8 ∈ orbit {6,8,23},  13 ∈ orbit {5,13,19},  24 ∈ orbit {18,24,32}.
  The discrete logs of CB are {3,11,29}: differences {8,18,10} — not step 12.
  CB is a cross-orbit selection: one element from each of three distinct orbits.
"""

P = 37

POWER_TABLE = {
     1:  2,   2:  4,   3:  8,   4: 16,   5: 32,   6: 27,
     7: 17,   8: 34,   9: 31,  10: 25,  11: 13,  12: 26,
    13: 15,  14: 30,  15: 23,  16:  9,  17: 18,  18: 36,
    19: 35,  20: 33,  21: 29,  22: 21,  23:  5,  24: 10,
    25: 20,  26:  3,  27:  6,  28: 12,  29: 24,  30: 11,
    31: 22,  32:  7,  33: 14,  34: 28,  35: 19,  36:  1,
}

IC         = {1, 10, 26}
SA         = {4, 9, 25, 30}
ST         = {3, 12, 21, 30}
CB         = {8, 13, 24}
ORBIT_11   = {11, 27, 36}
SEED_ORBIT = {18, 24, 32}
BASIN_Y    = {17, 22, 35}
D7         = {7, 33, 34}


def run():
    print("=" * 66)
    print("THEOREM 117 — DISCRETE LOGARITHM BASE 2 AND THE 137-MAP IN GF(37)")
    print("=" * 66)

    # ---------------------------------------------------------------
    # PART 1 — Verify all 36 powers of 2
    # ---------------------------------------------------------------
    print("\n--- Part 1: Verify all 36 powers of 2 mod 37 ---")
    for k, expected in POWER_TABLE.items():
        actual = pow(2, k, P)
        assert actual == expected, f"2^{k} = {actual}, expected {expected}"
    assert len(set(POWER_TABLE.values())) == 36   # hits every residue
    assert POWER_TABLE[36] == 1                    # returns to identity
    print("  All 36 powers verified.  2 is confirmed as primitive root mod 37.")
    print(f"  2^12 = {POWER_TABLE[12]}  (the 137-map multiplier)")
    print(f"  2^18 = {POWER_TABLE[18]} = -1 mod 37  (halfway: negation symmetry)")
    print(f"  2^36 = {POWER_TABLE[36]}  (identity)")

    # Build discrete log table
    dlog = {v: k for k, v in POWER_TABLE.items()}

    # ---------------------------------------------------------------
    # PART 2 — 137-map is shift by 12 in log-space
    # ---------------------------------------------------------------
    print("\n--- Part 2: 137-map f(a)=26a is shift +12 in discrete log ---")
    assert dlog[26] == 12, "26 = 2^12"
    f = lambda n: (26 * n) % P

    for a in range(1, P):
        k      = dlog[a]
        fa     = f(a)
        k_fa   = dlog[fa]
        assert k_fa == (k + 12) % 36 or (k_fa == 36 and (k + 12) % 36 == 0), \
            f"dlog(f({a})) = {k_fa}, expected ({k}+12) mod 36 = {(k+12)%36}"
    print("  For every a in (ℤ/37ℤ)×:  dlog₂(26a) ≡ dlog₂(a) + 12  (mod 36)  ✓")
    print("  The 137-map is a cyclic shift of order 3 in exponent space.")

    # ---------------------------------------------------------------
    # PART 3 — Every orbit has AP discrete logs with step 12
    # ---------------------------------------------------------------
    print("\n--- Part 3: All 12 orbits have discrete logs forming AP step 12 ---")
    seen, orbits = set(), []
    for start in range(1, P):
        if start not in seen:
            orb, n = [], start
            for _ in range(3):
                orb.append(n); n = f(n)
            assert n == start, "orbit does not close"
            orbits.append(sorted(orb))
            seen.update(orb)

    assert len(orbits) == 12
    min_exps = []
    for orb in sorted(orbits):
        logs = sorted(dlog[g] for g in orb)
        diffs = [(logs[1]-logs[0]) % 36,
                 (logs[2]-logs[1]) % 36,
                 (logs[0]-logs[2] + 36) % 36]
        assert all(d == 12 for d in diffs), f"Orbit {orb} not AP step 12: {diffs}"
        min_exps.append(logs[0])

    assert sorted(min_exps) == list(range(1, 13)), \
        "Minimum exponents must be {1,...,12}"
    print(f"  All 12 orbits confirmed: discrete logs form AP with step 12.  ✓")
    print(f"  Minimum exponents of orbits: {sorted(min_exps)}")
    print(f"  = {{1,...,12}}: one coset representative of ⟨12⟩ in ℤ/36ℤ per orbit.")

    # Print the orbit table
    print()
    named_lookup = {}
    for nm, cls in [('IC',IC),('D7',D7),('ORBIT_11',ORBIT_11),
                    ('SEED_ORBIT',SEED_ORBIT),('BASIN_Y',BASIN_Y)]:
        for g in cls:
            named_lookup[g] = nm

    for orb in sorted(orbits):
        logs = sorted(dlog[g] for g in orb)
        tag  = named_lookup.get(orb[0], named_lookup.get(orb[1],
               named_lookup.get(orb[2], '—')))
        print(f"    {str(orb):<18}  dlogs={logs}  [{tag}]")

    # ---------------------------------------------------------------
    # PART 4 — Halfway symmetry
    # ---------------------------------------------------------------
    print("\n--- Part 4: Halfway symmetry — 2^18 ≡ -1 ---")
    assert POWER_TABLE[18] == 36 == P - 1
    for k in range(1, 19):
        a    = POWER_TABLE[k]
        neg_a = POWER_TABLE[k + 18]
        assert (a + neg_a) % P == 0, f"2^{k} + 2^{k+18} ≢ 0"
    print("  2^(k+18) ≡ -2^k (mod 37) for all k = 1,...,18  ✓")
    print("  (Power sequence is negation-symmetric about the midpoint k=18)")

    # ---------------------------------------------------------------
    # PART 5 — CB is cross-orbit; verify non-AP logs
    # ---------------------------------------------------------------
    print("\n--- Part 5: CB = {8,13,24} is a cross-orbit selection ---")
    cb_orbits = {}
    for g in CB:
        n, orb = g, []
        for _ in range(3):
            orb.append(n); n = f(n)
        cb_orbits[g] = sorted(orb)

    assert cb_orbits[8]  != cb_orbits[13]
    assert cb_orbits[13] != cb_orbits[24]

    cb_logs = sorted(dlog[g] for g in CB)
    diffs   = [(cb_logs[1]-cb_logs[0]) % 36,
               (cb_logs[2]-cb_logs[1]) % 36,
               (cb_logs[0]-cb_logs[2]+36) % 36]
    assert not all(d == 12 for d in diffs), "CB should NOT be AP step 12"

    print(f"  8  ∈ orbit {cb_orbits[8]}")
    print(f"  13 ∈ orbit {cb_orbits[13]}")
    print(f"  24 ∈ orbit {cb_orbits[24]}")
    print(f"  CB discrete logs: {cb_logs}  diffs={diffs}  (not AP step 12)  ✓")
    print(f"  CB is one element from each of three distinct orbits.")

    print()
    print("All assertions passed. THEOREM 117 verified.")


if __name__ == "__main__":
    run()

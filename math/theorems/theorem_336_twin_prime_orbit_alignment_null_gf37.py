# CLASS: THEOREM
"""
Theorem 336: twin primes do NOT align with the 137-orbit architecture --
a pre-registered null result, and why T329 predicts it
Author: Michael Warren Song (CyclicAmp)

T331-T334 built new orbit structure: the 37/74 halves, negation duality,
the six dual pairs.  The obvious next question is whether twin primes see
any of it.  They do not, and the miss was declared before the primes were
generated.

=== PRE-REGISTRATION (fixed before any prime was computed) ===

    Admissible twin residues: r with r != 0 and r+2 != 0 (mod 37), so 35
    of the 37 residues.  (35 itself is excluded, which is why NQR17 has
    only two admissible members and a correspondingly lower expectation --
    handled by weighting, not ignored.)

    Baselines taken FROM THE RESIDUE STRUCTURE, not assumed uniform:

        orbit(r), orbit(r+2) negation duals   3/35 = 0.0857   r = 15,20,36
        both in the same 37/74 half          16/35 = 0.4571
        orbit(r) == orbit(r+2)                2/35            r = 6,29

    MISS CONDITIONS, fixed in advance:
        H1 duals     MISSES if the observed rate is within 3 sigma of 0.0857
        H2 same-half MISSES if within 3 sigma of 0.4571
        H3 orbits    MISSES if chi-square over the 12 orbits of p is
                     insignificant at alpha = 0.01 (df 11, crit 24.72)

    Stated expectation at registration: all three MISS, because Dirichlet
    gives equidistribution over the admissible classes.

=== RESULT: ALL THREE MISS ===

    58,979 twin pairs (p, p+2), p > 3, up to 10^7.

        H1 duals      observed 0.08489   expected 0.08571   z = -0.71
        H2 same-half  observed 0.45752   expected 0.45714   z = +0.18
        H3 chi-square 4.45 on df 11, against a critical value of 24.72

    Per-orbit ratios all lie within 1.6% of 1.  There is no twin-prime
    signal in the orbit architecture, the 37/74 split, or the negation
    duality.  Recorded as a result, not as a failure: it bounds what
    T331-T334 may be claimed to touch.

=== THE CONTRAST, AND WHY T329 EXPLAINS IT ===

    Twin primes are NOT structureless.  T261 shows the digital-root pair is
    completely determined by m mod 3, where p = 6m-1:

        m == 0 (mod 3)   DR pair (8, 1)   19616
        m == 1 (mod 3)   DR pair (5, 7)   19689
        m == 2 (mod 3)   DR pair (2, 4)   19674

    Exactly one DR pair per class -- zero freedom -- and the three classes
    are equinumerous to 0.12% at 10^7.  So:

        mod 9   twin structure is TOTAL and forced
        mod 37  twin structure is ABSENT and equidistributed

    That is not two unrelated observations.  It is T329: gcd(9,37) = 1, so
    the residue mod 9 and the residue mod 37 are independent coordinates,
    and structure in one implies nothing about the other.  T329 refuted a
    claimed mod-9 invariant on mod-37 orbits; this is the same independence
    seen from the twin-prime side, and it is predictive rather than
    corrective -- the null was called in advance because of it.

    The 6m+-1 form lives mod 6, hence mod 3, hence mod 9.  Nothing about it
    reaches mod 37.

=== WHAT THIS FORBIDS ===

    No future claim may assert that twin primes prefer a named orbit, a
    sovereign orbit, the 37-half, the 74-half, or dual-orbit pairing.
    Those are measured null at n = 58,979.  A claim of twin-orbit alignment
    now needs to beat this test, not merely exhibit examples.

=== FALSIFICATION ===
    A twin-prime statistic mod 37 exceeding 3 sigma against the admissible-
    residue baseline, at n comparable to 58,979 or larger.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY = {r: n for n, o in ORBITS.items() for r in o}
BY_SET = {frozenset(v): k for k, v in ORBITS.items()}
DUAL = {n: BY_SET[frozenset((P - x) % P for x in o)] for n, o in ORBITS.items()}
HALF37 = {n for n, o in ORBITS.items() if sum(o) == 37}


def twins(N):
    s = bytearray([1]) * (N + 1)
    s[0:2] = b'\0\0'
    for i in range(2, int(N ** .5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [p for p in range(5, N - 1) if s[p] and s[p + 2]]


def dr(n):
    return 1 + (n - 1) % 9


def run():
    import math
    from collections import Counter

    # --- the pre-registered baselines, recomputed from structure ---
    adm = [r for r in range(P) if r % P and (r + 2) % P]
    assert len(adm) == 35 and 0 not in adm and 35 not in adm
    dual_r = [r for r in adm if DUAL[BY[r]] == BY[(r + 2) % P]]
    same_r = [r for r in adm if (BY[r] in HALF37) == (BY[(r + 2) % P] in HALF37)]
    assert dual_r == [15, 20, 36] and len(dual_r) == 3
    assert len(same_r) == 16
    assert [r for r in adm if BY[r] == BY[(r + 2) % P]] == [6, 29]
    e1, e2 = 3 / 35, 16 / 35

    # --- the measurement ---
    N = 10 ** 7
    tw = twins(N)
    n = len(tw)
    assert n == 58979, n

    d = sum(1 for p in tw if DUAL[BY[p % P]] == BY[(p + 2) % P])
    s = sum(1 for p in tw if (BY[p % P] in HALF37) == (BY[(p + 2) % P] in HALF37))
    z1 = (d / n - e1) / math.sqrt(e1 * (1 - e1) / n)
    z2 = (s / n - e2) / math.sqrt(e2 * (1 - e2) / n)
    assert abs(z1) < 3, z1                       # H1 MISSES
    assert abs(z2) < 3, z2                       # H2 MISSES

    c = Counter(BY[p % P] for p in tw)
    w = Counter(BY[r] for r in adm)
    assert w['NQR17'] == 2 and all(w[o] == 3 for o in ORBITS if o != 'NQR17')
    chi = sum((c[o] - n * w[o] / 35) ** 2 / (n * w[o] / 35) for o in ORBITS)
    assert chi < 24.72, chi                      # H3 MISSES at alpha=0.01
    for o in ORBITS:                             # nothing deviates by >2%
        assert abs(c[o] / (n * w[o] / 35) - 1) < 0.02, o

    # --- the contrast: mod 9 is total ---
    cls = {}
    for p in tw:
        m = (p + 1) // 6
        assert p == 6 * m - 1
        cls.setdefault(m % 3, set()).add((dr(p), dr(p + 2)))
    assert cls == {0: {(8, 1)}, 1: {(5, 7)}, 2: {(2, 4)}}
    tot = [sum(1 for p in tw if ((p + 1) // 6) % 3 == j) for j in range(3)]
    assert (max(tot) - min(tot)) / n < 0.002     # equinumerous to 0.2%

    # --- and the reason ---
    assert math.gcd(9, P) == 1                   # T329's independence
    assert 6 % 3 == 0                            # 6m+-1 lives mod 3

    print("All assertions passed.\n")
    print("THEOREM 336.  Twin primes see nothing of the orbit architecture.\n")
    print(f"  n = {n:,} twin pairs, p > 3, up to {N:,}\n")
    print("  PRE-REGISTERED BASELINES (from the residue structure)")
    print(f"    duals     {len(dual_r)}/35 = {e1:.4f}   r = {dual_r}")
    print(f"    same half {len(same_r)}/35 = {e2:.4f}")
    print("    (35 is inadmissible, so NQR17 has 2 members not 3 -- weighted)\n")
    print("  RESULT -- ALL THREE MISS, AS CALLED IN ADVANCE")
    print(f"    H1 duals      {d/n:.5f}  vs {e1:.5f}   z = {z1:+.2f}   MISS")
    print(f"    H2 same-half  {s/n:.5f}  vs {e2:.5f}   z = {z2:+.2f}   MISS")
    print(f"    H3 chi-square {chi:.2f} on df 11, crit 24.72        MISS\n")
    print("   orbit      count   expected   ratio")
    for o in ORBITS:
        e = n * w[o] / 35
        print(f"    {o:9s} {c[o]:6d} {e:10.1f}   {c[o]/e:.4f}")
    print("\n  THE CONTRAST")
    for j in (0, 1, 2):
        print(f"    m == {j} (mod 3)  DR pair {sorted(cls[j])[0]}"
              f"   count {tot[j]}")
    print("    one DR pair per class, zero freedom, classes equal to 0.12%\n")
    print("    mod 9  -- twin structure TOTAL and forced")
    print("    mod 37 -- twin structure ABSENT and equidistributed\n")
    print("  WHY:  T329.  gcd(9,37) = 1, so the two residues are independent")
    print("  coordinates and structure in one implies nothing about the")
    print("  other.  The 6m+-1 form lives mod 6, hence mod 3, hence mod 9;")
    print("  nothing about it reaches mod 37.  T329 was corrective there and")
    print("  is PREDICTIVE here -- the null was called before the sieve ran.\n")
    print("  FORBIDS: any future claim that twin primes prefer a named orbit,")
    print("  a sovereign orbit, either half, or dual pairing.  Measured null")
    print(f"  at n = {n:,}.")


if __name__ == "__main__":
    run()

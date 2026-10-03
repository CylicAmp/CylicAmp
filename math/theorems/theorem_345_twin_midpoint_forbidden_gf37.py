# CLASS: THEOREM
"""
Theorem 345: twin-prime midpoints avoid exactly 1 and -1, and those are the
two self-inverse orbits -- settling the T167 conjecture and closing T336's
open direction
Author: Michael Warren Song (CyclicAmp)

T336 tested where the LOWER TWIN p lands and left the midpoint untested,
saying so.  T167 (CLASS: CONJECTURE) states what the midpoint does.  This
file runs it.

=== T167's CLAIM, MEASURED ===

    A twin midpoint is 6n, with twins 6n+-1.  Two residues are impossible:

        6n == 1  (mod 37)  =>  6n-1 == 0  =>  lower twin divisible by 37
        6n == 36 (mod 37)  =>  6n+1 == 0  =>  upper twin divisible by 37

    Over 58,979 twin midpoints below 10^7:

        midpoint == 1      0 occurrences
        midpoint == 36     0 occurrences
        midpoint == 0   1679 occurrences   <- allowed, and it happens

    Exact, with no exceptions.  Residue 0 is NOT forbidden: a midpoint
    divisible by 37 leaves both twins coprime to 37, and 1679 such pairs
    occur.  Only the two neighbours of the seam are excluded.

=== THE CONNECTION T167 COULD NOT SEE ===

    The forbidden set is {1, 36} = {1, -1}.  Their orbits are

        1  in IC     index 0
        -1 in NEG_H  index 6

    and IC and NEG_H are, by T331 and T332:

        the negation-dual pair                  (0 and 0+6)
        the ONLY two inversion-closed orbits    (the two roots of 2j == 0)

    SO THE TWIN-PRIME MIDPOINT SIEVE REMOVES EXACTLY ONE ELEMENT FROM EACH
    OF THE TWO SELF-INVERSE ORBITS, AND FROM NO OTHER ORBIT.

    T167 predates T331 and T332 and lists the two orbits without remark.
    The identification is made here.

=== HOW MUCH THAT IS WORTH, STATED PLAINLY ===

    Both halves are forced, separately:

      * the exclusion set is {1,-1} because the twin condition is 6n-1 and
        6n+1, and those vanish exactly at those two residues.  Arithmetic.
      * IC and NEG_H are the self-inverse orbits because IC is the subgroup
        and NEG_H = -IC, with (-u)^-1 = -u^-1.  T332.

    Two forced facts meeting is still forced.  This EXPLAINS which orbits the
    sieve touches; it is not evidence for anything.  Recorded at that grade.

=== THE DISTRIBUTION, PRE-REGISTERED ===

    Fixed before the sieve ran: admissible midpoint residues number 35 of 37,
    giving IC and NEG_H a weight of 2 and every other orbit 3.  MISS if
    chi-square over the twelve orbits is insignificant at alpha = 0.01
    (df 11, critical 24.72).  Stated expectation: MISS, by Dirichlet.

    RESULT: chi-square = 3.15.  MISS.  Every per-orbit ratio within 1.6% of
    1.  The midpoint is as equidistributed as the lower twin was in T336 --
    once the two forced exclusions are taken out of the baseline rather than
    left in it.

=== FALSIFICATION ===
    A twin midpoint congruent to 1 or 36 mod 37, with both twins > 37.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY = {r: n for n, o in ORBITS.items() for r in o}
IDX = {BY[pow(2, j, P)]: j for j in range(12)}
FORBIDDEN = {1, 36}


def twin_midpoints(N):
    s = bytearray([1]) * (N + 1)
    s[0:2] = b'\0\0'
    for i in range(2, int(N ** .5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [p + 1 for p in range(5, N - 1) if s[p] and s[p + 2]]


def run():
    from collections import Counter

    # --- the exclusion is forced ---
    assert (1 - 1) % P == 0 and (36 + 1) % P == 0
    assert FORBIDDEN == {1, (P - 1)}
    assert 36 == P - 1

    # --- the identification ---
    assert BY[1] == 'IC' and BY[36] == 'NEG_H'
    assert IDX['IC'] == 0 and IDX['NEG_H'] == 6
    assert (IDX['NEG_H'] - IDX['IC']) % 12 == 6              # T331 dual pair
    inv = {x: pow(x, P - 2, P) for x in range(1, P)}
    closed = sorted(n for n, o in ORBITS.items()
                    if {inv[x] for x in o} == set(o))
    assert closed == ['IC', 'NEG_H']                         # T332
    assert [j for j in range(12) if (2 * j) % 12 == 0] == [0, 6]
    # one element removed from each self-inverse orbit, none elsewhere
    for n, o in ORBITS.items():
        k = len(set(o) & FORBIDDEN)
        assert k == (1 if n in ('IC', 'NEG_H') else 0), n

    # --- measurement ---
    mids = twin_midpoints(10 ** 7)
    n = len(mids)
    assert n == 58979, n
    assert all(m % 6 == 0 for m in mids)
    for r in FORBIDDEN:
        assert not [m for m in mids if m % P == r], r          # EXACT
    zero = [m for m in mids if m % P == 0]
    assert len(zero) == 1679 and zero                          # 0 is allowed
    for m in zero[:50]:                                        # both twins ok
        assert (m - 1) % P and (m + 1) % P

    # --- the pre-registered distribution ---
    w = {o: sum(1 for r in ORBITS[o] if r not in FORBIDDEN) for o in ORBITS}
    assert w['IC'] == 2 and w['NEG_H'] == 2
    assert all(w[o] == 3 for o in ORBITS if o not in ('IC', 'NEG_H'))
    c = Counter(BY[m % P] for m in mids if m % P)
    tot, nz = sum(w.values()), sum(Counter(BY[m % P]
                                           for m in mids if m % P).values())
    chi = sum((c[o] - nz * w[o] / tot) ** 2 / (nz * w[o] / tot) for o in ORBITS)
    assert chi < 24.72, chi
    for o in ORBITS:
        assert abs(c[o] / (nz * w[o] / tot) - 1) < 0.02, o

    print("All assertions passed.\n")
    print("THEOREM 345.  Twin midpoints avoid exactly 1 and -1.\n")
    print(f"  {n:,} twin midpoints 6n below 10^7, all divisible by 6\n")
    print("  T167's FORBIDDEN RESIDUES, MEASURED")
    for r in sorted(FORBIDDEN):
        print(f"    midpoint == {r:2d}    0 occurrences   ({BY[r]})")
    print(f"    midpoint ==  0 {len(zero):5d} occurrences   allowed, and it happens")
    print("    only the two neighbours of the seam are excluded.\n")
    print("  THE IDENTIFICATION T167 COULD NOT MAKE")
    print("    the forbidden set is {1, -1}; their orbits are IC (idx 0) and")
    print("    NEG_H (idx 6), which by T331 are the negation-dual pair and by")
    print("    T332 are the ONLY two inversion-closed orbits.")
    print("    So the sieve removes one element from each self-inverse orbit")
    print("    and from no other orbit.\n")
    print("    GRADE: both halves are forced, so the meeting is forced.")
    print("    It explains WHICH orbits the sieve touches. Not evidence.\n")
    print(f"  DISTRIBUTION, pre-registered: chi-square {chi:.2f} on df 11")
    print(f"  against 24.72 -> MISS, as predicted.\n")
    print("   orbit      count   expected   ratio  w")
    for o in ORBITS:
        e = nz * w[o] / tot
        print(f"    {o:9s} {c[o]:6d} {e:10.1f}   {c[o]/e:.4f}  {w[o]}")
    print("\n  T336 tested the lower twin and left this open. Closed here.")


if __name__ == "__main__":
    run()

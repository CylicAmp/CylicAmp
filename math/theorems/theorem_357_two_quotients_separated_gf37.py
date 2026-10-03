# CLASS: THEOREM
"""
Theorem 357: the 13-state cubic quotient and the 9-state doubling system,
kept apart -- and they differ in kind, not only in size
Author: Michael Warren Song (CyclicAmp)

Built to the stated order: 13-state coordinates, exact phi table, 9-state
table, then compare -- with no projection introduced between them.

=== TERMINOLOGY, CORRECTED FIRST ===

    "Terminal attractor" means a CYCLE or a FIXED POINT, not any bounded
    component.  And "the global transition graph must terminate" is wrong
    for a finite deterministic system: a trajectory eventually ENTERS a
    periodic attractor and then cycles forever.  It terminates only when
    the attractor is a fixed point.  Neither system below terminates in
    that sense; phi has no fixed point at all.

=== STEP 1: THE 13-STATE QUOTIENT ===

    q : F_37 -> F_37/~ with x ~ y iff x^3 = y^3.  Twelve nonzero cubing
    orbits plus the seam {0}: THIRTEEN states.  T(x) = x^3 + 33 is constant
    on each class, so T = iota o Tbar o q, and phi = q o Tbar.

        state      rep  Tbar    phi(state)   status
        IC           1    34    D7           cycle
        D7           7     6    TESLA        cycle
        TESLA        6    27    NEG_H        cycle
        NEG_H       11    32    SEED         cycle
        SEED        18    19    CAS_EXT      cycle
        CAS_EXT      5    10    IC           cycle
        C9          14     2    DARK_A       transient
        DARK_A       2     4    C3           transient
        C3           3    23    TESLA        transient
        SA_ST_A      9    22    NQR17        transient
        NQR17       17    25    SA_ST_B      transient
        SA_ST_B     21     7    D7           transient
        SEAM         0    33    D7           transient

        cycle 6, chains 3 + 3 + 1, total 13.

    phi is NOT a permutation.  Three states -- C9, SA_ST_A and SEAM -- have
    no phi-preimage; they are the sources of the three chains.

=== STEP 2: THE 9-STATE SYSTEM ===

    psi : r -> 2r (mod 9), on nine states.

        0 -> 0
        1 -> 2 -> 4 -> 8 -> 7 -> 5 -> 1
        3 -> 6 -> 3

    psi IS a permutation, since gcd(2,9) = 1.  No transients, no sources.
    Its decomposition is exactly the ring structure of Z/9Z:

        fixed point   {0}            the zero
        6-cycle       {1,2,4,8,7,5}  the unit group, ord_9(2) = 6
        2-cycle       {3,6}          the ideal (3) minus zero

        1 + 6 + 2 = 9.

=== STEP 3: THE COMPARISON, WITH NOTHING BLENDED ===

                              phi (13 states)      psi (9 states)
        permutation?          NO                   YES
        transient states      7 of 13              0 of 9
        sources (no preimage) 3                    0
        number of cycles      1                    3
        cycle lengths         6                    6, 2, 1
        fixed points          0                    1 (the zero)

    They differ in KIND.  psi is invertible and its whole state space is
    periodic; phi loses information at every step and more than half its
    states are transient.  No projection relates them, and none is
    proposed here.

    THE SHARED 6 IS NOT A BRIDGE.  psi's 6-cycle is ord_9(2) = 6, the order
    of 2 in the unit group of Z/9Z.  phi's 6-cycle is not an order of
    anything: phi is not a group action, it is the cubic map on cosets, and
    its cycle length is measured.  Two sixes arising from unrelated causes.
    By T329 and T336 there is no reason to expect the mod-9 and mod-37
    coordinates to interact at all -- gcd(9,37) = 1 and CRT makes them
    independent -- so the coincidence is what independence predicts.

=== ON T_C(N) << N ===

    Not addressed here, and correctly so.  T_C has no definition in this
    corpus and the inequality has no proof, so "global compressor" is an
    empirical description, not a theorem.  Recorded as an open item rather
    than used.

=== FALSIFICATION ===
    A phi-preimage for C9, SA_ST_A or SEAM; a transient state of psi; or a
    second cycle of phi.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY = {r: n for n, o in ORBITS.items() for r in o}
T = lambda x: (pow(x, 3, P) + 33) % P


def decompose(f, states):
    """(cycles, transient) for a self-map of a finite set."""
    per = set()
    for s in states:
        seen, y = {}, s
        i = 0
        while y not in seen:
            seen[y] = i
            y = f(y)
            i += 1
        z, cy = y, [y]
        while f(z) != y:
            z = f(z)
            cy.append(z)
        per |= set(cy)
    cycles, done = [], set()
    for s in sorted(per, key=str):
        if s in done:
            continue
        cy, y = [s], f(s)
        while y != s:
            cy.append(y)
            y = f(y)
        done |= set(cy)
        cycles.append(cy)
    return cycles, [s for s in states if s not in per]


def run():
    cls = lambda x: 'SEAM' if x == 0 else BY[x]
    CL = sorted(ORBITS) + ['SEAM']
    assert len(CL) == 13

    # --- step 1 ---
    Tbar = {c: (T(0) if c == 'SEAM' else T(ORBITS[c][0])) for c in CL}
    assert len(set(Tbar.values())) == 13                 # injective
    phi = {c: cls(Tbar[c]) for c in CL}
    cyc, tr = decompose(lambda c: phi[c], CL)
    assert len(cyc) == 1 and len(cyc[0]) == 6
    assert len(tr) == 7
    assert set(cyc[0]) == {'IC', 'D7', 'TESLA', 'NEG_H', 'SEED', 'CAS_EXT'}
    w = ['IC']
    while phi[w[-1]] != 'IC':
        w.append(phi[w[-1]])
    assert w == ['IC', 'D7', 'TESLA', 'NEG_H', 'SEED', 'CAS_EXT']
    assert sorted(set(CL) - set(phi.values())) == ['C9', 'SA_ST_A', 'SEAM']
    assert len(set(phi.values())) != 13                  # not a permutation
    assert 6 + 3 + 3 + 1 == 13

    # --- step 2 ---
    psi = {r: (2 * r) % 9 for r in range(9)}
    assert sorted(psi.values()) == list(range(9))        # IS a permutation
    pc, pt = decompose(lambda r: psi[r], list(range(9)))
    assert pt == []                                      # no transients
    assert sorted(len(c) for c in pc) == [1, 2, 6]
    assert {tuple(sorted(c)) for c in pc} == {(0,), (3, 6), (1, 2, 4, 5, 7, 8)}
    assert next(k for k in range(1, 9) if pow(2, k, 9) == 1) == 6
    assert 1 + 6 + 2 == 9

    # --- step 3: they differ in kind ---
    assert len(set(phi.values())) < 13 and len(set(psi.values())) == 9
    assert len(tr) == 7 and len(pt) == 0
    assert len(cyc) == 1 and len(pc) == 3
    assert not any(phi[c] == c for c in CL)              # phi has no fixed pt
    assert psi[0] == 0                                   # psi does
    from math import gcd
    assert gcd(9, P) == 1                                # T329 independence

    print("All assertions passed.\n")
    print("THEOREM 357.  Two quotients, kept apart.\n")
    print("  TERMINOLOGY: an attractor is a cycle or a fixed point. A finite")
    print("  deterministic trajectory ENTERS a periodic attractor; it does")
    print("  not terminate unless that attractor is a fixed point. phi has")
    print("  no fixed point, so nothing in it terminates.\n")
    print("  STEP 1 -- 13-STATE CUBIC QUOTIENT")
    print("   state      rep  Tbar   phi          status")
    for c in w + [x for x in CL if x not in w]:
        rep = 0 if c == 'SEAM' else min(ORBITS[c])
        print(f"   {c:9s} {rep:4d} {Tbar[c]:5d}   {phi[c]:9s}   "
              f"{'cycle' if c in w else 'transient'}")
    print(f"\n   cycle 6, chains 3 + 3 + 1, total 13")
    print(f"   permutation? NO. sources with no preimage:"
          f" {sorted(set(CL)-set(phi.values()))}\n")
    print("  STEP 2 -- 9-STATE DOUBLING,  r -> 2r (mod 9)")
    for c in sorted(pc, key=len, reverse=True):
        print(f"   {len(c)}-cycle: {' -> '.join(map(str,c))} -> {c[0]}")
    print("   permutation? YES. no transients.")
    print("   = the ring structure: unit group (6), ideal (3) minus 0 (2),")
    print("     and the zero (1). 1 + 6 + 2 = 9.\n")
    print("  STEP 3 -- COMPARISON, nothing blended")
    print("                          phi (13)       psi (9)")
    print("   permutation?           NO             YES")
    print(f"   transient states       {len(tr)} of 13       0 of 9")
    print("   sources                3              0")
    print(f"   cycles                 {len(cyc)}              {len(pc)}")
    print("   cycle lengths          6              6, 2, 1")
    print("   fixed points           0              1\n")
    print("   They differ in KIND. psi is invertible with every state")
    print("   periodic; phi loses information and 7 of 13 states are")
    print("   transient. No projection relates them and none is proposed.\n")
    print("   THE SHARED 6 IS NOT A BRIDGE: psi's is ord_9(2) = 6, an order")
    print("   in a group. phi's is not an order of anything -- phi is not a")
    print("   group action. gcd(9,37) = 1, so T329/T336 say the coordinates")
    print("   are independent; the coincidence is what independence predicts.")


if __name__ == "__main__":
    run()

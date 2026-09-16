# CLASS: THEOREM
"""
Theorem 358: no surjective semiconjugacy carries the cubic quotient onto
the mod-9 system -- formal presentation
Author: Michael Warren Song (CyclicAmp)

The theorem/lemma/corollary version of T357, with the factorisation and the
functional-graph decomposition as propositions.  It ends on a result T357
did not have: the two systems are separated by an impossibility, not merely
by a table of differing invariants.

Notation.  P = 37, mu_3 = {1, 10, 26}, q the quotient projection,
iota the inclusion, T(x) = x^3 + 33, psi(r) = 2r on Z/9Z.

--------------------------------------------------------------------------
LEMMA 1 (the fibres).  For x, y in F_37, x ~ y iff x^3 = y^3.  The classes
are the twelve cosets of mu_3 together with {0}, so |F_37/~| = 13.

  Proof.  For y != 0, x^3 = y^3 iff (x/y)^3 = 1 iff x/y in mu_3.  Now
  ord_37(10) = 3, since 10^3 = 1000 = 27(37) + 1, so mu_3 = <10> has order
  3.  Lagrange gives |F_37*| / |mu_3| = 36/3 = 12 cosets, and {0} is its
  own class.  []

LEMMA 2 (constancy, not merely preservation).  x ~ y implies T(x) = T(y).

  Proof.  x ~ y gives x^3 = y^3, hence x^3 + 33 = y^3 + 33.  []

  Remark.  Descent needs only x ~ y => T(x) ~ T(y).  Lemma 2 is strictly
  stronger and is what Corollary 4 uses.

PROPOSITION 3 (factorisation).  There is a unique Tbar : F_37/~ -> F_37
with T = iota o Tbar o q, and Tbar is injective.

  Proof.  Existence and uniqueness are the universal property of the
  quotient, available by Lemma 2.  For injectivity, Tbar([x]) = Tbar([y])
  gives x^3 + 33 = y^3 + 33, so x^3 = y^3 and [x] = [y].  []

COROLLARY 4 (in-degrees).  |im T| = 13.  Each image point has in-degree
equal to the size of its fibre class: 3 for each of the twelve orbits and 1
for the seam.  The remaining 24 elements of F_37 have in-degree 0.

  Proof.  im T = im Tbar, of size 13 by Proposition 3.  By Lemma 2 and
  injectivity, T^-1(Tbar([x])) = [x] exactly.  Class sizes are 3 (twelve
  times) and 1 (once), and 37 - 13 = 24.  []

DEFINITION 5.  phi = q o Tbar : F_37/~ -> F_37/~.

PROPOSITION 6 (decomposition).  phi has exactly one cycle, of length 6,

    IC -> D7 -> TESLA -> NEG_H -> SEED -> CAS_EXT -> IC,

and seven transient states in three chains,

    C9 -> DARK_A -> C3 -> TESLA          (length 3)
    SA_ST_A -> NQR17 -> SA_ST_B -> D7    (length 3)
    SEAM -> D7                           (length 1)

so 6 + 3 + 3 + 1 = 13.

  Proof.  Finite verification over the thirteen classes; asserted below.  []

PROPOSITION 7 (non-invertibility).  phi is not injective.  Exactly three
states have empty preimage: C9, SA_ST_A, SEAM.  phi has no fixed point.

PROPOSITION 8 (mod 9).  psi is a permutation of Z/9Z with cycle type
(1, 2, 6), decomposing as {0}, the ideal (3) minus zero = {3, 6}, and the
unit group {1,2,4,8,7,5}.

  Proof.  gcd(2,9) = 1 gives bijectivity.  Each listed set is psi-stable:
  2.0 = 0; 2.3 = 6 and 2.6 = 3; and the units are closed under
  multiplication by the unit 2.  The 6-cycle has that length because
  ord_9(2) = 6.  []

--------------------------------------------------------------------------
THEOREM 9 (separation).  There is NO surjective pi : F_37/~ -> Z/9Z with
pi o phi = psi o pi.

  Proof.  Suppose such a pi exists; then pi o phi^n = psi^n o pi for all n.
  By Proposition 6 every transient chain has length at most 3, so phi^3
  maps all thirteen states into the 6-cycle; hence |phi^3(X)| = 6.  Then

      psi^3(pi(X)) = pi(phi^3(X)),

  whose right-hand side has at most 6 elements.  But pi surjective gives
  pi(X) = Z/9Z, and psi is a bijection, so psi^3(Z/9Z) = Z/9Z has 9
  elements.  Hence 9 <= 6, a contradiction.  []

COROLLARY 10.  phi and psi are not isomorphic as dynamical systems, and
neither factors onto the other.  The shared cycle length 6 admits no
structural upgrade, not even a one-directional one.

REMARK 11 (what the proof actually uses).  Only two facts: that phi's
eventual image has 6 elements, and that a bijection has full eventual
image.  So the argument excludes a surjective semiconjugacy from phi onto
ANY permutation of more than six states.  It is not special to 9.

--------------------------------------------------------------------------
OPEN (not a proposition).  T_C remains undefined in this corpus and
T_C(N) << N unproved, so it is not used above.
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
cls = lambda x: 'SEAM' if x == 0 else BY[x]
CL = sorted(ORBITS) + ['SEAM']
PHI = {c: cls(T(0) if c == 'SEAM' else T(ORBITS[c][0])) for c in CL}
PSI = {r: (2 * r) % 9 for r in range(9)}


def run():
    from collections import Counter
    from math import gcd

    # LEMMA 1
    assert pow(10, 3, P) == 1 and 1000 == 27 * P + 1
    mu3 = {pow(10, k, P) for k in range(3)}
    assert mu3 == {1, 10, 26} and len(mu3) == 3
    assert (P - 1) // 3 == 12 and len(CL) == 13
    for o in ORBITS:
        r = min(ORBITS[o])
        assert set(ORBITS[o]) == {(r * h) % P for h in mu3}

    # LEMMA 2
    for o in ORBITS:
        assert len({T(x) for x in ORBITS[o]}) == 1
    # strictly stronger than preservation
    assert all(T(x) == T(y) for o in ORBITS
               for x in ORBITS[o] for y in ORBITS[o])

    # PROPOSITION 3
    Tbar = {c: (T(0) if c == 'SEAM' else T(ORBITS[c][0])) for c in CL}
    assert len(set(Tbar.values())) == 13

    # COROLLARY 4
    ind = Counter(T(x) for x in range(P))
    assert len(ind) == 13
    assert dict(Counter(ind.values())) == {3: 12, 1: 1}
    assert P - len(ind) == 24
    for c in CL:
        pre = {x for x in range(P) if T(x) == Tbar[c]}
        assert pre == ({0} if c == 'SEAM' else set(ORBITS[c]))

    # PROPOSITION 6
    cyc = ['IC']
    while PHI[cyc[-1]] != 'IC':
        cyc.append(PHI[cyc[-1]])
    assert cyc == ['IC', 'D7', 'TESLA', 'NEG_H', 'SEED', 'CAS_EXT']
    def chain(c):
        p = [c]
        while p[-1] not in cyc:
            p.append(PHI[p[-1]])
        return p
    assert chain('C9') == ['C9', 'DARK_A', 'C3', 'TESLA']
    assert chain('SA_ST_A') == ['SA_ST_A', 'NQR17', 'SA_ST_B', 'D7']
    assert chain('SEAM') == ['SEAM', 'D7']
    assert 6 + 3 + 3 + 1 == 13

    # PROPOSITION 7
    assert len(set(PHI.values())) < 13
    assert sorted(set(CL) - set(PHI.values())) == ['C9', 'SA_ST_A', 'SEAM']
    assert not any(PHI[c] == c for c in CL)

    # PROPOSITION 8
    assert gcd(2, 9) == 1 and sorted(PSI.values()) == list(range(9))
    assert PSI[0] == 0 and PSI[3] == 6 and PSI[6] == 3
    units = {1, 2, 4, 5, 7, 8}
    assert {PSI[r] for r in units} == units
    assert next(k for k in range(1, 9) if pow(2, k, 9) == 1) == 6

    # THEOREM 9 -- the two ingredients
    S = set(CL)
    for _ in range(3):
        S = {PHI[c] for c in S}
    assert S == set(cyc) and len(S) == 6         # eventual image is 6
    Z = set(range(9))
    for _ in range(3):
        Z = {PSI[r] for r in Z}
    assert Z == set(range(9)) and len(Z) == 9    # bijection: full image
    assert 9 > 6                                 # the contradiction

    # REMARK 11 -- the bound is on the target's size, not on 9
    assert len(set(cyc)) == 6

    print("All assertions passed.\n")
    print("THEOREM 358.  No surjective semiconjugacy phi -> psi.\n")
    print("  L1  13 classes: twelve mu_3-cosets plus {0}")
    print("  L2  x ~ y => T(x) = T(y)          constancy, not preservation")
    print("  P3  T = iota o Tbar o q, Tbar injective")
    print("  C4  |im T| = 13; in-degrees 3 (x12) and 1; 24 with none")
    print("  P6  phi: one 6-cycle, chains 3 + 3 + 1, total 13")
    print("  P7  phi not injective; sources C9, SA_ST_A, SEAM; no fixed pt")
    print("  P8  psi a permutation, type (1,2,6) = zero, ideal, units\n")
    print("  THEOREM 9.  Suppose pi surjective with pi.phi = psi.pi.")
    print("    Every chain has length <= 3, so phi^3 sends all 13 states")
    print("    into the 6-cycle and |phi^3(X)| = 6. Then")
    print("        psi^3(pi(X)) = pi(phi^3(X)),  at most 6 elements.")
    print("    But pi onto gives pi(X) = Z/9, and psi bijective gives")
    print("    psi^3(Z/9) = Z/9, of size 9. So 9 <= 6. Contradiction. []\n")
    print("  C10 phi and psi are not isomorphic and neither factors onto")
    print("      the other. The shared 6 admits no structural upgrade,")
    print("      not even one-directional.\n")
    print("  R11 the proof uses only |eventual image of phi| = 6 and that a")
    print("      bijection has full eventual image. So it excludes a")
    print("      surjective semiconjugacy onto ANY permutation of more than")
    print("      six states. Nothing about 9 is used.")


if __name__ == "__main__":
    run()

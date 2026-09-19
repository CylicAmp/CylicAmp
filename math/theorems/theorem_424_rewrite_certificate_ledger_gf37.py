# CLASS: THEOREM
"""
Theorem 424: the rewrite-certificate ledger as a subgroup filtration of
(Z/37Z)*, and the one relation that does NOT survive the DLQ map

Written to supply the left-hand side that T423 recorded as missing. T423
graded the "four-tier ledger = DLQ validation tiers" claim as UNGRADEABLE
because a grep for e_hard / K_E / EASY_EQ / quotient strata / kernel
filtration returned nothing across the corpus: there was no source object to
build a Phi from. This file writes that object down, so the claim can be
graded instead of deferred.

WHAT THIS IS, PLAINLY.  The supplied ledger named K_easy, K_E and e_hard but
never defined them here. This is a CONSTRUCTION, not a recovery: the
smallest filtration consistent with the names, built from objects already in
the corpus. If the intended K_E is a different subgroup the grade in Part 4
must be recomputed, and Part 4 says exactly which line changes.

PRIOR ART.
  T417 (spectral_embedding_gf37.py) and T419 (sigma3_eisenstein_gf37.py)
  already carry H u (-H) = {1,10,11,26,27,36} as the Cayley generator set,
  and T419 has -H as the cube roots of -1. This file uses that set as K_E;
  it does not re-derive it.
  T138/T200/T285/T339 carry the Z/12 orbit quotient G/H. Not used here --
  the quotient this ledger needs is G/K_E of order 6, which is a different
  quotient and is stated as such.
  T423 is the grading this file feeds.

================================================================================
THE LEDGER
================================================================================

  G = (Z/37Z)*, cyclic of order 36, generator 2.

  The filtration, each step a subgroup of the next:

      {1}  <|  H  <|  K_E  <|  G
       1      3       6       36          orders
          [H:1]=3  [K_E:H]=2  [G:K_E]=6   indices,  3 * 2 * 6 = 36

      H   = {1, 10, 26}            the 137-map kernel; ord_37(26) = 3
      K_E = H u (-H)
          = {1, 10, 11, 26, 27, 36}  the Cayley generator set (T417, T419)
      -H  = {11, 27, 36}           the cube roots of -1 (T419), = NEG_H

  K_easy = H.  e_hard = [K_E : H] = 2, so e_hard - 1 = 1 non-trivial coset,
  which is -H, and it has 3 elements. That is the supplied ledger's
  "e_hard - 1 non-trivial coset defects", now a count and not a phrase.

  The four tiers, as a partition of G:

      tier                x in                    size  orbit
      EXACT               {1}                        1  IC
      EASY_EQUIVALENT     H \\ {1} = {10,26}          2  IC
      FINAL_EQUIVALENT    K_E \\ H = -H              3  NEG_H
      INVALID             G \\ K_E                  30  the other 10 orbits
                                                   --
                                                   36

  The tier boundaries are the subgroup boundaries. That is the whole content
  of calling it a filtration, and it is why the tiers are not arbitrary
  buckets: each is a subgroup or a coset of one.

  COST READING, which is what makes the tiers a ledger and not just a chain:

      EXACT             x = 1                  nothing to certify
      EASY_EQUIVALENT   x in H, x != 1         one 137-map step: 26x, 26^2 x
      FINAL_EQUIVALENT  x in -H                x^3 = -1, a cube-root test
      INVALID           x not in K_E           no certificate exists

================================================================================
THE THREE STRUCTURAL FACTS (each asserted below)
================================================================================

  (1) NESTING IS REAL.  {1} < H < K_E < G, orders 1, 3, 6, 36, and H and K_E
      are closed under multiplication. A four-tier ledger whose tiers were
      not subgroups would have no composition law at all.

  (2) FINAL_EQUIVALENT IS A COSET, NOT A SUBGROUP.  -H is not closed:
      11 * 11 = 121 = 10 (mod 37), which is in H, not in -H. This is correct
      and not a defect -- the supplied ledger says "coset defects", and a
      coset is exactly what a non-trivial quotient class is. Two hard
      certificates compose to an easy one.

  (3) INVALID IS NOT ABSORBING.  This is the fact that decides the grade.
      Of the 30 * 30 = 900 ordered pairs of INVALID elements, 180 have a
      product back inside K_E -- (2,5) is the first, 2*5 = 10 in H. So two
      records that individually admit no certificate can compose into one
      that does.

================================================================================
WHAT THIS DOES TO T423's CLAIM 2
================================================================================

  Claim 2 was: "the four-tier rewrite-certificate ledger maps one-to-one to
  standard data quality and quarantine layers", with INVALID -> DLQ.

  With the left-hand side now written down, Cut 2 can be run. Define

      Phi:  tier of x in G   ->   disposition of a record in the pipeline
            EXACT            ->   bit-identical pass-through
            EASY_EQUIVALENT  ->   syntactic normalization, O(1)
            FINAL_EQUIVALENT ->   semantic reconciliation, heavy
            INVALID          ->   dead-letter queue

  Phi is now specified, and two named relations survive it:

      the tiers are totally ordered by certificate cost, and Phi is
      order-preserving;
      the easy tier is closed, so composing two easy records is easy --
      H is a subgroup.

  One named relation does NOT survive, and it is checked, not argued:

      IN THE ALGEBRA   INVALID is not absorbing: 180 of 900 ordered invalid
                       pairs land back in K_E.
      IN THE PIPELINE  the DLQ is absorbing. A dead-lettered row does not
                       combine with another dead-lettered row to produce a
                       valid one; that is the entire point of a DLQ.

  So Phi preserves the ordering and the easy-tier closure, and inverts the
  absorbing property. GRADE: Level 2 for the filtration, and the DLQ
  identification specifically FAILS at Cut 2, on a computed obstruction
  rather than on a missing object. That is a better outcome than T423's
  "ungradeable" and a worse one than the claim asserted.

  This is the same shape as rule 90 against rule 30: the literal object
  exists, it is computed, and it is a different object in one identified
  respect.

  WHAT WOULD CHANGE THE GRADE.  Only one line. If the intended K_E is a
  subgroup for which G \\ K_E IS closed under multiplication, the obstruction
  disappears. No such K_E exists: for any proper subgroup S < G, the
  complement G \\ S is never closed, since S has index >= 2 and two elements
  of the same non-trivial coset multiply into a coset that can be S itself.
  Asserted below over all nine subgroups of G. So the obstruction is not an
  artifact of choosing K_E = H u (-H); it holds for every possible choice,
  and the DLQ identification cannot be repaired by picking a better subgroup.

================================================================================
FALSIFICATION
================================================================================

  Any of: H or K_E failing closure; the indices not multiplying to 36;
  -H turning out closed; zero INVALID pairs landing in K_E; or some proper
  subgroup of G whose complement is closed. All five are asserted.
"""

import sys

P = 37
ORBITS = {
    "IC": {1, 10, 26}, "DARK_A": {2, 15, 20}, "C3": {3, 4, 30},
    "CAS_EXT": {5, 13, 19}, "TESLA": {6, 8, 23}, "D7": {7, 33, 34},
    "SA_ST_A": {9, 12, 16}, "NEG_H": {11, 27, 36}, "C9": {14, 29, 31},
    "NQR17": {17, 22, 35}, "SEED": {18, 24, 32}, "SA_ST_B": {21, 25, 28},
}


def orbit_of(x):
    r = x % P
    return "SEAM" if r == 0 else next(k for k, v in ORBITS.items() if r in v)


def closed(S):
    return all((a * b) % P in S for a in S for b in S)


def subgroups():
    """Every subgroup of the cyclic group (Z/37Z)*, via the generator 2."""
    g, out = 2, []
    for d in (1, 2, 3, 4, 6, 9, 12, 18, 36):
        h = pow(g, 36 // d, P)
        S = {pow(h, k, P) for k in range(d)}
        assert len(S) == d
        out.append(S)
    return out


def main():
    G = set(range(1, P))
    H = {1, 10, 26}
    negH = {(-x) % P for x in H}
    K_E = H | negH
    tiers = [("EXACT", {1}), ("EASY_EQUIVALENT", H - {1}),
             ("FINAL_EQUIVALENT", K_E - H), ("INVALID", G - K_E)]

    print("=" * 78)
    print("THEOREM 424: THE REWRITE-CERTIFICATE LEDGER AS A SUBGROUP FILTRATION")
    print("=" * 78)

    print("\nPart 1: the filtration {1} < H < K_E < G")
    print("   H   = %-24s order %d  closed %s" % (sorted(H), len(H), closed(H)))
    print("   -H  = %-24s order %d  closed %s"
          % (sorted(negH), len(negH), closed(negH)))
    print("   K_E = %-24s order %d  closed %s"
          % (sorted(K_E), len(K_E), closed(K_E)))
    print("   indices  [H:1]=%d  [K_E:H]=%d  [G:K_E]=%d   product %d = |G|"
          % (len(H), len(K_E) // len(H), (P - 1) // len(K_E),
             len(H) * (len(K_E) // len(H)) * ((P - 1) // len(K_E))))
    assert closed(H) and closed(K_E), "a tier boundary is not a subgroup"
    assert H < K_E < G, "the filtration does not nest"
    assert len(H) * 2 * 6 == 36, "indices do not multiply to |G|"
    assert pow(26, 3, P) == 1 and pow(26, 1, P) != 1, "ord(26) is not 3"
    assert negH == {x for x in G if pow(x, 3, P) == P - 1}, "-H != cube roots of -1"
    print("   -H is exactly the cube roots of -1 (T419), and NEG_H as an orbit")

    print("\nPart 2: the four tiers partition G")
    tot = 0
    for name, S in tiers:
        orbs = sorted({orbit_of(x) for x in S})
        print("   %-17s %2d  %s" % (name, len(S), orbs if len(orbs) < 4
                                    else "%d orbits" % len(orbs)))
        tot += len(S)
    print("   %-17s %2d" % ("total", tot))
    assert tot == 36, "tiers do not cover G"
    union = set()
    for _, S in tiers:
        assert not (union & S), "tiers overlap"
        union |= S
    assert union == G, "tiers do not partition G"
    assert (K_E - H) == negH

    print("\nPart 3: e_hard = [K_E : H] = %d, so e_hard - 1 = %d non-trivial coset"
          % (len(K_E) // len(H), len(K_E) // len(H) - 1))
    print("   that coset is -H, with %d elements" % len(negH))
    assert len(K_E) // len(H) == 2

    print("\nPart 4: FINAL_EQUIVALENT is a coset, not a subgroup")
    print("   11 * 11 = %d, which is in H, not in -H" % ((11 * 11) % P))
    assert not closed(negH), "-H is closed, so it is not a proper coset"
    assert (11 * 11) % P in H
    print("   two hard certificates compose to an easy one. Correct for a coset.")

    print("\nPart 5: INVALID is NOT absorbing -- the obstruction")
    bad = sorted(G - K_E)
    pairs = [(a, b) for a in bad for b in bad if (a * b) % P in K_E]
    print("   ordered INVALID pairs with product in K_E: %d of %d"
          % (len(pairs), len(bad) ** 2))
    print("   first four: %s   (2*5 = %d, in H)" % (pairs[:4], (2 * 5) % P))
    assert len(pairs) > 0, "INVALID is absorbing after all"
    assert (2 * 5) % P in H
    print("   the DLQ IS absorbing. Phi inverts this relation ->")
    print("   the DLQ identification fails Cut 2.")

    print("\nPart 6: no choice of K_E repairs it")
    for S in subgroups():
        comp = G - S
        if comp:
            assert not closed(comp), sorted(S)
    print("   checked all 9 subgroups of G: the complement of a proper")
    print("   subgroup is never closed. The obstruction is structural, not a")
    print("   consequence of choosing K_E = H u (-H).")

    print("\nGRADE for T423 claim 2")
    print("   filtration            Level 2  (Phi specified; order and easy-")
    print("                                  tier closure both survive)")
    print("   DLQ identification    fails Cut 2 on the absorbing property")
    print("   previously            UNGRADEABLE (no left-hand side)")

    print("\n" + "=" * 78)
    print("ALL ASSERTIONS PASS")
    print("=" * 78)


if __name__ == "__main__":
    sys.exit(main())

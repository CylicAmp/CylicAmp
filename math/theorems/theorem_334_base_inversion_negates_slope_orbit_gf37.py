# CLASS: THEOREM
"""
Theorem 334: inverting the base negates the slope orbit -- forced by Vieta,
universal over p == 1 (mod 3), and the 37-specific part graded
Author: Michael Warren Song (CyclicAmp)

The canon draft added a sovereign-pairing observation to T333:

    base 10  ->  slope b+2 = 12  in SA_ST_A  (anchor 9,  target 12)
    base 26  ->  slope b+2 = 28  in SA_ST_B  (anchor 25, target 21)

Both halves check out, and the structural half is forced.  The naming half
is not, and is graded below rather than asserted.

=== THE LAW, AND ITS PROOF FROM VIETA ===

    T333: the admissible bases are the roots of Phi_3(x) = x^2 + x + 1 mod
    37, namely b1 = 10 and b2 = 26 = b1^2, and the AP-triple residue is
    d(b+2).  Claim:

        ORBIT(b1 + 2)  and  ORBIT(b2 + 2)  are NEGATION DUALS.

    Proof.  The orbit generator is 26 = b1^2 = b2, and b1^3 = 1, so

        26 * (b2 + 2) = b1^2 (b1^2 + 2) = b1^4 + 2 b1^2 = b1 + 2 b2
        -(b1 + 2)     = -b1 - 2

    These agree iff 2(b1 + b2 + 1) = 0, i.e. iff b1 + b2 = -1 -- which is
    exactly Vieta on x^2 + x + 1.  So -(b1+2) = 26(b2+2) lies in the orbit
    of b2+2, and the two slope orbits are negation duals.  QED.

    Concretely: -(10+2) = -12 = 25, and 26 * 28 = 728 = 25 (mod 37).

    So T333's two admissible bases and T331's negation duality are the SAME
    involution seen twice: inverting the base (10 <-> 26, since 10*26 = 1)
    negates the slope orbit (SA_ST_A <-> SA_ST_B).

=== THE LAW IS UNIVERSAL, NOT A PROPERTY OF 37 ===

    The proof used only b1^3 = 1, b2 = b1^2, and b1 + b2 = -1.  All three
    hold for every prime p == 1 (mod 3).  Verified for

        p = 7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109, 127

    -- the slope orbits are negation duals in every one.  By the repo's own
    forcing taxonomy this is TIER A: true for every p == 1 (mod 3), and
    therefore carrying no information about 37 specifically.  Recorded that
    way deliberately; the draft's "tier 1" is right in its own scheme but
    does not distinguish universal from 37-specific, and that distinction is
    the whole point of the forced-check screen.

=== WHAT IS 37-SPECIFIC, AND ITS GRADE ===

    37 supplies the NAMES.  Its two slope orbits happen to be SA_ST_A and
    SA_ST_B -- the sovereign pair.  Is that worth anything?

        orbits meeting the sovereign sets: C3, SA_ST_A, SA_ST_B  (3 of 12)
        negation-dual pairs:                                      6
        pairs with BOTH members sovereign:   {SA_ST_A, SA_ST_B}   1 of 6

    The slopes are forced to be a dual pair (above), so the only question is
    WHICH of the 6 pairs.  They hit the unique both-sovereign pair:

        selectivity     1 in 6,  2.58 bits
        sample size     n = 1
        pre-registered  NO -- noticed after the slopes were computed

    SUGGESTIVE, NOT ESTABLISHED, and weaker than the row-5 match (5.21
    bits) which is itself only suggestive.  C3 is sovereign too but its
    dual D7 = {7,33,34} is not, so a hit on C3/D7 would have been half a
    hit; the space is small and the target was chosen afterwards.

    Recorded at that grade so the sovereign pairing is not quoted later as
    though it were the forced half.  The forced half is the duality.  The
    names are 1-in-6.

=== FALSIFICATION ===
    A prime p == 1 (mod 3) whose two slope orbits are not negation duals.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY_SET = {frozenset(v): k for k, v in ORBITS.items()}
ANCHORS, TARGETS = {4, 9, 25, 30}, {3, 12, 21, 30}


def slope_orbits(p):
    """(b1, b2, orbit of b1+2, orbit of b2+2) for a prime p == 1 mod 3."""
    roots = [b for b in range(p) if (b * b + b + 1) % p == 0]
    if len(roots) != 2:
        return None
    b1, b2 = roots
    if (b1 * b1) % p != b2:
        b1, b2 = b2, b1                      # ensure b2 = b1^2
    g = b2                                   # the orbit generator
    O = lambda s: {(s * pow(g, k, p)) % p for k in range(3)}
    return b1, b2, O(b1 + 2), O(b2 + 2)


def run():
    from math import log2

    # --- the law at 37 ---
    b1, b2, O1, O2 = slope_orbits(P)
    assert (b1, b2) == (10, 26)
    assert (b1 * b2) % P == 1                          # the bases are inverses
    assert (b1 + b2) % P == P - 1                      # Vieta: b1 + b2 = -1
    assert pow(b1, 3, P) == 1 and (b1 * b1) % P == b2
    assert O1 == set(ORBITS['SA_ST_A']) and O2 == set(ORBITS['SA_ST_B'])
    assert {(P - x) % P for x in O1} == O2              # negation duals
    # the forced step, concretely and symbolically
    assert (-(b1 + 2)) % P == 25 and (26 * (b2 + 2)) % P == 25
    assert (26 * (b2 + 2)) % P == (b1 + 2 * b2) % P
    assert ((b1 + 2 * b2) - (-(b1 + 2))) % P == (2 * (b1 + b2 + 1)) % P == 0
    # the sovereign memberships the draft cites
    assert set(ORBITS['SA_ST_A']) & ANCHORS == {9}
    assert set(ORBITS['SA_ST_A']) & TARGETS == {12}
    assert set(ORBITS['SA_ST_B']) & ANCHORS == {25}
    assert set(ORBITS['SA_ST_B']) & TARGETS == {21}
    assert (b1 + 2) % P == 12 and (b2 + 2) % P == 28 == (-9) % P

    # --- the law is universal over p == 1 (mod 3) ---
    PRIMES = (7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109, 127)
    for p in PRIMES:
        assert p % 3 == 1, p
        r = slope_orbits(p)
        assert r is not None, p
        c1, c2, A, B = r
        assert (c1 + c2) % p == p - 1                  # Vieta everywhere
        assert (c1 * c2) % p == 1
        assert {(p - x) % p for x in A} == B, p        # duals everywhere
    # so it says nothing about 37 in particular
    assert 37 in PRIMES and len(PRIMES) > 1

    # --- the 37-specific part, graded ---
    sov = [n for n, o in ORBITS.items() if set(o) & (ANCHORS | TARGETS)]
    assert sorted(sov) == ['C3', 'SA_ST_A', 'SA_ST_B']
    pairs = {frozenset((n, BY_SET[frozenset((P - x) % P for x in o)]))
             for n, o in ORBITS.items()}
    assert len(pairs) == 6
    both = [p for p in pairs if all(x in sov for x in p)]
    assert len(both) == 1 and both[0] == frozenset(('SA_ST_A', 'SA_ST_B'))
    assert abs(log2(6 / 1) - 2.585) < 0.01
    assert log2(6) < log2(37)                          # weaker than row 5
    # C3 is sovereign but its dual is not
    assert BY_SET[frozenset((P - x) % P for x in ORBITS['C3'])] == 'D7'
    assert 'C3' in sov and 'D7' not in sov

    print("All assertions passed.\n")
    print("THEOREM 334.  Inverting the base negates the slope orbit.\n")
    print(f"   admissible bases (T333): {b1}, {b2}   and {b1} x {b2} == 1,")
    print(f"   so the two bases are INVERSES.  Vieta: {b1} + {b2} == -1.\n")
    print(f"   base {b1} -> slope {b1+2:2d}  {BY_SET[frozenset(O1)]}"
          f"   anchor 9,  target 12")
    print(f"   base {b2} -> slope {b2+2:2d}  {BY_SET[frozenset(O2)]}"
          f"   anchor 25, target 21")
    print(f"   negation duals: {{(37-x) for x in O1}} == O2 -> True\n")
    print("   FORCED, from Vieta alone:")
    print("     26(b2+2) = b1^2(b1^2+2) = b1^4 + 2b1^2 = b1 + 2b2   (b1^3=1)")
    print("     -(b1+2)  = -b1 - 2")
    print("     equal  <=>  2(b1 + b2 + 1) = 0  <=>  b1 + b2 = -1")
    print("   concretely: -(10+2) = 25, and 26 x 28 = 728 = 25 (mod 37).\n")
    print("   So T333's two bases and T331's negation duality are ONE")
    print("   involution seen twice: base inversion induces orbit negation.\n")
    print("  BUT THE LAW IS UNIVERSAL -- it uses only b^3=1 and b1+b2=-1")
    print("   verified for p = " + ", ".join(map(str, PRIMES)))
    print("   duals in every one.  TIER A by the repo's forcing taxonomy:")
    print("   true for every p == 1 (mod 3), so it carries NO information")
    print("   about 37.  The draft's 'tier 1' is right in its own scheme but")
    print("   does not separate universal from 37-specific.\n")
    print("  WHAT IS 37-SPECIFIC: THE NAMES.  GRADED.")
    print(f"   orbits meeting the sovereign sets: {sorted(sov)}  (3 of 12)")
    print(f"   negation-dual pairs: {len(pairs)}")
    print(f"   pairs with BOTH members sovereign: 1 -> {sorted(both[0])}")
    print(f"   the slopes are FORCED to be a dual pair, so the only question")
    print(f"   is which of the {len(pairs)}.  They hit the unique one.")
    print(f"     selectivity    1 in {len(pairs)} = {log2(6):.2f} bits")
    print(f"     sample size    n = 1")
    print(f"     pre-registered NO -- noticed after the slopes were computed")
    print(f"   SUGGESTIVE, NOT ESTABLISHED -- and weaker than the row-5")
    print(f"   match at {log2(37):.2f} bits, which is itself only suggestive.")
    print(f"   (C3 is sovereign but its dual D7 is not, so a C3/D7 landing")
    print(f"   would have been half a hit.  Small space, target chosen after.)")
    print(f"\n   The forced half is the DUALITY.  The names are 1-in-6.")


if __name__ == "__main__":
    run()

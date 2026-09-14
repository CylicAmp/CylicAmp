# CLASS: THEOREM
"""
Theorem 332: the 6/6 split of T331 is FORCED, and exactly two orbits are
inversion-closed
Author: Michael Warren Song (CyclicAmp)

T331 observed that six 137-orbits sum to 37 and six sum to 74.  It did not
say why the halves are equal.  They are forced, by one line.

=== THE 6/6 SPLIT IS FORCED BY 666 ===

    The twelve orbits partition F_37*, so their sums total

        1 + 2 + ... + 36  =  36 x 37 / 2  =  666  =  18 x 37

    Each orbit sums to 37 or 74 (T331).  If a of them sum to 37:

        37a + 74(12 - a) = 666
        888 - 37a        = 666
        a                = 6

    So the halves are EQUAL of necessity.  Six and six is not an observed
    balance, it is the only solution.  T331 recorded it as a count; this is
    the reason.

    (666 also appears in T326 as the rotation-class sum of 123, where it is
    111 x (1+2+3).  Both are 18 x 37.  Recorded as a collision of small
    numbers with two different derivations, not as one mechanism.)

=== THE CLOSING CLAIM OF THE CANON DRAFT IS FALSE ===

    The draft ends: "Because no orbit in F_37* contains its own modular
    inverse, negation acts as a fixed-point-free involution."

    The conclusion is right and the reason is wrong -- it swaps INVERSE for
    NEGATIVE.  Two orbits are inversion-closed:

        IC    = {1, 10, 26}    inverses {1, 26, 10}    closed
        NEG_H = {11, 27, 36}   inverses {27, 11, 36}   closed

    IC is inversion-closed because it IS the subgroup <10>.  NEG_H = -IC is
    closed because (-u)^-1 = -u^-1.  So the premise as written fails on the
    first orbit in the table.

    The draft's OTHER statement of the same point is correct and is the one
    to keep:  -O = O iff -1 is in <10> = {1,10,26}, and 36 is not, so no
    orbit is self-negative and negation is fixed-point-free.  Negation and
    inversion are different maps and only one of them is fixed-point-free
    here.

=== AND THE COUNT OF TWO IS ITSELF FORCED ===

    A coset gO is inversion-closed iff g^-1 O = g O iff g^2 is in O = <10>.
    In the quotient F_37* / <10>, cyclic of order 36/3 = 12, that says the
    image of g squares to the identity.  A cyclic group of order 12 has
    exactly two elements of order dividing 2.  So EXACTLY TWO orbits are
    inversion-closed, never one and never three.

    The two are IC and NEG_H -- which are each other's negation duals
    (T331).  Inversion-closure and negation-duality meet at exactly one
    pair, and it is the pair built on 1 and -1.

=== FALSIFICATION ===
    A third inversion-closed orbit; or a 37/74 split other than 6/6.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY_SET = {frozenset(v): k for k, v in ORBITS.items()}


def run():
    inv = {x: pow(x, P - 2, P) for x in range(1, P)}

    # --- the orbits really do partition F_37* ---
    allres = sorted(x for o in ORBITS.values() for x in o)
    assert allres == list(range(1, P))
    assert sum(allres) == 666 == 36 * 37 // 2 == 18 * P

    # --- the 6/6 split is forced ---
    sums = {nm: sum(o) for nm, o in ORBITS.items()}
    assert set(sums.values()) == {37, 74}
    a = [x for x in range(13) if 37 * x + 74 * (12 - x) == 666]
    assert a == [6]                                  # the ONLY solution
    assert len([n for n, s in sums.items() if s == 37]) == 6
    assert len([n for n, s in sums.items() if s == 74]) == 6
    # the T326 collision, two derivations of the same integer
    assert 111 * (1 + 2 + 3) == 666 == 18 * P
    assert 123 + 312 + 231 == 666

    # --- the draft's premise is false: two orbits ARE inversion-closed ---
    closed = sorted(nm for nm, o in ORBITS.items()
                    if {inv[x] for x in o} == set(o))
    assert closed == ['IC', 'NEG_H'], closed
    assert {inv[x] for x in ORBITS['IC']} == {1, 26, 10}
    assert inv[10] == 26 and inv[26] == 10 and inv[1] == 1
    assert {inv[x] for x in ORBITS['NEG_H']} == set(ORBITS['NEG_H'])
    for u in ORBITS['IC']:                           # (-u)^-1 = -u^-1
        assert inv[(P - u) % P] == (P - inv[u]) % P

    # --- but the conclusion holds, via NEGATION, which is the right map ---
    assert 36 not in (1, 10, 26)                     # -1 not in <10>
    for nm, o in ORBITS.items():
        assert {(P - x) % P for x in o} != set(o)    # fixed-point-free
    assert BY_SET[frozenset((P - x) % P for x in ORBITS['IC'])] == 'NEG_H'

    # --- the count of two is forced by the quotient ---
    assert (P - 1) // 3 == 12                        # |F* / <10>| = 12
    # g O is inversion-closed iff g^2 in <10>
    sub = {1, 10, 26}
    gsq = sorted({g for g in range(1, P) if (g * g) % P in sub})
    cosets = {frozenset((g * s) % P for s in sub) for g in gsq}
    assert len(cosets) == 2                          # exactly two, forced
    assert {BY_SET[c] for c in cosets} == {'IC', 'NEG_H'}
    # a cyclic group of order 12 has exactly 2 elements of order dividing 2
    assert len([j for j in range(12) if (2 * j) % 12 == 0]) == 2

    print("All assertions passed.\n")
    print("THEOREM 332.  Six and six is forced, not observed.\n")
    print(f"   the 12 orbits partition F_37*, so their sums total")
    print(f"     1 + ... + 36 = 36 x 37 / 2 = 666 = 18 x 37")
    print(f"   each sum is 37 or 74 (T331), so with a orbits at 37:")
    print(f"     37a + 74(12-a) = 666  ->  888 - 37a = 666  ->  a = 6")
    print(f"   the only solution in 0..12: {a}\n")
    print(f"   (666 is also T326's rotation-class sum of 123 = 111 x 6.")
    print(f"    Two derivations of one integer -- a collision, not a")
    print(f"    mechanism.)\n")
    print("  THE DRAFT'S CLOSING PREMISE IS FALSE")
    print("   'no orbit contains its own modular inverse' -- two do:")
    for nm in closed:
        print(f"     {nm:6s} {ORBITS[nm]}  inverses"
              f" {tuple(inv[x] for x in ORBITS[nm])}")
    print("   IC is inversion-closed because it IS the subgroup <10>;")
    print("   NEG_H = -IC is closed because (-u)^-1 = -u^-1.\n")
    print("   The conclusion still holds, by the draft's OTHER statement,")
    print("   which is the correct one: -O = O iff -1 in <10>, and 36 is")
    print("   not in {1,10,26}, so negation is fixed-point-free on orbits.")
    print("   Negation and inversion are different maps; only negation is")
    print("   fixed-point-free here.\n")
    print("  AND TWO IS FORCED")
    print("   gO is inversion-closed iff g^2 in <10>, i.e. the image of g in")
    print("   F_37*/<10> -- cyclic of order 12 -- squares to the identity.")
    print("   A cyclic group of order 12 has exactly 2 such elements, so")
    print("   exactly 2 orbits are inversion-closed: IC and NEG_H.")
    print("   They are each other's negation duals, so inversion-closure and")
    print("   negation-duality meet at one pair, the one built on 1 and -1.")


if __name__ == "__main__":
    run()

# CLASS: THEOREM
"""
Theorem 343: T126, T128, T331, T333, T340, T341 are one congruence --
37 == 1 (mod 3)
Author: Michael Warren Song (CyclicAmp)

The reconciliation pass over T126 (j-function) and T128 (Loeschian norms),
run after T138 was found to be prior art for T329 and T339.  It collapses
more than expected.

=== THE LOESCHIAN FORM IS Phi_3 ===

    T128 studies the Loeschian norms, values of the Eisenstein norm form

        N(a,b) = a^2 + a b + b^2

    Setting b = 1 gives a^2 + a + 1 = Phi_3(a), identically.  So T128's
    subject and the polynomial T333/T340/T341 were built on are the same
    object, seen with b specialised or not.

=== 37 IS ITSELF A LOESCHIAN NUMBER ===

        37 = 3^2 + 3*4 + 4^2 = 9 + 12 + 16

    so 37 splits in the Eisenstein integers Z[w].  That is not an extra
    fact; it is the same one as everything below.

=== ONE CONGRUENCE, SIX FACES ===

    Every line here is equivalent to 37 == 1 (mod 3):

      -3 is a quadratic residue mod 37        x^2 == 34 for x = 16, 21
      Phi_3 has roots mod 37                  10 and 26           (T333)
      elements of order 3 exist, 10^3 == 1
      => twelve orbits of size 3                            (T138, T331)
      => each orbit sums to zero, 1+10+26 = 37              (T331, T340)
      => the Koopman spectrum is {1, w, w^2}                (T341)
      37 = a^2+ab+b^2, i.e. 37 splits in Z[w]               (T128)

    The bridge between the quadratic-residue face and the cube-root face is
    one line: if Phi_3(w) = 0 then

        (2w+1)^2 = 4w^2 + 4w + 1 = 4(w^2+w) + 1 = 4(-1) + 1 = -3

    so 2w+1 is a square root of -3.  With w = 10 that is 21, and
    21^2 = 441 == 34 == -3 (mod 37).  Verified.

    These are one congruence wearing six faces, and it holds for every
    prime p == 1 (mod 3) -- TIER A.  What 37 supplies is only that the
    order-3 element happens to be 10, the base we write in (T333).

=== T126's j-VALUES, NOW EXPLAINED ===

    T126 recorded, as observations:

        j(i) = 1728 == 26, in IC
        j(w) = 0    == 0,  the SEAM

    The first is FORCED by the T138/T339 index, not a coincidence.
    1728 = 12^3, idx(12) = 4, and cubing triples the index:

        idx(12^3) = 3 x 4 = 12 == 0 (mod 12)  =>  IC

    Any cube lands in index {0,3,6,9}, and 12 in particular lands on 0.
    The second is not a coincidence either: j vanishes at w because w is
    the CM point of discriminant -3 -- the same w as Phi_3, the same
    Eisenstein structure as T128.  Both j-values are Eisenstein facts.

=== A NON-INDEPENDENCE WORTH FLAGGING ===

    The square roots of -3 are 16 and 21, lying in SA_ST_A and SA_ST_B --
    the sovereign pair, which T334 also landed on.  That is NOT a second
    sighting.  T334's slope was w+2 = 12 and the root here is 2w+1 = 21;
    both are affine functions of the same w = 10, so they cannot
    corroborate each other.  Also forced: the two roots are negatives of
    each other (16+21 = 37), and negation swaps dual orbits (T331), so once
    one lands in SA_ST_A the other must land in SA_ST_B.  The only free
    content is "16 is in SA_ST_A" -- 1 in 12, post hoc, n = 1.

=== T128's SPEED-OF-LIGHT SECTION IS A UNIT ARTIFACT ===

    T128 records c = 299792458, c mod 37 = 32 in SEED, digit sum 55 == 18
    also in SEED.  The arithmetic is right and the reading is not
    admissible: c has that numerical value only because the metre and the
    second are defined as they are.  This is the same class of artifact as
    "37 C is a Celsius calibration numeral", which the corpus already
    excised in the biology audit.  Consistency requires the same grade
    here.  Flagged, not deleted -- the computation stands, the inference
    does not.

=== FALSIFICATION ===
    A face above not equivalent to 37 == 1 (mod 3); or idx(12^3) != 0.
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


def run():
    # --- the Loeschian form is Phi_3 ---
    N = lambda a, b: a * a + a * b + b * b
    phi3 = lambda x: x * x + x + 1
    for a in range(-20, 21):
        assert N(a, 1) == phi3(a)

    # --- 37 is Loeschian ---
    reps = [(a, b) for a in range(1, 10) for b in range(1, 10) if N(a, b) == P]
    assert sorted(reps) == [(3, 4), (4, 3)]
    assert N(3, 4) == 9 + 12 + 16 == 37

    # --- the six faces, all equivalent to 37 == 1 mod 3 ---
    assert P % 3 == 1
    roots_m3 = [x for x in range(P) if (x * x) % P == (-3) % P]
    assert roots_m3 == [16, 21]
    roots_phi3 = [b for b in range(P) if phi3(b) % P == 0]
    assert roots_phi3 == [10, 26]
    assert pow(10, 3, P) == 1 and pow(10, 1, P) != 1
    assert len({frozenset({x, (10 * x) % P, (100 * x) % P})
                for x in range(1, P)}) == 12
    assert (1 + 10 + 26) % P == 0 and 1 + 10 + 26 == P
    # the bridge: (2w+1)^2 = -3
    for w in roots_phi3:
        assert (2 * w + 1) ** 2 % P == (-3) % P
        assert (2 * w + 1) % P in roots_m3
    assert 21 * 21 == 441 and 441 % P == 34 == (-3) % P
    # Tier A: the same chain for every p == 1 mod 3
    for q in (7, 13, 19, 31, 43, 61, 67, 73):
        assert q % 3 == 1
        assert [b for b in range(q) if (b * b + b + 1) % q == 0]
        assert [(a, b) for a in range(1, q) for b in range(1, q)
                if N(a, b) == q]

    # --- T126's j-values ---
    assert 1728 == 12 ** 3 and 1728 % P == 26 and BY[26] == 'IC'
    assert IDX[BY[12]] == 4
    assert (3 * IDX[BY[12]]) % 12 == 0 == IDX['IC']
    assert IDX[BY[1728 % P]] == 0
    for x in range(1, P):                       # cubing triples the index
        assert IDX[BY[pow(x, 3, P)]] == (3 * IDX[BY[x]]) % 12
    assert 0 % P == 0                           # j(w) = 0 is the SEAM

    # --- the non-independence ---
    assert BY[16] == 'SA_ST_A' and BY[21] == 'SA_ST_B'
    assert 16 + 21 == P                         # negatives, so duals forced
    assert (2 * 10 + 1) == 21 and (10 + 2) == 12   # both affine in w = 10
    assert BY[12] == 'SA_ST_A'                  # T334's slope, same source

    # --- the unit artifact ---
    c = 299792458
    assert c % P == 32 and BY[32] == 'SEED'
    assert sum(map(int, str(c))) == 55 and 55 % P == 18 and BY[18] == 'SEED'

    print("All assertions passed.\n")
    print("THEOREM 343.  Six theorems, one congruence.\n")
    print("  THE LOESCHIAN FORM IS Phi_3")
    print("   N(a,b) = a^2+ab+b^2, and N(a,1) = a^2+a+1 = Phi_3(a).")
    print("   T128's subject and T333/T340/T341's polynomial are one object.\n")
    print(f"  37 IS LOESCHIAN:  37 = 3^2 + 3*4 + 4^2 = 9 + 12 + 16")
    print( "   so 37 splits in the Eisenstein integers Z[w].\n")
    print("  ONE CONGRUENCE, SIX FACES  (all == 37 == 1 mod 3)")
    print(f"   -3 is a QR mod 37            x = {roots_m3}")
    print(f"   Phi_3 has roots mod 37       {roots_phi3}              (T333)")
    print(f"   order-3 elements exist       10^3 == 1")
    print(f"   twelve orbits of size 3                           (T138,T331)")
    print(f"   each sums to zero            1+10+26 = 37         (T331,T340)")
    print(f"   Koopman spectrum {{1,w,w^2}}                        (T341)")
    print(f"   37 = a^2+ab+b^2                                   (T128)")
    print( "   bridge: (2w+1)^2 = 4(w^2+w)+1 = -3, so 2w+1 = sqrt(-3);")
    print(f"           w = 10 gives 21, and 21^2 = 441 == 34 == -3.\n")
    print( "   TIER A -- the whole chain holds for every p == 1 (mod 3).")
    print( "   What 37 supplies is only that the order-3 element is 10,")
    print( "   the base we write in (T333).\n")
    print("  T126's j-VALUES, EXPLAINED RATHER THAN OBSERVED")
    print(f"   j(i) = 1728 = 12^3 == 26 in IC -- FORCED: idx(12) = 4 and")
    print(f"   cubing triples the index, 3x4 = 12 == 0 (mod 12) -> IC.")
    print(f"   j(w) = 0 -> SEAM -- w is the CM point of discriminant -3,")
    print(f"   the same w as Phi_3.  Both are Eisenstein facts.\n")
    print("  NON-INDEPENDENCE FLAGGED")
    print(f"   sqrt(-3) = {roots_m3} lands in SA_ST_A / SA_ST_B, the pair T334")
    print( "   also hit.  NOT a second sighting: T334's slope is w+2 = 12 and")
    print( "   this root is 2w+1 = 21, both affine in the same w = 10.  And")
    print( "   16+21 = 37, so duality forces the second once the first is")
    print( "   placed.  Free content: '16 is in SA_ST_A', 1 in 12, post hoc.\n")
    print("  T128's SPEED OF LIGHT: UNIT ARTIFACT")
    print(f"   c = {c}, c mod 37 = {c%P} in SEED, digit sum 55 == 18 in SEED.")
    print( "   Arithmetic right, reading inadmissible: c has that value only")
    print( "   because the metre and second are defined so.  Same class as")
    print( "   '37 C is a Celsius numeral', already excised in the biology")
    print( "   audit.  Flagged for consistency -- computation stands, the")
    print( "   inference does not.")


if __name__ == "__main__":
    run()

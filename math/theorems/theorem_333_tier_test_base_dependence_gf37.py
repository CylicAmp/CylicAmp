# CLASS: THEOREM
"""
Theorem 333: the tier boundary is a TEST, not a label -- and running it
shows base 10 is not arbitrary
Author: Michael Warren Song (CyclicAmp)

(333 = 9 x 37, the CRT modulus of the three-tier scheme itself and the
T316 seed-class modulus.  Noted, not leaned on.)

The proposed audit architecture is right:

    Tier 1  coordinate-free invariants of F_37*, its cosets, negation, CRT
    Tier 2  exact but representation-dependent, with stated expiry
    Tier 3  observations awaiting a generative rule

What it lacks is a procedure.  A tier assigned by inspection is a label; a
tier assigned by a test is a fact.  The discriminator:

    RE-RUN THE CONSTRUCTION IN ANOTHER BASE.
    Survives every base  -> Tier 1.
    Breaks              -> Tier 2, and the break point IS the expiry.

=== RUNNING IT ON T326 ===

    In base b, an AP triple with digits (a, a+d, a+2d) is

        a(b^2 + b + 1) + d(b + 2)

    The start digit vanishes mod 37 iff b^2 + b + 1 == 0 (mod 37), whose
    roots are b = 10 and b = 26 -- exactly the primitive cube roots of 1,
    which are exactly IC \\ {1}, the non-identity elements of <10>.

        base 10   R3 = 111 = 3 x 37     residue 12d
        base 26   R3 = 703 = 19 x 37    residue 28d

    SO BASE 10 IS NOT ARBITRARY HERE.  It works because 10 generates the
    order-3 subgroup.  T326 is Tier 2, but its base-dependence is itself a
    Tier 1 fact: the admissible bases are a named orbit.  That is a
    stronger statement than "this is a decimal artifact", and it is only
    visible once the tier test is actually run.

=== RUNNING IT ON T328's PREFIX IDENTITY ===

    The claim is an INTEGER equality: the two-digit prefix equals the
    residue.  The prefix is d(b+2), so the claim holds while d(b+2) < 37:

        base 10   12d < 37   ->  d = 1, 2, 3      value 123, 246, 369
        base 26   28d < 37   ->  d = 1 only

    Base 10 gives three rows, base 26 gives one.  And base 10 is where two
    INDEPENDENT bounds coincide:

        digit range     3d < b   ->  d <= 3   (base 10);  d <= 8 (base 26)
        residue bound   d(b+2) < 37 -> d <= 3 (base 10);  d <= 1 (base 26)

    In base 10 they agree exactly at 3.  In base 26 they disagree by seven.
    The three-row stack of T327 exists because those two unrelated limits
    happen to meet, and the tier test is what exposes that as two facts
    rather than one.

=== THE PRE-REGISTERED ROW-5 HARNESS (T330 Tier 3) ===

    T330 graded the row-5 match as unfalsifiable for want of a generative
    rule.  The rule does not exist yet, so the TEST is registered now,
    before any candidate, and its pass condition is fixed here:

      A candidate rule f(rows) -> int passes iff, with no tuning:
        (1) f([123,246,369])  == 38515            exact reproduction
        (2) f([123,246,369])  == 35  (mod 37)      implied by (1)
        (3) f([246,492,738])  == 33  (mod 37)      the d=2 transfer
      Any failure terminates that candidate.  Passing justifies further
      work; it does not by itself establish a theorem.

    `check_row5_rule` below implements this.  It is exercised against two
    deliberate failures so the harness is shown to reject, not merely to
    exist.

=== ONE SLIP IN THE DRAFT ===

    "Since 3 x 37 = 111, the map x -> 37 - x induces an exact fixed-point-
    free involution."  The 111 explains the SUM pairing (37 + 74 = 111).
    It does not explain fixed-point-freeness, which is T332's reason:
    -O = O would need -1 in <10> = {1,10,26}, and 36 is not there.  Two
    facts, one clause, again.

=== FALSIFICATION ===
    Any assert below; or a base b not in {10,26} mod 37 in which the AP
    start digit vanishes.
"""

P = 37
IC = {1, 10, 26}


def ap_value(a, d, b):
    """digits (a, a+d, a+2d) read in base b."""
    return a * b * b + (a + d) * b + (a + 2 * d)


def check_row5_rule(f):
    """Pre-registered gate for a candidate row-5 generator. Returns
    (passed, report). Registered before any candidate rule existed."""
    rep = []
    try:
        v1 = f([123, 246, 369])
        v2 = f([246, 492, 738])
    except Exception as e:                       # a rule that cannot run fails
        return False, [f"rule raised {type(e).__name__}: {e}"]
    ok1 = v1 == 38515
    ok2 = v1 % P == 35
    ok3 = v2 % P == 33
    rep.append(f"(1) f(d=1 stack) = {v1}, want 38515        {'PASS' if ok1 else 'FAIL'}")
    rep.append(f"(2) that mod 37  = {v1 % P}, want 35           {'PASS' if ok2 else 'FAIL'}")
    rep.append(f"(3) f(d=2 stack) = {v2} == {v2 % P}, want 33   {'PASS' if ok3 else 'FAIL'}")
    return (ok1 and ok2 and ok3), rep


def run():
    # --- the tier test on T326: which bases make the start digit vanish ---
    roots = [b for b in range(P) if (b * b + b + 1) % P == 0]
    assert roots == [10, 26]
    assert set(roots) == IC - {1}
    assert all(pow(b, 3, P) == 1 and b != 1 for b in roots)
    for b in roots:
        assert (b * b + b + 1) % P == 0
        for a in range(1, 4):
            for d in range(1, 3):
                assert ap_value(a, d, b) % P == (d * (b + 2)) % P
    assert 111 == 3 * P and 703 == 19 * P
    # and in a base outside the orbit the start digit does NOT vanish
    for b in (2, 8, 12, 16):
        assert (b * b + b + 1) % P != 0
        assert ap_value(1, 1, b) % P != ap_value(2, 1, b) % P

    # --- the tier test on T328's prefix identity (an INTEGER equality) ---
    for b, last in ((10, 3), (26, 1)):
        for d in range(1, 5):
            val = ap_value(d, d, b)
            prefix = d * (b + 2)                 # the two leading digits
            assert val % P == prefix % P         # residues always agree
            assert (prefix == val % P) == (d <= last), (b, d)
        assert last == 36 // (b + 2)
    assert 36 // 12 == 3 and 36 // 28 == 1
    # the two independent bounds, and where they coincide
    assert (10 - 1) // 3 == 3 and 36 // 12 == 3          # base 10: agree
    assert (26 - 1) // 3 == 8 and 36 // 28 == 1          # base 26: disagree
    assert ap_value(1, 1, 10) == 123 and ap_value(3, 3, 10) == 369

    # --- the pre-registered harness must REJECT bad rules ---
    passed, _ = check_row5_rule(lambda rows: 38515)      # constant: ignores input
    assert not passed                                    # fails the d=2 leg
    passed, _ = check_row5_rule(lambda rows: sum(rows))  # the stack sum itself
    assert not passed                                    # 738 != 38515
    # and ACCEPT a rule meeting the spec, so the gate is not vacuous
    spec = {738: 38515, 1476: 33 + 37 * 100}
    passed, _ = check_row5_rule(lambda rows: spec[sum(rows)])
    assert passed
    assert 246 + 492 + 738 == 1476 and 1476 % P == 33
    assert sum([123, 246, 369]) == 738 and 738 % P == 35

    # --- the slip ---
    assert 37 + 74 == 111 == 3 * P                       # what 111 explains
    assert 36 not in IC                                  # what it does not

    print("All assertions passed.\n")
    print("THEOREM 333.  The tier boundary is a test.\n")
    print("  DISCRIMINATOR: re-run the construction in another base.")
    print("  survives every base -> Tier 1;  breaks -> Tier 2, and the")
    print("  break point is the expiry.\n")
    print("  T326 UNDER THE TEST")
    print("   base-b AP triple = a(b^2+b+1) + d(b+2)")
    print(f"   start digit vanishes iff b^2+b+1 == 0 (mod 37), roots {roots}")
    print(f"   those are the primitive cube roots of 1 = IC minus identity")
    for b in roots:
        print(f"     base {b:2d}:  R3 = {b*b+b+1:3d} = {(b*b+b+1)//P:2d} x 37"
              f"   residue {(b+2)%P}d")
    print("   base 10 is not arbitrary -- it works because 10 generates IC.")
    print("   T326 is Tier 2, but its base-dependence is a Tier 1 fact.\n")
    print("  T328's PREFIX IDENTITY UNDER THE TEST  (integer equality)")
    for b in roots:
        rows = [d for d in range(1, 9) if d * (b + 2) < P]
        print(f"     base {b:2d}: prefix {b+2}d < 37 -> d in {rows}"
              f"   ({len(rows)} row{'s' if len(rows)>1 else ''})")
    print("   two INDEPENDENT bounds:")
    print(f"     digit range   3d < b      -> d <= 3 (base 10), 8 (base 26)")
    print(f"     residue bound d(b+2) < 37 -> d <= 3 (base 10), 1 (base 26)")
    print("   base 10 is where they coincide.  T327's three-row stack exists")
    print("   because two unrelated limits happen to meet at 3.\n")
    print("  PRE-REGISTERED ROW-5 GATE  (fixed before any candidate exists)")
    for name, rule in (("constant 38515", lambda r: 38515),
                       ("the stack sum", lambda r: sum(r))):
        ok, rep = check_row5_rule(rule)
        print(f"   candidate: {name}  ->  {'PASS' if ok else 'REJECTED'}")
        for line in rep:
            print(f"      {line}")
    print("\n   The gate rejects. It is a real test, not a placeholder.\n")
    print("  SLIP IN THE DRAFT")
    print("   '3 x 37 = 111' explains the SUM pairing 37 + 74 = 111.")
    print("   It does not explain fixed-point-freeness -- that is -1 not in")
    print("   <10> (T332).  Two facts in one clause.")


if __name__ == "__main__":
    run()

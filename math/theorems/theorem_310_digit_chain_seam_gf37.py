# CLASS: THEOREM
"""
Theorem 310: aba = 111a always hits SEAM, for every digit a
Author: Michael Warren Song (CyclicAmp)

STATEMENT
    For any digit a in 1..9, the digit-chain skill's "aba" value at a=b=a
    is 111*a. Since 111 = 3*37, 111a mod 37 = 0 for every a: always SEAM,
    never a named orbit. Cofactor 111a/37 = 3a exactly.

FORCED (definition + homomorphism, not new structure)
    111 = 3*37 is arithmetic (T302 already uses this: 111 = Phi_3(10)).
    "111*a mod 37 = 0 for all a" follows immediately: it says nothing
    about a. DR(111a) = DR(3a) (DR is multiplicative, forced), giving the
    repeating pattern 3,6,9,3,6,9,3,6,9 for a=1..9 -- also forced, not
    independent facts per a.

CONNECTION
    This is the same 111=3x37 fact behind theorem_303's block map
    (B_MULT=27=999/37) and the digit-chain skill's own stated closed form
    ("aba hits SEAM exactly when a=b, since aba=111a"). It is also why
    every "Series (N,N)" digit-chain audited in this session (N=1..9)
    showed aba=SEAM without exception -- not 9 separate coincidences, one
    forced fact instantiated 9 times.

FALSIFICATION
    Any assert below failing.
"""

P = 37


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def run():
    assert 111 == 3 * P
    for a in range(1, 10):
        aba = 111 * a
        assert aba % P == 0
        assert aba // P == 3 * a
        assert dr(aba) == dr(3 * a)

    print("All assertions passed.\n")
    print("a   aba=111a   mod37   cofactor=3a   DR")
    for a in range(1, 10):
        aba = 111 * a
        print(f"{a}   {aba:<9} {aba % P:<7} {aba // P:<12} {dr(aba)}")


if __name__ == "__main__":
    run()

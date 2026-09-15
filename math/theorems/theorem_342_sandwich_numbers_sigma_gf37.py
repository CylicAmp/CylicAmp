# CLASS: THEOREM
"""
Theorem 342: 26+27 and 8+9 are sigma, and both left sides are uniqueness
numbers -- with the GF(37) reading reported null
Author: Michael Warren Song (CyclicAmp)

Given:      26 + 27 = 53        8 + 9 = 17

=== BOTH ARE THE SOPHIE GERMAIN MAP ===

    n + (n+1) = 2n + 1 = sigma(n), the T337 map, identically.  So these two
    lines are sigma evaluated at 26 and at 8.  Nothing is being observed
    about addition; the sum of consecutive integers IS sigma.

        sigma(26) = 53      sigma(8) = 17

    53 is prime and Sophie Germain (2x53+1 = 107 is prime).
    17 is prime and NOT Sophie Germain (2x17+1 = 35 = 5 x 7).

=== BOTH LEFT SIDES ARE CLASSICAL UNIQUENESS NUMBERS ===

    This is the real content, and it is not a GF(37) fact.

    26 is the ONLY integer between a perfect square and a perfect cube:
    25 = 5^2 and 27 = 3^3.  Equivalently the Mordell equation

        y^2 = x^3 - 2

    has the single integral solution x = 3, y = +-5.  Claimed by Fermat,
    and a theorem.  Searched to x = 2000 here: one solution.

    8 and 9 are the ONLY consecutive perfect powers.  That is Catalan's
    conjecture, open from 1844 and proved by Mihailescu in 2002:
    x^a - y^b = 1 with all of x,y,a,b > 1 forces 3^2 - 2^3 = 1.  Searched
    over perfect powers below 10^6 here: the pair (8,9) and nothing else.

    So the two lines pair the unique square-cube sandwich with the unique
    consecutive-power pair -- the two classical statements about how close
    perfect powers can come.  27 - 25 = 2 and 9 - 8 = 1, the gap-2 and
    gap-1 cases.

=== THE 26 CONNECTION, GRADED ===

    26 = 137 mod 37 is this project's central multiplier, and 26 is also
    the unique square-cube sandwich number.  Two distinctions on one
    integer, from unrelated sources: one is forced arithmetic (137 - 111),
    the other is a hard theorem.

    Recorded as a property of 26 that belongs in its standing analysis, NOT
    as evidence.  There is no mechanism linking Mordell's equation to the
    137-map, the pairing is post hoc with n = 1, and "small integer carries
    two distinctions" is weak by construction.

=== THE GF(37) READING IS NULL, AND IS REPORTED AS SUCH ===

    Both inputs shift by +4 in the T339 orbit index:

        26 in IC      idx 0  ->  53 == 16 in SA_ST_A  idx 4
         8 in TESLA   idx 3  ->  17 == 17 in NQR17    idx 7

    That looks like a pattern and is not.  sigma's index shift over all 35
    admissible x is essentially uniform -- shift +4 occurs 3 times of 35,
    which is the expected rate (35/12 = 2.9).  Two draws landing on the
    same value of a near-uniform statistic is what two draws do.  NULL.

    Forced and worth noting instead: 26 - 8 = 18, and 18 is exactly the
    sigma-preimage of the seam, sigma(18) = 37 == 0 -- the residue T337
    had to exclude from admissibility.  Hence sigma(26) - sigma(8) =
    2 x 18 = 36 = |F_37*|.  Arithmetic, not a finding.

=== FALSIFICATION ===
    A second integer strictly between a perfect square and a perfect cube;
    a second consecutive pair of perfect powers; or a non-uniform index
    shift for sigma.
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


def is_prime(m):
    return m > 1 and all(m % k for k in range(2, int(m ** .5) + 1))


def run():
    from collections import Counter

    # --- consecutive sums ARE sigma ---
    for n in range(1, 200):
        assert n + (n + 1) == 2 * n + 1
    assert 26 + 27 == 53 == 2 * 26 + 1
    assert 8 + 9 == 17 == 2 * 8 + 1
    assert is_prime(53) and is_prime(2 * 53 + 1) == is_prime(107) is True
    assert is_prime(17) and not is_prime(2 * 17 + 1)
    assert 2 * 17 + 1 == 35 == 5 * 7

    # --- 26 is the unique square-cube sandwich ---
    assert 25 == 5 ** 2 and 27 == 3 ** 3 and 27 - 25 == 2
    sols = [(x, y) for x in range(2, 2000)
            for y in [int(round((x ** 3 - 2) ** .5))]
            if x ** 3 - 2 >= 0 and y * y == x ** 3 - 2]
    assert sols == [(3, 5)]                      # Mordell y^2 = x^3 - 2

    # --- 8, 9 are the only consecutive perfect powers ---
    pw = sorted({b ** e for b in range(2, 60) for e in range(2, 21)
                 if b ** e < 10 ** 6})
    assert [(a, b) for a, b in zip(pw, pw[1:]) if b - a == 1] == [(8, 9)]
    assert 9 - 8 == 1 and 8 == 2 ** 3 and 9 == 3 ** 2

    # --- the 26 coincidence, stated and graded ---
    assert 137 % P == 26 and 137 - 111 == 26 and 111 == 3 * P

    # --- the GF(37) reading is NULL ---
    def shift(x):
        return (IDX[BY[(2 * x + 1) % P]] - IDX[BY[x % P]]) % 12
    assert shift(26) == shift(8) == 4
    assert BY[26] == 'IC' and BY[53 % P] == 'SA_ST_A'
    assert BY[8] == 'TESLA' and BY[17] == 'NQR17'
    adm = [x for x in range(1, P) if (2 * x + 1) % P]
    assert len(adm) == 35
    dist = Counter(shift(x) for x in adm)
    assert dist[4] == 3                           # the expected rate
    assert max(dist.values()) - min(dist.values()) <= 1   # essentially uniform
    assert abs(dist[4] - 35 / 12) < 1

    # --- the forced gap fact ---
    assert 26 - 8 == 18 and (2 * 18 + 1) % P == 0     # 18 is the seam preimage
    assert 53 - 17 == 36 == 2 * 18 == P - 1

    print("All assertions passed.\n")
    print("THEOREM 342.  Both lines are sigma; both left sides are theorems.\n")
    print("   n + (n+1) = 2n+1 = sigma(n) identically, so")
    print("     26 + 27 = 53 = sigma(26)      8 + 9 = 17 = sigma(8)")
    print("   nothing is observed about addition -- the consecutive sum IS")
    print("   the T337 Sophie Germain map.")
    print("     53 prime, Sophie Germain (107 prime)")
    print("     17 prime, NOT Sophie Germain (35 = 5 x 7)\n")
    print("  THE LEFT SIDES ARE CLASSICAL UNIQUENESS NUMBERS")
    print("   26 is the ONLY integer between a perfect square and a cube:")
    print("     25 = 5^2, 27 = 3^3.  Mordell y^2 = x^3 - 2 has the single")
    print(f"     integral solution {sols[0]}; searched to x = 2000.")
    print("   8 and 9 are the ONLY consecutive perfect powers -- Catalan's")
    print("     conjecture, open 1844-2002, proved by Mihailescu.")
    print(f"     consecutive perfect powers below 10^6: {[(8,9)]}")
    print("   gap 2 and gap 1: the two classical statements about how close")
    print("   perfect powers can come.\n")
    print("  THE 26 CONNECTION, GRADED")
    print("   26 = 137 mod 37 is this project's multiplier AND the unique")
    print("   square-cube sandwich.  One is forced arithmetic, the other a")
    print("   hard theorem, and no mechanism joins them.  Recorded as a")
    print("   property of 26 for its standing analysis, NOT as evidence.\n")
    print("  THE GF(37) READING IS NULL")
    print(f"   26 in IC idx 0 -> 53 == 16 in SA_ST_A idx 4      shift +4")
    print(f"    8 in TESLA idx 3 -> 17 == 17 in NQR17 idx 7     shift +4")
    print(f"   looks like a pattern; is not.  sigma's index shift over the")
    print(f"   35 admissible x: {dict(sorted(dist.items()))}")
    print(f"   +4 occurs {dist[4]} times, the expected rate 35/12 = 2.9.")
    print(f"   Two draws agreeing on a near-uniform statistic is what two")
    print(f"   draws do.  NULL.\n")
    print("   forced instead: 26 - 8 = 18, the sigma-preimage of the seam")
    print("   (sigma(18) = 37 == 0, the residue T337 excludes), so")
    print("   sigma(26) - sigma(8) = 2 x 18 = 36 = |F_37*|.  Arithmetic.")


if __name__ == "__main__":
    run()

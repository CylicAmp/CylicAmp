# CLASS: THEOREM
"""
The ABCBA place-value grid: annihilators from 10^m + 1

PRIOR ART, checked first.  The mod-37 side of ABCBA is already the corpus's.
palindrome_gf37.py (declares THEOREM 56) gives the coefficient rule
ABCBA = 11(A+B) + 26C (mod 37) and the SEAM condition C = A + B, by the
power-class argument on 10^k mod 37.  theorem_158_counting_palindrome_seam.py
counts seams; theorem_160_aba_portal_palindromes.py owns the A0A..A9A sweep;
math/lemmas/aba_palindrome_walk.py owns aba + bab = 111(a+b) and
aba - bab = 91(a-b).  T328 and T330 record 12321 = 111^2 = (3*37)^2 = 9*37^2
with residue 0 and DR 9; T371 gives its rotation cycle a D_5 action.  None of
that is restated as new here.

WHAT IS NEW is the INTEGER side: the grid as a place-value lattice, the
annihilator table that organises every divisibility rule at once, and three
exact statements that follow from it -- the 101 rule, the 37^2 layer, and the
uniqueness of 12321 among palindromic squares as a seam.

====================================================================
I.  THE LATTICE
====================================================================

    abcba = 10001 a + 1010 b + 100 c         a = 1..9,  b, c = 0..9

    10001 = 73 * 137
     1010 = 2 * 5 * 101
      100 = 2^2 * 5^2

900 palindromes, and the three place-values are the whole story.

====================================================================
II.  WHERE THE COEFFICIENTS COME FROM:  10^m + 1
====================================================================

A palindrome of length n pairs position k with position n-1-k, so that pair
contributes

    10^k + 10^(n-1-k)  =  10^k * (10^(n-1-2k) + 1).

Every coefficient is therefore a power of ten times some 10^m + 1, and the
primes available to annihilate a digit are exactly the prime factors of
10^m + 1:

    10^1 + 1 = 11                  10^5 + 1 = 11 * 9091
    10^2 + 1 = 101                 10^6 + 1 = 101 * 9901
    10^3 + 1 = 7 * 11 * 13         10^7 + 1 = 11 * 909091
    10^4 + 1 = 73 * 137            10^8 + 1 = 17 * 5882353

    n = 3   (0,2): 10^2+1 = 101                centre 10
    n = 5   (0,4): 10^4+1 = 10001 = 73*137     centre 100
            (1,3): 10*(10^2+1) = 1010
    n = 7   (0,6): 10^6+1 = 1000001 = 101*9901 centre 1000
            (1,5): 10*(10^4+1) = 100010
            (2,4): 100*(10^2+1) = 10100

So the 101 that governs the three-digit grid (aba = 101a + 10b) is 10^2 + 1,
and it does not disappear at length five -- it moves one layer in, onto b.
The NEW annihilator at length five is 10^4 + 1 = 73 * 137, and that is where
the 137 enters the palindrome story.

====================================================================
III.  THE ANNIHILATOR TABLE
====================================================================

A prime that divides a place-value erases the digit it multiplies.

    modulus   10001    1010     100    abcba is congruent to
    --------------------------------------------------------------
        2         1       0       0    a               blind to b, c
        5         1       0       0    a               blind to b, c
      101         2       0     100    2a + 100c       blind to b
       73         0      61      27    61b + 27c       blind to a
      137         0      51     100    51b + 100c      blind to a
    10001         0    1010     100    1010b + 100c    blind to a
       11         2       9       1    2a + 9b + c
       37        11      11      26    11a + 11b + 26c      (THEOREM 56)
        9         2       2       1    2a + 2b + c          (digit sum)

Read off:

  mod 2 and mod 5 the palindrome IS its outer digit, because 2 and 5 divide
  both 1010 and 100.  That single line forces the shape of the prime list in
  section V.

  mod 73 and mod 137 the outer digit is invisible, because 10001 = 73 * 137.
  Each of those is therefore a condition on the pair (b, c) alone, with a
  free -- so its solution count is a multiple of 9.

  mod 101 the middle-pair digit is invisible, because 1010 = 10 * 101.

====================================================================
IV.  THE RULES
====================================================================

Each is derived from the table and then checked on all 900 palindromes.

    2     | abcba  <=>  a even                          400 of 900
    5     | abcba  <=>  a = 5                            100
    101   | abcba  <=>  c = 2a    (b free, so a <= 4)      40
    11    | abcba  <=>  2(a - b) + c = 0 (mod 11)          82
    37    | abcba  <=>  c = a + b                          45
    73    | abcba  <=>  (b,c) in {(0,0), (2,9), (9,4)}     27
    137   | abcba  <=>  (b,c) in {(0,0), (9,5)}            18
    10001 | abcba  <=>  b = c = 0,  i.e. abcba = a000a      9
    9     | abcba  <=>  2(a + b) + c = 0 (mod 9)          100

THE 101 RULE is the direct answer to what happens one rung up from aba.
At length three, 101 | aba <=> b = 0 -- a condition on the CENTRE digit.
At length five, 101 is blind to b, so the condition moves off the middle
entirely and becomes c = 2a, a condition linking the OUTER digit to the
CENTRE, with b free.  The forty solutions are a000a-shaped in b:

    a=1, c=2:  10201 11211 12221 ... 19291
    a=2, c=4:  20402 21412 ... ;  a=3, c=6 ; a=4, c=8   (a >= 5 needs c > 9)

THE SEAM COUNT.  THEOREM 56 gives 11(a+b) + 26c = 0 (mod 37).  Since
11^-1 = 27 and 27 * 26 = 702 = -1 (mod 37), that is (a+b) - c = 0 (mod 37);
and a + b - c lies in [-8, 18], whose only multiple of 37 is 0.  So there is
no second branch -- c = a + b exactly, and the seams number

    sum over a=1..9 of (10 - a)  =  45  =  C(10,2).

====================================================================
V.  PRIMES
====================================================================

93 of the 900 are prime, and every one has a odd and a != 5 -- forced by the
first two rows of the table, not by inspection.  By outer digit:

    a = 1: 26      a = 3: 24      a = 7: 24      a = 9: 19

a in {2,4,6,8} contributes nothing (even), a = 5 nothing (multiple of 5),
and the remaining four outer digits carry all 93.

====================================================================
VI.  SQUARES, AND WHERE 12321 SITS
====================================================================

Seven of the 900 are perfect squares:

    10201 = 101^2    12321 = 111^2    14641 = 121^2    40804 = 202^2
    44944 = 212^2    69696 = 264^2    94249 = 307^2

Exactly ONE of them is a seam:

    12321 is the unique five-digit palindromic square with c = a + b.

Checked against all seven: (1,0,2) has a+b=1 vs c=2; (1,4,6) 5 vs 6;
(4,0,8) 4 vs 8; (4,4,9) 8 vs 9; (6,9,6) 15 vs 6; (9,4,2) 13 vs 2.  Only
(1,2,3) satisfies 3 = 1 + 2, and (1,2,3) is the 123 family.

THE 37^2 LAYER.  Three palindromes are divisible by 37^2 = 1369, and they
are consecutive multiples of 12321:

    12321 = 1 * 12321,   24642 = 2 * 12321,   36963 = 3 * 12321

and 4 * 12321 = 49284 is not a palindrome, which closes the list.  So the
whole 37^2 layer of the grid is the 12321 line, three terms long.

====================================================================
VII.  THE BLOCK IDENTITY
====================================================================

    abcba  =  100 * abc  +  ba

with abc = 100a + 10b + c the leading three digits and ba = 10b + a the
first two reversed.  For 12321: 100 * 123 + 21 = 12321.  Checked on all 900.
"""


# ---------------------------------------------------------------- helpers
def abcba(a, b, c):
    """The five-digit palindrome with digits a, b, c, b, a."""
    return 10001 * a + 1010 * b + 100 * c


def grid():
    """All 900 digit triples (a, b, c) of the five-digit palindrome grid."""
    return [(a, b, c) for a in range(1, 10) for b in range(10)
            for c in range(10)]


def pair_coefficient(k, n):
    """Coefficient of the digit pair at positions (k, n-1-k) in an n-digit
    palindrome: 10^k + 10^(n-1-k) = 10^k (10^(n-1-2k) + 1)."""
    return 10 ** k + 10 ** (n - 1 - k)


def factor(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def is_prime(n):
    return n > 1 and list(factor(n).values()) == [1]


def digital_root(n):
    return 9 if n == 0 else (n - 1) % 9 + 1


def residue_row(m):
    """(10001, 1010, 100) reduced mod m -- one row of the annihilator table."""
    return (10001 % m, 1010 % m, 100 % m)


def blind_digits(m):
    """Which of a, b, c the modulus m cannot see."""
    return [nm for co, nm in zip(residue_row(m), "abc") if co == 0]


# ---------------------------------------------------------------- the rules
RULES = {
    2:     lambda a, b, c: a % 2 == 0,
    5:     lambda a, b, c: a == 5,
    9:     lambda a, b, c: (2 * (a + b) + c) % 9 == 0,
    11:    lambda a, b, c: (2 * (a - b) + c) % 11 == 0,
    37:    lambda a, b, c: c == a + b,
    73:    lambda a, b, c: (61 * b + 27 * c) % 73 == 0,
    101:   lambda a, b, c: c == 2 * a,
    137:   lambda a, b, c: (51 * b + 100 * c) % 137 == 0,
    10001: lambda a, b, c: b == 0 and c == 0,
}

RULE_COUNTS = {2: 400, 5: 100, 9: 100, 11: 82, 37: 45,
               73: 27, 101: 40, 137: 18, 10001: 9}

PALINDROMIC_SQUARES_5 = [10201, 12321, 14641, 40804, 44944, 69696, 94249]
SEAM_SQUARE = 12321
SQ37_LAYER = [12321, 24642, 36963]
PRIME_COUNT_5 = 93
PRIMES_BY_OUTER = {1: 26, 3: 24, 7: 24, 9: 19}


# =====================================================================
#                             SELF-TESTS
# =====================================================================
def test_place_values():
    assert factor(10001) == {73: 1, 137: 1}
    assert factor(1010) == {2: 1, 5: 1, 101: 1}
    assert factor(100) == {2: 2, 5: 2}
    assert abcba(1, 2, 3) == 12321
    for a, b, c in grid():
        assert str(abcba(a, b, c)) == f"{a}{b}{c}{b}{a}"
    print("  I     abcba = 10001a + 1010b + 100c, 10001 = 73*137, "
          "1010 = 2*5*101")


def test_pair_coefficients_come_from_10m_plus_1():
    # the pair coefficient factors as 10^k (10^m + 1) with m = n-1-2k
    for n in (3, 5, 7, 9):
        for k in range(n // 2):
            m = n - 1 - 2 * k
            assert pair_coefficient(k, n) == 10 ** k * (10 ** m + 1), (k, n)
    # the specific ones this file uses
    assert pair_coefficient(0, 3) == 101 == 10 ** 2 + 1
    assert pair_coefficient(0, 5) == 10001 == 10 ** 4 + 1
    assert pair_coefficient(1, 5) == 1010 == 10 * (10 ** 2 + 1)
    # 101 governs aba and reappears inside 1010 -- it does not vanish
    assert 101 in factor(pair_coefficient(0, 3))
    assert 101 in factor(pair_coefficient(1, 5))
    # 137 is genuinely new at length five
    assert 137 in factor(10 ** 4 + 1)
    assert 137 not in factor(10 ** 2 + 1) and 137 not in factor(10 ** 3 + 1)
    assert factor(10 ** 3 + 1) == {7: 1, 11: 1, 13: 1}
    assert factor(10 ** 6 + 1) == {101: 1, 9901: 1}
    print("  II    pair coefficient = 10^k (10^m + 1); 101 from 10^2+1, "
          "73*137 from 10^4+1")


def test_annihilator_table():
    assert residue_row(2) == (1, 0, 0) and blind_digits(2) == ["b", "c"]
    assert residue_row(5) == (1, 0, 0) and blind_digits(5) == ["b", "c"]
    assert residue_row(101) == (2, 0, 100) and blind_digits(101) == ["b"]
    assert residue_row(73) == (0, 61, 27) and blind_digits(73) == ["a"]
    assert residue_row(137) == (0, 51, 100) and blind_digits(137) == ["a"]
    assert blind_digits(10001) == ["a"]
    assert residue_row(37) == (11, 11, 26)        # THEOREM 56
    assert residue_row(9) == (2, 2, 1)            # the digit sum 2(a+b)+c
    assert residue_row(11) == (2, 9, 1)
    # mod 2 and mod 5 the palindrome really is its outer digit
    for a, b, c in grid():
        n = abcba(a, b, c)
        assert n % 2 == a % 2 and n % 5 == a % 5
    # a is invisible mod 73, mod 137 and mod 10001
    for m in (73, 137, 10001):
        for b in range(10):
            for c in range(10):
                vals = {abcba(a, b, c) % m for a in range(1, 10)}
                assert len(vals) == 1, (m, b, c, vals)
    # b is invisible mod 101
    for a in range(1, 10):
        for c in range(10):
            vals = {abcba(a, b, c) % 101 for b in range(10)}
            assert len(vals) == 1, (a, c, vals)
    print("  III   table verified: 2,5 see only a; 73,137,10001 cannot see a; "
          "101 cannot see b")


def test_rules_on_all_900():
    G = grid()
    assert len(G) == 900
    for m, rule in RULES.items():
        bad = [t for t in G if (abcba(*t) % m == 0) != rule(*t)]
        assert bad == [], (m, bad[:4])
        cnt = sum(1 for t in G if rule(*t))
        assert cnt == RULE_COUNTS[m], (m, cnt)
    # the 101 rule needs a <= 4, and b is free
    s101 = [(a, b, c) for a, b, c in G if abcba(a, b, c) % 101 == 0]
    assert {a for a, _, _ in s101} == {1, 2, 3, 4}
    assert all(c == 2 * a for a, _, c in s101)
    assert len({b for _, b, _ in s101}) == 10        # every b occurs
    assert len(s101) == 40 == 4 * 10
    # the three-digit contrast: 101 | aba  <=>  b = 0
    aba = [(a, b) for a in range(1, 10) for b in range(10)
           if (101 * a + 10 * b) % 101 == 0]
    assert aba == [(a, 0) for a in range(1, 10)]
    # 73 and 137 are conditions on (b,c) only, so counts are multiples of 9
    for m, pairs in ((73, 3), (137, 2)):
        bc = {(b, c) for a, b, c in G if abcba(a, b, c) % m == 0}
        assert len(bc) == pairs and RULE_COUNTS[m] == 9 * pairs
    assert {(b, c) for a, b, c in G if abcba(a, b, c) % 73 == 0} == \
           {(0, 0), (2, 9), (9, 4)}
    assert {(b, c) for a, b, c in G if abcba(a, b, c) % 137 == 0} == \
           {(0, 0), (9, 5)}
    # 10001 is exactly the intersection: b = c = 0
    assert [abcba(*t) for t in G if abcba(*t) % 10001 == 0] == \
           [10001 * a for a in range(1, 10)]
    print("  IV    all nine rules exact on all 900; "
          "101 | abcba <=> c = 2a with b free (40 cases)")


def test_seam_reduction_and_count():
    # 11^-1 = 27 mod 37 and 27*26 = -1, so 11(a+b)+26c = 0  <=>  c = a+b
    assert (11 * 27) % 37 == 1
    assert (27 * 26) % 37 == 36 == (-1) % 37
    # a+b-c lies in [-8,18]; 0 is its only multiple of 37, so no second branch
    rng = {a + b - c for a in range(1, 10) for b in range(10)
           for c in range(10)}
    assert min(rng) == -8 and max(rng) == 18
    assert [v for v in rng if v % 37 == 0] == [0]
    seams = [t for t in grid() if abcba(*t) % 37 == 0]
    assert all(c == a + b for a, b, c in seams)
    assert len(seams) == 45 == sum(10 - a for a in range(1, 10))
    print(f"  IV    seam reduction c = a+b has no second branch; "
          f"{len(seams)} = C(10,2) seams")


def test_primes():
    G = grid()
    pr = [t for t in G if is_prime(abcba(*t))]
    assert len(pr) == PRIME_COUNT_5
    # forced by the table, not observed: a must be odd and not 5
    assert all(a % 2 == 1 and a != 5 for a, _, _ in pr)
    from collections import Counter
    assert dict(Counter(a for a, _, _ in pr)) == PRIMES_BY_OUTER
    assert sum(PRIMES_BY_OUTER.values()) == PRIME_COUNT_5
    print(f"  V     {PRIME_COUNT_5} palindromic primes, all with a odd and "
          f"a != 5: {PRIMES_BY_OUTER}")


def test_squares_and_the_unique_seam_square():
    from math import isqrt
    sq = [t for t in grid() if isqrt(abcba(*t)) ** 2 == abcba(*t)]
    assert sorted(abcba(*t) for t in sq) == PALINDROMIC_SQUARES_5
    seam_sq = [t for t in sq if t[2] == t[0] + t[1]]
    assert len(seam_sq) == 1
    assert abcba(*seam_sq[0]) == SEAM_SQUARE == 12321
    assert seam_sq[0] == (1, 2, 3)
    # 12321 = 111^2 = (3*37)^2 = 9*37^2
    assert 12321 == 111 ** 2 == (3 * 37) ** 2 == 9 * 37 ** 2
    assert digital_root(12321) == 9
    # the 37^2 layer is the 12321 line, three terms long
    layer = [abcba(*t) for t in grid() if abcba(*t) % (37 * 37) == 0]
    assert sorted(layer) == SQ37_LAYER
    assert SQ37_LAYER == [12321 * k for k in (1, 2, 3)]
    s = str(12321 * 4)
    assert s != s[::-1], "4*12321 must fail to be a palindrome"
    print(f"  VI    7 palindromic squares; {SEAM_SQUARE} is the unique seam "
          f"among them; 37^2 layer = {SQ37_LAYER}")


def test_block_identity():
    for a, b, c in grid():
        assert abcba(a, b, c) == 100 * (100 * a + 10 * b + c) + (10 * b + a)
    assert 100 * 123 + 21 == 12321
    print("  VII   abcba = 100*abc + ba, checked on all 900 "
          "(12321 = 100*123 + 21)")


def test_does_not_prove_too_much():
    """The table must not make true things false or false things true."""
    # a non-annihilated modulus sees every digit, so no blindness
    for m in (3, 7, 11, 13, 37):
        assert blind_digits(m) == [], m
    # 7 and 13 do NOT annihilate anything at length five, though they do
    # divide 10^3 + 1 -- that coefficient belongs to length four and seven
    assert factor(10 ** 3 + 1) == {7: 1, 11: 1, 13: 1}
    assert 10001 % 7 == 5 and 10001 % 13 == 4
    # the seam rule is not vacuous and not universal
    assert 0 < RULE_COUNTS[37] < 900
    # 10201 = 101^2 is divisible by 101 and is NOT a seam -- both rules agree
    assert 10201 % 101 == 0 and 10201 % 37 != 0
    assert RULES[101](1, 0, 2) and not RULES[37](1, 0, 2)
    print("  check moduli that annihilate nothing really see all three digits")


def self_test():
    print("abcba_place_value_grid.py self-tests\n")
    test_place_values()
    test_pair_coefficients_come_from_10m_plus_1()
    test_annihilator_table()
    test_rules_on_all_900()
    test_seam_reduction_and_count()
    test_primes()
    test_squares_and_the_unique_seam_square()
    test_block_identity()
    test_does_not_prove_too_much()
    print("\nAll assertions passed.")
    print("THE ABCBA GRID: abcba = 10001a + 1010b + 100c, and every")
    print("divisibility rule is read off one annihilator table.")
    print("  10^m + 1 supplies every coefficient: 101 = 10^2+1 governs aba")
    print("  and survives into 1010; 10^4+1 = 73*137 is new at length five.")
    print("  2, 5        see only a      -> 93 primes, all with a odd, a != 5")
    print("  73,137      cannot see a    -> conditions on (b,c), counts 27, 18")
    print("  101         cannot see b    -> c = 2a with b free, 40 cases")
    print("  37          c = a + b       -> 45 seams (THEOREM 56, no 2nd branch)")
    print("  12321 is the unique palindromic square that is a seam, and the")
    print("  whole 37^2 layer is 12321, 24642, 36963 -- three terms, then stop.")


if __name__ == "__main__":
    self_test()

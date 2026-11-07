"""
UCU: THE DRIP ON ANY TWO NUMBERS
================================================================

Prior art, and where this sits.  drip_cycle.py and owner_work/drip_cycle.md
(on claude/add-torus-animation-6Ey5Z and copilot/fix-github-actions-job-
failure-again) already run the drip cycle in the shape of the owner's
example of 2026-10-12, setting each digit of a number against every
ordering of its digits.  owner_work/TERMS.md indexes it to messages #227,
#228, #252 and #255, with full runs on 246 and on 0.25.  None of that is
restated here.

This file covers the OTHER reading, which that code does not: the drip on
two numbers rather than on one number's digits.

  UCU is a shape, not a pair of values.  U is whatever stands at both
  ends and C is whatever stands between, so 191, 121 and 212 are all UCU
  -- with (U,C) = (1,9), (1,2) and (2,1).  Neither letter is pinned to a
  digit.

  THEOREM 36  DR(UCU) = DR(2*DR(U) + DR(C)).  U enters DOUBLED and C
              enters once: the two registers are structurally asymmetric,
              which is what marking them apart records.  Checked on every
              pair below 200 with no exception.                 Level 1

  THEOREM 37  Chained, UCU is the decade string.  Holding U fixed and
              letting C count 1..9, then closing with one more U, gives
                  U1 U2 U3 U4 U5 U6 U7 U8 U9 U
              which at U = 1 is exactly 1112131415161718191.    Level 1

  THEOREM 38  THE BODY VANISHES.  The body U1..U9 has digit sum 9U + 45,
              and both terms are divisible by 9, so the whole decade is
              invisible mod 9 and the root of the chained drip is the
              TRAILING term alone -- for every U from 1 to 9:
                  tail U    -> root U      the same decade repeats
                  tail U+1  -> root U+1    the next decade begins
              So "two goes to the next sequence, one repeats" is a
              statement about the root: the choice at the boundary is the
              only thing the reduction can see, because everything
              between the boundaries cancels.                   Level 1

  THEOREM 40  WHERE ELSE THE BODY VANISHES.  body(U,h) = h(2U + h + 1)/2,
              and it is 0 mod 9 when h = 9 (for every U, being 9(U+5)),
              when h = 3 or 6 and U = 1 (mod 3) (being 3(U+2) and
              3(2U+7)), and otherwise at the single h with
              2U + h + 1 = 0 (mod 9).  Note the 2U: U enters DOUBLED here
              exactly as it does in THEOREM 36.  So every U has two cuts,
              except U = 1, 4, 7 which have three -- at 3, 6 and 9, the
              bottom third itself.  U = 1, the string as written, is one
              of those three.                                  Level 1

  THEOREM 39  UCU on the chart's own three pairs lands inside {3,6,9}:
                  (1,1)   -> 111     root 3
                  (6,6)   -> 666     root 9
                  (10,19) -> 101910  root 3
              and the same three roots come back when U and C are
              swapped.  {3,6,9} is the nilpotent ideal of Z/9Z -- the set
              that digitwise_operations.py THEOREM 10 shows is closed
              under doubling, tripling and columnwise addition.  The
              doubling of U in THEOREM 36 cannot leave it.      Level 1
"""


def digital_root(n):
    return 9 if n == 0 else (n - 1) % 9 + 1


def digit_sum(s):
    return sum(int(c) for c in str(s) if c.isdigit())


def ucu(u, c):
    """The drip on two numbers: U, then C, then U again."""
    return f"{u}{c}{u}"


def chained(u, lo=1, hi=9, tail=None):
    """U against each C in lo..hi, closed by one more term.

    tail defaults to U (the decade repeats); pass u+1 to advance.
    """
    if tail is None:
        tail = u
    return "".join(f"{u}{c}" for c in range(lo, hi + 1)) + str(tail)


def body_digit_sum(u, lo=1, hi=9):
    return sum(digit_sum(f"{u}{c}") for c in range(lo, hi + 1))


OWNER_EXAMPLES = [(1, 9, '191'), (1, 2, '121'), (2, 1, '212')]
CHART_PAIRS = [('indices 00,01', 1, 1), ('indices 05,06', 6, 6),
               ('indices 07,08', 10, 19)]
DECADE_STRING_U1 = '1112131415161718191'
BOTTOM = (3, 6, 9)


# ======================================================================
# tests
# ======================================================================

def test_ucu_is_a_shape_not_a_value():
    for u, c, want in OWNER_EXAMPLES:
        assert ucu(u, c) == want, (u, c)
        s = ucu(u, c)
        assert s == s[::-1]                       # single digits: palindromic
    # the three examples use three different (U, C) assignments
    assert len({(u, c) for u, c, _ in OWNER_EXAMPLES}) == 3
    assert {u for u, _, _ in OWNER_EXAMPLES} == {1, 2}
    assert {c for _, c, _ in OWNER_EXAMPLES} == {9, 2, 1}
    # multi-digit terms are UCU at the term level, not at the digit level
    s = ucu(10, 19)
    assert s == '101910' and s != s[::-1]


def test_root_closed_form():
    """THEOREM 36: U doubles, C does not."""
    for a in range(1, 200):
        for b in range(1, 200):
            assert digital_root(digit_sum(ucu(a, b))) == \
                digital_root(2 * digital_root(a) + digital_root(b)), (a, b)
    # the asymmetry is real: swapping U and C generally moves the root
    moved = [(a, b) for a in range(1, 40) for b in range(1, 40)
             if digital_root(digit_sum(ucu(a, b)))
             != digital_root(digit_sum(ucu(b, a)))]
    assert moved, 'swapping U and C should usually change the root'
    # and it does NOT move exactly when DR(U) = DR(C)
    for a in range(1, 60):
        for b in range(1, 60):
            same = (digital_root(digit_sum(ucu(a, b)))
                    == digital_root(digit_sum(ucu(b, a))))
            assert same == (digital_root(a) == digital_root(b)), (a, b)


def test_chained_is_the_decade_string():
    """THEOREM 37."""
    assert chained(1) == DECADE_STRING_U1
    assert len(DECADE_STRING_U1) == 19
    s = DECADE_STRING_U1
    assert all(s[i] == '1' for i in range(0, 19, 2))          # U drips
    assert [s[i] for i in range(1, 18, 2)] == [str(d) for d in range(1, 10)]
    for u in range(1, 10):
        c = chained(u)
        assert c.startswith(f'{u}1') and c.endswith(str(u))
        assert len(c) == 19


def test_body_vanishes():
    """THEOREM 38: only the trailing term survives the reduction."""
    for u in range(1, 10):
        b = body_digit_sum(u)
        assert b == 9 * u + 45, (u, b)
        assert b % 9 == 0
        # tail U repeats the decade; tail U+1 advances it
        assert digital_root(b + u) == digital_root(u) == u
        assert digital_root(b + u + 1) == digital_root(u + 1)
    # at U = 1 this is the pair of strings as written
    assert digital_root(digit_sum(chained(1, tail=1))) == 1
    assert digital_root(digit_sum(chained(1, tail=2))) == 2
    assert digit_sum(chained(1, tail=1)) == 55
    assert digit_sum(chained(1, tail=2)) == 56
    # the same holds for any window whose length makes the body 0 mod 9
    assert body_digit_sum(1, 1, 9) % 9 == 0
    assert body_digit_sum(1, 1, 8) % 9 != 0        # stopping at 8 does NOT


def test_chart_pairs_land_in_the_bottom_third():
    """THEOREM 39."""
    roots = []
    for _lab, u, c in CHART_PAIRS:
        r = digital_root(digit_sum(ucu(u, c)))
        roots.append(r)
        assert r in BOTTOM, (u, c, r)
    assert roots == [3, 9, 3]
    # swapping gives the same three
    swapped = [digital_root(digit_sum(ucu(c, u))) for _l, u, c in CHART_PAIRS]
    assert swapped == roots
    # {3,6,9} is closed under the doubling THEOREM 36 applies to U
    for d in BOTTOM:
        assert digital_root(2 * d) in BOTTOM
        for e in BOTTOM:
            assert digital_root(d + e) in BOTTOM
            assert digital_root(d * e) in BOTTOM


def test_where_the_body_vanishes():
    """THEOREM 40: the cut points, computed rather than guessed.

    body(U, h) = h*U + h(h+1)/2 = h(2U + h + 1)/2.  It is 0 mod 9 when:
      h = 9                         for every U, since it is 9(U+5)
      h = 3 or 6, if U = 1 (mod 3)  since they are 3(U+2) and 3(2U+7)
      otherwise the single h with 2U + h + 1 = 0 (mod 9)
    Note 2U again: U enters doubled here exactly as in THEOREM 36.
    """
    table = {u: [h for h in range(1, 10) if body_digit_sum(u, 1, h) % 9 == 0]
             for u in range(1, 10)}
    assert table == {1: [3, 6, 9], 2: [4, 9], 3: [2, 9], 4: [3, 6, 9],
                     5: [7, 9], 6: [5, 9], 7: [3, 6, 9], 8: [1, 9],
                     9: [8, 9]}, table
    # the closed forms.  U enters through its DIGIT SUM, so the formula is
    # in ds(U), not U -- they coincide only while U is a single digit.
    for u in range(1, 40):
        q = digit_sum(u)
        for h in range(1, 10):
            assert body_digit_sum(u, 1, h) == h * q + h * (h + 1) // 2
            assert 2 * body_digit_sum(u, 1, h) == h * (2 * q + h + 1)
        assert body_digit_sum(u, 1, 9) == 9 * (q + 5)
        assert body_digit_sum(u, 1, 3) == 3 * (q + 2)
        assert body_digit_sum(u, 1, 6) == 3 * (2 * q + 7)
    assert body_digit_sum(10, 1, 9) == body_digit_sum(1, 1, 9)   # ds(10) = 1
    # h = 9 always; 3 and 6 exactly for U = 1 mod 3
    for u in range(1, 10):
        assert 9 in table[u]
        assert (3 in table[u]) == (u % 3 == 1)
        assert (6 in table[u]) == (u % 3 == 1)
    # and every cut with h coprime to 3 satisfies 2U + h + 1 = 0 mod 9
    for u, hs in table.items():
        for h in hs:
            if h % 3:
                assert (2 * u + h + 1) % 9 == 0, (u, h)
    # three cuts for U = 1, 4, 7; two for the rest
    assert {u for u, hs in table.items() if len(hs) == 3} == {1, 4, 7}
    assert all(len(hs) == 2 for u, hs in table.items() if u % 3 != 1)
    # U = 1, the string as written, is one of the three-cut values
    assert table[1] == [3, 6, 9] == sorted(BOTTOM)


def test_does_not_prove_too_much():
    # UCU is palindromic only when U and C are single digits
    assert ucu(1, 9) == '191'[::-1]
    assert ucu(10, 19) != ucu(10, 19)[::-1]
    # THEOREM 38's body does not only vanish at 9 -- see THEOREM 40
    assert body_digit_sum(1, 1, 9) % 9 == 0
    assert [hi for hi in range(1, 10) if body_digit_sum(1, 1, hi) % 9 == 0] \
        == [3, 6, 9]
    for hi in (1, 2, 4, 5, 7, 8):
        assert body_digit_sum(1, 1, hi) % 9 != 0
    # and THEOREM 39 is about these three pairs, not all pairs
    off = [(a, b) for a in range(1, 30) for b in range(1, 30)
           if digital_root(digit_sum(ucu(a, b))) not in BOTTOM]
    assert off, 'most pairs do NOT land in {3,6,9}'
    assert len(off) > 500


def self_test():
    tests = [test_ucu_is_a_shape_not_a_value,
             test_root_closed_form,
             test_chained_is_the_decade_string,
             test_body_vanishes,
             test_where_the_body_vanishes,
             test_chart_pairs_land_in_the_bottom_third,
             test_does_not_prove_too_much]
    for t in tests:
        t()
        print(f'  ok  {t.__name__}')
    print()
    print('  THEOREM 36  DR(UCU) = DR(2*DR(U) + DR(C)) -- U doubles, C does not')
    print('  THEOREM 37  chained UCU at U=1 is ' + DECADE_STRING_U1)
    print('  THEOREM 38  body U1..U9 = 9U + 45 = 0 mod 9, so only the tail shows:')
    print('              tail U repeats the decade, tail U+1 advances it')
    print('  THEOREM 40  cuts: h=9 for every U; h=3,6 for U=1,4,7; else the '
          'h with 2U+h+1 = 0 mod 9')
    print('  THEOREM 39  the chart pairs give roots ' +
          str([digital_root(digit_sum(ucu(u, c))) for _l, u, c in CHART_PAIRS]) +
          ', all inside {3,6,9}')


if __name__ == '__main__':
    self_test()

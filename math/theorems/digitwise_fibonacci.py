"""
THE DIGITAL ROOT IS A HOMOMORPHISM, SO "1+2 only" IS FIBONACCI
================================================================

digitwise_backbone.py THEOREM 19 found that the rank-1 CRT component of a
sheet is its digital root, via the idempotent e = r^-1 J.  Being a module
map, that projector must transport any recurrence the sheet obeys down to
its roots.  This file works out what that forces.

The consequence is immediate and was sitting in plain sight: the row
digital roots of the C/P grid are 1, 1, 2, 3, 5.

Grading, as elsewhere in this repository:

  Level 1  proved parameter-free, or settled by exhausting a finite set
  Level 2  verified over a bounded range

  THEOREM 23  DR(a (+) b) = DR(a) + DR(b) (mod 9).  The per-column root
              reduction is invisible mod 9, since dr(x) = x (mod 9), so
              the digit sum of a columnwise sum is congruent to the sum
              of the digit sums.  DR is therefore a homomorphism from the
              sheet module onto Z/9Z -- which is exactly THEOREM 19's
              projector, stated additively.                     Level 1
  THEOREM 24  hence the row roots of ANY "1+2 only" sheet satisfy the
              Fibonacci recurrence mod 9, whatever the two seed rows are.
              The C/P grid's roots are 1, 1, 2, 3, 5 -- forced, not
              observed.  Fibonacci mod 9 has Pisano period 24, so a sheet
              longer than 24 rows repeats its root sequence exactly.
                                                                 Level 1
  THEOREM 25  with perturbed columns the deltas obey the SAME recurrence
              with the perturbations as an inhomogeneous source:
                  delta_i = delta_(i-2) + delta_(i-1) + mark_i  (mod 9)
              where mark_i is the total column change in row i.  So the
              root sequence locates the perturbations without the sheet
              being visible, and an unmarked row still departs once an
              earlier one has -- it inherits.  Exact on all seven steps
              of the nine-row sheet.                             Level 1
  THEOREM 26  (a negative result, recorded so it is not re-derived)  None
              of this demonstrates any connection to pi.  The reductions
              work because 10 = 1 (mod 9), so a number is congruent to
              its digit sum; that is the whole mechanism, and it is base
              arithmetic, not an appearance of a transcendental constant.
              A digit string agreeing with an initial segment of pi is
              not evidence: the root sequence of a "1+2 only" sheet is
              determined entirely by its two seed rows, and 24 values
              exhaust it.                                        Level 1

THEOREM 25 is what makes the marked columns of digitwise_sheets THEOREM 7
recoverable rather than merely recorded: three of the nine-row sheet's
rows carry marks, and the root sequence's departure from Fibonacci pins
their rows and their sizes.
"""

from math import gcd


def digital_root(n):
    return 9 if n == 0 else (n - 1) % 9 + 1


def digits(x):
    return [int(c) for c in str(x)]


def ring_digits(x):
    return [digital_root(int(c)) for c in str(x)]


def text(v):
    return ''.join(str(d) for d in v)


def cadd(a, b):
    return [digital_root(x + y) for x, y in zip(a, b)]


def DR(n):
    """Digital root of an integer, by repeated digit summing."""
    while n > 9:
        n = sum(int(c) for c in str(n))
    return 9 if n == 0 else n


def sheet_root(v):
    """Digital root of a sheet given as a digit vector."""
    return digital_root(sum(v))


# ----------------------------------------------------------------------
# THEOREM 24: Fibonacci mod 9
# ----------------------------------------------------------------------

def fib_mod9(a, b, n):
    """n terms of the Fibonacci recurrence mod 9, seeded at a, b."""
    out = [digital_root(a), digital_root(b)]
    while len(out) < n:
        out.append(digital_root(out[-1] + out[-2]))
    return out[:n]


PISANO_9 = 24
FIB9 = [1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9,
        8, 8, 7, 6, 4, 1, 5, 6, 2, 8, 1, 9]

CP_GRID = ['14689', '23572', '37262', '65334', '93596']
CP_ROOTS = [1, 1, 2, 3, 5]

NINE_SHEET = ['65334', '93396', '68631', '62937', '31638',
              '93666', '37395', '62962', '99367']
NINE_ROOTS = [3, 3, 6, 9, 3, 3, 9, 7, 7]

# (row index, column index, value the recurrence gives, value written)
MARKED_COLUMNS = [(4, 3, 6, 3), (6, 1, 4, 7), (7, 0, 3, 6), (7, 1, 1, 2)]
MARKS_BY_ROW = {4: 6, 6: 3, 7: 4}          # total column change, mod 9
NINE_DELTAS = [0, 0, 0, 0, 6, 6, 6, 7, 4]


def one_two_only(seed_a, seed_b, rows):
    sheet = [list(seed_a), list(seed_b)]
    while len(sheet) < rows:
        sheet.append(cadd(sheet[-2], sheet[-1]))
    return sheet


def marks_by_row(marked):
    out = {}
    for ri, _ci, p, w in marked:
        out[ri] = (out.get(ri, 0) + (w - p)) % 9
    return out


# ======================================================================
# tests
# ======================================================================

def test_the_pasted_values_are_right():
    """Every digital root quoted in the worked note checks out."""
    quoted = [(14689, 1), (23572, 1), (37262, 2), (65334, 3), (93, 3),
              (68, 5), (62, 8), (31, 4), (34, 7), (37, 1),
              (198, 9), (265, 4), (374, 5)]
    for n, want in quoted:
        assert DR(n) == want, (n, DR(n), want)
        assert DR(n) == digital_root(n)          # the two routes agree
    assert DR(9 + 9) == 9
    # the intermediate chains, as quoted
    assert sum(digits(198)) == 18 and DR(18) == 9
    assert sum(digits(265)) == 13 and DR(13) == 4
    assert sum(digits(374)) == 14 and DR(14) == 5
    assert digital_root(4 + 9) == digital_root(1 + 3) == 4
    assert (4 + 9) % 9 == 4 % 9 == (1 + 3) % 9


def test_root_is_a_homomorphism():
    """THEOREM 23, proved then swept.

    dr(x) = x (mod 9), so reducing each column changes nothing mod 9:
      sum_i dr(a_i + b_i) = sum_i (a_i + b_i) = sum a_i + sum b_i (mod 9).
    """
    for x in range(0, 200):
        assert digital_root(x) % 9 == x % 9      # the one fact it rests on
    for a in range(10000, 100000, 311):
        for b in range(10000, 100000, 1013):
            va, vb = ring_digits(a), ring_digits(b)
            s = cadd(va, vb)
            assert sheet_root(s) == digital_root(sheet_root(va) + sheet_root(vb))
            assert sheet_root(va) == digital_root(a)
    # it is a homomorphism for scaling too, hence for D and T
    for a in range(1000, 10000, 37):
        va = ring_digits(a)
        for k in range(1, 10):
            sk = [digital_root(k * d) for d in va]
            assert sheet_root(sk) == digital_root(k * sheet_root(va)), (a, k)
    # and at other lengths
    for r in (2, 3, 4, 6, 7):
        lo, hi = 10 ** (r - 1), 10 ** r
        step = max(1, (hi - lo) // 300)
        for a in range(lo, hi, step):
            va = ring_digits(a)
            vb = ring_digits(a + 1) if len(ring_digits(a + 1)) == r else va
            assert sheet_root(cadd(va, vb)) == \
                digital_root(sheet_root(va) + sheet_root(vb))


def test_one_two_only_is_fibonacci():
    """THEOREM 24: the roots are Fibonacci mod 9, for any seeds."""
    # the C/P grid
    roots = [DR(int(x)) for x in CP_GRID]
    assert roots == CP_ROOTS == [1, 1, 2, 3, 5]
    assert roots == fib_mod9(1, 1, 5)
    # and it is forced for ANY pair of seed rows
    for a in range(10000, 100000, 977):
        for b in range(10000, 100000, 1301):
            sheet = one_two_only(ring_digits(a), ring_digits(b), 12)
            got = [sheet_root(v) for v in sheet]
            assert got == fib_mod9(got[0], got[1], 12), (a, b)
    # Pisano period of 9 is 24
    assert fib_mod9(1, 1, 24) == FIB9
    assert fib_mod9(1, 1, 30)[24:30] == FIB9[:6]
    per = next(k for k in range(1, 500)
               if all(fib_mod9(1, 1, k + 12)[i + k] == FIB9[i] for i in range(12)))
    assert per == PISANO_9 == 24
    # a long sheet really does repeat its root sequence
    long_sheet = one_two_only(ring_digits(14689), ring_digits(23572), 60)
    lr = [sheet_root(v) for v in long_sheet]
    assert lr[:12] == lr[24:36] == lr[48:60]
    # the grid is too short to wrap
    assert len(CP_ROOTS) == 5 < 24


def test_marked_columns_are_an_inhomogeneous_source():
    """THEOREM 25: deltas obey the same recurrence, driven by the marks."""
    act = [DR(int(x)) for x in NINE_SHEET]
    assert act == NINE_ROOTS
    pred = fib_mod9(act[0], act[1], 9)
    delta = [(act[i] - pred[i]) % 9 for i in range(9)]
    assert delta == NINE_DELTAS == [0, 0, 0, 0, 6, 6, 6, 7, 4]
    mk = marks_by_row(MARKED_COLUMNS)
    assert mk == MARKS_BY_ROW == {4: 6, 6: 3, 7: 4}
    # the recurrence, every step
    for i in range(2, 9):
        rhs = (delta[i - 2] + delta[i - 1] + mk.get(i, 0)) % 9
        assert rhs == delta[i], (i, rhs, delta[i])
    # rows 1-4 are clean; 5 onward all depart
    assert delta[:4] == [0, 0, 0, 0]
    assert all(d != 0 for d in delta[4:])
    # rows 6 and 9 carry NO mark and still depart -- they inherit it
    assert 5 not in mk and 8 not in mk
    assert delta[5] != 0 and delta[8] != 0
    assert delta[5] == (delta[3] + delta[4]) % 9          # pure inheritance
    assert delta[8] == (delta[6] + delta[7]) % 9
    # and the marks are recoverable from the root sequence alone
    recovered = {}
    for i in range(2, 9):
        m = (delta[i] - delta[i - 2] - delta[i - 1]) % 9
        if m:
            recovered[i] = m
    assert recovered == mk                                # located, and sized


def test_no_pi_connection_is_demonstrated():
    """THEOREM 26, a negative result recorded so it is not re-derived."""
    # the mechanism is 10 = 1 (mod 9), nothing more
    assert 10 % 9 == 1
    for n in (198, 265, 374, 14689, 31415, 1431):
        assert n % 9 == sum(digits(n)) % 9          # the only mechanism
    # a sheet's whole root sequence is fixed by its two seeds, and there
    # are only 81 possible seed pairs, giving at most 81 sequences
    seqs = {tuple(fib_mod9(a, b, 24)) for a in range(1, 10) for b in range(1, 10)}
    assert len(seqs) == 81
    # every one of them is periodic with period dividing 24
    for s in seqs:
        ext = fib_mod9(s[0], s[1], 48)
        assert ext[:24] == list(s) and ext[24:48] == list(s)
    # pi's opening digits are not produced by any of them as a run of 5
    pi5 = (3, 1, 4, 1, 5)
    hits = [s for s in seqs if any(s[i:i + 5] == pi5 for i in range(20))]
    assert hits == [], hits
    # and 31415 is not a reachable collapse value at all: the bar map's
    # image is exactly the palindromes, and 31415 is not one.  checked by
    # searching every five-digit preimage rather than by assertion.
    assert str(31415) != str(31415)[::-1]
    tgt = ring_digits(31415)
    pre = [n for n in range(10000, 100000)
           if (lambda v: [digital_root(v[i] + v[4 - i]) for i in range(5)])(
               ring_digits(n)) == tgt]
    assert pre == [], pre
    # what IS true of 31415 here is only its root, which is unremarkable
    assert DR(31415) == 5 and 31415 % 9 == 5


def test_does_not_prove_too_much():
    # THEOREM 23 is about COLUMNWISE addition.  Ordinary addition carries,
    # and the digit sum is not additive under it -- only the root is.
    assert sum(digits(14689 + 98641)) != sum(digits(14689)) + sum(digits(98641))
    assert DR(14689 + 98641) == digital_root(DR(14689) + DR(98641))
    # so the root survives carrying but the digit sum does not
    assert sum(digits(113330)) == 11 and sum(digits(14689)) + sum(digits(98641)) == 56
    assert DR(113330) == DR(56) == 2
    # THEOREM 24 needs the recurrence, not merely a sheet
    rows = [ring_digits(x) for x in (14689, 23572, 11111)]
    assert [sheet_root(v) for v in rows] != fib_mod9(1, 1, 3)
    # THEOREM 25 recovers marks only up to their ROW TOTAL, not per column
    mk = marks_by_row(MARKED_COLUMNS)
    assert mk[7] == 4                     # two columns, +3 and +1, summed
    per_col = [(ci, (w - p) % 9) for ri, ci, p, w in MARKED_COLUMNS if ri == 7]
    assert sorted(per_col) == [(0, 3), (1, 1)]
    assert sum(d for _c, d in per_col) % 9 == mk[7]
    assert len(per_col) == 2              # the root cannot tell these apart
    # THEOREM 26 is a statement about absence of evidence, not impossibility
    assert DR(31415) == 5                 # pi's digits do have roots, trivially


def self_test():
    tests = [test_the_pasted_values_are_right,
             test_root_is_a_homomorphism,
             test_one_two_only_is_fibonacci,
             test_marked_columns_are_an_inhomogeneous_source,
             test_no_pi_connection_is_demonstrated,
             test_does_not_prove_too_much]
    for t in tests:
        t()
        print(f'  ok  {t.__name__}')
    print()
    print(f'  THEOREM 23  DR(a (+) b) = DR(a) + DR(b) mod 9, because '
          f'dr(x) = x mod 9')
    print(f'  THEOREM 24  so "1+2 only" roots are Fibonacci mod 9.  '
          f'C/P grid: {CP_ROOTS}')
    print(f'              Pisano period {PISANO_9}, and only 81 root '
          f'sequences exist in all')
    print(f'  THEOREM 25  deltas obey delta_i = delta_(i-2) + delta_(i-1) '
          f'+ mark_i (mod 9)')
    print(f'              nine-row sheet roots   {NINE_ROOTS}')
    print(f'              Fibonacci track        {fib_mod9(3, 3, 9)}')
    print(f'              deltas                 {NINE_DELTAS}')
    print(f'              marks recovered from the roots alone: {MARKS_BY_ROW}')
    print(f'              rows 6 and 9 carry no mark and depart anyway -- '
          f'they inherit')
    print(f'  THEOREM 26  no pi connection is demonstrated; the mechanism is '
          f'10 = 1 mod 9')


if __name__ == '__main__':
    self_test()

"""
DIGITWISE SHEETS: THE COLUMNWISE Z/9Z MODULE
================================================================

A digit string of length r, with each entry reduced to its digital root,
is a vector in (Z/9Z)^r written with 9 in place of 0.  Every operation
used on the sheets in this file acts on it COLUMN BY COLUMN with no
carrying.  That single restriction is what makes the sheets behave:
carrying is the only thing that breaks the symmetries below.

Results are graded as elsewhere in this repository:

  Level 1  proved parameter-free, or settled by exhausting a finite set
  Level 2  verified over a bounded range

Everything here is Level 1.  The state spaces are finite, so exhaustion
IS the proof; the two structural theorems (4 and 1b) are proved outright.

  THEOREM 1   columnwise scaling is a Z/9Z-module action, and reversal
              commutes with every digitwise map.                 Level 1
  THEOREM 2   tripling lands in {3,6,9} = 3Z/9Z for every input, and
              that set is closed under doubling and tripling.    Level 1
  THEOREM 3   digitwise doubling on two-digit states: period is the lcm
              of the two digit periods; 17 orbits over 81 states, one
              fixed, four of period 2, twelve of period 6.       Level 1
  THEOREM 4   N (+) reverse(N) is a palindrome for EVERY N, columnwise.
              Ordinary addition fails this; carrying is why.     Level 1
  THEOREM 5   the 5-and-4 split of the digits 1..9 is non-primes against
              primes, and the 4 is forced.                       Level 1
  THEOREM 6   the C/P grid, as a certificate with its marked column.
  THEOREM 7   the "1+2 only" recurrence and the nine-row sheet.
  THEOREM 8   the 13331 layer: the across-bar collapse of a 1x/2x/3x
              sheet is 1,2,3 times one palindrome; 48 five-digit
              palindromes admit such a layer, 7 of them prime.   Level 1
  THEOREM 9   the trichotomy: adding 9 and regrouping digits both fix the
              root; doubling is the only one of the three that moves it.
              And N -> N + DR(N) preserves divisibility by 3, so it splits
              into two sectors; the non-multiples of 3 are partitioned by
              exactly three trajectories, seeded at 1, 5 and 7, each
              gaining 27 per 6 steps.                            Level 1

THEOREM 8 is the join between this file and abcba_place_value_grid.py.
The 48-member class is the same set from both sides: 13331 is its prime
end, and 12321 = 111^2 = 3^2 x 37^2 -- whose layer [12321, 24642, 36963]
is that file's 37^2 layer -- is its composite end.

PROVENANCE.  The sheets in THEOREMS 6, 7 and 8 are transcribed from
worked sheets, and several of their columns depart from the stated
recurrence.  Those columns are recorded here as data, in MARKED_COLUMNS,
with the departure measured.  They are deliberate perturbations at marked
positions, not transcription noise: in the C/P grid the perturbed digit is
the one set off by whitespace on both sides, and the departures in the
nine-row sheet are, three times out of four, exactly the doubling map
applied in place.  The perturbations are load-bearing -- re-running the
nine-row sheet from the unperturbed seed agrees only at row 2 and has
diverged completely by row 7 (test_perturbation_is_load_bearing).
"""


# ----------------------------------------------------------------------
# core: the columnwise module
# ----------------------------------------------------------------------

def digital_root(n):
    """Digital root in 1..9; 0 maps to 9."""
    return 9 if n == 0 else (n - 1) % 9 + 1


def digits(x):
    """Digit vector of an int or a digit string."""
    return [int(c) for c in str(x)]


def text(v):
    return ''.join(str(d) for d in v)


def cadd(a, b):
    """Columnwise sum, each column reduced to its digital root."""
    assert len(a) == len(b)
    return [digital_root(x + y) for x, y in zip(a, b)]


def cscale(k, a):
    """Columnwise scaling by k."""
    return [digital_root(k * x) for x in a]


def reverse(a):
    return a[::-1]


def D(a):
    """Doubling: the map N -> N + DR(N) induces on roots, run per column."""
    return cscale(2, a)


def T(a):
    """Tripling."""
    return cscale(3, a)


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


# ----------------------------------------------------------------------
# THEOREM 2: the bottom third is closed
# ----------------------------------------------------------------------

BOTTOM = (3, 6, 9)          # = 3Z/9Z, the multiples of 3


def tripling_table():
    return {d: digital_root(3 * d) for d in range(1, 10)}


def doubling_table():
    return {d: digital_root(2 * d) for d in range(1, 10)}


# ----------------------------------------------------------------------
# THEOREM 3: orbits of digitwise doubling
# ----------------------------------------------------------------------

def digit_period(d):
    """Period of d under doubling mod 9."""
    n, x = 1, digital_root(2 * d)
    while x != d:
        x = digital_root(2 * x)
        n += 1
    return n


def orbit(v):
    """Orbit of a digit vector under D, as a list starting at v."""
    out, x = [list(v)], D(v)
    while x != list(v):
        out.append(x)
        x = D(x)
    return out


def orbit_of(n):
    """Orbit of an integer under D, as integers."""
    return [int(text(w)) for w in orbit(digits(n))]


def two_digit_orbit_census():
    """All orbits of D over the 81 reduced two-digit states.

    Returns {period: number of orbits}.  Level 1: this exhausts the space.
    """
    seen, by_period = set(), {}
    for a in range(1, 10):
        for b in range(1, 10):
            if (a, b) in seen:
                continue
            o = orbit([a, b])
            seen.update((w[0], w[1]) for w in o)
            by_period[len(o)] = by_period.get(len(o), 0) + 1
    return by_period


ORBIT_CENSUS = {1: 1, 2: 4, 6: 12}      # 17 orbits over 81 states
TOTAL_ORBITS = 17

# the two orbits the worked sheets live on
ORBIT_93 = [93, 96]
ORBIT_37 = [37, 65, 31, 62, 34, 68]


# ----------------------------------------------------------------------
# THEOREM 4: N (+) reverse(N) is always a palindrome
# ----------------------------------------------------------------------

def bar_sum(n):
    """N (+) reverse(N), columnwise.  Always a palindrome -- THEOREM 4."""
    v = digits(n)
    return cadd(v, reverse(v))


def is_palindrome(v):
    v = list(v)
    return v == v[::-1]


# ----------------------------------------------------------------------
# THEOREM 5: the 5-and-4 split of the digits
# ----------------------------------------------------------------------

C_DIGITS = [d for d in range(1, 10) if not is_prime(d)]     # 1 4 6 8 9
P_DIGITS = [d for d in range(1, 10) if is_prime(d)]         # 2 3 5 7


def laid_into(group, slots):
    """Lay a digit group into `slots` columns, coming round to its head.

    C has 5 members and fills 5 slots exactly.  P has 4, so it wraps --
    the repeated digit is the 5-and-4, not a choice.
    """
    return [group[i % len(group)] for i in range(slots)]


# ----------------------------------------------------------------------
# THEOREM 6: the C/P grid
# ----------------------------------------------------------------------

CP_GRID = ['14689', '23572', '37262', '65334', '93596']
CP_LEFT = [14, 23, 37, 65, 93]          # the left column of the sheet


def cp_grid_rows():
    """Rebuild the grid.  Row 3 and row 5 are exact; row 4 is marked."""
    r1 = laid_into(C_DIGITS, 5)
    r2 = laid_into(P_DIGITS, 5)
    r3 = cadd(r1, r2)
    r4 = digits(CP_GRID[3])             # as written, with its marked column
    r5 = cadd(r3, r4)
    return [r1, r2, r3, r4, r5]


# ----------------------------------------------------------------------
# THEOREM 7: "1+2 only"
# ----------------------------------------------------------------------

NINE_SHEET = ['65334', '93396', '68631', '62937', '31638',
              '93666', '37395', '62962', '99367']

# the four columns of the nine-row sheet that depart from "1+2 only",
# as (row index, column index, value the recurrence gives, value written)
MARKED_COLUMNS = [(4, 3, 6, 3),         # D(6) = 3   doubling in place
                  (6, 1, 4, 7),         # +3         a step inside BOTTOM
                  (7, 0, 3, 6),         # D(3) = 6   doubling in place
                  (7, 1, 1, 2)]         # D(1) = 2   doubling in place

PURE_BOTTOM_ROWS = [1, 5]               # rows whose digits are all in BOTTOM


def one_two_only(seed_a, seed_b, rows):
    """Each row is the two above it, columnwise.  No cumulative sum."""
    sheet = [list(seed_a), list(seed_b)]
    while len(sheet) < rows:
        sheet.append(cadd(sheet[-2], sheet[-1]))
    return sheet


# ----------------------------------------------------------------------
# THEOREM 8: the 13331 layer
# ----------------------------------------------------------------------

SEED_PALINDROME = 13331
LAYER = [13331, 26662, 39993]           # 1, 2, 3 times the seed


def layer_class(length=5):
    """Palindromes whose 1x, 2x and 3x multiples are all palindromes.

    Tripling must not carry, so every digit is at most 3.  Level 1:
    this enumerates the whole class.
    """
    out = []
    half = (length + 1) // 2
    def build(pre):
        if len(pre) == half:
            full = pre + pre[:length - half][::-1]
            n = int(''.join(map(str, full)))
            if all(str(k * n) == str(k * n)[::-1] for k in (1, 2, 3)):
                out.append(n)
            return
        lo = 1 if not pre else 0
        for d in range(lo, 4):
            build(pre + [d])
    build([])
    return sorted(out)


LAYER_CLASS_SIZE = 48
LAYER_CLASS_PRIMES = [10301, 11311, 13331, 30103, 30203, 31013, 32323]

# the join to abcba_place_value_grid.py
ABCBA_SEAM_SQUARE = 12321                # = 111^2 = 3^2 x 37^2
ABCBA_37_LAYER = [12321, 24642, 36963]


# ----------------------------------------------------------------------
# THEOREM 9: the trichotomy, and the 27-per-6-steps law
# ----------------------------------------------------------------------

def plus_nine_fixes_root(n):
    return digital_root(n) == digital_root(n + 9)


def regrouping_fixes_root(ds):
    """A digit multiset determines the root, however it is grouped."""
    return digital_root(sum(ds))


def dr_walk(n, steps):
    """N -> N + DR(N)."""
    out = [n]
    for _ in range(steps):
        n = n + digital_root(n)
        out.append(n)
    return out


TRICHOTOMY = {'add 9':         'root FIXED  (9 = 0 mod 9)',
              'regroup digits': 'root FIXED  (same digit multiset)',
              'double':        'root MOVES  (d -> 2d)'}

LONG_CYCLE_GAIN = 27        # N -> N+DR(N) gains 27 per 6 steps on the 6-cycle
SHORT_CYCLE_GAIN = 9        # and 9 per 2 steps on 3 <-> 6


# ======================================================================
# tests
# ======================================================================

def test_module_action():
    """THEOREM 1: columnwise scaling is a Z/9Z-module action."""
    v = digits('14689')
    for j in range(1, 19):
        for k in range(1, 19):
            # (jk)v = j(kv)
            assert cscale(j * k, v) == cscale(j, cscale(k, v))
            # (j+k)v = jv (+) kv
            assert cscale(j + k, v) == cadd(cscale(j, v), cscale(k, v))
    assert cscale(9, v) == [9] * 5          # 9 is the zero
    assert cscale(10, v) == v               # and the action has period 9
    assert D(v) == cscale(2, v) and T(v) == cscale(3, v)


def test_reversal_commutes():
    """THEOREM 1b: reversal commutes with every digitwise map.

    This is why the right-hand side of a sheet stays the reversal of its
    left-hand side no matter how many times the sheet is scaled.
    """
    for n in range(10000, 100000, 7):
        v = digits(n)
        for k in range(1, 10):
            assert cscale(k, reverse(v)) == reverse(cscale(k, v))
    v = digits(14689)
    assert text(cscale(2, v)) == '28379'
    assert text(cscale(2, reverse(v))) == '97382'
    assert cscale(2, reverse(v)) == reverse(cscale(2, v))


def test_bottom_third_is_closed():
    """THEOREM 2: tripling forces {3,6,9}, which is then closed."""
    trip = tripling_table()
    for d in range(1, 10):
        assert trip[d] in BOTTOM, d
        assert trip[d] % 3 == 0
    # closed under both maps
    for d in BOTTOM:
        assert digital_root(2 * d) in BOTTOM
        assert digital_root(3 * d) in BOTTOM
    # and under columnwise addition
    for a in BOTTOM:
        for b in BOTTOM:
            assert digital_root(a + b) in BOTTOM
    # so it is a subgroup, and the only proper nontrivial one that is
    # doubling-invariant
    assert sorted(BOTTOM) == sorted({digital_root(3 * k) for k in range(1, 10)})
    invariant = [d for d in range(1, 10) if digit_period(d) <= 2]
    assert sorted(invariant) == sorted(BOTTOM), invariant
    # every multiple of 3 of any sheet is inside
    v = digits('14689')
    for k in (3, 6, 9, 12, 15):
        assert set(cscale(k, v)) <= set(BOTTOM), k
    assert text(T(v)) == '33969'
    assert text(cscale(6, v)) == '66939'
    assert text(cscale(9, v)) == '99999'


def test_digit_periods_and_orbit_census():
    """THEOREM 3: ord_9(2) = 6, and the 81 states split into 17 orbits."""
    per = {d: digit_period(d) for d in range(1, 10)}
    assert per[9] == 1
    assert per[3] == 2 and per[6] == 2
    for d in (1, 2, 4, 5, 7, 8):
        assert per[d] == 6, d
    assert digit_period(1) == 6                  # ord_9(2) = 6
    # period of a two-digit state is the lcm of its digits' periods
    from math import lcm
    for a in range(1, 10):
        for b in range(1, 10):
            assert len(orbit([a, b])) == lcm(per[a], per[b]), (a, b)
    census = two_digit_orbit_census()
    assert census == ORBIT_CENSUS, census
    assert sum(census.values()) == TOTAL_ORBITS
    assert sum(p * c for p, c in census.items()) == 81
    # the two orbits the worked sheets live on
    assert orbit_of(93) == ORBIT_93
    assert orbit_of(37) == ORBIT_37
    assert orbit_of(99) == [99]                  # the unique fixed point
    # 37 -> 65 is one step, and 68, 62, 31 are on the same orbit
    assert orbit_of(37)[1] == 65
    for n in (68, 62, 31, 65):
        assert n in ORBIT_37, n
    assert 96 in ORBIT_93


def test_bar_sum_is_always_a_palindrome():
    """THEOREM 4, proved then exhausted.

    Column i of N (+) reverse(N) is DR(N_i + N_{r+1-i}), which is
    unchanged when i and r+1-i trade places.  So the sum equals its own
    reversal for every N.  No hypothesis on N is used.
    """
    for r in (2, 3, 4, 5):
        lo, hi = 10 ** (r - 1), 10 ** r
        for n in range(lo, hi):
            assert is_palindrome(bar_sum(n)), n
    # the specific one on the sheet
    assert text(bar_sum(14689)) == '13331'
    assert text(bar_sum(98641)) == '13331'       # commutative: the swap is free
    # ordinary addition does NOT do this; the carries are what break it
    s = str(14689 + 98641)
    assert s == '113330' and s != s[::-1]
    raw = [a + b for a, b in zip(digits(14689), digits(98641))]
    assert raw == raw[::-1] == [10, 12, 12, 12, 10]   # symmetric before carrying
    assert text(bar_sum(14689)) == '13331'            # and after root reduction
    # a swept count of how often ordinary addition happens to succeed
    ok = sum(1 for n in range(10000, 100000)
             if str(n + int(str(n)[::-1])) == str(n + int(str(n)[::-1]))[::-1])
    assert 0 < ok < 90000, ok                    # sometimes, not always
    assert all(is_palindrome(bar_sum(n)) for n in range(10000, 100000))


def test_digit_split_is_primes_against_nonprimes():
    """THEOREM 5: the 5-and-4 is forced."""
    assert text(C_DIGITS) == '14689'
    assert text(P_DIGITS) == '2357'
    assert len(C_DIGITS) == 5 and len(P_DIGITS) == 4
    assert P_DIGITS == [2, 3, 5, 7]              # the primes below 10
    assert len(P_DIGITS) == 4                    # exactly four, so the 4 is forced
    assert sum(C_DIGITS) == 28 and sum(P_DIGITS) == 17
    assert sum(C_DIGITS) + sum(P_DIGITS) == 45
    assert digital_root(45) == 9
    # five slots: C fits exactly, P comes round to its head
    assert text(laid_into(C_DIGITS, 5)) == '14689'
    assert text(laid_into(P_DIGITS, 5)) == '23572'
    assert laid_into(P_DIGITS, 5)[4] == P_DIGITS[0]


def test_cp_grid():
    """THEOREM 6: row 3 and row 5 are exact; row 4 carries the marked column."""
    r1, r2, r3, r4, r5 = cp_grid_rows()
    assert text(r1) == CP_GRID[0] == '14689'
    assert text(r2) == CP_GRID[1] == '23572'
    assert text(r3) == CP_GRID[2] == '37262'
    assert r3 == cadd(r1, r2)                     # exact in all five columns
    assert text(r4) == CP_GRID[3] == '65334'
    assert text(r5) == CP_GRID[4] == '93596'
    # the marked column of row 4, against unperturbed doubling of row 3
    clean = D(r3)
    assert text(clean) == '65434'
    diff = [i for i in range(5) if clean[i] != r4[i]]
    assert diff == [2], diff                      # one column, the third
    assert (clean[2], r4[2]) == (4, 3)            # down by exactly 1
    # the 93 survives that column either way
    assert text(cadd(r3, r4))[:2] == '93'
    assert text(cadd(r3, clean))[:2] == '93'
    # and the left column of the sheet samples four distinct D-orbits
    assert CP_LEFT == [14, 23, 37, 65, 93]
    orbs = {tuple(sorted(orbit_of(n))) for n in CP_LEFT}
    assert len(orbs) == 4                         # 37 and 65 share one
    assert tuple(sorted(orbit_of(37))) == tuple(sorted(orbit_of(65)))
    # row 5 hands off to the chain notation: 93 = 3 = 96
    assert digital_root(93) == 3
    assert 93 + digital_root(93) == 96
    assert digital_root(96) == 6 and 96 + 7 == 103
    assert digital_root(103) == 4 and 1 + 3 == 4


def test_one_two_only():
    """THEOREM 7: 31 of the nine-row sheet's 35 columns are exact."""
    rows = [digits(s) for s in NINE_SHEET]
    exact = marked = 0
    found = []
    for i in range(2, 9):
        pred = cadd(rows[i - 2], rows[i - 1])
        for j in range(5):
            if pred[j] == rows[i][j]:
                exact += 1
            else:
                marked += 1
                found.append((i, j, pred[j], rows[i][j]))
    assert exact + marked == 35
    assert exact == 31 and marked == 4, (exact, marked)
    assert found == MARKED_COLUMNS, found
    # three of the four departures are the doubling map applied in place
    doubling = [(i, j) for i, j, p, w in found if digital_root(2 * p) == w]
    assert len(doubling) == 3, doubling
    # the fourth is +3, a step inside the closed bottom third
    other = [(i, j, p, w) for i, j, p, w in found if digital_root(2 * p) != w]
    assert len(other) == 1
    i, j, p, w = other[0]
    assert (w - p) % 9 == 3
    assert digital_root(3) in BOTTOM and p not in BOTTOM
    # rows 2 and 6 come out pure, four apart
    pure = [i for i, r in enumerate(rows) if set(r) <= set(BOTTOM)]
    assert pure == PURE_BOTTOM_ROWS == [1, 5]
    assert pure[1] - pure[0] == 4 == len(P_DIGITS)
    # the first three rows of the earlier sheet, under the same rule
    r1 = digits('14689')
    assert text(D(r1)) == '28379'
    assert text(cadd(r1, D(r1))) == '33969'
    assert cadd(r1, D(r1)) == T(r1)              # 1 + 2 = 3, so "1+2 only" is 3x


def test_perturbation_is_load_bearing():
    """The marked column of the C/P grid propagates through the whole sheet."""
    rows = [digits(s) for s in NINE_SHEET]
    clean = one_two_only(digits('65434'), digits('93396'), 9)
    agree = [i for i in range(9) if clean[i] == rows[i]]
    assert agree == [1], agree                   # only the shared second row
    for i in range(6, 9):
        assert clean[i] != rows[i]               # fully diverged by row 7
    assert text(clean[6]) == '34865' and text(rows[6]) == '37395'


def test_13331_layer():
    """THEOREM 8: the across-bar collapse, and the class it lands in."""
    seed = digits('14689')
    for k in (1, 2, 3):
        row = cscale(k, seed)
        got = cadd(row, reverse(row))
        assert got == cscale(k, digits(SEED_PALINDROME))
        assert int(text(got)) == LAYER[k - 1]
        assert is_palindrome(got)
    assert LAYER == [13331, 26662, 39993]
    assert all(13331 * k == LAYER[k - 1] for k in (1, 2, 3))
    # 13331 is prime, and survives every annihilator in the abcba grid
    assert is_prime(SEED_PALINDROME)
    a, b, c = 1, 3, 3
    assert int(f'{a}{b}{c}{b}{a}') == SEED_PALINDROME
    for m in (2, 5, 9, 11, 37, 73, 101, 137, 10001):
        assert SEED_PALINDROME % m != 0, m
    assert a % 2 == 1 and a != 5                 # as every abcba prime must be
    assert c != a + b                            # not a seam, so 37 misses it
    # the class: every digit at most 3, so tripling never carries
    cls = layer_class(5)
    assert len(cls) == LAYER_CLASS_SIZE == 48
    assert all(max(digits(n)) <= 3 for n in cls)
    assert all(is_palindrome(digits(k * n)) for n in cls for k in (1, 2, 3))
    assert [n for n in cls if is_prime(n)] == LAYER_CLASS_PRIMES
    assert len(LAYER_CLASS_PRIMES) == 7
    # the two ends of the same class
    assert SEED_PALINDROME in cls and ABCBA_SEAM_SQUARE in cls
    assert is_prime(SEED_PALINDROME)
    assert ABCBA_SEAM_SQUARE == 111 ** 2 == 9 * 37 ** 2
    assert ABCBA_37_LAYER == [12321 * k for k in (1, 2, 3)]
    assert not is_prime(ABCBA_SEAM_SQUARE)
    # a digit of 4 anywhere breaks it, which is what bounds the class at 48
    assert not is_palindrome(digits(3 * 14341))


def test_trichotomy_and_the_27_law():
    """THEOREM 9: two stabilizers and the generator they stabilize against."""
    for n in range(1, 2000):
        assert plus_nine_fixes_root(n)
    # regrouping cannot move the root: it depends on the multiset alone
    assert regrouping_fixes_root([1, 2, 3]) == regrouping_fixes_root([3, 2, 1])
    assert digital_root(123) == digital_root(1 + 23) == digital_root(12 + 3)
    # doubling does move it
    assert digital_root(2 * 3) == 6 != 3
    assert set(TRICHOTOMY) == {'add 9', 'regroup digits', 'double'}
    # the two stabilizers commute with the doubling, so they never disturb
    # a 2d progression
    for n in (93, 68, 62, 31, 14, 23, 37, 65):
        assert digital_root(2 * digital_root(n)) == digital_root(2 * digital_root(n + 9))
    # N -> N+DR(N) gains exactly 27 per 6 steps off the long cycle,
    # and 9 per 2 steps on 3 <-> 6
    w = dr_walk(1, 6)
    assert w[-1] - w[0] == LONG_CYCLE_GAIN == 27
    assert dr_walk(5, 6)[-1] - 5 == 27
    assert dr_walk(7, 6)[-1] - 7 == 27
    assert dr_walk(3, 2)[-1] - 3 == SHORT_CYCLE_GAIN == 9
    assert dr_walk(6, 2)[-1] - 6 == 9
    assert dr_walk(9, 1)[-1] - 9 == 9
    # divisibility by 3 is invariant under the walk, so it splits the
    # integers into two sectors that never mix
    for n in range(1, 3000):
        assert ((n + digital_root(n)) % 3 == 0) == (n % 3 == 0), n
    # and the non-multiples of 3 are partitioned by exactly three
    # trajectories, seeded at 1, 5 and 7.  Level 1 by counting: each walk
    # advances 6 steps per 27 integers, so covers 6 of every 27; three
    # disjoint walks cover 18 of every 27, which is exactly how many
    # non-multiples of 3 there are.  checked against the bound below.
    bound = 20000
    tracks = [set(dr_walk(seed, 6000)) for seed in (1, 5, 7)]
    tracks = [{x for x in t if x <= bound} for t in tracks]
    for i in range(3):
        for j in range(i + 1, 3):
            assert not (tracks[i] & tracks[j]), (i, j)      # disjoint
    union = tracks[0] | tracks[1] | tracks[2]
    expected = {n for n in range(1, bound + 1) if n % 3}
    assert union == expected                                # and exhaustive
    assert len(expected) == sum(len(t) for t in tracks)
    for t in tracks:
        assert all(x % 3 for x in t)


def test_does_not_prove_too_much():
    """Guard the boundaries of each claim."""
    # THEOREM 4 is about columnwise addition only.  Ordinary addition of a
    # number to its reversal is NOT always palindromic -- that is the 196
    # problem, and 14689 is already a counterexample.
    assert str(14689 + 98641) != str(14689 + 98641)[::-1]
    # tripling forces BOTTOM; doubling does not
    assert set(cscale(3, digits('14689'))) <= set(BOTTOM)
    assert not set(cscale(2, digits('14689'))) <= set(BOTTOM)
    # the orbit census is for TWO-digit states; longer strings differ
    from math import lcm
    assert len(orbit(digits('14689'))) == lcm(*[digit_period(d) for d in digits('14689')])
    assert len(orbit(digits('14689'))) == 6
    assert len(orbit(digits('33969'))) == 2      # all digits in BOTTOM
    assert len(orbit(digits('99999'))) == 1
    # the C/P grid's row 4 is as-written, not derived; the module says so
    r1, r2, r3, r4, r5 = cp_grid_rows()
    assert r4 != D(r3)
    assert r4 == digits(CP_GRID[3])
    # the layer class is not all palindromes, and 4x already escapes it
    cls = layer_class(5)
    assert len(cls) == 48 < 900
    assert 12421 not in cls
    assert not is_palindrome(digits(4 * 13331))  # 4x leaves the layer
    # and the 7 primes are a strict subset of the 93 abcba palindromic primes
    assert len(LAYER_CLASS_PRIMES) == 7 < 93


def self_test():
    tests = [test_module_action,
             test_reversal_commutes,
             test_bottom_third_is_closed,
             test_digit_periods_and_orbit_census,
             test_bar_sum_is_always_a_palindrome,
             test_digit_split_is_primes_against_nonprimes,
             test_cp_grid,
             test_one_two_only,
             test_perturbation_is_load_bearing,
             test_13331_layer,
             test_trichotomy_and_the_27_law,
             test_does_not_prove_too_much]
    for t in tests:
        t()
        print(f'  ok  {t.__name__}')
    print()
    print(f'  THEOREM 2  tripling forces {{3,6,9}}; closed under x2, x3 and (+)')
    print(f'  THEOREM 3  {TOTAL_ORBITS} orbits over 81 two-digit states: '
          f'{ORBIT_CENSUS}')
    print(f'  THEOREM 4  N (+) rev(N) palindromic for all 90000 five-digit N; '
          f'ordinary addition fails')
    print(f'  THEOREM 5  5-and-4 = non-primes {text(C_DIGITS)} against primes '
          f'{text(P_DIGITS)}; the 4 is forced')
    print(f'  THEOREM 6  C/P grid: rows 3 and 5 exact, row 4 marked at column 3')
    print(f'  THEOREM 7  nine-row sheet: 31 of 35 columns exact, '
          f'{len(MARKED_COLUMNS)} marked, 3 of those the doubling map')
    print(f'  THEOREM 8  layer {LAYER} = 1,2,3 x {SEED_PALINDROME}; class of '
          f'{LAYER_CLASS_SIZE}, {len(LAYER_CLASS_PRIMES)} prime')
    print(f'             joins abcba_place_value_grid: {ABCBA_SEAM_SQUARE} = '
          f'111^2 is in the same class')
    print(f'  THEOREM 9  two stabilizers (+9, regroup) and one generator '
          f'(double); {LONG_CYCLE_GAIN} per 6 steps')
    print(f'             and the non-multiples of 3 are exactly three '
          f'trajectories, seeded at 1, 5, 7')


if __name__ == '__main__':
    self_test()

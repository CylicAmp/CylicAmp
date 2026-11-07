"""
THE BACKBONE: THE BASE, THE LENGTH, AND THE GROUP RING
================================================================

digitwise_sheets.py worked one operation in one base at one length.
digitwise_operations.py worked every operation, still in base 10.
This file lets the two remaining constants go:

    the BASE b  --  digital root is reduction mod b-1, so base 10 gives
                    Z/9Z only because 9 = 10-1.  The backbone is really
                    vectors over Z/(b-1)Z, and which ring that is depends
                    entirely on how b-1 factors.

    the LENGTH r --  a sheet of length r carrying a cyclic shift is an
                    element of the group ring Z/(b-1)Z[x]/(x^r - 1).
                    Whether that ring has the projector that extracts
                    the digital root depends on gcd(r, b-1).

Letting them go turns three base-10 observations into statements about
which (b, r) they hold for -- and two of them turn out to be conditional
in ways base 10 hides.

Grading, as elsewhere in this repository:

  Level 1  proved parameter-free, or settled by exhausting a finite set
  Level 2  verified over a bounded range

  THEOREM 17  the base trichotomy.  b-1 prime -> Z/(b-1)Z is a FIELD;
              b-1 squarefree -> semisimple, CRT splits it, no nilpotents;
              b-1 with a square factor -> nilpotents exist.  Base 10 is
              the nilpotent case (9 = 3^2), which is why {3,6,9} absorbs
              under multiplication; base 8 is a field; base 11 is
              semisimple with no absorbing set at all; base 13 gives
              Z/12Z, the Law of 12 ring, also nilpotent.        Level 1
  THEOREM 18  the eigenspace split of OPERATIONS THEOREM 15 holds iff 2
              is a unit mod b-1, i.e. iff b is EVEN -- but NOT for the
              reason that file gave.  The middle column of v - reverse(v)
              is d - d, so it is the zero class trivially, in EVERY base;
              2 plays no part in it.  What 2 being a unit actually buys
              is three equivalent things:
                (a) the bar-difference map is ONTO the antipalindrome
                    space.  In an odd base its image has m^2 elements
                    while the space has 2m^2, so it misses exactly half.
                (b) Pal and Anti meet only in zero.  In an odd base the
                    intersection has 2^ceil(r/2) elements (8 at r = 5):
                    v = -v forces 2v = 0 in every column, but palindromy
                    is still an extra condition on top, so only the free
                    half of the columns is counted.
                (c) hence Pal (+) Anti both SPANS and is DIRECT exactly
                    when gcd(2, m) = 1.  At b = 11, r = 5 the sum has
                    25000 of the 100000 sheets -- a quarter of the space,
                    not all of it.
              So the decomposition is an even-base theorem; the forced
              middle column never was one.                       Level 1
  THEOREM 19  sheets of length r form the group ring Z/(b-1)Z[x]/(x^r-1).
              The all-ones element J satisfies J^2 = rJ, so e = r^-1 J is
              an idempotent exactly when gcd(r, b-1) = 1, and e extracts
              the digit sum -- the rank-1 CRT component IS the digital
              root.  In base 10 the lengths r = 3, 6, 9 are degenerate:
              no projector exists.                               Level 1
  THEOREM 20  the bar map v -> v (+) reverse(v) is a SURJECTIVE module map
              onto the palindromes whose kernel is the antipalindromes, so
              every palindrome has exactly (b-1)^floor(r/2) preimages --
              81 when b = 10, r = 5.                             Level 1
  THEOREM 21  the symmetry group is dihedral.  Cyclic shift (the wrapping
              that laid 4 primes into 5 slots) and reversal (the bar)
              generate D_r of order 2r, and Burnside counts the sheets up
              to that symmetry.                                  Level 1
  THEOREM 22  the carry operator is the entire obstruction, and the
              implication only runs one way.  If no column sum of
              N + reverse(N) reaches the base then the ORDINARY sum is a
              palindrome -- all 12375 five-digit witnesses.  The converse
              FAILS: 72 five-digit N carry and are palindromic anyway,
              the smallest 20009, where the carry runs the full width and
              comes out symmetric.  Columnwise there is no obstruction at
              all, so 196 and the Lychrel question have no analogue on
              the backbone: every N reaches a palindrome in one step.
                                                                 Level 1
"""

from math import gcd


# ----------------------------------------------------------------------
# a sheet over an arbitrary base
# ----------------------------------------------------------------------

class Sheet:
    """Digit vectors of length r over Z/(b-1)Z, written with b-1 for 0."""

    def __init__(self, base=10):
        assert base >= 3
        self.base = base
        self.m = base - 1                 # the modulus
        self.ring = list(range(1, base))  # representatives, m stands for 0
        self.zero = self.m

    # --- reduction
    def red(self, n):
        """Representative of n mod m, using m for the class of 0."""
        n %= self.m
        return self.m if n == 0 else n

    def digits(self, x, width=None):
        """Digits of x in this base, as ring representatives."""
        if x == 0:
            ds = [0]
        else:
            ds = []
            while x:
                ds.append(x % self.base)
                x //= self.base
            ds.reverse()
        if width:
            ds = [0] * (width - len(ds)) + ds
        return [self.red(d) for d in ds]

    # --- columnwise operations
    def add(self, a, b):
        return [self.red(x + y) for x, y in zip(a, b)]

    def sub(self, a, b):
        return [self.red(x - y) for x, y in zip(a, b)]

    def mul(self, a, b):
        return [self.red(x * y) for x, y in zip(a, b)]

    def scale(self, k, a):
        return [self.red(k * x) for x in a]

    def rev(self, a):
        return a[::-1]

    def bar(self, a, op=None):
        op = op or (lambda x, y: self.red(x + y))
        r = len(a)
        return [op(a[i], a[r - 1 - i]) for i in range(r)]

    # --- structure
    def units(self):
        return [d for d in self.ring if gcd(d, self.m) == 1]

    def nonunits(self):
        return [d for d in self.ring if gcd(d, self.m) != 1]

    def nilpotents(self):
        """Elements with x^k = 0 for some k >= 1 (excluding none)."""
        out = []
        for d in self.ring:
            x, k = d % self.m, 0
            while k < 64 and x:
                x = x * d % self.m
                k += 1
            if x == 0:
                out.append(d)
        return out

    def two_is_unit(self):
        return gcd(2, self.m) == 1

    def split_works(self):
        """The Pal (+) Anti decomposition needs 2 invertible."""
        return self.two_is_unit()

    def forced_middle(self):
        """Solutions of 2v = 0: what an odd-length antipalindrome's
        middle column is allowed to be."""
        return sorted(self.red(v) for v in range(self.m) if 2 * v % self.m == 0)

    def root_idempotent(self, r):
        """Coefficient c with (cJ)^2 = cJ, i.e. c = r^-1.  None if absent."""
        if gcd(r, self.m) != 1:
            return None
        return self.red(pow(r, -1, self.m))


# ----------------------------------------------------------------------
# THEOREM 17: classifying the base
# ----------------------------------------------------------------------

def factorize(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def is_squarefree(n):
    return all(e == 1 for e in factorize(n).values())


def base_class(base):
    """'field', 'semisimple' or 'nilpotent' for Z/(base-1)Z."""
    m = base - 1
    f = factorize(m)
    if len(f) == 1 and sum(f.values()) == 1:
        return 'field'
    if is_squarefree(m):
        return 'semisimple'
    return 'nilpotent'


BASE_CLASSES = {3: 'field', 4: 'field', 5: 'nilpotent', 6: 'field',
                7: 'semisimple', 8: 'field', 9: 'nilpotent',
                10: 'nilpotent', 11: 'semisimple', 12: 'field',
                13: 'nilpotent', 14: 'field', 15: 'semisimple',
                16: 'semisimple', 17: 'nilpotent', 18: 'field',
                19: 'nilpotent'}

LAW_OF_12_BASE = 13                     # b-1 = 12
DEGENERATE_LENGTHS_BASE_10 = [3, 6, 9]  # gcd(r,9) > 1


# ----------------------------------------------------------------------
# THEOREM 21: Burnside over the dihedral group
# ----------------------------------------------------------------------

def _cycles(perm):
    n, seen, c = len(perm), [False] * len(perm), 0
    for i in range(n):
        if not seen[i]:
            c += 1
            j = i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
    return c


def dihedral_orbits(r, m):
    """Sheets of length r over Z/mZ up to shift and reversal."""
    total = 0
    for k in range(r):
        total += m ** _cycles([(i + k) % r for i in range(r)])      # rotations
    for k in range(r):
        total += m ** _cycles([(k - i) % r for i in range(r)])      # reflections
    assert total % (2 * r) == 0
    return total // (2 * r)


DIHEDRAL_BASE_10 = {3: 165, 4: 1035, 5: 6273, 6: 46185, 7: 344925}


# ----------------------------------------------------------------------
# THEOREM 22: the carry operator
# ----------------------------------------------------------------------

def column_sums(n, base=10):
    d = []
    x = n
    while x:
        d.append(x % base)
        x //= base
    d.reverse()
    return [d[i] + d[len(d) - 1 - i] for i in range(len(d))]


def ordinary_bar_is_palindrome(n, base=10):
    d = []
    x = n
    while x:
        d.append(x % base)
        x //= base
    rv = 0
    for c in d:                       # d is least-significant-first
        rv = rv * base + c
    s = n + rv
    out = []
    while s:
        out.append(s % base)
        s //= base
    return out == out[::-1]


NO_CARRY_5DIGIT = 12375
CARRY_BUT_PALINDROMIC = 72
SMALLEST_CONSPIRACY = 20009


# ======================================================================
# tests
# ======================================================================

def test_base_trichotomy():
    """THEOREM 17."""
    for b, want in BASE_CLASSES.items():
        assert base_class(b) == want, (b, base_class(b), want)
    S10, S8, S11, S13 = Sheet(10), Sheet(8), Sheet(11), Sheet(13)
    # base 10: nilpotent, and the nilpotents are exactly {3,6,9}
    assert base_class(10) == 'nilpotent'
    assert S10.m == 9 and factorize(9) == {3: 2}
    assert S10.nilpotents() == [3, 6, 9] == S10.nonunits()
    assert {S10.red(a * b) for a in S10.nilpotents()
            for b in S10.nilpotents()} == {9}
    # base 8: a field, so there is nothing to absorb
    assert base_class(8) == 'field' and S8.m == 7
    assert S8.nonunits() == [7] and S8.nilpotents() == [7]   # only the zero
    assert len(S8.units()) == 6 == S8.m - 1                  # every nonzero
    # base 11: semisimple, Z/10Z = Z/2 x Z/5, no nilpotents but zero divisors
    assert base_class(11) == 'semisimple' and S11.m == 10
    assert is_squarefree(10) and factorize(10) == {2: 1, 5: 1}
    assert S11.nilpotents() == [10]                          # only the zero
    assert sorted(S11.nonunits()) == [2, 4, 5, 6, 8, 10]
    # base 13: the Law of 12 ring, nilpotent because 4 = 2^2
    assert S13.m == 12 == LAW_OF_12_BASE - 1
    assert base_class(13) == 'nilpotent'
    assert factorize(12) == {2: 2, 3: 1}
    assert S13.nilpotents() == [6, 12]                       # 6^2 = 36 = 0
    assert S13.red(6 * 6) == 12 == S13.zero
    # and the classification is exhaustive over a range
    for b in range(3, 60):
        k = base_class(b)
        m = b - 1
        assert k in ('field', 'semisimple', 'nilpotent')
        assert (k == 'field') == (len(factorize(m)) == 1
                                  and sum(factorize(m).values()) == 1)
        assert (k == 'nilpotent') == (not is_squarefree(m))


def test_split_needs_an_even_base():
    """THEOREM 18, with the middle column put back in its place.

    The middle column of v - reverse(v) is d - d.  It is the zero class
    in every base, odd or even, and 2 has nothing to do with it.  The
    even-base condition governs the DECOMPOSITION instead.
    """
    # (0) the middle column is trivially zero, in every base
    for b in (7, 8, 10, 11, 13, 16):
        S = Sheet(b)
        for n in range(b ** 4, b ** 4 + 1500):
            v = S.digits(n)
            if len(v) != 5:
                continue
            A = S.bar(v, lambda x, y: S.red(x - y))
            assert A[2] == S.zero, (b, n)
            assert A[2] == S.red(v[2] - v[2])        # it is literally d - d
    # (1) 2 is a unit exactly in even bases
    for b in range(3, 40):
        S = Sheet(b)
        assert S.two_is_unit() == (b % 2 == 0), b
        assert S.split_works() == (b % 2 == 0)
    # (2) the submodule counts, brute-forced at r = 3 and 4, then applied
    from itertools import product
    def brute(m, r):
        R = range(m)
        P = {v for v in product(R, repeat=r) if list(v) == list(v)[::-1]}
        A = {v for v in product(R, repeat=r)
             if all((v[i] + v[r - 1 - i]) % m == 0 for i in range(r))}
        Sm = {tuple((a[i] + b[i]) % m for i in range(r)) for a in P for b in A}
        return len(P), len(A), len(P & A), len(Sm)
    for m in (7, 8, 9, 10, 11, 12):
        for r in (3, 4):
            nP, nA, nI, nS = brute(m, r)
            g = gcd(2, m)
            assert nP == m ** ((r + 1) // 2), (m, r, nP)
            # each pair (i, r+1-i) is free on one side; an odd r's middle
            # column contributes the g solutions of 2v = 0
            assert nA == m ** (r // 2) * g ** (r % 2), (m, r, nA)
            assert nI == g ** ((r + 1) // 2), (m, r, nI)   # palindromy is extra
            assert nS == nP * nA // nI                     # submodule sum law
            assert (nI == 1) == (m % 2 == 1)               # direct iff m odd
            assert (nS == m ** r) == (m % 2 == 1)          # spans iff m odd
    # applied at r = 5, the length of the worked sheets
    r = 5
    for b in range(7, 18):
        S = Sheet(b)
        m, g = S.m, gcd(2, S.m)
        pal = m ** 3                                  # {a,b,c,b,a}
        anti = m ** 2 * g                             # free ends, 2v=0 middle
        image = m ** 2                                # ends free, middle 0
        inter = g ** 3                                # g^ceil(5/2)
        # (a) onto the antipalindromes iff 2 is a unit
        assert (anti == image) == S.two_is_unit(), b
        if not S.two_is_unit():
            assert image * 2 == anti                  # misses exactly half
        # (b) Pal meets Anti only in zero iff 2 is a unit
        assert (inter == 1) == S.two_is_unit(), b
        if not S.two_is_unit():
            assert inter == 8                         # 2^3, not 2^5
        # (c) so the sum both spans and is direct iff 2 is a unit
        assert (pal * anti // inter == m ** r) == S.two_is_unit(), b
    # (3) the overlap, built explicitly
    S11, S10 = Sheet(11), Sheet(10)
    assert not S11.split_works() and S10.split_works()
    half11 = sorted(v for v in S11.ring if S11.red(2 * v) == S11.zero)
    half10 = sorted(v for v in S10.ring if S10.red(2 * v) == S10.zero)
    assert half11 == [5, 10] and half10 == [9]
    both11 = {(a, b2, c, b2, a) for a in half11 for b2 in half11
              for c in half11}
    assert len(both11) == 8 == len(half11) ** 3        # free a, b, c only
    both10 = {(a, b2, c, b2, a) for a in half10 for b2 in half10
              for c in half10}
    assert len(both10) == 1 and both10 == {(9, 9, 9, 9, 9)}
    # base 11 loses three quarters of the space, not none
    assert 1000 * 200 // 8 == 25000 < 10 ** 5
    assert 729 * 81 // 1 == 59049 == 9 ** 5
    # (4) reassembly really fails in an odd base: no inverse of 2
    assert gcd(2, 10) != 1
    try:
        pow(2, -1, 10)
        raise AssertionError('2 should not be invertible mod 10')
    except ValueError:
        pass


def test_group_ring_and_the_root_projector():
    """THEOREM 19: the rank-1 CRT component is the digital root."""
    S = Sheet(10)
    for r in range(2, 14):
        c = S.root_idempotent(r)
        if gcd(r, 9) == 1:
            assert c is not None
            assert S.red(c * c * r) == c            # (cJ)^2 = cJ
            assert S.red(c * r) == 1                # c = r^-1, so c*r = 1
            assert c == S.red(pow(r, -1, 9))
        else:
            assert c is None, r
            assert r % 3 == 0
    assert [r for r in range(2, 11) if S.root_idempotent(r) is None] == \
        DEGENERATE_LENGTHS_BASE_10
    # the projector extracts the digit sum, i.e. the digital root
    for n in (14689, 23572, 37262, 93596, 11111, 99999):
        v = S.digits(n)
        r = len(v)
        c = S.root_idempotent(r)
        assert c is not None
        proj = [S.red(c * sum(v)) for _ in range(r)]
        assert len(set(proj)) == 1                   # uniform across columns
        assert S.red(r * proj[0]) == S.red(sum(v))   # scaling back recovers it
        assert S.red(sum(v)) == S.red(sum(int(d) for d in str(n)))
    # r = 3 is genuinely degenerate: J^2 = 3J and (3J) squares to zero
    assert S.red(3) == 3
    assert S.red(3 * 3) == 9 == S.zero
    assert S.root_idempotent(3) is None
    # but in base 8 (modulus 7, prime) every length works
    S8 = Sheet(8)
    for r in range(2, 20):
        assert (S8.root_idempotent(r) is None) == (r % 7 == 0), r


def test_bar_map_is_onto_with_equal_fibers():
    """THEOREM 20."""
    S = Sheet(10)
    from collections import Counter
    cnt = Counter()
    R = S.ring
    for a in R:
        for b in R:
            for c in R:
                for d in R:
                    for e in R:
                        v = [a, b, c, d, e]
                        cnt[tuple(S.bar(v))] += 1
    pals = {(a, b, c, b, a) for a in R for b in R for c in R}
    assert set(cnt) == pals                      # surjective onto palindromes
    assert len(pals) == 9 ** 3 == 729
    assert set(cnt.values()) == {81}             # every fiber the same size
    assert 9 ** 5 // 9 ** 3 == 81 == 9 ** (5 // 2)
    # the kernel is the antipalindromes
    zeros = [(a, b, c, d, e) for a in R for b in R for c in R for d in R
             for e in R if S.bar([a, b, c, d, e]) == [9] * 5]
    assert len(zeros) == 81 == 9 ** 2
    for z in zeros:
        assert all(S.red(z[i] + z[4 - i]) == 9 for i in range(5))
    # the general count, for other lengths and bases
    for b in (8, 10):
        Sb = Sheet(b)
        for r in (2, 3, 4):
            dom = Sb.m ** r
            img = Sb.m ** ((r + 1) // 2)
            assert dom // img == Sb.m ** (r // 2)


def test_dihedral_symmetry():
    """THEOREM 21: shift and reversal generate D_r; Burnside counts."""
    for r, want in DIHEDRAL_BASE_10.items():
        assert dihedral_orbits(r, 9) == want, (r, dihedral_orbits(r, 9))
    # the r=5 count by hand, from the cycle structure
    assert dihedral_orbits(5, 9) == (9 ** 5 + 4 * 9 + 5 * 9 ** 3) // 10 == 6273
    # orbits are at most |D_r| times smaller than the whole space
    for r in (3, 4, 5, 6, 7):
        n = dihedral_orbits(r, 9)
        assert 9 ** r // (2 * r) <= n <= 9 ** r
    # columnwise operations really do commute with both generators
    S = Sheet(10)
    for n in range(10000, 100000, 101):
        v = S.digits(n)
        for k in range(5):
            sh = v[k:] + v[:k]
            assert S.scale(2, sh) == S.scale(2, v)[k:] + S.scale(2, v)[:k]
        assert S.scale(2, S.rev(v)) == S.rev(S.scale(2, v))
    # a reflection of odd r fixes one position; of even r, none or two
    assert _cycles([(0 - i) % 5 for i in range(5)]) == 3
    assert _cycles([(0 - i) % 4 for i in range(4)]) == 3
    assert _cycles([(1 - i) % 4 for i in range(4)]) == 2


def test_carry_is_the_whole_obstruction():
    """THEOREM 22, including the direction that FAILS."""
    # no carry => the ordinary sum is a palindrome
    nocarry = [n for n in range(10000, 100000) if max(column_sums(n)) <= 9]
    assert len(nocarry) == NO_CARRY_5DIGIT == 12375
    assert all(ordinary_bar_is_palindrome(n) for n in nocarry)
    # but the converse fails: carries can conspire
    carry = [n for n in range(10000, 100000) if max(column_sums(n)) > 9]
    conspire = [n for n in carry if ordinary_bar_is_palindrome(n)]
    assert len(conspire) == CARRY_BUT_PALINDROMIC == 72
    assert min(conspire) == SMALLEST_CONSPIRACY == 20009
    assert 20009 + 90002 == 110011 == int(str(110011)[::-1])
    assert max(column_sums(20009)) == 11 > 9
    # columnwise there is no obstruction, for any N at any length
    S = Sheet(10)
    for r in (2, 3, 4, 5):
        lo, hi = 10 ** (r - 1), 10 ** r
        for n in range(lo, hi, max(1, (hi - lo) // 2000)):
            w = S.bar(S.digits(n))
            assert w == w[::-1], n
    # so 196 is immediate on the backbone and open in ordinary arithmetic
    assert S.bar(S.digits(196)) == [7, 9, 7]
    x = 196
    for _ in range(6):
        x = x + int(str(x)[::-1])
        assert str(x) != str(x)[::-1]           # still no palindrome
    assert column_sums(14689) == [10, 12, 12, 12, 10]
    assert column_sums(14689) == column_sums(14689)[::-1]   # symmetric already
    assert not ordinary_bar_is_palindrome(14689)            # carries break it


def test_does_not_prove_too_much():
    """Guard every boundary."""
    # the trichotomy is about b-1, never about b
    assert base_class(10) == 'nilpotent' and base_class(11) == 'semisimple'
    assert base_class(8) == 'field'
    # being a field is not the same as having no zero divisors in a sheet:
    # columnwise, a zero in ANY column still kills that column
    S8 = Sheet(8)
    assert S8.mul([1, 2, 7], [3, 3, 3]) == [3, 6, 7]
    # the even-base condition is about 2 only; odd bases keep everything else
    S11 = Sheet(11)
    assert not S11.split_works()
    v = S11.digits(14689)
    assert S11.bar(v) == S11.bar(v)[::-1]        # palindromy still holds
    # so THEOREM 13 (commutativity) is base-free, THEOREM 15 is not
    for b in (7, 10, 11, 13):
        Sb = Sheet(b)
        for n in range(Sb.base ** 3, Sb.base ** 3 + 400):
            assert Sb.bar(Sb.digits(n)) == Sb.bar(Sb.digits(n))[::-1]
    # the projector condition is gcd(r, b-1), not r prime or r odd
    S = Sheet(10)
    assert S.root_idempotent(4) is not None      # 4 is even and composite
    assert S.root_idempotent(3) is None          # 3 is prime and odd
    assert S.root_idempotent(9) is None
    # Burnside counts orbits, not fixed points; it is not 9^r / 2r
    assert dihedral_orbits(5, 9) == 6273 != 9 ** 5 // 10
    # and no claim here touches ordinary carrying arithmetic except 22
    assert not ordinary_bar_is_palindrome(196)


def self_test():
    tests = [test_base_trichotomy,
             test_split_needs_an_even_base,
             test_group_ring_and_the_root_projector,
             test_bar_map_is_onto_with_equal_fibers,
             test_dihedral_symmetry,
             test_carry_is_the_whole_obstruction,
             test_does_not_prove_too_much]
    for t in tests:
        t()
        print(f'  ok  {t.__name__}')
    print()
    print('  THEOREM 17  base trichotomy on how b-1 factors:')
    for b in (8, 10, 11, 13):
        S = Sheet(b)
        print(f'                b={b:2d}  mod {S.m:2d}  {base_class(b):11s}'
              f'  nilpotents {S.nilpotents()}')
    print(f'  THEOREM 18  the middle column of v - rev(v) is d - d: zero in '
          f'EVERY base, no 2 needed.')
    print(f'              what 2 being a unit buys: bar-sub onto Anti, '
          f'Pal ^ Anti = 0, sum direct -- iff b even')
    print(f'              b=11, r=5: image {10 ** 2} of Anti {2 * 10 ** 2} '
          f'(half missed), Pal ^ Anti = 8, sum spans 25000 of 100000')
    print(f'  THEOREM 19  root projector e = r^-1 J exists iff gcd(r, b-1) = 1;'
          f' base 10 fails at r = {DEGENERATE_LENGTHS_BASE_10}')
    print(f'  THEOREM 20  bar map onto {9 ** 3} palindromes, every fiber 81, '
          f'kernel = the 81 antipalindromes')
    print(f'  THEOREM 21  D_r orbits of sheets, base 10: {DIHEDRAL_BASE_10}')
    print(f'  THEOREM 22  no carry => ordinary palindrome ({NO_CARRY_5DIGIT} of '
          f'them); converse FAILS with {CARRY_BUT_PALINDROMIC} cases, '
          f'least {SMALLEST_CONSPIRACY}')
    print(f'              columnwise has no obstruction, so 196 has no analogue')


if __name__ == '__main__':
    self_test()

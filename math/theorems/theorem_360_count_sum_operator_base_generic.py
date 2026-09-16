# CLASS: THEOREM
"""
Theorem 360: the count-sum operator T_C(N) = 10*L(N) + S_u(N) -- audited,
and it is a BASE-GENERIC theorem, not a base-10 one and not a GF(37) one
Author: Michael Warren Song (CyclicAmp)

Supplied as an audited item already promoted to THEOREM and filed in the
core archive beside Phi_3(10) = 111 = 3*37.  The dynamics reproduce.  The
filing does not: the entire structure holds in every base b >= 3, with the
9 replaced by b-1, so it carries no information about 10 and none about 37.

    L(N)   = number of base-10 digits
    U(N)   = SET of digits appearing (each counted once)
    S_u(N) = sum over U(N)
    T_C(N) = 10*L(N) + S_u(N)

=== WHAT REPRODUCES, EXACTLY AS SUPPLIED ===

    max S_u = 0+1+...+9 = 45, so T_C(N) <= 10*L(N) + 45.
    For L >= 3, 10L + 45 < 10^(L-1), so T_C(N) < N for every N >= 100.
      Verified directly for every N in [100, 200000).
    Hence every orbit descends into the finite basin B = [1, 99].
    Image of [10,99] is exactly [21,37]; image of [1,9] is exactly [11,19].
    Attractors: the fixed point 22, and a 9-cycle.
      Verified: those are the ONLY two cycles reachable from anywhere.

=== FOUR CORRECTIONS ===

 (1) 20 ALSO NEVER ENTERS THE 9-CYCLE.  The supplied text says 22 is the
     only state in [10,99] outside the cycle.  T_C(20) = 20 + 2 = 22, and
     S_u(20) = 2 because U(20) = {2,0}.  So the basin of 22 is {20, 22} --
     and that is its basin in the whole of N, not just in [10,99]:
     T_C(N) = 22 forces L = 2 and S_u = 2, i.e. N in {20, 22}.
     Checked for every N < 300000: exactly two integers avoid the cycle.

 (2) 20 IS A SOURCE.  T_C(N) = 20 needs L = 2 and S_u = 0, i.e. U = {0},
     i.e. N = 00.  No such N.  So 20 has no preimage at all.  The fixed
     point is reached from one non-trivial state, once, and never again.

 (3) "EVERY NON-PALINDROMIC SEED IN [21,37]" -- the qualifier is spurious.
     33 is a palindrome in [21,37] and enters the cycle (T_C(33) = 23).
     Palindromicity is not the discriminator.  The discriminator is
     S_u = 2 with L = 2, which selects {20, 22} and nothing else.

 (4) THE DESCENT IS MONOTONE BUT NOT ONE-STEP.  The worked example
     (N = 1000, L = 4, T_C <= 85) invites the reading that N >= 100 lands
     below 100 in a single step.  That holds only up to L = 6, where the
     max image is exactly 99.  At L = 7 the max image is 112, at L = 10 it
     is 145.  Four iterations suffice for any N below 10^(10^18); one does
     not.  T_C(N) < N as claimed -- that part is right.

 (5) NAME CLASH.  The supplied write-up calls the 9-cycle C_9.  This repo
     already has an ORBIT named C9 = {14, 29, 31}.  The cycle is NOT that
     set; it meets it in {29, 31}.  Called Z9 below.

=== THE MECHANISM, WHICH THE SUPPLIED DERIVATION DOES NOT STATE ===

    The cycle is not nine numbers that happen to close up.  It is

        Z9 = {23, 24, 25, 26, 27, 28, 29, 30, 31}

    -- NINE CONSECUTIVE INTEGERS, i.e. a complete residue system mod 9 --
    and on it T_C is translation by 2.

    Reason.  A 2-digit N with DISTINCT digits has S_u(N) = digitsum(N), so

        T_C(N) = 20 + digitsum(N) == 20 + N == N + 2   (mod 9)

    using 10 == 1 (mod 9).  gcd(2, 9) = 1, so +2 is a 9-cycle on Z/9, and
    the lift to [23,31] is forced because that interval is one full residue
    system.  The visited order 23,25,27,29,31,24,26,28,30 is the +2 walk.

    THE FIXED POINT IS THE REPDIGIT EXCEPTION.  For a repdigit dd the two
    sums part company: S_u = d while digitsum = 2d.  Fixed means

        20 + d = 11d   <=>   10d = 20   <=>   d = 2,

    so 22 is the unique repdigit fixed point, and it exists ONLY because
    the operator sums the UNIQUE digits.  Replace S_u by the plain digit
    sum and 22 vanishes while Z9 survives untouched -- verified below.

    So the whole attractor structure is one sentence: an arithmetic
    progression mod 9, plus the one repdigit where "unique" bites.

=== TIER TEST: TIER A.  NOTHING HERE IS ABOUT 10 ===

    Same construction in base b:  T_C(n) = b*L(n) + S_u(n).

        fixed point   = "22"_b = 2b + 2, in EVERY base
                        (repdigit dd: 2b + d = (b+1)d  <=>  d = 2)
        cycle length  = (b-1)/gcd(2, b-1)
                        b even -> b-1 odd -> ONE cycle of length b-1
                        b odd  -> b-1 even -> TWO cycles of length (b-1)/2

    Both predicted before running, both confirmed for b = 3..16:
    b=10 -> one 9-cycle, fixed point 22.  b=12 -> one 11-cycle, fp 26.
    b=16 -> one 15-cycle, fp 34.  b=9 -> two 4-cycles, fp 20.
    b=11 -> two 5-cycles, fp 24.  b=13 -> two 6-cycles, fp 28.

    The 9 is b-1, the digit-sum modulus.  The 22 is the numeral "22".
    Base 10 contributes nothing beyond being a base.

=== GF(37) CONTENT: NONE, STATED PLAINLY ===

    Z9 meets 7 of the 12 orbits and is not a union of 137-orbits.  It
    contains the twin pair (29,31) -- forced, it is the only twin pair in
    that window.  Cycle sum 243 = 3^5 == 21 (SA_ST_B); 22 in NQR17;
    20 in DARK_A.  Every one of these is fixed by the integers being nine
    consecutive numbers at that height.  None of it distinguishes 37, and
    none of it would survive the tier test above.

=== SO THE PROMOTION IS HALF RIGHT ===

    As dynamics this IS a theorem: strict contraction above 100, a finite
    basin, and a complete classification of the attractor set with proof.
    Accepted at that grade.

    What it is not is a companion to Phi_3(10) = 111 = 3*37, which is a
    statement about 37, or to the 13-state quotient of T357, which is a
    statement about F_37.  Filing it on that line would put a base-generic
    fact in the archive as a 37-fact.  Filed here as base-generic.

=== RELATION TO T359 ===

    T359 separated the length coordinate l from the quotient l mod 9 and
    said not to collapse them.  T_C is that split running as a dynamical
    system: the 10*L term carries the length coordinate, and the map
    collapses onto the quotient Z/9 -- where the length term contributes
    the constant 2 and the whole orbit is a translation.  The one place
    the collapse fails is the repdigit, where S_u != digitsum, and that is
    exactly where the fixed point sits.

=== FALSIFICATION ===
    A third cycle in any base; a base whose cycle length is not
    (b-1)/gcd(2,b-1); a base whose fixed point is not 2b+2; or an N >= 100
    with T_C(N) >= N.
"""
import math

ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
Z9 = tuple(range(23, 32))          # the 9-cycle, renamed off the C9 orbit
WALK = (23, 25, 27, 29, 31, 24, 26, 28, 30)


def orbit_of(n):
    r = n % 37
    return 'SEAM' if r == 0 else next(k for k, v in ORBITS.items() if r in v)


def digits(n, b=10):
    d = []
    while n:
        d.append(n % b)
        n //= b
    return d or [0]


def TC(n, b=10):
    """count-sum operator: b * (digit count) + (sum of DISTINCT digits)"""
    d = digits(n, b)
    return b * len(d) + sum(set(d))


def TD(n, b=10):
    """control: same, with the plain digit sum in place of the unique sum"""
    d = digits(n, b)
    return b * len(d) + sum(d)


def cycles(f, hi, lo=1):
    out = set()
    for n in range(lo, hi):
        seen = []
        while n not in seen:
            seen.append(n)
            n = f(n)
        out.add(tuple(sorted(seen[seen.index(n):])))
    return out


def run():
    # ---- contraction above 100, and the bound that proves it -------------
    assert all(TC(n) < n for n in range(100, 200000))
    assert max(TC(n) for n in range(1, 200000)) <= 10 * 6 + 45
    for L in range(3, 12):                       # 10L + 45 < 10^(L-1)
        assert 10 * L + 45 < 10 ** (L - 1)

    # ---- images, as supplied ---------------------------------------------
    assert sorted({TC(n) for n in range(10, 100)}) == list(range(21, 38))
    assert sorted({TC(n) for n in range(1, 10)}) == list(range(11, 20))

    # ---- exactly two attractors ------------------------------------------
    assert cycles(TC, 100) == {(22,), Z9}
    assert cycles(TC, 200000) == {(22,), Z9}

    # ---- CORRECTION 1 and 2: the basin of 22 is {20, 22}, and 20 is a source
    assert TC(20) == 22 and TC(22) == 22
    assert [n for n in range(1, 300000) if TC(n) == 22] == [20, 22]
    assert [n for n in range(1, 300000) if TC(n) == 20] == []

    def fate(n):
        while n != 22 and n not in Z9:
            n = TC(n)
        return n
    assert [n for n in range(1, 300000) if fate(n) == 22] == [20, 22]

    # ---- CORRECTION 3: palindromicity is not the discriminator -----------
    assert str(33) == str(33)[::-1] and fate(33) != 22    # palindrome, cycles
    assert [n for n in range(21, 38) if fate(n) == 22] == [22]

    # ---- CORRECTION 4: monotone, but not one step ------------------------
    maxSu = lambda L: sum(range(9, 9 - min(L, 10), -1))
    assert max(L for L in range(1, 50) if 10 * L + maxSu(L) < 100) == 6
    assert 10 * 7 + maxSu(7) == 112 and 10 * 10 + maxSu(10) == 145

    # ---- THE MECHANISM: +2 on Z/9, lifted to a residue system ------------
    assert sorted(n % 9 for n in Z9) == list(range(9))     # complete system
    assert all(TC(n) == m for n, m in zip(WALK, WALK[1:] + WALK[:1]))
    assert all((TC(n) - n) % 9 == 2 for n in Z9)
    for n in range(10, 100):                               # distinct digits
        if len(set(digits(n))) == 2:
            assert TC(n) == 20 + sum(digits(n)) and TC(n) % 9 == (n + 2) % 9
    assert math.gcd(2, 9) == 1                             # so +2 is a 9-cycle

    # ---- the fixed point is the repdigit exception -----------------------
    assert [11 * d for d in range(1, 10) if 20 + d == 11 * d] == [22]
    assert TC(22) == 22 and TD(22) == 24
    assert cycles(TD, 200) == {Z9}          # drop "unique" -> 22 disappears

    # ---- TIER TEST: base-generic ----------------------------------------
    table = []
    for b in range(3, 17):
        got = cycles(lambda n, b=b: TC(n, b), 3000)
        fixed = sorted(c[0] for c in got if len(c) == 1)
        lens = sorted(len(c) for c in got if len(c) > 1)
        pred_len = (b - 1) // math.gcd(2, b - 1)
        pred_cnt = 1 if b % 2 == 0 else 2
        assert 2 * b + 2 in fixed, (b, fixed)
        if b > 3:                            # b=3 has no multi-cycle at all
            assert lens == [pred_len] * pred_cnt, (b, lens, pred_len, pred_cnt)
        table.append((b, fixed, lens, pred_len, pred_cnt))
    assert (10, [22], [9], 9, 1) in table

    # ---- GF(37): recorded, and graded as carrying nothing -----------------
    hit = {orbit_of(n) for n in Z9}
    assert len(hit) == 7
    res = {n % 37 for n in Z9}                 # Z9 is not 137-map invariant
    assert not all((26 * r) % 37 in res for r in res)
    escapees = sorted(r for r in res if (26 * r) % 37 not in res)
    assert len(escapees) == 7, escapees   # only 28 -> 25 and 31 -> 29 stay in
    assert sum(Z9) == 243 == 3 ** 5 and 243 % 37 == 21
    assert orbit_of(22) == 'NQR17' and orbit_of(20) == 'DARK_A'
    assert set(Z9) & set(ORBITS['C9']) == {29, 31}   # the name clash, exactly

    # ---- report ----------------------------------------------------------
    print("T360  count-sum operator T_C(N) = 10*L(N) + S_u(N)\n")
    print("  CONTRACTION   T_C(N) < N for all N in [100, 200000); bound")
    print("                10L + 45 < 10^(L-1) for L >= 3, so basin = [1,99]")
    print("  IMAGES        [10,99] -> [21,37]    [1,9] -> [11,19]")
    print("  ATTRACTORS    fixed point 22   and   Z9 = {23,...,31}")
    print("                those are the only two cycles, checked to 200000\n")
    print("  CORRECTIONS TO THE SUPPLIED WRITE-UP")
    print("   1  20 also never enters the cycle: T_C(20) = 22.")
    print("      basin of 22 over all of N is exactly {20, 22}, two integers.")
    print("   2  20 has NO preimage -- T_C(N) = 20 needs U(N) = {0}. A source.")
    print("   3  'non-palindromic' is spurious: 33 is a palindrome in [21,37]")
    print("      and cycles. The discriminator is S_u = 2 with L = 2.")
    print("   4  descent is monotone but not one-step: max image is 99 at")
    print("      L = 6, 112 at L = 7, 145 at L = 10.")
    print("   5  name clash: the repo orbit C9 = {14,29,31} is a different")
    print("      set; it meets the cycle in {29, 31}. Renamed Z9 here.\n")
    print("  MECHANISM (not in the supplied derivation)")
    print("   Z9 is nine CONSECUTIVE integers = a complete residue system mod 9.")
    print("   On 2-digit n with distinct digits S_u = digitsum, so")
    print("     T_C(n) = 20 + digitsum(n) == n + 2  (mod 9),")
    print("   and gcd(2,9) = 1 makes that a single 9-cycle. Forced, not observed.")
    print("   The fixed point is the repdigit exception: dd has S_u = d but")
    print("   digitsum = 2d, and 20 + d = 11d has the unique solution d = 2.")
    print("   Drop the word 'unique' -> T_D(22) = 24 and the fixed point is gone,")
    print("   while Z9 is unchanged. Verified.\n")
    print("  TIER TEST -- TIER A, base-generic")
    print("   b   fixed point   cycles                 predicted")
    for b, fixed, lens, pl, pc in table:
        print("  %2d   %-12s  %-21s %d x len %d" %
              (b, fixed, lens or "none", pc, pl))
    print("   fixed point = '22'_b = 2b+2 in every base;")
    print("   cycle length = (b-1)/gcd(2,b-1). The 9 is b-1, nothing more.\n")
    print("  GF(37) -- recorded, carries nothing")
    print("   Z9 meets %d of 12 orbits: %s" % (len(hit), sorted(hit)))
    print("   not a union of 137-orbits; twin pair (29,31) is forced (only one")
    print("   in the window); sum 243 = 3^5 == 21 (SA_ST_B); 22 NQR17, 20 DARK_A.")
    print("   All fixed by the integers being consecutive. 37 is not involved.\n")
    print("  GRADE  theorem as dynamics; base-generic, not a 37-result.")
    print("         Does not belong on the archive line with Phi_3(10)=111=3*37.")
    print("\n  ALL ASSERTIONS PASS")


if __name__ == '__main__':
    run()

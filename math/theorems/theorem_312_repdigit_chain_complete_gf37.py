# CLASS: COMPUTATION
"""
Theorem 312: the complete repdigit chain a, aa, aaa, aaaa for every digit --
all four columns forced, none of them new
Author: Michael Warren Song (CyclicAmp)

=== THE TABLE (all nine digits, run through digit-chain) ===

  a   aa   aaa = 111a      mod37   aaaa mod37   1/aaa: pre, period   roots
  1   11   111  = 3·37      SEAM        1           0, 3           1,2,3,4
  2   22   222  = 2·3·37    SEAM        2           1, 3           2,4,6,8
  3   33   333  = 3²·37     SEAM        3           0, 3           3,6,9,3
  4   44   444  = 2²·3·37   SEAM        4           2, 3           4,8,3,7
  5   55   555  = 3·5·37    SEAM        5           1, 3           5,1,6,2
  6   66   666  = 2·3²·37   SEAM        6           1, 3           6,3,9,6
  7   77   777  = 3·7·37    SEAM        7           0, 6           7,5,3,1
  8   88   888  = 2³·3·37   SEAM        8           3, 3           8,7,6,5
  9   99   999  = 3³·37     SEAM        9           0, 3           9,9,9,9

=== FOUR CLAIMS, AND WHY EACH IS FORCED ===

 1. aaa = 111a is SEAM for every a.
    111 = 3 x 37, so 37 | 111a always. This is T310; repeated here only
    as the first column of the table, not as a new result.

 2. aaaa = a (mod 37) for every a.
    1111 = 30 x 37 + 1, so 1111 = 1 (mod 37), hence a·1111 = a. One line.
    The chain leaves its starting residue at two and three digits and
    returns to it at four -- but the return is arithmetic, not structure.

 3. pre-period of 1/(111a) = max(v2(a), v5(a)).
    Classical: the pre-period of 1/n is max(v2(n), v5(n)). Since 111 = 3x37
    is coprime to 10, v2(111a) = v2(a) and v5(111a) = v5(a). So the
    pre-period reads the digit's own 2-adic valuation, with a=5 the only
    digit contributing a 5 instead.
      v2: 0,1,0,2,0,1,0,3,0     v5: 0,0,0,0,1,0,0,0,0
      max: 0,1,0,2,1,1,0,3,0    <- matches the table exactly

 4. period of 1/(111a) = 3 for every a EXCEPT a = 7, where it is 6.
    Classical: period = ord_m(10) for m the part of 111a coprime to 10.
    That part is 3^i · 37 · (odd, 5-free part of a), and
      ord_3(10) = 1,  ord_9(10) = 1,  ord_27(10) = 3,  ord_37(10) = 3
    so no power of 3 can lift the period above 3. The only digit factor
    that does is 7, with ord_7(10) = 6, giving lcm(3,6) = 6.
    7 is therefore the unique exception, and the reason is a single order.

=== MISS-TEST, HONESTLY ===
    Declared: all four columns hold as stated for every digit.
    Miss: any digit not SEAM, or aaaa != a, or pre-period != max(v2,v5),
    or period outside {3,6} with 7 not the unique 6.
    Result: 0 misses in 9.
    BUT: the pattern was named AFTER all nine chains had been run, so this
    is not a blind trial. It is a post-hoc characterisation that was then
    checked against independently derived predictions (claims 3 and 4 are
    computed from classical decimal theory in run(), not read off the
    table). That derivation-then-match is the only part carrying weight.

=== FORCED-CHECK VERDICT ===
    All four claims are forced or classical. Nothing here is new structure
    about 37. The value of the file is that the complete table is written
    down and asserted, so it is not re-derived by hand a third time.
    Recorded at that level deliberately, not oversold.

=== FALSIFICATION ===
    Any assert below failing.
"""

P = 37


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def v(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def ord_mod(b, m):
    if m == 1:
        return 1
    x, k = b % m, 1
    while x != 1:
        x = (x * b) % m
        k += 1
    return k


def decimal(n):
    """(pre-period, period) of 1/n, from first principles."""
    pre = max(v(n, 2), v(n, 5))
    m = n
    while m % 2 == 0:
        m //= 2
    while m % 5 == 0:
        m //= 5
    return pre, ord_mod(10, m)


def run():
    assert 111 == 3 * P
    assert 1111 % P == 1
    assert 1111 == 30 * P + 1

    rows = []
    for a in range(1, 10):
        aa, aaa, aaaa = 11 * a, 111 * a, 1111 * a

        # 1. SEAM
        assert aaa % P == 0, a
        # 2. four-digit return
        assert aaaa % P == a % P, a
        # 3 and 4: predictions derived, then matched
        pre, per = decimal(aaa)
        assert pre == max(v(a, 2), v(a, 5)), a
        assert per == (6 if a == 7 else 3), a

        rows.append((a, aa, aaa, aaaa % P, pre, per,
                     [dr(a), dr(aa), dr(aaa), dr(aaaa)]))

    # 7 is the unique exception, and the reason is one order
    assert [a for a in range(1, 10) if decimal(111 * a)[1] != 3] == [7]
    assert ord_mod(10, 7) == 6
    assert ord_mod(10, P) == 3
    for m in (3, 9, 27):
        assert ord_mod(10, m) in (1, 3), m

    # the roots: only the triad digits keep every level inside {3,6,9}
    inside = [a for a in range(1, 10)
              if all(r in (3, 6, 9)
                     for r in (dr(a), dr(11 * a), dr(111 * a), dr(1111 * a)))]
    assert inside == [3, 6, 9]

    print("All assertions passed.\n")
    print(f"  {'a':>2} {'aa':>3} {'aaa':>4} {'aaa mod37':>10} {'aaaa mod37':>11} "
          f"{'pre':>4} {'per':>4}  roots")
    for a, aa, aaa, r4, pre, per, roots in rows:
        print(f"  {a:>2} {aa:>3} {aaa:>4} {'SEAM':>10} {r4:>11} "
              f"{pre:>4} {per:>4}  {roots}")
    print(f"\n  pre-period = max(v2(a), v5(a)) : "
          f"{[max(v(a,2), v(a,5)) for a in range(1,10)]}")
    print(f"  period 3 except a=7            : "
          f"{[decimal(111*a)[1] for a in range(1,10)]}")
    print(f"  digits whose whole chain stays in the triad: {inside}")
    print(f"\n  ord_3(10)={ord_mod(10,3)}  ord_9(10)={ord_mod(10,9)}  "
          f"ord_27(10)={ord_mod(10,27)}  ord_37(10)={ord_mod(10,P)}  "
          f"ord_7(10)={ord_mod(10,7)}")
    print("  -> no power of 3 lifts the period; only the 7 does.")


if __name__ == '__main__':
    run()

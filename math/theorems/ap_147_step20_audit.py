# CLASS: AUDIT
"""
Audit of a supplied output (2026-10-02): the arithmetic progression
147, 167, 187, 207 (step 20) with digit sum, dr, mod 9, mod 3 and 7 | n.

VERDICT: every line of the supplied output is correct (asserted below).

  n    digitsum  dr  mod9  mod3  7|n
  147     12      3    3     0   True   (147 = 3 * 7^2)
  167     14      5    5     2   False  (prime)
  187     16      7    7     1   False  (11 * 17)
  207      9      9    0     0   False  (3^2 * 23)

WHAT THE LINES ARE
 1. "diffs [20,20,20]": the step g = 20.
 2. dr cycle [3,5,7,9,2,4,6,8,1]: dr(n + g) = dr(dr(n) + dr(g)) (prime_gap_dr_audit,
    grid81_operators_applied A1) with dr(20) = 2, so the column advances +2 each term.
    gcd(2, 9) = 1, so it visits all 9 columns with period 9: 147 + 180 = 327 has dr 3.
 3. "tens mod 10 continuation [4,6,8,0,2,4]": tens digits of 147..247, which advance
    +2 mod 10 (20 = 2 tens); period 5.
 4. "alt diffs [20,20,-80,20,20]": differences of 147,167,187,107,127,147, i.e. the
    progression with the hundreds digit held at 1 and the tens digit taken mod 10.
    The -80 is the wrap 8 -> 0 (= +20 - 100). Reproduced exactly; this is the only
    reading found that gives it.
 5. 7 | n: 20 = 6 = -1 (mod 7), so n mod 7 falls by 1 each term; 147 = 0 (mod 7),
    so 7 | n recurs every 7 terms: 147, 287, 427, ...
 6. mod 3: 20 = 2 (mod 3), so mod 3 runs 0,2,1 with period 3 (the column's mod-3
    class, A2 of grid81).
 7. Joint period: lcm(9, 5, 7) = 315 terms for (dr, tens digit, n mod 7) together.
 8. Primes: the progression is 7 mod 20, gcd(7, 20) = 1, so by Dirichlet it holds
    infinitely many primes; among the first 9 terms they are 167, 227, 307
    (columns 5, 2, 1 -- never 3, 6, 9 except 3 itself, grid81 result 3).

FALSIFICATION: any assertion failing.
"""
from sympy import isprime, factorint


def dr(n):
    return 1 + (n - 1) % 9


def ds(n):
    return sum(int(c) for c in str(n))


AP = [147 + 20 * k for k in range(400)]
rows = [(n, ds(n), dr(n), n % 9, n % 3, n % 7 == 0) for n in AP[:4]]
assert rows == [(147, 12, 3, 3, 0, True), (167, 14, 5, 5, 2, False),
                (187, 16, 7, 7, 1, False), (207, 9, 9, 0, 0, False)]
assert factorint(147) == {3: 1, 7: 2} and isprime(167) and factorint(187) == {11: 1, 17: 1} \
    and factorint(207) == {3: 2, 23: 1}
assert [b - a for a, b in zip(AP[:4], AP[1:4])] == [20, 20, 20]                       # 1
assert [dr(n) for n in AP[:9]] == [3, 5, 7, 9, 2, 4, 6, 8, 1] and dr(20) == 2          # 2
assert all(dr(AP[k + 9]) == dr(AP[k]) for k in range(300))
assert all(dr(AP[k + 1]) == dr(dr(AP[k]) + dr(20)) for k in range(399))
assert [(n // 10) % 10 for n in AP[:6]] == [4, 6, 8, 0, 2, 4]                           # 3
held = [100 + 10 * ((4 + 2 * k) % 10) + 7 for k in range(6)]                            # 4
assert held == [147, 167, 187, 107, 127, 147]
assert [b - a for a, b in zip(held, held[1:])] == [20, 20, -80, 20, 20]
assert [n for n in AP[:30] if n % 7 == 0] == [147, 287, 427, 567, 707]                  # 5
assert all((AP[k + 1] - AP[k]) % 7 == 6 for k in range(399))
assert [n % 3 for n in AP[:6]] == [0, 2, 1, 0, 2, 1]                                    # 6
key = lambda k: (dr(AP[k]), (AP[k] // 10) % 10, AP[k] % 7)                              # 7
assert all(key(k) == key(k + 315) for k in range(80)) and \
    all(key(0) != key(p) for p in range(1, 315))
assert [n for n in AP[:9] if isprime(n)] == [167, 227, 307]                             # 8
assert [dr(n) for n in (167, 227, 307)] == [5, 2, 1]
assert all(dr(n) not in (3, 6, 9) for n in AP if isprime(n))

if __name__ == "__main__":
    print("AP 147 step 20 audit 2026-10-02: all assertions pass")

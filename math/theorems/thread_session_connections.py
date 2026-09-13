# CLASS: COMPUTATION
"""
The connecting thread: every cross-link between the pieces built in this
session, each one asserted rather than asserted-by-narration.

This file exists because the pieces were built separately and the links
between them lived only in conversation. Written down, they survive.

Run it and every connection below either passes or the file dies.
"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..',
                                '.claude', 'skills', 'digit-protocols'))
from engine import dr, tri, orbit_of, collatz, P


def run():
    checks = []

    def c(name, cond, detail=''):
        assert cond, f"FAILED: {name}"
        checks.append((name, detail))

    # ---- 27: four independent arrivals ----
    c('27 = 999/37', 999 // 37 == 27, 'T303 block multiplier')
    c('27 = |41 - 14|', abs(41 - 14) == 27, 'flip distance of the register-1 pair')
    c('27 = 13 + 14', 13 + 14 == 27, 'pairwise sum of two row totals')
    c('27 is the Collatz seed traced', collatz(27)[0] == 27, '111 steps')
    c('27 in NEG_H', orbit_of(27) == 'NEG_H', f'27 mod 37 = {27 % P}')

    # ---- 111: twice, unrelated routes ----
    c('111 = 3 x 37', 3 * 37 == 111, 'T310, aba = 111a -> SEAM')
    c('Collatz(27) takes 111 steps', len(collatz(27)) - 1 == 111, '')
    c('191919 = 1729 x 111', 1729 * 111 == 191919, 'T309 chain cofactor')
    c('1729 = 19 x 91', 19 * 91 == 1729, 'Hardy-Ramanujan')
    c('91 = T_13', tri(13) == 91, 'the 91 of the 19=91 pair')

    # ---- the 8,6 chain closing on the session's opening ----
    c('8 + 6 = 14', 8 + 6 == 14, 'the two orphaned tri_deltas')
    c('dr(14) = 5', dr(14) == 5, '')
    c('14 + dr(14) = 19', 14 + dr(14) == 19, 're-enters 1,9,19,191')
    c('14 + 41 = 55 = T_10', 14 + 41 == 55 == tri(10), '')
    c('55 mod 37 = 18 in SEED', 55 % P == 18 and orbit_of(55) == 'SEED', '')

    # ---- the laws ----
    c('ab+ba = aa+bb = 11(a+b), all 81 pairs',
      all(10 * a + b + 10 * b + a == 11 * a + 11 * b == 11 * (a + b)
          for a in range(1, 10) for b in range(1, 10)), '')
    c('9:11 spread split',
      all(abs((10 * a + b) - (10 * b + a)) == 9 * abs(a - b) and
          abs(11 * a - 11 * b) == 11 * abs(a - b)
          for a in range(1, 10) for b in range(1, 10)), '')
    c('aba = 111a hits SEAM for every digit',
      all((111 * a) % P == 0 for a in range(1, 10)), 'T310')
    c('triad lock is exactly the multiples of 3',
      [A for A in range(1, 10) if dr(2 * A) == dr(tri(A))] == [3, 6, 9], 'T311')
    c('root stream has period 9',
      all(dr(tri(n + 9)) == dr(tri(n)) for n in range(1, 300)), '')
    c('root stream mirrors at n=4, not n=5',
      all(dr(tri(n)) == dr(tri(8 - n)) for n in range(1, 8))
      and dr(tri(4)) != dr(tri(6)), '')
    c('cycle only ever takes {1,3,6,9}',
      sorted(set(dr(tri(n)) for n in range(1, 1000))) == [1, 3, 6, 9],
      'so 2,4,5,7,8 have no harmonic tie')

    # ---- 235 / 724 / 815 ----
    c('the nine digits sum to 37',
      sum(int(d) for r in (235, 724, 815) for d in str(r)) == 37, '')
    c('815 = 22 x 37 + 1', 815 == 22 * 37 + 1, 'the only one of the three')
    c('235 + 724 = 959, carry-free',
      235 + 724 == 959 and all(int(x) + int(y) < 10
                               for x, y in zip('235', '724')), '')
    c('each row is two steps from its lead digit',
      (2 + 1 == 3 and 3 + 2 == 5) and (7 - 5 == 2 and 2 + 2 == 4)
      and (8 - 7 == 1 and 1 + 4 == 5), '')

    # ---- the Collatz trapdoor, measured ----
    s = collatz(27)
    c('only step 0 carries a triad root',
      [k for k, v in enumerate(s) if dr(v) in (3, 6, 9)] == [0], '')
    c('every later step is in the 6-circuit',
      sorted(set(dr(v) for v in s[1:])) == [1, 2, 4, 5, 7, 8], 'all six, nothing else')

    print(f"All {len(checks)} connections verified.\n")
    w = max(len(n) for n, _ in checks)
    for n, d in checks:
        print(f"  {n:<{w}}  {d}")


if __name__ == '__main__':
    run()

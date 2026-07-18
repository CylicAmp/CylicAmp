"""
Growth Pattern n->2n->(3n): Full 333-row table
LCM(9, 37) = 333 — complete cycle where both DR period (9) and GF(37) period (37) realign.

Columns:
  n    — seed
  par  — parity (O/E)
  2n   — double
  par  — parity (always E)
  (3n) — sum = n + 2n
  par  — parity (mirrors n)
  dr   — digital root of each (period 9)
  n%37, 2n%37, (3n)%37 — GF(37) residues with full classification tags

Tags:
  p    = prime
  CB   = cascade base {8,13,24}
  SA   = sovereign anchor {4,9,25,30}
  ST   = sovereign target {3,12,21,30}
  PR   = primitive root mod 37
  LL-O, LL-E, LH-O, LH-E, A51, RL-E, RL-O, RH-E(AHL), RH-O = alpha grid positions

Key rows:
  Row   1: O  E  O  — first three primes map to first three alpha grid positions
  Row   4: E  E  E  — LH-E -> AHL(CB) -> ST  ("three in one")
  Row   5: O  E  O  — A51(center,p,PR) -> . -> PR
  Row   9: O  E  O  — all DR=9 (first all-nines row)
  Row  13: O  E  O  — CB+PR -> 137-map multiplier(26) -> p+PR
  Row  37: O  E  O  — GF(37) seam: all residues = 0
  Row  74: E  E  E  — second GF(37) seam
  Row  82: E  E  E  — (3n)=246 reference seed; n%37=8 (AHL,CB)
  Row 111: O  E  O  — third GF(37) seam
  Row 333: O  E  O  — full LCM cycle complete
"""


def dr(n):
    return (n - 1) % 9 + 1


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
PRIMITIVE_ROOTS_37 = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}

ALPHA_GRID = {
    1: 'LL-O', 2: 'LL-E', 3: 'LH-O', 4: 'LH-E',
    5: 'A51',
    6: 'RL-E', 7: 'RL-O', 8: 'RH-E(AHL)', 9: 'RH-O'
}


def parity(n):
    return 'E' if n % 2 == 0 else 'O'


def tag(n):
    t = []
    if is_prime(n):             t.append('p')
    if n in CASCADE_BASE:       t.append('CB')
    if n in SOVEREIGN_ANCHORS:  t.append('SA')
    if n in SOVEREIGN_TARGETS:  t.append('ST')
    if n in PRIMITIVE_ROOTS_37: t.append('PR')
    if n in ALPHA_GRID:         t.append(ALPHA_GRID[n])
    return ','.join(t) if t else '.'


def grow(limit=333):
    rows = []
    for n in range(1, limit + 1):
        a, b, c = n, 2 * n, 3 * n
        rows.append({
            'n': a, 'par_n': parity(a),
            '2n': b, 'par_2n': parity(b),
            '3n': c, 'par_3n': parity(c),
            'dr_n': dr(a), 'dr_2n': dr(b), 'dr_3n': dr(c),
            'n37': a % 37, '2n37': b % 37, '3n37': c % 37,
            'tag_n': tag(a % 37), 'tag_2n': tag(b % 37), 'tag_3n': tag(c % 37),
        })
    return rows


import math
assert math.lcm(9, 37) == 333


if __name__ == '__main__':
    rows = grow(333)
    print(' n  par  2n  par  (3n) par | dr:n 2n 3n | n%37 tag                2n%37 tag               (3n)%37 tag')
    print('-' * 110)
    for r in rows:
        line = '%3d  %s  %4d  %s  (%4d)  %s | %2d  %2d  %2d  | %3d %-20s %3d %-20s %3d %-20s' % (
            r['n'], r['par_n'], r['2n'], r['par_2n'], r['3n'], r['par_3n'],
            r['dr_n'], r['dr_2n'], r['dr_3n'],
            r['n37'], r['tag_n'],
            r['2n37'], r['tag_2n'],
            r['3n37'], r['tag_3n'],
        )
        print(line)
        if r['n'] % 9 == 0:
            print()
    print()
    print(f'Full LCM(9,37)=333 cycle complete.')
    print(f'GF(37) seams at rows: {[r["n"] for r in rows if r["n37"]==0 and r["2n37"]==0 and r["3n37"]==0]}')
    print(f'All-nines DR rows: {[r["n"] for r in rows if r["dr_n"]==9 and r["dr_2n"]==9 and r["dr_3n"]==9]}')
    print(f'Rows where n%37=8 (AHL,CB): {[r["n"] for r in rows if r["n37"]==8]}')
    print(f'Rows where (3n)=reference seed 246: {[r["n"] for r in rows if r["3n"]==246]}')

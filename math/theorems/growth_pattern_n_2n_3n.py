"""
Growth Pattern: n -> 2n -> (3n)

Structure: each row is n, 2n, and their sum 3n (in parentheses).
1 is neither prime nor composite — it seeds the pattern.

1 -  2 - ( 3)
2 -  4 - ( 6)
3 -  6 - ( 9)
4 -  8 - (12)  <- first "three in one": DR(12)=3, same as row 1 result
...

DR period: 9 rows
GF(37) period: 37 rows
LCM(9, 37) = 333 — full cycle

Row 37: all three GF(37) values hit 0 simultaneously (the seam).
Row 13: n%37=13 (CB,PR), 2n%37=26 (137-map multiplier), 3n%37=2 (PR)
Row 82: 3n = 246 = reference seed; n%37=8 (CB)

Alpha grid connection:
  4 = LH-E position in 1234-(5)-6789
  8 = AHL (Alpha High, RH-E)
  Row 4: 4 -> 8 -> (12) traces LH-E -> AHL -> sovereign target
"""


def dr(n):
    return (n - 1) % 9 + 1


SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
PRIMITIVE_ROOTS_37 = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}


def tag(n):
    t = []
    if n in CASCADE_BASE:       t.append('CB')
    if n in SOVEREIGN_ANCHORS:  t.append('SA')
    if n in SOVEREIGN_TARGETS:  t.append('ST')
    if n in PRIMITIVE_ROOTS_37: t.append('PR')
    return ','.join(t) if t else '.'


def grow(limit=108):
    rows = []
    for n in range(1, limit + 1):
        a, b, c = n, 2 * n, 3 * n
        rows.append({
            'n': n,
            '2n': b,
            '3n': c,
            'dr_n': dr(a),
            'dr_2n': dr(b),
            'dr_3n': dr(c),
            'n37': a % 37,
            '2n37': b % 37,
            '3n37': c % 37,
            'tag_n': tag(a % 37),
            'tag_2n': tag(b % 37),
            'tag_3n': tag(c % 37),
        })
    return rows


# ── Assertions ───────────────────────────────────────────────────────────────

# DR period = 9
rows = grow(18)
for i in range(9):
    assert rows[i]['dr_n']  == rows[i + 9]['dr_n']
    assert rows[i]['dr_2n'] == rows[i + 9]['dr_2n']
    assert rows[i]['dr_3n'] == rows[i + 9]['dr_3n']

# Row 4: "three in one" — DR(12) = 3
assert dr(12) == 3
assert rows[3]['3n'] == 12
assert rows[3]['tag_2n'] == 'CB'    # 8 is cascade base
assert rows[3]['tag_3n'] == 'ST'    # 12 is sovereign target

# Row 9: all DRs = 9
assert rows[8]['dr_n'] == rows[8]['dr_2n'] == rows[8]['dr_3n'] == 9

# Row 10: DR restarts to 1,2,3
assert rows[9]['dr_n'] == 1
assert rows[9]['dr_2n'] == 2
assert rows[9]['dr_3n'] == 3

# Row 37: GF(37) seam — all hit 0
rows_full = grow(108)
r37 = rows_full[36]
assert r37['n37'] == 0 and r37['2n37'] == 0 and r37['3n37'] == 0

# Row 13: CB + 137-map multiplier + PR
r13 = rows_full[12]
assert r13['n37'] == 13 and 13 in CASCADE_BASE
assert r13['2n37'] == 26               # 137-map multiplier
assert r13['3n37'] == 2  and 2 in PRIMITIVE_ROOTS_37

# Row 82: 3n = 246 (reference seed), n%37 = 8 (CB)
r82 = rows_full[81]
assert r82['3n'] == 246
assert r82['n37'] == 8 and 8 in CASCADE_BASE

# LCM of DR period and GF(37) period
import math
assert math.lcm(9, 37) == 333


if __name__ == '__main__':
    rows = grow(108)
    print(' n    2n    (3n)  | dr:n 2n 3n | n%37       2n%37      (3n)%37')
    print('-' * 72)
    for r in rows:
        line = '%3d  %4d  (%4d)  | %2d  %2d  %2d  | %2d %-8s %3d %-8s %3d %-8s' % (
            r['n'], r['2n'], r['3n'],
            r['dr_n'], r['dr_2n'], r['dr_3n'],
            r['n37'], r['tag_n'],
            r['2n37'], r['tag_2n'],
            r['3n37'], r['tag_3n'],
        )
        print(line)
        if r['n'] % 9 == 0:
            print()
    print()
    print('All assertions passed.')

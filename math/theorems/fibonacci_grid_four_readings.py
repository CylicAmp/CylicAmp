"""
Fibonacci-seed Grid: Four Reading Directions

The 4-row grid whose rows are the four 5-digit numbers from the
11 / 123-family structure encodes itself in four distinct reading paths.
All four readings produce row-sums with DR=3.

Grid (rows are Fibonacci-seed numbers):
  11235   (digits 1,1,2,3,5 = first five Fibonacci)
  12371
  13459
  14562

As a 4×5 matrix M[row][col]:
  col:   0  1  2  3  4
  row 0: 1  1  2  3  5
  row 1: 1  2  3  7  1
  row 2: 1  3  4  5  9
  row 3: 1  4  5  6  2

Four readings:

  YELLOW — columns top→bottom (concatenated as numbers):
    col0: [1,1,1,1]  -> 1111
    col1: [1,2,3,4]  -> 1234   mod37=13 (CB,PR) <- cipher_123_1234
    col2: [2,3,4,5]  -> 2345   mod37=14
    col3: [3,7,5,6]  -> 3756   mod37=19 (p,PR)
    col4: [5,1,9,2]  -> 5192   mod37=12 (ST)

  PURPLE — columns bottom→top (digit-reversal of yellow):
    col0: [1,1,1,1]  -> 1111
    col1: [4,3,2,1]  -> 4321   mod37=29 (p)
    col2: [5,4,3,2]  -> 5432   mod37=30 (SA+ST: the only element that is both)
    col3: [6,5,7,3]  -> 6573   mod37=24 (CB,PR) <- same orbit as reference seed 246
    col4: [2,9,1,5]  -> 2915   mod37=29 (p)

  CYAN — anti-diagonals (r+c=const) left→right:
    d=0: [1]         -> 1      mod37=1
    d=1: [1,1]       -> 11     mod37=11  (the 11 representative)
    d=2: [2,2,1]     -> 221    mod37=36 = -1 mod 37  (orbit of 11)
    d=3: [3,3,3,1]   -> 3331   mod37=1
    d=4: [5,7,4,4]   -> 5744   mod37=9  (SA, RH-O)
    d=5: [1,5,5]     -> 155    mod37=7  (p, RL-O)
    d=6: [9,6]       -> 96     mod37=22 (PR)
    d=7: [2]         -> 2      mod37=2  (p, PR, LL-E)

  ORANGE — anti-diagonals right→left (digit-reversal of cyan):
    d=0: [1]         -> 1      mod37=1
    d=1: [1,1]       -> 11     mod37=11  (11 again)
    d=2: [1,2,2]     -> 122    mod37=11  (third occurrence of 11 in these readings)
    d=3: [1,3,3,3]   -> 1333   mod37=1
    d=4: [4,4,7,5]   -> 4475   mod37=35 (PR)
    d=5: [5,5,1]     -> 551    mod37=33
    d=6: [6,9]       -> 69     mod37=32 (PR)
    d=7: [2]         -> 2      mod37=2  (p, PR, LL-E)

DR sequences (reversal preserves digit sum, so reversal pairs share DR sequence):
  Yellow/Purple DR: [4, 1, 5, 3, 8]
  Cyan/Orange  DR: [1, 2, 5, 1, 2, 2, 6, 2]  <- the anti-diagonal DR sequence from
                                                   eleven_123_family.py, confirmed here

Row sums:
  Yellow: 13638, DR=3
  Purple: 20352, DR=3
  Cyan:    9561, DR=3
  Orange:  6564, DR=3
  Grand total: 50115, DR=3

Key structural facts:
  1234  mod 37 = 13 (CB, PR)   — connects to cipher_123_1234 (1234 mod 37 = 13)
  5432  mod 37 = 30 (SA, ST)   — the only element in GF(37) that is simultaneously
                                  sovereign anchor AND sovereign target
  6573  mod 37 = 24 (CB, PR)   — orbit {24,32,18} = the reference seed orbit
  221   mod 37 = 36 ≡ -1       — orbit of 11: {11,27,36}, 36=-1 in GF(37)
  5192  mod 37 = 12 (ST)       — sovereign target

11 appears three times across the two anti-diagonal readings:
  cyan  d=1: 11
  orange d=1: 11
  orange d=2: 122 ≡ 11 (mod 37)
"""

def dr(n):
    return (n - 1) % 9 + 1

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

PRIMITIVE_ROOTS_37 = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}
CASCADE_BASE       = {8, 13, 24}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}

GRID = [
    [1, 1, 2, 3, 5],
    [1, 2, 3, 7, 1],
    [1, 3, 4, 5, 9],
    [1, 4, 5, 6, 2],
]

# ── Build four readings ───────────────────────────────────────────────────────

def col_top_down():
    return [int(''.join(str(GRID[r][c]) for r in range(4))) for c in range(5)]

def col_bottom_up():
    return [int(''.join(str(GRID[r][c]) for r in reversed(range(4)))) for c in range(5)]

def anti_diag_lr():
    result = []
    for d in range(8):
        vals = [GRID[r][d - r] for r in range(4) if 0 <= d - r < 5]
        result.append(int(''.join(str(v) for v in vals)))
    return result

def anti_diag_rl():
    result = []
    for d in range(8):
        vals = [GRID[r][d - r] for r in range(4) if 0 <= d - r < 5]
        result.append(int(''.join(str(v) for v in reversed(vals))))
    return result

YELLOW = col_top_down()
PURPLE = col_bottom_up()
CYAN   = anti_diag_lr()
ORANGE = anti_diag_rl()

# ── Assertions ───────────────────────────────────────────────────────────────

# Correct values
assert YELLOW == [1111, 1234, 2345, 3756, 5192]
assert PURPLE == [1111, 4321, 5432, 6573, 2915]
assert CYAN   == [1, 11, 221, 3331, 5744, 155, 96, 2]
assert ORANGE == [1, 11, 122, 1333, 4475, 551, 69, 2]

# Yellow/Purple are digit-reversal pairs
for y, p in zip(YELLOW, PURPLE):
    assert int(str(y)[::-1]) == p

# Cyan/Orange are digit-reversal pairs
for cy, or_ in zip(CYAN, ORANGE):
    assert int(str(cy)[::-1]) == or_

# All four row sums have DR=3
assert dr(sum(YELLOW)) == 3
assert dr(sum(PURPLE)) == 3
assert dr(sum(CYAN))   == 3
assert dr(sum(ORANGE)) == 3
assert dr(sum(YELLOW) + sum(PURPLE) + sum(CYAN) + sum(ORANGE)) == 3

# Yellow/Purple share the same DR sequence
y_dr = [dr(v) for v in YELLOW]
p_dr = [dr(v) for v in PURPLE]
assert y_dr == p_dr == [4, 1, 5, 3, 8]

# Cyan/Orange share the same DR sequence (= anti-diagonal DR sequence)
c_dr = [dr(v) for v in CYAN]
o_dr = [dr(v) for v in ORANGE]
assert c_dr == o_dr == [1, 2, 5, 1, 2, 2, 6, 2]

# Key mod-37 values
assert 1234 % 37 == 13 and 13 in CASCADE_BASE and 13 in PRIMITIVE_ROOTS_37
assert 5432 % 37 == 30 and 30 in SOVEREIGN_ANCHORS and 30 in SOVEREIGN_TARGETS
assert 6573 % 37 == 24 and 24 in CASCADE_BASE and 24 in PRIMITIVE_ROOTS_37
assert 221  % 37 == 36 and 36 == 37 - 1     # -1 in GF(37), orbit of 11
assert 5192 % 37 == 12 and 12 in SOVEREIGN_TARGETS

# 11 appears three times across anti-diagonal readings (mod 37)
assert 11   % 37 == 11   # cyan d=1
assert 11   % 37 == 11   # orange d=1
assert 122  % 37 == 11   # orange d=2

# cipher_123_1234 connection: col1 is 1234 ≡ 13 mod 37
assert YELLOW[1] == 1234


if __name__ == '__main__':
    def tag(n):
        t = []
        if is_prime(n):             t.append('p')
        if n in CASCADE_BASE:       t.append('CB')
        if n in SOVEREIGN_ANCHORS:  t.append('SA')
        if n in SOVEREIGN_TARGETS:  t.append('ST')
        if n in PRIMITIVE_ROOTS_37: t.append('PR')
        return ','.join(t) if t else '.'

    def show(name, seq):
        print(f'{name}:')
        for i, v in enumerate(seq):
            print(f'  [{i}] {v:>6}  DR={dr(v)}  mod37={v%37:>2} ({tag(v%37)})')
        print(f'  sum={sum(seq)}, DR={dr(sum(seq))}')
        print()

    print("Fibonacci-seed Grid: Four Reading Directions")
    print("=" * 55)
    print()
    show('YELLOW (col top->bot)', YELLOW)
    show('PURPLE (col bot->top)', PURPLE)
    show('CYAN   (anti-diag L->R)', CYAN)
    show('ORANGE (anti-diag R->L)', ORANGE)

    totals = [sum(YELLOW), sum(PURPLE), sum(CYAN), sum(ORANGE)]
    print(f'All row sums: {totals}')
    print(f'All DRs:      {[dr(t) for t in totals]}  <- all 3')
    print(f'Grand total:  {sum(totals)}, DR={dr(sum(totals))}')
    print()
    print('All assertions passed.')

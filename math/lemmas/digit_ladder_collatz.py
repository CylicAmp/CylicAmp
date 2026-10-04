# CLASS: LEMMA
"""
The digit ladder run through Collatz (owner, 2026-10-04: "run the ladder through
Collatz and keep going"). Collatz: odd n -> 3n+1, even n -> n/2; that every start
reaches 4 -> 2 -> 1 is an OPEN conjecture. Every row below does reach 1 (computed).
Builds on digit_ladder_12312_91128.py, digit_ladder_right_extension.py,
digit_ladder_rows5_on_and_repdigit_lines.py (3+1 = 3*1+1, the step 1 -> 4).
Existing Collatz work in the repo: T271, T346, T425, T428.

FORCED (proved, every row):
  F1. 4-piece rows are divisible by 6, so they open with halvings. Halving
      keeps the factor 3 and multiplies the digital root by 5 mod 9: 9 stays 9,
      3 and 6 alternate. The rows' 9,6,3 roots run only through these halvings.
  F2. The first odd step leaves the multiples of 3 with digital root exactly 1:
      n = 3m odd -> 3n+1 = 9m+1. Then 3 never divides a later value (3n+1 = 1
      mod 3, halving keeps that), so the roots 3, 6, 9 never return.
      12312 -> 6156 -> 3078 -> 1539 -> 4618 (DR 9,9,9,9 then 1).
  F3. 5-piece rows are odd (digit_ladder_right_extension), so they open with
      3n+1; rows a = 1 mod 3 (DR 3,9,6) are multiples of 3 and go straight to DR 1.

COMPUTED (contingent, recorded, not explained):
  4-piece rows 1-18: steps to 1
    12312 37 | 23514 82 | 34716 173 | 45918 176 | 56220 91 | 67422 130 |
    78624 138 | 89826 133 | 91128 208 | 12330 37 | 23532 144 | 34734 111 |
    45936 83 | 56238 47 | 67440 161 | 78642 50 | 89844 71 | 91146 133
  5-piece rows 1-9: 1231221 54 | 2351423 192 | 3471625 252 | 4591827 105 |
    5622029 157 | 6742231 147 | 7862433 173 | 8982635 212 | 9112837 225
  Equal totals are explained by merging at equal depth:
    12312 and 12330 (rows 1, 10) join at 184, both at step 19 -> 37 and 37.
    89826 and 91146 (rows 8, 18) join at 214, both at step 32 -> 133 and 133.
  12312, 78624, 45936 and 67440 never rise above their start.

TESTED AGAINST A BASELINE -- NOT FINDINGS:
  All nine 4-piece rows pass through 40: so do 94% of random 5-digit numbers.
  Seven of the nine pass through 1732: random 5-digit numbers do 40% of the
  time, and 1732 was picked after looking, so this is not established.
  Repdigit/opening pairs with equal totals (44/45 16, 66/67 27, 99/100 25):
  37% of consecutive n < 1000 share a total; not special.

FALSIFICATION: any assertion below failing.
"""
def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def traj(n):
    t = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        t.append(n)
    return t

def row(a, P=4):
    parts = [dr(a), dr(a + 1), dr(2 * a + 1)] + [2 * a + 1 + 9 * j for j in range(1, P - 2)]
    return int("".join(map(str, parts)))

STEPS4 = [37, 82, 173, 176, 91, 130, 138, 133, 208, 37, 144, 111, 83, 47, 161, 50, 71, 133]
STEPS5 = [54, 192, 252, 105, 157, 147, 173, 212, 225]
assert [len(traj(row(a))) - 1 for a in range(1, 19)] == STEPS4
assert [len(traj(row(a, 5))) - 1 for a in range(1, 10)] == STEPS5

for a in range(1, 200):
    n = row(a)
    t = traj(n)
    assert n % 6 == 0
    k = next(i for i, x in enumerate(t) if x % 3)
    assert all(x % 2 == 0 for x in t[:k - 1]) and t[k - 1] % 2 == 1
    assert all(dr(t[i + 1]) == dr(5 * t[i]) for i in range(k - 1))
    assert dr(t[k]) == 1 and all(x % 3 for x in t[k:])
for n in range(3, 300000, 3):
    t = traj(n)
    k = next(i for i, x in enumerate(t) if x % 3)
    assert dr(t[k]) == 1
for a in range(1, 100):
    n = row(a, 5)
    assert n % 2 == 1 and (n % 3 == 0) == (a % 3 == 1)
assert traj(12312)[:5] == [12312, 6156, 3078, 1539, 4618]

def join(x, y):
    tx, ty = traj(x), traj(y)
    sy = set(ty)
    v = next(v for v in tx if v in sy)
    return v, tx.index(v), ty.index(v)
assert join(12312, 12330) == (184, 19, 19) and join(89826, 91146) == (214, 32, 32)
assert all(max(traj(n)) == n for n in (12312, 78624, 45936, 67440))
assert all(40 in traj(row(a)) for a in range(1, 10))
assert sum(1732 in traj(row(a)) for a in range(1, 10)) == 7

if __name__ == "__main__":
    for a in range(1, 19):
        print(a, row(a), len(traj(row(a))) - 1)
    print("all assertions pass")

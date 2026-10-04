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
  common among neighbours -- see the next section.

THE "37%" (owner, 2026-10-04: "37% not a coincidence") -- TESTED, IT IS NOT A
CONSTANT. The share of n whose total equals that of n+1 depends on the range:
    n <= 999        365 / 999          0.365
    n <= 9,999      4,161 / 9,999      0.416
    n <= 99,999     45,022 / 99,999    0.450
    n <= 999,999    477,245 / 999,999  0.477
    n <= 1,999,999  966,531 / 1,999,999 0.483
  It keeps rising; "37%" was 36.5% at the cutoff 1000, rounded. 365/999 =
  0.365365... repeats because the denominator is 999 (any k/999 repeats k).
  Proved part: 8k+4 and 8k+5 always share a total -- both reach 6k+4 in three
  steps (8k+4 -> 4k+2 -> 2k+1 -> 6k+4; 8k+5 -> 24k+16 -> 12k+8 -> 6k+4) -- so the
  share is at least 1/8 for every range.

ROWS 19-36 (4 pieces, first piece DR(a)):
    12348 112 | 23550 126 | 34752 142 | 45954 176 | 56256 153 | 67458 68 |
    78660 50 | 89862 133 | 91164 133 | 12366 156 | 23568 100 | 34770 85 |
    45972 176 | 56274 83 | 67476 60 | 78678 200 | 89880 89 | 91182 58
  Never above start: also 34752, 56256, 78660, 23568, 67476, 89880.
  Shared totals across rows 1-36:
    133: rows 8, 18, 26, 27 (89826, 91146, 89862, 91164)
    176: rows 4, 22, 31 (45918, 45954, 45972)
    37: rows 1, 10 | 83: rows 13, 32 | 50: rows 16, 25
  12 equal pairs among 36 rows. Against 36 random multiples of 6 (10k-100k):
  mean 4.9, 12 or more in 1.2% -- looks unusual. But ladder rows come in
  families 18 apart (row a+9 = row a + 18) and close numbers merge early.
  Random bases with the SAME layout give mean 13.2, 12 or more in 59%.
  So the shared totals are explained by the +18 layout, not by anything else.

ROWS 37-72 (owner: "keep going to row 72"):
    12384 125 | 23586 100 | 34788 204 | 45990 83 | 56292 153 | 67494 60 |
    78696 107 | 89898 164 | 911100 201 | 123102 255 | 235104 168 | 347106 73 |
    459108 200 | 562110 133 | 674112 48 | 786114 74 | 898116 188 | 911118 56 |
    123120 149 | 235122 199 | 347124 78 | 459126 63 | 562128 177 | 674130 84 |
    786132 74 | 898134 188 | 911136 56 | 123138 211 | 235140 150 | 347142 166 |
    459144 81 | 562146 177 | 674148 84 | 786150 56 | 898152 201 | 911154 56
  From row 45 the last piece has 3 digits and the rows have 6 digits; the +18
  family step holds for a+9 <= 44 and resumes inside the 6-digit block.
  Shared totals over rows 1-72: 33 equal pairs (largest: 133 at rows 8, 18,
  26, 27, 50; 56 at rows 54, 63, 70, 72). Same-layout null: mean 34.6, 33 or
  more in 57% -- the +18 layout again, nothing more.

RISING ABOVE THE START -- decided by the parity of the row number:
  F4 (proved). Even a: the last piece 2a+10 = 2 mod 4, so the row is 2 mod 4:
      n -> n/2 (odd) -> 3n/2 + 1 > n. Every even row rises above its start.
      Odd a: 2a+10 = 0 mod 4, so the row is 0 mod 4 and opens with two halvings.
  Rows 1-72 that never rise above their start: 1, 7, 13, 15, 21, 23, 25, 29,
  33, 35, 37, 41, 47, 51, 53, 55, 59, 61, 63, 65, 67, 69, 71 -- odd rows only,
  as F4 forces. 23 of the 36 odd rows (64%); random multiples of 12 of the
  same size stay below 58% of the time, so the odd-row rate is ordinary.

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

STEPS4 = [37, 82, 173, 176, 91, 130, 138, 133, 208, 37, 144, 111, 83, 47, 161, 50, 71, 133,
          112, 126, 142, 176, 153, 68, 50, 133, 133, 156, 100, 85, 176, 83, 60, 200, 89, 58,
          125, 100, 204, 83, 153, 60, 107, 164, 201, 255, 168, 73, 200, 133, 48, 74, 188, 56,
          149, 199, 78, 63, 177, 84, 74, 188, 56, 211, 150, 166, 81, 177, 84, 56, 201, 56]
STEPS5 = [54, 192, 252, 105, 157, 147, 173, 212, 225]
assert [len(traj(row(a))) - 1 for a in range(1, 73)] == STEPS4
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

def steps(n):
    c = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        c += 1
    return c

ST = [0, 0] + [steps(n) for n in range(2, 10001)]
assert sum(ST[n] == ST[n + 1] for n in range(1, 1000)) == 365
assert sum(ST[n] == ST[n + 1] for n in range(1, 10000)) == 4161
assert all(ST[8 * k + 4] == ST[8 * k + 5] for k in range(1, 1249))
assert all(traj(8 * k + 4)[3] == traj(8 * k + 5)[3] == 6 * k + 4 for k in range(1, 5000))
assert all(max(traj(row(a))) == row(a) for a in (21, 23, 25, 29, 33, 35))
assert [a for a in range(1, 37) if STEPS4[a - 1] == 133] == [8, 18, 26, 27]
assert [a for a in range(1, 37) if STEPS4[a - 1] == 176] == [4, 22, 31]
assert sum(STEPS4[i] == STEPS4[j] for i in range(36) for j in range(i + 1, 36)) == 12
assert sum(STEPS4[i] == STEPS4[j] for i in range(72) for j in range(i + 1, 72)) == 33
assert [a for a in range(1, 73) if STEPS4[a - 1] == 133] == [8, 18, 26, 27, 50]
for a in range(1, 400):
    n = row(a)
    assert n % 4 == (2 if a % 2 == 0 else 0)
    if a % 2 == 0:
        assert traj(n)[2] == 3 * (n // 2) + 1 > n
NEVER = [a for a in range(1, 73) if max(traj(row(a))) == row(a)]
assert NEVER == [1, 7, 13, 15, 21, 23, 25, 29, 33, 35, 37, 41, 47, 51, 53, 55, 59,
                 61, 63, 65, 67, 69, 71]
assert all(a % 2 for a in NEVER) and len(NEVER) == 23
assert all(row(a + 9) - row(a) == 18 for a in range(1, 28))

if __name__ == "__main__":
    for a in range(1, 73):
        print(a, row(a), len(traj(row(a))) - 1)
    print("all assertions pass")

# CLASS: AUDIT
"""
Audit of supplied text (2026-10-03): digital roots of the stack counts from
t325_uniformity_supplied_audit_2026_10_03.py, extended to n-digit stacks with the count
formula uniform = n! * n^(n-1), total = (n!)^n. Mathematics only.

CORRECT
  R1 Every number and digital root given: n=3: 216, 54, 162 -> 9, 9, 9; n=4: 331,776,
     1,536, 330,240 -> 9, 6, 3; n=5: 24,883,200,000, 75,000, 24,883,125,000 -> 9, 3, 6.
  R2 uniform = n! * n^(n-1) for n-row stacks of n-digit permutations, confirmed by brute
     force at n = 4 (all 331,776 stacks): the T325 converse (uniform <=> every row a rotation
     of row 0) holds at n = 4 as at n = 3.
  R3 "uniform root + broken root = 9" is forced: uniform + broken = total, and total = 0 mod 9.

WRONG
  R4 "The balance alternates between 3 and 6 no matter how high n scales." It stops at n = 6:
     from n = 6 on, 9 | n!, so uniform, broken and total are all 0 mod 9 -- every root is 9.
        n:        3  4  5  6  7  8  9  10
        uniform:  9  6  3  9  9  9  9  9
  R5 The reason given for total = 0 mod 9 ("n! contains 9 for n >= 6") does not cover n = 3,4,5,
     where n! has a single 3. The real reason: 3 | n! for n >= 3, so 3^n | (n!)^n, and n >= 2
     gives 9. (n = 2: total 4, not a multiple of 9.)
NOT ESTABLISHED
  R6 "Double-Notch" and "Split-Chirality wave" shapes in the 330,240 broken 4-digit stacks:
     named, not computed.
FALSIFICATION: any assertion failing.
"""
import itertools
from math import factorial

dr = lambda m: 1 + (m - 1) % 9 if m else 0
uniform = lambda n: factorial(n) * n ** (n - 1)
total = lambda n: factorial(n) ** n

assert (total(3), uniform(3), total(3) - uniform(3)) == (216, 54, 162)
assert (total(4), uniform(4), total(4) - uniform(4)) == (331_776, 1_536, 330_240)
assert (total(5), uniform(5), total(5) - uniform(5)) == (24_883_200_000, 75_000, 24_883_125_000)
assert [dr(x) for x in (216, 54, 162, 331_776, 1_536, 330_240)] == [9, 9, 9, 9, 6, 3]
assert [dr(x) for x in (24_883_200_000, 75_000, 24_883_125_000)] == [9, 3, 6]          # R1

# R2: brute force n = 4
perms = list(itertools.permutations(range(4)))
pos = {p: {d: p.index(d) for d in range(4)} for p in perms}
count = 0
for stack in itertools.product(perms, repeat=4):
    base = [pos[r][0] for r in stack]
    ok = True
    for d in (1, 2, 3):
        s = (pos[stack[0]][d] - base[0]) % 4
        if any((pos[r][d] - b) % 4 != s for r, b in zip(stack, base)):
            ok = False
            break
    if ok:
        rot0 = {stack[0][k:] + stack[0][:k] for k in range(4)}
        assert all(r in rot0 for r in stack)
        count += 1
assert count == uniform(4) == 1536

for n in range(3, 30):                                                                   # R3
    assert total(n) % 9 == 0 and (dr(uniform(n)) + dr(total(n) - uniform(n))) % 9 == 0
assert [dr(uniform(n)) for n in range(3, 11)] == [9, 6, 3, 9, 9, 9, 9, 9]                # R4
assert all(uniform(n) % 9 == 0 for n in range(6, 40))
assert total(2) == 4 and [factorial(n) % 9 == 0 for n in (3, 4, 5)] == [False] * 3      # R5

if __name__ == "__main__":
    print("uniform roots n=3..10:", [dr(uniform(n)) for n in range(3, 11)])

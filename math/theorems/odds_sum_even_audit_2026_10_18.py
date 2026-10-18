# CLASS: AUDIT
"""
The pasted text "An even number of odd integers always sums to an even total" (owner_work #340, 2026-10-18). Another tool's text, relayed by the owner.

RIGHT:
  2 odds: 1+3=4.  4 odds: 1+3+5+7=16.  An even number of odd numbers always adds to an even number.
  1+3+5+...+(2n-1)=n^2.  n=2: 4, n=4: 16, n=6: 36, n=8: 64 (even).  n=1: 1, n=3: 9, n=5: 25 (odd).
WRONG:
  "Since 2 factors out completely, the sum is divisible by 2": the sum of m odds is 2(k1+...+km)-m. The -m only has a 2 in it when m is even. The proof
  leaves out that the count must be even; with an odd count the 2 does not factor out.
  "Pairing any set of odds ... forcing the sum to even every time": wrong. 1+3+5=9 is odd, and the paste's own n=3, n=5 lines (9, 25) show it.
  Pairing works only when every odd gets a partner, so only for an even count. An odd count leaves one over, and the sum is odd.
CONNECTION to the owner's lines (owner_work 2026-10-18): the owner's 135=9 is 1+3+5, the first three odds, 9=3x3. The first six odds add to 36=6x6 and 36 is the
  owner's 12+24=36 (246=12, 789=24). The first nine add to 81=9x9. So 3, 6, 9 give 9, 36, 81, and all three have digital root 9.
FRAMEWORKS (gf37-audit): 4 C3; 16 SA_ST_A; 36 NEG_H; 64 NEG_H; 1 IC; 9 SA_ST_A; 25 SA_ST_B; 81 D7.
FALSIFICATION: any assertion failing.
"""
from itertools import combinations


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


odds = list(range(1, 60, 2))
assert all(sum(c) % 2 == 0 for m in (2, 4, 6) for c in combinations(odds[:12], m))                  # even count: even sum
assert all(sum(c) % 2 == 1 for m in (1, 3, 5) for c in combinations(odds[:12], m))                  # odd count: odd sum
assert 1 + 3 == 4 and 1 + 3 + 5 + 7 == 16 and 1 + 3 + 5 == 9
assert all(sum(2 * k - 1 for k in range(1, n + 1)) == n * n for n in range(1, 200))
assert [n * n for n in (2, 4, 6, 8)] == [4, 16, 36, 64] and [n * n for n in (1, 3, 5)] == [1, 9, 25]
m = 4
ks = [3, 5, 8, 2]
assert sum(2 * k - 1 for k in ks) == 2 * sum(ks) - m and (2 * sum(ks) - m) % 2 == 0                  # -m has a 2 only because m is even
assert (2 * sum([3, 5, 8]) - 3) % 2 == 1                                                          # three odds: the 2 does not factor out
assert 1 + 3 + 5 == 9 and 9 % 2 == 1                                                              # "every time" is wrong
assert 1 + 3 + 5 == 9 == 3 * 3 and sum(range(1, 12, 2)) == 36 == 6 * 6 and sum(range(1, 18, 2)) == 81 == 9 * 9
assert 2 + 4 + 6 == 12 and 7 + 8 + 9 == 24 and 12 + 24 == 36 and [dr(n) for n in (9, 36, 81)] == [9, 9, 9]
assert [n % 37 for n in (4, 16, 36, 64, 1, 9, 25, 81)] == [4, 16, 36, 27, 1, 9, 25, 7]

if __name__ == "__main__":
    print("even count of odds adds to even: right; the proof and 'every time' are wrong (1+3+5=9); 9, 36, 81 are 3x3, 6x6, 9x9 and 36=12+24")

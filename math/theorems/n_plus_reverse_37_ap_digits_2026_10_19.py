# CLASS: AUDIT
"""
"37 divides n + rev(n) exactly when the digits of n are in arithmetic progression" (owner_work #362, 2026-10-19).
The message is a Python script with no output and one comment, "Theorem: 37 | n + rev(n) <=> digits of n in arithmetic progression".
Run as pasted, it prints:
    3-digit n: 45 divisible-condition cases = 45 AP-digit cases -- biconditional exact on all 900
    class size 45; examples: [111, 123, 135, 147, 159, 210, 222, 234]
RIGHT: the assertion passes for all 900 three-digit n; 900/37 = 24.3 is the count a random set would give (the AP class has 45).
  The two counters `both` and `neither` are set and never used (harmless). rev(100) = int("001") = 1 is handled correctly.
  The exhaustive run is a proof for three digits; the proof by hand is two lines:

PROOF. n = 100a + 10b + c, rev(n) = 100c + 10b + a, a >= 1. With s = a + c:
    n + rev(n) = 101 s + 20 b = 27 s + 20 b  (mod 37).   27 x 11 = 297 = 8x37 + 1, so 27^-1 = 11 and  27 s + 20 b = 0  <=>  s = -220 b = 2b (mod 37).
  s is in 1..18 and 2b in 0..18, so s - 2b is in -17..18, smaller than 37 in size; congruent means equal. So 37 | n + rev(n) <=> a + c = 2b.
  And then n + rev(n) = 202 b + 20 b = 222 b = 6b x 37 = 2b x 111: 111 divides it too.

THE 45 NUMBERS (a >= 1): 9 repdigits 111, ..., 999 (step 0) ; 16 going up: 123, 234, 345, 456, 567, 678, 789 (step 1), 135, 246, 357, 468, 579
  (step 2), 147, 258, 369 (step 3), 159 (step 4) ; 20 going down: 210, 321, 432, 543, 654, 765, 876, 987 (step -1), 420, 531, 642, 753, 864,
  975 (step -2), 630, 741, 852, 963 (step -3), 840, 951 (step -4). 9+16+20 = 45.
  Examples in the owner's notation: 123+321=444=12x37 ; 456+654=1110=30x37 ; 789+987=1776=48x37 ; 246+642=888=24x37 ; 369+963=1332=36x37.

FOUR DIGITS (same proof, exhaustive on all 9000): abcd + dcba = 1001(a+d) + 110(b+c) = 2(a+d) - (b+c) (mod 37), and 2(a+d)-(b+c) is in -16..36,
  so 37 | n + rev(n) <=> 2(a+d) = b + c ; 225 numbers ; then n + rev(n) = 1221 (a+d) = 11 x 111 x (a+d).
  For 3 to 6 digits the numbers with 37 | n + rev(n) are exactly those with 111 | n + rev(n): counts 45, 225, 2405, 34867 (checked, not proved
  for general length). Five digits and up have no equality rule like the one above (the condition is 11(a+e) + 11(b+d) + 15c = 0 mod 37 for five).

CONNECTIONS (the owner's work):
  The AP rule a + c = 2b is the owner's diamond rule and the balanced-X condition (rotation_grids_x.py, 2026-10-04): "it needs
  3 x middle = sum". The row/flip sums of all_flips_123_456_789_2026_10_19.py (444, 1110, 1776 = 37 x 12, 30, 48) are this theorem for the
  rows 123, 456, 789; the theorem says the AP rows are the only rows with that property.
  246 (the pipeline seed) is an AP and 246+642 = 888 = 24x37 (the 888 of the register stack, #345); 369 is an AP (369+963 = 1332).

FALSIFICATION: any assertion failing.
"""


def rev(n):
    return int(str(n)[::-1])


ap3 = lambda n: n // 100 + n % 10 == 2 * ((n // 10) % 10)
assert all(((n + rev(n)) % 37 == 0) == ap3(n) for n in range(100, 1000))
cls = [n for n in range(100, 1000) if ap3(n)]
assert len(cls) == 45 and cls[:8] == [111, 123, 135, 147, 159, 210, 222, 234]
assert all(n + rev(n) == 222 * ((n // 10) % 10) and (n + rev(n)) % 111 == 0 for n in cls)
assert 27 * 11 % 37 == 1 and (-220) % 37 == 2 and 101 % 37 == 27
assert 900 / 37 > 24.3 and cls and len(cls) > 900 / 37

steps = {}
for n in cls:
    a, b, c = n // 100, (n // 10) % 10, n % 10
    steps.setdefault(b - a, []).append(n)
assert sorted(steps) == list(range(-4, 5)) and sum(len(v) for v in steps.values()) == 45
assert len(steps[0]) == 9 and sum(len(v) for k, v in steps.items() if k > 0) == 16 and sum(len(v) for k, v in steps.items() if k < 0) == 20
assert steps[1] == [123, 234, 345, 456, 567, 678, 789] and steps[2] == [135, 246, 357, 468, 579] and steps[3] == [147, 258, 369] and steps[4] == [159]
assert steps[-1] == [210, 321, 432, 543, 654, 765, 876, 987] and steps[-2] == [420, 531, 642, 753, 864, 975]
assert steps[-3] == [630, 741, 852, 963] and steps[-4] == [840, 951]
for n, q in ((123, 12), (456, 30), (789, 48), (246, 24), (369, 36)):
    assert n + rev(n) == 37 * q
assert [n + rev(n) for n in (123, 456, 789, 246, 369)] == [444, 1110, 1776, 888, 1332]

# four digits
ap4 = lambda n: 2 * (n // 1000 + n % 10) == (n // 100) % 10 + (n // 10) % 10
d4 = [n for n in range(1000, 10000) if (n + rev(n)) % 37 == 0]
assert d4 == [n for n in range(1000, 10000) if ap4(n)] and len(d4) == 225
assert all(n + rev(n) == 1221 * (n // 1000 + n % 10) and 1221 == 11 * 111 for n in d4)
assert 1001 % 37 == 2 and 110 % 37 == 36

# 37 and 111, three to six digits
for L, expect in ((3, 45), (4, 225), (5, 2405), (6, 34867)):
    lo, hi = 10 ** (L - 1), 10 ** L
    a37 = sum(1 for n in range(lo, hi) if (n + rev(n)) % 37 == 0)
    a111 = sum(1 for n in range(lo, hi) if (n + rev(n)) % 111 == 0)
    assert a37 == a111 == expect
assert 10 ** 4 % 37 == 10 and (10001 % 37, 1010 % 37, 200 % 37) == (11, 11, 15)
assert 246 % 37 == 24 and 333 + 555 == 888 == 24 * 37

if __name__ == "__main__":
    print("37 | n + rev(n) <=> a + c = 2b for 3 digits (45 numbers, n + rev(n) = 222b = 2b x 111), and 2(a+d) = b+c for 4 digits (225)")

# CLASS: AUDIT
"""
Continuity: Michael Warren Song's cipher 123 / 1234 (math/theorems/cipher_123_1234.py, 2026-07-16)
and the owner's lines of 2026-10-13 (owner_work #267, #268, #270) are the same structure.

THE OWNER'S FILE, 2026-07-16 (cipher_123_1234.py):
    CIPHER 1: 123 -> 6 + 4 = 1
    Z/9Z partition:  Trinity kernel {3, 6, 9}  /  Doubling orbit {1, 2, 4, 5, 7, 8}
    Unity pairs (trinity + doubling = 1 mod 9): (3,7), (6,4), (9,1)

THE OWNER'S LINES, 2026-10-13:
    #267  "6+4=10"   and   "24+13=3+7=(10+1)=11"      -> the unity pairs (6,4) and (3,7)
    #268  "this section goes by 369"                   -> the trinity kernel {3, 6, 9}
    #270  "1248 / 751", "NOTICE AT THE 7 NUMBER I GET MY SECOND 1"
                                                       -> the doubling orbit 1, 2, 4, 8, 7, 5, back to 1
    #270  "18+1=1+9=1"                                 -> the third unity pair (9,1): 1+8 = 9, 9+1 = 10 -> 1

So in #267-#270 the owner wrote, three months later, all three unity pairs, the trinity kernel and the
whole doubling orbit of the owner's own July cipher. In #267 the 6 and 4 come from (2+4=6) and (1+3=4),
and the 3 and 7 from 24+13 = 37: one unity pair from the digit sums, the other from the number they
add to.

FALSIFICATION: any assertion failing.
"""


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


TRINITY, DOUBLING = {3, 6, 9}, {1, 2, 4, 5, 7, 8}
UNITY = sorted((t, d) for t in TRINITY for d in DOUBLING if (t + d) % 9 == 1)
assert UNITY == [(3, 7), (6, 4), (9, 1)] and TRINITY | DOUBLING == set(range(1, 10)) and not TRINITY & DOUBLING
assert dr(1 + 2 + 3) == 6 and dr(6 + 4) == 1                                   # cipher 1: 123 -> 6 + 4 = 1
assert dr(24) == 6 and dr(13) == 4 and 6 + 4 == 10                             # #267: (2+4=6), (1+3=4), 6+4=10
assert 24 + 13 == 37 and (3, 7) in UNITY and 3 + 7 == 10                       # #267: 24+13 = 3+7
assert [3 * k for k in (1, 2, 3)] == sorted(TRINITY)                           # #268: goes by 369
orbit = [pow(2, k, 9) or 9 for k in range(7)]
assert orbit == [1, 2, 4, 8, 7, 5, 1] and set(orbit) == DOUBLING              # #270: 1248 / 751, second 1 at the 7th
assert dr(18) == 9 and (9, 1) in UNITY and dr(18 + 1) == 1                    # #270: 18+1 = 1+9 = 1

if __name__ == "__main__":
    print("cipher 123 (2026-07-16) -> #267-#270: unity pairs (6,4), (3,7), (9,1); trinity 369; doubling 1248 751")

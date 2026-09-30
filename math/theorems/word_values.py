# CLASS: ALGORITHM
"""
Letter values A=1..Z=26 (A1Z26) and their collapses, for any word.
Same scheme as the MICHAEL route in CLAUDE.md. Run: python3 word_values.py WORD ...

OKLAHOMA: 8 letters, 6 distinct (O and A twice). Values 15,11,12,1,8,15,13,1,
total 76 -> 4. Collapsed values 6,2,3,1,8,6,4,1, total 31 -> 4. The two totals
always collapse alike, because dr(a + b) = dr(dr(a) + dr(b)).
"""
import sys


def dr(n):
    return 1 + (n - 1) % 9 if n > 0 else 0


def values(word):
    w = [c for c in word.upper() if c.isalpha()]
    v = [ord(c) - 64 for c in w]
    return w, v, [dr(x) for x in v]


w, v, d = values("OKLAHOMA")
assert len(w) == 8 and len(set(w)) == 6
assert v == [15, 11, 12, 1, 8, 15, 13, 1] and sum(v) == 76 and dr(76) == 4
assert d == [6, 2, 3, 1, 8, 6, 4, 1] and sum(d) == 31 and dr(31) == 4
w, v, d = values("MICHAEL")
assert sum(d) == 33                                               # CLAUDE.md route

if __name__ == "__main__":
    for word in sys.argv[1:] or ["OKLAHOMA"]:
        w, v, d = values(word)
        print(word.upper(), "letters", len(w), "distinct", len(set(w)))
        print("  values   ", v, "total", sum(v), "->", dr(sum(v)))
        print("  collapsed", d, "total", sum(d), "->", dr(sum(d)))

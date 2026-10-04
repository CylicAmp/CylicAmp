# CLASS: COMPUTATION
"""
X, diamond and other shapes from the two new stacks of 2026-10-03, built the T325 way.
Author: Michael Warren Song (CyclicAmp)

T325 (theorem_325_rotation_walk_shapes_gf37.py) draws figures by WALKING a stack and
following where one digit sits in each row:
    sawtooth  a b c a b c a      chevron  c b a b c
    diamond   c b a a b c        X        chevron crossed with its column mirror
Stacks: B = 123 / 231 / 321 (the alternative), C = 357 / 573 / 735.
(rotation_alternative_123_231_321_and_357.py has the stacks themselves.)

=== C (357): THE SAME FIGURES AS T325 ===
C is a rotation class, so every T325 figure appears, and all three digits draw the same
shape shifted across the columns (T325's "the three tracks are one shape" holds).
Digit 7 draws them clean:
    chevron 0 1 2 1 0     diamond 0 1 2 2 1 0     X-arm 2 1 0 1 2
C turns the opposite way to T325's 123/312/231, so the clean figure moves to the LAST
digit (7) instead of the first (1).

=== B (123/231/321): X AND DIAMOND STILL FORM -- FROM ONE DIGIT ONLY ===
Digit 3 draws every T325 figure clean:
    chevron 0 1 2 1 0     diamond 0 1 2 2 1 0     X-arm 2 1 0 1 2   -> X
The other two digits draw DIFFERENT shapes, because B is not a rotation class:
    digit 2:  1 0 1 0 1    a ZIGZAG held in the left two columns (new)
    digit 1:  2 2 0 2 2    a NOTCH: stays right, drops to the left edge once (new)
So T325's "the three tracks are one shape" FAILS for B: one stack, three different figures.

Pictures (each row of the walk, the digit marked, others '.'):

    B chevron, digit 3    B diamond, digit 3    B X (digit 3, both arms)
    3 . .                 3 . .                 3 . 3
    . 3 .                 . 3 .                 . 3 .
    . . 3                 . . 3                 3 . 3     <- arms meet in the middle column on rows 2 and 4
    . 3 .                 . . 3                 . 3 .
    3 . .                 . 3 .                 3 . 3
                          3 . .
    B zigzag, digit 2     B notch, digit 1
    . 2 .                 . . 1
    2 . .                 . . 1
    . 2 .                 1 . .
    2 . .                 . . 1
    . 2 .                 . . 1
FALSIFICATION: any assertion failing.
"""

B = ["123", "231", "321"]
C = ["357", "573", "735"]


def walks(S):
    a, b, c = S
    return {"sawtooth": [a, b, c, a, b, c, a], "chevron": [c, b, a, b, c],
            "diamond": [c, b, a, a, b, c], "xarm": [a, b, c, b, a]}


def track(stack, d):
    return [r.index(d) for r in stack]


def picture(cols, mark):
    return ["".join(mark if i == c else "." for i in range(3)) for c in cols]


CHEV, DIAM, XARM = [0, 1, 2, 1, 0], [0, 1, 2, 2, 1, 0], [2, 1, 0, 1, 2]
mirror = lambda t: [2 - c for c in t]

# C: every figure, all three digits the same shape shifted mod 3
wC = walks(C)
assert track(wC["chevron"], "7") == CHEV and track(wC["diamond"], "7") == DIAM
assert track(wC["xarm"], "7") == XARM and mirror(CHEV) == XARM
for name, st in wC.items():
    t7 = track(st, "7")
    for d in "35":
        shift = (track(st, d)[0] - t7[0]) % 3
        assert track(st, d) == [(c + shift) % 3 for c in t7], (name, d)

# B: digit 3 clean, digits 1 and 2 different shapes
wB = walks(B)
assert track(wB["chevron"], "3") == CHEV and track(wB["diamond"], "3") == DIAM
assert track(wB["xarm"], "3") == XARM
assert track(wB["chevron"], "2") == [1, 0, 1, 0, 1]
assert track(wB["chevron"], "1") == [2, 2, 0, 2, 2]
t3 = track(wB["chevron"], "3")
assert not any(track(wB["chevron"], d) == [(c + s) % 3 for c in t3] for d in "12" for s in range(3))

# X: the two arms meet in the middle column on rows 2 and 4
x = [["."] * 3 for _ in range(5)]
for i, (c1, c2) in enumerate(zip(CHEV, XARM)):
    x[i][c1] = x[i][c2] = "3"
assert ["".join(r) for r in x] == ["3.3", ".3.", "3.3", ".3.", "3.3"]
assert picture(track(wB["chevron"], "2"), "2") == [".2.", "2..", ".2.", "2..", ".2."]
assert picture(track(wB["chevron"], "1"), "1") == ["..1", "..1", "1..", "..1", "..1"]

if __name__ == "__main__":
    for name in ("chevron", "diamond"):
        print(f"B {name}, digit 3:", picture(track(wB[name], "3"), "3"))
    print("B X:", ["".join(r) for r in x])
    print("B zigzag, digit 2:", picture(track(wB["chevron"], "2"), "2"))
    print("B notch, digit 1:", picture(track(wB["chevron"], "1"), "1"))

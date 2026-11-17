# CLASS: COMPUTATION
"""
The owner's lines (2026-11-17), quoted as written:

    "3333=12 or 66 or 39
     12121212=
     34343434=
     46464646="

CLEANED: cut 3333 three ways and add the pieces:
    3 + 3 + 3 + 3 = 12      33 + 33 = 66      3 + 3 + 33 = 39                                   right, all three
  and the same cuts for the three 8-digit numbers (the 39 cut read as 3 + 3 + 33 on each 4-digit block), with the
  halves and the comma groups (the "both ways" count) added:
    12121212:  singles 12   pairs 12+12+12+12 = 48     blocks (1+2+12)+(1+2+12) = 30   halves 1212+1212 = 2424
               commas 12,121,212 -> 12+121+212 = 345
    34343434:  singles 28   pairs 34 x 4 = 136         blocks 41 + 41 = 82             halves 3434+3434 = 6868
               commas 34+343+434 = 811
    46464646:  singles 40   pairs 46 x 4 = 184         blocks 56 + 56 = 112            halves 4646+4646 = 9292
               commas 46+464+646 = 1156
    3333 with the comma: 3,333 -> 3 + 333 = 336

WHY THEY AGREE (forced): every cut keeps the root, because 10 leaves 1 by 9 -- 3333's 12, 66, 39, 336 all give 3;
  12121212's cuts all give 3; 34343434's all give 1; 46464646's all give 4.
WHAT THE THREE ADD TO: 12 + 34 = 46, so 12121212 + 34343434 = 46464646, and every cut adds the same way:
  12 + 28 = 40, 48 + 136 = 184, 30 + 82 = 112, 2424 + 6868 = 9292, 345 + 811 = 1156; roots 3 + 1 = 4.
FORCED: abababab = ab x 1010101 = ab x 73 x 101 x 137 (10001 = 73 x 137), so each holds 73, 101 and 137; and 1010101
  leaves 1 by 37, so each leaves the same as its pair: 12121212 -> 12, 34343434 -> 34, 46464646 -> 9 (46 - 37).

FALSIFICATION: any assertion failing.
"""
from sympy import factorint


def root(n):
    return 1 + (n - 1) % 9 if n else 0


def cuts(s):
    singles = sum(map(int, s))
    pairs = sum(int(s[i:i + 2]) for i in range(0, len(s), 2))
    blocks = sum(int(b[0]) + int(b[1]) + int(b[2:]) for b in (s[i:i + 4] for i in range(0, len(s), 4)))
    halves = int(s[:len(s) // 2]) + int(s[len(s) // 2:]) if len(s) > 4 else None
    comma = sum(int(g) for g in f"{int(s):,}".split(","))
    return singles, pairs, blocks, halves, comma


assert cuts("3333")[:3] == (12, 66, 39) and cuts("3333")[4] == 336
assert 3 + 33 + 3 == 33 + 3 + 3 == 39
assert cuts("12121212") == (12, 48, 30, 2424, 345)
assert cuts("34343434") == (28, 136, 82, 6868, 811)
assert cuts("46464646") == (40, 184, 112, 9292, 1156)

for s in ("3333", "12121212", "34343434", "46464646"):
    assert {root(v) for v in cuts(s) if v} == {root(int(s))}
assert [root(int(s)) for s in ("3333", "12121212", "34343434", "46464646")] == [3, 3, 1, 4]

assert 12121212 + 34343434 == 46464646
assert all(a + b == c for a, b, c in zip(cuts("12121212"), cuts("34343434"), cuts("46464646")))

for ab, n in ((12, 12121212), (34, 34343434), (46, 46464646)):
    assert n == ab * 1010101 and n % (73 * 101 * 137) == 0 and n % 37 == ab % 37
assert 1010101 % 37 == 1 and factorint(1010101) == {73: 1, 101: 1, 137: 1}

if __name__ == "__main__":
    print("3333 = 12, 66, 39 right; 12121212 / 34343434 / 46464646: singles 12, 28, 40; pairs 48, 136, 184; roots 3, 1, 4")

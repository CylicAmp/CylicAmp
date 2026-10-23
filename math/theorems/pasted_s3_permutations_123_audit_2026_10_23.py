# CLASS: AUDIT
"""
The pasted "Complete Permutation Basis (S_3)" text: the six orders of 1 2 3 (123 231 312 132 213 321), their
parity and cycles, five tracks, the sandwiches, and a table of left shift / right shift / full inversion
(owner_work #422, 2026-10-23). Audit on arrival.

THE PASTE: text from another tool, relayed by the owner (the same message asks for the walk to 100,000,000,
owner_engine_walk_100m_2026_10_23.py). Nothing below puts a claim of the paste in the owner's mouth.

PRIOR ART: the owner's flips of 123 456 789 (two_flips_123_456_789_2026_10_19.py, all_flips_123_456_789_2026_10_19.py,
#358); the 1 2 3 substrate (owner_equals_chain_three_things_brackets_2026_10_22.py, #410); the 37 test
(owner_framework_flips_halves_moves_2026_10_20.py, #374).

RIGHT (re-run), every line:
  123 even, identity;  231 even, the cycle (1 2 3);  312 even, (1 3 2)
  132 odd, swap of 2 and 3;  213 odd, swap of 1 and 2;  321 odd, swap of 1 and 3
  123 -> 231 -> 312 -> 123: each step moves the first digit to the end
  132 213 321: the three odd orders; every order of 1 2 3 adds to 6
  321 312 213 231 132 123: each step swaps two places, so even and odd take turns, and all six come once
  the table: left shift, right shift and reversal of each of the six -- all 18 entries right; the even rows are
    123 231 312
  (the paste's "Full Inversion" column is the order read backwards -- the owner's flip -- not the inverse
   permutation: the inverse of 231 is 312, its flip is 132; the column's values are the flips, all right)

NEW LINES, owner's notation:
  moving the first digit to the end is the same as adding 1 to every digit with 3 -> 1 (the 1 2 3 substrate, #410):
    123 -> +1 each -> 231 -> +1 each -> 312 -> +1 each -> 123
  so the three even orders are 123 moved along the substrate, and the three odd ones are its flip 321 moved along it.
  all six added: 123 + 132 + 213 + 231 + 312 + 321 = 1332 = 12 x 111 (each place holds 1, 2, 3 twice: 12)
  each order plus its flip (the 37 test, a + c = 2b):
    123 + 321 = 444 = 12 x 37 (1 + 3 = 2 x 2: right)   231 + 132 = 363 (2 + 1 is not 2 x 3)   312 + 213 = 525 (3 + 2 is not 2 x 1)
  by 37 (gf37-audit): 123 -> 12, 231 -> 9, 312 -> 16: SA_ST_A, all three; 132 -> 21, 213 -> 28, 321 -> 25: SA_ST_B,
    all three. Forced: moving the first digit to the end multiplies by 10 by 37 (1000 = 27 x 37 + 1), and
    x, 10x, 26x is one orbit -- so the even orders share an orbit and the odd orders share another.

FALSIFICATION: any assertion failing.
"""
from itertools import permutations

words = ["123", "231", "312", "132", "213", "321"]
assert sorted(words) == sorted("".join(p) for p in permutations("123"))


def perm(w):
    return {i + 1: int(c) for i, c in enumerate(w)}      # position i holds w[i]; as a map i -> w[i]


def parity(w):
    inv = sum(1 for i in range(3) for j in range(i + 1, 3) if w[i] > w[j])
    return 1 if inv % 2 == 0 else -1


def cycles(w):
    m, seen, out = perm(w), set(), []
    for s in (1, 2, 3):
        if s in seen:
            continue
        c, x = [], s
        while x not in seen:
            seen.add(x)
            c.append(x)
            x = m[x]
        if len(c) > 1:
            out.append(tuple(c))
    return out


assert [parity(w) for w in words] == [1, 1, 1, -1, -1, -1]
assert [cycles(w) for w in words] == [[], [(1, 2, 3)], [(1, 3, 2)], [(2, 3)], [(1, 2)], [(1, 3)]]

left = lambda w: w[1:] + w[0]
right = lambda w: w[-1] + w[:-1]
flip = lambda w: w[::-1]
table = {"123": ("231", "312", "321", True), "231": ("312", "123", "132", True), "312": ("123", "231", "213", True),
         "132": ("321", "213", "231", False), "213": ("132", "321", "312", False), "321": ("213", "132", "123", False)}
assert all((left(w), right(w), flip(w), parity(w) == 1) == v for w, v in table.items())

# the tracks
assert [left("123"), left(left("123")), left(left(left("123")))] == ["231", "312", "123"]
assert all(sum(map(int, w)) == 6 for w in words)
track = ["321", "312", "213", "231", "132", "123"]
assert sorted(track) == sorted(words) and [parity(w) for w in track] == [-1, 1, -1, 1, -1, 1]
assert all(sum(a != b for a, b in zip(track[i], track[i + 1])) == 2 for i in range(5))   # one swap per step

# "Full Inversion" is the flip, not the inverse permutation
def inverse(w):
    m = perm(w)
    inv = {v: k for k, v in m.items()}
    return "".join(str(inv[i]) for i in (1, 2, 3))


assert inverse("231") == "312" != flip("231") == "132"

# new lines
plus1 = lambda w: "".join(str(int(c) % 3 + 1) for c in w)
assert all(plus1(w) == left(w) for w in ("123", "231", "312", "321", "213", "132"))
assert sum(int(w) for w in words) == 1332 == 12 * 111
assert 123 + 321 == 444 == 12 * 37 and (231 + 132, 312 + 213) == (363, 525) and 363 % 37 and 525 % 37
assert [int(w) % 37 for w in words] == [12, 9, 16, 21, 28, 25]
assert {12, 9, 16} == {9, 12, 16} and {21, 28, 25} == {21, 25, 28}
assert 1000 == 27 * 37 + 1 and all(int(left(w)) % 37 == int(w) * 10 % 37 for w in words)
assert 26 * 26 % 37 == 10

if __name__ == "__main__":
    print("#422 permutations: every line right; the three even orders are 123 moved along 1 2 3 (+1 each digit), "
          "the odd ones its flip 321; by 37 the evens are SA_ST_A, the odds SA_ST_B (moving a digit to the end = x10)")

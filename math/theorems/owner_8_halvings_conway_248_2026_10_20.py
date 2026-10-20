# CLASS: AUDIT
"""
8 by halvings, read Conway's way and the owner's way; 248 and 24424884 (owner_work #373, 2026-10-20). Process entry: owner_work/PROCESS.md, #373.

THE OWNER'S LINES, verbatim:
    8=44,2222,111,111,11
    2442|31|31+21=5+2=7
    248
    24332

    248=
    its also
    24424884
  and in the owner's words (dictated): "here we're doing a little Conway, and we're doing a little bit of me and we've already gone over this ...
  the first one I'm going there is 2 fours and 4 twos, and then I'm going there's 3 ones. And then another three ones. And then two ones ...
  Then on the second one, I'm just going 2, 4, 8 stands for each number ... And then there's what Conway does and some more."
PRIOR (the owner's, found): 2026-10-04, "1+7=8=44,2222,11111111=248=1+4=5" (math/lemmas/ladder_loops_squares.py, line 31); Conway's
  look-and-say in the repo: T146 (theorem_146_look_and_say_142241_gf37.py, 4221111 -> 142241); 2442 and 4884 are ABBA numbers with B = 2A,
  multiples of 37 (connection_map.py).

CLEANED AND CHECKED:
  8 = 4+4 = 2+2+2+2 = 1+1+1+1+1+1+1+1 -> 44 2222 111 111 11 (the eight 1s in comma groups of 3 3 2)          right
  read each group as count then digit (the owner's way):  44 -> 24 (two 4s) ; 2222 -> 42 (four 2s) ; 111 -> 31 ; 111 -> 31 ; 11 -> 21
    -> 2442 | 31 | 31 | 21                                                                                     right
  31+21=52 -> 5+2=7                                                                                            right
  248: how many of each digit -- two 4s, four 2s, eight 1s -> 2 4 8                                            right
  24332: the sizes of the groups 44, 2222, 111, 111, 11 -> 2 4 3 3 2 ; 2+4+3+3+2=14, all 14 digits             right
  248 -> 24424884 = 24 42 48 84: each neighbour pair of 2 4 8 and its flip ; and 2442 doubled is 4884              right, both
  Conway's own step on 44222211111111 counts the eight 1s together: 24 42 81 -> 244281 (the next step 1224121811). The owner's step
    counts the 1s by comma groups: 31 31 21 instead of 81 ("a little Conway and a little bit of me").
FRAMEWORKS (gf37-audit): 248 = 2x2x2x31 = 26 mod 37 (IC, the 137-map multiplier) ; 2442 = 2x3x11x37, 4884 = 2x2x3x11x37 and 24424884 =
  2x2x3x3x11x37x1667 are 0 mod 37 ; 24332 = 2x2x7x11x79 = 23 TESLA ; 52 = 2x2x13 = 15 DARK_A ; 2222 = 2x11x101 = 2 DARK_A ; 44 = 7 D7 ;
  244281 = 3x107x761 = 7 D7 ; 31 prime (twin with 29), 7 and 11 prime.

#374 (2026-10-20), the owner adds, verbatim: "Oh, I forgot to say, the one that's even, for example, if I got 2442, then I'm going, or I got 2248,
  right? I start with 248. What I'm doing there is I go, I got 2442 4884."
  Cleaned: 248 → 24 → 2442 (24 and its flip 42) ; 48 → 4884 (48 and its flip 84). "2248" in the dictation reads as "to 248" (the start); as a number
  it would be 2+2+4+8=16. "The one that's even": 2442 and 4884 have an even number of digits and only even digits; both readings fit.
  Checked: a four-digit mirror abba = 1001a + 110b = 11 x (91a + 10b), always a multiple of 11 (forced); with b = 2a it is 1221a = 3x11x37xa:
  2442 = 2x1221, 4884 = 4x1221 = 2x2442 ; 2442+4884 = 7326 = 6x1221.                                                         right

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime


def look_and_say(s):
    out, i = "", 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out += str(j - i) + s[i]
        i = j
    return out


groups = ["44", "2222", "111", "111", "11"]
assert [sum(map(int, g)) for g in groups[:2]] == [8, 8] and sum(map(int, "".join(groups[2:]))) == 8
assert 4 + 4 == 2 + 2 + 2 + 2 == 8 * 1 == 8
owner_read = [look_and_say(g) for g in groups]
assert owner_read == ["24", "42", "31", "31", "21"] and "".join(owner_read[:2]) == "2442"
assert 31 + 21 == 52 and 5 + 2 == 7
whole = "".join(groups)
assert [whole.count(d) for d in "421"] == [2, 4, 8] and "".join(str(whole.count(d)) for d in "421") == "248"
assert "".join(str(len(g)) for g in groups) == "24332" and sum(len(g) for g in groups) == 14 == len(whole)
digits = [2, 4, 8]
pairs = [f"{a}{b}{b}{a}" for a, b in zip(digits, digits[1:])]
assert "".join(pairs) == "24424884" and 2442 * 2 == 4884 and int("24424884") == 2442 * 10 ** 4 + 4884
assert look_and_say(whole) == "244281" and look_and_say("244281") == "1224121811"

assert factorint(248) == {2: 3, 31: 1} and 248 % 37 == 26
assert all(n % 37 == 0 for n in (2442, 4884, 24424884)) and 2442 == 66 * 37 and 4884 == 132 * 37 and 1221 * 2 == 2442
assert factorint(24424884) == {2: 2, 3: 2, 11: 1, 37: 1, 1667: 1} and factorint(24332) == {2: 2, 7: 1, 11: 1, 79: 1} and 24332 % 37 == 23
assert (52 % 37, 2222 % 37, 44 % 37, 244281 % 37) == (15, 2, 7, 7) and factorint(244281) == {3: 1, 107: 1, 761: 1}
assert isprime(31) and isprime(29) and isprime(7) and isprime(11)

# #374: the mirrors of the neighbour pairs of 248
for a in range(1, 10):
    for b in range(10):
        assert (1001 * a + 110 * b) % 11 == 0
        if b == 2 * a:
            assert 1001 * a + 110 * b == 1221 * a and (1221 * a) % 37 == 0
assert 1221 == 3 * 11 * 37 and 2442 == 2 * 1221 and 4884 == 4 * 1221 == 2 * 2442 and 2442 + 4884 == 7326 == 6 * 1221
assert all(int(c) % 2 == 0 for c in "24424884") and len("2442") % 2 == 0 and "2442"[::-1] == "2442" and "4884"[::-1] == "4884"
assert 2 + 2 + 4 + 8 == 16

if __name__ == "__main__":
    print("#373: 8 = 44 2222 111 111 11 -> 2442 31 31 21 ; 31+21 = 52 -> 7 ; counts 248 ; group sizes 24332 ; 248 -> 24 42 48 84 ; Conway: 244281")

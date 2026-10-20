# CLASS: AUDIT
"""
248 read back and forth, Conway out loud, 8 halved to 1, and 0.125 -> 0.123 (owner_work #375, 2026-10-20). Process entry: owner_work/PROCESS.md, #375.

THE OWNER'S LINES, verbatim:
    248 becomes
    24.
    42
    48
    84

    what we get from reading back and forth

    conways speak out loud

    44,2222,1111|1111

    244281


    2|8|1
    8÷2÷2÷2=1
    9+3=1+2=3
    9+6=1+5=6

    0.125
    hmm  if I minus 2 from 5
    11.123
    0.333
    11.222

CLEANED AND CHECKED:
  248 → 24 42 48 84 (each neighbour pair, then the same pair read back)                         right
  Conway out loud: 44 2222 1111|1111 → two 4s, four 2s, eight 1s → 24 42 81 → 244281            right
    (each count times its digit is 8: 2x4 = 4x2 = 8x1 = 8)
  2|8|1 read as: divide by 2, start at 8, end at 1 → 8 ÷ 2 = 4 → ÷ 2 = 2 → ÷ 2 = 1                right
  9 + 3 = 12 → 1 + 2 = 3 ; 9 + 6 = 15 → 1 + 5 = 6                                              right (adding 9 never changes the root)
  0.125 = 1 ÷ 2 ÷ 2 ÷ 2 (the three twos of #368: 9 ÷ 8 = 1.125 = 1 + 0.125)
  minus 2 from the 5: 0.125 − 0.002 = 0.123                                                    right
  11.123, 0.333, 11.222: the step that leads to them is missing (asked). What the numbers show:
    1+1+1+2+3 = 8 and 1+1+2+2+2 = 8 (11.123 and 11.222 both add to 8) ; 0.333 → 3+3+3 = 9
    .123 → .222: one moved from the 3 to the 1, the sum stays 6 (1+3 = 2+2, the owner's a+c = 2b)
    11.222 − 11.123 = 0.099 ; .123 + .333 = .456, the next row of 123 456 789
FRAMEWORKS (gf37-audit): 24 SEED, 42 = 5 CAS_EXT, 48 = 11 NEG_H, 84 = 10 IC, 244281 = 7 D7, 125 = 14 C9, 123 = 12 SA_ST_A, 11123 = 7x7x227 = 23 TESLA,
  333 = 9x37 = 0, 11222 = 2x31x181 = 11 NEG_H.

#376 (2026-10-20), the owner explains the last step (verbatim excerpts): "I started with a 5 at the end. And I took minus 2 from that 5. That's how I
  got the 1-1. ... I could have just put 2 right there. And it would have been 2, 1, 2, 3. But I decided to put a 1 and a 1 there. ... I might have
  messed up on the 333 ... The 333 is not in there. ... So it's 11123 11222. Because I could just minus 1 from the 3. And give it to the 1 in the
  front, and that's how I get the 222. Now, I can also have 323. ... But that's the best it's going to get."
  Cleaned: 0.125 → take 2 from the 5 → 0.123, and put the 2 in front: as 2 → 2.123, or as 1 1 → 11.123 ;
           11.123 → take 1 from the 3, give it to the 1 in front of it → 11.222 ;
           or give the 2 to the first digit → 0.323 ;
           0.333 is out (the owner's correction).
  Checked: every one keeps the 8 of 0.125: 1+2+5 = 8, 2+1+2+3 = 8, 1+1+1+2+3 = 8, 1+1+2+2+2 = 8, 3+2+3 = 8.        right
  The digits move, the 8 stays; the value changes (0.125, 2.123, 11.123, 11.222, 0.323 are five different numbers).
  Frameworks: 2123 = 11x193 = 14 C9 ; 323 = 17x19 (17 and 19 are twin primes) = 27 NEG_H ; 125 = 5x5x5 = 14 C9.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as Q

from sympy import factorint

assert [24, 42, 48, 84] == [int(f"{a}{b}") for a, b in ((2, 4), (4, 2), (4, 8), (8, 4))] and int(str(24)[::-1]) == 42 and int(str(48)[::-1]) == 84


def look_and_say(s):
    out, i = "", 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out += str(j - i) + s[i]
        i = j
    return out


assert look_and_say("44" + "2222" + "1111" + "1111") == "244281" and 2 * 4 == 4 * 2 == 8 * 1 == 8
assert Q(8) / 2 / 2 / 2 == 1 and [Q(8) / 2, Q(8) / 4] == [4, 2]
assert 9 + 3 == 12 and 1 + 2 == 3 and 9 + 6 == 15 and 1 + 5 == 6
dr = lambda n: 0 if n == 0 else 1 + (n - 1) % 9
assert all(dr(9 + n) == dr(n) for n in range(1, 1000))
assert Q(1) / 2 / 2 / 2 == Q(125, 1000) and Q(9, 8) == 1 + Q(125, 1000)
assert Q(125, 1000) - Q(2, 1000) == Q(123, 1000)
assert sum(map(int, "11123")) == 8 == sum(map(int, "11222")) and sum(map(int, "333")) == 9 and 1 + 2 + 3 == 2 + 2 + 2 == 6 and 1 + 3 == 2 + 2
assert Q(11222, 1000) - Q(11123, 1000) == Q(99, 1000) and 123 + 333 == 456 and 456 + 333 == 789
assert [n % 37 for n in (24, 42, 48, 84, 244281, 125, 123, 11123, 333, 11222)] == [24, 5, 11, 10, 7, 14, 12, 23, 0, 11]
assert factorint(11123) == {7: 2, 227: 1} and factorint(11222) == {2: 1, 31: 1, 181: 1} and 333 == 9 * 37

# #376: move units between places, the 8 stays
forms = ["0125", "2123", "11123", "11222", "0323"]
assert all(sum(map(int, f)) == 8 for f in forms) and sum(map(int, "333")) == 9
assert len({Q(int(f), 1000) for f in forms}) == 5
assert (5 - 2, 3 - 1, 1 + 1) == (3, 2, 2) and 1 + 1 == 2 and 2 + 1 == 3
assert factorint(2123) == {11: 1, 193: 1} and factorint(323) == {17: 1, 19: 1} and (2123 % 37, 323 % 37, 125 % 37) == (14, 27, 14)

if __name__ == "__main__":
    print("#375: 248 -> 24 42 48 84 ; Conway 244281 ; 8/2/2/2 = 1 ; 9+3 -> 3, 9+6 -> 6 ; 0.125 - 0.002 = 0.123 ; 11.123 / 0.333 / 11.222: step missing")

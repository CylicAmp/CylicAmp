# CLASS: AUDIT
"""
Odd and even, the doubling in rows of 3, and 181 (owner_work #270, 2026-10-13).

THE OWNER'S LINES, verbatim:
    It may boil down to this

    1+1=2(odd+odd=( thats even)
    2+3=5(even,odd=(mix uneven)
    3+4=7(3.5+3.5=16÷2=(8+8)

    2+3 even /odd
    3+4 odd /even

    8=44,222,211,111,111=
    8=44,222,211,111,111=

    Here we have Below
    OEO
    123
    246
    not doubled at 3

    Below we have
    EEE=Doubling SETS OF 3
    248+  5
    510=+6+5=(1+1=2)
    758+20=2

    DOUBLE EVEN BY 4
    1248
    751

    NOTICE AT THE 7 NUMBER I GET MY SECOND 1

    BECAUSE

    0=(o=1)
    00=eo~~(2+3+1)=(5+1=6)
    0=e=(4=(1+3)or(3+1=4)
    00=oe(5
    0+(o=7)

    124|8
    751|4+8=(1+2=3 at 4×2=8)

    because if not by sets of 4

    124
    875
    1

    see that 181? firsr row up or down

    which is

    18+1=1+9=1
    1+18=1+9=1+1=2)0

    my build out of 181
    55=equal odds compress
    because 10÷2=5

    1÷2=0.5+0.5=1.


EVERY LINE CHECKED HOLDS. Where a line's meaning is not settled by the lines, it says so.

ODD AND EVEN
  1+1 = 2: odd + odd is even.  2+3 = 5: even + odd is odd ("mix uneven").  2+3 is even/odd, 3+4 odd/even.
  3+4 = 7 halved is 3.5 + 3.5; the digits 3+5+3+5 = 16, 16/2 = 8, 8+8 = 16.

8 = 44,222,211,111,111 -- the halving string of #263 (8 = 44|2222|11111111) written with commas:
  14 digits (2+4+8), four commas, digit sum 24 (4+4 + 2+2+2+2 + eight 1s = 8+8+8), root 6.
  The comma groups 44|222|211|111|111 cut the 2222 block (222,2) -- the commas and the halving
  blocks do not line up.

OEO and EEE
  123 is odd, even, odd; 246 = 2 x 123 (246 is the repo's reference seed). "not doubled at 3":
  1 -> 2 doubles, 2 -> 3 does not; 2 -> 4 doubles, 4 -> 6 does not. 248 is even, even, even, each
  the double of the one before.
  248 + 510 = 758. 248 -> 14 -> 5; 510 -> 6; 5+6 = 11 -> 1+1 = 2; 758 -> 7+5+8 = 20 -> 2. Both 2
  (digital roots add). Where 510 comes from is not settled by the lines.

THE DOUBLING, "NOTICE AT THE 7 NUMBER I GET MY SECOND 1"
  1, 2, 4, 8, 16, 32, 64 have roots 1, 2, 4, 8, 7, 5, 1 -- written 1248 / 751. The 7th is the
  second 1: 64 -> 10 -> 1. Forced: 2^6 = 64 = 1 (mod 9), so the roots repeat every 6.
  The BECAUSE lines mark the seven places o, e o, e, o e, o (0 | 00 | 0 | 00 | 0): odd places
  1, 3, 5, 7 and even places 2, 4, 6; the 7th place is odd like the 1st. (2+3+1) = (5+1 = 6) is
  2+3 = 5 with the +1 of #264; 4 = 1+3 or 3+1 are the comma splits of #267.
  124|8 / 751|4+8 = (1+2 = 3 at 4x2 = 8): 4+8 = 12 -> 3 and 4x2 = 8 hold; which 4 and 8 are
  meant, and what "at" ties, is not settled by the lines.

ROWS OF 3 AND 181
  The roots in rows of 3:  1 2 4 / 8 7 5 / 1.  The first column read down (or up) is 1, 8, 1 = 181.
  124 + 875 = 999: each root plus the one three places later is 9 (1+8, 2+7, 4+5) because
  2^3 = 8 = -1 (mod 9). So column 1 runs 1, 8, 1, 8, ... for ever, column 2 runs 2, 7, 2, 7, ...,
  column 3 runs 4, 5, 4, 5, ... -- forced by the same fact.
  18+1 = 19, 1+9 = 10 -> 1; 1+18 = 19, 1+9 = 10. "=1+1=2)0": 10 is 1 and 0; the 1 plus the +1 of
  #264 is 2 -- one reading; the ")0" is not settled.
  181: 1+8+1 = 10, 10/2 = 5, 5 and 5 = 55 ("equal odds compress"); 1/2 = 0.5, 0.5+0.5 = 1.
  The halves run through the message: 7 -> 3.5+3.5, 10 -> 5+5, 1 -> 0.5+0.5.

FRAMEWORKS (#270): 16 SA_ST_A; 35 NQR17; 55 SEED; 124 = 2^2 x 31 CAS_EXT; 181 D7, prime, twin
  (179, 181), not Sophie Germain (363); 246 SEED; 248 IC; 510 C9; 751 NEG_H, prime, not twin;
  758 SEED; 875 = 5^3 x 7 SEED; 999 = 27 x 37 SEAM; 1248 NEG_H; 44222211111111 D7.
  179, the twin of 181, is a factor of #269's 112233 = 3 x 11 x 19 x 179 -- recorded, not claimed.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


assert (1 + 1) % 2 == 0 and (2 + 3) % 2 == 1 and 3 + 4 == 7 and 3.5 + 3.5 == 7
assert 3 + 5 + 3 + 5 == 16 and 16 // 2 == 8 and 8 + 8 == 16
s = "44222211111111"
assert s == "44" + "2222" + "1" * 8 and f"{int(s):,}" == "44,222,211,111,111"
assert len(s) == 14 and sum(map(int, s)) == 24 and dr(int(s)) == 6 and f"{int(s):,}".count(",") == 4
assert [int(c) % 2 for c in "123"] == [1, 0, 1] and 246 == 2 * 123 and all(int(c) % 2 == 0 for c in "248")
assert 2 * 1 == 2 and 2 * 2 != 3 and 2 * 2 == 4 and 2 * 4 != 6 and 2 * 2 == 4 and 2 * 4 == 8
assert 248 + 510 == 758 and (dr(248), dr(510), dr(758)) == (5, 6, 2) and 5 + 6 == 11 and 7 + 5 + 8 == 20
roots = [dr(2 ** k) for k in range(7)]
assert roots == [1, 2, 4, 8, 7, 5, 1] and 2 ** 6 == 64 and pow(2, 6, 9) == 1 and roots[6] == 1
places = "o" + "eo" + "e" + "oe" + "o"
assert len(places) == 7 and all((c == "o") == (i % 2 == 1) for i, c in enumerate(places, 1))
assert 2 + 3 + 1 == 6 and 1 + 3 == 3 + 1 == 4 and 4 + 8 == 12 and 1 + 2 == 3 and 4 * 2 == 8
rows = [roots[0:3], roots[3:6], roots[6:]]
assert rows == [[1, 2, 4], [8, 7, 5], [1]] and int("".join(str(r[0]) for r in rows)) == 181
assert 124 + 875 == 999 == 27 * 37 and pow(2, 3, 9) == 8 == 9 - 1
assert all(dr(2 ** k) + dr(2 ** (k + 3)) == 9 for k in range(60))
assert 18 + 1 == 1 + 18 == 19 and 1 + 9 == 10 and dr(19) == 1
assert 1 + 8 + 1 == 10 and 10 / 2 == 5 and 1 / 2 == 0.5 and 0.5 + 0.5 == 1
assert isprime(181) and isprime(179) and not isprime(363) and isprime(751) and not isprime(749) and not isprime(753)
assert factorint(124) == {2: 2, 31: 1} and factorint(875) == {5: 3, 7: 1} and factorint(112233)[179] == 1
assert [n % 37 for n in (124, 181, 246, 248, 510, 751, 758, 875, 999, 1248)] == [13, 33, 24, 26, 29, 11, 18, 24, 0, 27]

if __name__ == "__main__":
    print("#270 holds: doubling roots 1 2 4 8 7 5 1 (7th is the second 1); rows of 3 give 181 down column 1;")
    print("124 + 875 = 999 because 2^3 = -1 (mod 9); 248 + 510 = 758, roots 5 + 6 -> 2")

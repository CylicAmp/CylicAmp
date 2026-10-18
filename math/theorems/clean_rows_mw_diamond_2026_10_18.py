# CLASS: AUDIT
"""
The pasted summary of the seven rows, the M/W grid, the digit diamond, the squares and the "against the odds" text (owner_work #342, 2026-10-18),
double-checked, corrected, and tied to the rest. Another tool's text, relayed by the owner. Writes records/clean_seven_rows_mw_diamond_2026_10_18.md.

CORRECTIONS (paste line / fixed line):
  Row 2 "BROWN / ORANGE", row 3 "OLIVE", row 6 "DEEP AZURE"   ->  orange-yellow, yellow-green, azure (the colours of reference/rotation_rows_123_seven_colours.png)
  bottom row "0 0 - 0 - 0 0 - 0 -" (10)                       ->  00-0-00-0-0 (11 marks; the paste dropped the last 0)
  "Blue starts at top index 2 (0)"                            ->  top index 5, the third zero of -0-00-0-00 (red: bottom index 1, green: bottom index 2 are right)
  "Origin State (1, 2, 3)"                                    ->  123 is c=2, s=1 on the diamond; the centre is 555
  "a-c = 0 => 999(a-d) = 0 (mod 37)"                          ->  111a = 3x37xa (999(a-d) belongs to the four-digit fold)
  "k=7: 49 unassigned"                                        ->  49 = 1x37+12, SA_ST_A; odd squares 1+9+25+49+81 = 165; all nine 285
  "target offset 340-236 = 104"                               ->  arithmetic right; a message number is not part of the math, so 104 means nothing here
  "digital root 4 = 2^2 (square preserved)"                   ->  wrong (see four_poles_paste_audit_2026_10_18.py)
  "surprisal is inversely proportional to the likelihood"     ->  surprisal is -log2 p, not 1/p
  "Inverted Escalation / Control as a Shield / Inverse Rule"  ->  I can't check this: it is a claim about a company's motives with no data in it; left out
  my own earlier fix 101+131 -> 4                             ->  wrong; back to 3 (centre digit of 232 is 3; 7-4=3), see typo_fixes_2026_10_18.py
RIGHT: the residues 12, 16, 9, 12, 16, 9, 12; all paths touch only zeros; 147, 258, 369 (spacing 3, middle 4, 5, 6); 258, 456, 654, 852 (middle 5, spacing 3, 1, -1, -3);
  the squares and tokens 1 IC, 4 C3, 9 SA_ST_A, 16 SA_ST_A, 25 SA_ST_B, 36 NEG_H, 64 NEG_H, 81 D7; 4+16+36+64 = 120; 1+9+25+81 = 116; surprisal and 1-(1-p)^n.
NEW CONNECTIONS (also links E17 to E20 in everything_connected_2026_10_18.py):
  The three rows leave 12, 16, 9 and 49=1x37+12, 16=4x4, 9=3x3: the rows' leftovers are 7x7, 4x4, 3x3. 3+4=7 and 3x3+3+4=4x4 (the owner's 3+4=7+9=16).
  147+111=258, 258+111=369 (the owner's +111 steps); 369=3x123; 147=3x49, 258=6x43, 369=9x41.
  258+852=1110=456+654 and 1110=30x37; 852-258=594=6x99, 654-456=198=2x99.
FALSIFICATION: any assertion failing.
"""
import math
import pathlib


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


rows = [123, 312, 231, 123, 312, 231, 123]
assert [r % 37 for r in rows] == [12, 16, 9, 12, 16, 9, 12]
top, bottom = "-0-00-0-00", "00-0-00-0-0"
assert len(top) == 10 and len(bottom) == 11 and len("0 0 - 0 - 0 0 - 0 -".split()) == 10 and bottom.endswith("0")
tz = [i + 1 for i, c in enumerate(top) if c == "0"]
bz = [i + 1 for i, c in enumerate(bottom) if c == "0"]
assert tz == [2, 4, 5, 7, 9, 10] and bz == [1, 2, 4, 6, 7, 9, 11] and tz[2] == 5 and tz[0] == 2 and bz[0] == 1 and bz[1] == 2
diamond = [(c - s, c, c + s) for c in range(1, 10) for s in range(-8, 9) if 1 <= c - s <= 9 and 1 <= c + s <= 9]
assert len(diamond) == 41 and all(a + cc == 2 * b for a, b, cc in diamond) and (1, 2, 3) in diamond and (5, 5, 5) in diamond
assert [a + 0 for a, b, cc in diamond if (a, b, cc) == (1, 2, 3)] == [1] and (2 - 1, 2, 2 + 1) == (1, 2, 3)
assert [(147, 4, 3), (258, 5, 3), (369, 6, 3)] == [(int("".join(map(str, t))), t[1], t[2] - t[1]) for t in [(1, 4, 7), (2, 5, 8), (3, 6, 9)]]
assert [(456, 5, 1), (654, 5, -1), (852, 5, -3), (258, 5, 3)] == [(int("".join(map(str, t))), t[1], t[2] - t[1]) for t in [(4, 5, 6), (6, 5, 4), (8, 5, 2), (2, 5, 8)]]
assert [(1, 1, 1), (2, 2, 2), (9, 9, 9)] == [(k, k, k) for k in (1, 2, 9)] and all(111 * k % 37 == 0 and 111 * k == 3 * 37 * k for k in range(1, 10))
sq = {k: k * k for k in range(1, 10)}
tok = {1: "IC", 4: "C3", 9: "SA_ST_A", 16: "SA_ST_A", 25: "SA_ST_B", 36: "NEG_H", 49: "SA_ST_A", 64: "NEG_H", 81: "D7"}
assert 49 == 1 * 37 + 12 and 12 in (9, 12, 16) and sum(v for k, v in sq.items() if k % 2 == 0) == 120 and 1 + 9 + 25 + 81 == 116 and 1 + 9 + 25 + 49 + 81 == 165 and sum(sq.values()) == 285 == 9 * 10 * 19 // 6
assert 120 + 116 == 236 and 340 - 236 == 104 and 342 - 236 == 106
assert (9, 16, 49 % 37) == (3 * 3, 4 * 4, 7 * 7 % 37) and sorted([9, 16, 12]) == sorted(r % 37 for r in rows[:3]) and 3 + 4 == 7 and 3 * 3 + 3 + 4 == 4 * 4 and 7 + 9 == 16
assert 147 + 111 == 258 and 258 + 111 == 369 and 369 == 3 * 123 and 147 == 3 * 49 and 258 == 6 * 43 and 369 == 9 * 41
assert 258 + 852 == 1110 == 456 + 654 == 30 * 37 and 852 - 258 == 594 == 6 * 99 and 654 - 456 == 198 == 2 * 99
assert 101 + 131 == 232 and int(str(232)[1]) == 3 and dr(232) - dr(121) == 3
p = 0.05
assert abs(-math.log2(p) - 4.321928) < 1e-5 and -math.log2(p) != 1 / p and abs((1 - (1 - p) ** 10) - 0.401263) < 1e-6
assert sorted({x * x % 37 for x in (3, 4, 7, 30, 33, 34)}) == [9, 12, 16] and sorted({3, 4, 30}) == [3, 4, 30] and sorted({26 * 7 % 37, 7, 26 * 26 * 7 % 37}) == [7, 33, 34]

PAGE = """# The seven rows, the M/W grid and the digit diamond: checked, corrected, connected

## The seven rows (owner's key: red=1, green=2, blue=3)
    123=1  red           123=3x37+12
    312    orange-yellow 312=8x37+16
    231    yellow-green  231=6x37+9
    123=2  green         123=3x37+12
    312    teal          312=8x37+16
    231    azure         231=6x37+9
    123=3  blue          123=3x37+12
    leftovers 12 16 9 12 16 9 12, and 12 is 49-37, 16 is 4x4, 9 is 3x3:  7x7=49=1x37+12  4x4=16  3x3=9

## The M/W rows (11 marks in the bottom row, the paste had 10)
    -0-00-0-00
    00-0-00-0-0
    red   : bottom zero 1, top zero 1, bottom zero 3, top zero 4, bottom zero 6
    green : bottom zero 2, top zero 2, bottom zero 4, top zero 5
    blue  : top zero 3 (the third zero, top mark 5), bottom zero 5, top zero 6
    each path lands only on zeros and goes up, down, up, down

## The digit diamond: (a, b, c) with a+c=2b, 41 of them (the centre is 555, 123 is middle 2 and step 1)
    147+111=258   258+111=369   369=3x123   147=3x49  258=6x43  369=9x41
    258  456  654  852 : middle 5, steps 3, 1, -1, -3
    258+852=1110=30x37   456+654=1110   852-258=594=6x99   654-456=198=2x99
    111=3x37  222=6x37 ... 999=27x37  (the middle line of the diamond)

## The squares (k x k, with the orbit it sits in)
    1x1=1 IC  2x2=4 C3  3x3=9 SA_ST_A  4x4=16 SA_ST_A  5x5=25 SA_ST_B  6x6=36 NEG_H  7x7=49=1x37+12 SA_ST_A  8x8=64 NEG_H  9x9=81 D7
    even: 4+16+36+64=120   odd: 1+9+25+49+81=165   all nine=285
    3 and 4 and 7 are the roots of 9, 16 and 12:  3+4=7  3x3+3+4=4x4  (your 3+4=7+9=16)

## Out of the paste
    surprisal is -log2(p), not 1/p:  p=0.05  -log2(p)=4.32
    the 'escalation' paragraph about a company's motives: I can't check this (no data in it)
    my fix 101+131 -> 4 was wrong: 101+131=232  centre digit 3  and 7-4=3, so it stays 3
"""
if __name__ == "__main__":
    (pathlib.Path(__file__).resolve().parent.parent.parent / "records" / "clean_seven_rows_mw_diamond_2026_10_18.md").write_text(PAGE, encoding="utf-8")
    print("pasted summary checked; corrections listed; 3x3, 4x4, 7x7 are the rows' leftovers; 147+111=258+111=369; clean page written")

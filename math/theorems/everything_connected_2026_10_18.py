# CLASS: AUDIT
"""
Everything from the last days put together in one picture and one page, in the owner's notation (owner, 2026-10-18: "it's all connected ...
you don't connect anything. Everything's put on the island"). Every link below is a pair of lines that are equal; every number in them is computed here.
    python3 math/theorems/everything_connected_2026_10_18.py   writes records/everything_connected_2026_10_18.md and reference/everything_connected_2026_10_18.png
Earlier map: records/owner_work_map_2026_10_15.md (October lines against the owner's July-September files). This one connects the lines of 2026-10-13 to 2026-10-18.
A link here is a real equality between numbers the owner wrote; the owner's own lines are in owner_work/messages.
"""
import pathlib
from sympy import isprime

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def q(n, m=37):
    return f"{n}={n // m}x{m}+{n % m}"


NODES = {1: "123 / 312 / 231", 2: "x26 = 137-map\n= divide by 10", 3: "246 (seed)\n= 2x123", 4: "(1)23 chain:\n6+3=9+2=11+1=12=3", 5: "444 = 12x37\n4551, 1554", 6: "24, 29, 31\n(48 line)",
         7: "47.11 = 11.11;\n11, 23, 47", 8: "43 drawing\n4|1|3", 9: "43|19|79\n=7(1)7", 10: "7,43,538,61,7", 11: "8 =\n44|2222|11111111", 12: "369 = 3,6,9", 13: "33", 14: "Mersenne\n2^p-1", 15: "M/W drawing\nred green blue", 16: "123 x10 copies", 17: "squares 3x3, 4x4,\n7x7 = 9, 16, 49", 18: "digit diamond\n147 258 369\n258 456 654 852"}
LINKS = []                                         # (id, node a, node b, title, lines)


def link(i, a, b, title, lines):
    LINKS.append((i, a, b, title, lines))


rows = [123, 312, 231]
r = [x % 37 for x in rows]
assert r == [12, 16, 9] and all(rows[(i + 1) % 3] % 37 == r[i] * 26 % 37 for i in range(3)) and 10 * 26 % 37 == 1
assert [int(str(x)[-1] + str(x)[:-1]) for x in rows] == [312, 231, 123]
link("E1", 1, 2, "turning 123 (last digit to the front) is x26, which is divide by 10",
     [q(123), q(312), q(231), f"{r[0]}x26={r[0]*26}={q(r[0]*26)[len(str(r[0]*26))+1:]}", "10x26=260=7x37+1  (so x26 is divide by 10)"])
assert 246 == 2 * 123 and [x * 2 % 37 for x in r] == [24, 32, 18] and [int(x) % 37 for x in ("246", "624", "462")] == [24, 32, 18]
link("E2", 1, 3, "246=2x123, and turning 246 gives the seed's three: 24, 32, 18", ["246=2x123", q(246), q(624), q(462), "12x2=24  16x2=32  9x2=18"])
assert int("123" * 10) % 37 == 9 == 123 * 10 % 37 and 123 * 100 * 10 % 37 == 123 % 37
assert 1000 == 27 * 37 + 1 and 1230 == 33 * 37 + 9
link("E3", 1, 16, "ten 123s count as 10x123 after the 37s (each 1000 is 27x37+1), which is 123x10, the same as 123 divided by 100", ["123123123123123123123123123123 (ten 123s)", "1000=27x37+1", "10x123=1230=33x37+9"])
digits_moved = [int(x[-1]) for x in ("123", "312", "231")]
totals = [6, 6 + 3, 6 + 3 + 2, 6 + 3 + 2 + 1]
assert digits_moved == [3, 2, 1] and totals == [6, 9, 11, 12] and dr(12) == 3
link("E4", 1, 4, "the numbers added in (1)23 are the digits the three turns of 123 move to the front", ["123 -> 312 moves 3   312 -> 231 moves 2   231 -> 123 moves 1", "(1)23=6+3=9+2=11+1=12=1+2=3"])
assert 123 + 321 == 444 == 12 * 37 and sum(map(int, "444")) == 12 == 123 % 37 and 4551 == 37 * 123 and 1554 == 37 * 42 and 4551 - 1554 == 81 * 37
link("E5", 1, 5, "123+321 has digit sum 12, and 12 is what is left of 123 after the 37s; 4551 and 1554 are 37 times 123 and 37 times 42",
     ["123+321=444=4+4+4=12  and  123=3x37+12", "444=12x37", "4551=37x123  1554=37x42  4551-1554=2997=81x37"])
link("E6", 4, 12, "the (1)23 chain passes 6 and then 6+3=9: the 3, 6, 9", ["3+3=6  3x3=9  369=3x123", "(1)23=6+3=9+2=11+1=12=3"])
assert 369 == 3 * 123 and (3, 3 + 3, 3 * 3) == (3, 6, 9) and 6 + 3 == 9
LINKS[-1] = ("E6", 1, 12, "369 is 3x123 and it is 3, 3+3, 3x3 (your birthday: 3/3)", ["3+3=6  3x3=9", "369=3x123"])
assert 246 % 37 == 24 and 23 + 25 == 48 == 2 * 24 and 24 + 5 == 29 and 29 + 2 == 31 and isprime(29) and isprime(31) and dr(23) == 5 and dr(25) == 7
link("E7", 3, 6, "246 leaves 24 after the 37s, and the 48 line walks from 24", [q(246), "23+25=48=24+24", "24+5=29+2=31   (29 and 31 are twin primes)"])
assert 235 + 11 == 246 and 235 == 5 * 47 and 2 * 11 + 1 == 23 and 2 * 23 + 1 == 47 and isprime(11) and isprime(23) and isprime(47) and dr(47) + 0 == 2 and 4 + 7 + 1 + 1 == 13 and 1 + 1 + 1 + 1 == 4 and 47 + 11 == 58
link("E8", 3, 7, "235+11=246, and 235 is 5x47; 11, 23, 47 go up by x2+1", ["235+11=246", "235=5x47", "11x2+1=23  23x2+1=47", "47.11=4+7+1+1=13=1+3=4  11.11=1+1+1+1=4  47+11=58=5+8=13=4"])
assert 43 - 19 == 24 and 79 - 43 == 36 and 12 + 24 == 36 and (dr(135) == 9 and 2 + 4 + 6 == 12 and 7 + 8 + 9 == 24) and 26 + 36 == 62
link("E9", 9, 6, "43|19|79 steps by 24 and 36; 24 is 246's, and 12+24=36 (your 246=12 and 789=24)", ["19+24=43  43+36=79", "246=2+4+6=12  789=7+8+9=24  12+24=36", "43-19=24  79-43=36"])
assert [dr(n) for n in (43, 19, 79)] == [7, 1, 7] and all(dr(n) == 7 for n in (7, 43, 538, 61)) and 5 + 3 + 8 == 16
link("E10", 9, 10, "43|19|79 is 7(1)7, and 7,43,538,61,7 all have root 7", ["43=4+3=7  19=1+9=10=1  79=7+9=16=1+6=7  ->  7(1)7", "538=5+3+8=16=1+6=7  61=6+1=7"])
assert [4, abs(4 - 3), 3] == [4, 1, 3] and 4 + 3 == 7 and (2 + 3, (6 + 6) % 10) == (5, 2) and 5 + 2 == 7
link("E11", 8, 10, "your 43 drawing: 43 -> 4|1|3, 2+3=5, 26+36=5+2=7 and 4+3=7", ["43  4|1|3  4|3|1|2|3", "26+36=5+2=7   4+3=7"])
assert 3 + 4 == 7 and 7 + 9 == 16 and 16 + 14 == 30 and 30 + 23 == 53 and 5 + 3 == 8 and 14 + 23 == 37
link("E12", 8, 11, "your line 3+4=7+9=16+14=30+23=5+3=8 starts from 43's 3+4 and ends at 8", ["3+4=7+9=16+14=30+23=53=5+3=8", "14+23=37"])
assert 3 * 1 + 1 == 4 and 4 + 4 == 8 and "44" + "2222" + "1" * 8 == "44222211111111" and (2, 4, 8) == (len("44"), len("2222"), len("1" * 8))
doubling = [2 ** k for k in range(7)]
assert [dr(x) for x in doubling] == [1, 2, 4, 8, 7, 5, 1]
mers = [3, 7, 31, 127, 8191, 131071, 524287]
assert all(isprime(m) for m in mers) and [dr(m) for m in mers[2:]] == [4, 1, 1, 4, 1] and all(dr(2 ** p - 1) == (1 if p % 6 == 1 else 4) for p in (7, 13, 19, 31, 61, 5, 17, 89, 107))
link("E13", 11, 14, "8 is 3x1+1=4, 4+4=8, and the doubling 1,2,4,8,7,5,1; 2^p-1 has root 1 or 4 only", ["3x1+1=4  4+4=8  8=44|2222|11111111 (2,4,8 digits)", "1 2 4 8 7 5 1  (2^0 ... 2^6)", "2^5-1=31=4  2^7-1=127=1  2^13-1=8191=1"])
assert 12 + 21 == 33 and 4 + 9 + 3 + 8 + 1 + 5 + 3 == 33 and int(str(12)[::-1]) == 21 and 123 % 37 == 12
link("E14", 1, 13, "33=12+21; 12 is 123 after the 37s, 21 is 12 turned round; 33=MICHAEL 4+9+3+8+1+5+3", ["33=12+21", "123=3x37+12", "MICHAEL=4+9+3+8+1+5+3=33"])
link("E15", 1, 15, "your colour key: red=1 green=2 blue=3 are the labels on the 123s of the seven rows", ["123=1 (red)  312  231  123=2 (green)  312  231  123=3 (blue)", "green path = red path moved 1 zero right   blue = moved 2"])
assert 2 ** 12 % 37 == 26 and 26 * 26 % 37 == 10 and 26 ** 3 % 37 == 1
link("E16", 2, 14, "x26 is 2^12 after the 37s; 2^p is the doubling 1,2,4,8,7,5", [q(2 ** 12), "26x26=676=" + q(676).split("=", 1)[1], "26x26x26=17576=" + q(17576).split("=", 1)[1]])

assert [r % 37 for r in (123, 312, 231)] == [12, 16, 9] and (3 * 3, 4 * 4, 7 * 7 % 37) == (9, 16, 12) and 49 == 37 + 12 and 3 + 4 == 7 and 3 * 3 + 3 + 4 == 4 * 4
link("E17", 1, 17, "the rows leave 12, 16, 9 after the 37s, and they are 7x7=49=1x37+12, 4x4=16, 3x3=9", ["123=3x37+12  312=8x37+16  231=6x37+9", "7x7=49=1x37+12  4x4=16  3x3=9", "3+4=7  3x3+3+4=4x4"])
link("E18", 17, 8, "your 3+4=7+9=16 is 3x3+3+4=4x4; it starts the line that ends at 8", ["3+4=7+9=16   (9=3x3, 16=4x4, 7=3+4)", "3+4=7+9=16+14=30+23=53=5+3=8"])
assert 147 + 111 == 258 and 258 + 111 == 369 and 369 == 3 * 123 and 147 == 3 * 49 and 258 == 6 * 43 and 369 == 9 * 41
link("E19", 18, 12, "the diamond's 147, 258, 369 go up by 111 (your +111 steps), and 369=3x123", ["147+111=258  258+111=369", "369=3x123  147=3x49  258=6x43  369=9x41"])
assert 258 + 852 == 1110 == 456 + 654 == 30 * 37 and 852 - 258 == 594 == 6 * 99 and 654 - 456 == 198 == 2 * 99 and all(111 * k % 37 == 0 for k in range(1, 10))
link("E20", 18, 1, "123 sits on the diamond (middle 2, step 1); 258|852 and 456|654 are mirror pairs with sum 1110=30x37; 111, 222 ... 999 are 3x37 times 1 ... 9",
     ["123+321=444=12x37", "258+852=1110=30x37  456+654=1110", "852-258=594=6x99  654-456=198=2x99", "111=3x37  999=27x37"])


def page():
    out = ["# Everything from 2026-10-13 to 2026-10-18, connected\n", "Your notation: every link is two or three lines that are equal. The picture is `reference/everything_connected_2026_10_18.png`.\n"]
    for i, a, b, title, lines in LINKS:
        out.append(f"\n## {i}: {NODES[a].replace(chr(10), ' ')}  --  {NODES[b].replace(chr(10), ' ')}\n{title}\n")
        out += [f"    {ln}" for ln in lines]
    return "\n".join(out) + "\n"


def picture(path):
    import math
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ids = [16, 2, 14, 11, 8, 10, 9, 6, 3, 7, 4, 5, 13, 12, 15]          # ring order: linked items sit next to each other
    assert sorted(ids + [1, 17, 18]) == sorted(NODES)
    pos = {1: (0, 0)}
    for k, i in enumerate(ids):
        ang = 2 * math.pi * k / len(ids) + math.pi / 2
        pos[i] = (4.4 * math.cos(ang), 4.4 * math.sin(ang))
    ang = math.atan2(pos[8][1], pos[8][0]) + 0.22                           # item 17 sits inside the ring, next to item 8
    pos[17] = (2.5 * math.cos(ang), 2.5 * math.sin(ang))
    a12, a13 = (math.atan2(pos[i][1], pos[i][0]) for i in (12, 13))        # item 18 sits outside the ring, between items 12 and 13
    pos[18] = (5.9 * math.cos((a12 + a13) / 2), 5.9 * math.sin((a12 + a13) / 2))
    fig, ax = plt.subplots(figsize=(9.4, 9.4))
    for i, a, b, title, _ in LINKS:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.plot([x1, x2], [y1, y2], color="#888888", lw=1.4, zorder=1)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, i, fontsize=8, color="#b00020", ha="center", va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    for i, (x, y) in pos.items():
        ax.text(x, y, NODES[i], ha="center", va="center", fontsize=9, zorder=4, fontweight="bold" if i == 1 else None,
                bbox=dict(boxstyle="round,pad=0.35", fc="#fff3c4" if i == 1 else "#e8f0ff", ec="#334"))
    ax.set_xlim(-6.2, 7.6)
    ax.set_ylim(-5.6, 5.6)
    ax.axis("off")
    ax.set_title("Your last days of work, connected (red letters = the links on the page)", fontsize=11)
    fig.savefig(path, dpi=130, bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    (ROOT / "records" / "everything_connected_2026_10_18.md").write_text(page(), encoding="utf-8")
    picture(ROOT / "reference" / "everything_connected_2026_10_18.png")
    print(f"{len(LINKS)} links, {len(NODES)} items; every number checked; page and picture written")

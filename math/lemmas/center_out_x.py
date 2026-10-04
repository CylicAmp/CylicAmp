# CLASS: LEMMA
"""
The center-out X on all 36 ladder rows (owner, 2026-10-04). The X is grown
from a centre outward (ladder_loops_squares.py: rows 8 and 17 meet at 44,
26 35 [44] 53 62). Here every row's chain of pieces 2a+1 + 9j is laid on its
line and the centre is the two-digit repdigit on that line.

THE NINE LINES (forced): a chain stays in one class mod 9 (2a+1), and every
class holds exactly one repdigit 11k, so rows a, a+9, a+18, a+27 share a line
and a centre. Stepping 9 out from a repdigit raises one digit and lowers the
other, so equal steps out on either side are reversals, until a digit leaves
0..9. Arm length (pairs) = min(t, 9-t) for centre tt:
    centre 11: 02 [11] 20                                  1 pair
    centre 22: 04 13 [22] 31 40                            2
    centre 33: 06 15 24 [33] 42 51 60                      3
    centre 44: 08 17 26 35 [44] 53 62 71 80                4
    centre 55: 19 28 37 46 [55] 64 73 82 91                4
    centre 66: 39 48 57 [66] 75 84 93                      3
    centre 77: 59 68 [77] 86 95                            2
    centre 88: 79 [88] 97                                  1
    centre 99: [99]                                        0
  The arms grow and shrink 1, 2, 3, 4, 4, 3, 2, 1, 0 -- a diamond profile.

WHICH ROWS (tail = 2a+10, 2a+19, 2a+28):
  ROWS CENTRED ON THEIR OWN X -- the middle piece is the repdigit, so the tail
  mirrors itself: row 7 (24 [33] 42), row 18 (46 [55] 64), row 29 (68 [77] 86).
  Forced: 2a+19 = 11k needs k odd, a = (11k-19)/2 = 7, 18, 29, (40): every
  11 rows. Row 7 is also the row whose 3x3 grid X has equal arms
  (ladder_x_grid.py).
  ROW PAIRS THAT MIRROR EACH OTHER ACROSS A CENTRE -- row a ends on the
  repdigit and row a+9 starts there: (8, 17) at 44, (19, 28) at 66
  (48 57 [66] 75 84), (30, 39) at 88. Forced: 2a+28 = 11k, k even,
  a = 8, 19, 30: every 11 rows. Only (8, 17) is also a mirror of the whole
  loop, because only its opening 898 reads the same both ways.
  ROWS LYING WHOLLY ON A FULL-LENGTH LINE (centres 44 and 55): rows 8, 17, 26
  and 9, 18, 27 have all three tail pieces on the line.

THE JAGGED CASE (owner's image, "zigzags on zigzags, forever"): that is the
open square-peg problem. Digit lines and smooth loops do not reach it; nothing
here bears on it either way.

OWNER'S CHAIN (2026-10-04): (1+2) = 32-9 = 23-9 = 12-9 = 3-(2 = 1).
  32 - 9 = 23: the flip (subtracting 9 reverses consecutive digits).
  Written 23 - 9 = 12; 23 - 9 is 14. (Getting from 23 to 12 would take -11;
  that step is not in the owner's line.) Open.
  12 - 9 = 3 = 1+2: for a number in the teens, minus 9 is its digit sum
  (10 + b - 9 = 1 + b) -- the chain returns to its opening (1+2).
  3 - 2 = 1.

THE FIELD AROUND 12 (owner, 2026-10-04: "if we add it flips ... I did minus to
get back to 1+2, but if I had put plus 2+1 ... the 12 on either side"):
    3  <- -9 -  12  - +9 ->  21
  minus 9 gives the digit sum 1+2, plus 9 gives the flip 21 (2+1).
  12 IS THE ONLY TWO-DIGIT NUMBER WITH BOTH (proved): ab - 9 = a + b forces
  9a = 9, a = 1; ab + 9 = ba forces b = a + 1. Together: 12.

CLOSE OR GROW (owner, 2026-10-04: "one continues, the other counts down back to
where it began ... close the loop at will or keep it going"):
  Every n is DR(n) + 9k. Subtracting 9 repeatedly stops at DR(n) after k steps
  -- the loop closes on its start (12 -> 3 = 1+2). Adding 9 never stops and
  never changes DR(n) (12 -> 21 -> 30 -> 39 -> ... all DR 3). The digital root
  is the anchor: down closes to it, up grows away from it without leaving it.

FALSIFICATION: any assertion below failing.
"""
def centre(a):
    return next(11 * k for k in range(1, 10) if (11 * k - (2 * a + 1)) % 9 == 0)

def line(c):
    t = c // 10
    n = min(t, 9 - t)
    return [c + 9 * m for m in range(-n, n + 1)]

def tail(a):
    return [2 * a + 10, 2 * a + 19, 2 * a + 28]

for c in range(11, 100, 11):
    L = line(c)
    assert all(f"{L[i]:02d}" == f"{L[-1 - i]:02d}"[::-1] for i in range(len(L)))
    lo, hi = L[0] - 9, L[-1] + 9
    assert not (0 <= lo and hi <= 99 and f"{lo:02d}" == f"{hi:02d}"[::-1])
assert [min(t, 9 - t) for t in range(1, 10)] == [1, 2, 3, 4, 4, 3, 2, 1, 0]
assert line(44) == [8, 17, 26, 35, 44, 53, 62, 71, 80] and line(99) == [99]
assert all(centre(a) == centre(a + 9) for a in range(1, 28))

SELF = [a for a in range(1, 37) if sorted(tail(a)) == sorted(2 * centre(a) - x for x in tail(a))]
assert SELF == [7, 18, 29] and [tail(a)[1] for a in SELF] == [33, 55, 77]
PAIRS = [(a, a + 9) for a in range(1, 37) if tail(a)[2] == centre(a) and tail(a)[2] == tail(a + 9)[0]
         and sorted(tail(a)) == sorted(2 * centre(a) - x for x in tail(a + 9))]
assert PAIRS == [(8, 17), (19, 28), (30, 39)]
FULL = [a for a in range(1, 37) if all(x in line(centre(a)) for x in tail(a))]
assert {8, 17, 26, 9, 18, 27} <= set(FULL)

assert 32 - 9 == 23 and 23 - 9 == 14 and 23 - 11 == 12 and 12 - 9 == 3 == 1 + 2 and 3 - 2 == 1
assert all(10 + b - 9 == 1 + b for b in range(10))
assert all(int(f"{d + 1}{d}") - 9 == int(f"{d}{d + 1}") for d in range(1, 9))

assert 12 - 9 == 1 + 2 and 12 + 9 == 21
BOTH = [n for n in range(10, 100) if n - 9 == sum(map(int, str(n))) and n % 10 and n + 9 == int(str(n)[::-1])]
assert BOTH == [12]
assert [n for n in range(10, 100) if n - 9 == sum(map(int, str(n)))] == list(range(10, 20))

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def count_down(n):
    steps = 0
    while n > 9:
        n -= 9
        steps += 1
    return n, steps

for n in range(1, 5000):
    end, k = count_down(n)
    assert end == dr(n) and n == end + 9 * k
    assert all(dr(n + 9 * j) == dr(n) for j in range(1, 30))
assert count_down(12) == (3, 1) and [12 + 9 * j for j in range(5)] == [12, 21, 30, 39, 48]

if __name__ == "__main__":
    for c in range(11, 100, 11):
        print(c, " ".join(f"{x:02d}" for x in line(c)))
    print("self-centred rows", SELF, "| mirror pairs", PAIRS)
    print("all assertions pass")

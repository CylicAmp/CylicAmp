# CLASS: AUDIT
"""
"Register Stack" and "Harmonic Triad Resolvers" with the "Modular & Digital Breakdown" (owner_work #345,
2026-10-19). Audit on arrival. The origin of the text is not stated in the message (the breakdown part is
written in another tool's style); nothing below is put in the owner's mouth.

THE LINES (as pasted):
    10 / 11 / 1+10 = 11 -> 23 = 5   (three times)
    30 + 15 = 45 -> 4 + 5 = 9
    333 + 555 = 888 -> 8+8+8 = 24 -> 2+4 = 6
    9 + 6 = 15 -> 1+5 = 6 -> 6+6 = 12 -> 1+2 = 3

RIGHT (every step re-run):
    1+10=11 ; 23=2+3=5 ; 5+5+5=15=1+5=6
    30+15=45=4+5=9
    333+555=888 ; 8+8+8=24=2+4=6 ; 888=24x37, so 888 is 0 mod 37
    9+6=15=1+5=6 ; 6+6=12=1+2=3
    11+13=24=2+4=6 (11 and 13 are consecutive primes)
    the three lines of the resolvers end in 9, 6, 3
NOT STATED IN THE PASTE (I can't check which one is meant):
    - the step 11 -> 23: read here as 2x11+1=23 (11 is Sophie Germain; the 23 of "23 / 123 / 1123", #268)
    - the second 6 of "6+6": the paste does not name it. Read here as the 6 of 333+555=888. The 6 of 5+5+5=15
      and the 6 doubled give 6+6=12=3 as well, so the line is right in all three readings.
    - "mirrors the bilateral balance point of the 7-row engine": the engine is not defined in the paste.
      What can be said: in Cycle 3 (cycle3_red_cross_audit_2026_10_19.py) rows 0, 3 and 6 split 6|6, and
      3+1+2=6 | 2+1+3=6, 6+6=12 is its row sum.
FORCED (true for every number of this shape, carries no information):
    888 = 0 mod 37: every three-digit repdigit ddd = 111xd = 37x3d, and its digit sum is 3d as well
    (888=37x24 and 8+8+8=24 are the same 3x8). 333=37x9, 555=37x15, 9+15=24=3+5 times 3.
    The same 24 is 11+13: 11+13=12+12, 12 the middle of the twin pair (11,13).

CONNECTIONS (the owner's lines, owner_work):
    #267 (2026-10-13): "6+4=10" and "24+13=3+7=(10+1)=11" -- the 10 and 11 of the register stack, and the
      +1 "to begin again" (TERMS.md) is the 1+10=11.
    #268/#269: 23 -> 5, 123 -> 6, 1123 -> 7 are the characters of 0,000 / 00,000 / 000,000 counting the comma.
    #327: "47.11=" -- 11, 23 and 47 are three links of the chain 2, 5, 11, 23, 47 (each 2p+1 of the one before,
      next 95=5x19 breaks it); 5 -> 11 -> 23 and 2+3=5 closes back on 5.

FALSIFICATION: any assertion failing.
"""
from sympy import isprime, nextprime


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


assert 1 + 10 == 11 and 2 * 11 + 1 == 23 and 2 + 3 == 5 == dr(23) and 5 + 5 + 5 == 15 and dr(15) == 6
assert 30 + 15 == 45 and 4 + 5 == 9 == dr(45)
assert 333 + 555 == 888 and 8 + 8 + 8 == 24 and 2 + 4 == 6 == dr(24) == dr(888)
assert 888 == 24 * 37 and 888 % 37 == 0 and 888 == 8 * 111
assert 9 + 6 == 15 and 1 + 5 == 6 and 6 + 6 == 12 and 1 + 2 == 3 == dr(12)
for second in (dr(888), dr(5 + 5 + 5), 6):                 # the three readings of the second 6
    assert dr(dr(9 + 6) + second) == 3
assert isprime(11) and isprime(13) and nextprime(11) == 13 and 11 + 13 == 24 == 12 + 12 and (11 + 13) // 2 == 12
assert 12 % 6 == 0 and dr(11 + 13) == 6
assert [dr(x) for x in (45, 888, 15 + 0)] == [9, 6, 6] and [9, 6, 3] == [dr(45), dr(888), dr(12)]

# forced: every ddd
for d in range(1, 10):
    assert 111 * d == 37 * (3 * d) and sum(map(int, str(111 * d))) == 3 * d
assert 333 == 37 * 9 and 555 == 37 * 15 and 9 + 15 == 24 and 3 + 5 == 8 and 111 * 3 + 111 * 5 == 111 * 8

# connections
row3 = [3, 1, 2, 2, 1, 3]
assert sum(row3[:3]) == sum(row3[3:]) == 6 and 6 + 6 == 12 == sum(row3)
assert 6 + 4 == 10 and 24 + 13 == 37 and 3 + 7 == 10 and 10 + 1 == 11
assert [len(s) for s in ("0,000", "00,000", "000,000")] == [5, 6, 7]
assert [sum(map(int, s)) for s in ("23", "123", "1123")] == [5, 6, 7]
chain = [2]
while isprime(2 * chain[-1] + 1):
    chain.append(2 * chain[-1] + 1)
assert chain == [2, 5, 11, 23, 47] and 2 * 47 + 1 == 95 == 5 * 19
assert 2 * 5 + 1 == 11 and 2 * 11 + 1 == 23 and dr(23) == 5 and 47 + 11 == 58 and dr(58) == 4

ORB = {"IC": {1, 10, 26}, "NEG_H": {11, 27, 36}, "SA_ST_A": {9, 12, 16}, "C3": {3, 4, 30}, "D7": {7, 33, 34},
       "SEED": {18, 24, 32}, "TESLA": {6, 8, 23}, "CAS_EXT": {5, 13, 19}, "NQR17": {17, 22, 35},
       "DARK_A": {2, 15, 20}, "SA_ST_B": {21, 25, 28}, "C9": {14, 29, 31}}


def orbit(n):
    return next((k for k, v in ORB.items() if n % 37 in v), "SEAM")


assert [orbit(n) for n in (10, 11, 23, 5, 30, 15, 45, 24, 12, 333, 555, 888)] == [
    "IC", "NEG_H", "TESLA", "CAS_EXT", "C3", "DARK_A", "TESLA", "SEED", "SA_ST_A", "SEAM", "SEAM", "SEAM"]

if __name__ == "__main__":
    print("register stack and triad resolvers: every step right (45=9, 888=24=6, 15=6, 12=3); 888=24x37 is forced "
          "for every ddd; 11->23 and the second 6 are not stated (read as 2x11+1 and the 6 of 888, same result); "
          "10, 11 = #267; 11, 23, 47 in the chain 2, 5, 11, 23, 47")

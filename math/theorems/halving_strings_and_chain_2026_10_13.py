# CLASS: AUDIT
"""
Halving strings and the 3+4 chain (owner_work #263, 2026-10-13).

THE OWNER'S LINES, verbatim:
    1=1
    2=11
    6=3322111
    8 =44222211111111
    
    6x2=(1+2=3)
    6+2=(8+12=20)
    3+4=7+9=16+14=30+23=5+3=8

THE HALVING STRINGS: each number is split in half, every part again, down to 1s, and each level
written out -- every level adds back to the number.
  2  -> 11
  8  -> 44 | 2222 | 11111111                  = 44222211111111  (exactly as written)
  6  -> 33 | 2211 | 111111 (3 = 2 + 1)        = 332211111111
       written 3322111: the first 7 digits of 332211111111, five 1s short. Open: confirm.
THE OTHER LINES -- all hold
  6x2 = 12 -> 1+2 = 3   (answers #262: "6+2=12" meant 6x2)
  6+2 = 8, and 8 + 12 = 20: the sum plus the product; 20 -> 2 (fits the first 2 of 2--3--7--2, #262)
  3+4 = 7, +9 = 16, +14 = 30, +23 = 53 -> 5+3 = 8.  14 + 23 = 37, so 16 and 53 share their residue
  (53 = 16 + 37 -> SA_ST_A {9, 12, 16}, with 9 itself).

FRAMEWORKS: 53 prime, Sophie Germain (107), -> 16 SA_ST_A; 23 prime, Sophie Germain (47), TESLA;
  3322111 = 13 x 421 x 607 -> 29 C9; 44222211111111 = 3 x 11 x 1340067003367 -> 33 D7;
  20 DARK_A; 30 C3; 14 C9; 16 and 9 SA_ST_A.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime


def halving(v):
    rows, row = [], [v]
    while any(x > 1 for x in row):
        row = [p for x in row for p in ((x // 2, x - x // 2) if x > 1 else (x,))]
        rows.append(sorted(row, reverse=True))
    return rows


def as_string(v):
    return "".join("".join(map(str, r)) for r in halving(v))


assert as_string(2) == "11" and as_string(8) == "44222211111111" and as_string(6) == "332211111111"
assert all(sum(r) == v for v in (2, 6, 8) for r in halving(v))
assert as_string(6)[:7] == "3322111" and len(as_string(6)) - 7 == 5
assert 6 * 2 == 12 and 1 + 2 == 3 and 6 + 2 == 8 and 8 + 12 == 20
run, acc = [], 0
for a in (3, 4, 9, 14, 23):
    acc += a; run.append(acc)
assert run == [3, 7, 16, 30, 53] and 5 + 3 == 8 and 14 + 23 == 37 and 53 % 37 == 16 % 37 == 16
assert isprime(53) and isprime(107) and isprime(23) and isprime(47)
assert factorint(3322111) == {13: 1, 421: 1, 607: 1} and 3322111 % 37 == 29
assert factorint(44222211111111) == {3: 1, 11: 1, 1340067003367: 1} and 44222211111111 % 37 == 33

if __name__ == "__main__":
    print("8 = 44|2222|11111111 exact; 6 = 33|2211|111111 (3322111 is its first 7 digits); chain holds; 14+23 = 37")

# CLASS: THEOREM
"""
What Excel is, mathematically, and where the owner's math meets it (2026-09-30).

EXCEL'S STRUCTURE
  - A sheet is a grid of cells addressed (column letters, row number).
    Limits: 16,384 columns (last = XFD) = 2^14, 1,048,576 rows = 2^20.
  - Column letters are BIJECTIVE BASE 26: A = 1 ... Z = 26, AA = 27, ... There
    is no zero digit. The digit values are exactly A1Z26, the letter values the
    owner uses (word_values.py, the MICHAEL route in CLAUDE.md).
  - Numbers are IEEE-754 doubles shown to 15 significant digits, so integers
    above 2^53 are not exact in Excel.

WHERE THE OWNER'S MATH MEETS IT (all asserted below)
 1. Adding a word's letter values is casting out 25s in base 26, the exact
    analogue of the digit-sum collapse (casting out 9s) in base 10:
        letter sum  =  (column number of the word)  mod 25,
    because 26 = 1 (mod 25), as 10 = 1 (mod 9). OKLAHOMA: letter sum 76 and
    column number 124,018,410,751 are both 1 mod 25.
 2. The base-10 collapse of a column number is an ALTERNATING letter sum,
    because 26 = -1 (mod 9):  column mod 9 = sum of (+/-) letter values mod 9.
    So summing letters (the owner's method) and collapsing Excel's column
    number mod 9 are different operations; they agree mod 25, not mod 9.
 3. The owner's 9x9 grid G(r, c) = 9r + c is an Excel sheet with 9 columns
    A..I: cell index 9*(ROW()-1) + COLUMN(). Column I (the 9th) is the column
    where the collapse is 9.
 4. The collapse is one Excel formula: =1+MOD(A1-1,9)  (for A1 >= 1).

EXCEL FORMULAS TO TEST THIS IN EXCEL
  Grid:        in A1, then fill A1:I9      =9*(ROW()-1)+COLUMN()
  Collapse:    =1+MOD(A1-1,9)
  Column no.:  =COLUMN(INDIRECT("XFD1"))  -> 16384
  Letter sum:  for text in A1: =SUMPRODUCT(CODE(MID(UPPER(A1),ROW(INDIRECT("1:"&LEN(A1))),1))-64)

FALSIFICATION: any assertion failing.
"""
import random


def col(word):
    n = 0
    for ch in word.upper():
        n = n * 26 + (ord(ch) - 64)
    return n


def letters(word):
    return [ord(c) - 64 for c in word.upper()]


def alt(word):
    v = letters(word)
    return sum(x * (-1) ** (len(v) - 1 - i) for i, x in enumerate(v))


assert col("XFD") == 16384 == 2 ** 14 and 1048576 == 2 ** 20
assert col("A") == 1 and col("Z") == 26 and col("AA") == 27 and col("ZZ") == 702
assert 26 % 25 == 1 and 26 % 9 == 8                                     # 26 = 1 mod 25, -1 mod 9
assert sum(letters("OKLAHOMA")) == 76 and col("OKLAHOMA") == 124018410751 and 76 % 25 == col("OKLAHOMA") % 25 == 1
R = random.Random(0)
WORDS = ["".join(chr(65 + R.randrange(26)) for _ in range(R.randrange(1, 9))) for _ in range(20000)]
assert all(sum(letters(w)) % 25 == col(w) % 25 for w in WORDS)          # 1
assert all(col(w) % 9 == alt(w) % 9 for w in WORDS)                     # 2
assert any(sum(letters(w)) % 9 != col(w) % 9 for w in WORDS)            # 2: sum != column mod 9 in general
assert all(9 * ((r + 1) - 1) + c == 9 * r + c for r in range(9) for c in range(1, 10))   # 3
assert all(1 + (n - 1) % 9 == (n % 9 or 9) for n in range(1, 10 ** 5))  # 4
assert float(2 ** 53 + 1) == float(2 ** 53)                             # doubles lose integers past 2^53

if __name__ == "__main__":
    for w in ("OKLAHOMA", "EXCEL", "MICHAEL", "XFD"):
        print(f"{w:9} column {col(w):>13}  letter sum {sum(letters(w)):3}  -> both {col(w) % 25} mod 25")
    print("all assertions pass")

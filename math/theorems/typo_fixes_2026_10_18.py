# CLASS: AUDIT
"""
The typos found in the owner's lines and in the pasted text on 2026-10-17/18, each FIXED here with the corrected line checked (owner_work #332:
"a typo, and you're not going to fix it"). Rule (CLAUDE.md): a clear slip is pointed out in one line, the intended value is used, and the work goes on.

OWNER'S LINES                                      FIXED LINE                                             WHY
  89=8+6=5+8=4+8=3+6=8      (#317)                 89=8+6=5+8=4+8=3+6=9                                   3+6 = 9; 8 and 9 are neighbouring keys
  33+33=6+6=1+12=3          (#318)                 33+33=6+6=1+2=3                                        6+6 = 12 and 1+2 = 3; "1+12" is 13
  457=1+7=8                 (2026-10-18)           457=1+6=7                                              4+5+7 = 16 and 1+6 = 7 (the +1 rule would give 8; plain arithmetic is used)
PASTED TEXT (not the owner's)
  101+131 -> 3                                     101+131 -> 4                                           the chain it shows ends 232 - 111 = 121 -> 1+2+1 = 4; no 3 appears
  "121 -> drip -> 010, a flat repunit"             121 - 111 = 010; the repunit is the 111 taken away     010 is not a repunit
  "7 = 3 (mod 4)"                                  7 is the digital root of 232 (mod 9 world)             mod 4 is not the modulus of digital roots

CANNOT BE FIXED FROM WHAT IS HERE (no guess made): the "outcome row 1, 1, 2, 2, 3, 4, 3" of the pasted analysis. The owner's lines it came from are not in the
  record and no operation on the pairs (1,2) (3,1) (2,3) ... gives it. Sent again with its lines, it is checked at once. (The pairs are the first two columns of the seven rows
  123 312 231 123 312 231 123: 1321321 and 2132132; with the third column 3213213 the three add to 6666666, no carries.)
FALSIFICATION: any assertion failing.
"""


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


assert dr(8 + 9) == 8 and dr(8 + 6) == 5 and dr(5 + 8) == 4 and dr(4 + 8) == 3 and dr(3 + 6) == 9 and 3 + 6 == 9 != 8
assert 33 + 33 == 66 and 6 + 6 == 12 and 1 + 2 == 3 and 1 + 12 == 13
assert 4 + 5 + 7 == 16 and 1 + 6 == 7 and dr(457) == 7 and dr(457) + 1 == 8
assert 101 + 131 == 232 and 232 - 111 == 121 and 1 + 2 + 1 == 4 and dr(121) == 4
assert 121 - 111 == 10 and set(str(111)) == {"1"} and set(str(10)) != {"1"}
assert dr(232) == 7 and 7 % 4 == 3
rows = ["123", "312", "231", "123", "312", "231", "123"]
cols = ["".join(r[i] for r in rows) for i in range(3)]
assert cols == ["1321321", "2132132", "3213213"] and sum(map(int, cols)) == 6666666

if __name__ == "__main__":
    print("typos fixed: 89 chain ends 9; 33+33=6+6=1+2=3; 457=1+6=7; 101+131 -> 4; the outcome row 1,1,2,2,3,4,3 needs its source lines")

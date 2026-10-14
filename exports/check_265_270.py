# Michael Warren Song -- checks of messages #265-#270 (2026-10-13). Paste into any Python 3 and run.
def dr(n): return 0 if n == 0 else 1 + (n - 1) % 9
def count_commas(commas, with1):          # #266: lead 1, each comma, each group of 3
    out = [1]
    for c in range(1, commas + 1): out += [c + 1 if with1 else c, 3]
    return int("".join(map(str, out)))
checks = [
 ("#265 0,000=4  00,000=5  000,000=6  0,000,000=7", [len(s.replace(",", "")) for s in ("0,000","00,000","000,000","0,000,000")] == [4,5,6,7]),
 ("#265/#266 12333 = commas counted with 1", count_commas(2, True) == 12333),
 ("#265/#266 11323 = commas counted without", count_commas(2, False) == 11323),
 ("#267 1+3, 2+2, 3+1 = 4", 1+3 == 2+2 == 3+1 == 4),
 ("#267 12+34=46, 21+43=64", 12+34 == 46 and 21+43 == 64),
 ("#267 12+21=33, 34+43=77, 46+64=110", (12+21, 34+43, 46+64) == (33, 77, 110)),
 ("#267 24+13=37 -> 3+7=10 -> +1 = 11", 24+13 == 37 and 3+7+1 == 11),
 ("#268 ,000 x3: 3+6+9=18 -> 9; +3 commas -> 21 and 12", 3+6+9 == 18 and dr(18) == 9 and 18+3 == 21 and 9+3 == 12),
 ("#269 10/11, 20/22, 30/33 -> 3, 6, 9", [dr(a+b) for a, b in ((10,11),(20,22),(30,33))] == [3,6,9]),
 ("#270 doubling roots 1 2 4 8 7 5 1 (7th = second 1)", [dr(2**k) for k in range(7)] == [1,2,4,8,7,5,1]),
 ("#270 rows 124 / 875 / 1 -> column 181", int("".join(str(dr(2**k)) for k in (0,3,6))) == 181),
 ("#270 124 + 875 = 999", 124 + 875 == 999),
 ("#270 248 + 510 = 758, roots 5+6 -> 2", 248+510 == 758 and dr(dr(248)+dr(510)) == dr(758) == 2),
]
for title, ok in checks: print("PASS" if ok else "FAIL", " ", title)
print(sum(ok for _, ok in checks), "of", len(checks), "checks passed")

# CLASS: COMPUTATION
"""
The owner's draining system, "casting out tens" -- filed 2026-10-04 from the owner's
message of 2026-09-23 05:39 UTC (it was never filed before; nothing in the repo held it).
Author: Michael Warren Song (CyclicAmp)

OWNER'S WORDS (verbatim, the counting part)
  "10 isnt tens its a marker meaning 1 zero has been drained...
   so the idea is 0 has a maximum capacity of 45 which is 1 thru 9 added up...When a Zero
   reaching its maximum we drain it back to zero...
   45+1=4+6=10
   So 9 becomes 0 and I say the zero has been drained 1 time I mark like this (+1 0)
   10+9=19+1=20
   see at 20 we drained the 9 twice.
   but at 18 which is 9+9 =18 is our true second 9 not 19...19 is based on counting 10s..
   first 9+1=(1<0)
   second 9+9 needs +1+1 +2=20=(27 nines)(29 tens)
   third =9+9+9=27 needs +1+1+1 +3=30-(36)(39
   forth +4  and so on
   what's interesting is when I get to 99 i only need +1
   but 9x9=81+19=(100+1)  because 8+1=9(+1=1)
   if we caste out 10s and 5
   (0)1-2-3-4(0)5-6-7-8-9(0)
   Here i create alpha O/E numbers i call them
   1=LLO 2=LLE 3=LRO 4=LRE 5=RLO 6=RLE 7=RRO 8=RRO"
  The message continues with grids (000/000/000, 222/212/222, 333/323/333), streams
  (212, 121, 21212/12121), the snake grid 123/654/789 and L / | / tetris shapes; those are
  recorded in the owner's message file and decoded in rotation_shapes_new_stacks_2026_10_03.py
  and theorem_325 where they overlap.

DECODED (every line checked below)
  D1 THE DRAIN COUNTER. A number is drains and remainder: n = 10 * (drains) + r. 10 is
     "(+1 0)": one drain, 0 left. 20: drained twice.
  D2 THE CAPACITY. 1 + 2 + ... + 9 = 45 (the triangular number T(9)); 45 + 1 = 46, digits
     4 + 6 = 10: one past capacity reads as one drain.
  D3 THE TWO COUNTS OF "THE k-th NINE".
       counting nines (9, 18, 27, 36): the k-th is 9k
       counting tens  (9, 19, 29, 39): the k-th is 10k - 1
     They differ by k - 1: (9,9), (18,19), (27,29), (36,39) -- the owner's
     "(27 nines)(29 tens)" and "(36)(39".
  D4 THE DRAIN LAW. "+1 per nine": 9k + k = 10k. k nines need k units to drain k times
     (9 + 1 = 10, 18 + 2 = 20, 27 + 3 = 30, ...). Forced: 9k + k = 10k.
  D5 "At 99 I only need +1": 99 + 1 = 100 -- one unit drains both columns at once (the
     carry chain; the exact law is T432's Kummer identity). By the D4 count, 99 = 11 nines
     would need +11 to reach 110 = 11 drains; reaching 100 instead takes one unit because
     the drain itself cascades.
  D6 "9x9 = 81 + 19 = (100+1)": 81 + 19 = 100; the "+1" is written as a drain marker
     ("8+1=9(+1=1)"), not as an addend -- 81 + 19 is 100, not 101.
  D7 THE ALPHA O/E CODE IS 3-BIT BINARY OF n - 1. Reading L = 0, R = 1 and O = 0, E = 1:
        1 LLO = 000   2 LLE = 001   3 LRO = 010   4 LRE = 011
        5 RLO = 100   6 RLE = 101   7 RRO = 110   8 RRE = 111
     First letter: which half (1-4 or 5-8, split at the "(0)" before 5); second: which pair
     inside the half; third: odd/even. The page writes 8 = RRO; the rule gives RRE (8 is
     even, and RRO is already 7) -- recorded as written, flagged as the one line the rule
     does not reproduce. 9 is not coded on the page.
FALSIFICATION: any assertion failing.
"""
dsum = lambda n: sum(map(int, str(n)))

# D1
assert [divmod(n, 10) for n in (10, 19, 20)] == [(1, 0), (1, 9), (2, 0)]
# D2
assert sum(range(1, 10)) == 45 and dsum(45 + 1) == 10
# D3
for k in range(1, 30):
    assert (10 * k - 1) - 9 * k == k - 1
assert [(9 * k, 10 * k - 1) for k in (1, 2, 3, 4)] == [(9, 9), (18, 19), (27, 29), (36, 39)]
# D4
assert all(9 * k + k == 10 * k for k in range(1, 100))
assert [9 + 1, 18 + 2, 27 + 3] == [10, 20, 30]
# D5
assert 99 + 1 == 100 and 99 == 9 * 11 and 99 + 11 == 110
# D6
assert 9 * 9 == 81 and 81 + 19 == 100 and 8 + 1 == 9
# D7
PAGE = {1: "LLO", 2: "LLE", 3: "LRO", 4: "LRE", 5: "RLO", 6: "RLE", 7: "RRO", 8: "RRO"}
rule = lambda n: "".join("LR"[b] for b in ((n - 1) >> 2 & 1, (n - 1) >> 1 & 1)) + "OE"[(n - 1) & 1]
assert [n for n in range(1, 9) if rule(n) == PAGE[n]] == [1, 2, 3, 4, 5, 6, 7]
assert rule(8) == "RRE" != PAGE[8] and len({rule(n) for n in range(1, 9)}) == 8
assert all(("O" if n % 2 else "E") == rule(n)[2] for n in range(1, 9))

if __name__ == "__main__":
    for n in range(1, 9):
        print(n, rule(n), format(n - 1, "03b"), "" if rule(n) == PAGE[n] else f"(page: {PAGE[n]})")

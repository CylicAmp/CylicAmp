# CLASS: AUDIT
"""
Adding 8 in the chain (owner_work #400, 2026-10-20). Process entry: owner_work/PROCESS.md, #400.

THE OWNER'S LINES, verbatim:
    1+8=9
    2+8=1
    3+8=2

    4+8=3
    5+8=4
    6+8=5

    7+8=6=2
    8+8=7=9
    8+9=8+9=8

    8+10=1+8=9+8=8
    8+11=1+9=10+9=1+8=9

CLEANED AND CHECKED:
  1+8 = 9 ; 2+8 = 10 → 1 ; 3+8 = 11 → 2 ; 4+8 = 12 → 3 ; 5+8 = 13 → 4 ; 6+8 = 14 → 5 ; 7+8 = 15 → 6 ; 8+8 = 16 → 7      all right
  8+9 = 17 → 8 (adding 9 changes nothing)                                                                             right
  8+10 = 18 → 1+8 = 9 ; then +8 → 9+8 = 17 → 8                                                                         right
  8+11 = 19 → 1+9 = 10 → 1 ; then +8 → 1+8 = 9                                                                         right
  ("10+9" as written is 19, which comes back to 10 → 1; the step to 1+8 reads as 10 → 1, then + 8.)
  What the lines show: adding 8 takes 1 off the chain every time (n + 8 → n − 1, and 1 + 8 → 9): 8 = 9 − 1, so adding 8 is adding 9 (nothing) and paying
  the 1 -- the "eight is the barrier and cost 1" of #399. Adding 9 takes nothing, 10 adds 1, 11 adds 2: 8+9 → 8, 8+10 → 9, 8+11 → 10 → 1.
  Each group of three lines adds to 3: 9+1+2 = 12 → 3, 3+4+5 = 12 → 3, 6+7+8 = 21 → 3.
MISSING (asked): the step after "7+8=6" to "=2", and after "8+8=7" to "=9".

FALSIFICATION: any assertion failing.
"""
chain = lambda n: n if n < 10 else chain(sum(map(int, str(n))))
assert [chain(n + 8) for n in range(1, 9)] == [9, 1, 2, 3, 4, 5, 6, 7]
assert all(chain(n + 8) == (n - 1 if n > 1 else 9) for n in range(1, 10))
assert all(chain(n + 8) == chain(n + 9 - 1 + 9) for n in range(1, 500)) and all(chain(n + 8) == chain(n - 1) for n in range(2, 500))
assert chain(8 + 9) == 8 and 8 + 10 == 18 and chain(18) == 9 and chain(9 + 8) == 8
assert 8 + 11 == 19 and 1 + 9 == 10 and chain(10) == 1 and 1 + 8 == 9 and chain(10 + 9) == 1
assert (chain(9 + 1 + 2), chain(3 + 4 + 5), chain(6 + 7 + 8)) == (3, 3, 3)

if __name__ == "__main__":
    print("#400: every line right -- adding 8 takes 1 off the chain (8 = 9 - 1); the steps 6 → 2 and 7 → 9 are asked for")

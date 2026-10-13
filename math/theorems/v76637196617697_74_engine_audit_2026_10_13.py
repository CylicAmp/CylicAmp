# CLASS: AUDIT
"""
The owner's 14-digit number and the pasted "74 engine" (owner_work #258, 2026-10-13).

THE OWNER'S LINES, verbatim:
    7663,7196,6176,(97)
    76,637,196,617,697

    7+6=1+3=4
    4+6=1+0=1
    1+3=4

  Both top lines are the same 14 digits, V = 76637196617697, grouped in 4s and in 3s.
  The three lines below are the running digital root along V's digits (add the next digit,
  reduce): 7, 7+6 -> 4, 4+6 -> 1, 1+3 -> 4. Across all 14 digits the walk is
      7, 4, 1, 4, 2, 3, 3, 9, 6, 7, 5, 2, 2, 9
  and it ends on 9 because V's digits sum to 81.

FOUND: 7663 = 79 x 97 -- the first group is 97 (the group the owner set in parentheses) times its
  reversal 79; both prime.

THE PASTED "74 ENGINE" BLOCK, checked exactly
  The engine: 1 + 44 + 14 + 11 + 4 = 74 = 2 x 37 (a SEAM value); 44 = 2^2*11, 14 = 2*7, 4 = 2^2.
  All ten products V x 74^k (k = 1..10) are correct.
  Digit sums: iterations 5 and 6 are swapped (5 sums to 108, 6 to 99 -- stated 99 and 108), and
  iteration 10 sums to 117, not 126. Every root is 9, which is forced: V is a multiple of 9
  (digit sum 81), so every multiple of V is.
  V mod 1..10 = 0, 1, 0, 1, 2, 3, 2, 1, 0, 7 -- the block's "mod 7 = 1" is 2.

FRAMEWORKS
  V = 3^2 x 103 x 82672272511 -> 3 (C3), DR 9.   7663 -> C3.   7196 = 2^2*7*257 -> SEED.
  6176 = 2^5*193 -> D7.   97 prime -> TESLA.   76 -> DARK_A.   637 = 7^2*13 -> TESLA.
  196 = 2^2*7^2 -> NEG_H.   617 prime, twin (617, 619) -> SA_ST_B.   697 = 17*41 -> C9.   74 -> SEAM.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime

V = 76637196617697
dr = lambda n: 0 if n == 0 else 1 + (n - 1) % 9
assert "7663719661769" "7" == str(V) == "76" "637" "196" "617" "697"
walk, r = [], 0
for c in str(V):
    r = dr(r + int(c)); walk.append(r)
assert walk == [7, 4, 1, 4, 2, 3, 3, 9, 6, 7, 5, 2, 2, 9] and walk[1:4] == [4, 1, 4]
assert 7 + 6 == 13 and 1 + 3 == 4 and 4 + 6 == 10 and sum(map(int, str(V))) == 81
assert 7663 == 79 * 97 and isprime(79) and isprime(97) and str(79) == str(97)[::-1]
assert 1 + 44 + 14 + 11 + 4 == 74 == 2 * 37
ds = []
p = V
for _ in range(10):
    p *= 74; ds.append(sum(map(int, str(p))))
assert p == 377360820225814352692011083523072
assert ds == [81, 99, 72, 81, 108, 99, 90, 144, 162, 117] and all(d % 9 == 0 for d in ds)
assert [V % k for k in range(1, 11)] == [0, 1, 0, 1, 2, 3, 2, 1, 0, 7]
assert factorint(V) == {3: 2, 103: 1, 82672272511: 1} and V % 37 == 3
assert isprime(617) and isprime(619) and 7196 % 37 == 18 and 6176 % 37 == 34 and 697 == 17 * 41

if __name__ == "__main__":
    print("walk 7,4,1,4,2,3,3,9,6,7,5,2,2,9; 7663 = 79 x 97; products right; ds 5/6 swapped, 10 is 117; mod 7 = 2")

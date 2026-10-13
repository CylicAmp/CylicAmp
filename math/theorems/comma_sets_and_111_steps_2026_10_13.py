# CLASS: AUDIT
"""
Comma sets and the +111 steps (owner_work #265, 2026-10-13).

THE OWNER'S LINES, verbatim:
    a set can be 
    0,000=1+3=4
    00,000=2+3=5
    000,000=3+3=6
    0+1=0,000,000=1+6=7
    or 12333 count commas with 1
    or 11323 count commas with out
    
    134+111
    235+111
    336-167
    167=cap plus new beginning

COMMA SETS -- all hold: a numeral's digits are the lead group plus groups of three.
  0,000 = 1+3 = 4;  00,000 = 2+3 = 5;  000,000 = 3+3 = 6;  0,000,000 = 1+6 = 7 (the owner's +1
  starts a new lead group: "everything needs +1 ... to begin again", #264).
  Open: 12333 ("count commas with 1") and 11323 ("count commas with out").

THE +111 STEPS
  134+111 = 245 and 235+111 = 346 -- +111 adds 1 to every digit. 346 is the number under the grid
  in #259: 346 = 235 + 111. 111 = 3 x 37, so +111 never changes the residue: 134 and 245 are both
  23 (TESLA); 235 and 346 are both 13 (CAS_EXT). 134, 235, 336 step by 101.
  336 - 167 = 169 = 13^2.
  "167 = cap plus new beginning": 6 (cap) + 1 (new beginning) = 7, written 1, 6, 7 -- the owner's
  1+6 = 7. 167 is prime and a safe prime ((167-1)/2 = 83 is prime).
  11323 = 169 x 67: 169 = 336 - 167 above, and 67 is half of 134.

FRAMEWORKS: 336 = 2^4*3*7 -> 3 C3; 167 -> 19 CAS_EXT; 169 -> 21 SA_ST_B; 12333 = 3 x 4111 -> 12
  SA_ST_A; 11323 -> 1 IC; 111 SEAM.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime

for s, k in (("0,000", 4), ("00,000", 5), ("000,000", 6), ("0,000,000", 7)):
    g = s.split(",")
    assert sum(map(len, g)) == k and all(len(x) == 3 for x in g[1:])
assert 1 + 3 == 4 and 2 + 3 == 5 and 3 + 3 == 6 and 1 + 6 == 7
assert 134 + 111 == 245 and 235 + 111 == 346 and 111 == 3 * 37
assert all(int(b) == int(a) + 1 for a, b in zip("134", "245")) and all(int(b) == int(a) + 1 for a, b in zip("235", "346"))
assert 134 % 37 == 245 % 37 == 23 and 235 % 37 == 346 % 37 == 13 and 235 - 134 == 336 - 235 == 101
assert 336 - 167 == 169 == 13 ** 2 and isprime(167) and isprime(83) and (167 - 1) // 2 == 83
assert 11323 == 169 * 67 and 134 == 2 * 67 and factorint(12333) == {3: 1, 4111: 1}
assert 12333 % 37 == 12 and 11323 % 37 == 1 and 167 % 37 == 19 and 169 % 37 == 21

if __name__ == "__main__":
    print("comma sets hold; 346 = 235 + 111; 336 - 167 = 13^2; 167 safe prime; 11323 = 169 x 67")

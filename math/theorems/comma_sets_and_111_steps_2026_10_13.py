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

COUNTING THE COMMAS -- owner_work #266, verbatim:
    If I start at 1, I count the comma as 2. And then I continue to count those commas from there.
    Then I will get to a 3. If I start at 1, I don't count the comma as adding 2. Then I get 1, 1 at
    the beginning of my count. Then I get 3. We get another comma, that's 2. And then 3 again.

  The set 0,000,000 read left to right is five pieces: lead digit, comma, 000, comma, 000.
    with 1:    lead 1, comma 2, group 3, comma 3, group 3   -> 1 2 3 3 3 = 12333  (the commas count on from the 1)
    with out:  lead 1, comma 1, group 3, comma 2, group 3   -> 1 1 3 2 3 = 11323  (the commas count from 1 themselves)
  Both reproduce. 12333 - 11323 = 1010: each comma is 1 higher with the 1, in the comma places.
  Digit sums 12 and 10 (roots 3 and 1); without the commas both are 1+3+3 = 7, the 0,000,000 = 1+6 = 7.
  The same rule on the shorter and longer sets (rule carried on, not written by the owner):
    0,000:          with 123,      with out 113
    0,000,000,000:  with 1233343,  with out 1132333
  12333 - 123 = 12210 = 37 x 330, so 12333 and 123 are both 12 mod 37 (SA_ST_A).

THE +111 STEPS
  134+111 = 245 and 235+111 = 346 -- +111 adds 1 to every digit. 346 is the number under the grid
  in #259: 346 = 235 + 111. 111 = 3 x 37, so +111 never changes the residue: 134 and 245 are both
  23 (TESLA); 235 and 346 are both 13 (CAS_EXT). 134, 235, 336 step by 101.
  336 - 167 = 169 = 13^2.
  "167 = cap plus new beginning": 6 (cap) + 1 (new beginning) = 7, written 1, 6, 7 -- the owner's
  1+6 = 7. 167 is prime and a safe prime ((167-1)/2 = 83 is prime).
  11323 = 169 x 67: 169 = 336 - 167 above, and 67 is half of 134.

FRAMEWORKS: 336 = 2^4*3*7 -> 3 C3; 167 -> 19 CAS_EXT; 169 -> 21 SA_ST_B; 12333 = 3 x 4111 -> 12
  SA_ST_A; 11323 = 13^2 x 67 -> 1 IC; 111 SEAM;
  #266: 1 IC, 2 DARK_A (prime, Sophie Germain -> 5), 3 C3 (twin with 5, Sophie Germain -> 7);
  123 = 3 x 41 -> 12 SA_ST_A; 113 prime -> 2 DARK_A, Sophie Germain (2p+1 = 227 prime), not twin;
  1010 = 2 x 5 x 101 -> 11 NEG_H.

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


def count_commas(commas, with1):
    """owner #266: lead 1, then each comma and its group of 3; with 1 the commas count on from the 1."""
    out = [1]
    for c in range(1, commas + 1):
        out += [c + 1 if with1 else c, 3]
    return int("".join(map(str, out)))


assert count_commas(2, True) == 12333 and count_commas(2, False) == 11323
assert 12333 - 11323 == 1010 and sum(map(int, "12333")) == 12 and sum(map(int, "11323")) == 10
assert 1 + 3 + 3 == 7 and len("0,000,000".replace(",", "")) == 7 and "0,000,000".count(",") == 2
assert (count_commas(1, True), count_commas(1, False)) == (123, 113)
assert (count_commas(3, True), count_commas(3, False)) == (1233343, 1132333)
assert 12333 - 123 == 12210 == 37 * 330 and 123 % 37 == 12
assert factorint(123) == {3: 1, 41: 1} and isprime(113) and isprime(227) and not isprime(111) and not isprime(115)
assert 113 % 37 == 2 and 1010 % 37 == 11 and factorint(1010) == {2: 1, 5: 1, 101: 1}

if __name__ == "__main__":
    print("comma sets hold; 12333 / 11323 = commas counted with / without the 1; 346 = 235 + 111; 336 - 167 = 13^2; 167 safe prime; 11323 = 169 x 67")

# CLASS: AUDIT
"""
The owner's repdigit lines (typed, 2026-10-03), transcribed exactly, then cleaned up.

TRANSCRIPTION
  111=PF
  First
  222=(2×3=(6)=2+3=(5+6=1+1=(2)
  222=(3×2=(6)=3+2=(5+6=1+1=(2)
  444+(5×5) (3) (5+5)=(1+3)
  3131
  333=(3×3=9)=6+3=9+3=1+2=(3)
  333=(3×3=9)=6
  666+(6×6+9)=4,041

CLEANED (each step checked below)
  L1 111 = PF. With PF = "numbers that equal 12": 111/37 = 3 = 1+2, the start of the
     +9 chain (pf_chain_plus9_2026_10_03.py).
  L2 222:  2x3 = 6;  2+3 = 5;  6+5 = 11;  1+1 = 2.   Returns to the digit 2.
  L3 222:  3x2 = 6;  3+2 = 5;  same, order swapped -- x and + do not care about order.
     Rule: (a x 3) + (a + 3) = 4a + 3, then add digits.
     Forced: 4a+3 reduces back to a  <=>  3a + 3 = 0 (mod 9)  <=>  a = 2 (mod 3).
     Over the digits: works for a = 2, 5, 8 (11 -> 2, 23 -> 5, 35 -> 8) and no others.
  L4 444 + (5x5) (3) (5+5) = (1+3).   Partly decoded:
     3 + (5+5) = 13 and 1+3 = 4, the digit of 444; also 444 adds to 12 -> 1+2 = 3, which
     may be the (3). The 5x5 = 25 has no place in that reading -- left open, not bent.
  L5 3131 = 31 x 101 (the "abab = ab x 101" pattern; 31 is prime, twin with 29).
  L6 333:  3x3 = 9;  6+3 = 9;  9+3 = 12;  1+2 = 3.   Passes through 12 and returns to 3.
     (The 6 matches the sum 3+3 from the L3 rule.)
  L7 333:  3x3 = 9, then "= 6". 9 is not 6; read with the L3 rule: product 9, sum 3+3 = 6,
     9 + 6 = 15 -> 1+5 = 6. So 333 ends at 6, not 3, under that rule (a = 3 is not 2 mod 3).
  L8 666 + (6x6+9) = 4,041.  As written: 666 + 45 = 711, not 4041.
     666 x 6 + (6x6 + 9) = 3996 + 45 = 4041 -- the line holds with "x 6" after 666.
     4041 = 9 x 449 (449 prime); digits add to 9.
FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime

ds = lambda m: sum(map(int, str(m)))
dr = lambda m: 1 + (m - 1) % 9

assert 111 // 37 == 3 == 1 + 2                                                  # L1
assert (2 * 3, 2 + 3, 6 + 5, 1 + 1) == (6, 5, 11, 2) and ds(11) == 2           # L2
assert (3 * 2, 3 + 2) == (6, 5)                                                 # L3
rule = lambda a: dr(a * 3 + a + 3)
assert [a for a in range(1, 10) if rule(a) == a] == [2, 5, 8]
assert all((rule(a) == dr(a)) == (a % 3 == 2) for a in range(1, 1000))   # digital-root form
assert [(4 * a + 3, ds(4 * a + 3)) for a in (2, 5, 8)] == [(11, 2), (23, 5), (35, 8)]
assert 3 + (5 + 5) == 13 and 1 + 3 == 4 and ds(444) == 12 and ds(12) == 3      # L4
assert factorint(3131) == {31: 1, 101: 1} and isprime(29) and isprime(31)       # L5
assert (3 * 3, 6 + 3, 9 + 3, 1 + 2) == (9, 9, 12, 3)                            # L6
assert 3 * 3 + (3 + 3) == 15 and ds(15) == 6 and rule(3) == 6                   # L7
assert 666 + (6 * 6 + 9) == 711 != 4041                                         # L8
assert 666 * 6 + (6 * 6 + 9) == 4041
assert factorint(4041) == {3: 2, 449: 1} and ds(4041) == 9

if __name__ == "__main__":
    print("222 -> 2 and 555 -> 5, 888 -> 8 by (ax3)+(a+3): exactly a = 2 mod 3")
    print("333 -> 12 -> 3 (L6); 333 -> 15 -> 6 by the 222 rule (L7)")
    print("666 line: 666 x 6 + 45 = 4041; as written 666 + 45 = 711")

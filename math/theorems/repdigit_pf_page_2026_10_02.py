# CLASS: AUDIT
"""
The owner's repdigit page (photo, 2026-10-02) and a correspondent's note on it.

PAGE (777 is not on the page)
  999 = x3            666 = x3           333 = x3
  555 = x2            222 = x2
  888 = (PF-33)3x3    444 = (PF-23)2x3   111 = (PF-13)1x3
PF = "prime foundational", the owner's own term (named in the correspondence).

WHAT THE PAGE DETERMINES (notation-decode: a reading is kept only if it fits
every line)
 1. Every aaa = 111 a = 3 * 37 * a.
 2. The x3 lines are exactly a in {3, 6, 9}: 3 | a, and then aaa = 3 * (another
    repdigit) -- 999 = 3*333, 666 = 3*222, 333 = 3*111.
 3. "Label by a mod 3" FAILS: 8 = 2 (mod 3) like 2 and 5, but 888 is a PF line.
 4. Two rules fit all eight lines:
      R1  3|a -> x3;  a prime -> x2;  otherwise PF      (777 -> x2)
      R2  3|a -> x3;  a in {2,5} -> x2;  otherwise PF   (777 -> PF)
    They differ only at 7, so the 777 line decides between them.  Under R1
    the PF digits {1, 4, 8} are the digits that are neither prime nor
    multiples of 3 -- also exactly 2^0, 2^2, 2^3.
 5. The PF lines carry an index k = 1, 2, 3 in two places: (PF-k3) and k x 3,
    for a = 1, 4, 8 in that order.  Consistent with "PF number k of 3".  What
    value PF itself takes is not on the page; the earlier reading "PF =
    largest prime factor" (operator audit, 999 line) gives 37 for every
    repdigit, so it cannot distinguish 111, 444, 888 -- it does not decode
    these lines.

CORRESPONDENT'S NOTE: "calculating moduli with base 11 produces a finite field;
base 10 moduli produce a ring with zero divisors."
  - Z/11 is a field (11 prime) and Z/10 has zero divisors (2*5 = 0): CORRECT.
  - Precision: the modulus, not the numeral base, decides.  In base b, the
    digit sum works mod b-1 and the alternating digit sum mod b+1.  So base 10
    ALREADY gives the field Z/11 (alternating sum), alongside Z/9 (digit sum,
    zero divisors 3*3 = 0).  Base 11 gives Z/10 (digit sum) and Z/12
    (alternating), both with zero divisors.
  - On this page: aaa = a (mod 11), aaa = 3a (mod 9), aaa = 0 (mod 37), for
    every digit a.  Same fact as excel_structure_connection.py (26 = -1 mod 9
    gives the alternating sum there).

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime

PAGE = {9: "x3", 8: "PF", 6: "x3", 5: "x2", 4: "PF", 3: "x3", 2: "x2", 1: "PF"}
PF_INDEX = {1: 1, 4: 2, 8: 3}

assert all(111 * a == 3 * 37 * a for a in range(1, 10))                               # 1
assert sorted(a for a, v in PAGE.items() if v == "x3") == [3, 6, 9]                    # 2
assert all(111 * a == 3 * 111 * (a // 3) for a in (3, 6, 9))

mod3 = lambda a: "x3" if a % 3 == 0 else ("x2" if a % 3 == 2 else "PF")
R1 = lambda a: "x3" if a % 3 == 0 else ("x2" if isprime(a) else "PF")
R2 = lambda a: "x3" if a % 3 == 0 else ("x2" if a in (2, 5) else "PF")
assert mod3(8) != PAGE[8]                                                              # 3
assert all(R1(a) == v for a, v in PAGE.items()) and all(R2(a) == v for a, v in PAGE.items())   # 4
assert (R1(7), R2(7)) == ("x2", "PF")
assert sorted(a for a in range(1, 10) if R1(a) == "PF") == [1, 4, 8] == [2 ** 0, 2 ** 2, 2 ** 3]
assert sorted(PF_INDEX) == sorted(a for a, v in PAGE.items() if v == "PF")              # 5
assert all(max(factorint(111 * a)) == 37 for a in range(1, 10))

# correspondent
def is_field(m):
    return all(any(x * y % m == 1 for y in range(1, m)) for x in range(1, m))
def zero_divisors(m):
    return sorted({x for x in range(1, m) for y in range(1, m) if x * y % m == 0})
assert is_field(11) and not is_field(10) and zero_divisors(10) == [2, 4, 5, 6, 8]
assert zero_divisors(9) == [3, 6] and zero_divisors(12) and not is_field(12)


def digits(n, b):
    out = []
    while n:
        out.append(n % b); n //= b
    return out


for b in (10, 11):
    for n in range(1, 5000):
        d = digits(n, b)
        assert sum(d) % (b - 1) == n % (b - 1)
        assert sum(x * (-1) ** i for i, x in enumerate(d)) % (b + 1) == n % (b + 1)
assert all(111 * a % 11 == a and 111 * a % 9 == 3 * a % 9 and 111 * a % 37 == 0 for a in range(1, 10))

if __name__ == "__main__":
    print("repdigit PF page: R1 and R2 both fit all 8 lines; 777 decides (R1: x2, R2: PF); "
          "base-10 alternating sum already gives the field Z/11")

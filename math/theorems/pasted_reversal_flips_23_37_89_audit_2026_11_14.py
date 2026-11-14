# CLASS: AUDIT
"""
Pasted text (2026-11-14), from another tool working on the owner's lines, relayed by the owner: the flips pair up as
reversals 23|32, 37|73, 89|98; "56 flips back to 23|32"; "□ = 73 pairs with 37"; "8,9 flips to 98".

RIGHT:
  32 - 23 = 9, 73 - 37 = 36, 98 - 89 = 9: a two-digit number and its reversal differ by 9 x (digit difference),
    always (10a + b - (10b + a) = 9(a - b)) -- forced;
  23 + 32 = 55, 37 + 73 = 110, 89 + 98 = 187, all multiples of 11 (sum = 11(a + b)) -- forced;
  37 x 73 = 2701;
  23, 37, 73, 89 are prime; 32 and 98 are not; 37 <-> 73 is the only one of the three flips sending a prime to a
    prime (37 and 73 are both emirps, OEIS A006567).

NOT CHECKABLE FROM THE PASTE: "56 flips back to 23|32" and "your single □ at position 7" come from the owner's
  lines, which are not in the paste (23 + 32 = 55, not 56). Wording, no number changes: "the M23 step" for 36 (in the
  repo M23 is the Mathieu group, fibonacci_mathieu_gf37.py).

FALSIFICATION: any assertion failing.
"""
from sympy import isprime

flips = [(23, 32), (37, 73), (89, 98)]
for a, b in flips:
    da, db = divmod(a, 10)
    assert b == 10 * db + da                              # reversal
    assert b - a == 9 * (da - db) * -1 or a - b == 9 * (da - db)
    assert (a + b) == 11 * (da + db)
assert [b - a for a, b in flips] == [9, 36, 9] and [a + b for a, b in flips] == [55, 110, 187]
assert 37 * 73 == 2701
assert [isprime(a) for a, _ in flips] == [True, True, True] and [isprime(b) for _, b in flips] == [False, True, False]
for a in range(10, 100):                                  # forced for every two-digit number
    b = (a % 10) * 10 + a // 10
    assert (a - b) % 9 == 0 and (a + b) % 11 == 0

if __name__ == "__main__":
    print("23|32, 37|73, 89|98: differences 9, 36, 9 and sums 55, 110, 187 forced; only 37 <-> 73 is prime to prime")

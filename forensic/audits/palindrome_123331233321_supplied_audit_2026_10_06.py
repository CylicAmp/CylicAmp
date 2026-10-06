# CLASS: AUDIT
"""
Supplied script (2026-10-06): is_prime / palindrome / factor check on
n = 123331233321.

FAULTS
  F1 is_prime returns the smallest factor (here 3) instead of False for a
     composite. It prints "Is Prime: 3", and 3 is truthy, so
     `if is_prime(n)` would treat this composite as prime.
  F2 n is not a palindrome: reversed it reads 123332133321. The script's own
     check prints False, which is correct.

RESULT
  n = 3^2 * 29 * 472533461; 12 digits; DR 9.
  - n mod 37 = 9: SA_ST_A {9, 12, 16}, class 4, and in SA.
  - 29 is a twin prime (29, 31), both in C9.
  - 472533461 is prime and Sophie Germain: 2q+1 = 945066923 is prime. It is
    in no twin pair, is not safe, and q mod 37 = 23 (TESLA).
  - Rule 30 one step: 239, which is 17 mod 37 (NQR17).
  - n * 137 = 12 mod 37 and n / 137 = 16 mod 37: both stay in SA_ST_A.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime

def supplied_is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return i
    return True

n = 123331233321
assert supplied_is_prime(n) == 3 and bool(supplied_is_prime(n)) and not isprime(n)   # F1
assert str(n)[::-1] == "123332133321" and str(n) != str(n)[::-1]                     # F2
assert len(str(n)) == 12 and n % 9 == 0
assert factorint(n) == {3: 2, 29: 1, 472533461: 1}
assert n % 37 == 9 and (n * 137) % 37 == 12 and (n * pow(137, -1, 37)) % 37 == 16
assert isprime(31) and 29 % 37 == 29 and 31 % 37 == 31
q = 472533461
assert isprime(q) and isprime(2 * q + 1) and 2 * q + 1 == 945066923
assert not isprime(q - 2) and not isprime(q + 2) and not isprime((q - 1) // 2) and q % 37 == 23
print("123331233321 = 3^2 * 29 * 472533461; supplied is_prime returns 3 (truthy). All assertions pass.")

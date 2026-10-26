# CLASS: AUDIT
"""
The pasted script and output on 222,222,222 + 1 = 222,222,223 (owner_work #440, 2026-10-26). Audit on arrival.
The script and output are from another tool, relayed by the owner; its line "The user's observation: 8 twos and 1 three"
is the script's.

RIGHT (re-run), every printed line:
  222222222 + 1 = 222222223; 9 digits each; even, odd
  nine 2s; eight 2s and one 3; 8 = 4 x 2, 3 = 1.5 x 2, 8 : 3 = 4 : 1.5
  222222222 = 2 x 111111111, 111111111 = 37 x 3003003, so 222222222 = 74 x 3003003
  222222223 = 449 x 494927, and 449 is the smallest factor (no prime below 449 divides it); 494927 is prime
  roots: 222222222 -> 18 -> 9; 222222223 -> 19 -> 10 -> 1

THE SCRIPT (a fault for other inputs, not this one): is_prime returns a pair for odd numbers from 5 up -- (False,
  factor) or (True, None) -- but a single True or False for 2, 3, even numbers and numbers below 2, and the line
  `result, factor = is_prime(m)` needs a pair: for an even m, or m = 2 or 3, the script stops with an error.
  For m = 222222223 it works.

NEW LINES, owner's notation:
  111111111 = 9 x 12345679 = 9 x 37 x 333667; 3003003 = 9 x 333667
  222222222 + 1: the root goes 9 -> 1 (adding 1 to a 9)
  222222222 -> 0 by 37 (it is 2 x 111111111, and 111 = 3 x 37), so 222222223 -> 1 by 37 (IC)

FRAMEWORKS (gf37-audit): 222222223 -> 1 IC; 449 -> 5 CAS_EXT (prime; 447 and 451 are not, so no twin);
  494927 -> 15 DARK_A (prime).

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime

n, m = 222_222_222, 222_222_223
assert n + 1 == m and len(str(n)) == len(str(m)) == 9 and n % 2 == 0 and m % 2 == 1
assert str(n) == "2" * 9 and sorted(str(m)) == ["2"] * 8 + ["3"]
assert 8 == 4 * 2 and 3 == 1.5 * 2 and 8 / 3 == 4 / 1.5
assert n == 2 * 111_111_111 and 111_111_111 == 37 * 3_003_003 and n == 74 * 3_003_003
assert m == 449 * 494_927 and isprime(449) and isprime(494_927)
assert all(m % p for p in range(2, 449)) and factorint(m) == {449: 1, 494927: 1}
assert sum(map(int, str(n))) == 18 and (n - 1) % 9 + 1 == 9 and sum(map(int, str(m))) == 19 and (m - 1) % 9 + 1 == 1


def is_prime_as_pasted(n):
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False, i
    return True, None


assert is_prime_as_pasted(m) == (False, 449)
assert is_prime_as_pasted(13) == (True, None)        # odd primes from 5 up come back as a pair
for bad in (222_222_224, 3, 2, 1):                  # even numbers, 2, 3 and below 2 come back bare
    try:
        result, factor = is_prime_as_pasted(bad)
        raise AssertionError("expected the unpacking to fail")
    except TypeError:
        pass

assert 111_111_111 == 9 * 12_345_679 and factorint(111_111_111) == {3: 2, 37: 1, 333667: 1} and 3_003_003 == 9 * 333_667
assert n % 37 == 0 and m % 37 == 1 and 449 % 37 == 5 and 494_927 % 37 == 15
assert not isprime(447) and not isprime(451)

if __name__ == "__main__":
    print("222222223 = 449 x 494927: every printed line right; the script's is_prime breaks on even numbers, 2, 3 and below 2")

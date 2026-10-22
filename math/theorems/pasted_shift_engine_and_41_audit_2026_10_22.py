# CLASS: AUDIT
"""
The pasted "The audit holds" text: the combined shift +8 then -4, the 4 -> 9 boundary, and the
profile of 41 (owner_work #416, 2026-10-22). Audit on arrival. It restates
pasted_minus_4_and_dr_question_audit_2026_10_22.py and adds the profile of 41.

THE PASTE: text from another tool, relayed by the owner. Nothing below puts a claim of the paste
in the owner's mouth.

RIGHT (re-run), every line:
  + 8 takes 1 off, - 4 adds 5, together + 4:  7 -> 6 -> 2,  7 + 4 = 11 -> 2
  n - 4 with n = 13, 22, 31 ... has root 9; 4 - 4 = 0
  41 = 1 x 37 + 4;  41 and 43 are twins, 42 = 6 x 7;  2 x 41 + 1 = 83 is prime (so 41 is
  Sophie Germain and 83 is safe);  x x x + x + 41 is prime for x = 0 to 39

ALREADY IN THE REPO (the paste adds nothing beyond these):
  seed_246_polymath_gap_gf37.py -- 246 = 2 x 3 x 41, Euler's lucky prime 41, x x x + x + 41 prime
    for x = 0 to 39, its discriminant 1 - 4 x 41 = -163
  twin_prime_structure.py -- Theorem 5, Euler's polynomial; the six lucky primes 2 3 5 11 17 41
  theorem_266_n123_multiples_dr369_gf37.py -- 123 x k: 123, 246, 369 (roots 6, 3, 9)
  so 41 x 3 = 123, 41 x 6 = 246 (the reference seed), 41 x 9 = 369; and x = 40 gives
  40 x 40 + 40 + 41 = 1681 = 41 x 41, the first value that is not prime.

FALSIFICATION: any assertion failing.
"""
from sympy import isprime


def root(n):
    while n > 9:
        n = sum(map(int, str(n)))
    return n


assert root(7 + 8) == 6 and root(15 - 4) == 2 and root(7 + 4) == 2
assert all(root(n - 4) == 9 for n in range(13, 10000, 9)) and 4 - 4 == 0
assert 41 == 37 + 4 and isprime(41) and isprime(43) and 42 == 6 * 7
assert isprime(83) and 83 == 2 * 41 + 1
assert all(isprime(x * x + x + 41) for x in range(40)) and 40 * 40 + 40 + 41 == 1681 == 41 * 41
assert 1 - 4 * 41 == -163
assert (41 * 3, 41 * 6, 41 * 9) == (123, 246, 369) and [root(v) for v in (123, 246, 369)] == [6, 3, 9]
assert [q for q in range(2, 100) if isprime(q) and all(isprime(x * x + x + q) for x in range(q - 1))] == [2, 3, 5, 11, 17, 41]

if __name__ == "__main__":
    print("#416: every line right; 41's profile (Euler's x x x + x + 41, prime 0..39; 1681 = 41 x 41 at 40) is already "
          "in seed_246_polymath_gap_gf37.py and twin_prime_structure.py; 41 x 3, 6, 9 = 123, 246, 369")

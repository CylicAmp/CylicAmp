# A framework made from the owner's work

Michael Warren Song, 2026-10-20 (owner_work #390: "create a framework that's made from my work that attempts to prove something").
Every check is in `math/theorems/owner_framework_flips_halves_moves_2026_10_20.py`, which CI runs on every push.

## The operations — the owner's, with where they were used

1. **Add the digits in a chain** until one is left: 8+7=15 → 1+5=6, 6+3=9, 9+5=14 → 1+4=5 (#369).
2. **Flip**: write a number backwards — "what about with two flips" (#358), "reading back and forth" (#375).
3. **Mirror**: a pair, then its flip — 248 → 24 42 → 2442, 48 84 → 4884 (#374).
4. **Halve**: 9 ÷ 2 ÷ 2 ÷ 2 = 1.125 (#368), 5 ÷ 2 = 2.5 + 2.5 (#382), 7 ÷ 2 = 3.5 + 3.5 (#383).
5. **Move**: take from one digit and give to another or to a new place — "minus 1 from the 3. And give it to the 1 in the front" (#376, #378).
6. **Count both ways**: with zero and without — "so totals are for both" (#379, #269).

## What the operations prove

**1. The chain ends on the remainder by 9.** 10 = 9 + 1, so every number and its digit total differ by a multiple of 9.
So the chain of a sum is the chain of the chains, and adding 9 changes nothing: 9 + 3 = 12 → 3, 9 + 6 = 15 → 6.

**2. Moves keep the total, so they keep the chain.** All forms of 0.125 (total 8) and 0.137 (total 11), counted both ways:

    0.125   without zero 576      with zero 51480 (up to 8 digits)
    0.137   without zero 6139     with zero 3878545 (up to 11 digits)

The count works for any total: the ways to write the total as digits, times the places the point can go.

**3. Halving walks the doubling chain backwards.** x ÷ 2 = 5 × x ÷ 10, and moving the point changes no digit:

    1 → 0.5 → 0.25 → 0.125 → 0.0625 → 0.03125 → 0.015625
    1 → 5   → 7    → 8     → 4      → 2       → 1
    the doubling chain 1 2 4 8 7 5, read backwards

Doubling a half always gives the whole's chain back, because 2 × 5 = 10 → 1 (8 + 8 = 16 → 7 for 7, 7 + 7 = 14 → 5 for 5).

**4. A flip moves a number by a multiple of 9.** For two digits: 9 × 7 = 63 and 9 × 4 = 36, 9 × 6 = 54 and 9 × 5 = 45 — the flip of 9 × k is 9 × (11 − k).

**5. The 37 test.**

    three digits abc:   37 divides abc + cba  exactly when  a + c = 2b       and then abc + cba = 222 × b
    four digits abcd:   37 divides abcd + dcba exactly when  2(a + d) = b + c and then the sum = 1221 × (a + d)
    four-digit mirror abba: always a multiple of 11; a multiple of 37 exactly when b = 2a: 1221 2442 3663 4884

Why, for three digits: abc + cba = 101 × (a + c) + 20 × b. Take out the 37s: 101 = 74 + 27, and 27 × 11 = 297 = 296 + 1, so the test becomes
"a + c and 2b leave the same remainder by 37". Both are between 0 and 18, so they must be equal.
So 248's mirrors 2442 and 4884 are multiples of 37 because each pair doubles: 2 → 4, 4 → 8.

**6. The 1 to 9 grid.** Each flip of 123, 456 or 789 adds 198:

    1368 → 1566 → 1764 → 1962        0, 1, 2, 3 flips
    1368 + 1962 = 1566 + 1764 = 3330 = 90 × 37 = 222 × (2 + 5 + 8)

**7. Two ones.** 1 0 0 1 adds to 2. Fill the space with 9s and the chain stays 2 (1991 → 20 → 2); add one more 9 and it carries through: 1991 + 9 = 2000 —
"now a part of the 2" (#369).

**8. Twin primes through the chain.** Every twin pair after (3, 5) chains to (2, 4), (5, 7) or (8, 1): neither twin is a multiple of 3, so the first
leaves 2 by 3, so 2, 5 or 8 by 9. The 18x − 1, 18x + 1 family is always (8, 1).

## The attempt: does 37 bring 111 with it?

If 37 divides a number plus its flip, does 111 = 3 × 37 divide it too?

    1 and 2 digits   37 never divides the sum (it is at most 18 and 11 × 18)
    3 digits         yes, proved: the sum is 222 × b = 2b × 111
    4 digits         yes, proved: the sum is 1221 × (a + d) = 11 × 111 × (a + d)
    5 digits         yes: all 2405 numbers checked
    6 digits         yes: all 34867 numbers checked
    7 digits         NO

The smallest number that breaks it:

    1009019 + 9109001 = 10118020 = 37 × 273460
    1+0+1+1+8+0+2+0 = 13 → 4, not a multiple of 3, so 111 does not divide it

At 7 digits 17084 of 234646 cases break; at 8 digits 107428 of 2396127.

Why it lasts to 6 digits and breaks at 7: a number plus its flip leaves the same remainder by 3 as twice its digit total. Up to 6 digits every way of passing the
37 test needs a digit total that is a multiple of 3; at 7 digits there is room for one that is not — 1009019 has digit total 20.

**Result:** "37 brings 111 with it" is proved for every number of 1 to 6 digits, and disproved from 7 digits on by 1009019.

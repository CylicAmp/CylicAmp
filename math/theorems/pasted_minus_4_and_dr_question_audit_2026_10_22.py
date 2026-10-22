# CLASS: AUDIT
"""
The pasted "Subtracting 4" block and the question "If an integer n has a digital root of
dr(n) = 7, what is the digital root of n + 8?" (owner_work #415, 2026-10-22). Audit on arrival.

THE PASTE: text from another tool, relayed by the owner; the question at the end is quoted as it
arrived ("dr(n) € f1,2,...,9)" reads as dr(n) in {1, 2, ..., 9}). Nothing below puts a claim of
the paste in the owner's mouth.

PRIOR ART: owner_adding_8_2026_10_20.py (#400: adding 8 takes 1 off the root, 8 = 9 - 1; the
owner's line "7+8=6"); pasted_signs_percent_equals_markov_audit / owner_equals_chain_three_things
(75.7% x 75.7% = 57.3049%); pasted_1137_squared_running_sum_audit (the ladder ending 45 -> 9).

THE QUESTION: dr(n) = 7 -> dr(n + 8) = 6.
    7 + 8 = 15 -> 1 + 5 = 6. Adding 8 takes 1 off: 7 -> 6 (the owner's #400 line "7+8=6").
    Every n with root 7 (7, 16, 25, ... 997) gives n + 8 with root 6.

RIGHT (the paste, re-run):
    taking 4 off a number takes 4 off its root, the same as adding 5: 4 + 5 = 9
    9 -> 5,  7 -> 3,  4 -> 9,  2 -> 7
    45 - 4 = 41 -> 4 + 1 = 5;  9 - 4 = 5
    573049 -> 5+7+3+0+4+9 = 28 -> 10 -> 1;  1 - 4 -> 6
      (57.3049 - 4 = 53.3049 -> 5+3+3+0+4+9 = 24 -> 6;  573049 - 4 = 573045 -> 24 -> 6)

BOTH WAYS (with zero and without): the root 4 -> 9 line is right from 13 on (13 - 4 = 9);
    at 4 itself, 4 - 4 = 0, and 0 has root 0 -- the one number where the answer is 0, not 9.
    Without zero (n - 4 at least 1): every n from 5 on follows the rule.

NEW LINE: the two rules side by side, owner's notation:
    + 8 = + 9 - 1 -> takes 1 off        - 4 = - 9 + 5 -> adds 5 (takes 4 off)
    + 8 then - 4 = + 4 -> adds 4:  7 -> 6 -> 2;  7 + 4 = 11 -> 2

RESIDUES mod 37 (gf37-audit): 41 -> 4 C3 (prime, twin with 43, Sophie Germain 83), 15 DARK_A.

FALSIFICATION: any assertion failing.
"""


def root(n):
    while n > 9:
        n = sum(map(int, str(n)))
    return n


# the question
assert 7 + 8 == 15 and root(15) == 6
assert all(root(n + 8) == 6 for n in range(1, 100000) if root(n) == 7)

# the paste
assert all(root(n - 4) == (root(n) + 5 - 1) % 9 + 1 for n in range(5, 100000))
assert [(r - 4 - 1) % 9 + 1 for r in (9, 7, 4, 2)] == [5, 3, 9, 7]
assert 45 - 4 == 41 and root(41) == 5 and 9 - 4 == 5
assert sum(map(int, "573049")) == 28 and root(573049) == 1 and (1 - 4 - 1) % 9 + 1 == 6
assert root(533049) == 6 and 573049 - 4 == 573045 and root(573045) == 6

# both ways
assert 13 - 4 == 9 and root(9) == 9 and 4 - 4 == 0

# side by side
assert all(root(n + 8 - 4) == root(n + 4) for n in range(1, 1000))
assert root(7 + 8) == 6 and root(15 - 4) == 2 and root(7 + 4) == 2

assert [x % 37 for x in (41, 15)] == [4, 15]

if __name__ == "__main__":
    print("dr(n) = 7 -> dr(n + 8) = 6 (7 + 8 = 15 -> 6; adding 8 takes 1 off, #400); "
          "the minus-4 paste right (takes 4 off = adds 5); 4 - 4 = 0 is the one 0")

# CLASS: AUDIT
"""
The pasted analysis of the rows 891 782 673 564 455 346 237 128 919 891, the step 109 and the
roots counting down (owner_work #401, 2026-10-20). Audit on arrival.

THE PASTE: text from another tool, relayed by the owner. It opens "Here is the mathematical
structure and mechanics of the sequence you laid out". Nothing below puts a claim of the paste
in the owner's mouth.

WHERE THE ROWS COME FROM: not in #400 (1+8=9, 2+8=1, ... 8+11=...) and not elsewhere in
owner_work/ (searched for 891, 782, 673-564, 455-346). No check below needs it: every line of the
paste is checked from the rows themselves. (The reply asked for it as "missing"; per #408 that is
not a missing piece, since nothing was blocked.)

PRIOR ART: math/theorems/sliding_window_9cycle_gf37.py -- the windows 123 -> 234 -> ... -> 789,
every column +1, step 111, and the step changes at the wrap. The paste's rows are the same build
with the columns moving -1 -1 +1. What is new here: the general rule for any column moves (below),
and the wrap steps of the paste worked out.

RIGHT (re-run):
  columns   hundreds 8 7 6 5 4 3 2 1 9 8   tens 9 8 7 6 5 4 3 2 1 9   units 1 2 3 4 5 6 7 8 9 1
  891 - 782 = 782 - 673 = 673 - 564 = 564 - 455 = 455 - 346 = 346 - 237 = 237 - 128 = 109
  -100 - 10 + 1 = -109
  digit totals 18 17 16 15 14 13 12 11 19 18  ->  roots 9 8 7 6 5 4 3 2 1 9
  919 -> 9+1+9 = 19 -> 1+9 = 10 -> 1+0 = 1
  109 -> 1+0+9 = 10 -> 1
  every one of the 9 steps takes 1 off the root

WRONG (one fault): section 4, "Subtracting 109 at each step". Two of the 9 steps are not -109:
  128 -> 919 is +791      919 -> 891 is -28
  The roots still drop 1 at those steps, for a reason the paste does not give. At a wrap a column
  jumps by 8 in place of 1, which is 9 more in that place:
    128 -> 919   hundreds 1 -> 9 is +800, not -100: 900 more     -109 + 900 = 791
    919 -> 891   tens 1 -> 9 is +80, not -10: 90 more
                 units 9 -> 1 is -8, not +1: 9 less             -109 + 90 - 9 = -28
  900, 90 and 9 are all made of 9s, so they leave the root alone:
    791 -> 7+9+1 = 17 -> 8 = 9 - 1      28 -> 2+8 = 10 -> 1
  So +791 and -28 both take 1 off, like -109. Around the whole loop:
    7 x 109 = 763 = 791 - 28 -> the 9 steps add to 0

BOTH WAYS (with zero and without, #269 #379):
  every row is 1000 - 109 x k:  k = 1 -> 891, k = 2 -> 782, ... k = 8 -> 128
  with zero      k = 9 -> 019; the step 128 -> 019 is -109 again (8 steps of -109),
                 and the loop closes 019 -> 891 = +872 = 8 x 109
  without zero   the 0 is written 9 -> 919; the steps 128 -> 919 = +791, 919 -> 891 = -28
  019 -> 0+1+9 = 10 -> 1 and 919 -> 19 -> 10 -> 1: the same root both ways

NEW LINES, owner's notation:
  1000 -> 1+0+0+0 = 1; take 109 (root 1) k times -> root 1 - k: 891 -> 9, 782 -> 8, ...
  #400 "adding 8" takes 1 off; taking 109 takes 1 off; 8 + 109 = 117 = 9 x 13
    891 + 8 = 899 -> 8+9+9 = 26 -> 8      891 - 109 = 782 -> 17 -> 8   same root
  each column holds 1 to 9 once, so the 9 rows add to 45 x 111 = 4995:
    891 + 782 + 673 + 564 + 455 + 346 + 237 + 128 + 919 = 4995

  Any column moves (a, b, c), each +1 or -1: step 100a + 10b + c, root moves a + b + c.
    +1 +1 +1 -> 111, root +3 -> roots 3 6 9 only (the sliding window: 6 9 3 6 9 3 ...)
    -1 -1 -1 -> -111, root -3 -> 3 roots only
    the other 6 moves -> root +1 or -1 -> all 9 roots, like the paste's -1 -1 +1 = -109
  So 6 of the 8 moves walk all 9 roots; only 111 and -111 walk 3.

RESIDUES mod 37 (gf37-audit): -109 = -111 + 2, so each -109 step adds 2:
  891 -> 3 C3, 782 -> 5 CAS_EXT, 673 -> 7 D7, 564 -> 9 SA_ST_A, 455 -> 11 NEG_H,
  346 -> 13 CAS_EXT, 237 -> 15 DARK_A, 128 -> 17 NQR17, 919 -> 31 C9
  rows = 888+3, 777+5, 666+7, 555+9, 444+11, 333+13, 222+15, 111+17 (repdigit + odd number)
  primes: 673 (cousin with 677), 919, 109 (twin with 107); 891 = 3^4 x 11, 128 = 2^7,
  455 = 5 x 7 x 13, 4995 = 3^3 x 5 x 37.

FALSIFICATION: any assertion failing.
"""
from itertools import product
from sympy import isprime, factorint


def root(n):
    n = abs(n)
    while n > 9:
        n = sum(map(int, str(n)))
    return n


def chain_mod9(n):          # the root as a remainder by 9, 9 written for 0
    return n % 9 or 9


rows = [891, 782, 673, 564, 455, 346, 237, 128, 919, 891]
digits = [[int(d) for d in str(r)] for r in rows]

# --- RIGHT ---
assert [d[0] for d in digits] == [8, 7, 6, 5, 4, 3, 2, 1, 9, 8]
assert [d[1] for d in digits] == [9, 8, 7, 6, 5, 4, 3, 2, 1, 9]
assert [d[2] for d in digits] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
assert [rows[i] - rows[i + 1] for i in range(7)] == [109] * 7
assert -100 - 10 + 1 == -109
assert [sum(d) for d in digits] == [18, 17, 16, 15, 14, 13, 12, 11, 19, 18]
assert [root(r) for r in rows] == [9, 8, 7, 6, 5, 4, 3, 2, 1, 9]
assert root(919) == 1 and sum(map(int, "919")) == 19 and root(109) == 1

# --- WRONG: the two wrap steps are not -109 ---
steps = [rows[i + 1] - rows[i] for i in range(9)]
assert steps == [-109] * 7 + [791, -28]
assert -109 + 900 == 791 and -109 + 90 - 9 == -28
assert root(791) == 8 and root(28) == 1
assert all((s + 1) % 9 == 0 for s in steps)                  # every step takes 1 off the root
assert sum(steps) == 0 and 7 * 109 == 763 == 791 - 28

# --- BOTH WAYS ---
assert [1000 - 109 * k for k in range(1, 9)] == rows[:8]
assert 1000 - 109 * 9 == 19                                   # with zero: 019
assert 891 - 19 == 872 == 8 * 109
assert 919 == 19 + 900                                        # without zero: the 0 written 9
assert root(19) == root(919) == 1

# --- NEW LINES ---
assert root(1000) == 1
assert all(chain_mod9(1000 - 109 * k) == chain_mod9(1 - k) for k in range(1, 10))
assert 8 + 109 == 117 == 9 * 13 and root(891 + 8) == root(891 - 109) == 8
assert sum(rows[:9]) == 4995 == 45 * 111
assert all(sorted(d[c] for d in digits[:9]) == list(range(1, 10)) for c in range(3))

walks = {}
for a, b, c in product((1, -1), repeat=3):
    step, move = 100 * a + 10 * b + c, a + b + c
    reached = {chain_mod9(1 + move * t) for t in range(9)}
    walks[step] = len(reached)
assert walks[111] == 3 and walks[-111] == 3
assert sorted(s for s, n in walks.items() if n == 9) == [-109, -91, -89, 89, 91, 109]
assert sum(1 for n in walks.values() if n == 9) == 6

# the sliding window (prior art): +111 steps give the roots 6 9 3 only
window = [123, 234, 345, 456, 567, 678, 789]
assert [window[i + 1] - window[i] for i in range(6)] == [111] * 6
assert [root(w) for w in window] == [6, 9, 3, 6, 9, 3, 6]

# --- RESIDUES mod 37 ---
assert [r % 37 for r in rows[:9]] == [3, 5, 7, 9, 11, 13, 15, 17, 31]
assert -109 == -111 + 2 and (-109) % 37 == 2
assert all(rows[i] == 111 * (8 - i) + (3 + 2 * i) for i in range(8))
assert [n for n in rows[:9] + [109] if isprime(n)] == [673, 919, 109]
assert isprime(107) and isprime(677) and not isprime(111)
assert factorint(891) == {3: 4, 11: 1} and factorint(128) == {2: 7}
assert factorint(455) == {5: 1, 7: 1, 13: 1} and factorint(4995) == {3: 3, 5: 1, 37: 1}

if __name__ == "__main__":
    print("891 -> 128: seven steps of -109, right; 128 -> 919 = +791 and 919 -> 891 = -28, not -109 "
          "(the paste's 'at each step' is wrong); every step still takes 1 off the root because a wrap "
          "adds 900 or 90 - 9; rows = 1000 - 109k; 6 of the 8 column moves walk all 9 roots, 111 and -111 walk 3")

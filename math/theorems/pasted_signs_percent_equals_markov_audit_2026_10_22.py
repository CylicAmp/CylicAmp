# CLASS: AUDIT
"""
The pasted blocks inside owner_work #410 (2026-10-22): x × (−x × (−1)), 1.137% and 75.7% squared,
the three texts on 2 = (2) × 2 = 4, and "The 3 Actions" (Markov chain, the = key table, the
bracket frames, the 11 22 33 66 ladder, 1 2 3 as Z/3Z). Audit on arrival.
The owner's own lines of #410 are in owner_equals_chain_three_things_brackets_2026_10_22.py.
The 1.137 paste at the top of #410 repeats #409 (pasted_1137_squared_running_sum_audit_2026_10_22.py).

THE PASTES: text from another tool, relayed by the owner. One paste opens with a quotation it
credits to the owner ("2 = 2 isn't an action, it's a statement"); that sentence is not among the
owner's own lines in #410, and nothing below puts it, or any claim of the pastes, in the owner's mouth.

RIGHT:
  x × (−x × (−1)) = x × x
  1.137 × 1.137 = 1.292769
  1.137% = 0.01137; 0.01137 × 0.01137 = 0.0001292769 = 0.01292769%
  75.7% = 0.757; −0.757 × (−1) = 0.757; 0.757 × 0.757 = 0.573049 = 57.3049%
  2 = (2) × 2 = 4 and 2 = 2 × 2 = 4, read with "=" as the same value: the first piece says 2 = 4,
    wrong; (2) × 2 = 4 right; 2 = (2 × 2) ÷ 2 = 4 ÷ 2 right; 2 -> 2 × 2 = 4 right
  the = key table: = same value, ≠ not the same, ≈ close, ≡ the same remainder (10 ≡ 1 by 9)
  13)12)13)12)13 is 12(13(12(13(12 with 12 and 13 swapped and ( turned to ); doing the swap twice
    gives back the first line
  11 × 1 = 11, 11 × 2 = 22, 11 × 3 = 33, 11 × 6 = 66; roots 2, 4, 6, 12 -> 3
  1 2 3 1 2 3 ... repeats every 3

WRONG:
  1. "In mathematics, this exact loop is called a Markov chain": a Markov chain's next step uses
     the present state only -- it forgets what came before. "Remember what is connected to the
     past" needs the one behind as well: next = f(behind, current), a recurrence that looks back
     two (1 1 2 3 5 8: 1+1 = 2, 1+2 = 3, 2+3 = 5). The paste's other name, "recurrence relation",
     is right; "Markov chain" is not.
  2. "an exact time-reversal": reading 12(13(12(13(12 backwards gives 12 13 12 13 12 again (it
     reads the same both ways), not 13 12 13 12 13. The bottom line comes from swapping 12 and 13,
     not from reversing. (The "chiral spins", "absorption", "emission" lines carry no arithmetic.)
  3. "Repunit step ladder": a repunit is all 1s (11, 111, 1111). 22, 33 and 66 are repdigits
     (one digit repeated), not repunits.
  4. The = key table gives ≡ one meaning only; it has a second common one: the same for every
     value (x + x ≡ 2x).

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F

for x in (F(1137, 1000), F(1137, 100000), F(757, 1000), F(-3, 7), F(5)):
    assert x * (-x * -1) == x * x
assert F(1137, 1000) ** 2 == F("1.292769")
assert F(1137, 100000) ** 2 == F("0.0001292769") and F("0.0001292769") * 100 == F("0.01292769")
assert F(757, 1000) ** 2 == F("0.573049") and F("0.573049") * 100 == F("57.3049")

# 2 = (2) x 2 = 4
assert 2 != (2) * 2 and (2) * 2 == 4 and 2 == F(2 * 2, 2) == F(4, 2)

# WRONG 1: Markov forgets the past; looking back two needs it
fib = [1, 1]
for _ in range(4):
    fib.append(fib[-2] + fib[-1])
assert fib == [1, 1, 2, 3, 5, 8]
# the current value 1 comes twice and is followed once by 1 and once by 2:
# the next cannot be read from the current alone -- the one behind decides it
assert (fib[0], fib[1]) == (1, 1) and (fib[1], fib[2]) == (1, 2)
assert all(fib[i + 1] == fib[i] + fib[i - 1] for i in range(1, 5))

# WRONG 2: reversing vs swapping
top = [12, 13, 12, 13, 12]
bottom = [13, 12, 13, 12, 13]
assert top[::-1] == top != bottom
assert [{12: 13, 13: 12}[v] for v in top] == bottom
assert [{12: 13, 13: 12}[v] for v in bottom] == top

# WRONG 3: repunits vs repdigits
def repunit(n):
    return set(str(n)) == {"1"}


def repdigit(n):
    return len(set(str(n))) == 1


assert repunit(11) and not any(repunit(n) for n in (22, 33, 66)) and all(repdigit(n) for n in (11, 22, 33, 66))
assert [11 * k for k in (1, 2, 3, 6)] == [11, 22, 33, 66]

# the = key table and the 1 2 3 cycle
assert 10 % 9 == 1 % 9 and 66 != 33
assert [n % 3 or 3 for n in range(1, 13)] == [1, 2, 3] * 4

if __name__ == "__main__":
    print("#410 pastes: the squares (1.292769, 0.01292769%, 57.3049%) and the 2 = 2 x 2 = 4 reading right; "
          "wrong: 'Markov chain' (it forgets the past; this needs the one behind), 'time-reversal' "
          "(the bottom line is a swap, not a reversal), 'repunit' (22 33 66 are repdigits), ≡ given one meaning of two")

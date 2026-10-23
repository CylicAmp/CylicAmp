# CLASS: AUDIT
"""
The NameError in the script that builds "unified_structural_reinforcement.json", and the pasted calculus reading
(owner_work #426, 2026-10-23). The owner: "If you fixed this skip but if not its not a logic error by me but rather a
Sentax issue." This one had not been fixed before (the earlier NameError, #424, was in simulate_ssr).

THE ERROR:
    184  "partial_sum_to_1e9": round(brun_constant_full - 2 * 0.6601618158468696 / math.log(1e9), 4),
    NameError: name 'brun_constant_full' is not defined
  Right: a missing name, not the logic. Line 183 writes the constant straight into the dictionary
  ("brun_constant": 1.902160583104), so the name brun_constant_full was never made. The fix, before line 79:
        brun_constant_full = 1.902160583104
  and line 183 can then read "brun_constant": brun_constant_full.

TWO NUMBERS IN THE SAME SCRIPT, made right (each changes a value the script writes):
  line 184: the part of Brun's sum past x is about 4 x C2 / ln x (each twin pair adds 1/p + 1/(p + 2), two terms,
    on a density of 2 x C2 / (ln x)^2). With 4:   1.902160583104 - 4 x 0.66016... / ln(10^9) = 1.774736
    -- the sum counted directly over the 3,424,506 pairs below 10^9 is 1.774736 (pasted_bundle_..._audit, #425).
    With the script's 2 it gives 1.838448.
  line 73's comment gives the density of twin primes as C2 / (log x)^2; it is 2 x C2 / (log x)^2 -- the factor 2
  that line 70 then drops.
  line 70: the expected count of twin pairs is 2 x C2 x N / (ln N)^2 (3,074,426), or sharper 3,425,308; with the
    factor 2 in, "ratio ≈ 2.23" becomes 1.114, or 0.99977 with the sharper form (#425).

THE CALCULUS PASTE: it reads "f'(Gz) = (-xG-41" as f'(x) = -x(x - 4), or as f'(x) = -(x - 4), and says f has its
  global maximum at x = 4.
    f'(x) = -(x - 4):    f = -(x - 4)^2 / 2 + c, highest at x = 4 for every x -- right
    f'(x) = -x(x - 4):   f = -x^3 / 3 + 2 x^2 + c; f' = 0 at x = 0 and x = 4; x = 4 is the highest point near it,
                         but f keeps growing as x goes down past 0 (f(-10) = 533.3 + c > f(4) = 10.67 + c), so on
                         all numbers x = 4 is not the global maximum; it is on x >= 0 (or any interval where the
                         ends are lower)
  Which reading is meant, and the interval, decide it; the problem as first written is not in the message.

FALSIFICATION: any assertion failing.
"""
import math
from fractions import Fraction as F

C2 = 0.6601618158468696
brun_constant_full = 1.902160583104
L = math.log(1e9)
partial_4 = brun_constant_full - 4 * C2 / L
partial_2 = brun_constant_full - 2 * C2 / L
direct = 1.7747359576385369          # pasted_bundle_mod37_twins_g5_audit_2026_10_23.py, summed over 3,424,506 pairs
assert round(partial_4, 6) == 1.774736 == round(direct, 6)
assert round(partial_2, 6) == 1.838448
assert round(2 * C2 * 1e9 / L ** 2) == 3_074_426 and round(3_424_506 / (2 * C2 * 1e9 / L ** 2), 3) == 1.114


# the calculus readings
def f_b(x):            # f'(x) = -x(x - 4) = -x^2 + 4x
    return -F(x) ** 3 / 3 + 2 * F(x) ** 2


def fprime_b(x):
    return -x * (x - 4)


assert [x for x in range(-20, 21) if fprime_b(x) == 0] == [0, 4]
assert fprime_b(-1) < 0 < fprime_b(1) and fprime_b(3) > 0 > fprime_b(5)          # 0 is a low point, 4 a high one
assert f_b(4) == F(32, 3) and f_b(-10) == F(1000, 3) + 200 and f_b(-10) > f_b(4)    # not the highest on all numbers
assert all(f_b(x) <= f_b(4) for x in [F(k, 10) for k in range(0, 200)])              # highest on x >= 0
assert all(-(F(x) - 4) ** 2 / 2 <= 0 for x in range(-50, 50))                         # f'(x) = -(x - 4): highest at 4

if __name__ == "__main__":
    print("NameError: add brun_constant_full = 1.902160583104; with 4 x C2 the line gives 1.774736 = the direct sum; "
          "calculus: x = 4 is the global maximum for f' = -(x - 4), only a local one for f' = -x(x - 4) on all numbers")

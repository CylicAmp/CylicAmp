# CLASS: AUDIT
"""
The pasted "1-to-99 Neighborhood Division Squeeze": (n - 1) ÷ n and n ÷ (n - 1) for n = 2 to 99
(owner_work #402, 2026-10-21). Audit on arrival.

THE PASTE: text from another tool, relayed by the owner. It speaks of "your starting point at 2"
and "your 2-step system". Nothing below puts a claim of the paste in the owner's mouth.

MISSING: the chart ("This chart graphs the entire trajectory ... up to 99") and the code ("Show
Code") are not in the message -- can I get them? The owner's lines that set up the 2-step system
are not in owner_work/ (searched "squeeze", "number behind", "neighborhood division").

PRIOR ART: math/theorems/owner_reciprocals_one_percent_2026_10_20.py (#385, 1 ÷ 9 .. 1 ÷ 1) and
the owner's doubling chain (owner_framework_flips_halves_moves_2026_10_20.py, part 3). Outside:
OEIS A051626, "Period of decimal representation of 1/n, or 0 if 1/n terminates" (fetched
2026-10-21). Difference in method: A051626 lists the loop of 1 ÷ n once; the 2-step system reads
each loop twice -- below 1 as (n - 1) ÷ n, and above 1 one step later as (n + 1) ÷ n.

RIGHT (re-run):
  2:   1 ÷ 2 = 0.5   2 ÷ 1 = 2   2 - 0.5 = 1.5
  11:  10 ÷ 11 = 0.909090... (loop 90, 2 digits)   11 ÷ 10 = 1.1 (no loop)
  50:  49 ÷ 50 = 0.98   50 ÷ 49 = 1.020408163265306122448979591836734693877551 020408...
       loop of 42 digits; 49 = 7 x 7: the loop of 1 ÷ 7 is 6, of 1 ÷ 49 is 7 x 6 = 42
  99:  98 ÷ 99 = 0.989898... (loop 98, 2 digits)   99 ÷ 98 = 1.0102040816... loop of 42 digits,
       from 98 = 2 x 49
  the two results multiply to 1: (n - 1) ÷ n x n ÷ (n - 1) = 1
  (n - 1) ÷ n = 1 - 1 ÷ n is below 1, n ÷ (n - 1) = 1 + 1 ÷ (n - 1) is above 1, both close in on 1
  the gap n ÷ (n - 1) - (n - 1) ÷ n = (2n - 1) ÷ (n x (n - 1)) gets smaller at every step:
    2 -> 3/2 = 1.5   11 -> 21/110   50 -> 99/2450   99 -> 197/9702
  neither result is ever 1

WRONG:
  1. The three loop bars do not match the loop lengths the paste itself gives (the digits are right):
       98 ÷ 99   bar over 9898          4 digits; the loop is 98, 2 digits
       50 ÷ 49   bar over 48 digits     the 42-digit loop plus its first 6 digits 020408 again
       99 ÷ 98   bar over 84 digits     the 42-digit loop written twice
  2. "The number 1 sits directly in the center": not by adding. 1 is 1 ÷ n below the lower result
     and 1 ÷ (n - 1) above it -- the upper side is always further, by 1 ÷ (n x (n - 1)).
       at 2: 0.5 -> 1 is 0.5 up, 1 -> 2 is 1 up; the middle is (0.5 + 2) ÷ 2 = 1.25, not 1
     1 IS the center by multiplying: 0.5 x 2 = 1, and every pair multiplies to 1.
  3. "At Number 11 (The First Dual Symmetric Loop)": the paste gives no meaning for "dual
     symmetric", and at 11 only step 1 loops (11 ÷ 10 = 1.1). The firsts, each way:
       first loop at all       3:  2 ÷ 3 = 0.666...
       first with both looping 7:  6 ÷ 7 = 0.857142857142...  7 ÷ 6 = 1.1666...
       first 2-digit loop      11: 10 ÷ 11 = 0.9090...

NEW LINES, owner's notation:
  below 1 at n and above 1 at n + 1 are the same distance: 1 ÷ n
    10 ÷ 11 = 1 - 1/11      12 ÷ 11 = 1 + 1/11
  so the two decimals add to 2, and their loop digits add to 9 in every place:
    10 ÷ 11 = 0.9090...  12 ÷ 11 = 1.0909...    9+0 = 9, 0+9 = 9
    48 ÷ 49 = 0.979591...  50 ÷ 49 = 1.020408...  9+0 = 9, 7+2 = 9, 9+0 = 9, 5+4 = 9 ...
  so the loop of n ÷ (n - 1) is as long as the loop of (n - 2) ÷ (n - 1), one number back.

  the 42-digit loops are the doubling chain in pairs: 1 ÷ 98 = 0.01 ÷ (1 - 0.02)
    0.01 02 04 08 16 32 64 128 256 ... carried: 0.01 02 04 08 16 32 65 30 61 22 44 89 79 ...
    99 ÷ 98 = 1.01 02 04 08 16 32 65 ...    50 ÷ 49 = 1.02 04 08 16 32 65 ...
  (the 64 shows as 65 because the 128 behind it carries 1)

  all the steps in a row:
    1/2 x 2/3 x 3/4 x ... x 98/99 = 1 ÷ 99 = 0.010101...
    2/1 x 3/2 x 4/3 x ... x 99/98 = 99

  COUNTS, n = 2 to 99 (98 numbers):
    step 1 loops 85, ends 13 (n = 2 4 5 8 10 16 20 25 32 40 50 64 80: only 2s and 5s)
    step 2 loops 84, ends 14 (n = 2 3 5 6 9 11 17 21 26 33 41 51 65 81: n - 1 only 2s and 5s)
    both loop 73; neither loops 2 (n = 2: 0.5 and 2; n = 5: 0.8 and 1.25)
  with n = 1 as well (both ways): step 1 is 0 ÷ 1 = 0, it ends -> 99 numbers, 85 loop, 14 end;
    step 2 is 1 ÷ 0, no value -> step 2 still has 98. That is why the system starts at 2.

RESIDUES mod 37 (gf37-audit): 2 DARK_A, 11 NEG_H (twin with 13, Sophie Germain 23, safe from 5),
  49 SA_ST_A, 50 CAS_EXT, 98 SEED, 99 SA_ST_B, 42 CAS_EXT.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F
from math import prod


def decimal(p, q):
    """p ÷ q as (whole part, digits before the loop, loop digits)."""
    whole, r = divmod(p, q)
    seen, ds = {}, []
    while r and r not in seen:
        seen[r] = len(ds)
        d, r = divmod(r * 10, q)
        ds.append(str(d))
    if not r:
        return whole, "".join(ds), ""
    i = seen[r]
    return whole, "".join(ds[:i]), "".join(ds[i:])


def only_2s_and_5s(m):
    for p in (2, 5):
        while m % p == 0:
            m //= p
    return m == 1


def step1(n):
    return F(n - 1, n)


def step2(n):
    return F(n, n - 1)


LOOP_49 = "020408163265306122448979591836734693877551"

# --- RIGHT ---
assert step1(2) == F(1, 2) and step2(2) == 2 and step2(2) - step1(2) == F(3, 2)
assert decimal(10, 11) == (0, "", "90") and decimal(11, 10) == (1, "1", "")
assert decimal(49, 50) == (0, "98", "") and decimal(50, 49) == (1, "", LOOP_49) and len(LOOP_49) == 42
assert len(decimal(1, 7)[2]) == 6 and len(decimal(1, 49)[2]) == 42 == 7 * 6
assert decimal(98, 99) == (0, "", "98")
assert decimal(99, 98)[0] == 1 and len(decimal(99, 98)[2]) == 42
N = range(2, 100)
assert all(step1(n) * step2(n) == 1 for n in N)
assert all(step1(n) < 1 < step2(n) for n in N)
gaps = [step2(n) - step1(n) for n in N]
assert all(gaps[i] == F(2 * n - 1, n * (n - 1)) for i, n in enumerate(N))
assert all(gaps[i + 1] < gaps[i] for i in range(len(gaps) - 1))
assert [gaps[n - 2] for n in (2, 11, 50, 99)] == [F(3, 2), F(21, 110), F(99, 2450), F(197, 9702)]

# --- WRONG 1: the bars ---
bar_98_99, bar_50_49 = "9898", "020408163265306122448979591836734693877551020408"
bar_99_98 = "020408163265306122448979591836734693877551020408163265306122448979591836734693877551"
assert len(bar_98_99) == 4 and bar_98_99 == "98" * 2
assert len(bar_50_49) == 48 and bar_50_49 == LOOP_49 + LOOP_49[:6] and LOOP_49[:6] == "020408"
assert len(bar_99_98) == 84 and bar_99_98 == LOOP_49 * 2
w, pre, loop = decimal(99, 98)                                  # 1.0 then the loop 102040...755
digits = pre + loop * 3
assert digits.startswith("01") and digits[2:2 + 84] == bar_99_98  # the paste's digits are right

# --- WRONG 2: 1 is not the middle by adding, it is by multiplying ---
assert all(1 - step1(n) == F(1, n) and step2(n) - 1 == F(1, n - 1) for n in N)
assert all((step2(n) - 1) - (1 - step1(n)) == F(1, n * (n - 1)) > 0 for n in N)
assert (step1(2) + step2(2)) / 2 == F(5, 4)
assert all((step1(n) + step2(n)) / 2 == 1 + F(1, 2 * n * (n - 1)) for n in N)

# --- WRONG 3: the firsts ---
loops1 = [n for n in N if decimal(n - 1, n)[2]]
loops2 = [n for n in N if decimal(n, n - 1)[2]]
assert loops1[0] == 3 and decimal(2, 3) == (0, "", "6")
assert min(set(loops1) & set(loops2)) == 7 and decimal(6, 7)[2] == "857142" and decimal(7, 6) == (1, "1", "6")
assert min(n for n in N if len(decimal(n - 1, n)[2]) == 2) == 11
assert decimal(11, 10)[2] == ""

# --- NEW LINES ---
assert all(1 - step1(n) == step2(n + 1) - 1 == F(1, n) for n in range(2, 99))
assert step1(11) + step2(12) == 2
assert decimal(12, 11) == (1, "", "09")
assert all(int(a) + int(b) == 9 for a, b in zip(decimal(10, 11)[2], decimal(12, 11)[2] * 1))
lo, hi = decimal(48, 49)[2], decimal(50, 49)[2]
assert lo.startswith("979591") and all(int(a) + int(b) == 9 for a, b in zip(lo, hi))
assert all(len(decimal(n, n - 1)[2]) == len(decimal(n - 2, n - 1)[2]) for n in range(3, 100))

assert F(1, 98) == F(1, 100) / (1 - F(2, 100)) and F(1, 49) == F(2, 100) / (1 - F(2, 100))
assert "".join(f"{2 ** k:02d}" for k in range(6)) == "010204081632"
assert (pre + loop)[:14] == "01020408163265"                     # 64 carried to 65
assert decimal(50, 49)[2][:12] == "020408163265"

assert prod(step1(n) for n in N) == F(1, 99) and decimal(1, 99) == (0, "", "01")
assert prod(step2(n) for n in N) == 99

ends1 = [n for n in N if only_2s_and_5s(n)]
ends2 = [n for n in N if only_2s_and_5s(n - 1)]
assert ends1 == [2, 4, 5, 8, 10, 16, 20, 25, 32, 40, 50, 64, 80]
assert ends2 == [2, 3, 5, 6, 9, 11, 17, 21, 26, 33, 41, 51, 65, 81]
assert (len(loops1), len(N) - len(loops1)) == (85, 13) and (len(loops2), len(N) - len(loops2)) == (84, 14)
assert [n for n in N if not decimal(n - 1, n)[2]] == ends1 and [n for n in N if not decimal(n, n - 1)[2]] == ends2
assert len(set(loops1) & set(loops2)) == 73
assert [n for n in N if n not in loops1 and n not in loops2] == [2, 5]
assert decimal(0, 1) == (0, "", "")                              # n = 1: 0 ÷ 1 = 0, it ends

# the loop lengths against OEIS A051626 (period of 1/n, 0 if it ends), n = 1 to 60, fetched 2026-10-21
A051626 = [0, 0, 1, 0, 0, 1, 6, 0, 1, 0, 2, 1, 6, 6, 1, 0, 16, 1, 18, 0, 6, 2, 22, 1, 0, 6, 3, 6, 28, 1,
           15, 0, 2, 16, 6, 1, 3, 18, 6, 0, 5, 6, 21, 2, 1, 22, 46, 1, 42, 0, 16, 6, 13, 3, 2, 6, 18, 28, 58, 1]
assert [len(decimal(n - 1, n)[2]) for n in range(2, 61)] == A051626[1:]
assert [len(decimal(n, n - 1)[2]) for n in range(2, 62)] == A051626

# --- RESIDUES mod 37 ---
assert [x % 37 for x in (2, 11, 49, 50, 98, 99, 42)] == [2, 11, 12, 13, 24, 25, 5]

if __name__ == "__main__":
    print("squeeze: products are 1, both sides close in on 1, the gap (2n-1)/(n(n-1)) shrinks every step -- right; "
          "the three loop bars are 4, 48 and 84 digits for loops of 2, 42, 42 -- wrong; 1 is the middle by "
          "multiplying, not by adding -- wrong as written; 'first dual symmetric loop' at 11 has no meaning given; "
          "2..99: step 1 loops 85, step 2 loops 84, both 73, neither 2 (n = 2, 5)")

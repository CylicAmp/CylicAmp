# CLASS: AUDIT
"""
Pasted audit of the 99-row consecutive-integer sums S(n) = n + (n+1) = 2n + 1, n = 1..99 (2026-11-22). The paste's range
and operator lines came through blank; the rows it uses are 3, 5, 7, ..., 199. Audit on arrival. Every number RIGHT:

  total 2 x 4950 + 99 = 99 x (3 + 199)/2 = 9999 = 3^2 x 11 x 101 = 99 x 101, root 9
  S(n) + S(100 - n) = 202: 3 + 199, 37 + 165, 73 + 129, 99 + 103, 101 + 101; 49 x 202 + 101 = 9999
  S(n + 9) = S(n) + 18, so roots repeat 3 5 7 9 2 4 6 8 1; 99 rows = 11 cycles, each root 11 times, 11 x 45 = 495 -> 9
  2n + 1 a multiple of 37 exactly when n leaves 18 by 37: n = 18, 55, 92 -> 37, 111, 185 (roots 1, 3, 5);
  S(18 + 37k) = 37(2k + 1), roots step by 2 (37 leaves 1 by 9)
  T(N) = N(N + 2) = (N + 1)^2 - 1: 99, 399, 2499, 9999, 999999, 99999999; T(10^k - 1) = 10^(2k) - 1
No fault changes a number. No earlier file holds this 99-row construction itself (grep, 2026-11-22); it connects to:

CONNECTIONS (each asserted below):
  1. odds_sum_even_audit_2026_10_18.py (#340): 1 + 3 + ... + (2n - 1) = n^2. The rows are the odd numbers from 3, so
     T(N) = (N + 1)^2 - 1 is that square without its 1 -- reinforces. Your 9, 36, 81 there (the first 3, 6, 9 odds)
     come back as T(2) + 1, T(5) + 1, T(8) + 1.
  2. owner_1125_1137_ones_by_zeros_2026_10_19.py (#368, ones separated by zeros 11, 101, 1001, 10001 = 73 x 137):
     T(10^k - 1) = (10^k - 1)(10^k + 1), so the nines in the table are 9 x 11, 99 x 101, 999 x 1001, 9999 x 10001.
     The 99-row total 9999 = 99 x 101 with 101 the middle row; 99,999,999 = 9999 x 73 x 137 -- explains the nines.
  3. twin_prime_consolidation.py (T385, twin product (6n - 1)(6n + 1) = 36n^2 - 1): T(6n - 1) = 36n^2 - 1, so every
     twin pair (p, p + 2) is a row total, T(p) = p(p + 2), and T(p) + 1 = (p + 1)^2 = 36n^2: 15, 35, 143, 323, 899, ...
     -- hands the totals to the twin-prime thread.
  4. theorem_364_complement_involution_3663.py (C(X) = 9999 - X) and michael_prime_crt.py (mirror 9999 - p): the total
     9999 is that complement constant; the row mirror S(n) + S(100 - n) = 202 is the same kind of fold, x -> 202 - x.
  5. ap_147_step20_audit.py (2026-10-02): the same root cycle 3 5 7 9 2 4 6 8 1, because steps 2 and 20 both leave 2 by 9
     -- reinforces.
  6. owner_369_729_189_rotations_flips_2026_11_19.py (What's not 369): 33 of the 99 rows land on 3, 6 or 9 (n leaving 1
     by 3), 66 do not.

FALSIFICATION: any assertion failing.
"""
S = lambda n: n + (n + 1)
dr = lambda n: 1 + (n - 1) % 9
rows = [S(n) for n in range(1, 100)]
assert rows[0] == 3 and rows[-1] == 199 and sum(rows) == 9999 == 99 * 101 == 9 * 11 * 101 and dr(9999) == 9
assert 2 * 4950 + 99 == 9999 == 99 * (3 + 199) // 2
assert all(S(n) + S(100 - n) == 202 for n in range(1, 100)) and 49 * 202 + 101 == 9999 and S(50) == 101 and S(49) == 99
assert all((a, b) in {(S(n), S(100 - n)) for n in range(1, 100)} for a, b in ((3, 199), (37, 165), (73, 129), (99, 103), (101, 101)))
assert [dr(S(n)) for n in range(1, 10)] == [3, 5, 7, 9, 2, 4, 6, 8, 1] and all(S(n + 9) == S(n) + 18 for n in range(1, 91))
assert all([dr(r) for r in rows].count(d) == 11 for d in range(1, 10)) and dr(11 * 45) == 9
assert [n for n in range(1, 100) if S(n) % 37 == 0] == [18, 55, 92] and [S(n) for n in (18, 55, 92)] == [37, 111, 185]
assert [dr(v) for v in (37, 111, 185)] == [1, 3, 5] and all(S(18 + 37 * k) == 37 * (2 * k + 1) for k in range(100))
assert [dr(37 * (2 * k + 1)) for k in range(9)] == [1, 3, 5, 7, 9, 2, 4, 6, 8]
T = lambda N: sum(S(n) for n in range(1, N + 1))
assert all(T(N) == N * (N + 2) == (N + 1) ** 2 - 1 for N in range(1, 300))
assert [T(N) for N in (9, 19, 49, 99, 999, 9999)] == [99, 399, 2499, 9999, 999999, 99999999]
assert all(T(10 ** k - 1) == 10 ** (2 * k) - 1 for k in range(1, 6))

# CONNECTIONS
import pathlib
from sympy import factorint, isprime
TH = pathlib.Path(__file__).resolve().parent
assert all(sum(range(1, 2 * n, 2)) == n * n for n in range(1, 200)) and all(T(N) + 1 == sum(range(1, 2 * N + 2, 2)) for N in range(1, 200))
assert [T(N) + 1 for N in (2, 5, 8)] == [9, 36, 81]
assert [T(10 ** k - 1) for k in (1, 2, 3, 4)] == [9 * 11, 99 * 101, 999 * 1001, 9999 * 10001] and factorint(10001) == {73: 1, 137: 1}
assert S(50) == 101 and T(9999) == 99999999 == 9999 * 73 * 137
twins = [q for q in range(3, 2000) if isprime(q) and isprime(q + 2)]
assert all(T(q) == q * (q + 2) and T(q) + 1 == (q + 1) ** 2 for q in twins) and all(T(6 * n - 1) == 36 * n * n - 1 for n in range(1, 500))
assert [T(q) for q in twins[:5]] == [15, 35, 143, 323, 899] and all((q + 1) % 6 == 0 for q in twins[1:])
assert T(99) == 9999 and all(S(n) + S(100 - n) == 202 for n in range(1, 100))
assert [dr(147 + 20 * k) for k in range(9)] == [3, 5, 7, 9, 2, 4, 6, 8, 1] == [dr(S(n)) for n in range(1, 10)] and 20 % 9 == 2 % 9
assert sum(1 for r in rows if dr(r) in (3, 6, 9)) == 33 and all((dr(S(n)) in (3, 6, 9)) == (n % 3 == 1) for n in range(1, 100))
for f in ("odds_sum_even_audit_2026_10_18.py", "owner_1125_1137_ones_by_zeros_2026_10_19.py", "twin_prime_consolidation.py",
          "theorem_364_complement_involution_3663.py", "ap_147_step20_audit.py", "owner_369_729_189_rotations_flips_2026_11_19.py"):
    assert (TH / f).exists(), f
assert (TH.parents[1] / "michael_prime_crt.py").exists()

if __name__ == "__main__":
    print("99-row consecutive sums: every number right; total 9999; T(N) = (N+1)^2 - 1")

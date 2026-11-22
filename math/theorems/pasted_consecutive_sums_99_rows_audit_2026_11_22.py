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
No fault changes a number. Prior work: none in the repo on this 99-row construction (grep, 2026-11-22).

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

if __name__ == "__main__":
    print("99-row consecutive sums: every number right; total 9999; T(N) = (N+1)^2 - 1")

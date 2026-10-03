# CLASS: AUDIT
"""
Audit of a supplied Rust program, "clusters_search_final.rs" (2026-10-02),
that searches for m <= bound with m | sigma_2(m).  The source is kept in
tools/supplied/clusters_search_final_condensed.rs (same code, condensed
formatting, plus output of the solution list).

PRIOR ART: OEIS A046762, "Numbers k such that the sum of the squares of the
divisors of k is divisible by k" (1, 10, 60, 65, 84, 130, ...), b-file with
3200 terms up to 86651428500.  Cited there: the sequence is infinite and
sigma_2(n)/n is unbounded, with finitely many n for each ratio (Cai, Chen,
Zhang, Int. J. Number Theory 2015; Amer. Math. Monthly Problem 11090, 2006).

RESULTS (program compiled with cargo --release and run here)
  bound    true count   program   missed   false positives
  10^6        114          114        0          0
  10^9        972          969        3          0
  10^10      1807         1799        8          0
Every value it prints is a genuine solution; it is NOT a complete list.

DEFECTS
 D1 The "optimized bound" branch: if new_prod*q > bound it only tests
    new_prod and never extends it by other primes.  Removing that branch
    recovers 2 of the 3 misses below 10^9 (804770757, 978134072).  Symptom:
    those two ARE found when the bound is 10^10 -- results below 10^9 depend on
    the bound chosen.
 D2 The tree is incomplete in principle: it only multiplies by a NEW prime q
    that divides sigma_2(current product), starting from seeds <= 10000, and
    never raises an exponent already present.  248183272 = 2^3*17*31*37^2*43
    is missed even with D1 removed.
 D3 `s2_prod.min(U128::MAX) as U64` truncates: min with U128::MAX does
    nothing and the cast keeps the low 64 bits once sigma_2 > 2^64: always
    for products above 2^32 ~ 4.3e9 (sigma_2(n) > n^2), sooner for products
    with many divisors.  The candidate primes then come from a wrong
    number.  The advertised run to 10^12 is affected throughout.
 D4 factor() trial-divides only by primes <= 10^6 and reports the leftover as
    a prime; for the (truncated) sigma_2 values up to 1.8e19 that leftover can
    be composite, giving non-prime "candidates".
 D5 `q.pow(e)` wraps silently in release builds on overflow (2^64 and up).
 D6 The LOCKED table and find_locked are never used; no threads are started
    (Arc/Mutex are present, the search is single-threaded); every product is
    revisited from many seeds (6.9 million nodes for 971 solutions at 10^9
    without D1).
What gives a complete list: a sigma_2 sieve (every m up to the bound), which
is how the reference counts here were confirmed to 10^6, and the OEIS b-file
above that.

CONNECTION: T245 (theorem_245_n130_divisor_square_sum_gf37.py) asks for n equal
to the sum of the squares of its k SMALLEST divisors; sigma_2 is the sum over
ALL divisors.  130 is the T245 k=4 solution and is also in A046762:
sigma_2(130) = 22100 = 170 * 130.

FALSIFICATION: any assertion failing.
"""
import os

from sympy import divisor_sigma, factorint

HERE = os.path.dirname(os.path.abspath(__file__))
REF = [int(l) for l in open(os.path.join(HERE, "data_A046762_le_1e10.txt")) if l.strip() and not l.startswith("#")]
REF = [x for x in REF if x > 1]
assert REF[:10] == [10, 60, 65, 84, 130, 140, 150, 175, 260, 350]

# reference counts; the 10^6 count also by a direct sieve
N = 10 ** 6
s = [0] * (N + 1)
for d in range(1, N + 1):
    for k in range(d, N + 1, d):
        s[k] += d * d
sieve = [m for m in range(2, N + 1) if s[m] % m == 0]
assert sieve == [x for x in REF if x <= N] and len(sieve) == 114
assert sum(1 for x in REF if x <= 10 ** 9) == 972 and sum(1 for x in REF if x <= 10 ** 10) == 1807

MISSED_1E9 = [248183272, 804770757, 978134072]
MISSED_1E10 = [248183272, 1622670250, 1824877000, 2775637917, 5551275834,
               6490681000, 7197314888, 9736021500]
for m in sorted(set(MISSED_1E9 + MISSED_1E10)):
    assert divisor_sigma(m, 2) % m == 0 and m in REF        # genuine solutions
assert factorint(248183272) == {2: 3, 17: 1, 31: 1, 37: 2, 43: 1}
assert 969 == 972 - len(MISSED_1E9) and 1799 == 1807 - len(MISSED_1E10)
assert set(MISSED_1E9) - set(MISSED_1E10) == {804770757, 978134072}  # found at 10^10, missed at 10^9 (D1)

# D3: sigma_2 exceeds 2^64 well inside the advertised range
n = 2 ** 32 + 15                       # sigma_2(n) > n^2 > 2^64
assert n * n > 2 ** 64 and divisor_sigma(n, 2) > 2 ** 64
assert min(m for m in range(10 ** 9, 5 * 10 ** 9, 10 ** 8) if divisor_sigma(m, 2) > 2 ** 64) < 2 ** 32  # sooner when divisor-rich
assert int(divisor_sigma(n, 2)) % 2 ** 64 != divisor_sigma(n, 2)

assert divisor_sigma(130, 2) == 22100 == 170 * 130 and 130 in REF        # connection

if __name__ == "__main__":
    print("sigma_2 Rust audit: outputs genuine but incomplete (misses 3 <= 1e9, 8 <= 1e10); defects D1-D6")

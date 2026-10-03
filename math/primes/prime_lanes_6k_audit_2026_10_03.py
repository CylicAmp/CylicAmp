"""Audit of supplied code (2026-10-03): generate_prime_lanes, the 6k-1 / 6k+1 lane sieve.

Verdict:
  P1 CORRECT for K >= 1. Output = all primes <= 6K+1, checked against trial division for K = 1..400
     and K = 2000. Why it is complete: a composite n with gcd(n,6)=1 factors as a*b with
     a,b >= 5 and gcd(ab,6)=1, so each factor is 6i-1 or 6i+1, with i <= K; the three
     product forms cover every pairing ((6i+1)(6j-1) is c2 with i,j swapped).
  P2 "without division" -- true: it uses only products and set membership. It is a sieve,
     not a primality test; any sieve is "deterministic".
  P3 Cost: K^2 products, but only pairs with (6i-1)(6j-1) <= 6K+1 matter, i.e. about
     (K/6) ln K of them. For K = 2000 the loop forms 12,000,000 products and keeps
     WORK_USED (below); bounding j by (6K+1)//(6i-1) gives the same output.
  P4 Edges: m > 1 and p > 1 are always true (m >= 5); harmless. K = 0 is a real (small)
     defect: the bound is 6*0+1 = 1, yet [2, 3] is returned -- 2 and 3 are hard-coded
     whatever the limit. Correct for every K >= 1.
  P5 Twin primes: a lane pair (6k-1, 6k+1) with both survivors is exactly a twin pair
     other than (3,5). The indices k are OEIS A002822 ("6m-1, 6m+1 are twin primes"),
     where Jon Perry (2002) records: twin iff k is not of the form 6ab +- a +- b. That is
     this sieve's product set rewritten in k -- checked below for k <= 2000.
Prior art in this repo: math/primes/prime_engine.py (DR filter = 6k+-1 wheel) and
T250 (theorem_250_n250_twin_prime_engine_gf37.py, twin pairs at 6k_m +- 1).
"""


# ---- supplied code, verbatim ----
def generate_prime_lanes(limit_k: int):
  """Partitions the integer line into twin deterministic lanes (6k - 1, 6k + 1)

  and filters composites via coordinate indexing without division.
  """
  lane_minus = [6 * k - 1 for k in range(1, limit_k + 1)]
  lane_plus = [6 * k + 1 for k in range(1, limit_k + 1)]

  # Identify composite positions without trial division
  composites = set()
  for i in range(1, limit_k + 1):
    for j in range(1, limit_k + 1):
      c1 = (6 * i - 1) * (6 * j - 1)
      c2 = (6 * i - 1) * (6 * j + 1)
      c3 = (6 * i + 1) * (6 * j + 1)
      for c in (c1, c2, c3):
        if c <= 6 * limit_k + 1:
          composites.add(c)

  # Deterministic prime output from lanes
  primes = [2, 3]
  for m, p in zip(lane_minus, lane_plus):
    if m not in composites and m > 1:
      primes.append(m)
    if p not in composites and p > 1:
      primes.append(p)

  return sorted(primes)
# ---- end supplied code ----


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def lanes_bounded(K):
    """Same sieve, j bounded so only products <= 6K+1 are formed."""
    N = 6 * K + 1
    comp = set()
    for i in range(1, K + 1):
        a, b = 6 * i - 1, 6 * i + 1
        if a * a > N:
            break
        for j in range(1, N // a // 6 + 2):
            for c in (a * (6 * j - 1), a * (6 * j + 1), b * (6 * j + 1), b * (6 * j - 1)):
                if c <= N:
                    comp.add(c)
    return [2, 3] + [n for k in range(1, K + 1) for n in (6 * k - 1, 6 * k + 1) if n not in comp]


assert generate_prime_lanes(15) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                                    59, 61, 67, 71, 73, 79, 83, 89]
assert generate_prime_lanes(0) == [2, 3]          # P4: should be [] for bound 1
assert [n for n in range(2, 2) if is_prime(n)] == []
for K in range(1, 401):
    assert generate_prime_lanes(K) == [n for n in range(2, 6 * K + 2) if is_prime(n)], K
K = 2000
REF = [n for n in range(2, 6 * K + 2) if is_prime(n)]
assert generate_prime_lanes(K) == REF
assert lanes_bounded(K) == REF
WORK_USED = sum(1 for i in range(1, K + 1) for j in range(1, K + 1)
                if (6 * i - 1) * (6 * j - 1) <= 6 * K + 1)
assert WORK_USED < 3000, WORK_USED          # vs 4,000,000 (i,j) pairs looped

# P5: twin lanes <-> k not of the form 6ab +- a +- b  (A002822, Perry 2002)
KMAX = 2000
twin_k = {k for k in range(1, KMAX + 1) if is_prime(6 * k - 1) and is_prime(6 * k + 1)}
forms = set()
for a in range(1, KMAX + 1):
    for b in range(1, KMAX + 1):
        if 6 * a * b - a - b > KMAX:
            break
        for v in (6 * a * b + a + b, 6 * a * b - a - b, 6 * a * b + a - b, 6 * a * b - a + b):
            if 1 <= v <= KMAX:
                forms.add(v)
assert twin_k == set(range(1, KMAX + 1)) - forms
assert sorted(twin_k)[:12] == [1, 2, 3, 5, 7, 10, 12, 17, 18, 23, 25, 30]   # A002822 start

if __name__ == "__main__":
    print(generate_prime_lanes(15))
    print(f"P1 correct for K=1..400 and K=2000 ({len(REF)} primes <= {6*K+1})")
    print(f"P3 pairs that matter at K=2000: {WORK_USED} of {K*K:,} looped")
    print(f"P5 twin lanes k<= {KMAX}: {len(twin_k)}, = complement of 6ab+-a+-b (A002822)")

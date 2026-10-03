"""
Grid G(r, c) = 9r + c, r = 0..8, c = 1..9 (the numbers 1..81), with the
collapse (digital root), P3 = [3 divides n] and the prime types applied.

Standalone: plain Python 3, no libraries. Run:  python3 grid81_standalone.py
Every check prints PASS or FAIL. Claims about primes are checked on the grid
AND on every number up to LIMIT.
"""

LIMIT = 1_000_000


def dr(n):                      # collapse: repeated digit sum, 1..9
    return 1 + (n - 1) % 9


def digit_sum_collapse(n):      # same thing done the slow way, to cross-check dr
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def sieve(n):
    flags = bytearray([1]) * (n + 1)
    flags[0] = flags[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if flags[i]:
            flags[i * i::i] = bytearray(len(flags[i * i::i]))
    return flags


IS_P = sieve(2 * LIMIT + 10)
def isprime(n): return n >= 2 and IS_P[n] == 1

results = []
def check(name, ok):
    results.append(ok)
    print(("PASS  " if ok else "FAIL  ") + name)


G = {(r, c): 9 * r + c for r in range(9) for c in range(1, 10)}
grid_primes = [n for n in range(1, 82) if isprime(n)]

check("dr formula equals repeated digit sum for n = 1..LIMIT",
      all(dr(n) == digit_sum_collapse(n) for n in range(1, LIMIT + 1)))
check("1. column c is exactly the collapse class c",
      all(dr(v) == c for (r, c), v in G.items()))
check("1. subtracting 9 moves up one row in the same column",
      all(G[r, c] - 9 == G[r - 1, c] for r in range(1, 9) for c in range(1, 10)))
check("2. 3 divides n exactly on columns 3, 6, 9",
      all((v % 3 == 0) == (c in (3, 6, 9)) for (r, c), v in G.items()))
check("3. grid has 22 primes", len(grid_primes) == 22)
check("3. only prime in columns 3, 6, 9 is 3 (up to LIMIT)",
      [p for p in range(2, LIMIT) if isprime(p) and dr(p) in (3, 6, 9)] == [3])

twins = [(p, p + 2) for p in range(5, LIMIT) if isprime(p) and isprime(p + 2)]
check("4. twin pairs p > 3 move only 2->4, 5->7, 8->1 (up to LIMIT)",
      {(dr(p), dr(q)) for p, q in twins} == {(2, 4), (5, 7), (8, 1)})

sophie = [p for p in range(5, LIMIT) if isprime(p) and isprime(2 * p + 1)]
check("5. Sophie Germain primes p > 3 lie only in columns 2, 5, 8 (up to LIMIT)",
      {dr(p) for p in sophie} == {2, 5, 8})
check("5. Sophie column map: 2->5, 5->2, 8->8 (up to LIMIT)",
      {(dr(p), dr(2 * p + 1)) for p in sophie} == {(2, 5), (5, 2), (8, 8)})

sexy = [p for p in range(5, LIMIT) if isprime(p) and isprime(p + 6)]
check("6. sexy pairs shift the column by 6 (up to LIMIT)",
      {(dr(p), dr(p + 6)) for p in sexy} == {(1, 7), (2, 8), (4, 1), (5, 2), (7, 4), (8, 5)})

check("7. row sums = 81r + 45",
      all(sum(G[r, c] for c in range(1, 10)) == 81 * r + 45 for r in range(9)))
check("7. column sums = 324 + 9c",
      all(sum(G[r, c] for r in range(9)) == 324 + 9 * c for c in range(1, 10)))

print()
print("twin pairs found:", len(twins), " Sophie primes:", len(sophie), " sexy pairs:", len(sexy))
print("ALL PASS" if all(results) else "SOME CHECKS FAILED")

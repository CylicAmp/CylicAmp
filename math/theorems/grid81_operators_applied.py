# CLASS: THEOREM
"""
The 9x9 grid G(r, c) = 9r + c (r = 0..8, c = 1..9) with the collapse, P3 and the
prime types applied to every cell.

 1. Column c is exactly the collapse class c: dr(9r + c) = c. The operator
    R(n) = n - 9 moves up one row inside the same column.
 2. P3(n) = [3 | n] holds exactly on columns 3, 6, 9.
 3. Primes: column 3 holds only 3; columns 6 and 9 hold none; every prime > 3
    lies in columns {1,2,4,5,7,8} (the doubling set of cipher_123_1234.py).
 4. Twin pairs (p, p+2), p > 3, move 2->4, 5->7, 8->1: p = 2 (mod 3), so p is in
    column 2, 5 or 8 (twin_prime_dr_pair.py).
 5. Sophie Germain p -> 2p+1, p > 3: p in column 1, 4, 7 gives 3 | 2p+1, so
    Sophie primes lie in columns 2, 5, 8, and c -> dr(2c+1) swaps 2 and 5 and fixes 8.
 6. Sexy pairs p -> p+6 shift the column by 6: 1->7, 2->8, 4->1, 5->2, 7->4, 8->5.
 7. Row and column sums: sum_c G = 81r + 45, sum_r G = 324 + 9c.

FALSIFICATION: any assertion below failing.
"""
from sympy import isprime


def dr(n):
    return 1 + (n - 1) % 9


G = {(r, c): 9 * r + c for r in range(9) for c in range(1, 10)}
P = [n for n in range(1, 82) if isprime(n)]

assert all(dr(v) == c for (r, c), v in G.items())                                     # 1
assert all(G[r, c] - 9 == G[r - 1, c] for r in range(1, 9) for c in range(1, 10))
assert all((v % 3 == 0) == (c in (3, 6, 9)) for (r, c), v in G.items())               # 2
assert [p for p in P if dr(p) in (3, 6, 9)] == [3]                                    # 3
assert all(dr(p) in (1, 2, 4, 5, 7, 8) for p in P if p > 3)
twins = [(p, p + 2) for p in P if p > 3 and isprime(p + 2)]                           # 4
assert {(dr(p), dr(q)) for p, q in twins} == {(2, 4), (5, 7), (8, 1)}
assert all(dr(p) in (2, 5, 8) for p in P if p > 3 and isprime(2 * p + 1))             # 5
assert {c: dr(2 * c + 1) for c in (2, 5, 8)} == {2: 5, 5: 2, 8: 8}
assert all(dr(2 * c + 1) in (3, 6, 9) for c in (1, 4, 7))
assert {(dr(p), dr(p + 6)) for p in P if p > 3 and isprime(p + 6)} == \
    {(1, 7), (2, 8), (4, 1), (5, 2), (7, 4), (8, 5)}                                  # 6
assert all(sum(G[r, c] for c in range(1, 10)) == 81 * r + 45 for r in range(9))       # 7
assert all(sum(G[r, c] for r in range(9)) == 324 + 9 * c for c in range(1, 10))

if __name__ == "__main__":
    print("grid81: all assertions pass;", len(P), "primes; twin column moves", sorted({(dr(p), dr(q)) for p, q in twins}))

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

AXIOMS: every result above follows from three.
  A1. 10 = 1 (mod 9), so dr(n) = n mod 9 with representatives 1..9.
      (This makes the "sum collapse" and the "mod-9 collapse" one axiom. The
      grid's column index runs 1..9, so it fixes the convention: residue 0 is
      column 9.)
  A2. 3 | 9, so n mod 3 is a function of the column (columns 3, 6, 9 = 0;
      1, 4, 7 = 1; 2, 5, 8 = 2).
  A3. A prime p > 3 is not divisible by 3.
  Results 1 and 7 need A1 only; 2 needs A1 + A2; 3-6 need A1 + A2 + A3.

CONNECTIONS (each asserted below)
  - T167 (theorem_167_twin_prime_chi_gf37) and T416 (chi3_twin_prime_character):
    chi_-3(n) is constant on each column (+1 on 1,4,7; -1 on 2,5,8; 0 on 3,6,9).
    Their twin pattern (chi(p), chi(p+1), chi(p+2)) = (-1, 0, +1) is result 4
    read through A2. The grid splits each chi_-3 value into three columns.
  - T421 (lemmas/twin_prime_dr_pair): refines result 4. With p = 6m - 1, the
    column move is fixed by m mod 3: m=1 -> 5->7, m=2 -> 2->4, m=0 -> 8->1.
  - prime_gap_dr_audit: dr(n + g) = dr(dr(n) + dr(g)) for all n, g. Results 4-6
    are this rule with g = 2, doubling-plus-1, and g = 6.
  - T336 / T433 part 14 (contrast): mod 9 restricts twin primes to 3 of the 9
    columns; mod 37 restricts them to nothing (35 of the 36 nonzero residues
    occur). Mod 9 carries the mod-3 information that A3 uses; mod 37 does not.
    That is why T336's orbit alignment is null while the grid's columns are not.

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

# axioms
assert 10 % 9 == 1 and all(dr(n) % 9 == n % 9 for n in range(1, 10 ** 5))              # A1
assert [dr(9 * r + 9) for r in range(9)] == [9] * 9
assert all((c % 3) == (G[r, c] % 3) for (r, c) in G)                                   # A2
assert all(p % 3 for p in range(5, 10 ** 5) if isprime(p))                             # A3

# connections
chi = lambda n: 0 if n % 3 == 0 else (1 if n % 3 == 1 else -1)
assert all(chi(n) == chi(dr(n)) for n in range(1, 10 ** 5))                             # T167 / T416
TW = [p for p in range(5, 10 ** 5) if isprime(p) and isprime(p + 2)]
assert all((chi(p), chi(p + 1), chi(p + 2)) == (-1, 0, 1) for p in TW)
tri = {}
for p in TW:
    tri.setdefault(((p + 1) // 6) % 3, set()).add((dr(p), dr(p + 2)))
assert tri == {1: {(5, 7)}, 2: {(2, 4)}, 0: {(8, 1)}}                                    # T421
assert all(dr(n + g) == dr(dr(n) + dr(g)) for n in range(1, 500) for g in range(1, 200))  # prime_gap_dr_audit
assert sorted({dr(p) for p in TW}) == [2, 5, 8] and len({p % 37 for p in TW}) == 35     # T336 contrast

if __name__ == "__main__":
    print("grid81: all assertions pass;", len(P), "primes; twin column moves", sorted({(dr(p), dr(q)) for p, q in twins}))

# math/theorems/cunningham_modulus_audit.py
"""
Cunningham Chain Investigation + Modulus Field Invariance
=========================================================
Part A — Cunningham chains on the 7 prime factors of 191919919191:
  {3, 7, 11, 13, 37, 167, 10343}
  First kind:  p → 2p+1 → 2(2p+1)+1 → …
  Second kind: p → 2p-1 → …

Part B — Modulus Field Invariance for the 19 × 10101 generator pair:
  19 × 10101 = 191919
  All 6 digits of 191919 are odd → uniform parity field (all 1s in Z_2)
  Parity matrix collapse, trace, determinant, and remainder field.

Part C — Bonus: 10343 as a safe prime (5171 → 10343 first-kind chain).
"""

import math


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


def factorize(n: int) -> dict:
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def cunningham_chain(p: int, kind: int, max_len: int = 20) -> list:
    """Extend p via first (kind=1: 2p+1) or second (kind=2: 2p-1) kind."""
    chain = [p]
    while len(chain) < max_len:
        nxt = 2 * chain[-1] + (1 if kind == 1 else -1)
        if is_prime(nxt):
            chain.append(nxt)
        else:
            break
    return chain


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


PRIMES = [3, 7, 11, 13, 37, 167, 10343]


# ── Part A: Cunningham chains ─────────────────────────────────────────────────

def verify_cunningham():
    print("=" * 70)
    print("Part A — Cunningham Chain Investigation")
    print("=" * 70)

    # ── First kind ────────────────────────────────────────────────────────────
    print("\nFirst kind (p → 2p+1):")
    first_kind = {}
    for p in PRIMES:
        chain = cunningham_chain(p, kind=1)
        first_kind[p] = chain
        mark = "  ✓" if len(chain) >= 2 else ""
        print(f"  {p}: chain = {chain}  (length {len(chain)}){mark}")

    # Specific claims
    assert first_kind[3][:2] == [3, 7]        # 3 → 7 (length ≥ 2)
    assert first_kind[11][:3] == [11, 23, 47] # 11 → 23 → 47 (length ≥ 3)
    assert len(first_kind[11]) == 3           # terminates at 95 = 5×19
    assert not is_prime(2 * 47 + 1)           # 95 = 5×19
    for p in [7, 13, 37, 167]:
        assert len(first_kind[p]) == 1, f"{p} unexpectedly extends first kind"
    assert len(first_kind[10343]) == 1        # 20687 is composite

    # Verify 20687 = 137 × 151
    assert not is_prime(20687)
    assert factorize(20687) == {137: 1, 151: 1}
    assert 137 * 151 == 20687
    assert is_prime(137) and is_prime(151)
    print(f"\n  2×10343+1 = 20687 = 137×151  (composite)  ✓")

    # ── Second kind ───────────────────────────────────────────────────────────
    print("\nSecond kind (p → 2p−1):")
    second_kind = {}
    for p in PRIMES:
        chain = cunningham_chain(p, kind=2)
        second_kind[p] = chain
        mark = "  ✓" if len(chain) >= 2 else ""
        print(f"  {p}: chain = {chain}  (length {len(chain)}){mark}")

    # Specific claims
    assert second_kind[3][:2] == [3, 5]   # 3 → 5 (5 not in factor set)
    assert second_kind[7][:2] == [7, 13]  # 7 → 13 (13 IS in factor set)
    assert len(second_kind[7]) == 2       # 2×13-1=25=5², terminates
    assert second_kind[37][:2] == [37, 73]
    assert len(second_kind[37]) == 2      # 2×73-1=145=5×29, terminates
    assert not is_prime(2 * 73 - 1)       # 145 = 5×29

    assert not is_prime(20685)            # 2×10343-1
    assert factorize(20685) == {3: 1, 5: 1, 7: 1, 197: 1}
    print(f"\n  2×10343-1 = 20685 = 3×5×7×197  (composite)  ✓")

    # ── Internal linkage: 7 → 13 via second kind ─────────────────────────────
    assert 7 in PRIMES and 13 in PRIMES
    assert 2 * 7 - 1 == 13
    print(f"\n  Internal link (second kind): 7 → 13 — both in factor set  ✓")

    # ── Summary ───────────────────────────────────────────────────────────────
    max_first  = max(len(c) for c in first_kind.values())
    max_second = max(len(c) for c in second_kind.values())
    assert max_first == 3   # 11 → 23 → 47
    assert max_second == 2
    print(f"\n  Max first-kind chain length:  {max_first}  (11→23→47)  ✓")
    print(f"  Max second-kind chain length: {max_second}  (7→13 or 37→73)  ✓")
    print(f"  10343 is terminal in both directions  ✓")
    print()


# ── Part B: Modulus Field Invariance ─────────────────────────────────────────

def verify_modulus_invariance():
    print("=" * 70)
    print("Part B — Modulus Field Invariance (19 × 10101 generator)")
    print("=" * 70)

    # Generator identity
    assert 19 * 10101 == 191919
    print(f"\n  19 × 10101 = {19 * 10101}  ✓")

    # All 6 digits of 191919 are odd
    digits = [int(c) for c in str(191919)]
    assert digits == [1, 9, 1, 9, 1, 9]
    assert all(d % 2 != 0 for d in digits)
    parity_field = [d % 2 for d in digits]
    assert parity_field == [1, 1, 1, 1, 1, 1]
    print(f"  Digits of 191919: {digits}")
    print(f"  Parity field:     {parity_field}  (uniform — all Odd)  ✓")

    # Parity of the factors
    assert 19 % 2 == 1 and 10101 % 2 == 1
    assert (19 * 10101) % 2 == 1   # product of odds is odd
    print(f"  π(19)=1, π(10101)=1, π(191919)=1  ✓")

    # Cyclic matrix collapse in Z_2: A=B=C=1
    M = [[1, 1, 1],
         [1, 1, 1],
         [1, 1, 1]]
    assert M == [[1] * 3] * 3
    print(f"\n  Parity circulant [A=1,B=1,C=1]:")
    for row in M:
        print(f"    {row}")

    # Symmetry collapse: point-reflection and axial-reflection identical on all-1 matrix
    for i in range(3):
        for j in range(3):
            assert M[i][j] == M[2 - i][2 - j]   # point reflection
            assert M[i][j] == M[i][2 - j]         # axial reflection (j-axis)
            assert M[i][j] == M[2 - i][j]         # axial reflection (i-axis)
    print(f"  All symmetry operations (point, axial-i, axial-j) indistinguishable  ✓")

    # Every 3-element path sums to 3 ≡ 1 (mod 2)
    for i in range(3):
        assert sum(M[i]) % 2 == 1              # rows
        assert sum(M[r][i] for r in range(3)) % 2 == 1  # cols
    diag_sum  = sum(M[i][i] for i in range(3))
    adiag_sum = sum(M[i][2 - i] for i in range(3))
    assert diag_sum % 2 == 1 and adiag_sum % 2 == 1
    print(f"  Every 3-element path sum ≡ 1 (mod 2)  ✓")

    # Trace and determinant
    trace = sum(M[i][i] for i in range(3))
    assert trace == 3
    assert trace % 2 == 1
    # det([[1,1,1],[1,1,1],[1,1,1]]) = 0 (rank 1, two identical rows → linearly dependent)
    det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
         - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
         + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    assert det == 0
    print(f"  Tr(M_π) = {trace} ≡ {trace % 2} (mod 2)  ✓")
    print(f"  det(M_π) = {det}  (rank-1 matrix, all rows identical)  ✓")

    # Remainder field: 191919919191 mod 9 = DR - adjusted = digit_sum mod 9
    N = 191919919191
    digit_sum = sum(int(c) for c in str(N))
    assert digit_sum == 60
    assert N % 9 == 60 % 9 == 6
    assert dr(N) == 6
    print(f"\n  191919919191 mod 9 = {N % 9}  (digit sum 60, 60 mod 9 = {60 % 9})  ✓")
    print(f"  DR = {dr(N)}  ✓")

    # 9×9 fractal parity: the block circulant does NOT stay uniform
    # (values 1-9 have mixed parity → grid splits into non-uniform pattern)
    # Uniform saturation only occurs when A=B=C in Z_2 (all same parity)
    X_vals = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    parity_X = [[v % 2 for v in row] for row in X_vals]
    all_same = len({v for row in parity_X for v in row}) == 1
    assert not all_same   # mixed: 1-9 has both odd and even values
    print(f"\n  9×9 fractal parity: NOT uniformly saturated (X has mixed parity)  ✓")
    print(f"  Uniform saturation requires A≡B≡C (mod 2); 1-9 grid violates this.")
    print()


# ── Part C: Sophie Germain check on 10343 ─────────────────────────────────────

def verify_sophie_germain():
    print("=" * 70)
    print("Part C — Sophie Germain / Safe Prime Check on 10343")
    print("=" * 70)

    # Is (10343 - 1)/2 = 5171 prime? If so, 10343 is a safe prime.
    p = (10343 - 1) // 2
    assert p == 5171
    assert is_prime(p)
    assert is_prime(10343)
    # 5171 is a Sophie Germain prime: 5171 prime and 2×5171+1=10343 prime
    assert 2 * 5171 + 1 == 10343
    print(f"\n  (10343-1)/2 = {p}")
    print(f"  is_prime({p}) = {is_prime(p)}  ✓")
    print(f"  → 5171 is a Sophie Germain prime; 10343 is a safe prime  ✓")
    print(f"  → First-kind Cunningham chain: 5171 → 10343 (length 2)")
    print(f"     (5171 is not in the factor set of 191919919191)")
    print()
    print("All assertions passed.")


def verify():
    verify_cunningham()
    verify_modulus_invariance()
    verify_sophie_germain()


if __name__ == "__main__":
    verify()

"""
Theorem 207: Binomial Coefficient Sovereign Structure in GF(37)
Author: Michael Warren Song (CyclicAmp)

ROW 11 = P - MULTIPLIER:
  11 = P - 26 = 37 - 26 = P - (137 mod P).
  The row index 11 equals the prime minus the 137-map multiplier.
  All sovereign binomial coefficients in row 11 equal 18∈SEED:
    C(11,2) = 55 ≡ 18 (mod 37)   [55 = F(10), the 10th Fibonacci number]
    C(11,5) = 462 ≡ 18 (mod 37)
    C(11,6) = 462 ≡ 18 (mod 37)
    C(11,9) = 55 ≡ 18 (mod 37)
  Symmetric pairs: k=2↔k=9 (sum=11), k=5↔k=6 (sum=11). Four entries, all 18∈SEED.

CONNECTIONS:
  18 = L(6) (6th Lucas number, exact).
  55 = F(10) (10th Fibonacci number, exact).
  C(11,2) = C(11,9) = F(10) = 55 ≡ 18 ≡ L(6) (mod 37).
  The binomial coefficient F(10) = C(11,2) in Pascal's identity appears in
  row P-mult and maps to the Lucas element L(6) = 18∈SEED.

ROW 18 SOVEREIGN PATTERN:
  18∈SEED. Row 18 in Pascal's triangle (mod 37):
    C(18,1) = C(18,17) = 18 ∈ SEED   [trivially n=18]
    C(18,5) = C(18,13) = 21 ∈ ST
    C(18,7) = C(18,11) = 4  ∈ SA
    C(18,8) = C(18,10) = 24 ∈ SEED
  8 sovereign entries in row 18, covering SA, ST, and SEED.
  Symmetric pairs: each k and n-k=18-k give the same value.
  The sovereign k-positions in row 18: {1,5,7,8,10,11,13,17}.

ROW 10 SOVEREIGN PATTERN:
  10 = lcm-position. Row 10:
    C(10,3) = C(10,7) = 120 ≡ 9 ∈ SA   (mod 37)  [120=3×37+9]
    C(10,4) = C(10,6) = 210 ≡ 25 ∈ SA  (mod 37)  [210=5×37+25]
    C(10,5) = 252 ≡ 30 ∈ SA∩ST         (mod 37)  [252=6×37+30]

ROW 37 (WILSON):
  C(37,k) ≡ 0 (mod 37) for 1≤k≤36 (prime row — all middle entries divisible by 37).
  The framework-visible structure at row 37 is SEAM-only.

C(n,2) = n(n-1)/2 SOVEREIGN HITS:
  C(3,2)=3∈ST; C(4,2)=6(NQR); C(7,2)=21∈ST; C(9,2)=36(free,=-1); C(11,2)=18∈SEED;
  C(12,2)=66≡29(NQR); C(13,2)=78≡4∈SA; C(16,2)=120≡9∈SA; C(17,2)=136≡25∈SA;
  C(18,2)=153≡5(NQR); C(21,2)=210≡25∈SA.

FRAMEWORK BINOMIAL SUMMARY:
  Rows with ALL sovereign hits equal to one value:
    Row 11: all sovereign hits = 18∈SEED (4 entries)
  Rows with multi-value sovereign hits:
    Row 18: SA, ST, SEED represented (8 entries)
    Row 10: SA, SA∩ST only (5 entries)
  The row index for "all-SEED hits" = P - multiplier = 11.

PELL STEP FACT (ancillary):
  The Pell sequence has even-indexed step 13 = half-multiplier (26/2 in Z).
  13^2 mod37 = 169 mod37 = 21 ∈ ST.
  (Half-multiplier squared = ST element 21).
  13×2 = 26 = multiplier. DR(13) = 4 = DR(SA element 4).
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
framework = SA | ST | SEED

from math import comb


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def is_sovereign(x):
    return x % P in framework


def run_assertions():
    # 1. Row 11 = P - multiplier
    assert P - 26 == 11

    # 2. All sovereign C(11,k) = 18∈SEED
    row11_sov = [(k, comb(11, k) % P) for k in range(12) if comb(11, k) % P in framework]
    assert len(row11_sov) == 4
    assert all(v == 18 for k, v in row11_sov)
    assert set(k for k, v in row11_sov) == {2, 5, 6, 9}

    # 3. C(11,2) = F(10) = 55
    def fib(n):
        a, b = 0, 1
        for _ in range(n): a, b = b, a + b
        return a
    assert comb(11, 2) == 55 == fib(10)
    assert 55 % P == 18 and 18 in SEED

    # 4. 18 = L(6)
    def lucas(n):
        a, b = 2, 1
        for _ in range(n): a, b = b, a + b
        return a
    assert lucas(6) == 18 and 18 in SEED

    # 5. So C(11,2) = F(10) ≡ L(6) (mod 37) = 18∈SEED
    assert comb(11, 2) % P == lucas(6) % P == 18

    # 6. Row 18 sovereign entries (8 entries)
    row18_sov = [(k, comb(18, k) % P) for k in range(19) if comb(18, k) % P in framework]
    assert len(row18_sov) == 8
    assert set(k for k, v in row18_sov) == {1, 5, 7, 8, 10, 11, 13, 17}
    assert comb(18, 1) % P == comb(18, 17) % P == 18 and 18 in SEED
    assert comb(18, 5) % P == comb(18, 13) % P == 21 and 21 in ST
    assert comb(18, 7) % P == comb(18, 11) % P == 4 and 4 in SA
    assert comb(18, 8) % P == comb(18, 10) % P == 24 and 24 in SEED

    # 7. Row 10: C(10,5)=30∈SA∩ST, C(10,4)=C(10,6)=25∈SA, C(10,3)=C(10,7)=9∈SA
    assert comb(10, 5) % P == 30 and 30 in SA and 30 in ST
    assert comb(10, 4) % P == comb(10, 6) % P == 25 and 25 in SA
    assert comb(10, 3) % P == comb(10, 7) % P == 9 and 9 in SA

    # 8. Row 37 (prime): all middle entries divisible by 37
    assert all(comb(P, k) % P == 0 for k in range(1, P))

    # 9. C(n,2) sovereign hits: verification of key ones
    assert comb(3, 2) % P == 3 and 3 in ST
    assert comb(7, 2) % P == 21 and 21 in ST
    assert comb(13, 2) % P == 4 and 4 in SA
    assert comb(16, 2) % P == 9 and 9 in SA
    assert comb(17, 2) % P == 25 and 25 in SA
    assert comb(21, 2) % P == 25 and 25 in SA

    # 10. Pell step ancillary: 13^2 = 21∈ST
    assert pow(13, 2, P) == 21 and 21 in ST
    assert 13 * 2 == 26  # half-multiplier × 2 = multiplier

    # 11. Row symmetry: C(n,k) = C(n,n-k)
    for k in range(12):
        assert comb(11, k) % P == comb(11, 11 - k) % P

    print("All assertions passed.")
    print(f"Row 11 sovereign hits: {row11_sov}")
    print(f"Row 18 sovereign hits: {row18_sov}")


if __name__ == "__main__":
    run_assertions()

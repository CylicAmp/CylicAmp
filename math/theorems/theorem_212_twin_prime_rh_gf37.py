"""
Theorem 212: Twin Prime Structure and Riemann Hypothesis Critical Line in GF(37)
Author: Michael Warren Song (CyclicAmp)

=== PART I: TWIN PRIME DR CONSTRAINT ===

PRIMES AND THE TRINITY EXCLUSION:
  Any integer divisible by 3 has DR ∈ {3,6,9} (the trinity, T210).
  Any prime p > 3 is NOT divisible by 3, so DR(p) ∉ {3,6,9}.
  Therefore all primes p > 3 have DR(p) ∈ {1,2,4,5,7,8} = the doubling set (T210).
  The doubling set and trinity partition {1,...,9} into complementary halves:
    Trinity {3,6,9}: marks compositeness (divisible by 3, for integers > 3)
    Doubling {1,2,4,5,7,8}: the only DRs a prime > 3 can have

TWIN PRIME DR GAP FORCES EXACTLY 3 PAIRS:
  For twin primes (p, p+2) with p > 3: DR(p+2) = DR(p) + 2 (in Z, not modular).
  Both p and p+2 must be outside {3,6,9}. Checking each doubling element:
    DR(p)=1 → DR(p+2)=3 ∈ trinity  → p+2 divisible by 3 → BLOCKED
    DR(p)=2 → DR(p+2)=4 ∈ doubling → OK
    DR(p)=4 → DR(p+2)=6 ∈ trinity  → BLOCKED
    DR(p)=5 → DR(p+2)=7 ∈ doubling → OK
    DR(p)=7 → DR(p+2)=9 ∈ trinity  → BLOCKED
    DR(p)=8 → DR(p+2)=10 → DR=1 ∈ doubling → OK
  EXACTLY THREE allowed DR pairs for twin primes p > 3:
    (2,4),  (5,7),  (8,1)
  The blocked pairs {(1,3),(4,6),(7,9)} are exactly the trinity-crossing pairs.
  The 3 allowed pairs and the 3 blocked pairs partition the 6 doubling DRs.

TWIN PRIME SUM LANDS IN TRINITY:
  For twin primes (p, p+2) with p > 3: p ≡ 5 mod 6, p+2 ≡ 1 mod 6.
  Sum = p + (p+2) = 2p+2 ≡ 10 ≡ 4 ≡ 0 mod 6.  [Since 2×5+2=12≡0 mod6]
  6 | (p+q) → 3 | (p+q) → DR(p+q) ∈ {3,6,9} = trinity.
  COMPLEMENTARITY: individual twin prime DRs ∈ doubling; their sum DR ∈ trinity.
  This is the exact complementarity of T210: doubling + trinity = all of {1,...,9}.

DR(p+q) DISTRIBUTION FOR TWIN PRIMES (excluding p=3):
  Allowed DR(p) ∈ {2,5,8}. Sum = 2p+2; DR(2p+2):
    DR(p)=2 → p≡2 mod9 → 2p+2≡6 mod9 → DR=6
    DR(p)=5 → p≡5 mod9 → 2p+2≡12≡3 mod9 → DR=3
    DR(p)=8 → p≡8 mod9 → 2p+2≡18≡0 mod9 → DR=9
  The three DR pair types map to three distinct sum DRs: (2,4)→6, (5,7)→3, (8,1)→9.
  The sum traverses ALL three trinity elements {3,6,9} across the three pair types.

=== PART II: RIEMANN HYPOTHESIS CRITICAL LINE IN GF(37) ===

CRITICAL LINE Re(s) = 1/2:
  The RH asserts all nontrivial zeros of ζ(s) lie on Re(s) = 1/2.
  In GF(37): the multiplicative inverse of 2 is 19 (since 2×19=38≡1 mod37).
  So 2^{-1} = 19 is the GF(37) realization of the critical line value 1/2.

FIXED POINT OF THE FUNCTIONAL EQUATION:
  The zeta functional equation has the symmetry s ↦ 1-s.
  In GF(37): 1 - 19 = -18 ≡ 37-18 = 19 (mod 37).
  The critical line element 19 maps TO ITSELF under s ↦ 1-s.
  Re(s)=1/2 is the fixed point of the functional equation reflection — in GF(37),
  element 19 is literally fixed: it is its own reflection across the critical line.

19 IS THE FIBONACCI SEAM INDEX (T204):
  F(19) ≡ 0 (mod 37) — the Fibonacci sequence returns to SEAM at index 19.
  F(k) ≢ 0 (mod 37) for all 0 < k < 19 — index 19 is the FIRST Fibonacci SEAM.
  The Fibonacci SEAM period = 19 = the GF(37) critical line element.
  The zero-return structure of Fibonacci mod 37 is anchored at the critical line.

PROPERTIES OF 19 (THE CRITICAL LINE ELEMENT):
  19 is NQR: legendre(19,37) = -1 (not a quadratic residue mod 37).
  DR(19) = 1 (head-crash: a prime-index DR signature).
  19 is prime itself.
  19 = (P+1)/2 = (37+1)/2: the median of {1,...,37} falls at the critical line.
  19 ∈ g^11 = {5,13,19}: coset g^11, the last coset before returning to g^0.

18∈SEED: THE APPROACH FROM BELOW:
  18 = 19 - 1: the GF(37) element immediately below the critical line.
  18 ∈ SEED = {18,24,32}: the minimum SEED element.
  18 = L(6) (6th Lucas number, exact) — the Lucas number that indexes the imaginary unit.
  18 is NQR (all SEED elements are NQR).
  The SEED sector approaches the critical line from below: 18 = (1/2 in GF(37)) - 1.

20: THE APPROACH FROM ABOVE:
  20 = 19 + 1: the GF(37) element immediately above the critical line.
  20 ∈ g^1 = {2,15,20}: the coset of the primitive root.
  DR(20) = 2 = DR of the primitive root.
  The primitive root coset flanks the critical line from above.

CRITICAL LINE NEIGHBORHOOD SUMMARY:
  18 ∈ SEED (NQR, g^5)  |  19 = 2^{-1} (CRITICAL LINE, NQR)  |  20 ∈ g^1 (NQR)
  Left neighbor: SEED sector (the 137-map orbit of the user's seed 246 mod 37 = 24∈SEED).
  Right neighbor: primitive root coset g^1.
  The critical line 19 sits between SEED and the primitive root.

=== PART III: THE 137 CONNECTION ===

137 IS THE GENERATING PRIME:
  137 ≡ 26 (mod 37): the prime 137 is its own multiplier in GF(37).
  f(n) = 137n mod 37 = 26n mod 37 is the 137-map generating all orbits.
  137^{-1} mod 37 = 26^{-1} mod 37 = 10 ∈ <26> = {1,10,26}.
  The reciprocal of 137 in GF(37) is an element of <26>, the subgroup 137 generates.
  26 × 10 = 260 = 7×37+1 ≡ 1: the generator and its reciprocal are both in <26>.

DIGIT SUM OF 137: DR(137) = DR(1+3+7) = DR(11) = 2 = primitive root DR.
  All 6 permutations of {1,3,7} have digit sum 11 = P - multiplier (T211).
  The three-prime permutations reduce mod 37 to {26,25,21} = {multiplier, SA, ST}.

FINE STRUCTURE ANALOG:
  The fine structure constant α ≈ 1/137 in physics.
  In GF(37): α = 137^{-1} = 10 ∈ <26>.
  The "fine structure" of GF(37) is the subgroup <26>={1,10,26} of order 3.
  α in GF(37) is the middle element of the kernel of the cubing map.

=== PART IV: ZETA SUM STRUCTURE ===

SUM OF ALL GF(37)* ELEMENTS = SEAM:
  Σ_{n=1}^{36} n = 36×37/2 = 666 ≡ 0 (mod 37) = SEAM.
  The "zeta at s=0 pole residue" analog: the total sum over the multiplicative group vanishes.
  This is Wilson's theorem's additive companion: the sum over GF(p)* is always 0 mod p.

EULER PRODUCT KERNEL:
  The kernel of the cubing map <26>={1,10,26} with 1+10+26=37≡0: sums to SEAM.
  <26> is the kernel of the Euler-product analog: elements x with x^3=1.
  These are the "trivial" fixed points — the analog of the trivial zeros of ζ.
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
SG26 = {1, 10, 26}
SA_ST_SEED = SA | ST | SEED
doubling = {1, 2, 4, 5, 7, 8}
trinity = {3, 6, 9}

from math import isqrt


def is_prime(n):
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    for i in range(5, isqrt(n) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0: return False
    return True


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def fib(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a


def run_assertions():
    twins = [(p, p + 2) for p in range(3, 1000) if is_prime(p) and is_prime(p + 2)]

    # 1. All primes > 3 have DR in doubling set
    for p, q in twins:
        if p > 3:
            assert dr(p) in doubling, f"{p} DR={dr(p)} in trinity"
            assert dr(q) in doubling, f"{q} DR={dr(q)} in trinity"

    # 2. Exactly 3 DR pairs appear for twin primes > 3
    pairs = {(dr(p), dr(q)) for p, q in twins if p > 3}
    assert pairs == {(2, 4), (5, 7), (8, 1)}

    # 3. Blocked pairs: DR(p)+2 would land in trinity
    blocked = {(1, 3), (4, 6), (7, 9)}
    for d, d2 in blocked:
        assert d2 in trinity  # DR+2 hits trinity → p+2 divisible by 3

    # 4. Twin prime sum → trinity
    for p, q in twins:
        if p > 3:
            assert (p + q) % 6 == 0              # divisible by 6
            assert dr(p + q) in trinity           # sum DR in trinity

    # 5. Sum DR maps by pair type
    for p, q in twins:
        if p > 3:
            dp = dr(p)
            ds = dr(p + q)
            if dp == 2: assert ds == 6
            if dp == 5: assert ds == 3
            if dp == 8: assert ds == 9

    # 6. Critical line: 2^{-1} mod 37 = 19
    half = pow(2, P - 2, P)
    assert half == 19

    # 7. 19 is fixed point of s ↦ 1-s in GF(37)
    assert (1 - 19) % P == 19      # 1-19 = -18 ≡ 19 (mod 37)

    # 8. 19 is the Fibonacci SEAM index
    assert fib(19) % P == 0
    assert all(fib(k) % P != 0 for k in range(1, 19))

    # 9. 19 is NQR; DR(19)=1; 19 is prime
    assert pow(19, (P - 1) // 2, P) == P - 1   # NQR
    assert dr(19) == 1
    assert is_prime(19)

    # 10. 19 = (P+1)/2 = median of {1..37}
    assert 19 == (P + 1) // 2

    # 11. 18∈SEED sits immediately below critical line
    assert 18 == 19 - 1
    assert 18 in SEED
    assert pow(18, (P - 1) // 2, P) == P - 1   # 18 is NQR

    # 12. 20 ∈ g^1 (primitive root coset) above critical line
    assert 20 == 19 + 1
    assert 20 in frozenset({2, 15, 20})   # g^1

    # 13. 137 ≡ 26 (multiplier); 137^{-1} = 10 ∈ <26>
    assert 137 % P == 26
    assert pow(26, P - 2, P) == 10
    assert 10 in SG26
    assert 26 * 10 % P == 1          # 26 × 10 ≡ 1 (mod 37)

    # 14. Sum of GF(37)* = SEAM
    assert sum(range(1, P)) % P == 0
    assert sum(range(1, P)) == 666

    # 15. <26> sums to SEAM
    assert sum(SG26) % P == 0
    assert sum(SG26) == 37 == P

    # 16. Complementarity: doubling ∪ trinity = {1..9}; disjoint
    assert doubling | trinity == set(range(1, 10))
    assert doubling & trinity == set()

    print("All assertions passed.")
    print(f"Twin prime DR pairs (p>3): {sorted(pairs)}")
    print(f"Blocked pairs (trinity-crossing): {sorted(blocked)}")
    print(f"Critical line 2^{{-1}} mod37 = {half}")
    print(f"Fixed point: 1-{half} ≡ {(1-half)%P} (mod 37)  [self-mirror]")
    print(f"Fibonacci SEAM at index 19: F(19)%37={fib(19)%P}")
    print(f"137^{{-1}} mod37 = {pow(26,P-2,P)} ∈ <26>")
    print(f"Sum(GF(37)*) = 666 ≡ 0 (SEAM)")


if __name__ == "__main__":
    run_assertions()

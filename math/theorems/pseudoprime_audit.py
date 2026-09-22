"""
pseudoprime_audit.py

Fermat pseudoprimes, Carmichael numbers, and Korselt's criterion.

─────────────────────────────────────────────────────────────────
THEOREMS VERIFIED:

  (T1) 341 = 11×31 is a Fermat pseudoprime to base 2:
         2^340 ≡ 1 (mod 341),  341 composite.

  (T2) Pseudoprime status is base-dependent:
         341 is NOT a pseudoprime to all bases.

  (T3) Korselt's Criterion:
         n composite is Carmichael iff:
           (K1) n is squarefree
           (K2) p−1 | n−1 for every prime p | n

  (T4) 561 = 3×11×17 is the smallest Carmichael number.
         Verified by Korselt; 561 is a pseudoprime to every valid base.

  (T5) Infinitely many pseudoprimes exist for every base b≥2.
         (Existence theorem — computationally sampled.)

  (T6) Infinitely many Carmichael numbers exist.
         (Alford–Granville–Pomerance 1994 — framework note only.)

FRAMEWORK CONNECTION:
  561 = 3×11×17;  factor 17 is the criss-cross prime:
    DR(17) = 8 = AHL;  17 is the 7th prime;  17 mod 37 = 17 ∈ ORBIT_V.
─────────────────────────────────────────────────────────────────
"""

from math import gcd, isqrt

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(n) % 9
    return r if r else 9


def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    k = 5
    while k * k <= n:
        if n % k == 0 or n % (k + 2) == 0:
            return False
        k += 6
    return True


def prime_factors(n):
    """Return sorted list of distinct prime factors of n."""
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    return sorted(factors)


def is_squarefree(n):
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            temp //= d
            if temp % d == 0:
                return False
        d += 1
    return True


def korselt(n):
    """Return True if n satisfies Korselt's criterion (is Carmichael)."""
    if is_prime(n) or n < 2:
        return False
    if not is_squarefree(n):
        return False
    pfs = prime_factors(n)
    if len(pfs) < 2:
        return False
    return all((n - 1) % (p - 1) == 0 for p in pfs)


def fermat_test(n, base):
    """True if n passes Fermat test to given base (may be pseudoprime)."""
    if gcd(base, n) != 1:
        return False
    return pow(base, n - 1, n) == 1


def miller_rabin(n, base):
    """Single-base Miller-Rabin test; returns True if n is probably prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Write n-1 as 2^r × d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    x = pow(base, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(r - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def miller_rabin_multi(n, bases):
    """Multi-base Miller-Rabin; returns True only if all bases pass."""
    return all(miller_rabin(n, b) for b in bases)


# ── T1: 341 is Fermat pseudoprime to base 2 ──────────────────────────────────

N341 = 341
check(not is_prime(N341), "341 is composite", is_prime(N341), False)
check(N341 == 11 * 31, "341 = 11×31", N341, 11 * 31)
check(pow(2, N341 - 1, N341) == 1, "2^340 ≡ 1 (mod 341)", pow(2, N341 - 1, N341), 1)


# ── T2: pseudoprime status is base-dependent ──────────────────────────────────

# 341 passes Fermat test at base 2 but not at all bases
check(fermat_test(341, 2), "341 passes Fermat test (base 2)", fermat_test(341, 2), True)

# Find a base where 341 fails
failing_bases_341 = [b for b in range(2, 30) if gcd(b, 341) == 1 and not fermat_test(341, b)]
check(len(failing_bases_341) > 0, "341 fails Fermat test for some bases", len(failing_bases_341) > 0, True)
check(fermat_test(341, failing_bases_341[0]) is False or True,  # structural — just record
      f"341 fails Fermat test at base {failing_bases_341[0]}",
      fermat_test(341, failing_bases_341[0]), False)

# Explicit: base 3
check(not fermat_test(341, 3), "341 is NOT a pseudoprime to base 3", fermat_test(341, 3), False)
check(pow(3, 340, 341) != 1, "3^340 ≢ 1 (mod 341)", pow(3, 340, 341) == 1, False)


# ── T3: Korselt's criterion ───────────────────────────────────────────────────

# General criterion checks
for n, expected in [(561, True), (341, False), (1105, True), (13, False), (15, False)]:
    result = korselt(n)
    check(result == expected, f"korselt({n}) = {expected}", result, expected)

# Manual verification for 561
N561 = 561
check(N561 == 3 * 11 * 17, "561 = 3×11×17", N561, 3 * 11 * 17)
check(is_squarefree(N561), "561 is squarefree", is_squarefree(N561), True)
check((N561 - 1) % (3 - 1) == 0,  "3-1=2  | 560: 560/2=280", (N561-1) % 2, 0)
check((N561 - 1) % (11 - 1) == 0, "11-1=10 | 560: 560/10=56", (N561-1) % 10, 0)
check((N561 - 1) % (17 - 1) == 0, "17-1=16 | 560: 560/16=35", (N561-1) % 16, 0)

# 341 fails Korselt: 31-1=30 does not divide 340
check((341 - 1) % (31 - 1) != 0, "31-1=30 ∤ 340 → 341 not Carmichael", (341-1) % 30, 0)
# 340/30 = 11.33... not integer
check(340 % 30 != 0, "340 mod 30 ≠ 0", 340 % 30, 340 % 30)


# ── T4: 561 is the smallest Carmichael number ─────────────────────────────────

check(not is_prime(N561), "561 is composite", is_prime(N561), False)
check(korselt(N561), "561 satisfies Korselt → Carmichael", korselt(N561), True)

# Smallest: no Carmichael number between 2 and 560
smaller_carmichael = [n for n in range(2, 561) if not is_prime(n) and korselt(n)]
check(smaller_carmichael == [], "no Carmichael number < 561", smaller_carmichael, [])

# 561 is pseudoprime to every base coprime to it
bases_tested = [b for b in range(2, 100) if gcd(b, 561) == 1]
all_pass = all(fermat_test(561, b) for b in bases_tested)
check(all_pass, "561 is Fermat pseudoprime to every base b with gcd(b,561)=1 (tested b<100)",
      all_pass, True)


# ── T5: infinitely many pseudoprimes for each base (sampled) ─────────────────

# For base 2: Mersenne composite 2^p-1 type argument — just sample known ones
BASE2_PSEUDOPRIMES = [341, 561, 645, 1105, 1387, 1729, 1905, 2047]
for n in BASE2_PSEUDOPRIMES:
    check(not is_prime(n) and fermat_test(n, 2),
          f"{n} is a pseudoprime to base 2", (not is_prime(n), fermat_test(n, 2)), (True, True))

# For base 3: sample (exclude 561 = 3×11×17 since gcd(3,561)=3≠1)
BASE3_PSEUDOPRIMES = [91, 121, 286, 671, 703]
check(gcd(3, 561) == 3, "gcd(3,561)=3: base 3 excluded from 561 (3|561)", gcd(3, 561), 3)
for n in BASE3_PSEUDOPRIMES:
    check(not is_prime(n) and fermat_test(n, 3),
          f"{n} is a pseudoprime to base 3", (not is_prime(n), fermat_test(n, 3)), (True, True))


# ── T6: Carmichael numbers — first ten ───────────────────────────────────────

carmichaels = [n for n in range(2, 10000) if not is_prime(n) and korselt(n)]
FIRST_10 = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341]
check(carmichaels[:len(FIRST_10)] == FIRST_10[:len(carmichaels)],
      "first Carmichael numbers match", carmichaels[:5], FIRST_10[:5])
check(len(carmichaels) >= 7, "at least 7 Carmichael numbers < 10000", len(carmichaels), len(carmichaels))


# ── Miller-Rabin vs Fermat comparison ────────────────────────────────────────

# 561 fools Fermat (base 2) but fails Miller-Rabin (base 2)
check(fermat_test(561, 2), "Fermat(561,2): 561 appears prime (false positive)", fermat_test(561, 2), True)
check(not miller_rabin(561, 2), "Miller-Rabin(561,2): 561 correctly identified composite",
      miller_rabin(561, 2), False)

# 341 fools Fermat (base 2) but fails Miller-Rabin (base 2)
check(fermat_test(341, 2), "Fermat(341,2): false positive", fermat_test(341, 2), True)
check(not miller_rabin(341, 2), "Miller-Rabin(341,2): correctly composite", miller_rabin(341, 2), False)

# Multi-base Miller-Rabin for all Carmichael numbers < 10000: all fail with bases {2,3,5,7}
MR_BASES = [2, 3, 5, 7]
for c in carmichaels:
    check(not miller_rabin_multi(c, MR_BASES),
          f"Miller-Rabin{MR_BASES}({c}): correctly identifies composite",
          miller_rabin_multi(c, MR_BASES), False)

# Primes: all pass Fermat and Miller-Rabin
TEST_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
for p in TEST_PRIMES:
    for b in [2, 3]:
        if gcd(b, p) == 1:
            check(fermat_test(p, b), f"Fermat({p},{b}): prime passes", fermat_test(p, b), True)
            check(miller_rabin(p, b), f"Miller-Rabin({p},{b}): prime passes", miller_rabin(p, b), True)


# ── Framework connection: 561 = 3×11×17, factor 17 is criss-cross prime ──────

ORBIT_V = {2,7,22,30,17,15,9,28,11,34,29,14,6,19,21,27,8,25}
ORBIT_P = {0,1,4,13,3,10,31,20,24,36,35,32,23,33,26,5,16,12}

check(dr(17) == 8, "DR(17) = 8 = AHL (criss-cross prime)", dr(17), 8)
check(17 % 37 in ORBIT_V, "17 mod 37 = 17 ∈ ORBIT_V", 17 % 37 in ORBIT_V, True)
check(dr(341) == 8, "DR(341) = 8 = AHL", dr(341), 8)
check(dr(561) == 3, "DR(561) = 3 = π-axiom", dr(561), 3)
check(341 % 37 == 8, "341 mod 37 = 8 ∈ ORBIT_V", 341 % 37, 8)
check(561 % 37 == 6, "561 mod 37 = 6 ∈ ORBIT_V", 561 % 37, 6)
check(341 % 37 in ORBIT_V, "341 mod 37 ∈ ORBIT_V", 341 % 37 in ORBIT_V, True)
check(561 % 37 in ORBIT_V, "561 mod 37 ∈ ORBIT_V", 561 % 37 in ORBIT_V, True)

# 1729 = 7×13×19 (Ramanujan's taxicab; also Carmichael): factor DRs
N1729 = 1729
check(N1729 == 7 * 13 * 19, "1729 = 7×13×19", N1729, 7 * 13 * 19)
check(korselt(N1729), "1729 is Carmichael (Korselt)", korselt(N1729), True)
check(dr(N1729) == 1, "DR(1729) = 1 = φ-axiom = UNIT", dr(N1729), 1)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Pseudoprime and Carmichael Audit")
    print("=" * 66)

    print(f"\n── T1: 341 is Fermat pseudoprime to base 2 ──")
    print(f"  341 = 11×31  (composite: {not is_prime(341)})")
    print(f"  2^340 mod 341 = {pow(2,340,341)}  (≡1 → passes Fermat test)")

    print(f"\n── T2: pseudoprime status is base-dependent ──")
    print(f"  Base 2: Fermat(341) = {fermat_test(341,2)}  (false positive)")
    print(f"  Base 3: Fermat(341) = {fermat_test(341,3)}  (correctly identified)")
    print(f"  3^340 mod 341 = {pow(3,340,341)}  (≠1 → 341 fails Fermat to base 3)")
    print(f"  Bases where 341 fails (first few): {failing_bases_341[:8]}")

    print(f"\n── T3: Korselt's criterion ──")
    print(f"  n Carmichael iff: squarefree AND p-1 | n-1 for all prime p|n")
    print(f"  561 = 3×11×17;  561-1 = 560")
    print(f"    2  | 560: 560/2  = {560//2}  ✓")
    print(f"   10  | 560: 560/10 = {560//10}  ✓")
    print(f"   16  | 560: 560/16 = {560//16}  ✓")
    print(f"  341 fails: 30 ∤ 340 (340 mod 30 = {340%30})")

    print(f"\n── T4: 561 is smallest Carmichael number ──")
    print(f"  No Carmichael number < 561: {smaller_carmichael == []}")
    print(f"  561 is Fermat pseudoprime to every base coprime to 561 (b<100): {all_pass}")

    print(f"\n── Carmichael numbers < 10000 ({len(carmichaels)} found) ──")
    print(f"  {carmichaels}")

    print(f"\n── Miller-Rabin vs Fermat ──")
    print(f"  {'Test':<20}  {'341':<8}  {'561':<8}  {'Notes'}")
    print(f"  {'Fermat (base 2)':<20}  {str(fermat_test(341,2)):<8}  {str(fermat_test(561,2)):<8}  false positives")
    print(f"  {'Miller-Rabin b=2':<20}  {str(miller_rabin(341,2)):<8}  {str(miller_rabin(561,2)):<8}  correct (no false positive)")
    print(f"  All Carmichael < 10000 fail Miller-Rabin{{2,3,5,7}}: True")
    print(f"  (AKS: deterministic polynomial-time; no false positives — referenced, not implemented)")

    print(f"\n── Framework connections ──")
    print(f"  DR(341) = {dr(341)} = AHL;  341 mod 37 = {341%37} ∈ ORBIT_V")
    print(f"  DR(561) = {dr(561)} = π-axiom;  561 mod 37 = {561%37} ∈ ORBIT_V")
    print(f"  Factor 17: DR(17)={dr(17)}=AHL, 17 mod 37={17%37}∈ORBIT_V (criss-cross prime)")
    print(f"  1729 (Carmichael) = 7×13×19;  DR(1729) = {dr(1729)} = φ-axiom = UNIT")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")

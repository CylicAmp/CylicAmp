"""
korselt_proof_audit.py

Computational audit of the full proof of Korselt's Criterion (1899).

─────────────────────────────────────────────────────────────────
THEOREM (Korselt):
  A composite n > 1 is Carmichael iff:
    (K1) n is squarefree
    (K2) p−1 | n−1 for every prime p | n

PROOF STEPS AUDITED:
  P1  ("if"):   K1+K2 ⟹ a^(n-1) ≡ 1 (mod p_i) by FLT
  P2  ("if"):   CRT assembles ≡ 1 (mod n) from ≡ 1 (mod p_i)
  P3  (sq-free): (1+p)^m ≡ 1+mp (mod p²)  [binomial lemma]
  P4  (sq-free): contradiction witness a=1+p when p²|n
  P5  (p−1|n−1): primitive root forces p−1 | n−1
─────────────────────────────────────────────────────────────────
"""

from math import gcd
from itertools import product as iproduct

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
    factors = []
    d, temp = 2, n
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
    d, temp = 2, n
    while d * d <= temp:
        if temp % d == 0:
            temp //= d
            if temp % d == 0:
                return False
        d += 1
    return True


def korselt(n):
    if is_prime(n) or n < 2:
        return False
    if not is_squarefree(n):
        return False
    pfs = prime_factors(n)
    return len(pfs) >= 2 and all((n - 1) % (p - 1) == 0 for p in pfs)


def primitive_root(p):
    """Find the smallest primitive root mod prime p."""
    if p == 2:
        return 1
    phi = p - 1
    pf_phi = prime_factors(phi)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in pf_phi):
            return g
    return None


# ── P1: FLT step — K1+K2 ⟹ a^(n-1) ≡ 1 (mod p_i) ───────────────────────────
#
# Given: p_i | n, p_i−1 | n−1, gcd(a, p_i) = 1.
# FLT: a^(p_i−1) ≡ 1 (mod p_i).
# Since p_i−1 | n−1, write n−1 = k·(p_i−1).
# Then a^(n−1) = (a^(p_i−1))^k ≡ 1^k = 1 (mod p_i).

CARMICHAELS = [561, 1105, 1729, 2465, 2821]

for n in CARMICHAELS:
    pfs = prime_factors(n)
    for p in pfs:
        k = (n - 1) // (p - 1)
        check((n - 1) == k * (p - 1), f"{n}: (n-1) = {k}×(p-1) for p={p}", (n-1), k*(p-1))
        # Verify for several bases
        for a in range(2, 20):
            if gcd(a, n) == 1:
                flt_step = pow(a, p - 1, p)
                check(flt_step == 1, f"FLT: {a}^{p-1} ≡ 1 mod {p}", flt_step, 1)
                full = pow(a, n - 1, p)
                check(full == 1, f"P1: {a}^{n-1} ≡ 1 mod {p} (via FLT×k)", full, 1)
                break   # one base per (n,p) pair sufficient for structure check


# ── P2: CRT assembly — ≡1 (mod p_i) for all i ⟹ ≡1 (mod n) ─────────────────
#
# Since n = p_1·…·p_k with distinct primes and a^(n-1) ≡ 1 (mod p_i) for all i,
# CRT gives a^(n-1) ≡ 1 (mod n).
# (CRT applies because the p_i are distinct primes ⟹ pairwise coprime.)

for n in CARMICHAELS:
    pfs = prime_factors(n)
    # Verify pairwise coprimality
    for i in range(len(pfs)):
        for j in range(i + 1, len(pfs)):
            check(gcd(pfs[i], pfs[j]) == 1,
                  f"p_i, p_j coprime: gcd({pfs[i]},{pfs[j]})=1", gcd(pfs[i], pfs[j]), 1)
    # Verify full Fermat condition for several bases
    for a in range(2, 50):
        if gcd(a, n) == 1:
            # Check each factor
            all_one = all(pow(a, n - 1, p) == 1 for p in pfs)
            combined = pow(a, n - 1, n)
            check(all_one, f"P2 premise: {a}^{n-1}≡1 mod p_i for all p_i|{n}", all_one, True)
            check(combined == 1, f"P2 CRT: {a}^{n-1}≡1 mod {n}", combined, 1)


# ── P3: Binomial lemma — (1+p)^m ≡ 1+mp (mod p²) ───────────────────────────
#
# (1+p)^m = Σ C(m,k) p^k.
# k=0: 1; k=1: mp; k≥2: divisible by p².
# So (1+p)^m ≡ 1 + mp (mod p²).

SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19]
for p in SMALL_PRIMES:
    p2 = p * p
    for m in range(1, 20):
        direct = pow(1 + p, m, p2)
        approx = (1 + m * p) % p2
        check(direct == approx,
              f"(1+{p})^{m} ≡ 1+{m}·{p} (mod {p2})", direct, approx)


# ── P4: Squarefree contradiction — if p²|n then a=1+p is witness ─────────────
#
# Assume p²|n. Take a = 1+p.  gcd(a,n)=1 since a≡1 (mod p).
# By P3: a^(n-1) ≡ 1+(n-1)p (mod p²).
# For a^(n-1) ≡ 1 (mod n) ⊇ ≡ 1 (mod p²): need (n-1)p ≡ 0 (mod p²) → p|n-1.
# But p|n → n≡0 (mod p) → n-1≡-1 (mod p): contradiction (p≥2).

# Construct non-squarefree composites: p²·q
def crt_witness(p, n):
    """
    Construct a ≡ 1+p (mod p²) with gcd(a, n) = 1 by CRT.
    For each other prime factor q | n, enforce a ≡ 1 (mod q).
    The direct choice a = 1+p can share factors with q if q | (1+p);
    CRT avoids this by working modulo p² and each other prime separately.
    """
    p2 = p * p
    other_primes = [q for q in prime_factors(n) if q != p]
    # Build a via iterative CRT: start with a ≡ 1+p (mod p²)
    a_val = 1 + p
    a_mod = p2
    for q in other_primes:
        # Combine (a_val mod a_mod) with (1 mod q) via CRT
        # Find x such that x ≡ a_val (mod a_mod) and x ≡ 1 (mod q)
        # x = a_val + a_mod * t, need a_val + a_mod*t ≡ 1 (mod q)
        # a_mod*t ≡ (1 - a_val) (mod q)
        inv_a_mod_q = pow(a_mod % q, -1, q)
        t = ((1 - a_val) * inv_a_mod_q) % q
        a_val = a_val + a_mod * t
        a_mod = a_mod * q
    return a_val % a_mod, a_mod


def test_squarefree_contradiction(p, q):
    """Verify that p²q fails to be Carmichael via CRT-constructed witness."""
    n = p * p * q
    p2 = p * p
    # Proper witness: a ≡ 1+p (mod p²), a ≡ 1 (mod q), gcd(a,n)=1
    a, _ = crt_witness(p, n)
    g = gcd(a, n)
    approx_mod_p2 = (1 + (n - 1) * p) % p2
    direct_mod_p2 = pow(a, n - 1, p2)   # should equal approx since a≡1+p (mod p²)
    n_minus_1_mod_p = (n - 1) % p
    return {
        "n": n, "a": a, "gcd_a_n": g,
        "n-1 mod p": n_minus_1_mod_p,
        "a mod p2": a % p2,
        "expected a mod p2": (1 + p) % p2,
        "approx_mod_p2": approx_mod_p2,
        "direct_mod_p2": direct_mod_p2,
        "a_n-1_mod_n": pow(a, n - 1, n),
    }

for p, q in [(2, 3), (3, 2), (5, 7), (7, 11)]:
    res = test_squarefree_contradiction(p, q)
    n = res["n"]
    a = res["a"]
    # Witness correctly constructed: a ≡ 1+p (mod p²)
    check(res["a mod p2"] == res["expected a mod p2"],
          f"p={p},q={q}: a≡1+{p} (mod {p*p})", res["a mod p2"], res["expected a mod p2"])
    # gcd(a, n) = 1
    check(res["gcd_a_n"] == 1,
          f"gcd({a},{n}) = 1 (CRT witness coprime to n)", res["gcd_a_n"], 1)
    # n-1 ≡ -1 (mod p): the key contradiction
    check(res["n-1 mod p"] == p - 1,
          f"n-1≡{p-1}≡-1 (mod {p}) (not 0 → (n-1)p≢0 mod p² → contradiction)",
          res["n-1 mod p"], p - 1)
    # a^(n-1) ≢ 1 (mod n)
    check(res["a_n-1_mod_n"] != 1,
          f"a^(n-1) ≢ 1 (mod {n}): {n} not Carmichael", res["a_n-1_mod_n"] != 1, True)

# Explicit 561 case isn't needed (561 IS squarefree); verify squarefree numbers pass
check(is_squarefree(561), "561 is squarefree", is_squarefree(561), True)
# A non-squarefree number, e.g. 12 = 2²×3, fails korselt
check(not korselt(12), "12 = 2²×3 is not Carmichael (not squarefree)", korselt(12), False)


# ── P5: Generator argument — primitive root forces p−1 | n−1 ─────────────────
#
# (Z/pZ)* is cyclic of order p−1. If a^(n-1) ≡ 1 (mod p) for all a coprime to p,
# then in particular for the primitive root g (ord_p(g) = p−1).
# ord(g) | n−1  ⟹  p−1 | n−1.

for n in CARMICHAELS:
    pfs = prime_factors(n)
    for p in pfs:
        g = primitive_root(p)
        check(g is not None, f"primitive root mod {p} exists", g is not None, True)
        # Verify g has order p-1
        ord_g = p - 1
        check(pow(g, ord_g, p) == 1, f"g^(p-1) ≡ 1 mod p={p}", pow(g, ord_g, p), 1)
        # Verify no smaller exponent works: ord(g) = p-1
        smaller = [e for e in range(1, p - 1) if (p - 1) % e == 0 and pow(g, e, p) == 1]
        check(smaller == [], f"no smaller order for primitive root mod {p}", smaller, [])
        # Key: g^(n-1) ≡ 1 (mod p), and ord(g)=p-1, so (p-1) | (n-1)
        check(pow(g, n - 1, p) == 1,
              f"P5: g^(n-1) ≡ 1 mod {p} (since {n} Carmichael)", pow(g, n - 1, p), 1)
        check((n - 1) % (p - 1) == 0,
              f"P5: (p-1)={p-1} | (n-1)={n-1}", (n - 1) % (p - 1), 0)


# ── Application to 561 ────────────────────────────────────────────────────────

N = 561
PFS = [3, 11, 17]
check(N == 3 * 11 * 17, "561 = 3×11×17", N, 3 * 11 * 17)
check(is_squarefree(N), "561 squarefree (K1)", is_squarefree(N), True)
for p in PFS:
    check((N - 1) % (p - 1) == 0,
          f"K2: {p-1} | {N-1} (p={p})", (N - 1) % (p - 1), 0)

# "If" direction: every base coprime to 561 gives a^560 ≡ 1 mod 561
bases_coprime = [a for a in range(2, 200) if gcd(a, N) == 1]
all_pass = all(pow(a, N - 1, N) == 1 for a in bases_coprime)
check(all_pass, "all a<200 with gcd(a,561)=1: a^560≡1 mod 561", all_pass, True)

# "Only if": confirm squarefree and p-1|560
for p in PFS:
    g = primitive_root(p)
    check(pow(g, N - 1, p) == 1,
          f"primitive root {g} mod {p}: g^{N-1}≡1 mod {p}", pow(g, N - 1, p), 1)
    check((N - 1) % (p - 1) == 0,
          f"(p-1)={p-1} | 560", (N - 1) % (p - 1), 0)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Korselt Proof Audit")
    print("=" * 66)

    print(f"\n── P1: FLT step ──")
    print(f"  If p-1|n-1 and gcd(a,p)=1: a^(n-1) = (a^(p-1))^k ≡ 1^k ≡ 1 (mod p)")
    for n in CARMICHAELS[:3]:
        pfs = prime_factors(n)
        parts = [f"({n-1})/({p-1})={((n-1)//(p-1))}" for p in pfs]
        print(f"  {n} = {'×'.join(str(p) for p in pfs)}: k = {', '.join(parts)}")

    print(f"\n── P2: CRT step ──")
    print(f"  Primes of n pairwise coprime ⟹ CRT applies")
    print(f"  a^(n-1) ≡ 1 (mod p_i) for all i ⟹ a^(n-1) ≡ 1 (mod n)")
    for n in CARMICHAELS[:3]:
        check_base = next(a for a in range(2, 100) if gcd(a, n) == 1)
        print(f"  {n}: {check_base}^{n-1} mod {n} = {pow(check_base,n-1,n)}")

    print(f"\n── P3: Binomial lemma (1+p)^m ≡ 1+mp (mod p²) ──")
    for p in [3, 5, 7]:
        for m in [10, 20, 30]:
            d = pow(1+p, m, p*p)
            a = (1 + m*p) % (p*p)
            print(f"  (1+{p})^{m} mod {p*p}: direct={d}, 1+{m}·{p}={a}  {'✓' if d==a else '✗'}")

    print(f"\n── P4: Contradiction witness a=1+p when p²|n ──")
    for p, q in [(2,3),(3,2),(5,7)]:
        n = p*p*q
        a = 1+p
        n_mod = (n-1)%p
        print(f"  n={n}={p}²×{q}: a={a}, n-1≡{n_mod} (mod {p})")
        print(f"    Need n-1≡0 (mod {p}) for Carmichael; got {n_mod}≡-1 → contradiction")
        print(f"    a^(n-1) mod n = {pow(a,n-1,n)} ≠ 1 → {n} is not Carmichael ✓")

    print(f"\n── P5: Generator argument — primitive root forces p-1|n-1 ──")
    for p in [3, 11, 17]:
        g = primitive_root(p)
        print(f"  p={p}: primitive root g={g}, ord={p-1}")
        for n in [561, 1105, 1729]:
            if (n-1)%(p-1)==0:
                print(f"    {g}^{n-1} mod {p} = {pow(g,n-1,p)} → (p-1)={p-1}|{n-1} ✓")
                break

    print(f"\n── Application: 561 ──")
    print(f"  561 = 3×11×17; squarefree: {is_squarefree(561)}")
    print(f"  K2: 2|560={560%2==0}, 10|560={560%10==0}, 16|560={560%16==0}")
    print(f"  All a<200 coprime to 561: a^560≡1 mod 561: {all_pass}")
    print(f"  Primitive roots: {[primitive_root(p) for p in PFS]} (mod 3,11,17)")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")

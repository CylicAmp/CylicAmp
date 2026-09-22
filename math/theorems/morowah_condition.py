# math/theorems/morowah_condition.py
"""
Morowah Condition — Chahine's S_d / S_p symmetry
=================================================

For n ∈ ℕ, define:
    S_d(n) = digital_root(n)                   (1–9)
    S_p(n) = digital_root(Σ dr(p)·e  for p^e | n)  (weighted prime DR sum)

n satisfies the Morowah condition if there exist natural numbers a ≠ r
with a, r ∈ [1,9] such that:
    S_d(n) = a^r   and   S_p(n) = r^a

Valid (S_d, S_p) target pairs (a^r, r^a) with a≠r, both ≤ 9:
    (1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9)  — a=1 family
    (2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1)  — r=1 family
    (8,9)  — a=2,r=3: 2^3=8, 3^2=9
    (9,8)  — a=3,r=2: 3^2=9, 2^3=8

Note: pure primes have S_d = S_p, so they never produce a Morowah pair
(no solution to a^r = r^a ≤ 9 with a≠r in natural numbers).
"""

import math


# ── Core functions ────────────────────────────────────────────────────────────

def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def factorize(n: int) -> dict:
    """Trial division factorization. Returns {prime: exponent}."""
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


def prime_factors_digital_sum(n: int) -> int:
    """dr(Σ dr(p)·e) over all prime power factors p^e of n."""
    factors = factorize(n)
    total = sum(dr(p) * e for p, e in factors.items())
    return dr(total)


# All valid (S_d, S_p) Morowah targets
MOROWAH_TARGETS = {}
for _a in range(1, 10):
    for _r in range(1, 10):
        if _a != _r:
            sd_val = _a ** _r
            sp_val = _r ** _a
            if 1 <= sd_val <= 9 and 1 <= sp_val <= 9:
                MOROWAH_TARGETS[(sd_val, sp_val)] = (_a, _r)


def is_morowah(n: int):
    """Return (a, r) if n satisfies Morowah condition, else None."""
    key = (dr(n), prime_factors_digital_sum(n))
    return MOROWAH_TARGETS.get(key)


# ── Anchor tests ──────────────────────────────────────────────────────────────

def verify_anchors():
    print("Morowah Condition — Anchor Numbers\n")

    anchors = [11, 37, 111, 137, 248, 919]
    for n in anchors:
        sd   = dr(n)
        sp   = prime_factors_digital_sum(n)
        pair = is_morowah(n)
        fac  = factorize(n)
        print(f"  {n:4d}  factors={fac}  S_d={sd}  S_p={sp}  "
              f"Morowah={pair if pair else '—'}")

    # 248 is the only anchor that satisfies the condition
    assert is_morowah(248) == (5, 1)
    for n in [11, 37, 111, 137, 919]:
        assert is_morowah(n) is None

    print()
    print("  Verification: 248 = 2³×31")
    print(f"    S_d(248) = dr(248) = {dr(248)}  = 5¹  ✓")
    print(f"    S_p(248) = dr(dr(2)×3 + dr(31)×1) = dr(2×3 + 4×1) = dr(10) = {prime_factors_digital_sum(248)}  = 1⁵  ✓")
    print(f"    Pair (a=5, r=1): 5^1={5**1}, 1^5={1**5}  ✓")


# ── Valid target table ────────────────────────────────────────────────────────

def print_target_table():
    print("\nValid Morowah (S_d, S_p) targets:")
    print(f"  {'a':>3} {'r':>3} {'a^r=S_d':>8} {'r^a=S_p':>8}")
    for (sd, sp), (a, r) in sorted(MOROWAH_TARGETS.items()):
        print(f"  {a:>3} {r:>3} {sd:>8} {sp:>8}")
    print(f"  Total valid target pairs: {len(MOROWAH_TARGETS)}")


# ── Exhaustive scan 1–1000 ────────────────────────────────────────────────────

def scan_morowah(limit: int = 1000):
    hits = [(n, is_morowah(n)) for n in range(2, limit+1) if is_morowah(n)]
    print(f"\nMorowah numbers in [2, {limit}]:  {len(hits)} found")
    for n, pair in hits[:20]:
        sd = dr(n); sp = prime_factors_digital_sum(n)
        print(f"  {n:5d}  S_d={sd}  S_p={sp}  pair={pair}  factors={factorize(n)}")
    if len(hits) > 20:
        print(f"  ... ({len(hits)-20} more)")
    return hits


if __name__ == "__main__":
    verify_anchors()
    print_target_table()
    hits = scan_morowah(1000)
    print("\nAll assertions passed.")

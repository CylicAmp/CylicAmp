"""
euler_quadratic_twin_audit.py

Comparison of three quadratic prime-generators and their twin prime output.

─────────────────────────────────────────────────────────────────
POLYNOMIALS:
  E(n)  = n² + n + 41        (Euler's polynomial, disc = −163)
  P(k)  = 4k² − k + 41      (41-seeded variant)
  C(k)  = 4k² − 2k + 1      (Ulam NE diagonal)

PRIME COUNTS to k=1000:
  E:  582 primes   (58.1%)
  P:  116 primes   (11.6%)
  C:  166 primes   (16.6%)

KEY STRUCTURAL FINDINGS:

1. PARITY KILL on P:
   4k²−k+41 is even for every odd k (mod-2 root at k=1).
   Only even k can produce odd primes → effective pool halved.
   E(n) has NO roots mod 2 — always odd — full pool.

2. HEEGNER NUMBER advantage of E:
   disc(E) = 1−4×41 = −163 (Heegner number → class number 1).
   E has NO roots mod 2, 3, 5, 7, 11, or 13.
   E produces primes for n=0..39 (40 consecutive) — breaks at n=40:
   E(40) = 41² (composite).
   disc(P) = 1−4×4×41 = −655 = −5×131 (not Heegner — no bonus).
   disc(C) = 4−4×4 = −12.

3. MOD-3 TWIN PRIME FILTER on the Ulam diagonals:
   Twin pair at k requires both f(k) and f(k)+2 prime.

   A+2 = 4k²+2k+3 ≡ k(k+2) mod 3 → 0 when k≡0 OR k≡1 (mod 3)
         [2/3 of cases forced composite]
   B+2 = 4k²+3     ≡ k²    mod 3 → 0 when k≡0        (mod 3)
         [1/3 of cases forced composite]
   C+2 = 4k²−2k+3 ≡ k(k−2) mod 3 → 0 when k≡0 OR k≡2 (mod 3)
         [2/3 of cases forced composite]

   CONCLUSION: B is the primary twin-prime diagonal.
   A and C each shed 2/3 of twin candidates to mod-3 forcing.

TWIN PRIME PAIRS (f(k) prime AND f(k)+2 prime):
  A (k=1..200):  0 pairs
  B (k=1..200): 15 pairs — (5,7), (17,19), (101,103), (197,199)...
  C (k=1..200):  1 pair  — (3,5) at k=1 only
  E (n=0..1000): 65 pairs
─────────────────────────────────────────────────────────────────
"""

import sympy

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


def E(n):  return n*n + n + 41
def P(k):  return 4*k*k - k + 41
def C(k):  return 4*k*k - 2*k + 1
def A(k):  return 4*k*k + 2*k + 1
def B(k):  return 4*k*k + 1


# ── Parity: P is even for all odd k ──────────────────────────────────────────

for k in range(1, 20, 2):
    check(P(k) % 2 == 0,
          f"P({k})={P(k)} is even (odd k)", P(k) % 2, 0)

for n in range(20):
    check(E(n) % 2 == 1,
          f"E({n})={E(n)} is always odd", E(n) % 2, 1)


# ── Discriminants ─────────────────────────────────────────────────────────────

check(1 - 4*41   == -163, "disc(E) = -163 (Heegner)", 1 - 4*41,    -163)
check(1 - 4*4*41 == -655, "disc(P) = -655",            1 - 4*4*41,  -655)
check(4 - 4*4    == -12,  "disc(C) = -12",             4 - 4*4,     -12)


# ── Euler consecutive primes: n=0..39, breaks at n=40 ────────────────────────

for n in range(40):
    check(sympy.isprime(E(n)),
          f"E({n})={E(n)} prime", sympy.isprime(E(n)), True)

check(E(40) == 41**2, "E(40) = 41² (first composite)", E(40), 41**2)
check(not sympy.isprime(E(40)), "E(40) composite", sympy.isprime(E(40)), False)


# ── E has no roots mod 2,3,5,7,11,13 ────────────────────────────────────────

for p in [2, 3, 5, 7, 11, 13]:
    roots = [k for k in range(p) if E(k) % p == 0]
    check(roots == [],
          f"E has no roots mod {p}", roots, [])


# ── Prime counts to k=1000 ────────────────────────────────────────────────────

e_count = sum(1 for n in range(1001) if E(n) > 1 and sympy.isprime(E(n)))
p_count = sum(1 for k in range(1001) if P(k) > 1 and sympy.isprime(P(k)))
c_count = sum(1 for k in range(1001) if C(k) > 1 and sympy.isprime(C(k)))

check(e_count == 582, "E prime count to k=1000", e_count, 582)
check(p_count == 116, "P prime count to k=1000", p_count, 116)
check(c_count == 166, "C prime count to k=1000", c_count, 166)

# E leads C by how much?
check(e_count - c_count == 416, "E−C = 416", e_count - c_count, 416)
check(dr(e_count - c_count) == 2, "DR(416) = 2", dr(e_count - c_count), 2)


# ── Mod-3 twin filter on A, B, C ─────────────────────────────────────────────

# A+2 ≡ k(k+2) mod 3 → 0 when k≡0 or k≡1 (mod 3)
for k in range(30):
    expected_zero = (k % 3 in {0, 1})
    check((A(k) + 2) % 3 == 0 if expected_zero else (A(k) + 2) % 3 != 0,
          f"A({k})+2 mod-3 zero iff k≡0,1 (mod 3)",
          (A(k) + 2) % 3 == 0, expected_zero)

# B+2 ≡ k² mod 3 → 0 when k≡0 (mod 3) only
for k in range(30):
    expected_zero = (k % 3 == 0)
    check((B(k) + 2) % 3 == 0 if expected_zero else (B(k) + 2) % 3 != 0,
          f"B({k})+2 mod-3 zero iff k≡0 (mod 3)",
          (B(k) + 2) % 3 == 0, expected_zero)

# C+2 ≡ k(k-2) mod 3 → 0 when k≡0 or k≡2 (mod 3)
for k in range(30):
    expected_zero = (k % 3 in {0, 2})
    check((C(k) + 2) % 3 == 0 if expected_zero else (C(k) + 2) % 3 != 0,
          f"C({k})+2 mod-3 zero iff k≡0,2 (mod 3)",
          (C(k) + 2) % 3 == 0, expected_zero)


# ── Twin prime pairs ──────────────────────────────────────────────────────────

def twin_count(fn, k_start, k_end):
    return [(k, fn(k), fn(k)+2)
            for k in range(k_start, k_end+1)
            if fn(k) > 1 and sympy.isprime(fn(k)) and sympy.isprime(fn(k)+2)]

# k=1..200
twins_A = twin_count(A, 1, 200)
twins_B = twin_count(B, 1, 200)
twins_C = twin_count(C, 1, 200)

check(len(twins_A) == 0,  "A twin pairs k=1..200: 0", len(twins_A), 0)
check(len(twins_B) == 15, "B twin pairs k=1..200: 15", len(twins_B), 15)
check(len(twins_C) == 1,  "C twin pairs k=1..200: 1",  len(twins_C), 1)

# B's first four twin pairs
B_first4 = [(k, p, p+2) for k, p, _ in twins_B[:4]]
check(B_first4[0] == (1, 5, 7),      "B k=1: (5,7)",       B_first4[0], (1, 5, 7))
check(B_first4[1] == (2, 17, 19),    "B k=2: (17,19)",     B_first4[1], (2, 17, 19))
check(B_first4[2] == (5, 101, 103),  "B k=5: (101,103)",   B_first4[2], (5, 101, 103))
check(B_first4[3] == (7, 197, 199),  "B k=7: (197,199)",   B_first4[3], (7, 197, 199))

# C's one pair is (3,5) at k=1
check(twins_C[0] == (1, 3, 5), "C k=1: (3,5)", twins_C[0], (1, 3, 5))

# Euler twin pairs n=0..1000
twins_E = [(n, E(n)) for n in range(1001)
           if E(n) > 1 and sympy.isprime(E(n)) and sympy.isprime(E(n)+2)]
check(len(twins_E) == 65, "E twin pairs n=0..1000: 65", len(twins_E), 65)

# First Euler twin pairs
check(twins_E[0] == (0, 41),  "E n=0: (41,43)",   twins_E[0], (0, 41))
check(twins_E[1] == (5, 71),  "E n=5: (71,73)",   twins_E[1], (5, 71))
check(twins_E[2] == (12, 197),"E n=12: (197,199)",twins_E[2], (12, 197))

# Twin prime ratio B/E (density comparison)
# B produces 15 twins in 200 steps; E produces 65 in 1001 steps
# Per-step rates: B=0.075, E=0.065 — B slightly higher in this window
check(15/200 > 65/1001, "B twin rate > E twin rate in these ranges",
      15/200 > 65/1001, True)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Euler vs Ulam Quadratics — Prime Density and Twin Prime Audit")
    print("=" * 66)

    print(f"\n── Polynomial definitions ──")
    print(f"  E(n) = n² + n + 41      disc = -163 (Heegner)")
    print(f"  P(k) = 4k² − k + 41    disc = -655 = -5×131")
    print(f"  C(k) = 4k² − 2k + 1   disc = -12")

    print(f"\n── Parity ──")
    print(f"  P(k) even for ALL odd k → prime only when k even")
    print(f"  E(n) odd for ALL n ≥ 0  → full candidate pool")

    print(f"\n── Euler consecutive primes ──")
    print(f"  n=0..39: all 40 values prime")
    print(f"  n=40: E(40) = {E(40)} = 41² (composite)")

    print(f"\n── Roots mod small primes ──")
    print(f"  {'p':>4}  {'E roots':>10}  {'P roots':>10}  {'C roots':>10}")
    for p in [2, 3, 5, 7, 11, 13]:
        re = [k for k in range(p) if E(k) % p == 0]
        rp = [k for k in range(p) if P(k) % p == 0]
        rc = [k for k in range(p) if C(k) % p == 0]
        print(f"  {p:>4}  {str(re):>10}  {str(rp):>10}  {str(rc):>10}")

    print(f"\n── Prime counts to k=1000 ──")
    print(f"  E: {e_count} ({e_count/10.01:.1f}%)")
    print(f"  P: {p_count} ({p_count/10.01:.1f}%)")
    print(f"  C: {c_count} ({c_count/10.01:.1f}%)")

    print(f"\n── Mod-3 twin filter ──")
    print(f"  A+2: ≡0 mod 3 when k≡0,1 → 2/3 forced composite")
    print(f"  B+2: ≡0 mod 3 when k≡0   → 1/3 forced composite")
    print(f"  C+2: ≡0 mod 3 when k≡0,2 → 2/3 forced composite")
    print(f"  B is the primary twin-prime diagonal")

    print(f"\n── Twin prime pairs (f(k) and f(k)+2 both prime) ──")
    print(f"  A k=1..200:  {len(twins_A):3d} pairs")
    print(f"  B k=1..200:  {len(twins_B):3d} pairs  {[(k,p) for k,p,_ in twins_B[:6]]}")
    print(f"  C k=1..200:  {len(twins_C):3d} pairs  {[(k,p) for k,p,_ in twins_C]}")
    print(f"  E n=0..1000: {len(twins_E):3d} pairs")
    print(f"  First Euler twins: {[(n,p) for n,p in twins_E[:8]]}")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")

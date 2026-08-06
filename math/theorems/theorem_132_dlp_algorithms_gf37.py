"""
Theorem 132: Discrete Logarithm Algorithms in GF(37)

Group: (ℤ/37ℤ)×  =  ⟨2⟩,  order φ(37) = 36 = 2²×3²

36 is EXTREMELY SMOOTH (largest prime factor is 3).
Pohlig-Hellman reduces every DLP here to sub-problems of size 4 and 9.
This makes (ℤ/37ℤ)× useless for cryptography but perfect for complete
verification: every algorithm can be run to completion and cross-checked.

ALGORITHM COMPARISON ON GF(37)*
=================================

  Algorithm         Time         Memory   GF(37) cost
  Brute force       O(n)=O(36)   O(1)    ≤ 36 multiplications
  Baby-step giant-step O(√n)≈6   O(6)    6 babysteps + ≤6 giant steps
  Pollard rho       O(√n)≈6      O(1)    ~6 steps expected
  Pohlig-Hellman    O(Σ eᵢ√pᵢ)  O(1)    sub-problems of size 2, 3

POHLIG-HELLMAN REDUCTION
=========================

36 = 2² × 3²  →  decompose DLP into mod-4 and mod-9 sub-problems.

mod-4 sub-problem (Sylow 2, size 4):
  Elements {1, 6, 31, 36} = one from each of IC, TESLA_ORB, ORBIT_11, NQR_14.
  At most 2 steps each at two lifting stages.

mod-9 sub-problem (Sylow 3, size 9):
  Elements IC ∪ SA_ORB ∪ D7 = {1,7,9,10,12,16,26,33,34}.
  Inner sub-problem of size 3 (mod 3 first, then lift to mod 9).

CRT recombination: x mod 36 = CRT(x mod 4, x mod 9).
"""

P = 37
G = 2   # primitive root mod 37, ord₃₇(2) = 36

# Named classes
IC     = frozenset({1,  10, 26})
SA_ORB = frozenset({9,  12, 16})
D7     = frozenset({7,  33, 34})
SA     = frozenset({4,  9,  25, 30})
ST     = frozenset({3,  12, 21, 30})
CB     = frozenset({8,  13, 24})


def dr(n):
    if n == 0: return 9
    return (abs(n) - 1) % 9 + 1


# ── Algorithm 1: Brute Force ──────────────────────────────────────────────────

def dlp_brute(g, h, p=P):
    """Solve g^k ≡ h (mod p) by exhaustive search. O(p)."""
    x = 1
    for k in range(p - 1):
        if x == h:
            return k
        x = (x * g) % p
    return None


# ── Algorithm 2: Baby-step Giant-step ─────────────────────────────────────────

def dlp_bsgs(g, h, n, p=P):
    """Solve g^k ≡ h (mod p) via BSGS. O(√n) time and space."""
    import math
    m = math.isqrt(n) + 1

    # Baby steps: table of g^j for j=0..m-1
    table = {}
    gj = 1
    for j in range(m):
        table[gj] = j
        gj = (gj * g) % p

    # Giant steps: compute h · (g^{-m})^i = h · (g^m)^{-i}
    gm_inv = pow(pow(g, m, p), p - 2, p)
    cur = h
    for i in range(m + 1):
        if cur in table:
            k = i * m + table[cur]
            if k > 0:
                return k % n
        cur = (cur * gm_inv) % p
    return None


# ── Algorithm 3: Pollard Rho ──────────────────────────────────────────────────

def dlp_pollard_rho(g, h, n, p=P):
    """Solve g^k ≡ h (mod p) via Pollard rho (Floyd's cycle detection).
    For smooth n, falls back to brute force when r is not coprime to n."""
    from math import gcd

    def f(x, a, b):
        if x % 3 == 1:
            return (h * x) % p, a, (b + 1) % n
        elif x % 3 == 2:
            return (x * x) % p, (2 * a) % n, (2 * b) % n
        else:
            return (g * x) % p, (a + 1) % n, b

    x, a, b = 1, 0, 0
    X, A, B = 1, 0, 0
    for _ in range(n * 2):
        x, a, b = f(x, a, b)
        X, A, B = f(*f(X, A, B))
        if x == X:
            r = (b - B) % n
            if r == 0 or gcd(r, n) > 1:
                return dlp_brute(g, h, p)   # fallback for smooth n
            k = (A - a) * pow(r, -1, n) % n
            if pow(g, k, p) == h:
                return k
            return dlp_brute(g, h, p)
    return dlp_brute(g, h, p)


# ── Algorithm 4: Pohlig-Hellman ───────────────────────────────────────────────

def dlp_pohlig_hellman(g, h, p=P):
    """Solve g^k ≡ h (mod p) via Pohlig-Hellman. Requires n = φ(p) = 36 = 4×9."""
    n = p - 1   # 36

    # ── Mod-4 sub-problem (Sylow 2-subgroup) ──────────────────────────────
    g4 = pow(g, n // 4, p)   # order 4
    h4 = pow(h, n // 4, p)
    x4 = dlp_brute(g4, h4, p) or 0

    # ── Mod-9 sub-problem (Sylow 3-subgroup) ──────────────────────────────
    g9 = pow(g, n // 9, p)   # order 9
    h9 = pow(h, n // 9, p)
    # inner mod-3
    g3 = pow(g9, 3, p)       # order 3
    h3 = pow(h9, 3, p)
    x3 = dlp_brute(g3, h3, p) or 0
    # lift to mod-9
    h9b = (h9 * pow(pow(g9, x3, p), p - 2, p)) % p
    x3b = dlp_brute(g3, h9b, p) or 0
    x9 = x3 + 3 * x3b

    # ── CRT: x mod 4, x mod 9 → x mod 36 ─────────────────────────────────
    # 4^{-1} mod 9 = 7
    t = ((x9 - x4) * 7) % 9
    x = x4 + 4 * t
    return x % n


# ── Verification: all algorithms agree on every element ──────────────────────

def verify_all_algorithms():
    errors = []
    for h in range(1, P):
        bf   = dlp_brute(G, h)
        bsgs = dlp_bsgs(G, h, P - 1)
        ph   = dlp_pohlig_hellman(G, h)
        pr   = dlp_pollard_rho(G, h, P - 1)

        # All should satisfy 2^k ≡ h (mod 37)
        for name, k in [('brute', bf), ('bsgs', bsgs), ('ph', ph), ('rho', pr)]:
            if k is None or pow(G, k, P) != h:
                errors.append(f"  {name}: h={h} → k={k}, check={pow(G,k,P) if k else '?'}")

    if errors:
        print("ERRORS:")
        for e in errors: print(e)
    else:
        print("All four algorithms agree on all 36 discrete logs in GF(37)*.")


# ── Complete DLP table ────────────────────────────────────────────────────────

def dlp_table():
    """Print complete discrete log table log₂(h) mod 37 for h=1..36."""
    print(f"{'h':>4}  {'k=log₂(h)':>10}  {'orbit':20}  {'cross':10}  {'DR(h)':>6}")
    print("  " + "-" * 58)

    orbits = {
        'IC':IC, 'SA_ORB':SA_ORB, 'D7':D7,
        'SOVEREIGN_SPIRAL':frozenset({3,4,30}),
        'OUTLIER_ORB':frozenset({21,25,28}),
        'ORBIT_11':frozenset({11,27,36}),
        'DARK_A':frozenset({2,15,20}),
        'NQR_5':frozenset({5,13,19}),
        'TESLA_ORB':frozenset({6,8,23}),
        'NQR_14':frozenset({14,29,31}),
        'NQR_17':frozenset({17,22,35}),
        'SEED_ORB':frozenset({18,24,32}),
    }
    def orbit_of(r):
        for name, s in orbits.items():
            if r in s: return name
        return '?'
    def cross(r):
        parts = []
        if r in SA: parts.append('SA')
        if r in ST: parts.append('ST')
        if r in CB: parts.append('CB')
        return '+'.join(parts) or '—'

    for h in range(1, P):
        k = dlp_pohlig_hellman(G, h)
        orb = orbit_of(h)
        cr  = cross(h)
        print(f"  {h:>2}  {k:>10}  {orb:<20}  {cr:<10}  {dr(h):>6}")


# ── Cryptographic insecurity note ─────────────────────────────────────────────

def security_analysis():
    print()
    print("SECURITY ANALYSIS — (ℤ/37ℤ)×")
    print("=" * 44)
    print(f"  Order:         36 = 2² × 3²  (smooth)")
    print(f"  Primitive root: {G}  (ord₃₇({G}) = 36)")
    print(f"  Pohlig-Hellman: sub-problems of size 4 and 9")
    print(f"  Brute force:   ≤36 multiplications")
    print(f"  BSGS:          m = ⌈√36⌉ = 6 babysteps")
    print()
    print("  WHY INSECURE FOR CRYPTO:")
    print("  Cryptographic groups need n with a large prime factor.")
    print("  36 = 4×9 has largest prime factor 3 — trivially attacked.")
    print()
    print("  WHY VALUABLE FOR MATH:")
    print("  Complete verifiability. Every algorithm terminates immediately.")
    print("  GF(37) is the minimal prime field where the 137-map structure")
    print("  (12 orbits of size 3 under ×26) emerges at all.")
    print("  The smooth order enables exhaustive cross-checking of structure.")


if __name__ == "__main__":
    verify_all_algorithms()
    print()
    dlp_table()
    security_analysis()

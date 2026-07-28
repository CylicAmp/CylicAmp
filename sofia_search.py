#!/usr/bin/env python3
"""
Sofia Germain Prime Search — GF(37)-guided

A "Sofia prime" is a Sophie Germain prime p = k × 2^n − 1 where
p ≡ SCALAR_137 = 26 mod 37.  This requires:
  k × 2^n ≡ 27 mod 37
  → with n ≡ 12 mod 36 (so 2^n ≡ 26 = SCALAR_137): k ≡ 11 mod 37
  → with n ≡  0 mod 36 (so 2^n ≡  1): k ≡ 27 mod 37
  → with n ≡  6 mod 36 (so 2^n ≡ 27 ∈ ORBIT_11): k ≡ 1 mod 37 (∈ IC)
  ... etc.

Strategy:
  For each n in {search_n_list}, precompute 2^n once.
  Sieve k values to eliminate those with small prime factors in p or q.
  Full Miller-Rabin on survivors; record any Sophie Germain prime found.

The world record is p = 2618163402417 × 2^1290000 − 1 (~388k digits).
That scale requires ~18h per candidate; we search at n ~ 100–10000 (30–3000 digits)
to find examples and demonstrate the method.
"""

import gmpy2
from gmpy2 import mpz, is_prime
import time
import sys

# ── Constants ────────────────────────────────────────────────────────────────

SA   = frozenset({4,9,25,30})
ST   = frozenset({3,12,21,30})
CB   = frozenset({8,13,24})
IC   = frozenset({1,10,26})
O2   = frozenset({9,12,16})
OB11 = frozenset({11,27,36})
SEED = frozenset({18,24,32})
SCALAR_137 = 26

def dr(n): return 0 if n==0 else 1+(n-1)%9

def classify(r):
    tags = []
    if r in SA:   tags.append('SA')
    if r in ST:   tags.append('ST')
    if r in CB:   tags.append('CB')
    if r in IC:   tags.append('IC')
    if r in O2:   tags.append('O2')
    if r in OB11: tags.append('ORBIT_11')
    if r in SEED: tags.append('SEED')
    return ','.join(tags) if tags else str(r)

# ── Sieve ────────────────────────────────────────────────────────────────────

def small_primes_up_to(b):
    sieve = bytearray([1]) * (b+1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(b**0.5)+1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
    return [i for i in range(2, b+1) if sieve[i]]

SPRIMES = small_primes_up_to(50000)

def build_sieve_table(n):
    """
    For each small prime r (r != 2), compute residues of k mod r
    that cause r to divide p = k*2^n-1 or q = k*2^{n+1}-1.
    Returns: list of (r, bad_k_mod_r_for_p, bad_k_mod_r_for_q)
    """
    table = []
    for r in SPRIMES:
        if r == 2: continue
        pow2n   = pow(2, n,   r)
        pow2n1  = pow(2, n+1, r)
        if pow2n  == 0: continue   # r | 2^n, skip (r must be odd so this won't happen)
        # p ≡ 0 mod r iff k*pow2n ≡ 1 mod r iff k ≡ pow(pow2n, r-2, r)
        bad_p = pow(pow2n,  r-2, r)  # inverse
        bad_q = pow(pow2n1, r-2, r)
        table.append((r, bad_p, bad_q))
    return table

def passes_sieve(k_int, table):
    for r, bad_p, bad_q in table:
        kmod = k_int % r
        if kmod == bad_p or kmod == bad_q:
            return False
    return True

# ── Search ───────────────────────────────────────────────────────────────────

def search_n(n, k_start=3, k_max=10_000_000, target_p37=SCALAR_137,
             verbose=True, mr_rounds=25):
    """
    Search k values in [k_start, k_max] for given n.
    Only tests k where k*2^n-1 ≡ target_p37 mod 37 (GF(37) filter).
    Returns list of (k, n, p_mod37, q_mod37, p_dr, q_dr) for found pairs.
    """
    # GF(37) constraint: k * pow(2,n,37) ≡ target_p37+1 mod 37
    pow2n_37 = pow(2, n, 37)
    need_kpow = (target_p37 + 1) % 37   # k*2^n must be ≡ this mod 37
    # k ≡ need_kpow * pow(pow2n_37, 35, 37) mod 37 (Fermat inverse)
    k_residue = (need_kpow * pow(pow2n_37, 35, 37)) % 37

    # Build sieve table (once per n)
    t_sieve = time.time()
    table = build_sieve_table(n)
    t_sieve = time.time() - t_sieve

    # Precompute 2^n (expensive, done once)
    t_pow = time.time()
    POW2N = mpz(2) ** n
    t_pow = time.time() - t_pow

    if verbose:
        print(f"\nn={n}  2^n≡{pow2n_37} mod37  need k≡{k_residue} mod37")
        print(f"  sieve built in {t_sieve:.2f}s, pow2n built in {t_pow:.4f}s")
        print(f"  searching k in [{k_start}, {k_max}]...")

    found = []
    tested = 0
    sieve_pass = 0
    t0 = time.time()
    last_report = t0

    # Step through k values ≡ k_residue mod 37
    # Start from first k >= k_start with correct residue
    k_int = k_start
    rem = k_int % 37
    if rem != k_residue:
        k_int += (k_residue - rem) % 37

    while k_int <= k_max:
        # Quick sieve
        if passes_sieve(k_int, table):
            sieve_pass += 1
            # Compute p = k * 2^n - 1
            p = mpz(k_int) * POW2N - 1
            if is_prime(p, mr_rounds):
                q = 2 * p + 1
                if is_prime(q, mr_rounds):
                    p37 = (k_int * pow2n_37 - 1) % 37
                    q37 = (2 * p37 + 1) % 37
                    p9  = (k_int * pow(2, n, 9) - 1) % 9
                    q9  = (2 * p9 + 1) % 9
                    result = {
                        'k': k_int, 'n': n,
                        'digits': p.num_digits(),
                        'p_mod37': p37, 'p_class': classify(p37),
                        'q_mod37': q37, 'q_class': classify(q37),
                        'dr_p': p9 if p9 > 0 else 9,
                        'dr_q': q9 if q9 > 0 else 9,
                    }
                    found.append(result)
                    print(f"\n  *** FOUND: k={k_int}, n={n}, digits={p.num_digits()}")
                    print(f"      p mod37={p37} ({classify(p37)}), q mod37={q37} ({classify(q37)})")
                    print(f"      DR(p)={result['dr_p']}, DR(q)={result['dr_q']}")

        tested += 1
        k_int += 37   # step to next k with same residue mod 37

        now = time.time()
        if verbose and now - last_report > 30:
            rate = tested / (now - t0)
            print(f"  {tested:,} tested, {sieve_pass:,} passed sieve, "
                  f"{rate:.0f}/s, {len(found)} found  [k={k_int}]")
            last_report = now

    elapsed = time.time() - t0
    if verbose:
        print(f"  Done: {tested:,} k-values tested, {sieve_pass:,} passed sieve, "
              f"{len(found)} found  ({elapsed:.1f}s)")
    return found

# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Sofia Germain Prime Search — GF(37) guided")
    print("=" * 60)
    print(f"Target: p ≡ {SCALAR_137} = SCALAR_137 ∈ IC mod 37")
    print(f"World record: 2618163402417 × 2^1290000 − 1  (~388k digits)")
    print()

    all_found = []

    # Phase 1: small n (fast, demonstrate concept)
    for n in [500, 1000, 2000, 5000]:
        results = search_n(n, k_start=3, k_max=5_000_000,
                           target_p37=SCALAR_137, verbose=True, mr_rounds=15)
        all_found.extend(results)

    print("\n" + "=" * 60)
    print(f"SUMMARY: {len(all_found)} Sofia primes found")
    if all_found:
        biggest = max(all_found, key=lambda r: r['digits'])
        print(f"Largest: k={biggest['k']} × 2^{biggest['n']} − 1  ({biggest['digits']} digits)")
        print(f"  p mod37={biggest['p_mod37']} ({biggest['p_class']})")
        print(f"  q mod37={biggest['q_mod37']} ({biggest['q_class']})")
        print(f"  DR(p)={biggest['dr_p']}  DR(q)={biggest['dr_q']}")
        print()
        print("All found Sofia primes (p ≡ SCALAR_137 mod 37):")
        for r in sorted(all_found, key=lambda x: x['digits']):
            print(f"  {r['k']} × 2^{r['n']} − 1  "
                  f"({r['digits']} digits)  "
                  f"q≡{r['q_mod37']}({r['q_class']})  "
                  f"DR={r['dr_p']}/{r['dr_q']}")

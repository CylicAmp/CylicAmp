# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 262: E8 Theta Function mod 37 — Zero Distribution and GF(37) Structure
================================================================================

E8 THETA FUNCTION:
  Θ_{E8}(q) = 1 + 240·Σ_{n≥1} σ₃(n)·qⁿ
  where σ₃(n) = sum of cubes of divisors of n.

  Coefficients: a(n) = 240·σ₃(n) for n ≥ 1.
  a(n) mod 37 = 0 ⟺ 37 | σ₃(n)  (since gcd(240,37)=1; 240≡18 mod 37)

VERIFIED RESULT (n=1..5000):
  Zeros: 761 out of 5,000 = 15.2%

ZERO ENRICHMENT STRUCTURE (verified):
  n ≡ 0 (mod 11): 416/454 = 91.6% zero rate; 6.0× enrichment over baseline
    Reason: 11 ∈ -H = {11,27,36}; σ₃(11) = 1+11³ = 1332 = 36·37 ≡ 0 (mod 37)
    Any multiple of 11 picks up this factor; most give σ₃(11k)≡0.
  n ≡ 0 (mod 37): 15/135 = 11.1% zero rate
    Note: σ₃(37) = 1 + 37³ ≡ 1 (mod 37) → n=37 itself is NOT a zero.
    Zeros at multiples of 37 arise from other divisors.

CONNECTION TO THEOREM 257 (σ₃ DIVISIBILITY):
  37|σ₃(p) ⟺ p∈{11,27,36} (mod 37) = -H (cube roots of -1 mod 37)
  240 mod 37 = 18 ∈ SEED = {18,24,32}
  E8 coefficient a(n) = 240·σ₃(n); 240 ≡ 18 (mod 37), 18 ∈ SEED orbit

  The SEED orbit under the 137-map: 18 → 24 → 32 → 18.
  The E8 scaling factor 240 ≡ 18 (mod 37) places the theta function
  at the SEED entry point of the orbit.

GF(37) KEY FACTS:
  37 | σ₃(n) for:
    n = p with p ≡ 11, 27, or 36 (mod 37): σ₃(p) = 1+p³ ≡ 0 (T257)
    n = 11k for most k (since 37|σ₃(11) and σ₃ is multiplicative-like)
  37 ∤ σ₃(37): σ₃(37) = 1+37³ ≡ 1+0 = 1 (mod 37) ≠ 0
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from math import gcd

P = 37
H    = {1, 10, 26}
SA   = {4, 9, 25, 30}
ST   = {3, 12, 21, 30}
SEED = {18, 24, 32}
NEG_H = {11, 27, 36}
CASCADE = {8, 13, 24}


def sigma3_mod(n, m):
    s = 0
    for d in range(1, n+1):
        if n % d == 0:
            s = (s + pow(d, 3, m)) % m
    return s


def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i*i <= n:
        if n%i==0 or n%(i+2)==0: return False
        i += 6
    return True


def run():
    print("=" * 70)
    print("THEOREM 262: E8 THETA FUNCTION MOD 37 — ZERO DISTRIBUTION")
    print("=" * 70)

    A240 = 240 % P
    print(f"\n240 mod 37 = {A240} ∈ SEED = {{18,24,32}}")
    assert A240 == 18 and A240 in SEED
    assert gcd(A240, P) == 1
    print(f"gcd(240,37) = 1 ⟹ a(n)≡0 (mod 37) ⟺ 37|σ₃(n)  check")

    # σ₃(11) verification
    s11 = sigma3_mod(11, P)
    assert s11 == 0
    assert 11 in NEG_H
    print(f"\nσ₃(11) mod 37 = {s11}  (1332 = 36·37; 11 ∈ -H)  check")

    # σ₃(37) — note: NOT zero
    s37 = sigma3_mod(37, P)
    print(f"σ₃(37) mod 37 = {s37}  (1 + 37³ ≡ 1; NOT zero)  check")
    assert s37 == 1

    N = 5000
    print(f"\nComputing E8 theta zeros (n=1..{N})...")
    zeros = [n for n in range(1, N+1) if sigma3_mod(n, P) == 0]

    print(f"Zeros: {len(zeros)} out of {N} = {len(zeros)/N*100:.1f}%")

    # n ≡ 0 mod 11 enrichment
    zeros_mod11 = [n for n in zeros if n % 11 == 0]
    all_mod11   = [n for n in range(1, N+1) if n % 11 == 0]
    rate_mod11  = len(zeros_mod11) / len(all_mod11)
    baseline    = len(zeros) / N
    enrichment  = rate_mod11 / baseline
    print(f"\nn≡0 (mod 11): {len(zeros_mod11)}/{len(all_mod11)} zeros "
          f"= {rate_mod11*100:.1f}%")
    print(f"Baseline: {baseline*100:.1f}%  Enrichment: {enrichment:.1f}×  check")

    # n ≡ 0 mod 37
    zeros_mod37 = [n for n in zeros if n % 37 == 0]
    all_mod37   = [n for n in range(1, N+1) if n % 37 == 0]
    print(f"\nn≡0 (mod 37): {len(zeros_mod37)}/{len(all_mod37)} zeros "
          f"= {len(zeros_mod37)/len(all_mod37)*100:.1f}%")
    print(f"σ₃(37)≡1 (mod 37) → n=37 itself is not a zero")

    # Prime zeros — all should be in -H
    prime_zeros = [n for n in zeros if is_prime(n)]
    violations = [p for p in prime_zeros if p % P not in NEG_H]
    assert len(violations) == 0
    print(f"\nPrime zeros: {len(prime_zeros)}")
    print(f"All have p mod 37 ∈ -H = {{11,27,36}}  check")
    print(f"Sample: {prime_zeros[:10]}")
    for p in prime_zeros[:5]:
        print(f"  p={p}, p mod 37={p%P} ∈ -H, σ₃(p)=1+p³≡0  check")

    # Residue distribution
    from collections import Counter
    res_counts = Counter(n % P for n in zeros)
    zero_res = [r for r in range(1, P) if res_counts[r] == 0]
    print(f"\nResidues with 0 zero-hits (n mod 37): {zero_res}")
    top5 = sorted(res_counts.items(), key=lambda x: -x[1])[:5]
    print(f"Top 5 residues by count: {top5}")

    # SEED orbit counts
    print(f"\nSEED orbit {sorted(SEED)} zero counts:")
    for s in sorted(SEED):
        c = res_counts.get(s, 0)
        print(f"  n≡{s} (mod 37): {c} zeros")

    # -H counts
    print(f"\n-H = {{11,27,36}} zero counts:")
    for s in sorted(NEG_H):
        c = res_counts.get(s, 0)
        print(f"  n≡{s} (mod 37): {c} zeros")

    print(f"\nGF(37) SUMMARY:")
    print(f"  240 ≡ 18 ∈ SEED: E8 scaling enters at SEED orbit node 18")
    print(f"  37|σ₃(p) ⟺ p∈-H (Theorem 257) — prime zeros classified")
    print(f"  11∈-H: σ₃(11)≡0 drives the mod-11 enrichment (6×)")
    print(f"  σ₃(37)≡1 ≠ 0: multiples of 37 not automatically zeros")

    print(f"\nAll verifications passed.")
    print(f"\nSUMMARY: E8 theta mod 37: {len(zeros)}/5000 = "
          f"{len(zeros)/N*100:.1f}% zeros.")
    print(f"Prime zeros: all have p≡11,27,36 (mod 37) = -H (cube roots of -1).")
    print(f"E8 scaling 240 ≡ 18 ∈ SEED = 137-map orbit of reference seed 246.")


if __name__ == "__main__":
    run()

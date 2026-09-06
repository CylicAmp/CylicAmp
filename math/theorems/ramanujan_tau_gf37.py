# -*- coding: utf-8 -*-
"""
THEOREM 260: Ramanujan τ mod 37 — GF(37) Classification
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
SA    = {4,9,25,30}
ST    = {3,12,21,30}
H     = {1,10,26}
SEED  = {18,24,32}
C3    = {3,4,30}
C9    = {14,29,31}
NEG_H = {11,27,36}
CASCADE = {8,13,24}

def dr(n):
    n=abs(n)
    if n==0: return 0
    r=n%9; return 9 if r==0 else r

def is_prime(n):
    if n<2: return False
    for i in range(2,int(n**0.5)+1):
        if n%i==0: return False
    return True

def compute_tau_mod(N, m):
    # Δ(q) = q * prod_{k>=1} (1-q^k)^24
    # Correct approach: apply (1-q^k) 24 times for each k
    # coeffs[i] = coeff of q^i in prod_{k=1}^{N} (1-q^k)^24
    coeffs = [0]*(N+1)
    coeffs[0] = 1
    for k in range(1, N+1):
        for _ in range(24):
            # multiply by (1-q^k) in place, high to low
            for i in range(N, k-1, -1):
                coeffs[i] = (coeffs[i] - coeffs[i-k]) % m
    # tau(n) = coeffs[n-1]  (shift by one factor of q)
    tau = [0]*(N+1)
    for n in range(1, N+1):
        tau[n] = coeffs[n-1]
    return tau

def classify(r):
    tags=[]
    if r in H:       tags.append('H')
    if r in SA:      tags.append('SA')
    if r in ST:      tags.append('ST')
    if r in SEED:    tags.append('SEED')
    if r in C3:      tags.append('C3')
    if r in C9:      tags.append('C9')
    if r in NEG_H:   tags.append('-H')
    if r in CASCADE: tags.append('CASCADE')
    return tags

def run():
    N = 5000
    print("="*70)
    print("THEOREM 260: RAMANUJAN tau MOD 37 — GF(37) CLASSIFICATION")
    print("="*70)

    print("\nComputing tau(n) mod 37 for n=1..5000...")
    tau = compute_tau_mod(N, P)

    zeros = [n for n in range(1,N+1) if tau[n]==0]
    print(f"tau(n)≡0 (mod 37): {len(zeros)} out of {N} = {len(zeros)/N*100:.2f}%")

    # n≡13 (mod 37) check
    mod13 = [n for n in zeros if n%P==13]
    all13 = [n for n in range(1,N+1) if n%P==13]
    print(f"\nn≡13 (mod 37): {len(mod13)} zeros out of {len(all13)} = CASCADE element")
    assert 13 in CASCADE

    # high/low residue counts
    from collections import Counter
    res_counts = Counter(n%P for n in zeros)
    print(f"\nResidues with 4+ hits: {sorted((r,c) for r,c in res_counts.items() if c>=4)}")
    print(f"Residues with 0 hits:  {[r for r in range(1,P) if res_counts[r]==0]}")

    # primes
    prime_zeros = [n for n in zeros if is_prime(n)]
    print(f"\nPrimes p with tau(p)≡0 (mod 37): {len(prime_zeros)}")
    print(f"Values: {prime_zeros}")
    print(f"\nMod 37 classification of these primes:")
    for p in prime_zeros:
        r = p%P
        tags = classify(r)
        print(f"  p={p:<5} mod37={r:<3} DR={dr(p):<2} {tags}")

    # twin primes
    twins_zero = [p for p in prime_zeros if is_prime(p-2) or is_prime(p+2)]
    print(f"\nTwin primes with tau(p)≡0 (mod 37): {twins_zero}")

    # double-zero twin pairs: both p and p+2 have tau≡0
    zero_set = set(zeros)
    double_pairs = [(p,p+2) for p in prime_zeros if is_prime(p+2) and (p+2) in zero_set]
    print(f"\nTwin pairs where BOTH have tau≡0: {double_pairs}")
    for p,q in double_pairs:
        print(f"  ({p},{q}): {p}≡{p%P} (mod37) {classify(p%P)}, "
              f"{q}≡{q%P} (mod37) {classify(q%P)}")

    # sovereign set hits
    print(f"\nPrimes p with tau(p)≡0 AND p mod37 in sovereign sets:")
    for p in prime_zeros:
        r=p%P; tags=classify(r)
        if tags:
            print(f"  p={p:<5} mod37={r:<3} {tags}")

    print(f"\nAll checks complete.")

if __name__=="__main__":
    run()

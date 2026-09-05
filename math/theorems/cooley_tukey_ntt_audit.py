#!/usr/bin/env python3
"""
cooley_tukey_ntt_audit.py

Cooley-Tukey NTT (Number Theoretic Transform) over F_5, N=4, ω=2.
Verifies the butterfly implementation against the naive O(N²) NTT
from automorphic_orbit_ntt_audit.py.

INPUT:  [1, 2, 3, 4]  (non-zero elements of F_5)
OUTPUT: [0, 4, 3, 2]  (confirmed by both algorithms)

BUTTERFLY TRACE:
  After bit-reverse:  [1, 3, 2, 4]
  Stage 1 (size=2):   α_step = ω^(N/2) = 2^2 = 4 mod 5
    [0,1]: u=1, v=3  → [4, 3]
    [2,3]: u=2, v=4  → [1, 3]
    After: [4, 3, 1, 3]
  Stage 2 (size=4):   α_step = ω^(N/4) = 2^1 = 2 mod 5
    [0,2]: twiddle=1, u=4, v=1  → a[0]=0, a[2]=3
    [1,3]: twiddle=2, u=3, v=1  → a[1]=4, a[3]=2
    After: [0, 4, 3, 2]

─────────────────────────────────────────────────────────────────
COPY-PASTE READY: run with  python3 cooley_tukey_ntt_audit.py
Requires: Python 3.6+, numpy
─────────────────────────────────────────────────────────────────
"""

import numpy as np

FAIL = []

def check(cond, label, actual=None, expected=None):
    if not cond:
        FAIL.append(f"  ✗  {label}  actual={actual!r}  expected={expected!r}")
    return cond

def bit_reverse_permutation(signal):
    n = len(signal)
    bits = int(np.log2(n))
    permutated = np.zeros(n, dtype=int)
    for i in range(n):
        rev_idx = int('{:0{b}b}'.format(i, b=bits)[::-1], 2)
        permutated[rev_idx] = signal[i]
    return permutated

def cooley_tukey_ntt(signal, prime, root_of_unity):
    a = bit_reverse_permutation(signal)
    n = len(a)
    base_alpha = root_of_unity
    stage_size = 2
    while stage_size <= n:
        exponent = n // stage_size
        alpha_step = pow(base_alpha, exponent, prime)
        half_size = stage_size // 2
        for i in range(0, n, stage_size):
            twiddle = 1
            for j in range(half_size):
                u = a[i + j]
                v = (a[i + j + half_size] * twiddle) % prime
                a[i + j] = (u + v) % prime
                a[i + j + half_size] = (u - v + prime) % prime
                twiddle = (twiddle * alpha_step) % prime
        stage_size *= 2
    return a

def naive_ntt(signal, prime, root_of_unity):
    n = len(signal)
    return [sum(signal[j] * pow(root_of_unity, j * k, prime)
                for j in range(n)) % prime
            for k in range(n)]

def run():
    print("COOLEY-TUKEY NTT AUDIT")
    print("=" * 60)

    p, N, alpha = 5, 4, 2
    input_signal = np.array([1, 2, 3, 4])
    expected_out = [0, 4, 3, 2]

    print(f"\n  p={p}, N={N}, ω={alpha}")
    print(f"  input:  {list(input_signal)}")

    # ── BIT-REVERSE PERMUTATION ───────────────────────────────────
    bit_rev = bit_reverse_permutation(input_signal)
    check(list(bit_rev) == [1, 3, 2, 4],
          "bit-reverse([1,2,3,4]) = [1,3,2,4]", list(bit_rev), [1,3,2,4])

    # Verify each index mapping
    mappings = [(0,'00','00',0), (1,'01','10',2), (2,'10','01',1), (3,'11','11',3)]
    for i, fwd, rev_s, rev_i in mappings:
        check(int(rev_s, 2) == rev_i,
              f"bit-rev({i}): '{fwd}'→'{rev_s}'={rev_i}", int(rev_s,2), rev_i)

    print(f"  bit-reverse: {list(bit_rev)}")

    # ── STAGE 1 ──────────────────────────────────────────────────
    alpha_step1 = pow(alpha, N // 2, p)
    check(alpha_step1 == 4, f"Stage 1 α_step = ω^(N/2) = 2^2 = 4 mod 5",
          alpha_step1, 4)

    # [0,1]: u=1, v=3*1=3 mod 5
    check((1 + 3) % p == 4, "Stage 1 [0,1]: (1+3)%5=4")
    check((1 - 3 + p) % p == 3, "Stage 1 [0,1]: (1-3+5)%5=3")
    # [2,3]: u=2, v=4*1=4 mod 5
    check((2 + 4) % p == 1, "Stage 1 [2,3]: (2+4)%5=1")
    check((2 - 4 + p) % p == 3, "Stage 1 [2,3]: (2-4+5)%5=3")
    print(f"  Stage 1 (α_step={alpha_step1}): [4, 3, 1, 3]")

    # ── STAGE 2 ──────────────────────────────────────────────────
    alpha_step2 = pow(alpha, N // 4, p)
    check(alpha_step2 == 2, f"Stage 2 α_step = ω^(N/4) = 2^1 = 2 mod 5",
          alpha_step2, 2)

    # [0,2]: twiddle=1, u=4, v=1*1=1
    check((4 + 1) % p == 0, "Stage 2 [0,2]: (4+1)%5=0")
    check((4 - 1) % p == 3, "Stage 2 [0,2]: (4-1)%5=3")
    # [1,3]: twiddle=2, u=3, v=3*2=6%5=1
    check((3 * 2) % p == 1, "Stage 2 twiddle·v: 3*2=6≡1 mod 5")
    check((3 + 1) % p == 4, "Stage 2 [1,3]: (3+1)%5=4")
    check((3 - 1) % p == 2, "Stage 2 [1,3]: (3-1)%5=2")
    print(f"  Stage 2 (α_step={alpha_step2}): [0, 4, 3, 2]")

    # ── FULL RUN ─────────────────────────────────────────────────
    X_ct  = cooley_tukey_ntt(input_signal.copy(), p, alpha)
    X_naive = naive_ntt(list(input_signal), p, alpha)

    check(list(X_ct) == expected_out,
          f"Cooley-Tukey NTT = {expected_out}", list(X_ct), expected_out)
    check(X_naive == expected_out,
          f"Naive NTT = {expected_out}", X_naive, expected_out)
    check(list(X_ct) == X_naive,
          "Cooley-Tukey == Naive (algorithms agree)")

    print(f"\n  Cooley-Tukey: {list(X_ct)}")
    print(f"  Naive NTT:    {X_naive}")
    print(f"  Match:        {list(X_ct) == X_naive}")

    # ── TWIDDLE FACTOR STRUCTURE ──────────────────────────────────
    print(f"\n  Twiddle factor schedule  (ω={alpha} mod {p}):")
    print(f"  Stage 1: α_step = ω^(N/2) = ω^2 = {pow(alpha,2,p)}")
    print(f"    twiddles: [1]  (half_size=1, only j=0)")
    print(f"  Stage 2: α_step = ω^(N/4) = ω^1 = {pow(alpha,1,p)}")
    tw = 1
    twiddles2 = []
    for _ in range(2):
        twiddles2.append(tw)
        tw = (tw * alpha_step2) % p
    print(f"    twiddles: {twiddles2}  (half_size=2, j=0,1)")
    check(twiddles2 == [1, 2], "Stage 2 twiddle sequence [1,2]", twiddles2, [1,2])

    # ── CORRECTIONS ───────────────────────────────────────────────
    # Condition for NTT of length N: N | (p-1), i.e. 4 | (p-1).
    # p=5 is the SMALLEST such prime but NOT the only one.
    # Any prime p ≡ 1 (mod 4) supports a length-4 NTT.
    import math
    print(f"\n  Condition for NTT length N=4: 4 | (p-1)")
    qualifying = [q for q in range(2, 50)
                  if all(q%i!=0 for i in range(2,q)) and (q-1)%4==0]
    print(f"  Primes p<50 with 4|(p-1): {qualifying}")
    check(qualifying == [5,13,17,29,37,41],
          "qualifying primes < 50", qualifying, [5,13,17,29,37,41])

    # Primitive 4th roots of unity for each qualifying prime
    print(f"  Primitive 4th roots of unity:")
    for q in qualifying:
        roots = [g for g in range(1,q) if pow(g,4,q)==1 and pow(g,2,q)!=1]
        print(f"    p={q:2d}: {roots}")

    # ── INVERSE NTT ───────────────────────────────────────────────
    # x_k = N^(-1) * sum_{j=0}^{N-1} X_j * ω^(-jk)  mod p
    print(f"\n  Inverse NTT:  x_k = N^(-1) * Σ X_j * ω^(-jk) mod p")
    N_inv   = pow(N, -1, p)
    omega_inv = pow(alpha, -1, p)
    check(N_inv == 4,   f"N^(-1)=4^(-1)≡{N_inv} mod 5", N_inv, 4)
    check(omega_inv==3, f"ω^(-1)=2^(-1)≡{omega_inv} mod 5", omega_inv, 3)
    check((N * N_inv) % p == 1, "4·4=16≡1 mod 5")
    check((alpha * omega_inv) % p == 1, "2·3=6≡1 mod 5")

    X_forward = list(X_ct)
    x_rec = []
    for k in range(N):
        total = sum(X_forward[j] * pow(omega_inv, j*k, p) for j in range(N)) % p
        xk = int((N_inv * total) % p)
        x_rec.append(xk)
        print(f"    x_{k} = 4·Σ(X_j·3^(j·{k})) mod 5 = {xk}")
    check(x_rec == [1,2,3,4],
          "inverse NTT reconstructs [1,2,3,4]", x_rec, [1,2,3,4])

    # ── p=37 CONNECTION ───────────────────────────────────────────
    print(f"\n  p=37 (emirp, 37×73=2701):")
    check((37-1) % 4  == 0, "4 | 36: length-4 NTT valid over F_37")
    check((37-1) % 36 == 0, "36 | 36: length-36 NTT valid over F_37 (=φ(37))")
    roots37 = [g for g in range(1,37) if pow(g,4,37)==1 and pow(g,2,37)!=1]
    print(f"  Primitive 4th roots of unity mod 37: {roots37}")
    print(f"  F_37 supports NTT of length 4 (roots {roots37}) "
          f"and length 36 (full unit group)")

    print("\n" + "=" * 60)
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f)
        import sys; sys.exit(1)
    else:
        print("ALL ASSERTIONS PASSED")

if __name__ == "__main__":
    run()

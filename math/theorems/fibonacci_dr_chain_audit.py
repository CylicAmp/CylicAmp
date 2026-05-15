# math/theorems/fibonacci_dr_chain_audit.py
"""
Fibonacci–DR–Cunningham–AP Chain
=================================
Reading the sketch: 1+1=2+3=5  32=10=1+10=11
                    2+3=5 ~ 14–23–3–2

Chain of connections:

  1+1 = 2                       Fibonacci step F(1)+F(2)=F(3)
  2+3 = 5                       Fibonacci step F(3)+F(4)=F(5); digit sum of 23
  532 mod 37 = 14               second member of the DR=5 AP {5,14,23,32}
  532 digit sum = 10; DR = 1    collapse via mod-9
  1+10 = 11                     positional weight sum w₀+w₁ mod 37 = 11
  2→5→11→23                     Cunningham first-kind chain; 11 is the link
  11 → 23                       2×11+1=23; 23 is the third AP member

Second line:
  2+3 = 5  →  first AP member
  14          second AP member (532 ≡ 14 mod 37)
  23          third AP member; also a prime and digit sum of prime 23
  3–2         digits of 32 (fourth AP member)
  sum(3,2)=5  DR(32)=5, closing the loop

DR=5 AP: {5,14,23,32}, step 9, palindromic prime distribution [1,5,5,1]
"""

import math


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def is_prime(n: int) -> bool:
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0: return False
    return True


def verify():
    print("Fibonacci–DR–Cunningham–AP Chain\n")

    # ── 1+1=2 ────────────────────────────────────────────────────────────────
    assert 1 + 1 == 2
    assert dr(1 + 1) == 2
    print("1. 1+1 = 2  (Fibonacci: F1+F2=F3)  ✓")

    # ── 2+3=5 ─────────────────────────────────────────────────────────────────
    assert 2 + 3 == 5
    assert dr(2 + 3) == 5
    # 2 and 3 are the digits of the prime 23
    assert sum(int(c) for c in "23") == 5
    assert is_prime(23)
    print(f"2. 2+3 = 5  (Fibonacci: F3+F4=F5; digit sum of prime 23)  ✓")

    # ── 532 ───────────────────────────────────────────────────────────────────
    # 532 mod 37 = 14  (second member of the DR=5 AP)
    assert 532 % 37 == 14
    assert dr(14) == 5
    # 532 digit sum = 10; DR = 1
    assert sum(int(c) for c in "532") == 10
    assert dr(532) == dr(10) == 1
    print(f"3. 532 mod 37 = {532%37}  (second AP member)  ✓")
    print(f"   532 digit sum = {sum(int(c) for c in '532')},  DR(532) = {dr(532)}  ✓")

    # ── 1+10=11 ───────────────────────────────────────────────────────────────
    # Positional weights mod 37: w₀=1, w₁=10, w₂=26 (period 3)
    w0, w1, w2 = pow(10, 0, 37), pow(10, 1, 37), pow(10, 2, 37)
    assert w0 == 1 and w1 == 10 and w2 == 26
    assert w0 + w1 == 11                 # sum of first two positional weights
    assert (w0 + w1 + w2) % 37 == 0      # full period sums to 37 ≡ 0
    print(f"4. 1+10 = 11  (w₀+w₁ mod 37; period weights sum to 0)  ✓")

    # ── Cunningham chain 2→5→11→23 ────────────────────────────────────────────
    chain = [2, 5, 11, 23]
    for i in range(len(chain) - 1):
        assert 2 * chain[i] + 1 == chain[i + 1]
        assert is_prime(chain[i + 1])
    # DR alternates: 2, 5, 2, 5
    drs = [dr(p) for p in chain]
    assert drs == [2, 5, 2, 5]
    assert 2 * 11 + 1 == 23             # 11 → 23 is the link into the AP
    print(f"5. Cunningham chain: {chain}  DRs={drs}  (alternating 2,5)  ✓")
    print(f"   11 → 23 via 2×11+1=23; 23 is the third AP member  ✓")

    # ── AP {5,14,23,32} ───────────────────────────────────────────────────────
    AP = [5, 14, 23, 32]
    assert all(dr(r) == 5 for r in AP)
    assert AP[1] - AP[0] == AP[2] - AP[1] == AP[3] - AP[2] == 9
    # 32 = 3×10+2; digits 3 and 2; sum = 5 = DR(32) closes the loop
    assert 3 + 2 == 5
    assert dr(32) == 5
    assert int("3") * 10 + int("2") == 32
    print(f"6. AP {AP}  step=9  all DR=5  ✓")
    print(f"   32 digits: 3,2  →  3+2=5=DR(32)  (loop closes)  ✓")

    # ── Full chain summary ────────────────────────────────────────────────────
    print()
    print("  Chain: 1+1=2  →  2+3=5  →  532≡14(mod37)")
    print("         DR(532)=1  →  1+10=11  →  11→23 (Cunningham)")
    print("         23 = AP member 3  ←→  5,14,23,32 (DR=5, step 9)")
    print("         32 digits 3,2: sum=5=DR(32)  ← closes loop")
    print()

    # ── Fibonacci context ────────────────────────────────────────────────────
    fib = [1, 1]
    while fib[-1] < 200:
        fib.append(fib[-1] + fib[-2])
    # F5=5, F10=55, F11=89, F12=144...
    assert fib[:7] == [1, 1, 2, 3, 5, 8, 13]
    fib_drs = [dr(f) for f in fib[:12]]
    print(f"  Fibonacci DRs (first 12): {fib_drs}")
    # DR of Fibonacci numbers is periodic with period 24
    # DR=5 appears at positions where Fib ≡ 5 mod 9
    fib_dr5 = [(i + 1, fib[i]) for i in range(12) if dr(fib[i]) == 5]
    print(f"  Fib terms with DR=5: {fib_dr5}")
    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()

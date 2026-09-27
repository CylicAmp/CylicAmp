# math/theorems/arithmetic_sequence_1111.py
"""
Arithmetic Sequence with Common Difference −1111

Terms: 9859, 8748, 7637, 6526, 5415, 4304, 3193, ...
Common difference: −1111 = −(11 × 101)
General term: a_n = 9859 − 1111(n−1)

DR pattern: each term's digital root increases by 5 (mod 9)
Because −1111 ≡ −4 ≡ +5 (mod 9)
"""

import math

SEQ_START = 9859
DIFF = -1111
TERMS = [SEQ_START + DIFF * i for i in range(7)]

def dr(n): return 1 + (n-1)%9 if n>0 else 9

# ── Factorization ──────────────────────────────────────────────────────────────

def factorize(n):
    factors = {}
    d, m = 2, abs(n)
    while d*d <= m:
        while m % d == 0:
            factors[d] = factors.get(d,0) + 1
            m //= d
        d += 1
    if m > 1: factors[m] = factors.get(m,0) + 1
    return factors

assert factorize(1111) == {11:1, 101:1}
assert factorize(8748)  == {2:2, 3:7}    # 2² × 3⁷
assert 4 * 3**7 == 8748

# ── Sequence verification ──────────────────────────────────────────────────────

assert TERMS == [9859,8748,7637,6526,5415,4304,3193]
assert all(TERMS[i]-TERMS[i+1] == 1111 for i in range(len(TERMS)-1))

# ── DR pattern: +5 mod 9 each step ────────────────────────────────────────────

DRS = [dr(t) for t in TERMS]
assert all((DRS[i+1] - DRS[i]) % 9 == 5 for i in range(len(DRS)-1))
# −1111 mod 9: 1+1+1+1=4, so −4 ≡ 5 (mod 9)
assert 1111 % 9 == 4
assert (-1111) % 9 == 5


if __name__ == "__main__":
    print("Arithmetic Sequence: common difference −1111 = −(11×101)")
    print()
    for i, (t, d) in enumerate(zip(TERMS, DRS), 1):
        print(f"  a_{i} = {t:5d}   DR={d}")
    print()
    print(f"  −1111 mod 9 = {(-1111)%9}  →  DR increases by 5 each step")
    print(f"  8748 = 2² × 3⁷ = {4 * 3**7}")
    print()
    print("All assertions passed.")

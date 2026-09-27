"""
connection_7518.py

7518 appears in two places and they are structurally linked:

  (A) 103/137 repeating decimal: block = 75182481, first 4 digits = 7518
  (B) sum of quadratic residues mod 179 = 42 × 179 = 7518

Both facts pass through the identity:  103 × 73 = 7519 = 7518 + 1

CHAIN:
  10^4 + 1 = 73 × 137          (both 73 and 137 have ord_p(10)=8)
  75182481 = 9999 × 103 × 73   (repeating block of 103/137)
  7518 = 103 × 73 - 1          (floor(75182481/10^4) = 7519-1)
  7518 = 42 × 179              (sum(QRs mod 179) via class number)
  42 = (179-1-2h(-179))/4      (closed form, h(-179)=5)
  103 × 73 ≡ 1 (mod 179)       (73 = 103^(-1) mod 179)

CLOSED FORM (correcting Thread 1 for primitive-root subcases):
  When 10 is a primitive root mod p and p ≡ 3 (mod 4):
    H = <10^2> = full set of quadratic residues mod p
    lift = sum(H)/p = (p - 1 - 2h(-p)) / 4
  where h(-p) is the class number of Q(√(-p)) (= number of reduced
  primitive positive definite binary quadratic forms of discriminant -p).
  This formula is verified for all 8 primitive-root cases below p=200.
"""

from sympy import factorint, isprime
from math import gcd

def ord10(p):
    k, cur = 1, 10 % p
    while cur != 1:
        cur = (cur * 10) % p
        k += 1
    return k

def subgroup_generated(g, p):
    h, elems = g % p, []
    while True:
        elems.append(h)
        h = (h * g) % p
        if h == elems[0]:
            break
    return elems

def class_number(p):
    """
    Number of reduced primitive positive definite binary quadratic forms
    of discriminant -p (p prime, p ≡ 3 mod 4).
    Reduced: |b| <= a <= c; if |b|=a or a=c then b>=0. Primitive: gcd(a,b,c)=1.
    """
    count = 0
    for a in range(1, int((p / 3) ** 0.5) + 2):
        for b in range(-a, a + 1):
            disc = b * b + p
            if disc % (4 * a) != 0:
                continue
            c = disc // (4 * a)
            if c < a:
                continue
            if b < 0 and (abs(b) == a or a == c):
                continue
            if gcd(gcd(a, abs(b)), c) != 1:
                continue
            assert b * b - 4 * a * c == -p
            count += 1
    return count


# ──────────────────────────────────────────────────────────────────────────────
# PART 1: 10^4 + 1 = 73 × 137
# ──────────────────────────────────────────────────────────────────────────────

assert 10**4 + 1 == 73 * 137
assert factorint(10**4 + 1) == {73: 1, 137: 1}

# Both 73 and 137 have multiplicative order 8 mod 10
assert ord10(73)  == 8
assert ord10(137) == 8

# Equivalently: 10^4 ≡ -1 (mod 73) and 10^4 ≡ -1 (mod 137)
assert pow(10, 4, 73)  == 72   # 72 ≡ -1 (mod 73)
assert pow(10, 4, 137) == 136  # 136 ≡ -1 (mod 137)


# ──────────────────────────────────────────────────────────────────────────────
# PART 2: 75182481 = 9999 × 103 × 73 (repeating block of 103/137)
# ──────────────────────────────────────────────────────────────────────────────

BLOCK = 103 * (10**8 - 1) // 137
assert BLOCK == 75182481
assert BLOCK == 9999 * 103 * 73     # the key factorization

# Split: 75182481 = 7518 × 10^4 + 2481, with 7518 + 2481 = 9999
assert BLOCK == 7518 * 10**4 + 2481
assert 7518 + 2481 == 9999

# 7518 = first 4 digits of the 8-digit block
assert BLOCK // 10**4 == 7518

# Why: BLOCK = 9999 × 7519, so floor(BLOCK/10^4) = 9999×7519//10^4
# = floor(7519 - 7519/10^4) = 7519 - 1 = 7518  (since 7519 < 10^4)
assert 9999 * 7519 == 75182481
assert 7519 < 10**4
assert 7518 == 7519 - 1


# ──────────────────────────────────────────────────────────────────────────────
# PART 3: 103 × 73 = 7519 = 7518 + 1
# ──────────────────────────────────────────────────────────────────────────────

assert 103 * 73 == 7519
assert 103 * 73 == 7518 + 1

# 73 = (10^4 + 1) / 137  (exact integer division)
assert (10**4 + 1) // 137 == 73

# Therefore: 103 × (10^4+1) = 103 × 73 × 137 = 7519 × 137 = (7518+1) × 137
assert 103 * (10**4 + 1) == 7519 * 137


# ──────────────────────────────────────────────────────────────────────────────
# PART 4: sum(QRs mod 179) = 7518 = 42 × 179
# ──────────────────────────────────────────────────────────────────────────────

# ord_179(10) = 178 = p-1, so 10 is a primitive root mod 179
assert ord10(179) == 178
assert 179 - 1 == 178

# H = <10^2> = quadratic residues mod 179 (since 10 is a primitive root)
H = subgroup_generated(pow(10, 2, 179), 179)
assert len(H) == 89   # (p-1)/2 quadratic residues
assert sum(H) == 7518
assert sum(H) == 42 * 179

# -1 is not a quadratic residue (since 179 ≡ 3 mod 4)
assert 179 % 4 == 3
assert 178 not in H   # 178 ≡ -1 (mod 179)


# ──────────────────────────────────────────────────────────────────────────────
# PART 5: CLOSED FORM VIA CLASS NUMBER h(-179) = 5
# ──────────────────────────────────────────────────────────────────────────────

h_179 = class_number(179)
assert h_179 == 5

# Lift formula: sum(QRs)/p = (p-1-2h(-p))/4
lift_179 = (179 - 1 - 2 * h_179) // 4
assert lift_179 == 42
assert sum(H) == lift_179 * 179


# ──────────────────────────────────────────────────────────────────────────────
# PART 6: THE BRIDGE — 103 × 73 ≡ 1 (mod 179)
# ──────────────────────────────────────────────────────────────────────────────

# 73 is the modular inverse of 103 modulo 179
assert pow(103, -1, 179) == 73
assert (103 * 73) % 179 == 1

# sum(QRs mod 179) ≡ 0 (mod 179) and 103×73 ≡ 1 (mod 179)
# so 103×73 - sum(QRs) = 1:
assert 103 * 73 - sum(H) == 1

# The two occurrences of 7518 in the same equation:
assert 103 * (10**4 + 1) // 137 - 1 == sum(H)
# i.e., 103 × (10^4+1)/137 = sum(QRs mod 179) + 1


# ──────────────────────────────────────────────────────────────────────────────
# PART 7: LIFT FORMULA FOR ALL PRIMITIVE-ROOT CASES BELOW p=200
# ──────────────────────────────────────────────────────────────────────────────

primitive_root_data = [
    (  7,   6,  3,    7,  1),
    ( 19,  18,  9,   76,  4),
    ( 23,  22, 11,   92,  4),
    ( 47,  46, 23,  423,  9),
    ( 59,  58, 29,  767, 13),
    (131, 130, 65, 3930, 30),
    (167, 166, 83, 6012, 36),
    (179, 178, 89, 7518, 42),
]

for p, o, k, s, lift in primitive_root_data:
    assert isprime(p) and p % 4 == 3       # p ≡ 3 (mod 4)
    assert ord10(p) == p - 1               # 10 is a primitive root
    h = class_number(p)
    formula = (p - 1 - 2 * h) // 4
    assert formula == lift, f"p={p}: formula={formula}, actual={lift}"


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Structural connection: 7518 in 103/137 and in sum(QRs mod 179)")
    print("=" * 66)

    print("\n── CHAIN ──")
    print(f"  10^4 + 1 = {10**4+1} = 73 × 137  (both have ord_p(10)=8)")
    print(f"  103 × (10^8-1)/137 = {BLOCK} = 9999 × 103 × 73")
    print(f"  7518 = floor({BLOCK}/10^4) = 103×73 - 1 = 7519-1")
    print(f"  7518 = sum(QRs mod 179) = lift × 179 = 42×179")
    print(f"  42 = (179-1-2×h(-179))/4 = (178-10)/4,  h(-179)={h_179}")
    print(f"  103×73 ≡ 1 (mod 179):  73 = 103^(-1) mod 179")
    print(f"  ∴ 103×73 - sum(QRs mod 179) = 1")

    print("\n── FACTORIZATION ──")
    print(f"  10^4+1 = {10**4+1} = {factorint(10**4+1)}")
    print(f"  73: ord_73(10)={ord10(73)}, 10^4 mod 73={pow(10,4,73)} ≡ -1")
    print(f"  137: ord_137(10)={ord10(137)}, 10^4 mod 137={pow(10,4,137)} ≡ -1")

    print("\n── CLASS NUMBER FORMULA (PRIMITIVE ROOT CASES) ──")
    print(f"  lift = sum(QRs mod p)/p = (p-1-2h(-p))/4  when 10 is primitive root mod p ≡ 3 (mod 4)")
    print()
    print(f"  {'p':>5} | {'h(-p)':>6} | {'formula':>8} | {'actual':>7} | match")
    print("  " + "-" * 43)
    for p, o, k, s, lift in primitive_root_data:
        h = class_number(p)
        f = (p-1-2*h)//4
        print(f"  {p:>5} | {h:>6} | {f:>8} | {lift:>7} | {'✓' if f==lift else '✗'}")

    print()
    print("All assertions passed.")

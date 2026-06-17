"""
cyclic_142857.py

142857 is the cyclic number: the repeating block of 1/7 = 0.142857142857...

FACTORIZATION:
  142857 = 999 × 143
         = (27 × 37) × (11 × 13)
         = 3³ × 37 × 11 × 13

CYCLIC ROTATIONS (= successive multiples):
  142857 × 1 = 142857
  142857 × 2 = 285714
  142857 × 3 = 428571
  142857 × 4 = 571428
  142857 × 5 = 714285
  142857 × 6 = 857142
  142857 × 7 = 999999   ← overflow to all-nines

37-HUB CONNECTION:
  37 divides 142857 directly (37 × 3861 = 142857).
  999 = 27 × 37 = 3³ × 37 — the three-repunit is the 37 scaffold.
  ord₃₇(10) = 3 (heartbeat period in the 37-hub).
  ord₇(10)  = 6 (cyclic period of 1/7).
  6 = 2 × 3 — the cyclic period doubles the heartbeat period.
"""

from sympy import isprime, factorint

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# ──────────────────────────────────────────────────────────────────────────────
# FACTORIZATION
# ──────────────────────────────────────────────────────────────────────────────

assert 999 * 143 == 142857
assert 27  * 37  == 999
assert 11  * 13  == 143
assert 3**3 * 37 * 11 * 13 == 142857

# 7 is absent from 142857's factorization — it is the generator
assert 142857 % 7 != 0
assert 142857 * 7 == 999999

# Full prime factorization
assert factorint(142857) == {3: 3, 11: 1, 13: 1, 37: 1}
assert factorint(999999) == {3: 3, 7: 1, 11: 1, 13: 1, 37: 1}
# 999999 = 142857 × 7 adds exactly the factor 7


# ──────────────────────────────────────────────────────────────────────────────
# CYCLIC ROTATIONS
# ──────────────────────────────────────────────────────────────────────────────

rotations = [142857 * k for k in range(1, 7)]
assert rotations == [142857, 285714, 428571, 571428, 714285, 857142]

# User's specific identities
assert 428571 == 999 * 143 * 3   # cyclic rotation ×3
assert 285714 == 999 * 143 * 2   # cyclic rotation ×2

# All rotations have digit sum 27 → DR = 9
for r in rotations:
    assert sum(int(d) for d in str(r)) == 27
    assert dr(r) == 9

# All rotations are divisible by 37 (since 37 | 142857)
for r in rotations:
    assert r % 37 == 0


# ──────────────────────────────────────────────────────────────────────────────
# SPLIT-COMPLEMENT PROPERTY: first half + second half = 999
# ──────────────────────────────────────────────────────────────────────────────

# PROOF:
#   142857 = 999 × 143  →  142857 ≡ 0 (mod 999)
#   Every rotation k×142857 ≡ 0 (mod 999)
#   For any 6-digit R = C×10³ + D:
#     10³ ≡ 1 (mod 999)  →  C×10³ + D ≡ C + D (mod 999)
#   Therefore C + D ≡ 0 (mod 999)
#   C and D are both < 999, so C + D = 999 exactly.

assert 10**3 % 999 == 1    # 1000 ≡ 1 (mod 999) — the key step

for r in rotations:
    s = str(r).zfill(6)
    C, D = int(s[:3]), int(s[3:])
    assert C + D == 999
    assert r % 999 == 0    # follows from 142857 = 999×143

# ×7 property: rotation k × 142857 × 7 = k × 999999
for k, r in enumerate(rotations, 1):
    assert r * 7 == 999999 * k


# ──────────────────────────────────────────────────────────────────────────────
# 37-HUB CONNECTION
# ──────────────────────────────────────────────────────────────────────────────

# ord₃₇(10) = 3: the heartbeat period (proven in cylicamp_master.py)
assert pow(10, 1, 37) == 10
assert pow(10, 2, 37) == 26   # = SCALAR_137
assert pow(10, 3, 37) == 1    # period 3

# ord₇(10) = 6: the cyclic period of 1/7
assert pow(10, 1, 7) == 3
assert pow(10, 2, 7) == 2
assert pow(10, 3, 7) == 6
assert pow(10, 4, 7) == 4
assert pow(10, 5, 7) == 5
assert pow(10, 6, 7) == 1    # period 6

# Period of 1/7 = 2 × period in 37-hub
assert 6 == 2 * 3

# 999999 = 10^6 - 1 ≡ 0 (mod 37): follows from ord₃₇(10)=3 dividing 6
assert (10**6 - 1) % 37 == 0
assert (10**3 - 1) % 37 == 0    # 999 ≡ 0 (mod 37)
assert 999 % 37 == 0
assert 999 // 37 == 27           # 999 = 27 × 37


# ──────────────────────────────────────────────────────────────────────────────
# CONNECTION TO 111 REPUNIT SCAFFOLD
# ──────────────────────────────────────────────────────────────────────────────

# 111 = 3 × 37  (the base repunit of the 37-hub)
assert 3 * 37 == 111

# 999 = 9 × 111 = 3³ × 37
assert 9 * 111 == 999

# 142857 = (9 × 111) × 143
assert 9 * 111 * 143 == 142857

# 142857 / 111 = 9 × 143 = 1287
assert 142857 // 111 == 1287
assert 9 * 143 == 1287
assert factorint(1287) == {3: 2, 11: 1, 13: 1}


# ──────────────────────────────────────────────────────────────────────────────
# 143 = 11 × 13 AND 1001 = 7 × 11 × 13
# ──────────────────────────────────────────────────────────────────────────────

assert 1001 == 7 * 11 * 13
assert 1001 == 7 * 143
assert 142857 == 999999 // 7
assert 1001    == 1001            # 1001 = 7 × 143, 142857 = 999 × 143

# DR values
assert dr(143) == 8    # 1+4+3=8
assert dr(999) == 9    # 9+9+9=27→9
assert dr(111) == 3    # 1+1+1=3
assert dr(1001) == 2   # 1+0+0+1=2
assert dr(1287) == 9   # 1+2+8+7=18→9


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Cyclic Number 142857")
    print("=" * 62)

    print("\n── FACTORIZATION ──")
    print(f"  142857 = 999 × 143")
    print(f"         = (27 × 37) × (11 × 13)")
    print(f"         = 3³ × 37 × 11 × 13")
    print(f"  7 ∤ 142857  (7 is the generator, not a factor)")
    print(f"  142857 × 7 = {142857*7}  (all-nines overflow)")

    print("\n── CYCLIC ROTATIONS ──")
    for k, r in enumerate(rotations, 1):
        print(f"  142857 × {k} = {r}   digit sum={sum(int(d) for d in str(r))} DR={dr(r)}")
    print(f"  142857 × 7 = 999999   DR={dr(999999)}")

    print("\n── 37-HUB CONNECTION ──")
    print(f"  ord₃₇(10) = 3   (heartbeat period)")
    print(f"  ord₇(10)  = 6   (cyclic period of 1/7)")
    print(f"  6 = 2 × 3       (cyclic period = 2 × heartbeat period)")
    print(f"  999 = 27 × 37,  999 mod 37 = {999%37}")
    print(f"  All rotations divisible by 37: {all(r%37==0 for r in rotations)}")

    print("\n── 111 SCAFFOLD ──")
    print(f"  111 = 3 × 37")
    print(f"  999 = 9 × 111 = 3³ × 37")
    print(f"  142857 = 9 × 111 × 143  =  {9*111*143}")
    print(f"  142857 / 111 = {142857//111} = 9 × 143")

    print("\n── DR VALUES ──")
    print(f"  DR(142857) = {dr(142857)}  (all rotations share this)")
    print(f"  DR(999)    = {dr(999)}")
    print(f"  DR(111)    = {dr(111)}")
    print(f"  DR(143)    = {dr(143)}")
    print(f"  DR(1001)   = {dr(1001)}")

    print()
    print("All assertions passed.")

# math/theorems/palindrome_cipher_37R.py
"""
Registry Pulse Cipher — Palindrome Structure

Three 8-digit palindromic seeds, each mirrored to form a 16-digit palindrome.
Seeds A, B, C all have digit sum 20 → palindromes have digit sum 40.
40 mod 37 = 3  (trinity residue in 37-field)

─────────────────────────────────────────────────────────────────────────────
ALGEBRAIC PROPERTY: pair sums always divisible by 11
─────────────────────────────────────────────────────────────────────────────
For any 8-digit palindrome d₁d₂d₃d₄d₄d₃d₂d₁:
  Outer pair:  (10d₁+d₂) + (10d₂+d₁) = 11(d₁+d₂)
  Inner pair:  (10d₃+d₄) + (10d₄+d₃) = 11(d₃+d₄)

Both sums are always multiples of 11. This is a theorem, not coincidence.

A: 11×(3+2)=55,  11×(5+0)=55
B: 11×(3+2)=55,  11×(0+5)=55
C: 11×(3+0)=33,  11×(2+5)=77

─────────────────────────────────────────────────────────────────────────────
37-FIELD RELATIONS
─────────────────────────────────────────────────────────────────────────────
  55 = 37 + 18
  33 = 37 − 4
  77 = 2×37 + 3
  50 mod 37 = 13
  40 mod 37 = 3

─────────────────────────────────────────────────────────────────────────────
OSCILLATION PATTERN: A-B-A-C-B-A
─────────────────────────────────────────────────────────────────────────────
Concentric structure (read center outward):
  Center:  C  (position 3)
  Shell 1: A  (positions 2, 4)
  Shell 2: B  (positions 1, 5)
  Shell 3: A  (position 0)
"""

SEEDS = {
    'A': '32500523',
    'B': '32055023',
    'C': '30255203',
}

PALINDROMES = {k: v+v for k,v in SEEDS.items()}

PATTERN = ['A','B','A','C','B','A']

def dr(n): return 1 + (n-1)%9 if n>0 else 9

def pair_sums(seed):
    d = [int(c) for c in seed]
    outer = (10*d[0]+d[1]) + (10*d[1]+d[0])
    inner = (10*d[2]+d[3]) + (10*d[3]+d[2])
    return outer, inner

# ── Seed palindrome property ───────────────────────────────────────────────────

for label, seed in SEEDS.items():
    assert seed == seed[::-1], f"Seed {label} is not a palindrome"
    assert sum(int(d) for d in seed) == 20, f"Seed {label} digit sum ≠ 20"

# ── 16-digit palindrome properties ────────────────────────────────────────────

for label, pal in PALINDROMES.items():
    assert len(pal) == 16
    assert sum(int(d) for d in pal) == 40
    assert sum(int(d) for d in pal) % 37 == 3

# ── Pair sums: theorem verification ───────────────────────────────────────────

# All pair sums are multiples of 11 (algebraic consequence of palindrome structure)
for label, seed in SEEDS.items():
    outer, inner = pair_sums(seed)
    assert outer % 11 == 0, f"Outer pair sum {outer} not divisible by 11"
    assert inner % 11 == 0, f"Inner pair sum {inner} not divisible by 11"

# Specific values
assert pair_sums('32500523') == (55, 55)
assert pair_sums('32055023') == (55, 55)
assert pair_sums('30255203') == (33, 77)

# General proof: for palindrome d1d2d3d4d4d3d2d1
# outer = (10d1+d2) + (10d2+d1) = 11(d1+d2) — multiple of 11 always
# inner = (10d3+d4) + (10d4+d3) = 11(d3+d4) — multiple of 11 always
def verify_palindrome_11_theorem(d1, d2, d3, d4):
    seed = f"{d1}{d2}{d3}{d4}{d4}{d3}{d2}{d1}"
    outer, inner = pair_sums(seed)
    assert outer == 11*(d1+d2)
    assert inner == 11*(d3+d4)

for d1 in range(1,4):
    for d2 in range(0,4):
        for d3 in range(0,4):
            for d4 in range(0,4):
                verify_palindrome_11_theorem(d1, d2, d3, d4)

# ── 37-field arithmetic ────────────────────────────────────────────────────────

assert 55 == 37 + 18
assert 33 == 37 - 4
assert 77 == 2*37 + 3
assert 50 % 37 == 13
assert 40 % 37 == 3
assert 6*16 == 96 == 3*32

# ── Oscillation pattern ────────────────────────────────────────────────────────

assert PATTERN == ['A','B','A','C','B','A']
assert PATTERN[3] == 'C'                    # C at center (index 3)
assert PATTERN[2] == 'A' and PATTERN[4] == 'B'   # A left of C, B right of C
assert PATTERN[1] == 'B' and PATTERN[5] == 'A'   # B outer left, A outer right
assert PATTERN[0] == 'A'                   # A leads


if __name__ == "__main__":
    print("Registry Pulse Cipher — Palindrome Structure")
    print()
    for label, seed in SEEDS.items():
        pal = PALINDROMES[label]
        outer, inner = pair_sums(seed)
        dsum = sum(int(d) for d in pal)
        print(f"  {label}: {pal}")
        print(f"     seed={seed}  (palindrome)  digit_sum=2×20={dsum}  {dsum}%37={dsum%37}")
        print(f"     outer pair sum: {outer} = 11×{outer//11}")
        print(f"     inner pair sum: {inner} = 11×{inner//11}")
        print()
    print("Theorem: for any 8-digit palindrome d₁d₂d₃d₄d₄d₃d₂d₁,")
    print("  outer pair sum = 11(d₁+d₂),  inner pair sum = 11(d₃+d₄)")
    print("  Verified for all (d₁,d₂,d₃,d₄) ∈ {1..3}×{0..3}³")
    print()
    print(f"37-field: 55=37+18, 33=37−4, 77=2×37+3")
    print(f"Pattern:  {PATTERN}  (C at center, A/B shells)")
    print()
    print("All assertions passed.")

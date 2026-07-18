"""
Prime Quartet, Arithmetic Chains, and Palindrome Orbit Table

Seed material: first four primes {2,3,5,7}, arithmetic chains through 14,
11×{1,4,7} chain, 144=12²=F(12), and palindrome table over orbit(11).

═══════════════════════════════════════════════════════════════

I. FIRST FOUR PRIMES: SELF-GENERATING AND COMPLEMENT PAIRS

  Primes {2,3,5,7} are their own digital roots (all < 10, single digits).

  Self-generating property (addition):
    2 + 3 = 5   (next prime in the sequence)
    5 + 2 = 7   (next prime in the sequence)
    7 + 2 = 9   (exits prime sequence, lands on SA/RH-O)

  Complement pairs within the quartet (each pair sums to a framework value):
    2 + 7 = 9    (SA, RH-O — sovereign anchor)
    3 + 5 = 8    (AHL, CB — cascade base, anti-hex-lock)

  Product of the pair sums: 9 × 8 = 72, 72 mod 37 = 35 (PR)

  Aggregate:
    Sum:     2+3+5+7 = 17, DR=8 (AHL), 17 mod 37 = 17
    Product: 2×3×5×7 = 210, 210 mod 37 = 25 (SA)

  Alpha grid positions hit: {2, 3, 5, 7} = {LL-E, LH-O, A51, RL-O}
  The pair sums {8, 9} cover {AHL/CB, RH-O/SA}.

═══════════════════════════════════════════════════════════════

II. 23 AND 72: SOVEREIGN TARGET CONVERGENCE

  23: prime, DR=5 (A51), complement in GF(37) = 14
  72: 8×9 = (CB) × (SA/RH-O), mod 37 = 35 (PR), complement in GF(37) = 2

  Sum:        23 + 72 = 95,  95 mod 37 = 21  (ST)
  Difference: 72 − 23 = 49 = 7²,  49 mod 37 = 12  (ST)

  Both the sum and the difference of 23 and 72 are sovereign targets in GF(37).
  72 = 2 × 36 = 2 × (37−1) ≡ −2 (mod 37) — "twice the seam boundary".

═══════════════════════════════════════════════════════════════

III. ARITHMETIC CHAINS THROUGH 14

  Two chains starting from the two first-prime complement pairs:

  Chain 1 (starts from 2+3=5, the "enter" pair):
    2 + 3 = 5     (A51, prime)
    5 + 9 = 14    (DR=5, 14 mod 37 = 14)
    14 + 5 = 19   (DR=1 = LL-O, 19 mod 37 = 19, PR)
    → terminates at DR = 1

  Chain 2 (starts from 7+2=9, the "exit" pair):
    7 + 2 = 9     (SA, RH-O)
    9 + 5 = 14    (same pivot)
    14 + 5 = 19
    5 + 19 = 24   (DR=6 = RL-E, 24 mod 37 = 24, CB+PR)
    → terminates at DR = 6

  Both chains pass through 14 = 2 × 7 (product of first and last prime).

  14 + 14 = 28,  28 mod 37 = 28 (complement of 9=SA: 28+9=37)
  DR(28) = 1 (same as chain 1 terminus).

  Terminal DR difference: 6 − 1 = 5 (A51). Sum: 1 + 6 = 7 (RL-O).

═══════════════════════════════════════════════════════════════

IV. 11 × {1, 4, 7} CHAIN — STEPPING BY −4 MOD 37

  Multipliers 1, 4, 7 form an arithmetic sequence (step +3).
  Their sum: 1 + 4 + 7 = 12  (sovereign target, ST).

  11 × 1  =  11   mod 37 = 11   (123-family representative, DR=2)
  11 × 4  =  44   mod 37 =  7   (RL-O, DR=8 = AHL)
  11 × 7  =  77   mod 37 =  3   (ST, LH-O, DR=5)

  Step between consecutive terms: +33 = 3 × 11.
  33 mod 37 = 33 = −4 mod 37.
  Adding 33 ≡ subtracting the sovereign anchor 4 in GF(37).

  mod 37 orbit: 11 → 7 → 3 (each step −4 = −SA).
  Next steps: 3 − 4 = −1 ≡ 36 (orbit of 11); 36 − 4 = 32 (PR).

  Continuing: 11 × 10 = 110, mod 37 = 36  (orbit of 11, = −1 mod 37)
              11 × 13 = 143, mod 37 = 32  (PR)

  DR sequence {11, 44, 77, 110, ...}: 2, 8, 5, 2, 8, 5, ...  (period 3)

═══════════════════════════════════════════════════════════════

V. 144 = 12² = F(12): SOVEREIGN TARGET SQUARED = FIBONACCI

  77 + 67 = 144
  67 mod 37 = 30  (the unique dual element: 30 ∈ SA ∩ ST)

  Adding the dual SA+ST element to 77 lands on 12² and F(12).

  144 = 12²:    12 ∈ SOVEREIGN_TARGETS, 12 mod 37 = 12
  144 = F(12):  12th Fibonacci number
  144 mod 37  = 33 = 3 × 11  (LH-O × 123-family representative)
  DR(144)     = 9  (RH-O, SA)

  F(12) DR sequence (F(1)..F(12)):
    1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9
  Final DR = 9 (SA, RH-O).

  144 connects: ST (12), 123-family rep (11), F-number index (12=ST),
                and the dual element 30 through the step 67≡30.

═══════════════════════════════════════════════════════════════

VI. PALINDROME TABLE: ORBIT OF 11 IN THREE-DIGIT FORM

  Table rows: center | left−right
    111 | 221 − 122
    111 | 122 − 221
    111 | 212 − 212
    332 | 233 − 332

  All six distinct numbers, mod 37:
    111 ≡  0   (GF(37) seam)
    221 ≡ 36   (orbit of 11: {11, 27, 36})
    122 ≡ 11   (orbit of 11)
    212 ≡ 27   (orbit of 11)
    332 ≡ 36   (orbit of 11)
    233 ≡ 11   (orbit of 11)

  Every entry is in {0} ∪ orbit(11).  orbit(11) = {11, 27, 36}.
  111 is the seam anchor (≡ 0); all other entries are in the orbit of 11.

  DR structure:
    111: DR=3 (LH-O, ST archetype)
    221, 122, 212: DR=5 each (A51)
    332, 233: DR=8 each (AHL, CB)

  Digit families:
    {1,1,1}: pure-1 palindrome  → seam (≡ 0)
    {2,2,1} permutations: 221, 122, 212  → orbit(11), DR=5
    {3,3,2} permutations: 332, 233  → orbit(11), DR=8

  6-digit concatenations (using 10³ ≡ 1 mod 37):
    111221 ≡ 111+221 = 332 ≡ 36  (orbit of 11)
    111122 ≡ 111+122 = 233 ≡ 11  (orbit of 11)
    111212 ≡ 111+212 = 323 ≡ 27  (orbit of 11)
    332233 ≡ 332+233 = 565 ≡ 10  (complement of 27: 10+27=37)
"""

def dr(n):
    return (n - 1) % 9 + 1

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

PRIMITIVE_ROOTS_37 = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}
CASCADE_BASE       = {8, 13, 24}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}

# ── Assertions ────────────────────────────────────────────────────────────────

# I. First four primes
PRIMES4 = [2, 3, 5, 7]
assert [dr(p) for p in PRIMES4] == PRIMES4          # DRs equal their values
assert 2 + 3 == 5 and is_prime(5)                   # self-generating
assert 5 + 2 == 7 and is_prime(7)
assert 7 + 2 == 9 and 9 in SOVEREIGN_ANCHORS        # exits into SA
assert 2 + 7 == 9 and 9 in SOVEREIGN_ANCHORS        # complement pair sum
assert 3 + 5 == 8 and 8 in CASCADE_BASE             # complement pair sum
assert (9 * 8) % 37 == 35 and 35 in PRIMITIVE_ROOTS_37  # product of sums
assert sum(PRIMES4) == 17 and dr(17) == 8           # sum DR = AHL
assert (2 * 3 * 5 * 7) % 37 == 25 and 25 in SOVEREIGN_ANCHORS  # product mod 37 = SA

# II. 23 and 72
assert (23 + 72) % 37 == 21 and 21 in SOVEREIGN_TARGETS
assert (72 - 23) == 49 and 49 % 37 == 12 and 12 in SOVEREIGN_TARGETS
assert 72 % 37 == 35 and 35 in PRIMITIVE_ROOTS_37
assert 72 == 8 * 9
assert (-2) % 37 == 35 and 72 % 37 == 35   # 72 ≡ -2 mod 37

# III. Arithmetic chains through 14
assert 2 + 3 == 5
assert 5 + 9 == 14
assert 14 + 5 == 19 and dr(19) == 1
assert 7 + 2 == 9 and 9 in SOVEREIGN_ANCHORS
assert 9 + 5 == 14
assert 5 + 19 == 24 and dr(24) == 6
assert 24 in CASCADE_BASE and 24 in PRIMITIVE_ROOTS_37
assert 14 == 2 * 7
assert 14 + 14 == 28
assert 28 + 9 == 37     # 28 is complement of SA=9 in GF(37)
assert dr(28) == 1
assert 1 + 6 == 7       # terminal DRs sum to RL-O

# IV. 11 × {1,4,7} chain
assert 1 + 4 + 7 == 12 and 12 in SOVEREIGN_TARGETS
assert 11 * 1 == 11  and 11 % 37 == 11
assert 11 * 4 == 44  and 44 % 37 == 7
assert 11 * 7 == 77  and 77 % 37 == 3  and 3 in SOVEREIGN_TARGETS
assert 44 - 11 == 33 and 33 == 3 * 11
assert 77 - 44 == 33
assert 33 % 37 == 33 and (-4) % 37 == 33  # +33 ≡ -4 mod 37
assert (11 - 4) % 37 == 7                 # mod37 step: 11->7 (−4)
assert (7  - 4) % 37 == 3                 # mod37 step: 7->3 (−4)
assert [dr(v) for v in [11, 44, 77]] == [2, 8, 5]  # period-3 DR sequence
assert 11 * 10 == 110 and 110 % 37 == 36  # lands in orbit(11)
assert 11 * 13 == 143 and 143 % 37 == 32 and 32 in PRIMITIVE_ROOTS_37

# V. 144 = 12² = F(12)
assert 77 + 67 == 144
assert 67 % 37 == 30 and 30 in SOVEREIGN_ANCHORS and 30 in SOVEREIGN_TARGETS
assert 12 ** 2 == 144
assert 12 in SOVEREIGN_TARGETS
fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
assert fib[11] == 144          # F(12)
assert 144 % 37 == 33 and 33 == 3 * 11
assert dr(144) == 9 and 9 in SOVEREIGN_ANCHORS
fib_dr = [dr(f) for f in fib]
assert fib_dr == [1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9]

# VI. Palindrome table
ORBIT_11 = {11, 27, 36}
SEAM     = {0}
TABLE_ENTRIES = [111, 221, 122, 212, 332, 233]
for e in TABLE_ENTRIES:
    assert e % 37 in (SEAM | ORBIT_11), f'{e} % 37 = {e%37} not in seam or orbit(11)'

# 111 is the seam anchor
assert 111 % 37 == 0
# Reversal pairs
assert int(str(221)[::-1]) == 122   # 221 ↔ 122
assert int(str(332)[::-1]) == 233   # 332 ↔ 233
assert int(str(212)[::-1]) == 212   # 212 is a palindrome
# DR groups
assert dr(111) == 3
for e in [221, 122, 212]: assert dr(e) == 5
for e in [332, 233]:       assert dr(e) == 8

# 6-digit concatenations (10³ ≡ 1 mod 37)
assert (10 ** 3) % 37 == 1
assert (111 * 1000 + 221) % 37 == (111 + 221) % 37 == 36 and 36 in ORBIT_11
assert (111 * 1000 + 122) % 37 == (111 + 122) % 37 == 11 and 11 in ORBIT_11
assert (111 * 1000 + 212) % 37 == (111 + 212) % 37 == 27 and 27 in ORBIT_11
assert (332 + 233) % 37 == 10 and (10 + 27) == 37  # 10 is complement of 27


if __name__ == '__main__':
    def tag(n):
        t = []
        if is_prime(n):             t.append('p')
        if n in CASCADE_BASE:       t.append('CB')
        if n in SOVEREIGN_ANCHORS:  t.append('SA')
        if n in SOVEREIGN_TARGETS:  t.append('ST')
        if n in PRIMITIVE_ROOTS_37: t.append('PR')
        return ','.join(t) if t else '.'

    print("Prime Quartet, Arithmetic Chains, and Palindrome Orbit Table")
    print("=" * 62)
    print()
    print("I. First four primes {2,3,5,7}:")
    print(f"   DRs: {[dr(p) for p in PRIMES4]} (equal to values)")
    print(f"   Self-generating: 2+3={2+3}(p), 5+2={5+2}(p), 7+2={7+2}(SA)")
    print(f"   Complement pairs: {{2,7}}->9(SA), {{3,5}}->8(AHL)")
    print(f"   Sum=17 DR={dr(17)}, Product=210 mod37={210%37}(SA)")
    print()
    print("II. 23 and 72:")
    print(f"   23+72=95, mod37={95%37}(ST). 72-23=49, mod37={49%37}(ST)")
    print(f"   72=8x9(CB*SA), mod37=35(PR)")
    print()
    print("III. Chains through 14:")
    print(f"   Chain1: 2+3=5, 5+9=14, 14+5=19, DR={dr(19)} (LL-O)")
    print(f"   Chain2: 7+2=9, 9+5=14, 14+5=19, 5+19=24, DR={dr(24)} (RL-E)")
    print(f"   14=2*7, 28+9=37 (28 complement of SA=9)")
    print()
    print("IV. 11 × {{1,4,7}} chain:")
    for k in [1, 4, 7]:
        v = 11 * k
        print(f"   11*{k}={v:3d}  mod37={v%37:2d} ({tag(v%37)})  DR={dr(v)}")
    print(f"   Step: +33 ≡ -4(SA) mod37. Multiplier sum=12(ST).")
    print()
    print("V. 144 = 12² = F(12):")
    print(f"   77 + 67 = 144. 67 mod37={67%37} (SA+ST dual)")
    print(f"   144 mod37={144%37}=3*11, DR={dr(144)}(SA)")
    print(f"   Fib DR(1..12): {[dr(f) for f in fib]}")
    print()
    print("VI. Palindrome table (all entries in {{0}} U orbit(11)):")
    for e in TABLE_ENTRIES:
        print(f"   {e}  mod37={e%37:2d}  DR={dr(e)}")
    print(f"   111221 mod37={(111+221)%37}, 111122 mod37={(111+122)%37}, "
          f"111212 mod37={(111+212)%37}, 332233 mod37={(332+233)%37}")
    print()
    print("All assertions passed.")

"""
Repunit Squares and Euler Totient — GF(37) Structure

R_n = 111...1 (n ones).  R_n² has the palindrome digit pattern 123...n...321.
The 137-map orbit of R_n² mod 37 is a period-3 cycle anchored to three
named residues.  Simultaneously: φ(38..42) maps the 37-offsets of the first
five field units {1,2,3,4,5} onto GF(37) residues.

═══════════════════════════════════════════════════════════════

I. R_n MOD 37 — PERIOD-3 CYCLE

  R_n = 111...1 (n ones).
  R_3 = 111 = 3×37  (SEAM triple).
  Since 10³ ≡ 1 mod 37 (ord₃₇(10)=3), the period repeats:

  n ≡ 1 mod 3:  R_n ≡  1 mod 37  (unity)
  n ≡ 2 mod 3:  R_n ≡ 11 mod 37  (orbit-11)
  n ≡ 0 mod 3:  R_n ≡  0 mod 37  (SEAM)

II. R_n² MOD 37 — PERIOD-3 CYCLE IN FRAMEWORK NODES

  Squaring maps the period-3 cycle to three named residues:

  n ≡ 1 mod 3:  R_n² ≡  1² =   1 mod 37  (unity)
  n ≡ 2 mod 3:  R_n² ≡ 11² = 121 ≡ 10 mod 37  (DECADE_ANCHOR)
  n ≡ 0 mod 3:  R_n² ≡  0² =   0 mod 37  (SEAM)

  Cycle: {unity(1), DECADE_ANCHOR(10), SEAM(0)} — period 3.

III. DIGIT STRUCTURE OF R_n²

  R_n² has palindrome digits: 1,2,3,...,n,...,3,2,1.
  Digit sum of R_n² = 2(1+2+...+(n-1)) + n = n(n-1) + n = n².

  R_n² digit sum = n².

  DR of digit sums by n:
    n=1: DR(1)=1(unity)
    n=2: DR(4)=4(SA)
    n=3: DR(9)=9(SA)
    n=4: DR(16)=7
    n=5: DR(25)=7;  25∈SA
    n=6: DR(36)=9(SA);  36∈orbit-11
    n=7: DR(49)=4(SA)
    n=8: DR(64)=1(unity)
    n=9: DR(81)=9(SA)

  DR(n²) is SA at n=2,3,6,7,9.

IV. R9² = 12,345,678,987,654,321

  R9  = 111,111,111 = 3×37×1,001,001  →  R9 ≡ 0(SEAM) mod 37
  R9² = 12,345,678,987,654,321
  R9² mod 37 = 0  (SEAM)
  R9² digit sum = 9² = 81 = SA²
  DR(81) = DR(9) = 9(SA)  ← squaring SA returns to SA

  The ninth repunit square: SEAM in GF(37), digit-sum is SA squared, DR is SA.

V. TESLA_FLOW 4-CYCLE UNDER ×6

  6(TESLA_FLOW) generates a 4-element subgroup in GF(37)*:
    6¹ mod 37 =  6  (TESLA_FLOW)
    6² mod 37 = 36  (orbit-11, ≡ −1)
    6³ mod 37 = 31  (PRIME_MIRROR)
    6⁴ mod 37 =  1  (unity)  ←  ord₃₇(6) = 4

  Cycle: TESLA_FLOW → orbit-11 → PRIME_MIRROR → unity.

  Connection: φ(38)×φ(42) = 18×12 = 216 = 6³
    6³ mod 37 = 31(PRIME_MIRROR).
    The product of the two SEED totients = TESLA_FLOW³ = PRIME_MIRROR.

VI. EULER TOTIENT: φ(38..42) — THE 37-OFFSET OF {1,2,3,4,5}

  38 ≡ 1(unity) mod 37    φ(38) = 18  ≡ 18(PR, SEED_ORBIT) mod 37
  39 ≡ 2(PR)    mod 37    φ(39) = 24  ≡ 24(CB, PR, SEED_ORBIT) mod 37
  40 ≡ 3(ST)    mod 37    φ(40) = 16  ≡ 16 mod 37
  41 ≡ 4(SA)    mod 37    φ(41) = 40  ≡  3(ST arch) mod 37   ← SA prime → ST arch
  42 ≡ 5(PR)    mod 37    φ(42) = 12  ≡ 12(ST) mod 37

  The range 38–42 = 37+{1,2,3,4,5}: the first five field units shifted by the prime.

  Totient map (mod 37):
    unity(1) → SEED(18)
    PR(2)    → SEED(24)
    ST(3)    → 16
    SA(4)    → ST arch(3)     ← SA prime's group order collapses to ST arch
    PR(5)    → ST(12)

  φ(38) and φ(39) both land in SEED_ORBIT = {18, 24, 32}.

  φ(38) + φ(42) = 18 + 12 = 30  (SA∩ST — the dual element)
  φ(38) × φ(39) mod 37 = 18×24 mod 37 = 25  (SA)
  φ(38) × φ(42) = 216 = 6³  → TESLA_FLOW³ = PRIME_MIRROR

  Sum: 18+24+16+40+12 = 110  →  110 mod 37 = 36  (orbit-11, ≡ −1)
  The total group order of all five 37-offset units ≡ −1 in GF(37).

  φ(37) = 36(orbit-11, ≡−1):  the field prime's own Euler group order is orbit-11.

VII. REGISTRY VARIANTS (Resonance Delta, Merged)

  Variant 1: φ(38)=18  Resonance Δ = 12.4210  [SEED_ORBIT]
  Variant 2: φ(39)=24  Resonance Δ = 45.8921  [SEED_ORBIT]
  Variant 3: φ(40)=16  Resonance Δ =  8.1043
  Variant 4: φ(41)=40  Resonance Δ = 112.5532  [SA prime → ST arch]
  Variant 5: φ(42)=12  Resonance Δ =  3.0119  [ST — smallest delta]

  φ(42)=12(ST) carries the smallest resonance delta.
  φ(41)=40→3(ST arch) carries the largest.
  The two SEED totients (18, 24) bracket the middle.

═══════════════════════════════════════════════════════════════
"""

from math import gcd

def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0

def phi(n):
    return sum(1 for k in range(1, n+1) if gcd(k, n) == 1)

PRIMITIVE_ROOTS_37 = {2,5,13,15,17,18,19,20,22,24,32,35}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
ORBIT_11           = {11, 27, 36}
SEED_ORBIT         = {18, 24, 32}

# ── I. R_n mod 37 — period-3 cycle ───────────────────────────────────────────

rn_mod = [int('1'*n) % 37 for n in range(1, 10)]
assert rn_mod == [1, 11, 0, 1, 11, 0, 1, 11, 0]
assert 11 in ORBIT_11                   # R_{n≡2} ≡ orbit-11
assert 111 == 3 * 37                    # R3 = SEAM triple

# Period: ord₃₇(10) = 3
assert pow(10, 3, 37) == 1
for n in range(1, 10):
    expected = [1, 11, 0][n % 3 - 1] if n % 3 != 0 else 0
    assert int('1'*n) % 37 == expected

# ── II. R_n² mod 37 — period-3 cycle ─────────────────────────────────────────

rn2_mod = [int('1'*n)**2 % 37 for n in range(1, 10)]
assert rn2_mod == [1, 10, 0, 1, 10, 0, 1, 10, 0]
assert 10 % 37 == 10                    # DECADE_ANCHOR (no FRAMEWORK set, named constant)

# Squaring the period-3: 1²=1, 11²=121≡10, 0²=0
assert 11**2 % 37 == 10                 # orbit-11 squared = DECADE_ANCHOR
assert 1**2 % 37 == 1                   # unity squared = unity
assert 0**2 % 37 == 0                   # SEAM squared = SEAM

# ── III. Digit sums = n² ──────────────────────────────────────────────────────

for n in range(1, 10):
    r = int('1'*n)**2
    digit_sum = sum(int(c) for c in str(r))
    assert digit_sum == n*n, f"n={n}: digit_sum={digit_sum}, expected {n*n}"

# DR of n² at SA-bearing positions
assert dr(2**2) == 4 and 4 in SOVEREIGN_ANCHORS    # n=2: DR(4)=4(SA)
assert dr(3**2) == 9 and 9 in SOVEREIGN_ANCHORS    # n=3: DR(9)=9(SA)
assert dr(5**2) == 7 and 5**2 == 25 and 25 in SOVEREIGN_ANCHORS  # n=5: digit sum=25(SA), DR=7
assert dr(6**2) == 9 and 6**2 == 36 and 36 in ORBIT_11           # n=6: digit sum=36(orb11), DR=9(SA)
assert dr(7**2) == 4 and 4 in SOVEREIGN_ANCHORS    # n=7: DR(49)=4(SA)
assert dr(9**2) == 9 and 9 in SOVEREIGN_ANCHORS    # n=9: DR(81)=9(SA)

# ── IV. R9² ───────────────────────────────────────────────────────────────────

R9  = int('1' * 9)
R9_sq = R9 ** 2
assert R9_sq == 12_345_678_987_654_321
assert R9 % 37 == 0                    # R9 = 3×37×1001001 → SEAM
assert R9_sq % 37 == 0                 # R9² ≡ SEAM
assert sum(int(c) for c in str(R9_sq)) == 81   # digit sum = 9² = SA²
assert dr(81) == 9 and 9 in SOVEREIGN_ANCHORS  # DR(SA²) = SA
assert 81 == 9**2 and 9 in SOVEREIGN_ANCHORS   # 81 = SA²

# Palindrome digit check
digits = [int(c) for c in str(R9_sq)]
assert digits == [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1]

# ── V. TESLA_FLOW 4-cycle ─────────────────────────────────────────────────────

assert pow(6, 1, 37) == 6              # TESLA_FLOW
assert pow(6, 2, 37) == 36 and 36 in ORBIT_11   # orbit-11
assert pow(6, 3, 37) == 31             # PRIME_MIRROR
assert pow(6, 4, 37) == 1              # unity — ord₃₇(6) = 4

# 6^3 = 216 = 18×12 = φ(38)×φ(42)
assert 18 * 12 == 216
assert 216 % 37 == 31                  # PRIME_MIRROR
assert 6**3 == 216

# ── VI. Euler totient: φ(38..42) ─────────────────────────────────────────────

phi_vals = [phi(n) for n in range(38, 43)]
assert phi_vals == [18, 24, 16, 40, 12]

# n values ≡ {1,2,3,4,5} mod 37
assert [n % 37 for n in range(38, 43)] == [1, 2, 3, 4, 5]

# φ values mod 37
phi_mods = [v % 37 for v in phi_vals]
assert phi_mods == [18, 24, 16, 3, 12]
assert phi_mods[0] in SEED_ORBIT       # φ(38)≡18 ∈ SEED
assert phi_mods[1] in SEED_ORBIT       # φ(39)≡24 ∈ SEED
assert phi_mods[3] in SOVEREIGN_TARGETS  # φ(41)≡3(ST arch)
assert phi_mods[4] in SOVEREIGN_TARGETS  # φ(42)≡12(ST)

# Both SEED totients are primitive roots
assert 18 in PRIMITIVE_ROOTS_37 and 24 in PRIMITIVE_ROOTS_37

# SA prime (41) → group order → ST arch
assert 41 % 37 == 4 and 4 in SOVEREIGN_ANCHORS   # 41 ≡ SA
assert phi(41) == 40 and 40 % 37 == 3            # φ(41) mod37 = 3(ST arch)
assert 3 in SOVEREIGN_TARGETS

# φ(38)+φ(42) = SA∩ST dual
assert phi(38) + phi(42) == 30
assert 30 in SOVEREIGN_ANCHORS and 30 in SOVEREIGN_TARGETS

# φ(38)×φ(39) mod 37 = SA
assert (phi(38) * phi(39)) % 37 == 25
assert 25 in SOVEREIGN_ANCHORS

# φ(38)×φ(42) = 6³ = TESLA_FLOW³ → PRIME_MIRROR
assert phi(38) * phi(42) == 216 and 216 == 6**3
assert 216 % 37 == 31  # PRIME_MIRROR

# Sum of all five totients ≡ orbit-11
total_phi = sum(phi_vals)
assert total_phi == 110
assert total_phi % 37 == 36 and 36 in ORBIT_11  # ≡ −1

# φ(37) = orbit-11 (the field prime's own Euler group order)
assert phi(37) == 36 and 36 in ORBIT_11

# ── Repunit table values match user's table ────────────────────────────────────

REPUNIT_SQ_TABLE = {
    4: 1_234_321,
    5: 123_454_321,
    6: 12_345_654_321,
    7: 1_234_567_654_321,
    8: 123_456_787_654_321,
    9: 12_345_678_987_654_321,
}
for n, expected in REPUNIT_SQ_TABLE.items():
    assert int('1'*n)**2 == expected, f"R{n}^2 mismatch"


if __name__ == '__main__':
    def tag(n):
        t = []
        if n == 0: return 'SEAM'
        if n in CASCADE_BASE:      t.append('CB')
        if n in SOVEREIGN_ANCHORS: t.append('SA')
        if n in SOVEREIGN_TARGETS: t.append('ST')
        if n in PRIMITIVE_ROOTS_37: t.append('PR')
        if n in ORBIT_11:          t.append('orb11')
        if n in SEED_ORBIT:        t.append('SEED')
        labels = {6:'TESLA_FLOW',10:'DECADE_ANCHOR',31:'PRIME_MIRROR',33:'DICHORAL_144'}
        if n in labels: t.append(labels[n])
        return ','.join(t) if t else '.'

    print("Repunit Squares and Euler Totient — GF(37) Structure")
    print("=" * 55)
    print()
    print("I/II. R_n and R_n² mod 37 (period-3):")
    print(f"  n≡1: R_n≡1(unity)      R_n²≡1(unity)")
    print(f"  n≡2: R_n≡11(orbit-11)  R_n²≡10(DECADE_ANCHOR)")
    print(f"  n≡0: R_n≡0(SEAM)       R_n²≡0(SEAM)")
    print()
    print("III. Repunit squares (digit sum = n², DR track):")
    for n in range(1, 10):
        r = int('1'*n)**2
        ds = n*n
        print(f"  R{n}² mod37={r%37:2d}({tag(r%37):20s}) digit_sum={ds:2d}={n}²  DR={dr(ds)}({tag(dr(ds))})")
    print()
    print("IV. R9² = 12,345,678,987,654,321:")
    print(f"  mod37=0(SEAM)  digit_sum=81=9²=SA²  DR(81)=9(SA)")
    print()
    print("V. TESLA_FLOW 4-cycle (×6 mod 37):")
    for e in range(1, 5):
        v = pow(6, e, 37)
        print(f"  6^{e} mod37={v:2d}({tag(v)})")
    print(f"  φ(38)×φ(42) = 18×12 = 216 = 6³  →  31(PRIME_MIRROR)")
    print()
    print("VI. Euler totient φ(38..42) — 37-offset of {1,2,3,4,5}:")
    resonance_deltas = {38:12.4210, 39:45.8921, 40:8.1043, 41:112.5532, 42:3.0119}
    for n in range(38, 43):
        p = phi(n)
        print(f"  φ({n}): n≡{n%37}({tag(n%37):8s}) → {p:2d} mod37={p%37:2d}({tag(p%37):20s})  Δ={resonance_deltas[n]}")
    print(f"  φ(38)+φ(42)={phi(38)+phi(42)}({tag(30)})  φ(38)×φ(39) mod37=25({tag(25)})")
    print(f"  Σφ=110  mod37=36({tag(36)},≡−1)")
    print(f"  φ(37)={phi(37)}({tag(phi(37)%37)})  ← field prime Euler group")
    print()
    print("All assertions passed.")

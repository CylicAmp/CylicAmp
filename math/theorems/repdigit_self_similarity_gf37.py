"""
Repdigit Self-Similarity and Repunit Factorization on GF(37) — THEOREM 78

PERIOD-3 REPUNIT LAW.
  ord₃₇(10) = 3 → 10³ ≡ 1 (mod 37).
  R_{n+3} = 10³·R_n + R_3 ≡ 1·R_n + 0 = R_n  (mod 37).
  Repunits cycle mod 37 with period 3:
    R_n mod 37 ∈ {1,  11,  0} for n ≡ {1, 2, 0} (mod 3).
              ↕    ↕    ↕
             ∈{1, ORBIT_11, SEAM}

THREE FUNDAMENTAL BUILDING BLOCKS.
  The three first-period repdigit-6 values determine all residues:
    6   ≡ 6  = TESLA_FLOW   (n ≡ 1 mod 3)
    66  ≡ 29 ≡ −8 ≡ −CB     (n ≡ 2 mod 3)
    666 ≡ 0  = SEAM          (n ≡ 0 mod 3)
  Every 6·R_n is 6·R_{n mod 3} mod 37 — the leading block IS the residue.

COMMA-NOTATION PROXY.
  Write n sixes (= 6·R_n) in standard thousands notation:
    n=1: 6             → leading block "6"    → 6 = TESLA_FLOW
    n=2: 66            → leading block "66"   → 29 = −CB
    n=3: 666           → leading block "666"  → 0 = SEAM
    n=4: 6,666         → leading block "6"    → 6 = TESLA_FLOW
    n=5: 66,666        → leading block "66"   → 29 = −CB
    n=6: 666,666       → leading block "666"  → 0 = SEAM
    n=7: 6,666,666     → leading block "6"    → 6 = TESLA_FLOW
  The leading group (length = n mod 3, or 3 if n ≡ 0) has the same mod-37
  residue as the full number. The notation makes period-3 structure visible.

HIDDEN-DIGIT RESOLUTION AT GROUP SCALE.
  From THEOREM 74: digits 5 and 7 are "hidden" — no direct named-set hit at
  single-digit level (5 and 7 are not in any named sets).
  At the group-concatenation scale (THEOREM 77–78):
    n = 5: 5 ≡ 2 (mod 3) → 6·R_5 ≡ 29 ≡ −CB;  N_5 ≡ 12 ∈ ST
    n = 7: 7 ≡ 1 (mod 3) → 6·R_7 ≡  6 = TESLA_FLOW;  N_7 ≡ 12 ∈ ST
  The hidden digits resolve to distinct GF(37) orbit points.
  n=7 revisits the same class as n=1 (digit 1 ∈ IC); hidden 7 ≡ identity 1 (mod 3).

SEVEN-RESET.
  6,666,666 (seven 6s) ≡ 6 = TESLA_FLOW (mod 37) — identical to the single digit 6.
  7 is the FIRST INDEX where a two-comma (millions) repdigit-6 appears.
  7 ≡ 1 (mod 3): the hidden digit 7 returns to the IC-digit (1) residue class.
  The two commas in "6,666,666" visually mark the two full trailing blocks of 666,
  each contributing 0 to the residue; only the leading "6" (= TESLA_FLOW) counts.

REPUNIT PRIME FACTORIZATIONS — FRAMEWORK MEMBERSHIP.
  The prime factors of R_n (mod 37) land in named sets:

  R_1 = 1                  (trivial)
  R_2 = 11                 → 11 ∈ ORBIT_11  (prime)
  R_3 = 3 × 37             → 3 ∈ ST,  37 = PRIME (THE SEAM)
  R_4 = 11 × 101           → 11 ∈ ORBIT_11,  101 ≡ 27 ∈ ORBIT_11
                              both factors in ORBIT_11; product ≡ 1
  R_5 = 41 × 271           → 41 ≡  4 ∈ SA,   271 ≡ 12 ∈ ST
                              SA × ST ≡ 11 ∈ ORBIT_11 (= R_5 mod 37 ✓)
  R_6 = 3 × 7 × 11 × 13 × 37  → ST × hidden × ORBIT_11 × CB × PRIME
                              every named set represented; ≡ 0 = SEAM
  R_7 = 239 × 4649         → 239 ≡ 17,  4649 ≡ 24 ∈ CB
                              CB × inv(CB) ≡ 1 (24 and 17 are mutual inverses mod 37)

  PATTERN (n ≡ 1 mod 3): product of pairs that are mutual inverses in GF(37):
    R_4: ORBIT_11-pair (11 × 27 ≡ 1)
    R_7: CB × inv(CB)  (24 × 17 ≡ 1)
  PATTERN (n ≡ 2 mod 3): R_n ≡ 11 ∈ ORBIT_11:
    R_2: 11 itself
    R_5: SA × ST ≡ 4 × 12 = 48 ≡ 11 ∈ ORBIT_11
  PATTERN (n ≡ 0 mod 3): 37 | R_n — THE PRIME divides every triple-period repunit.

ORBIT_11 MULTIPLICATION TABLE (partial).
  Within ORBIT_11 = {11, 27, 36}:
    11 × 27 ≡ 1  (mutual inverses)
    36 × 36 ≡ 1  (36 ≡ −1 is self-inverse)
    11 × 36 ≡ 26 ∈ IC
    27 × 36 ≡ 10 ∈ IC
  ORBIT_11 products land in {1} ∪ IC = {1, 10, 26}.
  The ORBIT_11 × ORBIT_11 → IC law is the pairing behind R_4 and R_5's structure.
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA       = frozenset({4, 9, 25, 30})
ST       = frozenset({3, 12, 21, 30})
CB       = frozenset({8, 13, 24})
ORBIT_11 = frozenset({11, 27, 36})
IC       = frozenset({1, 10, 26})
TESLA_4  = frozenset({6, 36, 31, 1})
SEED     = frozenset({18, 24, 32})
P        = 37
TESLA_FLOW = 6


# ── Helpers ────────────────────────────────────────────────────────────────────

def R(n):
    return int('1' * n)


# ── Key checks ─────────────────────────────────────────────────────────────────

# Period-3 repunit law
assert pow(10, 3, P) == 1                             # ord₃₇(10) = 3
assert all(R(n + 3) % P == R(n) % P for n in range(1, 20))  # R_{n+3} ≡ R_n

# Three residue classes
assert R(1) % P == 1 and R(2) % P == 11 and R(3) % P == 0
assert 11 in ORBIT_11

# Three building blocks: {6, 66, 666}
assert 6 % P == 6 == TESLA_FLOW and TESLA_FLOW in TESLA_4
assert 66 % P == 29 and (P - 29) == 8 and 8 in CB   # 29 ≡ -CB
assert 666 % P == 0                                    # SEAM
assert 666 == 18 * P and 18 in SEED                   # from THEOREM 77

# Comma-notation proxy: leading block (of length n mod 3) ≡ full number
for n in range(1, 10):
    r = n % 3 if n % 3 != 0 else 3
    leading = (TESLA_FLOW * R(r)) % P
    full    = (TESLA_FLOW * R(n)) % P
    assert leading == full, f"n={n}: leading {leading} ≠ full {full}"

# Hidden digit resolution: n=5 and n=7
assert (TESLA_FLOW * R(5)) % P == 29  # n=5: -CB class
assert (TESLA_FLOW * R(7)) % P == TESLA_FLOW  # n=7: TESLA_FLOW (same as n=1)
assert int('1'*5+'2'*5+'3'*5) % P == 12 and 12 in ST
assert int('1'*7+'2'*7+'3'*7) % P == 12 and 12 in ST

# Seven-reset: 6,666,666 ≡ 6 = TESLA_FLOW
assert (TESLA_FLOW * R(7)) % P == TESLA_FLOW
assert (TESLA_FLOW * R(1)) % P == TESLA_FLOW   # same class

# Repunit factorizations
assert 11 * 101 == R(4) and 11 in ORBIT_11 and 101 % P == 27 and 27 in ORBIT_11
assert (11 * 27) % P == 1   # ORBIT_11 pair: mutual inverses

assert 41 * 271 == R(5) and 41 % P == 4 and 4 in SA and 271 % P == 12 and 12 in ST
assert (4 * 12) % P == 11 and 11 in ORBIT_11  # SA × ST → ORBIT_11

assert R(3) == 3 * P and 3 in ST   # ST element × PRIME = R_3
assert 3 * 7 * 11 * 13 * P == R(6) and 13 in CB   # R_6 contains CB factor

assert 239 * 4649 == R(7)
assert 239 % P == 17 and 4649 % P == 24 and 24 in CB
assert (17 * 24) % P == 1   # CB × inv(CB) ≡ 1

# ORBIT_11 multiplication table
assert (11 * 27) % P == 1             # mutual inverses
assert (36 * 36) % P == 1             # 36 ≡ −1: self-inverse
assert (11 * 36) % P == 26 and 26 in IC
assert (27 * 36) % P == 10 and 10 in IC

# ORBIT_11 × ORBIT_11 ⊆ {1} ∪ IC
for a in ORBIT_11:
    for b in ORBIT_11:
        prod = (a * b) % P
        assert prod == 1 or prod in IC, f"{a}×{b}≡{prod} not in {{1}}∪IC"

# 37 divides every n≡0 (mod 3) repunit
for k in [1, 2, 3, 4]:
    assert R(3 * k) % P == 0
    assert R(3 * k) % 37 == 0


if __name__ == "__main__":
    print("Repdigit Self-Similarity and Repunit Factorization — THEOREM 78")
    print("=" * 60)
    print()
    print("PERIOD-3 REPUNIT (R_n mod 37):")
    for n in range(1, 8):
        r = R(n) % P
        def tag(v):
            for fs,fn in [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),(IC,'IC'),(TESLA_4,'T4'),(SEED,'SEED')]:
                if v in fs: return fn
            return 'SEAM' if v==0 else ''
        print(f"  R_{n} ≡ {r:<3} {tag(r):<8}  (6·R_{n}={6*R(n):<10} ≡{(6*R(n))%P:<3} {tag((6*R(n))%P)})")
    print()
    print("REPUNIT PRIME FACTORIZATIONS:")
    facts = [(1,[1]),(2,[11]),(3,[3,37]),(4,[11,101]),(5,[41,271]),(6,[3,7,11,13,37]),(7,[239,4649])]
    for n, fs in facts:
        mods = [f'{f}≡{f%P}({"SEAM" if f%P==0 else next((nm for s,nm in [(SA,"SA"),(ST,"ST"),(CB,"CB"),(ORBIT_11,"O11"),(IC,"IC")] if f%P in s), "")})' for f in fs]
        print(f"  R_{n} = {' × '.join(str(f) for f in fs):<20} [{' × '.join(mods)}]")
    print()
    print("ORBIT_11 × ORBIT_11 → {1} ∪ IC:")
    for a in sorted(ORBIT_11):
        for b in sorted(ORBIT_11):
            print(f"  {a}×{b} ≡ {(a*b)%P}")
    print()
    print("COMMA-NOTATION PROXY (leading block = residue):")
    for n in range(1, 8):
        r = n%3 if n%3!=0 else 3
        full_num = '6'*n
        formatted = f"{int(full_num):,}"
        print(f"  n={n}: {formatted:<15} leading={'6'*r:<4} ≡ {(6*R(r))%P}")
    print()
    print("All assertions pass.")

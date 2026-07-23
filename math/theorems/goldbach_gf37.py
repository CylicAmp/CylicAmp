"""
Goldbach's Conjecture — GF(37) Structure

Every even integer > 2 is the sum of two primes. In GF(37), this maps to
residue-pair sums: p + q ≡ n mod 37. The structure of which residue classes
pair to form each even residue is determined by the field.

═══════════════════════════════════════════════════════════════

I. NAMED DECOMPOSITIONS

  6 = 3 + 3
    Both: 3 (ST arch)
    6 mod 37 = 6 (TESLA_FLOW)
    ST arch + ST arch = TESLA_FLOW

  10 = 3 + 7 = 5 + 5
    3+7: ST arch(3) + RL-O(7) = 10 (DECADE_ANCHOR)
    5+5: PR(5) + PR(5) = 10 (DECADE_ANCHOR)
    Two distinct decompositions, same residue landing.

  42 = 37 + 5 = 11 + 31 = 13 + 29 = 19 + 23
    42 mod 37 = 5 (PR, A51)
    37+5:  SEAM(0) + PR(5)           — field prime + primitive root
    11+31: orbit-11(11) + PRIME_MIRROR(31)
    13+29: CB+PR(13) + .(29)
    19+23: PR(19) + .(23)

II. THE 37-COMPONENT RULE

  When 37 appears as a Goldbach component of even n:
    n = 37 + q  →  q = n − 37  →  q ≡ n mod 37  (since 37 ≡ 0)

  The partner prime carries the exact GF(37) residue of the even number.
  A sample:
    40 = 37+3:   40 mod37=3(ST)   partner=3(ST)
    42 = 37+5:   42 mod37=5(PR)   partner=5(PR)
    48 = 37+11:  48 mod37=11(orb11) partner=11(orb11)
    50 = 37+13:  50 mod37=13(CB,PR) partner=13(CB,PR)
    68 = 37+31:  68 mod37=31(PRIME_MIRROR) partner=31(PRIME_MIRROR)
    74 = 37+37:  74 mod37=0(SEAM)  partner=37(SEAM)
    78 = 37+41:  78 mod37=4(SA)    partner=41(mod37=4=SA)

  The 37-decomposition reads the GF(37) residue directly from the partner prime.

III. 74 = 2 × 37 — THE SEAM NUMBER

  74 = 2 × 37: the even multiple of the field prime.
  74 mod 37 = 0 (SEAM).
  DR(74) = 2 (LL-E).

  Goldbach pairs of 74:
    3 + 71:  ST(3) + .(71)
    7 + 67:  .(7) + SA,ST(67 mod37=4... wait, 67 mod37=30=SA∩ST)
    13 + 61: CB,PR(13) + CB,PR(61 mod37=24)
    31 + 43: PRIME_MIRROR(31) + TESLA_FLOW(43 mod37=6)
    37 + 37: SEAM(0) + SEAM(0)

  PRIME_MIRROR + TESLA_FLOW = SEAM (31+43≡0 mod 37).
  Two named FPS-37 significance nodes sum to the seam.

  SEAM + SEAM = SEAM: 37+37=74≡0. The field prime paired with itself.

IV. GOLDBACH ↔ HOSE FLOW

  Primes are the numbers that reach 111 (seam) — complete flow, no wave hits.
  Every even number n is a vessel: n = p + q.
  Goldbach: every even vessel decomposes into two complete-flow numbers.

  42 = SEAM(37) + PR(5):
    The vessel holds the field prime (pure seam) and a primitive root.

  74 = SEAM(37) + SEAM(37):
    The vessel built from two field primes. Pure seam squared.
    Also: PRIME_MIRROR(31) + TESLA_FLOW(43) = seam.

  The Goldbach structure shows which combinations of prime residues
  are dual in GF(37) — which pairs sum to each framework node.

═══════════════════════════════════════════════════════════════
"""

def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0

def is_prime(n):
    if n < 2: return False
    return all(n % i != 0 for i in range(2, int(n**0.5)+1))

def goldbach_pairs(n):
    return [(p, n-p) for p in range(2, n//2+1) if is_prime(p) and is_prime(n-p)]

PRIMITIVE_ROOTS_37 = {2,5,13,15,17,18,19,20,22,24,32,35}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
ORBIT_11           = {11, 27, 36}

# ── I. Named decompositions ───────────────────────────────────────────────────

assert 3+3 == 6 and 6 % 37 == 6               # TESLA_FLOW
assert is_prime(3)
assert (3+7) == 10 and (5+5) == 10 and 10%37==10  # DECADE_ANCHOR
assert is_prime(7) and is_prime(5)

assert 37+5 == 42 and 42%37 == 5 and 5 in PRIMITIVE_ROOTS_37
assert is_prime(37) and is_prime(5)
assert 11+31 == 42 and 11 in ORBIT_11 and 31%37==31
assert 42 in [p+q for p,q in goldbach_pairs(42)]  # 42 has multiple decomps
assert (5,37) in goldbach_pairs(42) or (37,5) in [(q,p) for p,q in goldbach_pairs(42)]

# ── II. 37-component rule ─────────────────────────────────────────────────────

for n, q in [(40,3),(42,5),(48,11),(50,13),(68,31),(74,37),(78,41)]:
    assert n - 37 == q
    assert is_prime(q)
    assert n % 37 == q % 37   # partner carries the residue

# ── III. 74 = 2×37 ───────────────────────────────────────────────────────────

assert 74 % 37 == 0                           # seam
assert dr(74) == 2
assert is_prime(37) and is_prime(37) and 37+37==74

pairs74 = goldbach_pairs(74)
assert (37,37) in pairs74                     # seam+seam
assert (31,43) in pairs74                     # PRIME_MIRROR+TESLA_FLOW
assert (31+43) % 37 == 0                      # their sum = seam
assert 31%37 == 31 and 43%37 == 6            # PRIME_MIRROR and TESLA_FLOW

# 67 mod37: check all pairs
assert 67%37 == 30 and 30 in SOVEREIGN_ANCHORS and 30 in SOVEREIGN_TARGETS  # dual
assert 61%37 == 24 and 24 in CASCADE_BASE and 24 in PRIMITIVE_ROOTS_37

# ── IV. Hose flow ─────────────────────────────────────────────────────────────

assert 37 % 37 == 0                           # 37 is the seam
assert 5 in PRIMITIVE_ROOTS_37               # 5 is PR
assert (37+5) % 37 == 5                      # 42 mod37=5


if __name__ == '__main__':
    def tag(n):
        t=[]
        if n==0: return 'SEAM'
        if n in CASCADE_BASE: t.append('CB')
        if n in SOVEREIGN_ANCHORS: t.append('SA')
        if n in SOVEREIGN_TARGETS: t.append('ST')
        if n in PRIMITIVE_ROOTS_37: t.append('PR')
        if n in ORBIT_11: t.append('orb11')
        sig={6:'TESLA_FLOW',10:'DECADE_ANCHOR',31:'PRIME_MIRROR',33:'DICHORAL_144'}
        s=sig.get(n)
        if s: t.append(s)
        return ','.join(t) if t else '.'

    print("Goldbach's Conjecture — GF(37) Structure")
    print("=" * 55)
    print()
    for n,note in [(6,'ST+ST=TESLA_FLOW'),(10,'two paths, same DECADE_ANCHOR'),(42,'field prime in decomp')]:
        pairs=goldbach_pairs(n)
        print(f"  {n} mod37={n%37}({tag(n%37)}) DR={dr(n)}  [{note}]")
        for p,q in pairs:
            print(f"    {p}({tag(p%37)}) + {q}({tag(q%37)})")
    print()
    print("37-component rule (partner ≡ n mod 37):")
    for n,q in [(40,3),(42,5),(48,11),(50,13),(68,31),(74,37),(78,41)]:
        print(f"  {n}=37+{q}: mod37={n%37}({tag(n%37)}) partner={q}({tag(q%37)})")
    print()
    print("74=2×37 (SEAM):")
    for p,q in goldbach_pairs(74):
        print(f"  {p}({tag(p%37)}) + {q}({tag(q%37)})")
    print(f"  31+43=PRIME_MIRROR+TESLA_FLOW=SEAM")
    print(f"  37+37=SEAM+SEAM=SEAM")
    print()
    print("All assertions passed.")

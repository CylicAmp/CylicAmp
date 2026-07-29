"""
Ghost Kervaire Chain and the Fermat-SEAM Identity on GF(37) — THEOREM 82

USER INPUT: 2+4 = 6+7 = 14+16 = 30+32 = 62+12+4+2
  Read as five groups; each group sums to a term of the ghost chain:
    (2+4) → 6     (6+7) → 13     (14+16) → 30     (30+32) → 62     (62+12+4+2) → 80
  Partial sums: 6, 13, 30, 62, 80.

GHOST KERVAIRE CHAIN.
  The five partial sums, mod 37:
    6   ≡  6 ∈ TESLA_4   (= TESLA_FLOW = K(3), second Kervaire dimension)
    13  ≡ 13 ∈ CB         (Cascade Base element — CB landing)
    30  ≡ 30 ∈ SA∩ST      (Sovereign junction node)
    62  ≡ 25 ∈ SA          (Sovereign Anchor)
    80  ≡  6 ∈ TESLA_4   (CYCLE CLOSES: returns to TESLA_FLOW)
  The chain traverses: TESLA_4 → CB → SA∩ST → SA → TESLA_4.
  Starting node = ending node = 6 = TESLA_FLOW mod 37.

FOUR GAP VALUES.
  Gaps between consecutive partial sums: 7, 17, 32, 18.
  These replace the "correct" Kervaire increments 8, (none), 32, 64 with GF(37)-significant values.
  Sum of gaps:  7+17+32+18 = 74 = 2×37 = 2×PRIME ≡ 0 = SEAM (mod 37).
  Paired sub-sums:
    7 + 17 = 24 ∈ CB ∩ SEED_ORBIT   (first two gaps sum to CB node)
    32 + 18 = 50 ≡ 13 ∈ CB          (last two gaps sum to CB element 13)
  Both gap-pairs land in CB. Together: 24 + 13 = 37 = PRIME → SEAM.

GHOST INCREMENTS.
  The chain uses 7 (not 8=2³=K(3)+2) and 18 (not 64=2⁶) as "ghost" steps.
    8 ∈ CB: the correct step hits CB; the ghost step (7) is one below CB.
    18 ∈ SEED_ORBIT: the ghost step uses the SEED node rather than 2⁶≡27∈ORBIT_11.
  Ghost increment sum: 7 + 18 = 25 ∈ SA (Sovereign Anchor).
  Cross-pairs: 7+32 = 39 ≡ 2 ∈ PR;  17+18 = 35 ∈ PR.
    Both cross-pairs land in PR (primitive roots mod 37).

SUM AND PRODUCT OF PARTIAL SUMS.
  Sum:      6+13+30+62+80 = 191 ≡ 6 = TESLA_FLOW (mod 37).  [sum = start = TESLA_FLOW]
  Product:  6×13×30×62×80 ≡ 18 ∈ SEED_ORBIT (mod 37).       [product lands in SEED]
  The product 18 matches the sum of all Kervaire dimensions ≡ 18∈SEED (THEOREM 81).

KERVAIRE RECURRENCE K(j+1) = 2·K(j) + 2 (mod 37).
  Closed form: K(j) = 2^j − 2 ≡ 4·2^{j-2} − 2 (mod 37).
  Fixed point: K = 35∈PR  (2×35+2=72≡35 mod 37).
  Period: 36 = ord₃₇(2) = φ(37).  K(j+36) ≡ K(j) for all j.

FERMAT-SEAM IDENTITY.
  K(p) ≡ 0 = SEAM (mod p) for any prime p.
  Proof: K(p) = 2^p − 2 ≡ 2 − 2 = 0 (mod p)  by Fermat's little theorem (a^p ≡ a).
  For p = 37:  K(37) = 2^{37} − 2 ≡ 0 = SEAM (mod 37).
  The Kervaire recurrence hits SEAM at exactly j = 37 = THE PRIME.
  This is the FIRST SEAM hit: no j ∈ {2,...,36} gives K(j) ≡ 0 (mod 37)
  (since 2^j ≡ 2 mod 37 only for j ≡ 1 mod 36, i.e., j=1,37,73,...).

PERIOD-37 FRAMEWORK SCAN.
  Framework hits in K(j) mod 37 for j = 2,...,37:
    j = 3:  K ≡  6 ∈ TESLA_4   (TESLA_FLOW = K(3))
    j = 5:  K ≡ 30 ∈ SA        (=SA∩ST junction)
    j = 6:  K ≡ 25 ∈ SA
    j = 8:  K ≡ 32 ∈ SEED_ORBIT (first excluded Kervaire dim; first SEED hit)
    j = 11: K ≡ 11 ∈ ORBIT_11
    j = 12: K ≡ 24 ∈ CB ∩ SEED_ORBIT
    j = 13: K ≡ 13 ∈ CB
    j = 15: K ≡ 21 ∈ ST
    j = 20: K ≡ 31 ∈ TESLA_4
    j = 21: K ≡ 27 ∈ ORBIT_11
    j = 23: K ≡  3 ∈ ST
    j = 24: K ≡  8 ∈ CB
    j = 25: K ≡ 18 ∈ SEED_ORBIT
    j = 26: K ≡  1 ∈ IC
    j = 27: K ≡  4 ∈ SA
    j = 28: K ≡ 10 ∈ IC
    j = 30: K ≡  9 ∈ SA
    j = 33: K ≡ 12 ∈ ST
    j = 34: K ≡ 26 ∈ IC  (= SCALAR_137)
    j = 36: K ≡ 36 ∈ ORBIT_11
    j = 37: K ≡  0 = SEAM   (Fermat-SEAM identity)
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
IC         = frozenset({1, 10, 26})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
P          = 37
TESLA_FLOW = 6


# ── Ghost Kervaire chain ─────────────────────────────────────────────────────────

GHOST_GROUPS = [(2, 4), (6, 7), (14, 16), (30, 32), (62, 12, 4, 2)]
PARTIALS     = [sum(g) for g in GHOST_GROUPS]   # [6, 13, 30, 62, 80]

assert PARTIALS == [6, 13, 30, 62, 80]

# Mod-37 partial sums form a closed cycle starting and ending at TESLA_FLOW
_mods = [s % P for s in PARTIALS]
assert _mods == [6, 13, 30, 25, 6]
assert _mods[0] == _mods[-1] == TESLA_FLOW   # cycle closes at TESLA_FLOW
assert 6 in TESLA_4 and 13 in CB and 30 in SA and 30 in ST and 25 in SA

# ── Gap analysis ────────────────────────────────────────────────────────────────

GAPS = [PARTIALS[i+1] - PARTIALS[i] for i in range(len(PARTIALS) - 1)]
assert GAPS == [7, 17, 32, 18]

# Sum of gaps = 2×PRIME = SEAM
assert sum(GAPS) == 2 * P == 74
assert sum(GAPS) % P == 0   # SEAM

# Gap sub-sums both land in CB
assert (7 + 17) == 24 and 24 in CB and 24 in SEED_ORBIT
assert (32 + 18) % P == 13 and 13 in CB

# Together: both CB nodes sum to PRIME
assert (24 + 13) == P   # 24 + 13 = 37 = PRIME → SEAM

# ── Ghost increments ─────────────────────────────────────────────────────────────

# Ghost increments: 7 (instead of 8∈CB) and 18∈SEED (instead of 64≡27∈ORBIT_11)
assert (7 + 18) % P == 25 and 25 in SA   # ghost increment sum ∈ SA
assert (7 + 32) % P == 2 and 2 in PR     # cross-pair 1 ∈ PR
assert (17 + 18) % P == 35 and 35 in PR  # cross-pair 2 ∈ PR

# ── Sum and product of partial sums ──────────────────────────────────────────────

assert sum(PARTIALS) == 191 and sum(PARTIALS) % P == 6 == TESLA_FLOW

import math
_prod = math.prod(s % P for s in PARTIALS) % P
assert _prod == 18 and 18 in SEED_ORBIT   # product ≡ 18 ∈ SEED_ORBIT
# same SEED value as sum of all Kervaire dims (THEOREM 81: ∑K(j)=240≡18∈SEED)
assert 240 % P == 18 and _prod == 240 % P

# ── Kervaire recurrence mod P ────────────────────────────────────────────────────

def K_mod(j, p=P, start=2):
    k = start
    for _ in range(j - 2):
        k = (2 * k + 2) % p
    return k


# Fixed point: 2×35+2≡35 (mod 37)
assert (2 * 35 + 2) % P == 35 and 35 in PR

# Period = 36 = ord₃₇(2)
assert K_mod(2) == 2 and K_mod(2 + 36) == 2   # period 36

# ── Fermat-SEAM identity: K(p) ≡ 0 = SEAM (mod p) ──────────────────────────────

# By Fermat's little theorem: 2^p ≡ 2 (mod p) → K(p)=2^p-2≡0
assert pow(2, P, P) == 2           # Fermat: 2^37 ≡ 2 (mod 37)
assert K_mod(P) == 0               # K(37) ≡ 0 = SEAM

# First occurrence of SEAM in the recurrence
_first_seam = next(j for j in range(2, 100) if K_mod(j) == 0)
assert _first_seam == P == 37      # j=37 is the FIRST SEAM hit

# No earlier SEAM: for j=2,...,36, K(j) ≠ 0
assert all(K_mod(j) != 0 for j in range(2, P))

# ── Period-37 framework scan ─────────────────────────────────────────────────────

EXPECTED_HITS = {
    3: TESLA_4, 5: SA, 6: SA, 8: SEED_ORBIT, 11: ORBIT_11,
    12: CB, 13: CB, 15: ST, 20: TESLA_4, 21: ORBIT_11, 23: ST,
    24: CB, 25: SEED_ORBIT, 26: IC, 27: SA, 28: IC,
    30: SA, 33: ST, 34: IC, 36: ORBIT_11,
}

for j, expected_set in EXPECTED_HITS.items():
    kj = K_mod(j)
    assert kj in expected_set, f"j={j}: K≡{kj} not in expected set {expected_set}"

assert K_mod(37) == 0   # SEAM (Fermat-SEAM)

# Verify all non-SEAM j in [2..36] have framework or non-framework residues
# (not asserting all are framework; some are non-framework, which is fine)
_fw_hits = [j for j in range(2, 38) if K_mod(j) in SA | ST | CB | ORBIT_11 | IC | SEED_ORBIT | TESLA_4]
assert set(EXPECTED_HITS.keys()).issubset(set(_fw_hits))


if __name__ == "__main__":
    print("Ghost Kervaire Chain and the Fermat-SEAM Identity on GF(37) — THEOREM 82")
    print("=" * 72)
    print()
    print("GHOST KERVAIRE CHAIN (user's groups → partial sums):")
    fw_map = [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),
              (IC,'IC'),(SEED_ORBIT,'SEED'),(TESLA_4,'T4'),(PR,'PR')]
    def fw(n):
        n = n % P
        for s,nm in fw_map:
            if n in s: return nm
        return '—' if n != 0 else 'SEAM'
    for i, (g, ps) in enumerate(zip(GHOST_GROUPS, PARTIALS)):
        print(f"  {'+'.join(str(x) for x in g):>15} = {ps:>3}  ≡ {ps%P:>2} ({fw(ps)})")
    print(f"  Cycle: starts and ends at {TESLA_FLOW} = TESLA_FLOW")
    print()
    print("GAPS: 7, 17, 32, 18")
    print(f"  Sum = 74 = 2×37 ≡ 0 = SEAM")
    print(f"  7+17 = 24 ∈ CB∩SEED;   32+18 ≡ 13 ∈ CB")
    print(f"  Ghost increments 7+18 = 25 ∈ SA")
    print(f"  Cross-pairs: 7+32≡2∈PR; 17+18=35∈PR")
    print()
    print(f"SUM of partial sums  = 191 ≡ 6 = TESLA_FLOW")
    print(f"PRODUCT of partial sums ≡ 18 ∈ SEED_ORBIT (= ∑Kervaire_dims mod 37 from T81)")
    print()
    print("FERMAT-SEAM IDENTITY:")
    print(f"  K(p) = 2^p − 2 ≡ 2 − 2 = 0 = SEAM (mod p)  [Fermat's little theorem]")
    print(f"  For p=37: K(37) ≡ {K_mod(37)} = SEAM.  First occurrence at j = {_first_seam} = THE PRIME")
    print()
    print("K(j) mod 37 framework hits (j=2..37):")
    for j in range(2, 38):
        k = K_mod(j)
        name = fw(k)
        if k == 0 or name != '—':
            print(f"  j={j:>2}: K ≡ {k:>2}  ({name})")
    print()
    print("All assertions pass.")

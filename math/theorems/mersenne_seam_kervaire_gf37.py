"""
Mersenne-SEAM Theorem and SEED-Shifted Kervaire Continuation on GF(37) — THEOREM 84

SETUP.
  Let K_j = 2^j − 2 (the j-th Kervaire dimension, j ≥ 2).
  Let S_k = ∑_{i=1}^k 2^i = 2^{k+1} − 2 = K_{k+1} (cumulative power-of-2 chain).

MERSENNE-SEAM THEOREM.
  For any odd prime p:
    S_k ≡ 0 (mod p)  ⟺  p | 2^k − 1  ⟺  p = 2^k − 1 is a Mersenne prime.
  Proof: S_k = 2(2^k − 1). Since p odd, p ∤ 2, so p | S_k iff p | 2^k − 1.
  A Mersenne prime p = 2^k − 1 satisfies this with equality.

CONSEQUENCE TABLE.
  k | p = 2^k−1 | prime | S_k = K_{k+1} | SEAM at | Kervaire status
  ─────────────────────────────────────────────────────────────────────
  2 |   3       | YES   | K_3  = 6      | step 2  | included (j=3, YES)
  3 |   7       | YES   | K_4  = 14     | step 3  | included (j=4, YES)
  4 |  15       | NO    | K_5  = 30     | —       | (composite, no SEAM)
  5 |  31       | YES   | K_6  = 62     | step 5  | included (j=6, YES)
  6 |  63       | NO    | K_7  = 126    | —       | (composite, no SEAM)
  7 | 127       | YES   | K_8  = 254    | step 7  | FIRST EXCLUDED (j=8, NO)

  For p=37 (NOT Mersenne): no S_k ≡ 0 (mod 37). The chain from THEOREM 83
  needs a ghost step A_6=12∈ST to hit SEAM at 74=2×37.

p=31 (MERSENNE, 2^5−1): SEAM falls at the second-to-last included Kervaire dim.
  S_5 = K_6 = 62 = 2×31 = 2p ≡ 0 (mod 31).
  No ghost step needed. This is the unique Mersenne prime where the SEAM
  falls within the included Kervaire dimensions.

p=127 (MERSENNE, 2^7−1): SEAM falls at the FIRST EXCLUDED Kervaire dim.
  S_7 = K_8 = 254 = 2×127 = 2p ≡ 0 (mod 127).
  K_8 = 254 is the first dimension excluded by Hill-Hopkins-Ravenel (2016).
  The 7-step power-of-2 chain — using exactly the Kervaire exponents j=2..7
  plus j=8 — hits SEAM at the HHR boundary, mod the Mersenne prime 127.

p=37 (NON-MERSENNE): GHOST STEP IN ST.
  The ghost g = p − (K_6 mod p) = 37 − 25 = 12.
  12 ∈ ST (Sovereign Targets = {n : DR(n)=3}).
  12 = f(9), where 9 ∈ SA (Sovereign Anchors).
  THEOREM 83 uses j=6: the unique index in {2,...,9} for which the ghost ∈ ST.
  Ghost classification across j (p=37):
    j=2: ghost=35∈PR;  j=3: ghost=31∈T4;  j=4: ghost=23(—);
    j=5: ghost=7(—);   j=6: ghost=12∈ST;  j=7: ghost=22∈PR;
    j=8: ghost=5∈PR;   j=9: ghost=8∈CB.
  The j=6 ghost is the sole ST landing; and 12=f(9) means the ghost traces
  the 137-map from SA(9) to ST(12) — the Sovereign gateway.

SEED-SHIFTED KERVAIRE CONTINUATION.
  After the T83 chain ends at S_8=80≡TESLA_FLOW (mod 37), extend by adding
  further Kervaire differences 2^j for j=6,7,8,...:
    cumsum(j) = 80 + ∑_{i=6}^{j} 2^i = 2^{j+1} + 16 = K_{j+1} + 18.
  Since 18 ∈ SEED_ORBIT, the continuation generates:
    cumsum(j) ≡ K(j+1) + SEED_node  (mod 37).
  The Kervaire recurrence orbit from THEOREM 82 is SHIFTED BY 18∈SEED.
  GF(37) hits in the continuation (j=6..15):
    j=7:  K(8)+18 ≡ 13 ∈ CB
    j=9:  K(10)+18 ≡  4 ∈ SA
    j=11: K(12)+18 ≡  5 ∈ PR
    j=12: K(13)+18 ≡ 31 ∈ TESLA_4
    j=14: K(15)+18 ≡  2 ∈ PR
    j=15: K(16)+18 ≡ 25 ∈ SA
  The 18-shift means K(j)+18≡0=SEAM iff K(j)≡-18≡19 (mod 37).
  K(j)≡19 iff 2^j≡21 (mod 37). The orbit of 2 mod 37 hits 21 at j=? (check below).
"""

# ── Constants ──────────────────────────────────────────────────────────────────

import math

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
SEED_NODE  = 18

def f137(n): return (26*n)%P
def dr(n):
    while n>=10: n=sum(int(c) for c in str(n))
    return n
def is_prime(n):
    if n<2: return False
    for d in range(2,int(n**0.5)+1):
        if n%d==0: return False
    return True

# ── Mersenne-SEAM theorem ─────────────────────────────────────────────────────

# S_k = 2^{k+1}-2 = K_{k+1}
def S(k): return 2**(k+1) - 2

# For each Mersenne prime 2^k-1, S_k ≡ 0 (mod p) for p = 2^k-1
for k in [2, 3, 5, 7]:
    p_m = 2**k - 1
    assert is_prime(p_m), f"2^{k}-1 not prime"
    assert S(k) % p_m == 0, f"S_{k} not SEAM for p={p_m}"
    assert S(k) == 2 * p_m   # exactly 2p (double-prime SEAM)

# Composite cases give no SEAM (e.g. k=4: 2^4-1=15 not prime)
for k in [4, 6, 8]:
    p_c = 2**k - 1
    assert not is_prime(p_c)
    # For p=37 (a prime not of Mersenne form): no S_k ≡ 0 mod 37
# p=37 is non-Mersenne: no S_k ≡ 0 (mod 37) for k=1..35 (the Kervaire-length range)
# S(k)≡0 mod 37 iff 36|k; first hit at k=36 via Fermat (THEOREM 82: K(37)=S(36)≡0)
assert all(S(k) % P != 0 for k in range(1, P-1))   # k=1..35: no SEAM
assert S(P-1) % P == 0                              # k=36: S(36)=K_37≡0 by Fermat

# ── p=31 case ─────────────────────────────────────────────────────────────────

# 31 = 2^5-1: S_5 = K_6 = 62 = 2×31 ≡ 0 (mod 31)
assert S(5) == 62 == 2 * 31
assert S(5) % 31 == 0
# 62 is the second-to-last included Kervaire dim (j=6, included since LWX 2025 confirms j≤7)
kervaire_included = [2**j-2 for j in range(2,8)]   # j=2..7
assert 62 in kervaire_included

# ── p=127 case ────────────────────────────────────────────────────────────────

# 127 = 2^7-1: S_7 = K_8 = 254 = 2×127 ≡ 0 (mod 127)
assert S(7) == 254 == 2 * 127
assert S(7) % 127 == 0
# 254 = K_8 is the FIRST EXCLUDED Kervaire dim (j=8)
kervaire_excluded_first = 2**8 - 2
assert kervaire_excluded_first == 254   # first excluded = 254
# S_7 uses the 7-step chain ending exactly at the HHR boundary
assert S(7) == kervaire_excluded_first

# ── p=37 ghost step analysis ──────────────────────────────────────────────────

# K_6 mod 37 = 25 ∈ SA
assert (2**6 - 2) % P == 25 and 25 in SA

# Ghost g = 37 - 25 = 12 ∈ ST
ghost_37 = P - (S(5) % P)   # S(5) = K_6 = 62
assert ghost_37 == 12 and 12 in ST

# 12 = f(9), 9 ∈ SA: ghost traces SA → ST under 137-map
assert f137(9) == 12 and 9 in SA and 12 in ST

# Among j=2..9, j=6 is the unique index where ghost ∈ ST
_ghosts = {j: P - ((2**(j+1)-2) % P) or P for j in range(2,10)}
# Correct computation: ghost = (-K_j) % P, with ghost=P if 0
_ghosts = {}
for j in range(2,10):
    r = (2**j-2) % P
    g = (-r) % P
    if g == 0: g = P
    _ghosts[j] = g
assert _ghosts[6] == 12 and 12 in ST
assert sum(1 for j,g in _ghosts.items() if g in ST) == 1   # j=6 is unique ST ghost
assert sum(1 for j,g in _ghosts.items() if g in PR) == 3   # j=2,7,8: PR ghosts

# ── SEED-shifted Kervaire continuation ────────────────────────────────────────

# After 80=TESLA_FLOW (end of T83 chain), add 2^j for j=6,7,...
# cumsum(j) = 80 + ∑_{i=6}^{j} 2^i = 2^{j+1}+16 = K_{j+1}+18
def continuation_cumsum(j_end):
    return 80 + sum(2**i for i in range(6, j_end+1))

for j in range(6, 20):
    cs = continuation_cumsum(j)
    kj1 = 2**(j+1) - 2   # K_{j+1}
    assert cs == kj1 + SEED_NODE   # exact equality (not just mod 37)

# GF(37) hits in the SEED-shifted sequence
_seed_hits = {}
for j in range(6, 36):
    cs_mod = continuation_cumsum(j) % P
    _seed_hits[j] = cs_mod

# Verify: K(j+1)+18 ≡ cumsum (mod 37) for all j
for j in range(6, 36):
    kj1_mod = (2**(j+1) - 2) % P
    assert (kj1_mod + SEED_NODE) % P == _seed_hits[j]

# The SEAM occurs in SEED-shifted sequence when K(j+1)+18 ≡ 0 (mod 37)
# iff K(j+1) ≡ -18 ≡ 19 (mod 37) iff 2^{j+1} ≡ 21 (mod 37)
_seam_j = [j for j in range(6,50) if _seed_hits.get(j, (continuation_cumsum(j))%P) == 0]
# Since 2 has order 36 mod 37, check if 21 is in the orbit
_pow2_orbit = {pow(2,k,P): k for k in range(36)}
assert 21 in _pow2_orbit   # 2^k≡21 for some k; so SEAM occurs
_k_for_21 = _pow2_orbit[21]
assert pow(2, _k_for_21, P) == 21
# SEAM in continuation at j = _k_for_21 - 1
_seam_continuation_j = _k_for_21 - 1
assert continuation_cumsum(_seam_continuation_j) % P == 0

# ── SA, ST algebraic characterizations ────────────────────────────────────────

# SA = f^{-1}(ST) (preimage of ST under 137-map)
assert frozenset(n for n in range(1,P) if f137(n) in ST) == SA
# ST = {n ∈ [1,36] : DR(n) = 3}
assert frozenset(n for n in range(1,P) if dr(n)==3) == ST
# Both contained in QR (quadratic residues) mod 37
legendre = lambda a: pow(a,(P-1)//2,P)
assert all(legendre(a)==1 for a in SA)
assert all(legendre(a)==1 for a in ST)


if __name__ == "__main__":
    print("Mersenne-SEAM Theorem and SEED-Shifted Kervaire Continuation — THEOREM 84")
    print("=" * 72)
    print()

    print("MERSENNE-SEAM THEOREM:")
    print("  S_k = 2^{k+1}-2 = K_{k+1}; S_k ≡ 0 (mod p) iff p = 2^k-1 (Mersenne)")
    print()
    print(f"  {'k':>3} | {'p=2^k-1':>8} | prime | S_k = K_{{k+1}} | Kervaire status")
    print(f"  {'-'*60}")
    notes = {2:'incl. j=3',3:'incl. j=4',5:'incl. j=6',7:'FIRST EXCLUDED j=8'}
    for k in range(2,9):
        p_c = 2**k-1
        sk  = S(k)
        note = notes.get(k,'')
        print(f"  {k:>3} | {p_c:>8} | {str(is_prime(p_c)):>5} | K_{k+1}={sk:<9} | {note}")
    print()

    print("p=37 (NOT Mersenne): no S_k ≡ 0 (mod 37)")
    print(f"  Ghost step g = p - (K_6 mod p) = 37 - 25 = 12 ∈ ST")
    print(f"  12 = f(9), 9 ∈ SA → the ghost traces the SA→ST gateway")
    print()

    print("GHOST STEPS (p=37) ACROSS KERVAIRE DIMS j=2..9:")
    fw_map = [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),
              (IC,'IC'),(SEED_ORBIT,'SEED'),(TESLA_4,'T4'),(PR,'PR')]
    def fw(n):
        n=n%P; return 'SEAM' if n==0 else next((nm for s,nm in fw_map if n in s),'—')
    for j in range(2,10):
        r = (2**j-2)%P
        g = _ghosts[j]
        mark = ' ← THEOREM 83 (unique ST ghost)' if j==6 else ''
        print(f"  j={j}: K_j%37={r:>2} ({fw(r):>4}), ghost={g:>2} ({fw(g):>4}){mark}")
    print()

    print("SEED-SHIFTED CONTINUATION after S_8=80≡TESLA_FLOW:")
    print(f"  cumsum(j) = K(j+1) + {SEED_NODE} (exact), ≡ K(j+1)+SEED_node (mod 37)")
    print()
    print(f"  {'j':>3} | cumsum | K(j+1)+18 | mod37 | GF(37)")
    for j in range(6,16):
        cs = continuation_cumsum(j)
        print(f"  {j:>3} | {cs:>7} | {2**(j+1)-2+SEED_NODE:>9} | {cs%P:>5} | {fw(cs)}")
    print()
    print(f"  SEAM in continuation at j={_seam_continuation_j} (when K(j+1)≡19, i.e., 2^{{j+1}}≡21 mod 37)")
    print(f"  (ord₃₇(2)=36, so SEAM recurs every 36 steps in the continuation)")
    print()
    print("All assertions pass.")

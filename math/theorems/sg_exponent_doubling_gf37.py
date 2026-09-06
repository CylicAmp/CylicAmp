"""
Sophie Germain Exponent Doubling and Perfect Number Chain on GF(37) — THEOREM 86

USER INPUT TABLE.
  N₁ = 6    | exp=1 | chain: 2¹
  N₂ = 28   | exp=2 | chain: 2, 4, 2²
  N₃ = 496  | exp=4 | chain: 1, 2, 4, 8, 16, 2⁴
  N₄ = 8128 | exp=6 | chain: 1, 2, 4, 8, 16, 32, 64, 2⁶  [SG break]

THE EXPONENT DOUBLING.
  Perfect number N = 2^(p-1) × (2^p − 1).  The Sophie Germain triad (p=2,3,5)
  has p−1 ∈ {1, 2, 4} = {2⁰, 2¹, 2²} — the first three powers of 2.

  "4 at 3 and 1" → exponent 4 = 2² at N₃ (row 3), exponent 1 = 2⁰ at N₁ (row 1).

  p | p−1 | power of 2? | SG? | note
  ──────────────────────────────────────────────
  2 |  1  | 2⁰ = 1  ✓  | ✓   | exponent 1  (row 1)
  3 |  2  | 2¹ = 2  ✓  | ✓   | exponent 2  (row 2)
  5 |  4  | 2² = 4  ✓  | ✓   | exponent 4  (row 3)  ← "4 at 3"
  7 |  6  | 6 ≠ 2³  ✗  | ✗   | BREAK — exponent 6 = 2+4, not 8

  The SG condition and the power-of-2 exponent condition COINCIDE for p=2,3,5.
  At p=7: Sophie Germain fails (2×7+1=15 composite) AND p−1=6 is not a power of 2.
  The dual failure is simultaneous; both conditions break at the same prime.

DOUBLING CHAINS IN THE CHAIN TOP SEQUENCE.
  The chain tops 2^(p-1) for the SG perfect numbers form a doubling sequence:
    2¹ = 2  →  2² = 4  →  2⁴ = 16.
  The chain tops double: 2→4→16 (multiplying by 2, then by 4).
  Under the 137-map (mod 37): 2→4→16.
    2 ∈ PR, 4 ∈ SA, 16 ∈ — (unclassed).
  The SG break substitutes the actual 2^6=64≡27∈ORBIT_11 for the expected 2^8≡34.

CUMULATIVE CHAIN SUMS AS MERSENNE PRIMES.
  For each SG perfect number, the cumulative sum of the doubling chain 1+2+...+2^(p-1)
  is exactly the Mersenne prime factor:
    p=2: 1+2 = 3  (Mersenne prime 2²-1=3)
    p=3: 1+2+4 = 7  (Mersenne prime 2³-1=7)
    p=5: 1+2+4+8+16 = 31  (Mersenne prime 2⁵-1=31)
    p=7: 1+2+4+8+16+32+64 = 127  (Mersenne prime 2⁷-1=127)
  This is 2^p − 1 = ∑_{k=0}^{p-1} 2^k — the geometric series identity.

CHAIN SUM MOD 37.
  The cumulative sums (= Mersenne primes) in GF(37):
    3   mod 37 = 3  ∈ ST
    7   mod 37 = 7  ∈ —
    31  mod 37 = 31 ∈ T4
    127 mod 37 = 16 ∈ —  [first excluded Kervaire dimension — see THEOREM 84]
  The SG triad: ST, —, T4. The break prime 127 connects to the SEAM at K_8 (T84).

PARTIAL CHAIN SUMS MOD 37 FOR THE SG TRIAD.
  For N₃=496 (p=5), the doubling chain partial sums:
    S(0)=1, S(1)=3, S(2)=7, S(3)=15, S(4)=31.
  In GF(37): 1∈IC, 3∈ST, 7∈—, 15∈PR, 31∈T4.
  The final partial sum 31∈T4 is the Mersenne prime factor of 496.
  Path: IC → ST → — → PR → T4 (five steps, four named-set transitions).

CHAIN TOP MOD 37 SEQUENCE (2^(p-1) for p=2,3,5,7).
  p=2: 2^1  =  2 ∈ PR
  p=3: 2^2  =  4 ∈ SA
  p=5: 2^4  = 16 ∈ —
  p=7: 2^6  = 27 ∈ ORBIT_11  (the ORBIT_11 entry coincides with the SG break)

MISSING EXPONENT 8.
  The next power-of-2 exponent would be p−1=8 → p=9, composite. No Mersenne prime.
  2^8 mod 37 = 34 ∈ — (unclassed, same class as 2^4=16 and (2^7-1) mod 37=16).
  Gap between actual (2^6≡27) and expected (2^8≡34): 34−27=7∈— (same class as 2^3-1=7).
  The missing element 7 appears again as the unclassed Mersenne prime 7 (p=3 row).

OUTER SYMMETRY OF CHAIN TOPS.
  Chain tops for SG+1: [2, 4, 16, 27].
  Product mod 37: 2×4×16×27 = 3456 mod 37.
    3456 / 37 = 93.4..., 93×37=3441, 3456−3441=15.
    Product ≡ 15 ∈ PR — same as N₃=496 mod 37.
  Sum mod 37: (2+4+16+27)=49≡12∈ST.
  Chain top sum lands in ST — the same class as the Mersenne prime for p=2.
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
IC         = frozenset({1, 10, 26})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
P          = 37
SCALAR_137 = 26


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


def isprime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True


# ── Exponent doubling: p-1 is a power of 2 iff p ∈ {2,3,5} ──────────────────

sg_mersenne_p = [2, 3, 5]
break_p = 7
for p in sg_mersenne_p:
    e = p - 1
    assert (e & (e - 1)) == 0   # e is a power of 2
    assert isprime(2*p + 1)      # Sophie Germain condition

# At the break: p=7, p-1=6 is NOT a power of 2 and NOT Sophie Germain
assert (6 & 5) != 0              # 6 is not a power of 2
assert not isprime(2*7 + 1)      # 15 = 3×5 composite

# Exponents form 2^0, 2^1, 2^2
assert [p - 1 for p in sg_mersenne_p] == [1, 2, 4]
assert [2**k for k in range(3)] == [1, 2, 4]   # = [2^0, 2^1, 2^2]

# ── Doubling chains ────────────────────────────────────────────────────────────

# Chain for each p: [2^0, 2^1, ..., 2^(p-1)]
chains = {p: [2**k for k in range(p)] for p in [2, 3, 5, 7]}

# Chain for p=2: [1, 2] — top is 2^1=2
assert chains[2] == [1, 2] and chains[2][-1] == 2

# Chain for p=3: [1, 2, 4] — top is 2^2=4
assert chains[3] == [1, 2, 4] and chains[3][-1] == 4

# Chain for p=5: [1, 2, 4, 8, 16] — top is 2^4=16
assert chains[5] == [1, 2, 4, 8, 16] and chains[5][-1] == 16

# Chain for p=7: [1, 2, 4, 8, 16, 32, 64] — top is 2^6=64
assert chains[7] == [1, 2, 4, 8, 16, 32, 64] and chains[7][-1] == 64

# ── Cumulative chain sums = Mersenne primes ────────────────────────────────────

for p in [2, 3, 5, 7]:
    mersenne = 2**p - 1
    assert sum(chains[p]) == mersenne           # geometric series identity
    assert isprime(mersenne)                     # Mersenne prime

# ── Chain sum (= Mersenne prime) mod 37 ──────────────────────────────────────

mersenne_mod37 = {p: (2**p - 1) % P for p in [2, 3, 5, 7]}
assert mersenne_mod37[2] == 3  and 3  in ST        # p=2: ST
assert mersenne_mod37[3] == 7  and 7  not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR  # —
assert mersenne_mod37[5] == 31 and 31 in TESLA_4   # p=5: T4
assert mersenne_mod37[7] == 16 and 16 not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR  # — (HHR)

# ── Chain tops mod 37 ─────────────────────────────────────────────────────────

tops_mod37 = {p: pow(2, p-1, P) for p in [2, 3, 5, 7]}
assert tops_mod37[2] == 2  and 2  in PR           # p=2: PR
assert tops_mod37[3] == 4  and 4  in SA           # p=3: SA
assert tops_mod37[5] == 16 and 16 not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR  # —
assert tops_mod37[7] == 27 and 27 in ORBIT_11     # p=7: ORBIT_11 (SG break)

# ── Partial chain sums for N₃=496 ────────────────────────────────────────────

# Partial sums: 1, 3, 7, 15, 31 (chain for p=5)
partials_p5 = []
s = 0
for x in chains[5]:
    s += x
    partials_p5.append(s)
assert partials_p5 == [1, 3, 7, 15, 31]

# In GF(37): 1∈IC, 3∈ST, 7∉fw, 15∈PR, 31∈T4
assert partials_p5[0] % P == 1  and 1  in IC
assert partials_p5[1] % P == 3  and 3  in ST
assert partials_p5[2] % P == 7  and 7  not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR
assert partials_p5[3] % P == 15 and 15 in PR
assert partials_p5[4] % P == 31 and 31 in TESLA_4

# ── Missing exponent: p-1=8 (expected 2^3) ───────────────────────────────────

# p=9 is composite → no Mersenne prime at the expected power-of-2 exponent
assert not isprime(9)

# 2^8 mod 37 (expected chain top) vs 2^6 mod 37 (actual for p=7)
expected_top = pow(2, 8, P)   # 34 — unclassed
actual_top   = pow(2, 6, P)   # 27 ∈ ORBIT_11

assert expected_top == 34 and 34 not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR
assert actual_top   == 27 and 27 in ORBIT_11

# Gap between expected and actual chain tops
gap = (expected_top - actual_top) % P
assert gap == 7 and 7 not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR  # same class as M(p=3)=7

# ── Product and sum of all four chain tops ────────────────────────────────────

all_tops = [tops_mod37[p] for p in [2, 3, 5, 7]]   # [2, 4, 16, 27]
assert all_tops == [2, 4, 16, 27]

prod_tops = 1
for t in all_tops:
    prod_tops = prod_tops * t % P
assert prod_tops == 15 and 15 in PR           # product ≡ 15 = N₃ mod 37 ∈ PR

sum_tops = sum(all_tops) % P
assert sum_tops == 49 % P == 12 and 12 in ST  # sum ≡ 12 ∈ ST


if __name__ == "__main__":
    print("Sophie Germain Exponent Doubling and Perfect Number Chain on GF(37) — THEOREM 86")
    print("=" * 80)
    print()
    print("EXPONENT DOUBLING:")
    print(f"  p=2: p-1=1=2⁰  SG ✓  2^(p-1) mod 37 = {tops_mod37[2]} ∈ PR")
    print(f"  p=3: p-1=2=2¹  SG ✓  2^(p-1) mod 37 = {tops_mod37[3]} ∈ SA")
    print(f"  p=5: p-1=4=2²  SG ✓  2^(p-1) mod 37 = {tops_mod37[5]} ∈ —  ← '4 at 3'")
    print(f"  p=7: p-1=6≠2³  SG ✗  2^(p-1) mod 37 = {tops_mod37[7]} ∈ O11 [SG break]")
    print()
    print("'4 at 3 and 1': exponent 4=2² at row 3 (N₃=496=2⁴×31), exponent 1=2⁰ at row 1 (N₁=6=2¹×3)")
    print()

    fw_map = [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),
              (IC,'IC'),(SEED_ORBIT,'SEED'),(TESLA_4,'T4'),(PR,'PR')]
    def fw(n):
        n = n % P
        if n == 0: return 'SEAM'
        for s, nm in fw_map:
            if n in s: return nm
        return '—'

    print("DOUBLING CHAINS:")
    for p in [2, 3, 5, 7]:
        chain = chains[p]
        M = 2**p - 1
        chain_tops_37 = [pow(2,k,P) for k in range(p)]
        sg = '✓' if isprime(2*p+1) else '✗'
        print(f"  p={p}: chain {chain} → sum={M}∈Mersenne; top 2^{p-1}={2**(p-1)}≡{pow(2,p-1,P)}∈{fw(pow(2,p-1,P))}  SG{sg}")
    print()

    print("PARTIAL CHAIN SUMS (p=5, N₃=496):")
    s = 0
    for i, x in enumerate(chains[5]):
        s += x
        print(f"  2^{i}={x:>3}: cumsum={s:>3} ≡ {s%P:>3} ∈ {fw(s)}")
    print(f"  Final sum = 31∈T4 = Mersenne prime factor of 496  ✓")
    print()

    print(f"MISSING EXPONENT: expected p-1=2³=8 → p=9 (composite, no Mersenne)")
    print(f"  2^8 mod 37 = {expected_top} ∈ — (expected chain top, never reached)")
    print(f"  2^6 mod 37 = {actual_top} ∈ O11 (actual p=7 chain top; gap={gap}∈— same class as M_3=7)")
    print()

    print(f"CHAIN TOPS [2,4,16,27] mod 37:")
    print(f"  Sum   = {sum(all_tops)} ≡ {sum(all_tops)%P} ∈ ST  (same class as M_2=3)")
    print(f"  Product = {2*4*16*27} ≡ {prod_tops} ∈ PR = N₃ mod 37")
    print()
    print("All assertions pass.")

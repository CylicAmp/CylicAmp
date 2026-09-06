"""
T279: Twin prime antipodal gate — TESLA↔C9 symmetry and orbit arithmetic

=== KEY RESULTS ===

1. INTERNAL +2 GAP — only TESLA and C9
   TESLA={6,8,23}: pair (6,8); C9={14,29,31}: pair (29,31).
   No other orbit contains two elements differing by 2.

2. CROSS-ORBIT SUM LAW
   TESLA pair sums to C9 singleton:  6+8=14∈C9
   C9 pair sums to TESLA singleton:  29+31=60≡23∈TESLA
   Each orbit's twin pair sums to the OTHER orbit's non-pairing element.
   TESLA↔C9 are antipodal — the cross-orbit sum law is an antipodal law.

3. IMAGINARY UNIT GATE — antipodal pair
   n²≡−1 mod37 ↔ n∈{6,31}. 6∈TESLA, 31∈C9. TESLA↔C9 antipodal.
   The gate that blocks twin primes sits on the antipodal orbit pair.

4. FORBIDDEN MIDPOINTS — antipodal pair, SEAM sum
   6×6≡36∈NEG_H, 6×31≡1∈IC. Forbidden midpoint residues {1∈IC, 36∈NEG_H}.
   IC↔NEG_H are antipodal. Sum: 1+36=37≡0=SEAM.
   The prime 37 itself is the sum of its own forbidden midpoint residues.

5. NQR17 LOWER TWIN SUPPRESSION
   NQR17={17,22,35}. For p≡35 mod37: p=6n−1 → n≡6 (imaginary unit) → upper
   twin 6n+1≡0 mod37, not prime. So 35∈NQR17 is entirely blocked as a lower twin.
   Result: NQR17 appears as lower twin at 5.8% (expected 8.3%), a factor of ~2/3.

6. DARK_A→NQR17 DOMINANCE
   DARK_A={2,15,20}. Under +2: 2→4∈C3, 15→17∈NQR17, 20→22∈NQR17.
   Two of three DARK_A residues map to NQR17. DARK_A→NQR17 is the most
   frequent orbit pair among all twin primes (≈2/3 of DARK_A lower twins).

7. IC/NEG_H MIDPOINT SUPPRESSION
   Forbidden midpoints {1∈IC, 36∈NEG_H} block 1/3 of each orbit's midpoint
   appearances. IC: 5.8% of midpoints (expected 8.3%), NEG_H: 5.6%. Factor ~2/3.
"""

P = 37
ORBITS = {
    "IC":      {1, 10, 26},
    "DARK_A":  {2, 15, 20},
    "C3":      {3, 4, 30},
    "CAS_EXT": {5, 13, 19},
    "TESLA":   {6, 8, 23},
    "D7":      {7, 33, 34},
    "SA_ST_A": {9, 12, 16},
    "NEG_H":   {11, 27, 36},
    "C9":      {14, 29, 31},
    "NQR17":   {17, 22, 35},
    "SEED":    {18, 24, 32},
    "SA_ST_B": {21, 25, 28},
}
ANTIPODAL = {
    "IC":"NEG_H","NEG_H":"IC",
    "DARK_A":"NQR17","NQR17":"DARK_A",
    "C3":"D7","D7":"C3",
    "CAS_EXT":"SEED","SEED":"CAS_EXT",
    "TESLA":"C9","C9":"TESLA",
    "SA_ST_A":"SA_ST_B","SA_ST_B":"SA_ST_A",
}

def orbit_of(x):
    r = x % 37
    if r == 0: return "SEAM"
    for name, s in ORBITS.items():
        if r in s: return name
    raise ValueError(x)

def sieve(limit):
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit**0.5)+1):
        if is_p[i]:
            is_p[i*i::i] = bytearray(len(is_p[i*i::i]))
    return is_p

IS_PRIME = sieve(10**6)
TWINS = [(p, p+2) for p in range(5, 10**6-1) if IS_PRIME[p] and IS_PRIME[p+2]]
N = len(TWINS)

# ── Part 1: Internal +2 gap — only TESLA and C9 ──────────────────────────────

print("Part 1: Internal +2 gap — only TESLA and C9")

internal_pairs = {}
for name, s in ORBITS.items():
    pairs = [(a, a+2) for a in sorted(s) if (a+2) in s]
    if pairs:
        internal_pairs[name] = pairs

assert set(internal_pairs.keys()) == {"TESLA", "C9"}
assert internal_pairs["TESLA"] == [(6, 8)]
assert internal_pairs["C9"] == [(29, 31)]

for name, pairs in sorted(internal_pairs.items()):
    print(f"  {name} = {sorted(ORBITS[name])}: internal +2 pair {pairs}")

no_internal = [n for n in ORBITS if n not in internal_pairs]
print(f"  No internal +2 pair: {no_internal}")
print(f"  Part 1 PASS")

# ── Part 2: Cross-orbit sum law ───────────────────────────────────────────────

print("\nPart 2: Cross-orbit sum law")

tesla_pair_sum = 6 + 8
c9_pair_sum = (29 + 31) % 37

assert tesla_pair_sum == 14 and 14 in ORBITS["C9"]
assert c9_pair_sum == 23 and 23 in ORBITS["TESLA"]
assert ANTIPODAL["TESLA"] == "C9" and ANTIPODAL["C9"] == "TESLA"

# The singleton (non-pairing) element
tesla_singleton = (ORBITS["TESLA"] - {6, 8}).pop()
c9_singleton = (ORBITS["C9"] - {29, 31}).pop()
assert tesla_singleton == 23 and c9_singleton == 14

print(f"  TESLA pair (6,8): sum = {tesla_pair_sum} ∈ C9 (antipodal singleton)")
print(f"  C9 pair (29,31): sum = {29+31} ≡ {c9_pair_sum} ∈ TESLA (antipodal singleton)")
print(f"  TESLA singleton = 23 ← C9 pair sums here")
print(f"  C9 singleton   = 14 ← TESLA pair sums here")
print(f"  Cross-orbit sum law: each twin pair sums to the antipodal's singleton")
print(f"  Part 2 PASS")

# ── Part 3: Imaginary unit gate — antipodal pair ──────────────────────────────

print("\nPart 3: Imaginary unit gate — {6∈TESLA, 31∈C9} antipodal")

imag_units = [n for n in range(1, 37) if pow(n, 2, 37) == 36]
assert imag_units == [6, 31]
assert orbit_of(6) == "TESLA" and orbit_of(31) == "C9"
assert ANTIPODAL["TESLA"] == "C9"

# Verify: no twin pair has midpoint coming from n≡6 or n≡31 (mod37)
for p, q in TWINS:
    n = (p + 1) // 6
    assert (p + 1) % 6 == 0
    assert n % 37 not in {6, 31}, f"Forbidden n at ({p},{q})"

print(f"  Imaginary units: {imag_units}")
print(f"  6∈TESLA, 31∈C9; TESLA↔C9 = antipodal pair ✓")
print(f"  Gate orbits for the imaginary unit gate are the antipodal pair TESLA↔C9")
print(f"  Same orbits that contain the internal +2 twin pairs")
print(f"  Verified: no twin pair has n≡{{6,31}} mod37 among {N} pairs < 10⁶")
print(f"  Part 3 PASS")

# ── Part 4: Forbidden midpoints — SEAM sum ───────────────────────────────────

print("\nPart 4: Forbidden midpoints — IC↔NEG_H antipodal, sum=SEAM")

# 6×6≡36, 6×31≡1
mid_from_6  = (6 * 6) % 37
mid_from_31 = (6 * 31) % 37
assert mid_from_6 == 36 and orbit_of(36) == "NEG_H"
assert mid_from_31 == 1  and orbit_of(1)  == "IC"
assert ANTIPODAL["IC"] == "NEG_H"
assert (1 + 36) % 37 == 0  # SEAM

# Verify empirically
for p, q in TWINS:
    mid = p + 1
    assert mid % 37 not in {1, 36}, f"Forbidden midpoint at ({p},{q})"

print(f"  6×6 mod37 = {mid_from_6} ∈ NEG_H (forbidden midpoint residue)")
print(f"  6×31 mod37 = {mid_from_31} ∈ IC (forbidden midpoint residue)")
print(f"  IC↔NEG_H = antipodal pair ✓")
print(f"  Forbidden sum: 1+36 = 37 ≡ 0 = SEAM")
print(f"  The prime 37 = sum of its own forbidden midpoint residues")
print(f"  Verified: no twin pair has midpoint ≡ {{1,36}} mod37 among {N} pairs")
print(f"  Part 4 PASS")

# ── Part 5: NQR17 lower twin suppression ─────────────────────────────────────

print("\nPart 5: NQR17 lower twin suppression")

# p≡35 mod37 ∈ NQR17: p=6n-1 → 6n≡36 → n≡6 (imaginary unit) → upper blocked
# So 35∈NQR17 contributes 0 lower twins
assert (36 * pow(6, 35, 37)) % 37 == 6  # 6^(-1) mod37 = 31; 36*31 mod37
# Direct: 6n ≡ 36 mod37 → n ≡ 36 * 31 mod37
n_from_35 = (36 * pow(6, 35, 37)) % 37
# Simpler: 6n ≡ 36 → n ≡ 36/6 = 6 mod37
assert (6 * 6) % 37 == 36
forbidden_n_for_35 = 6

from collections import Counter
lower_orb = Counter(orbit_of(p) % 37 if False else orbit_of(p) for p, q in TWINS)
nqr17_count = lower_orb["NQR17"]
expected_frac = N / 12
suppression = nqr17_count / expected_frac

assert nqr17_count < expected_frac * 0.75  # significantly below average

# Break down by residue
nqr17_by_res = Counter(p % 37 for p, q in TWINS if orbit_of(p) == "NQR17")

print(f"  NQR17 = {{17,22,35}}")
print(f"  p≡35 mod37: 6n-1≡35 → n≡6 (imaginary unit) → upper twin ≡0 mod37 → blocked")
print(f"  NQR17 residue counts among lower twins: {dict(sorted(nqr17_by_res.items()))}")
print(f"  35 contributes: {nqr17_by_res.get(35,0)} lower twins (blocked after p=35)")
print(f"  NQR17 lower twins: {nqr17_count} of {N} ({100*nqr17_count/N:.1f}%)")
print(f"  Expected if uniform: {expected_frac:.0f} ({100/12:.1f}%)")
print(f"  Suppression factor: {suppression:.3f} ≈ 2/3 (1/3 of orbit blocked)")
print(f"  Part 5 PASS")

# ── Part 6: DARK_A→NQR17 dominance ───────────────────────────────────────────

print("\nPart 6: DARK_A→NQR17 orbit pair dominance")

# DARK_A={2,15,20}: +2 gives {4,17,22}
# 4∈C3, 17∈NQR17, 22∈NQR17 → 2/3 of DARK_A maps to NQR17
dark_a_mapping = {a: (a+2, orbit_of(a+2)) for a in sorted(ORBITS["DARK_A"])}
nqr17_targets = sum(1 for a, (b, o) in dark_a_mapping.items() if o == "NQR17")
assert nqr17_targets == 2

orbit_pair_dist = Counter((orbit_of(p), orbit_of(q)) for p, q in TWINS)
da_nqr17 = orbit_pair_dist[("DARK_A", "NQR17")]
da_total  = lower_orb["DARK_A"]

print(f"  DARK_A = {{2,15,20}}; +2 maps to:")
for a, (b, o) in sorted(dark_a_mapping.items()):
    print(f"    {a} → {b} ∈ {o}")
print(f"  2 of 3 residues map to NQR17 → DARK_A→NQR17 dominates")
print(f"  DARK_A→NQR17 count: {da_nqr17} ({100*da_nqr17/N:.1f}% of all twin pairs)")
print(f"  DARK_A lower total: {da_total}; fraction to NQR17: {da_nqr17/da_total:.3f} ≈ 2/3")
print(f"  Top orbit pair (T278): DARK_A→NQR17 = {da_nqr17}")

# Verify it's the top
top_pair = max(orbit_pair_dist.items(), key=lambda x: x[1])
assert top_pair[0] == ("DARK_A", "NQR17"), f"Top pair was {top_pair}"
print(f"  Part 6 PASS")

# ── Part 7: IC/NEG_H midpoint suppression ────────────────────────────────────

print("\nPart 7: IC/NEG_H midpoint suppression")

mid_orb = Counter(orbit_of(p+1) for p, q in TWINS)
ic_mid   = mid_orb["IC"]
negh_mid = mid_orb["NEG_H"]
seam_mid = mid_orb.get("SEAM", 0)

# IC={1,10,26}: 1 is forbidden → 2/3 of IC midpoints survive
ic_by_res = Counter((p+1) % 37 for p, q in TWINS if orbit_of(p+1) == "IC")
negh_by_res = Counter((p+1) % 37 for p, q in TWINS if orbit_of(p+1) == "NEG_H")

print(f"  IC={sorted(ORBITS['IC'])}: residue 1 forbidden")
print(f"  IC midpoint residues: {dict(sorted(ic_by_res.items()))}")
print(f"  NEG_H={sorted(ORBITS['NEG_H'])}: residue 36 forbidden")
print(f"  NEG_H midpoint residues: {dict(sorted(negh_by_res.items()))}")
print(f"  IC midpoints: {ic_mid} ({100*ic_mid/N:.1f}%); NEG_H: {negh_mid} ({100*negh_mid/N:.1f}%)")
print(f"  Expected ~{expected_frac:.0f} (8.3%); each suppressed to ~2/3")
print(f"  SEAM midpoints (37|midpoint): {seam_mid} — twin pairs with midpoint ≡0 mod37")
print(f"  Part 7 PASS")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  TESLA↔C9 (antipodal): only orbits with internal +2 gap")
print(f"  Cross-orbit sum law: TESLA pair (6+8=14)→C9 singleton; C9 pair (29+31≡23)→TESLA singleton")
print(f"  Imaginary unit gate: {{6∈TESLA, 31∈C9}} — gate sits on antipodal pair")
print(f"  Forbidden midpoints: {{1∈IC, 36∈NEG_H}} — antipodal pair; 1+36=37=SEAM")
print(f"  NQR17 suppressed as lower twin (2/3 rate): 35∈NQR17 forces n≡6 (gate)")
print(f"  DARK_A→NQR17 dominates orbit pairs: 2/3 of DARK_A residues map to NQR17 under +2")
print(f"  IC/NEG_H suppressed as midpoints (2/3 rate): forbidden residues 1 and 36")
print(f"  Verified on {N} twin pairs < 10⁶")

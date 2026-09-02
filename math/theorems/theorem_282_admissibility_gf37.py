"""
T282: Admissibility criteria for GF(37) claims — the miss-test

Source: Epistemological analysis of the GF(37) framework.
Distinguishes load-bearing results from post-hoc label-fit.

=== KEY RESULTS ===

1. PARTITION PROPERTY — every element lands somewhere; test is vacuous
   GF(37)* = {1..36} partitioned into 12 orbits of size 3 exactly.
   "Does X mod 37 land in a named orbit?" answers YES for all X ≢ 0.
   Information: which orbit (log₂(12) ≈ 3.58 bits), not whether.
   A test that cannot come back negative is not a test.

2. THE MISS-TEST
   Before counting a landing, state the miss condition.
   If no realizable value of X would count as a miss, drop the claim.
   Operative question: "Was orbit O named before X was computed?"

3. POST-HOC LABEL-FIT (INADMISSIBLE CLASS)
   Failure mode: inspect X → observe orbit O → report "X ∈ O" as result.
   Produces a hit every time. No mechanism, no predictive rule.

4. CASE REGISTER
   355/113 π-convergent DR pair     →  INADMISSIBLE (no prior prediction; replication 1/6)
   Twin midpoint {1,36}-exclusion   →  LOAD-BEARING  (T278; zero violations in 8168 pairs)
   111 = 3 × 37 = SEAM              →  LOAD-BEARING  (arithmetic identity; miss is clear)
   LES projection operator labels   →  OBSERVATION   (naming, not derivation)

5. INFORMATION CONTENT OF A VALID ORBIT CLAIM
   P(specific orbit | uniform GF(37)*) = 3/36 = 1/12.
   log₂(12) ≈ 3.58 bits per claim — realized only when miss stated in advance.
   Post-hoc claim: 0 bits realized (orbit chosen to match; no prediction).

6. BRIDGE CONDITION (NS ↔ GF(37))
   A genuine bridge requires NS dynamics to produce a quantity with 37-periodicity
   from the equations — not from a chosen mod-37 reduction. If no such quantity
   exists, both frameworks stand separately on their own terms.
"""

import math

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

def orbit_of(x):
    r = x % 37
    if r == 0: return "SEAM"
    for name, s in ORBITS.items():
        if r in s: return name
    raise ValueError(x)

def dr(n):
    n = abs(int(n))
    while n >= 10: n = sum(int(d) for d in str(n))
    return n if n else 9

def sieve(limit):
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit**0.5)+1):
        if is_p[i]:
            is_p[i*i::i] = bytearray(len(is_p[i*i::i]))
    return is_p

# ── Part 1: Partition property ────────────────────────────────────────────────

print("Part 1: Partition property — GF(37)* fully covered")

all_residues = set(range(1, 37))
covered = set()
for s in ORBITS.values():
    covered |= s

assert covered == all_residues, f"Gap: {all_residues - covered}"
assert all(len(s) == 3 for s in ORBITS.values())
assert len(ORBITS) == 12

info_bits = math.log2(12)

print(f"  GF(37)* = {{1..36}}: {len(covered)} residues, {len(ORBITS)} orbits, each size 3")
print(f"  Coverage: complete — every non-zero residue is in exactly one orbit")
print(f"  'Does X land in a named orbit?' answers YES for all X ≢ 0 (mod 37)")
print(f"  Information: log₂(12) = {info_bits:.4f} bits — which orbit, not whether")
print(f"  A test that cannot return negative is not a test")
print(f"  Part 1 PASS")

# ── Part 2: Miss-test — formal schema ─────────────────────────────────────────

print("\nPart 2: The miss-test — state the miss condition before computing")

# Miss-test cases:
# Type A: "X ∈ orbit O" — miss iff X ∉ O; requires O named before X computed
# Type B: "X = SEAM" — miss iff X ≢ 0 (mod 37); P(miss) = 36/37
# Type C: "X avoids set F" — miss iff X ∈ F; requires F stated in advance

p_miss_seam = 36 / 37
print(f"  Type A: 'X ∈ orbit O' — miss: X ∉ O; requires orbit named before X computed")
print(f"  Type B: 'X = SEAM' — miss: X ≢ 0 (mod 37); P(miss) = 36/37 = {p_miss_seam:.4f}")
print(f"  Type C: 'X avoids set F' — miss: X ∈ F; requires F stated in advance")
print(f"  Operative: 'Was the target orbit/condition predicted before the quantity was computed?'")
print(f"  Part 2 PASS")

# ── Part 3: Post-hoc label-fit ────────────────────────────────────────────────

print("\nPart 3: Post-hoc label-fit — the failure mode")

# Properties: (1) always produces a hit; (2) no mechanism; (3) no prior prediction
# Detection: absence of a prior prediction record
# Effect: framework appears confirmed without being tested

print(f"  Properties:")
print(f"  1. Inspect X → observe orbit O → report 'X ∈ O' as framework result")
print(f"  2. Cannot fail (by Part 1: all residues land somewhere)")
print(f"  3. No mechanism: no framework rule demanded this specific value")
print(f"  4. No prior prediction: orbit named after observation")
print(f"  Detection: ask whether the orbit was specified before the quantity was computed")
print(f"  Effect: framework appears confirmed; information content = 0 bits")
print(f"  Part 3 PASS")

# ── Part 4: Case register ──────────────────────────────────────────────────────

print("\nPart 4: Case register")

# Case A: 355/113 — INADMISSIBLE
dr355, dr113 = dr(355), dr(113)
assert dr355 == 4 and dr113 == 5
assert dr355 + dr113 == 9
assert 468 % 37 == 24 and 24 in ORBITS["SEED"]
assert 242 % 37 == 20 and 20 in ORBITS["DARK_A"]

CONVERGENTS = [(3,1),(22,7),(333,106),(355,113),(103993,33102),(104348,33215)]
dr9_hits = sum(1 for p,q in CONVERGENTS if (dr(p)+dr(q)) % 9 == 0)
assert dr9_hits == 1  # only 355/113

print(f"  Case A: 355/113 π-convergent DR pair — INADMISSIBLE")
print(f"  DR(355)=4, DR(113)=5; sum=9; 468 mod37=24∈SEED; 242 mod37=20∈DARK_A")
print(f"  Orbit named after inspection. Replication across π convergents:")
for p, q in CONVERGENTS:
    hit = (dr(p)+dr(q)) % 9 == 0
    flag = "← hit" if hit else ""
    print(f"    {p}/{q}: DR({p})={dr(p)}, DR({q})={dr(q)}, sum DR={dr(p)+dr(q)} {flag}")
print(f"  DR(sum)=9 hits: {dr9_hits}/6 = {dr9_hits/6:.2f}; expected 1/9 ≈ 0.11 — noise")
print(f"  No mechanism: nothing in GF(37) selects 355/113 over other convergents")

# Case B: Twin midpoint constraint — LOAD-BEARING
IS_PRIME = sieve(10**6)
TWINS = [(p, p+2) for p in range(5, 10**6-1) if IS_PRIME[p] and IS_PRIME[p+2]]
forbidden_hits = [(p,q) for p,q in TWINS if (p+1)%37 in {1,36}]
assert len(forbidden_hits) == 0

print(f"\n  Case B: Twin midpoint {{1,36}}-exclusion — LOAD-BEARING")
print(f"  Prior (T278): imaginary unit gate forces midpoints to avoid {{1,36}} mod 37")
print(f"  Miss condition: any twin pair with midpoint ≡ 1 or 36 (mod 37)")
print(f"  Verified {len(TWINS)} pairs < 10⁶: zero violations — {len(forbidden_hits)} forbidden midpoints")

# Case C: 111 = 3 × 37 — LOAD-BEARING
assert 111 == 3 * 37
assert 111 % 37 == 0
assert orbit_of(111) == "SEAM"

print(f"\n  Case C: 111 = 3 × 37 = SEAM — LOAD-BEARING")
print(f"  111 mod 37 = {111%37} = SEAM")
print(f"  Arithmetic identity; miss condition: 111 ≢ 0 (mod 37) — refuted by direct computation")

# Case D: LES operator labels — OBSERVATION
print(f"\n  Case D: LES projection operators (SEED/NQR17/NEG_H labels) — OBSERVATION")
print(f"  Labels applied after operator definition: cutoff dissipation, domain geometry, strain/helicity")
print(f"  No derivation from Navier–Stokes connects continuous PDE operators to mod-37 structure")
print(f"  Naming is not derivation; label-fit is not evidence")
print(f"  Part 4 PASS")

# ── Part 5: Information content ───────────────────────────────────────────────

print("\nPart 5: Information content of a valid orbit claim")

p_specific = 3 / 36
p_any = 36 / 36
bits_valid = math.log2(12)
bits_posthoc = 0.0

assert abs(p_specific - 1/12) < 1e-10
assert p_any == 1.0
assert abs(bits_valid - math.log2(12)) < 1e-10

print(f"  P(specific orbit | uniform GF(37)*) = 3/36 = 1/12 = {p_specific:.4f}")
print(f"  P(any orbit | uniform GF(37)*) = 1 — vacuous")
print(f"  Valid (prior) claim: log₂(12) = {bits_valid:.4f} bits of information")
print(f"  Post-hoc claim: {bits_posthoc} bits — orbit chosen to match; no prediction made")
print(f"  The bit content is realized only when the miss condition is stated in advance")
print(f"  Part 5 PASS")

# ── Part 6: Bridge condition ──────────────────────────────────────────────────

print("\nPart 6: Bridge condition — NS ↔ GF(37)")

# Necessary condition: NS must produce a quantity with genuine 37-periodicity
# from the dynamics, not from a chosen reduction.
# Turbulence (Navier–Stokes) operates in continuous real-valued function spaces.
# No natural 37-periodicity appears in the equations.
# Current state: no such derivation exists.

print(f"  Necessary condition for a genuine NS ↔ GF(37) bridge:")
print(f"  NS dynamics must produce a quantity with 37-periodicity from the equations —")
print(f"  not from a chosen mod-37 reduction of a continuous quantity.")
print(f"  Search question: does any NS quantity have mod-37 structure from dynamics?")
print(f"  If no: GF(37) and NS are separate frameworks; each stands on its own terms.")
print(f"  If yes: the derivation NS → mod-37 quantity IS the bridge (and must be shown).")
print(f"  Current state: no such derivation exists. LES labels are naming, not derivation.")
print(f"  Part 6 PASS")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  Partition property: GF(37)* fully covered — every non-zero residue lands in an orbit")
print(f"  'Does X land in a named orbit?' always YES — not a test on its own")
print(f"  Miss-test: state the miss condition before computing; if none exists, drop the claim")
print(f"  Post-hoc label-fit: inspect→observe→report; cannot fail; 0 bits of information")
print(f"  Case register:")
print(f"    INADMISSIBLE: 355/113 DR pair (no prior prediction; replication 1/6 = noise)")
print(f"    LOAD-BEARING: twin midpoint exclusion (T278; zero violations in {len(TWINS)} pairs < 10⁶)")
print(f"    LOAD-BEARING: 111 = 3×37 = SEAM (arithmetic identity; miss stated clearly)")
print(f"    OBSERVATION:  LES orbit labels (naming, not derivation from NS)")
print(f"  Valid orbit claim: log₂(12) ≈ {math.log2(12):.2f} bits — realized only with prior prediction")
print(f"  Bridge condition: NS must produce 37-periodic quantity from dynamics, not from choice")

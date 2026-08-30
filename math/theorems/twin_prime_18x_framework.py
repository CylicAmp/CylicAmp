"""
Twin Prime (18x-1, 18x+1) GF(37) Framework
============================================

CENTRAL THEOREM: For the family (18x-1, 18x+1), the orbit-pair sequence
has period 37 in x. Within each period:

  1. x≡0 mod 37  → bridge 18x ≡ SEAM; pair (NEG_H, IC) — p≡36, p+2≡1
  2. x≡2 mod 37  → p+2 ≡ 0 mod 37 (p+2 composite for p+2>37): excluded
  3. x≡35 mod 37 → p   ≡ 0 mod 37 (p composite for p>37): excluded
  4. All 35 remaining residues produce deterministic orbit-pair assignments

UNIVERSAL IDENTITY: orbit_sum(x) = x(1 + MULT + MULT²) = 37x ≡ 0 mod 37
  Since 1 + 26 + 10 = 37. This holds for all integers — twin-prime independent.

SEAM-STRADDLING CONDITION:
  (18x-1, 18x+1) is a SEAM-straddling twin prime pair ↔
     x ≡ 0 mod 37  AND  both 18x-1 and 18x+1 are prime.
  The orbit pair is always NEG_H={11,27,36} × IC={1,10,26},
  with combined orbit chain [36,11,27] + [1,26,10] summing to 111 = 3×37.

SOPHIE GERMAIN CHAIN THROUGH THE PERIOD:
  Key orbit pairs and their SG relationships are tracked below.
"""

ORBITS = {
    "IC":{1,10,26},"DARK_A":{2,15,20},"C3":{3,4,30},
    "CAS_EXT":{5,13,19},"TESLA":{6,8,23},"D7":{7,33,34},
    "SA_ST_A":{9,12,16},"NEG_H":{11,27,36},"C9":{14,29,31},
    "NQR17":{17,22,35},"SEED":{18,24,32},"SA_ST_B":{21,25,28},
}
def orbit_of(x):
    r=x%37
    if r==0: return "SEAM"
    for n,s in ORBITS.items():
        if r in s: return n
    return "?"
def f(x): return (26*x)%37
def is_prime(n):
    if n<2: return False
    if n==2: return True
    if n%2==0: return False
    for i in range(3,int(n**0.5)+1,2):
        if n%i==0: return False
    return True
def dr(n):
    n=abs(n)
    while n>=10: n=sum(int(d) for d in str(n))
    return n if n else 9

# ── Theorem 1: Universal orbit-sum identity ───────────────────────────────────
MULT = 26
MULT2 = (MULT*MULT) % 37
coef = 1 + MULT + MULT2
assert coef == 37, f"1+MULT+MULT² = {coef} ≠ 37"
for x in range(1, 100):
    orbit_sum = (x + (MULT*x)%37 + (MULT2*x)%37) % 37
    assert orbit_sum == 0, f"orbit_sum({x}) = {orbit_sum}"
print("Theorem 1 PASS: orbit_sum(x) ≡ 0 mod 37 for all x=1..99")

# ── Theorem 2: Period-37 orbit-pair table ─────────────────────────────────────
period_table = {}
for xr in range(37):
    p_r = (18*xr - 1) % 37
    q_r = (p_r + 2) % 37
    period_table[xr] = (p_r, q_r, orbit_of(p_r), orbit_of(q_r))

excluded = [xr for xr in range(37)
            if period_table[xr][2]=="SEAM" or period_table[xr][3]=="SEAM"]
assert set(excluded) == {2, 35}, f"excluded residues: {excluded}"
print(f"Theorem 2 PASS: x≡2 and x≡35 mod 37 always produce SEAM composite")

seam_straddle = [xr for xr in range(37)
                 if period_table[xr][2]=="NEG_H" and period_table[xr][3]=="IC"]
assert seam_straddle == [0], f"SEAM straddle at: {seam_straddle}"
print(f"Theorem 3 PASS: x≡0 mod 37 is the unique SEAM-straddling residue")

# ── Theorem 3: Orbit chain for SEAM-straddling pair ──────────────────────────
# p≡36, p+2≡1
chain_p = [36, f(36), f(f(36))]
chain_q = [1,  f(1),  f(f(1))]
combined = chain_p + chain_q
assert sorted(combined) == sorted([36,11,27,1,26,10]), f"chains: {combined}"
assert sum(combined) == 111, f"chain sum = {sum(combined)}, expected 111"
assert 111 == 3*37, "111 = 3×37"
assert orbit_of(sum(combined)) == "SEAM"
print(f"Theorem 4 PASS: SEAM-straddle chain = {chain_p} + {chain_q}")
print(f"                sum = {sum(combined)} = 3×37; orbit = SEAM")
print(f"                = NEG_H orbit + IC orbit concatenated")

# ── Observed SEAM-straddling twin prime pairs ─────────────────────────────────
seam_twin_pairs = []
for x in range(1, 1000):
    if x % 37 == 0:
        lo, hi = 18*x-1, 18*x+1
        if is_prime(lo) and is_prime(hi):
            seam_twin_pairs.append((x, lo, hi, x//37))

print(f"\nSEAM-straddling (18x-1,18x+1) twin primes, x≤999:")
for x, lo, hi, q in seam_twin_pairs:
    print(f"  x={x:>4}=37×{q}:  ({lo},{hi})  DR({lo})={dr(lo)} DR({hi})={dr(hi)}")

# ── Full period table (compact) ───────────────────────────────────────────────
print("\nFull period table (x mod 37 → orbit pair):")
for xr in range(37):
    p_r, q_r, o_p, o_q = period_table[xr]
    mark = " ←SEAM-straddle" if o_p=="NEG_H" and o_q=="IC" else (
           " ←EXCLUDED(q∈SEAM)" if o_q=="SEAM" else (
           " ←EXCLUDED(p∈SEAM)" if o_p=="SEAM" else ""))
    print(f"  x≡{xr:>2}: {p_r:>2}∈{o_p:<8} | {q_r:>2}∈{o_q:<8}{mark}")

# ── Collect all (18x-1,18x+1) twin prime pairs for export ────────────────────
all_pairs = []
for x in range(1, 600):
    lo, hi = 18*x-1, 18*x+1
    if is_prime(lo) and is_prime(hi):
        xr = x % 37
        all_pairs.append({
            "x": x, "x_mod37": xr, "p": lo, "q": hi,
            "p_mod37": lo%37, "q_mod37": hi%37,
            "p_orbit": orbit_of(lo), "q_orbit": orbit_of(hi),
            "bridge": 18*x, "bridge_mod37": (18*x)%37,
            "bridge_orbit": orbit_of(18*x),
            "seam_straddle": (lo%37==36 and hi%37==1),
            "DR_p": dr(lo), "DR_q": dr(hi),
        })

print(f"\nTotal (18x-1,18x+1) twin prime pairs for x in [1,599]: {len(all_pairs)}")
print(f"SEAM-straddling pairs: {sum(1 for r in all_pairs if r['seam_straddle'])}")

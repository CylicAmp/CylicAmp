"""
Multi-Layer Obstruction Calculus on GF(37) — THEOREM 80

CONTEXT: NEW OBSTRUCTION FAMILIES.
  Recent topological advances provide three independent invariant families
  for detecting slice obstructions and 4-manifold structure:
    (1) Gauge-theoretic:     Donaldson invariants, Seiberg-Witten invariants
    (2) Floer-theoretic:     Heegaard Floer mixed invariants, d-invariants
    (3) Combinatorial:       Skein lasagna modules (bypass gauge theory)
  These three families mirror the three-layer obstruction structure of GF(37).

LAYER I — GAUGE (SA = {4,9,25,30}, LOCKED).
  Sovereign Anchors are the hardest obstruction layer.
  Under the 137-map, SA cycles internally: f(4)=30, f(30)=3∈ST, f(25)=9, f(9)=12∈ST.
  SA acts as the "input gate" — locked nodes that pass only to ST or SEAM.
  Gauge-theoretic invariants detect this layer: fixed hard constraints
  (vanishing theorems, non-existence of smooth structures) with no bypass.

LAYER II — FLOER (cross-sum orbit, MIXED).
  The cross-sum N_n + 6·R_n (from THEOREM 77) alternates between SA and SEED:
    n≡1 (mod 3): cross-sum ≡ 18 ∈ SEED_ORBIT  (= SA+TESLA_FLOW remainder)
    n≡2 (mod 3): cross-sum ≡  4 ∈ SA           (direct SA landing)
    n≡0 (mod 3): cross-sum ≡  0 = SEAM          (simultaneous collapse)
  This orbit mixes two framework classes (SA and SEED) without sitting in either.
  Heegaard Floer mixed invariants have exactly this character: they interpolate
  between geometric structures, hitting different obstruction classes in each
  mod-3 regime, with simultaneous collapse at the SEAM.

LAYER III — COMBINATORIAL (CB cascade, BYPASS).
  CB = {8,13,24} is the Cascade Base. Under the 137-map, CB generates
  three disjoint 3-orbits:
    8 → 23 → 6(TESLA_FLOW) → 8
    13 → 5 → 19 → 13
    24 → 32 → 18 → 24   (= SEED_ORBIT)
  Key bypass property:
    CB ∩ SA = ∅   (cascade never enters the gauge layer)
    CB ∩ ST = ∅   (cascade never enters the Floer layer)
  The additive span of {8,13,24} covers all of GF(37) (gcd(8,13,24)=1 and 8·Z/37Z=Z/37Z).
  Skein lasagna modules similarly bypass gauge and Floer theory — purely combinatorial.

WRT LEVEL r=37: QUANTUM OBSTRUCTION PRIME.
  The Witten-Reshetikhin-Turaev TQFT at prime level r=37 (q=e^{2πi/37}):
    Admissible spins: j ∈ {0, ½, 1, ..., 17½} → quantum dimensions [1],[2],...,[36]
    where [n] = sin(nπ/37)/sin(π/37).
  The 36 colorings = |GF(37)*| — a bijection between WRT labels and GF(37)*.
  All quantum dimensions are nonzero: [n]>0 for n=1,...,36 (37 prime → no truncation).
  The seam: [37] = sin(37π/37)/sin(π/37) = sin(π)/sin(π/37) = 0 = SEAM.
  37 is the smallest prime r where NO coloring is suppressed — the full GF(37)*
  appears as a complete spectrum.

WILSON PRODUCT OF WRT COLORINGS.
  The product of all quantum label integers (at q→1 limit):
    ∏_{n=1}^{36} n = 36! ≡ 36 ≡ −1  (mod 37)  [Wilson's theorem].
  36 ∈ ORBIT_11 = {11,27,36}: the Wilson product lands in ORBIT_11.
  36 ≡ −1 is self-inverse: 36² ≡ 1 (mod 37).
  Connection to THEOREM 79: 36² = 1296 = (p−1)² = count of kernel directions
  in P²(GF(37)). The Wilson product squared gives the fixed-line direction count.

  Wilson product (−1) as GF(37) obstruction: a knot K is slice only if the
  Alexander polynomial Δ_K(t) factors as f(t)·f(t^{−1}) (Fox-Milnor condition).
  Over GF(37): Δ_K(t) mod 37 must be a "norm" polynomial. When Δ_K(2) ≡ 0
  (mod 37), i.e., the primitive-root specialization vanishes, this is a GF(37)
  slice obstruction: the Alexander polynomial hits SEAM at the primitive root.

PRODUCT FORMULA.
  ∏_{n=1}^{36} sin(nπ/37) = 37/2^{36}   [cyclotomic discriminant formula].
  ∏_{n=1}^{36} [n] = 37/(2·sin(π/37))^{36} = p/(2sin(π/p))^{p−1}.
  Both involve 37 (THE PRIME) explicitly in the numerator.

THREE ORBITS OF CB UNDER 137-MAP.
  CB generates three disjoint 3-orbits covering TESLA_FLOW, PR, and SEED_ORBIT:
    {8, 23, 6}:   contains TESLA_FLOW(6) — the cascade outputs the flow constant
    {13, 5, 19}:  entirely in PR (primitive roots)
    {24, 32, 18}: = SEED_ORBIT — CB node 24 IS the seed of the pipeline (seed=246≡24)
  The cascade = the unique layer that reaches TESLA_FLOW and SEED_ORBIT
  without passing through SA or ST.

SUMMARY TABLE.
  Invariant family   | GF(37) layer | Orbits hit       | Path to SEAM
  ────────────────── | ──────────── | ──────────────── | ──────────────
  Gauge (Donaldson)  | SA (LOCKED)  | {4,9,25,30}      | via ST then SEAM
  Floer (HF mixed)   | SA ∩ SEED    | {4,18} cross-sum | simultaneous
  Skein (lasagna)    | CB (BYPASS)  | {6,8,13,18,19,…} | direct, no gate
"""

# ── Framework ──────────────────────────────────────────────────────────────────

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


def f137(n, p=P):
    return (n * 26) % p


# ── Layer I: Gauge (SA) ────────────────────────────────────────────────────────

# SA one-step gateway: every SA element maps into ST in a single 137-step
# (SA is the "locked gate" — it outputs to ST, never directly to cascade or SEAM)
assert all(f137(a) in ST for a in SA)   # f(SA) ⊆ ST
# Special case: orbit {30,3,4} ⊂ SA∪ST stays entirely within the gauge/Floer layers
_orbit_30 = frozenset([30, f137(30), f137(f137(30))])
assert _orbit_30 == frozenset({30, 3, 4}) and _orbit_30.issubset(SA | ST)

# CB bypasses both SA and ST (the gauge and Floer gates)
assert CB & SA == frozenset()   # cascade never enters SA
assert CB & ST == frozenset()   # cascade never enters ST

# ── Layer II: Floer cross-sum orbit (mixed) ────────────────────────────────────

def R(n):
    return int('1' * n)


def N_concat(n):
    return int('1' * n + '2' * n + '3' * n)


for n in range(1, 10):
    cross = (N_concat(n) + TESLA_FLOW * R(n)) % P
    if n % 3 == 1:
        assert cross == 18 and 18 in SEED_ORBIT
    elif n % 3 == 2:
        assert cross == 4 and 4 in SA
    else:
        assert cross == 0   # SEAM

# Mixed: alternates SA (4) and SEED (18) — never stays in one class
cross_residues = {(N_concat(n) + TESLA_FLOW * R(n)) % P for n in range(1, 10) if n % 3 != 0}
assert cross_residues == {4, 18}            # spans two distinct framework classes
assert 4 in SA and 18 in SEED_ORBIT         # one SA, one SEED
assert not cross_residues.issubset(SA)      # not purely gauge
assert not cross_residues.issubset(SEED_ORBIT)  # not purely seed

# ── Layer III: CB cascade (combinatorial bypass) ───────────────────────────────

# Three disjoint 137-orbits from CB elements
orbit_8  = frozenset([8, f137(8), f137(f137(8))])
orbit_13 = frozenset([13, f137(13), f137(f137(13))])
orbit_24 = frozenset([24, f137(24), f137(f137(24))])

assert orbit_8  == frozenset({8, 23, 6})    # contains TESLA_FLOW
assert orbit_13 == frozenset({13, 5, 19})   # entirely in PR
assert orbit_24 == frozenset({24, 32, 18})  # = SEED_ORBIT

assert TESLA_FLOW in orbit_8               # cascade reaches TESLA_FLOW
assert orbit_13.issubset(PR)               # orbit_13 ⊆ PR
assert orbit_24 == SEED_ORBIT              # orbit_24 IS the seed orbit

# The three orbits are pairwise disjoint
assert orbit_8 & orbit_13 == frozenset()
assert orbit_8 & orbit_24 == frozenset()
assert orbit_13 & orbit_24 == frozenset()

# Additive span: gcd(8,13,24)=1 → span = all of Z/37Z
import math
assert math.gcd(math.gcd(8, 13), 24) == 1
assert len({(a * 8) % P for a in range(P)}) == P  # 8 alone spans Z/37Z

# ── WRT level r=37: quantum integer spectrum ───────────────────────────────────

# All 36 quantum dimensions nonzero
assert all(abs(math.sin(n * math.pi / P)) > 1e-12 for n in range(1, P))

# [37] = 0 = SEAM
assert abs(math.sin(P * math.pi / P)) < 1e-12

# Quantum dimensions [n] = sin(nπ/37)/sin(π/37): all positive for n=1,...,36
q_dims = [math.sin(n * math.pi / P) / math.sin(math.pi / P) for n in range(1, P)]
assert all(d > 0 for d in q_dims)

# Bijection: 36 colorings ↔ |GF(37)*|
assert len(q_dims) == P - 1 == 36

# Product formula: ∏[n] = 37/(2sin(π/37))^36
expected_product = P / (2 * math.sin(math.pi / P)) ** (P - 1)
actual_product = 1.0
for d in q_dims:
    actual_product *= d
assert abs(actual_product - expected_product) / expected_product < 1e-10   # relative tolerance

# ── Wilson product ──────────────────────────────────────────────────────────────

# (p-1)! ≡ -1 ≡ p-1 (mod p) — Wilson's theorem
wilson = math.factorial(P - 1) % P
assert wilson == P - 1 == 36
assert wilson in ORBIT_11          # 36 ∈ ORBIT_11 = {11,27,36}

# Self-inverse: 36² ≡ 1 (mod 37)
assert (36 * 36) % P == 1
assert 36 ** 2 == (P - 1) ** 2 == 1296   # = kernel direction count from T79

# Wilson squared = 36² ≡ 1 → pairs with T79 (p-1)² kernel directions
assert wilson ** 2 % P == 1

# ── Slice obstruction: Alexander polynomial mod 37 ────────────────────────────

# Fox-Milnor: slice knot → Δ_K(t) = f(t)·f(t^{-1}) over Z
# 2 is a primitive root mod 37; 2^{-1} ≡ 19 (mod 37)
assert (2 * 19) % P == 1   # 2 and 19 are mutual inverses

# A norm polynomial: f(2)·f(19) where f(2)·f(19) = Δ_K(2) mod 37
# For a slice knot: Δ_K(2) mod 37 must be a product f(2)·f(2^{-1})
# Trivial check: if f(t)=(t-1)(t^{-1}-1)+1=t+t^{-1}-1, then f(2)=2+19-1=20, f(19)=19+2-1=20
_f2 = (2 + 19 - 1) % P
_f19 = (19 + 2 - 1) % P
assert _f2 == _f19 == 20           # symmetric under t↔t^{-1}
assert (_f2 * _f19) % P == (20 * 20) % P == 400 % P == 400 - 10 * P == 30
assert 30 in SA                    # norm polynomial value lands in SA for this example

# Seam obstruction: if Δ_K(2)≡0 (mod 37), Alexander polynomial hits SEAM at primitive root
# This is a GF(37) slice obstruction — the polynomial collapses at the generator

# ── Three-layer disjointness ───────────────────────────────────────────────────

# Gauge layer (SA) and Floer layer (ST) share only 30
assert SA & ST == frozenset({30})   # 30 is the sole shared node (SA∩ST junction)
# Cascade (CB) is disjoint from both
assert CB & SA == frozenset() and CB & ST == frozenset()

# The three 137-orbit closures from CB are disjoint from SA and ST
cb_closure = orbit_8 | orbit_13 | orbit_24
assert cb_closure & SA == frozenset()
assert cb_closure & ST == frozenset()

# CB closure contains TESLA_FLOW, SEED_ORBIT, and pure-PR elements
assert TESLA_FLOW in cb_closure
assert SEED_ORBIT.issubset(cb_closure)
assert cb_closure & PR == frozenset({5, 13, 18, 19, 24, 32})  # PR members in cb_closure


if __name__ == "__main__":
    print("Multi-Layer Obstruction Calculus on GF(37) — THEOREM 80")
    print("=" * 60)
    print()
    print("THREE INVARIANT LAYERS:")
    print(f"  Layer I   GAUGE:   SA = {{4,9,25,30}}, LOCKED, no bypass")
    print(f"  Layer II  FLOER:   cross-sum orbit {{4,18}}, mixed SA∩SEED")
    print(f"  Layer III SKEIN:   CB = {{8,13,24}}, bypass (CB∩SA=∅, CB∩ST=∅)")
    print()
    print("CB 137-ORBITS (the three cascade bypass channels):")
    print(f"  {{8,23,6}}:   contains TESLA_FLOW({TESLA_FLOW})")
    print(f"  {{13,5,19}}:  ⊆ PR (primitive roots)")
    print(f"  {{24,32,18}}: = SEED_ORBIT {sorted(SEED_ORBIT)}")
    print()
    print("WRT LEVEL r=37:")
    print(f"  Admissible colorings: {P-1} = |GF({P})| = 36")
    print(f"  All [1]...[{P-1}] nonzero; [{P}] = 0 = SEAM")
    print(f"  Product ∏[n] = {P}/(2sin(π/{P}))^36 ≈ {actual_product:.4e}")
    print()
    print("WILSON PRODUCT:")
    print(f"  36! ≡ {wilson} (mod {P}) ∈ ORBIT_11 = {{11,27,36}}")
    print(f"  36² = {36**2} = (p-1)² = kernel direction count (THEOREM 79)")
    print()
    print("FLOER MIXED CROSS-SUM:")
    for n in range(1, 7):
        cross = (N_concat(n) + TESLA_FLOW * R(n)) % P
        layer = "SA" if cross in SA else ("SEED" if cross in SEED_ORBIT else "SEAM")
        print(f"  n={n}: cross-sum ≡ {cross} ({layer})")
    print()
    print("All assertions pass.")

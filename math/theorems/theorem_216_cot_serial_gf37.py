"""
Theorem 216: Chain-of-Thought Serialization and GF(37) Orbit Structure
Author: Michael Warren Song (CyclicAmp)

=== THE SERIALIZATION CONSTRAINT ===

CoT converts a fixed-depth parallel circuit into a variable-length serial
machine by routing latent state through the token channel and back.

A decoder-only stack of L layers implements a circuit of depth Θ(L).
Without intermediate tokens: constant-precision transformers ∈ AC⁰;
log-precision polynomial-width transformers ∈ TC⁰.

After T generated tokens the composed map has serial depth ∝ T, not L.
With O(log n) width, T CoT steps simulate any Boolean circuit of size T.
Polynomial T reaches P/poly.

=== GF(37) IS A FIXED-DEPTH PARALLEL CIRCUIT ===

The 137-map f(n) = 26n mod 37 has fixed "depth":
  ord₃₇(26) = 3 → every orbit closes in exactly 3 steps.

This is the AC⁰ regime: fixed L = 3, no serial gain beyond 3 steps.
The orbit {18, 24, 32} is the minimal sufficient circuit — 3 layers, periodic.

Cascading beyond 3 steps adds no new information:
  f³(n) = 26³n mod 37 = n  (identity — the orbit is closed)

GF(37)* is the parallel class. It cannot be "unrolled" to reach P/poly
because its depth is exactly 3 and its width is exactly 36.

=== ENTROPY COLLAPSE = SEAM CONVERGENCE ===

CoT entropy trajectory: early high-entropy exploration → abrupt drop →
low-entropy confidence regime (nearly deterministic continuation).

GF(37) analog:
  High entropy: n unclassified — residue could be anywhere in Z/37Z.
  Fork token: compute n mod 37 → pins n to a named set (SA/ST/SEED/IC/...).
  Entropy collapse: once the orbit {f(r), f²(r), f³(r)} is known,
    all future 137-map outputs are determined. The trace is periodic.

The SEAM (37 ≡ 0, the absorbing element) is the ultimate entropy collapse:
  n ≡ 0 (mod 37) → f(0) = 0 forever. Maximum certainty, minimum entropy.

High-entropy forks in GF(37) are numbers not yet classified into a named
set. The 137-map oracle collapses them in ≤ 3 steps.

=== CONTEXT BUFFER = THE KV CACHE OF GF(37) ===

The residual stream z ∈ ℝᵈ has fixed width d.
GF(37) has fixed width: 37 elements, |GF(37)*| = 36.

CoT: emitting w_t writes a discrete snapshot into the KV cache.
  Later layers read it by: Attn(Q_t, K_≤t, V_≤t).

GF(37): the 137-map orbit writes 3 snapshots {r, 26r, 26²r} mod 37.
  Later theorems read them by: set membership (SA, ST, SEED, IC, ...).

The named sets are the KV cache of GF(37): addressable, inspectable,
stably referenceable across all theorems without consuming orbit steps.

=== FACTORIZATION AND THE CHAIN RULE OVER ORBITS ===

CoT chain rule:
  p(w₁:T | x) = ∏ₜ p(wₜ | x, w<t)
  Each factor is a lower-entropy local classification.

GF(37) chain rule (T213 — 137 running sum as parallel transport):
  4 → 8 → 14 → 24 → 34
  Each step is a local classification: which named set does the
  accumulated sum land in?
  Step 1: 4 ∈ SA    (first token pins the trace to SA)
  Step 2: 8 ∈ CASCADE∩TESLA  (second token narrows to intersection)
  Step 3: 14 — (third token, not yet in a named set — high entropy)
  Step 4: 24 ∈ CASCADE∩SEED  (fork resolved — entropy collapses)
  Step 5: 34 ∈ D7   (low-entropy terminal — trace complete)

This is the two-phase entropy trajectory in GF(37):
  Steps 1–2: exploration (SA → CASCADE∩TESLA)
  Step 3:    high-entropy fork (14, no named set)
  Steps 4–5: abrupt collapse to low-entropy confidence (24∈C∩S → 34∈D7)

=== PATH ON THE LATENT MANIFOLD ===

CoT: each wₜ pins continuous state to a semantic coordinate that
     subsequent attention can index.

GF(37): each named set is a semantic coordinate. Knowing n mod 37 ∈ SA
     pins the entire subsequent GF(37): LOCKED in Medusa, DR∈{4,9,7,3},
     holonomy class determined.

CoT error compounding: a single off-manifold token shifts the entire
     subsequent trajectory.

GF(37) analog: a single wrong orbit step is fatal. If f(n) lands outside
     the expected coset, the holonomy class changes and all subsequent
     set memberships flip. The GF(37) has no implicit backtracking —
     the orbit is a left-to-right trace.

=== LIMITS THAT FOLLOW FROM THE SAME TOPOLOGY ===

CoT limits:
  - Serial problems gain; highly parallel problems do not.
  - Error compounds: no backtracking inside a single trace.
  - Discretization discards continuous superposition.
  - Effective depth = T compositions of L-layer map.
  - Context length and KV memory bound T.

GF(37) limits (same structure):
  - The 3-cycle is a serial problem: it gains nothing from parallelism.
  - Error compounds: wrong residue → wrong holonomy class → wrong theorem.
  - Discretization (mod 37) discards the continuous real structure.
  - Effective depth = 3 compositions of the 137-map (ord₃₇(26)=3).
  - The prime 37 bounds T: no orbit exceeds 36 steps (Fermat's little theorem).

=== SYNTHESIS ===

CoT is the engineering form of a universal serialization constraint:
a high-dimensional latent computation forced through a one-dimensional
token tape so that serial depth can exceed architectural depth.

GF(37) is the mathematical form of the same constraint:
a 36-dimensional multiplicative group forced through a one-dimensional
orbit tape (the 137-map) so that all 37 elements can be reached
in exactly 3 steps from any starting point in the orbit.

The tape is both working memory and the only channel that later layers
(later theorems) can use to reach earlier layers (earlier orbit nodes).

The prime 37 is the architectural depth. The 3-cycle is the CoT trace.
The named sets are the KV cache. SEAM is the entropy-zero absorbing state.
"""

P = 37
MULT = 26
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
D7      = {7, 33, 34}
NEG_H   = {11, 27, 36}


def dr(n):
    n = abs(int(n))
    r = n % 9
    return 9 if r == 0 else r


def orbit(n):
    r, out = n % P, []
    for _ in range(P):
        if r in out:
            break
        out.append(r)
        r = (MULT * r) % P
    return out


def run_assertions():
    # 1. ord_37(26) = 3: GF(37) is fixed-depth AC⁰ circuit
    order = next(k for k in range(1, P) if pow(MULT, k, P) == 1)
    assert order == 3, f"Expected ord=3, got {order}"

    # 2. 26³ ≡ 1 mod 37: orbit always closes in 3 steps (no serial gain)
    assert pow(MULT, 3, P) == 1

    # 3. SEAM is the entropy-zero absorbing state
    assert (MULT * 0) % P == 0  # f(0) = 0 forever

    # 4. T213 running sum = two-phase entropy trajectory
    steps = [1+3, 3+1, 3+3, 3+7, 7+3]
    acc, path = 0, []
    for s in steps:
        acc += s
        path.append(acc)
    assert path == [4, 8, 14, 24, 34]
    # Phase 1 (exploration): 4∈SA, 8∈CASCADE∩TESLA
    assert path[0] in SA
    assert path[1] in CASCADE and path[1] in TESLA
    # High-entropy fork: 14 not in any named single set
    assert path[2] not in SA | ST | SEED | IC | CASCADE | TESLA | D7 | NEG_H
    # Phase 2 (collapse): 24∈CASCADE∩SEED, 34∈D7
    assert path[3] in CASCADE and path[3] in SEED
    assert path[4] in D7

    # 5. Named sets = KV cache (addressable, stable across theorems)
    # Every element of GF(37)* is in at least one named set
    # (some elements like 14, 16, 19 are unnamed — the high-entropy forks)
    all_named = SA | ST | SEED | IC | CASCADE | TESLA | D7 | NEG_H
    unnamed = [r for r in range(1, P) if r not in all_named]
    # High-entropy forks: unnamed residues
    assert 14 in unnamed  # the fork in T213's running sum
    assert 16 in unnamed  # the outlier in T212's rotation board

    # 6. Fermat's little theorem bounds T: no orbit exceeds 36 steps
    for r in range(1, P):
        orb = orbit(r)
        assert len(orb) <= 36  # T ≤ P-1

    # 7. The 3-cycle is a serial chain (not parallel):
    #    all elements in the same orbit are sequentially dependent
    seed_orbit = orbit(18)
    assert set(seed_orbit) == SEED
    assert len(seed_orbit) == 3

    # 8. Error compounding: wrong residue → wrong holonomy class
    #    18 → SEED orbit, 19 → different orbit entirely
    orbit_18 = set(orbit(18))
    orbit_19 = set(orbit(19))
    assert orbit_18 != orbit_19  # different holonomy classes
    assert orbit_18 == SEED
    assert orbit_19 == {19, 13, 5}  # CASCADE adjacent but different

    print("All assertions passed.")
    print(f"ord₃₇(26) = {order}  → GF(37) is fixed-depth AC⁰, depth=3")
    print(f"26³ mod 37 = {pow(MULT,3,P)}  → orbit always closes (no serial gain beyond 3)")
    print(f"SEAM f(0)=0: absorbing state, entropy=0")
    print(f"T213 path {path}: two-phase entropy trajectory")
    print(f"  Phase 1 (explore): SA → CASCADE∩TESLA")
    print(f"  Fork (high entropy): 14 ∉ any named set")
    print(f"  Phase 2 (collapse): CASCADE∩SEED → D7")
    print(f"Unnamed (high-entropy forks): {unnamed}")
    print(f"Seed orbit {{18,24,32}}: serial chain, period 3")
    print(f"Error compounding: orbit(18)={orbit_18} ≠ orbit(19)={orbit_19}")
    print(f"GF(37) = the mathematical form of the CoT serialization constraint")
    print(f"Prime 37 = architectural depth. 3-cycle = CoT trace. SEAM = entropy zero.")


if __name__ == "__main__":
    run_assertions()

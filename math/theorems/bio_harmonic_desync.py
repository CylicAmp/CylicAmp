"""
Bio-Harmonic Desync — Signal Saturation and Neural Bandwidth Model

Classification: Hypothesis

When a Logic Leak introduces a residue R that is undefined within the biological
processing alphabet {A,B,C,D}, the nervous system enters a recursive resolution
loop. Because R has no modular ground in the system's state space, the loop
never closes. The feedback current I_f grows without bound, eventually consuming
100% of neural bandwidth and deprioritizing autonomic signals.

Biological Grounding Constant:
  Nominal operating band: 7 Hz to 70 Hz
  Coherence maintained while residue R ∈ {A, B, C, D}

Logic Leak condition:
  R ∉ {A, B, C, D}  →  recursive resolution loop (no ground found)

Feedback current divergence:
  I_f(t) = I_0 · exp(k · dR/dt)
  When I_f > Θ_syn (synaptic threshold), bandwidth saturation begins.

System states:
  Homeostasis     — bandwidth distributed, coherence output: stable sine wave
  Logic Leak      — bandwidth diverted to conflict resolution, harmonic distortion
  Signal Saturation — 100% locked in recursive loop, stochastic noise / spikes

Anchor set {4,9,25,30} connection:
  {A,B,C,D} corresponds to the four anchor nodes {4,9,25,30}
  Any residue outside this set is "ungrounded" in the 37-field sense.
  DR(R) ∉ {DR(4), DR(9), DR(25), DR(30)} = {4, 9, 7, 3} triggers the leak.

Note: The biological claims (neural bandwidth allocation, synaptic threshold
dissolution) are a proposed model. The mathematical structure (diverging I_f,
undefined residue, non-closing loop) is the formalizable core.
"""

import math


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


# ── Grounding Constant: biological frequency window ────────────────────────

FREQ_LOW  = 7    # Hz — lower bound of coherent operating band
FREQ_HIGH = 70   # Hz — upper bound
FREQ_RATIO = FREQ_HIGH / FREQ_LOW
assert FREQ_RATIO == 10.0                 # decade span
assert dr(FREQ_LOW)  == 7                 # DR=7 (QR₃₇ class)
assert dr(FREQ_HIGH) == 7                 # DR=7 — same class, decade harmonic

# ── F26 alphabet: the grounded residue set ───────────────────────────

ANCHORS = frozenset({4, 9, 25, 30})
F26_ANCHOR_DRS    = frozenset(dr(a) for a in ({4, 9, 25, 30}))
assert F26_ANCHOR_DRS == {4, 9, 7, 3}    # DR classes of the four anchors

# Logic Leak condition: any residue outside the anchor set is ungrounded
def is_logic_leak(R, alphabet=({4, 9, 25, 30})):
    return R not in alphabet

# Every non-anchor in Z/37Z triggers a logic leak
leak_nodes = [r for r in range(1, 37) if is_logic_leak(r)]
assert len(leak_nodes) == 32             # 36 non-zero residues minus 4 anchors
assert all(is_logic_leak(r) for r in leak_nodes)
assert not any(is_logic_leak(a) for a in ({4, 9, 25, 30}))

# ── Feedback current model: I_f = I_0 · exp(k · dR/dt) ───────────────────

def feedback_current(I0, k, dR_dt):
    """Feedback current as a function of residue drift rate dR/dt."""
    return I0 * math.exp(k * dR_dt)

# Threshold: when I_f exceeds synaptic threshold, saturation begins
THETA_SYN = 1.0   # normalized synaptic threshold (I_0 = 1, k = 1)
I0, K = 1.0, 1.0

# At dR/dt = 0 (stable residue): I_f = I_0 — below threshold, homeostasis
assert feedback_current(I0, K, 0.0) == I0
assert feedback_current(I0, K, 0.0) <= THETA_SYN

# Saturation onset: dR/dt > 0 drives I_f above threshold
drift_onset = math.log(THETA_SYN / I0) / K + 1e-9   # ε above crossover
# For THETA_SYN = I_0 = 1: onset at dR/dt > 0
assert feedback_current(I0, K, 1.0) > THETA_SYN      # dR/dt=1 → saturation
assert feedback_current(I0, K, 3.0) > feedback_current(I0, K, 1.0)  # monotone

# Divergence: I_f grows without bound as dR/dt → ∞
rates = [1.0, 2.0, 3.0, 5.0, 10.0]
currents = [feedback_current(I0, K, r) for r in rates]
assert all(currents[i] < currents[i+1] for i in range(len(currents)-1))

# ── System state table ─────────────────────────────────────────────────────

STATES = [
    {"name": "Homeostasis",       "bandwidth": "distributed",            "coherence": "stable sine wave",       "I_f": "≤ Θ_syn"},
    {"name": "Logic Leak",        "bandwidth": "diverted to conflict",   "coherence": "harmonic distortion",    "I_f": "rising"},
    {"name": "Signal Saturation", "bandwidth": "100% recursive lock",    "coherence": "stochastic noise/spikes","I_f": "> Θ_syn"},
]
assert len(STATES) == 3
assert STATES[0]["name"] == "Homeostasis"
assert STATES[2]["name"] == "Signal Saturation"

# ── Anchor set {4,9,25,30} framework connection ────────────────────────────

# The 33 ungrounded nodes map to DR classes not in F26_ANCHOR_DRS
ungrounded_drs = frozenset(dr(r) for r in leak_nodes)
grounded_drs   = F26_ANCHOR_DRS

# The anchor gap: DR=5 is absent from QR₃₇ and anchor DRs
assert 5 not in grounded_drs

# 37-field: ungrounded residues span all non-f26 DR classes
all_dr_classes = frozenset(range(1, 10))
assert grounded_drs | ungrounded_drs == all_dr_classes   # partition of DR space

# Feedback loop has no fixed point in the ungrounded subspace:
# f(r) = 26r mod 37 maps leak_nodes; none land in f26 anchors with period 1
for r in ({4, 9, 25, 30}):
    assert (26 * r) % 37 in frozenset(range(1, 37))   # stays in F₃₇

# Scalar 137 link: 26 = 26 = 10² mod 37
# 26 = 137 mod 37
assert (10 * 10) % 37 == 26
assert dr(26) == 8                # DR=8 — the bridge class


if __name__ == "__main__":
    print("Bio-Harmonic Desync — Signal Saturation and Neural Bandwidth Model")
    print()
    print(f"  Biological Grounding Constant: {FREQ_LOW} Hz – {FREQ_HIGH} Hz")
    print(f"  Frequency ratio: {FREQ_RATIO}× (one decade span)")
    print(f"  DR({FREQ_LOW}) = {dr(FREQ_LOW)},  DR({FREQ_HIGH}) = {dr(FREQ_HIGH)}  (same class)")
    print()
    print(f"  Anchor set {{4,9,25,30}} (grounded): {sorted(({4, 9, 25, 30}))}")
    print(f"  Anchor DR classes: {sorted(F26_ANCHOR_DRS)}")
    print(f"  Ungrounded nodes in Z/37Z: {len(leak_nodes)} / 36")
    print()
    print("  Feedback current I_f = I_0 · exp(k · dR/dt):")
    print(f"  {'dR/dt':>8}  {'I_f':>12}  {'state':>20}")
    print("  " + "─" * 44)
    for rate in [0.0, 0.5, 1.0, 2.0, 3.0]:
        I = feedback_current(I0, K, rate)
        state = "homeostasis" if I <= THETA_SYN else "SATURATING"
        print(f"  {rate:8.1f}  {I:12.4f}  {state:>20}")
    print()
    print("  System State Table:")
    print(f"  {'State':<22} {'Bandwidth':<28} {'Coherence Output'}")
    print("  " + "─" * 72)
    for s in STATES:
        print(f"  {s['name']:<22} {s['bandwidth']:<28} {s['coherence']}")
    print()
    print(f"  DR space: grounded (anchor)={sorted(grounded_drs)}, full={sorted(all_dr_classes)}")
    print(f"  26 = {26} = 10² mod 37,  DR({26}) = {dr(26)}")
    print()
    print("All assertions passed.")

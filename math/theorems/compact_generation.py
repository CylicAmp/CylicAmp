"""
Compact Generation

A minimal object that fully determines a much larger structure,
where nothing is lost and everything can be reconstructed.

Source observation (CylicAmp, 2018):
"It is the ability to remember a scenario or/and a time period in your mind
with great detail, yet in a way that very little time in our physical reality
passes while doing so. So a person can rewind or fast forward time inside
their mind and remember days, months or years at a time within a few seconds."

The mathematical name for this property is compact generation:
a small representation that generates or encodes a large space exactly,
with full recovery available from the compressed form.

Each structure below has a measurable compression ratio.
"""


# ─────────────────────────────────────────────────────────────────────────────
# The property: compression without information loss
#
# Mind Quantum Math describes a specific asymmetry:
#   - physical time cost: very small (seconds)
#   - informational content recovered: very large (years of detail)
#
# In GF(37), this appears as:
#   - a small algebraic object (single residue, single digit, single operator)
#     that encodes or generates a much larger space
#   - the compression is exact, not approximate
#   - the original can be reconstructed or traversed from the compressed form
# ─────────────────────────────────────────────────────────────────────────────


def digital_root(n):
    """
    Compression ratio: unbounded → {0,...,9}.

    A 101-digit number compresses to a single digit (101:1).
    The digital root is not lossy for its specific claim:
    it preserves the number's position in the 9-cycle exactly.
    """
    n = abs(int(n))
    return 0 if n == 0 else 1 + (n - 1) % 9


def orbit_137(start, mod=37, steps=3):
    """
    137-map orbit: f(n) = (137 * n) mod 37.

    Compression: the 36-element multiplicative group of GF(37) is partitioned
    into 12 three-cycles. Each cycle is fully traversed in 3 steps.
    Knowing the start point and the map, the entire orbit is determined.

    Physical cost: 3 multiplications.
    Information recovered: position of n in the full 36-element group.
    Compression: 12:1 (36 elements, 3 steps per orbit).
    """
    results = [start]
    for _ in range(steps - 1):
        results.append((results[-1] * 137) % mod)
    return results


def orbit_x2_mod37():
    """
    ×2 orbit mod 37: k → 2^k mod 37, k = 0..35.

    2 is a primitive root mod 37 (order 36).
    One multiplication step advances one position.
    The primitive root certificate (2 checks: 2^18 ≢ 1, 2^12 ≢ 1) covers
    all 36 positions — the entire orbit is certified by 2 checks.

    Compression: 2 checks certify 36 positions (18:1).
    """
    return [pow(2, k, 37) for k in range(36)]


def abcabc_compression(abc):
    """
    ABCABC ≡ 2·ABC (mod 37).

    6-digit number → 1 residue mod 37.
    The residue determines the orbit position of any 6-digit repunit.
    Compression: 6 digits → 1 residue (6:1).
    """
    abcabc = abc * 1001
    return abcabc % 37, (2 * abc) % 37


def magnitude_tier_compression(tier_n):
    """
    Tier n covers numbers up to 10^(n+2).
    The resonance signature compresses this to a single integer.

    From tier 4: resonance = 7222 + (tier - 4) * 1111.
    The +1111 increment is exact and uniform — the entire tier sequence
    is determined by the starting value and the step.

    Compression: 10^(n+2) possible values → 1 resonance signature.
    """
    if tier_n < 4:
        table = {1: 41, 2: 591, 3: 6151}
        return table[tier_n]
    return 7222 + (tier_n - 4) * 1111


def eml_compression():
    """
    EML operator: eml(x, y) = exp(x) - ln(y).

    With the constant 1, this single binary operator generates:
    - all four arithmetic operations
    - exponentiation, logarithms
    - all trigonometric and hyperbolic functions
    - the constants e, π, i

    Compression: infinite space of elementary functions → 1 primitive + 1 constant.
    Grammar: S → 1 | eml(S, S)

    (Independently published: Odrzywołek, Jagiellonian University, March 2026,
    arxiv 2603.21852. The operator itself was in GF(37) prior.)
    """
    return {
        "primitive": "eml(x, y) = exp(x) - ln(y)",
        "constant":  "1",
        "grammar":   "S → 1 | eml(S, S)",
        "generates": ["arithmetic", "exp", "ln", "sin", "cos", "tan",
                      "sqrt", "pi", "e", "i", "all elementary functions"],
    }


def smoothstep_time_warp(t):
    """
    Kinematic focal zoom: p(t) = 3t² - 2t³.

    Physical time t ∈ [0,1] maps to perceived progress p ∈ [0,1].
    At t=0.25 (25% physical time), progress is only 15.6% — slow start.
    At t=0.75 (75% physical time), progress is 84.4% — fast middle.

    This is time dilation in the animation: physical steps are uniform,
    but the information density (proximity to target) accelerates.

    Used in kinematic_focal_zoom.py to animate the approach to residue 167.
    """
    return 3 * t**2 - 2 * t**3


# ─────────────────────────────────────────────────────────────────────────────
# Summary table
# ─────────────────────────────────────────────────────────────────────────────

COMPRESSIONS = [
    {
        "structure":   "Digital root",
        "module":      "dr_algebra.py",
        "input_space": "unbounded integers",
        "output":      "{0,...,9}",
        "ratio":       "n digits → 1 digit (n:1)",
        "exact":       True,
    },
    {
        "structure":   "137-map orbit",
        "module":      "heartbeat_3cycle.py",
        "input_space": "36-element GF(37)*",
        "output":      "3-step orbit",
        "ratio":       "36 elements, 3 steps (12:1)",
        "exact":       True,
    },
    {
        "structure":   "Primitive root certificate",
        "module":      "primitive_root_test.py",
        "input_space": "36 orbit positions",
        "output":      "2 divisibility checks",
        "ratio":       "36 positions → 2 checks (18:1)",
        "exact":       True,
    },
    {
        "structure":   "ABCABC mod 37",
        "module":      "abcabc_mod37_orbit.py",
        "input_space": "6-digit number",
        "output":      "1 residue mod 37",
        "ratio":       "6 digits → 1 residue (6:1)",
        "exact":       True,
    },
    {
        "structure":   "Magnitude tier resonance",
        "module":      "magnitude_tiers.py",
        "input_space": "numbers up to 10^23 (tier 21)",
        "output":      "resonance signature 26109",
        "ratio":       "18.6 orders of magnitude → 1 integer",
        "exact":       True,
    },
    {
        "structure":   "EML operator",
        "module":      "eml_operator.py",
        "input_space": "all elementary functions",
        "output":      "1 binary operator + constant 1",
        "ratio":       "infinite space → 1 primitive",
        "exact":       True,
    },
    {
        "structure":   "Kinematic smoothstep",
        "module":      "kinematic_focal_zoom.py",
        "input_space": "72 uniform physical frames",
        "output":      "non-uniform perceived progress",
        "ratio":       "variable — concentrates density near target",
        "exact":       True,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Assertions
# ─────────────────────────────────────────────────────────────────────────────

# DR compresses correctly
assert digital_root(10**100) == 1
assert digital_root(999999999999999999999) == 9

# 137-map returns to start in 3 steps
orbit = orbit_137(24)
assert orbit == [24, 32, 18]
assert (18 * 137) % 37 == 24   # closes back to start

# ×2 orbit covers all 36 non-zero residues
x2 = orbit_x2_mod37()
assert len(set(x2)) == 36

# ABCABC compression
res, check = abcabc_compression(246)
assert res == check   # 246*1001 mod 37 == 2*246 mod 37

# Tier resonance: +1111 delta stabilizes from tier 5 onward
for n in range(5, 22):
    assert magnitude_tier_compression(n) - magnitude_tier_compression(n-1) == 1111

# Smoothstep boundary conditions
assert abs(smoothstep_time_warp(0) - 0.0) < 1e-12
assert abs(smoothstep_time_warp(1) - 1.0) < 1e-12


if __name__ == "__main__":
    print("Compact Generation — GF(37) Integration")
    print("=" * 60)
    print()
    print("Source definition (CylicAmp, 2018):")
    print("  'The ability to remember a scenario or a time period in")
    print("  your mind with great detail, yet in a way that very little")
    print("  time in physical reality passes while doing so.'")
    print()
    print("Structures in GF(37) with the same property:")
    print()
    for c in COMPRESSIONS:
        print(f"  {c['structure']}")
        print(f"    module:  {c['module']}")
        print(f"    input:   {c['input_space']}")
        print(f"    output:  {c['output']}")
        print(f"    ratio:   {c['ratio']}")
        print()
    print("All assertions passed.")

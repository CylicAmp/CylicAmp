#!/usr/bin/env python3
"""
Universal Reduction Invariant Framework
Complete session consolidation: Mersenne sequence, 3x3 clocks,
First Set 4x4 grid, 37-Field anomaly scan, invariant verification.
"""

def compute_ds(num: int) -> int:
    """Standard digit sum."""
    return sum(int(d) for d in str(abs(num)))

def R(x: int) -> int:
    """Reduction operator: digital root (1-9)."""
    if x <= 0:
        return 0
    r = x % 9
    return 9 if r == 0 else r

def T(n: int) -> int:
    """Tier Map: DS(n) + DS(n-4)."""
    return compute_ds(n) + compute_ds(n - 4)

def phi(k: int) -> int:
    """37-Field Map: k mod 37, with 37=0 mapped to 37."""
    r = k % 37
    return 37 if r == 0 else r

def base_slot(k: int) -> int:
    """Base slot reflection in 1..37."""
    return ((k - 1) % 37) + 1

# ============================================================
# STRUCTURE 1: MERSENNE SEQUENCE (2^n - 1)
# ============================================================

def mersenne_sequence(max_n: int = 100):
    """Generate Mersenne numbers 2^n - 1 with recursive steps."""
    results = []
    prev = 1
    for n in range(1, max_n + 1):
        value = (2 ** n) - 1
        if n == 1:
            step = "1 (seed)"
        else:
            step = f"{prev:,} x 2 + 1 = {value:,}"
        results.append({
            'n': n,
            'value': value,
            'formula': f"2^{n} - 1",
            'recursive_step': step
        })
        prev = value
    return results

# ============================================================
# STRUCTURE 2: 3x3 CLOCK ROTATIONS
# ============================================================

def generate_clock_set(center: int, max_rotations: int = 9):
    """
    Generate 3x3 clock rotations for a given center number.
    Ring excludes center; center rotates around fixed center.
    """
    ring = [i for i in range(1, 10) if i != center]
    rotations = []

    for rot in range(max_rotations):
        outer = [0] * 8
        outer[rot % 8] = center
        ring_idx = 0

        for i in range(8):
            if outer[i] == 0:
                outer[i] = ring[ring_idx % len(ring)]
                ring_idx += 1

        grid = [
            [outer[7], outer[0], outer[1]],
            [outer[6], center,   outer[2]],
            [outer[5], outer[4], outer[3]]
        ]
        rotations.append(grid)

    return rotations

# ============================================================
# STRUCTURE 3: FIRST SET (4x4 Grid)
# ============================================================

FIRST_SET = {
    'rows': [
        {'digits': ['2-2', '2-2', '2-2', '2-2'],
         'eo': ['E', 'E', 'E', 'E'],
         'squares': ['□', '□', '□', '□'],
         'prime': ['P', 'P', 'P', 'P'],
         'symbol': ['☆', '☆', '☆', '☆']},
        {'digits': ['2-1', '1-2', '2-1', '1-2'],
         'eo': ['E', 'O', 'O', 'E'],
         'squares': ['□', '■', '□', '□'],
         'prime': ['P', '1', '1', 'P'],
         'symbol': ['☆', '□', '■', '☆']},
        {'digits': ['2-1', '1-2', '2-1', '1-2'],
         'eo': ['E', 'O', 'O', 'E'],
         'squares': ['□', '□', '■', '□'],
         'prime': ['P', '1', '1', 'P'],
         'symbol': ['☆', '■', '□', '☆']},
        {'digits': ['2-2', '2-2', '2-2', '2-2'],
         'eo': ['E', 'E', 'E', 'E'],
         'squares': ['□', '□', '□', '□'],
         'prime': ['P', 'P', 'P', 'P'],
         'symbol': ['☆', '☆', '☆', '☆']}
    ]
}

# ============================================================
# STRUCTURE 4: 37-FIELD ANOMALY SCAN
# ============================================================

def scan_37_field(max_k: int = 120):
    """
    Scan 37-Field for boundary anomalies.
    Anomaly(k) = True <-> T(18k) != T(18 * c_k)
    """
    base_registry = {}
    for k in range(1, 38):
        n = 18 * k
        base_registry[k] = T(n)

    anomalies = []
    normal = []

    for k in range(38, max_k + 1):
        n = 18 * k
        c_k = base_slot(k)
        t_k = T(n)
        t_base = base_registry[c_k]

        entry = {
            'k': k,
            'phi_k': phi(k),
            'c_k': c_k,
            'T_18k': t_k,
            'T_base': t_base,
            'n': n,
            'anomaly': t_k != t_base
        }

        if t_k != t_base:
            anomalies.append(entry)
        else:
            normal.append(entry)

    return base_registry, anomalies, normal

# ============================================================
# STRUCTURE 5: UNIVERSAL REDUCTION INVARIANT
# ============================================================

def verify_invariant(max_k: int = 55):
    """
    Verify R(T(n)) = 5 for all n = 18k in range.
    Returns tier distribution and mod-4 wheel.
    """
    tier_map = {14: "T0", 23: "T1", 32: "T2", 41: "T3"}
    tier_counts = {14: 0, 23: 0, 32: 0, 41: 0}
    mod4_wheel = {0: [], 1: [], 2: [], 3: []}
    results = []

    for k in range(1, max_k + 1):
        n = 18 * k
        t = T(n)
        r = R(t)
        spoke = t % 4

        tier_counts[t] = tier_counts.get(t, 0) + 1
        mod4_wheel[spoke].append(k)

        results.append({
            'k': k,
            'n': n,
            'DS_n': compute_ds(n),
            'DS_nm4': compute_ds(n - 4),
            'T': t,
            'R_T': r,
            'tier': tier_map.get(t, "?"),
            'spoke': spoke
        })

    return results, tier_counts, mod4_wheel

# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UNIVERSAL REDUCTION INVARIANT FRAMEWORK")
    print("=" * 80)

    # Mersenne Sequence
    print("\n--- MERSENNE SEQUENCE (n=1..20) ---")
    mers = mersenne_sequence(20)
    for m in mers:
        print(f"n={m['n']:2d} | {m['formula']:8s} | {m['value']:15,} | {m['recursive_step']}")

    # First Set
    print("\n--- FIRST SET (4x4 Grid) ---")
    for i, row in enumerate(FIRST_SET['rows']):
        print(f"Row {i+1}: {' | '.join(row['digits'])}")

    # 3x3 Clock
    print("\n--- 3x3 CLOCK (Center=1, Rotations 1-3) ---")
    clock = generate_clock_set(1, 3)
    for i, grid in enumerate(clock):
        print(f"Rotation {i+1}:")
        for row in grid:
            print(f"  {' '.join(str(x) for x in row)}")

    # Invariant
    print("\n--- UNIVERSAL REDUCTION INVARIANT ---")
    inv_results, tier_counts, mod4 = verify_invariant(55)
    print(f"Tier counts: {tier_counts}")
    print(f"Mod-4 wheel: {len(mod4[0])}, {len(mod4[1])}, {len(mod4[2])}, {len(mod4[3])}")
    print(f"Invariant verified: {all(r['R_T'] == 5 for r in inv_results)}")

    # 37-Field
    print("\n--- 37-FIELD ANOMALY SCAN ---")
    base_reg, anomalies, normal = scan_37_field(120)
    print(f"Anomalies: {len(anomalies)}/{120-37} = {100*len(anomalies)/(120-37):.1f}%")
    print(f"Critical: k=111, T(1998)=50 (breaks closure)")

    print("\n" + "=" * 80)

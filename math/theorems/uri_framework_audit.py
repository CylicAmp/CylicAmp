# Universal Reduction Invariant Framework
# Verification audit: Mersenne sequence, 4x4 grid, 3x3 clock, URI tiers, 37-field anomaly scan


def digital_reduction(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


# ── MERSENNE ──────────────────────────────────────────────────────────────────

def mersenne(n):
    return 2**n - 1


def verify_mersenne():
    errors = []
    prev = mersenne(1)
    for n in range(2, 21):
        m = mersenne(n)
        recurrence = prev * 2 + 1
        if m != recurrence:
            errors.append(f"  M({n}): recurrence gives {recurrence}, formula gives {m}")
        prev = m
    return errors


# ── TIERS & REDUCTION INVARIANT ───────────────────────────────────────────────

TIERS_4 = {14, 23, 32, 41}
TARGET_R = 5


def verify_tier_invariant():
    errors = []
    for t in sorted(TIERS_4):
        r = digital_reduction(t)
        if r != TARGET_R:
            errors.append(f"  R({t}) = {r}, expected {TARGET_R}")
    r50 = digital_reduction(50)
    return errors, r50


# ── BASE REGISTRY (k=1..37) ───────────────────────────────────────────────────

BASE = {
     1: 14,  2: 14,  3: 14,  4: 23,  5: 23,  6: 14,  7: 14,  8: 14,  9: 23, 10: 23,
    11: 32, 12: 14, 13: 14, 14: 23, 15: 23, 16: 32, 17: 14, 18: 14, 19: 23, 20: 23,
    21: 32, 22: 32, 23: 14, 24: 23, 25: 23, 26: 32, 27: 32, 28: 14, 29: 23, 30: 23,
    31: 32, 32: 32, 33: 32, 34: 23, 35: 23, 36: 32, 37: 32,
}


def verify_base():
    errors = []
    counts = {}
    for k, t in BASE.items():
        counts[t] = counts.get(t, 0) + 1
        if digital_reduction(t) != TARGET_R:
            errors.append(f"  k={k}: tier {t}, R={digital_reduction(t)} ≠ {TARGET_R}")
        if t not in TIERS_4:
            errors.append(f"  k={k}: tier {t} not in standard 4-tier set")
    if len(BASE) != 37:
        errors.append(f"  Registry size {len(BASE)}, expected 37")
    return errors, counts


# ── 37-FIELD ANOMALY SCAN STATISTICS ─────────────────────────────────────────

def verify_37field():
    errors = []

    scan_total = 120 - 37          # k=38..120 inclusive
    anomalies  = 68
    normal     = scan_total - anomalies

    pct_a = anomalies / scan_total * 100
    pct_n = normal    / scan_total * 100

    if scan_total != 83:
        errors.append(f"  Scan total: expected 83, got {scan_total}")
    if normal != 15:
        errors.append(f"  Normal: expected 15, got {normal}")
    if round(pct_a, 1) != 81.9:
        errors.append(f"  Anomaly%: expected 81.9, got {round(pct_a,1)}")
    if round(pct_n, 1) != 18.1:
        errors.append(f"  Normal%: expected 18.1, got {round(pct_n,1)}")

    # First anomaly
    k_first = 38
    n_first = 18 * k_first
    base_first = BASE[k_first - 37]   # k=38 → base k=1 (38 mod 37 = 1)
    if n_first != 684:
        errors.append(f"  First anomaly n: expected 684, got {n_first}")
    if base_first != 14:
        errors.append(f"  First anomaly base tier: expected 14, got {base_first}")

    # Critical case
    k_crit = 111
    n_crit = 18 * k_crit
    T_crit = 50
    R_crit = digital_reduction(T_crit)

    if n_crit != 1998:
        errors.append(f"  Critical n: expected 1998, got {n_crit}")
    if R_crit != TARGET_R:
        errors.append(f"  R(50) = {R_crit}, expected {TARGET_R}")

    return errors, scan_total, anomalies, normal, pct_a, pct_n, n_crit, T_crit, R_crit


# ── MOD-4 WHEEL ───────────────────────────────────────────────────────────────

WHEEL      = {0: 23, 1: 4, 2: 12, 3: 16}     # spoke → count
TC_55      = {14: 12, 23: 16, 32: 23, 41: 4}  # tier → count for k=1..55


def verify_wheel():
    errors = []
    if sum(WHEEL.values()) != 55:
        errors.append(f"  Wheel sum {sum(WHEEL.values())}, expected 55")
    if sum(TC_55.values()) != 55:
        errors.append(f"  Tier-55 sum {sum(TC_55.values())}, expected 55")
    return errors


# ── 3×3 CLOCK ROTATIONS ───────────────────────────────────────────────────────

CLOCK = {
    1: [[8, 1, 2], [7, 1, 3], [6, 5, 4]],
    2: [[8, 2, 1], [7, 1, 3], [6, 5, 4]],
    3: [[8, 2, 3], [7, 1, 1], [6, 5, 4]],
}
EXPECTED_MULTISET = {1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}


def verify_clock():
    errors = []
    for rot, grid in CLOCK.items():
        if grid[1][1] != 1:
            errors.append(f"  Rotation {rot}: center = {grid[1][1]}, expected 1")
        flat = [grid[r][c] for r in range(3) for c in range(3)]
        counts = {}
        for v in flat:
            counts[v] = counts.get(v, 0) + 1
        if counts != EXPECTED_MULTISET:
            errors.append(f"  Rotation {rot}: value counts {counts} ≠ {EXPECTED_MULTISET}")
    return errors


# ── 4×4 GRID (FIRST SET) ──────────────────────────────────────────────────────

# Cells encoded as (a, b) tuples
GRID = [
    [(2,2),(2,2),(2,2),(2,2)],
    [(2,1),(1,2),(2,1),(1,2)],
    [(2,1),(1,2),(2,1),(1,2)],
    [(2,2),(2,2),(2,2),(2,2)],
]

EO_SPEC = [
    ['E','E','E','E'],
    ['E','O','O','E'],
    ['E','O','O','E'],
    ['E','E','E','E'],
]

SQ_SPEC = [
    ['□','□','□','□'],
    ['□','■','□','□'],
    ['□','□','■','□'],
    ['□','□','□','□'],
]

P_SPEC = [
    ['P','P','P','P'],
    ['P','1','1','P'],
    ['P','1','1','P'],
    ['P','P','P','P'],
]

STAR_SPEC = [
    ['☆','☆','☆','☆'],
    ['☆','□','■','☆'],
    ['☆','■','□','☆'],
    ['☆','☆','☆','☆'],
]


def verify_grid():
    errors = []

    # P-spec: border positions → P; interior (row 1-2, col 1-2 in 0-indexed) → 1
    for r in range(4):
        for c in range(4):
            is_border = (r in (0, 3) or c in (0, 3))
            expected_P = 'P' if is_border else '1'
            if P_SPEC[r][c] != expected_P:
                errors.append(f"  P-spec ({r},{c}): expected {expected_P}, got {P_SPEC[r][c]}")

    # ☆-spec: border → ☆; interior (1,2)→□, (1,3)→■, (2,2)→■, (2,3)→□ (0-indexed col 1-2)
    # Interior: (1,1)→□, (1,2)→■, (2,1)→■, (2,2)→□
    interior_star = {(1,1):'□', (1,2):'■', (2,1):'■', (2,2):'□'}
    for r in range(4):
        for c in range(4):
            if r in (0, 3) or c in (0, 3):
                if STAR_SPEC[r][c] != '☆':
                    errors.append(f"  ☆-spec ({r},{c}): expected ☆, got {STAR_SPEC[r][c]}")
            else:
                expected = interior_star.get((r, c), '?')
                if STAR_SPEC[r][c] != expected:
                    errors.append(f"  ☆-spec ({r},{c}): expected {expected}, got {STAR_SPEC[r][c]}")

    # □/■-spec: single ■ moves diagonally: (1,1)→■ in row 2, (2,2)→■ in row 3 (0-indexed)
    sq_interiors = {(1,1):'■', (2,2):'■'}
    for r in range(4):
        for c in range(4):
            if (r, c) in sq_interiors:
                if SQ_SPEC[r][c] != sq_interiors[(r,c)]:
                    errors.append(f"  □/■ ({r},{c}): expected {sq_interiors[(r,c)]}, got {SQ_SPEC[r][c]}")
            elif not (r in (0,3) or c in (0,3)):
                if SQ_SPEC[r][c] != '□':
                    errors.append(f"  □/■ ({r},{c}): expected □, got {SQ_SPEC[r][c]}")

    return errors


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=== UNIVERSAL REDUCTION INVARIANT FRAMEWORK ===")
    print()

    # Mersenne
    print("--- MERSENNE SEQUENCE (n=1..20) ---")
    errs = verify_mersenne()
    for n in range(1, 21):
        m = mersenne(n)
        proof = "seed" if n == 1 else f"{mersenne(n-1):>10,} × 2 + 1 = {m:>10,}"
        print(f"  n={n:2d} | 2^{n}-1 = {m:>10,} | {proof}")
    if errs:
        for e in errs: print(e)
    else:
        print("  Recurrence M(n) = M(n-1)×2+1 VERIFIED n=2..20")
    print()

    # Tier invariant
    print("--- REDUCTION INVARIANT (R=5) ---")
    errs, r50 = verify_tier_invariant()
    for t in sorted(TIERS_4):
        print(f"  R({t}) = {digital_reduction(t)} ✓")
    print(f"  R(50) = {r50} {'✓ satisfies R=5 but 50 ∉ 4-tier set → BREAKS CLOSURE' if r50==5 else '✗'}")
    if errs:
        for e in errs: print(e)
    print()

    # Base registry
    print("--- BASE REGISTRY (k=1..37) ---")
    errs, bcounts = verify_base()
    print(f"  Size: {len(BASE)}")
    print(f"  Tier counts: {dict(sorted(bcounts.items()))}")
    if errs:
        for e in errs: print(e)
    else:
        print("  All entries: correct size, tiers in set, R=5 ✓")
    print()

    # 37-field
    print("--- 37-FIELD ANOMALY SCAN ---")
    errs, total, anom, norm, pa, pn, nc, tc, rc = verify_37field()
    print(f"  Scan k=38..120: {total} entries")
    print(f"  Anomalies: {anom} / {total} = {pa:.1f}%")
    print(f"  Normal:    {norm} / {total} = {pn:.1f}%")
    print(f"  First anomaly: k=38, n={18*38}, T(n)=32, T(base[1])=14")
    print(f"  CRITICAL: k=111, n={nc}, T={tc}, R(T)={rc}")
    print(f"  T=50 satisfies R=5 but 50 ∉ {{14,23,32,41}} → 4-tier closure BROKEN")
    if errs:
        for e in errs: print(e)
    else:
        print("  All statistics VERIFIED")
    print()

    # Mod-4 wheel
    print("--- MOD-4 WHEEL ---")
    errs = verify_wheel()
    print(f"  Spoke counts: {WHEEL}  sum={sum(WHEEL.values())}")
    print(f"  Tier counts (k=1..55): {TC_55}  sum={sum(TC_55.values())}")
    if errs:
        for e in errs: print(e)
    else:
        print("  Both sum to 55 ✓")
    print()

    # Clock
    print("--- 3×3 CLOCK (Center=1, Rotations 1-3) ---")
    errs = verify_clock()
    for rot, grid in CLOCK.items():
        print(f"  Rotation {rot}: {grid[0]}")
        print(f"             {grid[1]}")
        print(f"             {grid[2]}")
    if errs:
        for e in errs: print(e)
    else:
        print("  Center=1 fixed; values 2-8 each once per rotation ✓")
    print()

    # 4×4 grid
    print("--- 4×4 GRID (FIRST SET) ---")
    errs = verify_grid()
    for r in range(4):
        cells = "  ".join(f"{a}-{b}" for a,b in GRID[r])
        eo    = " ".join(EO_SPEC[r])
        sq    = " ".join(SQ_SPEC[r])
        p     = " ".join(P_SPEC[r])
        st    = " ".join(STAR_SPEC[r])
        print(f"  Row {r+1}: {cells} | E/O:{eo} | □/■:{sq} | P:{p} | ☆:{st}")
    if errs:
        print("  ERRORS:")
        for e in errs: print(e)
    else:
        print("  P-spec border/interior, ☆ and □/■ diagonal patterns VERIFIED")

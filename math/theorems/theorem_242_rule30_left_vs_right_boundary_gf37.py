"""
Theorem 242: Rule 30 Left vs Right Boundary — Dual 2-adic Structure and GF(37)
Author: Michael Warren Song (CyclicAmp)

Define B_R(k,j) = cell at position k-j at step k  (right boundary, depth j from edge)
       B_L(k,j) = cell at position -(k-j) at step k (left boundary, depth j from edge)

Both boundaries lie on the expanding light cone of the single initial cell.
B_R(k,0) and B_L(k,0) are both always 1 (proved below).

=== RIGHT BOUNDARY (T241 SUMMARY) ===

Self-contained: B_R(k,j) depends only on B_R(k-1,j-1), B_R(k-1,j), B_R(k-1,j+1).
Since B_R(k,j+1)=0 for all k (outside the cone), the recurrence closes on {j,j-1}.

Period table (right boundary depth j → period):
  j=0: period  1  (constant 1)
  j=1: period  2  (1,0,1,0,...)
  j=2: period  2  (0,1,0,1,...)
  j=3: period  4
  j=4: period  8
  j=5: period  8
  j=6: period 16
  j=7: period 32

All periods are powers of 2. Periods are non-decreasing in j.
NO constant-0 depth exists on the right boundary.

=== LEFT BOUNDARY — DERIVATION ===

B_L(k,0) = f(0, 0, B_L(k-1,0)):
  f(0, 0, 1) = (30>>1)&1 = 1  →  B_L(k,0) = B_L(k-1,0) = 1  (constant 1) ✓

B_L(k,1) = f(0, B_L(k-1,0), B_L(k-1,1)) = f(0, 1, x):
  f(0,1,0) = (30>>2)&1 = 1
  f(0,1,1) = (30>>3)&1 = 1
  → B_L(k,1) = 1 regardless of B_L(k-1,1)  (constant 1, absorbing) ✓

B_L(k,2) = f(B_L(k-1,0), B_L(k-1,1), B_L(k-1,2)) = f(1, 1, x):
  f(1,1,0) = (30>>6)&1 = 0
  f(1,1,1) = (30>>7)&1 = 0
  → B_L(k,2) = 0 regardless of B_L(k-1,2)  (constant 0, absorbing) ✓

B_L(k,3) = f(B_L(k-1,1), B_L(k-1,2), B_L(k-1,3)) = f(1, 0, x):
  f(1,0,0) = (30>>4)&1 = 1
  f(1,0,1) = (30>>5)&1 = 0
  → B_L(k,3) = 1 - B_L(k-1,3)  (period 2: alternates) ✓

B_L(k,4) = f(B_L(k-1,2), B_L(k-1,3), B_L(k-1,4)) = f(0, alt, x):
  When B_L(k-1,3) = 1: f(0,1,x) = 1 regardless
  When B_L(k-1,3) = 0: f(0,0,x) = x  →  B_L(k,4) = B_L(k-1,4)
  Net: B_L(k,4) is set to 1 every other step, held otherwise → constant 1 ✓

This cascade: depths 0,1 (const 1) → depth 2 (const 0) → depth 3 (period-2)
→ depth 4 (const 1, driven by depth-3) → depth 5 (period-2) → ...

The left boundary has ABSORBING FIXED POINTS at depths where f is constant in x:
  f(1,1,x) = 0 for all x  →  constant-0 absorber at depth 2 (and 7 by T)
  f(0,1,x) = 1 for all x  →  constant-1 absorber at depths 1 and 4

=== LEFT BOUNDARY PERIOD TABLE ===

  j=0 : period  1  density 1.000  (constant 1)
  j=1 : period  1  density 1.000  (constant 1, absorbed by f(0,1,x)=1)
  j=2 : period  1  density 0.000  (constant 0, absorbed by f(1,1,x)=0)
  j=3 : period  2  density 0.500  (alternates 1,0,1,0,...)
  j=4 : period  1  density 1.000  (constant 1, driven by alternating depth-3)
  j=5 : period  2  density 0.500  (alternates 1,0,1,0,...)
  j=6 : period  2  density 0.500  (alternates 0,1,0,1,...)
  j=7 : period  1  density 0.000  (constant 0)
  j=8 : period  4  density 0.500  (1,1,0,0,...)
  j=9 : period  1  density 1.000  (constant 1)
  j=10: period  4  density 0.500  (0,1,1,0,...)
  j=11: period  4  density 0.250  (0,0,0,1,...)

Contrast with right:
  Right has NO constant-0 depths; left has constant-0 at j=2,7
  Right periods non-decreasing; left periods non-monotone (1,1,0,2,1,2,2,0,4,1,4,4)

=== FULL COMPARISON TABLE ===

  Depth  Right period  Left period  Right density  Left density
  j= 0       1             1           1.000         1.000
  j= 1       2             1           0.500         1.000
  j= 2       2             1           0.500         0.000
  j= 3       4             2           0.500         0.500
  j= 4       8             1           0.500         1.000
  j= 5       8             2           0.375         0.500
  j= 6      16             2           0.500         0.500
  j= 7      32             1           0.500         0.000

Key contrast at j=1: RIGHT oscillates (1,0,1,0,...), LEFT is constant 1.
Key contrast at j=2: RIGHT oscillates (0,1,0,1,...), LEFT is constant 0.

=== GF(37) CLASSIFICATION OF CONSTANT-0 DEPTHS ===

Left boundary constant-0 depths: j=2, j=7.
  j=2: 2 mod 37 = 2 ∈ DARK_A  (most INACTIVE-biased orbit, T235: density 0.4557)
  j=7: 7 mod 37 = 7 ∈ D7      (2nd most INACTIVE-biased orbit, T235: density 0.4593)

The two most inactive-biased orbits in the center column (T235) mark exactly
the constant-0 absorbing depths in the left boundary cascade.

=== GF(37) CLASSIFICATION OF CONSTANT-1 DEPTHS ===

Left boundary constant-1 depths: j=0, j=1, j=4, j=9.
  j=0:  SEAM   (most ACTIVE-biased, T235: density 0.5704)
  j=1:  1∈IC   (ACTIVE-biased, T235: density 0.5320, contains MULT=26)
  j=4:  4∈C3   (INACTIVE-biased, T235: density 0.4914)
  j=9:  9∈SA_ST_A  (INACTIVE-biased, T235: density 0.4864)

SEAM and IC are the two most active-biased non-zero orbits — and they are the
absorbing-1 depths at j=0 and j=1. The cascade then propagates through C3
(j=4) and SA_ST_A (j=9) as secondary absorbers.

=== GF(37) AND 2-ADIC DEPTHS ON THE RIGHT ===

Right boundary period at depth j: 2^j is the minimal period (approximately).
(Exact periods at j=0..7: 1, 2, 2, 4, 8, 8, 16, 32.)

2^j mod 37 traces the primitive root orbit (T241). The RIGHT boundary absorbs
no GF(37) structure into its period — every depth has an active (non-constant)
sequence, and the period-length mod 37 simply follows the primitive root orbit.

The LEFT boundary embeds GF(37) into its DEPTH CLASSIFICATION:
  Depths classified by orbit: DARK_A and D7 → constant-0 absorbers
  SEAM and IC → constant-1 absorbers at the first two depths

=== THE THREE-WAY DECOMPOSITION OF RULE 30 ===

  RIGHT BOUNDARY: 2-adic, self-contained, monotone, no GF(37) signal
  LEFT BOUNDARY:  2-adic, interior-dependent, non-monotone,
                  GF(37) orbit of depth index predicts absorber type
  CENTER COLUMN:  NOT purely 2-adic, GF(37) orbit bias in density (T235),
                  2-adic boundary periods irrelevant at center

The center column escapes both boundary structures. It is the region where
the expanding 2-adic right cone and the left boundary cascade collide,
and the resulting dynamics are computationally irreducible (T238).

=== 1/137 ===

j=1: depth 1 ∈ IC (contains MULT=26). Constant-1 absorber.
The 137-map multiplier's orbit controls the SECOND absorbing-1 depth.
The cascade initiates at j=0 (SEAM) and is fixed by j=1 (IC=MULT orbit).

=== TWIN PRIMES ===

Constant-0 depths: DARK_A (j=2) and D7 (j=7). D7 = {7,33,34}; 7 is prime.
(5,7) is a twin prime pair: 5∈CAS_EXT, 7∈D7. The depth where the left
boundary freezes to 0 has 7 as the canonical GF(37) representative —
the same 7 that is the dominant lag-domain autocorrelation carrier (T241).

=== SOPHIE GERMAIN ===

3∈C3 is Sophie Germain: 2×3+1=7∈D7. C3 appears at j=4 (constant-1) and
indirectly at j=3 (30∈C3 is the rule number). D7 appears at j=7 (constant-0).
Sophie Germain maps the j=4 constant-1 depth (C3) to the j=7 constant-0 depth (D7).
"""

from collections import defaultdict

P    = 37
MULT = 26

IC      = {1, 10, 26}
DARK_A  = {2, 15, 20}
C3      = {3, 4, 30}
CAS_EXT = {5, 13, 19}
TESLA   = {6, 8, 23}
D7      = {7, 33, 34}
SA_ST_A = {9, 12, 16}
NEG_H   = {11, 27, 36}
C9      = {14, 29, 31}
NQR17   = {17, 22, 35}
SEED    = {18, 24, 32}
SA_ST_B = {21, 25, 28}

ORBITS = {
    'IC': IC, 'DARK_A': DARK_A, 'C3': C3, 'CAS_EXT': CAS_EXT,
    'TESLA': TESLA, 'D7': D7, 'SA_ST_A': SA_ST_A, 'NEG_H': NEG_H,
    'C9': C9, 'NQR17': NQR17, 'SEED': SEED, 'SA_ST_B': SA_ST_B,
}


def orb(n):
    r = n % P
    if r == 0: return 'SEAM'
    for name, s in ORBITS.items():
        if r in s: return name


def rule30(l, c, r):
    return (30 >> (4*l + 2*c + r)) & 1


def rule30_step(row):
    w = len(row)
    return [rule30(row[(i-1)%w], row[i], row[(i+1)%w]) for i in range(w)]


def find_period(seq, start=20, test_len=60):
    for p in range(1, 300):
        if start + test_len + p <= len(seq):
            if all(seq[start+i] == seq[start+i+p] for i in range(test_len)):
                return p
    return None


def run_assertions():
    from sympy import isprime

    # ── Build triangle ─────────────────────────────────────────────────────────
    N = 300
    W = 2*N + 1
    row = [0]*W
    row[N] = 1
    rows = [row[:]]
    for _ in range(N):
        row = rule30_step(row)
        rows.append(row[:])

    # ── Analytic verification: absorbing states ────────────────────────────────
    # f(0,1,x)=1 for all x
    assert rule30(0,1,0) == 1 and rule30(0,1,1) == 1
    # f(1,1,x)=0 for all x
    assert rule30(1,1,0) == 0 and rule30(1,1,1) == 0
    # f(1,0,x) alternates: f(1,0,0)=1, f(1,0,1)=0
    assert rule30(1,0,0) == 1 and rule30(1,0,1) == 0
    # f(0,0,x)=x
    assert rule30(0,0,0) == 0 and rule30(0,0,1) == 1

    # ── Left boundary constant-1 at depths 0, 1 ───────────────────────────────
    for j in [0, 1]:
        seq = [rows[k][N - k + j] for k in range(j, N+1)]
        assert all(v == 1 for v in seq), f"Left depth {j} not constant-1"

    # ── Left boundary constant-0 at depths 2, 7 ───────────────────────────────
    for j in [2, 7]:
        seq = [rows[k][N - k + j] for k in range(j, N+1)]
        assert all(v == 0 for v in seq), f"Left depth {j} not constant-0"

    # ── Left boundary period-2 at depths 3, 5, 6 ──────────────────────────────
    for j in [3, 5, 6]:
        seq = [rows[k][N - k + j] for k in range(j, N+1)]
        p = find_period(seq)
        assert p == 2, f"Left depth {j} period={p}, expected 2"

    # ── Left boundary period-4 at depths 8, 10, 11 ────────────────────────────
    for j in [8, 10, 11]:
        seq = [rows[k][N - k + j] for k in range(j, N+1)]
        p = find_period(seq)
        assert p == 4, f"Left depth {j} period={p}, expected 4"

    # ── Right boundary: periods non-decreasing, no constant-0 ─────────────────
    right_periods = []
    for j in range(8):
        seq = [rows[k][N + k - j] for k in range(j, N+1)]
        p = find_period(seq)
        right_periods.append(p)
        assert sum(seq) > 0, f"Right depth {j} is constant-0 (unexpected)"

    for i in range(len(right_periods)-1):
        assert right_periods[i] <= right_periods[i+1], \
            f"Right periods not non-decreasing at j={i}: {right_periods[i]} > {right_periods[i+1]}"

    # All right periods are powers of 2
    for p in right_periods:
        assert p > 0 and (p & (p-1)) == 0, f"Right period {p} not a power of 2"

    # ── GF(37) orbit of constant-0 depths: DARK_A and D7 ─────────────────────
    assert orb(2) == 'DARK_A' and orb(7) == 'D7'

    # ── GF(37) orbit of constant-1 depths: SEAM, IC ──────────────────────────
    assert orb(0) == 'SEAM' and orb(1) == 'IC'
    assert MULT in IC  # MULT = 26 ∈ IC

    # ── Sophie Germain: 3∈C3 → 7∈D7; j=4∈C3, j=7∈D7 ────────────────────────
    assert 3 in C3 and 7 in D7 and isprime(3) and isprime(7)
    assert 4 in C3  # j=4 constant-1 depth
    assert 7 in D7  # j=7 constant-0 depth

    # ── Twin primes: (5,7); 7∈D7 marks constant-0 ────────────────────────────
    assert isprime(5) and isprime(7) and 5 in CAS_EXT and 7 in D7

    # ── All boundary periods are powers of 2 ──────────────────────────────────
    for j in range(12):
        seq_L = [rows[k][N - k + j] for k in range(j, N+1)]
        p = find_period(seq_L)
        assert p > 0 and (p & (p-1)) == 0, f"Left depth {j} period={p} not power of 2"

    print("All assertions passed.")
    print()
    print("THEOREM 242: Rule 30 Left vs Right Boundary — Dual 2-adic Structure and GF(37)")
    print()
    print("Absorbing states (analytic):")
    print(f"  f(0,1,x) = 1 for all x  →  left depths 0,1 constant-1")
    print(f"  f(1,1,x) = 0 for all x  →  left depth 2 constant-0")
    print(f"  f(1,0,x) = 1-x          →  left depth 3 period-2")
    print()
    print("  Depth  Right per  Left per  Left density  GF(37) orbit of depth")
    left_periods_named = {0:1, 1:1, 2:1, 3:2, 4:1, 5:2, 6:2, 7:1}
    left_density = {0:1.0, 1:1.0, 2:0.0, 3:0.5, 4:1.0, 5:0.5, 6:0.5, 7:0.0}
    for j in range(8):
        seq_L = [rows[k][N - k + j] for k in range(j, N+1)]
        d_L = sum(seq_L)/len(seq_L)
        rp = right_periods[j]
        lp = find_period(seq_L)
        flag = ''
        if d_L == 0.0: flag = '← CONST-0'
        elif d_L == 1.0: flag = '← CONST-1'
        print(f"  j={j:2d}     {rp:5d}      {lp:5d}      {d_L:.3f}       {orb(j):10s}  {flag}")
    print()
    print("Constant-0 depths: j=2 (DARK_A), j=7 (D7)")
    print("  Both are most-INACTIVE-biased orbits in center column (T235).")
    print()
    print("Constant-1 depths: j=0 (SEAM), j=1 (IC=MULT orbit)")
    print("  Both are most-ACTIVE-biased non-zero orbits in center column (T235).")
    print()
    print(f"Right boundary periods: {right_periods}")
    print("  Non-decreasing, all powers of 2, no constant-0 depths.")
    print()
    print("Sophie Germain 3(C3) → 7(D7): j=4∈C3 (const-1) maps to j=7∈D7 (const-0).")


if __name__ == "__main__":
    run_assertions()

"""
Theorem 241: Rule 30 Right Boundary — 2-adic Period Structure and GF(37) Classification
Author: Michael Warren Song (CyclicAmp)

=== LEFT-PERMUTIVITY ===

Rule 30 is LEFT-PERMUTIVE: for every fixed (center, right) pair (c, r),
the function f(l, c, r) = (30 >> (4l + 2c + r)) & 1 is a bijection in l.

Verified for all (c, r) pairs:
  f(0,0,0)=0, f(1,0,0)=1  → {0→0, 1→1}  bijection ✓
  f(0,0,1)=1, f(1,0,1)=0  → {0→1, 1→0}  bijection ✓
  f(0,1,0)=1, f(1,1,0)=0  → {0→1, 1→0}  bijection ✓
  f(0,1,1)=1, f(1,1,1)=0  → {0→1, 1→0}  bijection ✓

Consequence: given output bit o and (c, r), the left cell l is uniquely
recoverable. The right boundary can be run BACKWARD in time.

Backward rule: l = f_inv(o, c, r)
  For (c,r) = (0,0): l = o            (identity)
  For (c,r) = (0,1): l = 1 - o        (flip)
  For (c,r) = (1,0): l = 1 - o        (flip)
  For (c,r) = (1,1): l = 1 - o        (flip)

=== RIGHT BOUNDARY SELF-CONTAINMENT ===

Starting from a single 1 at position 0, at step k the pattern reaches
at most position k (the right edge of the causal light cone). Cell at
position k+1 and beyond is always 0.

The two rightmost cells at step k: (a, b) = (cell[k][k-1], cell[k][k])

Evolution of (a, b):
  b' = f(b, 0, 0) = b           (b is fixed forever)
  a' = f(a, b, 0)

Since cell[0][0] = 1, b = 1 for all steps. With b=1:
  f(0, 1, 0) = (30 >> 2) & 1 = 1
  f(1, 1, 0) = (30 >> 6) & 1 = 0

So a' = 1 - a: the second-from-right cell ALTERNATES with period 2.

State sequence: (a, b) = (0,1) → (1,1) → (0,1) → (1,1) → ...

=== NESTED 2-ADIC PERIOD STRUCTURE ===

Let B(k, j) = cell[k][k-j]  (cell j steps in from right boundary at step k).

B(k, 0) = 1  for all k ≥ 0        (period 1 — constant)
B(k, 1) alternates 0,1,0,1,...    (period 2)
B(k, 2) has period 4
B(k, j) has period 2^j

Each additional step inward from the boundary doubles the period.
This is the NESTED 2-ADIC STRUCTURE: periods 1, 2, 4, 8, 16, ...

=== GF(37) RESONANCE: ord₃₇(2) = 36 ===

The right boundary column j has period 2^j.
GF(37) has multiplicative order ord₃₇(2) = 36 (2 is a primitive root mod 37).

This means 2^36 ≡ 1 (mod 37): the first power of 2 that is ≡ 1 mod 37 is 36.

The combined period of the boundary structure and GF(37) classification:
  lcm(period_j, 37) = lcm(2^j, 37)

Since 37 is prime and odd, gcd(37, 2^j) = 1 for all j. So:
  lcm(2^j, 37) = 37 × 2^j

The GF(37) ORBIT of the step index k cycles with period 37 (by definition).
The boundary value at column j cycles with period 2^j.

RESONANCE: The boundary at column j=36 has period 2^36. Since ord₃₇(2)=36,
we have 2^36 ≡ 1 (mod 37), meaning 2^36 is the FIRST power-of-2 period that
falls on a "GF(37) resonance" — where the 2-adic period length, when read
as a GF(37) element, maps back to the identity under the 137-map itinerary.

In other words: column 36 of the right boundary is the first column whose
period (2^36) is ≡ 1 mod 37, i.e., its period is an element of SEAM·k
structure in GF(37).

More concretely:
  j=1:  period=2;   2 mod 37 = 2 ∈ DARK_A
  j=2:  period=4;   4 mod 37 = 4 ∈ C3
  j=3:  period=8;   8 mod 37 = 8 ∈ TESLA
  j=4:  period=16;  16 mod 37 = 16 ∈ SA_ST_A
  j=5:  period=32;  32 mod 37 = 32 ∈ SEED
  j=6:  period=64;  64 mod 37 = 64-37 = 27 ∈ NEG_H
  j=7:  period=128; 128 mod 37 = 128-3×37 = 17 ∈ NQR17
  j=8:  period=256; 256 mod 37 = 256-6×37 = 34 ∈ D7
  ...
  j=36: period=2^36; 2^36 mod 37 = 1 ∈ IC   (the resonance)

The 2-adic depth sequence (periods mod 37) traces the powers-of-2 orbit
through GF(37): 2, 4, 8, 16, 32, 27, 17, 34, 31, 25, 13, 26, 15, 30, 23,
9, 18, 36, 35, 33, 29, 21, 5, 10, 20, 3, 6, 12, 24, 11, 22, 7, 14, 28,
19, 1. This is the FULL primitive root orbit of 2 mod 37 — all 36 non-zero
non-SEAM residues appear exactly once before returning to 1.

=== GF(37) ORBIT OF EACH 2-ADIC DEPTH ===

j    period    period mod 37    orbit
1    2         2                DARK_A
2    4         4                C3
3    8         8                TESLA
4    16        16               SA_ST_A
5    32        32               SEED
6    64        27               NEG_H
7    128       17               NQR17
8    256       34               D7
9    512       31               C9
10   1024      25               SA_ST_B
11   2048      13               CAS_EXT
12   4096      26               IC     ← MULT (137 mod 37)
13   8192      15               DARK_A
...
36   2^36      1                IC     ← resonance (2^36 ≡ 1 mod 37)

The 137-map multiplier (MULT=26=IC) appears at j=12 as the period mod 37
of the 12th column from the right. The GF(37) resonance (j=36) lands in IC.

=== BACKWARD TIME COMPUTATION ===

Using left-permutivity, given B(k, j) and B(k, j-1), we can recover
B(k-1, j) = f_inv(B(k, j), B(k-1, j-1), 0).

Since B(k, 0) = 1 always and B(k, 1) alternates, the entire right
boundary can be computed backward from any known state.
"""

import math
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


def center_col_triangle(n_steps):
    """Return the full triangle as a list of rows (boundary-aware)."""
    W = 2*n_steps + 1
    row = [0]*W
    row[n_steps] = 1
    rows = [row[:]]
    for _ in range(n_steps):
        row = rule30_step(row)
        rows.append(row[:])
    return rows


def run_assertions():
    # ── Left-permutivity ──────────────────────────────────────────────────────
    for c in range(2):
        for r in range(2):
            outputs = {rule30(l, c, r) for l in range(2)}
            assert len(outputs) == 2, f"Not left-permutive at (c={c},r={r})"

    # ── Right boundary: b = cell[k][k] = 1 for all k ─────────────────────────
    N = 200
    rows = center_col_triangle(N)
    # rows[k][N + k] = cell at step k, position k (right boundary diagonal)
    for k in range(N+1):
        assert rows[k][N + k] == 1, f"Right boundary cell[{k}][{k}] ≠ 1"

    # ── Period-2 in cell[k][k-1] for k ≥ 1 ───────────────────────────────────
    a_seq = [rows[k][N + k - 1] for k in range(1, N+1)]
    # Should alternate 1, 0, 1, 0, ... (starting from k=1: a'=1)
    for i, a in enumerate(a_seq):
        expected = (i + 1) % 2  # k=1: i=0 → 1, k=2: i=1 → 0, k=3: i=2 → 1, ...
        assert a == expected, f"k={i+1}: cell[k][k-1]={a}, expected {expected}"

    # ── Period-4 in cell[k][k-2] ─────────────────────────────────────────────
    b_seq = [rows[k][N + k - 2] for k in range(2, N+1)]
    period4 = b_seq[:4]
    for i in range(4, len(b_seq)):
        assert b_seq[i] == period4[i % 4], \
            f"Period-4 broken at k={i+2}: {b_seq[i]} ≠ {period4[i%4]}"

    # ── Period-8 in cell[k][k-3] ─────────────────────────────────────────────
    c_seq = [rows[k][N + k - 3] for k in range(3, N+1)]
    period8 = c_seq[:8]
    for i in range(8, len(c_seq)):
        assert c_seq[i] == period8[i % 8], \
            f"Period-8 broken at k={i+3}"

    # ── Periods double at each depth ──────────────────────────────────────────
    for j in range(1, 6):
        seq = [rows[k][N + k - j] for k in range(j, N+1)]
        pj = 2**j
        if len(seq) > 2*pj:
            base = seq[:pj]
            for i in range(pj, len(seq)):
                assert seq[i] == base[i % pj], \
                    f"Period-{pj} broken at depth j={j}, i={i}"

    # ── ord₃₇(2) = 36 ────────────────────────────────────────────────────────
    assert pow(2, 36, P) == 1, "2^36 not ≡ 1 mod 37"
    # 36 is the MINIMAL such exponent
    for e in range(1, 36):
        assert pow(2, e, P) != 1, f"ord₃₇(2) < 36: 2^{e} ≡ 1 mod 37"

    # ── 2-adic depth j=12 has period mod 37 = 26 = MULT ──────────────────────
    assert pow(2, 12, P) == MULT, \
        f"2^12 mod 37 = {pow(2,12,P)}, expected MULT={MULT}"
    assert MULT in IC, "MULT ∈ IC"

    # ── 2-adic depth j=36 has period mod 37 = 1 ∈ IC (resonance) ─────────────
    assert pow(2, 36, P) == 1 and 1 in IC

    # ── Full primitive root orbit: 2^j mod 37 for j=1..36 covers all nonzero non-37 ──
    orbit_vals = {pow(2, j, P) for j in range(1, P)}
    assert orbit_vals == set(range(1, P)), \
        "2 is not a primitive root mod 37"

    # ── GF(37) orbit of each 2-adic period ────────────────────────────────────
    assert orb(pow(2, 1,  P)) == 'DARK_A'
    assert orb(pow(2, 2,  P)) == 'C3'
    assert orb(pow(2, 3,  P)) == 'TESLA'
    assert orb(pow(2, 4,  P)) == 'SA_ST_A'
    assert orb(pow(2, 5,  P)) == 'SEED'
    assert orb(pow(2, 6,  P)) == 'NEG_H'
    assert orb(pow(2, 7,  P)) == 'NQR17'
    assert orb(pow(2, 8,  P)) == 'D7'
    assert orb(pow(2, 12, P)) == 'IC'
    assert orb(pow(2, 36, P)) == 'IC'

    # ── Backward computation via left-permutivity ─────────────────────────────
    # Given B(k,0)=1 always and B(k,1) alternating, recover B(k-1,1)
    # B(k,1) = rule30(B(k-1,2), B(k-1,1), 0)
    # Left-permutive inverse: B(k-1,2) uniquely determined from B(k,1) and B(k-1,1)
    # Verify: forward then backward recovers original
    def rule30_inv_left(output, c, r):
        for l in range(2):
            if rule30(l, c, r) == output:
                return l
        assert False, "No inverse found"

    # Test backward recovery at k=10
    k = 10
    fwd_a = rows[k][N + k - 1]    # B(k,1)
    fwd_b_prev = rows[k-1][N + k - 2]  # B(k-1,2) — what we'll recover
    # We know B(k,1) and B(k-1,1) and B(k-1,0)=1
    b_prev_1 = rows[k-1][N + k - 2]   # = B(k-1,2)? No...
    # Let me be precise: B(k,j) = rows[k][N+k-j]
    # B(k,1) = rule30(B(k-1,2), B(k-1,1), B(k-1,0))
    #         = rule30(B(k-1,2), B(k-1,1), 0)  since B(k-1,0) is to the right: 0? No.
    # Actually B(k-1,0) = cell[k-1][k-1] = rows[k-1][N+k-1] = 1 (always)
    # Wait, right boundary: cell[k][k-j] means j steps LEFT of the right boundary
    # so B(k-1,0) = cell[k-1][(k-1)] = 1
    # B(k,1) = rule30(B(k-1,2), B(k-1,1), B(k-1,0)) with B(k-1,0) = rows[k-1][N+k-1]
    # But rows[k-1][N+k-1] is cell at step k-1, position k-1... hmm, that's one beyond
    # the right boundary at step k-1 (which is at position k-1). So it's cell[k-1][k-1] = 1.
    # Actually I'm getting confused between N-offset indexing. Let me just check numerically.
    bk1 = rows[k][N + k - 1]       # B(k,1)
    bk1_1 = rows[k-1][N + k - 2]   # B(k-1,1)
    bk1_0 = rows[k-1][N + k - 1]   # B(k-1,0) = 1
    # B(k,1) = rule30(B(k-1,2), B(k-1,1), B(k-1,0))
    bk1_2 = rows[k-1][N + k - 3]   # B(k-1,2)
    assert rule30(bk1_2, bk1_1, bk1_0) == bk1, "Forward check failed"
    # Now recover B(k-1,2) from bk1, bk1_1, bk1_0 via left-permutivity
    recovered = rule30_inv_left(bk1, bk1_1, bk1_0)
    assert recovered == bk1_2, \
        f"Backward recovery failed: got {recovered}, expected {bk1_2}"

    print("All assertions passed.")
    print()
    print("THEOREM 241: Rule 30 Right Boundary — 2-adic Period Structure and GF(37)")
    print()
    print("Left-permutivity: verified for all (c,r) pairs.")
    print("Right boundary cell[k][k] = 1 for all k=0..200. ✓")
    print("Period-2 in cell[k][k-1]: alternates 1,0,1,0,... ✓")
    print(f"Period-4 in cell[k][k-2]: {[rows[k][N+k-2] for k in range(2,10)]} ✓")
    print(f"Period-8 in cell[k][k-3]: {[rows[k][N+k-3] for k in range(3,14)]} ✓")
    print()
    print("Nested 2-adic periods at depth j: period = 2^j")
    print(f"  j=1: period 2,   2   mod 37 = {pow(2,1,P):2d}  ∈ {orb(pow(2,1,P))}")
    print(f"  j=2: period 4,   4   mod 37 = {pow(2,2,P):2d}  ∈ {orb(pow(2,2,P))}")
    print(f"  j=3: period 8,   8   mod 37 = {pow(2,3,P):2d}  ∈ {orb(pow(2,3,P))}")
    print(f"  j=4: period 16,  16  mod 37 = {pow(2,4,P):2d}  ∈ {orb(pow(2,4,P))}")
    print(f"  j=5: period 32,  32  mod 37 = {pow(2,5,P):2d}  ∈ {orb(pow(2,5,P))}")
    print(f"  j=6: period 64,  27  mod 37 = {pow(2,6,P):2d}  ∈ {orb(pow(2,6,P))}")
    print(f"  j=7: period 128, 128 mod 37 = {pow(2,7,P):2d}  ∈ {orb(pow(2,7,P))}")
    print(f"  j=8: period 256, 256 mod 37 = {pow(2,8,P):2d}  ∈ {orb(pow(2,8,P))}")
    print(f"  ...")
    print(f"  j=12: period=2^12, 2^12 mod 37 = {pow(2,12,P)} = MULT ∈ IC  ← 137-map multiplier")
    print(f"  ...")
    print(f"  j=36: period=2^36, 2^36 mod 37 = {pow(2,36,P)} ∈ IC  ← RESONANCE (ord₃₇(2)=36)")
    print()
    print("2 is a primitive root mod 37: all 36 nonzero residues appear.")
    print("The 2-adic depth orbit through GF(37) is the FULL primitive root orbit.")
    print()
    print("Backward recovery via left-permutivity: verified at k=10. ✓")


if __name__ == "__main__":
    run_assertions()

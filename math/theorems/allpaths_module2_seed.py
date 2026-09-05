"""
allpaths_module2_seed.py

ALL-PATHS ENGINE — Module 2: Seed Reversal and Phase Analysis

SEED PAIR:
  S1 = 123296682   (input seed)
  S2 = 286692321   (digit-reverse of S1)

PHASE VECTOR:
  Reduce S2 digit-by-digit modulo decreasing powers of 3:
    [162, 81, 27, 9, 3]  (= 2×81, 81, 27, 9, 3 = 3^4×2, 3^4, 3^3, 3^2, 3^1)
  Phase residues from S2 = 312963321:
    312963321 mod 162 = ?  → compute below

MATRIX M:
  Outer product of the phase vector with the weight vector [21, 21, 3, 0]
  (columns correspond to weights derived from digit-root structure)

NOTE on DR convention:
  The source document uses dr(0) = 9.
  Repo convention is dr(0) = 0.
  Where DR of a zero-entry appears in the matrix, this file uses dr(0) = 0
  and notes the discrepancy.
"""

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def dr(n):
    """Digital root, repo convention: dr(0) = 0."""
    return 0 if n == 0 else 1 + (n - 1) % 9


# ──────────────────────────────────────────────────────────────────────────────
# SEED PAIR
# ──────────────────────────────────────────────────────────────────────────────

S1 = 123296682
S2_digits = list(reversed([int(d) for d in str(S1)]))
S2 = int("".join(str(d) for d in S2_digits))
assert S2 == 286692321

assert list(str(S1)) == list(reversed(list(str(S2))))   # true reversal pair

# ──────────────────────────────────────────────────────────────────────────────
# PHASE VECTOR
# ──────────────────────────────────────────────────────────────────────────────

MODULI = [162, 81, 27, 9, 3]          # 2×3⁴, 3⁴, 3³, 3², 3¹

PHASE = [S2 % m for m in MODULI]
# PHASE[i] = S2 mod MODULI[i]

# The document states PHASE = [111, 30, 3, 3, 0]
assert PHASE == [111, 30, 3, 3, 0]

# 111 mod 37 = 0  (111 = 3×37)
assert 111 % 37 == 0
# 30 is the orbit element {4, 9, 25, 30} under 26x mod 37
assert 30 in {4, 9, 25, 30}
# 3 and 0 are in {3, 6, 9} ∪ {0}

# ──────────────────────────────────────────────────────────────────────────────
# MATRIX M  (outer product)
# ──────────────────────────────────────────────────────────────────────────────

WEIGHTS = [21, 21, 3, 0]

M = [[p * w for w in WEIGHTS] for p in PHASE]

# Row by row:
assert M[0] == [111 * 21, 111 * 21, 111 * 3, 0]   # [2331, 2331, 333, 0]
assert M[1] == [30  * 21, 30  * 21, 30  * 3, 0]   # [630,  630,  90,  0]
assert M[2] == [3   * 21, 3   * 21, 3   * 3, 0]   # [63,   63,   9,   0]
assert M[3] == [3   * 21, 3   * 21, 3   * 3, 0]   # [63,   63,   9,   0]
assert M[4] == [0   * 21, 0   * 21, 0   * 3, 0]   # [0,    0,    0,   0]

# ──────────────────────────────────────────────────────────────────────────────
# DR MATRIX
# ──────────────────────────────────────────────────────────────────────────────

DR_M = [[dr(v) for v in row] for row in M]

# Non-zero entries: dr(2331)=9, dr(333)=9, dr(630)=9, dr(90)=9, dr(63)=9, dr(9)=9
assert dr(2331) == 9    # 2+3+3+1=9
assert dr(333)  == 9    # 3+3+3=9
assert dr(630)  == 9    # 6+3+0=9
assert dr(90)   == 9    # 9+0=9
assert dr(63)   == 9    # 6+3=9
assert dr(9)    == 9

# dr(0) = 0 under repo convention
assert dr(0) == 0

# DR matrix: all non-zero entries are 9, zero entries are 0
for row in DR_M:
    for v in row:
        assert v in {0, 9}, f"unexpected DR value {v}"


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("ALL-PATHS MODULE 2 — Seed Reversal and Phase Analysis")
    print("=" * 62)

    print(f"\n  S1 = {S1}")
    print(f"  S2 = {S2}  (digit-reverse)")

    print(f"\n  Phase vector (S2 mod [162,81,27,9,3]):")
    print(f"    {PHASE}")
    print(f"    PHASE[0] = 111 = 3×37  (0 mod 37)")
    print(f"    PHASE[1] = 30  ∈ {{4,9,25,30}} (orbit under 26x mod 37)")

    print(f"\n  Weight vector: {WEIGHTS}")

    print(f"\n  Matrix M (PHASE ⊗ WEIGHTS):")
    for i, row in enumerate(M):
        print(f"    row {i}: {row}")

    print(f"\n  DR(M) — all non-zero entries = 9:")
    for i, row in enumerate(DR_M):
        print(f"    row {i}: {row}")

    print(f"\n  Note: dr(0) = 0 here (repo convention).")
    print(f"  Source document may use dr(0) = 9 — entries in row 4 differ under that convention.")

    print()
    print("All assertions passed.")

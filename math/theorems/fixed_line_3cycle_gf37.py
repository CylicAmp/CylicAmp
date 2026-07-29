"""
Fixed-Line Structure of 3-Cycle Affine Processes on GF(37) — THEOREM 79

SETUP: PURE 3-CYCLE PROCESS MATRIX.
  A three-party affine process with a single directed 3-cycle
  (A receives from C, B receives from A, C receives from B)
  and diagonal self-loop terms is encoded by the 3×3 matrix:

      A = [[1-u,  0,   r],
           [ s,  1-v,  0],
           [ 0,   t,  1-w]]

  The six parameters (r,s,t,u,v,w) ∈ GF(37)* cover:
    r = weight of A←C edge (cycle step C→A)
    s = weight of B←A edge (cycle step A→B)
    t = weight of C←B edge (cycle step B→C)
    u = 1 − a_{AA}  (A's self-deficit)
    v = 1 − a_{BB}  (B's self-deficit)
    w = 1 − a_{CC}  (C's self-deficit)

  The effective map for fixed-point equations is:

      I − A = [[u,   0,  -r],
               [-s,  v,   0],
               [ 0,  -t,  w]]

DETERMINANT.
  det(I − A) = uvw − rst.
  Fixed points are unique when uvw ≢ rst (mod 37).
  The fixed-point collapses to a LINE when uvw ≡ rst (mod 37).

RIGHT KERNEL (fixed-line direction, when uvw = rst).
  Solving (I−A)·x = 0:
    u·x_A = r·x_C  →  x_A = (r/u)·x_C
    v·x_B = s·x_A  →  x_B = (s·r)/(u·v)·x_C
  Scale by uv:
    (x_A : x_B : x_C) = (rv : rs : uv)  in P²(GF(37)).

LEFT KERNEL (solvability normal, when uvw = rst).
  Solving (I−A)^T·w = 0:
    u·w_A = s·w_B  →  w_A = (s/u)·w_B = (st)/(uv)·w_C
    v·w_B = t·w_C  →  w_B = (t/v)·w_C
  Scale by uv:
    (w_A : w_B : w_C) = (st : ut : uv)  in P²(GF(37)).

SOLVABILITY (FIXED LINE EXISTS FOR GIVEN b).
  b ∈ im(I−A)  ⟺  (left kernel) · b = 0
  ⟺  st·b_A + ut·b_B + uv·b_C ≡ 0  (mod 37).
  This is one linear equation on b ∈ GF(37)³ →
  exactly p² = 37² = 1369 vectors b give a fixed line.

UNIFORM DISTRIBUTION OF KERNEL DIRECTIONS.
  As (r,s,t,u,v,w) range over GF(37)* ⁶ with uvw ≡ rst:
    The right-kernel direction (rv : rs : uv) ∈ P²(GF(37)).
    All coordinates are nonzero (since r,s,u,v ≠ 0).
    The all-nonzero-coordinate stratum of P²(GF(37)) has
    exactly (p−1)² = 36² = 1296 points.
    Each direction is hit by exactly (p−1)³ = 36³ = 46,656
    parameter triples (r,v,t) — the distribution is UNIFORM.

  Proof of count: fix direction (1 : α : β) with α,β ∈ GF(37)*.
    Set s = α·v and u = β·r. Then for each (r,v,t) ∈ GF(37)*³:
      rv, rs=r(αv)=αrv, uv=βrv — direction (rv:αrv:βrv) = (1:α:β). ✓
    w = rst/(uv) = (r)(αv)(t)/(βr·v) = αt/β is determined.
    Total: 36³ = 46,656 solutions per direction.

DIAGONAL BALANCE CONDITION.
  The fixed-line direction is (1 : 1 : 1) iff rv = rs = uv.
    rv = rs  →  v = s.
    rv = uv  →  r = u.
  In process terms: r = u and s = v and t = w, i.e.,
    (cycle weight A←C) = (A self-deficit)
    (cycle weight B←A) = (B self-deficit)
    (cycle weight C←B) = (C self-deficit).
  This is the DIAGONAL BALANCE CONDITION: each node's incoming
  cycle weight equals its own self-loop deficit from identity.

GF(37) SPECIFICS.
  (p−1)²  = 36² = 1296  distinct kernel directions in P²(GF(37)).
  (p−1)³  = 36³ = 46,656  parameter triples per direction.
  p²       = 37² = 1369   solvable b-vectors per kernel.
  36 ∈ ORBIT_11 (36 ≡ −1 mod 37); 36² = 1296 carries ORBIT_11 structure.
  det condition: uvw ≡ rst is a multiplicative seam — exactly
    (p−1)⁵ choices of (r,s,t,u,v) with w = rst/(uv) forced.

18 IS NOT PRIVILEGED.
  The number 18 appears in GF(37) as 18 ∈ SEED_ORBIT = {18,24,32}.
  In the kernel direction (rv : rs : uv), the value 18 appears at
  uniform rate 1/36 per coordinate, i.e., 1/36 × (1/36) of
  all-nonzero directions have first coordinate 18. This is
  1/1296 of the 1296 directions — the base rate.
  2^18 ≡ −1 (mod 37) is an order-of-2 fact; it does not select
  18 as a special kernel direction.

TWO FUTURE DIRECTIONS (from reviewer, verbatim).
  (1) Drop the pure 3-cycle and allow the full 6 off-diagonal
      entries, where det(I−A) picks up two 2-cycle terms and
      the locus stops being a simple product identity.
  (2) Push the diagonal-balance condition to n parties and see
      whether 1−a_ii = incoming weight survives as the criterion
      for a diagonal kernel.
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
IC         = frozenset({1, 10, 26})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
P          = 37


# ── Matrix and determinant ──────────────────────────────────────────────────────

def det_IminusA(r, s, t, u, v, w, p=P):
    return (u * v * w - r * s * t) % p


def right_kernel(r, s, u, v, p=P):
    """Direction (rv : rs : uv) mod p."""
    return ((r * v) % p, (r * s) % p, (u * v) % p)


def left_kernel(s, t, u, v, p=P):
    """Direction (st : ut : uv) mod p."""
    return ((s * t) % p, (u * t) % p, (u * v) % p)


def solvability_check(s, t, u, v, b_A, b_B, b_C, p=P):
    """b ∈ im(I-A) iff st·b_A + ut·b_B + uv·b_C = 0."""
    return (s * t % p * b_A + u * t % p * b_B + u * v % p * b_C) % p == 0


# ── Key checks ─────────────────────────────────────────────────────────────────

# det(I-A) = uvw - rst
_r, _s, _t, _u, _v, _w = 3, 5, 7, 4, 9, 2
_det = (_u * _v * _w - _r * _s * _t) % P
assert det_IminusA(_r, _s, _t, _u, _v, _w) == _det

# When uvw ≡ rst, det = 0 → fixed line
_r2, _s2, _t2, _u2, _v2 = 2, 3, 4, 1, 6
_w2 = (_r2 * _s2 * _t2 * pow(_u2 * _v2, P - 2, P)) % P   # w = rst/(uv)
assert (_u2 * _v2 * _w2 - _r2 * _s2 * _t2) % P == 0
assert det_IminusA(_r2, _s2, _t2, _u2, _v2, _w2) == 0

# Right kernel direction (rv : rs : uv)
_rk = right_kernel(_r2, _s2, _u2, _v2)
assert _rk == (_r2 * _v2 % P, _r2 * _s2 % P, _u2 * _v2 % P)
assert all(c != 0 for c in _rk)

# Left kernel direction (st : ut : uv)
_lk = left_kernel(_s2, _t2, _u2, _v2)
assert _lk == (_s2 * _t2 % P, _u2 * _t2 % P, _u2 * _v2 % P)
assert all(c != 0 for c in _lk)

# Right kernel satisfies (I-A)·v = 0 when uvw = rst
def matmul_IminusA(r, s, t, u, v, w, vec, p=P):
    x, y, z = vec
    return (
        (u * x - r * z) % p,
        (-s * x + v * y) % p,
        (-t * y + w * z) % p,
    )

_rk_full = right_kernel(_r2, _s2, _u2, _v2)
_result = matmul_IminusA(_r2, _s2, _t2, _u2, _v2, _w2, _rk_full)
assert _result == (0, 0, 0), f"Right kernel not in null space: {_result}"

# Left kernel satisfies w^T(I-A) = 0, i.e., (I-A)^T·w = 0
def matmul_IminusA_transpose(r, s, t, u, v, w, vec, p=P):
    x, y, z = vec
    return (
        (u * x - s * y) % p,
        (v * y - t * z) % p,
        (-r * x + w * z) % p,
    )

_lk_full = left_kernel(_s2, _t2, _u2, _v2)
_result_T = matmul_IminusA_transpose(_r2, _s2, _t2, _u2, _v2, _w2, _lk_full)
assert _result_T == (0, 0, 0), f"Left kernel not in null space of transpose: {_result_T}"

# Solvability: b in im(I-A) iff left_kernel · b = 0 → exactly p² = 1369 such b
_sol_count = sum(
    1 for bA in range(P) for bB in range(P) for bC in range(P)
    if solvability_check(_s2, _t2, _u2, _v2, bA, bB, bC)
)
assert _sol_count == P ** 2 == 1369

# Count distinct kernel directions (all nonzero coordinates) = (p-1)^2 = 1296
_dirs = set()
for r_ in range(1, P):
    for s_ in range(1, P):
        for u_ in range(1, P):
            for v_ in range(1, P):
                rv = r_ * v_ % P
                rs = r_ * s_ % P
                uv = u_ * v_ % P
                # Normalize projectively: divide by first nonzero coord
                inv_rv = pow(rv, P - 2, P)
                _dirs.add((1, rs * inv_rv % P, uv * inv_rv % P))
assert len(_dirs) == (P - 1) ** 2 == 1296

# Each direction is hit exactly (p-1)^3 = 46656 times
# Verify for one direction: count (r,s,u,v,t,w) with direction = (1:α:β)
_alpha, _beta = 2, 3   # direction (1:2:3)
_hit_count = 0
for r_ in range(1, P):
    for v_ in range(1, P):
        for t_ in range(1, P):
            s_ = _alpha * v_ % P
            u_ = _beta * r_ % P
            w_ = _alpha * t_ * pow(_beta, P - 2, P) % P
            if w_ == 0:
                continue
            rv = r_ * v_ % P
            rs = r_ * s_ % P
            uv = u_ * v_ % P
            inv_rv = pow(rv, P - 2, P)
            if rs * inv_rv % P == _alpha and uv * inv_rv % P == _beta:
                _hit_count += 1
assert _hit_count == (P - 1) ** 3 == 46656

# Diagonal balance: right kernel = (1:1:1) iff r=u and s=v
# Set r=u, s=v, t=w (balance condition)
_rb, _sb, _tb = 5, 7, 11
_ub, _vb, _wb = _rb, _sb, _tb
assert (_ub * _vb * _wb - _rb * _sb * _tb) % P == 0   # det = 0 ✓
_rk_bal = right_kernel(_rb, _sb, _ub, _vb)
_inv = pow(_rk_bal[0], P - 2, P)
assert _rk_bal[1] * _inv % P == 1 and _rk_bal[2] * _inv % P == 1   # (1:1:1) ✓

# Conversely, direction (1:1:1) forces r=u and s=v
# (rv:rs:uv)=(1:1:1) → rv=rs → v=s AND rv=uv → r=u.
# Check: for general r,s,u,v with s≠v or r≠u, direction is NOT (1:1:1)
_r3, _s3, _u3, _v3 = 2, 5, 2, 7   # r=u=2 but s≠v (5≠7)
_rk3 = right_kernel(_r3, _s3, _u3, _v3)
_inv3 = pow(_rk3[0], P - 2, P)
assert not (_rk3[1] * _inv3 % P == 1 and _rk3[2] * _inv3 % P == 1)

# GF(37) specifics
assert (P - 1) ** 2 == 1296
assert (P - 1) ** 3 == 46656
assert P ** 2 == 1369
assert 36 in ORBIT_11   # 36 ≡ -1; (p-1)^2 = 36^2 carries ORBIT_11 structure

# 18 is not privileged: rv≡18 is hit by exactly (p-1) pairs (r,v), same as any nonzero target.
# The directions are stored normalized to first projective coord = 1; 18 appears as
# a component in un-normalized (rv:rs:uv) at rate 1/(p-1) = 1/36, not elevated.
_count_18 = sum(
    1 for r_ in range(1, P) for v_ in range(1, P) if r_ * v_ % P == 18
)
assert _count_18 == P - 1 == 36   # 36 pairs (r,v) give rv≡18; same count for any nonzero target
# All nonzero targets hit equally often — 18 is not special
for _target in range(1, P):
    assert sum(1 for r_ in range(1, P) for v_ in range(1, P) if r_ * v_ % P == _target) == P - 1
assert 18 in SEED_ORBIT            # 18 ∈ {18,24,32} but rate = 1/36, not elevated


if __name__ == "__main__":
    print("Fixed-Line Structure of 3-Cycle Affine Processes on GF(37) — THEOREM 79")
    print("=" * 70)
    print()
    print("MATRIX STRUCTURE (I − A):")
    print("  [[u,  0, -r],")
    print("   [-s, v,  0],")
    print("   [ 0, -t, w]]")
    print("  det(I−A) = uvw − rst")
    print()
    print("KERNEL DIRECTIONS (when uvw = rst):")
    print("  Right kernel (fixed-line direction): (rv : rs : uv)")
    print("  Left kernel  (solvability normal):   (st : ut : uv)")
    print()
    print("SOLVABILITY:")
    print(f"  b ∈ im(I−A) iff st·b_A + ut·b_B + uv·b_C ≡ 0 (mod {P})")
    print(f"  → exactly p² = {P**2} b-vectors give a fixed line")
    print()
    print("DISTRIBUTION OF KERNEL DIRECTIONS:")
    print(f"  (p−1)² = {(P-1)**2} distinct directions in P²(GF({P}))")
    print(f"  Each hit by (p−1)³ = {(P-1)**3} parameter triples")
    print()
    print("DIAGONAL BALANCE (fixed line = (1:1:1)):")
    print("  r = u  AND  s = v  AND  t = w")
    print("  i.e., (cycle weight) = (self-deficit) at each node")
    print()
    print("GF(37) SPECIFICS:")
    print(f"  (p−1)² = 36² = {36**2}  ← 36 ∈ ORBIT_11 = {{11,27,36}}")
    print(f"  (p−1)³ = 36³ = {36**3}  ← uniform hit count per direction")
    print(f"  p²     = 37² = {37**2}  ← solvable b-vectors per kernel")
    print()
    print("SAMPLE (r=2, s=3, t=4, u=1, v=6):")
    _w_sample = 2 * 3 * 4 * pow(1 * 6, P - 2, P) % P
    _rk_s = right_kernel(2, 3, 1, 6)
    _lk_s = left_kernel(3, 4, 1, 6)
    print(f"  w = rst/(uv) = {_w_sample}")
    print(f"  Right kernel (rv:rs:uv) = ({_rk_s[0]}:{_rk_s[1]}:{_rk_s[2]})")
    print(f"  Left kernel  (st:ut:uv) = ({_lk_s[0]}:{_lk_s[1]}:{_lk_s[2]})")
    print()
    print("All assertions pass.")

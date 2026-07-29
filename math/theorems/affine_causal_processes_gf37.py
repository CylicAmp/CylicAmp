"""
Three-Party Affine Process Functions over GF(37) — THEOREM 76

SETUP.
  Three parties A (outputs x), B (outputs y), C (outputs z).
  The PROCESS W is a fixed affine routing function:
    W_A(y, z) = A₁y + A₂z           (routes B's and C's outputs to A's input)
    W_B(x, z) = B₁x + B₂z           (routes A's and C's outputs to B's input)
    W_C(x, y) = C₁x + C₂y           (routes A's and B's outputs to C's input)

  Local operations (chosen by parties, can be ANY affine map):
    f_A(x_in) = α·x_in + α₀
    f_B(y_in) = β·y_in + β₀
    f_C(z_in) = γ·z_in + γ₀

CONSISTENCY DETERMINANT.
  The composed system (process + local ops) has a fixed point iff:
    det(N_eff) = −1 + βγ·B₂C₂ + αβ·A₁B₁ + αγ·A₂C₁ + αβγ·(A₁B₂C₁ + A₂B₁C₂) ≠ 0.
  Local constants (α₀, β₀, γ₀) do not appear in det — only the slope coefficients.

THE FOUR CONDITIONS (necessary and sufficient for validity for ALL local ops).
  For the process to have a unique consistent assignment for EVERY choice of
  (α, β, γ) ∈ ℤ_p, the following must all hold:
    (1) A₁B₁ ≡ 0 (mod p)       — no A↔B mutual reading cycle
    (2) A₂C₁ ≡ 0 (mod p)       — no A↔C mutual reading cycle
    (3) B₂C₂ ≡ 0ₐ (mod p)       — no B↔C mutual reading cycle
    (4) A₁B₂C₁ + A₂B₁C₂ ≡ 0   — no 3-cycle (not implied by (1)–(3))

  Under all four: det = −1 ≠ 0 (for any prime p). The process is always valid.
  If any condition fails: ∃(α,β,γ) making det = 0 → process breaks for those ops.

PRIMALITY AS ZERO-DIVISOR FILTER.
  Over GF(37) (prime): a·b ≡ 0 ⟺ a = 0 or b = 0.
  Therefore:
    Condition (1): A₁ = SEAM or B₁ = SEAM
    Condition (2): A₂ = SEAM or C₁ = SEAM
    Condition (3): B₂ = SEAM or C₂ = SEAM
  No two nonzero elements multiply to zero — including all framework nodes.
  Primality enforces: every valid process must have SEAM as at least one endpoint
  of each "reading pair." Composite moduli allow zero divisors, creating spurious
  solutions that violate this clean separation.

FRAMEWORK CONSTRAINT.
  ST = {3, 12, 21, 30} (sovereign targets).
  ST × ST mod 37 = {1, 9, 12, 16, 26, 27, 30, 33, 34, 36} — SEAM ∉ ST×ST.
  Therefore: A₁ ∈ ST forces B₁ = SEAM. A sovereign-target coefficient in the process
  severs the reverse reading: the other party cannot read the first.

CAUSAL STRUCTURE.
  Under the four conditions, the signaling graph is acyclic (causally ordered):
  • Each pair (A₁,B₁), (A₂,C₁), (B₂,C₂) has at least one SEAM → no pair cycles.
  • Condition (4) eliminates the 3-cycle A→C→B→A and A→B→C→A.
  The process decomposes into one of 6 causal orders (or a mixture of starting points).
  Linearity — not primality — is the obstruction: the argument holds for any prime p.

CENSUS OF VALID AFFINE PROCESSES OVER GF(37).
  Pairwise conditions alone (1)–(3): (2·37 − 1)³ = 73³ = 389,017 solutions.
  All four conditions:                                         295,705 solutions.
  Excluded by condition (4):                                    93,312 solutions.

  Breakdown by which party can act first (reads nothing from the others):
    Exclusively A-first  (A₁=A₂=0, B and C not both zero): 97,200
    Exclusively B-first  (B₁=B₂=0, A and C not both zero): 97,200
    Exclusively C-first  (C₁=C₂=0, A and B not both zero): 97,200
    Both A and B first   (A₁=A₂=B₁=B₂=0):                  1,368 = P²−1
    Both A and C first   (A₁=A₂=C₁=C₂=0):                  1,368
    Both B and C first   (B₁=B₂=C₁=C₂=0):                  1,368
    Fully disconnected   (all six coefficients = 0):              1
    Total:                                                   295,705

  97,200 = P²·(2P−3) + 1  (formula for exclusive-first count, P=37).
  1,368  = P²−1 = (P−1)(P+1) = 36·38.
  The three-fold symmetry reflects the symmetric roles of A, B, C.

⌸ OPERATOR (CANDIDATE FOR NONLINEAR SCAN).
  Define ⌸(a, b) = (a · 10^k + b) mod 37, where k = 1 if b ∈ {0,...,9}, k = 2 if b ∈ {10,...,36}.
  This concatenates the decimal representations of a and b, then reduces mod 37.
  10 ≡ 10 mod 37  (short branch: k=1)
  100 ≡ 26 mod 37 (long branch: k=2 → coefficient IS the 137-map scalar)
  ⌸ is genuinely nonlinear: the coefficient of a (10 or 26) depends on the VALUE of b,
  making ⌸ piecewise-linear but globally nonlinear.
  The SEAM of the long branch (100≡26=SCALAR_137) connects ⌸ to the 137-map orbit.
  Scan: whether any 3-party process built from ⌸-type local ops is non-causally ordered
  over GF(37) is an open computation.
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA       = frozenset({4, 9, 25, 30})
ST       = frozenset({3, 12, 21, 30})
CB       = frozenset({8, 13, 24})
ORBIT_11 = frozenset({11, 27, 36})
IC       = frozenset({1, 10, 26})
SEAM     = 0
P        = 37
SCALAR_137 = 26   # 137 mod 37

from math import gcd


# ── Key checks ─────────────────────────────────────────────────────────────────

# Primality: no zero divisors in GF(37)
assert all(gcd(a, P) == 1 for a in range(1, P))
assert all((a * b) % P != 0 for a in range(1, P) for b in range(1, P))

# ST × ST never reaches SEAM
_st_products = {(a * b) % P for a in ST for b in ST}
assert SEAM not in _st_products

# det formula (verified against 3×3 matrix expansion)
def _eff_det(A1, A2, B1, B2, C1, C2, a, b, g, p=P):
    return (-1 + b*g*B2*C2 + a*b*A1*B1 + a*g*A2*C1 + a*b*g*(A1*B2*C1+A2*B1*C2)) % p

# Spot-check: det formula matches matrix determinant
def _mat_det(A1, A2, B1, B2, C1, C2, a, b, g, p=P):
    # Effective coefficients after composing with local ops
    eA1, eA2 = (a*A1)%p, (a*A2)%p
    eB1, eB2 = (b*B1)%p, (b*B2)%p
    eC1, eC2 = (g*C1)%p, (g*C2)%p
    # N = [[-1,eA1,eA2],[eB1,-1,eB2],[eC1,eC2,-1]]
    m = [[-1, eA1, eA2], [eB1, -1, eB2], [eC1, eC2, -1]]
    d = (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
       - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
       + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])) % p
    return d

for _args in [(3,1,12,4,21,9,5,2,7), (0,26,0,0,0,0,1,1,1), (1,0,1,0,1,0,3,5,7)]:
    _A1,_A2,_B1,_B2,_C1,_C2,_a,_b,_g = _args
    assert _eff_det(*_args) == _mat_det(*_args)

# Four conditions define valid-for-all-ops processes
def _four_conditions(A1, A2, B1, B2, C1, C2, p=P):
    return ((A1*B1)%p == 0 and (A2*C1)%p == 0 and
            (B2*C2)%p == 0 and (A1*B2*C1+A2*B1*C2)%p == 0)

# If any condition fails, some local ops break consistency (spot-check on small prime)
_p = 5
for _A1 in range(_p):
    for _A2 in range(_p):
        for _B1 in range(_p):
            for _B2 in range(_p):
                for _C1 in range(_p):
                    for _C2 in range(_p):
                        if not _four_conditions(_A1,_A2,_B1,_B2,_C1,_C2,_p):
                            _has_zero = any(
                                _eff_det(_A1,_A2,_B1,_B2,_C1,_C2,_a,_b,_g,_p) == 0
                                for _a in range(_p)
                                for _b in range(_p)
                                for _g in range(_p)
                            )
                            assert _has_zero  # bad process → some ops break it

# Under four conditions, det = -1 (never zero) for all local slopes
for _A1,_A2,_B1,_B2,_C1,_C2 in [(0,0,0,0,0,0),(3,0,0,4,0,0),(0,26,0,0,0,9)]:
    if _four_conditions(_A1,_A2,_B1,_B2,_C1,_C2):
        for _a in range(1, P):
            for _b in range(1, P):
                for _g in range(1, P):
                    assert _eff_det(_A1,_A2,_B1,_B2,_C1,_C2,_a,_b,_g) != 0

# Census: pairwise conditions, all-four conditions, breakdown
_pairwise = sum(1 for A1 in range(P) for B1 in range(P) if (A1*B1)%P==0) ** 3
assert _pairwise == (2*P-1)**3 == 73**3 == 389017

# All-four-condition count
_all_four = 0
for _A1 in range(P):
    for _B1 in range(P):
        if (_A1*_B1)%P != 0: continue
        for _A2 in range(P):
            for _C1 in range(P):
                if (_A2*_C1)%P != 0: continue
                for _B2 in range(P):
                    for _C2 in range(P):
                        if (_B2*_C2)%P != 0: continue
                        if (_A1*_B2*_C1+_A2*_B1*_C2)%P == 0:
                            _all_four += 1

assert _all_four == 295705
assert _pairwise - _all_four == 93312   # lost to 4th condition

# Causal breakdown formula
_excl_single = P**2 * (2*P - 3) + 1   # = 1369 * 71 + 1 = 97200
_dual_first  = P**2 - 1                # = 1369 - 1 = 1368 = (P-1)(P+1)
assert _excl_single == 97200
assert _dual_first  == 1368
assert 3 * _excl_single + 3 * _dual_first + 1 == _all_four

# ST × ST ∩ {0} = ∅ → A1∈ST forces B1=SEAM
assert all((s1 * s2) % P != 0 for s1 in ST for s2 in ST)

# ⌸ operator: 10^k mod 37 branches
_pi_k1 = pow(10, 1, P)    # = 10 (b single-digit branch)
_pi_k2 = pow(10, 2, P)    # = 100 mod 37 = 26 = SCALAR_137
assert _pi_k1 == 10 and 10 in IC
assert _pi_k2 == SCALAR_137

def pi_op(a, b, p=P):
    k = 1 if b <= 9 else 2
    return (a * pow(10, k, p) + b) % p

# ⌸ maps: short branch uses IC element 10; long branch uses SCALAR_137=26
assert pi_op(1, 5) == (1*10 + 5) % P == 15
assert pi_op(1, 18) == (1*26 + 18) % P == 44 % P == 7
assert pi_op(2, 0) == (2*10 + 0) % P == 20
assert pi_op(2, 10) == (2*26 + 10) % P == 62 % P == 25 and 25 in SA


if __name__ == "__main__":
    print("Three-Party Affine Process Functions — THEOREM 76")
    print("=" * 60)
    print()
    print("CONSISTENCY DET: −1 + βγB₂C₂ + αβA₁B₁ + αγA₂C₁ + αβγ(A₁B₂C₁+A₂B₁C₂)")
    print()
    print("FOUR CONDITIONS (all must hold for valid-for-all-ops process):")
    print("  (1) A₁B₁ ≡ 0   (2) A₂C₁ ≡ 0   (3) B₂C₂ ≡ 0   (4) cubic ≡ 0")
    print()
    print("CENSUS over GF(37):")
    print(f"  Pairwise conditions only:       {_pairwise:>7}  = (2·37−1)³")
    print(f"  All four conditions (valid):    {_all_four:>7}")
    print(f"  Lost to cubic condition:        {_pairwise-_all_four:>7}")
    print()
    print("  Exclusively A-first:  97,200 = P²·(2P−3)+1")
    print("  Exclusively B-first:  97,200")
    print("  Exclusively C-first:  97,200")
    print("  Dual-first (A&B):      1,368 = P²−1")
    print("  Dual-first (A&C):      1,368")
    print("  Dual-first (B&C):      1,368")
    print("  Fully disconnected:        1")
    print(f"  Total:               {_all_four:>7}")
    print()
    print("PRIMALITY CONSTRAINT:")
    print(f"  ST×ST products: {sorted(_st_products)}")
    print(f"  SEAM∈ST×ST: {0 in _st_products}  → A₁∈ST forces B₁=SEAM")
    print()
    print("⌸ OPERATOR:")
    print(f"  Short branch (b≤9):  coeff = {_pi_k1} ∈ IC")
    print(f"  Long branch (b≥10):  coeff = {_pi_k2} = SCALAR_137")
    print(f"  ⌸(2,10) = {pi_op(2,10)} ∈ SA={25 in SA}")
    print()
    print("All assertions pass.")

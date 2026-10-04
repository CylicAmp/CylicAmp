"""
Digital-Root Pattern Suite

Covers ten verified findings from the pattern survey:

  A. Universal Collapse to S = {0,2,3,6,8,9}
  B. 1-9 Core: 27 digits, sum = 135, DR(135) = 9
  C. 9↔6 Flip via ±3 seed
  D. 5-Boundary: +9 spacing, period 9
  E. 123/321 Mirror: 444 = 12×37, 888 = 24×37
  F. 6×4 / 64→27 grid observation
  G. 7-Digit Matrix: center 28 = 2×(3+4+7)
  H. Tesla 4-bit bend → DR-3 class
  I. Date Coordinates: session date DR chain 2→7→1
  J. Cardano / ω: roots of x³ − 3x − 1 = 0 via cube root of unity
  K. DR=1 cluster: {c, 37, 73, 2701} and 11g ≡ 44g (mod 9) for 3∣g
  L. D₄ group algebra: ℂ[D₄] Wedderburn blocks for K = ασ + βτ
  M. D₄ Class II Hamiltonian: S={r,r⁻¹,s,r²s} — cancellations, M_E, multiplicities
  N. Engineered motif M=[4,5,6,7,6,5,4,3,4,3,2,1]: gradient word, center of D₄

DR convention used throughout: DR(n) = (n−1)%9+1 for n>0; DR(0)=0.
"""


def dr(n: int) -> int:
    """Digital root: DR(0)=0; DR(n)=9 if 9|n else n%9, for n>0.
    Sign-invariant: DR(n) = DR(|n|)."""
    n = abs(n)
    if n == 0:
        return 0
    r = n % 9
    return r if r != 0 else 9


# =============================================================================
# A. Universal Collapse to S = {0,2,3,6,8,9}
# =============================================================================
# Translation set M = {+2, -2, +3, 0} mod 9.
# Residues not in S: {1, 4, 5, 7}. Each maps into S in one step.
S = {0, 2, 3, 6, 8, 9}
outside_S = {r for r in range(10) if r not in S}  # {1,4,5,7}

collapse_map = {
    1: (1 + 2) % 9,   # 1 +2 → 3 ∈ S
    4: (4 + 2) % 9,   # 4 +2 → 6 ∈ S
    5: (5 + 3) % 9,   # 5 +3 → 8 ∈ S
    7: (7 + 2) % 9,   # 7 +2 → 0 ∈ S  (9 ≡ 0)
}

for r, image in collapse_map.items():
    assert r in outside_S
    assert image in S or image == 0, f"{r} → {image} not in S"

assert outside_S == {1, 4, 5, 7}

# =============================================================================
# B. 1-9 Core: 27 digits, sum 135 → DR 9
# =============================================================================
core_27 = list(range(1, 10)) * 3
assert len(core_27) == 27
assert sum(core_27) == 135
assert dr(135) == 9

# =============================================================================
# C. 9↔6 Flip via seed 3
# =============================================================================
# Subtracting 3 shifts DR: 9 → 6, 6 → 3.
# Adding 3 shifts DR:      6 → 9, 3 → 6.
# Representative pairs:
for n in range(9, 10000, 9):       # DR(n) = 9
    assert dr(n - 3) == 6, f"n={n}: expected DR(n-3)=6, got {dr(n-3)}"
for n in range(6, 10000, 9):       # DR(n) = 6
    assert dr(n + 3) == 9, f"n={n}: expected DR(n+3)=9, got {dr(n+3)}"

# =============================================================================
# D. 5-Boundary: +9 spacing, period 9
# =============================================================================
# DR(5 + 9k) = 5 for all k >= 0.
for k in range(1000):
    assert dr(5 + 9 * k) == 5, f"k={k}: DR(5+9k) != 5"

# The 1-9 digital-root grid has period 9: DR(n+9) = DR(n) for all n>0.
for n in range(1, 1000):
    assert dr(n + 9) == dr(n), f"period-9 fails at n={n}"

# =============================================================================
# E. 123/321 Mirror: 444 = 12×37, 888 = 24×37
# =============================================================================
assert 123 + 321 == 444
assert 444 == 12 * 37
assert 444 * 2 == 888
assert 888 == 24 * 37
assert dr(444) == 3   # 4+4+4=12, 1+2=3
assert dr(888) == 6

# =============================================================================
# F. 6×4 Grid / 64 → 27 = 3³  (consecutive perfect cubes)
# =============================================================================
# 4³ = 64, 3³ = 27.  The two consecutive perfect cubes bracket 37:  27 < 37 < 64.
# DR(64) = DR(6+4) = DR(10) = 1.
# DR(27) = DR(2+7) = DR(9) = 9.
assert 4 ** 3 == 64
assert 3 ** 3 == 27
assert 27 < 37 < 64
assert dr(64) == 1
assert dr(27) == 9
# Position 3: 27 = 3³ is the cube of 3, the third perfect cube (1,8,27).
cubes = [n ** 3 for n in range(1, 10)]
assert cubes.index(27) == 2   # 0-indexed → "position 3" in 1-indexed terms
assert cubes[2] == 27

# =============================================================================
# G. 7-Digit Matrix: center 28 = 2×(3+4+7)
# =============================================================================
anchor_digits = (3, 4, 7)
digit_sum = sum(anchor_digits)
center = 2 * digit_sum
assert digit_sum == 14
assert center == 28
assert center == 2 * 14
assert dr(28) == dr(2 + 8) == 1   # DR(28)=10→1

# =============================================================================
# H. Tesla {3,6,9}: 4-bit numbers — DR-3 subclass bends to 3
# =============================================================================
# 4-bit numbers: 1 through 15.
four_bit = list(range(1, 16))
tesla_class = [n for n in four_bit if dr(n) in {3, 6, 9}]  # {3,6,9,12,15}
assert set(tesla_class) == {3, 6, 9, 12, 15}

# DR-3 subclass (DR=3) within 4-bit range: {3, 12}
dr3_class = [n for n in four_bit if dr(n) == 3]
assert dr3_class == [3, 12]
# "4-bit bend → 3": 3 is the generator; 12 = 4×3 reduces back to DR=3.
assert dr(3) == 3
assert dr(12) == 3

# =============================================================================
# I. Date Coordinates: project session date 2026-04-11 → DR chain
# =============================================================================
# Session date: 2026-04-11
year, month, day = 2026, 4, 11
dr_year  = dr(sum(int(d) for d in str(year)))   # 2+0+2+6=10→1
dr_month = dr(month)                             # 4
dr_day   = dr(sum(int(d) for d in str(day)))     # 1+1=2
full_date_digits = sum(int(d) for d in "20260411")  # 2+0+2+6+0+4+1+1=16
dr_full = dr(full_date_digits)                   # 16→7

assert dr_year  == 1
assert dr_month == 4
assert dr_day   == 2
assert dr_full  == 7
# DR chain for the full date integer 20260411:
date_val = 20260411
assert dr(date_val) == 7

# =============================================================================
# J. Cardano / ω: roots of x³ − 3x − 1 = 0
# =============================================================================
# This cubic has discriminant Δ = 4p³ + 27q² with p=−3, q=−1:
# Δ = 4(−3)³ + 27(−1)² = −108 + 27 = ... use standard form Δ = −4(−3)³ − 27(−1)² = 108−27 = 81.
# Δ > 0: three distinct real roots (casus irreducibilis — requires ω to express via radicals).
# Roots: 2cos(2π/9), 2cos(8π/9), 2cos(14π/9).
# Connection to ω = e^(2πi/3): ω satisfies ω² + ω + 1 = 0 → ω = (−1 ± i√3)/2.
# DR(81) = 9; DR of discriminant = 9 (Tesla anchor).

import math

p_coeff, q_coeff = -3, -1
discriminant = -4 * p_coeff**3 - 27 * q_coeff**2   # 81
assert discriminant == 81
assert dr(discriminant) == 9

# Verify the three roots numerically
roots = [2 * math.cos(math.pi / 9 + 2 * math.pi * k / 3) for k in range(3)]
for r in roots:
    val = r**3 - 3*r - 1
    assert abs(val) < 1e-9, f"root {r:.6f} fails: x³−3x−1 = {val:.2e}"

# ω² + ω + 1 = 0; "3ω" refers to 3×ω (the Eisenstein unit scaled by 3).
omega = complex(-0.5, math.sqrt(3) / 2)   # e^(2πi/3)
assert abs(omega**2 + omega + 1) < 1e-12

# =============================================================================
# K. DR=1 cluster and multiplicative identity DR(11g) = DR(44g) for 3∣g
# =============================================================================
# DR=1 cluster: c (speed of light m/s), 37, 73, 2701 = 37×73
c_light = 299_792_458
assert dr(c_light) == 1   # digit sum 55→10→1
assert dr(37) == 1
assert dr(73) == 1
assert dr(2701) == 1
assert 37 * 73 == 2701

# Triadic identity — algebraic proof (no loop needed):
#   44 − 11 = 33,  and  33·g ≡ 0 (mod 9) whenever 3|g.
#   Proof: g = 3k → 33·3k = 99k = 9·11k ≡ 0 (mod 9). ∎
#   Therefore 11g ≡ 44g (mod 9) → DR(11g) = DR(44g) for all 3|g.
assert (44 - 11) == 33
assert 33 % 9 == 6           # 33 ≡ 6 mod 9
assert (33 * 3) % 9 == 0     # the key collapse: 99 ≡ 0 mod 9
# Sample check (belt-and-suspenders, not a substitute for the proof above):
for k in (1, 2, 3, 7, 100, 333):
    g = 3 * k
    assert dr(11 * g) == dr(44 * g)

# The 6k DR cycle: 6,3,9,6,3,9,… (period 3, follows from 33·3k ≡ 0 mod 9)
expected_dr_cycle = [6, 3, 9]
for k in range(1, 10):
    raw = (6 * k) % 9
    actual = raw if raw != 0 else 9
    assert actual == expected_dr_cycle[(k - 1) % 3]

# DR is a multiplicative homomorphism: DR(a×b) = DR(DR(a) × DR(b))
# This is the general principle behind the {37,73,2701} cluster:
#   37 ≡ 1, 73 ≡ 1 (mod 9) → product ≡ 1 (mod 9) → DR = 1.
for a, b in [(37, 73), (2, 5), (4, 7), (9, 9), (6, 6)]:
    assert dr(a * b) == dr(dr(a) * dr(b)), f"homomorphism fails at {a},{b}"


# =============================================================================
# L. D₄ group algebra: ℂ[D₄] Wedderburn decomposition for K = ασ + βτ
# =============================================================================
# D₄ = ⟨σ,τ | σ⁴=e, τ²=e, τστ=σ⁻¹⟩
# 5 irreps: A₁,A₂,B₁,B₂ (1D) and E (2D).
#
# For K = ασ + βτ, the image in each irrep:
#   A₁: χ(σ)=+1, χ(τ)=+1  →  K_{A₁} = α + β
#   A₂: χ(σ)=+1, χ(τ)=−1  →  K_{A₂} = α − β
#   B₁: χ(σ)=−1, χ(τ)=+1  →  K_{B₁} = −α + β
#   B₂: χ(σ)=−1, χ(τ)=−1  →  K_{B₂} = −α − β
#   E:  σ → [[0,−1],[1,0]], τ → [[1,0],[0,−1]]
#       K_E = [[β,−α],[α,−β]]   eigenvalues ±√(β²−α²)

import numpy as np  # already available in this environment

def _d4_spectrum(alpha: float, beta: float) -> dict:
    """Return full D₄ group-algebra spectrum for K = α·σ + β·τ."""
    one_d = {
        "A1": alpha + beta,
        "A2": alpha - beta,
        "B1": -alpha + beta,
        "B2": -alpha - beta,
    }
    K_E = np.array([[beta, -alpha], [alpha, -beta]], dtype=complex)
    evals_E = np.linalg.eigvals(K_E)
    return {"1D": one_d, "E_matrix": K_E, "E_eigenvalues": evals_E}


def _e_eigenvalues_analytic(alpha: float, beta: float):
    disc = beta**2 - alpha**2
    if disc >= 0:
        return math.sqrt(disc), -math.sqrt(disc)
    return complex(0, math.sqrt(-disc)), complex(0, -math.sqrt(-disc))


# --- Fiber K_E = [[0,1+i],[1-i,0]] has eigenvalues ±√2 ---
K_fiber = np.array([[0, 1+1j], [1-1j, 0]])
evals_fiber = np.linalg.eigvals(K_fiber)
assert np.allclose(sorted(evals_fiber.real), [-math.sqrt(2), math.sqrt(2)], atol=1e-12)
assert np.allclose(evals_fiber.imag, 0, atol=1e-12)

# --- Verify analytic formula against numpy for several (α,β) pairs ---
for alpha, beta in [(1, 0), (0, 1), (1, 1), (3, 2), (2, 3)]:
    spec = _d4_spectrum(alpha, beta)
    one_d = spec["1D"]

    assert abs(one_d["A1"] - (alpha + beta)) < 1e-12
    assert abs(one_d["A2"] - (alpha - beta)) < 1e-12
    assert abs(one_d["B1"] - (-alpha + beta)) < 1e-12
    assert abs(one_d["B2"] - (-alpha - beta)) < 1e-12

    lam_p, lam_m = _e_eigenvalues_analytic(alpha, beta)
    numeric = list(spec["E_eigenvalues"])
    for a in [lam_p, lam_m]:
        assert min(abs(n - a) for n in numeric) < 1e-10, (
            f"α={alpha},β={beta}: analytic eigenvalue {a} not found in {numeric}"
        )

# --- Special regimes ---
# (i) β=α → E-block eigenvalues = 0 (flat)
lp, lm = _e_eigenvalues_analytic(1, 1)
assert abs(lp) < 1e-12 and abs(lm) < 1e-12

# (ii) α=0 → E-block eigenvalues = ±β (pure reflection, real)
lp, lm = _e_eigenvalues_analytic(0, 3)
assert abs(lp - 3) < 1e-12 and abs(lm + 3) < 1e-12

# (iii) β=0 → E-block eigenvalues = ±iα (pure rotation, imaginary)
lp, lm = _e_eigenvalues_analytic(2, 0)
assert abs(lp - complex(0, 2)) < 1e-12 and abs(lm - complex(0, -2)) < 1e-12

# --- 1D spectrum forms a ℤ/2 × ℤ/2 pattern under (±α) × (±β) ---
for alpha, beta in [(1, 2), (3, 5)]:
    vals = sorted([alpha+beta, alpha-beta, -alpha+beta, -alpha-beta])
    expected = sorted([-alpha-beta, -alpha+beta, alpha-beta, alpha+beta])
    assert vals == expected

# =============================================================================
# M. D₄ Class II Hamiltonian: generating set S = {r, r⁻¹, s, r²s}
# =============================================================================
# With the specific generating set S = {σ, σ³, τ, σ²τ} the two pairs cancel:
#   U_E(σ) + U_E(σ³) = 0    (rotation + inverse)
#   U_E(τ)  + U_E(σ²τ) = 0  (reflection + conjugate)
# This forces ALL four 1D isotypic blocks to zero (regardless of 1D characters
# being ±1, both sub-sums vanish independently).
# The only active sector is the 2D E block: M_E = Σ U_E(a)⊗U_E(a) with
# eigenvalues [-4, 0, 0, 4].
# On 64 sites = 8×|D₄| with 2D fiber: +4 (×16), 0 (×96), -4 (×16).

# E-irrep generator matrices (standard faithful representation of D₄)
_r      = np.array([[ 0, -1], [ 1,  0]])   # σ: rotation 90°
_r_inv  = np.array([[ 0,  1], [-1,  0]])   # σ³ = σ⁻¹
_s      = np.array([[ 1,  0], [ 0, -1]])   # τ: reflection
_r2s    = np.array([[-1,  0], [ 0,  1]])   # σ²τ

# --- Cancellation identities ---
assert np.all(_r + _r_inv == 0),   "U(r) + U(r⁻¹) ≠ 0"
assert np.all(_s + _r2s   == 0),   "U(s) + U(r²s) ≠ 0"

_S_class2 = [_r, _r_inv, _s, _r2s]

# --- All four 1D block matrices vanish ---
# χ(r), χ(r³), χ(s), χ(r²s) for each irrep:
_chars_1d = {
    "A1": [ 1,  1,  1,  1],
    "A2": [ 1,  1, -1, -1],
    "B1": [-1, -1,  1,  1],
    "B2": [-1, -1, -1, -1],
}
for _name, _ch in _chars_1d.items():
    _M = sum(c * U for c, U in zip(_ch, _S_class2))
    assert np.all(_M == 0), f"M_{_name} ≠ 0: {_M}"

# --- E-block: M_E = Σ U_E(a) ⊗ U_E(a) ---
_M_E = sum(np.kron(U, U) for U in _S_class2)
_M_E_evals = np.linalg.eigvals(_M_E)
assert np.allclose(sorted(_M_E_evals.real), [-4, 0, 0, 4], atol=1e-10)
assert np.allclose(_M_E_evals.imag, 0, atol=1e-10)

# --- Multiplicity counting on 64-site = 8×|D₄| lattice with 2D fiber ---
# Regular rep of D₄ (order 8): A1,A2,B1,B2 appear 1× each; E appears 2×.
# With 8 copies of the regular rep (= 64 sites):
#   1D irreps: 8 occurrences each in base; with 2D fiber → 16 states each
#   E irrep:  16 occurrences in base; with 2D fiber → 16×4 = 64 states
#     M_E evals [-4,0,0,4] → 16 at -4, 32 at 0, 16 at +4
_n_reg_copies = 64 // 8           # = 8
_n_per_1d = _n_reg_copies * 1 * 2  # 8 occurrences × dim1 × fiber2 = 16
_n_e_copies = 2 * _n_reg_copies    # 2 per regular rep × 8 = 16
_n_plus4  = _n_e_copies * 1        # 16 (one +4 eigenvalue per 4×4 block)
_n_minus4 = _n_e_copies * 1        # 16
_n_zero   = 4 * _n_per_1d + _n_e_copies * 2   # 64 (1D) + 32 (E zeros) = 96

assert _n_plus4  == 16
assert _n_minus4 == 16
assert _n_zero   == 96
assert _n_plus4 + _n_zero + _n_minus4 == 128

# =============================================================================
# N. Engineered motif M and D₄ word evaluation
# =============================================================================
# Proposed Phase-B motif: M = [4,5,6,7,6,5,4,3,4,3,2,1]
# Gradient lift rule (orientation-preserving subgroup Z₄ ⊂ D₄, abelian):
#   Δmⱼ > 0  →  r      (exponent +1 mod 4)
#   Δmⱼ < 0  →  r⁻¹    (exponent -1 mod 4)
#   Δmⱼ = 0  →  e      (exponent  0)
# In the abelian Z₄ the word product is just the sum of exponents mod 4.
# Periodic motif: the 12th gradient is m₀ - m₁₁ (wrap-around).

_motif = [4, 5, 6, 7, 6, 5, 4, 3, 4, 3, 2, 1]
_n_steps = len(_motif)                                  # 12
_grads = [_motif[(j+1) % _n_steps] - _motif[j] for j in range(_n_steps)]
# Exponents: +1 for positive, -1 for negative, 0 for zero step
_exps = [+1 if d > 0 else (-1 if d < 0 else 0) for d in _grads]
_word_exp = sum(_exps) % 4          # total word exponent in Z₄
_prefix4_exp = sum(_exps[:4]) % 4   # first-4-step prefix

# What the word actually evaluates to (naming by exponent mod 4):
_word_name  = {0: "e", 1: "r", 2: "r²", 3: "r³"}
_word_full   = _word_name[_word_exp]
_word_prefix = _word_name[_prefix4_exp]

# --- Center of D₄ ---
# Z(D₄) = {e, r²}: r² is the unique non-trivial central element.
# Verify: r² commutes with every generator (r and s).
# r·r² = r³ = r²·r  ✓  (r commutes with r² trivially in Z₄)
# s·r²·s⁻¹ = r⁻² = r²  (since r⁻² = r² in Z₄, and s·rᵏ·s = r⁻ᵏ)
def _d4_conjugate_r2_by_s():
    """Conjugate r² by s: s·r²·s⁻¹ = r⁻² = r² (in Z₄)."""
    return (-2) % 4   # r⁻² ≡ r² mod 4

assert _d4_conjugate_r2_by_s() == 2   # r⁻² ≡ r²
# r²·r² = r⁴ = e
assert (2 + 2) % 4 == 0

# --- Report what the motif's word actually is ---
# (The engineered motif targets P₁₂=e and prefix=r², but the actual
#  computed values are recorded here without override.)
_motif_grads_summary = _grads        # stored for __main__ print
_full_word_result   = _word_full
_prefix_word_result = _word_prefix

# =============================================================================
# O. D₄ E-representation algebra generation and M_E commutant structure
# =============================================================================
# Structural correction to Section M:
# "Operator lives in non-abelian isotypic ideal" is correct; "pure E-sector
# with independent copies" is too strong.  The full algebra is End(E^⊕8) ≅
# M_8(M_2(C)), which does not imply decoupling across multiplicities.
#
# Two concrete checks:
# (1) Burnside density: the 8 E-rep images of D₄ span all of M_2(C).
# (2) Commutant of M_E in M_4(C): encodes hidden structure from the two zero
#     modes.  For eigenvalues {-4(×1), 0(×2), +4(×1)}, the commutant is
#     M_1(C) ⊕ M_2(C) ⊕ M_1(C)  (dim = 1+4+1 = 6).

# --- (1) E-rep spans M_2(C) ---
_d4_e_reps = [
    np.eye(2, dtype=int),              # e
    _r,                                 # r
    _r @ _r,                            # r²
    _r @ _r @ _r,                       # r³
    _s,                                 # s
    _r @ _s,                            # rs
    _r @ _r @ _s,                       # r²s
    _r @ _r @ _r @ _s,                  # r³s
]
# Vectorise each 2×2 matrix → column in a 4×8 matrix
_e_vecs = np.column_stack([m.flatten().astype(float) for m in _d4_e_reps])
_e_span_rank = np.linalg.matrix_rank(_e_vecs)
assert _e_span_rank == 4, (
    f"E-rep should span M_2(C) (dim=4) by Burnside density; got rank {_e_span_rank}"
)

# --- (2) Commutant of M_E in M_4(C) ---
# X commutes with M_E  ⟺  (I⊗M_E − M_E^T⊗I) vec(X) = 0
# M_E is symmetric (each kron(U,U)^T = kron(U^T,U^T) = kron(−U,−U) = kron(U,U))
_comm_map = np.kron(np.eye(4), _M_E) - np.kron(_M_E.T, np.eye(4))  # 16×16
_comm_dim = 16 - int(np.round(np.linalg.matrix_rank(_comm_map)))
# Expected: eigenvalue multiplicities 1,2,1 → commutant dim = 1+4+1 = 6
assert _comm_dim == 6, (
    f"Commutant of M_E should be dim 6 (1+M_2+1 from eigenvalue structure), "
    f"got {_comm_dim}"
)

# --- M_E² eigenvalues: {(−4)², 0², 0², 4²} = {0,0,16,16} ---
_M_E_sq = _M_E @ _M_E
_M_E_sq_evals = sorted(np.linalg.eigvals(_M_E_sq).real)
assert np.allclose(_M_E_sq_evals, [0, 0, 16, 16], atol=1e-10)

# =============================================================================
# P. Kernel of M_E: explicit basis, D₄ action, and commutant generators
# =============================================================================
# The 2D kernel of M_E = 2·kron(r,r) + 2·kron(s,s) consists of vec(X) for
# 2×2 matrices X satisfying s·X·s = r·X·r (kernel condition).
# Solution: X must be traceless AND have antisymmetric off-diagonal:
#   X = a·σ_z + b·[[0,1],[-1,0]]  for any a,b ∈ C.
# Basis:
#   k₁ = vec([[0,1],[-1,0]]) = [0,1,-1,0]   (= vec(iσ_y))
#   k₂ = vec([[1,0],[0,-1]]) = [1,0,0,-1]   (= vec(σ_z))

_k1 = np.array([0., 1.,-1., 0.])   # vec([[0,1],[-1,0]])
_k2 = np.array([1., 0., 0.,-1.])   # vec([[1,0],[0,-1]])

assert np.allclose(_M_E @ _k1, 0, atol=1e-10), "k₁ not in kernel"
assert np.allclose(_M_E @ _k2, 0, atol=1e-10), "k₂ not in kernel"
assert abs(_k1 @ _k2) < 1e-10, "k₁, k₂ should be orthogonal"

# --- D₄ acts on kernel via g⊗g — action is diagonal (abelian Z₂×Z₂ image) ---
# Claim: every g⊗g preserves {k₁,k₂} and acts diagonally in that basis.
# This means the non-abelian D₄ reduces to an abelian group on ker(M_E).
_d4_kron_elems = {
    "e"  : np.kron(np.eye(2),           np.eye(2)),
    "r"  : np.kron(_r.astype(float),    _r.astype(float)),
    "r2" : np.kron((_r@_r).astype(float), (_r@_r).astype(float)),
    "r3" : np.kron((_r@_r@_r).astype(float), (_r@_r@_r).astype(float)),
    "s"  : np.kron(_s.astype(float),    _s.astype(float)),
    "rs" : np.kron((_r@_s).astype(float), (_r@_s).astype(float)),
    "r2s": np.kron((_r@_r@_s).astype(float), (_r@_r@_s).astype(float)),
    "r3s": np.kron((_r@_r@_r@_s).astype(float), (_r@_r@_r@_s).astype(float)),
}
_K = np.column_stack([_k1/np.sqrt(2), _k2/np.sqrt(2)])   # orthonormal kernel frame

_d4_ker_diags = {}
for _gname, _gg in _d4_kron_elems.items():
    _act = _K.T @ _gg @ _K   # 2×2 restricted action
    # Must be diagonal
    assert abs(_act[0,1]) < 1e-10 and abs(_act[1,0]) < 1e-10, (
        f"g={_gname}: D₄ action on kernel should be diagonal, got {_act}"
    )
    _d4_ker_diags[_gname] = (round(_act[0,0]), round(_act[1,1]))

# r⊗r acts as diag(+1,−1) = σ_z;  s⊗s acts as diag(−1,+1) = −σ_z on kernel
assert _d4_ker_diags["r"]  == ( 1,-1), "r⊗r should act as σ_z on kernel"
assert _d4_ker_diags["s"]  == (-1, 1), "s⊗s should act as -σ_z on kernel"
assert _d4_ker_diags["rs"] == (-1,-1), "rs⊗rs should act as -I on kernel"
assert _d4_ker_diags["e"]  == ( 1, 1), "e⊗e should act as I on kernel"

# --- σ_z⊗I and I⊗σ_z do NOT preserve ker(M_E) ---
_sz_kron_I = np.kron(np.diag([1.,-1.]), np.eye(2))
_I_kron_sz = np.kron(np.eye(2), np.diag([1.,-1.]))
assert not np.allclose(_M_E @ (_sz_kron_I @ _k1), 0, atol=1e-10), (
    "σ_z⊗I maps k₁ OUT of ker(M_E)"
)
assert not np.allclose(_M_E @ (_I_kron_sz @ _k1), 0, atol=1e-10), (
    "I⊗σ_z maps k₁ OUT of ker(M_E)"
)

# --- Commutant generators on ker(M_E): outer products Pᵢⱼ = kᵢ⊗kⱼᵀ ---
_P11 = np.outer(_K[:,0], _K[:,0])
_P12 = np.outer(_K[:,0], _K[:,1])
_P21 = np.outer(_K[:,1], _K[:,0])
_P22 = np.outer(_K[:,1], _K[:,1])

for _P, _name in zip([_P11,_P12,_P21,_P22], ["P11","P12","P21","P22"]):
    assert np.allclose(_M_E @ _P - _P @ _M_E, 0, atol=1e-10), (
        f"{_name} should commute with M_E"
    )

# Their restricted actions on ker span all of M₂(C) (standard basis e_ij)
assert np.allclose(_K.T @ _P11 @ _K, [[1,0],[0,0]], atol=1e-10)
assert np.allclose(_K.T @ _P12 @ _K, [[0,1],[0,0]], atol=1e-10)
assert np.allclose(_K.T @ _P21 @ _K, [[0,0],[1,0]], atol=1e-10)
assert np.allclose(_K.T @ _P22 @ _K, [[0,0],[0,1]], atol=1e-10)

# =============================================================================
# Q. H_E(t,δ) perturbation matrix — exact characteristic polynomial
# =============================================================================
# H_E is NOT M_E from Section M.  It is a separate 4×4 matrix proposed as an
# "E-block Hamiltonian":
#   H_E(t,δ) = [[0,4+t,δ,0],[4+t,0,0,0],[δ,0,0,4-t],[0,0,4-t,0]]
#
# Exact characteristic polynomial (no approximation):
#   λ⁴ − [(4+t)²+(4-t)²+δ²]·λ² + (4+t)²(4-t)² = 0
#
# Correction to proposed formula:
#   "±(4t+δ), ±(4t-δ)" is wrong: at t=0.5, δ=0 gives ±2, actual is ±4.5.
#   "±((4+t)+δ), ±((4-t)−δ)" is also wrong: splitting is O(δ²), not O(δ).
#   Exact lower eigenvalue: (4−t)·√(1 − δ²/(2(A−B))) where A=(4+t)², B=(4−t)²,
#   A−B = 16t. First-order-in-δ correction is identically zero.

def _H_E_perturb(t, d):
    return np.array([[0,4+t,d,0],[4+t,0,0,0],[d,0,0,4-t],[0,0,4-t,0]], dtype=float)

# Verify exact char poly coefficients via tr(H²) and det(H)
for _tq, _dq in [(0.5, 0.0), (0.5, 0.1), (4.0, 0.0), (4.0, 0.5)]:
    _Hq  = _H_E_perturb(_tq, _dq)
    _Aq  = (4 + _tq) ** 2
    _Bq  = (4 - _tq) ** 2
    _trH2q = np.trace(_Hq @ _Hq)
    _detq  = np.linalg.det(_Hq)
    assert np.isclose(-_trH2q / 2, -(_Aq + _Bq + _dq**2), rtol=1e-9), \
        f"λ² coefficient wrong at t={_tq}, δ={_dq}"
    assert np.isclose(_detq, _Aq * _Bq, atol=1e-8), \
        f"constant coefficient wrong at t={_tq}, δ={_dq}"

# At δ=0: eigenvalues exactly ±(4+t), ±(4−t)
for _tq in [0.0, 0.5, 1.0, 2.0, 3.5]:
    _evq = sorted(np.linalg.eigvalsh(_H_E_perturb(_tq, 0.0)))
    assert np.allclose(_evq, [-(4+_tq), -(4-_tq), 4-_tq, 4+_tq], atol=1e-10), \
        f"δ=0 eigenvalues wrong at t={_tq}"

# At t=4 (flat-band condition): det=0 and zero modes survive all δ
# Char poly at t=4: λ²(λ²−64−δ²)=0  →  eigenvalues {0,0,±√(64+δ²)}
for _dq in [0.0, 0.1, 0.5, 1.0]:
    _Hq  = _H_E_perturb(4.0, _dq)
    assert abs(np.linalg.det(_Hq)) < 1e-9, f"det should be 0 at t=4, δ={_dq}"
    _evq = sorted(np.linalg.eigvalsh(_Hq))
    assert abs(_evq[1]) < 1e-9 and abs(_evq[2]) < 1e-9, \
        f"two zero modes should survive at t=4, δ={_dq}"
    assert np.isclose(abs(_evq[0]), np.sqrt(64 + _dq**2), rtol=1e-8), \
        f"outer eigenvalue wrong at δ={_dq}"

# Splitting is O(δ²): eigenvalue ≈ −(4−t)·(1−δ²/(2(A−B))) where A−B=16t
# Verified via the exact char poly: eigenvalue² = B·(1−δ²/(A−B)) + O(δ⁴)
_tq, _Aq, _Bq = 0.5, (4.5)**2, (3.5)**2   # A−B = 16·0.5 = 8
for _dq in [0.05, 0.10, 0.20]:
    _ev_lower = sorted(np.linalg.eigvalsh(_H_E_perturb(_tq, _dq)))[1]
    _second_order = -(4 - _tq) * (1 - _dq**2 / (2 * (_Aq - _Bq)))
    assert abs(_ev_lower - _second_order) < 1e-3, \
        f"O(δ²) approximation off at δ={_dq}"
    # First-order error grows as δ (the actual correction is 0 to first order)
    _first_order_err = abs(_ev_lower - (-(4 - _tq) + _dq))   # error of "(4-t)+δ" claim
    _second_order_err = abs(_ev_lower - _second_order)
    # Second-order formula is far better: ratio of errors > 10 for δ≥0.05
    assert _first_order_err / (_second_order_err + 1e-12) > 10, \
        f"O(δ²) formula should be ×10 better than O(δ) at δ={_dq}"

# =============================================================================
# R. D₄-equivariant perturbation splits zero modes — accidental symmetry proof
# =============================================================================
# The document "Sovereign Kernel" (Section V) correctly concludes:
#   "Without an external locking mechanism, the zero modes remain vulnerable
#    to D₄-respecting perturbations that break the accidental commutant symmetry."
# This section makes that explicit.
#
# Correction to the document: ker(M_E) has dim=2, not dim=4.
# (The 4 is the commutant dimension on the kernel, i.e., dim M₂(C) = 4.)
# Also: the 12-step motif bulk word = r² (not e), per Section N.
#
# Explicit D₄-equivariant perturbation:
#   Q = P₁₁ − P₂₂   (outer-product difference of orthonormal kernel basis vectors)
#
# Q is in the commutant of every D₄ group element (verified below).
# On ker(M_E): Q·k₁/√2 = +k₁/√2, Q·k₂/√2 = −k₂/√2  (acts as σ_z on kernel).
# On ±4 eigenspaces: Q = 0 (leaves ±4 bands exactly intact).
#
# Consequence: M_E + ε·Q has eigenvalues {−4, −ε, +ε, +4} for any ε ∈ ℝ.
# The zero modes are NOT protected by D₄ symmetry alone.

_Q_split = _P11 - _P22   # D₄-equivariant; acts as σ_z on kernel, 0 on ±4 spaces

# Q commutes with every D₄ group element (g⊗g for all g ∈ D₄)
for _gname_r, _gg_r in _d4_kron_elems.items():
    assert np.allclose(_Q_split @ _gg_r - _gg_r @ _Q_split, 0, atol=1e-10), (
        f"Q should commute with D₄ element {_gname_r}"
    )

# Q acts as ±1 on the kernel basis vectors, 0 on ±4 eigenvectors
_u_plus  = np.array([1., 0., 0., 1.]) / np.sqrt(2)   # +4 eigenvector
_u_minus = np.array([0., 1., 1., 0.]) / np.sqrt(2)   # -4 eigenvector
assert np.allclose(_Q_split @ _u_plus,  0, atol=1e-10), "Q should annihilate +4 eigenvec"
assert np.allclose(_Q_split @ _u_minus, 0, atol=1e-10), "Q should annihilate -4 eigenvec"
assert np.allclose(_Q_split @ _K[:,0], +_K[:,0], atol=1e-10), "Q acts +1 on k₁/√2"
assert np.allclose(_Q_split @ _K[:,1], -_K[:,1], atol=1e-10), "Q acts -1 on k₂/√2"

# M_E + ε·Q has eigenvalues {−4, −ε, +ε, +4} for any ε ∈ ℝ
for _eps_r in [0.1, 0.5, 1.0, 2.0]:
    _M_pert = _M_E + _eps_r * _Q_split
    _ev_pert = sorted(np.linalg.eigvalsh(_M_pert))
    assert np.allclose(_ev_pert, [-4, -_eps_r, _eps_r, 4], atol=1e-10), (
        f"Perturbed eigenvalues wrong at ε={_eps_r}: {_ev_pert}"
    )


if __name__ == "__main__":
    print("Digital-Root Pattern Suite")
    print()

    print("A. Universal Collapse — S = {0,2,3,6,8,9}")
    for r, img in collapse_map.items():
        print(f"   {r} + delta → {img} ∈ S")
    print(f"   Residues outside S: {sorted(outside_S)} — all reach S in 1 step")
    print()

    print("B. 1-9 Core (×3 = 27 digits)")
    print(f"   sum = {sum(core_27)},  DR(135) = {dr(135)}")
    print()

    print("C. 9↔6 Flip via seed 3")
    print(f"   DR(9−3) = DR(6) = {dr(6)};  DR(6+3) = DR(9) = {dr(9)}")
    print()

    print("D. 5-Boundary: DR(5+9k)=5, period 9  (verified for k=0..999)")
    print()

    print("E. 123/321 Mirror")
    print(f"   123 + 321 = {123+321} = 12×37  ✓")
    print(f"   888 = 24×37  ✓;  DR(444)={dr(444)}, DR(888)={dr(888)}")
    print()

    print("F. 6×4 Grid / 64→27")
    print(f"   4³=64, DR(64)={dr(64)};  3³=27, DR(27)={dr(27)};  27<37<64  ✓")
    print()

    print("G. 7-Digit Matrix Center")
    print(f"   3+4+7={digit_sum};  center=2×{digit_sum}={center};  DR(28)={dr(28)}")
    print()

    print("H. Tesla 4-bit bend → 3")
    print(f"   Tesla class (DR∈{{3,6,9}}): {tesla_class}")
    print(f"   DR-3 subclass: {dr3_class}")
    print()

    print("I. Date Coordinates (2026-04-11)")
    print(f"   DR(year)={dr_year}, DR(month)={dr_month}, DR(day)={dr_day}, DR(full)={dr_full}")
    print()

    print("J. Cardano / ω  (x³−3x−1=0)")
    print(f"   Discriminant = {discriminant},  DR({discriminant}) = {dr(discriminant)}")
    print(f"   Roots: {[f'{r:.6f}' for r in roots]}")
    print(f"   ω = e^(2πi/3) satisfies ω²+ω+1=0  ✓")
    print()

    print("K. DR=1 cluster and triadic identity")
    print(f"   DR(c=299792458)={dr(c_light)}, DR(37)={dr(37)}, DR(73)={dr(73)}, DR(2701)={dr(2701)}")
    print(f"   37 × 73 = {37*73}  ✓  (37≡73≡1 mod 9, product≡1 mod 9)")
    print(f"   Triadic identity: 44g−11g=33g≡0 (mod 9) when 3|g  (proof, not loop)")
    print(f"   6k DR cycle: {[expected_dr_cycle[(k-1)%3] for k in range(1,10)]}…")
    print(f"   Homomorphism: DR(a×b)=DR(DR(a)×DR(b)) verified for 5 pairs")
    print()

    print("L. D₄ group algebra — K = ασ + βτ spectral decomposition")
    _ab = [(1, 0), (0, 1), (1, 1), (3, 2)]
    for _a, _b in _ab:
        _eig1d = [_a+_b, _a-_b, -_a+_b, -_a-_b]
        _eig2d = (complex(0, _a) if _a**2 > _b**2
                  else math.sqrt(_b**2 - _a**2))
        print(f"   α={_a}, β={_b}: 1D={_eig1d}, E±={_b**2-_a**2}^½")
    print(f"   Fiber K_E([[0,1+i],[1-i,0]]) eigenvalues = ±{math.sqrt(2):.6f}")
    print()

    print("M. D₄ Class II Hamiltonian — S={r,r⁻¹,s,r²s}")
    print(f"   U(r)+U(r⁻¹) = 0  ✓   U(s)+U(r²s) = 0  ✓")
    print(f"   1D blocks M_{{A1,A2,B1,B2}} = 0  ✓")
    print(f"   M_E eigenvalues = {[round(v) for v in sorted(_M_E_evals.real)]}  ✓")
    print(f"   64-site spectrum (t=1): +4×{_n_plus4}, 0×{_n_zero}, -4×{_n_minus4} = {_n_plus4+_n_zero+_n_minus4} ✓")
    print()

    print("N. Engineered motif M=[4,5,6,7,6,5,4,3,4,3,2,1]")
    print(f"   Gradients (cyclic): {_motif_grads_summary}")
    print(f"   Exponents: {_exps}")
    print(f"   12-step word P₁₂  = {_full_word_result}  (claimed: e)")
    print(f"   4-step prefix word = {_prefix_word_result}  (claimed: r²)")
    print(f"   Z(D₄) center: r²·r²=e ✓, s·r²·s⁻¹=r² ✓")
    print()

    print("O. D₄ E-rep algebra generation and M_E commutant")
    print(f"   E-rep images span M_2(C): rank={_e_span_rank}/4  ✓  (Burnside density)")
    print(f"   Commutant of M_E in M_4(C): dim={_comm_dim}  (= 1+4+1, eigenvalues {{-4,0,0,+4}})")
    print(f"   M_E² eigenvalues: {[round(v) for v in _M_E_sq_evals]}  (= {{0,0,16,16}})  ✓")
    print(f"   Conclusion: zero modes occupy a 2D null-space with full M_2(C) commutant;")
    print(f"   system is partially integrable (not maximally non-abelian in E-sector).")
    print()

    print("Q. H_E(t,δ) perturbation matrix — exact characteristic polynomial")
    print(f"   det(H-λI) = λ⁴ − [(4+t)²+(4-t)²+δ²]λ² + (4+t)²(4-t)²  ✓")
    print(f"   δ=0: eigenvalues exactly ±(4+t), ±(4-t)  ✓  (verified t∈{{0,0.5,1,2,3.5}})")
    print(f"   t=4: char poly = λ²(λ²−64−δ²); zero modes survive all δ  ✓")
    print(f"   Splitting: lower eval ≈ −(4-t)(1−δ²/(32t)); O(δ²), NOT O(δ)  ✓")
    print(f"   Formula '±(4t+δ)': WRONG (gives ±2 at t=0.5 instead of ±4.5)")
    print(f"   Formula '±((4+t)±δ)': WRONG (first-order δ correction is zero)")
    print()

    print("P. Kernel of M_E: basis, D₄ action, and commutant generators")
    print(f"   ker(M_E) = span{{k₁=[0,1,-1,0], k₂=[1,0,0,-1]}} (orthogonal, dim=2)")
    print(f"   k₁ = vec(iσ_y) = vec([[0,1],[-1,0]]),  k₂ = vec(σ_z) = vec([[1,0],[0,-1]])")
    print(f"   D₄ image on ker (via g⊗g): {_d4_ker_diags}")
    print(f"   → All actions diagonal: Z₂×Z₂ image (abelian, not full D₄)")
    print(f"   r⊗r acts as diag(+1,−1) = σ_z on ker  ✓")
    print(f"   s⊗s acts as diag(−1,+1) = -σ_z on ker  ✓")
    print(f"   σ_z⊗I and I⊗σ_z do NOT preserve ker(M_E)  ✓  (proposed T_z/S_z are wrong)")
    print(f"   Commutant generators P_ij = k_i⊗k_j^T commute with M_E ✓")
    print(f"   Actions on ker: P11=e11, P12=e12, P21=e21, P22=e22 → span M_2(C) ✓")
    print()

    print("R. D₄-equivariant perturbation Q=P₁₁−P₂₂ splits zero modes")
    print(f"   Q commutes with all 8 D₄ elements (g⊗g)  ✓")
    print(f"   Q·k₁/√2 = +k₁/√2,  Q·k₂/√2 = −k₂/√2  (σ_z on kernel)  ✓")
    print(f"   Q·u₊ = Q·u₋ = 0  (±4 bands unaffected)  ✓")
    print(f"   M_E+ε·Q eigenvalues = {{−4, −ε, +ε, +4}} for ε∈{{0.1,0.5,1,2}}  ✓")
    print(f"   Zero modes are NOT protected by D₄ symmetry alone (accidental symmetry)  ✓")
    print(f"   Corrections to 'Sovereign Kernel' document:")
    print(f"     dim ker(M_E) = 2  (not 4; 4 is commutant-on-kernel dim)")
    print(f"     Motif bulk word P₁₂ = r² (not e; verified in Section N)")
    print()

    print("All assertions passed.")

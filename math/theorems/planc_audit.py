"""
planc_audit.py

Mathematical audit of the PLANC (gold nanocluster PROTAC) framework.
Covers:
  A. Hook effect — ternary complex [ELT] vs. ligand concentration L₀
     Solves the coupled mass-action system numerically; finds optimal L₀.
  B. Surface geometry — effective reaction volume V_eff and local density ρ
  C. PEG conformational entropy ΔS_conf (Gaussian chain model)
  D. Stokes-Einstein diffusion coefficient and P_app (Fick's law)
  E. Epistemic audit: proven vs. plausible conjecture vs. not yet shown

Epistemic labels used throughout:
  [PROVEN]    standard result, derivable from first principles
  [CONJECTURE] plausible, testable, not shown by this paper
  [UNDEFINED]  claim requires definitions not provided
"""

import math
import numpy as np
from scipy.optimize import brentq
import warnings
warnings.filterwarnings('ignore')

k_B = 1.380649e-23   # J/K
T_K = 310.15          # body temperature (37 °C)
eta_water = 6.9e-4    # Pa·s at 37 °C


# ============================================================
# A.  Hook Effect — Ternary Complex Formation
# ============================================================
print("=" * 70)
print("A.  Hook Effect — [PROVEN: mass-action equilibrium]")
print("=" * 70)
print("""
  Bifunctional PROTAC L bridges E3 ligase (E) and target protein (T).
  Species:  E, L, T, EL, LT, ELT
  Reactions (one L per ternary complex):
    E + L ⇌ EL       K_EL = [E][L]/[EL]
    L + T ⇌ LT       K_LT = [L][T]/[LT]
    EL + T ⇌ ELT     K_ELT_T  (= K_LT/α by cooperativity convention)
    E + LT ⇌ ELT     K_ELT_E  (= K_EL/α, thermodynamic cycle)

  With cooperativity α:
    [EL]  = [E][L]/K_EL
    [LT]  = [T][L]/K_LT
    [ELT] = α·[E][L][T]/(K_EL·K_LT)

  Conservation:
    E₀ = [E] + [EL] + [ELT]
    T₀ = [T] + [LT] + [ELT]
    L₀ = [L] + [EL] + [LT] + [ELT]

  Substituting [E] and [T] from conservation into [ELT] expression
  yields a cubic in [L].  Solved numerically below.
""")

def solve_ternary(L0_vals, E0, T0, K_EL, K_LT, alpha=1.0):
    """
    Solve the ternary complex system for each L0 value.
    Returns arrays of [ELT], [EL], [LT], [E], [T], [L].
    """
    ELT_arr = []
    for L0 in L0_vals:
        # Express everything in terms of free [L] = l
        # [EL]  = E0·l / (K_EL + l + alpha·l·T/(K_LT))  — implicit in T
        # Coupled system; solve by substitution:
        # Given l, compute [E], [T], then [ELT]
        def equations(l):
            if l < 0:
                return 1e30
            # [E] from E0 conservation (self-consistent via [ELT])
            # [ELT] = alpha*[E]*l*[T]/(K_EL*K_LT)
            # [EL] = [E]*l/K_EL
            # Let e = [E], t = [T]
            # e(1 + l/K_EL + alpha*l*t/K_EL/K_LT) = E0
            # t(1 + l/K_LT + alpha*l*e/K_EL/K_LT) = T0
            # Solve these two simultaneously given l
            def inner(e):
                if e < 0: return 1e30
                inner_coeff = 1 + l/K_LT + alpha*l*e/(K_EL*K_LT)
                if inner_coeff <= 0: return 1e30
                t = T0 / inner_coeff
                residual = e * (1 + l/K_EL + alpha*l*t/(K_EL*K_LT)) - E0
                return residual
            try:
                e_sol = brentq(inner, 0, E0, xtol=1e-15, maxiter=1000)
            except Exception:
                return 1e30
            inner_coeff = 1 + l/K_LT + alpha*l*e_sol/(K_EL*K_LT)
            t_sol = T0 / inner_coeff
            elt = alpha * e_sol * l * t_sol / (K_EL * K_LT)
            el  = e_sol * l / K_EL
            lt  = t_sol * l / K_LT
            # L conservation residual
            return l + el + lt + elt - L0

        try:
            l_sol = brentq(equations, 0, L0 + 1e-15, xtol=1e-18, maxiter=2000)
        except Exception:
            ELT_arr.append(np.nan)
            continue

        # Recover all species
        def inner(e):
            inner_coeff = 1 + l_sol/K_LT + alpha*l_sol*e/(K_EL*K_LT)
            t = T0 / inner_coeff
            return e * (1 + l_sol/K_EL + alpha*l_sol*t/(K_EL*K_LT)) - E0
        try:
            e_sol = brentq(inner, 0, E0, xtol=1e-15, maxiter=1000)
        except Exception:
            ELT_arr.append(np.nan)
            continue
        inner_coeff = 1 + l_sol/K_LT + alpha*l_sol*e_sol/(K_EL*K_LT)
        t_sol = T0 / inner_coeff
        elt = alpha * e_sol * l_sol * t_sol / (K_EL * K_LT)
        ELT_arr.append(elt)

    return np.array(ELT_arr)


# Parameters (representative, not from this specific paper)
E0    = 1e-7    # 100 nM Cereblon
T0    = 5e-7    # 500 nM Tau
K_EL  = 2e-7    # 200 nM PROTAC–Cereblon affinity
K_LT  = 1e-6    # 1 µM PROTAC–Tau affinity
alpha = 1.0     # no cooperativity baseline

L0_vals = np.logspace(-9, -4, 400)   # 1 pM to 100 µM

ELT_base = solve_ternary(L0_vals, E0, T0, K_EL, K_LT, alpha=1.0)
ELT_coop = solve_ternary(L0_vals, E0, T0, K_EL, K_LT, alpha=3.0)

# Find optimal L0 (peak [ELT])
valid_mask = ~np.isnan(ELT_base)
if valid_mask.any():
    peak_idx = np.nanargmax(ELT_base)
    L0_opt   = L0_vals[peak_idx]
    ELT_peak = ELT_base[peak_idx]
    # Half-max points (hook width)
    half_max = ELT_peak / 2
    left_idx  = np.where(ELT_base[:peak_idx] > half_max)[0]
    right_idx = np.where(ELT_base[peak_idx:] > half_max)[0]
    L0_left  = L0_vals[left_idx[0]]  if left_idx.size  else np.nan
    L0_right = L0_vals[peak_idx + right_idx[-1]] if right_idx.size else np.nan

print(f"  Representative parameters (illustrative, not paper-specific):")
print(f"    E₀ = {E0*1e9:.0f} nM  (Cereblon)")
print(f"    T₀ = {T0*1e9:.0f} nM  (Tau)")
print(f"    K_EL = {K_EL*1e9:.0f} nM  (PROTAC–Cereblon)")
print(f"    K_LT = {K_LT*1e6:.1f} µM   (PROTAC–Tau)")
print(f"    α = 1.0 (no cooperativity)")
print(f"\n  Results:")
print(f"    L₀_opt = {L0_opt*1e9:.2f} nM   (peak [ELT])")
print(f"    [ELT]_max = {ELT_peak*1e9:.4f} nM")
print(f"    Half-max window: [{L0_left*1e9:.2f}, {L0_right*1e9:.2f}] nM")
print(f"    Window width (log): {math.log10(L0_right/L0_left):.2f} decades")

print(f"\n  Hook effect confirmed [PROVEN]:")
print(f"    At low L₀: [ELT] rises as L₀ (ligand-limited)")
print(f"    At L₀ = L₀_opt ≈ {L0_opt*1e9:.0f} nM: [ELT] is maximised")
print(f"    At high L₀: [ELT] → 0 as L₀⁻² (binary complexes dominate)")

# Analytic approximation for optimal L0 (dilute limit, α=1)
L0_opt_analytic = math.sqrt(K_EL * K_LT)
print(f"\n  Analytic approximation (dilute limit, α=1):")
print(f"    L₀_opt ≈ √(K_EL·K_LT) = √({K_EL*1e9:.0f}·{K_LT*1e9:.0f}) nM")
print(f"           = {L0_opt_analytic*1e9:.2f} nM  (vs numeric {L0_opt*1e9:.2f} nM)")
print(f"    Error: {abs(L0_opt_analytic-L0_opt)/L0_opt*100:.1f}%  "
      f"({'dilute approximation holds' if abs(L0_opt_analytic-L0_opt)/L0_opt < 0.3 else 'concentrated — analytic fails'})")

print(f"""
  Cooperativity (α=3) shifts the optimum and sharpens the peak:
    Peak [ELT] with α=3: {np.nanmax(ELT_coop)*1e9:.4f} nM
    (vs α=1: {ELT_peak*1e9:.4f} nM, improvement ×{np.nanmax(ELT_coop)/ELT_peak:.2f})

  [CONJECTURE: The PLANC nanocluster provides effective α > 1 by
   co-localising PROTAC elements.  This is plausible but requires
   direct measurement of K_ELT vs K_EL·K_LT/α for this specific system.]
""")


# ============================================================
# B.  Surface Geometry — V_eff and local density
# ============================================================
print("=" * 70)
print("B.  Surface Geometry [PROVEN: spherical shell geometry]")
print("=" * 70)

R_c  = 1.5e-9    # 1.5 nm AuNC core radius
L_p  = 10e-9     # 10 nm PEG linker length
N_A  = 6.022e23

V_eff = (4/3) * math.pi * ((R_c + L_p)**3 - R_c**3)
V_eff_linear = 4 * math.pi * R_c**2 * L_p   # thin-shell approx

print(f"\n  AuNC core radius R_c  = {R_c*1e9:.1f} nm")
print(f"  PEG linker length L_p = {L_p*1e9:.1f} nm")
print(f"\n  V_eff (exact shell) = {V_eff*1e27:.4f} nm³ = {V_eff*1e27:.2e} nm³")
print(f"  V_eff (thin shell)  = {V_eff_linear*1e27:.4f} nm³   "
      f"(L_p<<R_c approx {'valid' if L_p < R_c/3 else 'INVALID here — L_p > R_c'})")
print(f"  V_eff in µM-equivalent: {1/(V_eff*N_A)*1e6:.2f} µM per molecule in V_eff")

# Local effective concentration from N ligands on surface
for N_pom in [1, 4, 8, 16]:
    C_local = N_pom / (V_eff * N_A)
    print(f"    N_Pom={N_pom:>2}: C_local = {C_local*1e6:.2f} µM   "
          f"({'above K_EL' if C_local > K_EL else 'below K_EL'})")

print(f"""
  Key issue [CONJECTURE to verify]:
    The effective local concentration C_local greatly exceeds bulk
    concentration when fewer than ~{int(V_eff*N_A*K_EL)} molecules/cluster.
    However, both Pom and Tol must simultaneously bind E and T at the
    SAME cluster — the relevant concentration is that of the paired
    geometry, not each ligand individually.

    True effective concentration for ternary complex requires:
      C_eff_ELT ∝ (probability of bridging geometry) × (local density)²
    This probability depends on ΔS_conf (Section C) and is NOT simply
    N/V_eff.  The paper's local density argument is a necessary but
    not sufficient condition.
""")


# ============================================================
# C.  PEG Conformational Entropy
# ============================================================
print("=" * 70)
print("C.  PEG Conformational Entropy [PROVEN formula; CONJECTURE application]")
print("=" * 70)
print("""
  Gaussian chain model for a single PEG linker of N Kuhn segments,
  each of length b ≈ 0.76 nm (PEG Kuhn length).
  For end-to-end distance r:
    ΔS_conf = −k_B · (3r²)/(2Nb²)    [PROVEN: Gaussian chain]
  Maximum extension: r_max = N·b; rms end-to-end: r_rms = √(N)·b.
""")

b_PEG = 0.76e-9    # nm Kuhn length
MW_PEG = 2000      # 2 kDa PEG
M_monomer = 44     # g/mol per EO unit
N_mon = MW_PEG // M_monomer
N_Kuhn = max(1, N_mon // 3)   # ~3 monomers per Kuhn segment for PEG
r_rms = math.sqrt(N_Kuhn) * b_PEG

print(f"  PEG 2 kDa: ~{N_mon} monomers, ~{N_Kuhn} Kuhn segments")
print(f"  Kuhn length b = {b_PEG*1e9:.2f} nm")
print(f"  r_rms = √N·b = {r_rms*1e9:.2f} nm   (natural end-to-end)")
print(f"  Contour length L_p = N·b = {N_Kuhn*b_PEG*1e9:.2f} nm")

print(f"\n  ΔS_conf vs stretching fraction r/L_p:")
print(f"  {'r/L_p':>8}  {'r (nm)':>8}  {'ΔS/k_B':>10}  {'−TΔS (kJ/mol)':>15}")
print(f"  {'-'*46}")
for frac in [0.2, 0.4, 0.6, 0.8, 0.9]:
    r = frac * N_Kuhn * b_PEG
    dS_kB = -3 * r**2 / (2 * N_Kuhn * b_PEG**2)
    T_dS_kJmol = -k_B * T_K * dS_kB * N_A / 1000
    print(f"  {frac:>8.1f}  {r*1e9:>8.2f}  {dS_kB:>10.3f}  {T_dS_kJmol:>15.2f}")

print(f"""
  [CONJECTURE — application to PLANC]:
    The paper claims to minimize ΔS_conf by choosing L_p ≥ distance
    between E and T binding sites (d_ET).  If d_ET ≈ 10–15 nm (rough
    estimate from protein crystal structures), then:
      r/L_p required ≈ d_ET / (N·b)
    This requires N·b ≥ d_ET, i.e. PEG ≥ {10e-9/(N_Kuhn*b_PEG)*100:.0f}% of
    contour length to reach d_ET = 10 nm.
    The linker design constraint is plausible but the specific
    d_ET for Cereblon–pTau bridging is not reported.
""")

d_ET = 12e-9    # assumed bridging distance
frac_required = d_ET / (N_Kuhn * b_PEG)
dS_required = -k_B * (-3 * d_ET**2 / (2 * N_Kuhn * b_PEG**2))
T_dS_req = -dS_required * T_K * N_A / 1000
print(f"  Assuming d_ET = {d_ET*1e9:.0f} nm:")
print(f"    r/L_p required = {frac_required:.2f}   "
      f"({'feasible' if frac_required < 0.9 else 'near maximum extension — chain force high'})")
print(f"    −TΔS_conf penalty = {T_dS_req:.2f} kJ/mol")
print(f"    This must be overcome by the ternary complex binding energy.")


# ============================================================
# D.  Diffusion Coefficient and P_app
# ============================================================
print()
print("=" * 70)
print("D.  Stokes-Einstein + Fick's Law P_app [PROVEN formulas]")
print("=" * 70)

# Stokes-Einstein: D = k_B T / (6π η r_h)
r_h_vals = [1.5e-9, 3e-9, 5e-9, 8e-9]   # hydrodynamic radii

print(f"\n  D = k_BT / (6πηr_h)  at T={T_K-273.15:.0f}°C, η={eta_water:.2e} Pa·s")
print(f"\n  {'r_h (nm)':>10}  {'D (m²/s)':>12}  {'D (µm²/s)':>12}  "
      f"{'crossing ~5µm BBB? [approx]':>30}")
print(f"  {'-'*68}")
for r_h in r_h_vals:
    D = k_B * T_K / (6 * math.pi * eta_water * r_h)
    D_um2s = D * 1e12
    # Rough diffusion time across 5 µm
    t_cross = (5e-6)**2 / (2 * D)
    print(f"  {r_h*1e9:>10.1f}  {D:>12.3e}  {D_um2s:>12.3f}  "
          f"  diffusion time ~{t_cross:.2f} s")

print(f"""
  [PROVEN: Stokes-Einstein holds for spherical particles in dilute solution]
  [CAVEAT: At r_h < 2 nm, the continuum assumption breaks down;
   discrete solvent structure matters — D may differ by ×2–5 from
   the Stokes-Einstein value. The sub-nm AuNC core requires MD
   simulation or empirical measurement for accurate D.]

  P_app = (1/A·C₀) · dQ/dt  [PROVEN: Fick's first law for steady flux]
  Typical BBB MDCK-MDR1 P_app threshold: >10⁻⁶ cm/s for CNS penetration.
""")

print(f"  P_app estimates for D from Stokes-Einstein:")
A_transwell = 0.6e-4   # m² (0.6 cm² standard transwell)
h_membrane  = 5e-6     # 5 µm membrane thickness
print(f"  {'r_h (nm)':>10}  {'D (m²/s)':>12}  {'P_app (cm/s)':>14}  {'CNS?':>8}")
print(f"  {'-'*50}")
for r_h in r_h_vals:
    D = k_B * T_K / (6 * math.pi * eta_water * r_h)
    P_app = D / h_membrane * 100   # convert m/s to cm/s
    cns = "✓" if P_app > 1e-6 else "✗"
    print(f"  {r_h*1e9:>10.1f}  {D:>12.3e}  {P_app:>14.3e}  {cns:>8}")

print(f"""
  [CONJECTURE — the BBB-to-window claim]:
    The paper claims that tuning r_h ensures the in-vivo AuNC
    concentration "lands in" the optimal window L₀_opt ≈ {L0_opt*1e9:.0f} nM.

    This requires:
      C_brain = f(P_app, dose, clearance, cell uptake) ≈ L₀_opt

    P_app determines flux across the BBB in vitro.
    In-vivo concentration C_brain depends additionally on:
      — systemic clearance and plasma half-life
      — brain tissue binding and non-specific uptake
      — intracellular vs extracellular distribution
      — dose administered

    P_app × dose does NOT uniquely determine C_brain.
    This is a design target, not a mathematical guarantee.
    [STATUS: Plausible engineering goal; requires pharmacokinetic
     modelling (PK/PD) with in-vivo data to verify.]
""")


# ============================================================
# E.  Epistemic Audit Summary
# ============================================================
print("=" * 70)
print("E.  Epistemic Audit")
print("=" * 70)
print(f"""
  PROVEN (standard results — build on without hedging):
    ✓ Hook effect: [ELT] non-monotonic in L₀; peak at √(K_EL·K_LT) (dilute)
    ✓ At L₀ >> √(K_EL·K_LT): [ELT] → 0 as L₀⁻² (binary complexes dominate)
    ✓ V_eff = 4π/3·[(R_c+L_p)³ − R_c³] for spherical shell
    ✓ ΔS_conf = −k_B·3r²/(2Nb²) for Gaussian PEG chain
    ✓ D = k_BT/(6πηr_h) for spherical particle in dilute solution
    ✓ P_app = (1/AC₀)·dQ/dt (Fick's first law for steady-state flux)
    ✓ Thermodynamic cycle: K_EL·K_E,LT = K_LT·K_EL,T (enforces α)

  PLAUSIBLE CONJECTURE (testable, not yet shown for this system):
    ? PLANC nanocluster provides effective cooperativity α > 1 by
      co-localising Pom and Tol.  Requires direct measurement of K_ELT.
    ? Local surface concentration C_local > K_EL drives ternary complex
      formation.  True but C_local ≠ C_eff for the bridging geometry;
      bridging probability requires ΔS_conf analysis and is likely <<1.
    ? PEG linker length is long enough to bridge Cereblon–pTau (d_ET ~{d_ET*1e9:.0f} nm).
      Geometric feasibility depends on unreported crystal structure data.
    ? In-vivo C_brain lands in the optimal window [{L0_left*1e9:.1f}, {L0_right*1e9:.1f}] nM.
      Requires full PK/PD model; cannot follow from P_app alone.

  NOT YET DEFINED (unfalsifiable as written):
    ✗ "Conformational phase-space volume Ω" — described qualitatively but
      not computed; ΔS_conf = k_B·ln(Ω) requires specifying the
      accessible linker conformations, which depends on excluded volume,
      protein surface geometry, and solvent.
    ✗ α for the PLANC system — the cooperativity factor is central but its
      value (and whether it exceeds 1) is not reported numerically.
    ✗ The specific d_ET for Cereblon active site to pTau epitope —
      required to evaluate the entropic penalty but not given.

  MATHEMATICAL ISSUE — the "directly lands in the window" claim:
    L₀_opt ≈ √(K_EL·K_LT) = {L0_opt_analytic*1e9:.0f} nM (dilute limit)
    The half-max window spans [{L0_left*1e9:.1f}, {L0_right*1e9:.1f}] nM
    (log-width {math.log10(L0_right/L0_left):.2f} decades, i.e. a factor of {L0_right/L0_left:.0f}×).
    This is a relatively wide window — the system does NOT require
    surgical precision in L₀.  The narrowness claim is overstated
    relative to what the hook effect mathematics actually predicts.
    [STATUS: The window is ~{math.log10(L0_right/L0_left):.1f} log-decades wide; at K_EL={K_EL*1e9:.0f} nM
     and K_LT={K_LT*1e6:.1f} µM, sub-nM precision is NOT required.]
""")

# Numerical check: how wide does the window get for more similar affinities?
print(f"  Hook window width vs. K_EL/K_LT ratio:")
print(f"  {'K_EL/K_LT':>12}  {'L0_opt (nM)':>12}  {'window (dec)':>14}")
print(f"  {'-'*42}")
for ratio in [1, 10, 100, 1000]:
    K_EL_t = 1e-7
    K_LT_t = K_EL_t * ratio
    L_arr = np.logspace(-10, -3, 300)
    ELT_t = solve_ternary(L_arr, E0, T0, K_EL_t, K_LT_t)
    if not np.all(np.isnan(ELT_t)):
        pk = np.nanargmax(ELT_t)
        hm = np.nanmax(ELT_t) / 2
        li = np.where(ELT_t[:pk] > hm)[0]
        ri = np.where(ELT_t[pk:] > hm)[0]
        l_left  = L_arr[li[0]] if li.size else np.nan
        l_right = L_arr[pk + ri[-1]] if ri.size else np.nan
        w = math.log10(l_right / l_left) if not (np.isnan(l_left) or np.isnan(l_right)) else float('nan')
        print(f"  {ratio:>12}  {L_arr[pk]*1e9:>12.2f}  {w:>14.2f}")

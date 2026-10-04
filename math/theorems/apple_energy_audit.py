# math/theorems/apple_energy_audit.py
"""
Apple Energy Audit — Atom Count, Vaporization, and Framework Claims

─────────────────────────────────────────────────────────────────────────────
CONFIRMED PHYSICS
─────────────────────────────────────────────────────────────────────────────
  Atom count (180g apple, 85% water, 15% glucose):
    Water:  (153/18) × 6.022×10²³ × 3 = 1.536×10²⁵ atoms
    Carbs:  (27/180) × 6.022×10²³ × 24 = 2.168×10²⁴ atoms
    Total:  1.75×10²⁵ atoms                                               ✓

  Energy chain from KE = ½(0.18)(11186)² = 11,261,250 J ≈ 11.26 MJ:
    TNT equivalent:  11.26 / 4.18 = 2.69 kg TNT                          ✓
    33L water 20→100°C: 33×4184×80 = 11.045 MJ                           ✓

  Apple vaporization (real thermodynamics):
    Heat 180g to 100°C: 0.18 × 3600 J/(kg·°C) × 80°C = 51.8 kJ
    Vaporize 153g water: 0.153 × 2,260,000 J/kg = 345.8 kJ
    Total to fully vaporize:  397.6 kJ
    Fraction of 11.26 MJ:     3.5%
    Remaining 10.86 MJ:       heats steam to ~9200°C, dissociates molecules

─────────────────────────────────────────────────────────────────────────────
THE ~3% FIGURE — SOURCE IS THERMODYNAMICS, NOT "JACOBIAN PREDICTION"
─────────────────────────────────────────────────────────────────────────────
  The "Discretization Breakdown at 3% of launch energy" is approximately
  correct as a fraction — but it comes from the latent heat of vaporization
  of water plus sensible heat, not from any Jacobian or lattice model.

  Q_vaporize / E_total = 397.6 kJ / 11,261 kJ = 3.53%   ← standard thermo

  The apple stops being a solid object when it vaporizes; that threshold
  is fully explained by L_vap and c_p. No lattice model is required.

─────────────────────────────────────────────────────────────────────────────
FABRICATED CLAIMS
─────────────────────────────────────────────────────────────────────────────
  1. "3737 lattice": not a defined physical or mathematical object.
     3737 = 37 × 101 (semiprime). No "lattice" with this label exists in
     solid-state physics, crystallography, or the framework audited here.

  2. "Jacobian prediction model from your image": no image is attached to
     this session. The Jacobian in physics is a matrix of partial
     derivatives (coordinate transformations, ODE linearization, etc.).
     Neither usage defines a "prediction model" for energy thresholds.

  3. "Discretization Breakdown": a real numerical-methods term (when a
     discrete grid fails to represent continuous physics). Applied here to
     a physical apple, it conflates numerical discretization with phase
     transition. The correct term is simply "vaporization threshold."

  4. "Left graph": no graph is provided; no simulation output is shown.

─────────────────────────────────────────────────────────────────────────────
PRESSURE WAVE INTENSITY (ACTUAL CALCULATION)
─────────────────────────────────────────────────────────────────────────────
  11.26 MJ released as a single pulse ≡ 2.69 kg TNT equivalent.

  Peak overpressure at distance r (Hopkinson-Cranz scaling):
    Scaled distance Z = r / W^(1/3)  where W is TNT-equivalent mass in kg

  W = 2.69 kg,  W^(1/3) = 1.392 m/kg^(1/3)

  Overpressure (kPa) vs distance (m):
    1  m : Z=0.72  → P ≈  4,700 kPa  (47 bar; structural collapse)
    3  m : Z=2.16  → P ≈    200 kPa  (2 bar; reinforced concrete failure)
    10 m : Z=7.19  → P ≈     18 kPa  (below eardrum rupture ~35 kPa)
    30 m : Z=21.6  → P ≈      5 kPa  (window breakage threshold)
    100m : Z=71.9  → P ≈      1 kPa  (barely perceptible)

  These are instantaneous peak values; actual damage depends on impulse
  duration. Standard reference: Kinney & Graham, "Explosive Shocks in Air."

Classification: Theorem (atom count, energy chain, vaporization fraction);
                Refutation (3737 lattice, Jacobian model, Discretization Breakdown)
"""

# ── Verified computations ─────────────────────────────────────────────────────

weight = 180   # g
water_content = 0.85 * weight
carb_content  = 0.15 * weight
NA = 6.022e23

atoms_water = (water_content / 18)  * NA * 3
atoms_carb  = (carb_content  / 180) * NA * 24
total_atoms = atoms_water + atoms_carb

assert abs(total_atoms - 1.75e25) / 1.75e25 < 0.01   # within 1%

E_J = 11_261_250    # J
tnt_equiv = E_J / 4.18e6
assert abs(tnt_equiv - 2.69) < 0.01

water_heat_33L = 33 * 4184 * (100 - 20)
assert abs(water_heat_33L / 1e6 - 11.05) < 0.01

m_apple = 0.180           # kg
cp_apple = 3600           # J/(kg·°C)
L_vap = 2.26e6            # J/kg
Q_vaporize = m_apple * cp_apple * 80 + 0.85 * m_apple * L_vap
frac_vap = Q_vaporize / E_J
assert 0.03 < frac_vap < 0.04   # ~3.5%

# 3737 is NOT a meaningful lattice parameter
assert 3737 == 37 * 101          # semiprime, no special crystallographic role

# Hopkinson-Cranz pressure wave (simplified Brode/UFC 3-340-02 fit)
def peak_overpressure_kPa(r_m, W_tnt_kg):
    """Peak overpressure in kPa at range r (metres) from W kg TNT."""
    Z = r_m / (W_tnt_kg ** (1/3))   # scaled distance, m/kg^(1/3)
    # Simplified empirical fit (valid Z=0.5..20):
    #   P(Z) ≈ 1772/Z³ − 114/Z² + 108/Z   (kPa, UFC 3-340-02 free-air)
    if Z < 0.5:
        return 1e6   # saturates; nuclear-range overpressure
    return max(0.1, 1772/Z**3 - 114/Z**2 + 108/Z)

W = 2.69
PRESSURE_TABLE = {r: round(peak_overpressure_kPa(r, W)) for r in [1,3,10,30,100]}

assert PRESSURE_TABLE[1]   > 1000     # 1m: catastrophic (>10 bar)
assert PRESSURE_TABLE[100] < 10       # 100m: survivable


if __name__ == "__main__":
    print("Apple Energy Audit")
    print()
    print(f"  Atom count (180g apple): {total_atoms:.2e}")
    print(f"  TNT equivalent:          {tnt_equiv:.2f} kg  ✓")
    print(f"  33L water heat:          {water_heat_33L/1e6:.3f} MJ  ✓")
    print()
    print(f"  Vaporization threshold:  {Q_vaporize/1e3:.1f} kJ = {frac_vap*100:.1f}% of 11.26 MJ")
    print(f"  Source: L_vap and c_p (thermodynamics, NOT Jacobian or lattice)")
    print()
    print(f"  '3737 lattice': 3737 = 37 × 101 (semiprime, no lattice structure)")
    print(f"  'Jacobian prediction model': no image attached; no model defined")
    print(f"  'Discretization Breakdown': correct term = vaporization threshold")
    print()
    print("  Pressure wave (11.26 MJ = 2.69 kg TNT, free-air burst):")
    for r, P in PRESSURE_TABLE.items():
        ref = {1:"structural collapse", 3:"reinforced concrete failure",
               10:"eardrum rupture (~35 kPa)", 30:"window breakage (~3 kPa)",
               100:"threshold effect"}
        print(f"    r={r:4d} m: Z={r/W**(1/3):.2f}  P≈{P:7d} kPa  ({ref[r]})")
    print()
    print("All assertions passed.")

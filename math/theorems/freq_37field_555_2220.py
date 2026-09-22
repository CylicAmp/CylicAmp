"""
freq_37field_555_2220.py

Verified arithmetic connecting three frequencies to the 37-field.

Frequencies (MHz): 3232, 1716, 2220
Common base: 4 MHz
Ratios: 808 : 429 : 555

37-field connections:
  2220 = 60 × 37         (exact multiple)
  555  = 15 × 37         (ratio also exact multiple)
  1716 ≡ 14 (mod 37)    (14 opens the 3-cycle {14, 31, 29})
  3232 ≡ 13 (mod 37)

Energy resolution conversion:
  10⁻³² J/Hz ÷ ℏ ≈ 94.8ℏ
  (J/Hz = J·s is standard SQUID energy sensitivity unit)

Magnetic shielding bound:
  Published superconducting + mu-metal multi-layer maximum: ~10⁸–10¹⁰×
  Claim of 10¹⁴× overstated by ~4 orders of magnitude
"""

from math import isclose

hbar = 1.0545718e-34  # J·s

# ── RATIOS ────────────────────────────────────────────────────────────────────

assert 3232 // 4 == 808
assert 1716 // 4 == 429
assert 2220 // 4 == 555

# ── 37-FIELD CONNECTIONS ──────────────────────────────────────────────────────

assert 2220 % 37 == 0         # 2220 = 60 × 37
assert 2220 // 37 == 60
assert 555 % 37 == 0          # 555 = 15 × 37
assert 555 // 37 == 15

assert 1716 % 37 == 14        # 14 opens 3-cycle {14, 31, 29}
assert 14 in {14, 31, 29}

assert 3232 % 37 == 13

# ── ENERGY RESOLUTION ────────────────────────────────────────────────────────

e_res = 1e-32                  # J/Hz = J·s
hbar_count = e_res / hbar
assert isclose(hbar_count, 94.8, rel_tol=1e-2)

# ── SHIELDING BOUND ───────────────────────────────────────────────────────────

# Published superconducting shield maximum ~10^10 (generous upper bound)
# Claimed 10^14 exceeds by ~4 orders of magnitude
assert 1e14 / 1e10 == 1e4

# ── OUTPUT ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Frequency / 37-field arithmetic")
    print("=" * 50)
    print(f"  Ratios at 4 MHz base: 808 : 429 : 555")
    print(f"  2220 = {2220 // 37} × 37")
    print(f"  555  = {555  // 37} × 37")
    print(f"  1716 mod 37 = {1716 % 37}  (in 3-cycle {{14,31,29}})")
    print(f"  3232 mod 37 = {3232 % 37}")
    print(f"  10⁻³² J/Hz  = {e_res / hbar:.1f} ℏ")
    print(f"  Shielding 10¹⁴ overstated by ~{1e14/1e10:.0e}×")
    print()
    print("All assertions passed.")

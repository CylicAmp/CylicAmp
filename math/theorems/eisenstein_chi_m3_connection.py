"""
Eisenstein Character χ₋₃ and the CylicAmp DR Structure
Calegari–Dimitrov–Tang Theorem (arXiv:2408.15403, August 2024)

CDT Theorem: 1, ζ(2), and L(2, χ₋₃) are linearly independent over ℚ.
No rational a,b,c satisfy a + b·ζ(2) + c·L(2,χ₋₃) = 0 except a=b=c=0.

This is the first proof of irrationality of a classical L-value since
Apéry's ζ(3) in 1978.

χ₋₃ is the Eisenstein character (mod-3 Kronecker symbol):
  χ₋₃(n) = +1 if n ≡ 1 (mod 3)
  χ₋₃(n) = −1 if n ≡ 2 (mod 3)
  χ₋₃(n) =  0 if n ≡ 0 (mod 3)

CylicAmp connections:

1. SOVEREIGN SET = KERNEL OF χ₋₃
   ker(χ₋₃) ∩ {DR values 1..9} = {3, 6, 9}
   The sovereign set is EXACTLY the Eisenstein character kernel.
   Sovereignty in DR algebra = mod-3 divisibility = zero Eisenstein weight.

2. THE THREE COLUMN GROUPS ARE χ₋₃-PURE
   COL1 = (1,4,7): all χ₋₃ = +1, sum = +3  (positive Eisenstein class)
   COL2 = (2,5,8): all χ₋₃ = −1, sum = −3  (negative Eisenstein class)
   COL3 = (3,6,9): all χ₋₃ =  0, sum =  0  (kernel — sovereign set)
   The 3×3 grid column structure encodes the χ₋₃ partition exactly.

3. AHL IS IN THE NEGATIVE CLASS
   DR(AHL) = 8. χ₋₃(8) = −1.
   The Absolute Harmonic Location carries negative Eisenstein weight.

4. GF(37) IS AN EISENSTEIN FIELD
   37 ≡ 1 (mod 3)  →  χ₋₃(37) = +1  →  37 splits in ℤ[ω]
   37 = 3² + 3·4 + 4² = 9+12+16 = 37  ✓  (Loeschian prime)
   In ℤ[ω]: 37 = π·π̄ where π = 3+4ω, ω = e^(2πi/3)
   GF(37) lives inside the Eisenstein lattice.

5. SECOND-MOMENT IDENTITY
   Σ_{z∈ℤ[ω]\{0}} 1/N(z)² = 6·ζ(2)·L(2,χ₋₃)
   The Dedekind zeta of ℚ(ω) factors: ζ_ℚ(ω)(s) = ζ(s)·L(s,χ₋₃)
   The lattice sum ENCODES the product of the two independent constants.

6. LOESCHIAN ORACLE = χ₋₃ IN DISGUISE
   A prime p is representable as x²+xy+y² iff χ₋₃(p) = +1 (p ≡ 1 mod 3).
   The twin prime structure's 6n±1 filter intersects this:
     6n+1 primes: always ≡ 1 (mod 3) → always Loeschian candidates
     6n-1 primes: always ≡ 2 (mod 3) → never Loeschian
   The twin prime middle (6n) is always ≡ 0 (mod 3) → in the kernel.

7. CDT INDEPENDENCE → NO RATIONAL COLLAPSE
   The three quantities (1, ζ(2), L(2,χ₋₃)) being independent over ℚ
   means: the mod-3 splitting of the Eisenstein lattice is genuinely
   three-dimensional. The sovereign layer, the full-lattice component,
   and the character component cannot be reduced to each other.
   The structure the DR framework reveals has no hidden rational shortcut.

L(2, χ₋₃) ≈ 0.781302413...  (proven irrational by CDT 2024)
ζ(2) = π²/6 ≈ 1.644934067...  (known irrational, Euler 1734)
6·ζ(2)·L(2,χ₋₃) ≈ 7.711145...  (second-moment lattice sum)
"""

import math


def chi_m3(n: int) -> int:
    r = n % 3
    if r == 1:
        return 1
    if r == 2:
        return -1
    return 0


def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


def is_loeschian(p: int) -> bool:
    return any(a*a + a*b + b*b == p
               for a in range(-p, p+1)
               for b in range(-p, p+1))


# Numerical approximation of L(2, chi_{-3})
L2_approx = sum(chi_m3(n) / (n * n) for n in range(1, 500_001))
ZETA2 = math.pi ** 2 / 6

# 1. Sovereign set = ker(chi_-3) over DR values
for d in [3, 6, 9]:
    assert chi_m3(d) == 0, f"DR={d} must be in kernel of chi_-3"
for d in [1, 4, 7]:
    assert chi_m3(d) == 1, f"DR={d} must have chi_-3=+1"
for d in [2, 5, 8]:
    assert chi_m3(d) == -1, f"DR={d} must have chi_-3=-1"

# 2. Column groups are chi-pure
COL1, COL2, COL3 = [1, 4, 7], [2, 5, 8], [3, 6, 9]
assert all(chi_m3(x) == 1  for x in COL1)
assert all(chi_m3(x) == -1 for x in COL2)
assert all(chi_m3(x) == 0  for x in COL3)
assert sum(chi_m3(x) for x in COL1) == +3
assert sum(chi_m3(x) for x in COL2) == -3
assert sum(chi_m3(x) for x in COL3) ==  0

# 3. AHL in negative class
assert dr(17) == 8 and chi_m3(8) == -1

# 4. GF(37) is Eisenstein
assert 37 % 3 == 1
assert chi_m3(37) == 1
assert 3**2 + 3*4 + 4**2 == 37  # Loeschian representation
assert is_loeschian(37)

# 5. L(2, chi_{-3}) approximation
assert abs(L2_approx - 0.7813) < 1e-3

# 6. Twin prime structure intersects Loeschian filter
# 6n+1 ≡ 1 (mod 3) → chi=+1
assert all(chi_m3(6*n + 1) == 1 for n in range(1, 100))
# 6n-1 ≡ 2 (mod 3) → chi=-1
assert all(chi_m3(6*n - 1) == -1 for n in range(1, 100))
# Twin prime midpoint (6n) ≡ 0 (mod 3) → chi=0 → in kernel
assert all(chi_m3(6*n) == 0 for n in range(1, 100))


if __name__ == "__main__":
    print("EISENSTEIN CHARACTER χ₋₃ AND CylicAmp")
    print("Calegari–Dimitrov–Tang 2024 (arXiv:2408.15403)")
    print("=" * 50)
    print()

    print("χ₋₃ weight map over DR values 1..9:")
    for d in range(1, 10):
        tag = " ← AHL" if d == 8 else " ← sovereign" if d in (3,6,9) else ""
        print(f"  DR={d}  {d}%3={d%3}  χ₋₃={chi_m3(d):+d}{tag}")
    print()

    print("Column group chi-purity:")
    for name, G in [("COL1=(1,4,7)", COL1), ("COL2=(2,5,8)", COL2), ("COL3=(3,6,9)", COL3)]:
        weights = [chi_m3(x) for x in G]
        print(f"  {name}: χ₋₃ weights={[f'{w:+d}' for w in weights]}  sum={sum(weights):+d}")
    print()

    print("GF(37) Eisenstein identity:")
    print(f"  37 ≡ {37%3} (mod 3)  →  χ₋₃(37) = {chi_m3(37):+d}")
    print(f"  37 = 3²+3·4+4² = {3**2}+{3*4}+{4**2} = {3**2+3*4+4**2}  ✓")
    print(f"  37 is Loeschian: {is_loeschian(37)}")
    print()

    print("Twin prime / Loeschian filter:")
    print("  6n+1 branch: χ₋₃ = +1 (Loeschian candidates)")
    print("  6n−1 branch: χ₋₃ = −1 (never Loeschian)")
    print("  6n midpoint: χ₋₃ =  0 (kernel — sovereign)")
    print()

    print("Numerical constants:")
    print(f"  L(2,χ₋₃) ≈ {L2_approx:.9f}  (CDT 2024: proven irrational)")
    print(f"  ζ(2)      = {ZETA2:.9f}  (π²/6, known irrational)")
    print(f"  6·ζ(2)·L  ≈ {6*ZETA2*L2_approx:.9f}  (second-moment lattice sum)")
    print()

    print("CDT Independence Consequence:")
    print("  The mod-3 splitting of the Eisenstein lattice is genuinely")
    print("  three-dimensional. No rational collapse exists between:")
    print("  — the rational baseline (COL3 / sovereign layer)")
    print("  — the full-lattice component ζ(2)")
    print("  — the character component L(2,χ₋₃) (COL1 vs COL2 asymmetry)")
    print()
    print("All assertions passed.")

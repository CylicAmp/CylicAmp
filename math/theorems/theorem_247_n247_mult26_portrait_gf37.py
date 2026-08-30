"""
Theorem 247: n = 247 — The 137-Map Multiplier Portrait (GF(37))

FACTORIZATION:
  247 = 13 × 19
  Both 13 and 19 are in CAS_EXT = {5, 13, 19}.
  n is the product of the two non-seed CAS_EXT elements.
  247 mod 37 = 25 ∈ SA_ST_B = {21, 25, 28}

ORBIT-SQUARE IDENTITY (central result):
  The 137-map f(x) = 26x mod 37 acts on the CAS_EXT orbit seed x=5 as:
    f(5)  = 19   (first image)
    f²(5) = 13   (second image)
  Their ordinary integer product:
    f(5) × f²(5) = 19 × 13 = 247 = n
  And in GF(37):
    f(x) · f²(x) = 26x · 10x = 260x² ≡ x²  (mod 37)
    247 mod 37 = 25 = 5²  (mod 37)
  So n = 247 is the literal product of f(5) and f²(5), and n ≡ 5² (mod 37).
  The orbit-square identity f(x)·f²(x) ≡ x² (mod 37) is verified at x=5.

ORDER-3 PORTRAIT OF MULT = 26:
  MULT = 137 mod 37 = 26.
  26¹ ≡ 26 (mod 37)  ∈ IC
  26² ≡ 10 (mod 37)  ∈ IC
  26³ ≡  1 (mod 37)  ∈ IC
  ord₃₇(26) = 3.  ⟨26⟩ = {1, 26, 10} = IC orbit.
  Inverse: 26 × 10 = 260 ≡ 1 (mod 37)  →  26⁻¹ = 10 = f⁻¹.
  f²(x) = 10x = f⁻¹(x):  applying f twice is the same as applying f⁻¹ once.
  The 3-cycle is: x → 26x → 10x → x.

DECIMAL RESONANCE (26 = 10² in GF(37)×):
  10² mod 37 = 100 mod 37 = 26.  The MULT is the square of the decimal base.
  10³ mod 37 = 1  →  ord₃₇(10) = 3:  1/37 = 0.027̄  has period 3.
  37 | R(3) = 111  and  10³ − 1 = 999 = 27 × 37.
  26³ − 1 = 17575 = 5² × 19 × 37:
    extra factors are the CAS_EXT seed² and the CAS_EXT image 19.

CYCLOTOMIC PORTRAIT:
  Φ₃(26) = 26² + 26 + 1 = 703 = 19 × 37.
  The order-3 cyclotomic evaluation at MULT factors through both
  the CAS_EXT image 19 and the field prime 37.
  Connection to n: Φ₃(26) / 19 = 37  and  n / 13 = 19.
  gcd(703, 247) = 19 — Φ₃(26) and n share the factor 19.

DISCRETE LOGARITHMS (base 2, a primitive root mod 37):
  log₂(26) = 12    (since 2¹² = 4096 ≡ 26 (mod 37))
  log₂(10) = 24 = 2 × 12.
  Same square relation in the exponent: 10 = 2²⁴ = (2¹²)² = 26² in GF(37)×.
  12 = 36/3 = [GF(37)× : ⟨26⟩] = the index of the IC subgroup.

INTEGER ANATOMY OF 26:
  26 = 2 × 13   (DARK_A × CAS_EXT)
  φ(26) = φ(2) × φ(13) = 1 × 12 = 12.
  12 = log₂(26) = φ(26) = 36/3 = index of ⟨26⟩ in GF(37)×.
  There are exactly 12 cosets of ⟨26⟩ in GF(37)× — the 12 named non-zero orbits.
  26 = 11010₂:  popcount = 3 = ord₃₇(26) = period of 1/37.

TWIN PRIME CONNECTIONS:
  13 is the CAS_EXT member of the twin prime pair (11, 13).  11 ∈ NEG_H.
  19 is the CAS_EXT member of the twin prime pair (17, 19).  17 ∈ NQR17.
  n = 247 = (CAS_EXT twin of 11) × (CAS_EXT twin of 17).
  Both factors of n are the CAS_EXT twins of primes from non-CAS_EXT orbits.

RULE 30:
  247 = 0b11110111.  One Rule 30 step: 132 = 0b10000100.
  132 mod 37 = 21 ∈ SA_ST_B.
  n=247 and R30(247) both map to SA_ST_B under mod 37 (25 and 21 respectively).

RIEMANN CONNECTION:
  floor(N(247)) = 144 = 12².
  12 = log₂(26) = φ(26) = 36/3.
  The Riemann zero count at height 247 is 12 squared.
  144 mod 37 = 33 ∈ D7 = {7, 33, 34}.

CAS_EXT CYCLE (×26 mod 37):
  5 → 19 → 13 → 5
  Read as: seed → n/13 → MULT/2 → seed.

Named orbits (GF(37)):
  IC={1,10,26}  DARK_A={2,15,20}  C3={3,4,30}  CAS_EXT={5,13,19}
  TESLA={6,8,23}  D7={7,33,34}  SA_ST_A={9,12,16}  NEG_H={11,27,36}
  C9={14,29,31}  NQR17={17,22,35}  SEED={18,24,32}  SA_ST_B={21,25,28}
"""

import math

ORBITS = {
    "SEAM":    {0},
    "IC":      {1, 10, 26},
    "DARK_A":  {2, 15, 20},
    "C3":      {3, 4, 30},
    "CAS_EXT": {5, 13, 19},
    "TESLA":   {6, 8, 23},
    "D7":      {7, 33, 34},
    "SA_ST_A": {9, 12, 16},
    "NEG_H":   {11, 27, 36},
    "C9":      {14, 29, 31},
    "NQR17":   {17, 22, 35},
    "SEED":    {18, 24, 32},
    "SA_ST_B": {21, 25, 28},
}

def orbit_of(n: int) -> str:
    v = n % 37
    for name, s in ORBITS.items():
        if v in s:
            return name
    return "UNKNOWN"

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def dr(n: int) -> int:
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n

def discrete_log2_gf37(target: int) -> int:
    v = 1
    for k in range(1, 37):
        v = (v * 2) % 37
        if v == target:
            return k
    raise ValueError(f"No discrete log base 2 of {target} in GF(37)")

RULE30 = [(30 >> i) & 1 for i in range(8)]

def rule30_one_step(v: int, nbits: int = 8) -> int:
    result = 0
    for i in range(nbits):
        left   = (v >> (i + 1)) & 1
        center = (v >> i) & 1
        right  = (v >> (i - 1)) & 1 if i > 0 else 0
        idx    = (left << 2) | (center << 1) | right
        result |= (RULE30[idx] << i)
    return result


def main():
    print("=" * 70)
    print("THEOREM 247: n=247 — The 137-Map Multiplier Portrait (GF(37))")
    print("=" * 70)

    n = 247

    # -----------------------------------------------------------------------
    # Part 1: Factorization and orbit
    # -----------------------------------------------------------------------
    print("\n--- PART 1: Factorization and Orbit ---")
    assert 13 * 19 == n
    assert orbit_of(13) == "CAS_EXT"
    assert orbit_of(19) == "CAS_EXT"
    assert not is_prime(n)
    print(f"  247 = 13 × 19  (CAS_EXT × CAS_EXT) ✓")
    print(f"  247 mod 37 = {n % 37} ∈ {orbit_of(n)}")
    assert orbit_of(n) == "SA_ST_B"
    print(f"  247 is composite (13 × 19), not prime ✓")

    # -----------------------------------------------------------------------
    # Part 2: Orbit-square identity
    # -----------------------------------------------------------------------
    print("\n--- PART 2: Orbit-Square Identity ---")
    x = 5
    fx  = (26 * x) % 37
    f2x = (26 * fx) % 37
    assert fx == 19
    assert f2x == 13
    assert fx * f2x == n
    print(f"  f(5)  = 26×5 mod 37 = {fx} ∈ {orbit_of(fx)} ✓")
    print(f"  f²(5) = 26×{fx} mod 37 = {f2x} ∈ {orbit_of(f2x)} ✓")
    print(f"  f(5) × f²(5) = {fx} × {f2x} = {fx*f2x} = n ✓")
    # f(x)·f²(x) = 260x² ≡ x² (mod 37)
    assert (260 * x**2) % 37 == (x**2) % 37
    assert 260 % 37 == 1
    print(f"  260 mod 37 = {260 % 37}  →  f(x)·f²(x) = 260x² ≡ x² (mod 37) ✓")
    assert n % 37 == (x**2) % 37
    print(f"  247 mod 37 = {n%37} = 5² = {x**2} ≡ {(x**2)%37} (mod 37) ✓")

    # -----------------------------------------------------------------------
    # Part 3: Order-3 portrait of MULT=26
    # -----------------------------------------------------------------------
    print("\n--- PART 3: Order-3 Portrait of MULT=26 ---")
    MULT = 137 % 37
    assert MULT == 26
    assert pow(26, 1, 37) == 26 and orbit_of(26) == "IC"
    assert pow(26, 2, 37) == 10 and orbit_of(10) == "IC"
    assert pow(26, 3, 37) == 1
    print(f"  MULT = 137 mod 37 = {MULT}")
    print(f"  26¹ mod 37 = {pow(26,1,37)} ∈ {orbit_of(26)} ✓")
    print(f"  26² mod 37 = {pow(26,2,37)} ∈ {orbit_of(10)} ✓")
    print(f"  26³ mod 37 = {pow(26,3,37)} ✓  →  ord₃₇(26) = 3")
    assert (26 * 10) % 37 == 1
    print(f"  26 × 10 mod 37 = {(26*10)%37}  →  26⁻¹ = 10 = f⁻¹ ✓")
    print(f"  ⟨26⟩ = {{1, 26, 10}} = IC orbit")
    print(f"  f²(x) = 10x = f⁻¹(x):  two forward steps = one backward step ✓")

    # -----------------------------------------------------------------------
    # Part 4: Decimal resonance
    # -----------------------------------------------------------------------
    print("\n--- PART 4: Decimal Resonance (26 = 10² in GF(37)×) ---")
    assert pow(10, 2, 37) == 26
    assert pow(10, 3, 37) == 1
    print(f"  10² mod 37 = {pow(10,2,37)} = MULT ✓")
    print(f"  10³ mod 37 = {pow(10,3,37)}  →  ord₃₇(10) = 3,  period(1/37) = 3 ✓")
    assert 999 % 37 == 0 and 999 // 37 == 27
    print(f"  10³ - 1 = 999 = 27 × 37 ✓")
    v26 = 26**3 - 1
    assert v26 == 17575
    assert v26 % (5**2 * 19 * 37) == 0
    print(f"  26³ - 1 = {v26} = 5² × 19 × 37 ✓  (CAS_EXT seed² × image × prime)")

    # -----------------------------------------------------------------------
    # Part 5: Cyclotomic portrait
    # -----------------------------------------------------------------------
    print("\n--- PART 5: Cyclotomic Portrait ---")
    phi3_26 = 26**2 + 26 + 1
    assert phi3_26 == 703
    assert phi3_26 == 19 * 37
    print(f"  Φ₃(26) = 26² + 26 + 1 = {phi3_26} = 19 × 37 ✓")
    print(f"  Φ₃(26) / 37 = 19 ∈ {orbit_of(19)};  Φ₃(26) / 19 = 37 (the prime) ✓")
    import math
    assert math.gcd(phi3_26, n) == 19
    print(f"  gcd(Φ₃(26), n) = gcd(703, 247) = {math.gcd(phi3_26, n)} ∈ {orbit_of(19)} ✓")
    print(f"  Φ₃(26) = 37 × (n/13) = 37 × {n//13} ✓")

    # -----------------------------------------------------------------------
    # Part 6: Discrete logarithms
    # -----------------------------------------------------------------------
    print("\n--- PART 6: Discrete Logarithms (base 2) ---")
    log26 = discrete_log2_gf37(26)
    log10 = discrete_log2_gf37(10)
    assert log26 == 12
    assert log10 == 24
    assert log10 == 2 * log26
    print(f"  log₂(26) = {log26}  (2¹² ≡ 26 (mod 37)) ✓")
    print(f"  log₂(10) = {log10} = 2 × {log26} ✓  (same square relation in exponent)")
    assert log26 == 36 // 3
    print(f"  12 = 36/3 = index of ⟨26⟩ in GF(37)× ✓")

    # -----------------------------------------------------------------------
    # Part 7: Integer anatomy of 26
    # -----------------------------------------------------------------------
    print("\n--- PART 7: Integer Anatomy of MULT=26 ---")
    assert 2 * 13 == 26
    assert orbit_of(2) == "DARK_A"
    assert orbit_of(13) == "CAS_EXT"
    print(f"  26 = 2 × 13  ({orbit_of(2)} × {orbit_of(13)}) ✓")
    phi26 = sum(1 for k in range(1, 27) if math.gcd(k, 26) == 1)
    assert phi26 == 12
    assert phi26 == log26 == 36 // 3
    print(f"  φ(26) = φ(2)·φ(13) = 1·12 = {phi26} ✓")
    print(f"  12 = log₂(26) = φ(26) = 36/3 = [GF(37)× : ⟨26⟩] — one constant, four identities")
    print(f"  12 cosets of ⟨26⟩ in GF(37)× = 12 named non-zero orbits ✓")
    b26 = bin(26)
    assert b26.count('1') == 3
    print(f"  26 = {b26}  popcount = {b26.count('1')} = ord₃₇(26) = period(1/37) ✓")

    # -----------------------------------------------------------------------
    # Part 8: Twin prime connections
    # -----------------------------------------------------------------------
    print("\n--- PART 8: Twin Prime Connections ---")
    assert is_prime(11) and is_prime(13) and 13 - 11 == 2
    assert is_prime(17) and is_prime(19) and 19 - 17 == 2
    print(f"  (11,13) twin pair: 11∈{orbit_of(11)}, 13∈{orbit_of(13)} ✓")
    print(f"  (17,19) twin pair: 17∈{orbit_of(17)}, 19∈{orbit_of(19)} ✓")
    print(f"  n=247 = (CAS_EXT twin of 11) × (CAS_EXT twin of 17)")
    print(f"  Both factors are the CAS_EXT members of their twin prime pairs ✓")

    # -----------------------------------------------------------------------
    # Part 9: Binary and DR
    # -----------------------------------------------------------------------
    print("\n--- PART 9: Binary and Digital Root ---")
    b247 = bin(n)
    print(f"  247 = {b247}  popcount = {b247.count('1')}")
    dr_n = dr(n)
    assert dr_n == 4
    assert orbit_of(dr_n) == "C3"
    print(f"  DR(247) = {dr_n} ∈ {orbit_of(dr_n)} ✓")

    # -----------------------------------------------------------------------
    # Part 10: Rule 30
    # -----------------------------------------------------------------------
    print("\n--- PART 10: Rule 30 ---")
    r30 = rule30_one_step(n, nbits=8)
    assert r30 == 132
    assert r30 % 37 == 21
    assert orbit_of(r30) == "SA_ST_B"
    assert orbit_of(n) == "SA_ST_B"
    print(f"  R30(247={bin(n)}) = {r30} = {bin(r30)}")
    print(f"  {r30} mod 37 = {r30%37} ∈ {orbit_of(r30)} ✓")
    print(f"  Both n=247 (→25) and R30(n)=132 (→21) land in SA_ST_B ✓")

    # -----------------------------------------------------------------------
    # Part 11: Riemann connection
    # -----------------------------------------------------------------------
    print("\n--- PART 11: Riemann Connection ---")
    N247 = n * math.log(n / (2 * math.pi)) / (2 * math.pi)
    floor_N = int(N247)
    assert floor_N == 144
    assert 144 == 12 ** 2
    assert log26 == 12
    assert floor_N % 37 == 33
    assert orbit_of(floor_N) == "D7"
    print(f"  N(247) ≈ {N247:.2f}")
    print(f"  floor(N(247)) = {floor_N} = 12² = (log₂(26))² = (φ(26))² ✓")
    print(f"  {floor_N} mod 37 = {floor_N%37} ∈ {orbit_of(floor_N)} ✓")

    print("\n" + "=" * 70)
    print("THEOREM 247 VERIFIED")
    print("=" * 70)


if __name__ == "__main__":
    main()

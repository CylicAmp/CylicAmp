"""
Theorem 248: n = 248 — E₈ Resonance (GF(37))

HEADLINE:
  dim(E₈) = 248 ≡ 26 (mod 37) = MULT — the 137-map multiplier.
  The three fundamental E₈ invariants each land in a named GF(37) orbit:

    rank(E₈)           =   8  ≡  8 (mod 37) ∈ TESLA
    Coxeter number      =  30  ≡ 30 (mod 37) ∈ C3       (= Rule 30 rule number)
    number of roots     = 240  ≡ 18 (mod 37) ∈ SEED      (= pipeline seed orbit)
    dim(E₈)            = 248  ≡ 26 (mod 37) ∈ IC = MULT

  The two structural equations of E₈ become orbit identities in GF(37):

    roots = rank × Coxeter   →   240 = 8 × 30   →   TESLA × C3 ≡ SEED   (mod 37)
    dim   = rank + roots     →   248 = 8 + 240   →   TESLA + SEED ≡ MULT  (mod 37)

  Rule 30's rule number (30 ∈ C3) is the Coxeter number of E₈, and the pipeline
  seed orbit {18,24,32} is the orbit of the root count 240.

FACTORIZATION:
  248 = 2³ × 31 = 8 × 31
  8   = meta multiplier from pipeline (seed 246, step 3) ∈ TESLA
  31  ∈ C9 = {14, 29, 31};  31 is the larger member of twin prime pair (29, 31)
  Both 29 and 31 lie in C9 — an intra-orbit twin prime pair.
  248 = TESLA_element × C9_element ≡ 26 (mod 37) ∈ IC

POWER DECOMPOSITION:
  248 = 2⁸ − 2³
  2⁸ mod 37 = 34 ∈ D7 = {7, 33, 34}
  2³ mod 37 =  8 ∈ TESLA
  34 − 8    = 26 = MULT ✓
  248 is the difference of two powers of 2 whose mod-37 residues differ by MULT.

SUCCESSOR IDENTITY:
  248 = 247 + 1 = f(5)·f²(5) + 1
  T247 showed 247 = 19 × 13 = f(5)·f²(5).
  248 is the integer successor of the CAS_EXT orbit-product.

WEYL GROUP:
  |W(E₈)| = 696,729,600 = 2¹⁴ × 3⁵ × 5² × 7
  696,729,600 mod 37 = 27 ∈ NEG_H = {11, 27, 36}

TWIN PRIME CONNECTIONS:
  (29, 31): both ∈ C9. Unique among named orbits — both twins in the same orbit.
  248 = 8 × 31, so 248 uses the larger C9 twin.
  (239, 241): nearest twin pair below 248. 239 ∈ NQR17, 241 ∈ CAS_EXT.

RULE 30:
  248 = 0b11111000.  One Rule 30 step: 132 = 0b10000100.
  132 mod 37 = 21 ∈ SA_ST_B.
  R30(247) = R30(248) = 132 — two consecutive integers share the same Rule 30 image.

RIEMANN:
  floor(N(248)) = 145 = 5 × 29.  5 ∈ CAS_EXT,  29 ∈ C9.
  145 mod 37 = 34 ∈ D7.
  floor(N(247)) = 144 mod 37 = 33 ∈ D7.  Consecutive theorems, consecutive D7 values.

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
    print("THEOREM 248: n=248 — E₈ Resonance (GF(37))")
    print("=" * 70)

    n = 248

    # -----------------------------------------------------------------------
    # Part 1: E₈ resonance — the headline
    # -----------------------------------------------------------------------
    print("\n--- PART 1: E₈ Resonance ---")
    rank  = 8
    roots = 240
    cox   = 30
    dim   = rank + roots
    assert dim == n
    assert rank * cox == roots
    print(f"  rank(E₈)           = {rank:3d}  mod 37 = {rank%37:2d} ∈ {orbit_of(rank)}")
    print(f"  Coxeter number     = {cox:3d}  mod 37 = {cox%37:2d} ∈ {orbit_of(cox)}  (Rule 30 rule number)")
    print(f"  number of roots    = {roots}  mod 37 = {roots%37:2d} ∈ {orbit_of(roots)}  (pipeline seed orbit)")
    print(f"  dim(E₈)            = {dim}  mod 37 = {dim%37:2d} ∈ {orbit_of(dim)}  (= MULT) ✓")
    assert orbit_of(rank)  == "TESLA"
    assert orbit_of(cox)   == "C3"
    assert orbit_of(roots) == "SEED"
    assert orbit_of(dim)   == "IC"
    assert dim % 37 == 26
    # Orbit equations
    assert (rank * cox) % 37 == roots % 37    # TESLA × C3 ≡ SEED
    assert (rank + roots) % 37 == 26          # TESLA + SEED ≡ MULT
    print(f"\n  roots = rank × Cox  →  {rank}×{cox}={roots}  →  TESLA×C3 ≡ SEED (mod 37) ✓")
    print(f"  dim   = rank + roots →  {rank}+{roots}={dim} →  TESLA+SEED ≡ MULT (mod 37) ✓")
    print(f"  Rule 30 rule number = Coxeter number of E₈ = 30 ∈ C3 ✓")
    print(f"  Pipeline seed orbit {{18,24,32}} = SEED = orbit of root count 240 ✓")

    # -----------------------------------------------------------------------
    # Part 2: Factorization
    # -----------------------------------------------------------------------
    print("\n--- PART 2: Factorization ---")
    assert 8 * 31 == n
    assert is_prime(31)
    assert not is_prime(n)
    print(f"  248 = 2³ × 31 = 8 × 31")
    print(f"  8  mod 37 = {8%37} ∈ {orbit_of(8)}  (meta multiplier from pipeline seed 246)")
    print(f"  31 mod 37 = {31%37} ∈ {orbit_of(31)}")
    print(f"  248 mod 37 = {n%37} ∈ {orbit_of(n)}  (= MULT) ✓")
    assert orbit_of(8 * 31) == "IC"

    # -----------------------------------------------------------------------
    # Part 3: Power decomposition 2⁸ − 2³
    # -----------------------------------------------------------------------
    print("\n--- PART 3: Power Decomposition ---")
    assert 2**8 - 2**3 == n
    assert pow(2, 8, 37) == 34 and orbit_of(34) == "D7"
    assert pow(2, 3, 37) ==  8 and orbit_of(8)  == "TESLA"
    print(f"  248 = 2⁸ − 2³ = {2**8} − {2**3}")
    print(f"  2⁸ mod 37 = {pow(2,8,37)} ∈ {orbit_of(pow(2,8,37))}")
    print(f"  2³ mod 37 = {pow(2,3,37)} ∈ {orbit_of(pow(2,3,37))}")
    print(f"  34 − 8 = {34-8} = MULT ✓")
    assert pow(2, 8, 37) - pow(2, 3, 37) == 26

    # -----------------------------------------------------------------------
    # Part 4: Successor identity
    # -----------------------------------------------------------------------
    print("\n--- PART 4: Successor Identity ---")
    assert n == 247 + 1
    fx  = (26 * 5) % 37   # f(5) = 19
    f2x = (26 * fx) % 37  # f²(5) = 13
    assert fx * f2x == 247
    print(f"  248 = 247 + 1 = f(5)·f²(5) + 1 = {fx}×{f2x} + 1 ✓")
    print(f"  248 is the integer successor of the T247 CAS_EXT orbit-product")

    # -----------------------------------------------------------------------
    # Part 5: Discrete log
    # -----------------------------------------------------------------------
    print("\n--- PART 5: Discrete Logarithm ---")
    assert pow(2, 12, 37) == 26
    print(f"  248 ≡ 26 = 2¹² (mod 37)")
    print(f"  log₂(248 mod 37) = log₂(MULT) = 12 = φ(26) = 36/3 ✓")

    # -----------------------------------------------------------------------
    # Part 6: Weyl group
    # -----------------------------------------------------------------------
    print("\n--- PART 6: Weyl Group ---")
    weyl = 696729600
    assert weyl % 37 == 27
    assert orbit_of(weyl) == "NEG_H"
    print(f"  |W(E₈)| = {weyl:,}")
    print(f"  {weyl:,} mod 37 = {weyl%37} ∈ {orbit_of(weyl)}")

    # -----------------------------------------------------------------------
    # Part 7: Twin prime connections
    # -----------------------------------------------------------------------
    print("\n--- PART 7: Twin Prime Connections ---")
    assert is_prime(29) and is_prime(31) and 31 - 29 == 2
    assert orbit_of(29) == orbit_of(31) == "C9"
    print(f"  (29,31) twin pair: both ∈ {orbit_of(29)} ✓  (intra-orbit twin prime pair)")
    print(f"  248 = 8 × 31  (meta multiplier × larger C9 twin)")
    assert is_prime(239) and is_prime(241) and 241 - 239 == 2
    print(f"  (239,241) nearest twin pair below 248:")
    print(f"    239 ∈ {orbit_of(239)},  241 ∈ {orbit_of(241)}")

    # -----------------------------------------------------------------------
    # Part 8: Digital root
    # -----------------------------------------------------------------------
    print("\n--- PART 8: Digital Root ---")
    dr_n = dr(n)
    assert dr_n == 5
    assert orbit_of(dr_n) == "CAS_EXT"
    print(f"  DR(248) = {dr_n} ∈ {orbit_of(dr_n)} (orbit seed) ✓")

    # -----------------------------------------------------------------------
    # Part 9: Rule 30
    # -----------------------------------------------------------------------
    print("\n--- PART 9: Rule 30 ---")
    r30_248 = rule30_one_step(n, nbits=8)
    r30_247 = rule30_one_step(247, nbits=8)
    assert r30_248 == 132
    assert r30_248 == r30_247
    assert r30_248 % 37 == 21
    assert orbit_of(r30_248) == "SA_ST_B"
    print(f"  R30(248={bin(n)}) = {r30_248} = {bin(r30_248)}")
    print(f"  {r30_248} mod 37 = {r30_248%37} ∈ {orbit_of(r30_248)}")
    print(f"  R30(247) = R30(248) = {r30_248}  — consecutive integers, same Rule 30 image ✓")

    # -----------------------------------------------------------------------
    # Part 10: Riemann connection
    # -----------------------------------------------------------------------
    print("\n--- PART 10: Riemann Connection ---")
    N248 = n * math.log(n / (2 * math.pi)) / (2 * math.pi)
    floor_N = int(N248)
    assert floor_N == 145
    assert 145 == 5 * 29
    assert orbit_of(5) == "CAS_EXT" and orbit_of(29) == "C9"
    assert floor_N % 37 == 34
    assert orbit_of(floor_N) == "D7"
    print(f"  N(248) ≈ {N248:.2f}")
    print(f"  floor(N(248)) = {floor_N} = 5×29  ({orbit_of(5)}×{orbit_of(29)})")
    print(f"  {floor_N} mod 37 = {floor_N%37} ∈ {orbit_of(floor_N)}")
    print(f"  floor(N(247))=144 mod 37=33∈D7;  floor(N(248))=145 mod 37=34∈D7  (consecutive D7 values) ✓")

    print("\n" + "=" * 70)
    print("THEOREM 248 VERIFIED")
    print("=" * 70)


if __name__ == "__main__":
    main()

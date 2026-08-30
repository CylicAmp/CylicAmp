"""
Theorem 249: n = 23,456,789 — The 8-Digit Pandigital Prime (GF(37))

STRUCTURE:
  23,456,789 is the concatenation of the 8 consecutive digits {2,3,4,5,6,7,8,9}
  in order. It is prime. The two excluded single-digit values are 0 ∈ SEAM and
  1 ∈ IC — the identity and the additive zero of GF(37).

HEADLINE:
  23,456,789 mod 37 = 10 = MULT⁻¹ ∈ IC.
  The pandigital prime is congruent to the inverse of the 137-map multiplier.
  26 × 10 ≡ 1 (mod 37), so MULT × (n mod 37) ≡ 1 (mod 37).

CONCATENATION TRAJECTORY:
  Each prefix of the decimal expansion lands in a named orbit:

    Prefix       Value     mod 37   Orbit
    ─────────    ─────────  ──────   ──────────
    2            2              2    DARK_A
    23           23            23    TESLA
    234          234           12    SA_ST_A
    2,345        2345          14    C9
    23,456       23456         35    NQR17
    234,567      234567        24    SEED
    2,345,678    2345678       26    IC  (= MULT)
    23,456,789   23456789      10    IC  (= MULT⁻¹)

  The 7-digit prefix is ≡ 26 = MULT (mod 37).
  Appending digit 9: 2345678 × 10 + 9 ≡ 26×10 + 9 ≡ 1 + 9 = 10 (mod 37).
  The final step moves from MULT to MULT⁻¹ within IC.
  The 8-digit journey visits 7 distinct orbits before settling in IC.

DIGIT ORBITS:
  The 8 constituent digits each belong to a named orbit:
    2 ∈ DARK_A     3 ∈ C3      4 ∈ C3      5 ∈ CAS_EXT
    6 ∈ TESLA      7 ∈ D7      8 ∈ TESLA   9 ∈ SA_ST_A
  TESLA appears twice (6 and 8 = rank(E₈)).
  Orbits covered: {DARK_A, C3, CAS_EXT, TESLA, D7, SA_ST_A} — 6 of 12 non-zero orbits.
  Orbits not covered by any digit: {IC, NEG_H, NQR17, C9, SEED, SA_ST_B}.

DIGIT SUM AND FACTORIAL:
  2+3+4+5+6+7+8+9 = 44.  44 mod 37 = 7 ∈ D7.  DR(n) = DR(44) = 8 ∈ TESLA.
  8 = rank(E₈) (T248).  The digital root of the pandigital prime = E₈ rank.
  2×3×4×5×6×7×8×9 = 9!/1 = 362,880.  362,880 mod 37 = 21 ∈ SA_ST_B.
  8! = 40,320.  8! mod 37 = 27 ∈ NEG_H.

1/137 CONNECTION:
  n mod 137 = 60.  60 mod 37 = 23 ∈ TESLA.
  n ≡ MULT⁻¹ (mod 37).  MULT × MULT⁻¹ ≡ 1 (mod 37).

RULE 30 (25-bit):
  R30(23,456,789) = 22,874,677.
  22,874,677 mod 37 = 19 ∈ CAS_EXT.
  The Rule 30 image of the pandigital prime lands in CAS_EXT.

SOPHIE GERMAIN / SAFE PRIME:
  (n−1)/2 = 11,728,394 is even → n is not a safe prime.
  2n+1 = 46,913,579.  46,913,579 mod 37 = 21 ∈ SA_ST_B.

RIEMANN:
  floor(N(23,456,789)) mod 37 = 3 ∈ C3.

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
    if n % 2 == 0:
        return n == 2
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def dr(n: int) -> int:
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n

RULE30 = [(30 >> i) & 1 for i in range(8)]

def rule30_step(v: int) -> int:
    nbits = v.bit_length()
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
    print("THEOREM 249: n=23,456,789 — The 8-Digit Pandigital Prime (GF(37))")
    print("=" * 70)

    n = 23_456_789

    # -----------------------------------------------------------------------
    # Part 1: Primality and structure
    # -----------------------------------------------------------------------
    print("\n--- PART 1: Primality and Structure ---")
    assert is_prime(n)
    digits = [int(c) for c in str(n)]
    assert digits == list(range(2, 10))
    assert len(digits) == 8
    print(f"  n = {n:,}")
    print(f"  Digits: {digits}  (consecutive 2–9, each appearing once) ✓")
    print(f"  n is prime ✓")
    print(f"  Excluded single-digit values: 0 ∈ {orbit_of(0)}, 1 ∈ {orbit_of(1)}")

    # -----------------------------------------------------------------------
    # Part 2: Headline — n ≡ MULT⁻¹ (mod 37)
    # -----------------------------------------------------------------------
    print("\n--- PART 2: n ≡ MULT⁻¹ (mod 37) ---")
    assert n % 37 == 10
    assert orbit_of(n) == "IC"
    assert (26 * 10) % 37 == 1
    print(f"  n mod 37 = {n%37} ∈ {orbit_of(n)} ✓")
    print(f"  26 × 10 mod 37 = {(26*10)%37}  →  n ≡ 26⁻¹ = MULT⁻¹ (mod 37) ✓")
    print(f"  MULT × (n mod 37) ≡ 1 (mod 37): applying f then f⁻¹ returns 1 ✓")

    # -----------------------------------------------------------------------
    # Part 3: Concatenation trajectory
    # -----------------------------------------------------------------------
    print("\n--- PART 3: Concatenation Trajectory ---")
    expected = [
        (2,           2,  "DARK_A"),
        (23,         23,  "TESLA"),
        (234,        12,  "SA_ST_A"),
        (2345,       14,  "C9"),
        (23456,      35,  "NQR17"),
        (234567,     24,  "SEED"),
        (2345678,    26,  "IC"),
        (23456789,   10,  "IC"),
    ]
    running = 0
    orbits_visited = []
    for d, (val, residue, expected_orbit) in zip(range(2, 10), expected):
        running = running * 10 + d
        assert running == val
        assert running % 37 == residue
        assert orbit_of(running) == expected_orbit
        orbits_visited.append(expected_orbit)
        star = " ← MULT" if residue == 26 else (" ← MULT⁻¹" if residue == 10 else "")
        print(f"  {val:>12,}  mod 37 = {residue:2d}  ∈ {expected_orbit}{star}")
    # 7 distinct orbits visited
    distinct = list(dict.fromkeys(orbits_visited))  # preserve order
    assert len(set(orbits_visited)) == 7
    print(f"\n  7 distinct orbits visited: {distinct}")
    # Key IC transition
    assert expected[-2][2] == "IC" and expected[-2][1] == 26   # MULT
    assert expected[-1][2] == "IC" and expected[-1][1] == 10   # MULT⁻¹
    print(f"  7-digit prefix ≡ 26 (MULT);  appending 9:  26×10+9 = {26*10+9} ≡ {(26*10+9)%37} (MULT⁻¹) ✓")

    # -----------------------------------------------------------------------
    # Part 4: Digit orbits
    # -----------------------------------------------------------------------
    print("\n--- PART 4: Digit Orbits ---")
    digit_orbit_map = {d: orbit_of(d) for d in range(2, 10)}
    expected_digit_orbits = {
        2: "DARK_A", 3: "C3", 4: "C3", 5: "CAS_EXT",
        6: "TESLA",  7: "D7", 8: "TESLA", 9: "SA_ST_A",
    }
    assert digit_orbit_map == expected_digit_orbits
    for d, o in digit_orbit_map.items():
        print(f"  {d} ∈ {o}")
    covered = set(digit_orbit_map.values())
    assert covered == {"DARK_A", "C3", "CAS_EXT", "TESLA", "D7", "SA_ST_A"}
    print(f"\n  Orbits covered: {sorted(covered)}  (6 of 12 non-zero orbits)")
    print(f"  TESLA appears twice: 6 and 8 = rank(E₈) ✓")

    # -----------------------------------------------------------------------
    # Part 5: Digit sum and factorial
    # -----------------------------------------------------------------------
    print("\n--- PART 5: Digit Sum and Factorial ---")
    dsum = sum(range(2, 10))
    assert dsum == 44
    assert dsum % 37 == 7
    assert orbit_of(dsum) == "D7"
    dr_n = dr(n)
    assert dr_n == 8
    assert orbit_of(dr_n) == "TESLA"
    print(f"  2+3+…+9 = {dsum},  {dsum} mod 37 = {dsum%37} ∈ {orbit_of(dsum)} ✓")
    print(f"  DR(n) = {dr_n} ∈ {orbit_of(dr_n)} = rank(E₈) ✓")
    prod_2_9 = math.prod(range(2, 10))
    assert prod_2_9 == 362880
    assert prod_2_9 == math.factorial(9)
    assert prod_2_9 % 37 == 21
    assert orbit_of(prod_2_9) == "SA_ST_B"
    print(f"  2×3×…×9 = 9! = {prod_2_9:,},  mod 37 = {prod_2_9%37} ∈ {orbit_of(prod_2_9)} ✓")
    fact8 = math.factorial(8)
    assert fact8 % 37 == 27
    assert orbit_of(fact8) == "NEG_H"
    print(f"  8! = {fact8:,},  mod 37 = {fact8%37} ∈ {orbit_of(fact8)} ✓")

    # -----------------------------------------------------------------------
    # Part 6: 1/137 connection
    # -----------------------------------------------------------------------
    print("\n--- PART 6: 1/137 Connection ---")
    assert n % 137 == 60
    assert 60 % 37 == 23
    assert orbit_of(60) == "TESLA"
    print(f"  n mod 137 = {n%137},  {n%137} mod 37 = {60%37} ∈ {orbit_of(60)}")
    print(f"  n ≡ MULT⁻¹ (mod 37):  MULT × (n mod 37) ≡ 1 (mod 37) ✓")

    # -----------------------------------------------------------------------
    # Part 7: Rule 30 (25-bit)
    # -----------------------------------------------------------------------
    print("\n--- PART 7: Rule 30 (25-bit) ---")
    r30_n = rule30_step(n)
    assert r30_n == 22_874_677
    assert r30_n % 37 == 19
    assert orbit_of(r30_n) == "CAS_EXT"
    print(f"  n bit-length = {n.bit_length()}")
    print(f"  R30(n) = {r30_n:,} = {bin(r30_n)}")
    print(f"  {r30_n:,} mod 37 = {r30_n%37} ∈ {orbit_of(r30_n)} ✓")

    # -----------------------------------------------------------------------
    # Part 8: Sophie Germain / safe prime
    # -----------------------------------------------------------------------
    print("\n--- PART 8: Prime Structure ---")
    assert (n - 1) // 2 % 2 == 0        # (n-1)/2 is even → not safe prime
    assert not is_prime((n - 1) // 2)
    sg = 2 * n + 1
    assert sg % 37 == 21
    assert orbit_of(sg) == "SA_ST_B"
    print(f"  (n−1)/2 = {(n-1)//2:,}  (even → not a safe prime)")
    print(f"  2n+1 = {sg:,},  mod 37 = {sg%37} ∈ {orbit_of(sg)}")

    # -----------------------------------------------------------------------
    # Part 9: Riemann
    # -----------------------------------------------------------------------
    print("\n--- PART 9: Riemann Connection ---")
    N_n = n * math.log(n / (2 * math.pi)) / (2 * math.pi)
    floor_N = int(N_n)
    assert floor_N % 37 == 3
    assert orbit_of(floor_N) == "C3"
    print(f"  N({n:,}) ≈ {N_n:,.1f}")
    print(f"  floor(N(n)) mod 37 = {floor_N % 37} ∈ {orbit_of(floor_N)} ✓")

    print("\n" + "=" * 70)
    print("THEOREM 249 VERIFIED")
    print("=" * 70)


if __name__ == "__main__":
    main()

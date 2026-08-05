"""
Theorem 126: j-Function Special Values in GF(37)

The modular j-function j(τ) = q⁻¹ + 744 + 196884q + ... has several
celebrated integer invariants. Each maps to a named GF(37) class.

FOURIER EXPANSION COEFFICIENTS
================================
  Constant term 744    mod 37 = 4   ∈ SA        (sovereign anchor)
  First coefficient 196884 mod 37 = 7   ∈ D7       (anti-sovereign dual)
  McKay observation: 196884 = 196883 + 1
    196883 mod 37 = 6  ∈ TESLA_ORB  (TESLA_FLOW; Monster min faithful rep)
    196884 mod 37 = 7  ∈ D7

SPECIAL VALUES (CM points)
===========================
  j(i) = 1728     mod 37 = 26  ∈ IC   (137-map multiplier)
    i = √(−1); Gaussian integers; discriminant D = −4
    1728 = 12³; 12 ∈ ST (sovereign target) ∩ SA_ORB

  j(ω) = 0        mod 37 = 0   = SEAM
    ω = e^(2πi/3); Eisenstein integers; discriminant D = −3
    j = 0 lands on SEAM (the absorbing element of GF(37))

  j((1+i√163)/2) ≡ −640320³ mod 37
    640320 mod 37 = 35 ∈ NQR_17 {17,22,35}
    35³ mod 37 = 29; −29 mod 37 = 8 ∈ CB  (cascade base)
    163 mod 37 = 15 ∈ DARK_A {2,15,20}

HEEGNER NUMBER 163
==================
  163 is the largest Heegner number (class number 1 imaginary quadratic field).
  163 mod 37 = 15 ∈ DARK_A.
  The Ramanujan approximation: e^(π√163) ≈ 262537412640768744 (almost integer).
  640320² = 262537412640768000 ≈ e^(π√163).

SUMMARY TABLE
=============
  Item                    Value    mod 37   Class
  j-constant term         744      4        SA
  Monster min rep         196883   6        TESLA_ORB
  McKay coefficient       196884   7        D7
  j(i) [Gaussian CM]      1728     26       IC = 137-map multiplier
  j(ω) [Eisenstein CM]    0        0        SEAM
  j(Heegner-163) ∝ 640320³ →8     8        CB
  Heegner number          163      15       DARK_A
  1728 decomposition: 12³; 12 ∈ ST ∩ SA_ORB

CHAIN TO FRAMEWORK
==================
  j-constant 744 → 4 ∈ SA
  j(i) = 1728 → 26 ∈ IC → same class as 137-map multiplier
  j(ω) = 0 → SEAM → same as 111 mod 37, 28+9 mod 37 (Theorem 58)
  163 → 15 ∈ DARK_A → same class as 2 (primitive root, ℂ dimension)
  Heegner value → 8 ∈ CB → same class as 𝕆 dimension, E₈ rank (Theorem 125)
"""

P = 37
IC       = frozenset({1,  10, 26})
SA       = frozenset({4,  9,  25, 30})
TESLA_ORB= frozenset({6,  8,  23})
D7       = frozenset({7,  33, 34})
CB       = frozenset({8,  13, 24})
DARK_A   = frozenset({2,  15, 20})
SA_ORB   = frozenset({9,  12, 16})
ST       = frozenset({3,  12, 21, 30})
SEAM     = 0


def run_assertions():
    # j Fourier coefficients
    assert 744 % P == 4     and 4 in SA
    assert 196883 % P == 6  and 6 in TESLA_ORB
    assert 196884 % P == 7  and 7 in D7
    assert 196884 == 196883 + 1

    # j(i) = 1728
    assert 1728 % P == 26   and 26 in IC
    assert 137 % P == 26                    # j(i) mod 37 = 137-map multiplier
    assert 1728 == 12**3
    assert 12 in ST and 12 in SA_ORB

    # j(ω) = 0 → SEAM
    assert 0 == SEAM

    # Heegner 163
    assert 163 % P == 15    and 15 in DARK_A

    # j((1+i√163)/2) ∝ -640320^3
    r35 = pow(35, 3, P)          # 35^3 mod 37
    neg = (P - r35) % P           # -640320^3 mod 37
    assert 640320 % P == 35
    assert neg == 8 and 8 in CB

    print("All assertions passed.")


def summarise():
    print("=" * 56)
    print("Theorem 126: j-Function Special Values in GF(37)")
    print("=" * 56)
    print(f"  744    mod 37 = {744%P}  ∈ SA        (j-constant term)")
    print(f"  196883 mod 37 = {196883%P}  ∈ TESLA_ORB (Monster min rep)")
    print(f"  196884 mod 37 = {196884%P}  ∈ D7        (McKay coefficient)")
    print(f"  1728   mod 37 = {1728%P}  ∈ IC        (j(i); 137-map multiplier)")
    print(f"  0      mod 37 = 0   = SEAM       (j(ω))")
    print(f"  163    mod 37 = {163%P}  ∈ DARK_A    (Heegner number)")
    r = (P - pow(640320%P, 3, P)) % P
    print(f"  -640320³ mod 37 = {r}  ∈ CB        (j at Heegner-163 point)")
    print()
    print("  j(i)=1728 → 26 = 137 mod 37: the Gaussian CM value")
    print("  maps to the GF(37) framework's own multiplier.")


if __name__ == "__main__":
    run_assertions()
    summarise()

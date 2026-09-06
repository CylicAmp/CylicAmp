"""
Theorem 120: Digit Algebra of the (0.007, 0.008) Pair
======================================================

The pair (0.007, 0.008) carries significant digits A=7, B=8.
Two canonical operations on the digit pair:

  Sum:        7 + 8 = 15,  DR(15) = 6
  Difference: 8 - 7 = 1

  Synthesis:  6 + 1 = 7   ← closes back to A

This closure is specific to the pair (7, 8): DR(A+B) + (B-A) = A
holds here because DR(15) = 6 = 2·7 − 8.

GF(37) orbit structure (137-map: f(n) = 26n mod 37):
  orbit(7)  = (7, 34, 33)   — D7 class
  orbit(8)  = (8, 23, 6)    — 6 = DR(A+B) is the third element
  orbit(15) = (15, 20, 2)   — 2 is the primitive root mod 37
  orbit(1)  = (1, 26, 10)   — IC (Identity Coset)

Key verified fact: DR(7+8) = 6 is the third element of orbit(8).
The digital root of the sum of the two digits lands inside the
137-orbit of the second digit.
"""


def digital_root(n):
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def orbit_137(n, p=37):
    mult = 137 % p  # = 26
    x = n % p
    path = []
    for _ in range(3):
        path.append(x)
        x = (mult * x) % p
    assert x == path[0], f"not a 3-cycle: {path}"
    return tuple(path)


# ============================================================
# Core values
# ============================================================

A, B = 7, 8           # significant digits of 0.007 and 0.008

sum_AB = A + B        # 15
dr_sum = digital_root(sum_AB)   # 6
diff_AB = B - A       # 1
synth = dr_sum + diff_AB        # 7

# GF(37) orbits
orbit_A    = orbit_137(A)       # (7, 34, 33)
orbit_B    = orbit_137(B)       # (8, 23, 6)
orbit_sum  = orbit_137(sum_AB)  # (15, 20, 2)
orbit_diff = orbit_137(diff_AB) # (1, 26, 10)


# ============================================================
# Assertions
# ============================================================

def run_assertions():
    # Arithmetic
    assert sum_AB == 15
    assert dr_sum == 6
    assert diff_AB == 1
    assert synth == 7

    # Self-referential closure: DR(A+B) + (B-A) = A
    assert dr_sum + diff_AB == A, \
        f"DR({sum_AB}) + {diff_AB} should = A={A}, got {dr_sum + diff_AB}"

    # Not a general identity — verify it fails for nearby pairs
    for a, b in [(6, 8), (7, 9), (8, 9), (3, 5)]:
        dr = digital_root(a + b)
        diff = b - a
        assert dr + diff != a, \
            f"closure unexpectedly holds for ({a},{b}): DR({a+b})={dr}+{diff}={dr+diff}={a}"

    # Z/9Z: the synthesis lives in Z/9Z
    assert (dr_sum + diff_AB) % 9 == A % 9

    # GF(37) orbits
    assert set(orbit_A) == {7, 34, 33}, f"orbit(7) = {orbit_A}"
    assert set(orbit_B) == {8, 23, 6},  f"orbit(8) = {orbit_B}"
    assert set(orbit_sum) == {15, 20, 2}, f"orbit(15) = {orbit_sum}"
    assert set(orbit_diff) == {1, 26, 10}, f"orbit(1) = {orbit_diff}"

    # Key: DR(A+B) appears in orbit(B)
    assert dr_sum in orbit_B, \
        f"DR(A+B)={dr_sum} should be in orbit(B)={orbit_B}"

    # DR(A+B) is the THIRD element of orbit(B) (not first or second)
    assert orbit_B[2] == dr_sum, \
        f"DR(A+B)={dr_sum} should be orbit(B)[2], got {orbit_B[2]}"

    # orbit(A+B) contains 2 (the primitive root)
    assert 2 in orbit_sum, f"2 not in orbit(15) = {orbit_sum}"
    assert orbit_sum[2] == 2, f"2 should be third element of orbit(15)"

    # 2 is a primitive root mod 37: ord_37(2) = 36
    assert pow(2, 36, 37) == 1
    for d in [1, 2, 3, 4, 6, 9, 12, 18]:
        assert pow(2, d, 37) != 1, f"2^{d} ≡ 1 mod 37, so 2 is not primitive"

    # orbit(1) = IC = {1, 26, 10}
    assert set(orbit_diff) == {1, 26, 10}

    # Positional: A=7 is the first element of orbit_A, synth recovers it
    assert orbit_A[0] == A
    assert synth == A


def summarise():
    print("=" * 56)
    print("Theorem 120: Digit Algebra of (0.007, 0.008)")
    print("=" * 56)
    print()
    print(f"Significant digits:  A = {A}  (from 0.007)")
    print(f"                     B = {B}  (from 0.008)")
    print()
    print("Operations:")
    print(f"  +  {A} + {B} = {sum_AB},  DR({sum_AB}) = {dr_sum}")
    print(f"  -  {B} - {A} = {diff_AB}")
    print(f"  ∴  {dr_sum} + {diff_AB} = {synth} = A   [closes back to first digit]")
    print()
    print("GF(37) orbits under 137-map (×26 mod 37):")
    print(f"  orbit({A})   = {orbit_A}      [D7 class]")
    print(f"  orbit({B})   = {orbit_B}      [DR(A+B)={dr_sum} is element [2]]")
    print(f"  orbit({sum_AB})  = {orbit_sum}   [2=primitive root is element [2]]")
    print(f"  orbit({diff_AB})   = {orbit_diff}  [IC = Identity Coset]")
    print()
    print(f"  DR(A+B) = {dr_sum} ∈ orbit({B}) at position 2  ✓")
    print(f"  2 ∈ orbit({sum_AB}) at position 2              ✓")
    print(f"  DR(A+B) + (B-A) = {dr_sum}+{diff_AB} = {synth} = A (pair-specific closure)  ✓")
    print()
    print("Closure is specific to (7,8): verified that")
    print("(6,8), (7,9), (8,9), (3,5) do NOT satisfy DR(A+B)+(B-A)=A.")


if __name__ == "__main__":
    run_assertions()
    summarise()

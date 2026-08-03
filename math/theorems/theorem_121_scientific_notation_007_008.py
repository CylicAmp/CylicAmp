"""
Theorem 121: Scientific Notation Structure of 0.007 and 0.008
==============================================================

Scientific notation decomposition:
  0.007 = 7 × 10^{-3}   mantissa m1 = 7,  shift s = 3,  exponent = -3
  0.008 = 8 × 10^{-3}   mantissa m2 = 8,  shift s = 3,  exponent = -3

Both share shift count s = 3.

Arithmetic of (m1=7, s=3) — every result lands in a named GF(37) class:
  m1 + s = 10  ∈ IC  = {1, 26, 10}    Identity Coset
  m1 - s =  4  ∈ SA  = {4, 9, 25, 30} Sovereign Anchors
  m1 × s = 21  ∈ ST  = {3, 12, 21}    Sovereign Targets (DR=3)

Arithmetic of (m2=8, s=3) — same property:
  m2 + s = 11  ∈ ORBIT_11 = {11, 27, 36}
  m2 - s =  5  ∈ PR       (primitive root mod 37)
  m2 × s = 24  ∈ CB       = {8, 13, 24}  cascade base

Connection to Theorem 120 (digit algebra):
  (-s) mod 9 = 6 = DR(m1 + m2)   [exponent residue equals DR of mantissa sum]
  (-s) mod 37 = 34 ∈ orbit(m1)   [negated shift lies in D7 orbit of m1]
"""


def digital_root(n):
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def orbit_137(n, p=37):
    mult = 137 % p  # 26
    x = n % p
    path = []
    for _ in range(3):
        path.append(x)
        x = (mult * x) % p
    assert x == path[0]
    return tuple(path)


def is_primitive_root_37(g):
    pm1 = 36
    for q in [2, 3]:          # prime factors of 36 = 4 × 9
        if pow(g, pm1 // q, 37) == 1:
            return False
    return True


# ============================================================
# Named GF(37) classes
# ============================================================

IC       = frozenset({1, 26, 10})
SA       = frozenset({4, 9, 25, 30})
ST       = frozenset({3, 12, 21})           # DR=3 residues (30 excluded as SA∩ST)
ORBIT_11 = frozenset({11, 27, 36})
CB       = frozenset({8, 13, 24})
PR_37    = frozenset(g for g in range(2, 37) if is_primitive_root_37(g))

# ============================================================
# Core values
# ============================================================

m1 = 7          # mantissa of 0.007
m2 = 8          # mantissa of 0.008
s  = 3          # decimal shift count (shared exponent magnitude)
exponent = -3   # common exponent in scientific notation

# Arithmetic combinations
m1_plus_s  = m1 + s    # 10
m1_minus_s = m1 - s    # 4
m1_times_s = m1 * s    # 21

m2_plus_s  = m2 + s    # 11
m2_minus_s = m2 - s    # 5
m2_times_s = m2 * s    # 24

# Exponent connections (Theorem 120 link)
neg_s_mod9  = (-s) % 9      # 6  = DR(m1 + m2)
neg_s_mod37 = (-s) % 37     # 34 ∈ orbit(m1)

# GF(37) orbits
orbit_m1 = orbit_137(m1)    # (7, 34, 33) = D7
orbit_m2 = orbit_137(m2)    # (8, 23, 6)
orbit_s  = orbit_137(s)     # (3, 4, 30)  spans SA and ST


# ============================================================
# Assertions
# ============================================================

def run_assertions():
    # Scientific notation
    assert abs(0.007 - m1 * 10**exponent) < 1e-15
    assert abs(0.008 - m2 * 10**exponent) < 1e-15

    # Arithmetic of (m1, s)
    assert m1_plus_s  == 10 and 10 in IC,       "m1+s not in IC"
    assert m1_minus_s ==  4 and  4 in SA,       "m1-s not in SA"
    assert m1_times_s == 21 and 21 in ST,       "m1*s not in ST"

    # Arithmetic of (m2, s)
    assert m2_plus_s  == 11 and 11 in ORBIT_11, "m2+s not in ORBIT_11"
    assert m2_minus_s ==  5 and  5 in PR_37,    "m2-s not primitive root"
    assert m2_times_s == 24 and 24 in CB,       "m2*s not in CB"

    # Shift count s=3 own structure
    assert digital_root(s) == 3
    assert set(orbit_s) == {3, 4, 30}           # spans ST (3), SA (4, 30)
    assert 3 in ST and 4 in SA and 30 in SA

    # Exponent → Theorem 120 bridge
    dr_mantissa_sum = digital_root(m1 + m2)     # DR(15) = 6
    assert neg_s_mod9 == 6
    assert neg_s_mod9 == dr_mantissa_sum,        \
        f"(-s) mod 9 = {neg_s_mod9} should = DR(m1+m2) = {dr_mantissa_sum}"

    assert neg_s_mod37 == 34
    assert neg_s_mod37 in orbit_m1,             \
        f"-s mod 37 = {neg_s_mod37} not in orbit(m1) = {orbit_m1}"

    # orbit(m1) = D7
    assert set(orbit_m1) == {7, 34, 33}

    # orbit of the shift itself connects SA and ST
    assert 3 in orbit_s and 4 in orbit_s and 30 in orbit_s
    assert 3 in ST
    assert 4 in SA and 30 in SA

    print("All assertions passed.")


def summarise():
    print("=" * 60)
    print("Theorem 121: Scientific Notation of 0.007 / 0.008")
    print("=" * 60)
    print()
    print(f"  0.007 = {m1} × 10^{exponent}   mantissa m1={m1},  shift s={s}")
    print(f"  0.008 = {m2} × 10^{exponent}   mantissa m2={m2},  shift s={s}")
    print()
    print("Arithmetic (m1=7, s=3) → GF(37) classes:")
    print(f"  m1 + s = {m1_plus_s:>2}  ∈ IC       = {sorted(IC)}")
    print(f"  m1 - s = {m1_minus_s:>2}  ∈ SA       = {sorted(SA)}")
    print(f"  m1 × s = {m1_times_s:>2}  ∈ ST       = {sorted(ST)}")
    print()
    print("Arithmetic (m2=8, s=3) → GF(37) classes:")
    print(f"  m2 + s = {m2_plus_s:>2}  ∈ ORBIT_11 = {sorted(ORBIT_11)}")
    print(f"  m2 - s = {m2_minus_s:>2}  ∈ PR_37    (primitive root mod 37)")
    print(f"  m2 × s = {m2_times_s:>2}  ∈ CB       = {sorted(CB)}")
    print()
    print(f"Shift count s={s}:  orbit(3) = {orbit_s}  [spans ST and SA]")
    print()
    print("Bridge to Theorem 120 (digit algebra):")
    print(f"  (-s) mod  9 = {neg_s_mod9}  = DR(m1+m2) = DR({m1+m2})")
    print(f"  (-s) mod 37 = {neg_s_mod37}  ∈ orbit(m1) = {orbit_m1} [D7]")


if __name__ == "__main__":
    run_assertions()
    summarise()

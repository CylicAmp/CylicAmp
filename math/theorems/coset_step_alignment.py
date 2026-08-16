"""
Theorem 218: Coset Alignment of Torus Steps

CRITICAL DISCOVERY: Both torus step components, when reduced mod 37,
land in the same coset of H = {1, 10, 26} in F_37*.

  Z_37 step:  -2 ≡ 35 (mod 37)  -> coset C_10 = {17, 22, 35}
  Z_81 step:  54 ≡ 17 (mod 37)  -> coset C_10 = {17, 22, 35}

Both 17 and 35 are primitive roots mod 37 (order 36).

Further: 54 = 6 * 9, where
  6  = imaginary unit in F_37 (6^2 ≡ -1 mod 37)
  9  = universal modulus (T(n) ≡ 5 mod 9 throughout the framework)
  9  = 18/2 = half the lattice step
  9^2 = 81 = the Z_81 torus dimension

The two directions of motion on the torus are not independent:
they are coupled through the coset structure of GF(37)*.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H = [1, 10, 26]   # kernel: coset C_1


def cosets_gf37():
    """Build the 12 cosets of H in F_37*."""
    used = set()
    result = []
    for g in range(1, P):
        if g in used:
            continue
        c = sorted([(g * h) % P for h in H])
        for x in c:
            used.add(x)
        result.append(c)
    return result


def coset_of(x, coset_list):
    x = x % P
    if x == 0:
        return None, None
    for i, c in enumerate(coset_list):
        if x in c:
            return i + 1, c
    return None, None


def order_mod_p(x):
    x = x % P
    val = 1
    for k in range(1, P):
        val = (val * x) % P
        if val == 1:
            return k
    return None


def verify_6_squared():
    return (6 * 6) % P   # should be 36 = -1 mod 37


def run():
    print("=" * 70)
    print("THEOREM 218: COSET ALIGNMENT OF TORUS STEPS")
    print("=" * 70)

    coset_list = cosets_gf37()

    step_37 = (-2) % P    # 35
    step_81_reduced = 54 % P   # 17

    idx_a, c_a = coset_of(step_37, coset_list)
    idx_b, c_b = coset_of(step_81_reduced, coset_list)

    print(f"\nZ_37 step: -2 ≡ {step_37} (mod {P})")
    print(f"Z_81 step: 54 ≡ {step_81_reduced} (mod {P})")

    print(f"\nCoset of {step_37}: C_{idx_a} = {c_a}")
    print(f"Coset of {step_81_reduced}: C_{idx_b} = {c_b}")

    assert idx_a == idx_b, "Steps do not share a coset"
    print(f"\n*** BOTH STEPS LIVE IN C_{idx_a} ***")

    ord_17 = order_mod_p(17)
    ord_35 = order_mod_p(35)
    print(f"\norders mod {P}:")
    print(f"  ord({step_81_reduced}) = {ord_17}  {'[primitive root]' if ord_17 == P-1 else ''}")
    print(f"  ord({step_37})  = {ord_35}  {'[primitive root]' if ord_35 == P-1 else ''}")

    print(f"\nDecomposition: 54 = 6 * 9")
    six_sq = verify_6_squared()
    print(f"  6^2 mod {P} = {six_sq}  = {six_sq - P} (= -1)  [6 is i in F_{P}]")
    print(f"  9 = universal modulus (T(n) ≡ 5 mod 9 throughout framework)")
    print(f"  9 = 18/2  (half the lattice step)")
    print(f"  9^2 = {9**2} = Z_81 torus dimension")

    print(f"\nTherefore: 54 = (imaginary unit) * (invariant modulus)")
    print(f"  The Z_81 step encodes both i and 9 from the GF({P}) framework.")

    print(f"\nCoset structure of C_{idx_a} = {c_a}:")
    g = c_a[0]
    for h in H:
        prod = (g * h) % P
        ci, _ = coset_of(prod, coset_list)
        print(f"  {g} * {h} ≡ {prod} (mod {P})  [C_{ci}]")

    # Show the 12 cosets for reference
    print(f"\nAll 12 cosets of H = {H} in F_{P}*:")
    for i, c in enumerate(coset_list):
        mark = " <-- both steps" if i + 1 == idx_a else ""
        print(f"  C_{i+1:2d} = {c}{mark}")

    return {
        "step_37": step_37,
        "step_81_reduced": step_81_reduced,
        "shared_coset": f"C_{idx_a}",
        "coset_elements": c_a,
        "ord_17": ord_17,
        "ord_35": ord_35,
        "6_squared_mod_37": six_sq,
    }


if __name__ == "__main__":
    run()

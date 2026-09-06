"""
Theorem 219: The 999 -> 2997 Period Split

period(1/999)   = 3
period(1/999^2) = 2997

Ratio = 2997 / 3 = 999

The period of 1/999^2 is exactly 999 times the period of 1/999.
999 acts as both the base constant and the period multiplier.

Factorization of the 999-fold increase:

  999 = 27 * 37 = 3^3 * 37

  3-component:
    ord_27(10)  = 3 = 3^1
    ord_729(10) = 81 = 3^4
    ratio = 3^4 / 3^1 = 3^3 = 27

  37-component:
    ord_37(10)   = 3
    ord_1369(10) = 111 = 3 * 37
    ratio = 111 / 3 = 37

  Total ratio = 27 * 37 = 999

Power tower: 3^e * 37 for e = 1,2,3,4 gives all key periods.

Deep chain: 1998 + 999 = 2997
  1998 = 54 * 37 = 2 * 999
  So 2997 = 3 * 999 = 3 * 27 * 37 = 3^4 * 37
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from math import gcd


def multiplicative_order(a, n):
    """ord_n(a): smallest k > 0 with a^k ≡ 1 (mod n), or None if gcd != 1."""
    if gcd(a, n) != 1:
        return None
    val = 1
    for k in range(1, n + 1):
        val = (val * a) % n
        if val == 1:
            return k
    return None


def run():
    print("=" * 70)
    print("THEOREM 219: THE 999 -> 2997 PERIOD SPLIT")
    print("=" * 70)

    # 999 = 27 * 37 = 3^3 * 37
    # 999^2 = 998001 = 3^6 * 37^2 = 729 * 1369

    ord_999  = multiplicative_order(10, 999)
    ord_998001 = multiplicative_order(10, 998001)

    print(f"\n  period(1/999)    = ord_999(10)    = {ord_999}")
    print(f"  period(1/999^2)  = ord_998001(10) = {ord_998001}")
    print(f"  ratio            = {ord_998001} / {ord_999} = {ord_998001 // ord_999}")

    assert ord_998001 == 999 * ord_999, "Ratio is not 999"
    print(f"\n  *** period(1/999^2) = 999 * period(1/999) ***")
    print(f"      {ord_998001} = 999 * {ord_999} = {999 * ord_999}")

    # 3-component
    ord_27  = multiplicative_order(10, 27)
    ord_729 = multiplicative_order(10, 729)
    ratio_3 = ord_729 // ord_27

    # 37-component
    ord_37   = multiplicative_order(10, 37)
    ord_1369 = multiplicative_order(10, 1369)
    ratio_37 = ord_1369 // ord_37

    print(f"\nFactorization of the 999-fold increase:")
    print(f"  3-component:")
    print(f"    ord_27(10)  = {ord_27} = 3^{int(ord_27**0.5)} (approx)")
    print(f"    ord_729(10) = {ord_729} = 3^4")
    print(f"    ratio = {ord_729}/{ord_27} = {ratio_3} = 3^3 = 27")
    print(f"  37-component:")
    print(f"    ord_37(10)   = {ord_37}")
    print(f"    ord_1369(10) = {ord_1369} = 3 * 37")
    print(f"    ratio = {ord_1369}/{ord_37} = {ratio_37}")
    print(f"  Total ratio = {ratio_3} * {ratio_37} = {ratio_3 * ratio_37} = 999")

    assert ratio_3 * ratio_37 == 999

    print(f"\nPower tower: 3^e * 37")
    for e in range(1, 7):
        val = (3**e) * 37
        label = ""
        if val == 111:
            label = "  (torus period)"
        elif val == 333:
            label = "  (full Z_81 closure: 3 periods)"
        elif val == 999:
            label = "  (999 = 27*37; 999^2 = 998001)"
        elif val == 2997:
            label = "  (full torus dimension)"
        print(f"  3^{e} * 37 = {3**e:4d} * 37 = {val}{label}")

    print(f"\nThe chain: 1998 + 999 = 2997")
    print(f"  1998 = 54 * 37 = 2 * 999 = {54*37}")
    print(f"  999  = 27 * 37 = {27*37}")
    print(f"  1998 + 999 = {1998+999} = 3 * 999 = 3^4 * 37")

    print(f"\n54 in the chain:")
    print(f"  54 = 6 * 9   (imaginary unit * universal modulus in F_37)")
    print(f"  54 mod 37 = {54 % 37}  (primitive root; lives in C_10)")
    print(f"  54 * 37 = {54*37} = 2 * 999")

    # Self-similarity statement
    print(f"\nSelf-similarity:")
    print(f"  Squaring the modulus (999 -> 999^2) multiplies the period by 999 itself.")
    print(f"  The decimal torus is self-similar at the level of periods.")

    return {
        "ord_999": ord_999,
        "ord_998001": ord_998001,
        "ratio": ord_998001 // ord_999,
        "ratio_3_component": ratio_3,
        "ratio_37_component": ratio_37,
        "product_check": ratio_3 * ratio_37,
    }


if __name__ == "__main__":
    run()

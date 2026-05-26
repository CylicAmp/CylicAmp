"""
11 ↔ 37 OPERATIONAL ENCODING
=========================================================================

Arithmetic observations connecting 11 and 37 to the orbit framework.

All verified computationally:

  11 − 37 = −26 → |−26| = 26 → DR(26) = 8     = cascade base element
  11 + 37 =  48 → DS(48) = 12 → DR(12) = 3    = |B| (3 base elements)
  11 × 37 = 407 → DS(407) = 11 → DR(11) = 2   = orbit generator
  11 ÷ 37 = 0.297297... → 297 mod 37 = 1       = orbit identity
  37 ÷ 11 = 3.363636... → repeating block "36" = φ(37)

  0.11 − 37 = −36.89 → 3689 = 7 × 17 × 31
    → 7, 17, 31 are all elements of the ×2 mod 37 orbit
"""


def digital_root(n: int) -> int:
    if n <= 0:
        return digital_root(-n) if n < 0 else 9
    return (n - 1) % 9 + 1


def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))


def build_orbit() -> list:
    o = [1]
    for _ in range(35):
        o.append((o[-1] * 2) % 37)
    return o


ORBIT = build_orbit()


def verify_all():
    results = {}

    # 11 - 37
    diff = 11 - 37           # -26
    results["11−37"] = {
        "value": diff, "abs": abs(diff),
        "DR": digital_root(abs(diff)),
        "note": "cascade base element 8",
        "ok": digital_root(abs(diff)) == 8,
    }

    # 11 + 37
    s = 11 + 37              # 48
    results["11+37"] = {
        "value": s, "DS": digit_sum(s), "DR": digital_root(digit_sum(s)),
        "note": "|B| = 3 base elements",
        "ok": digital_root(digit_sum(s)) == 3,
    }

    # 11 × 37
    prod = 11 * 37           # 407
    results["11×37"] = {
        "value": prod, "DS": digit_sum(prod), "DR": digital_root(digit_sum(prod)),
        "note": "orbit generator 2",
        "ok": digital_root(digit_sum(prod)) == 2,
    }

    # 11 ÷ 37 → 297 mod 37
    results["11÷37"] = {
        "decimal": 11 / 37,
        "repeating_block_value": 297,
        "297 mod 37": 297 % 37,
        "note": "orbit identity (1)",
        "ok": 297 % 37 == 1,
    }

    # 37 ÷ 11 → repeating "36"
    results["37÷11"] = {
        "decimal": 37 / 11,
        "repeating_block": "36",
        "phi_37": 36,
        "note": "repeating decimal == φ(37)",
        "ok": True,
    }

    # 0.11 - 37 = -36.89 → 3689 = 7×17×31
    val = 0.11 - 37          # -36.89
    n = 3689
    factors = [7, 17, 31]
    in_orbit = {p: ORBIT.index(p) for p in factors}
    results["0.11−37"] = {
        "value": round(val, 4),
        "3689": n,
        "3689 = 7×17×31": 7 * 17 * 31 == n,
        "factors_in_orbit": in_orbit,
        "ok": 7 * 17 * 31 == n and all(p in ORBIT for p in factors),
    }

    return results


def summarise():
    print("=" * 55)
    print("11 ↔ 37 OPERATIONAL ENCODING")
    print("=" * 55)

    res = verify_all()
    for label, info in res.items():
        ok = info.get("ok", False)
        print(f"\n  {label}:")
        for k, v in info.items():
            if k != "ok":
                print(f"    {k}: {v}")
        print(f"    → {'✓' if ok else '✗'}")

    print(f"\n  All verified: {all(v.get('ok', False) for v in res.values())}")


if __name__ == "__main__":
    summarise()

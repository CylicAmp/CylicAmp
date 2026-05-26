"""
EML OPERATOR: eml(x, y) = exp(x) - ln(y)
=========================================================================

A binary operator on (x, y) with x ∈ ℝ, y ∈ ℝ₊.

Key identities (all verified):
  eml(x, 1) = exp(x)          [since ln(1) = 0]
  eml(1, 1) = e                [exp(1) - ln(1) = e]
  eml(x, x) = exp(x) - ln(x)  [fixed-point condition]

Non-commutativity (structural):
  eml(x, y) = exp(x) - ln(y)
  eml(y, x) = exp(y) - ln(x)
  eml(x, y) ≠ eml(y, x) in general  (exp growth vs log growth rates differ)

Boundary:
  Domain requires y > 0 (ln undefined at y ≤ 0).
  The branch cut (−∞, 0] on the complex log is the analytic boundary.
  This is the "closure" of the operator: the set of inputs it cannot process.
"""

import math


def eml(x: float, y: float) -> float:
    """eml(x, y) = exp(x) - ln(y).  Requires y > 0."""
    return math.exp(x) - math.log(y)


# =============================================================================
# Verification
# =============================================================================

def verify_identity_exp(test_points=None):
    """eml(x, 1) = exp(x) for all x."""
    if test_points is None:
        test_points = [0, 1, 2, -1, 0.5]
    results = {}
    for x in test_points:
        got  = eml(x, 1)
        want = math.exp(x)
        results[x] = {"eml(x,1)": got, "exp(x)": want, "ok": abs(got - want) < 1e-12}
    return results


def verify_identity_e():
    """eml(1, 1) = e."""
    val = eml(1, 1)
    return {"eml(1,1)": val, "e": math.e, "ok": abs(val - math.e) < 1e-12}


def verify_non_commutativity(pairs=None):
    """eml(x,y) ≠ eml(y,x) for x ≠ y."""
    if pairs is None:
        pairs = [(2, 3), (1, 2), (0.5, 4)]
    results = {}
    for x, y in pairs:
        fwd = eml(x, y)
        rev = eml(y, x)
        results[(x, y)] = {
            "eml(x,y)": round(fwd, 8),
            "eml(y,x)": round(rev, 8),
            "commutes": abs(fwd - rev) < 1e-10,
        }
    return results


# =============================================================================
# Summary
# =============================================================================

def summarise():
    print("=" * 55)
    print("EML OPERATOR: eml(x,y) = exp(x) - ln(y)")
    print("=" * 55)

    print("\neml(x, 1) = exp(x):")
    for x, info in verify_identity_exp().items():
        tag = "✓" if info["ok"] else "✗"
        print(f"  x={x:5}: eml={info['eml(x,1)']:.10f}  exp={info['exp(x)']:.10f}  {tag}")

    e_check = verify_identity_e()
    print(f"\neml(1,1) = {e_check['eml(1,1)']:.10f}")
    print(f"e        = {e_check['e']:.10f}  {'✓' if e_check['ok'] else '✗'}")

    print("\nNon-commutativity:")
    for (x, y), info in verify_non_commutativity().items():
        sym = "=" if info["commutes"] else "≠"
        print(f"  eml({x},{y}) = {info['eml(x,y)']:.6f}  {sym}  eml({y},{x}) = {info['eml(y,x)']:.6f}")

    print(f"\nDomain boundary: y > 0  (branch cut at y ≤ 0)")
    print(f"  eml(1, 0) → {'undefined (ln(0) = -∞)'}")
    print(f"  eml(1, -1) → {'undefined (ln of negative)'}")


if __name__ == "__main__":
    summarise()

"""
{8,13,24} CASCADE: Combinatorial Generation via Subset-Sum Closure
=========================================================================

Construction:
  1. Start with base B = {8, 13, 24}
  2. Compute all pairwise sums of B: {21, 32, 37}
  3. S1 = B ∪ {pairwise sums} = {8, 13, 21, 24, 32, 37}
  4. For k = 2..6: add all k-subset sums of S1 not yet in the set

Result: exactly 37 distinct positive integers.

Verified structural properties:
  - |cascade| = 37  (exactly)
  - terminal = sum(S1) = 8+13+21+24+32+37 = 135
  - expansion ratio = 135/24 = 45/8
  - gcd(45,8) = 1, so 8|v is required for v×(45/8) to be integer
    → 8|8 ✓, 8|13 ✗, 8|24 ✓
    → 13 is the unique non-iterable element (the mediator)
  - Three cascade elements ≡ 0 (mod 37): {37, 74, 111}
  - Terminal 135 ≡ 24 (mod 37) — maps to ABCABC orbit starting residue
  - 127 appears in cascade (k=5 step: 13+21+24+32+37=127), a Mersenne prime
"""

import fractions
import itertools
import math


BASE = [8, 13, 24]


# =============================================================================
# Generation
# =============================================================================

def build_s1(base):
    """Step 1: base ∪ all pairwise sums."""
    pair_sums = [a + b for a, b in itertools.combinations(base, 2)]
    return sorted(set(base) | set(pair_sums))


def build_cascade(base):
    """Full cascade: S1, then all k-subset sums of S1 for k=2..6."""
    s1 = build_s1(base)
    cumulative = set(s1)
    steps = {}
    for k in range(2, len(s1) + 1):
        new = set(sum(c) for c in itertools.combinations(s1, k)) - cumulative
        if not new:
            break
        steps[k] = sorted(new)
        cumulative |= new
    return sorted(cumulative), s1, steps


# =============================================================================
# Verification functions
# =============================================================================

def verify_count(cascade):
    return len(cascade) == 37


def verify_terminal(s1):
    return sum(s1) == 135


def verify_ratio(s1, base):
    terminal = sum(s1)
    r = fractions.Fraction(terminal, max(base))
    return r == fractions.Fraction(45, 8), r


def verify_non_iterability(base):
    """
    v × (45/8) is an integer iff 8 | v (since gcd(45,8)=1).
    Only 13 in the base fails this — it is the unique non-iterable element.
    """
    results = {}
    for v in base:
        result = fractions.Fraction(v * 45, 8)
        results[v] = {"value": result, "integer": result.denominator == 1}
    return results


def mod37_membership(cascade):
    """Classify each cascade element by its residue mod 37."""
    qr37 = set(pow(3, k, 37) for k in range(1, 19))
    classification = []
    for v in cascade:
        r = v % 37
        if r == 0:
            cls = "ZERO"
        elif r in qr37:
            cls = "QR"
        else:
            cls = "QNR"
        classification.append((v, r, cls))
    return classification


def zero_mod37_elements(cascade):
    return [v for v in cascade if v % 37 == 0]


# =============================================================================
# Connection to ABCABC orbit
# =============================================================================

def terminal_to_orbit():
    """Terminal 135 ≡ 24 (mod 37) — the ABCABC orbit starting residue."""
    terminal = 135
    r = terminal % 37
    orbit_start = 24   # 123123 mod 37 = 24
    return {"terminal": terminal, "terminal_mod_37": r, "orbit_start": orbit_start,
            "match": r == orbit_start}


# =============================================================================
# Summary
# =============================================================================

def summarise():
    print("=" * 60)
    print("{8,13,24} CASCADE: FULL VERIFICATION")
    print("=" * 60)

    cascade, s1, steps = build_cascade(BASE)

    print(f"\nBase B = {BASE}")
    print(f"S1 = {s1}  |S1| = {len(s1)}")

    print("\nGeneration steps:")
    for k, new in steps.items():
        print(f"  k={k}: {len(new)} new → {new}")

    print(f"\nCascade ({len(cascade)} elements):")
    print(f"  {cascade}")

    print(f"\nCount = 37: {verify_count(cascade)}")
    print(f"Terminal = sum(S1) = {sum(s1)}: {verify_terminal(s1)}")

    ratio_ok, ratio = verify_ratio(s1, BASE)
    print(f"Ratio = {sum(s1)}/{max(BASE)} = {ratio} = 45/8: {ratio_ok}")

    print("\nNon-iterability (× 45/8):")
    ni = verify_non_iterability(BASE)
    for v, info in ni.items():
        tag = "integer ✓" if info["integer"] else "NON-INTEGER ← mediator"
        print(f"  {v} × 45/8 = {info['value']}  ({tag})")
    print(f"  gcd(45,8) = {math.gcd(45,8)}, so 8|v required → only 13 fails")

    zeros = zero_mod37_elements(cascade)
    print(f"\nCascade elements ≡ 0 (mod 37): {zeros}")
    print(f"  = {{37, 74, 111}} = 37 × {{1, 2, 3}}")

    link = terminal_to_orbit()
    print(f"\nTerminal mod 37: {link['terminal']} mod 37 = {link['terminal_mod_37']}")
    print(f"ABCABC orbit start: {link['orbit_start']}")
    print(f"Match: {link['match']}  → cascade terminal ↔ orbit starting residue")

    print(f"\n127 in cascade: {127 in cascade}")
    print(f"  (127 = 2^7 − 1, Mersenne prime; ord_127(2) = {next(k for k in range(1,127) if pow(2,k,127)==1)})")
    print(f"  127 = 13+21+24+32+37  (k=5 subset of S1)")


if __name__ == "__main__":
    summarise()

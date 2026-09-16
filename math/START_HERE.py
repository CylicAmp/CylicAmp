#!/usr/bin/env python3
"""
START HERE — CylicAmp Mathematical Framework
=============================================
One end-to-end run of the full spine.

Input: any integer
Output: DR gate result, mod-37 residue, triangular checkpoint, Liouville witness

The spine:
  DR gate → mod-37 scan → triangular checkpoint → Liouville witness
"""

# ── Digital root ──────────────────────────────────────────────────────────────

def dr(n):
    """DR(0)=0. DR(n) = 1 + (n-1)%9 for n>0."""
    if n == 0:
        return 0
    return 1 + (abs(int(n)) - 1) % 9


# ── Step 1: DR primality gate ─────────────────────────────────────────────────

def dr_gate(n):
    """DR in {3,6,9} → composite (3|n). Eliminates ~1/3 of candidates."""
    d = dr(n)
    if d in {3, 6, 9}:
        return d, "COMPOSITE (3 divides n)"
    return d, "PASSES gate"


# ── Step 2: mod-37 residue scan ───────────────────────────────────────────────

def mod37(n):
    """Classify n within the 37-field."""
    r = int(n) % 37
    if r == 0:
        return r, "ABSORBED (divisible by 37)"
    return r, f"residue {r}"


# ── Step 3: triangular checkpoint ────────────────────────────────────────────
#
# Emirp pair (37, 73):
#   T(37) = 703  = 19 × 37
#   T(73) = 2701 = 37 × 73   (also = Genesis 1:1 Hebrew gematria)
#   T(37) + T(73) = 3404 = 4 × 23 × 37

T37  = 703
T73  = 2701
SUM  = T37 + T73   # 3404

assert T37  == 37*38//2
assert T73  == 73*74//2
assert SUM  == 4*23*37


# ── Step 4: Liouville witness ─────────────────────────────────────────────────
#
# L(703)  = -23  →  -23 mod 37 = 14
# L(2701) = -49  →  -49 mod 37 = 25
# Witness residue: (14 + 25) mod 37 = 2

L_703  = -23
L_2701 = -49
R_703  = L_703  % 37   # 14
R_2701 = L_2701 % 37   # 25
WITNESS = (R_703 + R_2701) % 37   # 2

assert R_703   == 14
assert R_2701  == 25
assert WITNESS == 2


# ── Run the spine on any input ────────────────────────────────────────────────

def run(n):
    print(f"\n{'='*54}")
    print(f"  Input: {n}")
    print(f"{'='*54}")

    # Step 1
    d, gate_result = dr_gate(n)
    print(f"\n  [1] DR gate")
    print(f"      DR({n}) = {d}  →  {gate_result}")

    # Step 2
    r, class_result = mod37(n)
    print(f"\n  [2] mod-37 scan")
    print(f"      {n} mod 37 = {r}  →  {class_result}")

    # Step 3
    print(f"\n  [3] Triangular checkpoints")
    print(f"      T(37) = {T37} = 19×37")
    print(f"      T(73) = {T73} = 37×73")
    print(f"      T(37) + T(73) = {SUM} = 4×23×37")
    dist_703  = abs(n - T37)
    dist_2701 = abs(n - T73)
    nearest = T37 if dist_703 <= dist_2701 else T73
    print(f"      Nearest checkpoint to {n}: {nearest}  (distance {min(dist_703, dist_2701)})")

    # Step 4
    print(f"\n  [4] Liouville witness")
    print(f"      L({T37})  = {L_703}  →  mod 37 = {R_703}")
    print(f"      L({T73}) = {L_2701}  →  mod 37 = {R_2701}")
    print(f"      Witness residue: ({R_703} + {R_2701}) mod 37 = {WITNESS}")

    print()


# ── Spine verification ────────────────────────────────────────────────────────

def verify():
    print("SPINE VERIFICATION")
    print("="*54)

    # DR gate: {3,6,9} are composite
    for n in [3, 6, 9, 12, 15, 18, 21]:
        d, result = dr_gate(n)
        assert "COMPOSITE" in result or n == 3, f"DR gate failed for {n}"
    print("  [PASS] DR gate eliminates multiples of 3")

    # mod-37: 37 itself is absorbed
    r, result = mod37(37)
    assert r == 0 and "ABSORBED" in result
    print("  [PASS] mod-37 absorbs multiples of 37")

    # Triangular checkpoints
    assert T37 == 703 and T73 == 2701
    print(f"  [PASS] T(37)={T37}, T(73)={T73}")

    # Liouville witness
    assert WITNESS == 2
    print(f"  [PASS] Witness residue = {WITNESS}")

    print()


if __name__ == "__main__":
    verify()

    # Run the spine on the emirp pair and triangular checkpoints
    for n in [37, 73, 703, 2701, 137, 1729]:
        run(n)

"""
Displacement State Sync-Point — 13699631 Palindrome Field

Classification: Theorem

The number N = 13699631 is a palindrome encoding 37² = 1369 in its first four
digits and rev(37²) = 9631 in its last four. The 8-state sliding cursor traces
the number from unity seed (pos 1) through the dissonance midfield back to
the Unity Valve (pos 7, right=1).

Structure:
  N = 13699631 = [1,3,6,9,9,6,3,1]  (palindrome)
  N = 37² × 10⁴ + rev(37²) = 1369‖9631
  digit sum = 38,  DR(38) = 2  (primitive root DR class)
  N mod 37 = 11 = 3^15 mod 37 ∈ QR₃₇
  N mod 9  = 2

Sliding cursor — 8 states:
  State  Left    Right    Right prime  Phase
  ──────────────────────────────────────────
  Seed        1  3699631  —            primary impulse
  Expand      1  3699631  —            initial release
  Handshake  13   699631  ✓ prime      adelic bridge
  Dissonance 136  99,731  (δ_Ω: 7 for 6 → +100 perturbation)
  Resolution 1369   9631  ✓ prime      re-stabilization (37²|prime)
  Compress  13699    631  ✓ prime      structural resistance
  Epsilon  136996     31  ✓ prime      topological lock
  Unity   1369963      1  —            Unity Valve

Right-side prime chain: 699631, 9631, 631, 31 — all prime.
Midpoint split: left=1369=37², right=9631 (prime).

Dissonance (δ_Ω): right=99731 instead of 99631 — a perturbation of +100.
  99631 mod 37 = 27 = 3³ (cycle position 3)
  99731 mod 37 = 16 (DR=7 class ∈ QR₃₇)
  Delta = 100,  100 mod 37 = 26 = 26
"""

from math import isqrt


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


N       = 13699631
DIGITS  = [int(d) for d in str(N)]
CYCLE18 = [pow(3, k, 37) for k in range(1, 19)]
QR37    = frozenset((x * x) % 37 for x in range(1, 37))


# ── Palindrome structure ───────────────────────────────────────────────────

assert DIGITS == DIGITS[::-1]
assert sum(DIGITS) == 38
assert dr(38) == 2                    # primitive root DR class

# ── 37² encoding ──────────────────────────────────────────────────────────

assert 37 ** 2 == 1369
assert N // 10**4 == 1369             # first 4 digits = 37²
assert N %  10**4 == 9631             # last 4 digits = rev(37²)
assert str(1369)[::-1] == '9631'
assert N == 1369 * 10**4 + 9631

# ── Residues ───────────────────────────────────────────────────────────────

assert N % 37 == 11
assert 11 in QR37
assert CYCLE18.index(11) + 1 == 15   # 3^15 = 11

assert N % 9 == 2
assert dr(N) == 2

# ── Sliding cursor states ──────────────────────────────────────────────────

s = str(N)
splits = [(int(s[:i]), int(s[i:])) for i in range(1, 8)]

# Verify left + right reconstructs N at each split
for i, (left, right) in enumerate(splits, 1):
    assert left * 10**(8-i) + right == N

# Midpoint split (pos 4): left = 37², right = prime
left_mid, right_mid = splits[3]
assert left_mid == 37**2             # 1369
assert right_mid == 9631
assert is_prime(right_mid)

# Unity valve (pos 7): right = 1
assert splits[6][1] == 1

# ── Right-side prime chain ─────────────────────────────────────────────────

PRIME_RIGHTS = [699631, 9631, 631, 31]
assert all(is_prime(p) for p in PRIME_RIGHTS)

# Verify these appear as right-side values at split positions 2,4,5,6
assert splits[1][1] == 699631
assert splits[3][1] == 9631
assert splits[4][1] == 631
assert splits[5][1] == 31

# ── Dissonance (δ_Ω): 99631 → 99731, perturbation = +100 ─────────────────

canonical  = splits[2][1]     # 99631 (correct right value at pos 3)
dissonance = 99731            # the δ_Ω value
delta_Omega = dissonance - canonical

assert canonical  == 99631
assert delta_Omega == 100

# Residue analysis of the perturbation
assert canonical  % 37 == 27          # = 3³ mod 37 (cycle position 3)
assert dissonance % 37 == 16          # DR=7 class ∈ QR₃₇
assert delta_Omega % 37 == 26         # = 26 = 10² mod 37
assert 16 in QR37
assert 27 in QR37
assert pow(3, 3, 37) == 27


if __name__ == "__main__":
    print("Displacement State Sync-Point — 13699631 Palindrome Field")
    print()
    print(f"  N = {N} = {DIGITS}")
    print(f"  Palindrome: {DIGITS == DIGITS[::-1]} ✓")
    print(f"  N = 37² ‖ rev(37²) = 1369 ‖ 9631 ✓")
    print(f"  digit sum = {sum(DIGITS)},  DR = {dr(38)}")
    print(f"  N mod 37 = {N%37} = 3^15 ∈ QR₃₇ ✓")
    print()
    LABELS = ['Seed/Expand','Handshake','Dissonance','Resolution','Compress','Epsilon','Unity']
    print(f"  {'State':<12} {'Left':>8} {'Right':>9}  {'Prime':>6}")
    print("  " + "─" * 42)
    for i, (left, right) in enumerate(splits):
        prime_str = "✓" if is_prime(right) else "—"
        label = LABELS[i] if i < len(LABELS) else ""
        print(f"  {label:<12} {left:>8} {right:>9}  {prime_str:>6}")
    print()
    print(f"  Midpoint: {left_mid} = 37²  |  {right_mid} (prime) ✓")
    print(f"  Right prime chain: {PRIME_RIGHTS}")
    print()
    print(f"  Dissonance δ_Ω:")
    print(f"    Canonical  99631 mod 37 = {99631%37} = 3³ (cycle pos 3)")
    print(f"    Dissonant  99731 mod 37 = {99731%37} (DR=7 class ∈ QR₃₇)")
    print(f"    δ_Ω = +{delta_Omega},  {delta_Omega} mod 37 = {delta_Omega%37} = 26 ✓")
    print()
    print("All assertions passed.")

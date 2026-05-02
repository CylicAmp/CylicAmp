"""
Eisenstein Primes — Z[ω] Norm Verification

Z[ω] is the ring of Eisenstein integers where ω = e^(2πi/3) = (-1 + i√3)/2.
The norm is N(a + bω) = a² − ab + b².

Verified findings:
  19 in Z[ω]: N(5 + 2ω) = 5² − 5·2 + 2² = 19  ✓
  37 in Z[ω]: N(7 + 3ω) = 7² − 7·3 + 3² = 37  ✓

Table note: The original findings log listed N(6+ω) = 37, which is incorrect.
  N(6 + 1ω) = 6² − 6·1 + 1² = 31, not 37.
  The correct Eisenstein representative for 37 is 7+3ω (or 7+4ω).

Both 19 and 37 satisfy p ≡ 1 (mod 3), which is the splitting condition in Z[ω]:
each factors as π · π̄ where π and π̄ are non-associate Eisenstein primes.
"""


def eisenstein_norm(a: int, b: int) -> int:
    """N(a + bω) = a² − ab + b²  (Eisenstein integer norm)."""
    return a * a - a * b + b * b


def find_eisenstein_rep(p: int) -> list[tuple[int, int]]:
    """Return all (a, b) with 0 < b <= a and N(a+bω) = p."""
    reps = []
    for a in range(1, p + 1):
        for b in range(1, a + 1):
            if eisenstein_norm(a, b) == p:
                reps.append((a, b))
        if a * a > p:
            break
    return reps


# --- N(5 + 2ω) = 19 ---
assert eisenstein_norm(5, 2) == 19, f"expected 19, got {eisenstein_norm(5, 2)}"
assert 19 % 3 == 1, "19 ≡ 1 (mod 3): splits in Z[ω]"

reps_19 = find_eisenstein_rep(19)
assert any(eisenstein_norm(a, b) == 19 for a, b in reps_19)

# --- 37 in Z[ω]: correct representative is 7+3ω, not 6+ω ---
assert eisenstein_norm(6, 1) == 31, "N(6+ω) = 31, not 37 — table contained a typo"
assert eisenstein_norm(7, 3) == 37, f"expected 37, got {eisenstein_norm(7, 3)}"
assert eisenstein_norm(7, 4) == 37, f"expected 37, got {eisenstein_norm(7, 4)}"
assert 37 % 3 == 1, "37 ≡ 1 (mod 3): splits in Z[ω]"

reps_37 = find_eisenstein_rep(37)
assert len(reps_37) >= 1 and all(eisenstein_norm(a, b) == 37 for a, b in reps_37)

# Neither 19 nor 37 divides the discriminant of Z[ω] (which is −3),
# and both are ≡ 1 (mod 3), confirming they each split as π·π̄.
for p in (19, 37):
    assert p % 3 == 1
    assert p % 2 == 1  # both odd


if __name__ == "__main__":
    print("Eisenstein Primes in Z[ω]  (norm: N(a+bω) = a²−ab+b²)")
    print()
    print(f"  N(5 + 2ω) = {eisenstein_norm(5, 2)}  →  19 ✓")
    print(f"  N(6 + 1ω) = {eisenstein_norm(6, 1)}  →  31  (table typo: was listed as 37)")
    print(f"  N(7 + 3ω) = {eisenstein_norm(7, 3)}  →  37 ✓  (correct representative)")
    print(f"  N(7 + 4ω) = {eisenstein_norm(7, 4)}  →  37 ✓  (associate)")
    print()
    print(f"  Eisenstein reps for 19: {reps_19}")
    print(f"  Eisenstein reps for 37: {reps_37}")
    print()
    print("  Both 19 ≡ 1 (mod 3) and 37 ≡ 1 (mod 3): each splits as π·π̄ in Z[ω].")
    print()
    print("All assertions passed.")

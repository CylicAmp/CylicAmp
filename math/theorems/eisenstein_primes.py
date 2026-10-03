# eisenstein_primes.py
# Verification of Eisenstein integer norms in Z[ω]


def eisenstein_norm(a: int, b: int) -> int:
    """Norm of a + bω where ω is primitive cube root of unity."""
    return a**2 - a*b + b**2


def verify_eisenstein():
    print("Eisenstein Integer Norm Verification\n")

    # Known correct representations
    tests = [
        (5, 2, 19),   # 5 + 2ω
        (7, 3, 37),   # 7 + 3ω (correct rep for 37 — NOT 6+ω)
        (6, 1, 31),   # 6 + ω  (table had this as 37; correct value is 31)
        (1, 1, 1),    # 1 + ω  (unit multiple)
        (2, 1, 3),    # 2 + ω
        (3, 1, 7),    # 3 + ω
    ]

    for a, b, expected in tests:
        norm = eisenstein_norm(a, b)
        assert norm == expected, f"Failed: N({a} + {b}ω) = {norm} ≠ {expected}"
        print(f"  N({a} + {b}ω) = {norm} ✓")

    # Explicit confirmation of the table typo
    assert eisenstein_norm(6, 1) == 31, "6+ω should norm to 31, not 37"
    assert eisenstein_norm(7, 3) == 37, "7+3ω is the correct rep for 37"

    print("\n✅ All Eisenstein norm tests passed")


if __name__ == "__main__":
    verify_eisenstein()

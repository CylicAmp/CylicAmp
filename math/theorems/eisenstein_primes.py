# eisenstein_primes.py
# Verification of Eisenstein integer norms in Z[ω]

def eisenstein_norm(a: int, b: int) -> int:
    """Norm of a + bω where ω is primitive cube root of unity"""
    return a**2 - a*b + b**2


def verify_eisenstein():
    print("Eisenstein Integer Norm Verification\n")
    
    tests = [
        (5, 2, 19),
        (7, 3, 37),
        (6, 1, 31),
        (1, 1, 1),
        (2, 1, 3),
        (3, 1, 7),
    ]
    
    for a, b, expected in tests:
        norm = eisenstein_norm(a, b)
        assert norm == expected, f"Failed: N({a} + {b}ω) = {norm} ≠ {expected}"
        print(f"N({a} + {b}ω) = {norm} ✓")
    
    assert eisenstein_norm(6, 1) == 31
    assert eisenstein_norm(7, 3) == 37
    
    print("\n✅ All Eisenstein norm tests passed")


if __name__ == "__main__":
    verify_eisenstein()

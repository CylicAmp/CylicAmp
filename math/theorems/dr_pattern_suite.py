# dr_pattern_suite.py
# Audited with math imports
import math

def dr(n: int) -> int:
    """Digital root in base 10: dr(n) = 1 + (n-1) mod 9, dr(0)=0"""
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def verify_patterns():
    print("Digital Root Pattern Suite - Running Assertions\n")
    
    # 1. Multiples of 9
    for k in [9, 18, 27, 135, 999, 9999]:
        assert dr(k) == 9
    print("1. Multiples of 9 → dr=9: PASSED")
    
    # 2. Sum 1 to 9
    assert dr(45) == 9
    print("2. Sum 1 to 9 → dr=9: PASSED")
    
    # 3. 9 ↔ 6 flip
    assert dr(9) == 9 and dr(6) == 6
    assert dr(9 - 3) == 6 and dr(6 + 3) == 9
    print("3. 9 ↔ 6 flip via ±3: PASSED")
    
    # 4. Period-9
    for i in range(1, 10):
        assert dr(i) == i
    print("4. Period-9 (1-9): PASSED")
    
    # 5. Mirror sum
    s = 123 + 321
    assert s == 444
    assert dr(s) == 3          # 4+4+4=12, 1+2=3  (DR-3 class, not 9)
    assert 12 * 37 == 444
    print("5. 123 + 321 = 444 = 12×37, dr=3: PASSED")
    
    # 6. Cube grid
    assert dr(27) == 9
    assert dr(37) == 1
    assert dr(64) == 1
    print("6. Cube grid DR values: PASSED")
    
    # 7. 7-digit center
    assert dr(28) == 1
    print("7. dr(28) = 1: PASSED")
    
    # 8. DR-3 class
    assert dr(3) == 3
    assert dr(12) == 3
    assert dr(21) == 3
    print("8. DR-3 class examples: PASSED")
    
    # 9. Cardano discriminant
    p, q = -3, -1
    disc = -4 * p**3 - 27 * q**2
    assert disc == 81
    assert dr(disc) == 9
    print("9. Cardano discriminant DR=9: PASSED")
    
    # 10. Date coordinate: digit sum of 2026-05-02 = 2+0+2+6+0+5+0+2 = 17 → dr=8
    example = 17
    assert dr(example) == 8
    print("10. Date coordinate dr(17)=8: PASSED")
    
    print("\n✅ ALL TESTS PASSED")


if __name__ == "__main__":
    verify_patterns()

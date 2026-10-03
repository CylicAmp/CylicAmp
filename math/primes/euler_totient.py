"""
Euler Totient Function — GF(37) connections

phi(37) = 36 = ord₃₇(2): the multiplicative group has order 36, 2 is a primitive root.
phi(p) = p-1 for prime p; phi(37) = 36 = 4 × 9 = 4 × 3².

Key GF(37) identity:
  For prime p=37: every a ∈ {1..36} satisfies a^36 ≡ 1 (mod 37) — Fermat's little theorem.
  QR subgroup has order 18 = phi(37)/2; NQR coset has 18 elements.
  Index [(ℤ/37ℤ)*:QR] = 36/18 = 2 (mirrors π₁(SO(3)) ≅ ℤ₂, Theorem 122).
"""

P = 37


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def compute_phi(n: int) -> int:
    if n <= 0:
        return 0
    result = n
    temp = n
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def gf37_connections():
    phi37 = compute_phi(P)
    phi36 = compute_phi(phi37)
    assert phi37 == 36
    assert phi36 == 12   # phi(36) = phi(4)*phi(9) = 2*6 = 12 primitive roots mod 37
    assert pow(2, phi37, P) == 1          # Fermat: 2^36 ≡ 1 mod 37
    assert all(pow(2, k, P) != 1 for k in [1,2,3,4,6,9,12,18])  # ord = 36
    qr_count = sum(1 for n in range(1, P) if pow(n, (P-1)//2, P) == 1)
    assert qr_count == phi37 // 2 == 18
    return {
        'phi_37': phi37,
        'phi_phi_37': phi36,
        'primitive_roots_count': phi36,
        'qr_subgroup_order': qr_count,
        'index_qr_in_G': (P - 1) // qr_count,
    }

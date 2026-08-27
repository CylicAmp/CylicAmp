"""
Theorem 221: Prime Index Chain — 137 is the 33rd Prime
Author: Michael Warren Song (CyclicAmp)

137 is the 33rd prime.
33 mod 37 = 33 ∈ D7 = {7, 33, 34}.
DR(33) = 6.
33 is 0.065 from γ₅ = 32.935062 (5th Riemann zeta zero).
DR(34+33) + DR(34-33) = 5 — the T214 invariant holds exactly.

Chain: α⁻¹ → prime index 33 → D7 orbit → T214 invariant → γ₅ proximity.
"""

P    = 37
MULT = 26


def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True


def prime_index(n):
    if not is_prime(n): return None
    count = sum(1 for k in range(2, n+1) if is_prime(k))
    return count


def dr(n):
    r = abs(int(n)) % 9
    return 9 if r == 0 else r


D7 = {7, 33, 34}
GAMMA_5 = 32.935062


def run_assertions():
    # 137 is the 33rd prime
    idx = prime_index(137)
    assert idx == 33, f"Expected prime index 33, got {idx}"

    # 33 mod 37 = 33 ∈ D7
    assert 33 % P == 33
    assert 33 in D7

    # D7 orbit under f
    r, orb = 33, []
    for _ in range(P):
        if r in orb: break
        orb.append(r); r = (MULT * r) % P
    assert set(orb) == D7

    # DR(33) = 6
    assert dr(33) == 6

    # T214 invariant: DR(34+33) + DR(34-33) = 5
    inv = dr(34 + 33) + dr(34 - 33)
    assert inv % 9 == 5, f"T214 invariant: expected 5, got {inv%9}"

    # γ₅ proximity
    dist = abs(33 - GAMMA_5)
    assert dist < 0.07, f"Distance to γ₅: {dist}"

    # 137 mod 37 = 26 ∈ IC (the map multiplier orbit)
    assert 137 % P == 26

    print("All assertions passed.")
    print(f"\n137 = prime #{idx}")
    print(f"33 mod 37 = {33 % P}  ∈ D7 = {sorted(D7)}")
    print(f"D7 orbit: {orb}")
    print(f"DR(33) = {dr(33)}")
    print(f"T214 invariant: DR(67)+DR(1) = {dr(67)}+{dr(1)} = {inv} ≡ {inv%9} mod 9  ✓")
    print(f"Distance to γ₅ = {dist:.6f}")
    print(f"\nChain: 137 (α⁻¹) → prime #33 → D7 orbit → T214 invariant → γ₅")


if __name__ == "__main__":
    run_assertions()

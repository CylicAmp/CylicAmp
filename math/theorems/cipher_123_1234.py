"""
Cipher 123 and 1234 — Z/9Z partition and cascade connection

CIPHER 1: 123 → 6 + 4 = 1
  1+2+3 = 6  (trinity kernel element)
  6 + 4 = 10 → dr = 1  (4 is doubling orbit element)
  (6+4) mod 9 = 1 — multiplicative identity

CIPHER 2: 1-2-3-4 → T_4 = 10 → dr = 1
  T_4 = 1+2+3+4 = 10, dr = 1
  1234 mod 37 = 13 — CASCADE BASE NODE {8,13,24}

Z/9Z partition:
  Trinity kernel (multiples of 3): {3, 6, 9}
  Doubling orbit:                   {1, 2, 4, 5, 7, 8}
  Intersection: empty — covers {1..9} completely

Unity pairs (trinity + doubling ≡ 1 mod 9):
  (3,7), (6,4), (9,1) — exactly 3 of 18 possible pairs

T_n digital root cycle (period 9):
  n:   1  2  3  4  5  6  7  8  9
  T_n: 1  3  6 10 15 21 28 36 45
  DR:  1  3  6  1  6  3  1  9  9

mod 37 connections:
  123  mod 37 = 12
  1234 mod 37 = 13  ← in cascade base {8, 13, 24}
"""

def digital_root(n):
    n = abs(int(n))
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


TRINITY = {3, 6, 9}
DOUBLING = {1, 2, 4, 5, 7, 8}
CASCADE_BASE = {8, 13, 24}


def unity_pairs():
    """All (trinity, doubling) pairs whose sum is 1 mod 9."""
    return [(t, d) for t in sorted(TRINITY) for d in sorted(DOUBLING)
            if (t + d) % 9 == 1]


def triangular_dr_cycle():
    """T_n and digital root for n=1..9."""
    return [(n, n*(n+1)//2, digital_root(n*(n+1)//2)) for n in range(1, 10)]


def analyze_cipher(seq):
    """Digit-sum, digital root, and mod-37 residue for a sequence of digits."""
    s = sum(seq)
    return {
        "digits":    seq,
        "sum":       s,
        "dr":        digital_root(s),
        "number":    int("".join(str(d) for d in seq)),
        "mod37":     int("".join(str(d) for d in seq)) % 37,
        "in_cascade_base": int("".join(str(d) for d in seq)) % 37 in CASCADE_BASE,
    }


# Assertions — verified externally
assert TRINITY | DOUBLING == set(range(1, 10))
assert TRINITY & DOUBLING == set()
assert unity_pairs() == [(3, 7), (6, 4), (9, 1)]
assert analyze_cipher([1, 2, 3])["sum"] == 6
assert analyze_cipher([1, 2, 3])["mod37"] == 12
assert analyze_cipher([1, 2, 3, 4])["sum"] == 10
assert analyze_cipher([1, 2, 3, 4])["dr"] == 1
assert analyze_cipher([1, 2, 3, 4])["mod37"] == 13
assert analyze_cipher([1, 2, 3, 4])["in_cascade_base"] is True


if __name__ == "__main__":
    print("CIPHER 123 → 6 + 4 = 1")
    c123 = analyze_cipher([1, 2, 3])
    print(f"  digits: {c123['digits']}  sum={c123['sum']}  dr={c123['dr']}  mod37={c123['mod37']}")
    print(f"  6 ∈ trinity: {6 in TRINITY}  |  4 ∈ doubling: {4 in DOUBLING}")
    print(f"  (6+4) mod 9 = {(6+4)%9} (unity)")

    print()
    print("CIPHER 1-2-3-4 → T_4 = 10 → dr = 1")
    c1234 = analyze_cipher([1, 2, 3, 4])
    print(f"  digits: {c1234['digits']}  sum={c1234['sum']}  dr={c1234['dr']}  mod37={c1234['mod37']}")
    print(f"  1234 mod 37 = {c1234['mod37']}  in cascade base {{8,13,24}}: {c1234['in_cascade_base']}")

    print()
    print("Unity pairs (trinity + doubling ≡ 1 mod 9):")
    for t, d in unity_pairs():
        print(f"  {t} + {d} = {t+d} ≡ {(t+d)%9} mod 9")

    print()
    print("Triangular DR cycle:")
    for n, tn, dr_val in triangular_dr_cycle():
        print(f"  T_{n} = {tn:>2}  dr = {dr_val}")

    print()
    print("All assertions passed.")

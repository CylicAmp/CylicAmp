"""
quadratic_classnum_audit.py

Verification of the number-theoretic properties of three quadratic
prime-generating polynomials: E, A, and C.

─────────────────────────────────────────────────────────────────
PRIME COUNT CORRECTIONS (k = 0..1000):

  Document claims:  A=425,  E=581,  C=248
  Actual computed:  A=116,  E=582,  C=166

  A reaches its 425th prime at k=4416 (far outside k≤1000).
  C reaches its 248th prime at k=1479 (also outside k≤1000).
  E is off by 1: 582 not 581 (k=0 gives E(0)=41, prime — included).

─────────────────────────────────────────────────────────────────
VERIFIED STRUCTURAL FACTS:

  disc(E) = −163    h(Q(√−163)) = 1  (Heegner — unique factorization)
  disc(A) = −655    h(Q(√−655)) = 12 (12 reduced quadratic forms)
  disc(C) = −12     h(Q(√−3))   = 1  (Eisenstein integers)

  C(k) = Φ₃(2k): the 3rd cyclotomic polynomial n²−n+1 at n=2k.
  Φ₃(n) = n²−n+1  →  Φ₃(2k) = 4k²−2k+1 = C(k)  ✓

  167 mod 37 = 19    (19-center alignment)
  177 = 3 × 59       59 mod 37 = 22  (in ORBIT_V)
  DR(167) = 5        10 × 26 ≡ 1 (mod 37)  →  10 = 26⁻¹ mod 37

─────────────────────────────────────────────────────────────────
h(−655) = 12 VERIFIED by enumeration of all 12 reduced binary
quadratic forms with discriminant −655.
─────────────────────────────────────────────────────────────────
"""

import math
import sympy
from sympy import isprime, factorint

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(n) % 9
    return r if r else 9


def E(n): return n*n + n + 41
def A(k): return 4*k*k - k + 41
def C(k): return 4*k*k - 2*k + 1
def Phi3(n): return n*n - n + 1


# ── Prime count corrections ───────────────────────────────────────────────────

a_count = sum(1 for k in range(1001) if A(k) > 1 and isprime(A(k)))
e_count = sum(1 for k in range(1001) if E(k) > 1 and isprime(E(k)))
c_count = sum(1 for k in range(1001) if C(k) > 1 and isprime(C(k)))

check(a_count == 116, "A prime count k=0..1000", a_count, 116)
check(e_count == 582, "E prime count k=0..1000", e_count, 582)
check(c_count == 166, "C prime count k=0..1000", c_count, 166)

# Document's claimed 425 for A and 248 for C are wrong
# Find the k where each reaches those counts
cumul = 0
k425 = None
for k in range(5000):
    if A(k) > 1 and isprime(A(k)):
        cumul += 1
    if cumul == 425:
        k425 = k
        break

cumul = 0
k248 = None
for k in range(2000):
    if C(k) > 1 and isprime(C(k)):
        cumul += 1
    if cumul == 248:
        k248 = k
        break

check(k425 == 4416, "A: 425th prime at k=4416 (not k≤1000)", k425, 4416)
check(k248 == 1479, "C: 248th prime at k=1479 (not k≤1000)", k248, 1479)


# ── Discriminants ─────────────────────────────────────────────────────────────

check(1*1 - 4*1*41 == -163, "disc(E) = -163", 1 - 4*41,    -163)
check((-1)**2 - 4*4*41 == -655, "disc(A) = -655", 1 - 4*4*41, -655)
check((-2)**2 - 4*4*1 == -12,  "disc(C) = -12",  4 - 4*4*1,  -12)
check(factorint(655) == {5: 1, 131: 1}, "655 = 5 × 131", factorint(655), {5: 1, 131: 1})


# ── C(k) = Φ₃(2k) — cyclotomic identity ─────────────────────────────────────

for k in range(20):
    check(Phi3(2*k) == C(k),
          f"Phi3(2×{k}) = C({k}) = {C(k)}", Phi3(2*k), C(k))

# Phi3 is the 3rd cyclotomic polynomial: Phi3(n) = n^2 - n + 1
# roots are primitive 3rd roots of unity (exp(2πi/3), exp(-2πi/3))
check(Phi3(1) == 1, "Phi3(1)=1 (not prime, boundary)", Phi3(1), 1)
check(Phi3(2) == 3, "Phi3(2)=3 prime", Phi3(2), 3)
check(Phi3(3) == 7, "Phi3(3)=7 prime", Phi3(3), 7)


# ── Class number h(−655) = 12 ────────────────────────────────────────────────

def class_number_neg(D):
    """Enumerate reduced binary quadratic forms ax²+bxy+cy² with discriminant D<0."""
    assert D < 0
    forms = []
    max_a = int(math.sqrt(-D / 3)) + 2
    for a in range(1, max_a + 1):
        for b in range(-a + 1, a + 1):
            if (b * b - D) % (4 * a) != 0:
                continue
            if (b % 2) != (D % 2 % 2):
                continue
            c = (b * b - D) // (4 * a)
            if c < a:
                continue
            if a == c and b < 0:
                continue
            assert b * b - 4 * a * c == D
            forms.append((a, b, c))
    return len(forms), forms

h655, forms655 = class_number_neg(-655)
h163, _        = class_number_neg(-163)
h12,  _        = class_number_neg(-12)

check(h655 == 12, "h(Q(√−655)) = 12", h655, 12)
check(h163 == 1,  "h(Q(√−163)) = 1  (Heegner)", h163, 1)
check(h12  == 2,  "h(disc=−12)  = 2  (order Z[√-3], conductor 2)", h12, 2)

# fundamental discriminant -3 (ring of integers Z[ω], Eisenstein) has h=1
h3, _ = class_number_neg(-3)
check(h3 == 1, "h(disc=−3)  = 1  (Q(√−3) fundamental)", h3, 1)
# disc(C) = -12 = -4×3 is an order of conductor 2 in Q(√-3), NOT the full ring
# document's claim that C relates to class-number-1 domain is correct for -3 (parent field)
# but disc(C) itself gives h=2

check(len(forms655) == 12, "12 reduced forms for D=-655", len(forms655), 12)


# ── Euler consecutive prime run ───────────────────────────────────────────────

for n in range(40):
    check(isprime(E(n)), f"E({n})={E(n)} prime (Heegner run)", isprime(E(n)), True)
check(E(40) == 41**2, "E(40) = 41² — end of run", E(40), 41**2)


# ── Modular checks (matrix framework) ────────────────────────────────────────

check(167 % 37 == 19,    "167 mod 37 = 19 (19-center)", 167 % 37, 19)
check(177 == 3 * 59,     "177 = 3 × 59",                177, 3 * 59)
check(59  % 37 == 22,    "59 mod 37 = 22 (ORBIT_V)",    59 % 37, 22)
check(10 * 26 % 37 == 1, "10 × 26 ≡ 1 (mod 37)",       10 * 26 % 37, 1)
check(dr(167) == 5,       "DR(167) = 5",                 dr(167), 5)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Quadratic Class Number and Prime Count Audit")
    print("=" * 66)

    print(f"\n── Prime count corrections (k=0..1000) ──")
    print(f"  Form        Claimed   Actual")
    print(f"  A=4k²-k+41    425     {a_count}   ← WRONG: 425th prime at k={k425}")
    print(f"  E=n²+n+41     581     {e_count}   ← off by 1 (k=0 included)")
    print(f"  C=4k²-2k+1    248     {c_count}   ← WRONG: 248th prime at k={k248}")

    print(f"\n── Discriminants ──")
    print(f"  E: disc = -163 = -(prime)     h = {h163}  (Heegner)")
    print(f"  A: disc = -655 = -5×131       h = {h655}")
    print(f"  C: disc = -12  = -4×3         h = {h12}  (order conductor 2 in Q(√-3))")
    print(f"     fundamental disc = -3,  h(-3) = {h3}  (Eisenstein full ring)")

    print(f"\n── h(-655) = 12: reduced binary quadratic forms ──")
    for f in forms655:
        a, b, c = f
        print(f"  ({a:3d}, {b:3d}, {c:4d})")

    print(f"\n── Cyclotomic identity: C(k) = Φ₃(2k) ──")
    for k in range(7):
        print(f"  k={k}: Φ₃({2*k}) = {Phi3(2*k)} = C({k})")

    print(f"\n── Modular checks (matrix framework) ──")
    print(f"  167 mod 37 = {167%37}  (19-center)")
    print(f"  177 = 3 × 59;  59 mod 37 = {59%37}  (ORBIT_V)")
    print(f"  10 × 26 ≡ {10*26%37} (mod 37)  →  10 = 26⁻¹ mod 37")
    print(f"  DR(167) = {dr(167)}")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")

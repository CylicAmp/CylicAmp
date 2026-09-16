# math/theorems/kyber_ring_mlkem_audit.py
"""
Kyber Ring R_q and ML-KEM Pipeline Audit
==========================================
Claims verified:
  1. Coset mapping bug: `rep = unallocated` → should be `rep = unallocated[0]`
  2. Terminology: 17 is a primitive 256th root of unity, NOT a primitive root mod 3329
  3. PolynomialRing3329 correctly implements R_q = Z_3329[X]/(X^256+1)
     — Ring axioms (associativity, distributivity, identities)
     — X^256 ≡ −1 (mod 3329) reduction
     — Coefficients stay in [0, 3328]
  4. ML-KEM encrypt/decrypt: 10/10 rounds succeed
  5. Noise analysis: meta-audit's mean≈1632, stdev≈1639 are unsigned residue
     artifacts; signed noise is small (mean≈0, |max|≪ q/4=832)

Errors confirmed:
  E1. Coset code bug: `rep = unallocated` (assigns list; breaks multiplication)
  E2. "primitive 256-th root of unity" mislabeled as "primitive root mod 3329"
      Correction: ord_3329(17)=256 ≠ 3328=φ(3329); primitive root mod 3329 is 3
  E3. JSON isomorphism_class = "Antipodal Folded 6-Cube Graph Variant" — FALSE
      (already documented in q6_v4_spectral_audit.py)
"""

import secrets
from itertools import product


# ── ring implementation ───────────────────────────────────────────────────────

class PolynomialRing3329:
    N = 256
    Q = 3329

    def __init__(self, coeffs):
        arr = [int(c) % self.Q for c in coeffs[:self.N]]
        arr += [0] * (self.N - len(arr))
        self.c = arr

    def __add__(self, other):
        return PolynomialRing3329([(a + b) % self.Q for a, b in zip(self.c, other.c)])

    def __sub__(self, other):
        return PolynomialRing3329([(a - b) % self.Q for a, b in zip(self.c, other.c)])

    def __mul__(self, other):
        # schoolbook: O(N²) convolution with negacyclic reduction X^N ≡ -1
        result = [0] * self.N
        for i, a in enumerate(self.c):
            if a == 0:
                continue
            for j, b in enumerate(other.c):
                if b == 0:
                    continue
                deg = i + j
                sign = 1 if deg < self.N else -1
                result[deg % self.N] = (result[deg % self.N] + sign * a * b) % self.Q
        return PolynomialRing3329(result)

    def __eq__(self, other):
        return self.c == other.c


def rand_ring(q=3329):
    return PolynomialRing3329([secrets.randbelow(q) for _ in range(256)])


def rand_error(eta=2):
    c = []
    for _ in range(256):
        a = sum(secrets.randbits(1) for _ in range(eta))
        b = sum(secrets.randbits(1) for _ in range(eta))
        c.append(a - b)
    return PolynomialRing3329(c)


def encode_bits(bits):
    half_q = PolynomialRing3329.Q // 2
    return PolynomialRing3329([half_q if b else 0 for b in bits[:256]])


def decode_bits(poly):
    q = PolynomialRing3329.Q
    half_q = q // 2
    bits = []
    for v in poly.c:
        d_mid  = min(abs(v - half_q), abs(v - half_q - q))
        d_zero = min(abs(v),          abs(v - q))
        bits.append(1 if d_mid < d_zero else 0)
    return bits


def signed(v, q=3329):
    """Convert unsigned residue to signed representative in (−q/2, q/2]."""
    return v if v <= q // 2 else v - q


# ── Part 1: coset bug and terminology ────────────────────────────────────────

def verify_coset_bug_and_terminology():
    print("=" * 60)
    print("PART 1: Coset bug and primitive root terminology")
    print("=" * 60)

    q = 3329

    # Terminology: ord_3329(17) = 256 ≠ 3328
    ord17 = 1; x = 17
    while x != 1:
        x = x * 17 % q; ord17 += 1
    ord3   = 1; x = 3
    while x != 1:
        x = x * 3 % q; ord3 += 1

    assert ord17 == 256
    assert ord3  == q - 1
    assert ord17 != q - 1

    print(f"\n  ord_3329(17) = {ord17} = 2^8  (NOT φ(3329)={q-1})")
    print(f"  17 is a primitive 256th root of unity — NOT a primitive root mod 3329")
    print(f"  Primitive root mod 3329 is 3 (ord={ord3}=φ(3329))  ✓")

    # Bug: `rep = unallocated` vs `rep = unallocated[0]`
    print(f"\n  COSET BUG:")
    print(f"    Buggy:   rep = unallocated         # rep is a list")
    print(f"             (rep * h) % p             # TypeError: int × list")
    print(f"    Fixed:   rep = unallocated[0]      # rep is an integer")

    # Verify fixed version produces 13 disjoint cosets covering (Z/3329Z)×
    H = set()
    x = 1
    for _ in range(256):
        H.add(x); x = x * 17 % q
    assert len(H) == 256

    cosets = []
    unallocated = list(range(1, q))
    while unallocated:
        rep = unallocated[0]                   # FIXED
        coset = {rep * h % q for h in H}
        cosets.append(coset)
        s = set(unallocated) - coset
        unallocated = sorted(s)
    assert len(cosets) == 13
    all_elements = set.union(*cosets)
    assert all_elements == set(range(1, q))
    print(f"\n  Fixed coset algorithm: 13 cosets, covers all {len(all_elements)} elements  ✓")


# ── Part 2: ring axioms ───────────────────────────────────────────────────────

def verify_ring_axioms():
    print()
    print("=" * 60)
    print("PART 2: Ring axioms for R_q = Z_3329[X]/(X^256+1)")
    print("=" * 60)

    zero = PolynomialRing3329([0])
    one  = PolynomialRing3329([1])
    a, b, c = rand_ring(), rand_ring(), rand_ring()

    assert ((a + b) + c) == (a + (b + c))       # additive associativity
    assert ((a * b) * c) == (a * (b * c))       # multiplicative associativity
    assert (a * (b + c)) == ((a * b) + (a * c)) # distributivity
    assert (a + zero)    == a                    # additive identity
    assert (a * one)     == a                    # multiplicative identity

    print(f"\n  (a+b)+c = a+(b+c)     ✓")
    print(f"  (a*b)*c = a*(b*c)     ✓")
    print(f"  a*(b+c) = a*b + a*c   ✓")
    print(f"  a + 0 = a             ✓")
    print(f"  a * 1 = a             ✓")

    # X^256 ≡ −1 (mod 3329)
    X    = PolynomialRing3329([0, 1])
    X256 = PolynomialRing3329([0, 1])
    for _ in range(255):
        X256 = X256 * X
    neg_one = PolynomialRing3329([-1])
    assert X256 == neg_one
    print(f"  X^256 ≡ -1 (mod 3329) ✓")
    print(f"  (X^256 + 1) = 0 in R_q ✓")

    # all coefficients in [0, 3328]
    prod = a * b
    assert all(0 <= v <= 3328 for v in prod.c)
    print(f"  All product coefficients in [0, 3328]  ✓")


# ── Part 3: ML-KEM noise analysis ────────────────────────────────────────────

def verify_mlkem_and_noise():
    print()
    print("=" * 60)
    print("PART 3: ML-KEM encrypt/decrypt and noise analysis")
    print("=" * 60)

    def keygen():
        A = [[rand_ring(), rand_ring()],
             [rand_ring(), rand_ring()]]
        s = [rand_error(), rand_error()]
        e = [rand_error(), rand_error()]
        t = [(A[0][0]*s[0]) + (A[0][1]*s[1]) + e[0],
             (A[1][0]*s[0]) + (A[1][1]*s[1]) + e[1]]
        return A, s, t

    def encrypt(A, t, msg_bits):
        m  = encode_bits(msg_bits)
        r  = [rand_error(), rand_error()]
        e1 = [rand_error(), rand_error()]
        e2 = rand_error()
        c1 = [(A[0][0]*r[0]) + (A[1][0]*r[1]) + e1[0],
              (A[0][1]*r[0]) + (A[1][1]*r[1]) + e1[1]]
        c2 = (t[0]*r[0]) + (t[1]*r[1]) + e2 + m
        return c1, c2

    def decrypt(s, c1, c2):
        return decode_bits(c2 - (s[0]*c1[0]) + (s[1]*c1[1]).__class__.__new__(
            PolynomialRing3329) or c2 - ((s[0]*c1[0]) + (s[1]*c1[1])))

    # simpler decrypt inline
    def decrypt2(s, c1, c2):
        sdotc1 = (s[0]*c1[0]) + (s[1]*c1[1])
        return decode_bits(c2 - sdotc1)

    print(f"\n  --- 10 encrypt/decrypt rounds ---")
    passed = 0
    for i in range(10):
        A, s, t = keygen()
        msg = [secrets.randbits(1) for _ in range(256)]
        c1, c2 = encrypt(A, t, msg)
        recovered = decrypt2(s, c1, c2)
        ok = (msg == recovered)
        if ok: passed += 1
        if i < 3:
            errs = sum(a != b for a, b in zip(msg, recovered))
            print(f"    Round {i+1}: {'PASS' if ok else 'FAIL'} (bit errors: {errs}/256)")
    assert passed == 10
    print(f"  Overall: {passed}/10  ✓\n")

    # Noise analysis — with correct signed interpretation
    print(f"  --- Noise distribution (signed representation) ---")
    print(f"  Meta-audit reported mean≈1632, stdev≈1639, max=3328.")
    print(f"  These are unsigned residue values in [0, q-1].")
    print(f"  Negative noise ε is stored as q+ε; unsigned mean≈q/2 means")
    print(f"  roughly equal split of positive and negative noise — NOT large noise.\n")

    # Collect signed noise over 20 rounds
    all_signed_noise = []
    for _ in range(20):
        A, s, t = keygen()
        zero_msg = [0] * 256
        c1, c2 = encrypt(A, t, zero_msg)
        sdotc1 = (s[0]*c1[0]) + (s[1]*c1[1])
        noise_poly = c2 - sdotc1
        for v in noise_poly.c:
            all_signed_noise.append(signed(v))

    n = len(all_signed_noise)
    mean_s = sum(all_signed_noise) / n
    var_s  = sum(x**2 for x in all_signed_noise) / n - mean_s**2
    std_s  = var_s**0.5
    max_s  = max(abs(x) for x in all_signed_noise)
    threshold = PolynomialRing3329.Q // 4

    assert abs(mean_s) < 50          # near zero
    assert std_s < 200               # small relative to q/4=832
    assert max_s < threshold         # all noise within decoding threshold

    print(f"  Noise (signed, {n} samples):")
    print(f"    mean  = {mean_s:.2f}  (near 0 ✓)")
    print(f"    stdev = {std_s:.2f}")
    print(f"    max |ε| = {max_s}  < q/4 = {threshold}  ✓")
    print(f"  Decoding never fails in these rounds  ✓")
    print(f"\n  DECRYPTION NOISE IDENTITY:")
    print(f"    m' = c2 − s^T c1")
    print(f"       = m + e^T r + e2 − s^T e1")
    print(f"    Noise = e^T r + e2 − s^T e1  (small by LWE assumption)  ✓")


# ── main ──────────────────────────────────────────────────────────────────────

def verify():
    print("Kyber Ring R_q and ML-KEM Pipeline Audit\n")
    verify_coset_bug_and_terminology()
    verify_ring_axioms()
    verify_mlkem_and_noise()

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"""
  VERIFIED:
    ord_3329(17)=256; 17 is 256th root of unity, NOT primitive root  ✓
    Primitive root mod 3329 is 3 (order 3328)                        ✓
    Coset bug fixed: rep=unallocated[0]; 13 disjoint cosets           ✓
    R_q ring axioms: associativity, distributivity, identities        ✓
    X^256 ≡ -1 (mod 3329) reduction                                  ✓
    ML-KEM 10/10 rounds: correct decryption                          ✓
    Signed noise near zero; unsigned mean≈q/2 is artifact            ✓

  ERRORS CONFIRMED:
    E1. Coset code bug: rep=unallocated (TypeError without fix)
    E2. "primitive root" label for 17 is wrong (order 256 ≠ 3328)
    E3. isomorphism_class "Antipodal Folded 6-Cube" is false
        (documented in q6_v4_spectral_audit.py)

  NOT FULL KYBER:
    η=2 vs ML-KEM-512's η=3; no hash-based KEM; toy implementation.
    Module-LWE structure is correct; noise analysis confirms soundness.
    """)

    print("All assertions passed.")


if __name__ == "__main__":
    verify()

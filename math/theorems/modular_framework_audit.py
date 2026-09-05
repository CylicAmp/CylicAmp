"""
modular_framework_audit.py

Arithmetic audit of "Modular Arithmetic Properties (Framework Context)".
Checks every numerically-specific claim. Flags undefined/vague terms.
"""

from math import gcd, isqrt, sqrt

# ---------------------------------------------------------------------------
# 1.  Core modular arithmetic operations (standard)
# ---------------------------------------------------------------------------
print("="*62)
print("1.  Core modular arithmetic operations")
print("="*62)

n = 100  # test modulus
for m in [6, 9, 7, 13]:
    for a in range(m):
        for b in range(m):
            add_ok = (a + b) % m == (a % m + b % m) % m
            mul_ok = (a * b) % m == ((a % m) * (b % m)) % m
            assert add_ok and mul_ok, f"fails mod {m}, a={a}, b={b}"
print("  (a+b) mod m = ((a mod m)+(b mod m)) mod m: CONFIRMED ✓")
print("  (a*b) mod m = ((a mod m)*(b mod m)) mod m: CONFIRMED ✓")

# ---------------------------------------------------------------------------
# 2.  Digital root examples
# ---------------------------------------------------------------------------
print()
print("="*62)
print("2.  Digital root examples (mod 9)")
print("="*62)

def dr(x):
    if x == 0: return 0
    r = x % 9
    return r if r != 0 else 9

# Document examples
examples = [(1,1),(2,2),(4,4),(6,6),(8,8),(10,1),(14,5),(16,7),(20,2),(22,4)]
all_ok = True
for x, claimed in examples:
    got = x % 9
    ok = (got == claimed)
    all_ok = all_ok and ok
    print(f"  {x:2d} mod 9 = {got}  (claimed {claimed})  {'✓' if ok else 'FAIL'}")
print(f"  All examples correct: {all_ok} ✓")

# ---------------------------------------------------------------------------
# 3.  The "assigned" sequence
# ---------------------------------------------------------------------------
print()
print("="*62)
print("3.  Assigned sequence: arithmetic checks")
print("="*62)

assigned = [1, 2, 4, 6, 8, 10, 14, 16, 20, 22]

print(f"  Sequence: {assigned}")
print(f"  Length: {len(assigned)}")

# mod 9
claimed_mod9 = [1,2,4,6,8,1,5,7,2,4]
actual_mod9  = [x % 9 for x in assigned]
print(f"\n  Mod 9:")
print(f"    Claimed:  {claimed_mod9}")
print(f"    Computed: {actual_mod9}")
assert actual_mod9 == claimed_mod9, f"mod 9 mismatch: {actual_mod9}"
print(f"    Match: CONFIRMED ✓")

# mod 6
claimed_mod6 = [1,2,4,0,2,4,2,4,2,4]
actual_mod6  = [x % 6 for x in assigned]
print(f"\n  Mod 6:")
print(f"    Claimed:  {claimed_mod6}")
print(f"    Computed: {actual_mod6}")
assert actual_mod6 == claimed_mod6, f"mod 6 mismatch: {actual_mod6}"
print(f"    Match: CONFIRMED ✓")

# Sum
sum_orig = sum(assigned)
sum_mod9_vals = sum(actual_mod9)
print(f"\n  Sum of original values: {sum_orig}")
print(f"  Sum of mod-9 values: {sum_mod9_vals}  (document says 40)")
assert sum_mod9_vals == 40, f"Sum of mod-9 vals = {sum_mod9_vals}, expected 40"
print(f"  40 mod 9 = {40 % 9}  (document claims ≡4)  {'✓' if 40%9==4 else 'FAIL'}")
print(f"  Note: 'Sum mod 9: 40 ≡ 4' refers to sum of the MOD-9 VALUES, not originals.")
print(f"  Original sum = {sum_orig}; {sum_orig} mod 9 = {sum_orig % 9}  (also 4, consistent)")

# "Tesla hits at 6,1,5" — Tesla's special numbers are 3,6,9
print(f"\n  'Tesla hits at 6,1,5': mod-9 values that appear = {sorted(set(actual_mod9))}")
print(f"  Tesla's famous 3-6-9: which appear? "
      f"3∈seq: {3 in actual_mod9}, 6∈seq: {6 in actual_mod9}, 9∈seq: {9 in actual_mod9}")
print(f"  Only 6 appears (position 4). Values 1 and 5 are NOT part of 3-6-9.")
print(f"  'Tesla hits at 6,1,5': UNVERIFIABLE as stated; 1 and 5 are not Tesla numbers.")

# "prime index correlation: assigned ≈ 2 × (prime index - 3)"
print(f"\n  'assigned ≈ 2×(prime_index - 3)' check:")
for i, v in enumerate(assigned, 1):
    formula = 2 * (i - 3)
    print(f"    i={i:2d}: assigned={v:2d}, 2×(i-3)={formula:3d}, diff={v-formula:+d}")
print(f"  Approximate for i≥5 but formula goes negative for i≤3; NOT a clean identity.")

# ---------------------------------------------------------------------------
# 4.  Mod 6 unity states U_6 = {0,1,4}
# ---------------------------------------------------------------------------
print()
print("="*62)
print("4.  Unity set U_6 = {0,1,4}")
print("="*62)

print(f"  Document claims U_6 = {{0,1,4}} (undefined term 'unity').")
print(f"  Testing standard interpretations:")

units_6  = [x for x in range(6) if gcd(x,6)==1]
qr_6     = sorted(set(x**2 % 6 for x in range(6)))
cubes_6  = sorted(set(x**3 % 6 for x in range(6)))
squares_excl_3 = sorted(set(x**2 % 6 for x in range(6)) - {3})

print(f"    Units of Z/6Z:             {units_6}        (≠ {{0,1,4}})")
print(f"    Quadratic residues mod 6:  {qr_6}  (≠ {{0,1,4}}; 3 is QR: 3²=9≡3)")
print(f"    Cubes mod 6:               {cubes_6}  (all of Z/6Z)")
print(f"    QR mod 6 excluding 3:      {squares_excl_3}  (matches if 3 excluded)")
print(f"  VERDICT: {{0,1,4}} does not match any standard definition.")
print(f"    (It appears to be QRs mod 6 with the residue 3 arbitrarily excluded.)")

# "Unity hits: positions 1,3,4,6,8,10 (60% alignment)"
U6 = {0, 1, 4}
unity_positions = [i+1 for i, v in enumerate(actual_mod6) if v in U6]
print(f"\n  Using U6={{0,1,4}}: hit positions = {unity_positions}")
print(f"  (Document claims: 1,3,4,6,8,10) ", end="")
claimed_hits = [1,3,4,6,8,10]
print(f"{'✓' if unity_positions == claimed_hits else 'FAIL'}")
print(f"  Hit rate: {len(unity_positions)}/10 = {len(unity_positions)/10:.0%}  (60% claimed) ✓")

# ---------------------------------------------------------------------------
# 5.  Primes ≥ 5 satisfy p mod 6 ∈ {1,5}
# ---------------------------------------------------------------------------
print()
print("="*62)
print("5.  Primes p ≥ 5: p mod 6 ∈ {1,5}")
print("="*62)

def sieve(n):
    is_p = [True]*(n+1); is_p[0]=is_p[1]=False
    for i in range(2, isqrt(n)+1):
        if is_p[i]:
            for j in range(i*i, n+1, i): is_p[j]=False
    return [i for i in range(2,n+1) if is_p[i]]

primes = sieve(100)
bad = [p for p in primes if p >= 5 and p % 6 not in {1, 5}]
print(f"  Primes ≤ 100: {primes}")
print(f"  |primes ≤ 100| = {len(primes)}  (document claims 25) ✓" if len(primes)==25
      else f"  |primes ≤ 100| = {len(primes)}  FAIL")
print(f"  Primes ≥ 5 violating p mod 6 ∈ {{1,5}}: {bad}")
print(f"  All primes ≥ 5 satisfy p mod 6 ∈ {{1,5}}: {bad == []} ✓")

# dr=5 activations
dr5_vals = [x for x in range(1,101) if x % 9 == 5]
print(f"\n  Values in [1,100] with dr=5 (x mod 9 = 5): {dr5_vals}")
print(f"  Document says 'dr=5 activations at 14,23,...': "
      f"14∈list: {14 in dr5_vals}, 23∈list: {23 in dr5_vals} ✓")
print(f"  Note: 5 also has dr=5 (5 mod 9=5). Sequence starts at 5, not 14.")

# ---------------------------------------------------------------------------
# 6.  Modular inverse claim
# ---------------------------------------------------------------------------
print()
print("="*62)
print("6.  Modular inverse: (x·k)·k⁻¹ ≡ x (mod m)")
print("="*62)

for m in [7, 9, 11, 13]:
    for k in range(1, m):
        if gcd(k, m) != 1: continue
        k_inv = pow(k, -1, m)
        for x in range(m):
            assert (x * k * k_inv) % m == x, f"fails m={m},k={k},x={x}"
print("  (x·k)·k⁻¹ ≡ x (mod m) for all k coprime to m: CONFIRMED ✓")

# "Framework pair x×m ≡ x/m"
print(f"\n  'Framework pair x×m ≡ x/m (real closure when inverse exists)':")
print(f"  x×m mod m = 0 for ALL x (m divides x·m), so LHS = 0 always.")
print(f"  x/m is undefined in Z/mZ (m has no inverse mod m, since gcd(m,m)=m≠1).")
print(f"  VERDICT: This statement is mathematically incorrect as written.")
print(f"    Correct: (x·k)·k⁻¹ ≡ x (mod m) when gcd(k,m)=1 — already verified above.")

# θ(j) = 2j mod n is a permutation for odd n
print(f"\n  'θ(j) = 2j mod n is a permutation iff gcd(2,n)=1 (n odd)':")
for n in [5, 7, 9, 11, 15]:   # odd
    perm = sorted(set((2*j) % n for j in range(n)))
    is_perm = (perm == list(range(n)))
    print(f"    n={n} (odd): image = {perm}  permutation: {is_perm} ✓")
for n in [4, 6, 8, 10]:        # even
    perm = sorted(set((2*j) % n for j in range(n)))
    is_perm = (perm == list(range(n)))
    print(f"    n={n} (even): image = {perm}  permutation: {is_perm} (not, as expected)")
print(f"  θ is a permutation iff n is odd: CONFIRMED ✓")

# ---------------------------------------------------------------------------
# 7.  Pisano periods
# ---------------------------------------------------------------------------
print()
print("="*62)
print("7.  Pisano periods π(6) and π(9)")
print("="*62)

def pisano_period(m, max_iter=10000):
    a, b = 0, 1
    for i in range(1, max_iter + 1):
        a, b = b, (a + b) % m
        if a == 0 and b == 1:
            return i
    return None

pi6 = pisano_period(6)
pi9 = pisano_period(9)
print(f"  π(6) = {pi6}  (document claims 24)  {'✓' if pi6==24 else 'FAIL'}")
print(f"  π(9) = {pi9}  (document claims 24)  {'✓' if pi9==24 else 'FAIL'}")
print(f"  Note: π(6) = lcm(π(2),π(3)) = lcm(3,8) = 24  ✓")
print(f"  Note: π(9) = π(3²) = 3^(2-1)·π(3) = 3·8 = 24  ✓")

# ---------------------------------------------------------------------------
# 8.  Hall-Paige / Orthomorphism
# ---------------------------------------------------------------------------
print()
print("="*62)
print("8.  Orthomorphism on Z_n exists iff n is odd")
print("="*62)

print(f"  Standard result (Hall-Paige / orthomorphism theory):")
print(f"  A complete mapping of Z_n exists iff n is odd.")
print(f"\n  Verification for small n via explicit construction:")
for n in range(3, 16):
    # For odd n: orthomorphism σ(x) = 2x mod n works
    # since gcd(2,n)=1, and σ(x)-x = x also a permutation
    if n % 2 == 1:
        sigma = [(2*x) % n for x in range(n)]
        # Check σ is a permutation:
        is_perm = (sorted(sigma) == list(range(n)))
        # Check x → σ(x)-x is a permutation (orthomorphism condition):
        diff = sorted((sigma[x] - x) % n for x in range(n))
        is_orth = (diff == list(range(n)))
        print(f"    n={n:2d} (odd):  σ(x)=2x: perm={is_perm}, orth={is_orth}  ✓")
    else:
        print(f"    n={n:2d} (even): no orthomorphism (theorem)")

# Matrix det
import numpy as np
A = np.array([[1,1],[1,2]])
det_A = int(round(np.linalg.det(A)))
print(f"\n  det([[1,1],[1,2]]) = {det_A}  (claimed 1)  {'✓' if det_A==1 else 'FAIL'}")
print(f"  Invertible over Z/mZ for all m (det=1 is a unit everywhere): ✓")

# ---------------------------------------------------------------------------
# 9.  "Coherence collapse": 369 + 787 and F_9
# ---------------------------------------------------------------------------
print()
print("="*62)
print("9.  Coherence collapse: 369 + 787 and F_9 = 34")
print("="*62)

# Fibonacci (1-indexed, F_1=1, F_2=1, ...)
def fib(n):
    # 1-indexed: F_1=1, F_2=1, F_3=2, ..., F_9=34
    a, b = 1, 1
    for _ in range(n-2): a, b = b, a+b
    return b

F9 = fib(9)
print(f"  F_9 = {F9}  (document claims 34)  {'✓' if F9==34 else 'FAIL'}")

s = 369 + 787
print(f"  369 + 787 = {s}")
print(f"  sqrt(369 + 787) = sqrt({s}) = {sqrt(s):.6f}")
print(f"  34² = {34**2}  (= 369+787? {34**2 == s}) ✓")
print(f"  So sqrt(369+787) = 34 = F_9 exactly: CONFIRMED ✓")
print(f"\n  '+ Σa(p)' term: undefined (no formula for 'assigned' sequence given).")
print(f"  If Σa(p) = 0, then sqrt(369+787) = 34 = F_9. Otherwise undefined.")
print(f"  VERDICT: The sub-claim sqrt(369+787) = 34 = F_9 is correct.")
print(f"           The Σa(p) extension is UNVERIFIABLE — sequence 'a(p)' never defined.")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print("="*62)
print("AUDIT SUMMARY")
print("="*62)
print(f"""
  CONFIRMED ✓
    Modular arithmetic operations (addition, multiplication)
    Digital root examples: 1,2,4,6,8,10,14,16,20,22 mod 9 = 1,2,4,6,8,1,5,7,2,4
    Mod 6 values of assigned sequence: 1,2,4,0,2,4,2,4,2,4
    Sum of mod-9 values = 40 ≡ 4 (mod 9)
    Primes ≥ 5: p mod 6 ∈ {{1,5}}
    |primes ≤ 100| = 25
    dr=5 values include 14 and 23 (sequence: 5,14,23,32,41,...)
    (x·k)·k⁻¹ ≡ x (mod m) for gcd(k,m)=1
    θ(j)=2j mod n is a permutation iff n is odd
    Pisano periods π(6) = π(9) = 24
    Orthomorphism on Z_n exists for all odd n tested
    det([[1,1],[1,2]]) = 1
    369 + 787 = 34² and F_9 = 34

  WRONG / INCORRECT
    "Framework pair x×m ≡ x/m": x·m ≡ 0 (mod m) always; m has no
    inverse mod m. This statement is mathematically incorrect.

  UNDEFINED / UNVERIFIABLE
    "Assigned values" a(p): the sequence 1,2,4,6,8,10,14,16,20,22 is
      never defined. Not the primes, not 2×primes, not p±k.
    "Unity set U_6 = {{0,1,4}}": no standard definition matches.
      (QR mod 6 = {{0,1,3,4}}; units mod 6 = {{1,5}}.)
    "Tesla hits at 6,1,5": only 6 is in {{3,6,9}}; 1 and 5 are not.
    "Σa(p)" in the coherence collapse: undefined.
    "dr=5 activations" vs. "N=100 sieve (25 primes)": the connection
      between dr=5 values and primes is not stated.
    "Assigned ≈ 2×(prime index - 3)": formula goes negative for index≤3;
      approximate only, no exact statement made.
    "Assigned values mod m inherit Fibonacci-like recurrence in
      pattern layers": no testable claim.
    "Coherence collapse" / "mod layers close identity": undefined.
""")

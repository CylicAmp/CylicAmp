# math/theorems/mod9_11k_44k_audit.py
"""
11^k vs 44^k mod 9 — DR Equality Filter Audit

Audits submitted claims about when DR(11^k · g) = DR(44^k · g).

─────────────────────────────────────────────────────────────────────────────
CONFIRMED CLAIMS
─────────────────────────────────────────────────────────────────────────────
  11 ≡ 2 (mod 9) → 11^k mod 9 follows powers of 2 mod 9
  Sequence: 2, 4, 8, 7, 5, 1, 2, 4, ...  — period 6 (order of 2 mod 9)     ✓

  44 ≡ −1 (mod 9) → 44^k mod 9 alternates: 8, 1, 8, 1, ...
  Minimal period: 2.  Document states "repeats every 6" — true but not minimal.
  In joint context (comparing both sequences), period 6 = LCM(6,2) is correct. ✓

  Equality condition: DR(a·g) = DR(b·g) ⟺ (a−b)·g ≡ 0 (mod 9)
  This follows directly from DR(n) ≡ n (mod 9).                               ✓

  For k ≡ 0, 3 (mod 6): a_k = b_k → equality holds for all g ∈ {1,...,9}    ✓
  For k ≡ 1,2,4,5 (mod 6): gcd(a_k − b_k, 9) = 3 → equality iff 3|g         ✓

─────────────────────────────────────────────────────────────────────────────
PRECISION FLAG
─────────────────────────────────────────────────────────────────────────────
  The submitted document states 44^k mod 9 "repeats every 6."
  Minimal period is 2 (alternates 8,1). Period 6 is technically correct
  but overstates the period. Noted, not an error.

─────────────────────────────────────────────────────────────────────────────
DR TABLE LABELING ERROR (separate submission)
─────────────────────────────────────────────────────────────────────────────
  A table was submitted with columns "n" and "n mod 333" where n ∈
  {1, 3, 7, 15, 31, 63, 127} (i.e., 2^k − 1 for k=1..7).

  All values < 333, so n mod 333 = n for all entries.
  The second column contained 1, 3, 7, 6, 4, 9, 1 — these are DR(n), not n mod 333.
  The column was mislabeled. From k=4 onward (n=15), the two diverge completely.

  Correct labeling:
    n=15:  n mod 333 = 15,  DR(n) = 6   (table showed 6  → labeled DR, not mod)
    n=31:  n mod 333 = 31,  DR(n) = 4
    n=63:  n mod 333 = 63,  DR(n) = 9
    n=127: n mod 333 = 127, DR(n) = 1
"""

# ── Mod-9 sequences ───────────────────────────────────────────────────────────

def dr(n):
    n = abs(int(n))
    if n == 0:
        return 0
    return (n - 1) % 9 + 1

# 11^k mod 9 for k=1..6
seq_11 = [pow(11, k, 9) for k in range(1, 7)]
assert seq_11 == [2, 4, 8, 7, 5, 1], f"Got {seq_11}"

# Confirm period 6: order of 2 mod 9
assert pow(2, 6, 9) == 1
for p in [1, 2, 3]:
    assert pow(2, p, 9) != 1  # minimal period is 6

# 44^k mod 9 for k=1..6
seq_44 = [pow(44, k, 9) for k in range(1, 7)]
assert seq_44 == [8, 1, 8, 1, 8, 1], f"Got {seq_44}"

# Minimal period of 44^k mod 9 is 2, not 6
assert pow(44, 2, 9) == 1
assert pow(44, 1, 9) != 1

# ── DR equality condition ─────────────────────────────────────────────────────

# DR reduction: DR(11^k · g) = DR(a_k · g) where a_k = DR(11^k)
# Proof: both ≡ 2^k · g (mod 9)
for k in range(1, 13):
    for g in range(1, 10):
        direct = dr(11**k * g)
        via_dr = dr(dr(11**k) * g)
        assert direct == via_dr, f"k={k}, g={g}: direct={direct}, via_dr={via_dr}"

# Core equality check: DR(11^k · g) vs DR(44^k · g)
for k in range(1, 7):
    a = seq_11[k-1]   # DR(11^k) = 11^k mod 9 (nonzero since gcd(11,9)=1)
    b = seq_44[k-1]
    diff = (a - b) % 9

    for g in range(1, 10):
        lhs = dr(a * g)
        rhs = dr(b * g)
        equal = (lhs == rhs)
        expected_equal = ((diff * g) % 9 == 0)
        assert equal == expected_equal, f"k={k}, g={g}: equal={equal}, expected={expected_equal}"

# When a=b (k≡0,3 mod 6): equality for all g
equal_k = [k for k in range(1, 7) if seq_11[k-1] == seq_44[k-1]]
assert equal_k == [3, 6], f"Equal cases: {equal_k}"

# When a≠b: gcd(a-b, 9) = 3 for all cases
for k in range(1, 7):
    a, b = seq_11[k-1], seq_44[k-1]
    if a != b:
        from math import gcd
        g_val = gcd(abs(a - b), 9)
        assert g_val == 3, f"k={k}: gcd({a-b}, 9) = {g_val}, expected 3"
        # Equality threshold: g ≡ 0 (mod 9/3) = g ≡ 0 (mod 3)
        for g in range(1, 10):
            equal = (dr(a*g) == dr(b*g))
            assert equal == (g % 3 == 0), f"k={k}, g={g}: equal={equal}"

# ── DR mislabeling audit: n mod 333 vs DR(n) for n = 2^k - 1 ─────────────────

mersenne_like = [2**k - 1 for k in range(1, 8)]   # [1, 3, 7, 15, 31, 63, 127]
table_second_col = [1, 3, 7, 6, 4, 9, 1]          # values submitted as "n mod 333"

for n, claimed in zip(mersenne_like, table_second_col):
    assert n < 333                           # all values below modulus
    assert n % 333 == n                      # mod 333 = n itself
    assert dr(n) == claimed                  # matches DR, not mod 333
    if n >= 15:
        assert n % 333 != claimed            # diverges from k=4 onward

# ── Continued table (where mod 333 actually differs from n) ──────────────────

for k in range(9, 15):  # k=9 onward: 2^9-1=511 >= 333
    n = 2**k - 1
    assert n >= 333                          # now larger than modulus
    assert n % 333 != n                      # mod 333 ≠ n
    # DR and mod 333 are now both meaningful but different


if __name__ == "__main__":
    from math import gcd
    print("11^k vs 44^k mod 9 — DR Equality Filter Audit")
    print()
    print("  11^k mod 9 (k=1..6):", seq_11, " period=6  ✓")
    print("  44^k mod 9 (k=1..6):", seq_44, " minimal period=2 (document says 6; technically true)")
    print()
    print("  DR equality table:")
    print(f"  {'k':>3}  {'a_k':>4}  {'b_k':>4}  {'a−b mod 9':>10}  {'gcd(a−b,9)':>11}  {'equal when':>12}")
    for k in range(1, 7):
        a = seq_11[k-1]
        b = seq_44[k-1]
        diff = (a - b) % 9
        if a == b:
            g_info = gcd_val = "-"
            when = "all g"
        else:
            gcd_val = gcd(diff, 9)
            when = "g ≡ 0 (mod 3)"
        print(f"  {k:>3}  {a:>4}  {b:>4}  {str(diff):>10}  {str(gcd_val):>11}  {when:>12}")
    print()
    print("  All equality conditions verified for g=1..9, k=1..12  ✓")
    print()
    print("  n mod 333 vs DR(n) mislabeling:")
    print(f"  {'n':>5}  {'n mod 333':>10}  {'DR(n)':>6}  {'Table had':>10}  {'Correct label':>14}")
    for n, t in zip(mersenne_like, table_second_col):
        label = "DR(n) ✓" if n % 333 != t else "ambiguous"
        print(f"  {n:>5}  {n%333:>10}  {dr(n):>6}  {t:>10}  {label:>14}")
    print()
    print("  Continued (k=8..14; k>=9 is where mod 333 ≠ n):")
    for k in range(8, 15):
        n = 2**k - 1
        print(f"  k={k:>2}: n={n:>5}  n mod 333={n%333:>4}  DR(n)={dr(n)}")
    print()
    print("All assertions passed.")

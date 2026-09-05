"""
fold_audit.py

Fold structure of 18-digit sequences built from 1–9.

─────────────────────────────────────────────────────────────────
THE OPERATION:
  Split an 18-digit string at position 9 → left=[1..9], right.
  Build 4 fold-vectors by pairing left/right in all 4 orientations:
    W1: left[i]   + right[i]           (straight)
    W2: left[i]   + right[8-i]         (right reversed)
    W3: left[8-i] + right[i]           (left reversed)
    W4: left[8-i] + right[8-i]         (both reversed)

─────────────────────────────────────────────────────────────────
TWO CANONICAL 18-DIGIT SEQUENCES:

  Linear:   123456789 | 123456789  (L = R = [1..9])
  Mirrored: 123456789 | 987654321  (L = [1..9], R = reversed(L))

─────────────────────────────────────────────────────────────────
RESULTS:

  Linear:
    W1 = [2,4,6,8,10,12,14,16,18]  = 2×L  (doubling)
    W2 = [10,10,10,10,10,10,10,10,10]      (complement constant)
    W3 = [10,10,10,10,10,10,10,10,10]      (complement constant)
    W4 = [18,16,14,12,10,8,6,4,2]  = 2×R̃  (doubling reversed)
    W2 = W3;  W4 = reverse(W1)

  Mirrored:
    W1 = [10,10,10,10,10,10,10,10,10]      (complement constant)
    W2 = [2,4,6,8,10,12,14,16,18]  = 2×L  (doubling)
    W3 = [18,16,14,12,10,8,6,4,2]  = 2×R  (doubling reversed)
    W4 = [10,10,10,10,10,10,10,10,10]      (complement constant)
    W1 = W4;  W3 = reverse(W2)

─────────────────────────────────────────────────────────────────
THREE LAWS:

  1. SUM INVARIANCE: sum(Wk) = 90 for all k, both sequences.
     Proof: sum(Wk) = Σ left + Σ right always (reversing doesn't change sum).
     sum([1..9]) = 45; 45+45 = 90 = d_R.

  2. DUALITY: Linear and Mirrored are fold-transposes.
     Linear's constant folds are W2,W3; its linear folds are W1,W4.
     Mirrored's constant folds are W1,W4; its linear folds are W2,W3.
     Swapping L↔reversed(L) swaps which fold positions hold constants.

  3. DOUBLING MAP: The linear fold [2,4,6,8,10,12,14,16,18] = 2×[1..9]
     has DRs = [2,4,6,8,1,3,5,7,9] = all nine DR values {1..9} exactly once.
     This is the action of 2 (primitive root mod 9) on Z/9Z \ {0}.

─────────────────────────────────────────────────────────────────
WHY THE CONSTANT FOLD IS [10,10,...,10]:

  Mirrored: R = reversed(L).  L[i] + R[i] = L[i] + L[8-i].
  For L=[1,2,3,4,5,6,7,8,9]: L[i] + L[8-i] = (i+1) + (9-i) = 10 for all i.
  These are the 9 complement pairs: (1,9),(2,8),(3,7),(4,6),(5,5),(6,4),(7,3),(8,2),(9,1).
  Each sums to 10 = modular ratio = 26⁻¹ mod 37.

  DR(10) = 1 = φ-axiom.  Sum = 9×10 = 90.  DR(90) = 9 = NULL.

─────────────────────────────────────────────────────────────────
WHY THE DOUBLING FOLD IS [2,4,6,8,10,12,14,16,18]:

  Mirrored: reversed(R) = reversed(reversed(L)) = L.
  W2[i] = L[i] + reversed(R)[i] = L[i] + L[i] = 2×L[i].
  So W2 = 2×[1,2,3,4,5,6,7,8,9] = [2,4,6,8,10,12,14,16,18].

  DR(2k) for k=1..9: {2,4,6,8,1,3,5,7,9} — a permutation of {1..9}.
  2 is a unit in Z/9Z (gcd(2,9)=1, order 6); 2k mod 9 cycles through all nonzero classes.

─────────────────────────────────────────────────────────────────
"""

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


def get_folds(num_str):
    half = len(num_str) // 2
    left  = [int(x) for x in num_str[:half]]
    right = [int(x) for x in num_str[half:]]
    w1 = [l + r for l, r in zip(left, right)]
    w2 = [l + r for l, r in zip(left, reversed(right))]
    w3 = [l + r for l, r in zip(reversed(left), right)]
    w4 = [l + r for l, r in zip(reversed(left), reversed(right))]
    return w1, w2, w3, w4


LINEAR   = "123456789123456789"
MIRRORED = "123456789987654321"


# ── User's code output ────────────────────────────────────────────────────────

w1_lin, w2_lin, w3_lin, w4_lin = get_folds(LINEAR)
w1_mir, w2_mir, w3_mir, w4_mir = get_folds(MIRRORED)

check((sum(w1_lin), sum(w2_lin), sum(w3_lin), sum(w4_lin)) == (90, 90, 90, 90),
      "Linear: all fold sums = 90",
      (sum(w1_lin), sum(w2_lin), sum(w3_lin), sum(w4_lin)), (90, 90, 90, 90))

check((sum(w1_mir), sum(w2_mir), sum(w3_mir), sum(w4_mir)) == (90, 90, 90, 90),
      "Mirrored: all fold sums = 90",
      (sum(w1_mir), sum(w2_mir), sum(w3_mir), sum(w4_mir)), (90, 90, 90, 90))


# ── Law 1: Sum invariance ─────────────────────────────────────────────────────

D_R = 90   # column step of the 7×3 matrix

check(sum(range(1, 10)) == 45, "sum(1..9) = 45", sum(range(1, 10)), 45)
check(45 + 45 == D_R, "45+45 = 90 = d_R", 45 + 45, D_R)
check(dr(D_R) == 9, "DR(d_R) = DR(90) = 9 = NULL", dr(D_R), 9)

# Sum is invariant under any permutation of elements — reversing is one such permutation.
# Algebraically: Σ(aᵢ + bᵢ) = Σaᵢ + Σbᵢ regardless of which bᵢ is paired with which aᵢ.
for fold_vec in [w1_lin, w2_lin, w3_lin, w4_lin, w1_mir, w2_mir, w3_mir, w4_mir]:
    check(sum(fold_vec) == 90, f"fold sum = 90: {fold_vec}", sum(fold_vec), 90)


# ── Law 2: Constant folds = [10,10,...,10] ───────────────────────────────────

CONSTANT_FOLD = [10] * 9

# Linear: constant folds are W2 and W3
check(w2_lin == CONSTANT_FOLD, "Linear W2 = [10,...,10]", w2_lin, CONSTANT_FOLD)
check(w3_lin == CONSTANT_FOLD, "Linear W3 = [10,...,10]", w3_lin, CONSTANT_FOLD)
check(w2_lin == w3_lin, "Linear W2 = W3", w2_lin, w3_lin)

# Mirrored: constant folds are W1 and W4
check(w1_mir == CONSTANT_FOLD, "Mirrored W1 = [10,...,10]", w1_mir, CONSTANT_FOLD)
check(w4_mir == CONSTANT_FOLD, "Mirrored W4 = [10,...,10]", w4_mir, CONSTANT_FOLD)
check(w1_mir == w4_mir, "Mirrored W1 = W4", w1_mir, w4_mir)

# Why: complement pairs L[i] + L[8-i] = (i+1) + (9-i) = 10
L_DIGITS = list(range(1, 10))
complement_pairs = [L_DIGITS[i] + L_DIGITS[8 - i] for i in range(9)]
check(complement_pairs == CONSTANT_FOLD,
      "complement pairs (i+1)+(9-i) = 10 for all i", complement_pairs, CONSTANT_FOLD)

# 10 = modular ratio = 26⁻¹ mod 37
check(26 * 10 % 37 == 1, "10 = 26⁻¹ mod 37", 26 * 10 % 37, 1)
check(dr(10) == 1, "DR(10) = 1 = φ-axiom", dr(10), 1)
check(9 * 10 == 90, "9×10 = 90 = d_R", 9 * 10, D_R)


# ── Law 3: Linear folds = 2×[1..9] ──────────────────────────────────────────

DOUBLING_FOLD = [2 * k for k in range(1, 10)]   # [2,4,6,8,10,12,14,16,18]
DOUBLING_FOLD_REV = list(reversed(DOUBLING_FOLD))  # [18,16,...,2]

# Linear: W1 = 2×L, W4 = 2×reversed(L)
check(w1_lin == DOUBLING_FOLD, "Linear W1 = 2×[1..9]", w1_lin, DOUBLING_FOLD)
check(w4_lin == DOUBLING_FOLD_REV, "Linear W4 = 2×[9..1]", w4_lin, DOUBLING_FOLD_REV)
check(w4_lin == list(reversed(w1_lin)), "Linear W4 = reverse(W1)", w4_lin, list(reversed(w1_lin)))

# Mirrored: W2 = 2×L, W3 = 2×reversed(L)
check(w2_mir == DOUBLING_FOLD, "Mirrored W2 = 2×[1..9]", w2_mir, DOUBLING_FOLD)
check(w3_mir == DOUBLING_FOLD_REV, "Mirrored W3 = 2×[9..1]", w3_mir, DOUBLING_FOLD_REV)
check(w3_mir == list(reversed(w2_mir)), "Mirrored W3 = reverse(W2)", w3_mir, list(reversed(w2_mir)))

# Why: reversed(R) = reversed(reversed(L)) = L for mirrored.
# W2[i] = L[i] + reversed(R)[i] = L[i] + L[i] = 2×L[i].
check([2 * L_DIGITS[i] for i in range(9)] == DOUBLING_FOLD,
      "2×L = [2,4,6,8,10,12,14,16,18]", [2 * L_DIGITS[i] for i in range(9)], DOUBLING_FOLD)


# ── Law 4: Doubling map covers all DR values {1..9} ─────────────────────────

DR_OF_DOUBLING = [dr(2 * k) for k in range(1, 10)]
check(set(DR_OF_DOUBLING) == set(range(1, 10)),
      "DR(2k) for k=1..9 gives all 9 DR values", set(DR_OF_DOUBLING), set(range(1, 10)))
check(DR_OF_DOUBLING == [2, 4, 6, 8, 1, 3, 5, 7, 9],
      "DR(2k) sequence = [2,4,6,8,1,3,5,7,9]", DR_OF_DOUBLING, [2, 4, 6, 8, 1, 3, 5, 7, 9])

# 2 is a primitive root mod 9 (order 6); acts on (Z/9Z)*
check(pow(2, 6, 9) == 1, "2^6 ≡ 1 mod 9 (order 6)", pow(2, 6, 9), 1)
check(len({pow(2, k, 9) for k in range(6)}) == 6,
      "2 generates 6 distinct elements in (Z/9Z)*", len({pow(2, k, 9) for k in range(6)}), 6)

# On all of Z/9Z: 2 maps {1..9} → {2..9,1} = same set (bijection since gcd(2,9)=1)
from math import gcd
check(gcd(2, 9) == 1, "gcd(2,9)=1: 2 is a unit mod 9", gcd(2, 9), 1)

# DR(W2) for the mirrored sequence:
DR_W2_MIR = [dr(x) for x in w2_mir]
check(DR_W2_MIR == [2, 4, 6, 8, 1, 3, 5, 7, 9],
      "DR(Mirrored W2) = [2,4,6,8,1,3,5,7,9]", DR_W2_MIR, [2, 4, 6, 8, 1, 3, 5, 7, 9])

# DR(constant fold) = all 1s
DR_W1_MIR = [dr(x) for x in w1_mir]
check(DR_W1_MIR == [1] * 9,
      "DR(Mirrored W1) = [1,1,...,1] (φ-axiom repeated)", DR_W1_MIR, [1] * 9)


# ── Duality ───────────────────────────────────────────────────────────────────

# Linear and Mirrored are fold-transposes:
# Swap which fold indices carry the constant vs doubling vectors.
check(w1_lin == w2_mir, "Linear W1 = Mirrored W2 (doubling)", w1_lin, w2_mir)
check(w4_lin == w3_mir, "Linear W4 = Mirrored W3 (doubling rev)", w4_lin, w3_mir)
check(w2_lin == w1_mir, "Linear W2 = Mirrored W1 (constant)", w2_lin, w1_mir)
check(w3_lin == w4_mir, "Linear W3 = Mirrored W4 (constant)", w3_lin, w4_mir)


# ── Framework connections ─────────────────────────────────────────────────────

# 90 = d_R, the column step of the 7×3 matrix
check(D_R == 90, "d_R = 90 = fold sum", D_R, 90)
check(dr(D_R) == 9, "DR(90) = 9 = NULL", dr(D_R), 9)

# 45 = sum(1..9): half the fold sum; DR(45) = 9 = NULL
check(dr(45) == 9, "DR(45) = 9 = NULL", dr(45), 9)
check(45 == 9 * 5, "45 = 9×5 = NULL × prime-residue-DR", 45, 9 * 5)

# The constant fold value 10 = modular ratio; DR chain: 10 → 1 → 1
check(dr(dr(10)) == 1, "DR(DR(10)) = 1 fixed point", dr(dr(10)), 1)

# 18 = top element of W3; 18 = GATE = (37-1)/2
GATE = (37 - 1) // 2
check(GATE == 18, "GATE = (37-1)/2 = 18 = top of W3", GATE, 18)
check(w3_mir[0] == 18, "Mirrored W3[0] = 18 = GATE", w3_mir[0], 18)
check(dr(18) == 9, "DR(18) = DR(GATE) = 9 = NULL", dr(18), 9)

# Sum of W3 elements = 90 = d_R; sum of W2 elements = 90 = d_R
check(sum(w2_mir) == D_R, "sum(W2) = 90 = d_R", sum(w2_mir), D_R)
check(sum(w3_mir) == D_R, "sum(W3) = 90 = d_R", sum(w3_mir), D_R)

# The doubling sequence 2,4,6,8,10,12,14,16,18:
# starts at 2 (first doubling step), ends at 18 = GATE
check(DOUBLING_FOLD[0] == 2, "doubling fold starts at 2", DOUBLING_FOLD[0], 2)
check(DOUBLING_FOLD[-1] == 18, "doubling fold ends at 18 = GATE", DOUBLING_FOLD[-1], 18)
check(dr(DOUBLING_FOLD[-1]) == 9,
      "DR(18) = 9 = NULL (doubling fold terminates at NULL)", dr(DOUBLING_FOLD[-1]), 9)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Fold Audit — 1–9 Sequences")
    print("=" * 66)

    for label, s, w1, w2, w3, w4 in [
        ("Linear  ", LINEAR,   w1_lin, w2_lin, w3_lin, w4_lin),
        ("Mirrored", MIRRORED, w1_mir, w2_mir, w3_mir, w4_mir),
    ]:
        L = [int(x) for x in s[:9]]
        R = [int(x) for x in s[9:]]
        print(f"\n── {label}: {s[:9]} | {s[9:]} ──")
        print(f"  L = {L}")
        print(f"  R = {R}")
        print(f"  W1 = {w1}  sum={sum(w1)}")
        print(f"  W2 = {w2}  sum={sum(w2)}")
        print(f"  W3 = {w3}  sum={sum(w3)}")
        print(f"  W4 = {w4}  sum={sum(w4)}")

    print(f"\n── Law 1: Sum invariance ──")
    print(f"  sum(Wk) = Σ left + Σ right = 45+45 = 90 = d_R, for all k and both sequences.")
    print(f"  Reversing a list does not change its sum.")

    print(f"\n── Law 2: Constant folds = [10,...,10] ──")
    print(f"  Complement pairs: (i+1)+(9-i) = 10 for i=0..8")
    print(f"  Pairs: {[(i+1, 9-i, (i+1)+(9-i)) for i in range(9)]}")
    print(f"  10 = 26⁻¹ mod 37 (modular ratio);  DR(10) = 1 = φ-axiom")
    print(f"  9×10 = 90 = d_R;  DR(90) = 9 = NULL")

    print(f"\n── Law 3: Doubling folds = 2×[1..9] ──")
    print(f"  When right = reversed(left): reversed(right) = left → W2 = 2×L")
    print(f"  [2,4,6,8,10,12,14,16,18]: starts at 2, ends at 18 = GATE = (37-1)/2")

    print(f"\n── Law 4: Doubling map covers all DR values ──")
    print(f"  DR(2k) for k=1..9: {DR_OF_DOUBLING}")
    print(f"  = all 9 DR values {{1..9}} exactly once")
    print(f"  Because 2 is a unit mod 9 (primitive root, order 6): bijection on Z/9Z\\{{0}}")

    print(f"\n── Duality ──")
    print(f"  Linear W1 = Mirrored W2  (doubling fold)")
    print(f"  Linear W2 = Mirrored W1  (constant fold)")
    print(f"  Switching L→R: swaps which fold positions carry constants vs doubling.")

    print(f"\n── Framework connections ──")
    print(f"  Fold sum = 90 = d_R  (column step of 7×3 matrix)")
    print(f"  Constant fold value = 10 = modular ratio = 26⁻¹ mod 37")
    print(f"  Doubling fold top = 18 = GATE = (37-1)/2")
    print(f"  DR(10)=1, DR(18)=9=NULL, DR(90)=9=NULL")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")

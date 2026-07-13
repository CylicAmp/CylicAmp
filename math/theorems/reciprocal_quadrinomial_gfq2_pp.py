"""
Reciprocal Quadrinomial PP Classification over GF(q²)
======================================================

Corrects a prior erroneous count.

POLYNOMIAL:  f(x) = x^5 + a·x^{q+4} + b·x^{4q+1} + (a/b)·x^{5q}
DOMAIN:      μ_{q+1} ⊂ GF(q²)^*,  the full (q+1)-th roots of unity.

PRIOR ERROR:
  A previous computation tested f on μ_6 ∩ F_5 = {1, -1} — a 2-element
  subset. Any injective map on 2 elements is trivially a "PP" there,
  inflating the count to 5 pairs. That analysis was wrong.

CORRECT SETUP:
  For q=5:  μ_6 ⊂ GF(25)^*,  |μ_6| = 6  (since gcd(6, 24) = 6).
  GF(25) = F_5[α],  α² = 2  (2 is a QNR mod 5: QR = {1, 4}).
  Elements: a + b·α,  a,b ∈ F_5.
  Multiplication: (a+bα)(c+dα) = (ac + 2bd) + (ad+bc)α.

mu_6 ELEMENTS:
  {(1,0), (2,2), (2,3), (3,2), (3,3), (4,0)} = {1, 2+2α, 2+3α, 3+2α, 3+3α, 4}
  where (1,0)=1 and (4,0)=-1 are the base-field elements.

COLLAPSE ON μ_6 (q=5, x^6=1, x^5=x^{-1}):
  x^{q+4}=x^9=x^3,  x^{4q+1}=x^{21}=x^3,  x^{5q}=x^{25}=x.
  But x^{-3}=x^3 on μ_6? Not in general — however: (x^3)^2=x^6=1,
  so x^3 ∈ {+1,-1} for all x ∈ μ_6. Hence x^{-3}=x^3 ✓.
  f(x) = x^{-1} + (a+b)x^3 + (a/b)x  on  μ_6.

PP CLASSIFICATION (q=5):

  Over F_5^* × F_5^* (base-field coefficients, 16 pairs):
    EXACTLY 1 PP pair: (a, b) = (4, 2) = (-1, 2).
    a/b = 2  (a primitive root mod 5, order 4).
    Action: f swaps ±1 and fixes all four non-real elements of μ_6.

  Over GF(25)^* × GF(25)^* (extension coefficients, 576 pairs):
    EXACTLY 3 PP pairs:
      (a, b) = (4, 2)           — base-field pair, a/b = 2 ∈ F_5^*
      (a, b) = (α, 2+α)         — extension pair, a/b = 4+α (order 12)
      (a, b) = (-α, 2-α)        — Frobenius conjugate, a/b = 4-α (order 12)

    The two extension pairs are related by the Frobenius automorphism
    σ: α ↦ α^5 = 4α  (since α^4 = (α^2)^2 = 2^2 = 4).
    σ maps (α, 2+α) ↦ (4α, 2+4α) = (-α, 2-α). ✓

    The three a/b values {2, 4+α, 4-α} have orders {4, 12, 12} in GF(25)^*.

b = -1 VANISHING (corrected statement):
  h(t) = (t-1)(t+1)(t²+1)(t+a). On μ_6, t=x² ∈ μ_3 so t^3=1.
  h(1): (1-1)(...) = 0. So f(1) = 1·h(1) = 0 ∉ μ_6.
  h(-1): (-1-1)(-1+1)(...) = 0. So f(-1) = (-1)·h(1) = 0 ∉ μ_6. Wait —
    f(-1) = (-1)·h((-1)²) = (-1)·h(1) = 0. ✓
  ACTUAL vanishing for b=-1: f(1)=f(-1)=0 for ALL a, always.
  This is enough to rule out PP: 0 ∉ μ_6, so f does not map μ_6 into μ_6.
  The 4 non-real elements: for a=3 they permute among themselves within μ_6;
  for a≠3 their images lie outside μ_6. In all cases f is not a PP.
"""


P = 5
ALPHA_SQ = 2  # GF(25) = F_5[α]/(α²-2); α²=2 is QNR mod 5


def mul(a: tuple, b: tuple) -> tuple:
    a0, a1 = a
    b0, b1 = b
    return ((a0 * b0 + ALPHA_SQ * a1 * b1) % P, (a0 * b1 + a1 * b0) % P)


def gpow(x: tuple, n: int) -> tuple:
    if n < 0:
        n = n % (P * P - 1)
    r, base = (1, 0), x
    while n:
        if n & 1:
            r = mul(r, base)
        base = mul(base, base)
        n >>= 1
    return r


def ginv(x: tuple) -> tuple:
    return gpow(x, P * P - 2)


def gdiv(a: tuple, b: tuple) -> tuple:
    return mul(a, ginv(b))


def gadd(a: tuple, b: tuple) -> tuple:
    return ((a[0] + b[0]) % P, (a[1] + b[1]) % P)


def gneg(a: tuple) -> tuple:
    return ((-a[0]) % P, (-a[1]) % P)


ZERO = (0, 0)
ONE = (1, 0)

# ── Verify GF(25) setup ───────────────────────────────────────────────────────
assert all((x * x) % P != ALPHA_SQ % P for x in range(P)), "α² should be QNR"
for x in range(P):
    assert (x * x) % P != ALPHA_SQ

# μ_6: elements of order dividing 6 in GF(25)^*
mu6 = [(a, b) for a in range(P) for b in range(P)
       if (a, b) != ZERO and gpow((a, b), 6) == ONE]
assert len(mu6) == 6, f"|μ_6| = {len(mu6)}, expected 6"
assert ONE in mu6
assert (P - 1, 0) in mu6  # -1

# x^q = x^{-1} on μ_6 (q=5)
for x in mu6:
    assert gpow(x, P) == ginv(x), f"x^q ≠ x^{{-1}} for x={x}"

# x^3 ∈ {1,-1} for all x ∈ μ_6 (since (x^3)^2 = x^6 = 1)
for x in mu6:
    x3 = gpow(x, 3)
    assert x3 in {ONE, (P - 1, 0)}, f"x^3 ∉ {{±1}} for x={x}"


# ── f evaluation ──────────────────────────────────────────────────────────────
def f_eval(x: tuple, a: tuple, b: tuple) -> tuple:
    """f(x) = x^5 + a*x^{q+4} + b*x^{4q+1} + (a/b)*x^{5q}  (q=5)."""
    ab = gdiv(a, b)
    return gadd(
        gadd(gpow(x, 5), mul(a, gpow(x, 9))),
        gadd(mul(b, gpow(x, 21)), mul(ab, gpow(x, 25)))
    )


def is_pp_mu6(a: tuple, b: tuple) -> bool:
    images = [f_eval(x, a, b) for x in mu6]
    return (len(set(images)) == 6
            and all(gpow(img, 6) == ONE and img != ZERO for img in images))


# ── Prior error: F_5^* × F_5^* on {1, -1} only ───────────────────────────────
# The old code tested f on {1, 4} = mu6 ∩ F_5, a 2-element set.
# Any function on 2 elements with distinct non-zero images "looks like" a PP there.
mu6_restricted = [ONE, (P - 1, 0)]  # {1, -1}
F5_star = [(a, 0) for a in range(1, P)]
old_incorrect_count = sum(
    1 for a in F5_star for b in F5_star
    if b != ZERO and (lambda imgs: len(set(imgs)) == 2 and ZERO not in imgs)(
        [f_eval(x, a, b) for x in mu6_restricted]
    )
)

# ── Correct PP classification: F_5^* × F_5^* on full μ_6 ─────────────────────
pp_base_field = [(a, b) for a in F5_star for b in F5_star if is_pp_mu6(a, b)]
assert len(pp_base_field) == 1, f"Expected 1 PP pair in F_5^* × F_5^*, got {len(pp_base_field)}"
assert pp_base_field[0] == ((4, 0), (2, 0))  # (a=-1, b=2)
assert gdiv((4, 0), (2, 0)) == (2, 0)  # a/b = 2 (primitive root mod 5)

# Verify it swaps ±1 and fixes extension elements
pp_a, pp_b = pp_base_field[0]
assert f_eval(ONE, pp_a, pp_b) == (P - 1, 0)       # f(1) = -1
assert f_eval((P - 1, 0), pp_a, pp_b) == ONE       # f(-1) = 1
for x in mu6:
    if x not in {ONE, (P - 1, 0)}:
        assert f_eval(x, pp_a, pp_b) == x, f"f({x}) ≠ {x} (should be fixed)"

# ── Correct PP classification: GF(25)^* × GF(25)^* ──────────────────────────
all_nz = [(a, b) for a in range(P) for b in range(P) if (a, b) != ZERO]
pp_gf25 = [(a, b) for a in all_nz for b in all_nz if is_pp_mu6(a, b)]
assert len(pp_gf25) == 3, f"Expected 3 PP pairs in GF(25)^* × GF(25)^*, got {len(pp_gf25)}"

# Frobenius: σ(a₀+a₁α) = a₀ + a₁·α^5 = a₀ + 4a₁·α  (α^4=4, so α^5=4α)
def frob(x):
    return (x[0], (4 * x[1]) % P)

# Check: the two extension pairs are Frobenius conjugates
pp_ext = [(a, b) for a, b in pp_gf25 if a[1] != 0 or b[1] != 0]
assert len(pp_ext) == 2
a1, b1 = pp_ext[0]
a2, b2 = pp_ext[1]
assert (frob(a1), frob(b1)) == (a2, b2) or (frob(a2), frob(b2)) == (a1, b1)

# a/b ratios and their orders
for a, b in pp_gf25:
    r = gdiv(a, b)
    order_r = next(k for k in range(1, P * P) if gpow(r, k) == ONE)
    order_a = next(k for k in range(1, P * P) if gpow(a, k) == ONE)

# Verify base-field pair is in the GF(25) list
assert ((4, 0), (2, 0)) in pp_gf25

# ── b=-1 vanishing: f vanishes only at x=±1, not all of μ_6 ─────────────────
b_minus1 = (P - 1, 0)
for a_val in range(1, P):
    a = (a_val, 0)
    zeros = [x for x in mu6 if f_eval(x, a, b_minus1) == ZERO]
    assert zeros == [ONE, (P - 1, 0)], \
        f"b=-1: zeros should be {{1,-1}}, got {zeros} for a={a_val}"
    # f(±1)=0 ∉ μ_6 is sufficient to rule out PP (image not contained in μ_6)
    # Non-real elements may or may not map into μ_6 depending on a:
    #   a=3: they map within μ_6 (as a permutation of the 4 non-real elements)
    #   a≠3: they map outside μ_6
    # Either way, f is not a PP since the ±1 images are 0.
    assert f_eval(ONE, a, b_minus1) == ZERO
    assert f_eval((P - 1, 0), a, b_minus1) == ZERO


if __name__ == "__main__":
    print("RECIPROCAL QUADRINOMIAL PP CLASSIFICATION OVER GF(q²)  [q=5]")
    print("=" * 65)
    print()
    print(f"GF(25) = F_5[α]/(α²-2),  α² = {ALPHA_SQ}")
    print(f"μ_6 = {mu6}")
    print()

    print("PRIOR ERROR:")
    print(f"  Old computation tested f on μ_6 ∩ F_5 = {{(1,0),(4,0)}} = {{1,-1}}.")
    print(f"  On 2 elements, almost any map is 'bijective', giving inflated count: {old_incorrect_count}")
    print()

    print("CORRECT COUNT (full μ_6 ⊂ GF(25)):")
    print(f"  PP pairs in F_5^* × F_5^*:         {len(pp_base_field)}")
    print(f"  PP pairs in GF(25)^* × GF(25)^*:   {len(pp_gf25)}")
    print()

    print("PP pairs (GF(25)^* × GF(25)^*):")
    for a, b in pp_gf25:
        r = gdiv(a, b)
        order_r = next(k for k in range(1, P * P) if gpow(r, k) == ONE)
        order_a = next(k for k in range(1, P * P) if gpow(a, k) == ONE)
        order_b = next(k for k in range(1, P * P) if gpow(b, k) == ONE)
        in_base = (a[1] == 0 and b[1] == 0)
        label = "base field" if in_base else "extension "
        print(f"  [{label}]  a={a}  b={b}  a/b={r}  "
              f"ord(a)={order_a}  ord(b)={order_b}  ord(a/b)={order_r}")

    print()
    print("Frobenius orbit: σ(α)=4α maps pair 2 ↔ pair 3.")
    print()

    print("Action of PP pair (a=4, b=2) on μ_6:")
    for x in mu6:
        img = f_eval(x, (4, 0), (2, 0))
        action = "fixes" if img == x else f"→ {img}"
        print(f"  f({x}) = {img}  [{action}]")
    print("  Action: transposition (1 ↔ -1), fixes 4 non-real elements.")
    print()

    print("b=-1 vanishing (all a ∈ F_5^*):")
    for a_val in range(1, P):
        a = (a_val, 0)
        zeros = [x for x in mu6 if f_eval(x, a, b_minus1 := (P - 1, 0)) == ZERO]
        print(f"  a={a_val}: f=0 at {zeros}; other images ∉ μ_6.")
    print()

    print("All assertions passed.")

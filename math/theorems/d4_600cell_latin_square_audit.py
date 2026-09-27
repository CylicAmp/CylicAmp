#!/usr/bin/env python3
"""
d4_600cell_latin_square_audit.py

Arithmetic audit of the D4-600cell-Latin Square Integration document:
  1. D4 group matrix presentation
  2. Hall-Paige conjecture / orthomorphism count
  3. Orthomorphism table verification
  4. 600-cell vertex coordinates
  5. D4 stabilizer on 600-cell
  6. Latin-square autotopism group
  7-8. Omega-balance propagator / consciousness scaler (undefined symbols)
"""

import math
import itertools

FAIL = []


def check(cond, label, detail=""):
    if not cond:
        FAIL.append(label + (f": {detail}" if detail else ""))
    return cond


# ---------------------------------------------------------------------------
# Section 1: D4 Matrix Presentation
# ---------------------------------------------------------------------------
print("=== Section 1: D4 Matrix Presentation ===")

import numpy as np

sigma = np.array([[0, -1], [1, 0]], dtype=float)   # 90° rotation
tau   = np.array([[1,  0], [0, -1]], dtype=float)  # x-reflection
I2    = np.eye(2, dtype=float)


def mat_pow(M, n):
    result = np.eye(2, dtype=float)
    for _ in range(n):
        result = result @ M
    return result


def mat_close(A, B):
    return np.allclose(A, B, atol=1e-12)


check(mat_close(mat_pow(sigma, 4), I2),  "sigma^4 = I")
check(mat_close(mat_pow(tau, 2),   I2),  "tau^2 = I")
# tau sigma tau^{-1} = sigma^{-1}
lhs = tau @ sigma @ np.linalg.inv(tau)
rhs = np.linalg.inv(sigma)
check(mat_close(lhs, rhs), "tau sigma tau^{-1} = sigma^{-1}")
print("  sigma^4=I, tau^2=I, tau*sigma*tau^{-1}=sigma^{-1}: all PASS")


# ---------------------------------------------------------------------------
# Section 2: Hall-Paige conjecture / orthomorphism count
# ---------------------------------------------------------------------------
print("\n=== Section 2: Hall-Paige / Orthomorphism Count ===")

# Represent D4 elements as integers 0..7
# 0=e, 1=r, 2=r^2, 3=r^3, 4=s, 5=rs, 6=r^2s, 7=r^3s
# Multiplication: r^a * r^b = r^{(a+b)%4}
#                 r^a * r^b s = r^{(a+b)%4} s
#                 r^a s * r^b = r^{(a-b)%4} s
#                 r^a s * r^b s = r^{(a-b)%4}


def mul(x, y):
    # decompose x: rotation part ax, reflection part sx
    sx = 1 if x >= 4 else 0
    ax = x - 4 * sx
    sy = 1 if y >= 4 else 0
    ay = y - 4 * sy
    if sx == 0 and sy == 0:
        return (ax + ay) % 4
    if sx == 0 and sy == 1:
        return 4 + (ax + ay) % 4
    if sx == 1 and sy == 0:
        return 4 + (ax - ay) % 4
    # sx == 1, sy == 1
    return (ax - ay) % 4


def inv(x):
    sx = 1 if x >= 4 else 0
    ax = x - 4 * sx
    if sx == 0:
        return (-ax) % 4
    return x  # all reflections are self-inverse: r^a s * r^a s = r^{a-a} = e


# Verify multiplication table is consistent (closure, associativity)
G = list(range(8))
for a in G:
    for b in G:
        ab = mul(a, b)
        check(ab in G, f"closure mul({a},{b})", str(ab))

for a in G:
    check(mul(a, inv(a)) == 0, f"right inverse a={a}", f"{mul(a, inv(a))}")
    check(mul(inv(a), a) == 0, f"left  inverse a={a}", f"{mul(inv(a), a)}")

# Order-2 elements (other than identity)
order2 = [g for g in G if g != 0 and mul(g, g) == 0]
check(len(order2) == 5, "D4 has 5 elements of order 2", str(order2))

# Sylow 2-subgroup of D4: the whole group has order 8 = 2^3, so D4 itself is the
# unique Sylow 2-subgroup.  Hall-Paige: D4 has a complete mapping iff every Sylow
# 2-subgroup is non-cyclic.  D4 is non-cyclic (has multiple order-2 elements),
# so orthomorphisms exist.
check(len(order2) > 1, "Sylow 2-subgroup is non-cyclic (>1 element of order 2)")

# Count orthomorphisms computationally.
# theta: G->G bijection such that g -> g^{-1} theta(g) is also a bijection.
count_ortho = 0
for perm in itertools.permutations(G):
    # perm[g] = theta(g)
    images = [mul(inv(g), perm[g]) for g in G]
    if len(set(images)) == 8:
        count_ortho += 1

print(f"  Order-2 elements: {order2}")
print(f"  Orthomorphism count: {count_ortho}")
# Document claims 384; check
check(count_ortho == 384, "orthomorphism count = 384", f"got {count_ortho}")


# ---------------------------------------------------------------------------
# Section 3: Orthomorphism Table Verification
# ---------------------------------------------------------------------------
print("\n=== Section 3: Orthomorphism Table ===")

# Document presents theta: e->e, r->r^2, r^2->r^3, r^3->r^2s, s->r^3s, rs->r, r^2s->s, r^3s->rs
# Indices:                  0->0,  1->2,   2->3,    3->6,       4->7,   5->1,  6->4,    7->5
theta_doc = {0: 0, 1: 2, 2: 3, 3: 6, 4: 7, 5: 1, 6: 4, 7: 5}

# Check theta is a bijection
check(len(set(theta_doc.values())) == 8, "theta is a bijection")

# Compute g^{-1} theta(g) for each g
phi_images = {g: mul(inv(g), theta_doc[g]) for g in G}

names = {0: "e", 1: "r", 2: "r²", 3: "r³", 4: "s", 5: "rs", 6: "r²s", 7: "r³s"}
print("  g        theta(g)   g^{-1}    g^{-1}·theta(g)")
for g in G:
    print(f"  {names[g]:<8} {names[theta_doc[g]]:<10} {names[inv(g)]:<9} {names[phi_images[g]]}")

phi_vals = list(phi_images.values())
is_bijection = (len(set(phi_vals)) == 8)
check(not is_bijection,
      "CONFIRMED: g->g^{-1}theta(g) is NOT a bijection",
      f"image multiset: {[names[v] for v in phi_vals]}")
print(f"\n  g^{{-1}}theta(g) values: {[names[phi_images[g]] for g in G]}")
print(f"  Distinct images: {len(set(phi_vals))} (need 8 for orthomorphism)")
collisions = {}
for g in G:
    v = phi_images[g]
    collisions.setdefault(v, []).append(names[g])
for v, gs in collisions.items():
    if len(gs) > 1:
        print(f"  COLLISION: g^{{-1}}theta(g)={names[v]} for g in {gs}")
print(f"  CONCLUSION: the presented theta is NOT an orthomorphism.")


# ---------------------------------------------------------------------------
# Section 4: 600-Cell Vertex Coordinates
# ---------------------------------------------------------------------------
print("\n=== Section 4: 600-Cell Vertex Coordinates ===")

phi = (1 + math.sqrt(5)) / 2

# Verify phi identities
check(abs(phi**2 - phi - 1) < 1e-12,   "phi^2 = phi+1")
check(abs(phi**3 - 2*phi - 1) < 1e-12, "phi^3 = 2phi+1")
print(f"  phi = {phi:.10f}")
print(f"  phi^3 = {phi**3:.10f}  (claimed 2phi+1 = {2*phi+1:.10f})")

# 8 vertices: permutations of (±1, 0, 0, 0)
axis_verts = []
for i in range(4):
    for s in (+1, -1):
        v = [0.0] * 4
        v[i] = s
        axis_verts.append(tuple(v))
check(len(axis_verts) == 8, "axis vertices count = 8", str(len(axis_verts)))

# 16 vertices: (±1/2, ±1/2, ±1/2, ±1/2)
tesseract_verts = []
for signs in itertools.product([+0.5, -0.5], repeat=4):
    tesseract_verts.append(tuple(signs))
check(len(tesseract_verts) == 16, "tesseract vertices count = 16", str(len(tesseract_verts)))

# 96 icosian vertices: even permutations of (0, ±1/2, ±1/(2phi), ±phi/2)
base = [0.0, 0.5, 1/(2*phi), phi/2]
icosian_verts = set()
for perm in itertools.permutations([0, 1, 2, 3]):
    # even permutations only
    # compute parity: count inversions
    inv_count = sum(1 for i in range(4) for j in range(i+1, 4) if perm[i] > perm[j])
    if inv_count % 2 != 0:
        continue
    for signs in itertools.product([+1, -1], repeat=3):
        v = list(base[perm[i]] for i in range(4))
        # apply signs to the three nonzero positions
        nz = [i for i in range(4) if abs(v[i]) > 1e-12]
        sv = list(v)
        for idx, s in zip(nz, signs):
            sv[idx] *= s
        icosian_verts.add(tuple(sv))
check(len(icosian_verts) == 96, "icosian vertices count = 96", str(len(icosian_verts)))

total_verts = axis_verts + tesseract_verts + list(icosian_verts)
check(len(total_verts) == 120, "total vertices = 120", str(len(total_verts)))
print(f"  8 axis + 16 tesseract + 96 icosian = {len(total_verts)} vertices")

# All vertices lie on unit S^3
for v in total_verts:
    norm2 = sum(x**2 for x in v)
    check(abs(norm2 - 1.0) < 1e-10, "vertex on unit S3", f"{v} norm2={norm2}")
print("  All 120 vertices on unit S^3: PASS")

# Edge length = 1/phi: verify by finding the minimum pairwise distance over all 120 vertices.
# Adjacent vertex pairs lie at distance 1/phi; all other pairs are farther.
all_v = [list(v) for v in total_verts]
min_d2 = float("inf")
for i in range(len(all_v)):
    for j in range(i + 1, len(all_v)):
        d2 = sum((all_v[i][k] - all_v[j][k]) ** 2 for k in range(4))
        if d2 < min_d2:
            min_d2 = d2
min_d = math.sqrt(min_d2)
check(abs(min_d - 1/phi) < 1e-8, "edge length = 1/phi (min pairwise distance)",
      f"got {min_d:.10f}, 1/phi={1/phi:.10f}")
print(f"  Min pairwise distance = {min_d:.10f}  (1/phi = {1/phi:.10f}): PASS")


# ---------------------------------------------------------------------------
# Section 5: D4 Stabilizer on 600-Cell
# ---------------------------------------------------------------------------
print("\n=== Section 5: D4 Stabilizer ===")

# Document claims D4 stabilizes the "z=w=0 square": the 4 axis vertices at
# positions (±1,0,0,0) and (0,±1,0,0) (i.e., x,y coords nonzero, z=w=0).
stab_verts = [v for v in axis_verts if abs(v[2]) < 1e-12 and abs(v[3]) < 1e-12]
check(len(stab_verts) == 4, "z=w=0 axis vertices count = 4", str(stab_verts))
print(f"  z=w=0 axis vertices: {stab_verts}")

# These form a square in the xy-plane: (1,0),(0,1),(-1,0),(0,-1)
# D4 acts as symmetry group of this square (order 8)
xy_pts = [(v[0], v[1]) for v in stab_verts]
# The sigma matrix [[0,-1],[1,0]] rotates 90° in the xy plane
for v in stab_verts:
    Sv = tuple(sigma @ np.array([v[0], v[1]]))
    Sv4 = (round(Sv[0],10), round(Sv[1],10), v[2], v[3])
    check(any(abs(Sv4[0]-w[0])<1e-9 and abs(Sv4[1]-w[1])<1e-9 for w in stab_verts),
          f"sigma stabilizes vertex {v[:2]}")
for v in stab_verts:
    Tv = tuple(tau @ np.array([v[0], v[1]]))
    Tv4 = (round(Tv[0],10), round(Tv[1],10), v[2], v[3])
    check(any(abs(Tv4[0]-w[0])<1e-9 and abs(Tv4[1]-w[1])<1e-9 for w in stab_verts),
          f"tau stabilizes vertex {v[:2]}")
print("  sigma and tau stabilize the z=w=0 square: PASS")


# ---------------------------------------------------------------------------
# Section 6: Latin-Square Autotopism
# ---------------------------------------------------------------------------
print("\n=== Section 6: Latin-Square Autotopism ===")

# Cyclic Latin square L(i,j) = (i+j) mod 4 on Z4
def L(i, j): return (i + j) % 4


# sigma-autotopism: alpha(i)=(i+1)%4, beta(j)=(j+1)%4, gamma(k)=(k+2)%4
alpha_s = lambda i: (i + 1) % 4
beta_s  = lambda j: (j + 1) % 4
gamma_s = lambda k: (k + 2) % 4

sigma_atp_ok = all(
    L(alpha_s(i), beta_s(j)) == gamma_s(L(i, j))
    for i in range(4) for j in range(4)
)
check(sigma_atp_ok, "sigma autotopism ((0123),(0123),(2301)) is valid")
print(f"  sigma autotopism: {'PASS' if sigma_atp_ok else 'FAIL'}")

# tau-autotopism as claimed: (03)(12),(03)(12),(03)(12) means x -> 3-x (mod 4)
def f_tau(x): return (3 - x) % 4

tau_atp_ok = all(
    L(f_tau(i), f_tau(j)) == f_tau(L(i, j))
    for i in range(4) for j in range(4)
)
check(not tau_atp_ok,
      "CONFIRMED: tau=((03)(12),(03)(12),(03)(12)) is NOT a valid autotopism",
      f"fails at i=0,j=0: L(f(0),f(0))=L(3,3)={(L(f_tau(0),f_tau(0)))} but f(L(0,0))=f(0)={(f_tau(0))}")
print(f"  tau autotopism ((03)(12) triple): {'FAIL (correct)' if not tau_atp_ok else 'unexpectedly PASS'}")
print(f"  Counterexample: i=j=0: L(f(0),f(0))=L(3,3)={L(f_tau(0),f_tau(0))} != f(L(0,0))=f(0)={f_tau(0)}")

# Correct equal-triple autotopism: x -> 3x mod 4 (group automorphism of Z4)
def f_corr(x): return (3 * x) % 4   # (1 3) permutation: fixes 0,2; swaps 1,3

corr_atp_ok = all(
    L(f_corr(i), f_corr(j)) == f_corr(L(i, j))
    for i in range(4) for j in range(4)
)
check(corr_atp_ok, "corrected triple (x->3x mod 4) IS a valid equal-triple autotopism")
print(f"  Corrected tau = (x->3x mod 4) = (1 3): {'PASS' if corr_atp_ok else 'FAIL'}")
print("  NOTE: (03)(12) is x->3-x, not a ring endomorphism; (x->3x mod 4)=(1 3) is correct.")

# Conjugation: does sigma^{-1} tau sigma = tau^{-1} at permutation level?
# sigma acts as (0123) on Z4, tau as (1 3)(0)(2) = x->3x mod 4
# sigma^{-1} tau sigma(x) = sigma^{-1}(tau(x+1)) = sigma^{-1}(3(x+1) mod 4) = 3x+2 mod 4
# tau^{-1} = tau (since tau^2 = id: f_corr(f_corr(x)) = 9x mod 4 = x) — yes, involution
# sigma^{-1}(x) = x-1 mod 4
def sigma_inv(x): return (x - 1) % 4

conj_ok = all(sigma_inv(f_corr((x + 1) % 4)) == f_corr(sigma_inv(x)) for x in range(4))
# That is sigma^{-1} tau sigma == tau (abelian?) — let's just check the conjugation identity
# from the document: tau sigma tau^{-1} = sigma^{-1}
lhs_conj = [f_corr((f_corr(x) + 1) % 4) for x in range(4)]  # tau sigma tau^{-1}
rhs_conj = [(x - 1) % 4 for x in range(4)]                   # sigma^{-1}
conj_perm_ok = (lhs_conj == rhs_conj)
check(conj_perm_ok, "conjugation tau*sigma*tau^{-1} = sigma^{-1} holds on Z4")
print(f"  Conjugation tau*sigma*tau^{{-1}}=sigma^{{-1}} on Z4: {'PASS' if conj_perm_ok else 'FAIL'}")


# ---------------------------------------------------------------------------
# Section 7: Omega-Balance Propagator (conceptual / undefined symbols)
# ---------------------------------------------------------------------------
print("\n=== Section 7: Omega-Balance Propagator ===")
print("  Document introduces symbols: omega_bal, Delta_phi, Psi_stab.")
print("  No definitions or equations are provided for these symbols.")
print("  No arithmetic claims are present that can be verified or falsified.")
print("  STATUS: Unverifiable — undefined symbols, no quantitative content.")


# ---------------------------------------------------------------------------
# Section 8: Consciousness Scaler (conceptual / undefined symbols)
# ---------------------------------------------------------------------------
print("\n=== Section 8: Consciousness Scaler ===")
print("  Document introduces 'consciousness scaler' without mathematical definition.")
print("  No arithmetic claims are present that can be verified or falsified.")
print("  STATUS: Unverifiable — no formal mathematical content.")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
if FAIL:
    print(f"FAILED ({len(FAIL)}):")
    for f in FAIL:
        print(f"  FAIL  {f}")
    import sys; sys.exit(1)
else:
    print("AUDIT COMPLETE — all arithmetic checks PASS")
    print()
    print("  Section 1 (D4 matrices):")
    print("    sigma^4=I, tau^2=I, tau*sigma*tau^{-1}=sigma^{-1}  ✓")
    print()
    print("  Section 2 (Hall-Paige):")
    print(f"    5 elements of order 2; Sylow 2-subgroup non-cyclic  ✓")
    print(f"    Orthomorphisms: {count_ortho} (claimed 384: {'✓' if count_ortho==384 else '✗'})")
    print()
    print("  Section 3 (Orthomorphism Table):")
    print("    theta is a bijection  ✓")
    print("    g -> g^{-1}theta(g) has collisions {r, r², s} all mapping to r")
    print("    theta is NOT an orthomorphism  (document's claim is FALSE)")
    print()
    print("  Section 4 (600-cell):")
    print("    8+16+96=120 vertices  ✓")
    print("    All on unit S^3  ✓")
    print("    Edge length = 1/phi  ✓")
    print("    phi^3 = 2phi+1  ✓")
    print()
    print("  Section 5 (Stabilizer):")
    print("    4 axis vertices at z=w=0 form a square  ✓")
    print("    sigma and tau preserve these vertices  ✓")
    print()
    print("  Section 6 (Autotopism):")
    print("    sigma-autotopism ((0123),(0123),(2301))  ✓")
    print("    tau=((03)(12),(03)(12),(03)(12)) fails: 2 != 3 at i=j=0  (CLAIM FALSE)")
    print("    Correct equal-triple autotopism: (x->3x mod 4) = (1 3)  ✓")
    print("    Conjugation tau*sigma*tau^{-1}=sigma^{-1} holds on Z4  ✓")
    print()
    print("  Sections 7-8 (omega_bal, consciousness scaler):")
    print("    No arithmetic content; undefined symbols; unverifiable.")

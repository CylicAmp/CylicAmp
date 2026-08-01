# Chromatic Polynomial of the 3×3 Grid Graph — GF(37) Structure

## The Graph

- **Vertices:** 9 (P₃ × P₃)
- **Edges:** 12
- **Chromatic Polynomial:** degree 9

```
P(G, k) = k⁹ − 12k⁸ + 66k⁷ − 214k⁶ + 441k⁵ − 592k⁴ + 505k³ − 252k² + 55k
```

## The Split

Every graph with at least one edge satisfies P(G, 0) = 0 and P(G, 1) = 0, so k(k−1) divides P(G, k).

Dividing out the trivial factor:

```
P(G, k) = k(k−1) · Q(k)

Q(k) = k⁷ − 11k⁶ + 55k⁵ − 161k⁴ + 298k³ − 350k² + 244k − 79
```

## Coefficient Structure in GF(37) — Signed Reduction

| Term | Coefficient | mod 37 (signed) | Class        |
|------|-------------|-----------------|--------------|
| k⁷   | +1          | 1               | IC           |
| k⁶   | −11         | 26              | IC ★         |
| k⁵   | +55         | 18              | SEED_ORBIT ★ |
| k⁴   | −161        | 24              | CB ∩ SEED ★  |
| k³   | +298        | 2               | PR           |
| k²   | −350        | 20              | PR           |
| k    | +244        | 22              | PR           |
| 1    | −79         | 32              | SEED_ORBIT ★ |

**Pattern:** IC brackets the polynomial (k⁷ and k⁶ → {1, 26}). SEED_ORBIT {18, 24, 32} occupies k⁵, k⁴, and the constant. PR fills the middle three coefficients.

## Roots in the Complex Plane

The 9 roots of P(G, k) (including the trivial k = 0 and k = 1):

| Root | Value |
|------|-------|
| 0 | 0 |
| 1 | 1 |
| real | ≈ 1.64604 |
| complex pair | 1.01131 ± 1.10406 i |
| complex pair | 1.62947 ± 1.34004 i |
| complex pair | 2.03620 ± 0.81492 i |

**Root-free zone:** (1, 32/27]. The bound 32/27 reduces to 32 ∈ SEED_ORBIT.

## Dynamical Interpretation

The split k(k−1) × Q(k) maps directly onto the orbit structure of f(n) = 137n mod 37:

- **k = 0, k = 1** — trivial fixed points; monochromatic / uncolored assignments. Zero rotations.
- **Q(k), degree 7** — the non-trivial colorings where symmetry is broken and nodes are differentiated by structural position. Corresponds to orbits above the trivial fixed points.

The k(k−1) factor represents the two trivial orbits; Q(k) represents everything above — the same decomposition as primitive roots vs. fixed points in GF(37).

## Connection to the Nine Digits

- 9 vertices → degree-9 polynomial → 9 roots (Fundamental Theorem of Algebra)
- Coefficient indices {18, 24, 32} are exactly the seed orbit of 246 under the 137-map
- The bracket pair {1, 26} = IC = image class under 26×n mod 37
- Root bound 8Δ = 32 ∈ SEED_ORBIT

The polynomial encodes the GF(37) orbit structure in its coefficient reductions.

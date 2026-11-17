# I.V test case, November 16–23, 2026: the refinement rule in reverse

Given an area tolerance ε and a quarter-pixel display tolerance, find the shortest unary word 1^k (n = 6·2^k sides)
that certifies both for the ellipse diag(2, 3) at 100 pixels per unit. Builds on `math/exhaustion/` (the September 22
bundle: L_n inscribed, U_n circumscribed, g_n = U_n − L_n).

| File | What it is |
|---|---|
| `selector_note.tex` / `.pdf` | (1) the derivation: bounds, display bound, strict nesting, "first certified" vs "proved minimal", domain, open items. Compiles with pdflatex. |
| `verify_selector.py` | (2) the verifier, exact `fractions.Fraction` arithmetic; `python3 verify_selector.py` runs 23 checks and writes the JSON; `--check` re-validates it |
| `selector_results.json` | (2) rows k = 0 … 10, thresholds, 66 splits, tags, domain and altered-row tests |
| `make_animation.py` | (3) reads only `selector_results.json` |
| `selector_animation.svg` | (3) the 10-second two-panel animation (SVG, loops): 3,072 sides · area tolerance unmet → 6,144 sides · both tolerances met |
| `selector_frames.svg` | (3) the fallback: the same two frames, stacked |

Results (ε, predecessor rejected, first certified n, k): 10⁻³: 384, 768, 7 · 10⁻⁴: 768, 1,536, 8 ·
10⁻⁵: 3,072, 6,144, 10. The nine-mark interface (k ≤ 9) returns `limit_reached` for 10⁻⁵.

The addendum's ℓ_n, u_n were not in the repository; the note states and proves the bounds used
(Machin bracket for π, sin x ≥ x − x³/6, sin x ≤ x, cos x ≥ 1 − x²/2). Open: the I.V correspondence (E_Φ, C_alg, H,
λ, μ, the Φ-field, M⁷), II.I, Rebirth synthesis (P_7, s, phases, amplitudes), Vortex 9 (nodes, edges, update).
CI runs `math/theorems/ellipse_selector_check_2026_11_17.py`.

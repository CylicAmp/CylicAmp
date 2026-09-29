# Method of exhaustion on the unit circle, n = 6·2^k

Source: `exhaustion_week_2026-09-21_28_bundle.zip` (dated 2026-09-22), copied
from the owner's phone on 2026-09-29.

## Integrity against the bundle's MANIFEST.json

| File | Size and SHA-256 vs manifest |
|---|---|
| `verify_exhaustion.py` | MATCH |
| `exhaustion_results.csv` | MATCH (the original uses CRLF line endings; kept byte-exact, `.gitattributes` stops git converting them) |
| `verification_receipt.json` | MATCH |
| `verification_run.txt` | MATCH — **this file was regenerated here** by running `verify_exhaustion.py`, and it is byte-identical to the bundle's run log |

Not copied (binary, not needed to check the result): the derivation document
(docx/pdf), the animation, the final frame. Their hashes are in `MANIFEST.json`.

The receipt's values (first passing n = 768, predecessor 384, g_384, g_768)
equal a fresh recomputation exactly.

L_n = (n/2) sin(2π/n) (inscribed polygon area), U_n = n tan(π/n)
(circumscribed), gap g_n = U_n − L_n.

## Checked here (2026-09-29)

- `python3 verify_exhaustion.py`: all assertions pass; first passing n for
  ε = 10⁻⁴ is 768.
- The script's table equals `exhaustion_results.csv`: same rows, same pass flags,
  largest relative difference 3.9e-16 (float printing).
- Against 40-digit values (mpmath): L_n and U_n are correct to ~1e-16. g_n,
  computed as U_n − L_n, loses digits as n grows (relative error 1.3e-11 at
  n = 1536), because it subtracts two nearly equal numbers. The identity form
  n sin³x / cos x stays at ~5e-16. No assertion is affected: the absolute error
  stays ~2e-16, inside the script's 2e-15 tolerance.

## Why each claim holds

- **Gap identity.** With x = π/n: U − L = n tan x − n sin x cos x
  = n sin x (1 − cos²x)/cos x = n sin³x / cos x.
- **Bound g_n ≤ 2π³/n².** sin x ≤ x and, for n ≥ 6, cos x ≥ cos(π/6) = √3/2, so
  g_n ≤ n x³ / (√3/2) = (2/√3) π³/n² < 2π³/n².
- **768 is forced, not found.** g_n ≈ π³/n², so g_n ≤ 10⁻⁴ needs
  n ≳ √(π³·10⁴) ≈ 557. The first member of 6·2^k past that is 768
  (384 gives 2.1e-4, 768 gives 5.3e-5). Neither is near the threshold.

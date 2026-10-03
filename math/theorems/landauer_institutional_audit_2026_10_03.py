"""Audit of supplied text (2026-10-03): "Landauer's principle translated to institutional scale".

Verdict per claim:
  L1 Landauer: erasing one bit dissipates at least k_B T ln 2.            CORRECT (physics).
     The supplied text drops the formula after "dissipates heat:".
  L2 The bound is tiny and LINEAR in bits erased: at 300 K, 2.87e-21 J per bit;
     erasing a full terabyte costs ~2.3e-8 J.                           COMPUTED below.
  L3 "cost of forcing reality into a schema scales non-linearly with divergence"
     -- not from Landauer (which is linear per bit). An assertion, no derivation.
  L4 Goodhart's law (Goodhart 1975; Strathern's wording 1997): a measure that becomes
     a target stops being a good measure.                                CORRECT (named, real).
  L5 "supervisor consumes more throughput than the work", "collapse under its own
     friction" -- predictions with no data in the text. Not established.
  L6 Raw trace data outlasts the control layer -- matches one measured case:
     the session's compaction removed context from view, but the raw record
     (91,391,690 bytes, 2026-09-06 onward, 2,356 owner messages) survived on disk.
Grade (claim-grade): the institutional "translation" is an analogy (correspondence),
not a consequence of thermodynamics; real institutional costs are engineering and
attention costs, ~10^12+ times larger than the Landauer floor, so the floor never binds.
"""
import math

K_B = 1.380649e-23          # J/K, exact (SI 2019)
T = 300.0                   # K, room temperature
E_BIT = K_B * T * math.log(2)

assert abs(E_BIT - 2.871e-21) < 1e-24, E_BIT
TB_BITS = 8 * 10**12
E_TB = E_BIT * TB_BITS
assert 2.2e-8 < E_TB < 2.4e-8, E_TB
# linear: doubling the bits erased doubles the floor exactly
assert math.isclose(E_BIT * 2 * TB_BITS, 2 * E_TB)

if __name__ == "__main__":
    print(f"Landauer floor at {T:.0f} K: {E_BIT:.3e} J per bit")
    print(f"erase 1 TB: {E_TB:.2e} J  (linear in bits; no non-linearity from Landauer)")
    print("L1 correct, L2 computed, L3 unsupported, L4 correct, L5 not established, L6 matches one case")

# CLASS: AUDIT
"""
Ledger of the eight self-flagged files reported by tools/build_index.py --dupes
(owner, 2026-10-05: "clear this matter up ... looking through the entire body of
work for the answer"). Each was read in its own file and re-checked.

CLEARED
  1. audit_leibniz_row37 -- Thread 2 (Collatz on twin centres) reproduced in
     thread2_collatz_twin_centres.py: 3077 trunk with no twin enrichment, v_3 = 3
     elongation not present beyond the multiples-of-6 baseline, the odd-step mean
     depends on range. One correction to the 2026-09-26 source text (108's run is
     113 steps, max 9232, through 3077).
  5. smith_normal_form_z26 -- "Theorem 9" (kernel dim 5) re-labelled REFUTED: the
     file's own run shows the stated construction has no zero eigenvalue.
  6. T193 -- carried no open claim of its own, only a pointer; reworded, and its
     stale "Hejhal is not here" corrected.
  3. hejhal_maass_level1 -- its own computation passes (level-1 r_1 = 9.53369526135
     located, parity separation); it was flagged only for quoting the Selberg
     file's flags. Reworded.
  8. twin_prime_saturation -- the heuristic N* ~ 3.5x10^7 replaced by the exact
     value 43,068,437 (checked below; the heuristic was low). The 30M certified
     figures re-derived below by a full sieve. The file also had a SyntaxError
     (backslash inside an f-string) and had never run on Python 3.11; fixed.

STILL OPEN, residual stated exactly
  4. selberg_maass_montgomery -- Gamma_0(4) eigenvalues r_j and their GUE fit.
     One-cusp Hejhal exists; Gamma_0(4) has three cusps and needs Stromberg's
     block extension, not written. LMFDB serves only squarefree levels, and 4 is
     not squarefree. Clearing it means writing the three-cusp solver.
  2. audit_manifest_hashes ... C1 and 7. torus787_clusters ... C1 -- the 13,480
     STM coordinates were never supplied; nothing in the repository holds them.
     Clearing them needs that data file.

FALSIFICATION: any assertion below failing.
"""
import subprocess
import sys
import pathlib
import numpy as np
from sympy import isprime

ROOT = pathlib.Path(__file__).resolve().parents[2]

N = 30_000_000
sv = np.ones(N + 3, dtype=bool)
sv[:2] = False
for i in range(2, int((N + 2) ** 0.5) + 1):
    if sv[i]:
        sv[i * i::i] = False
tw = np.nonzero(sv[:N + 1] & sv[2:N + 3])[0]
M = 59049
dr = 1 + (tw - 1) % 9
gaps = {}
for t, d in (("A", 2), ("B", 5), ("C", 8)):
    filled = set((tw[dr == d] % M).tolist())
    gaps[t] = sorted(set(range(d, M, 9)) - filled)
assert gaps == {"A": [], "B": [31640, 43439], "C": [21716, 41345]}

FIRST = {}
for r in (31640, 43439, 21716, 41345):
    m = 0
    while not (isprime(r + M * m) and isprime(r + M * m + 2)):
        m += 1
    FIRST[r] = r + M * m
assert FIRST == {31640: 33158129, 43439: 35472839, 21716: 43068437, 41345: 31219217}
assert max(FIRST.values()) == 43068437 and min(FIRST.values()) > N

out = subprocess.run([sys.executable, str(ROOT / "tools/build_index.py"), "--dupes"],
                     capture_output=True, text=True, cwd=ROOT).stdout
line = [l for l in out.splitlines() if "self-flagged" in l][0]
assert "(3)" in line and "selberg_maass_montgomery" in line
assert "audit_manifest_hashes_supplied_audit_2026_10_04" in line and "torus787_clusters_supplied_audit_2026_10_04" in line

if __name__ == "__main__":
    print("ledger checks pass; open flags:", line.split(":", 1)[1].strip())

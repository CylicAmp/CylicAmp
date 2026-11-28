# CLASS: AUDIT
"""
The owner's Egor calculations on permanents and determinants of 3 x 3 digit grids (2026-11-28), relayed with another
tool's write-up. Audit on arrival. Every number RIGHT (re-run in math/permanent_mod9/reproduce.py, which this file runs):

  1 2 3 / 4 5 6 / 7 8 9: per 450, det 0, odd-permutation sum 225
  swap 2<->5: 594, 54, 270;   swap 7<->8: 459, -9, 234;   both: 612, 72, 270;   all four have per = det by 9
  interaction 72 - 54 - (-9) + 0 = 27; the single swaps give determinants of opposite sign (54, -9)
  the criterion A_ij = u_i + 3 v_j (u_i the three classes by 3): per = det by 9 iff v1 + v2 + v3 = 0 by 3 -- the proof
    in the write-up is right (written out in math/permanent_mod9/note.tex) and a check of 118,098 matrices finds no
    exception; the standard grid is the transpose of u = (1, 2, 3), v = (0, 1, 2).
ADDED (connection to the owner's flips, all_flips_123_456_789_2026_10_19.py): reversing rows keeps det = 0 (every row
  evenly spaced) and gives per 450, 478, 490, 502; per = det by 9 only for no flip and all three flips, otherwise the
  remainder is 1, 4 or 7.
BACKGROUND in the write-up (no number of the owner's depends on it): claimed proofs of Valiant's conjecture from Anthropic
  (posted 2026-11-23, Lean) and OpenAI, reported in the press as not yet peer reviewed; they concern circuit size for the
  permanent family, not fixed matrices.
Note and reproduction: math/permanent_mod9/ (note.tex, note.pdf, reproduce.py, plain Python 3).

FALSIFICATION: any assertion failing.
"""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parents[1] / "permanent_mod9"
run = subprocess.run([sys.executable, str(HERE / "reproduce.py")], capture_output=True, text=True)
assert run.returncode == 0 and "ALL PASS" in run.stdout and "FAIL " not in run.stdout, run.stdout
assert (HERE / "note.tex").exists() and (HERE / "note.pdf").exists()
assert (pathlib.Path(__file__).resolve().parent / "all_flips_123_456_789_2026_10_19.py").exists()

if __name__ == "__main__":
    print(run.stdout.strip().splitlines()[-1], "-- per/det swaps, mod-9 criterion, row flips")

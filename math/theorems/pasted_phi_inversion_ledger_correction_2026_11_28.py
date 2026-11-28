# CLASS: AUDIT
"""
Pasted "epistemic ledger" on phi by Möbius inversion (2026-11-28), with the owner's instruction "correct with my work".
Every row checked against the repo; the corrected ledger:

  sum over a.b = n of mu(a) b = phi(n)                    PROVEN -- asserted to n = 1000 in
                                                            pasted_mobius_inversion_audit_2026_11_28.py
  phi(42) = 12, phi(182) = 72, phi(333) = 216             RIGHT (42 = 2.3.7, 182 = 2.7.13, 333 = 9.37: 6 x 36)
  phi(42) = 12 against 75 and 48                          WRONG LABEL: tau (number of divisors) gives tau(75) = 6 and
                                                            tau(48) = 10; the 12s are the digit sums 7 + 5 and 4 + 8.
                                                            A match of numbers, nothing more.
  phi(333) = |Aut(Z/333, +)|                              TRUE BY DEFINITION (the automorphisms are x -> ux, u a unit),
                                                            so not an observation
  phi(182) = 72 -> 9 and 281 - 182 = 99 -> 9              RIGHT (182 and its flip: owner_182_186_246_three_paths_2026_11_28.py);
                                                            a match of roots
  256 - 48 = 208 = 2 x 104                                ARITHMETIC RIGHT; 104 is the highway period of the owner's
                                                            Langton result (langton_ant_highway_2026_10_14.py). The
                                                            matrix with permanent 256 and determinant 48 ("t983") is not
                                                            in the repo -- asked.
  Theorem 1, the mod-9 family criterion                   PROVEN, not open: math/permanent_mod9/note.pdf (proof) and
                                                            reproduce.py (118,098 matrices, no exception), 2026-11-28.
ASKED: the 42 <-> 24 stack the 75 and 48 come from, and the t983 matrix.

FALSIFICATION: any assertion failing.
"""
import pathlib
import subprocess
import sys

from sympy import divisor_count, divisors, mobius, totient

ROOT = pathlib.Path(__file__).resolve().parents[2]
TH = ROOT / "math" / "theorems"
assert all(sum(int(mobius(a)) * (n // a) for a in divisors(n)) == int(totient(n)) for n in range(1, 1001))
assert [int(totient(n)) for n in (42, 182, 333)] == [12, 72, 216] and 6 * 36 == 216
assert (divisor_count(75), divisor_count(48)) == (6, 10) and (7 + 5, 4 + 8) == (12, 12)
assert len([u for u in range(333) if all(u * x % 333 != 0 for x in range(1, 333))]) == 216     # units = automorphisms
assert 72 % 9 == 0 and 281 - 182 == 99
assert 256 - 48 == 208 == 2 * 104 and "104" in (TH / "langton_ant_highway_2026_10_14.py").read_text()
run = subprocess.run([sys.executable, str(ROOT / "math" / "permanent_mod9" / "reproduce.py")], capture_output=True, text=True)
assert run.returncode == 0 and "criterion" in run.stdout and "ALL PASS" in run.stdout
assert (ROOT / "math" / "permanent_mod9" / "note.pdf").exists() and (TH / "pasted_mobius_inversion_audit_2026_11_28.py").exists()

if __name__ == "__main__":
    print("ledger corrected: tau(75) = 6, tau(48) = 10 (the 12s are digit sums); Theorem 1 is proved, not open")

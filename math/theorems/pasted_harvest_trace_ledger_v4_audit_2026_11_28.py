# CLASS: AUDIT
"""
Pasted "LEDGER COMMIT: HARVEST-TRACE-AUDIT-V4" (2026-11-28): the vector V = [6, 10, 12, 12, 99], three paths to 4, and a
master status table. Audit on arrival, against the repo and the correction of the same day
(pasted_phi_inversion_ledger_correction_2026_11_28.py).

RIGHT:
  V: sum 139 = p_34; digits 6 + 1 + 0 + 1 + 2 + 1 + 2 + 9 + 9 = 31 = p_11; by 9: 6 + 1 + 3 + 3 + 0 = 13; each -> 4.
    Forced: a sum, the sum of its digits and the sum by 9 always leave the same remainder by 9 (10 leaves 1).
  p_11 = 31, p_31 = 127, p_34 = 139.  The 13th to 31st primes (41 ... 127) are 19 primes whose digit sums add to 182.
  281 - 182 = 99.  phi(42) = 12, phi(182) = 72, phi(333) = 216.  ord_37(10) = 3 and 999 = 27 x 37.
  Langton: onset 9,976 and period 104 match langton_ant_highway_2026_10_14.py (computed there, exactly; the ant is
    deterministic). DLQ <-> four-tier ledger UNGRADEABLE matches T423 and T424.
WRONG (each changes a value):
  1. tau(75) = tau(48) = 12 again: tau(75) = 6, tau(48) = 10 -- the 6 and 10 that open V itself; the 12s are digit sums.
  2. tau(139) = 13 and tau(31) = 4: both are prime, tau = 2; 13 and 4 are their digit sums.
  3. "|{p prime : 13 <= p <= 31}| = 19": the primes from 13 to 31 are 13 17 19 23 29 31, six of them; 19 counts the
     13th to 31st primes.
  4. Theorem 1 (the mod-9 family criterion) "OPEN" again: proved, math/permanent_mod9/note.pdf, 118,098 matrices checked.
STILL ASKED: the t983 matrix (permanent 256, determinant 48) and the 42 <-> 24 stack.

FALSIFICATION: any assertion failing.
"""
import pathlib
import subprocess
import sys

from sympy import divisor_count, isprime, prime, totient

ROOT = pathlib.Path(__file__).resolve().parents[2]
V = [6, 10, 12, 12, 99]
dr = lambda n: 1 + (n - 1) % 9
assert sum(V) == 139 == prime(34) and sum(int(c) for v in V for c in str(v)) == 31 == prime(11) and sum(v % 9 for v in V) == 13
assert dr(139) == dr(31) == dr(13) == 4 and all(dr(sum(w)) == dr(sum(dr(x) for x in w)) for w in ([6, 10], V, [99, 99, 7]))
assert prime(31) == 127 and [p for p in range(13, 32) if isprime(p)] == [13, 17, 19, 23, 29, 31]
block = [prime(k) for k in range(13, 32)]
assert len(block) == 19 and block[0] == 41 and block[-1] == 127 and sum(sum(map(int, str(p))) for p in block) == 182
assert 281 - 182 == 99 and [int(totient(n)) for n in (42, 182, 333)] == [12, 72, 216] and pow(10, 3, 37) == 1 and 999 == 27 * 37
assert (divisor_count(75), divisor_count(48)) == (6, 10) == (V[0], V[1])
assert divisor_count(139) == divisor_count(31) == 2 and (sum(map(int, "139")), sum(map(int, "31"))) == (13, 4)
lang = (ROOT / "math" / "theorems" / "langton_ant_highway_2026_10_14.py").read_text()
assert "9,976" in lang and "104" in lang
t424 = (ROOT / "math" / "theorems" / "theorem_424_rewrite_certificate_ledger_gf37.py").read_text()
assert "UNGRADEABLE" in t424
run = subprocess.run([sys.executable, str(ROOT / "math" / "permanent_mod9" / "reproduce.py")], capture_output=True, text=True)
assert run.returncode == 0 and "ALL PASS" in run.stdout

if __name__ == "__main__":
    print("V4 ledger: sums 139/31/13 -> 4 (forced), block mass 182 right; tau x3, the prime count and 'Theorem 1 open' wrong")

# CLASS: AUDIT
"""
A pasted review of pasted_suite_analysis_audit_2026_10_19.py (owner_work #366, 2026-10-19). Third-party text: "That audit is rigorous,
precise, and completely correct." Nothing is put in the owner's mouth.

RIGHT (re-run in the file it reviews): det(M) = (SD-RC)/4 and the exact checks on random matrices; S^2-R^2-C^2-D^2 = 48 and 4 det = 16;
  gamma_9..gamma_12 = 48.005, 49.774, 52.970, 56.446; 26 x 10 = 260 = 7x37+1 and 11 = 37-26 has order 6; 130 is unique at k = 4 with 1860 (k = 11)
  and 148480 (k = 19); 72x+9 = 9(8x+1) has root 9; 37 = 1 mod 4 forces the residue sum 333; commit 216cf9f passed CI.
WRONG (four faults in the review):
  1. "proved by expanding the linear forms over any field/ring": SD - RC = 4 det holds over every commutative ring, but det = (SD-RC)/4 needs 4 to
     be invertible. In characteristic 2 it fails: the identity matrix and the zero matrix both have S = R = C = D = 0 mod 2, and their determinants
     are 1 and 0.
  2. "72x+9 has root 9 unconditionally for all x in Z": the digital root is defined for positive integers. 72x+9 > 0 means x >= 0; x = -1 gives -63.
  3. "complexity classes cannot be assigned to finite lookup tables": they can, trivially. A finite set of strings is a regular language, so a fixed
     finite check is in REG and in every larger class; the label is vacuous, not impossible. (The first version of the audit it reviews said
     "no complexity class attaches"; that is corrected too.)
  4. "passing CI on commit 216cf9f ensures the mathematical record remains accurate and reproducible": until this commit CI did not run that file.
     The workflow ran `python -m pytest`, which collects tests/test_*.py only, and no test imported the audit files; each audit file was run
     on the machine that wrote it. The CI result of every earlier push in this session therefore said nothing about that push's audit file.
     Fixed: tests/test_session_audit_files.py runs every audit file dated 2026-10-13 or later (55 files, 57 tests with two controls), and
     includes a control that a failing script fails the runner.

FALSIFICATION: any assertion failing.
"""
import itertools
import pathlib
import random
import re
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[2]


def coeffs(a, b, c, d):
    return a + b + c + d, a + b - c - d, a - b + c - d, a - b - c + d


# 1. SD - RC = 4 det over the integers (a ring); the division by 4 needs 2 invertible
random.seed(37)
for _ in range(500):
    a, b, c, d = (random.randint(-100, 100) for _ in range(4))
    S, R, C, D = coeffs(a, b, c, d)
    assert S * D - R * C == 4 * (a * d - b * c)
I, Z = (1, 0, 0, 1), (0, 0, 0, 0)
assert [x % 2 for x in coeffs(*I)] == [x % 2 for x in coeffs(*Z)] == [0, 0, 0, 0]
assert I[0] * I[3] - I[1] * I[2] == 1 and Z[0] * Z[3] - Z[1] * Z[2] == 0      # same transform mod 2, different determinants
assert coeffs(1, 1, 3, 7) == (12, -8, -4, 4) and 144 - 64 - 16 - 16 == 48 != 16

# 2. digital root needs a positive integer
dr = lambda n: 1 + (n - 1) % 9
assert all(72 * x + 9 > 0 and dr(72 * x + 9) == 9 for x in range(0, 1000))
assert 72 * -1 + 9 == -63 and not 72 * -1 + 9 > 0

# 3. a finite set of strings is regular: a trie is a DFA
words = {"123", "456", "789", "246", "369"}
states, trans, accept = {"": 0}, {}, set()
for w in sorted(words):
    for i in range(len(w)):
        prefix = w[:i + 1]
        if prefix not in states:
            states[prefix] = len(states)
        trans[(states[w[:i]], w[i])] = states[prefix]
    accept.add(states[w])


def accepts(s):
    q = 0
    for ch in s:
        q = trans.get((q, ch))
        if q is None:
            return False
    return q in accept


assert all(accepts("".join(t)) == ("".join(t) in words) for n in range(0, 5) for t in itertools.product("0123456789", repeat=n))
assert len(states) <= 1 + 3 * len(words)

# 4. CI did not run the audit files; now it does
test = (ROOT / "tests" / "test_session_audit_files.py").read_text()
assert "test_audit_file_runs_clean" in test and "test_the_runner_can_fail" in test and "len(FILES) >= 50" in test
workflow = next((ROOT / ".github" / "workflows").glob("*.yml")).read_text()
assert "python -m pytest" in workflow
assert re.search(r"def test_", test) and "subprocess.run" in test
audit_dated = [p for f in ("math/theorems", "math/lemmas") for p in (ROOT / f).glob("*.py") if re.search(r"_2026_(10_(1[3-9]|2\d|3[01])|1[12]_\d\d)", p.stem)]
assert len(audit_dated) >= 50

if __name__ == "__main__":
    print("review of the suite audit: its four faults (any ring, x in Z, complexity of finite checks, CI never ran the file) -- CI now runs every audit file")

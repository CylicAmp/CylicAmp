# CLASS: AUDIT
"""
Pasted status from another tool (2026-11-28): a Lemma 1-9 traceability table added to the owner's page "Egor Algorithm --
Logic, Rules, and Tests"; Lemma 5 recorded two ways (the 7 + 10 = 17 bridge of the earlier handoff, and a newer
inventory that links Lemma 5 to the 12-phalanx count); the orbit Orb_2(7): its listed 12 terms are a prefix, and by 37
the full orbit has period 36. Audit on arrival.

IN THIS REPO (found by grep before writing):
  pasted_v6_ledger_lemmas_audit_2026_11_17.py -- Lemmas 1-8 of the ledger, with L5: 7 + 10 = 17 prime, pi(17) = 7,
    17 -> 8, 7 + 8 = 15;  pasted_ledger_lemmas_10_12_audit_2026_11_17.py -- Lemmas 10-12, which use Lemma 5's map 7 -> 8;
  pasted_unified_handoff_ledger_audit_2026_11_17.py -- the handoff ledger.
  The page itself, the newer inventory and the 12-phalanx count are not in the repo, Google Drive or the old message
  record (searched 2026-11-28).
RIGHT:
  Orb_2(7) by 37: 7, 14, 28, 19, 1, 2, 4, 8, 16, 32, 27, 17, ... -- 2 has order 36 by 37 (2 is a primitive root), so the
    orbit runs through all 36 nonzero classes before it returns to 7, and any 12 listed terms are a prefix.
    7 = 2^32 by 37, so the orbit reaches 1 at the fifth term (7 x 16 = 112 = 3 x 37 + 1).
  Lemma 5 as in the repo: 7 + 10 = 17, prime, pi(17) = 7, 1 + 7 = 8, 7 + 8 = 15.
ASKED (each blocks a check): the page's Lemma 1-9 table and the newer inventory's Lemma 5 line with the 12-phalanx count
  (to set the two versions side by side); the 12 orbit terms as the page lists them (to check they are this prefix).

FALSIFICATION: any assertion failing.
"""
import pathlib

from sympy import isprime, n_order, primepi

TH = pathlib.Path(__file__).resolve().parent
orbit = [7 * pow(2, k, 37) % 37 for k in range(36)]
assert orbit[:12] == [7, 14, 28, 19, 1, 2, 4, 8, 16, 32, 27, 17]
assert n_order(2, 37) == 36 and sorted(orbit) == list(range(1, 37)) and 7 * pow(2, 36, 37) % 37 == 7
assert pow(2, 32, 37) == 7 and 7 * 16 == 112 == 3 * 37 + 1 and orbit.index(1) == 4
assert 7 + 10 == 17 and isprime(17) and primepi(17) == 7 and 1 + 7 == 8 and 7 + 8 == 15
for f in ("pasted_v6_ledger_lemmas_audit_2026_11_17.py", "pasted_ledger_lemmas_10_12_audit_2026_11_17.py",
          "pasted_unified_handoff_ledger_audit_2026_11_17.py"):
    assert (TH / f).exists(), f

if __name__ == "__main__":
    print("Orb_2(7) by 37: period 36, the 12 terms a prefix (right); Lemma 5 in the repo = 7 + 10 = 17; phalanx line asked")

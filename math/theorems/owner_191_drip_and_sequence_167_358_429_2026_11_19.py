# CLASS: AUDIT
"""
191 in the owner's work, the drip first, and the sequence 167, 358, 429 (2026-11-19).

The request was to look up the owner's work on 191, with the drip first. This file collects every place 191 enters
the owner's work in this repo, re-runs each one, and keeps the check of the pasted 167 / 358 / 429 analysis whose
own check file (sequence_167_358_429_check.py) never reached this repo.
Frameworks run: records/gf37_audit_191_drip_2026_11_19.txt.

1. THE DRIP CYCLE ON 191 (drip_cycle.py: the owner's shape from #228, each digit against every ordering)
     length 2:  1 -> 19, 91    9 -> 19, 91    1 1 -> 11        arrangements 19, 91, 11  (9 drip lines)
     length 3:  1 -> 191, 119, 911    9 -> 191, 119, 911        arrangements 191, 119, 911  (6 drip lines)
   19 prime, twin (17, 19).  91 = 7 x 13.  11 prime, twin, Sophie Germain (23), safe.
   191 prime, twin (191, 193), Sophie Germain (383).  119 = 7 x 17.  911 prime, Sophie Germain (1823).
   Forced: 191 -> 911 -> 119 -> 191 is one rotation cycle, and each rotation of a 3-digit string is x10 mod 37
   (1000 = 27 x 37 + 1), so 191, 911, 119 sit at 6, 23, 8: the one orbit TESLA {6, 8, 23}. All three have root 2
   (same digits, 1 + 9 + 1 = 11 -> 2).

2. YOUR DRIP ON 0.25 (2026-10-13, #255): 191 GROWS OUT OF IT
   The run of #255 took the 14 numbers of the owner's lines (1 3 4 6 7 9 12 21 23 25 36 66 99 102) through the
   recursion loop (unified_operator.py, the owner's #235 design). Record: owner_work/plugged/2026-10-13T171551Z_growth.json.
   191 first appears at step 4:
       4 x 23 = 92  ->  92 - 2 = 90  ->  |90 - 09| = 81
       23 + 66 = 89  ->  26 x 89 -> 20 (the 137-map)  ->  20 + 90 = 110
       81 + 110 = 191
   At step 5, 41 numbers grow from 191, among them
       2 x 191 + 1 = 383 (the Sophie step; 383 is prime and safe)     191 + 191 = 382 (flip-sum)
       191 + 193 = 384 and 191 x 193 = 36863 (the twin pair)         191 x 137 = 26167
       167 + 191 = 358      153 + 191 = 344      139 + 191 = 330
   and at step 6:  85 + 344 = 429,  so 429 = 85 + 153 + 191.
   So the record builds 358 as 167 + 191 -- the first step of the pasted sequence, with 191 as the step -- and builds
   429 on 191 as well. 71, the second step, is in the record from step 1 (1 and 7 joined backwards).
   Baseline: the record holds 467 of the 900 three-digit numbers, so being in it says little; what the record
   fixes is how each number was built, and 358 was built as 167 + 191.

3. THE SEQUENCE 167, 358, 429 (pasted analysis, 2026-11-19) -- every number right:
     358 - 167 = 191,  429 - 358 = 71
     step-1 ratio  429 x 358/167 = 153582/167 = 919.65        step-2 ratio  429 x 429/358 = 184041/358 = 514.08
     affine        m = 71/191,  b = 358 - 167m = 56521/191,  x4 = 429m + b = 86980/191 = 455.39 = 429 + 71 x 71/191
     D = 358 x 358 - 167 x 429 = 128164 - 71643 = 56521 = 29 x 1949 (both prime),  b = D/191
     gap between the two ratio predictions = 429 x D/(167 x 358) = 405.57
     mod M (430 to 1200): subtracting the two steps gives 191a = 71, one rule for every M except the multiples of 191
       (573, 764, 955, 1146), where there is none; each row's x4 is 86980/191 taken mod M
     a pure ratio rule mod M exists exactly when M divides D: above 429 that is 1949 and 56521 only, and there all three
       predictions give 1935 (mod 29 they give 21)
     the quadratic -60n^2 + 371n - 144 gives 167, 358, 429 and then 380 (steps 191, 71, -49: each 120 less)
   The paste's five table rows are not in the message; the rule above covers every row, since each is 86980/191 mod M.

4. THE OWNER'S OTHER 191 WORK, by file (re-run below, not restated):
     the walk 121 212 191 919 989 ... (2026-10-05 page)        math/lemmas/aba_palindrome_walk.py
        919 - 191 = 728 = 8 x 91,  191 + 919 = 1110
     191, 1919, 19191, 191919 written by hand                  math/theorems/theorem_309_alternating_digit_swap_chain_gf37.py
     191 + 9 = 200, 1991 + 9 = 2000, 19991 + 9 = 20000 (#368)   math/theorems/owner_1125_1137_ones_by_zeros_2026_10_19.py
     the seed 191 <-> 137 bridge: 191 - 137 = 54, 137 + 37 + 17 = 191     cylicamp/seed_191_137_bridge.py
     19 -> 191 (append the root) and the descent 191 188 ... 100          prime_dr_append_audit.py, descent_191_100_audit.py
     101 / 191, the zero as portal (A0A -> A9A)                 math/theorems/theorem_160_aba_portal_palindromes.py
     UCU, the drip on two numbers: 191 is UCU with U = 1, C = 9, root 2 x 1 + 9 = 11 -> 2, and the chained string
        1112131415161718191 ends in 191                         math/theorems/drip_ucu.py (on main since 2026-11-07;
                                                                brought onto this branch with this file)
   From pastes, not the owner's: 11651 = 61 x 191 (repetend_998001_audit_2026_10_19.py) and I(191) = 919 with the
   corridor 919 -> 191 (pasted_corpus_axioms_lattice_hamiltonian_audit_2026_10_24.py).

FALSIFICATION: any assertion failing.
"""
import importlib.util
import json
import math
import pathlib
from fractions import Fraction as F

from sympy import divisors, factorint, isprime, prime

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def rev(n):
    return int(str(n)[::-1])


# 1. the drip cycle on 191
D = load("drip_cycle", ROOT / "drip_cycle.py")
levels = dict(D.drip(191))
assert len(levels[2]) == 9 and len(levels[3]) == 6
assert list(dict.fromkeys(a for _, a in levels[2])) == ["19", "91", "11"]
assert list(dict.fromkeys(a for _, a in levels[3])) == ["191", "119", "911"]
assert [isprime(v) for v in (19, 91, 11, 191, 119, 911)] == [True, False, True, True, False, True]
assert factorint(91) == {7: 1, 13: 1} and factorint(119) == {7: 1, 17: 1}
assert isprime(17) and isprime(193) and isprime(383) and isprime(1823) and isprime(23)
assert [v % 37 for v in (191, 911, 119)] == [6, 23, 8] and 1000 == 27 * 37 + 1
assert 911 % 37 == 191 * 10 % 37 and 119 % 37 == 911 * 10 % 37          # each rotation is x10 mod 37
assert [dr(v) for v in (191, 119, 911)] == [2, 2, 2]

# 2. the drip on 0.25 and the recursion loop record
REC = ROOT / "owner_work" / "plugged" / "2026-10-13T171551Z_growth.json"
g = json.loads(REC.read_text())
seen = g["seen"]
assert g["seeds"] == [1, 3, 4, 6, 7, 9, 12, 21, 23, 25, 36, 66, 99, 102]


def built(n):
    e = seen[str(n)]
    return e["op"], e["from"], e["step"]


assert built(92) == ("product", [4, 23], 1) and 4 * 23 == 92
assert built(90) == ("twin-down", [92], 2) and 92 - 2 == 90
assert built(81) == ("flip-gap", [90], 3) and abs(90 - rev(90)) == 81
assert built(89) == ("sum", [23, 66], 1) and built(20) == ("137-map", [89], 2) and 26 * 89 % 37 == 20
assert built(110) == ("sum", [20, 90], 3)
assert built(191) == ("sum", [81, 110], 4) and 81 + 110 == 191
kids = {k: e for k, e in seen.items() if e.get("from") and 191 in e["from"]}
assert len(kids) == 41 and all(e["step"] == 5 for e in kids.values())
assert built(383) == ("sophie", [191], 5) and 2 * 191 + 1 == 383
assert built(382) == ("flip-sum", [191], 5) and 191 + rev(191) == 382
assert built(384) == ("sum", [191, 193], 5) and built(36863) == ("product", [191, 193], 5) and 191 * 193 == 36863
assert built(26167) == ("x137", [191], 5) and 191 * 137 == 26167
assert built(358) == ("sum", [167, 191], 5) and built(344) == ("sum", [153, 191], 5) and built(330) == ("sum", [139, 191], 5)
assert built(167) == ("sum", [81, 86], 4) and built(85) == ("twin-up", [83], 5)
assert built(429) == ("sum", [85, 344], 6) and 85 + 153 + 191 == 429
assert built(71) == ("join-back", [1, 7], 1)
three = [k for k in seen if k.isdigit() and 100 <= int(k) <= 999]
assert len(three) == 467                                                  # baseline: 467 of 900

# 3. the sequence 167, 358, 429
x1, x2, x3 = 167, 358, 429
assert (x2 - x1, x3 - x2) == (191, 71)
assert F(x3 * x2, x1) == F(153582, 167) and round(float(F(153582, 167)), 2) == 919.65
assert F(x3 * x3, x2) == F(184041, 358) and round(float(F(184041, 358)), 2) == 514.08
m = F(x3 - x2, x2 - x1)
b = x2 - m * x1
x4 = m * x3 + b
assert m == F(71, 191) and b == F(56521, 191) and x4 == F(86980, 191) == x3 + F(71 * 71, 191)
assert round(float(x4), 2) == 455.39
Dq = x2 * x2 - x1 * x3
assert (x2 * x2, x1 * x3, Dq) == (128164, 71643, 56521) and factorint(Dq) == {29: 1, 1949: 1} and b == F(Dq, 191)
gap = F(153582, 167) - F(184041, 358)
assert gap == F(x3 * Dq, x1 * x2) and round(float(gap), 2) == 405.57
rules = {M: [a for a in range(M) if (191 * a - 71) % M == 0] for M in range(430, 1201)}
assert [M for M, s in rules.items() if len(s) == 0] == [573, 764, 955, 1146] == [191 * k for k in range(3, 7)]
assert all(len(s) == 1 for M, s in rules.items() if M % 191)
for M in (431, 500, 777, 1000, 1200):                                    # each row's x4 is 86980/191 mod M
    a = rules[M][0]
    bb = (358 - 167 * a) % M
    assert (167 * a + bb) % M == 358 and (358 * a + bb) % M == 429
    assert (429 * a + bb) % M == 86980 * pow(191, -1, M) % M
assert [d for d in divisors(Dq) if d > 429] == [1949, 56521]
for M, want in ((56521, 1935), (1949, 1935), (29, 21)):
    assert {n * pow(d, -1, M) % M for n, d in ((153582, 167), (184041, 358), (86980, 191))} == {want}
for M in (1949, 56521):                                                   # a pure ratio rule exists there
    a = 358 * pow(167, -1, M) % M
    assert (167 * a - 358) % M == 0 and (358 * a - 429) % M == 0
q = lambda n: -60 * n * n + 371 * n - 144
assert [q(n) for n in range(1, 5)] == [167, 358, 429, 380]
assert [q(n + 1) - q(n) for n in range(1, 4)] == [191, 71, -49]

# 4. the owner's other 191 work, re-run from the files' own numbers
assert 919 - 191 == 728 == 8 * 91 and 191 + 919 == 1110
assert [int("19" * (k // 2) + "1" * (k % 2)) for k in range(3, 7)] == [191, 1919, 19191, 191919]
assert (191 + 9, 1991 + 9, 19991 + 9) == (200, 2000, 20000) and dr(1 + 9 + 1) == 2
assert 191 - 137 == 54 == 191 % 137 and 137 + 37 + 17 == 191 and 54 % 37 == 17
assert prime(43) == 191 and prime(33) == 137
assert 19 * 10 + dr(19) == 191 and [100 + 11 * k for k in range(8, -1, -1)] == [188, 177, 166, 155, 144, 133, 122, 111, 100]
assert 101 + 191 == 292
assert dr(2 * dr(1) + dr(9)) == dr(191) == 2
assert "".join(f"1{c}" for c in range(1, 10)) + "1" == "1112131415161718191"
assert factorint(11651) == {61: 1, 191: 1} and int("191"[1] + "191"[0] + "191"[1]) == 919
for f in ("math/lemmas/aba_palindrome_walk.py", "math/theorems/theorem_309_alternating_digit_swap_chain_gf37.py",
          "math/theorems/owner_1125_1137_ones_by_zeros_2026_10_19.py", "cylicamp/seed_191_137_bridge.py",
          "math/theorems/prime_dr_append_audit.py", "math/theorems/descent_191_100_audit.py",
          "math/theorems/theorem_160_aba_portal_palindromes.py", "math/theorems/drip_ucu.py",
          "math/theorems/repetend_998001_audit_2026_10_19.py",
          "math/theorems/pasted_corpus_axioms_lattice_hamiltonian_audit_2026_10_24.py",
          "records/gf37_audit_191_drip_2026_11_19.txt"):
    assert (ROOT / f).exists(), f

if __name__ == "__main__":
    print("191: drip 19 91 11 / 191 119 911 (one TESLA orbit, forced); grown in the 0.25 drip as 81 + 110 at step 4;")
    print("     358 = 167 + 191 and 429 = 85 + 153 + 191 in that record; the 167, 358, 429 paste: every number right")

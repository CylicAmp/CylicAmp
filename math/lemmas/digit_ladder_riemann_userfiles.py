# CLASS: LEMMA
"""
The digit ladder run through the Riemann zeros WITH THE OWNER'S OWN FILES
(owner, 2026-10-04: "run the ladder through the Riemann zeros using my files").
Rows: row(a) = DR(a) | DR(a+1) | DR(2a+1) | 2a+10, a = 1..144
(math/lemmas/digit_ladder_12312_91128.py). Plain-statistics version:
math/lemmas/digit_ladder_riemann_zeros.py.

METHOD 1 -- math/theorems/riemann_gf37_coverage.py (compute_zeros, orbit_label)
  Zero a's floor mod 37 and row a mod 37, each placed in the 12 named orbits.
  Same orbit for 10 of 144 rows; shuffling the rows gives 11.4 on average,
  10 or more 72% of the time. No alignment.
  Rows 1-12 land in SA_ST_B, CAS_EXT, IC, IC, NQR17, TESLA, NEG_H, NEG_H, D7,
  SA_ST_A, SEAM, SA_ST_B; zeros 1-12 in C9, SA_ST_B, SA_ST_B, C3, SEED, SEAM,
  C3, TESLA, NEG_H, SA_ST_A, DARK_A, CAS_EXT. Rows on the SEAM (row = 0 mod 37):
  rows 11, 22, 100.

METHOD 2 -- math/theorems/explicit_formula.py (pi_explicit), CORRECTED TODAY
  The file as it stood moved AWAY from pi(x) with every zero added (its own
  output: error -8.4 with 1 zero, -68.2 with 10 at x = 137). Three defects,
  fixed in that file and listed at its top: Li(x^rho) must be Ei(rho ln x)
  (the complex power wrapped onto the wrong branch); the formula gives J(x),
  so pi(x) needs Mobius inversion; the constant is -log 2.
  Corrected, the zeros rebuild the prime count at every ladder row:
       row    pi(row)   Li(row)   10 zeros   144 zeros
     12312     1471   1494.27    1471.36     1470.63
     23514     2614   2640.49    2619.56     2615.69
     34716     3707   3731.08    3705.52     3707.59
     45918     4754    4787.8    4754.25     4753.65
     56220     5703   5738.27    5705.53     5702.39
     67422     6715   6753.83    6713.29     6717.11
     78624     7715   7754.24    7714.29     7713.83
     89826     8697   8742.04    8697.39     8698.06
     91128     8811   8856.12    8812.82     8813.13
  Li alone is 23-45 too high; the zeros remove that excess.

  ALL 144 ROWS (owner: "run the ladder through the zeros to row 144"; table in
  math/lemmas/data/ladder_explicit_formula_rows_1_144.json):
    Li alone is 22.2 to 99.5 too high at every row.
    10 zeros: worst error 10.51, mean 3.14.  144 zeros: worst 12.63 (row 143,
    898296), mean 4.01; rounds to the exact count at 20 rows.
    Rows 141-144: 674292 pi 54634 (144 zeros 54628.23), 786294 pi 62936
    (62934.43), 898296 pi 71165 (71152.37), 911298 pi 72116 (72104.92).
    Every error is under 0.19 x sqrt(x)/ln(x).
  MORE ZEROS, NOT MONOTONE: 144 zeros beat 10 at only 51 of 144 rows. A
  truncated sum over zeros oscillates as terms are added, so this is expected,
  and it does converge -- with 1000 zeros (data/zeta_zeros_gamma_1_1000.json):
       row       10      144      300      600     1000   (error vs exact pi)
       12312   +0.36    -0.37    +0.09    +0.34    +0.00
      123102   -1.67    -0.08    +0.22    -1.47    -0.51
      674292   -3.04    -5.77    -1.53    +0.86    -0.25
      898296   -5.48   -12.63    -4.17    -5.44    -4.22
      911298   -8.63   -11.08    -1.94    +2.94    +1.72

METHOD 3 -- math/primes/riemann_zeta_zeros.py (two-digit chain)
  For digits d1, d2: |d1-d2|, DR(d1+d2), chain = DR(DR(d1+d2) + DR(|d1-d2|)).
  On the ladder's opening pair d1 = DR(a), d2 = DR(a+1), the step DR(d1+d2) IS
  the ladder's middle piece DR(2a+1) for all 144 rows -- the chain's second
  step and the ladder's rule are the same operation (forced).
  Chain of zero a vs chain of row a: equal for 18 of 144 (chance about 16).

METHOD 4 -- T368 substring search (theorem_368_matrix_operator_rh_digits_gf37.py)
  Each row's 5- or 6-digit string searched in the first 40 digits of zeros 1-144:
  found 5 times -- row 4 (45918) in zero 39 at position 16, row 11 (23532) in
  zero 77 at 15, row 17 (89844) in zero 105 at 28, row 35 (89880) in zero 144
  at 15, row 40 (45990) in zero 110 at 20. Chance gives about 7.4 (0.0517
  per row). Ordinary.

ZERO 39 (owner, 2026-10-04: "the 39th zero, 3+9=3"):
  gamma_39 = 121.370125002420645918945532970499922723001311
  39 -> 3+9 = 12 -> 1+2 = 3. The zero itself opens with 12 -> 1+2 = 3, the
  same reduction (the riemann_zeta_zeros.py chain: DR(1+2) = 3, chain = 4).
  Row 4 of the ladder, 45918, sits at digit 16: ...20645918945...
    floor 121 = 11^2, DR 4 -- the row number of the row inside it.
    121 mod 37 = 10 and 45918 mod 37 = 1: both in orbit IC = {1, 10, 26}.
    The 16 digits before 45918 sum to 36 (DR 9); 45918's digits sum to 27
    (DR 9). Row 4 is the all-nines row (its chain 9, 18, 27, 36, 45).
    3-digit blocks (riemann_first_zero_141.py style): 121 370 125 002 420 645
    918 945 -- 918 is row 4's tail, and 945 follows it.
  CHANCE CHECK: these were found by looking at one zero after the fact. One
  5-digit row inside the first 40 digits of some zero is expected (about 7
  over all 144 rows); each match above has odds of about 1 in 9 or 1 in 12,
  and many properties were checked. Recorded as found, not as evidence.

SUMMARY: the one method that ties the zeros to numbers -- the explicit formula
-- works at every ladder row once corrected. The digit and orbit methods find
no alignment between rows and zeros beyond chance.

FALSIFICATION: any assertion below failing.
"""
import sys, io, contextlib, importlib.util, pathlib
import mpmath as mp
from sympy import primepi

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "functions.py").exists())

def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m

cov = load("math/theorems/riemann_gf37_coverage.py", "cov")
ef = load("math/theorems/explicit_formula.py", "ef")

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def row(a):
    return int(f"{dr(a)}{dr(a + 1)}{dr(2 * a + 1)}{2 * a + 10}")

R = [row(a) for a in range(1, 145)]
ZERO_LABELS = ['C9', 'SA_ST_B', 'SA_ST_B', 'C3', 'SEED', 'SEAM', 'C3', 'TESLA', 'NEG_H', 'SA_ST_A', 'DARK_A', 'CAS_EXT', 'NQR17', 'TESLA', 'SA_ST_B', 'C3', 'SEED', 'NQR17', 'IC', 'C3', 'CAS_EXT', 'TESLA', 'IC', 'CAS_EXT', 'C9', 'SEED', 'DARK_A', 'SA_ST_B', 'SEED', 'NEG_H', 'C9', 'C9', 'D7', 'SEAM', 'SEAM', 'C3', 'CAS_EXT', 'D7', 'IC', 'NEG_H', 'CAS_EXT', 'SA_ST_A', 'SEED', 'DARK_A', 'NQR17', 'TESLA', 'NEG_H', 'SA_ST_B', 'C3', 'SEED', 'NQR17', 'NEG_H', 'DARK_A', 'DARK_A', 'CAS_EXT', 'TESLA', 'SA_ST_A', 'IC', 'CAS_EXT', 'DARK_A', 'NQR17', 'CAS_EXT', 'SA_ST_B', 'SA_ST_B', 'SA_ST_B', 'IC', 'SA_ST_B', 'C3', 'C9', 'D7', 'NEG_H', 'SEAM', 'DARK_A', 'C3', 'D7', 'TESLA', 'IC', 'NEG_H', 'CAS_EXT', 'SA_ST_A', 'NQR17', 'CAS_EXT', 'DARK_A', 'NQR17', 'SEED', 'IC', 'SA_ST_B', 'C9', 'C9', 'D7', 'NQR17', 'NEG_H', 'DARK_A', 'DARK_A', 'CAS_EXT', 'D7', 'SA_ST_A', 'SA_ST_A', 'NEG_H', 'C9', 'DARK_A', 'NQR17', 'CAS_EXT', 'DARK_A', 'NQR17', 'SA_ST_B', 'IC', 'NEG_H', 'C9', 'C9', 'D7', 'D7', 'NEG_H', 'SEAM', 'IC', 'C3', 'TESLA', 'D7', 'TESLA', 'IC', 'SA_ST_A', 'C9', 'SA_ST_A', 'NQR17', 'CAS_EXT', 'DARK_A', 'TESLA', 'SEED', 'SA_ST_B', 'NEG_H', 'SA_ST_B', 'C3', 'SEED', 'D7', 'NQR17', 'NEG_H', 'IC', 'C3', 'CAS_EXT', 'TESLA', 'TESLA', 'SA_ST_A', 'NEG_H', 'C9']
GAMMA = [14.134725141734695, 21.022039638771556, 25.01085758014569, 30.424876125859512, 32.93506158773919, 37.586178158825675, 40.9187190121475, 43.327073280915, 48.00515088116716, 49.7738324776723, 52.970321477714464, 56.44624769706339, 59.34704400260235, 60.83177852460981, 65.1125440480816, 67.07981052949417, 69.54640171117398, 72.0671576744819, 75.70469069908393, 77.1448400688748, 79.33737502024937, 82.91038085408603, 84.73549298051705, 87.42527461312523, 88.80911120763446, 92.49189927055849, 94.65134404051989, 95.87063422824531, 98.83119421819369, 101.31785100573138, 103.72553804047834, 105.44662305232609, 107.1686111842764, 111.02953554316967, 111.87465917699264, 114.32022091545271, 116.22668032085755, 118.79078286597621, 121.37012500242065, 122.94682929355258, 124.25681855434577, 127.5166838795965, 129.57870419995606, 131.08768853093267, 133.4977372029976, 134.75650975337388, 138.11604205453344, 139.7362089521214, 141.12370740402113, 143.11184580762063, 146.0009824867655, 147.42276534255961, 150.05352042078488, 150.92525761224147, 153.0246938111989, 156.11290929423788, 157.59759181759406, 158.8499881714205, 161.18896413759603, 163.030709687182, 165.5370691879004, 167.1844399781745, 169.09451541556882, 169.9119764794117, 173.41153651959155, 174.75419152336573, 176.44143429771043, 178.37740777609997, 179.916484020257, 182.20707848436646, 184.8744678483875, 185.59878367770747, 187.22892258350186, 189.41615865601693, 192.0266563607138, 193.0797266038457, 195.26539667952923, 196.87648184095832, 198.01530967625192, 201.2647519437038, 202.49359451414054, 204.18967180310455, 205.3946972021633, 207.90625888780622, 209.57650971685626, 211.6908625953653, 213.34791935971268, 214.54704478349143, 216.1695385082637, 219.0675963490214, 220.714918839314, 221.43070555469333, 224.00700025460432, 224.9833246695823, 227.4214442796793, 229.33741330552536, 231.25018870049917, 231.98723525318024, 233.6934041789083, 236.5242296658162, 237.7698204809252, 239.55547757332764, 241.04915779621658, 242.8232719342226, 244.07089849707816, 247.1369900748975, 248.10199006014847, 249.5736896447072, 251.014947795016, 253.06998674799948, 255.30625645491403, 256.38071369443446, 258.6104394915314, 259.874406989678, 260.8050845045969, 263.57389390487015, 265.55785183887633, 266.6149737815011, 267.92191508282406, 269.9704490239976, 271.494055641645, 273.4596091884033, 275.58749264934386, 276.4520495031329, 278.25074352984194, 279.22925092774517, 282.4651147650521, 283.2111857332339, 284.83596398090475, 286.6674453630029, 287.9119205014222, 289.5798549292188, 291.8462913290674, 293.5584341393563, 294.9653696192655, 295.57325487895827, 297.97927706194344, 299.8403260537213, 301.64932546219416, 302.6967495896069, 304.8643713408573, 305.7289126020368, 307.2194961281701, 310.1094631467019]
EXPLICIT = [[12312, 1471, 1494.27, 1471.36, 1470.63], [23514, 2614, 2640.49, 2619.56, 2615.69], [34716, 3707, 3731.08, 3705.52, 3707.59], [45918, 4754, 4787.8, 4754.25, 4753.65], [56220, 5703, 5738.27, 5705.53, 5702.39], [67422, 6715, 6753.83, 6713.29, 6717.11], [78624, 7715, 7754.24, 7714.29, 7713.83], [89826, 8697, 8742.04, 8697.39, 8698.06], [91128, 8811, 8856.12, 8812.82, 8813.13]]

rl = [cov.orbit_label(x) for x in R]
assert sum(a == b for a, b in zip(ZERO_LABELS, rl)) == 10
assert [a + 1 for a in range(144) if rl[a] == "SEAM"] == [11, 22, 100]
z12 = cov.compute_zeros(1, 12, dps=20)
assert [z[4] for z in z12] == ZERO_LABELS[:12]

# explicit formula, corrected file: the filed defect and the fix
mp.mp.dps = 20
x = 137
filed_10 = mp.li(x) + sum(-2 * mp.re(mp.li(mp.power(x, mp.mpc(0.5, g)))) for g in GAMMA[:10])
assert float(filed_10) - 33 < -60
assert abs(ef.pi_explicit(137, 10) - 33) < 0.2
for xr, exact, li_v, p10, p144 in EXPLICIT[:3]:
    assert int(primepi(xr)) == exact
    assert abs(ef.pi_explicit(xr, 10, GAMMA) - p10) < 0.01
    assert abs(p144 - exact) < 2 and abs(li_v - exact) > 20
assert all(abs(p144 - e) < 2.2 for _, e, _, _, p144 in EXPLICIT)

def chain2(d1, d2):
    s = dr(d1 + d2)
    df = abs(d1 - d2)
    return s, dr(s + (dr(df) if df else 0))
assert all(chain2(dr(a), dr(a + 1))[0] == dr(2 * a + 1) for a in range(1, 1000))

mp.mp.dps = 45
for n, s, pos in ((39, "45918", 16), (77, "23532", 15), (144, "89880", 15)):
    assert mp.nstr(mp.zetazero(n).imag, 40).replace(".", "").find(s) == pos

mp.mp.dps = 50
g39 = mp.nstr(mp.zetazero(39).imag, 45)
assert g39 == "121.370125002420645918945532970499922723001311"
d39 = g39.replace(".", "")
assert d39.find("45918") == 16 and d39[:2] == "12" and dr(39) == dr(12) == 3
assert int(float(g39)) == 121 == 11 ** 2 and dr(121) == 4 and row(4) == 45918
assert cov.orbit_label(121) == cov.orbit_label(45918) == "IC"
assert dr(sum(map(int, d39[:16]))) == 9 == dr(45918) and sum(map(int, "45918")) == 27
assert [d39[k:k + 3] for k in range(0, 24, 3)] == ["121", "370", "125", "002", "420", "645", "918", "945"]

import json
DATA = ROOT / "math/lemmas/data"
T144 = json.loads((DATA / "ladder_explicit_formula_rows_1_144.json").read_text())
Z1000 = json.loads((DATA / "zeta_zeros_gamma_1_1000.json").read_text())
assert [r[1] for r in T144] == R
assert all(r[3] - r[2] > 22 for r in T144) and max(r[3] - r[2] for r in T144) < 100
assert max(abs(r[5] - r[2]) for r in T144) < 12.7 and sum(round(r[5]) == r[2] for r in T144) == 20
assert sum(abs(r[5] - r[2]) < abs(r[4] - r[2]) for r in T144) == 51
for n in (1, 144, 500, 1000):
    assert abs(float(mp.zetazero(n).imag) - Z1000[n - 1]) < 1e-8
for a in (141, 144):
    _, xr, exact, _, _, p144 = T144[a - 1]
    assert int(primepi(xr)) == exact and abs(ef.pi_explicit(xr, 144, Z1000) - p144) < 0.01
assert abs(ef.pi_explicit(12312, 1000, Z1000) - 1471) < 0.05
assert abs(ef.pi_explicit(911298, 1000, Z1000) - 72116) < 2

if __name__ == "__main__":
    for xr, exact, li_v, p10, p144 in EXPLICIT:
        print(xr, "pi", exact, "Li", li_v, "10 zeros", p10, "144 zeros", p144)
    print("all assertions pass")

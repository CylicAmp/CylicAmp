# CLASS: LEMMA
"""
All 36 reversal spans ab -> ba, 1 <= a < b <= 9 (owner, 2026-10-04: "keep going
to 16 through 61"; all spans done at once). Full row-by-row tables (kind, digit
sum, n mod 9, running sum, primes so far) are generated into
math/lemmas/reversal_spans_all_tables.md and checked here.
First spans and the owner's lines: reversal_spans_supplied_audit_2026_10_04.py.

16 THROUGH 61: 46 numbers, total 1771 = 7 x 11 x 23 -> 7 = 1+6. Twelve primes:
17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61. Digit sum 9 at 18, 27, 36, 45, 54.

LAWS, PROVED FOR ALL 36 (d = b - a):
  L1. The span has 9d+1 numbers: 10, 19, 28, 37, 46, 55, 64, 73 (all -> 1).
  L2. Total = (9d+1) x 11(a+b) / 2; always divisible by 11.
  L3. Total reduces to a+b, the digit sum at both ends.
  L4. When 9d+1 is odd (d even) it divides the total: so the five spans with
      d = 4 (15->51, 26->62, 37->73, 48->84, 59->95) all have 37 numbers and
      totals divisible by 37 (1221, 1628, 2035, 2442, 2849 = 37 x 33, 44, 55,
      66, 77). Likewise d = 2 gives 19 and d = 8 gives 73 (19->91: 4015 = 5 x 11 x 73).
  L5. Totals at fixed d step by 11 x (9d+1): the d = 4 totals are 37 x 11k.

FALSIFICATION: any assertion below failing.
"""
import pathlib
from sympy import isprime

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def ds(n):
    return sum(map(int, str(n)))

SPANS = [(10 * a + b, 10 * b + a, a, b) for a in range(1, 9) for b in range(a + 1, 10)]
assert len(SPANS) == 36

for lo, hi, a, b in SPANS:
    ns = range(lo, hi + 1)
    d, T = b - a, sum(ns)
    assert len(ns) == 9 * d + 1 and dr(len(ns)) == 1
    assert 2 * T == (9 * d + 1) * 11 * (a + b) and T % 11 == 0
    assert dr(T) == dr(a + b) == dr(ds(lo)) == dr(ds(hi))
    if d % 2 == 0:
        assert T % (9 * d + 1) == 0

D4 = [sum(range(lo, hi + 1)) for lo, hi, a, b in SPANS if b - a == 4]
assert D4 == [1221, 1628, 2035, 2442, 2849] == [37 * k for k in (33, 44, 55, 66, 77)]
assert sum(range(19, 92)) == 4015 == 5 * 11 * 73

ns = list(range(16, 62))
assert len(ns) == 46 and sum(ns) == 1771 == 7 * 11 * 23 and dr(1771) == 7
assert [p for p in ns if isprime(p)] == [17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
assert [n for n in ns if ds(n) == 9] == [18, 27, 36, 45, 54]

# the generated tables match a fresh computation, row by row
md = (pathlib.Path(__file__).parent / "reversal_spans_all_tables.md").read_text().splitlines()
for lo, hi, a, b in SPANS:
    i = md.index(f"### {lo} through {hi}")
    rs = pc = 0
    for k, n in enumerate(range(lo, hi + 1)):
        rs += n
        pc += isprime(n)
        kind = "prime" if isprime(n) else ("even" if n % 2 == 0 else "odd")
        assert md[i + 4 + k] == f"| {n} | {kind} | {ds(n)} | {n % 9} | {rs} | {pc} |"

if __name__ == "__main__":
    print("all assertions pass")

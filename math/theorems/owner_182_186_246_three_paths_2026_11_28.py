# CLASS: AUDIT
"""
The owner's image "182 . 186 . 246 -- NUMERICAL COMPARISON" (2026-11-28, made with the owner's AI tool): three columns
373 / 777 / 888, GATE 2 / 6 / 3, DIGRAPHS (1,1) / (5,5) / (7,7), "THREE PATHS . ONE NUMERIC ARCHITECTURE".

RIGHT:
  182, 186, 246 are the least diameters of admissible 39-, 40- and 50-tuples (OEIS A008407; math/primes/admissible_50_246.py,
    2026-11-21): 246 - 182 = 64 is the shift of the 39-suffix (h_12 = 64), 186 - 182 = 4, 246 - 186 = 60.
  GATES are the digital roots of the top numbers: 1+8+2 = 11 -> 2, 1+8+6 = 15 -> 6, 2+4+6 = 12 -> 3.
  DIGRAPHS are the roots of the two neighbour sums in 373, 777, 888: 3+7 = 10 -> 1 and 7+3 = 10 -> 1; 7+7 = 14 -> 5;
    8+8 = 16 -> 7.
  373 is prime (the 37 | 73 overlap palindrome of pasted_emirp_palindromes_audit_2026_11_21.py); 777 = 3 x 7 x 37;
    888 = 2^3 x 3 x 37 = 246 + 642 (a number plus its flip, 37 | n + rev(n) for evenly spaced digits).
ASKED (blocks a check): the step that takes 182 -> 373, 186 -> 777, 246 -> 888. 246 + 642 = 888 is a flip-sum, but
  182 + 281 = 463 and 186 + 681 = 867, so the flip-sum does not give the other two.
Frameworks: records/gf37_audit_182_186_246_2026_11_28.txt.

FALSIFICATION: any assertion failing.
"""
import importlib.util
import pathlib

from sympy import factorint, isprime

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("adm", ROOT / "math" / "primes" / "admissible_50_246.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
dr = lambda n: 1 + (n - 1) % 9
rev = lambda n: int(str(n)[::-1])

assert (A.A008407[39], A.A008407[40], A.A008407[50]) == (182, 186, 246) and A.SHIFT == 64 == 246 - 182
assert (186 - 182, 246 - 186) == (4, 60)
assert [sum(map(int, str(n))) for n in (182, 186, 246)] == [11, 15, 12] and [dr(n) for n in (182, 186, 246)] == [2, 6, 3]
digraph = lambda n: tuple(dr(int(a) + int(b)) for a, b in zip(str(n), str(n)[1:]))
assert [digraph(n) for n in (373, 777, 888)] == [(1, 1), (5, 5), (7, 7)]
assert isprime(373) and factorint(777) == {3: 1, 7: 1, 37: 1} and factorint(888) == {2: 3, 3: 1, 37: 1}
assert 246 + rev(246) == 888 and 182 + rev(182) == 463 != 373 and 186 + rev(186) == 867 != 777
assert (ROOT / "records" / "gf37_audit_182_186_246_2026_11_28.txt").exists()

if __name__ == "__main__":
    print("182 186 246 = A008407(39, 40, 50); gates = roots 2 6 3; digraphs (1,1) (5,5) (7,7) right; 182->373, 186->777 asked")

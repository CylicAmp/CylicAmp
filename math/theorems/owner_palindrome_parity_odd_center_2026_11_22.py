# CLASS: AUDIT
"""
The owner's "ODD CENTER" image (2026-11-22, made with the owner's AI tool): THE PALINDROME PARITY THEOREM --
"Odd length: free center -> all sums realizable. Even: paired digits -> only even sums. The center is King. Unpaired,
free. ... Theorem holds of all lengths." -- with a table by length and the labels OO (odd lengths), OZ (even lengths).

THE THEOREM -- RIGHT, every length checked by listing every palindrome up to 10 digits (leading digit 1-9):
  even length 2k: the digit sum is 2 x (the k paired digits), so exactly the even sums 2, 4, ..., 18k occur
  odd length 2k+1 (k >= 1): the sum is 2 x (paired digits) + centre, and the free centre 0-9 fills every value:
      every sum from 2 to 9(2k+1) occurs (3 digits: 2..27, 5: 2..45, 7: 2..63, 9: 2..81)
  length 1: 1..9
  The parity limit is on the digit sum only: even lengths still reach every digital root 1-9 (10 -> 1, 12 -> 3, ...).

THE TABLE AND LABELS -- WRONG where they change a result:
  rows 5 and 7 say "even only"; odd lengths give every sum (10001 -> 2, 10101 -> 3, 12321 -> 9 at length 5)
  row 4 (abba) says centre "yes"; an even palindrome has no centre
  the row strings do not have the row lengths: 5 is written abccba (6 letters), 6 abcccba (7), 7 abcddcba (8);
  length 3 (aba) is missing; on the left, abcdba, abddcba and abdccba are not palindromes
  (wording garbles "reaser", "EVNTER" left in the image, no number depends on them)
ASKED: what OO and OZ stand for (not in the repo, the old message record or the commit history).

CONNECTIONS:
  theorem_160_aba_portal_palindromes.py: "the zero holds the place of every possible value" -- A0A opens to A1A..A9A.
    That portal is the free centre: in each group the ten sums 2A + c run through every root 1-9 -- reinforces.
  rotation_grids_x.py and pasted_emirp_palindromes_audit_2026_11_21.py: every even-length palindrome divides by 11 --
    the other face of "paired digits".
  palindrome_1234_audit.py: the 24 eight-digit palindromes from 1,2,3,4 all add to 20 -- even, as the theorem says.

FALSIFICATION: any assertion failing.
"""
import pathlib

TH = pathlib.Path(__file__).resolve().parent
dr = lambda n: 1 + (n - 1) % 9


def palindromes(L):
    h = (L + 1) // 2
    for first in range(10 ** (h - 1), 10 ** h):
        s = str(first)
        yield int(s + s[:L // 2][::-1])


def sums(L):
    return sorted({sum(map(int, str(p))) for p in palindromes(L)})


assert sums(1) == list(range(1, 10))
for L in range(2, 11):
    if L % 2 == 0:
        assert sums(L) == list(range(2, 9 * L + 1, 2)), L
        assert {dr(s) for s in sums(L)} == set(range(1, 10)), L      # every root still occurs
    else:
        assert sums(L) == list(range(2, 9 * L + 1)), L
assert [sum(map(int, str(n))) for n in (10001, 10101, 12321)] == [2, 3, 9]
assert all(str(n) == str(n)[::-1] for n in (10001, 10101, 12321))
assert [len(s) for s in ("abccba", "abcccba", "abcddcba")] == [6, 7, 8]
assert all(s != s[::-1] for s in ("abcdba", "abddcba", "abdccba")) and all(s == s[::-1] for s in ("aa", "abba", "abcba", "abccba", "abcddcba"))
assert all(int(str(n) + str(n)[::-1]) % 11 == 0 for n in range(1, 10000))
for A in range(1, 10):
    assert {dr(2 * A + c) for c in range(10)} == set(range(1, 10))     # A0A .. A9A: every root
for f in ("theorem_160_aba_portal_palindromes.py", "pasted_emirp_palindromes_audit_2026_11_21.py", "palindrome_1234_audit.py"):
    assert (TH / f).exists(), f
assert (TH.parent / "lemmas" / "rotation_grids_x.py").exists()

if __name__ == "__main__":
    print("palindrome parity: even lengths -> exactly the even sums, odd lengths -> every sum 2..9L; table rows 5, 7 wrong")

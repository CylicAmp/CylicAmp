# CLASS: AUDIT
"""
What kind of pair are the comma count and the no comma count? -- survey of known mathematics and OEIS
(owner_work #269 and #270, 2026-10-13).

THE OWNER (#269), verbatim:
    no comma count should be explored also because it creates a better understanding of the bigger picture..

    I look at one from the other as
    1=1 thats i view as something like integers vs primes or odds and even or positive or negative... I'm
    pretty sure it's a fairly new concept. ... It is not actually positive and negative odds or evens or
    indigenous or primes. It might have its own category. That's what we should figure out
THE OWNER (#270): "It may boil down to this" -- odd/even, OEO 123, EEE 248, the doubling 1248 / 751.

The two counts (#266 rule; table in comma_count_table_2026_10_13.py):
    0,000          with 1: 123        with out: 113
    0,000,000      with 1: 12333      with out: 11323      (the owner's #265 values)
    0,000,000,000  with 1: 1233343    with out: 1132333    (rule carried on)

OEIS (oeis.org, searched 2026-10-13, re-checked by hand the same day):
  123, 12333, 1233343 -- No results.   113, 11323, 1132333 -- No results.
  Neither count, as a sequence, is in OEIS.
  Nearest entry: A135475, "Sorted list of strings that can be obtained by starting with 123 and
  repeatedly doubling any substring in place". It lists 123, 1123, 12333 and 112233 -- four of the
  owner's numbers (#265, #268, #269) -- each is 123 with pieces doubled. 23, 113, 11323 and 1233343
  are not in it (checked below by computation): the "with out" count is never a doubling of 123.
  23, 123, 1123 also sit in A055016 (smallest number whose digit squares add to n): n = 13, 14, 15,
  because each step puts a 1 in front. A title match, not about commas.

KNOWN PAIRS TESTED against the owner's two counts (each tested in python, trying to refute):
  cardinal / ordinal (how many vs which one): digit groups counted by how many (3), commas by which
    comma (1, 2) gives 11323; commas numbered on from the lead's 1 gives 12333. Both reproduce --
    but an all-cardinal and an all-ordinal reading give the same strings, so the label does not pin
    the owner's pair down. PARTIAL.
  Lambek-Moser theorem (a sequence and its complement each read from the other's counting function,
    Amer. Math. Monthly 61 (1954) 454-458): fits only the frame -- in a long grouped numeral the
    commas take 1 place in 4, the digits 3 in 4 (OEIS A008586 / A042968, complements). None of the
    owner's count strings comes out of it (26 readings tried). PARTIAL, frame only.
  Beatty / Rayleigh (two sequences that split the integers): commas fall at 2, 6, 10 or 3, 7, ...,
    depending on the lead, not at the 4, 8, 12 of the Beatty pair. NO.
  rank within its own letter (rank/select; the OEIS "ordinal transform"): position = digits so far +
    commas so far holds, but the ordinal transform of 0,000,000 is 11223, not 11323. NO for the strings.
  stars and bars: #267's three lines (1,3), (2,2), (3,1) are exactly every way to cut 4 into two
    positive parts, C(3,1) = 3 of them. EXACT for #267; it does not give the count strings.

RESULT: no established kind of pair reproduces both of the owner's counts. Cardinal/ordinal comes
closest and does not decide between readings. In OEIS neither count is listed. Open.

FALSIFICATION: any assertion failing.
"""
from itertools import combinations


def count_commas(commas, with1):
    out = [1]
    for c in range(1, commas + 1):
        out += [c + 1 if with1 else c, 3]
    return "".join(map(str, out))


assert [count_commas(k, True) for k in (1, 2, 3)] == ["123", "12333", "1233343"]
assert [count_commas(k, False) for k in (1, 2, 3)] == ["113", "11323", "1132333"]

seen, frontier = {"123"}, ["123"]          # A135475's definition, strings up to length 7
while frontier:
    s = frontier.pop()
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            t = s[:j] + s[i:j] + s[j:]
            if len(t) <= 7 and t not in seen:
                seen.add(t)
                frontier.append(t)
assert all(x in seen for x in ("123", "1123", "12333", "112233"))
assert not any(x in seen for x in ("23", "113", "11323", "1132333", "1233343"))


def smallest_square_digit_sum(n):
    return next(m for m in range(1, 10 ** 6) if sum(int(c) ** 2 for c in str(m)) == n)


assert [smallest_square_digit_sum(n) for n in (13, 14, 15)] == [23, 123, 1123]
assert sorted((a, 4 - a) for a in range(1, 4)) == [(1, 3), (2, 2), (3, 1)] == \
    sorted((c[0], 4 - c[0]) for c in combinations(range(1, 4), 1))

if __name__ == "__main__":
    print("neither count is in OEIS; A135475 holds 123, 1123, 12333, 112233 (doublings of 123), not 11323;")
    print("cardinal/ordinal reproduces both strings without deciding; #267 = the 3 cuts of 4 into two parts")

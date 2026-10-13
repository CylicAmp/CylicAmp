# CLASS: AUDIT
"""
The comma count and the no comma count, as a table (owner_work #265-#269, 2026-10-13).

THE OWNER'S LINES, verbatim (owner_work/messages/2026-10-13.txt):

#265:
    a set can be
    0,000=1+3=4
    00,000=2+3=5
    000,000=3+3=6
    0+1=0,000,000=1+6=7
    or 12333 count commas with 1
    or 11323 count commas with out

#266:
    If I start at 1, I count the comma as 2. And then I continue to count those commas from there.
    Then I will get to a 3. If I start at 1, I don't count the comma as adding 2. Then I get 1, 1 at
    the beginning of my count. Then I get 3. We get another comma, that's 2. And then 3 again.

#267:
    0,------000=1+3=4
    00,------00=2+2=4
    000,------0=3+1=4

#268 / #269 (added):
    0,
    00,
    000,

    this section goes by 369
    like this
    23
    123
    1123

    because
    123
    112233
    ...
    when we count the comma

    also with a comma we get 369

    ,000=3
    ,000=6
    ,000=9=18
    1+8=9
    and if we add the commas
    =18+3=21
    =9+3=12

    no comma count should be explored also because it creates a better understanding of the bigger picture..

THE OWNER'S #266 RULE, as used here (nothing added to it):
  a set is read left to right as pieces: the lead, then comma, group, comma, group, ...
  "with 1" (count commas with 1):  lead 1, each comma numbered on from the 1 (2, 3, 4, ...), each group of three = 3
  "with out" (count commas with out): lead 1, each comma numbered among the commas (1, 2, 3, ...), each group = 3
  0,000,000 -> with 1: 1 2 3 3 3 = 12333   with out: 1 1 3 2 3 = 11323   (the owner's two numbers; both reproduce)

  The rule starts "If I start at 1": it is written for a lead of ONE digit. So it determines every set
  0,000 / 0,000,000 / 0,000,000,000 / ... (lead 0, groups of three) and nothing else.

THE TABLE (source: owner = written by the owner; rule = carried on by the #266 rule)
  set                  digits commas  with 1         with out       source
  0,000                  4      1     123            113            rule (owner wrote 0,000=1+3=4)
  0,000,000              7      2     12333          11323          owner (#265, #266)
  0,000,000,000         10      3     1233343        1132333        rule
  0,000,000,000,000     13      4     123334353      113233343      rule
  0,000,..(5 commas)    16      5     12333435363    11323334353    rule
  00,000                 5      1     not settled    not settled    owner wrote 00,000=2+3=5 (lead of 2)
  000,000                6      1     not settled    not settled    owner wrote 000,000=3+3=6 (lead of 3)
  0,------000            4      1     123 / 113 if the six dashes are not a piece -- not settled  (owner: 1+3=4)
  00,------00            4      1     not settled    not settled    owner: 2+2=4 (lead 2, group of 2)
  000,------0            4      1     not settled    not settled    owner: 3+1=4 (lead 3, group of 1)
  0,                     1      1     23 (owner)     not settled    owner: "0, / 00, / 000, ... 23 / 123 / 1123 ... when we count the comma"
  00,                    2      1     123 (owner)    not settled    owner (paired with the leads in line order)
  000,                   3      1     1123 (owner)   not settled    owner (paired with the leads in line order)
  ,000 ,000 ,000         9      3     18+3=21; 9+3=12   3, 6, 9 = 18; 1+8 = 9    owner (#268): "if we add the commas"
  ,000 x k (k=1,2,4,5)  3k      k     3k + k         3k             rule (the #268 "add the commas", carried on)

FORCED BY THE #266 RULE (k = number of commas, lead of one digit):
  - both counts are 2k+1 pieces long; the pieces that are not commas are 1, 3, 3, ..., which add to
    1 + 3k = the owner's digit count (0,000 = 1+3 = 4; 0,000,000 = 1+6 = 7).
  - with 1 minus with out = 10, 1010, 101010, ... (k ones in the comma places): every comma is one higher
    with the 1, nothing else moves. 12333 - 11323 = 1010.
  - digit sum with 1 = 1 + 3k + (2 + 3 + ... + (k+1));  digit sum with out = 1 + 3k + (1 + 2 + ... + k);
    the two differ by exactly k (one per comma). 12333 -> 12, 11323 -> 10, difference 2 = two commas.
  - "with 1" reads 1, 2, 3, ..., k+1 down the lead and the commas: the commas carry the count on from the 1.
    "with out" restarts the commas at 1, so the 1 appears twice at the start -- the owner's "1, 1 at the
    beginning of my count".
  - for ,000 x k under "add the commas": with = 4k, without = 3k, difference k (one per comma) -- the same
    one-per-comma difference as the #266 digit sums.

NOT SETTLED BY THE OWNER'S LINES:
  - a lead of 2 or 3 digits (00,000 / 000,000, and 00,------00 / 000,------0) under either count: #266
    says "If I start at 1"; what the lead piece is written as when the lead has 2 or 3 digits is not given.
  - a group of fewer than three digits (00,------00 has a group of 2; 000,------0 a group of 1).
  - whether the six dashes in #267 are a piece.
  - how 0, gives 23 (and 00, gives 123, 000, gives 1123). The #266 rule on "0," (lead 1, then one comma, no
    group) gives 12 with 1 and 11 with out, not 23. 12 + 11 = 23 fits this one row; 00, and 000, have no
    #266 value to test it against, so it is recorded and not claimed.
  - the pairing 0,->23, 00,->123, 000,->1123 is the line order of the owner's lists; the owner did not
    write the pairs side by side.
  - the no comma count of the leads 0, / 00, / 000, ("no comma count should be explored also").
  - "this section goes by 369": how 23, 123, 1123 go by 3, 6, 9.

FALSIFICATION: any assertion failing.
"""


def comma_count(commas, with1):
    """owner #266, lead of one digit: lead 1, then each comma and its group of three (= 3)."""
    pieces = [1]
    for c in range(1, commas + 1):
        pieces += [c + 1 if with1 else c, 3]
    return "".join(map(str, pieces))


def digits_of(s):
    return len(s.replace(",", "").replace("-", ""))


# the owner's two numbers
assert comma_count(2, True) == "12333" and comma_count(2, False) == "11323"

# one-digit lead, k = 1..5 commas: the table rows determined by the rule
TABLE = {1: ("123", "113"), 2: ("12333", "11323"), 3: ("1233343", "1132333"),
         4: ("123334353", "113233343"), 5: ("12333435363", "11323334353")}
for k, (w, wo) in TABLE.items():
    s = "0" + ",000" * k
    assert (comma_count(k, True), comma_count(k, False)) == (w, wo)
    assert digits_of(s) == 1 + 3 * k and s.count(",") == k
    assert len(w) == len(wo) == 2 * k + 1
    # non-comma pieces (even positions) add to the owner's digit count 1 + 3k
    assert sum(map(int, w[0::2])) == sum(map(int, wo[0::2])) == 1 + 3 * k == digits_of(s)
    # with 1 minus with out = 1010...10 (k ones, in the comma places)
    assert int(w) - int(wo) == int("10" * k)
    # digit sums differ by exactly k
    dw, dwo = sum(map(int, w)), sum(map(int, wo))
    assert dw == 1 + 3 * k + sum(range(2, k + 2)) and dwo == 1 + 3 * k + sum(range(1, k + 1)) and dw - dwo == k
    # with 1: lead and commas read 1, 2, ..., k+1; with out: 1, then 1, ..., k
    assert [int(w[0])] + [int(x) for x in w[1::2]] == list(range(1, k + 2))
    assert [int(x) for x in wo[1::2]] == list(range(1, k + 1)) and wo[:2] == "11"

# #265 digit counts as the owner wrote them
for s, lead, total in (("0,000", 1, 4), ("00,000", 2, 5), ("000,000", 3, 6), ("0,000,000", 1, 7)):
    assert len(s.split(",")[0]) == lead and digits_of(s) == total
assert 1 + 3 == 4 and 2 + 3 == 5 and 3 + 3 == 6 and 1 + 6 == 7
assert sum(map(int, "12333")) == 12 and sum(map(int, "11323")) == 10 and 12333 - 11323 == 1010

# #267: lead + rest = 4 each; only the first has a group of three
for s, (a, b) in (("0,------000", (1, 3)), ("00,------00", (2, 2)), ("000,------0", (3, 1))):
    lead, rest = s.split(",")
    assert (len(lead), rest.count("0"), rest.count("-")) == (a, b, 6) and a + b == 4 == digits_of(s)
assert comma_count(1, True) == "123" and comma_count(1, False) == "113"   # 0,------000 if the dashes are no piece

# #268 leads: the #266 rule on "0," (lead 1, one comma, no group) is 12 / 11, not the owner's 23
assert "".join(map(str, [1, 2])) == "12" and "".join(map(str, [1, 1])) == "11" and 12 + 11 == 23
for n, s in (("23", "0,000"), ("123", "00,000"), ("1123", "000,000")):
    assert sum(map(int, n)) == len(s)             # 5, 6, 7 = characters with the comma counted
assert 123 - 23 == 100 and 1123 - 123 == 1000

# #268 ,000 three times and "if we add the commas"
run = [3, 6, 9]
assert [3 * k for k in (1, 2, 3)] == run and sum(run) == 18 and 1 + 8 == 9
assert 18 + 3 == 21 and 9 + 3 == 12 and digits_of(",000" * 3) == 9 and (",000" * 3).count(",") == 3
for k in (1, 2, 3, 4, 5):
    s = ",000" * k
    assert digits_of(s) == 3 * k and digits_of(s) + s.count(",") == 4 * k
assert [4 * k for k in (1, 2, 4, 5)] == [4, 8, 16, 20]

if __name__ == "__main__":
    print("set                    digits commas  with 1        with out")
    for k, (w, wo) in TABLE.items():
        print(f"{'0' + ',000' * k:22s} {1 + 3 * k:5d} {k:6d}   {w:13s} {wo}")
    print(",000 x3 (add the commas): without 3,6,9=18 -> 9; with 18+3=21, 9+3=12")
    print("all assertions hold; leads of 2 or 3 digits, groups under 3, the dashes and 0,->23 are not settled by the owner's lines")

# CLASS: AUDIT
"""
Audit of supplied text (2026-10-04): a 26-term two-digit "wave" -- doubles 00, 11, ..., 99,
each followed by +1 and its flip, closing back at 00. Sequence rebuilt from the text's own
column lists:
  00 11 12 22 23 32 33 34 43 44 45 54 55 56 65 66 67 76 77 79 87 88 89 98 99 00
Mathematics only.

CORRECT
  W1 26 terms; left-column sum 123.
  W2 The pattern aa -> a(a+1) -> (a+1)a -> (a+1)(a+1) holds for a = 2..6; flips cancel in
     tens-minus-units (ab and ba give +(a-b) and -(a-b)).

WRONG
  W3 Right-column sum: the text's own digits add to 125, not 122. So left - right = -2, not +1.
     The -2 comes exactly from the three terms with no partner flip: 12 (-1), 79 (-2), 87 (+1).
  W4 The pattern is broken in two places, not one: stage 1 has no 21 (the text marks it
     "skipped"), and after 77 the pattern's 78 is replaced by 79, so 78 and 97 never appear.
  W5 "A closed, self-correcting kinetic circuit with net drift 1": the imbalance is -2 and comes
     only from the three unpaired terms; with the pattern completed (adding 21, 78 -> 87, 89 ->
     98 pairs as they stand) the flips cancel exactly and the drift is 0.
  W6 99 + 1 = 100, not 00: as a two-column counter it wraps to 00 with 2 carries (T432);
     the 1 that leaves is the drain mark in the owner's system.
FALSIFICATION: any assertion failing.
"""
seq = "00 11 12 22 23 32 33 34 43 44 45 54 55 56 65 66 67 76 77 79 87 88 89 98 99 00".split()
L = [int(s[0]) for s in seq]
R = [int(s[1]) for s in seq]
assert len(seq) == 26 and sum(L) == 123                                                   # W1
for a in range(2, 7):                                                                      # W2
    i = seq.index(f"{a}{a}")
    assert seq[i:i + 4] == [f"{a}{a}", f"{a}{a+1}", f"{a+1}{a}", f"{a+1}{a+1}"]
assert sum(R) == 125 != 122 and sum(L) - sum(R) == -2                                      # W3
lone = [s for s in seq if s[0] != s[1] and s[::-1] not in seq]
assert lone == ["12", "79", "87"] and sum(int(s[0]) - int(s[1]) for s in lone) == -2
assert "21" not in seq and "78" not in seq and "97" not in seq                             # W4
full = [s for s in seq if s not in ("79",)] + ["21", "78"]
assert sum(int(s[0]) - int(s[1]) for s in full) == 0                                       # W5
assert 99 + 1 == 100 and (99 + 1) % 100 == 0                                               # W6

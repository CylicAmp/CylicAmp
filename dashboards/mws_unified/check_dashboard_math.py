# CLASS: AUDIT
"""
Checks of the numbers and statements on the MWS dashboard (dashboards/mws_unified/index.html, built from
the owner's handoff section 5, owner_work #272). Plain Python + sympy; run: python3 dashboards/mws_unified/check_dashboard_math.py

HOLDS   37 never divides 2^p - 1 for a prime p (the order of 2 mod 37 is 36, and 36 does not divide a prime);
        sieve counts 4, 25, 168, 1229 and mean gaps 1.667, 3.958, 5.958, 8.120 for limits 9, 99, 999, 9999;
        default matrix: spans sum 13, element-wise products [2, 12, 35] with sum 49, mean of all seven numbers 31/7 = 4.43;
        YSES 1: parallax 10.6124 mas -> 94.23 pc -> 307.3 light-years (consistent); 7.2 has digital root 9.
CORRECTED  the page said "self-alignment locks when p = 17 mod 36". The test (2^p - 1) mod 37 = p mod 37 holds for
        one class of p mod 1332 for each of the 36 residues of p mod 36. Not necessary: 241 passes (241 = 25 mod 36).
        Not sufficient: 53 = 17 mod 36 fails. The page now says what is true.
STATIC TEXT  "13.5" (Matrix Mean) and "0" (Cross-Dot) did not match what the code computes (4.43 and 49); the page now
        shows "..." until the code runs. The "Cross-Dot Vector" now shows the vector of products and its sum.
CHARTS  the page called the plotted mean gap "Mean Gap Variance"; it is the mean gap.
FALSIFICATION: any assertion failing.
"""
from sympy import n_order, primerange

assert n_order(2, 37) == 36 and all((pow(2, p, 37) - 1) % 37 != 0 for p in primerange(2, 5000))
expected = {9: (4, "1.667"), 99: (25, "3.958"), 999: (168, "5.958"), 9999: (1229, "8.120")}
for L, (count, mean) in expected.items():
    q = list(primerange(2, L + 1))
    assert len(q) == count and f"{(q[-1] - q[0]) / (len(q) - 1):.3f}" == mean
nodes, spans = [1, 3, 5, 9], [2, 4, 7]
prods = [a * b for a, b in zip(nodes, spans)]
assert sum(spans) == 13 and prods == [2, 12, 35] and sum(prods) == 49 and f"{sum(nodes + spans) / len(nodes + spans):.2f}" == "4.43"
passing = [p for p in range(1332 * 3) if (pow(2, p, 37) - 1) % 37 == p % 37]
assert sorted({p % 1332 for p in passing}) == [0, 1, 17, 94, 241, 245, 286, 304, 391, 401, 440, 564, 585, 618, 640, 647, 707, 738, 750, 753, 806, 811, 819, 838, 876, 890, 920, 940, 968, 1015, 1095, 1101, 1191, 1298, 1307, 1309]
assert len({p % 36 for p in passing}) == 36                                    # one class mod 1332 for every residue mod 36
assert [p for p in primerange(2, 2000) if p in set(passing) or (pow(2, p, 37) - 1) % 37 == p % 37] == [17, 241, 401, 647, 811, 1307, 1723, 1733, 1979]
assert 241 % 36 == 25 and (pow(2, 241, 37) - 1) % 37 == 241 % 37                # passes without being 17 mod 36
assert 53 % 36 == 17 and (pow(2, 53, 37) - 1) % 37 == 17 and 53 % 37 == 16      # 17 mod 36 but fails
pc = 1000 / 10.6124
assert abs(pc - 94.23) < 0.01 and abs(pc * 3.26156 - 307.3) < 0.05
assert sum(int(c) for c in "72") == 9

if __name__ == "__main__":
    print("dashboard numbers hold; alignment is one class mod 1332 per residue mod 36, not 'p = 17 mod 36'")

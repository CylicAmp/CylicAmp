# CLASS: COMPUTATION
"""
The owner's sequences that generate their next terms -- one index, each rule run forward.
Author: Michael Warren Song (CyclicAmp)

Each entry: the owner's sequence, the rule that produces the next term, the next terms the
rule gives, and the file where it is proved. Pulled together 2026-10-04.

1 THE ROADS (owner 2026-09-12: "123 ... next is 234 same way, than 345, 456, 567, 789, 891,
  912, 123"). Rule: add 111 to each digit, wrapping 9 -> 1. Next terms: 123 234 345 456 567
  678 789 891 912 -> back to 123 (period 9). The owner's list skips 678; the rule includes it.
  Proved in theorem_326_all_roads_ap_triples_gf37.py: the seven ascending roads are all
  12 mod 37; the wrap breaks it (891 = 3, 912 = 24 mod 37).
2 THE ROTATION OF EACH ROAD (same message: 123-321 / 312-213 / 231-132 / 123-321). Rule: move
  the last digit to the front. Closes after 3 rows, for every road -- theorem_325 (the
  rotation is multiplication by 26 = 137 mod 37, of order 3).
3 THE +9 CHAIN (owner 2026-09-13 "between 2 and 11 is 9 ... 3+9 = 12, +21"; 2026-10-03
  "1+2=3+9=12+9=21+9=30+9=39+9=48"). Rule: add 9. Next terms after 48: 57, 66, 75, 84, 93 --
  every term keeps the start's digital root. pf_chain_plus9_2026_10_03.py.
4 THE DRAIN COUNTER (owner 2026-09-23). Rule: the k-th nine is 9k counting nines, 10k - 1
  counting tens; k nines drain with +k (9k + k = 10k). Next pairs after (36, 39): (45, 49),
  (54, 59), (63, 69). casting_out_tens_drain_system.py.
5 THE OUT-AND-BACK REPDIGIT LINES (owner 2026-10-03, 333 / 222 / 111). Rule: aaa -> 3a x a ->
  back to 3a. Next: 444 -> 12 x 4 = 48 -> 12; 555 -> 15 x 5 = 75 -> 15.
  repdigit_return_lines_2026_10_03.py.

6 THE TWO-DIGIT ROADS (12 23 34 45 56 67 78 89 91 12). Same rule as 1 on two digits; period 9.
  Next after 91: 12. outer_step_parity_supplied_audit_2026_10_04.py.

NOT PREDICTIVE (checked, recorded so they are not reused as rules):
  - the 2-4-8 prime blocks every +90 (fails at 287 = 7 x 41): prime_root_mirror_53_...py
  - "roots alternate even/odd" for consecutive primes (55.3% flips): ending_vs_root_...py
FALSIFICATION: any assertion failing.
"""
dr = lambda n: 1 + (n - 1) % 9

road = lambda n: int("".join(str(int(c) % 9 + 1) for c in str(n)))
seq = [123]
for _ in range(9):
    seq.append(road(seq[-1]))
assert seq == [123, 234, 345, 456, 567, 678, 789, 891, 912, 123]                          # 1
assert [r % 37 for r in seq[:7]] == [12] * 7 and (891 % 37, 912 % 37) == (3, 24)

rot = lambda s: s[-1] + s[:-1]                                                           # 2
for r in seq[:9]:
    s = str(r)
    assert rot(rot(rot(s))) == s and int(rot(s)) % 37 == int(s) * 26 % 37

chain = [3]                                                                              # 3
for _ in range(10):
    chain.append(chain[-1] + 9)
assert chain[:6] == [3, 12, 21, 30, 39, 48] and chain[6:11] == [57, 66, 75, 84, 93]
assert {dr(t) for t in chain} == {3}

assert [(9 * k, 10 * k - 1) for k in (5, 6, 7)] == [(45, 49), (54, 59), (63, 69)]         # 4
assert all(9 * k + k == 10 * k for k in range(1, 50))

out_back = lambda a: (3 * a, 3 * a * a, 3 * a * a // a)                                  # 5
assert out_back(4) == (12, 48, 12) and out_back(5) == (15, 75, 15)
assert all(sum(map(int, str(111 * a))) == 3 * a for a in range(1, 10))

two = [12]                                                                               # 6
for _ in range(9):
    two.append(road(two[-1]))
assert two == [12, 23, 34, 45, 56, 67, 78, 89, 91, 12]

if __name__ == "__main__":
    print("roads:", seq)
    print("+9 chain:", chain)
    print("drain pairs:", [(9 * k, 10 * k - 1) for k in range(1, 8)])

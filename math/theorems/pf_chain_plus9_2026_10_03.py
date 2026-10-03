# CLASS: AUDIT
"""
The owner's chain (2026-10-03, verbatim):  1+2=3+9=12+9=21+9=30+9=39+9=48
with the owner's definition: PF = prime foundational = numbers that equal 12.

DECODED (every term checked)
  C1 Terms: 3, 12, 21, 30, 39, 48 -- start 1+2 = 3, then +9 each step.
  C2 Adding 9 never changes the digital root, so every term has the digital root of 12:
     each term "equals 12" under digit reduction (12 -> 1+2 = 3). That is the chain
     3 (mod 9).
  C3 Digit sums along the chain: 3, 3, 3, 3, 12, 12 -- 39 and 48 add straight to 12.
  C4 Every term is 3n with n = 1, 4, 7, 10, 13, 16 (n = 1 mod 3), so the first three are
     repdigits / 37:  3 = 111/37,  12 = 444/37,  21 = 777/37.
  C5 777 is not on the 2026-10-02 page. That page's audit left two rules that fit every
     line and differ only at 777 (R1: 777 -> x2;  R2: 777 -> PF). This chain puts
     777/37 = 21 on the PF chain -- it agrees with R2.
  C6 888: 888/37 = 24 has digital root 6, so 24 is NOT on this chain (24 = 3 + 9k has no
     whole k). 48 = 2 x 24 is on it. The page marks 888 as PF; how 888 joins the chain is
     not decoded here, and is not bent to fit.
  Connections: 1+2 = 3 is also line 1 of repdigit_return_lines_2026_10_03.py; 48 = 3*4^2
  is the a = 4 product there (4+8 = 12).
FALSIFICATION: any assertion failing.
"""
dr = lambda m: 1 + (m - 1) % 9
ds = lambda m: sum(map(int, str(m)))

chain = [1 + 2]
for _ in range(5):
    chain.append(chain[-1] + 9)
assert chain == [3, 12, 21, 30, 39, 48]                                   # C1
assert all(dr(t) == dr(12) == 3 for t in chain)                           # C2
assert all(t % 9 == 3 for t in chain)
assert [ds(t) for t in chain] == [3, 3, 3, 3, 12, 12]                     # C3
assert [t // 3 for t in chain] == [1, 4, 7, 10, 13, 16]                   # C4
assert all((t // 3) % 3 == 1 for t in chain)
assert (111 // 37, 444 // 37, 777 // 37) == (3, 12, 21) == tuple(chain[:3])
assert 777 // 37 in chain                                                 # C5 -> R2
assert 888 // 37 == 24 and 24 not in chain and (24 - 3) % 9 != 0         # C6
assert 2 * 24 == 48 in chain
assert 3 * 4 ** 2 == 48 and ds(48) == 12

if __name__ == "__main__":
    print("chain:", chain, " all digital root 3 = dr(12)")
    print("repdigits on it: 111, 444, 777 (3, 12, 21); 888 -> 24 not on it, 48 = 2*24 is")

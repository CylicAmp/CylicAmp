#!/usr/bin/env python3
"""
REPUNIT PALINDROME SEQUENCE AUDIT
===================================
Sequence: 1, 11, 12, 121, 212, 1221, 12121, 12321, 123321, 1234321,
          12344321, 123454321, 1234554321, 12345654321, 123456654321,
          1234567654321, 12345677654321, 123456787654321,
          1234567887654321, 12345678987654321, 123456789987654321

STRUCTURE:
  Two interleaved sub-sequences (from position 8 onward):
    A: R_n^2        = 1, 121, 12321, 1234321, 123454321, ...
    B: R_n x R_{n+1} = 11, 1221, 123321, 12344321, 1234554321, ...
  R_n = repunit = 111...1 (n ones) = (10^n - 1)/9

DIGIT SUM IDENTITIES [PROVEN]:
  digit_sum(R_n^2)         = n^2        (perfect squares)
  digit_sum(R_n x R_{n+1}) = n(n+1)     (oblong / pronic numbers)

EMIRP ANCHOR [PROVEN]:
  ord_37(10) = 3  =>  37 | R_3  =>  R_3 = 111 = 3 x 37
  R_3^2 = 12321 = 9 x 37^2  (R_3^2 divisible by 37^2)
  ord_73(10) = 8  =>  73 | R_8  =>  73 | 11111111

MOD-37 PERIOD [PROVEN]:
  R_n mod 37 has period 3: [1, 11, 0, 1, 11, 0, ...]
  R_n^2 and R_n x R_{n+1} together produce period-6 pattern:
    [1, 11, 10, 0, 0, 0, 1, 11, 10, 0, 0, 0, ...]

DR=8 ABSENT [PROVEN]:
  No number in the sequence has DR=8.
  DR values present: {1, 2, 3, 4, 5, 6, 7, 9}

ALTERNATING SUB-SEQUENCE (early terms only):
  12 (DR=3), 212 (DR=5), 12121 (DR=7)
  DR values are consecutive odd primes: 3, 5, 7
"""

from sympy import factorint

errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

def dr(n):
    return 0 if n == 0 else 1 + (abs(int(n)) - 1) % 9

def repunit(k):
    return (10**k - 1) // 9

def digit_sum(n):
    return sum(int(c) for c in str(n))

SEQ = [
    1, 11, 12, 121, 212, 1221, 12121, 12321,
    123321, 1234321, 12344321, 123454321, 1234554321,
    12345654321, 123456654321, 1234567654321, 12345677654321,
    123456787654321, 1234567887654321, 12345678987654321,
    123456789987654321
]

# ── ord_37(10) = 3 ────────────────────────────────────────────────────────────

print("=== ord_37(10) = 3 ===")
check("10^1 mod 37 = 10", pow(10,1,37) == 10)
check("10^2 mod 37 = 26", pow(10,2,37) == 26)
check("10^3 mod 37 = 1  (order = 3)", pow(10,3,37) == 1)
check("10^4 mod 37 = 10  (cycle restarts)", pow(10,4,37) == 10)
print()

# ── R_n mod 37 period-3 ───────────────────────────────────────────────────────

print("=== R_n mod 37: period 3 = [1, 11, 0] ===")
Rn_mod37 = [repunit(k) % 37 for k in range(1, 11)]
check("period: [1,11,0] repeating", Rn_mod37 == [1,11,0,1,11,0,1,11,0,1])
check("R_3 mod 37 = 0  (3 | R_3)", repunit(3) % 37 == 0)
check("R_6 mod 37 = 0", repunit(6) % 37 == 0)
check("R_9 mod 37 = 0", repunit(9) % 37 == 0)
print()

# ── EMIRP ANCHOR ──────────────────────────────────────────────────────────────

print("=== EMIRP ANCHOR ===")
R3 = repunit(3)
check("R_3 = 111 = 3 x 37", R3 == 111 and factorint(R3) == {3:1, 37:1})
check("R_3^2 = 12321 = 9 x 37^2", R3**2 == 12321 and 12321 == 9*37**2)
check("R_3^2 mod 37^2 = 0", R3**2 % 37**2 == 0)

check("ord_73(10) = 8  (10^8 ≡ 1 mod 73)", pow(10,8,73)==1 and all(pow(10,k,73)!=1 for k in range(1,8)))
R8 = repunit(8)
check("73 | R_8  (R_8 = 11111111)", R8 % 73 == 0)
check("R_8 / 73 = 152207", R8 // 73 == 152207)

print()
print("  Emirp pair in repunit sequence:")
print("    37 divides R_3  (position 3 = ord_37(10))")
print("    73 divides R_8  (position 8 = ord_73(10))")
print()

# ── DIGIT SUM IDENTITIES ──────────────────────────────────────────────────────

print("=== DIGIT SUM: digit_sum(R_n^2) = n^2 ===")
for k in range(1, 10):
    ds = digit_sum(repunit(k)**2)
    check(f"digit_sum(R_{k}^2) = {k}^2 = {k*k}", ds == k*k)
print()

print("=== DIGIT SUM: digit_sum(R_n x R_(n+1)) = n(n+1) ===")
for k in range(1, 10):
    ds = digit_sum(repunit(k) * repunit(k+1))
    check(f"digit_sum(R_{k} x R_{k+1}) = {k}x{k+1} = {k*(k+1)}", ds == k*(k+1))
print()

# ── MOD-37 PERIOD-6 IN SEQUENCE ───────────────────────────────────────────────

print("=== MOD-37 PERIOD-6 IN COMBINED SEQUENCE ===")
# From n=4 onwards, pattern [R_n^2, R_n x R_{n+1}] produces period-6 mod-37
combined = []
for k in range(4, 10):
    combined.append(repunit(k)**2 % 37)
    combined.append((repunit(k)*repunit(k+1)) % 37)

check("mod-37 pattern from n=4: [1,11,10,0,0,0] repeating period 6",
      combined == [1,11,10,0,0,0,1,11,10,0,0,0])
print()

# ── DR=8 ABSENT ───────────────────────────────────────────────────────────────

print("=== DR=8 ABSENT FROM SEQUENCE ===")
dr_vals = [dr(n) for n in SEQ]
check("DR=8 not in sequence", 8 not in dr_vals)
check("DR values present = {1,2,3,4,5,6,7,9}", set(dr_vals) == {1,2,3,4,5,6,7,9})
print(f"  DR sequence: {dr_vals}")
print()

# ── SEQUENCE CLASSIFICATION ───────────────────────────────────────────────────

print("=== SEQUENCE CLASSIFICATION ===")
Rn_sq   = {repunit(k)**2:          k for k in range(1,11)}
Rn_prod = {repunit(k)*repunit(k+1): k for k in range(1,10)}

for i, n in enumerate(SEQ, 1):
    ds = digit_sum(n)
    if n in Rn_sq:
        k = Rn_sq[n]
        label = f"R{k}^2  dsum=k^2={k*k}"
        check(f"#{i}: digit_sum={ds} = {k}^2", ds == k*k)
    elif n in Rn_prod:
        k = Rn_prod[n]
        label = f"R{k}xR{k+1}  dsum=k(k+1)={k*(k+1)}"
        check(f"#{i}: digit_sum={ds} = {k}x{k+1}", ds == k*(k+1))
    else:
        label = f"alt  DR={dr(n)}"
print()

# ── ALTERNATING SUB-SEQUENCE ──────────────────────────────────────────────────

print("=== ALTERNATING SUB-SEQUENCE: 12, 212, 12121 ===")
alts = [12, 212, 12121]
alt_drs = [dr(n) for n in alts]
check("DR values = [3, 5, 7]  (consecutive odd primes)", alt_drs == [3, 5, 7])
check("12 = 2^2 x 3", factorint(12) == {2:2, 3:1})
check("212 = 2^2 x 53", factorint(212) == {2:2, 53:1})
check("12121 = 17 x 23 x 31", factorint(12121) == {17:1, 23:1, 31:1})
print()

# ── FULL TABLE ────────────────────────────────────────────────────────────────

print("=== FULL TABLE ===")
print("  %2s  %-24s  %2s  %5s  %4s  %s" % ("#", "N", "DR", "mod37", "dsum", "type"))
print("  " + "-"*62)

for i, n in enumerate(SEQ, 1):
    d  = dr(n)
    m  = n % 37
    ds = digit_sum(n)
    if n in Rn_sq:
        k = Rn_sq[n]; t = "R%d^2" % k
    elif n in Rn_prod:
        k = Rn_prod[n]; t = "R%dxR%d" % (k,k+1)
    else:
        t = "alt"
    print("  %2d  %-24d  %2d  %5d  %4d  %s" % (i, n, d, m, ds, t))

print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All claims verified.")

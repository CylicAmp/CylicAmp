"""
fib_mod90_audit.py

Arithmetic audit of the 120-term Fibonacci mod 90 table.
Checks:
  1. Pisano period π(90) = 120
  2. Every listed F_n mod 90 value against independent computation
  3. Period closure: F_120 ≡ 0, F_121 ≡ 1
"""

# ---------------------------------------------------------------------------
# 1.  Compute Pisano period π(90) from first principles
# ---------------------------------------------------------------------------
print("="*62)
print("1.  Pisano period π(90)")
print("="*62)

def pisano_period(m, max_iter=100000):
    a, b = 0, 1
    for i in range(1, max_iter + 1):
        a, b = b, (a + b) % m
        if a == 0 and b == 1:
            return i
    return None

pi90 = pisano_period(90)
print(f"  Computed π(90) = {pi90}  (document claims 120)  "
      f"{'✓' if pi90==120 else 'FAIL'}")

# Cross-check via multiplicativity: π(90) = lcm(π(2), π(9), π(5))
# 90 = 2 × 3² × 5
pi2 = pisano_period(2)   # = 3
pi9 = pisano_period(9)   # = 24
pi5 = pisano_period(5)   # = 20
from math import lcm, gcd
pi90_check = lcm(lcm(pi2, pi9), pi5)
print(f"  Cross-check: lcm(π(2),π(9),π(5)) = lcm({pi2},{pi9},{pi5}) = {pi90_check} ✓")

# ---------------------------------------------------------------------------
# 2.  Generate authoritative F_n mod 90 for n = 0..121
# ---------------------------------------------------------------------------
print()
print("="*62)
print("2.  F_n mod 90: document vs. computed")
print("="*62)

def gen_fib_mod(m, count):
    seq = []
    a, b = 0, 1
    for _ in range(count):
        seq.append(a)
        a, b = b, (a + b) % m
    return seq

fibs_mod90 = gen_fib_mod(90, 122)   # n = 0..121

# Document table
table = {
    0:0, 1:1, 2:1, 3:2, 4:3, 5:5, 6:8, 7:13, 8:21, 9:34,
    10:55, 11:89, 12:34, 13:13, 14:47, 15:60, 16:7, 17:67,
    18:74, 19:31, 20:15, 21:46, 22:61, 23:17, 24:78, 25:5,
    26:83, 27:88, 28:71, 29:69, 30:50, 31:29, 32:79, 33:18,
    34:7, 35:25, 36:32, 37:57, 38:89, 39:56, 40:55, 41:21,
    42:76, 43:7, 44:83, 45:0, 46:83, 47:83, 48:76, 49:69,
    50:55, 51:34, 52:89, 53:33, 54:32, 55:65, 56:7, 57:72,
    58:79, 59:61, 60:50, 61:21, 62:71, 63:2, 64:73, 65:75,
    66:58, 67:43, 68:11, 69:54, 70:65, 71:29, 72:4, 73:33,
    74:37, 75:70, 76:17, 77:87, 78:14, 79:11, 80:25, 81:36,
    82:61, 83:7, 84:68, 85:75, 86:53, 87:38, 88:1, 89:39,
    90:40, 91:79, 92:29, 93:18, 94:47, 95:65, 96:22, 97:87,
    98:19, 99:16, 100:35, 101:51, 102:86, 103:47, 104:43, 105:0,
    106:43, 107:43, 108:86, 109:39, 110:35, 111:74, 112:19,
    113:3, 114:22, 115:25, 116:47, 117:72, 118:29, 119:11,
    120:0, 121:1,
}

errors = []
print(f"  {'n':>4}  {'computed':>9}  {'claimed':>8}  status")
print(f"  {'-'*40}")
for n in sorted(table):
    computed = fibs_mod90[n]
    claimed  = table[n]
    ok = (computed == claimed)
    if not ok:
        errors.append((n, computed, claimed))
    marker = "✓" if ok else f"FAIL  (correct={computed})"
    print(f"  {n:>4}  {computed:>9}  {claimed:>8}  {marker}")

# ---------------------------------------------------------------------------
# 3.  Period closure check
# ---------------------------------------------------------------------------
print()
print("="*62)
print("3.  Period closure")
print("="*62)

f120 = fibs_mod90[120]
f121 = fibs_mod90[121]
print(f"  F_120 mod 90 = {f120}  (should be 0)  {'✓' if f120==0 else 'FAIL'}")
print(f"  F_121 mod 90 = {f121}  (should be 1)  {'✓' if f121==1 else 'FAIL'}")

# ---------------------------------------------------------------------------
# 4.  Summary of errors
# ---------------------------------------------------------------------------
print()
print("="*62)
print("4.  Error summary")
print("="*62)
print(f"  Total entries checked: {len(table)}")
print(f"  Correct: {len(table) - len(errors)}")
print(f"  Errors:  {len(errors)}")
if errors:
    print(f"\n  {'n':>4}  {'correct':>8}  {'claimed':>8}  {'diff':>6}")
    print(f"  {'-'*36}")
    for n, corr, clm in errors:
        print(f"  {n:>4}  {corr:>8}  {clm:>8}  {corr-clm:>+6}")

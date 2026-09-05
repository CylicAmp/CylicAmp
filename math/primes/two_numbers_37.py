"""
{1,2}-sequence patterns connected to the GF(37).

A = 112211, B = 121121, C = 211112 are the three base blocks.
Their digit sums, DR values, and mod-37 residues connect directly
to GF(37)'s core structure.
"""


def dr(n):
    n = abs(int(n))
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


A = "112211"
B = "121121"
C = "211112"
BLOCKS = {"A": A, "B": B, "C": C}

# ── Connect blocks to DR algebra ──────────────────────────────────────────────
print("BLOCK → INTEGER → DR → mod 37")
print("-" * 40)
for name, seq in BLOCKS.items():
    n = int(seq)
    d = dr(n)
    m = n % 37
    print(f"  {name} = {seq}  →  {n}  →  DR={d}  →  mod37={m}")

print()

# ── Digit sums ────────────────────────────────────────────────────────────────
print("DIGIT SUMS:")
for name, seq in BLOCKS.items():
    s = sum(int(c) for c in seq)
    print(f"  {name}: digit_sum={s}  DR(digit_sum)={dr(s)}")

print()

# ── Palindrome cycle A,B,C,C,B,A as integers mod 37 ──────────────────────────
cycle = ["A", "B", "C", "C", "B", "A"]
print("PALINDROME CYCLE mod 37:")
vals = [int(BLOCKS[x]) % 37 for x in cycle]
print("  " + "  ".join(f"{x}={v}" for x, v in zip(cycle, vals)))
print(f"  Sum mod 37 = {sum(vals) % 37}")
print(f"  DR(sum)    = {dr(sum(vals))}")

print()

# ── Substitution: 1→12, 2→21 (Thue-Morse) — connect to 137-map ──────────────
print("THUE-MORSE SUBSTITUTION → mod 37 at each generation:")
s = "1"
for gen in range(7):
    n = int(s[:12]) if len(s) >= 12 else int(s)
    print(f"  gen {gen}: len={len(s):>5}  prefix_12={s[:12]:<12}  mod37={n % 37}  DR={dr(n % 37)}")
    s = s.replace("1", "X").replace("2", "21").replace("X", "12")

print()

# ── Field simulation thresholds → DR → mod 37 ────────────────────────────────
print("FIELD THRESHOLDS IN DR ALGEBRA:")
print("  A node's threshold maps to a DR class, which maps to a column in GF(37)")
thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
print(f"  {'threshold':>10}  {'×37':>6}  {'int':>4}  {'DR':>3}  {'mod37':>6}")
for t in thresholds:
    scaled = t * 37
    n = int(scaled)
    print(f"  {t:>10.2f}  {scaled:>6.2f}  {n:>4}  {dr(n):>3}  {n % 37:>6}")

print()

# ── meta_evolve_lane multiplier sequence → mod 37 ────────────────────────────
print("META-EVOLVE MULTIPLIER SEQUENCE → mod 37:")
multipliers = [7, 3, 5, 8, 10, 5]
for m in multipliers:
    print(f"  multiplier={m}  mod37={m % 37}  DR={dr(m)}  in_primitive_roots={'yes' if m in {2,5,13,15,17,18,19,20,22,24,32,35} else 'no'}")

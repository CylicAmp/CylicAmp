"""
Alpha Odds and Even Grid
1234-(5)-6789

Position labels:
  LL = Left Low    LH = Left High
  RL = Right Low   RH = Right High
  O = Odd          E = Even
  (5) = A51 — center axis

Grid:
  1: LL-O    2: LL-E    3: LH-O    4: LH-E
  (5): A51
  6: RL-E    7: RL-O    8: RH-E    9: RH-O
"""

def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9

# ── Position map ───────────────────────────────────────────────────────────
GRID = {
    1: {"side": "L", "level": "L", "parity": "O", "label": "LL-O"},
    2: {"side": "L", "level": "L", "parity": "E", "label": "LL-E"},
    3: {"side": "L", "level": "H", "parity": "O", "label": "LH-O"},
    4: {"side": "L", "level": "H", "parity": "E", "label": "LH-E"},
    5: {"side": "C", "level": "C", "parity": "O", "label": "A51"},   # center axis
    6: {"side": "R", "level": "L", "parity": "E", "label": "RL-E"},
    7: {"side": "R", "level": "L", "parity": "O", "label": "RL-O"},
    8: {"side": "R", "level": "H", "parity": "E", "label": "RH-E"},  # AHL
    9: {"side": "R", "level": "H", "parity": "O", "label": "RH-O"},
}

# AHL / ALO from previous session
AHL = 8   # Alpha High — RH-E
ALO = 7   # Alpha Low  — RL-O

# ── OEOEOEOE pattern ──────────────────────────────────────────────────────
# 12 pairs cycling: OE OE OE OE
# 12 × 4 = 48 → DR = 12 → DR = 3

oe_pairs = 4
base = 12
product = base * oe_pairs        # 48
print(f"OEOEOEOE: {base} × {oe_pairs} = {product} → DR = {dr(product)}")

# ── 12+n sequence (DR cycle) ───────────────────────────────────────────────
print("\n12+n DR cycle:")
for n in range(1, 10):
    val = 12 + n
    print(f"  12+{n} = {val} → DR = {dr(val)}")

# ── LL/LH/RL/RH count sums ────────────────────────────────────────────────
# LLLLLL-HH = 6+2 = 8+4 = 12 → DR = 3+1 = 4
# RRRR-LL-LL = 4+3 = 6+4 = 10 → DR = 1+3 = 4
print()
print(f"LL+HH chain: 6+2={6+2}+4={6+2+4} → DR={dr(6+2+4)} → 3+1=4")
print(f"RR+LL chain: 4+3={4+3}+4={4+3+4} → DR={dr(4+3+4)} → 1+3=4")

# ── 46/64 mirror ──────────────────────────────────────────────────────────
print()
print(f"64 - 46 = {64-46} → DR = {dr(64-46)}")
print(f"46 - 64 = {46-64} → abs DR = {dr(abs(46-64))}")
print(f"AHL({AHL}) + ALO({ALO}) = {AHL+ALO} → DR = {dr(AHL+ALO)}")
print(f"AHL in grid: {GRID[AHL]['label']}")
print(f"ALO in grid: {GRID[ALO]['label']}")

# ── Print full grid ────────────────────────────────────────────────────────
print()
print("── Full Alpha Grid ─────────────────────────────────────────────────")
for n, g in GRID.items():
    marker = " ← AHL" if n == AHL else " ← ALO" if n == ALO else ""
    print(f"  {n}: {g['label']}{marker}")

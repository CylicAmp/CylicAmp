import numpy as np

A = "112211"
B = "121121"
C = "211112"

BLOCKS = [A, B, C]
BLOCK_NAME = {A: "A", B: "B", C: "C"}


def expand(n_rows):
    """Build the fractal row sequence by prepending blocks in palindrome order."""
    prefix_order = [A, B, C, C, B, A]  # one full palindrome cycle
    seq = A
    rows = [seq]
    i = 1
    while len(rows) < n_rows:
        prefix = prefix_order[i % len(prefix_order)]
        seq = prefix + seq
        rows.append(seq)
        i += 1
    return rows


def to_grid(s, width=None):
    """Convert a string of 1s and 2s to a numpy array."""
    arr = np.array([int(c) for c in s])
    if width:
        # tile to exact width
        reps = -(-width // len(arr))
        arr = np.tile(arr, reps)[:width]
    return arr


def substitute(s, rules):
    """Apply a substitution rule dict to a string: e.g. {'1':'12', '2':'21'}"""
    return "".join(rules[c] for c in s)


def tile_2d(row_pattern, col_pattern, rows, cols):
    """Build a 2D grid by tiling two 1D patterns."""
    r = to_grid(row_pattern, cols)
    c = to_grid(col_pattern, rows)
    return np.outer(c, r) % 3 + 1  # combine and keep in {1,2}


def print_grid(arr):
    for row in arr:
        print("".join(str(v) for v in row))


# ── Show the fractal expansion ────────────────────────────────────────────────
print("FRACTAL EXPANSION (prepend palindrome cycle):")
rows = expand(6)
for i, row in enumerate(rows):
    blocks = [row[j:j+6] for j in range(0, len(row), 6)]
    labels = " | ".join(BLOCK_NAME.get(b, "?") for b in blocks)
    print(f"  row {i+1}: {row}  [{labels}]")

print()

# ── Substitution rules ────────────────────────────────────────────────────────
print("SUBSTITUTION RULES (1→12, 2→21 — Thue-Morse style):")
s = "1"
for gen in range(6):
    print(f"  gen {gen}: {s}")
    s = substitute(s, {"1": "12", "2": "21"})

print()

print("SUBSTITUTION RULES (1→112211, 2→211112):")
s = "1"
for gen in range(3):
    print(f"  gen {gen}: {s}")
    s = substitute(s, {"1": A, "2": C})

print()

# ── 2D tiling from the base patterns ─────────────────────────────────────────
print("2D GRID — outer product of A with itself:")
a = to_grid(A)
grid = (np.outer(a, a) % 2) + 1
print_grid(grid)

print()
print("2D GRID — outer product of B with C:")
b = to_grid(B)
c = to_grid(C)
grid2 = (np.outer(b, c) % 2) + 1
print_grid(grid2)

print()

# ── The user's 4x8 pattern as a signal ───────────────────────────────────────
pattern = np.array([
    [1,1,2,2,2,2,1,1],
    [1,2,2,1,1,2,2,1],
    [1,2,2,1,1,2,2,1],
    [1,1,2,2,2,2,1,1],
])

print("ORIGINAL 4x8 PATTERN — autocorrelation (self-similarity measure):")
flat = (pattern.flatten() - 1).astype(float)  # map to {0,1}
autocorr = np.correlate(flat, flat, mode='full')
print("  " + " ".join(f"{int(v):3}" for v in autocorr[len(flat)-1:]))

print()
print("ROW DIFFERENCES (how each row relates to the next):")
for i in range(len(pattern)-1):
    diff = pattern[i+1] - pattern[i]
    print(f"  row {i} → row {i+1}: {diff}")

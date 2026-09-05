# math/theorems/lob_44_9_bilateral_369_lock.py
"""
MWS Forensic Audit — LoB 44.9
24-Digit Bilateral 369 Lock

Number: 369663933696639336966369
8 blocks of 3. 369 is bilateral seal — first and last block identical.

─────────────────────────────────────────────────────────────────────────────
BLOCK STRUCTURE
─────────────────────────────────────────────────────────────────────────────
  369 | 663 | 933 | 696 | 639 | 336 | 966 | 369
  DR:  9  |  6  |  6  |  3  |  9  |  3  |  3  |  9

─────────────────────────────────────────────────────────────────────────────
FULL LOCK
─────────────────────────────────────────────────────────────────────────────
  DS=138, DR=3, mod37=13, mod18=3, mod13=2, mod11=4, mod9=3

─────────────────────────────────────────────────────────────────────────────
/3 DESCENT
─────────────────────────────────────────────────────────────────────────────
  369663933696639336966369 ÷ 3 = 123221311232213112322123
  Quotient opens and closes with 123.  369 = 3 × 123.

─────────────────────────────────────────────────────────────────────────────
30-ECHO
─────────────────────────────────────────────────────────────────────────────
  Interior DR sum (blocks 2–7): 6+6+3+9+3+3 = 30
  23-digit shadow (first 23 digits) mod 37 = 30  ← same value
"""

def dr(n): return (n - 1) % 9 + 1 if n > 0 else 9
def ds(n): return sum(int(d) for d in str(n))

N_STR = '369663933696639336966369'
N = int(N_STR)
Q = N // 3
Q_STR = str(Q)

BLOCKS = [N_STR[i:i+3] for i in range(0, 24, 3)]
BLOCK_VALS = [int(b) for b in BLOCKS]

BLOCK_DS = [18, 15, 15, 21, 18, 12, 21, 18]
BLOCK_DR = [ 9,  6,  6,  3,  9,  3,  3,  9]

# ── Structure ──────────────────────────────────────────────────────────────────

assert len(N_STR) == 24
assert len(BLOCKS) == 8
assert BLOCKS[0] == BLOCKS[-1] == '369'   # bilateral seal

# ── Block audit ────────────────────────────────────────────────────────────────

for i, (b, expected_ds, expected_dr) in enumerate(zip(BLOCK_VALS, BLOCK_DS, BLOCK_DR)):
    assert ds(b) == expected_ds, f"Block {i+1} DS"
    assert dr(b) == expected_dr, f"Block {i+1} DR"

# DR fingerprint matches document
assert [dr(b) for b in BLOCK_VALS] == BLOCK_DR

# ── Full lock ──────────────────────────────────────────────────────────────────

assert ds(N) == 138
assert dr(N) == 3
assert N % 37 == 13
assert N % 18 == 3
assert N % 13 == 2
assert N % 11 == 4
assert N % 9  == 3

# DS consistency: sum of block DS values
assert sum(BLOCK_DS) == 138

# ── /3 descent ────────────────────────────────────────────────────────────────

assert N % 3 == 0
assert Q == 123221311232213112322123
assert len(Q_STR) == 24
assert Q_STR[:3]  == '123'   # opens with 123
assert Q_STR[-3:] == '123'   # closes with 123

assert 369 == 3 * 123        # trinity frame scales to its seed

# Quotient block structure mirrors input
Q_BLOCKS = [Q_STR[i:i+3] for i in range(0, 24, 3)]
assert Q_BLOCKS[0] == Q_BLOCKS[-1] == '123'

# ── 30-echo ────────────────────────────────────────────────────────────────────

# Interior DR sum: blocks 2–7 (indices 1–6)
interior_drs = BLOCK_DR[1:7]
assert interior_drs == [6, 6, 3, 9, 3, 3]
assert sum(interior_drs) == 30

# 23-digit shadow: first 23 digits
shadow = int(N_STR[:23])
assert shadow % 37 == 30              # shadow mod 37 = interior DR sum
assert shadow % 37 == sum(interior_drs)

# ── Additive structure ─────────────────────────────────────────────────────────

# Full DR fingerprint sum: 9+6+6+3+9+3+3+9 = 48, DR=3
assert sum(BLOCK_DR) == 48 and dr(48) == 3 == dr(N)

# Outer DRs (blocks 1 and 8): both 9
assert BLOCK_DR[0] == BLOCK_DR[7] == 9

# Interior sum 30: DR(30) = 3 = DR(N)
assert dr(30) == 3 == dr(N)

# 369 mod 37
assert 369 % 37 == 369 - 9*37    # 9*37=333, 369-333=36 → 369%37=36? let me just use %
assert 369 % 37 == 36
assert 123 % 37 == 12


if __name__ == "__main__":
    print("LoB 44.9 — 24-Digit Bilateral 369 Lock")
    print()
    print("Block structure:")
    print("  " + " | ".join(BLOCKS))
    print("  DS: " + " | ".join(f"{ds(int(b)):2d}" for b in BLOCKS))
    print("  DR: " + " | ".join(f" {dr(int(b))}" for b in BLOCKS))
    print()
    print(f"Full lock:  DS={ds(N)}  DR={dr(N)}  mod37={N%37}  mod18={N%18}  mod13={N%13}  mod11={N%11}")
    print()
    print(f"/3 descent: {N_STR}")
    print(f"         ÷3 {Q_STR}")
    print(f"  Opens: {Q_STR[:3]}  Closes: {Q_STR[-3:]}  (369 = 3 × 123)")
    print()
    print(f"30-echo: interior DRs {interior_drs}  sum={sum(interior_drs)}")
    print(f"  23-digit shadow mod 37 = {shadow % 37}  ← same")
    print()
    print("All assertions passed.")

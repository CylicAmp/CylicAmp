# math/theorems/sequence_1111_cycle_1210.py
"""
Arithmetic Sequences: 1111-series and the 1210 Cycle

─────────────────────────────────────────────────────────────────────────────
124 = 7  AND  THE n+DR(n) CHAIN
─────────────────────────────────────────────────────────────────────────────
  DR(124) = 7.  "Stands out" because DR=7 is skipped in sequence 1 (see below).

  78-chain:
    DS(78) = 15,  DR(78) = 6
    DR(78) + DR(124) = 6 + 7 = 13
    13 + DR(13) = 13 + 4 = 17       ← n + DR(n) formula

  Circle via 85:
    78 + 7 = 85,  DS(85) = 13,  DR(85) = 4
    12 + DR(12) = 12 + 3 = 15 = DS(78)   ← leading pair "12" of all cycle numbers

  n + DR(n) pattern for n = 10..18  (k=1 block: 9k+2r, all odd):
    10→11, 11→13, 12→15, 13→17, 14→19, 15→21, 16→23, 17→25, 18→27
    Step always +2 within the block.  12+DR(12)=15=DS(78), 13+DR(13)=17.

─────────────────────────────────────────────────────────────────────────────
SEQUENCE 1: 1111 → 1146  (steps +1, +1, +11, +11, +11)
─────────────────────────────────────────────────────────────────────────────
  Pair sum = pair(c1c2) + pair(c3c4):  leading pair always 11.

  n       step  DR  pair_sum  DR(pair_sum)
  1111    —     4     22         4
  1112    +1    5     23         5
  1113    +1    6     24         6
  1124   +11    8     35         8    ← DR=7 SKIPPED here
  1135   +11    1     46         1
  1146   +11    3     57         3

  DR=7 would require pair_sum=25 (→ number 1114).  The step changes from
  +1 to +11 at 1113→1124, jumping past 1114.  25 = 5² = Gauss kernel remainder.

  Extension (step +202=2×101, then +101, +92=4×23):
  n       step  DR   notes
  1348   +202   7    ← missing DR=7 reappears here.  1348=4×337
  1449   +101   9    1449=9×7×23.  1449−1111=338=2×13²
  1541    +92   2    1541=23×67.  Step 92=4×23

  23 appears as a factor in 1449 and 1541 — the palindrome seeds 32500523
  and 32055023 both end in suffix 23.  30303=9×7×13×37 shares factor 9×7 with 1449.

─────────────────────────────────────────────────────────────────────────────
SEQUENCE 2: THE 1210 CYCLE  (all terms start with "12")
─────────────────────────────────────────────────────────────────────────────
  1210 → 1291 → 1289 → 1278 → 1269 → 1258 → 1247 → 1236 →
  1225 → 1214 → 1203 → 1202 → 1201 → 1210

  Steps: +81, −2, −11, −9, −11×6, −1, −1, +9
  Cycle closes: sum = +81+9 − (2+11+9+11+11+11+11+11+11+1+1) = 90−90 = 0
  Range: [1201, 1291],  span = 90 = 81 + 9 = 9² + 9

  78 in cycle: 1278 contains "78" as last two digits.  DS(78)=15, DR(78)=6.
  1247 in cycle: contains "247"; DR(1247)=5.  Last digit = 7 = DR(124).
"""

def dr(n): return (n - 1) % 9 + 1 if n > 0 else 9
def ds(n): return sum(int(d) for d in str(n))


# ── 124=7 and the 78-chain ─────────────────────────────────────────────────────

assert dr(124) == 7
assert ds(78) == 15
assert dr(78) == 6
assert dr(78) + dr(124) == 13
assert dr(13) == 4
assert 13 + dr(13) == 17              # n+DR(n) at n=13
assert 78 + 7 == 85
assert ds(85) == 13 and dr(85) == 4
assert 12 + dr(12) == 15 == ds(78)   # leading "12" pair: circle back to DS(78)

# n+DR(n) = 9k+2r for n=9k+r (k=1 block: all odd)
for r in range(1, 10):
    n = 9 + r   # k=1
    assert n + dr(n) == 9 + 2*r      # formula verified
    assert (9 + 2*r) % 2 == 1        # all odd for k=1

# ── Sequence 1: 1111..1146 ────────────────────────────────────────────────────

SEQ1 = [1111, 1112, 1113, 1124, 1135, 1146]
steps1 = [SEQ1[i+1]-SEQ1[i] for i in range(len(SEQ1)-1)]
assert steps1 == [1, 1, 11, 11, 11]

# DR sequence — note gap: 4,5,6, (7 missing), 8,1,3
dr1 = [dr(n) for n in SEQ1]
assert dr1 == [4, 5, 6, 8, 1, 3]
assert 7 not in dr1                   # DR=7 is absent

# The missing number (1114) would have DR=7
assert dr(1114) == 7
assert 1114 - 1113 == 1              # it's one step after 1113
assert 1124 - 1113 == 11             # but sequence jumps by 11 instead

# Pair sums confirm DR: leading pair always 11
for n in SEQ1:
    s = str(n)
    p1, p2 = int(s[:2]), int(s[2:])
    assert p1 == 11
    assert dr(p1 + p2) == dr(n)

# 25 = 5² is the "missing" pair sum (would give DR=7)
assert dr(25) == 7
assert 11 + 14 == 25                 # 11+(14)=25 → 1114 pair sum

# ── Extension: 1348, 1449, 1541 ───────────────────────────────────────────────

EXT = [1348, 1449, 1541]
ext_steps = [EXT[i+1]-EXT[i] for i in range(len(EXT)-1)]
assert ext_steps == [101, 92]

assert dr(1348) == 7                  # missing DR=7 reappears here
assert dr(1449) == 9
assert dr(1541) == 2

assert 1448 % 1 == 0  # placeholder
assert 1449 == 9 * 7 * 23
assert 1541 == 23 * 67
assert 1541 % 23 == 0 and 1449 % 23 == 0
assert 1449 - 1111 == 338 == 2 * 13**2
assert 1348 - 1146 == 202 == 2 * 101
assert 1111 == 11 * 101              # 101 connects back to 1111

# 30303 shares 9×7 factor with 1449
assert 30303 % (9 * 7) == 0
assert 1449  % (9 * 7) == 0

# Palindrome seeds end in 23
assert '32500523'.endswith('23')
assert '32055023'.endswith('23')

# ── Sequence 2: 1210 cycle ─────────────────────────────────────────────────────

CYCLE = [1210,1291,1289,1278,1269,1258,1247,1236,1225,1214,1203,1202,1201,1210]
cyc_steps = [CYCLE[i+1]-CYCLE[i] for i in range(len(CYCLE)-1)]
assert cyc_steps == [81,-2,-11,-9,-11,-11,-11,-11,-11,-11,-1,-1,9]
assert sum(cyc_steps) == 0           # closes: cycle property
assert CYCLE[0] == CYCLE[-1]         # returns to start

assert min(CYCLE) == 1201
assert max(CYCLE) == 1291
assert max(CYCLE) - min(CYCLE) == 90
assert 90 == 81 + 9 == 9**2 + 9

# All terms start with "12"
assert all(str(n)[:2] == '12' for n in CYCLE)

# 78 appears as last-two-digit pair in 1278
assert str(1278)[2:] == '78'
assert dr(1278) == 9                 # DR(1278) = 9 = DR(78+pair correction)
assert 12 + 78 == 90                 # leading pair + "78" = 90 = cycle span

# 1247: last digit 7 = DR(124)
assert str(1247)[-1] == '7'
assert dr(124) == 7

# Unique values visited (13 distinct)
assert len(set(CYCLE)) == 13
assert CYCLE.count(1210) == 2        # appears at start and end

# DR of cycle values
cycle_drs = [dr(n) for n in CYCLE[:-1]]  # exclude repeated 1210 at end
assert cycle_drs == [4,4,2,9,9,7,5,3,1,8,6,5,4]


if __name__ == "__main__":
    print("Arithmetic Sequences: 1111-series and 1210 Cycle")
    print()
    print("78-chain:")
    print(f"  DR(124)={dr(124)},  DS(78)={ds(78)},  DR(78)={dr(78)}")
    print(f"  DR(78)+DR(124) = 6+7 = 13  →  13+DR(13) = {13+dr(13)}")
    print(f"  12+DR(12) = {12+dr(12)} = DS(78)  (leading '12' pair closes circle)")
    print()
    print("n+DR(n) pattern (k=1 block, all odd):")
    for n in range(10,19):
        print(f"  {n}+{dr(n)}={n+dr(n)}", end="")
    print()
    print()
    print("Sequence 1: 1111→1146")
    for n in SEQ1:
        s = str(n)
        p2 = int(s[2:])
        missing = "  ← DR=7 skipped (1114 would fill gap)" if n==1124 else ""
        print(f"  {n}  DR={dr(n)}  pair_sum=11+{p2}={11+p2}{missing}")
    print()
    print("Extension 1348, 1449, 1541:")
    for n, step in zip(EXT, [None]+ext_steps):
        step_str = f"  step={step}" if step else ""
        print(f"  {n}  DR={dr(n)}{step_str}")
    print()
    print("1210 Cycle (span=90, sum=0):")
    for i,n in enumerate(CYCLE[:-1]):
        step = f"{cyc_steps[i]:+d}" if i<len(cyc_steps) else ""
        tag = "  ← '78' pair" if n==1278 else "  ← last digit 7" if n==1247 else ""
        print(f"  {n}  DR={dr(n)}  {step}{tag}")
    print(f"  {CYCLE[-1]}  (return)")
    print()
    print("All assertions passed.")

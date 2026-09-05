"""
mod37_slot_audit.py

Framework numbers mapped into Z/37Z (slot table) and their relationships.

─────────────────────────────────────────────────────────────────
SLOT TABLE (n mod 37):

  Constant   Value      mod 37   Interpretation
  ─────────  ─────────  ──────   ──────────────────────────────
  37         37         0        Field zero (37≡0)
  18         18         18       Center element ((37−1)/2)
  191        191        6        Seed → slot 6
  142857     142857     0        Null element (37×3861; 142857×7=999999)
  137        137        26       Slot 26
  248        248        26       137+111 = 248; same slot as 137
  359        359        26       137+222 = 359; same slot as 137

DESCENT 191→100 THROUGH Z/37Z:
  Terms:  191, 188, 177, 166, 155, 144, 133, 122, 111, 100
  Slots:  [6,  3,   29,  18,  7,   33,  22,  11,  0,   26]
  Notable:
    slot 18 (CENTER)  at term 166 (index 3)
    slot 11 (repunit_2 mod 37) at term 122 (index 7)
    slot  0 (FIELD ZERO) at term 111 (index 8)
    slot 26 at term 100 (index 9) — same slot as 137, 248, 359

KEY FACTS:
  (S1) Repunit mod 37 has period 3: 1→11→0→1→11→0…
       repunit_1 ≡ 1, repunit_2 ≡ 11, repunit_3 ≡ 0 (mod 37).

  (S2) Descent step −11 ≡ 26 (mod 37).
       The descent step equals the slot of the endpoint (100 mod 37 = 26).

  (S3) Slot difference top-to-bottom: (6 − 26) mod 37 = 17.
       17 is a criss-cross prime (DR(17)=8, DR(71)=8; 17+71=88 DR=7).

  (S4) 100 mod 37 = 26 = 137 mod 37; 137 − 100 = 37 exactly.
       100 and 137 occupy the same slot; they differ by the modulus.

  (S5) 2×18 = 36 ≡ −1 (mod 37): the center element is the square root of −1
       modulo 37 (in the sense 18² ≡ 324 ≡ 324−8×37=324−296=28; actually
       18≡−19, so 18²=361≡361−9×37=361−333=28; but 18=(37−1)/2 satisfies
       2·18=36≡−1, i.e. it is the "half-field" element).

  (S6) Discrete logarithms base 2 mod 37:
       2^27 ≡ 6  (mod 37)  → slot 6  is at log position 27
       2^17 ≡ 18 (mod 37)  → slot 18 is at log position 17
       2^12 ≡ 26 (mod 37)  → slot 26 is at log position 12
─────────────────────────────────────────────────────────────────
"""

from sympy import factorint, isprime
from math import gcd

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = n % 9
    return r if r else 9


# ── Slot table entries ────────────────────────────────────────────────────────

TABLE = [
    (37,     0,  "37 ≡ 0 (field zero)"),
    (18,     18, "18 ≡ 18 (center)"),
    (191,    6,  "191 ≡ 6 (seed slot)"),
    (142857, 0,  "142857 ≡ 0 (null element)"),
    (137,    26, "137 ≡ 26"),
    (248,    26, "248 ≡ 26 (137+111)"),
    (359,    26, "359 ≡ 26 (137+222)"),
]

for value, expected_slot, label in TABLE:
    check(value % 37 == expected_slot, label, value % 37, expected_slot)


# ── Slot 26 cluster: additions of 111 preserve slot ──────────────────────────

check(137 % 37 == 26, "137 mod 37 = 26", 137 % 37, 26)
check((137 + 111) % 37 == 26, "(137+111) mod 37 = 26", (137 + 111) % 37, 26)
check((137 + 222) % 37 == 26, "(137+222) mod 37 = 26", (137 + 222) % 37, 26)
check(248 - 137 == 111, "248-137 = 111", 248 - 137, 111)
check(359 - 248 == 111, "359-248 = 111", 359 - 248, 111)
check(factorint(111) == {3: 1, 37: 1}, "111 = 3×37", factorint(111), {3: 1, 37: 1})


# ── 18 as center element ──────────────────────────────────────────────────────

check(18 == (37 - 1) // 2, "18 = (37-1)/2", 18, (37 - 1) // 2)
check(2 * 18 % 37 == 36, "2×18 ≡ 36 ≡ -1 (mod 37)", 2 * 18 % 37, 36)
check(36 % 37 == 37 - 1, "36 ≡ -1 (mod 37)", 36 % 37, 37 - 1)


# ── 142857: null element ──────────────────────────────────────────────────────

check(142857 % 37 == 0, "142857 ≡ 0 (mod 37)", 142857 % 37, 0)
check(142857 // 37 == 3861, "142857 = 37×3861", 142857 // 37, 3861)
check(142857 * 7 == 999999, "142857×7 = 999999", 142857 * 7, 999999)
check(dr(142857) == 9, "DR(142857) = 9", dr(142857), 9)


# ── S1: Repunit mod 37 — period 3 ────────────────────────────────────────────

def repunit(n):
    return int("1" * n)

check(repunit(1) % 37 == 1,  "repunit_1 ≡ 1 (mod 37)",  repunit(1) % 37, 1)
check(repunit(2) % 37 == 11, "repunit_2 ≡ 11 (mod 37)", repunit(2) % 37, 11)
check(repunit(3) % 37 == 0,  "repunit_3 ≡ 0 (mod 37)",  repunit(3) % 37, 0)
check(repunit(4) % 37 == 1,  "repunit_4 ≡ 1 (mod 37)",  repunit(4) % 37, 1)
check(repunit(5) % 37 == 11, "repunit_5 ≡ 11 (mod 37)", repunit(5) % 37, 11)
check(repunit(6) % 37 == 0,  "repunit_6 ≡ 0 (mod 37)",  repunit(6) % 37, 0)

# Period 3 holds for n = 1..12
for n in range(1, 13):
    r = repunit(n) % 37
    expected = [1, 11, 0][(n - 1) % 3]
    check(r == expected, f"repunit_{n} mod 37 = {expected}", r, expected)


# ── Descent 191→100 mod 37 ───────────────────────────────────────────────────

DESCENT = [191] + [188 - 11 * k for k in range(9)]
check(len(DESCENT) == 10, "descent length = 10", len(DESCENT), 10)
check(DESCENT[0] == 191, "descent[0] = 191", DESCENT[0], 191)
check(DESCENT[-1] == 100, "descent[-1] = 100", DESCENT[-1], 100)

EXPECTED_SLOTS = [6, 3, 29, 18, 7, 33, 22, 11, 0, 26]
ACTUAL_SLOTS = [t % 37 for t in DESCENT]
check(ACTUAL_SLOTS == EXPECTED_SLOTS, "descent slots", ACTUAL_SLOTS, EXPECTED_SLOTS)

# Notable slots in descent
check(DESCENT[3] == 166 and ACTUAL_SLOTS[3] == 18, "term 166 → slot 18 (CENTER)",
      (DESCENT[3], ACTUAL_SLOTS[3]), (166, 18))
check(DESCENT[7] == 122 and ACTUAL_SLOTS[7] == 11, "term 122 → slot 11 (repunit_2)",
      (DESCENT[7], ACTUAL_SLOTS[7]), (122, 11))
check(DESCENT[8] == 111 and ACTUAL_SLOTS[8] == 0, "term 111 → slot 0 (FIELD ZERO)",
      (DESCENT[8], ACTUAL_SLOTS[8]), (111, 0))
check(DESCENT[9] == 100 and ACTUAL_SLOTS[9] == 26, "term 100 → slot 26",
      (DESCENT[9], ACTUAL_SLOTS[9]), (100, 26))


# ── S2: Descent step −11 ≡ 26 (mod 37) ──────────────────────────────────────

check((-11) % 37 == 26, "-11 ≡ 26 (mod 37)", (-11) % 37, 26)
check(100 % 37 == 26, "100 mod 37 = 26 (descent step = slot of endpoint)", 100 % 37, 26)

# First step 191→188 is -3; remaining steps are -11 ≡ +26 (mod 37)
check(DESCENT[1] - DESCENT[0] == -3, "first step = -3 (191→188)", DESCENT[1] - DESCENT[0], -3)
check((ACTUAL_SLOTS[1] - ACTUAL_SLOTS[0]) % 37 == (-3) % 37,
      "slot step 0→1 = -3 mod 37", (ACTUAL_SLOTS[1] - ACTUAL_SLOTS[0]) % 37, (-3) % 37)

for i in range(1, len(DESCENT) - 1):
    delta = (ACTUAL_SLOTS[i + 1] - ACTUAL_SLOTS[i]) % 37
    check(delta == 26, f"slot step {i}→{i+1} = 26", delta, 26)


# ── S3: Slot difference top-to-bottom = 17 ───────────────────────────────────

slot_top = ACTUAL_SLOTS[0]   # 6
slot_bot = ACTUAL_SLOTS[-1]  # 26
slot_diff = (slot_top - slot_bot) % 37
check(slot_top == 6, "slot(191) = 6", slot_top, 6)
check(slot_bot == 26, "slot(100) = 26", slot_bot, 26)
check(slot_diff == 17, "slot(191) - slot(100) ≡ 17 (mod 37)", slot_diff, 17)
check(isprime(17), "17 is prime", isprime(17), True)
check(dr(17) == 8, "DR(17) = 8 (criss-cross prime)", dr(17), 8)
check(dr(71) == 8, "DR(71) = 8 (criss-cross prime)", dr(71), 8)


# ── S4: 100 and 137 share slot 26; differ by 37 ──────────────────────────────

check(100 % 37 == 26, "100 mod 37 = 26", 100 % 37, 26)
check(137 % 37 == 26, "137 mod 37 = 26", 137 % 37, 26)
check(137 - 100 == 37, "137 - 100 = 37 (exactly one modulus)", 137 - 100, 37)


# ── S5: center element properties ────────────────────────────────────────────

# 18 + 18 = 36 ≡ -1 (mod 37)
check((18 + 18) % 37 == 36, "18+18 ≡ 36 ≡ -1 (mod 37)", (18 + 18) % 37, 36)
# 18 is at descent index 3 (term 166)
check(166 % 37 == 18, "166 mod 37 = 18", 166 % 37, 18)


# ── S6: Discrete logarithms base 2 mod 37 ────────────────────────────────────

# 2 is primitive root mod 37
check(pow(2, 27, 37) == 6,  "2^27 ≡ 6  (mod 37)", pow(2, 27, 37), 6)
check(pow(2, 17, 37) == 18, "2^17 ≡ 18 (mod 37)", pow(2, 17, 37), 18)
check(pow(2, 12, 37) == 26, "2^12 ≡ 26 (mod 37)", pow(2, 12, 37), 26)

# Log positions of key slots
log_positions = {}
for k in range(36):
    log_positions[pow(2, k, 37)] = k
check(log_positions[6]  == 27, "log₂(6)  = 27", log_positions[6], 27)
check(log_positions[18] == 17, "log₂(18) = 17", log_positions[18], 17)
check(log_positions[26] == 12, "log₂(26) = 12", log_positions[26], 12)

# Log of slot 17 (criss-cross slot diff)
check(log_positions[17] in range(36), "log₂(17) exists", log_positions[17], log_positions[17])


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Mod 37 Slot Audit")
    print("=" * 62)

    print("\n── Slot table ──")
    for value, expected_slot, label in TABLE:
        print(f"  {value:>8}  mod 37 = {value % 37:2d}  {label}")

    print("\n── S1: Repunit mod 37 (period 3) ──")
    for n in range(1, 7):
        print(f"  repunit_{n} = {'1'*n:>6}  mod 37 = {repunit(n) % 37}")

    print("\n── Descent 191→100 through Z/37Z ──")
    notable = {3: "CENTER", 7: "repunit_2", 8: "FIELD ZERO", 9: "slot 26"}
    for i, (t, s) in enumerate(zip(DESCENT, ACTUAL_SLOTS)):
        note = f"  ← {notable[i]}" if i in notable else ""
        print(f"  index {i}:  {t:3d}  mod 37 = {s:2d}{note}")

    print("\n── S2: Step −11 ≡ 26 (mod 37) ──")
    print(f"  -11 mod 37 = {(-11) % 37}")
    print(f"  100 mod 37 = {100 % 37}  (descent endpoint = descent step mod 37)")

    print("\n── S3: Slot difference 191→100 ──")
    print(f"  slot(191) = {slot_top},  slot(100) = {slot_bot}")
    print(f"  ({slot_top} - {slot_bot}) mod 37 = {slot_diff}  (criss-cross prime)")
    print(f"  DR(17) = {dr(17)},  DR(71) = {dr(71)}")

    print("\n── S4: 100 and 137 same slot ──")
    print(f"  100 mod 37 = {100 % 37}")
    print(f"  137 mod 37 = {137 % 37}")
    print(f"  137 - 100 = {137 - 100} = 37 exactly")

    print("\n── S6: Discrete log positions ──")
    print(f"  log₂(6)  mod 37 = {log_positions[6]}   (slot of 191)")
    print(f"  log₂(18) mod 37 = {log_positions[18]}   (CENTER)")
    print(f"  log₂(26) mod 37 = {log_positions[26]}   (slot of 100, 137, 248, 359)")
    print(f"  log₂(17) mod 37 = {log_positions[17]}   (slot diff)")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")

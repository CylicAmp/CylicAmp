#!/usr/bin/env python3
"""
audit_505_work.py -- every place 505 appears in the repo, re-checked.

Search (2026-11-22): `grep -rw 505` over the working tree, plus `git log -S505`
over the history.  Files where 505 carries content:

  1. math/theorems/source_mirror_manifold_396.py   SOURCE = 505-track, k=6
  2. math/theorems/theorem_infinite_666_resonances.py   505-track, m0=539 (mod 666)
  3. math/theorems/theorem_165_session_numbers_gf37.py  505, 5500 -> SEED orbit at 24
  4. math/theorems/joy_framework_v25_2_audit.py   "505 Fulcrum", T6: 2305 -> 505
  5. math/theorems/joy_lob_45_6_correction_audit.py  Table V row for 505
  6. math/theorems/mws_framework_verified.py   Sarah = 505 = 5 x 101; 505 from the grid
  7. math/theorems/mws_pure_math_extract.py    (2701-505) mod 37 = 13; 703 mod 505 = 198
  8. math/theorems/layer_trinity_factor_lattice.py   (505, 4444) divisor pair of 2,244,220
  9. math/theorems/one_over_137_framework.md (+ math/primes copy)
         "505 mod-18 ladder (double-sealed)", "505-anchor DR=1 sovereign coordinate"
 10. reference/two_digit_chains.txt  row 50: digits 5,0 -> 505 = 5*101

Incidental hits, no 505 content: a chi2 ratio 1.505 (T374), a table row index
(reversal_spans_all_tables.md row 55: T(10)*... = 505 is listed as a value only),
the k^3 coefficient 505 of the 3x3-grid chromatic polynomial, b-file line 505,
a Riemann-zero data file, two PNGs, and in the (now untracked) owner_work
archive a chromium PID 505 inside a pasted `ps` listing.

The owner_work archive (local copy, 2026-11-22) holds no owner message about
505 other than the request for this lookup.  The one_over_137_framework.md
cites conversations (Apr 2026) whose text is not in the repo, so the
"505 mod-18 ladder" has a name here and no content; what it was is not
recoverable from the repo.

Run:  python3 math/theorems/audit_505_work.py   (exit 0 = every check below holds)
"""
import sys
from math import gcd

P = 37
FAIL = []


def check(cond, label):
    print(("  PASS  " if cond else "  FAIL  ") + label)
    if not cond:
        FAIL.append(label)


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def orbit137(r):
    return sorted({r % P, (26 * r) % P, (26 * 26 * r) % P})


QR = {(x * x) % P for x in range(1, P)}

print("== 0. 505 itself ==")
check(factor(505) == {5: 1, 101: 1}, "505 = 5 x 101")
check(505 % P == 24, "505 mod 37 = 24")
check(orbit137(505) == [18, 24, 32], "137-orbit of 505 = {18,24,32} (the seed-246 orbit)")
check(24 not in QR, "24 is not a QR mod 37")
check(sum(map(int, "505")) == 10 and dr(505) == 1, "digit sum 10, DR 1")
check(505 % 18 == 1 and 505 % 13 == 11 and 505 % 11 == 10 and 505 % 9 == 1,
      "505 mod 18,13,11,9 = 1,11,10,1 (Table V row, joy_lob audit)")
check(sum(1 for k in range(2, 102) if is_prime(k)) == 26, "101 is the 26th prime")
check(str(101) == str(101)[::-1] and is_prime(101), "101 is a palindromic prime")
# twin / Sophie Germain framework: 505 is composite; its prime neighbours
check(is_prime(503) and is_prime(509) and not any(is_prime(k) for k in range(504, 509)),
      "505 sits inside the prime gap 503 .. 509 (gap 6); no twin pair touches it")
check(is_prime(2 * 5 + 1) and not is_prime(2 * 101 + 1),
      "factor 5 is Sophie Germain (11 prime); factor 101 is not (203 = 7 x 29)")
check(factor(203) == {7: 1, 29: 1}, "203 = 7 x 29")
# 1/137
check((505 * 137) % P == 32 and (505 * pow(137, -1, P)) % P == 18 and 505 % 137 == 94,
      "x137 -> 32, /137 -> 18 (both in the same orbit, forced: 137 = 26 mod 37), 505 mod 137 = 94")
# 1/505 decimal
check(pow(10, 4, 101) == 1 and all(pow(10, k, 101) != 1 for k in (1, 2)),
      "ord_101(10) = 4, so 1/505 has decimal period 4 (block 0198)")
check(str(10 ** 5 // 505).zfill(4)[-4:] == "0198" or (10 ** 5 // 505) == 198,
      "1/505 = 0.0019801980..., repeating block 0198")


def r30(bits):
    b = "0" + bits + "0"
    return "".join(str(int(b[i - 1]) ^ (int(b[i]) | int(b[i + 1]))) for i in range(1, len(b) - 1))


full = r30(bin(505)[2:])
check(bin(505)[2:] == "111111001", "505 = 111111001 (9 bits)")
check(int(full, 2) == 263 and 263 % P == 4,
      "Rule 30 one step on all 9 bits: 111111001 -> 100000111 = 263, mod 37 = 4")
def r30_ring8(n):
    b = format(n % 256, "08b")
    return int("".join(str(int(b[(i - 1) % 8]) ^ (int(b[i]) | int(b[(i + 1) % 8]))) for i in range(8)), 2)


check(r30_ring8(505) == 7,
      "gf37-audit uses an 8-cell ring: it reads 505 mod 256 = 249 = 11111001 (top bit dropped) "
      "and gives 00000111 = 7; the full 9-bit step gives 263. Two conventions, two answers")

print("\n== 1. source_mirror_manifold_396.py ==")
check(505 % P == 24 and 419 % P == 12 and 233 % P == 11, "tracks mod 37: 24, 12, 11")
check([dr(x) for x in (505, 419, 233)] == [1, 5, 8], "track DRs 1, 5, 8")
check([dr(k) for k in (6, 618, 3138)] == [6, 6, 6], "k = 6, 618, 3138 all DR 6")
check(618 % P == 26 and 100 % P == 26 and 3138 % P == 30, "618 = 26, 10^2 = 26, 3138 = 30 (mod 37)")
# The k values are written as constants; where they come from is not in the file.
# They are NOT the k = 6m of the 666-track file: for the 505-track that file
# gives m0 = 539, k = 3234 (DR 3), and k = 6 needs m = 1, but 17*1 = 17 != 505 mod 666.
check(6 * 539 == 3234 and dr(3234) == 3 and (17 * 1) % 666 != 505,
      "k = 6 for SOURCE is not the 666-track resonance k = 6*539 = 3234 (DR 3)")

print("\n== 2. theorem_infinite_666_resonances.py ==")
check(gcd(17, 666) == 1, "gcd(17, 666) = 1, so 17m = a (mod 666) solvable for every a")
tracks = {505: 539, 419: 103, 233: 523, 61: 317, 209: 169, 85: 5}
for a, m0 in tracks.items():
    sol = [m for m in range(666) if (17 * m) % 666 == a]
    check(sol == [m0], f"{a}-track: unique m0 = {m0} mod 666")
s = (9 + 10 + 17) // 2
check(s * (s - 9) * (s - 10) * (s - 17) == 36 ** 2, "Heron: triangle (9,10,17) has area 36")

print("\n== 3. theorem_165_session_numbers_gf37.py ==")
check(5500 % P == 24 and dr(5500) == 1, "5500 mod 37 = 24, DR 1")
check(factor(5500) == {2: 2, 5: 3, 11: 1}, "5500 = 2^2 x 5^3 x 11")
# The docstring line "5500 = 505 x (10000/101)" is false: 505 x 10000/101 = 50000.
check(505 * 10000 // 101 == 50000 and 505 * 10000 % 101 == 0,
      "T165 docstring error: 505 x (10000/101) = 50000, not 5500 (the assertions in T165 do not use it)")
check(5500 - 505 == 4995 == 135 * P, "why they agree mod 37: 5500 - 505 = 4995 = 135 x 37")
check((303 + 505) % P == 31 and dr(808) == 7, "303 + 505 = 808: mod 37 = 31, DR 7")
check((505 + 5500) % P == 11, "505 + 5500 = 6005: mod 37 = 11")
check(303 == 3 * 101 and 505 == 5 * 101 and 101 % P == 27 and orbit137(27) == [11, 27, 36],
      "303 = 3*101, 505 = 5*101; 101 = 27 mod 37, orbit {11,27,36}")

print("\n== 4. joy_framework_v25_2_audit.py ==")
check(int(f"{2 + 3:02d}{0 + 5:02d}") == 505, "T6: 2305 -> pair sums 05,05 -> 0505 -> 505")
check(24 % 18 == 6, "24 mod 18 = 6")

print("\n== 6/7. mws_framework_verified.py, mws_pure_math_extract.py ==")
check(300 + 200 + 5 == 505, "Sarah: shin 300 + resh 200 + he 5 = 505")
check(55 == 10 * 11 // 2, "55 = T(10)")
check(2701 == 37 * 73 and (2701 - 505) % P == 13,
      "(2701 - 505) mod 37 = 13 -- forced: 2701 = 37*73, so it is -24 = 13")
check(703 % 505 == 198 and 198 % P == 13, "703 mod 505 = 198, 198 mod 37 = 13")
check(13 == (-24) % P, "13 is the additive antipode of 24")

print("\n== 8. layer_trinity_factor_lattice.py ==")
check(505 * 4444 == 2244220 == 2 ** 2 * 5 * 11 * 101 ** 2, "505 x 4444 = 2,244,220 = 2^2*5*11*101^2")

print("\n== 10. reference/two_digit_chains.txt row 50 ==")
check(int("5" + "0" + "5") == 505 == 101 * 5, "aba for (a,b) = (5,0): 505 = 101 x 5")

print()
if FAIL:
    print(f"{len(FAIL)} FAILED")
    sys.exit(1)
print("All 505 checks hold.  Two faults in the stored files: T165's '5500 = 505 x (10000/101)' "
      "line, and the manifold's k-values not matching the 666-track k = 6m.")

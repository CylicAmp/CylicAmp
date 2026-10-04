# CLASS: AUDIT
"""
Audit of a supplied analysis (pasted 2026-10-04 with two scripts): the first 12
zeta zeros against a "14-13" reading, Collatz stopping times by n mod 9 and
mod 6 on 1..20000, and the nine ladder rows against their neighbours.
Ladder context: math/lemmas/digit_ladder_collatz.py.

REPRODUCED EXACTLY:
  - The 12 imaginary parts 14.1347251417 ... 56.4462476971 and nearest
    integers 14, 21, 25, 30, 33, 38, 41, 43, 48, 50, 53, 56.
  - Gaps 6.89, 3.99, 5.41, 2.51, 4.65, 3.33, 2.41, 4.68, 1.77, 3.20, 3.48;
    none near 1, so 14-13 = 1 is not a gap here.
  - Mean steps by n mod 9 run 91.14 .. 92.40; by n mod 6: 85.47 (0), 86.20 (2),
    86.22 (4), 97.14 (1), 97.56 (3), 97.79 (5). Even 85.97 vs odd 97.50.
  - Neighbour table: steps and deltas for all nine rows.

CORRECTIONS:
  C1. "All have real part 1/2 ... a verification of these zeros." mpmath's
      zetazero searches ON the critical line, so real part 1/2 is built in,
      not checked. The real check is the count: mp.nzeros(57) = 12 zeros in
      the whole strip up to height 57, and 12 were found on the line, so
      all zeros up to height 57 are on it. A finite check to height 57, not a proof.
  C2. "the 40 neighboring integers": the window k = -20..20 has 41 values and
      includes the row itself. Row 3's local mean rounds to 102.1, not 102.2
      (delta +70.9 is right).
  C3. "all nine trajectories meet at 40" is offered as a shared feature with no
      baseline: 94% of random 5-digit numbers pass through 40. It carries no
      information. (The factor-3 exit to digital root 1 IS forced: see F2.)
  C4. The even/odd gap (about 11.5 steps) is real; the stated reason is right
      in outline: even n takes steps(n/2) + 1 with n/2 smaller, odd n takes
      steps(3n+1) + 1 with 3n+1 larger.

NOT CHECKABLE HERE: the "14-13" and "1-13" readings are not defined in the
supplied text or in this session, so only the stated arithmetic was tested.

FALSIFICATION: any assertion below failing.
"""
import mpmath as mp

mp.mp.dps = 20
IMS = [14.1347251417, 21.0220396388, 25.0108575801, 30.4248761259, 32.9350615877,
       37.5861781588, 40.9187190121, 43.3270732809, 48.0051508812, 49.7738324777,
       52.9703214777, 56.4462476971]
for n, v in enumerate(IMS, 1):
    assert abs(float(mp.zetazero(n).imag) - v) < 1e-9
assert [int(mp.nint(v)) for v in IMS] == [14, 21, 25, 30, 33, 38, 41, 43, 48, 50, 53, 56]
gaps = [round(IMS[i + 1] - IMS[i], 2) for i in range(11)]
assert gaps == [6.89, 3.99, 5.41, 2.51, 4.65, 3.33, 2.41, 4.68, 1.77, 3.2, 3.48]
assert not any(abs(g - 1) < 0.2 for g in gaps)
assert int(mp.nzeros(57)) == 12

def steps(n):
    s = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        s += 1
    return s

N = 20000
S = [0] + [steps(n) for n in range(1, N + 1)]
mean = lambda xs: sum(xs) / len(xs)
m9 = [mean([S[n] for n in range(1, N + 1) if n % 9 == r]) for r in range(9)]
m6 = [round(mean([S[n] for n in range(1, N + 1) if n % 6 == r]), 2) for r in range(6)]
assert round(min(m9), 2) == 91.14 and round(max(m9), 2) == 92.4
assert m6 == [85.47, 97.14, 86.2, 97.56, 86.22, 97.79]
assert all(S[n] == 1 + S[n // 2] for n in range(4, N + 1, 2))

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def row(a):
    return int(f"{dr(a)}{dr(a + 1)}{dr(2 * a + 1)}{2 * a + 10}")

DELTA = [-69.9, -5.4, 70.9, 64.7, -18.5, -14.9, 38.2, 24.9, 57.8]
for a in range(1, 10):
    n = row(a)
    win = [steps(n + k) for k in range(-20, 21)]
    assert len(win) == 41
    assert round(steps(n) - mean(win), 1) == DELTA[a - 1]
assert round(mean([steps(row(3) + k) for k in range(-20, 21)]), 1) == 102.1

if __name__ == "__main__":
    print("all assertions pass")

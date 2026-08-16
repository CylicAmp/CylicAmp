"""
Theorem 220: Reversal Ladder — 2357, 291-Step Climb, and the 99² Lock

STRUCTURE:
  2357 = concat(2,3,5,7) — first four primes — and is itself prime.
  Split 23|57: DR(23)=5, DR(57)=3, 5+3=8=DR(2357)=DR(80).

  213(2)527: first four primes 2,3,5,7 with interleaved gaps 1,2,2.
  The parenthesized 2 is the first repeated gap — the twin-gap collision.

REVERSAL LADDER (first column climbs by 291):
  9381 | 1839     DR(9381) = 3      n+rev = 11220
  9672 | 2769     DR(9672) = 6      n+rev = 12441
  9963 | 3699     DR(9963) = 9      n+rev = 13662
  ---- : lock at 9963 ↔ 9936 ----
  9936 | 6399     DR(9936) = 9

  Increment 291 = 3 × 97, DR = 3 → DR ladder steps 3→6→9.
  Sum increment = 1221 = 3 × 11 × 37 (palindromic; carries 37).
  Gap decrement = -639 each rung.

LOCK:
  gap(9963) = 9963 - 3699 = 6264
  gap(9936) = 9936 - 6399 = 3537
  6264 + 3537 = 9801 = 99²

  The complementary gaps of the 2-cycle sum to 99².

KAPREKAR DEGENERACY:
  9963 has non-increasing digits (9,9,6,3): its reversal is its ascending sort.
  9963 - 3699 = 6264 is a genuine Kaprekar step.
  9936 is not sorted: Kaprekar step is again 9963 - 3699 = 6264.
  Both members of the 2-cycle collapse to the same Kaprekar successor.

MOD 37:
  291 ≡ 32 ≡ -5 (mod 37)
  Column-1 residues: 9381 ≡ 20,  9672 ≡ 15,  9963 ≡ 10
  Sequence: 20 → 15 → 10  (decreasing by 5 = -291 mod 37 each rung)
  Terminal residue 10 ∈ H = {1, 10, 26}  (sovereign kernel of GF(37)*)
  9936 ≡ 20 (mod 37): 9936 branch stays outside H.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H = {1, 10, 26}    # kernel of GF(37)*


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def digital_root(n):
    n = abs(n)
    if n == 0:
        return 0
    r = n % 9
    return 9 if r == 0 else r


def rev(n):
    return int(str(n)[::-1])


def kaprekar_step(n):
    digits = sorted(str(n), reverse=True)
    desc = int("".join(digits))
    asc  = int("".join(reversed(digits)))
    return desc - asc


def ladder(start, step=291, max_rungs=6):
    rungs = []
    n = start
    for _ in range(max_rungs):
        r = rev(n)
        rungs.append((n, r))
        n_next = n + step
        if len(str(n_next)) != 4:
            break
        n = n_next
    return rungs


def run():
    print("=" * 70)
    print("THEOREM 220: REVERSAL LADDER — 2357, 291-STEP CLIMB, 99² LOCK")
    print("=" * 70)

    # 2357 primality and concatenation
    print(f"\n2357: first four primes concatenated")
    primes4 = [2, 3, 5, 7]
    concat = int("".join(str(p) for p in primes4))
    assert concat == 2357
    assert is_prime(2357), "2357 should be prime"
    print(f"  concat(2,3,5,7) = {concat},  prime? {is_prime(concat)}")

    # DR split
    left, right = 23, 57
    dr_l, dr_r = digital_root(left), digital_root(right)
    dr_full = digital_root(2357)
    dr_sum = digital_root(2357 + 57)   # sum context
    print(f"\nDR split 23|57:")
    print(f"  DR(23) = {dr_l},  DR(57) = {dr_r},  sum = {dr_l + dr_r}")
    print(f"  DR(2357) = {dr_full}  [= DR(2+3+5+7=17) = DR(17) = {digital_root(17)}]")
    print(f"  23 + 57 = 80,  DR(80) = {digital_root(80)}")
    assert dr_l + dr_r == 8 and dr_full == 8

    # Gap structure 213(2)527
    print(f"\n213(2)527 — primes with interleaved gaps:")
    gaps = [3-2, 5-3, 7-5]
    print(f"  2 <{gaps[0]}> 3 <{gaps[1]}> 5 <{gaps[2]}> 7")
    print(f"  Gaps: {gaps}  — gap=2 repeats: first twin-gap collision")

    # The reversal ladder
    print(f"\nReversal Ladder (step = 291):")
    start = 9381
    rungs = ladder(start)

    sum_prev = None
    for n, r in rungs:
        s = n + r
        gap = n - r
        dr_n = digital_root(n)
        incr = f"  (+{s - sum_prev})" if sum_prev is not None else ""
        print(f"  {n} | {r:4d}   DR={dr_n}  gap={gap}  sum={s}{incr}")
        sum_prev = s

    # Verify 291 properties
    print(f"\n291 = 3 × 97,  prime(97)? {is_prime(97)},  DR(291) = {digital_root(291)}")
    print(f"  DR steps: {digital_root(9381)} → {digital_root(9672)} → {digital_root(9963)}")

    # 1221 = increment of sums
    incr_sum = 1221
    print(f"\nSum increment = {incr_sum} = 3 × 11 × 37 = {3}×{11}×{37}")
    assert 3 * 11 * 37 == incr_sum
    print(f"  Palindromic: '{incr_sum}'[::-1] = '{str(incr_sum)[::-1]}'  -> {str(incr_sum) == str(incr_sum)[::-1]}")
    print(f"  1221 mod 37 = {incr_sum % P}  [carries 37]")

    # Gap decrement
    gaps_col = [9381-1839, 9672-2769, 9963-3699]
    decrements = [gaps_col[i+1]-gaps_col[i] for i in range(len(gaps_col)-1)]
    print(f"\nGaps (n-rev(n)): {gaps_col}")
    print(f"  Decrements: {decrements}  (each = -639 = -3×213)")

    # The lock
    print(f"\nLock: 2-cycle at 9963 ↔ 9936")
    n1, n2 = 9963, 9936
    g1 = n1 - rev(n1)   # 9963 - 3699 = 6264
    g2 = n2 - rev(n2)   # 9936 - 6399 = 3537
    lock_sum = g1 + g2
    print(f"  gap(9963) = 9963 - {rev(n1)} = {g1}")
    print(f"  gap(9936) = 9936 - {rev(n2)} = {g2}")
    print(f"  {g1} + {g2} = {lock_sum} = {int(lock_sum**0.5)}² = 99²")
    assert lock_sum == 99**2, f"Expected 9801, got {lock_sum}"
    assert int(lock_sum**0.5) == 99

    # Kaprekar degeneracy
    print(f"\nKaprekar degeneracy:")
    kap_9963 = kaprekar_step(9963)
    kap_9936 = kaprekar_step(9936)
    digits_9963 = list(str(9963))
    is_nonincreasing = all(digits_9963[i] >= digits_9963[i+1] for i in range(len(digits_9963)-1))
    print(f"  9963 digits {digits_9963}: non-increasing? {is_nonincreasing}")
    print(f"  Kaprekar(9963) = {kap_9963}  (genuine: reversal = ascending sort)")
    print(f"  Kaprekar(9936) = {kap_9936}  (both collapse to same successor)")
    assert kap_9963 == kap_9936, "Kaprekar successors should match"
    print(f"  Oscillation is reversal-stable but Kaprekar-degenerate.")

    # Mod 37
    print(f"\nMod {P}:")
    print(f"  291 mod {P} = {291 % P}  ≡ -{P - (291 % P)} (= -5 mod 37)")
    col1 = [9381, 9672, 9963]
    residues = [n % P for n in col1]
    print(f"  Column-1 residues: {col1} -> {residues}")
    print(f"  Sequence: {' → '.join(str(r) for r in residues)}")
    print(f"  Step = {residues[1]-residues[0]} = -{P - (291%P)} mod {P}  [= -291 mod 37]")
    print(f"  Terminal residue {residues[-1]} ∈ H = {sorted(H)}? {residues[-1] in H}")
    r_9936 = 9936 % P
    print(f"  9936 mod {P} = {r_9936}  ({'inside' if r_9936 in H else 'outside'} H)")

    print(f"\nAll verifications passed.")

    return {
        "is_prime_2357": is_prime(2357),
        "dr_2357": digital_root(2357),
        "ladder_drsequence": [digital_root(n) for n, _ in rungs],
        "lock_sum": lock_sum,
        "kaprekar_degenerate": kap_9963 == kap_9936,
        "terminal_residue_mod37": residues[-1],
        "terminal_in_H": residues[-1] in H,
    }


if __name__ == "__main__":
    run()

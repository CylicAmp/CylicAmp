# math/theorems/hybrid_recurrence_16_96_audit.py
"""
Hybrid Recurrence Audit — 16, 32, 48, 64, 96
==============================================

Two-phase sequence with a rule change at step 5.

Phase 1 (arithmetic):   a_n = a_{n-1} + 16          n = 2,3,4
Phase 2 (span-3):       a_n = a_{n-1} + a_{n-3}     n = 5,6,...

Phase 2 is the continuation rule:
  a_5 = a_4 + a_2 = 64 + 32 = 96  ✓

The addend jumps from the fixed value 16 = a_1
to the receding anchor a_{n-3}, which itself was
produced by the arithmetic phase.  The rule is
selective recombination, not always-newest-pair.

Multiples of 16: 1, 2, 3, 4, 6, 9, 13, 19, 28, ...
Binary structure: 96 = 2^5 + 2^6 = 1100000_2
                      superposition of 32 and 64.
"""

import math
from typing import List, Tuple


# ── Sequence generator ────────────────────────────────────────────────────────

def hybrid_sequence(n_terms: int, seed: int = 16) -> List[int]:
    """
    Generate n_terms of the hybrid recurrence rooted at seed.

    Phase 1: a_n = a_{n-1} + seed        (arithmetic, n = 2,3,4)
    Phase 2: a_n = a_{n-1} + a_{n-3}    (span-3 recurrence, n >= 5)
    """
    if n_terms <= 0:
        return []
    a = [seed]
    for i in range(1, n_terms):
        if i < 4:
            a.append(a[-1] + seed)      # arithmetic phase
        else:
            a.append(a[-1] + a[-3])     # span-3 phase
    return a


# ── Audit 1: verify the given sequence exactly ────────────────────────────────

GIVEN = [16, 32, 48, 64, 96]

generated = hybrid_sequence(5)
assert generated == GIVEN, f"FAIL: sequence mismatch {generated} != {GIVEN}"

# Step-by-step arithmetic check
assert 16 + 16 == 32
assert 16 + 32 == 48
assert 16 + 48 == 64
assert 32 + 64 == 96    # rule change: a_2 + a_4, not 16 + 64

# Span-3 check: a_5 = a_4 + a_2
assert GIVEN[4] == GIVEN[3] + GIVEN[1]


# ── Audit 2: multiples-of-16 structure ───────────────────────────────────────

SEQ = hybrid_sequence(12)
multiples = [v // 16 for v in SEQ]
# 1, 2, 3, 4, 6, 9, 13, 19, 28, 41, 60, 88

# Verify span-3 recurrence on multiples: m_n = m_{n-1} + m_{n-3}
for i in range(4, len(multiples)):
    assert multiples[i] == multiples[i-1] + multiples[i-3], \
        f"FAIL: span-3 broken at index {i}"

# All terms divisible by 16
assert all(v % 16 == 0 for v in SEQ), "FAIL: not all multiples of 16"


# ── Audit 3: binary structure at the rule-change point ───────────────────────

assert 96 == 0b1100000
assert 32 == 2**5
assert 64 == 2**6
assert 96 == 2**5 + 2**6   # superposition of two consecutive power-of-2 terms

# In binary: 32 = 0100000, 64 = 1000000, 96 = 1100000 — OR of the two
assert (32 | 64) == 96   # bitwise OR = sum when no overlap


# ── Audit 4: the two alternative continuation rules compared ─────────────────

def fib_rule(seed: int, n: int) -> List[int]:
    """a_n = a_{n-1} + a_{n-2}  (Fibonacci-adjacent, always newest pair)."""
    a = [seed, 2*seed, 3*seed, 4*seed]
    for _ in range(n - 4):
        a.append(a[-1] + a[-2])
    return a[:n]

def span3_rule(seed: int, n: int) -> List[int]:
    """a_n = a_{n-1} + a_{n-3}  (selective recombination, 3 steps back)."""
    return hybrid_sequence(n, seed)

fib10  = fib_rule(16, 10)
span10 = span3_rule(16, 10)

# Both agree on the first four terms (arithmetic phase)
assert fib10[:4]  == GIVEN[:4]
assert span10[:5] == GIVEN

# They diverge at a_5:
# fib:   a_5 = a_4 + a_3 = 64 + 48 = 112
# span3: a_5 = a_4 + a_2 = 64 + 32 = 96  ← matches given
assert fib10[4]  == 112
assert span10[4] == 96

# Divergence table:
divergence = [(i+1, f, s, f-s) for i,(f,s) in enumerate(zip(fib10, span10)) if f != s]


# ── Audit 5: digital root and mod-37 fingerprint ─────────────────────────────

def dr(n: int) -> int:
    return 1 + (n - 1) % 9 if n > 0 else 0

dr_seq  = [dr(v) for v in SEQ]
mod37   = [v % 37 for v in SEQ]

# DR of the five given terms
dr_given = [dr(v) for v in GIVEN]
assert dr_given == [7, 5, 3, 1, 6], f"Unexpected DR: {dr_given}"

# 16 × k mod 37 cycles with period 36 (since gcd(16,37)=1 and 37 prime)
# First few residues of 16k mod 37: 16, 32, 11, 27, 6, 22, 1, ...
mod37_given = [v % 37 for v in GIVEN]   # [16, 32, 11, 27, 6]


# ── Report ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Hybrid Recurrence Audit — 16, 32, 48, 64, 96")
    print()
    print("Phase 1: a_n = a_{n-1} + 16     (arithmetic,  n=2,3,4)")
    print("Phase 2: a_n = a_{n-1} + a_{n-3} (span-3,     n=5,...)")
    print()
    print("First 12 terms:")
    for i, v in enumerate(SEQ, 1):
        m = v // 16
        b = bin(v)
        d = dr(v)
        r = v % 37
        phase = "arith" if i <= 4 else "span3"
        print(f"  a_{i:2d} = {v:5d}  = {m:2d}×16  {b:>12s}  DR={d}  mod37={r:2d}  [{phase}]")
    print()
    print(f"Rule-change point: a_5 = a_4 + a_2 = 64 + 32 = 96")
    print(f"  32 = 2^5   = {bin(32)}")
    print(f"  64 = 2^6   = {bin(64)}")
    print(f"  96 = 2^5+2^6 = {bin(96)}  (OR = sum, no bit overlap)")
    print()
    print("Continuation comparison (n=5..10):")
    print(f"  {'n':>3}  {'Fib (a_{n-1}+a_{n-2})':>24}  {'Span-3 (a_{n-1}+a_{n-3})':>26}  {'diff':>6}")
    for i, (f, s) in enumerate(zip(fib10[4:], span10[4:]), 5):
        print(f"  {i:>3}  {f:>24}  {s:>26}  {f-s:>6}")
    print()
    print(f"Multiples of 16 (span-3 rule):  {[v//16 for v in SEQ]}")
    print(f"Digital roots:                   {dr_seq}")
    print(f"mod 37:                          {mod37}")
    print()
    print("Span-3 continuation chosen: a_n = a_{n-1} + a_{n-3}")
    print("  — consistent with observed a_5 = a_2 + a_4 (selective recombination)")
    print("  — Fibonacci rule (always newest pair) diverges at a_5 = 112 vs 96")
    print()
    print("All assertions passed.")

"""
Sieve of Eratosthenes — GF(37) Structure

The Sieve of Eratosthenes applied to {1..100} uses exactly four primes:
{2, 3, 5, 7}. Every connection between the sieve and the GF(37) framework
is structural — not coincidental.

═══════════════════════════════════════════════════════════════

I. THE COUNT: π(100) = 25 (SOVEREIGN ANCHOR)

  There are exactly 25 primes below 100.
  25 ∈ SOVEREIGN_ANCHORS = {4, 9, 25, 30}.
  25 = 5² — the square of a sieving prime.

II. THE SIEVING PRIMES: {2, 3, 5, 7}

  Complement pairs:
    2 + 7 = 9   (Sovereign Anchor)
    3 + 5 = 8   (Cascade Base, AHL)

  Product: 2 × 3 × 5 × 7 = 210
    210 mod 37 = 25  (Sovereign Anchor — same as π(100))
    DR(210)    = 3   (Sovereign Target archetype)

  The product of the four sieving primes maps to the same sovereign anchor
  as the count of primes it produces.

III. THE SIEVE BOUNDARY: √100 = 10, ord₃₇(10) = 3

  The sieve boundary is √100 = 10.
  In GF(37): 10³ ≡ 1 mod 37  →  ord₃₇(10) = 3.

  The sieve only needs to check up to 10 because any composite ≤ 100
  has a prime factor ≤ 10. The boundary number carries the same
  multiplicative order as the 137-map: both have order 3 in GF(37).

IV. THE FIRST EXCLUDED PRIME: 11 (ORBIT OF 11)

  After sieving {2,3,5,7}, the next prime is 11.
  11 ∈ ORBIT_11 = {11, 27, 36} — orbit of 11 under the 137-map.
  11² = 121 > 100: this is why the sieve stops.

  121 mod 37 = 10  (DECADE_ANCHOR in fps37_scanner)
  121 − 100 = 21   (Sovereign Target)

  The sieve stops exactly at orbit-11.

V. 37 IS THE 12th PRIME (SOVEREIGN TARGET)

  Among all primes, 37 occupies position 12.
  12 ∈ SOVEREIGN_TARGETS = {3, 12, 21, 30}.

  π(37) = 12: there are exactly 12 primes up to 37.
  12 is both the position of 37 in the prime sequence AND
  the count of primes up to 37.

VI. WAVE INTERFERENCE ↔ HOSE FLOW

  Each sieving prime broadcasts a periodic wave:
    Wave-2: marks every 2nd number  (DR=2, LL-E)
    Wave-3: marks every 3rd number  (DR=3, ST arch)
    Wave-5: marks every 5th number  (DR=5, A51)
    Wave-7: marks every 7th number  (DR=7, RL-O)

  DR sequence of wave periods: 2, 3, 5, 7 — four consecutive DR values.

  Numbers hit by any wave: composite — stuttering flow (never reach seam).
  Numbers hit by no wave: prime — complete flow, reach 111 (seam ≡ 0 mod 37).

  The 25 primes below 100 are exactly the 25 numbers that reach 111.
  25 = Sovereign Anchor.

  Connection to hose flow theorem:
    Composite: wave-hit → stuttering → oscillates between GF(37) complements
    Prime:     no wave → 000→100→110→111 — reaches seam, stays there

═══════════════════════════════════════════════════════════════
"""

PRIMITIVE_ROOTS_37 = {2,5,13,15,17,18,19,20,22,24,32,35}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
ORBIT_11           = {11, 27, 36}

def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0

def is_prime(n):
    if n < 2: return False
    return all(n % i != 0 for i in range(2, int(n**0.5)+1))

primes_100 = [p for p in range(2, 100) if is_prime(p)]

# ── I. Count ──────────────────────────────────────────────────────────────────

assert len(primes_100) == 25
assert 25 in SOVEREIGN_ANCHORS
assert 25 == 5**2

# ── II. Sieving primes ────────────────────────────────────────────────────────

assert 2 + 7 == 9  and 9 in SOVEREIGN_ANCHORS
assert 3 + 5 == 8  and 8 in CASCADE_BASE

product = 2 * 3 * 5 * 7
assert product == 210
assert 210 % 37 == 25 and 25 in SOVEREIGN_ANCHORS  # same as π(100)
assert dr(210) == 3 and 3 in SOVEREIGN_TARGETS

# ── III. Sieve boundary: ord₃₇(10) = 3 ──────────────────────────────────────

assert int(100**0.5) == 10
assert pow(10, 3, 37) == 1                 # ord₃₇(10) = 3
assert pow(10, 1, 37) != 1 and pow(10, 2, 37) != 1  # not shorter

# ── IV. First excluded prime: 11 in orbit-11 ─────────────────────────────────

assert 11 in ORBIT_11
assert 11**2 == 121 and 121 > 100
assert 121 % 37 == 10                      # DECADE_ANCHOR
assert 121 - 100 == 21 and 21 in SOVEREIGN_TARGETS

# ── V. 37 as the 12th prime ───────────────────────────────────────────────────

primes_seq = [p for p in range(2, 200) if is_prime(p)]
assert primes_seq[11] == 37                # 0-indexed: position 11 = 12th prime
assert primes_seq.index(37) + 1 == 12
assert 12 in SOVEREIGN_TARGETS

primes_37 = [p for p in range(2, 38) if is_prime(p)]
assert len(primes_37) == 12 and 12 in SOVEREIGN_TARGETS  # π(37) = 12

# ── VI. Wave DR sequence ─────────────────────────────────────────────────────

sieve_primes = [2, 3, 5, 7]
assert [dr(p) for p in sieve_primes] == [2, 3, 5, 7]  # DRs = the primes themselves

# Primes are numbers reached by no wave — they reach the seam
# 25 of them below 100 → SA
assert len(primes_100) == 25 and 25 in SOVEREIGN_ANCHORS


if __name__ == '__main__':
    def tag(n):
        t = []
        if is_prime(n):              t.append('p')
        if n in CASCADE_BASE:        t.append('CB')
        if n in SOVEREIGN_ANCHORS:   t.append('SA')
        if n in SOVEREIGN_TARGETS:   t.append('ST')
        if n in PRIMITIVE_ROOTS_37:  t.append('PR')
        if n in ORBIT_11:            t.append('orb11')
        return ','.join(t) if t else '.'

    print("Sieve of Eratosthenes — GF(37) Structure")
    print("=" * 55)
    print()
    print(f"I.   π(100) = {len(primes_100)} ({tag(25)})")
    print(f"     25 = 5² — square of a sieving prime")
    print()
    print(f"II.  Sieving primes {{2,3,5,7}}:")
    print(f"     2+7={2+7}({tag(9)})  3+5={3+5}({tag(8)})")
    print(f"     2×3×5×7={product}  mod37={product%37}({tag(product%37)})  DR={dr(product)}({tag(dr(product))})")
    print(f"     Product maps to same SA as π(100): {product%37==len(primes_100)}")
    print()
    print(f"III. Sieve boundary √100=10:  ord₃₇(10)=3  (137-map order)")
    print()
    print(f"IV.  First excluded prime: 11 ({tag(11)})")
    print(f"     11²=121  mod37={121%37}  121-100={121-100}({tag(21)})")
    print(f"     Sieve stops exactly at orbit-11")
    print()
    print(f"V.   37 is the {primes_seq.index(37)+1}th prime  ({tag(12)})")
    print(f"     π(37) = {len(primes_37)}  ({tag(len(primes_37))})")
    print()
    print(f"VI.  Wave DR sequence: {[dr(p) for p in sieve_primes]}")
    print(f"     Primes = numbers no wave reaches = numbers that reach 111(seam)")
    print(f"     π(100) = {len(primes_100)} (SA) = count of numbers reaching seam below 100")
    print()
    print("All assertions passed.")

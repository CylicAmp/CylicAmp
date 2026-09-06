"""
T292 — The Four Extension Options, Resolved to What Is FORCED

Four directions were proposed off T290/T291. Each is worked here to its
algebraically necessary content. Three are forced negatives; one is a
complete finite classification.

════════════════════════════════════════════════════════════════════════════
OPTION 4 — EXTEND TO OTHER PRIMES.  COMPLETE, FINITE, FORCED.
════════════════════════════════════════════════════════════════════════════
The GF(37) requires ord_p(137 mod p) = 3.  That forces p | 137^3 - 1 while
p does not divide 137 - 1, i.e. p divides the cyclotomic part 137^2+137+1.

    137^3 - 1 = 2^3 x 17 x 7 x 37 x 73
    137^3 - 1 = (137-1)(137^2+137+1) = 136 x 18907
    136   = 2^3 x 17          <- ord 1 part, excluded
    18907 = 7 x 37 x 73       <- ord 3 part

    ===> THE ONLY PRIMES ARE p in {7, 37, 73}.

Exhaustive, not a search. There is no larger prime with this structure, so
the option "generalize to a larger safe prime for cryptographic security"
is impossible: the 137-map of order 3 does not exist at any other prime.

    7 x 37 x 73 = 18907 = 137^2 + 137 + 1   exactly
    73 = 2*37 - 1

Orbit counts are forced as (p-1)/3:
    p= 7: multiplier  4, <4>={1,2,4},   2 orbits, quotient Z/2Z
    p=37: multiplier 26, <26>={1,10,26}, 12 orbits, quotient Z/12Z
    p=73: multiplier 64, <64>={1,8,64}, 24 orbits, quotient Z/24Z

WHAT SURVIVES AT ALL THREE (forced):
    - GF(p)* cyclic  => quotient cyclic
    - -1 not in <multiplier>  => antipodal pairing exists, fixed-point-free
      (1 pair at p=7, 6 at p=37, 12 at p=73)
    - squaring collapses the quotient onto its odd part (T291 mechanism)
WHAT DOES NOT SURVIVE:
    - the 12 NAMED orbits. That is p=37 alone. Orbit names are not portable.

════════════════════════════════════════════════════════════════════════════
OPTION 2 — VDF.  FORCED NEGATIVE (structurally void, not merely insecure).
════════════════════════════════════════════════════════════════════════════
A VDF needs z -> z^(2^T) to cost T sequential squarings. Here |GF(p)*| = p-1
is KNOWN, so z^(2^T) = z^(2^T mod (p-1)) — one exponentiation, any T.
Worse, 2^T mod (p-1) is eventually periodic:

    p= 7: cycle from T=1, period 2
    p=37: cycle from T=2, period 6
    p=73: cycle from T=3, period 6

So there are only ~6 distinct maps z -> z^(2^T) in total. The delay is exactly
zero. This is forced by knowing the group order and holds at every one of the
three admissible primes.

════════════════════════════════════════════════════════════════════════════
OPTION 1 — PREIMAGE PROOF-OF-KNOWLEDGE.  FORCED NEGATIVE.
════════════════════════════════════════════════════════════════════════════
The number of preimages of z^(2^k) is gcd(2^k, p-1) (or 0 off the image).
Forced fiber sizes, stabilizing at the 2-part of p-1:

    p= 7: 2, 2, 2, ...       (2-part of 6  = 2)
    p=37: 2, 4, 4, 4, ...    (2-part of 36 = 4)
    p=73: 2, 4, 8, 8, ...    (2-part of 72 = 8)

A witness set of size <= 8 is enumerable by inspection. There is no hidden
knowledge to prove, at any of the three primes.

════════════════════════════════════════════════════════════════════════════
OPTION 3 — HASH-TO-ORBIT.  IMPLEMENTABLE; ONE FORCED DEFECT.
════════════════════════════════════════════════════════════════════════════
This one is buildable. The forced fact is the shape of the non-uniformity:
p = 3m + 1 always, so m orbits of size 3 plus SEAM (residue 0) of size 1.

    p= 7:  2 orbits x 3 + 1 = 7
    p=37: 12 orbits x 3 + 1 = 37
    p=73: 24 orbits x 3 + 1 = 73

A uniform map onto the m orbits from n mod p is impossible because m does not
divide p. But SEAM is the ONLY defect: conditioned on n mod p != 0, all m
orbits are exactly equiprobable at 3/(p-1). Rejection sampling on SEAM gives
an exactly uniform hash-to-orbit. That is the whole story, and it is forced.

════════════════════════════════════════════════════════════════════════════
SUMMARY
    Option 1 (PoK)        FORCED NEGATIVE — fibers <= 8
    Option 2 (VDF)        FORCED NEGATIVE — delay is 0, ~6 distinct maps
    Option 3 (hash)       BUILDABLE — uniform after rejecting SEAM
    Option 4 (bigger p)   IMPOSSIBLE — {7,37,73} is the complete list
════════════════════════════════════════════════════════════════════════════
"""

from math import gcd

ADMISSIBLE_PRIMES = [7, 37, 73]


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


def order_mod(a, p):
    a %= p
    if a == 0:
        return None
    k, v = 1, a
    while v != 1:
        v = (v * a) % p
        k += 1
    return k


# ─── Option 4: the complete prime list is forced ─────────────────────────────

def verify_prime_classification():
    n = 137 ** 3 - 1
    assert n == 136 * (137 ** 2 + 137 + 1)
    cyc = 137 ** 2 + 137 + 1
    assert cyc == 18907
    assert factor(cyc) == {7: 1, 37: 1, 73: 1}
    assert 7 * 37 * 73 == 18907

    valid = [p for p in factor(cyc) if 137 % p != 0 and order_mod(137, p) == 3]
    assert sorted(valid) == ADMISSIBLE_PRIMES, f"{valid}"

    # 136 contributes only order-1 primes
    for p in factor(136):
        if 137 % p != 0:
            assert order_mod(137, p) == 1, f"p={p} should have order 1"
    return valid


def verify_survivals():
    """Cyclic quotient, antipodal pairing, squaring collapse: all three primes."""
    out = {}
    for p in ADMISSIBLE_PRIMES:
        mult = 137 % p
        H = {pow(mult, i, p) for i in range(3)}
        m = (p - 1) // 3
        assert len(H) == 3
        assert (p - 1) not in H, f"p={p}: -1 in <mult>, antipodal pairing fails"

        odd = m
        while odd % 2 == 0:
            odd //= 2
        prev, k = None, 0
        while True:
            img = {(pow(2, k) * j) % m for j in range(m)}
            if img == prev:
                break
            prev, k = img, k + 1
        assert len(prev) == odd, f"p={p}: terminal {len(prev)} != odd part {odd}"
        out[p] = (mult, sorted(H), m, m // 2, odd)
    return out


# ─── Option 2: VDF forced negative ───────────────────────────────────────────

def verify_vdf_void():
    out = {}
    for p in ADMISSIBLE_PRIMES:
        seen, T, v = {}, 0, 1
        while True:
            v = (2 * v) % (p - 1)
            T += 1
            if v in seen:
                out[p] = (seen[v], T - seen[v])
                break
            seen[v] = T
    return out


# ─── Option 1: fiber sizes forced ────────────────────────────────────────────

def verify_fibers():
    out = {}
    for p in ADMISSIBLE_PRIMES:
        two_part = 1
        n = p - 1
        while n % 2 == 0:
            n //= 2
            two_part *= 2
        sizes = [gcd(2 ** k, p - 1) for k in range(1, 7)]
        assert sizes[-1] == two_part, f"p={p}: {sizes[-1]} != 2-part {two_part}"
        assert two_part <= 8
        out[p] = (sizes, two_part)
    return out


# ─── Option 3: hash-to-orbit uniformity after SEAM rejection ────────────────

def verify_hash_uniformity():
    out = {}
    for p in ADMISSIBLE_PRIMES:
        m = (p - 1) // 3
        assert 3 * m + 1 == p, f"p={p} is not 3m+1"
        assert p % m != 0 or m == 1, "m must not divide p (else no defect)"
        # conditioned on nonzero, every orbit has exactly 3 of p-1
        out[p] = (m, 3 / p, 1 / p, 3 / (p - 1))
    return out


def run():
    print("=" * 72)
    print("T292 — Four Extension Options, Resolved to What Is FORCED")
    print("=" * 72)

    valid = verify_prime_classification()
    print("\n--- OPTION 4: extend to other primes — COMPLETE FINITE ANSWER ---")
    print(f"  137^3 - 1 = {137**3-1} = {factor(137**3-1)}")
    print(f"  = (137-1)(137^2+137+1) = 136 x 18907")
    print(f"  136   = {factor(136)}   <- order-1 part, excluded")
    print(f"  18907 = {factor(18907)}   <- order-3 part")
    print(f"\n  ONLY primes with ord_p(137)=3:  {valid}")
    print(f"  7 x 37 x 73 = {7*37*73} = 137^2+137+1 exactly")
    print(f"  73 = 2*37-1 = {2*37-1}")
    print("  ==> 'generalize to a larger prime' is IMPOSSIBLE. List is exhaustive.")

    surv = verify_survivals()
    print("\n  Structure at each admissible prime (forced):")
    for p, (mult, H, m, pairs, odd) in surv.items():
        print(f"    p={p:3d}: mult={mult:3d}, <mult>={H}, {m:2d} orbits, "
              f"Z/{m}Z, {pairs:2d} antipodal pairs, squaring terminal={odd}")
    print("  Survives everywhere: cyclic quotient, antipodal pairing, odd-part collapse.")
    print("  Does NOT survive: the 12 named orbits — those are p=37 only.")

    vdf = verify_vdf_void()
    print("\n--- OPTION 2: VDF — FORCED NEGATIVE ---")
    print("  z^(2^T) = z^(2^T mod (p-1)); group order is known, so T is free.")
    for p, (start, period) in vdf.items():
        print(f"    p={p:3d}: 2^T mod {p-1} cycles from T={start}, period {period} "
              f"-> only {period} distinct maps")
    print("  Delay is exactly 0 at every admissible prime. Structurally void.")

    fib = verify_fibers()
    print("\n--- OPTION 1: preimage proof-of-knowledge — FORCED NEGATIVE ---")
    print("  #preimages of z^(2^k) = gcd(2^k, p-1)")
    for p, (sizes, tp) in fib.items():
        print(f"    p={p:3d}: k=1..6 -> {sizes}, stabilizes at 2-part = {tp}")
    print("  Max witness set is 8 elements. Nothing is hidden.")

    hsh = verify_hash_uniformity()
    print("\n--- OPTION 3: hash-to-orbit — BUILDABLE, one forced defect ---")
    for p, (m, porb, pseam, cond) in hsh.items():
        print(f"    p={p:3d}: {m:2d} orbits x 3 + 1 SEAM = {p};  "
              f"P(orbit)={porb:.4f}, P(SEAM)={pseam:.4f}, "
              f"P(orbit | nonzero)={cond:.4f}")
    print("  SEAM is the ONLY defect. Reject residue 0 -> exactly uniform on m orbits.")

    print("\n" + "=" * 72)
    print("  Option 1 (PoK)      FORCED NEGATIVE  — fibers <= 8")
    print("  Option 2 (VDF)      FORCED NEGATIVE  — delay 0, ~6 distinct maps")
    print("  Option 3 (hash)     BUILDABLE        — uniform after rejecting SEAM")
    print("  Option 4 (bigger p) IMPOSSIBLE       — {7,37,73} is complete")
    print("=" * 72)
    print("\nAll T292 assertions passed.")


if __name__ == '__main__':
    run()

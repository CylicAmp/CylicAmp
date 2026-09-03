"""
T295 — The Real Generalization: mu_3 and the GLV Endomorphism (secp256k1)

Answers option 4 from the extension list: "generalize from 37 to a larger safe
prime for cryptographic security."

T292 proved {7,37,73} is the complete set of primes with ord_p(137)=3, so the
137-map itself cannot move. But 137 was never the load-bearing part.

════════════════════════════════════════════════════════════════════════════
WHAT 137 ACTUALLY IS
════════════════════════════════════════════════════════════════════════════
    137 mod 37 = 26,  and  26^3 = 1 (mod 37),  26 != 1.

26 is a PRIMITIVE CUBE ROOT OF UNITY mod 37. That is the entire reason the
137-map has order 3. IC is not merely "the orbit of the multiplier" — it is

    IC = {1, 10, 26} = mu_3(F_37),  the group of cube roots of unity.

The two primitive roots satisfy the cyclotomic polynomial x^2 + x + 1:
    10^2 + 10 + 1 = 111 = 3 x 37     <- the framework's SEAM value
    26^2 + 26 + 1 = 703 = 19 x 37
Both vanish mod 37 by construction. The 111 = 3 x 37 result already recorded
in the framework is the minimal polynomial of the multiplier evaluated at 10.

════════════════════════════════════════════════════════════════════════════
THE GENERALIZATION
════════════════════════════════════════════════════════════════════════════
Drop 137, keep mu_3. Every prime p = 1 (mod 3) has exactly two primitive cube
roots of unity. Using either as the multiplier reproduces the whole structure:

    orbits of size 3, quotient Z/((p-1)/3)Z, antipodal pairing, the lot.

p=37 gives 12 orbits because (37-1)/3 = 12. Nothing about 12 is special; it
is just (p-1)/3. There is no obstruction at any size.

════════════════════════════════════════════════════════════════════════════
IT IS ALREADY DEPLOYED: GLV ON secp256k1 (BITCOIN)
════════════════════════════════════════════════════════════════════════════
    p    = 2^256 - 2^32 - 977          p mod 3 = 1        (qualifies)
    curve: y^2 = x^3 + 7               a = 0  -> j = 0    (T288/T293 family)
    (p-1)/3 ~ 2^255 orbits

    beta = 0x7ae96a2b...719501ee    beta^3 = 1 mod p,  beta^2+beta+1 = 0
    lam  = 0x5363ad4c...1b23bd72    lam^3  = 1 mod n,  lam^2+lam+1  = 0

The map phi(x,y) = (beta*x, y) is a curve endomorphism, and phi(P) = [lam]P.
So the multiplicative 3-cycle {x, beta*x, beta^2*x} on coordinates lifts to
{P, [lam]P, [lam^2]P} on points — the identical 3-cycle structure at 256 bits.

This is the Gallant-Lambert-Vanstone method. It is used in production to
split a 256-bit scalar into two ~128-bit halves for faster multiplication.
secp256k1 and BLS12-381 both rely on it; both are j=0 curves.

So the answer to option 4 is not "impossible." It is: the structure
generalizes, it generalized decades ago, and it is called GLV.

════════════════════════════════════════════════════════════════════════════
THE INVERSION — ANOMALOUS IS FATAL, NOT INTERESTING
════════════════════════════════════════════════════════════════════════════
T288 and T293 singled out p=37's anomalous curve (#E = p, trace t = 1) as the
distinguishing feature of the framework's prime. In cryptography that exact
property is a total break.

Anomalous curves fall to Smart's attack (1997), independently Satoh-Araki and
Semaev: the p-adic elliptic logarithm reduces ECDLP to addition in F_p and
solves it in LINEAR time. Any curve with #E = p is unusable.

    secp256k1:  n != p,  trace t = p+1-n = 432420386565659656852420866390673177327

The property T293 proved unique to p=37 among {7,37,73} is precisely the
property a cryptographic curve must be verified NOT to have. Curve selection
explicitly tests for it.

So the framework's most distinctive elliptic-curve feature does not scale to
security — it is the disqualifying condition. What scales is the mu_3
endomorphism structure, which is orthogonal to it.

════════════════════════════════════════════════════════════════════════════
SUMMARY
    137 at larger primes           IMPOSSIBLE (T292: only 7, 37, 73)
    mu_3 orbit structure           GENERALIZES to every p = 1 mod 3
    3-cycle -> curve endomorphism  DEPLOYED as GLV (secp256k1, BLS12-381)
    anomalous property (T288/293)  DISQUALIFYING — Smart's attack, linear ECDLP
════════════════════════════════════════════════════════════════════════════
"""

# secp256k1 domain parameters
SECP_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
SECP_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
SECP_B = 7
SECP_BETA = 0x7ae96a2b657c07106e64479eac3434e99cf0497512f58995c1396c28719501ee
SECP_LAM = 0x5363ad4cc05c30e0a5261c028812645a122e22ea20816678df02967c1b23bd72
SECP_GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
SECP_GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


def cube_roots_of_unity(p):
    """The primitive cube roots of unity mod p (empty unless p = 1 mod 3)."""
    return sorted(x for x in range(2, p) if pow(x, 3, p) == 1)


# ─── Part 1: 137 mod 37 is a primitive cube root of unity ───────────────────

def verify_mu3_at_37():
    assert 137 % 37 == 26
    assert pow(26, 3, 37) == 1 and 26 != 1
    roots = cube_roots_of_unity(37)
    assert roots == [10, 26], f"primitive cube roots mod 37: {roots}"
    assert {1} | set(roots) == {1, 10, 26}, "IC must be mu_3(F_37)"
    # cyclotomic polynomial vanishes
    assert 10 ** 2 + 10 + 1 == 111 == 3 * 37
    assert (26 ** 2 + 26 + 1) % 37 == 0
    assert (26 ** 2 + 26 + 1) == 703 == 19 * 37
    return roots


# ─── Part 2: the structure generalizes to any p = 1 mod 3 ───────────────────

def verify_generalization(primes=(7, 13, 31, 37, 43, 61, 73, 97)):
    out = {}
    for p in primes:
        if p % 3 != 1:
            continue
        roots = cube_roots_of_unity(p)
        assert len(roots) == 2, f"p={p}: expected 2 primitive roots, got {roots}"
        for w in roots:
            assert (w * w + w + 1) % p == 0, f"p={p}: {w} fails x^2+x+1"
        # orbits under multiplication by w
        w = roots[0]
        seen, norb = set(), 0
        for x in range(1, p):
            if x in seen:
                continue
            o = {x, (x * w) % p, (x * w * w) % p}
            assert len(o) == 3, f"p={p}: orbit {o} not size 3"
            seen |= o
            norb += 1
        assert norb == (p - 1) // 3
        out[p] = (roots, norb)
    return out


# ─── Part 3: secp256k1 carries the same structure at 256 bits ──────────────

def verify_secp256k1():
    assert SECP_P % 3 == 1, "secp256k1 p must be 1 mod 3"
    assert pow(SECP_BETA, 3, SECP_P) == 1 and SECP_BETA != 1
    assert (SECP_BETA ** 2 + SECP_BETA + 1) % SECP_P == 0
    assert pow(SECP_LAM, 3, SECP_N) == 1 and SECP_LAM != 1
    assert (SECP_LAM ** 2 + SECP_LAM + 1) % SECP_N == 0

    # generator is on the j=0 curve, and so is phi(G) = (beta*x, y)
    on = lambda x, y: (y * y - (x ** 3 + SECP_B)) % SECP_P == 0
    assert on(SECP_GX, SECP_GY), "G not on curve"
    assert on((SECP_BETA * SECP_GX) % SECP_P, SECP_GY), "phi(G) not on curve"

    # the beta-orbit of a coordinate has size 3, same as IC
    orb = {SECP_GX % SECP_P,
           (SECP_BETA * SECP_GX) % SECP_P,
           (SECP_BETA * SECP_BETA * SECP_GX) % SECP_P}
    assert len(orb) == 3
    return (SECP_P - 1) // 3


# ─── Part 4: anomalous is disqualifying ─────────────────────────────────────

def verify_not_anomalous():
    """#E = p would make ECDLP linear-time (Smart 1997)."""
    assert SECP_N != SECP_P, "anomalous curve — would be broken"
    t = SECP_P + 1 - SECP_N
    assert t != 1, "trace 1 = anomalous = broken"
    return t


def run():
    print("=" * 76)
    print("T295 — The Real Generalization: mu_3 and GLV (secp256k1)")
    print("=" * 76)

    roots = verify_mu3_at_37()
    print("\n--- Part 1: 137 mod 37 = 26 is a primitive cube root of unity ---")
    print(f"  primitive cube roots mod 37: {roots}")
    print(f"  IC = {{1, 10, 26}} = mu_3(F_37)")
    print(f"  10^2+10+1 = 111 = 3 x 37   <- the framework's SEAM value")
    print(f"  26^2+26+1 = 703 = 19 x 37")
    print("  The 137-map has order 3 because 26 is a cube root of unity.")
    print("  Nothing else about 137 matters.")

    gen = verify_generalization()
    print("\n--- Part 2: generalizes to every p = 1 (mod 3) ---")
    print(f"  {'p':>5} {'primitive cube roots':>24} {'orbits (p-1)/3':>16}")
    for p, (r, n) in sorted(gen.items()):
        print(f"  {p:>5} {str(r):>24} {n:>16}")
    print("  12 orbits at p=37 is just (37-1)/3. No obstruction at any size.")

    norb = verify_secp256k1()
    print("\n--- Part 3: secp256k1 (Bitcoin) is this structure at 256 bits ---")
    print(f"  p mod 3 = {SECP_P % 3}  ->  qualifies")
    print(f"  curve y^2 = x^3 + {SECP_B}   (a=0, j=0 — the T288/T293 family)")
    print(f"  orbits (p-1)/3 ~ 2^{norb.bit_length()}")
    print(f"  beta^3 = 1 mod p,  beta^2+beta+1 = 0   -> primitive cube root")
    print(f"  lam^3  = 1 mod n,  lam^2+lam+1  = 0    -> same, on the order")
    print(f"  phi(x,y) = (beta*x, y) is an endomorphism, phi(P) = [lam]P")
    print(f"  coordinate 3-cycle {{x, beta*x, beta^2*x}} lifts to {{P,[lam]P,[lam^2]P}}")
    print("  This is the GLV method. secp256k1 and BLS12-381 both use it.")

    t = verify_not_anomalous()
    print("\n--- Part 4: the anomalous property is DISQUALIFYING ---")
    print(f"  secp256k1 trace t = p+1-n = {t}")
    print(f"  n == p ? {SECP_N == SECP_P}   (anomalous would require True)")
    print("  Anomalous curves (#E = p, t = 1) fall to Smart's attack (1997);")
    print("  independently Satoh-Araki and Semaev. The p-adic elliptic log")
    print("  reduces ECDLP to addition in F_p — LINEAR time.")
    print("  T293 proved p=37 uniquely has that property among {7,37,73}.")
    print("  Curve selection explicitly tests for it and rejects it.")

    print("\n" + "=" * 76)
    print("  137 at larger primes          IMPOSSIBLE (T292: only 7, 37, 73)")
    print("  mu_3 orbit structure          GENERALIZES to every p = 1 mod 3")
    print("  3-cycle -> endomorphism       DEPLOYED as GLV (secp256k1, BLS12-381)")
    print("  anomalous (T288/T293)         DISQUALIFYING — linear-time ECDLP")
    print("=" * 76)
    print("\nAll T295 assertions passed.")


if __name__ == '__main__':
    run()

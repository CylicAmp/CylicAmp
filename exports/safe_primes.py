#!/usr/bin/env python3
"""
Safe primes -- one file, plain Python 3, nothing to install. Runs on a phone, an online Python, any computer.

    python3 safe_primes.py 1000000        the Sophie Germain primes below 1,000,000: how many, and the first ones
    python3 safe_primes.py --bits 1024    a new random safe prime of 1024 bits, ready for key exchange
                                          (512 bits: under a second; 1024: about 10 s; 2048: a few minutes)
    python3 safe_primes.py --check N      is N a safe prime?  (N in decimal, or in hex starting 0x)
    python3 safe_primes.py --test         every check below, PASS or FAIL

WHAT THEY ARE: p is a Sophie Germain prime when p and 2p + 1 are both prime; 2p + 1 is then a safe prime.
    2 -> 5,  3 -> 7,  5 -> 11,  11 -> 23,  23 -> 47,  29 -> 59, ...

WHAT THEY ARE FOR: Diffie-Hellman key exchange -- how two computers agree on a secret key over an open line -- runs
  on a safe prime q. Then the nonzero numbers by q split into groups of sizes 1, 2, p and 2p only, with p huge: no
  small group an attacker can trap a key in. The standard groups in RFC 3526 and RFC 7919 are safe primes; --test
  checks five of them.

HOW THE LIST IS MADE -- the walk's table: entry k says whether the odd number 2k + 1 is prime. For p = 2k + 1,
  2p + 1 = 4k + 3 = 2(2k + 1) + 1 is entry 2k + 1. So a Sophie Germain prime is an entry k that is prime together
  with entry 2k + 1. The walk reads entries n - 1 and n side by side; this reads k and 2k + 1.

FORCED (true of every one, nothing to find): above 3, p leaves 2 by 3 -- if it left 1, 2p + 1 would be a multiple
  of 3 -- so p and 2p + 1 both have root 2, 5 or 8, and above 7 the safe prime 2p + 1 leaves 11 by 12.

HOW A BIG ONE IS MADE (--bits):
  1. start at a random p of the right size that leaves 5 by 6 (odd, and 2 by 3);
  2. walk p up by 6 through a window and cross out every p where p or 2p + 1 has a prime factor below 65,536 --
     the walk's sieve again: p is out when p by r leaves 0 (r divides p) or (r - 1)/2 (r divides 2p + 1);
  3. a survivor p gets Miller-Rabin: 64 rounds with random bases, so a composite passes with chance below 4^-64;
     below 3.3 x 10^24 the bases 2, 3, 5, ..., 41 make the test exact;
  4. then q = 2p + 1 is PROVED prime, not only tested (Pocklington): q - 1 = 2p with p prime and p above the square
     root of q, so q is prime exactly when 2^(q-1) leaves 1 by q and 3 does not divide q.
  So the safe prime is as sure as p: proved when p is below 3.3 x 10^24, wrong with chance below 4^-64 above that.
  For key exchange use generator 4 (a square, so it makes the group of size p); 2 does the same when q leaves 7 by 8.
"""
import random
import secrets
import sys
import time

DH_PRIMES = {
    "RFC 3526 group 5 (1536-bit)": (
        "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DD"
        "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
        "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
        "83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF"
    ),
    "RFC 3526 group 14 (2048-bit)": (
        "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DD"
        "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
        "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
        "83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
        "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
        "15728E5A8AACAA68FFFFFFFFFFFFFFFF"
    ),
    "RFC 3526 group 15 (3072-bit)": (
        "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DD"
        "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
        "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
        "83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
        "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
        "15728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7"
        "ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200C"
        "BBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A93AD2CAFFFFFFFFFFFFFFFF"
    ),
    "RFC 7919 ffdhe2048": (
        "FFFFFFFFFFFFFFFFADF85458A2BB4A9AAFDC5620273D3CF1D8B9C583CE2D3695A9E13641146433FBCC939DCE249B3EF9"
        "7D2FE363630C75D8F681B202AEC4617AD3DF1ED5D5FD65612433F51F5F066ED0856365553DED1AF3B557135E7F57C935"
        "984F0C70E0E68B77E2A689DAF3EFE8721DF158A136ADE73530ACCA4F483A797ABC0AB182B324FB61D108A94BB2C8E3FB"
        "B96ADAB760D7F4681D4F42A3DE394DF4AE56EDE76372BB190B07A7C8EE0A6D709E02FCE1CDF7E2ECC03404CD28342F61"
        "9172FE9CE98583FF8E4F1232EEF28183C3FE3B1B4C6FAD733BB5FCBC2EC22005C58EF1837D1683B2C6F34A26C1B2EFFA"
        "886B423861285C97FFFFFFFFFFFFFFFF"
    ),
    "RFC 7919 ffdhe3072": (
        "FFFFFFFFFFFFFFFFADF85458A2BB4A9AAFDC5620273D3CF1D8B9C583CE2D3695A9E13641146433FBCC939DCE249B3EF9"
        "7D2FE363630C75D8F681B202AEC4617AD3DF1ED5D5FD65612433F51F5F066ED0856365553DED1AF3B557135E7F57C935"
        "984F0C70E0E68B77E2A689DAF3EFE8721DF158A136ADE73530ACCA4F483A797ABC0AB182B324FB61D108A94BB2C8E3FB"
        "B96ADAB760D7F4681D4F42A3DE394DF4AE56EDE76372BB190B07A7C8EE0A6D709E02FCE1CDF7E2ECC03404CD28342F61"
        "9172FE9CE98583FF8E4F1232EEF28183C3FE3B1B4C6FAD733BB5FCBC2EC22005C58EF1837D1683B2C6F34A26C1B2EFFA"
        "886B4238611FCFDCDE355B3B6519035BBC34F4DEF99C023861B46FC9D6E6C9077AD91D2691F7F7EE598CB0FAC186D91C"
        "AEFE130985139270B4130C93BC437944F4FD4452E2D74DD364F2E21E71F54BFF5CAE82AB9C9DF69EE86D2BC522363A0D"
        "ABC521979B0DEADA1DBF9A42D5C4484E0ABCD06BFA53DDEF3C1B20EE3FD59D7C25E41D2B66C62E37FFFFFFFFFFFFFFFF"
    ),
}


def odd_prime_table(N):
    """P[k] = 1 exactly when the odd number 2k + 1 is prime, k = 0 .. N (odd numbers up to 2N + 1)"""
    P = bytearray([1]) * (N + 1)
    P[0] = 0
    k = 1
    while (2 * k + 1) ** 2 <= 2 * N + 1:
        if P[k]:
            p = 2 * k + 1
            start = (p * p - 1) // 2
            P[start::p] = bytes(len(range(start, N + 1, p)))
        k += 1
    return P


def sophie_germain_count(N, P=None):
    """how many Sophie Germain primes p are below N (2 included)"""
    if N <= 2:
        return 0
    if P is None:
        P = odd_prime_table(N)
    m = (N - 2) // 2                                   # p = 2k + 1 < N  <=>  k <= m
    a = int.from_bytes(bytes(P[1:m + 1]), "little")      # entry k
    b = int.from_bytes(bytes(P[3:2 * m + 2:2]), "little")  # entry 2k + 1
    return 1 + bin(a & b).count("1")


def sophie_germain_list(N, P=None):
    """the Sophie Germain primes below N, in order"""
    if N <= 2:
        return []
    if P is None:
        P = odd_prime_table(N)
    return [2] + [2 * k + 1 for k in range(1, (N - 2) // 2 + 1) if P[k] and P[2 * k + 1]]


SMALL_PRIMES = [2] + [2 * k + 1 for k, v in enumerate(odd_prime_table(32768)) if v]   # primes below 65,536
DET_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
DET_LIMIT = 3317044064679887385961981            # below this, the bases 2 .. 41 make Miller-Rabin exact


def _composite_witness(a, n, d, s):
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return False
    return True


def is_prime(n, rounds=64, rng=None, bases=None):
    """exact below 3.3 x 10^24; above that, Miller-Rabin with `rounds` random bases"""
    if n < 2:
        return False
    for p in SMALL_PRIMES[:100]:
        if n == p:
            return True
        if n % p == 0:
            return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    if bases is None and n < DET_LIMIT:
        bases = DET_BASES
    if bases is not None:
        return not any(_composite_witness(a, n, d, s) for a in bases if a % n)
    rng = rng or secrets.SystemRandom()
    return not any(_composite_witness(rng.randrange(2, n - 1), n, d, s) for _ in range(rounds))


def pocklington_safe(q):
    """for q = 2p + 1 with p prime: True exactly when q is prime (2^(q-1) leaves 1 by q, and 3 does not divide q)"""
    return pow(2, q - 1, q) == 1 and q % 3 != 0


def is_safe_prime(q, rounds=64, rng=None):
    if q < 5 or q % 2 == 0:
        return False
    p = (q - 1) // 2
    return is_prime(p, rounds, rng) and pocklington_safe(q)


_SIEVE = [(r, pow(6, -1, r)) for r in SMALL_PRIMES if r > 3]


def safe_prime(bits, rng=None, window=4096, rounds=64):
    """a random safe prime q of exactly `bits` bits, and its Sophie Germain prime p = (q - 1)/2"""
    if bits < 6:
        raise ValueError("ask for 6 bits or more")
    rng = rng or secrets.SystemRandom()
    lo, hi = 1 << (bits - 2), (1 << (bits - 1)) - 1          # p has bits - 1 bits, so q = 2p + 1 has `bits`
    sieve = [(r, inv) for r, inv in _SIEVE if r < lo]
    while True:
        p0 = rng.randrange(lo, hi)
        p0 += (5 - p0 % 6) % 6                               # p leaves 5 by 6
        alive = bytearray([1]) * window
        for r, inv in sieve:
            for bad in (0, (r - 1) // 2):                    # r divides p, or r divides 2p + 1
                j = (bad - p0) * inv % r
                alive[j::r] = bytes(len(range(j, window, r)))
        j = alive.find(1)
        while j != -1:
            p = p0 + 6 * j
            if p > hi:
                break
            q = 2 * p + 1
            if pow(2, p - 1, p) == 1 and pocklington_safe(q) and is_prime(p, rounds, rng):
                return q, p
            j = alive.find(1, j + 1)


def as_int(s):
    s = s.strip().replace(" ", "").replace("_", "").replace(",", "")
    return int(s, 16) if s.lower().startswith("0x") else int(s)


def run_tests():
    results = []

    def claim(name, ok):
        results.append(bool(ok))
        print(("PASS  " if ok else "FAIL  ") + name)

    # OEIS A092816: Sophie Germain primes below 10^n
    a092816 = [3, 10, 37, 190, 1171, 7746, 56032]
    P = odd_prime_table(10 ** 7)
    got = [sophie_germain_count(10 ** n, P) for n in range(1, 8)]
    claim("counts below 10, 100, ..., 10^7 match OEIS A092816: %s" % got, got == a092816)

    # OEIS A005384 and A005385: the first 40 of each
    a005384 = [2, 3, 5, 11, 23, 29, 41, 53, 83, 89, 113, 131, 173, 179, 191, 233, 239, 251, 281, 293, 359, 419, 431,
               443, 491, 509, 593, 641, 653, 659, 683, 719, 743, 761, 809, 911, 953, 1013, 1019, 1031]
    a005385 = [5, 7, 11, 23, 47, 59, 83, 107, 167, 179, 227, 263, 347, 359, 383, 467, 479, 503, 563, 587, 719, 839,
               863, 887, 983, 1019, 1187, 1283, 1307, 1319, 1367, 1439, 1487, 1523, 1619, 1823, 1907, 2027, 2039, 2063]
    sg = sophie_germain_list(10 ** 6, P)
    claim("first 40 Sophie Germain primes match OEIS A005384", sg[:40] == a005384)
    claim("first 40 safe primes match OEIS A005385", [2 * p + 1 for p in sg[:40]] == a005385)

    claim("forced: above 3 every one leaves 2 by 3, so p and 2p + 1 have root 2, 5 or 8 (%d checked)" % len(sg),
          all(p % 3 == 2 and (2 * p + 1) % 3 == 2 for p in sg if p > 3))
    claim("forced: above 7 every safe prime leaves 11 by 12", all((2 * p + 1) % 12 == 11 for p in sg if p > 3))

    tested = 0
    ok = True
    for p in sg[:2000]:
        q = 2 * p + 1
        tested += 1
        ok &= pocklington_safe(q)
    for k in range(1, 50000):
        p, q = 2 * k + 1, 4 * k + 3
        if P[k] and not P[2 * k + 1]:
            tested += 1
            ok &= not pocklington_safe(q)
    claim("Pocklington step: right on every q = 2p + 1 with p prime, prime or not (%d tried)" % tested, ok)

    # the Miller-Rabin trap the repo found on 2026-09-30: bases 2 .. 37 call this composite prime
    trap = 318665857834031151167461
    claim("318665857834031151167461 = 399165290221 x 798330580441", trap == 399165290221 * 798330580441)
    claim("bases 2 .. 37 are fooled by it, bases 2 .. 41 are not",
          is_prime(trap, bases=DET_BASES[:-1]) and not is_prime(trap))
    claim("small cases: 561, 1105, 2047, 3215031751 composite; 2, 3, 65537, 2^61 - 1 prime",
          not any(is_prime(n) for n in (561, 1105, 2047, 3215031751)) and
          all(is_prime(n) for n in (2, 3, 65537, 2 ** 61 - 1)))

    for name, h in DH_PRIMES.items():
        q = int("".join(h), 16)
        claim("%s is a safe prime" % name, is_safe_prime(q, rounds=16))

    for bits, seed in ((16, 1), (64, 2), (128, 3), (256, 4)):
        q, p = safe_prime(bits, rng=random.Random(seed))
        claim("made a %d-bit safe prime: %d" % (bits, q) if bits <= 64 else "made a %d-bit safe prime" % bits,
              q.bit_length() == bits and q == 2 * p + 1 and is_safe_prime(q) and p % 6 == 5)
    return all(results)


def main(args):
    if not args or args[0] == "--test":
        return 0 if run_tests() else 1
    if args[0] == "--bits":
        bits = int(args[1]) if len(args) > 1 else 1024
        t = time.time()
        q, p = safe_prime(bits)
        print("safe prime q (%d bits), made in %.1f s" % (q.bit_length(), time.time() - t))
        print("q =", q)
        print("q = 0x%X" % q)
        print("p = (q - 1)/2 =", p)
        sure = "proved" if p < DET_LIMIT else "Miller-Rabin, 64 rounds"
        print("p prime: %s;  q prime: proved from p (Pocklington)" % sure)
        print("generator: 4 (makes the group of size p)" + ("; 2 also works (q leaves 7 by 8)" if q % 8 == 7 else ""))
        return 0
    if args[0] == "--check":
        for s in args[1:]:
            q = as_int(s)
            if is_safe_prime(q):
                print("safe prime: q = %s, p = (q - 1)/2 is prime" % s)
            elif q % 2 == 1 and is_prime(q):
                print("prime, but not safe: (q - 1)/2 = %d is not prime" % ((q - 1) // 2))
            else:
                print("not a safe prime (not prime)")
        return 0
    N = as_int(args[0])
    P = odd_prime_table(max(N, 3))
    count = sophie_germain_count(N, P)
    first = sophie_germain_list(min(N, 2000), P)[:20]
    print("Sophie Germain primes below %d: %d" % (N, count))
    print("first ones:   ", " ".join(map(str, first)))
    print("safe primes:  ", " ".join(str(2 * p + 1) for p in first))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

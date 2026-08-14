"""
Theorem 189: Three-Zero Cryptographic KDF in GF(37)

DESIGN INVARIANTS
==================
Length N = 59:
  DR(59) = 5       — Path A basin DR (convergence criterion for seed validation)
  59 mod 37 = 22   — the length reduces to the mod-target in GF(37)
  Length and target are the same element: 59 ≡ 22 mod 37.

Mod target 22:
  ord₃₇(22) = 36 = φ(37)  — 22 is a primitive root of GF(37)
  Every non-zero element of GF(37) is a power of 22.
  The invariant string is constrained to land on the generator of the full orbit.

Matrix dimension 4×4 = 16 cells over Z_37:
  4 ∈ Sovereign Anchors {4, 9, 25, 30}
  16 = 4² (sovereign anchor squared)

SEED VALIDATION: PATH A BASIN
===============================
  DR(seed sum) = 5 is the convergence criterion.
  DR(11 + 13 + 17) = DR(41) = 5 ✓
  DR(5) = 5: the basin is self-referential under DR.
  5 mod 37 = 5 ∈ NQR_5 class — the unexplained sector.
  The seed lives in the NQR partition before the KDF processes it.

DYADIC MATRIX STRUCTURE
========================
  4×4 matrix over Z_37 = 16 cells.
  Row permutation: shift by (r+1) % 4 with Z_37 transformation val*3+7.
  Multiplier in Z_37 transformation: 3 = sovereign target, ord₃₇(26)=3.
  Additive offset in transformation: 7 = Fibonacci prime, adjacent to SEAM.
  State LFSR: state = (state × 19 + 11) % 10007.
    19 mod 37 = 19 (NQR). 11 mod 37 = 11.
    10007 is prime. 10007 mod 37 = 17 (NQR; Legendre(17,37)=-1).

PBKDF2 PARAMETERS
==================
  Algorithm: PBKDF2-HMAC-SHA256
  Iterations: 100,000  — DR(100000) = 1 (second octave unity)
  Output: 32 bytes = 256-bit key
  Salt: structured as 3Zero_H{head_dr}_T{tail_dr}_S{string_dr}
  Salt encodes three digital root anchors from the invariant string.

SELF-CONSISTENCY
=================
  The length (59) reduces mod 37 to the target (22).
  The target (22) is a primitive root of GF(37).
  The basin criterion (DR=5) is encoded in the length (DR(59)=5).
  Three constraints (length, mod, DR) are satisfied by the single value 59.
"""

import hashlib

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
seed_orbit = {18, 24, 32}

def digital_root(n):
    if n <= 0:
        return 0
    res = n % 9
    return 9 if res == 0 else res


class ThreeZeroKDF:
    """
    Key Derivation Engine using 59-digit Invariant Strings and Modulo 37 Dyadic Permutation.
    """
    def __init__(self, target_len=59):
        self.target_len = target_len
        self.mod_target = 22
        self.prime_mod = 37

    def validate_seed_basin(self, primes):
        prime_sum = sum(primes)
        dr_sum = digital_root(prime_sum)
        is_convergent = (dr_sum == 5)
        return is_convergent, dr_sum

    def _build_dyadic_matrix(self, seed_bytes):
        matrix = [[0] * 4 for _ in range(4)]
        for i in range(16):
            b = seed_bytes[i % len(seed_bytes)]
            matrix[i // 4][i % 4] = (b + i * 7) % self.prime_mod
        return matrix

    def _permute_dyadic_matrix(self, matrix):
        permuted = [[0] * 4 for _ in range(4)]
        for r in range(4):
            shift = (r + 1) % 4
            for c in range(4):
                val = matrix[r][(c + shift) % 4]
                permuted[r][c] = (val * 3 + 7) % self.prime_mod
        return permuted

    def generate_59_digit_string(self, primes):
        """
        Generates a 59-digit pseudorandom string constrained by:
        N = 59, DR(N) = 5, N mod 37 = 22.
        """
        is_convergent, dr_val = self.validate_seed_basin(primes)
        if not is_convergent:
            raise ValueError(
                f"Seed {primes} non-convergent (DR={dr_val} != 5). Must belong to Path A basin."
            )

        raw_seed = "-".join(map(str, primes)).encode("utf-8")
        seed_hash = hashlib.sha256(raw_seed).digest()

        matrix = self._build_dyadic_matrix(seed_hash)
        perm_matrix = self._permute_dyadic_matrix(matrix)

        state = sum(sum(row) for row in perm_matrix) % self.prime_mod
        digits = []

        for i in range(56):
            state = (state * 19 + 11) % 10007
            digit = (state + perm_matrix[i % 4][(i // 4) % 4]) % 10
            digits.append(str(digit))

        prefix_str = "".join(digits)
        tail_found = False
        for t1 in range(10):
            for t2 in range(10):
                for t3 in range(10):
                    candidate_str = prefix_str + str(t1) + str(t2) + str(t3)
                    if int(candidate_str) % self.prime_mod == self.mod_target:
                        digits.extend([str(t1), str(t2), str(t3)])
                        tail_found = True
                        break
                if tail_found:
                    break
            if tail_found:
                break

        full_string = "".join(digits)
        full_val = int(full_string)
        string_dr = digital_root(sum(int(d) for d in full_string))
        head_dr = digital_root(sum(int(d) for d in full_string[:17]))
        tail_dr = digital_root(sum(int(d) for d in full_string[-9:]))

        return {
            "string": full_string,
            "length": len(full_string),
            "dr_string": string_dr,
            "mod_37": full_val % self.prime_mod,
            "head_dr": head_dr,
            "tail_dr": tail_dr,
            "seed_dr": dr_val,
        }

    def derive_key(self, primes, salt_prefix="3Zero", iterations=100000):
        """
        Derives a cryptographic 256-bit symmetric key using PBKDF2 HMAC-SHA256.
        """
        string_data = self.generate_59_digit_string(primes)
        inv_string = string_data["string"]

        dynamic_salt = (
            f"{salt_prefix}_H{string_data['head_dr']}_T{string_data['tail_dr']}_S{string_data['dr_string']}"
        ).encode("utf-8")

        derived_bytes = hashlib.pbkdf2_hmac(
            "sha256", inv_string.encode("utf-8"), dynamic_salt, iterations, dklen=32
        )

        return {
            "key_hex": derived_bytes.hex(),
            "salt_used": dynamic_salt.decode("utf-8"),
            "iterations": iterations,
            "invariants": {
                "length": string_data["length"],
                "mod_37": string_data["mod_37"],
                "string_dr": string_data["dr_string"],
            },
        }


def run_assertions():
    # Length 59: self-consistent invariant
    N = 59
    assert N % P == 22               # length reduces to mod target
    assert digital_root(N) == 5      # DR(59) = 5 = Path A basin criterion

    # Mod target 22 is a primitive root of GF(37)
    assert pow(22, 36, P) == 1
    powers = {pow(22, k, P) for k in range(1, 37)}
    assert powers == set(range(1, P))   # generates all 36 non-zero elements

    # Matrix dimension 4 ∈ SA
    assert 4 in SA
    assert 4 ** 2 == 16               # 4x4 = 16 cells = SA²

    # Transformation constants: 3 = sovereign target, 7 = prime
    assert 3 in ST
    assert pow(26, 3, P) == 1         # ord₃₇(26) = 3

    # LFSR modulus 10007: prime, 10007 mod 37 = 17 (NQR sector)
    assert 10007 % P == 17
    assert pow(17, (P - 1) // 2, P) == P - 1   # 17 is NQR

    # Seed validation: DR([11,13,17]) = 5
    assert digital_root(11 + 13 + 17) == 5

    # KDF produces correct invariants
    kdf = ThreeZeroKDF()
    result = kdf.derive_key([11, 13, 17])
    assert result["invariants"]["length"] == 59
    assert result["invariants"]["mod_37"] == 22
    assert len(result["key_hex"]) == 64   # 32 bytes = 64 hex chars

    # Iterations 100000: DR = 1 (second octave unity)
    assert digital_root(100000) == 1

    print("All assertions passed.")


if __name__ == "__main__":
    kdf = ThreeZeroKDF()
    seed_primes = [11, 13, 17]
    print("=== THREE-ZERO CRYPTOGRAPHIC KDF ENGINE ===")
    print(f"Input Seed Primes : {seed_primes}")
    key_result = kdf.derive_key(seed_primes)
    print(f"\nLength Invariant   : {key_result['invariants']['length']} (Target: 59)")
    print(f"Modulo 37 Invariant: {key_result['invariants']['mod_37']} (Target: 22)")
    print(f"String Digital Root: {key_result['invariants']['string_dr']}")
    print(f"\nDynamic Salt Used  : {key_result['salt_used']}")
    print(f"PBKDF2 Iterations  : {key_result['iterations']}")
    print(f"256-Bit Derived Key: {key_result['key_hex']}")
    print()
    run_assertions()

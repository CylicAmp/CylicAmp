"""
Corrected, deterministic, falsifiable implementation.
All claims computed; no hardcoded truths.
Includes proper Reed-Solomon over GF(37), BCH(7,4) over GF(2),
narcissistic number verification, 2048 dash splits,
meta-evolve engine, anchor codes, and exact arithmetic.
"""

import math
from itertools import product

# ===================== GF(37) =====================
class GF37:
    p = 37
    def add(self, a, b): return (a + b) % self.p
    def sub(self, a, b): return (a - b) % self.p
    def mul(self, a, b): return (a * b) % self.p
    def inv(self, a):
        for i in range(1, self.p):
            if self.mul(a, i) == 1: return i
        raise ValueError(f"{a} not invertible mod {self.p}")
    def zero_pair(self, a): return (a, self.sub(0, a))

# ===================== Reed-Solomon over GF(37) =====================
class ReedSolomon:
    """
    Systematic RS(n=10, k=6) over GF(37), t=2 errors correctable.
    Convention: all polynomials are high-degree-first lists.
    Generator: g(x) = prod_{i=1}^{n-k}(x - alpha^i), alpha=2.
    Roots at alpha^1..alpha^4; syndromes S_j = c(alpha^j) for j=1..4.
    """
    def __init__(self, n=10, k=6, gf=None):
        self.gf = gf or GF37()
        self.n = n
        self.k = k
        self.t = (n - k) // 2
        self.alpha = 2
        self.gen = self._gen_poly()

    def _gen_poly(self):
        # g(x) = (x-alpha)(x-alpha^2)...(x-alpha^{n-k}), high-degree first
        # x*g appends 0; then subtract root*g[j] from position j+1
        g = [1]
        for i in range(1, self.n - self.k + 1):
            root = pow(self.alpha, i, self.gf.p)
            new_g = g + [0]
            for j in range(len(g)):
                new_g[j + 1] = self.gf.sub(new_g[j + 1], self.gf.mul(root, g[j]))
            g = new_g
        return g

    def _poly_div_rem(self, dividend, divisor):
        """Polynomial division; returns remainder (high-degree first)."""
        r = dividend[:]
        dlen = len(divisor)
        for i in range(len(r) - dlen + 1):
            if r[i] == 0:
                continue
            c = self.gf.mul(r[i], self.gf.inv(divisor[0]))
            for j in range(dlen):
                r[i + j] = self.gf.sub(r[i + j], self.gf.mul(c, divisor[j]))
        return r[-(dlen - 1):]  # remainder has degree < len(divisor)-1

    def _eval(self, poly, x):
        """Evaluate polynomial at x (Horner, high-degree first)."""
        y = 0
        for c in poly:
            y = self.gf.add(self.gf.mul(y, x), c)
        return y

    def encode(self, msg):
        """Systematic encode: codeword = [msg | parity]."""
        if len(msg) != self.k:
            raise ValueError(f"msg must have length {self.k}")
        # Shift message up: m(x)*x^(n-k)
        padded = msg + [0] * (self.n - self.k)
        parity = self._poly_div_rem(padded, self.gen)
        # Subtract remainder to make divisible by gen
        codeword = msg + [self.gf.sub(0, p) for p in parity]
        return codeword

    def syndromes(self, received):
        return [self._eval(received, pow(self.alpha, i, self.gf.p))
                for i in range(1, self.n - self.k + 1)]

    def decode(self, received):
        """Decode received word; return message or None if uncorrectable."""
        if len(received) != self.n:
            raise ValueError(f"received must have length {self.n}")
        S = self.syndromes(received)
        if all(s == 0 for s in S):
            return received[:self.k]
        # BM returns sigma low-degree-first: sigma[0]=1, sigma[j]=coeff of x^j
        sigma = self._berlekamp_massey(S)
        # Chien search: sigma root at alpha^{-i} means error at position i
        error_locs = []
        for i in range(self.n):
            xi_inv = pow(self.alpha, -i, self.gf.p)
            if self._eval(sigma[::-1], xi_inv) == 0:  # reverse for hdf eval
                error_locs.append(i)
        if len(error_locs) != len(sigma) - 1:
            return None
        # Forney: omega = S(x)*sigma(x) mod x^{2t}, all low-degree-first
        # e_k = -omega(X_k^{-1}) / sigma'(X_k^{-1}), b0=1 convention
        # Chien i = polynomial power k; array index = n-1-k
        omega = self._poly_mul_mod(S, sigma, 2 * self.t)
        sigma_prime = self._formal_derivative(sigma)
        corrected = list(received)
        for i in error_locs:
            xi_inv = pow(self.alpha, -i, self.gf.p)
            arr_idx = self.n - 1 - i
            num = self.gf.sub(0, self._eval(omega[::-1], xi_inv))
            den = self._eval(sigma_prime[::-1], xi_inv)
            if den == 0:
                return None
            ei = self.gf.mul(num, self.gf.inv(den))
            corrected[arr_idx] = self.gf.sub(corrected[arr_idx], ei)
        if all(s == 0 for s in self.syndromes(corrected)):
            return corrected[:self.k]
        return None

    def _berlekamp_massey(self, S):
        """Return error locator polynomial sigma (high-degree last, i.e. sigma[0]=1)."""
        n = len(S)
        C = [1] + [0] * n   # current sigma
        B = [1] + [0] * n   # previous sigma
        L, m, b = 0, 1, 1
        for i in range(n):
            d = S[i]
            for j in range(1, L + 1):
                d = self.gf.add(d, self.gf.mul(C[j], S[i - j]))
            if d == 0:
                m += 1
            elif 2 * L <= i:
                T = C[:]
                coef = self.gf.mul(d, self.gf.inv(b))
                for j in range(m, n + 1):
                    C[j] = self.gf.sub(C[j], self.gf.mul(coef, B[j - m]))
                L, B, b, m = i + 1 - L, T, d, 1
            else:
                coef = self.gf.mul(d, self.gf.inv(b))
                for j in range(m, n + 1):
                    C[j] = self.gf.sub(C[j], self.gf.mul(coef, B[j - m]))
                m += 1
        return C[:L + 1]

    def _poly_mul_mod(self, a, b, deg):
        """Multiply two polynomials (low-degree first) and truncate to deg terms."""
        res = [0] * deg
        for i, ca in enumerate(a):
            for j, cb in enumerate(b):
                if i + j < deg:
                    res[i + j] = self.gf.add(res[i + j], self.gf.mul(ca, cb))
        return res

    def _formal_derivative(self, poly):
        """Formal derivative of polynomial (low-degree first)."""
        return [self.gf.mul((i + 1) % self.gf.p, poly[i + 1])
                for i in range(len(poly) - 1)]

# ===================== BCH(7,4) over GF(2) =====================
class BCH_7_4:
    """BCH(7,4) code with generator polynomial g(x)=1+x+x^3, corrects 1 error."""
    def __init__(self):
        self.gen = [1, 0, 1, 1]
        self.n = 7
        self.k = 4

    def encode(self, msg):
        if len(msg) != self.k: raise ValueError("msg length must be 4")
        poly = msg + [0,0,0]
        _, rem = self._gf2_poly_div(poly, self.gen)
        return msg + rem[:3]

    def _gf2_poly_div(self, a, b):
        a = a[:]
        for i in range(len(a)-len(b)+1):
            if a[i] == 1:
                for j in range(len(b)):
                    a[i+j] ^= b[j]
        return [], a[-len(b)+1:]

    def decode(self, received):
        if len(received) != self.n: raise ValueError("received length must be 7")
        # g(x)=x^3+x+1 has roots alpha,alpha^2,alpha^4; syndrome = c(alpha) in HDF
        # c_HDF(alpha) = sum_i received[i] * alpha^{n-1-i}
        alpha = 2
        s1 = 0
        for i, bit in enumerate(received):
            if bit:
                s1 ^= self._gf8_pow(alpha, self.n - 1 - i)
        if s1 == 0:
            return received[:self.k]
        # binary BCH: error at position j gives S1 = alpha^{n-1-j}
        # so n-1-j = log(S1), j = n-1-log(S1)
        exp = self._gf8_log(s1)
        if exp is None:
            return None
        arr_idx = self.n - 1 - exp
        if arr_idx < 0 or arr_idx >= self.n:
            return None
        corrected = received[:]
        corrected[arr_idx] ^= 1
        # verify: s1 of corrected should be 0
        s1c = 0
        for i, bit in enumerate(corrected):
            if bit:
                s1c ^= self._gf8_pow(alpha, self.n - 1 - i)
        if s1c == 0:
            return corrected[:self.k]
        return None

    def _gf8_mul(self, a, b):
        p = 0
        for _ in range(3):
            if b & 1: p ^= a
            a <<= 1
            if a & 0b1000: a ^= 0b1011
            b >>= 1
        return p & 0b111

    def _gf8_pow(self, base, exp):
        res = 1
        for _ in range(exp):
            res = self._gf8_mul(res, base)
        return res

    def _gf8_log(self, a):
        if a == 0: raise ValueError("log(0)")
        for i in range(7):
            if self._gf8_pow(2, i) == a:
                return i
        return None

# ===================== Sum of cubes =====================
def sum_of_cubes(n):
    return sum(int(d)**3 for d in str(abs(n)))

def narcissistic_series(start, max_iter=100):
    seen = set()
    path = [start]
    cur = start
    for _ in range(max_iter):
        cur = sum_of_cubes(cur)
        path.append(cur)
        if cur in seen:
            break
        seen.add(cur)
    return path

# ===================== Dash splits =====================
def generate_dash_splits(digit_string="137035999177"):
    n = len(digit_string)
    total = 1 << (n-1)
    splits = []
    for mask in range(total):
        parts = []
        current = digit_string[0]
        for i in range(n-1):
            if mask & (1 << i):
                parts.append(current)
                current = digit_string[i+1]
            else:
                current += digit_string[i+1]
        parts.append(current)
        splits.append(parts)
    return splits

# ===================== Anchor codes =====================
def anchor_code_to_palindrome(code_int):
    """Given integer like 153 or 137, return palindrome [anchor, bridge, peak, bridge, anchor].
    bridge = the digit that is neither anchor nor peak (the mediator)."""
    digits = [int(d) for d in str(code_int)]
    anchor = digits[0]
    peak = max(digits)
    remaining = [d for d in digits if d != anchor and d != peak]
    bridge = remaining[0] if remaining else digits[-1]
    return [anchor, bridge, peak, bridge, anchor]

# ===================== Meta-evolve engine =====================
class MetaEvolveEngine:
    def __init__(self, multiplier=1, cycle_state=None):
        self.multiplier = multiplier
        self.cycle_state = cycle_state or [7,3,11,2,5,13]
        self.mod_internal = 97
        self.mod_final = 999

    def run(self, num_cycles=3):
        state = self.cycle_state[:]
        hist = []
        for _ in range(num_cycles):
            state = [(v * self.multiplier + 1) % self.mod_internal for v in state]
            hist.append(state[:])
        final = sum(state) % self.mod_final + 1
        return {"final_state": final, "max_value": max(state), "state": state, "history": hist}

    def meta_evolve_lane(self, seed=246, iters=3):
        history = []
        cur_mult = self.multiplier
        cur_cycle = self.cycle_state[:]
        for step in range(iters):
            self.multiplier = cur_mult
            self.cycle_state = cur_cycle[:]
            result = self.run(3)
            new_mult = (result["max_value"] % 10) + 1
            new_cycle = [d % 13 for d in result["state"][:6]]
            seed = result["final_state"]
            history.append({"step": step+1, "multiplier": new_mult, "final_state": seed})
            cur_mult = new_mult
            cur_cycle = new_cycle[:]
        self.multiplier = cur_mult
        return history

    def prove_zero_excluded(self, tests=100):
        results = []
        for s in range(1, tests+1):
            self.cycle_state = [s % 13 for _ in range(6)]
            results.append(self.run()["final_state"])
        return {"min": min(results), "max": max(results), "zero_present": 0 in results}

# ===================== Exact arithmetic =====================
from fractions import Fraction
A = Fraction(137035999177, 1_000_000_000)
B = Fraction(153327351153, 1_000_000_000)

# ===================== Assertions =====================
def run_all_tests():
    fails = []
    gf = GF37()

    # GF(37): every element has an additive inverse summing to 0
    for a in range(37):
        neg = gf.sub(0, a)
        if gf.add(a, neg) != 0:
            fails.append(f"GF37 zero pair failed for {a}")

    # GF(37): multiplicative inverses
    for a in range(1, 37):
        inv_a = gf.inv(a)
        if gf.mul(a, inv_a) != 1:
            fails.append(f"GF37 inv failed for {a}")

    # GF(37): specific values
    assert gf.add(10, 20) == 30
    assert gf.mul(5, 7) == 35
    assert gf.mul(5, gf.inv(5)) == 1
    assert 137 % 37 == 26
    assert 153 % 37 == 5
    assert 371 % 37 == 1
    assert 713 % 37 == 10
    assert 999 % 37 == 0

    # Narcissistic numbers (3-digit cube sums)
    known_narc = {1, 153, 370, 371, 407}
    found_narc = {n for n in range(1, 1000) if sum_of_cubes(n) == n}
    if found_narc != known_narc:
        fails.append(f"Narcissistic numbers mismatch: {found_narc} != {known_narc}")

    # Trajectory from 3 reaches 153
    traj3 = narcissistic_series(3)
    if 3 not in traj3 or 27 not in traj3 or 351 not in traj3 or 153 not in traj3:
        fails.append(f"Trajectory from 3 incomplete: {traj3}")
    if traj3.index(27) < traj3.index(3) or traj3.index(351) < traj3.index(27):
        fails.append("Trajectory from 3 out of order")

    # Trajectory from 137 reaches 371 (fixed point)
    traj137 = narcissistic_series(137)
    if traj137[-1] != 371:
        fails.append(f"Trajectory from 137 ended at {traj137[-1]}, expected 371")
    assert sum_of_cubes(371) == 371, "371 must be a fixed point of sum_of_cubes"

    # Reed-Solomon: no-error case
    rs = ReedSolomon()
    msg = [5, 10, 15, 20, 25, 30]
    codeword = rs.encode(msg)
    if len(codeword) != 10:
        fails.append(f"RS codeword length {len(codeword)} != 10")
    decoded = rs.decode(codeword)
    if decoded != msg:
        fails.append(f"RS uncorrupted decode failed: {decoded} != {msg}")

    # Reed-Solomon: single error correction
    cw_err = codeword[:]
    cw_err[3] = gf.add(cw_err[3], 1)
    dec_err = rs.decode(cw_err)
    if dec_err != msg:
        fails.append(f"RS single error correction failed: {dec_err} != {msg}")

    # BCH(7,4): no-error
    bch = BCH_7_4()
    bch_msg = [1, 0, 1, 1]
    cw = bch.encode(bch_msg)
    if len(cw) != 7:
        fails.append(f"BCH codeword length {len(cw)} != 7")
    if bch.decode(cw) != bch_msg:
        fails.append("BCH uncorrupted decode failed")

    # BCH(7,4): single error correction
    for err_pos in range(7):
        cw_err = cw[:]
        cw_err[err_pos] ^= 1
        dec = bch.decode(cw_err)
        if dec != bch_msg:
            fails.append(f"BCH single error at pos {err_pos} correction failed: {dec}")

    # Dash splits
    splits = generate_dash_splits()
    if len(splits) != 2048:
        fails.append(f"Dash splits count {len(splits)} != 2048")
    if splits[0] != ["137035999177"]:
        fails.append(f"Split 0 wrong: {splits[0]}")
    if splits[-1] != list("137035999177"):
        fails.append(f"Split -1 wrong: {splits[-1]}")

    # Meta-evolve: final_state always >= 1 (never 0)
    eng = MetaEvolveEngine()
    proof = eng.prove_zero_excluded()
    if proof["zero_present"]:
        fails.append("MetaEvolve final_state reached zero")
    if proof["min"] < 1:
        fails.append(f"MetaEvolve min final_state {proof['min']} < 1")

    # Exact arithmetic
    diff = B - A
    expected_diff = Fraction(16291351976, 1_000_000_000)
    if diff != expected_diff:
        fails.append(f"B-A = {diff}, expected {expected_diff}")
    # Verify the simplified form
    assert diff == Fraction(2036418997, 125_000_000), \
        f"B-A simplified = {diff.limit_denominator()}"

    # Anchor code palindromes
    pal153 = anchor_code_to_palindrome(153)
    pal137 = anchor_code_to_palindrome(137)
    assert pal153 == [1, 3, 5, 3, 1], f"153 palindrome = {pal153}"
    assert pal137 == [1, 3, 7, 3, 1], f"137 palindrome = {pal137}"
    # Both are palindromes
    assert pal153 == pal153[::-1], "153 palindrome must be symmetric"
    assert pal137 == pal137[::-1], "137 palindrome must be symmetric"

    # Fine structure constant
    assert 137 % 37 == 26
    assert list("137035999177") == [str(d) for d in [1,3,7,0,3,5,9,9,9,1,7,7]]
    assert "137035999177"[::-1] == "771999530731"

    if fails:
        print("FAILURES:")
        for f in fails:
            print(f"  - {f}")
        return False
    print("All assertions passed.")
    return True


if __name__ == "__main__":
    success = run_all_tests()
    import sys
    sys.exit(0 if success else 1)

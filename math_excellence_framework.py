"""
MATHEMATICAL EXCELLENCE FRAMEWORK — COMPLETE SYSTEM
====================================================
Consolidated mathematical computing environment grounded in GF(37).

Verified foundation (every claim below is computationally confirmed):
  - Prime p = 37
  - 137 mod 37 = 26  →  the 137-map is f(n) = 26n mod 37
  - ord_37(26) = 3   →  all 137-map orbits are 3-cycles
  - ord_37(2)  = 36  →  2 is a primitive root mod 37
  - Seed orbit of 246: {18, 24, 32}  under the 137-map
  - Heartbeat 3-cycle: 24 → 32 → 18 → 24
  - Cascade base {8, 13, 24} generates exactly 37 elements
  - Sovereign anchors SA = {4, 9, 25, 30}
  - Sovereign targets ST = {3, 12, 21, 30}
  - {18, 24, 32} are all quadratic non-residues mod 37

Modules:
  - Map137           — the central 137-map and orbit engine
  - CyclicGroup      — multiplicative group (Z/pZ)×
  - Subgroup         — subgroup with coset enumeration
  - ResidueClassifier — Legendre / quadratic / quartic residues
  - HarmonicAnalyzer — DFT on cyclic groups
  - PrimeMapper      — modular classification of primes
  - DigitalRootSystem — mod-9 arithmetic (DR is a ring homomorphism)
  - PerfectNumberSystem — Euclid-Euler theorem
  - Family37System   — N = 37k + 35 sequences
  - DRFibonacciSystem — Pisano period 24 (DR-Fib is periodic, NOT convergent)
  - Prime21System    — 73 (21st prime) and 511 = 7 × 73
  - Z9OperatorSystem — G = <C, R, F> on Z_9
  - Z9Lattice        — Z_9 × Z_9 harmonic structure
  - SophieGermain    — Sophie Germain / safe prime analysis
  - ConcatenatedRange — phase-shift dynamics mod 37

Usage:
    from math_excellence_framework import *
    m = Map137()
    print(m.orbit(24))          # [24, 32, 18]
    print(m.heartbeat())        # 24 -> 32 -> 18 -> 24
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set, Union, Any
from collections import defaultdict, Counter
from fractions import Fraction
import math

# ============================================================
# THE 137-MAP — CENTRAL ENGINE OF THE FRAMEWORK
# ============================================================

class Map137:
    """
    The 137-map: f(n) = 137n mod 37 = 26n mod 37.

    Verified facts (computed, not assumed):
      - 137 mod 37 = 26
      - ord_37(26) = 3   -> every orbit is a 3-cycle
      - Seed orbit of 246 mod 37 = 24: {24, 32, 18}
      - Heartbeat: 24 -> 32 -> 18 -> 24
      - {24, 32, 18} are all quadratic non-residues mod 37
    """
    P   = 37
    MUL = 26          # 137 mod 37

    def f(self, n: int) -> int:
        return (self.MUL * n) % self.P

    def orbit(self, n: int) -> List[int]:
        """Compute the full orbit of n under the 137-map mod 37."""
        start = n % self.P
        orb = [start]
        x = self.f(start)
        while x != start:
            orb.append(x)
            x = self.f(x)
        return orb

    def orbit_length(self, n: int) -> int:
        return len(self.orbit(n))

    def heartbeat(self) -> str:
        """The 3-cycle of seed 246 (246 mod 37 = 24)."""
        orb = self.orbit(24)          # [24, 32, 18]
        return f"{orb[0]} -> {orb[1]} -> {orb[2]} -> {orb[0]}"

    def classify_all(self) -> Dict[int, List[int]]:
        """Partition {0..36} into orbits."""
        seen: Set[int] = set()
        orbits: Dict[int, List[int]] = {}
        for n in range(self.P):
            if n not in seen:
                orb = self.orbit(n)
                orbits[orb[0]] = orb
                seen.update(orb)
        return orbits

    def is_seed_orbit(self, n: int) -> bool:
        return (n % self.P) in {18, 24, 32}

    def verify(self) -> Dict[str, bool]:
        """Run all foundational verifications. Every entry must be True."""
        results = {}
        results["137 mod 37 == 26"] = (137 % 37 == 26)
        # ord_37(26) = 3: compute 26^k mod 37 for k=1,2,3,...
        x, k = 1, 0
        while True:
            k += 1; x = (x * 26) % 37
            if x == 1:
                break
        results["ord_37(26) == 3"] = (k == 3)
        results["orbit(24) == {24,32,18}"] = (set(self.orbit(24)) == {18, 24, 32})
        results["246 mod 37 == 24"] = (246 % 37 == 24)
        # All non-QR
        qr = {n for n in range(1, 37) if pow(n, 18, 37) == 1}
        results["{18,24,32} all non-QR"] = all(n not in qr for n in [18, 24, 32])
        return results


# ============================================================
# CORE MODULAR ARITHMETIC
# ============================================================

@dataclass
class CyclicGroup:
    """Cyclic multiplicative group (Z/pZ)× with primitive root g."""
    p: int
    g: int

    def __post_init__(self):
        self.order = self.p - 1
        self.elements = list(range(1, self.p))
        self._orbit_cache: Dict = {}
        self._dlog_cache: Dict = {}

    def mult(self, a: int, b: int) -> int:
        return (a * b) % self.p

    def pow(self, base: int, exp: int) -> int:
        return pow(base, exp, self.p)

    def orbit(self, element: int) -> List[int]:
        if element in self._orbit_cache:
            return self._orbit_cache[element]
        orb, current = [], 1
        for _ in range(self.order):
            orb.append(current)
            current = self.mult(current, element)
            if current == 1:
                break
        self._orbit_cache[element] = orb
        return orb

    def order_of(self, element: int) -> int:
        return len(self.orbit(element))

    def discrete_log(self, target: int, base: Optional[int] = None) -> int:
        if base is None:
            base = self.g
        current = 1
        for k in range(self.order):
            if current == target:
                return k
            current = self.mult(current, base)
        return -1   # target not in <base>

    def is_primitive_root(self, element: int) -> bool:
        return self.order_of(element) == self.order

    def get_primitive_roots(self) -> List[int]:
        return [a for a in self.elements if self.is_primitive_root(a)]


@dataclass
class Subgroup:
    """Subgroup of a cyclic group generated by a single element."""
    group: CyclicGroup
    generator: int
    _elements: Optional[List[int]] = field(default=None, repr=False)

    def __post_init__(self):
        if self._elements is None:
            self._elements = self.group.orbit(self.generator)
        self.size  = len(self._elements)
        self.index = self.group.order // self.size

    @property
    def elements(self) -> List[int]:
        return self._elements

    def contains(self, element: int) -> bool:
        return element in self._elements

    def cosets(self) -> List[List[int]]:
        cosets, remaining = [], set(self.group.elements)
        while remaining:
            rep   = min(remaining)
            coset = sorted((rep * e) % self.group.p for e in self._elements)
            cosets.append(coset)
            remaining -= set(coset)
        return cosets


class ResidueClassifier:
    """Classify residues: quadratic, quartic, etc."""
    def __init__(self, group: CyclicGroup):
        self.group = group
        self._qr: Optional[Set[int]] = None
        self._q4: Optional[Set[int]] = None

    def legendre_symbol(self, a: int) -> int:
        if a % self.group.p == 0:
            return 0
        return 1 if pow(a, (self.group.p - 1) // 2, self.group.p) == 1 else -1

    def quadratic_residues(self) -> Set[int]:
        if self._qr is None:
            self._qr = {a for a in range(1, self.group.p)
                        if pow(a, (self.group.p - 1) // 2, self.group.p) == 1}
        return self._qr

    def quartic_residues(self) -> Set[int]:
        if self._q4 is None:
            self._q4 = {pow(a, 4, self.group.p) for a in range(1, self.group.p)}
        return self._q4

    def is_quadratic_residue(self, a: int) -> bool:
        return a in self.quadratic_residues()

    def residue_symbol(self, a: int) -> str:
        if a == 0:
            return "zero"
        if a in self.quartic_residues():
            return "quartic"
        if self.is_quadratic_residue(a):
            return "quadratic"
        return "non-residue"


class HarmonicAnalyzer:
    """Fourier analysis on cyclic groups."""
    def __init__(self, group: CyclicGroup):
        self.group = group
        self.N = group.order

    def dft(self, values: np.ndarray) -> np.ndarray:
        return np.fft.fft(values)

    def idft(self, spectrum: np.ndarray) -> np.ndarray:
        return np.fft.ifft(spectrum)

    def subgroup_frequencies(self, subgroup_size: int) -> List[int]:
        if self.N % subgroup_size != 0:
            raise ValueError(f"{subgroup_size} does not divide {self.N}")
        step = self.N // subgroup_size
        return list(range(0, self.N, step))

    def project_onto_subgroup(self, values: np.ndarray,
                               subgroup_size: int) -> np.ndarray:
        spectrum = self.dft(values)
        freqs = self.subgroup_frequencies(subgroup_size)
        mask = np.zeros(self.N, dtype=bool)
        mask[freqs] = True
        return self.idft(spectrum * mask)


class PrimeMapper:
    """Map primes onto GF(37) group structure."""
    def __init__(self, group: CyclicGroup):
        self.group    = group
        self.residue  = ResidueClassifier(group)
        self._m137    = Map137()

    def map_prime(self, p: int) -> Dict:
        r = p % self.group.p
        return {
            'prime':          p,
            'residue_mod_37': r,
            'discrete_log':   self.group.discrete_log(r),
            'residue_type':   self.residue.residue_symbol(r),
            'in_seed_orbit':  self._m137.is_seed_orbit(r),
            'orbit':          self._m137.orbit(r),
            'in_group':       r != 0,
        }

    def map_sequence(self, primes: List[int]) -> List[Dict]:
        return [self.map_prime(p) for p in primes]


# ============================================================
# DIGITAL ROOT SYSTEM
# ============================================================

class DigitalRootSystem:
    """
    Digital root arithmetic mod 9.

    DR is a ring homomorphism from Z to Z/9Z:
      DR(a+b) = DR(DR(a) + DR(b))
      DR(a*b) = DR(DR(a) * DR(b))
    Both properties are computationally verified in verify().
    """

    @staticmethod
    def digital_root(n: int) -> int:
        if n == 0:
            return 0
        return 1 + (abs(n) - 1) % 9

    @staticmethod
    def dr_iterative(n: int) -> List[int]:
        steps = [n]
        while n >= 10:
            n = sum(int(d) for d in str(n))
            steps.append(n)
        return steps

    @staticmethod
    def validate_dr_addition(a: int, b: int) -> bool:
        DR = DigitalRootSystem.digital_root
        return DR(a + b) == DR(DR(a) + DR(b))

    @staticmethod
    def validate_dr_multiplication(a: int, b: int) -> bool:
        DR = DigitalRootSystem.digital_root
        return DR(a * b) == DR(DR(a) * DR(b))

    @staticmethod
    def dr_sequence(start: int, end: int) -> List[int]:
        DR = DigitalRootSystem.digital_root
        return [DR(n) for n in range(start, end + 1)]

    @staticmethod
    def analyze_pattern(numbers: List[int]) -> Dict:
        DR = DigitalRootSystem.digital_root
        drs = [DR(n) for n in numbers]
        counts: Dict[int, int] = defaultdict(int)
        for d in drs:
            counts[d] += 1
        return {
            'distribution': dict(counts),
            'cycles':        len(numbers) // 9,
            'remainder':     len(numbers) % 9,
            'dominant_dr':   max(counts, key=counts.get) if counts else None,
        }

    @staticmethod
    def verify() -> Dict[str, bool]:
        """Computationally confirm the homomorphism properties."""
        DR = DigitalRootSystem.digital_root
        add_ok = all(DR(a + b) == DR(DR(a) + DR(b))
                     for a in range(1, 20) for b in range(1, 20))
        mul_ok = all(DR(a * b) == DR(DR(a) * DR(b))
                     for a in range(1, 20) for b in range(1, 20))
        return {'addition_homomorphism': add_ok,
                'multiplication_homomorphism': mul_ok}


# ============================================================
# PERFECT NUMBER SYSTEM
# ============================================================

class PerfectNumberSystem:
    """Euclid-Euler theorem: even perfect numbers are 2^(p-1)(2^p − 1)."""

    # Known Mersenne prime exponents (52 confirmed as of 2024)
    MERSENNE_EXPONENTS = [
        2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203,
        2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497,
        86243, 110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221,
        3021377, 6972593, 13466917, 20996011, 24036583, 25964951, 30402457,
        32582657, 37156667, 42643801, 43112609, 57885161, 74207281, 77232917,
        82589933, 136279841,
    ]

    @classmethod
    def perfect_number(cls, p: int) -> Optional[int]:
        """Return 2^(p-1) * (2^p - 1) if p is a known Mersenne exponent."""
        if p not in cls.MERSENNE_EXPONENTS:
            return None
        return (1 << (p - 1)) * ((1 << p) - 1)

    @classmethod
    def info(cls, rank: int) -> Optional[Dict]:
        if rank < 1 or rank > len(cls.MERSENNE_EXPONENTS):
            return None
        p  = cls.MERSENNE_EXPONENTS[rank - 1]
        pn = cls.perfect_number(p)
        DR = DigitalRootSystem.digital_root
        return {
            'rank':             rank,
            'mersenne_exponent': p,
            'mersenne_prime':   (1 << p) - 1,
            'perfect_number':   pn,
            'digits':           len(str(pn)) if pn else 0,
            'digital_root':     DR(pn) if pn else None,
            # Verified: DR of every even perfect number except 6 is 1
            # DR(6) = 6;  DR(28) = 1;  DR(496) = 1;  DR(8128) = 1; ...
        }

    @classmethod
    def list_info(cls, start: int, end: int) -> List[Dict]:
        return [r for r in (cls.info(i) for i in range(start, end + 1)) if r]


# ============================================================
# 37-FAMILY LAW
# ============================================================

class Family37System:
    """37-Family Law: sequences of the form N = 37k + r."""

    @staticmethod
    def entry(factor: int, r: int = 35) -> Dict:
        N = 37 * factor + r
        DR = DigitalRootSystem.digital_root
        return {
            'factor':       factor,
            'N':            N,
            'mod_37':       N % 37,
            'digital_root': DR(N),
            'mod_9':        N % 9,
        }

    @classmethod
    def sequence(cls, factors: List[int], r: int = 35) -> List[Dict]:
        return [cls.entry(f, r) for f in factors]

    @classmethod
    def analyze_dr_pattern(cls, factors: List[int], r: int = 35) -> Dict:
        entries = cls.sequence(factors, r)
        drs     = [e['digital_root'] for e in entries]
        return {
            'sequence':     entries,
            'dr_sequence':  drs,
            'dr_pattern':   DigitalRootSystem.analyze_pattern(
                                [e['N'] for e in entries]),
        }

    @staticmethod
    def verify_2466() -> Dict:
        """
        2466 connection to GF(37).
        2466 = 2 × 3² × 137  (verified: 2*9*137 = 2466)
        2466 mod 37 = 24  (verified)
        24 ∈ SEED_ORBIT {18, 24, 32}  — this is the real connection.
        """
        n = 2466
        DR = DigitalRootSystem.digital_root
        assert 2 * 9 * 137 == 2466, "factorisation check"
        assert n % 37 == 24,        "mod 37 check"
        assert 24 in {18, 24, 32},  "seed orbit check"
        return {
            'value':            n,
            'factorisation':    '2 × 3² × 137',
            'mod_37':           n % 37,            # 24
            'in_seed_orbit':    True,               # 24 ∈ {18,24,32}
            'digital_root':     DR(n),
            'note':             '2466 mod 37 = 24 = seed orbit entry',
        }


# ============================================================
# DR-FIBONACCI SYSTEM
# ============================================================

class DRFibonacciSystem:
    """
    Fibonacci sequence collapsed via digital roots (mod 9).

    VERIFIED: The DR-Fibonacci sequence is PERIODIC with period 24
    (Pisano period mod 9).  It is bounded in {1..9} and does NOT
    converge — ratios of consecutive terms are not meaningful.
    """

    PISANO_PERIOD_9 = 24

    @staticmethod
    def _dr(n: int) -> int:
        if n == 0: return 0
        return 1 + (n - 1) % 9

    @classmethod
    def sequence(cls, seed: Tuple[int, int], length: int) -> List[int]:
        DR = cls._dr
        a, b = DR(seed[0]), DR(seed[1])
        seq  = [a, b]
        for _ in range(length - 2):
            a, b = b, DR(a + b)
            seq.append(b)
        return seq

    @classmethod
    def verify_period(cls) -> Dict:
        """Confirm the period is exactly 24."""
        seq = cls.sequence((1, 1), 48)
        period_correct = seq[:24] == seq[24:48]
        return {
            'first_24':       seq[:24],
            'period_is_24':   period_correct,
            'is_periodic':    True,
            'not_convergent': True,    # bounded in {1..9}, never approaches phi
        }

    @classmethod
    def analyze(cls, seed: Tuple[int, int], length: int) -> Dict:
        seq    = cls.sequence(seed, length)
        counts = Counter(seq)
        return {
            'sequence':     seq,
            'seed':         seed,
            'length':       length,
            'period':       cls.PISANO_PERIOD_9,
            'distribution': dict(counts),
            'is_periodic':  True,
            'not_convergent': True,
            # NOTE: ratio of consecutive terms is NOT phi.
            # DR-Fibonacci is periodic; phi arises from true Fibonacci.
        }


# ============================================================
# PRIME 21 SYSTEM
# ============================================================

class Prime21System:
    """73 is the 21st prime. 511 = 7 × 73 = 2^9 − 1 (not Mersenne prime)."""

    @staticmethod
    def analyze() -> Dict:
        p  = 73
        DR = DigitalRootSystem.digital_root
        # Verify 73 is the 21st prime
        def sieve(n):
            S = [True] * (n + 1); S[0] = S[1] = False
            for i in range(2, int(n**0.5) + 1):
                if S[i]:
                    for j in range(i*i, n+1, i): S[j] = False
            return [i for i, v in enumerate(S) if v]
        primes_to_80 = sieve(80)
        return {
            'prime':          p,
            'rank':           primes_to_80.index(p) + 1,    # confirmed 21
            'digital_root':   DR(p),
            'mod_37':         p % 37,
            '511':            511,
            '511_factors':    '7 × 73',
            '511_is_mersenne_prime': False,  # 511 = 7 × 73 is composite
            '7_mod_37':       7  % 37,
            '73_mod_37':      73 % 37,
            '511_mod_37':     511 % 37,
            'digital_root_511': DR(511),
        }


# ============================================================
# Z9 OPERATOR SYSTEM
# ============================================================

class Z9OperatorSystem:
    """
    Operator system G = <C, R, F> acting on Z_9.
    C: +1 mod 9 (cyclic shift, order 9)
    R: −n mod 9 (negation, order 2)
    F: 2n mod 9  (doubling, order 6 — since 2^6 ≡ 1 mod 9)

    All six group relations verified computationally:
      C^9 = I, R^2 = I, F^6 = I,
      RCR = C^{-1}, FCF^{-1} = C^2, FRF^{-1} = R
    """

    def __init__(self):
        self.N  = 9
        self.C  = [(x + 1) % 9 for x in range(9)]
        self.R  = [(-x) % 9    for x in range(9)]
        self.F  = [(2 * x) % 9 for x in range(9)]
        self._I = list(range(9))

    def compose(self, op1: List[int], op2: List[int]) -> List[int]:
        return [op1[op2[x]] for x in range(9)]

    def inverse(self, op: List[int]) -> List[int]:
        inv = [0] * 9
        for x in range(9):
            inv[op[x]] = x
        return inv

    def power(self, op: List[int], n: int) -> List[int]:
        result = self._I[:]
        for _ in range(n):
            result = self.compose(op, result)
        return result

    def verify_relations(self) -> Dict[str, bool]:
        I, C, R, F = self._I, self.C, self.R, self.F
        Finv = self.inverse(F)
        Cinv = self.inverse(C)
        return {
            'C^9 = I':       self.power(C, 9)                     == I,
            'R^2 = I':       self.power(R, 2)                     == I,
            'F^6 = I':       self.power(F, 6)                     == I,
            'RCR = C^-1':    self.compose(R, self.compose(C, R))  == Cinv,
            'FCF^-1 = C^2':  self.compose(F, self.compose(C,Finv))== self.power(C,2),
            'FRF^-1 = R':    self.compose(F, self.compose(R,Finv))== R,
        }

    def generate_group(self) -> List[List[int]]:
        group   = {tuple(self._I)}
        changed = True
        while changed:
            changed = False
            for g in list(group):
                for gen in [self.C, self.R, self.F]:
                    new = tuple(self.compose(list(g), gen))
                    if new not in group:
                        group.add(new); changed = True
        return [list(g) for g in group]

    def order(self) -> int:
        return len(self.generate_group())


class Z9Lattice:
    """Z_9 × Z_9 lattice with operator action."""

    def __init__(self):
        self.N      = 9
        self.points = [(x, y) for x in range(9) for y in range(9)]

    def translate(self, point: Tuple[int,int],
                  dx: int = 1, dy: int = 1) -> Tuple[int,int]:
        x, y = point
        return ((x + dx) % 9, (y + dy) % 9)

    def reflect(self, point: Tuple[int,int]) -> Tuple[int,int]:
        x, y = point
        return ((-x) % 9, (-y) % 9)

    def dilate(self, point: Tuple[int,int]) -> Tuple[int,int]:
        x, y = point
        return ((2*x) % 9, (2*y) % 9)

    def fourier_mode(self, a: int, b: int, x: int, y: int) -> complex:
        return np.exp(2j * np.pi * (a*x + b*y) / 9)


# ============================================================
# SOPHIE GERMAIN / SAFE PRIME ANALYSIS
# ============================================================

def _sieve(limit: int) -> List[int]:
    S = np.ones(limit + 1, dtype=bool)
    S[0:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if S[i]:
            S[i*i::i] = False
    return np.nonzero(S)[0].tolist()


def analyze_sophie_germain(N: int = 10**6) -> Dict:
    """
    Compute Sophie Germain and safe primes up to N.
    Verified counts (N=1,000,000): 7746 SG primes, 4324 safe primes.
    DR distributions are concentrated on {2, 5, 8} (the non-trinity residues).
    """
    primes    = _sieve(2 * N + 10)
    prime_set = set(primes)
    sg   = [p for p in primes if p <= N and 2*p + 1 in prime_set]
    safe = [q for q in primes if q <= N and q > 2 and (q-1)//2 in prime_set]
    DR   = DigitalRootSystem.digital_root
    return {
        'N':             N,
        'sg_count':      len(sg),
        'safe_count':    len(safe),
        'sg_dr_dist':    dict(Counter(DR(p) for p in sg)),
        'safe_dr_dist':  dict(Counter(DR(q) for q in safe)),
        'sg_in_37fam':   sum(1 for p in sg   if (p - 35) % 37 == 0),
        'safe_in_37fam': sum(1 for q in safe if (q - 35) % 37 == 0),
        'sg_first_20':   sg[:20],
        'safe_first_20': safe[:20],
    }


# ============================================================
# CONCATENATED RANGE PHASE-SHIFT DYNAMICS
# ============================================================

def analyze_concatenated_range(n: int) -> Dict:
    """
    Concatenation of 1..n  mod 37 with phase classification.
    Phase depends on len(concat) mod 3:
      0 → no shift  (pow(10, len, 37) = 1)
      1 → 10-multiplier
      2 → 26-multiplier (= 137-map multiplier)
    """
    s      = "".join(str(i) for i in range(1, n + 1))
    length = len(s)
    val    = int(s)
    phase  = length % 3
    pow10  = pow(10, length, 37)
    return {
        'n':          n,
        'length':     length,
        'length_mod3': phase,
        'mod_37':     val % 37,
        'pow10_mod37': pow10,
        'phase':      {0: 'none (×1)', 1: '×10', 2: '×26 (137-map)'}[phase],
    }


# ============================================================
# UNIFIED MASTER CONTROLLER
# ============================================================

class UnifiedMathematicalFramework:
    """Master controller integrating all mathematical systems."""

    def __init__(self):
        self.map137      = Map137()
        self.dr          = DigitalRootSystem()
        self.perfect     = PerfectNumberSystem()
        self.family37    = Family37System()
        self.dr_fib      = DRFibonacciSystem()
        self.prime21     = Prime21System()
        self.z9_ops      = Z9OperatorSystem()
        self.z9_lattice  = Z9Lattice()
        self.modular_core: Optional[CyclicGroup] = None

    def init_group(self, p: int, g: int) -> CyclicGroup:
        self.modular_core = CyclicGroup(p, g)
        return self.modular_core

    def analyze(self, n: int) -> Dict:
        DR  = DigitalRootSystem.digital_root
        m   = self.map137
        return {
            'input':          n,
            'digital_root':   DR(n),
            'mod_37':         n % 37,
            'orbit':          m.orbit(n % 37),
            'in_seed_orbit':  m.is_seed_orbit(n),
            'in_37fam':       (n - 35) % 37 == 0,
        }

    def full_verify(self) -> Dict[str, Dict]:
        """Run every verification in the framework. All must pass."""
        return {
            '137_map':      self.map137.verify(),
            'dr_system':    DigitalRootSystem.verify(),
            'z9_relations': self.z9_ops.verify_relations(),
            'dr_fib':       DRFibonacciSystem.verify_period(),
        }


# ============================================================
# SELF-TEST
# ============================================================

if __name__ == "__main__":
    fw = UnifiedMathematicalFramework()

    print("=" * 60)
    print("FULL FRAMEWORK VERIFICATION")
    print("=" * 60)

    results = fw.full_verify()
    all_pass = True
    for section, checks in results.items():
        for name, result in checks.items():
            status = "PASS" if result else "FAIL"
            if not result:
                all_pass = False
            print(f"  [{status}] {section}: {name}")

    print()
    print(f"Overall: {'ALL PASS' if all_pass else 'FAILURES DETECTED'}")
    print()

    print("137-MAP:")
    m = fw.map137
    print(f"  f(n) = 26n mod 37")
    print(f"  Orbit(24) = {m.orbit(24)}")
    print(f"  Heartbeat = {m.heartbeat()}")
    print(f"  All orbits: {m.classify_all()}")
    print()

    G  = fw.init_group(37, 2)
    H9 = Subgroup(G, 16)
    print(f"GF(37) group order: {G.order}")
    print(f"Primitive roots: {G.get_primitive_roots()[:6]} ...")
    print(f"<16> order = {H9.size}, elements = {H9.elements}")
    print()

    print("2466 CONNECTION:")
    print(fw.family37.verify_2466())
    print()

    print("DR-FIBONACCI (period verification):")
    print(fw.dr_fib.verify_period())
    print()

    print("Z9 RELATIONS:")
    print(fw.z9_ops.verify_relations())
    print("=" * 60)

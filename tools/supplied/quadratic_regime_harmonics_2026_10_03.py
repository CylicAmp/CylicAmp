# Supplied code, 2026-10-03, verbatim. Audited in
# math/theorems/split_regime_spectrum_supplied_audit_2026_10_03.py.
from enum import Enum
from typing import Union

class Regime(Enum):
    SPLIT = "Hyperbolic"
    ANISOTROPIC = "Elliptic"
    DEGENERATE = "Degenerate"

class HarmonicAnalysis:
    """Base protocol for harmonic analysis across regimes."""
    def fourier_spectrum(self) -> list: pass
    def circulant_graph_adjacency(self, connection_set: set): pass
    def graph_eigenvalues(self, connection_set: set): pass

class SplitHarmonicAnalysis(HarmonicAnalysis):
    """
    Harmonic analysis for the split regime over C_{p-1}.
    """
    def __init__(self, p: int):
        self.p = p
        self.order = p - 1
        self.sequence = self._build_character_sequence()

    def _build_character_sequence(self) -> list:
        # Sequence of Legendre symbols for g^j in F_p^*
        # We can just use the standard Legendre symbol on 1..p-1 ordered by a generator
        g = self._find_generator()
        seq = []
        val = 1
        for _ in range(self.order):
            chi = 0 if val == 0 else (1 if pow(val, (self.p - 1) // 2, self.p) == 1 else -1)
            seq.append(chi)
            val = (val * g) % self.p
        return seq

    def _find_generator(self) -> int:
        for g in range(2, self.p):
            if pow(g, (self.p - 1) // 2, self.p) != 1:
                # Probabilistic check for full generator
                is_gen = True
                temp = self.p - 1
                q = 2
                while q * q <= temp:
                    if temp % q == 0:
                        if pow(g, (self.p - 1) // q, self.p) == 1:
                            is_gen = False
                            break
                        while temp % q == 0: temp //= q
                    q += 1
                if temp > 1 and pow(g, (self.p - 1) // temp, self.p) == 1:
                    is_gen = False
                if is_gen:
                    return g
        raise ValueError("No generator found")

    def fourier_spectrum(self) -> list:
        import cmath
        N = self.order
        spectrum = []
        for k in range(N):
            c_k = sum(self.sequence[j] * cmath.exp(-2j * cmath.pi * j * k / N) 
                      for j in range(N))
            spectrum.append(round(abs(c_k))) # Return magnitudes
        return spectrum

class UnifiedQuadraticForm:
    """
    Factory and unified interface for binary quadratic forms over F_p.
    """
    def __init__(self, A: int, B: int, C: int, p: int):
        self.p = p
        self.A, self.B, self.C = A % p, B % p, C % p
        self.delta = (self.B**2 - 4 * self.A * self.C) % p
        
        self.regime = self._detect_regime()
        self._init_geometry()

    def _detect_regime(self) -> Regime:
        if self.delta == 0:
            return Regime.DEGENERATE
        chi = pow(self.delta, (self.p - 1) // 2, self.p)
        return Regime.SPLIT if chi == 1 else Regime.ANISOTROPIC

    def _init_geometry(self):
        if self.regime == Regime.SPLIT:
            self.geometry = SplitQuadraticForm(self.A, self.B, self.C, self.p)
            self.harmonics = SplitHarmonicAnalysis(self.p)
        elif self.regime == Regime.ANISOTROPIC:
            self.geometry = AnisotropicQuadraticForm(self.A, self.B, self.C, self.p)
            self.harmonics = TorusHarmonicAnalysis(self.geometry)
        else:
            self.geometry = DegenerateQuadraticForm(self.A, self.B, self.C, self.p)
            self.harmonics = None # Degenerate case lacks the cyclic torus structure

    def get_partition(self) -> dict:
        return self.geometry.get_partition_counts()

    def get_stabilizer(self) -> dict:
        return self.geometry.get_stabilizer_structure()
        
    def get_spectrum_magnitudes(self) -> list:
        if self.harmonics is None:
            raise NotImplementedError("Harmonic analysis is undefined for the degenerate regime.")
        return self.harmonics.fourier_spectrum()

# Placeholder classes to ensure the factory runs without the previous blocks being re-pasted
class SplitQuadraticForm:
    def __init__(self, A, B, C, p): pass
    def get_partition_counts(self): return {"null": 2, "square": (self.p-1)//2, "nonsquare": (self.p-1)//2}
    def get_stabilizer_structure(self): return {"group": "D_{p-1}", "order": 2*(self.p-1)}

class DegenerateQuadraticForm:
    def __init__(self, A, B, C, p): pass
    def get_partition_counts(self): return {"null": 1, "square": self.p, "nonsquare": 0}
    def get_stabilizer_structure(self): return {"group": "Borel", "order": self.p*(self.p-1)}

# Note: AnisotropicQuadraticForm and TorusHarmonicAnalysis are defined in the previous block.

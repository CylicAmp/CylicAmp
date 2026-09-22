"""
monomial_universe.py

Epistemic verification scaffold for divisor-closed families of monomials.

A "universe" F_k is the set of all order ideals (downsets under the
divisibility/product order) of size k in N^n, where the n variables are
LABELED by the primes (2, q, r, s, t, ...). No quotient by variable
permutation is taken: the primes are distinguishable objects.

Mathematical facts used
-----------------------
1. Every order ideal contains the minimal element 1 = (0,...,0).
2. F u {m} is an order ideal iff every IMMEDIATE divisor of m
   (decrement one positive coordinate) already lies in F.
   (Immediate-divisor closure implies full divisor closure by induction
   along any maximal chain from m down to 1.)
3. If |F| = k and m in F, then deg(m) <= k-1: a maximal chain
   1 = m_0 < m_1 < ... < m_d = m inside F has d+1 <= k distinct
   elements and each strict step raises degree by >= 1.
   Consequently degree bound k-1 suffices for a COMPLETE universe
   of size k; a smaller user-supplied bound defines a truncated
   (incomplete) universe and is rejected.
"""

from dataclasses import dataclass
from typing import Tuple, Optional, Dict, List, Set, FrozenSet, Iterable, Iterator
from enum import Enum
import itertools

# =====================================================================
# EPISTEMIC STATUS & PROOF STRATEGIES
# =====================================================================

class BranchStatus(Enum):
    PROVED_IMPOSSIBLE = "PROVED_IMPOSSIBLE"
    PROVED_WITNESS = "PROVED_WITNESS"
    OPEN = "OPEN"
    INVALID_CERTIFICATE = "INVALID_CERTIFICATE"

class ProofStrategy(Enum):
    MODULAR_PARITY = "MODULAR_PARITY"
    DISCRIMINANT_NON_RESIDUE = "DISCRIMINANT_NON_RESIDUE"
    PREFIX_BOUND_CONTRADICTION = "PREFIX_BOUND_CONTRADICTION"
    POLYNOMIAL_NEGATIVITY = "POLYNOMIAL_NEGATIVITY"
    SINGLE_PRIME_POWER = "SINGLE_PRIME_POWER"
    SANDWICH_BOUND = "SANDWICH_BOUND"
    MOD_R2_CONTENT = "MOD_R2_CONTENT"
    COFACTOR_SIZE = "COFACTOR_SIZE"
    MARKOV_HURWITZ = "MARKOV_HURWITZ"
    MOD3_CONTENT = "MOD3_CONTENT"
    OPEN = "OPEN"

# =====================================================================
# 1. MONOMIAL LATTICE
# =====================================================================

@dataclass(frozen=True, order=True)
class Monomial:
    """Canonical exponent vector over prime variables: (2, q, r, s, t, ...)."""
    exponents: Tuple[int, ...]

    def __post_init__(self):
        if any(e < 0 for e in self.exponents):
            raise ValueError("Monomial exponent vector must be strictly non-negative.")

    def divides(self, other: "Monomial") -> bool:
        if len(self.exponents) != len(other.exponents):
            raise ValueError("Monomials must share canonical basis dimension.")
        return all(a <= b for a, b in zip(self.exponents, other.exponents))

    def is_one(self) -> bool:
        return all(e == 0 for e in self.exponents)

    def degree(self) -> int:
        return sum(self.exponents)

    def __str__(self) -> str:
        return f"Monomial({self.exponents})"

@dataclass(frozen=True)
class MonomialShape:
    """Represents a divisor prefix shape with full structural verification."""
    monomials: Tuple[Monomial, ...]
    parity: str  # "EVEN" or "ODD"
    k: int

    def canonical(self) -> bool:
        return (
            len(self.monomials) == self.k
            and len(set(self.monomials)) == self.k
            and self.monomials == tuple(sorted(self.monomials))
            and self.monomials[0].is_one()
        )

    def is_order_ideal(self) -> bool:
        """Full divisor-closure verification, not merely immediate-closure."""
        if not self.canonical():
            return False

        F = set(self.monomials)
        for m in F:
            for i, e in enumerate(m.exponents):
                if e > 0:
                    pred = list(m.exponents)
                    pred[i] -= 1
                    if Monomial(tuple(pred)) not in F:
                        return False
        return True

    def __str__(self) -> str:
        return f"Shape({self.parity}, {self.k})"

# =====================================================================
# 2. UNIVERSE GENERATOR
# =====================================================================

class UniverseGenerator:
    """Generates the complete F_k universe through order-ideal closure.

    Parameters
    ----------
    max_variables : int
        Number n of labeled prime variables. All monomials are padded to
        dimension n, so 1 = (0,...,0) is the unique minimal element.
    max_degree : Optional[int]
        External degree cap. If None, an internally sufficient bound
        (k-1 at generation time) is used, guaranteeing completeness.
        If set below k-1 for a requested k, generation raises
        ValueError, because the resulting universe would be incomplete.
    """

    def __init__(self, max_variables: int = 3, max_degree: Optional[int] = None):
        if max_variables < 1:
            raise ValueError("max_variables must be >= 1.")
        if max_degree is not None and max_degree < 1:
            raise ValueError("max_degree must be >= 1 when provided.")
        self.max_variables = max_variables
        self.max_degree = max_degree
        self._cache: Dict[Tuple[int, str], List[MonomialShape]] = {}

    # ------------------------------------------------------------------
    # Basic lattice operations
    # ------------------------------------------------------------------

    def one(self) -> Monomial:
        """The multiplicative identity 1 = (0,...,0) in dimension n."""
        return Monomial((0,) * self.max_variables)

    def monomial(self, exponents: Tuple[int, ...]) -> Monomial:
        """Canonical padded monomial in the ambient dimension."""
        if len(exponents) > self.max_variables:
            raise ValueError(
                f"Exponent vector {exponents} exceeds ambient dimension "
                f"{self.max_variables}."
            )
        return Monomial(tuple(exponents) + (0,) * (self.max_variables - len(exponents)))

    def immediate_divisors(self, m: Monomial) -> List[Monomial]:
        """Elements covered by m in the product order (coatomic predecessors)."""
        out = []
        for i, e in enumerate(m.exponents):
            if e > 0:
                pred = list(m.exponents)
                pred[i] -= 1
                out.append(Monomial(tuple(pred)))
        return out

    def divisors_of(self, m: Monomial) -> FrozenSet[Monomial]:
        """Full divisor set of m, including 1 and m itself."""
        m = self.monomial(m.exponents)
        ranges = [range(e + 1) for e in m.exponents]
        return frozenset(Monomial(t) for t in itertools.product(*ranges))

    def divisor_closure(self, generators: Iterable[Monomial]) -> FrozenSet[Monomial]:
        """Order ideal generated by the given monomials (their divisor hull)."""
        F: Set[Monomial] = set()
        for g in generators:
            F.update(self.divisors_of(g))
        return frozenset(F)

    def candidates(self, degree_bound: int) -> List[Monomial]:
        """All monomials 1 != m with deg(m) <= degree_bound, in canonical order.

        Weak compositions of d into n parts are enumerated via
        combinations_with_replacement; total count is C(n+d-1, d) per degree.
        """
        if degree_bound < 0:
            return []
        n = self.max_variables
        out: List[Monomial] = []
        for total in range(1, degree_bound + 1):
            for cuts in itertools.combinations_with_replacement(range(n), total):
                exps = [0] * n
                for c in cuts:
                    exps[c] += 1
                out.append(Monomial(tuple(exps)))
        return out

    # ------------------------------------------------------------------
    # Independent structural verification
    # ------------------------------------------------------------------

    def is_order_ideal(self, F: FrozenSet[Monomial]) -> bool:
        """Verifier: down-closure under ALL divisors, checked via cover relation.

        Since every divisor of m is reachable from m by a finite chain of
        immediate-divisor steps, closure under immediate divisors is
        equivalent to closure under arbitrary divisors.
        """
        Fset = set(F)
        if self.one() not in Fset:
            return False
        for m in Fset:
            if len(m.exponents) != self.max_variables:
                return False
            for p in self.immediate_divisors(m):
                if p not in Fset:
                    return False
        return True

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def minimal_extensions(self, F: FrozenSet[Monomial],
                           degree_bound: int) -> Iterator[Monomial]:
        """Yield m not in F with F u {m} an order ideal (m a minimal new element).

        By fact (2) above, it suffices that every immediate divisor of m
        already lies in F.
        """
        Fset = set(F)
        for m in self.candidates(degree_bound):
            if m in Fset:
                continue
            if all(p in Fset for p in self.immediate_divisors(m)):
                yield m

    def generate(self, k: int, parity: Optional[str] = None) -> List[MonomialShape]:
        """Enumerate the complete F_k universe as canonical MonomialShapes.

        Growth is by levels: F_{s+1} is obtained from each F in F_s by
        adjoining one minimal extension. By fact (3), elements of an
        ideal of size s+1 have degree <= s, so degree_bound = s is
        internally sufficient when no external cap is set.

        parity records the branch-parity tag for downstream strategies
        (default: "EVEN" iff k is even; pass explicitly if your branch
        semantics assign parity differently). It is part of the cache key,
        so the same k under two parity tags yields two tagged families.
        """
        if k < 1:
            raise ValueError("k must be >= 1.")
        if parity is None:
            parity = "EVEN" if k % 2 == 0 else "ODD"
        if parity not in ("EVEN", "ODD"):
            raise ValueError('parity must be "EVEN" or "ODD".')
        if self.max_degree is not None and self.max_degree < k - 1:
            raise ValueError(
                f"max_degree={self.max_degree} < k-1={k-1}: the generated "
                f"universe would be incomplete (fact (3) in the module docstring)."
            )
        key = (k, parity)
        if key in self._cache:
            return self._cache[key]

        level: Set[FrozenSet[Monomial]] = {frozenset({self.one()})}
        for size in range(1, k):
            # elements entering an ideal of final size `size+1` need deg <= size
            if self.max_degree is None:
                bound = size
            else:
                bound = min(self.max_degree, size)
            nxt: Set[FrozenSet[Monomial]] = set()
            for F in level:
                for m in self.minimal_extensions(F, bound):
                    nxt.add(frozenset(set(F) | {m}))
            level = nxt
            if not level:
                break

        shapes = [MonomialShape(tuple(sorted(F)), parity, k) for F in level]

        # Dogfood: every emitted shape must pass its own structural verifier.
        for s in shapes:
            assert s.canonical(), f"non-canonical shape emitted: {s}"
            assert s.is_order_ideal(), f"non-ideal emitted: {s}"

        self._cache[key] = shapes
        return shapes

# =====================================================================
# 3. SELF-TESTS (run with: python monomial_universe.py)
# =====================================================================

def _brute_force_count(n: int, k: int) -> int:
    """Independent enumeration for validation: all k-subsets of the
    degree-(k-1) candidate ball containing 1, filtered by the verifier."""
    gen = UniverseGenerator(max_variables=n)
    cands = [gen.one()] + gen.candidates(k - 1)
    count = 0
    for combo in itertools.combinations(cands, k):
        if gen.is_order_ideal(frozenset(combo)):
            count += 1
    return count

def _partition_number(k: int) -> int:
    """p(k) via Euler's pentagonal recurrence, for the n=2 correspondence."""
    p = [0] * (k + 1)
    p[0] = 1
    for n in range(1, k + 1):
        total, i, sign = 0, 1, 1
        while True:
            g1 = i * (3 * i - 1) // 2
            g2 = i * (3 * i + 1) // 2
            if g1 > n and g2 > n:
                break
            if g1 <= n:
                total += sign * p[n - g1]
            if g2 <= n:
                total += sign * p[n - g2]
            i += 1
            sign = -sign
        p[n] = total
    return p[k]

def self_test() -> None:
    # (a) n = 1: exactly one ideal per k, the initial segment {1,...,x^{k-1}}.
    gen1 = UniverseGenerator(max_variables=1)
    for k in range(1, 8):
        shapes = gen1.generate(k)
        assert len(shapes) == 1, (k, len(shapes))
        assert shapes[0].is_order_ideal()
    print("[ok] n=1: unique chain ideal for each k")

    # (b) n = 2: labeled order ideals of size k are in bijection with
    #     partitions of k (anchored Ferrers diagrams; variables labeled,
    #     so a shape and its transpose are distinct when the partitions
    #     differ). Check against p(k) and against brute force.
    gen2 = UniverseGenerator(max_variables=2)
    for k in range(1, 7):
        got = len(gen2.generate(k))
        assert got == _partition_number(k), (k, got, _partition_number(k))
        assert got == _brute_force_count(2, k), (k, got, _brute_force_count(2, k))
    print("[ok] n=2: counts match partition numbers p(k) and brute force")

    # (c) n = 3: spot-check small k against brute force.
    gen3 = UniverseGenerator(max_variables=3)
    for k in range(1, 5):
        got = len(gen3.generate(k))
        assert got == _brute_force_count(3, k), (k, got, _brute_force_count(3, k))
    print("[ok] n=3: k<=4 matches brute force")

    # (d) truncation guard: max_degree < k-1 must raise.
    try:
        UniverseGenerator(max_variables=2, max_degree=2).generate(5)
    except ValueError:
        print("[ok] truncation guard raises for max_degree < k-1")
    else:
        raise AssertionError("truncation guard failed to raise")

    # (e) negative exponents rejected; padded canonical access.
    try:
        Monomial((1, -1))
    except ValueError:
        pass
    else:
        raise AssertionError("negative exponent accepted")
    gen = UniverseGenerator(max_variables=3)
    assert gen.monomial((2, 1)).exponents == (2, 1, 0)
    print("[ok] input validation and canonical padding")

    # (f) parity is part of the cache key: the same k under two tags
    #     yields two distinct tagged families over the same ideals.
    gen2b = UniverseGenerator(max_variables=2)
    even = gen2b.generate(4, "EVEN")
    odd = gen2b.generate(4, "ODD")
    assert all(s.parity == "EVEN" for s in even)
    assert all(s.parity == "ODD" for s in odd)
    assert {s.monomials for s in even} == {s.monomials for s in odd}
    print("[ok] parity tag does not collide in the cache")

    print("\nAll self-tests passed.")

if __name__ == "__main__":
    self_test()

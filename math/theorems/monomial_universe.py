"""
monomial_universe.py

Epistemic verification scaffold for divisor-closed families of monomials.

A "universe" F_k is the set of all order ideals (downsets under the
divisibility/product order) of size k in N^n, where the n variables are
LABELED by the primes (2, q, r, s, t, ...). No quotient by variable
permutation is taken: the primes are distinguishable objects.

--------------------------------------------------------------------
PROPOSITION 1 (structural characterization of order ideals)
--------------------------------------------------------------------
Let P = (N^n, <=) be the multi-index poset under the componentwise
product order, and for v in N^n let

    cov(v) = { v - e_i : i in 1..n, v_i > 0 }

be its set of lower covers. For ANY subset F of N^n:

    F is an order ideal  <=>  for all v in F, cov(v) is a subset of F.

(=>) is immediate. (<=) by induction on deg(v): if w | v and w != v,
some maximal chain v = u_0 > u_1 > ... > u_d = w has u_{j+1} in
cov(u_j), so w in F by descent.

This condition is LOCAL and CARDINALITY-FREE: it reads only the cover
relations of the graded poset and never the size of F. In particular
F = {} satisfies it vacuously and is an order ideal. The code honors
this: is_order_ideal() nowhere inspects |F|, and the k-indexed universe
is a separate notion layered on top.

--------------------------------------------------------------------
PROPOSITION 2 (cardinality-induced search truncation bound)
--------------------------------------------------------------------
Let F be an order ideal with |F| = k finite. Then every v in F has

    deg(v) <= k - 1,      deg(v) = v_1 + ... + v_n.

Proof: a maximal chain 1 = m_0 < m_1 < ... < m_d = v inside F (which
lies in F by Prop 1) has d+1 <= k distinct elements, and each strict
step raises degree by exactly 1, so deg(v) = d <= k-1.

Role in the algorithm: this truncates the infinite poset N^n to the
finite candidate subgrid

    G_{n,k} = { v in N^n : deg(v) <= k-1 },   |G_{n,k}| = C(n+k-1, n),

guaranteeing that exhaustive search over G_{n,k} omits no downset of
size k. This is a SEARCH BOUND, not a membership criterion: it never
appears in is_order_ideal(). A user-supplied max_degree below k-1
would truncate G_{n,k} itself and is rejected rather than silently
yielding a partial enumeration.

--------------------------------------------------------------------
CANONICALIZATION: PROJECTION INVARIANTS
--------------------------------------------------------------------
canonicalize() is the normal-form projection; canonical() is the
predicate recognizing its fixed points, i.e.

    canonical(S)  <=>  canonicalize(S) == S.

The projection satisfies, and the suite verifies:

  (i)   Idempotence:          C(C(F)) = C(F).
  (ii)  Support preservation: supp(C(F)) = pad(supp(F)), |C(F)| = |F|,
        where pad is the canonical embedding N^m -> N^n (m <= n) by
        zero-extension. C only reorders and re-represents; it never
        adds, drops, or moves a coordinate point.
  (iii) Ideal invariance:     is_order_ideal(C(F)) <=> is_order_ideal(F).
        The sharp form of "no shape distortion": normalization can
        neither create nor destroy the downset property.

--------------------------------------------------------------------
GENERATOR CORRECTNESS TRIAD
--------------------------------------------------------------------
Emit(n, k) must satisfy three properties:

  SOUNDNESS     every emitted F is an order ideal with |F| = k.
  COMPLETENESS  every order ideal of size k in N^n is emitted.
  UNIQUENESS    no order ideal is emitted twice.

Soundness is checked per-object at emission (every shape is asserted
against the independent verifier before release).

Completeness and uniqueness are structural, and rest on a canonical
parent rule rather than on deduplication. Fix any total order < on
N^n (here: degree, then lexicographic). For an order ideal F with
|F| >= 2 define

    parent(F) = F \ { the <-greatest MAXIMAL element of F }.

  - parent(F) is an order ideal of size |F|-1: deleting a maximal
    element of a downset cannot break Prop 1, since a maximal element
    lies in no other element's cover set.
  - COMPLETENESS (induction on k): for an ideal F with |F| = k >= 2,
    let m* be its <-greatest maximal element. Then parent(F) is an
    ideal of size k-1, and cov(m*) is a subset of parent(F) because
    cov(m*) is a subset of F by Prop 1 and m* is not in cov(m*). So m*
    is a legal minimal extension of parent(F), and F is reached from
    it. The base case k=1 is {1}, the unique ideal of size 1.
  - UNIQUENESS: parent is a well-defined single-valued function on
    ideals of size >= 2, so the reachability graph rooted at {1} is a
    TREE, not a DAG -- each ideal has exactly one ancestral path. The
    generator accepts a child F u {m} from F only when
    parent(F u {m}) == F, so each ideal is emitted along that one path
    and no other. Uniqueness is therefore a proved property of the
    search, not an artifact of a set-valued accumulator; the code
    accumulates into a LIST so the suite can actually falsify it.

EPISTEMIC STATUS. Prop 1, Prop 2, and the completeness/uniqueness
arguments above are Level 1 (proved, arguments recorded here). The
benchmark cardinality matches are Level 2 (empirical, finite slices):
they confirm the implementation on the stated ranges only, and no
finite slice extends to arbitrary n and k. Ranges are recorded at each
check in self_test().
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

    def covers(self) -> List["Monomial"]:
        """cov(v): the lower covers of this monomial in the product order."""
        out = []
        for i, e in enumerate(self.exponents):
            if e > 0:
                pred = list(self.exponents)
                pred[i] -= 1
                out.append(Monomial(tuple(pred)))
        return out

    def __str__(self) -> str:
        return f"Monomial({self.exponents})"

@dataclass(frozen=True)
class MonomialShape:
    """A k-element family in normal form, carrying a branch-parity tag.

    canonical() and is_order_ideal() are deliberately INDEPENDENT:
    the first is a statement about representation and cardinality,
    the second is the cardinality-free condition of Prop 1. Use
    is_valid() when both are wanted.
    """
    monomials: Tuple[Monomial, ...]
    parity: str  # "EVEN" or "ODD"
    k: int

    def canonical(self) -> bool:
        """Normal-form predicate: fixed points of canonicalize().

        Distinct, sorted, of declared length k, all of one dimension.
        Says nothing about divisor closure.
        """
        if len(self.monomials) != self.k:
            return False
        if len(set(self.monomials)) != self.k:
            return False
        if self.monomials != tuple(sorted(self.monomials)):
            return False
        dims = {len(m.exponents) for m in self.monomials}
        return len(dims) <= 1

    def is_order_ideal(self) -> bool:
        """Prop 1 verdict on the underlying set. Cardinality-free.

        Does NOT consult canonical(): an unsorted or mis-declared family
        is still either a downset or not, and the two questions are kept
        apart. Also does not require 1 in F -- Prop 1 already forces it
        for nonempty F, and {} is vacuously an ideal.
        """
        F = set(self.monomials)
        return all(c in F for m in F for c in m.covers())

    def is_valid(self) -> bool:
        """Emission criterion: correct normal form AND a genuine downset."""
        return self.canonical() and self.is_order_ideal()

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
        External cap on the Prop 2 search grid G_{n,k}. If None, the
        sufficient bound k-1 is used and the universe is complete. If
        set below k-1 for a requested k, generation raises ValueError:
        the grid itself would be truncated.
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
        """Canonical padded monomial: the embedding pad: N^m -> N^n."""
        if len(exponents) > self.max_variables:
            raise ValueError(
                f"Exponent vector {exponents} exceeds ambient dimension "
                f"{self.max_variables}."
            )
        return Monomial(tuple(exponents) + (0,) * (self.max_variables - len(exponents)))

    def immediate_divisors(self, m: Monomial) -> List[Monomial]:
        """cov(m): elements covered by m in the product order."""
        return m.covers()

    def immediate_multiples(self, m: Monomial) -> List[Monomial]:
        """The upper covers of m: m * x_i for each variable i."""
        out = []
        for i in range(len(m.exponents)):
            succ = list(m.exponents)
            succ[i] += 1
            out.append(Monomial(tuple(succ)))
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
        """G_{n,d} minus {1}: all 1 != m with deg(m) <= d, canonically ordered.

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
    # Independent structural verification (Prop 1)
    # ------------------------------------------------------------------

    def is_order_ideal(self, F: FrozenSet[Monomial]) -> bool:
        """Prop 1 verifier: cov-closure, read purely off the cover relation.

        Since every divisor of m is reachable from m by a finite chain of
        cover steps, closure under cov is equivalent to closure under
        arbitrary divisors. No cardinality is consulted, and 1 in F is
        not imposed: Prop 1 already implies it for nonempty F, and the
        empty set is vacuously an order ideal.
        """
        Fset = set(F)
        for m in Fset:
            if len(m.exponents) != self.max_variables:
                return False
            for p in m.covers():
                if p not in Fset:
                    return False
        return True

    # ------------------------------------------------------------------
    # Canonicalization: the normal-form projection
    # ------------------------------------------------------------------

    def canonicalize(self, F: Iterable[Monomial], parity: str = "EVEN",
                     k: Optional[int] = None) -> MonomialShape:
        """Normal-form projection C. Reorders and pads; never distorts shape.

        Satisfies C(C(F)) = C(F) and supp(C(F)) = pad(supp(F)). Raises on
        a multiset input, since collapsing duplicates would silently
        change |F| and violate support preservation.
        """
        padded = [self.monomial(m.exponents) for m in F]
        if len(set(padded)) != len(padded):
            raise ValueError("canonicalize() requires distinct monomials.")
        ordered = tuple(sorted(padded))
        return MonomialShape(ordered, parity, len(ordered) if k is None else k)

    # ------------------------------------------------------------------
    # Canonical parent rule (uniqueness of the spanning path)
    # ------------------------------------------------------------------

    @staticmethod
    def _rank(m: Monomial) -> Tuple[int, Tuple[int, ...]]:
        """The fixed total order < on N^n: by degree, then lexicographic."""
        return (m.degree(), m.exponents)

    def maximal_elements(self, F: FrozenSet[Monomial]) -> List[Monomial]:
        """Elements of F with no upper cover in F."""
        Fset = set(F)
        return [m for m in Fset
                if not any(s in Fset for s in self.immediate_multiples(m))]

    def canonical_parent(self, F: FrozenSet[Monomial]) -> Optional[FrozenSet[Monomial]]:
        """parent(F) = F minus its <-greatest maximal element.

        Single-valued on ideals of size >= 2, which is what makes the
        reachability graph a tree. Returns None for |F| <= 1.
        """
        if len(F) <= 1:
            return None
        greatest = max(self.maximal_elements(F), key=self._rank)
        return frozenset(set(F) - {greatest})

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def minimal_extensions(self, F: FrozenSet[Monomial],
                           degree_bound: int) -> Iterator[Monomial]:
        """Yield m not in F with F u {m} an order ideal.

        By Prop 1 it suffices that cov(m) is already a subset of F. The
        degree_bound argument supplies the Prop 2 truncation; the two
        roles stay separate here, the local test and the search bound.
        """
        Fset = set(F)
        for m in self.candidates(degree_bound):
            if m in Fset:
                continue
            if all(p in Fset for p in m.covers()):
                yield m

    def generate(self, k: int, parity: Optional[str] = None) -> List[MonomialShape]:
        """Enumerate the complete F_k universe as canonical MonomialShapes.

        Level-by-level growth along the canonical-parent tree: from each
        ideal F of size s, a minimal extension m is accepted only when
        parent(F u {m}) == F, so every ideal is built along exactly one
        path. Results accumulate in a LIST, never a set, so that a
        duplicate would survive to be caught by the uniqueness test
        rather than being silently absorbed.

        By Prop 2, elements of an ideal of size s+1 have degree <= s, so
        degree_bound = s is sufficient when no external cap is set.

        parity records the branch-parity tag for downstream strategies
        (default: "EVEN" iff k is even). It is part of the cache key, so
        the same k under two parity tags yields two tagged families.
        """
        if k < 1:
            raise ValueError("k must be >= 1.")
        if parity is None:
            parity = "EVEN" if k % 2 == 0 else "ODD"
        if parity not in ("EVEN", "ODD"):
            raise ValueError('parity must be "EVEN" or "ODD".')
        if self.max_degree is not None and self.max_degree < k - 1:
            raise ValueError(
                f"max_degree={self.max_degree} < k-1={k-1}: the Prop 2 search "
                f"grid G_(n,k) would be truncated and the universe incomplete."
            )
        key = (k, parity)
        if key in self._cache:
            return self._cache[key]

        level: List[FrozenSet[Monomial]] = [frozenset({self.one()})]
        for size in range(1, k):
            # elements entering an ideal of final size size+1 need deg <= size
            bound = size if self.max_degree is None else min(self.max_degree, size)
            nxt: List[FrozenSet[Monomial]] = []
            for F in level:
                for m in self.minimal_extensions(F, bound):
                    child = frozenset(set(F) | {m})
                    if self.canonical_parent(child) == F:
                        nxt.append(child)
            level = nxt
            if not level:
                break

        shapes = [self.canonicalize(F, parity, k) for F in level]

        # Dogfood (soundness, per object): nothing is released that does
        # not pass the independent verifier it claims to satisfy.
        for s in shapes:
            assert s.is_valid(), f"unsound emission: {s} {s.monomials}"

        self._cache[key] = shapes
        return shapes

# =====================================================================
# 3. SELF-TESTS (run with: python monomial_universe.py)
# =====================================================================

def _brute_force_ideals(n: int, k: int) -> Set[Tuple[Monomial, ...]]:
    """Independent oracle: every k-subset of the Prop 2 grid G_{n,k},
    filtered by the Prop 1 verifier. Returns the ideals themselves, so
    completeness can be tested by set equality rather than by counting."""
    gen = UniverseGenerator(max_variables=n)
    grid = [gen.one()] + gen.candidates(k - 1)
    return {tuple(sorted(c)) for c in itertools.combinations(grid, k)
            if gen.is_order_ideal(frozenset(c))}

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

# ---------------------------------------------------------------------
# 3a. Proposition 1: locality and cardinality-independence
# ---------------------------------------------------------------------

def test_proposition_1() -> None:
    gen = UniverseGenerator(max_variables=2)
    M = gen.monomial

    # cov-closure decides membership with no reference to |F|.
    assert gen.is_order_ideal(frozenset())                      # vacuous
    assert gen.is_order_ideal(frozenset({M((0, 0))}))
    assert not gen.is_order_ideal(frozenset({M((1, 0))}))       # missing 1
    assert not gen.is_order_ideal(frozenset({M((0, 0)), M((2, 0))}))
    assert gen.is_order_ideal(frozenset({M((0, 0)), M((1, 0)), M((2, 0))}))

    # Same underlying set, three declared cardinalities: the Prop 1
    # verdict is invariant, only the normal-form predicate moves.
    body = (M((0, 0)), M((1, 0)))
    for declared in (1, 2, 3):
        shape = MonomialShape(body, "EVEN", declared)
        assert shape.is_order_ideal(), "Prop 1 verdict moved with |F|"
    assert MonomialShape(body, "EVEN", 2).canonical()
    assert not MonomialShape(body, "EVEN", 3).canonical()

    # An unsorted family is still a downset: the two tests are decoupled.
    unsorted = MonomialShape((M((1, 0)), M((0, 0))), "EVEN", 2)
    assert unsorted.is_order_ideal()
    assert not unsorted.canonical()
    assert not unsorted.is_valid()
    print("[ok] Prop 1: cov-closure is local, cardinality-free, order-free")

# ---------------------------------------------------------------------
# 3b. Proposition 2: the truncation bound is a search bound only
# ---------------------------------------------------------------------

def test_proposition_2() -> None:
    for n in (1, 2, 3):
        gen = UniverseGenerator(max_variables=n)
        for k in range(1, 7):
            # grid size |G_{n,k}| = C(n+k-1, n)
            grid = [gen.one()] + gen.candidates(k - 1)
            expected = 1
            for j in range(n):
                expected = expected * (k - 1 + j + 1) // (j + 1)
            assert len(grid) == expected, (n, k, len(grid), expected)
            # every emitted ideal respects deg <= k-1
            for shape in gen.generate(k):
                assert max(m.degree() for m in shape.monomials) <= k - 1

    # The bound never leaks into the membership test: a deg-5 chain is
    # an ideal of size 6 regardless of any k the caller has in mind.
    gen = UniverseGenerator(max_variables=1)
    chain = frozenset({gen.monomial((i,)) for i in range(6)})
    assert gen.is_order_ideal(chain)
    print("[ok] Prop 2: |G_(n,k)| = C(n+k-1, n), bound confined to search")

# ---------------------------------------------------------------------
# 3c. Canonicalization invariants
# ---------------------------------------------------------------------

def test_canonicalization_invariants() -> None:
    gen = UniverseGenerator(max_variables=3)
    raw = [gen.monomial((0, 1, 0)), gen.monomial((0, 0, 0)),
           gen.monomial((1, 0, 0)), gen.monomial((2, 0, 0))]

    once = gen.canonicalize(raw, "EVEN")
    twice = gen.canonicalize(once.monomials, "EVEN")
    assert once == twice, "canonicalize is not idempotent"
    assert once.canonical(), "canonical() does not recognize C's image"

    # Support preservation, including under the padding embedding.
    assert set(once.monomials) == set(raw)
    assert len(once.monomials) == len(raw)
    short = gen.canonicalize([Monomial((1,)), Monomial((0, 0))], "EVEN")
    assert set(short.monomials) == {gen.monomial((1,)), gen.monomial((0, 0))}

    # Ideal invariance both ways: C creates no downset and destroys none.
    assert gen.canonicalize(raw, "EVEN").is_order_ideal()
    broken = [gen.monomial((0, 0, 0)), gen.monomial((2, 0, 0))]
    assert not gen.canonicalize(broken, "EVEN").is_order_ideal()

    # Multisets are refused rather than silently collapsed.
    try:
        gen.canonicalize([gen.monomial((1, 0, 0)), gen.monomial((1, 0, 0))])
    except ValueError:
        pass
    else:
        raise AssertionError("canonicalize collapsed a multiset")
    print("[ok] canonicalize: idempotent, support-preserving, ideal-invariant")

# ---------------------------------------------------------------------
# 3d. The correctness triad, against the independent oracle
# ---------------------------------------------------------------------

def test_generator_triad() -> None:
    # Ranges are the Level 2 evidence boundary, stated explicitly.
    slices = [(1, 8), (2, 6), (3, 5)]
    for n, kmax in slices:
        gen = UniverseGenerator(max_variables=n)
        for k in range(1, kmax + 1):
            emitted = gen.generate(k)

            # SOUNDNESS
            for s in emitted:
                assert s.is_order_ideal(), (n, k, s.monomials)
                assert len(s.monomials) == k
                assert s.is_valid()

            # UNIQUENESS -- meaningful because generate() accumulates a
            # list; a duplicate would survive to here.
            keys = [s.monomials for s in emitted]
            assert len(keys) == len(set(keys)), f"duplicate emission at n={n}, k={k}"

            # COMPLETENESS -- set equality with the oracle, not a count.
            oracle = _brute_force_ideals(n, k)
            assert set(keys) == oracle, (
                f"n={n}, k={k}: missing {len(oracle - set(keys))}, "
                f"spurious {len(set(keys) - oracle)}"
            )
    print(f"[ok] triad: sound, complete, unique vs oracle on {slices} (Level 2)")

def test_canonical_parent_tree() -> None:
    """The structural reason uniqueness holds: parent is single-valued and
    every ideal of size k >= 2 has its parent present one level down."""
    for n, kmax in [(2, 6), (3, 5)]:
        gen = UniverseGenerator(max_variables=n)
        for k in range(2, kmax + 1):
            below = {s.monomials for s in gen.generate(k - 1)}
            for s in gen.generate(k):
                F = frozenset(s.monomials)
                parent = gen.canonical_parent(F)
                assert parent is not None
                assert gen.is_order_ideal(parent), "parent left the ideal class"
                assert len(parent) == k - 1
                assert tuple(sorted(parent)) in below, "parent absent one level down"
    print("[ok] canonical parent: single-valued, ideal-preserving, tree-forming")

# ---------------------------------------------------------------------
# 3e. Benchmark counts (Level 2 empirical, finite slices)
# ---------------------------------------------------------------------

def test_benchmark_counts() -> None:
    # n = 1: the unique chain ideal {1, x, ..., x^{k-1}}, k = 1..8.
    gen1 = UniverseGenerator(max_variables=1)
    for k in range(1, 9):
        assert len(gen1.generate(k)) == 1, k

    # n = 2: labeled ideals of size k <-> partitions of k (anchored Ferrers
    # diagrams; variables labeled, so a shape and its transpose are distinct
    # whenever the partitions differ). k = 1..8.
    gen2 = UniverseGenerator(max_variables=2)
    for k in range(1, 9):
        got = len(gen2.generate(k))
        assert got == _partition_number(k), (k, got, _partition_number(k))

    # n = 3: plane partitions, OEIS A000219. k = 1..8.
    gen3 = UniverseGenerator(max_variables=3)
    assert [len(gen3.generate(k)) for k in range(1, 9)] == \
        [1, 3, 6, 13, 24, 48, 86, 160]

    # n = 4: solid partitions, OEIS A000293. k = 1..6.
    gen4 = UniverseGenerator(max_variables=4)
    assert [len(gen4.generate(k)) for k in range(1, 7)] == [1, 4, 10, 26, 59, 140]

    print("[ok] benchmarks: p(k) (n=2, k<=8), A000219 (n=3, k<=8), "
          "A000293 (n=4, k<=6) -- Level 2")

# ---------------------------------------------------------------------
# 3f. Guards and tagging
# ---------------------------------------------------------------------

def test_guards_and_tagging() -> None:
    try:
        UniverseGenerator(max_variables=2, max_degree=2).generate(5)
    except ValueError:
        pass
    else:
        raise AssertionError("truncation guard failed to raise")

    try:
        Monomial((1, -1))
    except ValueError:
        pass
    else:
        raise AssertionError("negative exponent accepted")

    gen = UniverseGenerator(max_variables=3)
    assert gen.monomial((2, 1)).exponents == (2, 1, 0)

    # parity is part of the cache key: two tags, two tagged families over
    # the identical underlying ideals.
    g = UniverseGenerator(max_variables=2)
    even, odd = g.generate(4, "EVEN"), g.generate(4, "ODD")
    assert all(s.parity == "EVEN" for s in even)
    assert all(s.parity == "ODD" for s in odd)
    assert {s.monomials for s in even} == {s.monomials for s in odd}
    print("[ok] guards: truncation, negative exponents, padding, parity key")

def self_test() -> None:
    test_proposition_1()
    test_proposition_2()
    test_canonicalization_invariants()
    test_generator_triad()
    test_canonical_parent_tree()
    test_benchmark_counts()
    test_guards_and_tagging()
    print("\nAll self-tests passed.")

if __name__ == "__main__":
    self_test()

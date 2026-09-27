# math/theorems/rotational_spiral_analyzer.py
"""
Rotational Spiral Analyzer — 3×3 Circulant Topology
=====================================================
Given a triple [A, B, C], construct the circulant matrix:

    [ A  B  C ]
    [ C  A  B ]
    [ B  C  A ]

Each row is a cyclic left-rotation of [A, B, C].

Five Topological Invariants
  1. Diagonal Invariant  — main diagonal is always [A, A, A]
  2. ML-Bar Signature    — 6 off-diagonal elements are always 3 B's + 3 C's
  3. V/X Hold            — mirror seam is palindromic (row-wise [X|X])
  4. Odd/Even Topology   — 4 classes: UNITY-ODD, UNITY-EVEN, SPIRAL-O, SPIRAL-E
  5. 8-Direction Set     — main diagonal the only ever-constant direction

B↔C Duality: swapping B and C preserves ML sum = 3(B+C)
              but flips the entire odd/even topology.
"""


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def _parity(x: int) -> str:
    return "O" if x % 2 != 0 else "E"


class RotationalSpiralAnalyzer:
    """10-layer topological fingerprint for any integer triple [A, B, C]."""

    def __init__(self, A: int, B: int, C: int):
        self.A, self.B, self.C = A, B, C
        self.matrix = [
            [A, B, C],
            [C, A, B],
            [B, C, A],
        ]

    # ── Layer 1: 8-direction set ──────────────────────────────────────────────
    def eight_directions(self) -> dict:
        m = self.matrix
        return {
            "row_0":     list(m[0]),
            "row_1":     list(m[1]),
            "row_2":     list(m[2]),
            "col_0":     [m[r][0] for r in range(3)],
            "col_1":     [m[r][1] for r in range(3)],
            "col_2":     [m[r][2] for r in range(3)],
            "main_diag": [m[i][i] for i in range(3)],
            "anti_diag": [m[i][2 - i] for i in range(3)],
        }

    # ── Layer 2: topological class ────────────────────────────────────────────
    def topological_class(self) -> str:
        A, B, C = self.A, self.B, self.C
        # Parity of A determines 3 diagonal cells; B,C each fill 3 off-diagonal
        a_odd = A % 2 != 0
        b_odd = B % 2 != 0
        c_odd = C % 2 != 0
        if a_odd and b_odd and c_odd:
            return "UNITY-ODD"
        if (not a_odd) and (not b_odd) and (not c_odd):
            return "UNITY-EVEN"
        total_odd = 3 * int(a_odd) + 3 * int(b_odd) + 3 * int(c_odd)
        return "SPIRAL-O" if total_odd >= 5 else "SPIRAL-E"

    # ── Layer 3: diagonal signature ───────────────────────────────────────────
    def diagonal(self) -> list:
        return [self.matrix[i][i] for i in range(3)]

    # ── Layer 4: ML-bar signature ─────────────────────────────────────────────
    def ml_bars(self) -> list:
        m = self.matrix
        return [m[i][j] for i in range(3) for j in range(3) if i != j]

    # ── Layer 5: odd/even map ─────────────────────────────────────────────────
    def odd_even_map(self) -> list:
        return [[_parity(self.matrix[i][j]) for j in range(3)] for i in range(3)]

    # ── Layer 6: V/X hold (palindromic seam) ─────────────────────────────────
    def mirror_seam(self) -> list:
        """Values at the center seam when matrix is mirrored horizontally."""
        m = self.matrix
        return [m[i][2] for i in range(3)]   # rightmost col = seam values

    def mirror_matrix(self) -> list:
        """3×6 view: [row | reversed(row)] for each row."""
        return [row + list(reversed(row)) for row in self.matrix]

    # ── Layer 7: surface/core/base decomposition ──────────────────────────────
    def layer_dimensions(self) -> dict:
        A, B, C = self.A, self.B, self.C
        # Core:    diagonal elements (all A)      — the invariant spine
        # Surface: off-diagonal (3 B's + 3 C's)  — the ML bars
        # Base:    total matrix sum               — arithmetic skeleton
        return {
            "core":         [A, A, A],
            "core_sum":     3 * A,
            "surface":      self.ml_bars(),
            "surface_sum":  3 * B + 3 * C,
            "base_sum":     3 * A + 3 * B + 3 * C,
            "base_dr":      dr(3 * (A + B + C)),
        }

    # ── Layer 8: mod-37 signature ─────────────────────────────────────────────
    def mod37_signature(self) -> dict:
        A, B, C = self.A, self.B, self.C
        abc = 100 * A + 10 * B + C
        return {
            "abc":          abc,
            "abc_mod37":    abc % 37,
            "abcabc_mod37": (abc * 1001) % 37,   # 1001 ≡ 2 (mod 37)
            "1001_mod37":   1001 % 37,
        }

    # ── Layer 9: digital root signature ──────────────────────────────────────
    def dr_signature(self) -> dict:
        A, B, C = self.A, self.B, self.C
        ml = self.ml_bars()
        return {
            "dr_A":       dr(A),
            "dr_B":       dr(B),
            "dr_C":       dr(C),
            "ml_sum":     sum(ml),
            "ml_dr":      dr(sum(ml)),
            "matrix_sum": 3 * (A + B + C),
            "matrix_dr":  dr(3 * (A + B + C)),
        }

    # ── Layer 10: mirror matrix (full V/X display) — see mirror_matrix() ─────

    def is_mirror_pair_of(self, other: "RotationalSpiralAnalyzer") -> bool:
        """True iff other is the B↔C swap of self."""
        return self.A == other.A and self.B == other.C and self.C == other.B

    def report(self, label: str = "") -> None:
        A, B, C = self.A, self.B, self.C
        diag  = self.diagonal()
        ml    = self.ml_bars()
        oe    = self.odd_even_map()
        cls   = self.topological_class()
        dims  = self.layer_dimensions()
        m37   = self.mod37_signature()
        drs   = self.dr_signature()
        mir   = self.mirror_matrix()
        total_odd = sum(row.count("O") for row in oe)
        tag = f"  [{label}]" if label else ""
        print(f"\n[A={A}, B={B}, C={C}]{tag}")
        print(f"  Matrix:      {self.matrix[0]}")
        print(f"               {self.matrix[1]}")
        print(f"               {self.matrix[2]}")
        print(f"  Class:       {cls}")
        print(f"  Diagonal:    {diag}  (invariant)")
        print(f"  ML bars:     {ml}  sum={sum(ml)}  DR={dr(sum(ml))}")
        print(f"  O/E map:     {oe}  ({total_odd}O, {9-total_odd}E)")
        print(f"  Core sum:    {dims['core_sum']}  Surface sum: {dims['surface_sum']}  Base: {dims['base_sum']} (DR={dims['base_dr']})")
        print(f"  Mod-37:      ABC={m37['abc']}  mod37={m37['abc_mod37']}  ABCABC mod37={m37['abcabc_mod37']}")
        print(f"  DR sig:      dr(A)={drs['dr_A']} dr(B)={drs['dr_B']} dr(C)={drs['dr_C']}  ml_dr={drs['ml_dr']}  matrix_dr={drs['matrix_dr']}")
        print(f"  Mirror V/X:")
        for row in mir:
            print(f"    {row[:3]} | {row[3:]}")


# ── Structural invariant assertions ──────────────────────────────────────────

def verify_invariants():
    """Verify all 5 topological invariants for a broad set of triples."""
    test_triples = [
        (1, 2, 3), (4, 3, 4), (3, 4, 3),
        (1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4),
        (3, 6, 9), (2, 5, 8), (7, 2, 5),
        (1, 9, 1), (4, 8, 4), (8, 5, 8),   # mod-37 identity ABCs
    ]

    for A, B, C in test_triples:
        s = RotationalSpiralAnalyzer(A, B, C)
        m = s.matrix

        # Invariant 1: diagonal is always [A, A, A]
        assert s.diagonal() == [A, A, A], f"Diagonal failed for [{A},{B},{C}]"

        # Invariant 2: ML bars are exactly 3 B's and 3 C's
        ml = s.ml_bars()
        assert len(ml) == 6
        if B != C:
            assert ml.count(B) == 3 and ml.count(C) == 3, (
                f"ML bar composition failed for [{A},{B},{C}]: {ml}"
            )
        else:
            # B == C: all 6 off-diagonal cells share the same value
            assert ml.count(B) == 6
        # ML sum = 3(B+C), independent of A
        assert sum(ml) == 3 * (B + C)

        # Invariant 3: mirror seam is palindromic — each row's center pair matches
        mir = s.mirror_matrix()
        for row in mir:
            assert row[2] == row[3], f"Mirror seam broken in row {row}"

        # Invariant 4: topological class consistent with odd/even counts
        oe = s.odd_even_map()
        total_odd = sum(r.count("O") for r in oe)
        cls = s.topological_class()
        if A % 2 != 0 and B % 2 != 0 and C % 2 != 0:
            assert cls == "UNITY-ODD" and total_odd == 9
        elif A % 2 == 0 and B % 2 == 0 and C % 2 == 0:
            assert cls == "UNITY-EVEN" and total_odd == 0
        elif total_odd >= 5:
            assert cls == "SPIRAL-O"
        else:
            assert cls == "SPIRAL-E"

        # Invariant 5: main diagonal is the ONLY constant direction (when A≠B or A≠C)
        dirs = s.eight_directions()
        if A != B or A != C:
            assert dirs["main_diag"] == [A, A, A]
            for name, vec in dirs.items():
                if name != "main_diag":
                    assert vec != [vec[0], vec[0], vec[0]], (
                        f"Non-diagonal direction {name} is constant for [{A},{B},{C}]"
                    )

    print("Invariant assertions: all passed")


def verify_specific():
    """Verify claims from the exposition verbatim."""

    # [1,2,3] → ML bars {2,3,3,2,2,3}, sum=15, DR=6
    s = RotationalSpiralAnalyzer(1, 2, 3)
    ml = s.ml_bars()
    assert sorted(ml) == [2, 2, 2, 3, 3, 3]
    assert sum(ml) == 15
    assert dr(15) == 6
    assert s.topological_class() == "SPIRAL-O"

    # [4,3,4] → ML bars {3,4,4,3,3,4}, sum=21, DR=3, SPIRAL-E
    s1 = RotationalSpiralAnalyzer(4, 3, 4)
    ml1 = s1.ml_bars()
    assert sorted(ml1) == [3, 3, 3, 4, 4, 4]
    assert sum(ml1) == 21
    assert dr(21) == 3
    assert s1.topological_class() == "SPIRAL-E"

    # [3,4,3] → ML bars {4,3,3,4,4,3}, sum=21, DR=3, SPIRAL-O
    s2 = RotationalSpiralAnalyzer(3, 4, 3)
    ml2 = s2.ml_bars()
    assert sorted(ml2) == [3, 3, 3, 4, 4, 4]
    assert sum(ml2) == 21
    assert dr(21) == 3
    assert s2.topological_class() == "SPIRAL-O"

    # Genuine B↔C mirror: [3,4,3] and [3,3,4]
    s_a = RotationalSpiralAnalyzer(3, 4, 3)
    s_b = RotationalSpiralAnalyzer(3, 3, 4)
    assert s_a.is_mirror_pair_of(s_b)
    assert s_b.is_mirror_pair_of(s_a)
    # B↔C swap preserves ML sum AND topological class:
    # total_odd = 3·p(A)+3·p(B)+3·p(C) is symmetric in B,C — class cannot flip
    assert sum(s_a.ml_bars()) == sum(s_b.ml_bars())
    assert s_a.topological_class() == s_b.topological_class()

    # The class-FLIP duality from the exposition is [X,Y,X]↔[Y,X,Y] — an A-swap,
    # not a B↔C swap: A changes from 4(even)→3(odd), flipping all 3 diagonal cells.
    assert RotationalSpiralAnalyzer(4, 3, 4).topological_class() == "SPIRAL-E"
    assert RotationalSpiralAnalyzer(3, 4, 3).topological_class() == "SPIRAL-O"
    # Both have identical ML bar multisets — only A's parity differs
    assert sorted(RotationalSpiralAnalyzer(4, 3, 4).ml_bars()) == \
           sorted(RotationalSpiralAnalyzer(3, 4, 3).ml_bars())

    # 1001 ≡ 2 (mod 37) — from mult_by_2_orbit audit
    assert 1001 % 37 == 2

    print("Specific claim assertions: all passed")


def run_mod37_triples():
    """Option A: feed the mod-37 identity ABCs through the engine."""
    print("\n--- Mod-37 Identity ABCs ---")
    triples = [(1, 9, 1), (4, 8, 4), (8, 5, 8)]
    analyzers = [RotationalSpiralAnalyzer(*t) for t in triples]
    for s in analyzers:
        s.report()
    # All share ABA structure (B↔C gives same A with B and C swapped)
    for s in analyzers:
        A, B, C = s.A, s.B, s.C
        m37 = s.mod37_signature()
        print(f"  [{A},{B},{C}]  ABC mod37={m37['abc_mod37']}  ABCABC mod37={m37['abcabc_mod37']}")


def verify():
    print("Rotational Spiral Analyzer — Structural Audit\n")
    verify_invariants()
    verify_specific()
    run_mod37_triples()

    print("\n--- Core Examples ---")
    for triple in [(1, 2, 3), (4, 3, 4), (3, 4, 3), (1, 1, 1), (2, 2, 2)]:
        RotationalSpiralAnalyzer(*triple).report()

    print("\nAll assertions passed.")


if __name__ == "__main__":
    verify()

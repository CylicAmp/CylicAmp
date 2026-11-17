# CLASS: AUDIT
"""
Pasted "Tsirelson bound -- explicit saturation construction" (2026-11-17), from another tool, relayed by the owner.
Convention: C = A0 (x) (B0 - B1) + A1 (x) (B0 + B1); A0 = Z, A1 = X, B0 = (Z + X)/sqrt2, B1 = (X - Z)/sqrt2;
state (|00> + |11>)/sqrt2. Every identity checked exactly below (sympy).

RIGHT:
  A_i, B_j self-adjoint with square I;  B0 - B1 = sqrt2 Z,  B0 + B1 = sqrt2 X;  C = sqrt2 (Z(x)Z + X(x)X);
  ZZ |Phi+> = XX |Phi+> = |Phi+>, so C |Phi+> = 2 sqrt2 |Phi+> and <Phi+|C|Phi+> = 2 sqrt2;
  for this convention C^2 = 4I + [A0, A1] (x) [B0, B1]  (the "corrected identity" -- right, for any such A_i, B_j);
  [A0, A1] = 2i Y;  eigenvalues of C: 2 sqrt2, 0, 0, -2 sqrt2, so ||C|| = 2 sqrt2 (Tsirelson's bound, attained).

WRONG (a sign):
  [B0, B1] = +2i Y, not -2i Y. So [A0, A1] (x) [B0, B1] = (2iY)(x)(2iY) = -4 Y(x)Y, and C^2 = 4I - 4 Y(x)Y, not
  4I + 4 Y(x)Y. The paste's version contradicts its own state result: (4I + 4YY)|Phi+> = 0, while C^2|Phi+> =
  8|Phi+> (YY|Phi+> = -|Phi+>). The norm conclusion survives either sign (C^2 has eigenvalues 8 and 0), but the
  identity and the component record must carry the minus sign.

PRIOR ART: the bound is Tsirelson's (1980); the identity C^2 = 4I +- [A0,A1](x)[B0,B1] is the standard route
  (Landau 1987). No earlier CHSH file in the repo.

FALSIFICATION: any assertion failing.
"""
import sympy as sp

I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.Matrix([[1, 0], [0, -1]])
kp = sp.kronecker_product
zero4 = sp.zeros(4)

A0, A1 = Z, X
B0, B1 = (Z + X) / sp.sqrt(2), (X - Z) / sp.sqrt(2)
for M in (A0, A1, B0, B1):
    assert M == M.H and sp.simplify(M * M) == I2
assert sp.simplify(B0 - B1) == sp.sqrt(2) * Z and sp.simplify(B0 + B1) == sp.sqrt(2) * X

C = kp(A0, B0 - B1) + kp(A1, B0 + B1)
assert sp.simplify(C - sp.sqrt(2) * (kp(Z, Z) + kp(X, X))) == zero4

phi = sp.Matrix([1, 0, 0, 1]) / sp.sqrt(2)
assert kp(Z, Z) * phi == phi and kp(X, X) * phi == phi
assert sp.simplify(C * phi - 2 * sp.sqrt(2) * phi) == sp.zeros(4, 1)
assert sp.simplify((phi.H * C * phi)[0]) == 2 * sp.sqrt(2)

cA = A0 * A1 - A1 * A0
cB = sp.simplify(B0 * B1 - B1 * B0)
assert cA == 2 * sp.I * Y
assert cB == 2 * sp.I * Y and cB != -2 * sp.I * Y                # the paste has -2iY
C2 = sp.simplify(C * C)
assert sp.simplify(C2 - 4 * sp.eye(4) - kp(cA, cB)) == zero4     # C^2 = 4I + [A0,A1](x)[B0,B1]: right
assert sp.simplify(C2 - (4 * sp.eye(4) - 4 * kp(Y, Y))) == zero4  # = 4I - 4 YY
assert sp.simplify(C2 - (4 * sp.eye(4) + 4 * kp(Y, Y))) != zero4  # the paste's 4I + 4 YY: wrong
assert sp.simplify(kp(Y, Y) * phi + phi) == sp.zeros(4, 1)        # YY phi = -phi
assert sp.simplify((4 * sp.eye(4) + 4 * kp(Y, Y)) * phi) == sp.zeros(4, 1)   # the paste's identity gives 0 here
assert sp.simplify(C2 * phi - 8 * phi) == sp.zeros(4, 1)
assert C.eigenvals() == {2 * sp.sqrt(2): 1, 0: 2, -2 * sp.sqrt(2): 1}

# the general identity, for any +-1 observables on each side, by the algebra: D- D+ = [B0,B1], D+ D- = -[B0,B1]
a, b = sp.symbols("a b", real=True)
U = sp.Matrix([[sp.cos(a), sp.sin(a)], [sp.sin(a), -sp.cos(a)]])
V = sp.Matrix([[sp.cos(b), sp.sin(b)], [sp.sin(b), -sp.cos(b)]])
Cg = kp(Z, U - V) + kp(X, U + V)
assert sp.simplify(Cg * Cg - 4 * sp.eye(4) - kp(Z * X - X * Z, U * V - V * U)) == zero4

# the corrected component record in records/ carries the right signs
import json  # noqa: E402
import pathlib  # noqa: E402

rec = json.loads((pathlib.Path(__file__).resolve().parents[2] / "records" / "tsirelson_component_record_2026_11_17.json").read_text())
assert rec["commutators"] == {"[A0,A1]": "2i sigma_y", "[B0,B1]": "2i sigma_y"}
assert rec["C_squared_explicit"] == "4I - 4 sigma_y (x) sigma_y" and rec["exact_operator_norm"] == "2 sqrt2"
assert rec["quantum_lean_status"] == "OPEN"

if __name__ == "__main__":
    print("Tsirelson saturation right (C phi = 2 sqrt2 phi, ||C|| = 2 sqrt2); sign: [B0,B1] = +2iY, C^2 = 4I - 4YY")

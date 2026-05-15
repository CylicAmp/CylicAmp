# math/theorems/node_verification_matrix_audit.py
"""
Node Verification Matrix — DR, QR(13), Sphenic, Happy
======================================================
Five nodes: 167, 241, 389, 463, 907
Probe:      371113

Checks per node:
  - digital root matches claim
  - DR parity (even/odd) matches claim
  - quadratic residue mod 13 determines QR_Shift ∈ {+1, -1}

Correlation finding:
  QR_Shift is determined SOLELY by n mod 13.
  No perfect correlation with DR parity: nodes 463 and 907 are mixed.
"""

import math


def calculate_digital_root(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def verify_dr_parity(n: int, expected_parity: str) -> bool:
    dr = calculate_digital_root(n)
    parity_str = "Even" if dr % 2 == 0 else "Odd"
    return parity_str == expected_parity


QR_MOD13 = {0, 1, 3, 4, 9, 10, 12}
NQR_MOD13 = {2, 5, 6, 7, 8, 11}


def verify_qr_mod_13(n: int, expected_shift: int) -> bool:
    shift = 1 if (n % 13) in QR_MOD13 else -1
    return shift == expected_shift


def is_happy(num: int) -> bool:
    seen: set = set()
    while num != 1 and num not in seen:
        seen.add(num)
        num = sum(int(c) ** 2 for c in str(num))
    return num == 1


def is_sphenic(n: int) -> bool:
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return len(factors) == 3 and len(set(factors)) == 3


NODES = {
    167: {"DR": 5, "Parity": "Odd",  "QR_Shift": -1},
    241: {"DR": 7, "Parity": "Odd",  "QR_Shift": -1},
    389: {"DR": 2, "Parity": "Even", "QR_Shift":  1},
    463: {"DR": 4, "Parity": "Even", "QR_Shift": -1},
    907: {"DR": 7, "Parity": "Odd",  "QR_Shift":  1},
}

PROBE = 371113


def verify():
    # ── Verification matrix ───────────────────────────────────────────────────
    for node, claims in NODES.items():
        assert calculate_digital_root(node) == claims["DR"], f"DR failed for {node}"
        assert verify_dr_parity(node, claims["Parity"]),     f"Parity failed for {node}"
        assert verify_qr_mod_13(node, claims["QR_Shift"]),   f"QR_Shift failed for {node}"

    # ── Probe ─────────────────────────────────────────────────────────────────
    assert is_sphenic(PROBE)
    assert is_happy(PROBE)

    # ── QR(13) correctness ───────────────────────────────────────────────────
    # Quadratic residues mod 13: x^2 mod 13 for x=0..12
    qr_actual = {(x * x) % 13 for x in range(13)}
    assert qr_actual == QR_MOD13
    assert QR_MOD13 | NQR_MOD13 == set(range(13))
    assert QR_MOD13 & NQR_MOD13 == set()

    # ── Correlation analysis ──────────────────────────────────────────────────
    # QR_Shift is not perfectly correlated with DR parity.
    # Nodes 463 (Even DR, QR=-1) and 907 (Odd DR, QR=+1) break the pattern.
    mixed = [n for n, c in NODES.items()
             if c["QR_Shift"] != (-1 if c["Parity"] == "Odd" else 1)]
    assert set(mixed) == {463, 907}

    # ── Individual mod-13 residues ────────────────────────────────────────────
    assert 167 % 13 == 11  and 11 in NQR_MOD13   # QR_Shift = -1 ✓
    assert 241 % 13 == 7   and 7  in NQR_MOD13   # QR_Shift = -1 ✓
    assert 389 % 13 == 12  and 12 in QR_MOD13    # QR_Shift = +1 ✓
    assert 463 % 13 == 8   and 8  in NQR_MOD13   # QR_Shift = -1 ✓
    assert 907 % 13 == 10  and 10 in QR_MOD13    # QR_Shift = +1 ✓

    # ── Print report ─────────────────────────────────────────────────────────
    print("Node Verification Matrix")
    print()
    print(f"  {'Node':>6}  {'DR':>3}  {'Parity':>5}  {'mod13':>5}  {'QR':>5}  {'Shift':>6}  All")
    for node, claims in NODES.items():
        mod13 = node % 13
        in_qr = mod13 in QR_MOD13
        dr    = calculate_digital_root(node)
        print(f"  {node:>6}  {dr:>3}  {claims['Parity']:>5}  {mod13:>5}  {str(in_qr):>5}  "
              f"{claims['QR_Shift']:>+6}  ✓")
    print()
    print(f"  Probe {PROBE}: sphenic={is_sphenic(PROBE)}, happy={is_happy(PROBE)}  ✓")
    print()
    print(f"  QR(13) = {sorted(QR_MOD13)}")
    print(f"  QR_Shift determined solely by n mod 13 — no correlation with DR parity.")
    print(f"  Mixed nodes (break Even↔+1 / Odd↔-1 hypothesis): {sorted(mixed)}")
    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()

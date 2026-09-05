"""
Dark Sector Algebra — GF(37)

The quadratic residue structure of GF(37) produces a clean visible/dark
sector partition that coincides exactly with the sovereign named sets.

VISIBLE SECTOR (QR — quadratic residues mod 37):
  SA = {4,9,25,30}    — all sovereign anchors are QR
  ST = {3,12,21,30}   — all sovereign targets are QR
  ORBIT_11 = {11,27,36} — entirely QR
  30 (SA∩ST intersection node) — QR

DARK SECTOR (NQR — non-quadratic residues mod 37):
  PR = {2,5,13,15,17,18,19,20,22,24,32,35} — all 12 primitive roots are NQR
  CB = {8,13,24}      — cascade base entirely NQR
  TESLA_FLOW = 6      — NQR but not a primitive root (NQR\\PR)

Proof that PR ⊂ NQR:
  Primitive roots have multiplicative order 36 = φ(37).
  Quadratic residues form a subgroup of order 18 = φ(37)/2,
  so every QR has order dividing 18.
  Therefore no primitive root can be a QR. □

Prime gap residues mod 37 land on named named residues:
  gap ≡  4: SA (visible sovereign anchor)
  gap ≡ 12: ST (visible sovereign target)
  gap ≡  8: CB (dark cascade base)
  gap ≡  6: TESLA_FLOW (dark)
  gap ≡  2: PR (dark primitive root)

Totient product formula: φ(37) × φ(k) = 36 × φ(k) for gcd(37,k)=1
  This governs the joint period of GF(37)* extended by k-structure.

The dark sector boundary is the Legendre symbol:
  χ(n) = (n/37) = +1 for visible, −1 for dark, 0 for SEAM
"""

import sympy

# ── Constants ────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
ORBIT_11   = frozenset({11, 27, 36})
TESLA_FLOW = 6
SCALAR_137 = 26
SEAM       = 0

PHI_37     = 36    # φ(37) = 37 − 1; ord₃₇(2) = 36


# ── Legendre symbol and sector classification ─────────────────────────────────

def legendre(n, p=37):
    """Legendre symbol (n/p): +1 QR, −1 NQR, 0 if p|n."""
    n = n % p
    if n == 0:
        return 0
    return 1 if pow(n, (p - 1) // 2, p) == 1 else -1


def sector(n):
    """Visible (+1), dark (−1), or seam (0)."""
    return legendre(n % 37)


# ── Sector sets ────────────────────────────────────────────────────────────────

QR  = frozenset(n for n in range(1, 37) if legendre(n) ==  1)   # visible
NQR = frozenset(n for n in range(1, 37) if legendre(n) == -1)   # dark


# ── Assertions: visible/dark sector partition ─────────────────────────────────

# PR ⊂ NQR — all primitive roots are dark
assert PR <= NQR

# NQR \ PR — dark non-generators (includes TESLA_FLOW and one CB element)
NQR_NON_PR = NQR - PR
assert TESLA_FLOW in NQR_NON_PR              # 6 is dark but not a primitive root
assert 8 in NQR_NON_PR                       # 8 ∈ CB is dark non-PR

# SA entirely visible
assert SA <= QR

# ST entirely visible
assert ST <= QR

# 30 = SA∩ST — visible (QR)
assert 30 in QR
assert SA & ST == frozenset({30})

# CB entirely dark
assert CB <= NQR

# ORBIT_11 entirely visible
assert ORBIT_11 <= QR

# Even split: exactly 18 QR and 18 NQR in GF(37)*
assert len(QR) == 18
assert len(NQR) == 18
assert QR | NQR == frozenset(range(1, 37))
assert QR & NQR == frozenset()

# TESLA_FLOW is dark
assert legendre(TESLA_FLOW) == -1

# SCALAR_137 = 26 in QR (the 137-map multiplier is visible)
assert legendre(SCALAR_137) == 1
assert SCALAR_137 in QR

# φ(37) = 36
assert PHI_37 == 36
assert len(PR) == PHI_37 // 3   # 12 = 36/3


# ── Prime gap residues mod 37 ─────────────────────────────────────────────────

def prime_gap_residues(limit=500):
    """Compute the set of prime gap values mod 37 up to the given prime limit."""
    primes = list(sympy.primerange(2, limit))
    gaps   = [primes[i+1] - primes[i] for i in range(len(primes) - 1)]
    return sorted(set(g % 37 for g in gaps))


GAP_RESIDUES = prime_gap_residues()

# Every prime gap residue hits a named named residue
GAP_FRAMEWORK = {
    4:  "SA",
    12: "ST",
    8:  "CB",
    6:  "TESLA_FLOW",
    2:  "PR/NQR",
    1:  "QR",
    10: "DECADE_ANCHOR/QR",
    14: "NQR",
}

assert all(g in GAP_FRAMEWORK for g in GAP_RESIDUES)

# The SA-hitting gap is 4 (twin prime gap scaled: 4 ∈ SA)
assert 4 in GAP_RESIDUES and 4 in SA

# The ST-hitting gap is 12
assert 12 in GAP_RESIDUES and 12 in ST

# The CB-hitting gap is 8
assert 8 in GAP_RESIDUES and 8 in CB

# The smallest prime gap (2 = twin prime spacing) is dark (NQR, PR)
assert 2 in GAP_RESIDUES and legendre(2) == -1 and 2 in PR


# ── Totient product formula ────────────────────────────────────────────────────

def totient_product(k):
    """φ(37) × φ(k) mod 37 — joint period governor."""
    return (PHI_37 * int(sympy.totient(k))) % 37


# φ(37)×φ(2) = 36×1 = 36 ≡ 36 (ORBIT_11 node: 36 ≡ −1 mod 37)
assert totient_product(2) == 36 and 36 in ORBIT_11

# φ(37)×φ(3) = 36×2 = 72 ≡ 72 mod 37 = 35 ∈ PR
assert totient_product(3) == 35 and 35 in PR

# φ(37)×φ(4) = 36×2 = 72 ≡ 35 ∈ PR
assert totient_product(4) == 35 and 35 in PR

# φ(37)×φ(9) = 36×6 = 216 ≡ 216 mod 37 = 216 - 5×37 = 216-185 = 31 ∈ NQR
assert totient_product(9) == 31 and 31 in NQR

# φ(37)×φ(36) = 36×12 = 432 ≡ 432 mod 37
_tp36 = (36 * 12) % 37
assert totient_product(36) == _tp36


# ── Sector summary ─────────────────────────────────────────────────────────────

SECTOR_MAP = {
    "SA":       ("visible", QR,  SA),
    "ST":       ("visible", QR,  ST),
    "ORBIT_11": ("visible", QR,  ORBIT_11),
    "PR":       ("dark",    NQR, PR),
    "CB":       ("dark",    NQR, CB),
}


if __name__ == "__main__":
    print("Dark Sector Algebra — GF(37)")
    print("=" * 60)
    print()
    print("Legendre symbol (n/37): +1 = visible (QR), −1 = dark (NQR)")
    print()

    print("VISIBLE SECTOR — QR (18 elements):")
    print(f"  {sorted(QR)}")
    print()
    print("DARK SECTOR — NQR (18 elements):")
    print(f"  {sorted(NQR)}")
    print()

    print("CLASS BREAKDOWN:")
    for cls, (sect, _, nodes) in SECTOR_MAP.items():
        syms = [(n, legendre(n)) for n in sorted(nodes)]
        print(f"  {cls:<10} [{sect}]: {syms}")
    print(f"  TESLA_FLOW  [dark]:    {TESLA_FLOW} → χ={legendre(TESLA_FLOW)}")
    print(f"  SCALAR_137  [visible]: {SCALAR_137} → χ={legendre(SCALAR_137)}")
    print(f"  30 (SA∩ST)  [visible]: χ={legendre(30)}")
    print()

    print("NQR \\ PR (dark non-generators):")
    print(f"  {sorted(NQR - PR)}")
    print(f"  includes TESLA_FLOW={TESLA_FLOW}, CB∩(NQR\\PR)={sorted(CB & (NQR-PR))}")
    print()

    print("PRIME GAP RESIDUES mod 37:")
    for g in GAP_RESIDUES:
        label = GAP_FRAMEWORK.get(g, "?")
        chi = legendre(g)
        sect = "visible" if chi == 1 else "dark"
        print(f"  gap ≡ {g:2d}: {sect:<8}  {label}")
    print()

    print("TOTIENT PRODUCTS φ(37)×φ(k) mod 37:")
    for k in [2, 3, 4, 6, 9, 12, 18, 36]:
        tp = totient_product(k)
        chi = legendre(tp)
        tags = []
        for s, nm in [(SA,"SA"),(ST,"ST"),(CB,"CB"),(PR,"PR"),(ORBIT_11,"O11")]:
            if tp in s: tags.append(nm)
        if chi == 1:  tags.append("QR")
        if chi == -1: tags.append("NQR")
        print(f"  φ(37)×φ({k:2d}) mod 37 = {tp:2d}  [{', '.join(tags)}]")
    print()

    print("All assertions pass. SA and ST are entirely visible (QR).")
    print("CB and PR are entirely dark (NQR). The sector boundary is the Legendre symbol.")

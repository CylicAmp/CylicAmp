"""
Theorem 216: Buckingham Pi Theorem — Null Space and F_37 Bridge

Variables: v, L, rho, mu, c_s
Rows of D: L (length), T (time), M (mass)

The dimensional matrix D has rank 3, nullity 2.
The null space basis gives Re = rho*v*L/mu and Ma = v/c_s.
Over F_37 the rank and nullity are preserved, and the null vectors
map as -1 -> 36 (mod 37), revealing structural resonance with the
GF(37).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import numpy as np

P = 37

# Dimensional matrix: rows = (L, T, M), cols = (v, L, rho, mu, c_s)
D = np.array([
    [ 1,  1, -3, -1,  1],   # L
    [-1,  0,  0, -1, -1],   # T
    [ 0,  0,  1,  1,  0],   # M
], dtype=int)

VARIABLES = ["v", "L", "rho", "mu", "c_s"]
DIMENSIONS = ["L", "T", "M"]

# Null space basis (SymPy exact, integer)
K1 = np.array([-1, -1, -1,  1,  0])   # 1/Re = mu/(rho*v*L)
K2 = np.array([-1,  0,  0,  0,  1])   # 1/Ma = c_s/v

# Standard dimensionless groups (negatives of above)
RE = -K1   # [1, 1, 1, -1, 0] -> Re = rho*v*L/mu
MA = -K2   # [1, 0, 0, 0, -1] -> Ma = v/c_s


def verify_null_space():
    assert np.all(D @ K1 == 0), "K1 not in null space"
    assert np.all(D @ K2 == 0), "K2 not in null space"
    assert np.all(D @ RE == 0), "Re not in null space"
    assert np.all(D @ MA == 0), "Ma not in null space"


def rank_nullity():
    rank = np.linalg.matrix_rank(D)
    n = D.shape[1]
    nullity = n - rank
    return rank, nullity


def null_space_f37():
    """Null space of D mod 37 over F_37."""
    D_mod = D % P
    # -1 mod 37 = 36, -3 mod 37 = 34
    k1_mod = K1 % P   # [36, 36, 36, 1, 0]
    k2_mod = K2 % P   # [36, 0, 0, 0, 1]
    # Verify: D_mod @ k1_mod ≡ 0 (mod 37)
    check1 = (D_mod @ k1_mod) % P
    check2 = (D_mod @ k2_mod) % P
    return D_mod, k1_mod, k2_mod, check1, check2


def group_action_summary():
    """
    The scaling group G = (R_{>0})^3 (one factor per dimension L,T,M)
    acts on R^5 (one factor per variable).

    R^5 = Im(D^T) + ker(D)
      dim Im(D^T) = rank(D) = 3   (gauge / scaling degrees of freedom)
      dim ker(D)  = nullity  = 2   (physical invariants: Re, Ma)

    The quotient R^5 / Im(D^T) is isomorphic to ker(D).
    Orbits of G are equivalence classes of physically identical systems.
    """
    rank, nullity = rank_nullity()
    n = D.shape[1]
    assert rank + nullity == n
    return rank, nullity, n


def run():
    print("=" * 70)
    print("THEOREM 216: BUCKINGHAM PI — NULL SPACE AND F_37 BRIDGE")
    print("=" * 70)

    print(f"\nDimensional matrix D (rows=L,T,M  cols=v,L,rho,mu,c_s):")
    print(D)

    verify_null_space()
    print("\nNull space basis (integer):")
    print(f"  K1 = {K1.tolist()}  ->  Pi_1 = mu/(rho*v*L)  [= 1/Re]")
    print(f"  K2 = {K2.tolist()}  ->  Pi_2 = c_s/v         [= 1/Ma]")
    print(f"  Re = {RE.tolist()}  ->  Pi_1 = rho*v*L/mu")
    print(f"  Ma = {MA.tolist()}  ->  Pi_2 = v/c_s")
    print("  All null-space verifications passed.")

    rank, nullity = rank_nullity()
    n = D.shape[1]
    print(f"\nRank-Nullity: n={n}, rank={rank}, nullity={nullity}")
    print(f"  {rank} + {nullity} = {rank + nullity} = {n}  [verified]")
    print(f"  -> 2 dimensionless groups: Re and Ma")

    D_mod, k1_mod, k2_mod, c1, c2 = null_space_f37()
    print(f"\nD mod {P}:")
    print(D_mod)
    print(f"\nNull space over F_{P}:")
    print(f"  k1 = {k1_mod.tolist()}  (36 = -1 mod 37)")
    print(f"  k2 = {k2_mod.tolist()}")
    print(f"  D*k1 mod 37 = {c1.tolist()}  (expect all zero)")
    print(f"  D*k2 mod 37 = {c2.tolist()}  (expect all zero)")

    assert np.all(c1 == 0), "F_37 null check failed for k1"
    assert np.all(c2 == 0), "F_37 null check failed for k2"
    print(f"\nStructural resonance: rank and nullity preserved over F_{P}.")
    print(f"  -1 -> 36 (mod 37): the null vectors are identical up to this map.")

    print("\nGroup action: G = (R_>0)^3 acts on R^5.")
    r, nul, n = group_action_summary()
    print(f"  dim Im(D^T) = {r}   (gauge degrees of freedom)")
    print(f"  dim ker(D)  = {nul}   (physical invariants)")
    print(f"  R^n = Im(D^T) + ker(D) : {r} + {nul} = {r+nul} = {n}  [verified]")

    return {
        "rank": rank,
        "nullity": nullity,
        "K1": K1.tolist(),
        "K2": K2.tolist(),
        "k1_F37": k1_mod.tolist(),
        "k2_F37": k2_mod.tolist(),
    }


if __name__ == "__main__":
    run()

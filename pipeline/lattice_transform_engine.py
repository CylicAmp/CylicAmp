"""
LATTICE TRANSFORM ENGINE
=========================================================================

Encodes D4 symmetry (rotations + mirror) combined with cyclic translational
shifts (h horizontal, v vertical) into a single integer token ID.

The canonical base sequence is [1, 2, 3, 4].  apply_transform operates on
this 4-element sequence and tiles it to width N for N×N lattice contexts.

Coordinate system:
  r  — D4 rotation index  [0, 3]  (cyclic right-shift of the base by r)
  m  — mirror flag         [0, 1]  (reverse after shifts)
  h  — horizontal shift    [0, N-1]  (additional cyclic right-shift, mod 4)
  v  — vertical shift      [0, N-1]  (row-phase offset in 2D contexts)

Encoding:
  stride_h = N,  stride_m = N²,  stride_r = 2N²
  ID = r·stride_r  +  m·stride_m  +  h·stride_h  +  v
  Max ID: 8N² − 1  (127 for N=4, 511 for N=8)

apply_transform algorithm on base [1, 2, 3, 4]:
  1. Cyclic right-shift by r  (mod 4)
  2. Cyclic right-shift by h  (mod 4)
  3. Reverse if m == 1
  4. Tile ×(N/4) to produce a width-N row

Verified against spec table (all 7 cases ✓):
  N=4  (0,0,0,0) →  0  → [1,2,3,4]
  N=4  (0,1,0,0) → 16  → [4,3,2,1]
  N=4  (1,0,1,1) → 37  → [3,4,1,2]
  N=4  (3,1,3,3) → 127 → [2,1,4,3]
  N=8  (0,0,0,0) →  0  → [1,2,3,4,1,2,3,4]
  N=8  (0,1,0,0) → 64  → [4,3,2,1,4,3,2,1]
  N=8  (3,1,7,7) → 511 → [2,1,4,3,2,1,4,3]
"""

from typing import Tuple, List


class LatticeTransformEngine:
    BASE: List[int] = [1, 2, 3, 4]
    BASE_N: int = 4

    def __init__(self, size: int = 4) -> None:
        if size not in (4, 8):
            raise ValueError("Size must be 4 or 8.")
        self.N        = size
        self.stride_h = size
        self.stride_m = size * size
        self.stride_r = size * size * 2
        self.max_id   = 8 * (size ** 2) - 1

    # ------------------------------------------------------------------
    # Encoding / decoding
    # ------------------------------------------------------------------

    def encode_id(self, r: int, m: int, h: int, v: int) -> int:
        """Convert (r, m, h, v) coordinates to a single integer token ID."""
        if not (0 <= r < 4):
            raise ValueError("r must be in [0, 3].")
        if not (0 <= m < 2):
            raise ValueError("m must be in [0, 1].")
        if not (0 <= h < self.N):
            raise ValueError(f"h must be in [0, {self.N - 1}].")
        if not (0 <= v < self.N):
            raise ValueError(f"v must be in [0, {self.N - 1}].")
        return r * self.stride_r + m * self.stride_m + h * self.stride_h + v

    def decode_id(self, transform_id: int) -> Tuple[int, int, int, int]:
        """Decode a token ID back to (r, m, h, v)."""
        if not (0 <= transform_id <= self.max_id):
            raise ValueError(
                f"transform_id {transform_id} out of bounds [0, {self.max_id}]."
            )
        r   = transform_id // self.stride_r
        rem = transform_id  % self.stride_r
        m   = rem // self.stride_m
        rem %= self.stride_m
        h   = rem // self.stride_h
        v   = rem  % self.stride_h
        return r, m, h, v

    # ------------------------------------------------------------------
    # Transform
    # ------------------------------------------------------------------

    def apply_transform(self, transform_id: int) -> List[int]:
        """
        Apply transform to the canonical base [1,2,3,4] and return a
        width-N row (tiled if N > 4).  v is a vertical phase parameter
        used when building 2D lattice rows; it does not affect this
        1D base output.
        """
        r, m, h, _v = self.decode_id(transform_id)
        seq = list(self.BASE)

        # Step 1 — rotation: cyclic right-shift by r
        r_mod = r % self.BASE_N
        if r_mod:
            seq = seq[-r_mod:] + seq[:-r_mod]

        # Step 2 — horizontal shift: cyclic right-shift by h (mod BASE_N)
        h_mod = h % self.BASE_N
        if h_mod:
            seq = seq[-h_mod:] + seq[:-h_mod]

        # Step 3 — mirror
        if m:
            seq = seq[::-1]

        # Step 4 — tile to width N
        return seq * (self.N // self.BASE_N)


# =============================================================================
# Verification
# =============================================================================

_SPEC: list = [
    # (N, r, m, h, v, expected_tid, expected_row)
    (4, 0, 0, 0, 0,   0, [1, 2, 3, 4]),
    (4, 0, 1, 0, 0,  16, [4, 3, 2, 1]),
    (4, 1, 0, 1, 1,  37, [3, 4, 1, 2]),
    (4, 3, 1, 3, 3, 127, [2, 1, 4, 3]),
    (8, 0, 0, 0, 0,   0, [1, 2, 3, 4, 1, 2, 3, 4]),
    (8, 0, 1, 0, 0,  64, [4, 3, 2, 1, 4, 3, 2, 1]),
    (8, 3, 1, 7, 7, 511, [2, 1, 4, 3, 2, 1, 4, 3]),
]


def run_verification() -> bool:
    all_ok = True
    print("=" * 70)
    print("LATTICE TRANSFORM ENGINE — SPEC VERIFICATION")
    print("=" * 70)

    for (N, r, m, h, v, expected_tid, expected_row) in _SPEC:
        eng = LatticeTransformEngine(N)

        tid   = eng.encode_id(r, m, h, v)
        dec   = eng.decode_id(tid)
        row   = eng.apply_transform(tid)

        enc_ok = tid == expected_tid
        dec_ok = dec == (r, m, h, v)
        row_ok = row == expected_row
        ok     = enc_ok and dec_ok and row_ok

        tag = "✓" if ok else "✗"
        print(
            f"  N={N} ({r},{m},{h},{v}) → tid={tid:3d}  enc={tag if enc_ok else '✗'}  "
            f"dec={tag if dec_ok else '✗'}  row={tag if row_ok else '✗'}  {row}"
        )
        if not ok:
            all_ok = False
            if not enc_ok:
                print(f"    ✗ encode: got {tid}, expected {expected_tid}")
            if not dec_ok:
                print(f"    ✗ decode: got {dec}, expected ({r},{m},{h},{v})")
            if not row_ok:
                print(f"    ✗ row:    got {row}")
                print(f"             expected {expected_row}")

    print(f"\nAll {len(_SPEC)} cases verified: {all_ok}")
    return all_ok


if __name__ == "__main__":
    run_verification()

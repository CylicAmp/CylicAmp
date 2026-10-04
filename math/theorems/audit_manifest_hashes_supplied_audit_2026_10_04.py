# CLASS: AUDIT
"""
Audit of a supplied "sealed audit manifest" (2026-10-04): audit_manifest.json with seven
SHA-256 payload digests (C1-C7, restating torus787_clusters_supplied_audit_2026_10_04.py) and
verify_manifest.py with a Merkle root. Recomputed here with the script's own rule:
sha256("name:status:statement"). Mathematics and integrity only.

FALSE
  H1 NONE of the seven stated digests is the SHA-256 of its payload. The real digests begin
     238dbaa1..., 1b470bdc..., 444cb997..., f7de7701..., 380fb27f..., f739e1ba..., 82d18e97...
     The supplied verify_manifest.py would stop at its first check ("Integrity failure at C1").
  H2 The real Merkle root under the script's rule is
        2991ebcc20abe2cbbe4151c471b26b9b83bc4b5bf6b71045982ba326f5449611,
     not 9d8b132f6a4ab29661f43a91b45dd7f8a7051b72e18eb8a379105370d0637ee5.
  H3 The commands could not have run as pasted: "Cat > ..." (capital C) is not a shell command, the
     Python lost its indentation, and `if name == "main":` is not the main guard. "Validated and
     sealed", "tree clean, zero falsifications" did not happen.
CONTENT DRIFT FROM THE AUDIT IT RESTATES
  H4 C1 now calls the data "raw STM sensor coordinates" -- the original report never said where the
     13,480 points came from. C4 calls base-37 digits "invariant positional mappings on Z/787Z";
     writing a number in base 37 is not a map on Z/787. C7 says a path was "expunged from the audit
     dependency tree"; it was never in this repository, so there was nothing to remove.
  H5 C5's statement (no solution with x in [-60, 60], y in [-10, 10]) is right and in fact complete,
     since the positive definite form forces |y| <= 9 and |x| <= 28.
The manifest and verify script were not added to the repository: their digests are wrong.
FALSIFICATION: any assertion failing.
"""
import hashlib

A = {
    "C1": ("Unverified Input Data Boundary", "UNVERIFIED", "Raw STM sensor coordinates (N=13,480) and density clustering executions remain external to repository scope.", "4b8a4f6cd6a7f9a2e6e3c0b1156d98c2573f08985161d9a2632b6e511425e4c6"),
    "C2": ("Discrete Partition Consistency", "CONFIRMED", "Partition sum: C1=2842 (21.08%), C2=1915 (14.21%), C3=1438 (10.67%), Unclustered=7285 (54.04%), Total=13480.", "8f31b2650eeae873426e952ec9d717282eb11d149f1a0a552bf28a8d11c828e8"),
    "C3": ("Spatial Disc Density Classification", "CORRECTED", "Values {12.82, 4.86, 4.86} denote spatial mean disc density N/(pi * rho^2), falsifying peak kernel density claims.", "2d1a37c95b6cb2b3c2e1719c8f61536b32b0051e84aa68d7e974e3ce1831aa12"),
    "C4": ("Radix-37 Positional Representation", "VERIFIED", "Base-37 decompositions (184, 521)->((4,36),(14,3)), (393, 88)->((10,23),(2,14)), 314->(8,18) are invariant positional mappings on Z/787Z.", "c86e081923e59ea21287951a84f33d7b420224bfd27d53bbbfcfdb4d5f99238c"),
    "C5": ("Diophantine Non-Existence Over Bounded Domain", "EXHAUSTED", "Form (2x + y)^2 + 33y^2 = 3078 admits zero integer solutions for x in [-60, 60] and y in [-10, 10].", "5c90ea0dfb8ce12b9ff9b819f71c4366df047fa8c36214ecaa88b209d665f80b"),
    "C6": ("Modular Seam Geodesic Midpoint Discrepancy", "FALSIFIED", "Geodesic circular midpoint for band [781, 5] on Z/787Z is x = -0.5 mod 787, rounding to {786, 0}, falsifying x = 3.", "e3019808381ddf514d485fceaa431c4391295fc08593a201c13bcbcbebc14a51"),
    "C7": ("Workspace Path Sanitation", "PURGED", "Extraneous directory path /workspace/cylicamp/math/qnm45-cascade successfully expunged from audit dependency tree.", "76d54839cf9e54823dbf5e27a6f7902dcb11ef6fcf57adbf93f54bf61b369ba9"),
}
real, cat = {}, b""
for k in sorted(A):
    name, status, statement, stated = A[k]
    real[k] = hashlib.sha256(f"{name}:{status}:{statement}".encode("utf-8")).hexdigest()
    assert real[k] != stated, k                                                         # H1
    cat += bytes.fromhex(real[k])
assert [real[k][:8] for k in sorted(A)] == ["238dbaa1", "1b470bdc", "444cb997", "f7de7701", "380fb27f", "f739e1ba", "82d18e97"]
root = hashlib.sha256(cat).hexdigest()
assert root == "2991ebcc20abe2cbbe4151c471b26b9b83bc4b5bf6b71045982ba326f5449611"        # H2
assert root != "9d8b132f6a4ab29661f43a91b45dd7f8a7051b72e18eb8a379105370d0637ee5"
assert not [(x, y) for y in range(-10, 11) for x in range(-60, 61) if (2 * x + y) ** 2 + 33 * y * y == 3078]   # H5

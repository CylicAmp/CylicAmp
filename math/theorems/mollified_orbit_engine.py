# math/theorems/mollified_orbit_engine.py
"""
Mollified Orbit Engine
Entry 110

Applies a smoothing layer (K=0.37, 37-field constant) to noisy data
before running the deterministic MWS Orbit Audit.

Valid frames: the two right-rotation orbits of {1,1,2,3} digits.
  Orbit1: 1123 → 3112 → 2311 → 1231 → (cycle)
  Orbit2: 1132 → 2113 → 3211 → 1321 → (cycle)

K = 0.37 is the smoothing threshold (mirrors the mod-37 field constant).
If |data_point − nearest_frame| / nearest_frame ≤ K, snap to that frame.
"""

ORBIT1 = [1123, 3112, 2311, 1231]
ORBIT2 = [1132, 2113, 3211, 1321]
VALID_FRAMES = ORBIT1 + ORBIT2

_ORBIT_MAP = {v: 1 for v in ORBIT1}
_ORBIT_MAP.update({v: 2 for v in ORBIT2})

# Right-rotation successor for each valid frame (deterministic next step)
_ROT_NEXT = {}
for _orb in (ORBIT1, ORBIT2):
    for _i in range(4):
        _ROT_NEXT[_orb[_i]] = _orb[(_i + 1) % 4]


def _rotR(n):
    s = str(n)
    return int(s[-1] + s[:-1])


def smooth_to_frame(data_point, k):
    """
    Pull data_point into the nearest valid rotation frame.
    Threshold k (default 0.37): relative distance ≤ k → snap.
    Returns the snapped frame, or data_point unchanged if outside threshold.
    """
    nearest = min(VALID_FRAMES, key=lambda f: abs(data_point - f))
    if abs(data_point - nearest) / nearest <= k:
        return nearest
    return data_point


def orbit_audit_engine(stream):
    """
    Deterministic orbit check on a (presumably mollified) stream.
    For each element reports:
      value            — the value being checked
      orbit            — 1, 2, or None (not a valid frame)
      valid_frame      — True if value is a recognised frame
      valid_transition — True if this step is a correct right-rotation of previous
      orbit_cross      — True if step moves between orbits (the Section-4 mistake pattern)
    """
    results = []
    for i, val in enumerate(stream):
        orbit = _ORBIT_MAP.get(val)
        valid_frame = orbit is not None

        if i == 0:
            valid_transition = True
            orbit_cross = False
        else:
            prev = stream[i - 1]
            prev_orbit = _ORBIT_MAP.get(prev)
            valid_transition = (_rotR(prev) == val) if prev in _ORBIT_MAP else False
            # Orbit cross: both recognised but in different orbits AND transition invalid
            orbit_cross = (
                prev_orbit is not None and
                orbit is not None and
                prev_orbit != orbit
            )

        results.append({
            'value': val,
            'orbit': orbit,
            'valid_frame': valid_frame,
            'valid_transition': valid_transition,
            'orbit_cross': orbit_cross,
        })
    return results


def mollified_orbit_audit(raw_data_stream, smoothing_factor=0.37):
    """
    Applies a Mollifier (Smoothing Layer) to raw noisy data
    before performing the MWS Orbit Audit.
    """
    # 1. MOLLIFIER LAYER (The 'Penn' Step)
    mollified_stream = [smooth_to_frame(pt, smoothing_factor) for pt in raw_data_stream]

    # 2. MWS ORBIT AUDIT (The 'Matt' Step)
    audit_results = orbit_audit_engine(mollified_stream)

    return audit_results


# ── Assertions ────────────────────────────────────────────────────────────────

# Orbit integrity
for orb in (ORBIT1, ORBIT2):
    for i in range(4):
        assert _rotR(orb[i]) == orb[(i + 1) % 4]

# Orbits are disjoint
assert set(ORBIT1) & set(ORBIT2) == set()

# All frames have DS=7, DR=7
def _ds(n): return sum(int(d) for d in str(n))
def _dr(n): return (n - 1) % 9 + 1 if n > 0 else 9
assert all(_ds(f) == 7 and _dr(f) == 7 for f in VALID_FRAMES)

# smooth_to_frame: exact frames snap to themselves
for f in VALID_FRAMES:
    assert smooth_to_frame(f, 0.37) == f

# smooth_to_frame: small noise snaps to nearest frame
assert smooth_to_frame(1120, 0.37) == 1123   # |1120-1123|/1123 ≈ 0.003 < 0.37
assert smooth_to_frame(3110, 0.37) == 3112
assert smooth_to_frame(2310, 0.37) == 2311
assert smooth_to_frame(1230, 0.37) == 1231

# smooth_to_frame: large noise stays put
assert smooth_to_frame(9999, 0.37) == 9999   # far from all frames

# orbit_audit_engine: clean Orbit1 sequence
clean1 = ORBIT1[:]
res1 = orbit_audit_engine(clean1)
assert all(r['orbit'] == 1 for r in res1)
assert all(r['valid_transition'] for r in res1)
assert not any(r['orbit_cross'] for r in res1)

# orbit_audit_engine: clean Orbit2 sequence
clean2 = ORBIT2[:]
res2 = orbit_audit_engine(clean2)
assert all(r['orbit'] == 2 for r in res2)
assert all(r['valid_transition'] for r in res2)
assert not any(r['orbit_cross'] for r in res2)

# orbit_audit_engine: Section-4 mistake — 3112→3211 is an orbit cross
mistake_stream = [1123, 3112, 3211, 1321]  # jumps from Orbit1 to Orbit2
res_m = orbit_audit_engine(mistake_stream)
assert res_m[0]['orbit'] == 1 and res_m[0]['valid_transition'] is True
assert res_m[1]['orbit'] == 1 and res_m[1]['valid_transition'] is True
assert res_m[2]['orbit'] == 2 and res_m[2]['orbit_cross'] is True   # caught
assert res_m[2]['valid_transition'] is False

# mollified_orbit_audit end-to-end: noisy Orbit1 stream
noisy = [1120, 3115, 2308, 1228]
audit = mollified_orbit_audit(noisy)
assert all(r['orbit'] == 1 for r in audit)
assert all(r['valid_transition'] for r in audit)
assert not any(r['orbit_cross'] for r in audit)

# K=0.37 connects to the 37-field: 1/37 ≈ 0.027, period-3 decimal
import math
assert abs(1 / 37 - 0.027027) < 1e-5
assert 27 * 37 == 999

# Orbit1 mod-37 residues
assert 1123 % 37 == 13
assert 3112 % 37 == 4
assert 2311 % 37 == 17
assert 1231 % 37 == 10

# Orbit2 mod-37 residues
assert 1132 % 37 == 22
assert 2113 % 37 == 4   # same as 3112 mod 37 — orbit collision in 37-field
assert 3211 % 37 == 29
assert 1321 % 37 == 26  # = AML Z/26Z modulus


if __name__ == "__main__":
    print("Mollified Orbit Engine")
    print()
    print(f"Valid frames: {VALID_FRAMES}")
    print(f"K = 0.37  (37-field constant, 1/37 = 0.027027... period-3)")
    print()

    print("Orbit structure:")
    for label, orb in [("Orbit1", ORBIT1), ("Orbit2", ORBIT2)]:
        mods = [f % 37 for f in orb]
        print(f"  {label}: {orb}  mod37={mods}")
    print()

    print("Noise-snap demo (K=0.37):")
    for noisy_val in [1120, 3115, 2308, 1228, 9999]:
        snapped = smooth_to_frame(noisy_val, 0.37)
        snap_str = f"→ {snapped}" if snapped != noisy_val else "→ (no snap)"
        print(f"  {noisy_val:5d}  {snap_str}")
    print()

    print("Orbit cross detection (Section-4 mistake pattern):")
    stream = [1123, 3112, 3211, 1321]
    results = orbit_audit_engine(stream)
    for r in results:
        cross_flag = "  ← ORBIT CROSS" if r['orbit_cross'] else ""
        inv_flag = "  [invalid transition]" if not r['valid_transition'] else ""
        print(f"  {r['value']}  orbit={r['orbit']}  valid_trans={r['valid_transition']}{inv_flag}{cross_flag}")
    print()
    print("All assertions passed.")

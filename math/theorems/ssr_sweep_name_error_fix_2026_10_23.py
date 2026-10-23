# CLASS: COMPUTATION
"""
The NameError in the pasted notebook cell (owner_work #424, 2026-10-23):

    125     details.append((n, cv, dr, is_dr7))
    NameError: name 'n' is not defined

THE CAUSE: inside simulate_ssr, line 125 writes n into each detail row, but nothing in the function gives n a value
-- the loop over the kept points names its own variable something else (or has no step number at all). Python only
finds out when the line runs, so the first call, simulate_ssr(36) on line 133, stops there.

THE FIX: give the loop the step number it is reporting. The kept points are the ones the pipeline's modular filter
keeps (cylicamp/insights.py: step numbers 0 and 1 by 37 -- 0, 1, 37, 38, 74, 75, ...), so the loop is

    for n, e in filtered:          # n = the step number, e = the energy at that step

The rest of the cell is not in the paste; simulate_ssr below is rebuilt from the repo's own pipeline code -- the
PHI/PSI trajectory of cylicamp/trajectory.py, the energy |x| + |y| and the angle 0.95 of cylicamp/engine_integration.py,
the filter of cylicamp/insights.py, the DR = 7 prime check of cylicamp/duality.py -- and checked against them.
If the notebook cell differs, the same one-line fix applies to it.

RESULT (the cell's sweep, run with the fix):
  steps 36 72 108 144 180 360 720 -> kept 2 4 6 8 10 20 40 points, SSR 0 every time
  why 0: the distance shrinks by PSI = 0.618 each step, so the check values run 1000 638 406 258 164 104 65 41 26
  16 10 6 4 2 1 and then 0 from step 15 on; the only kept steps before that are 0 (1000) and 1 (638 = 2 x 11 x 29),
  and neither is a prime with root 7. This is the pipeline's "Stability Ratio 0.0000".
  reduced PSI, 720 steps: 0.9, 0.95, 0.99 -> SSR 0; 0.999 -> SSR 1/40 = 0.025 (step 259, value 1087: prime, root 7)

FALSIFICATION: any assertion failing.
"""
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "math" / "primes")]
from cylicamp.trajectory import TrajectoryGenerator, PHI, PSI  # noqa: E402
from cylicamp.duality import DualityVerifier  # noqa: E402
from cylicamp.insights import MODULAR_CONSTANT  # noqa: E402
from field_simulation import Field, Packet  # noqa: E402

dv = DualityVerifier()


def pipeline_angle():
    f = Field(n=12)
    for _ in range(50):
        f.step()
    f.inject(Packet(value=0.95, activation=0.4))
    for _ in range(5):
        f.degrade(0.1)
    return f.mean_threshold()


ANGLE = pipeline_angle()


def trajectory(steps, psi=PSI, angle_multiplier=ANGLE):
    x, y = 1.0, 0.0
    out = [(x, y)]
    for _ in range(steps):
        a = math.atan2(y, x) + PHI * angle_multiplier
        d = math.hypot(x, y) * psi
        x, y = d * math.cos(a), d * math.sin(a)
        out.append((x, y))
    return out


def simulate_ssr(steps, psi_override=None):
    psi = PSI if psi_override is None else psi_override
    energies = [abs(x) + abs(y) for x, y in trajectory(steps, psi)]
    filtered = [(n, e) for n, e in enumerate(energies) if n % MODULAR_CONSTANT in (0, 1)]
    stable, details = 0, []
    for n, e in filtered:                          # the fix: n is the step number of the kept point
        cv = int(abs(e) * 1000)
        dr = dv.calculate_digital_root(cv)
        is_dr7 = dv.is_dr_7_prime(cv)
        if is_dr7:
            stable += 1
        details.append((n, cv, dr, is_dr7))
    ssr = stable / len(filtered) if filtered else 0
    return ssr, len(filtered), details


# --- the rebuild matches the repo's pipeline ---
assert abs(ANGLE - 0.95) < 1e-12
tg = TrajectoryGenerator()
ref = tg.generate_trajectory(steps=50, angle_multiplier=ANGLE)
assert all(abs(a[0] - b[0]) < 1e-12 and abs(a[1] - b[1]) < 1e-12 for a, b in zip(ref, trajectory(50)))
spectrum = [abs(x) + abs(y) for x, y in ref]
assert dv.verify_duality_spectrum(spectrum, 0.5)["Stability_Ratio"] == 0.0          # the pipeline's 0.0000

# --- the sweep the cell runs, now without the error ---
ssr_sweep = {}
for steps in [36, 72, 108, 144, 180, 360, 720]:
    ssr, count, details = simulate_ssr(steps)
    ssr_sweep[steps] = {"ssr": ssr, "filtered_count": count}
    assert count == len([n for n in range(steps + 1) if n % 37 in (0, 1)])
    assert all(d[0] % 37 in (0, 1) for d in details)
assert [ssr_sweep[s]["filtered_count"] for s in ssr_sweep] == [2, 4, 6, 8, 10, 20, 40]
assert all(v["ssr"] == 0 for v in ssr_sweep.values())

# why 0: the distance shrinks by PSI = 0.618... each step, so from step 15 on the energy x 1000 is below 1
e = [abs(x) + abs(y) for x, y in trajectory(40)]
assert [int(v * 1000) for v in e[:16]] == [1000, 638, 406, 258, 164, 104, 65, 41, 26, 16, 10, 6, 4, 2, 1, 0]
assert all(int(v * 1000) == 0 for v in e[15:])
assert int(e[0] * 1000) == 1000 and not dv.is_dr_7_prime(1000)                    # step 0: 1000, not prime
# the only kept steps before the energy dies are 0 and 1
assert [n for n in range(16) if n % 37 in (0, 1)] == [0, 1]
assert simulate_ssr(36)[2] == [(0, 1000, 1, False), (1, 638, 8, False)]    # 638 = 2 x 11 x 29, not prime

# --- the reduced-PSI tries (closer to 1 = slower shrinking) ---
psi_runs = {}
for psi in (0.9, 0.95, 0.99, 0.999):
    ssr, count, details = simulate_ssr(720, psi_override=psi)
    psi_runs[psi] = (ssr, count, [d for d in details if d[3]])
assert [psi_runs[p][0] for p in (0.9, 0.95, 0.99)] == [0, 0, 0]
assert psi_runs[0.999][0] == 1 / 40 and psi_runs[0.999][2] == [(259, 1087, 7, True)]
assert dv.is_dr_7_prime(1087) and 1 + 0 + 8 + 7 == 16

if __name__ == "__main__":
    print("NameError fixed: n = the step number of each kept point (0, 1, 37, 38, ...)")
    for s, v in ssr_sweep.items():
        print("  steps %4d: kept %2d, SSR %.4f" % (s, v["filtered_count"], v["ssr"]))
    for psi, (ssr, count, hits) in psi_runs.items():
        print("  psi %.3f, 720 steps: kept %d, SSR %.4f, DR 7 primes at %s" % (psi, count, ssr, [(d[0], d[1]) for d in hits]))

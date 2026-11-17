# CLASS: COMPUTATION
"""
CI check for math/exhaustion/ellipse_selector/ (I.V test case, November 16-23, 2026): runs the verifier's 23 checks,
re-validates the committed selector_results.json, and confirms both animation frames trace to tested rows
(k = 9: 3,072 sides, rejected at 1e-5, nine-mark limit_reached; k = 10: 6,144 sides, certified).

FALSIFICATION: any assertion failing.
"""
import json
import pathlib
import sys

D = pathlib.Path(__file__).resolve().parents[1] / "exhaustion" / "ellipse_selector"
sys.path.insert(0, str(D))
import verify_selector as V  # noqa: E402

ok, fresh = V.run_checks()
assert ok
committed = json.loads((D / "selector_results.json").read_text())
assert V.validate(committed) == []
rows = {r["k"]: r for r in committed["rows"]}
assert rows[9]["n"] == 3072 and rows[9]["decisions"]["1e-5"] == "rejected"
assert rows[10]["n"] == 6144 and rows[10]["decisions"]["1e-5"] == "certified"
for name in ("selector_animation.svg", "selector_frames.svg"):
    svg = (D / name).read_text()
    assert "3,072 sides · area tolerance unmet" in svg and "6,144 sides · both tolerances met" in svg
    assert "limit_reached" in svg and all(f"{f} Hz" in svg for f in (396, 417, 432, 528, 639, 741, 852, 963))
    assert "node layer: unset · edge layer: unset" in svg

if __name__ == "__main__":
    print("ellipse selector: 23 checks pass, committed JSON valid, both frames trace to rows k = 9 and k = 10")

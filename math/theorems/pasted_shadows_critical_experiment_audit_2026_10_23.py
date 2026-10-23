# CLASS: AUDIT
"""
The pasted description of a graphic: a sphere, a cylinder and a cone with equal circular bases cast the
same circular shadow under light from above, and a circle, a rectangle (a square when the height is
twice the radius) and a triangle under light from the side -- "underdetermination" and the test that
breaks it (owner_work #420, 2026-10-23). Audit on arrival.

THE PASTE: text from another tool, relayed by the owner; its "Formalization" lines arrived empty.
Nothing below puts a claim of the paste in the owner's mouth.

RIGHT (computed on a grid, radius r = 1, height h = 2, the solids standing on the floor):
  light from above, shadow on the floor:
    sphere    x x + y y <= 1                         a circle, area pi = 3.14...
    cylinder  x x + y y <= 1                         the same circle
    cone      x x + y y <= 1 (its base)              the same circle
    -> the three shadows are the same set of points: the test cannot tell the shapes apart
  light from the side, shadow on the wall:
    sphere    x x + (z - 1)(z - 1) <= 1              a circle, area pi
    cylinder  |x| <= 1, 0 <= z <= 2                  a 2 by 2 square, area 4
    cone      |x| <= 1 - z / 2, 0 <= z <= 2          a triangle, base 2, height 2, area 2
    -> three different shadows: this test tells them apart

IN THE REPO, THE SAME IDEA (a test that gives the same answer for every candidate says nothing):
  .claude/skills/miss-test and .claude/skills/null-control: declare in advance what a miss looks like,
    and run a do-nothing candidate through the check before believing the check.
  dashboards/owner_engine/: the control row "adding 8 adds 1" must show FAIL; and the walk's check is
    not only "missed by the prediction = 0" -- a prediction of "always yes" misses 0 too (light from
    above) -- but also "predicted at most one number in three", which "always yes" fails (light from
    the side). Both are asserted below.

FALSIFICATION: any assertion failing.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
import owner_engine as E  # noqa: E402

R, H, N = 1.0, 2.0, 400          # radius, height, grid points per unit
step = 1.0 / N


def grid(x0, x1, y0, y1):
    xs = [x0 + (i + 0.5) * step for i in range(int((x1 - x0) * N))]
    ys = [y0 + (j + 0.5) * step for j in range(int((y1 - y0) * N))]
    return [(x, y) for x in xs for y in ys]


# light from above: the shadow is where some height z puts the point inside the solid
top = grid(-1.2, 1.2, -1.2, 1.2)
sphere_top = {p for p in top if p[0] ** 2 + p[1] ** 2 <= R * R}
cylinder_top = {p for p in top if p[0] ** 2 + p[1] ** 2 <= R * R}
cone_top = {p for p in top if any(p[0] ** 2 + p[1] ** 2 <= (R * (1 - z / H)) ** 2 for z in (0.0,))}
assert sphere_top == cylinder_top == cone_top
assert abs(len(sphere_top) * step * step - math.pi) < 0.01

# light from the side (along y): the shadow on the wall (x, z)
side = grid(-1.2, 1.2, 0.0, 2.2)
sphere_side = {p for p in side if p[0] ** 2 + (p[1] - R) ** 2 <= R * R}
cylinder_side = {p for p in side if abs(p[0]) <= R and p[1] <= H}
cone_side = {p for p in side if p[1] <= H and abs(p[0]) <= R * (1 - p[1] / H)}
areas = [len(s) * step * step for s in (sphere_side, cylinder_side, cone_side)]
assert abs(areas[0] - math.pi) < 0.01 and abs(areas[1] - 4.0) < 0.01 and abs(areas[2] - 2.0) < 0.01
assert len({frozenset(sphere_side), frozenset(cylinder_side), frozenset(cone_side)}) == 3
assert 2 * R == H                 # the cylinder's side shadow is a square at h = 2r

# the engine's walk: "missed = 0" alone is light from above; "one in three" is light from the side
w = E.walk(1, 20000)
always_yes_predicted = w["numbers"]
always_yes_missed = 0             # predicting every number can never miss
assert w["missed"] == [] and always_yes_missed == 0                     # both pass the first check
assert w["predicted"] <= w["numbers"] // 3 + 1 < always_yes_predicted   # only the real prediction passes the second
results, control = E.check()
assert all(ok for *_, ok in results) and control is False

if __name__ == "__main__":
    print("shadows: from above all three are the same circle (area pi); from the side circle pi, square 4, "
          "triangle 2 -- right; the engine's control row and its one-in-three walk check are the side light")

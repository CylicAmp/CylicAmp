# CLASS: AUDIT
"""
Audit of a supplied clustering report (2026-10-04): DBSCAN on 13,480 "outlier coordinates" on the
torus (Z/787)^2, three clusters, base-37 encodings of their centroids, and repository anchors.
Mathematics only.

UNVERIFIED (no data)
  C1 The 13,480 coordinates were not supplied, nor how they were produced, so the clustering
     itself (centroids, counts, radii, the entropy 0.94 H_max) cannot be reproduced. Status:
     UNVERIFIED under the owner's protocol.
INTERNAL ARITHMETIC -- CORRECT
  C2 2842 / 1915 / 1438 of 13,480 are 21.08% / 14.21% / 10.67%; the remainder is 7,285 = 54.04%.
  C3 "Peak density" is count / (pi rho^2): 2842 / (pi 8.4^2) = 12.82, 1438 / (pi 9.7^2) = 4.86,
     1915 / (pi 11.2^2) = 4.86 (stated 4.85). That is the MEAN density inside the radius, not a peak.
  C4 Base-37 digits: 184 = 4*37 + 36, 521 = 14*37 + 3, 393 = 10*37 + 23, 88 = 2*37 + 14,
     314 = 8*37 + 18 -- all right. The encoding only rewrites each number in base 37; it adds no
     information (37 plays no part in a clustering on Z/787).
  C5 The repository record's Diophantine line is right: Q(x, y) = lambda_+(m) is
     2x^2 + 2xy + 17y^2 = m^2(2m + 1), and times 2 that is (2x + y)^2 + 33y^2 = 2m^2(2m + 1); at
     m = 9 the right side is 3078 and there is no integer solution (checked) -- the same fact as
     qnm45_package_supplied_audit_2026_10_04.py, Q6.
INCONSISTENT
  C6 Cluster gamma: centroid "781 <-> 5" (a band crossing the seam) is encoded as x = 3. The circular
     midpoint of 781 and 5 on Z/787 is 786.5, i.e. 786 or 0 -- not 3.
  C7 "Repository record: /workspace/cylicamp/math/qnm45-cascade on main": no such folder exists on
     main (checked after fetching origin). The facts it lists (cut 8, ratio 4/7, 41 cells) are this
     repository's audits, recorded elsewhere.
FALSIFICATION: any assertion failing.
"""
import math

counts = (2842, 1915, 1438)
assert [round(100 * c / 13480, 2) for c in counts] == [21.08, 14.21, 10.67]              # C2
assert 13480 - sum(counts) == 7285 and round(100 * 7285 / 13480, 2) == 54.04
dens = [c / (math.pi * r * r) for c, r in zip(counts, (8.4, 11.2, 9.7))]                 # C3
assert [round(d, 2) for d in dens] == [12.82, 4.86, 4.86]
assert [divmod(v, 37) for v in (184, 521, 393, 88, 314)] == [(4, 36), (14, 3), (10, 23), (2, 14), (8, 18)]  # C4
assert 2 * 81 * 19 == 3078                                                                # C5
assert not [(x, y) for y in range(-10, 11) for x in range(-60, 61) if (2 * x + y) ** 2 + 33 * y * y == 3078]
assert all(2 * (2 * x * x + 2 * x * y + 17 * y * y) == (2 * x + y) ** 2 + 33 * y * y for x in range(-5, 6) for y in range(-5, 6))
mid = (781 + (5 + 787)) / 2 % 787                                                         # C6
assert mid == 786.5 and mid != 3

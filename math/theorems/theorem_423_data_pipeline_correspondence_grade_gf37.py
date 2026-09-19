# CLASS: COMPUTATION
"""
Theorem 423: the data-pipeline correspondence, graded by the four cuts --
four of its five claims are decidable, and three of them decide against it

A supplied mapping reads modern pipeline architecture as "a physical
realization of the kernel filtration, quotient strata, and measure-preserving
transforms established across the ledger", in five claims. This file applies
claim-grade's four cuts to each. It does not argue about roles; where a
literal object exists it computes it, the way --check-eca decides rule 90
against rule 30.

PRIOR ART.
  T194 (theorem_194_mtls_ingestion_gf37.py) is the corpus's existing
  ingestion-pipeline-on-GF(37) file; this is a grading, not a second one.
  T379 is the shell/Riemann object claim 1 borrows.
  T380 is the birthday object claim 3 borrows.
  T381 is the napkin ring claim 4 borrows, plus its 2026-09-19 surface law.
  T305 is where the four cuts come from.
  The four-tier rewrite-certificate ledger of claim 2 is NOT in the corpus:
  `grep -rl "e_hard\\|K_E\\|EASY_EQ\\|quotient strata\\|kernel filtration"`
  returns nothing over every .py and .md. That absence is itself the grade
  for claim 2 and is asserted below.

================================================================================
THE GRADES
================================================================================

  claim                                        level  weakest cut  decided by
  1 batch partition = Riemann sum               L1    Cut 1        computation
  2 four-tier ledger = DLQ validation tiers     --    ungradeable  absent source
  3 birthday bound bounds bucket allocation     L1    Cut 3        native/corr.
  4 napkin ring = aggregation projection        L1    Cut 1        computation
  5 quadrant partition = sharding               L1    Cut 1        computation

  No claim reaches Level 2. Not one names a map Phi, objects on each side,
  and a relation that survives it. "Is a physical realization of" is the
  Level-1 formula: a role, asserted.

================================================================================
CLAIM 1 -- "batch partitioning evaluates a Riemann sum, and truncating
            endpoints incurs an O(1/n) defect"
================================================================================

  CUT 1, and it decides. Look for the literal object. A Riemann sum
  approximates an integral of a CONTINUOUS integrand, and its error is
  governed by that integrand's variation -- T379's whole content is that in
  the shell derivation the 1/n IS the entire error.

  Partitioning a stream is a different object: an exact partition of a finite
  multiset. Summing over batches is additive, so for EVERY n

      sum over batches  -  total  =  0

  exactly, with no error term to be O(1/n) of. Verified below over 10000
  records at n = 1, 3, 7, 100, 9999: the residual is 1e-12, which is float
  rounding, and it does not shrink with n because it was never an
  approximation error.

  The literal object exists and it is a DIFFERENT object. Decided, not a
  matter of taste. Level 1.

  What IS true, and is not this claim: an aggregate computed over a window
  of a stream is an approximation of the process generating the stream, and
  THAT has sampling error. But its rate is governed by the process, not by
  the batch count n, and it is present at n = 1.

================================================================================
CLAIM 2 -- "the four-tier rewrite-certificate ledger maps one-to-one to DLQ
            validation layers"
================================================================================

  Ungradeable as stated, and the reason is not a judgement call.

  Cut 2 asks, for Level 2, for the objects on each side. The DLQ side is
  clear. The ledger side -- EXACT / EASY_EQUIVALENT / FINAL_EQUIVALENT /
  INVALID, K_easy, K_E, e_hard - 1 non-trivial coset defects -- is not in
  this corpus under those names or any of them. The grep is asserted below.

  So there is no source object to build a Phi from. This is not "the claim is
  wrong"; it is "the claim's left-hand side has not been written down here".
  Two honest outcomes: write the ledger as its own file first and then grade
  the map, or read the claim as Level 1 about a four-tier filtration in
  general, which is a role and a common one.

  Noting the shape anyway: a filtration by cost-to-certify (0, O(1), heavy,
  fails) is a real and useful design, and it does not need GF(37) to be one.

================================================================================
CLAIM 3 -- "bucket allocation is bounded below by the birthday threshold"
================================================================================

  This is the one whose MATHEMATICS is strongest and whose CORRESPONDENCE is
  no stronger than the others. That gap is exactly Cut 3.

  NATIVE strength: Level 3, and verified. The 1/2-crossing point n*(N)
  satisfies n* / (1.1774 sqrt(N)) -> 1:

      N = 365      n* = 23    ratio 1.0225
      N = 4096     n* = 76    ratio 1.0086
      N = 65536    n* = 302   ratio 1.0019
      N = 10^6     n* = 1178  ratio 1.0005

  and 1.1774 = sqrt(2 ln 2). This is a theorem about hashing and it is true.

  CORRESPONDENCE strength: Level 1. The claim identifies the SAME theorem
  applied in two places -- 23 people in 365 days, n keys in N buckets -- and
  it is the same theorem, which is why nothing is being mapped. A single
  theorem used twice is not a correspondence between two domains; it is one
  domain with two instantiations. Cut 3's rule fires exactly here: the
  target's rigour does not upgrade the map, and there is no map.

  T380 is the relevant prior file, and note what it establishes: 253/365
  agrees with ln 2 to 3.5e-6, so the Poisson ESTIMATE lands on 1/2. The
  agreement is an artifact of choosing n = 23 on a 365-day calendar, not
  evidence about Poisson fidelity -- which is the correction already made to
  the supplied birthday script, and it applies to the crypto restatement too.

================================================================================
CLAIM 4 -- "napkin-ring invariance = an aggregate depending on the window and
            not on the background scale"
================================================================================

  CUT 1, and it decides, because the claim drops the mechanism.

  The R-cancellation in T381 is not a property of integrating over a window
  of height h. Integrate the SOLID sphere over the same window and R stays:

      int_{-h/2}^{h/2} pi (R^2 - z^2) dz  =  pi ( R^2 h - h^3/12 )

  which depends on R and is computed below at R = 3, 5, 20. The invariance
  appears only when the bore is subtracted,

      pi(R^2 h - h^3/12)  -  pi (R^2 - h^2/4) h  =  pi h^3 / 6

  i.e. R cancels because it appears TWICE with opposite sign, once in the
  sphere and once in the removed cylinder. The window does no cancelling.

  An aggregation has one term, not two. "Depends on the window, not the table
  size" is a statement that a query ignores a parameter -- an assumption
  about the query -- whereas the napkin ring is a cancellation between two
  terms that each carry the parameter. Different objects. Level 1.

  And the surface law added to T381 on 2026-09-19 sharpens the point:

      S(R) = 2 pi h ( R + sqrt(R^2 - (h/2)^2) ) ~ 4 pi R h

  The boundary carries R linearly however thin the ring gets. So even in the
  literal object, "independent of the background scale" is true of exactly
  one functional and false of the next one over.

================================================================================
CLAIM 5 -- "sharding into k partitions creates 90-degree corner loss, shifting
            the slope from 1/pi to 4/pi"
================================================================================

  CUT 1 again, with two separate computations, both below.

  (a) There is no loss in the measure. Quartering the unit disc:

          area:      4 x 0.785398 = 3.141593   vs  pi   excess 0
          perimeter: 4 x 3.570796 = 14.283185  vs 2 pi   excess 8.000000 = 8r

      The area is additive EXACTLY -- that is what a partition of a measure
      means, and it is why the final barrier sync reconstructs the total with
      no loss. The boundary is not additive: quartering adds 8r of new edge,
      the four cut radii counted twice.

  (b) Neither 1/pi nor 4/pi is any of the natural ratios:

          A/P    circle 0.500000   sector 0.219950
          A/P^2  circle 0.079577 = 1/(4 pi)   sector 0.061597
          claimed          1/pi = 0.318310    4/pi = 1.273240

      The claimed "slope" matches nothing the partition actually changes.
      Until the two quantities whose ratio is meant are named, there is no
      relation for a Phi to preserve, so Cut 2 cannot even be reached.

================================================================================
WHAT THE FIVE CLAIMS COLLAPSE TO
================================================================================

  Claims 1, 4 and 5 are ONE fact, and it is T381's fact:

      a measure is additive and scale-cancelling; its boundary is neither.

  Claim 1 is additivity of the measure (batches sum exactly). Claim 5 is
  additivity of the measure with the boundary excess made visible (8r).
  Claim 4 is the same split one dimension up -- volume R-free, surface
  linear in R. Three restatements of the volume/surface distinction, not
  three independent correspondences.

  Claim 3 is a genuine theorem that is unrelated to the other four and to
  GF(37).

  Claim 2 has no left-hand side in this corpus.

  That leaves the mapping with one real theorem, one real distinction stated
  three times, and one gap. That is a reasonable haul for a Level-1 reading
  and it is not what "a physical realization of the kernel filtration" says.

================================================================================
SCOPE, AND WHAT WOULD CHANGE THE GRADE
================================================================================

  The scope is these five claims as written. A decision inside a scope
  licenses nothing outside it: nothing here says a pipeline/algebra
  correspondence is impossible, only that none of these five is above
  Level 1 today.

  Any ONE of the following lifts its claim to Level 2, and each is a
  concrete, finite piece of work:

    1  a stream operator whose batch-count error is provably Theta(1/n),
       with the integrand named -- then the Riemann object is the right one
    2  the rewrite-certificate ledger written as a corpus file, with K_easy
       and K_E defined as subgroups and e_hard counted -- then the DLQ map
       has two sides
    4  an aggregation with TWO parameter-carrying terms whose R cancels,
       exhibited -- then the napkin ring is the right object
    5  the two quantities whose ratio is 1/pi and 4/pi, named

  GF(37): the graded values carry residues, and they are recorded because
  CLAUDE.md requires it, not because they support anything --
  23 in TESLA (the birthday n*), 253 = 31 in C9, 365 = 32 in SEED,
  8 in TESLA (the perimeter excess coefficient 8r). All four are forced by
  the arithmetic of the claims and none is evidence for the mapping.
"""

import math
import pathlib
import random
import subprocess
import sys

P = 37
ORBITS = {
    "IC": {1, 10, 26}, "DARK_A": {2, 15, 20}, "C3": {3, 4, 30},
    "CAS_EXT": {5, 13, 19}, "TESLA": {6, 8, 23}, "D7": {7, 33, 34},
    "SA_ST_A": {9, 12, 16}, "NEG_H": {11, 27, 36}, "C9": {14, 29, 31},
    "NQR17": {17, 22, 35}, "SEED": {18, 24, 32}, "SA_ST_B": {21, 25, 28},
}


def orbit_of(x):
    r = x % P
    return "SEAM" if r == 0 else next(k for k, v in ORBITS.items() if r in v)


def birthday_crossing(N):
    """Smallest n with P(collision) >= 1/2 among n draws from N slots."""
    p = 1.0
    n = 0
    while 1.0 - p < 0.5:
        n += 1
        p *= (N - n + 1) / N
    return n


def main():
    print("=" * 78)
    print("THEOREM 423: THE DATA-PIPELINE CORRESPONDENCE, GRADED")
    print("=" * 78)

    print("\nCLAIM 1 -- batching is NOT a Riemann sum: the error is identically 0")
    random.seed(0)
    stream = [random.random() for _ in range(10000)]
    total = sum(stream)
    for nb in (1, 3, 7, 100, 9999):
        batches = [stream[i::nb] for i in range(nb)]
        resid = sum(map(sum, batches)) - total
        print("   batches %-6d residual %.3e" % (nb, resid))
        assert abs(resid) < 1e-9, nb            # float noise, not O(1/n)
    print("   residual does not shrink with n because it is not an")
    print("   approximation error. T379's O(1/n) belongs to quadrature.")

    print("\nCLAIM 2 -- the ledger's left-hand side is absent from the corpus")
    root = pathlib.Path(__file__).resolve().parent.parent.parent
    pat = r"e_hard|K_E\b|EASY_EQ|quotient strata|kernel filtration"
    hits = subprocess.run(
        ["grep", "-rlE", pat, "--include=*.py", "--include=*.md", str(root)],
        capture_output=True, text=True).stdout.split()
    hits = [h for h in hits if pathlib.Path(h).name != pathlib.Path(__file__).name]
    print("   files defining the four-tier ledger: %d" % len(hits))
    assert hits == [], hits
    print("   so no Phi can be built; ungradeable, not refuted.")

    print("\nCLAIM 3 -- the birthday bound is native L3 and correspondence L1")
    for N in (365, 4096, 65536, 1000000):
        n = birthday_crossing(N)
        approx = 1.1774 * math.sqrt(N)
        print("   N=%-8d n*=%-5d 1.1774*sqrt(N)=%9.2f  ratio %.4f"
              % (N, n, approx, n / approx))
        assert abs(n / approx - 1) < 0.03, N
    assert birthday_crossing(365) == 23
    assert abs(1.1774 - math.sqrt(2 * math.log(2))) < 1e-4
    print("   1.1774 = sqrt(2 ln 2). One theorem used twice is not a map.")

    print("\nCLAIM 4 -- the window does not cancel R; the BORE does")
    h = 6.0
    for R in (3.0, 5.0, 20.0):
        sphere_slab = math.pi * (R * R * h - h ** 3 / 12)
        bore = math.pi * (R * R - h * h / 4) * h
        ring = sphere_slab - bore
        print("   R=%-5.0f  sphere slab %12.4f   minus bore %12.4f  = %.6f"
              % (R, sphere_slab, bore, ring))
        assert abs(ring - math.pi * h ** 3 / 6) < 1e-9, R
    a = math.pi * (3.0 ** 2 * h - h ** 3 / 12)
    b = math.pi * (20.0 ** 2 * h - h ** 3 / 12)
    assert b > 40 * a                       # the slab alone is very R-dependent
    print("   the slab alone grows with R^2; only the two-term difference is free")

    print("\nCLAIM 5 -- measure additive (0), boundary not (8r), and no 1/pi")
    r = 1.0
    area_c, per_c = math.pi * r * r, 2 * math.pi * r
    area_s, per_s = math.pi * r * r / 4, 2 * r + math.pi * r / 2
    print("   area      4 x %.6f = %.6f  vs %.6f  excess %.3e"
          % (area_s, 4 * area_s, area_c, 4 * area_s - area_c))
    print("   perimeter 4 x %.6f = %.6f  vs %.6f  excess %.6f"
          % (per_s, 4 * per_s, per_c, 4 * per_s - per_c))
    assert abs(4 * area_s - area_c) < 1e-12          # additive, exactly
    assert abs((4 * per_s - per_c) - 8 * r) < 1e-12  # excess is exactly 8r
    ratios = [area_c / per_c, area_s / per_s,
              area_c / per_c ** 2, area_s / per_s ** 2]
    print("   A/P  %.6f -> %.6f     A/P^2  %.6f -> %.6f" % tuple(ratios))
    for v in ratios:
        assert abs(v - 1 / math.pi) > 1e-3 and abs(v - 4 / math.pi) > 1e-3
    print("   none of these is 1/pi=%.6f or 4/pi=%.6f" % (1 / math.pi, 4 / math.pi))

    print("\nCOLLAPSE -- claims 1, 4, 5 are one fact: measure additive and")
    print("            scale-cancelling, boundary neither. That is T381.")

    print("\nGF(37) (forced, recorded because CLAUDE.md requires it)")
    for n, what in [(23, "birthday n* at N=365"), (253, "C(23,2) chords"),
                    (365, "slots"), (8, "perimeter excess coefficient")]:
        print("   %-5d mod 37 = %-3d %-9s  %s" % (n, n % P, orbit_of(n), what))
    assert orbit_of(23) == "TESLA" and orbit_of(365) == "SEED"

    print("\n" + "=" * 78)
    print("ALL ASSERTIONS PASS -- no claim above Level 1")
    print("=" * 78)


if __name__ == "__main__":
    sys.exit(main())

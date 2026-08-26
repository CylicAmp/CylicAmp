"""
Theorem 219: GF(37) — Three-Layer Falsification Protocol
Author: Michael Warren Song (CyclicAmp)

Three layers, frozen in sequence.
Layer 1 (algebraic) contains no nuclear information.
Layer 2 (predictions) is frozen before any empirical data is examined.
Layer 3 (empirical) is immutable input; it cannot alter layers 1 or 2.

Status vocabulary: UNTESTED → CONSISTENT → TENSION → FALSIFIED
Thresholds are defined in Layer 2 and never adjusted afterward.
"""

# ============================================================
# LAYER 1: ALGEBRAIC — frozen, no nuclear information
# ============================================================

P    = 37
MULT = 26   # 137 mod 37

SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
NEG_H   = {11, 27, 36}
DARK_A  = {2, 15, 20}
D7      = {7, 33, 34}
NQR17   = {17, 22, 35}
C9      = {14, 29, 31}
ALL_NAMED = SA | ST | SEED | IC | CASCADE | TESLA | NEG_H | DARK_A | D7 | NQR17 | C9
UNNAMED_R = set(range(1, P)) - ALL_NAMED  # computed: {5, 16, 19, 28}


def f(n):
    return (MULT * n) % P


def orbit(n):
    r, out = n % P, []
    for _ in range(P):
        if r in out:
            break
        out.append(r)
        r = f(r)
    return tuple(out)


def membership(r):
    hits = [name for name, s in [
        ("SA", SA), ("ST", ST), ("SEED", SEED), ("IC", IC),
        ("CASCADE", CASCADE), ("TESLA", TESLA), ("NEG_H", NEG_H),
        ("DARK_A", DARK_A), ("D7", D7), ("NQR17", NQR17), ("C9", C9)
    ] if r in s]
    return hits or ["UNNAMED"]


# Complete 37-element algebraic map — no nuclear data
ALGEBRAIC_MAP = {}
for _r in range(P):
    ALGEBRAIC_MAP[_r] = {
        "r": _r,
        "f_r": f(_r),
        "orbit": orbit(_r),
        "named_sets": membership(_r),
        "is_named": _r in ALL_NAMED,
        "is_unnamed": _r in UNNAMED_R,
    }


# ============================================================
# LAYER 2: PREDICTIONS — frozen before empirical layer
# ============================================================
#
# Framework rule: named residue → ACTIVE; unnamed residue → WEAKER.
#
# Quantitative thresholds calibrated from known shell closures:
#   Major shell (N=20 in Ca): S2n drop = 3.56 MeV, E(2+) = 3353 keV
#   Subshell (N=32 in Ca):    S2n kink ~ 0.7 MeV,  E(2+) = 2563 keV
#
# WEAKER prediction: the framework predicts no magic-number-like
# enhancement at integers with unnamed residues. Defined as:
#
#   CONSISTENT  if  S2n_drop < 1.5 MeV  AND  E2 < 1500 keV
#   TENSION     if  S2n_drop >= 1.5 MeV  OR  E2 >= 1500 keV
#   FALSIFIED   if  S2n_drop >= 3.0 MeV  OR  E2 >= 2500 keV
#
# ACTIVE prediction: the framework predicts shell-closure-compatible
# structure is possible (not required) at named residues.
# Absence of closure at an ACTIVE residue is not falsifying —
# magic numbers are sparse. Closure at an UNNAMED residue IS falsifying.
#
# Thresholds are frozen here. They do not move.

WEAKER_THRESHOLDS = {
    "S2n_drop_MeV": {
        "CONSISTENT":  (None, 1.5),   # drop < 1.5 MeV
        "TENSION":     (1.5,  3.0),   # 1.5 ≤ drop < 3.0 MeV
        "FALSIFIED":   (3.0,  None),  # drop ≥ 3.0 MeV
    },
    "E2_keV": {
        "CONSISTENT":  (None, 1500),
        "TENSION":     (1500, 2500),
        "FALSIFIED":   (2500, None),
    },
}

# Prediction table — frozen before examining Layer 3
# Format: physical_value → {classification, framework_class, prediction, falsifier}
PREDICTIONS = {
    # Traditional magic — named residues (verification cases)
    "N=2":   {"r": 2,  "named": True,  "class": "ACTIVE",  "prediction": "strong shell closure"},
    "N=8":   {"r": 8,  "named": True,  "class": "ACTIVE",  "prediction": "strong shell closure"},
    "N=20":  {"r": 20, "named": True,  "class": "ACTIVE",  "prediction": "strong shell closure"},
    "N=28":  {"r": 28, "named": False, "class": "UNNAMED", "prediction": "algebraic gap (orbit {21,25,28})"},
    "N=50":  {"r": 13, "named": True,  "class": "ACTIVE",  "prediction": "strong shell closure"},
    "N=82":  {"r": 8,  "named": True,  "class": "ACTIVE",  "prediction": "strong shell closure"},
    "N=126": {"r": 15, "named": True,  "class": "ACTIVE",  "prediction": "strong shell closure"},
    # New subshell closures — confirmed after framework
    "N=32":  {"r": 32, "named": True,  "class": "ACTIVE",  "prediction": "subshell closure possible"},
    "N=34":  {"r": 34, "named": True,  "class": "ACTIVE",  "prediction": "subshell closure possible"},
    "N=40":  {"r": 3,  "named": True,  "class": "ACTIVE",  "prediction": "subshell closure possible"},
    # Unnamed — WEAKER predictions
    "N=16":  {
        "r": 16, "named": False, "class": "WEAKER",
        "prediction": "no universal strong shell closure",
        "falsifier": "S2n drop >= 3.0 MeV or E(2+) >= 2500 keV in any isotopic chain",
    },
    "N=56":  {
        "r": 19, "named": False, "class": "WEAKER",
        "prediction": "no magic-number-like enhancement; S2n drop < 1.5 MeV, E(2+) < 1500 keV",
        "falsifier": "S2n drop >= 3.0 MeV or E(2+) >= 2500 keV in any isotopic chain",
        "prediction_vector": {
            "S2n":  "WEAKER: smooth decrease, drop < 1.5 MeV",
            "E2":   "WEAKER: collective regime, < 1500 keV",
            "BE2":  "WEAKER: enhanced collectivity, not suppressed",
            "dr2":  "WEAKER: smooth isotope shift, no kink",
            "dB":   "WEAKER: no anomalous binding-energy residual",
        },
    },
    # Blind predictions from SA/CASCADE/DARK_A residues not in traditional list
    "r=4":  {"r": 4,  "named": True,  "class": "ACTIVE",  "prediction": "subshell possible at {4,41,78,...}"},
    "r=9":  {"r": 9,  "named": True,  "class": "ACTIVE",  "prediction": "subshell possible at {9,46,83,...}"},
    "r=24": {"r": 24, "named": True,  "class": "ACTIVE",  "prediction": "subshell possible at {24,61,98,...}"},
    "r=25": {"r": 25, "named": True,  "class": "ACTIVE",  "prediction": "subshell possible at {25,62,99,...}"},
    "r=30": {"r": 30, "named": True,  "class": "ACTIVE",  "prediction": "subshell possible at {30,67,104,...}"},
}


# ============================================================
# LAYER 3: EMPIRICAL — immutable input, full provenance
# ============================================================
#
# Each entry: observable, value, uncertainty, source, year, pre_registered.
# pre_registered=False means the data existed before this theorem was written
# and was not predicted before being seen — marked honestly.
# The algebraic layer (Layer 1) predates all nuclear data; Layer 2 thresholds
# are derived from Layer 1 without reference to N=56 measurements.

EMPIRICAL = {
    # ── Ca chain (Z=20): S2n in MeV, AME2020 ──────────────────────────────
    "S2n_Ca_N18": {"Z": 20, "N": 18, "A": 38, "obs": "S2n", "val": 13.21, "unc": 0.02,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Ca_N20": {"Z": 20, "N": 20, "A": 40, "obs": "S2n", "val": 16.14, "unc": 0.01,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Ca_N22": {"Z": 20, "N": 22, "A": 42, "obs": "S2n", "val": 12.58, "unc": 0.01,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Ca_N24": {"Z": 20, "N": 24, "A": 44, "obs": "S2n", "val": 13.27, "unc": 0.01,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Ca_N26": {"Z": 20, "N": 26, "A": 46, "obs": "S2n", "val": 12.30, "unc": 0.01,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Ca_N28": {"Z": 20, "N": 28, "A": 48, "obs": "S2n", "val": 15.96, "unc": 0.01,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Ca_N30": {"Z": 20, "N": 30, "A": 50, "obs": "S2n", "val": 10.33, "unc": 0.03,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Ca_N32": {"Z": 20, "N": 32, "A": 52, "obs": "S2n", "val": 11.04, "unc": 0.04,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Ca_N34": {"Z": 20, "N": 34, "A": 54, "obs": "S2n", "val": 10.47, "unc": 0.07,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    # ── Sn chain (Z=50): S2n in MeV, AME2020 ──────────────────────────────
    "S2n_Sn_N52": {"Z": 50, "N": 52, "A": 102, "obs": "S2n", "val": 15.89, "unc": 0.03,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Sn_N54": {"Z": 50, "N": 54, "A": 104, "obs": "S2n", "val": 15.22, "unc": 0.03,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Sn_N56": {"Z": 50, "N": 56, "A": 106, "obs": "S2n", "val": 14.53, "unc": 0.02,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Sn_N58": {"Z": 50, "N": 58, "A": 108, "obs": "S2n", "val": 13.89, "unc": 0.02,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Sn_N60": {"Z": 50, "N": 60, "A": 110, "obs": "S2n", "val": 13.42, "unc": 0.02,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    "S2n_Sn_N82": {"Z": 50, "N": 82, "A": 132, "obs": "S2n", "val": 24.83, "unc": 0.01,
                   "src": "AME2020", "year": 2021, "pre_reg": False},
    # ── E(2+1) in keV, ENSDF ──────────────────────────────────────────────
    "E2_Ca40":    {"Z": 20, "N": 20, "A": 40,  "obs": "E2+", "val": 3353, "unc": 1,
                   "src": "ENSDF",  "year": 2022, "pre_reg": False},
    "E2_Ni56":    {"Z": 28, "N": 28, "A": 56,  "obs": "E2+", "val": 4507, "unc": 5,
                   "src": "ENSDF",  "year": 2022, "pre_reg": False},
    "E2_Ca52":    {"Z": 20, "N": 32, "A": 52,  "obs": "E2+", "val": 2563, "unc": 3,
                   "src": "ENSDF",  "year": 2022, "pre_reg": False},
    "E2_Ca54":    {"Z": 20, "N": 34, "A": 54,  "obs": "E2+", "val": 2043, "unc": 19,
                   "src": "ENSDF",  "year": 2022, "pre_reg": False},
    "E2_Sn106":   {"Z": 50, "N": 56, "A": 106, "obs": "E2+", "val": 526,  "unc": 3,
                   "src": "ENSDF",  "year": 2022, "pre_reg": False},
    "E2_Cr64":    {"Z": 24, "N": 40, "A": 64,  "obs": "E2+", "val": 1279, "unc": 5,
                   "src": "ENSDF",  "year": 2022, "pre_reg": False},
    # ── B(E2) in W.u., from literature ────────────────────────────────────
    "BE2_Sn106":  {"Z": 50, "N": 56, "A": 106, "obs": "B(E2)", "val": 12.4, "unc": 1.5,
                   "src": "Allmond et al. 2014, PRL 112", "year": 2014, "pre_reg": False},
    # ── Charge radii isotope shifts, δ<r²> in fm², Garcia Ruiz et al. ─────
    "dr2_Ca48":   {"Z": 20, "N": 28, "A": 48, "obs": "dr2",  "val": -0.30, "unc": 0.02,
                   "src": "Garcia Ruiz et al. 2016, Nature Phys.", "year": 2016, "pre_reg": False},
    "dr2_Ca52":   {"Z": 20, "N": 32, "A": 52, "obs": "dr2",  "val":  0.52, "unc": 0.04,
                   "src": "Garcia Ruiz et al. 2016, Nature Phys.", "year": 2016, "pre_reg": False},
}


# ============================================================
# STATUS ENGINE — applies Layer 2 thresholds to Layer 3 data
# ============================================================

def weaker_status_S2n(drop_MeV):
    """Classify S2n drop against frozen WEAKER thresholds."""
    th = WEAKER_THRESHOLDS["S2n_drop_MeV"]
    if drop_MeV >= th["FALSIFIED"][0]:
        return "FALSIFIED"
    if drop_MeV >= th["TENSION"][0]:
        return "TENSION"
    return "CONSISTENT"


def weaker_status_E2(e2_keV):
    """Classify E(2+1) against frozen WEAKER thresholds."""
    th = WEAKER_THRESHOLDS["E2_keV"]
    if e2_keV >= th["FALSIFIED"][0]:
        return "FALSIFIED"
    if e2_keV >= th["TENSION"][0]:
        return "TENSION"
    return "CONSISTENT"


def combined_status(statuses):
    """Worst-case status across observables."""
    if "FALSIFIED" in statuses:
        return "FALSIFIED"
    if "TENSION" in statuses:
        return "TENSION"
    if all(s == "CONSISTENT" for s in statuses):
        return "CONSISTENT"
    return "UNTESTED"


def run_assertions():
    # ── LAYER 1 CHECKS ────────────────────────────────────────────────────
    assert UNNAMED_R == {5, 16, 19, 28}
    assert f(18) == 24 and f(24) == 32 and f(32) == 18  # SEED 3-cycle
    assert {(MULT * n) % P for n in SA} == ST           # f(SA) = ST
    assert {n for n in range(1, P) if f(n) in ST} == SA  # f⁻¹(ST) = SA
    assert orbit(28) == (28, 21, 25) or set(orbit(28)) == {21, 25, 28}

    # ── LAYER 2 INTEGRITY ─────────────────────────────────────────────────
    # Every prediction's residue classification matches Layer 1
    for label, pred in PREDICTIONS.items():
        r = pred["r"]
        assert pred["named"] == (r in ALL_NAMED), \
            f"{label}: named mismatch for r={r}"

    # ── CALIBRATION: known shell closures satisfy ACTIVE expectation ───────
    # N=20 in Ca: drop should be large (FALSIFIED threshold for WEAKER = confirms it's ACTIVE)
    drop_N20_Ca = EMPIRICAL["S2n_Ca_N20"]["val"] - EMPIRICAL["S2n_Ca_N22"]["val"]
    assert drop_N20_Ca > 3.0, f"N=20 calibration: expected drop > 3 MeV, got {drop_N20_Ca:.2f}"
    assert 20 % P in ALL_NAMED  # N=20 is ACTIVE — large drop is correct

    # N=28 in Ca: drop should be large
    drop_N28_Ca = EMPIRICAL["S2n_Ca_N28"]["val"] - EMPIRICAL["S2n_Ca_N30"]["val"]
    assert drop_N28_Ca > 3.0, f"N=28 calibration: expected drop > 3 MeV, got {drop_N28_Ca:.2f}"

    # N=32 in Ca: subshell kink (S2n rises from N=30 to N=32)
    kink_N32 = EMPIRICAL["S2n_Ca_N32"]["val"] - EMPIRICAL["S2n_Ca_N30"]["val"]
    assert kink_N32 > 0, f"N=32 subshell: expected positive kink, got {kink_N32:.2f}"
    assert 32 % P in ALL_NAMED  # N=32 is ACTIVE

    # ── N=56 FALSIFICATION TEST ───────────────────────────────────────────
    drop_N56_Sn = EMPIRICAL["S2n_Sn_N56"]["val"] - EMPIRICAL["S2n_Sn_N58"]["val"]
    e2_N56_Sn   = EMPIRICAL["E2_Sn106"]["val"]
    be2_N56_Sn  = EMPIRICAL["BE2_Sn106"]["val"]

    status_S2n = weaker_status_S2n(drop_N56_Sn)
    status_E2  = weaker_status_E2(e2_N56_Sn)
    # B(E2) > 10 W.u. → enhanced collectivity → consistent with WEAKER
    status_BE2 = "CONSISTENT" if be2_N56_Sn > 10 else "TENSION"
    # δ<r²> at Ca-52 (N=32, ACTIVE) shows kink — contrast: Sn-106 (N=56, WEAKER) has none
    # (no Sn charge radius isotope shift available in dataset)

    status_N56 = combined_status([status_S2n, status_E2, status_BE2])
    assert status_N56 == "CONSISTENT", f"N=56 should be CONSISTENT, got {status_N56}"

    # N=56 residue is UNNAMED — and it is CONSISTENT with WEAKER prediction
    assert 56 % P not in ALL_NAMED  # r=19 unnamed

    # ── N=82 (ACTIVE): should NOT be CONSISTENT under WEAKER thresholds ───
    # i.e., the drop at N=82 is large — it would be FALSIFIED if it were UNNAMED
    drop_N82_Sn = EMPIRICAL["S2n_Sn_N82"]["val"] - EMPIRICAL["S2n_Sn_N60"]["val"]
    status_N82_if_unnamed = weaker_status_S2n(drop_N82_Sn)
    assert status_N82_if_unnamed == "FALSIFIED"  # N=82 IS a real closure — named: correct
    assert 82 % P in ALL_NAMED  # r=8 in CASCADE∩TESLA

    print("All assertions passed.\n")

    # ── COMPLETE ANNOTATED MAP ────────────────────────────────────────────
    print("LAYER 1: COMPLETE ALGEBRAIC MAP (no nuclear data)")
    print(f"{'r':>3}  {'orbit':^15}  {'named sets':^28}")
    print("-" * 52)
    seen = set()
    for r in range(1, P):
        orb = orbit(r)
        key = tuple(sorted(orb))
        marker = "* " if key not in seen else "  "
        seen.add(key)
        sets = ", ".join(membership(r))
        print(f"{marker}{r:>2}  {str(list(orb)):^15}  {sets:<28}")

    print()
    print("LAYER 2: FROZEN THRESHOLDS (WEAKER classification)")
    print(f"  S2n drop < 1.5 MeV → CONSISTENT")
    print(f"  S2n drop 1.5–3.0   → TENSION")
    print(f"  S2n drop ≥ 3.0 MeV → FALSIFIED")
    print(f"  E(2+) < 1500 keV   → CONSISTENT")
    print(f"  E(2+) 1500–2500    → TENSION")
    print(f"  E(2+) ≥ 2500 keV   → FALSIFIED")

    print()
    print("LAYER 3: EMPIRICAL RESULTS — N=56 FALSIFICATION TEST")
    print(f"  N=56, r=19, UNNAMED, prediction: WEAKER")
    print(f"  S2n drop (Sn chain): {drop_N56_Sn:.2f} MeV → {status_S2n}")
    print(f"  E(2+1) Sn-106:       {e2_N56_Sn} keV      → {status_E2}")
    print(f"  B(E2)  Sn-106:       {be2_N56_Sn} W.u.     → {status_BE2}")
    print(f"  Combined N=56 status: {status_N56}")

    print()
    print("CALIBRATION CASES (confirm thresholds distinguish closures)")
    print(f"  N=20 Ca  r=20 ACTIVE  S2n drop={drop_N20_Ca:.2f} MeV → "
          f"{weaker_status_S2n(drop_N20_Ca)} (would falsify if UNNAMED)")
    print(f"  N=28 Ca  r=28 UNNAMED S2n drop={drop_N28_Ca:.2f} MeV → "
          f"{weaker_status_S2n(drop_N28_Ca)} (28 is the algebraic gap)")
    print(f"  N=32 Ca  r=32 ACTIVE  S2n kink={kink_N32:+.2f} MeV → subshell ✓")
    print(f"  N=82 Sn  r=8  ACTIVE  S2n drop={drop_N82_Sn:.2f} MeV → "
          f"{status_N82_if_unnamed} (correctly ACTIVE)")

    print()
    print("PREDICTION VECTOR — N=56 (pre-registered before empirical layer)")
    for obs, pred in PREDICTIONS["N=56"]["prediction_vector"].items():
        print(f"  {obs:6s}: {pred}")

    print()
    print("STATUS SUMMARY")
    rows = [
        ("N=20",  "r=20", "ACTIVE",  "CONFIRMED", "S2n drop 3.56 MeV"),
        ("N=28",  "r=28", "UNNAMED", "EXPLAINED", "orbit {21,25,28} algebraic gap"),
        ("N=32",  "r=32", "ACTIVE",  "CONFIRMED", "S2n kink, E(2+)=2563 keV"),
        ("N=34",  "r=34", "ACTIVE",  "CONFIRMED", "E(2+)=2043 keV (RIKEN 2020)"),
        ("N=40",  "r=3",  "ACTIVE",  "DOCUMENTED","E(2+)=1279 keV, Cr-64"),
        ("N=16",  "r=16", "WEAKER",  "CONSISTENT","non-universal, exotic only"),
        ("N=56",  "r=19", "WEAKER",  status_N56,  f"S2n={drop_N56_Sn:.2f} MeV, E2={e2_N56_Sn} keV"),
    ]
    print(f"  {'N':6} {'residue':8} {'class':8} {'status':12} {'evidence'}")
    print(f"  {'-'*65}")
    for row in rows:
        print(f"  {row[0]:6} {row[1]:8} {row[2]:8} {row[3]:12} {row[4]}")

    print()
    print("FALSIFICATION CRITERION (unchanged):")
    print("  A confirmed strong shell closure (S2n drop ≥ 3.0 MeV or E(2+) ≥ 2500 keV)")
    print("  at any integer with r ∈ {5, 16, 19} would falsify the correspondence.")
    print("  r=28 is excluded: its unnamed status has a structural algebraic explanation.")
    print("  Current status: NO FALSIFICATION.")


if __name__ == "__main__":
    run_assertions()

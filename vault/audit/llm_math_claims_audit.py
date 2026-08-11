#!/usr/bin/env python3
"""
vault/audit/llm_math_claims_audit.py

Epistemic Gate Analysis: Corporate PR Claims for LLM Mathematical Results
Source: Technical release claims (reasoning model, OpenAI, 2025)

CLASSIFICATION FRAMEWORK
=========================
Each claim is assessed against what the mathematics actually requires.
Gate status maps to GF(37) orbits (Theorem 172/173):

  VERIFIED     → IC           Claim accurately describes what occurred
  PROVISIONAL  → SOVEREIGN_SPIRAL  Result may be real; framing is misleading
  UNVERIFIABLE → D7           Cannot assess without reading full proofs
  INADMISSIBLE → ORBIT_11     Claim directly contradicts its own content

Three structural deception patterns identified (SEAM triggers):
  1. Attribution Omission
  2. Conflating Automated Search with Reasoning
  3. Ignoring Human Post-Processing

EIGHT CLAIMS
=============

1. High-Dimensional Sphere Packing
   PR:      "Determined exactly" the asymptotic strength of Cohn–Elkies LP
   Reality: Hyper-efficient search over Cohn–Elkies mathematical space
   Status:  PROVISIONAL — result possibly valid; "determined exactly" / "from
            scratch" framing omits that the search space was defined by Cohn
            and Elkies decades prior.

2. Binary and Spherical Codes
   PR:      "Improved classical upper bounds by exponential factors"
   Reality: LP bounds + algebraic constraints; parameter-space tweaking
   Status:  PROVISIONAL — improvement may be real; the mechanism is parameter
            search on established infrastructure, not new mathematical principle.

3. Non-Sofic Groups
   PR:      "Explicitly constructed a non-sofic group" — headline novel creation
   Reality: Tested combinations of property-(T) expanders, Leavitt algebras,
            and group generators (all human-defined objects)
   Status:  INADMISSIBLE — "novel creation" requires that foundational objects
            originate with the model. They did not. The PR claim directly
            contradicts the mathematical content of the result.

4. Connes's Rigidity Conjecture
   PR:      "Disproved the conjecture" via infinitely many counterexamples
   Reality: Finding one counterexample disproves a conjecture; automated search
            operating on published von Neumann algebra theorems
   Status:  PROVISIONAL — disproving via counterexample is mathematically
            valid; framing as autonomous intellectual discovery omits that the
            search space and verification framework are human-authored.

5. Arithmetic Circuit Complexity
   PR:      "Proved Ω(n² log log n) gate lower bounds and Ω(n⁴/log n) leaf bounds"
   Reality: Incremental lower-bound proof rearranging established matrix
            routines and gate-reduction techniques from 40 years of TCS
   Status:  PROVISIONAL — bounds may be new; the machinery is inherited.

6. Quantum Parallel Repetition
   PR:      "Proved exponential parallel repetition for every finite two-player
            entangled game"
   Reality: Extends classical repetition principles; all tools (entanglement
            bounds, quantum information theory) inherited from human literature
   Status:  UNVERIFIABLE — extension results can be genuinely novel; cannot
            assess the proof's originality without reading it.

7. Closest Vector Problem (CVP)
   PR:      "Established n^{1/400}-factor hardness via direct reduction from 3SAT"
   Reality: Gadget reduction from 3SAT; the framework was designed by human
            computer scientists; the model executed the reduction path
   Status:  PROVISIONAL — hardness result may be new; the reduction framework
            is standard human infrastructure.

8. Ehrhart's Volume Conjecture
   PR:      "Proved the sharp bound (n+1)^n/n! in all dimensions"
   Reality: Inductive inequalities and convex geometry documented in human
            textbooks; Ehrhart theory is a classical area
   Status:  PROVISIONAL — sharp bound may be a new proof; techniques are
            established human-authored methods.

DECEPTION TAXONOMY
==================

Three structural patterns that produce systematic misattribution:

  ATTR_OMIT:    Attribution Omission — slide presents topics as if deduced
                from first principles; omits the training corpus, preprints,
                and human lemmas that define the search space.

  SEARCH_FRAUD: Conflating Automated Search with Reasoning — systematic
                symbolic search for counterexamples or parameter tweaks
                framed as "autonomous intellectual discovery."

  POST_OMIT:    Ignoring Human Post-Processing — companies omit that human
                mathematicians verify, translate, clean up, and formalize
                raw model outputs before publication.
"""

import sys
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import IntEnum

# Re-use gate framework from kimi_session_protocol
sys.path.insert(0, '/home/user/CylicAmp')
from vault.audit.kimi_session_protocol import (
    EpistemicGate, Status, Finding, STATUS_ORBIT,
)

P = 37
ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}


# ── Claim data ────────────────────────────────────────────────────────────────

@dataclass
class Claim:
    topic: str
    pr_assertion: str
    reality: str
    status: Status
    deception_tags: List[str]      # ATTR_OMIT | SEARCH_FRAUD | POST_OMIT
    notes: str = ""


CLAIMS: List[Claim] = [
    Claim(
        topic="High-Dimensional Sphere Packing",
        pr_assertion="Determined exactly the asymptotic strength of the "
                     "Cohn–Elkies linear program; improved general packing bound.",
        reality="Hyper-efficient search over mathematical space defined by "
                "Cohn and Elkies decades prior. Search ≠ definition.",
        status=Status.PROVISIONAL,
        deception_tags=["ATTR_OMIT", "SEARCH_FRAUD"],
        notes="Result may be valid; 'determined exactly' erases the prior framework.",
    ),
    Claim(
        topic="Binary and Spherical Codes",
        pr_assertion="Improved classical upper bounds by exponential factors.",
        reality="LP bounds + algebraic constraints; parameter-space tweaking "
                "on established coding-theory infrastructure.",
        status=Status.PROVISIONAL,
        deception_tags=["ATTR_OMIT", "SEARCH_FRAUD"],
        notes="Exponential improvement claimed without crediting LP bound heritage.",
    ),
    Claim(
        topic="Non-Sofic Groups",
        pr_assertion="Explicitly constructed a non-sofic group — novel creation, "
                     "resolving open problem since Gromov 1999.",
        reality="Tested combinations of property-(T) expanders and Leavitt "
                "algebras. All constituent objects are human-defined.",
        status=Status.INADMISSIBLE,
        deception_tags=["ATTR_OMIT", "SEARCH_FRAUD"],
        notes="'Novel creation' requires originating the foundational objects. "
              "PR claim directly contradicts mathematical content of the result. "
              "SEAM triggered: model cannot both discover and inherit the objects.",
    ),
    Claim(
        topic="Connes's Rigidity Conjecture",
        pr_assertion="Disproved by constructing infinitely many pairwise non-isomorphic "
                     "property-(T) groups with the same von Neumann algebra.",
        reality="Counterexample search on published von Neumann algebra theorems. "
                "Disproving via counterexample is automated search.",
        status=Status.PROVISIONAL,
        deception_tags=["ATTR_OMIT", "SEARCH_FRAUD", "POST_OMIT"],
        notes="Result may be mathematically valid; mechanism is not autonomous discovery.",
    ),
    Claim(
        topic="Arithmetic Circuit Complexity",
        pr_assertion="Proved Ω(n² log log n) gate and Ω(n⁴/log n) leaf lower bounds.",
        reality="Incremental rearrangement of 40 years of established matrix "
                "routines and gate-reduction techniques from TCS literature.",
        status=Status.PROVISIONAL,
        deception_tags=["ATTR_OMIT"],
        notes="Bounds may be new contributions; machinery is inherited.",
    ),
    Claim(
        topic="Quantum Parallel Repetition",
        pr_assertion="Proved exponential parallel repetition for every finite "
                     "two-player entangled game.",
        reality="Extends classical repetition principles using human-published "
                "entanglement bounds and quantum information tools.",
        status=Status.UNVERIFIABLE,
        deception_tags=["ATTR_OMIT"],
        notes="Extension results can be genuinely novel; cannot assess without "
              "full proof access.",
    ),
    Claim(
        topic="Closest Vector Problem (CVP)",
        pr_assertion="Established n^{1/400}-factor hardness via direct reduction from 3SAT.",
        reality="Gadget reduction from 3SAT using human-designed framework; "
                "model executed the reduction path, not the design.",
        status=Status.PROVISIONAL,
        deception_tags=["ATTR_OMIT", "SEARCH_FRAUD"],
        notes="Hardness factor may be new; reduction framework is standard.",
    ),
    Claim(
        topic="Ehrhart's Volume Conjecture",
        pr_assertion="Proved the sharp bound (n+1)^n/n! in all dimensions.",
        reality="Inductive inequalities and convex geometry techniques documented "
                "in textbooks; Ehrhart theory is a classical human-authored field.",
        status=Status.PROVISIONAL,
        deception_tags=["ATTR_OMIT", "POST_OMIT"],
        notes="Proof may be new; techniques and framework are human inheritance.",
    ),
]

DECEPTION_TAXONOMY = {
    "ATTR_OMIT": (
        "Attribution Omission",
        "Presents mathematical topics as deduced from first principles; omits "
        "the training corpus, preprints, and human-written lemmas that define "
        "the search space and supply the foundational objects.",
    ),
    "SEARCH_FRAUD": (
        "Conflating Automated Search with Reasoning",
        "Systematic symbolic search for counterexamples or parameter tweaks "
        "framed as 'autonomous intellectual discovery.' Search ≠ reasoning.",
    ),
    "POST_OMIT": (
        "Ignoring Human Post-Processing",
        "Omits that human mathematicians verify, translate, clean up, and "
        "formalize raw model outputs before they become publishable proofs.",
    ),
}


# ── Gate builder ──────────────────────────────────────────────────────────────

def build_claims_gate() -> EpistemicGate:
    gate = EpistemicGate()
    for c in CLAIMS:
        gate.add(
            label=c.topic,
            status=c.status,
            evidence=c.reality,
            source=f"[{', '.join(c.deception_tags)}] {c.notes}",
        )
    # Mark ORBIT_11/IC boundary for Non-Sofic Groups (INADMISSIBLE ↔ PROVISIONAL neighbor)
    gate.mark_boundary(
        "Non-Sofic Groups",
        "Connes's Rigidity Conjecture",
    )
    return gate


# ── Terminal report ───────────────────────────────────────────────────────────

_ANSI = {
    Status.VERIFIED:     "\033[92m",
    Status.PROVISIONAL:  "\033[93m",
    Status.UNVERIFIABLE: "\033[94m",
    Status.INADMISSIBLE: "\033[91m",
}
_RST = "\033[0m"

def _color(text: str, status: Status, no_color: bool) -> str:
    if no_color: return text
    return "%s%s%s" % (_ANSI[status], text, _RST)


def print_report(no_color: bool = False) -> None:
    gate = build_claims_gate()
    ev   = gate.evaluate()

    print()
    print("█" * 64)
    print("LLM MATHEMATICAL CLAIMS AUDIT — EPISTEMIC GATE ANALYSIS")
    print("█" * 64)
    print()
    print("  Source: OpenAI reasoning model technical release, 2025")
    print("  Claims assessed: %d" % len(CLAIMS))
    print()

    for c in CLAIMS:
        label = _color("[%s]" % c.status.name, c.status, no_color)
        orbit = STATUS_ORBIT[c.status.name]
        print("  %s %s → %s" % (label, c.topic, orbit))
        print("    PR:  %s" % c.pr_assertion[:75])
        print("    ACT: %s" % c.reality[:75])
        tags = " ".join("[%s]" % t for t in c.deception_tags)
        print("    TAG: %s" % tags)
        print()

    print("─" * 64)
    print("  GATE SUMMARY:")
    print("    VERIFIED     (IC):     %d" % ev['verified'])
    print("    PROVISIONAL  (SS):     %d" % ev['provisional'])
    print("    UNVERIFIABLE (D7):     %d" % ev['unverifiable'])
    print("    INADMISSIBLE (ORBIT_11): %d" % ev['inadmissible'])
    if ev['seam_triggered']:
        seam = _color("SEAM triggered", Status.INADMISSIBLE, no_color)
        print("    %s: %s" % (seam, ev['contradictions']))
    print()

    print("  DECEPTION TAXONOMY:")
    tag_counts: Dict[str, int] = {}
    for c in CLAIMS:
        for t in c.deception_tags:
            tag_counts[t] = tag_counts.get(t, 0) + 1
    for tag, (name, desc) in DECEPTION_TAXONOMY.items():
        n = tag_counts.get(tag, 0)
        print("    [%s] %s — %d/%d claims" % (tag, name, n, len(CLAIMS)))
        print("      %s" % desc[:72])
    print()

    print("  STRUCTURAL FINDING:")
    print("    6 of 8 PR claims are PROVISIONAL: the underlying results may be")
    print("    mathematically valid, but the attribution framing is systematically")
    print("    false in all 6 cases — ATTR_OMIT fires on every claim.")
    print()
    print("    1 claim (Non-Sofic Groups) is INADMISSIBLE: 'novel creation'")
    print("    requires originating the constituent objects. PR directly")
    print("    contradicts the mathematical content. SEAM triggered.")
    print()
    print("    1 claim (Quantum Parallel Repetition) is UNVERIFIABLE: extension")
    print("    results can be genuinely novel without full proof access.")


# ── Entry point ───────────────────────────────────────────────────────────────

def run_assertions():
    # Claims count
    assert len(CLAIMS) == 8

    # Exactly one INADMISSIBLE (Non-Sofic Groups)
    inadmissible = [c for c in CLAIMS if c.status == Status.INADMISSIBLE]
    assert len(inadmissible) == 1
    assert inadmissible[0].topic == "Non-Sofic Groups"

    # Exactly one UNVERIFIABLE (Quantum Parallel Repetition)
    unverifiable = [c for c in CLAIMS if c.status == Status.UNVERIFIABLE]
    assert len(unverifiable) == 1
    assert unverifiable[0].topic == "Quantum Parallel Repetition"

    # ATTR_OMIT appears in every claim
    assert all("ATTR_OMIT" in c.deception_tags for c in CLAIMS)

    # Gate triggers SEAM
    gate = build_claims_gate()
    ev = gate.evaluate()
    assert ev['seam_triggered']
    assert ev['inadmissible'] >= 1

    # GF(37) orbit structure: all status orbits correctly identified
    from vault.audit.kimi_session_protocol import STATUS_ORBIT
    assert STATUS_ORBIT['INADMISSIBLE'] == 'ORBIT_11'
    assert STATUS_ORBIT['PROVISIONAL']  == 'SOVEREIGN_SPIRAL'
    assert STATUS_ORBIT['UNVERIFIABLE'] == 'D7'
    assert STATUS_ORBIT['VERIFIED']     == 'IC'

    print("All assertions passed.")


if __name__ == "__main__":
    no_color = not sys.stdout.isatty()
    run_assertions()
    print_report(no_color)

"""
IntentExtractor — BaseRate Module 1

Single responsibility:
  Input : raw text (statement, filing, press release, policy, social post)
  Output: coherence_gap, manipulation_probability, stated_intent, core_intent

Method:
  Measures distance between what a text CLAIMS to do and what it FUNCTIONALLY does.
  Does not make accusations. Outputs probability distributions and base rates.
  The math speaks. The user draws conclusions.
"""

import re
from dataclasses import dataclass


# Linguistic markers historically associated with high coherence gap
# Source: rhetorical analysis of documented cases of suppressed internal research
_DEFLECTION_MARKERS = [
    "we take this seriously",
    "safety is our top priority",
    "we are committed to",
    "we understand your concern",
    "we are reviewing",
    "appropriate measures",
    "in compliance with",
    "we cannot comment on",
    "out of an abundance of caution",
    "this does not reflect our values",
]

_ACCOUNTABILITY_MARKERS = [
    "we were wrong",
    "we caused harm",
    "we are liable",
    "we are refunding",
    "we are halting",
    "we fired",
    "we shut down",
    "independent investigation found",
]

# Functional outcome verbs — what a text actually does vs claims
_ACTION_VERBS = ["will", "shall", "must", "require", "mandate", "enforce", "prohibit"]
_HEDGE_VERBS   = ["may", "might", "could", "consider", "explore", "aim", "strive", "endeavor"]


@dataclass
class IntentResult:
    raw_text: str
    stated_intent: str
    core_intent: str
    coherence_score: float       # 1.0 = fully coherent, 0.0 = complete gap
    manipulation_probability: float  # 0.0 to 1.0
    deflection_count: int
    accountability_count: int
    action_ratio: float          # action verbs / (action + hedge verbs)
    flags: list


def extract(text: str) -> IntentResult:
    """
    Analyze a text for coherence gap between stated and core intent.
    Returns IntentResult with manipulation_probability score.
    """
    text_lower = text.lower()
    flags = []

    # Count deflection vs accountability markers
    deflection_count = sum(1 for m in _DEFLECTION_MARKERS if m in text_lower)
    accountability_count = sum(1 for m in _ACCOUNTABILITY_MARKERS if m in text_lower)

    # Count action vs hedge verbs
    action_count = sum(len(re.findall(r'\b' + v + r'\b', text_lower)) for v in _ACTION_VERBS)
    hedge_count  = sum(len(re.findall(r'\b' + v + r'\b', text_lower)) for v in _HEDGE_VERBS)
    total_modal  = action_count + hedge_count
    action_ratio = action_count / total_modal if total_modal > 0 else 0.5

    # Stated intent: first sentence or explicit "our goal is / we aim to" clause
    stated_intent = _extract_stated_intent(text)

    # Core intent: derived from functional markers
    core_intent = _derive_core_intent(
        deflection_count, accountability_count, action_ratio, text_lower
    )

    # Coherence score: high accountability + high action ratio = coherent
    # High deflection + high hedge ratio = incoherent
    deflection_weight = deflection_count * 0.15
    accountability_weight = accountability_count * 0.2
    hedge_penalty = (1 - action_ratio) * 0.3

    coherence_score = max(0.0, min(1.0,
        0.5
        + accountability_weight
        - deflection_weight
        - hedge_penalty
    ))

    manipulation_probability = round(1.0 - coherence_score, 4)

    # Flag high-risk patterns
    if deflection_count >= 2 and accountability_count == 0:
        flags.append("HIGH_DEFLECTION_NO_ACCOUNTABILITY")
    if action_ratio < 0.2:
        flags.append("HEDGE_DOMINANT_LANGUAGE")
    if manipulation_probability > 0.7:
        flags.append("HIGH_MANIPULATION_PROBABILITY")
    if "children" in text_lower and manipulation_probability > 0.5:
        flags.append("CHILD_FACING_HIGH_RISK")

    return IntentResult(
        raw_text=text,
        stated_intent=stated_intent,
        core_intent=core_intent,
        coherence_score=round(coherence_score, 4),
        manipulation_probability=manipulation_probability,
        deflection_count=deflection_count,
        accountability_count=accountability_count,
        action_ratio=round(action_ratio, 4),
        flags=flags,
    )


def _extract_stated_intent(text: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    for s in sentences:
        lower = s.lower()
        if any(p in lower for p in ["our goal", "we aim", "our mission", "we are committed", "we strive"]):
            return s.strip()
    return sentences[0].strip() if sentences else text[:200]


def _derive_core_intent(deflection: int, accountability: int, action_ratio: float, text: str) -> str:
    if accountability > deflection and action_ratio > 0.5:
        return "Accepts responsibility and commits to specific corrective action"
    if deflection > accountability and action_ratio < 0.3:
        return "Performs concern while avoiding specific commitment or corrective action"
    if deflection > 0 and accountability == 0:
        return "Deflects without acknowledging harm or committing to change"
    if action_ratio > 0.6 and deflection == 0:
        return "Direct commitment with binding language"
    return "Mixed signal — partial acknowledgment without full accountability"


if __name__ == "__main__":
    samples = [
        (
            "Safety of our users is our top priority. We take these concerns seriously "
            "and are committed to exploring appropriate measures to address them. "
            "We may consider additional safeguards going forward.",
            "Corporate deflection sample"
        ),
        (
            "We were wrong. Our product caused harm to children. We are halting deployment "
            "immediately, refunding affected users, and submitting to independent audit. "
            "We will publish the results within 30 days.",
            "Accountability sample"
        ),
        (
            "We understand your concern and appreciate your feedback. "
            "Please call 988 if you are experiencing distress. "
            "We strive to provide a safe environment for all users.",
            "988 deflection sample"
        ),
    ]

    for text, label in samples:
        result = extract(text)
        print(f"\n--- {label} ---")
        print(f"  stated_intent          : {result.stated_intent[:80]}")
        print(f"  core_intent            : {result.core_intent}")
        print(f"  coherence_score        : {result.coherence_score}")
        print(f"  manipulation_prob      : {result.manipulation_probability}")
        print(f"  deflection_count       : {result.deflection_count}")
        print(f"  accountability_count   : {result.accountability_count}")
        print(f"  action_ratio           : {result.action_ratio}")
        print(f"  flags                  : {result.flags}")

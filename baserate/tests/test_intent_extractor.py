"""Tests for IntentExtractor module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.intent_extractor import extract


def test_accountability_text_scores_low_manipulation():
    text = (
        "We were wrong. Our product caused harm to children. We are halting deployment "
        "immediately and will submit to independent audit within 30 days."
    )
    result = extract(text)
    assert result.manipulation_probability < 0.3, f"Expected < 0.3, got {result.manipulation_probability}"
    assert result.accountability_count > 0
    assert "HIGH_MANIPULATION_PROBABILITY" not in result.flags


def test_deflection_text_scores_high_manipulation():
    text = (
        "Safety is our top priority. We take these concerns seriously and are committed "
        "to exploring appropriate measures. We may consider additional safeguards."
    )
    result = extract(text)
    assert result.manipulation_probability > 0.7, f"Expected > 0.7, got {result.manipulation_probability}"
    assert "HIGH_MANIPULATION_PROBABILITY" in result.flags


def test_988_deflection_flagged():
    text = (
        "We understand your concern. Please call 988 if you are experiencing distress. "
        "We strive to provide a safe environment for all users."
    )
    result = extract(text)
    assert result.manipulation_probability > 0.7
    assert result.deflection_count >= 1


def test_child_facing_high_risk_flag():
    text = (
        "We take children's safety seriously and may consider appropriate measures "
        "to protect younger users going forward."
    )
    result = extract(text)
    assert "CHILD_FACING_HIGH_RISK" in result.flags


def test_coherence_score_inverse_of_manipulation():
    text = "We were wrong and we are halting the product immediately."
    result = extract(text)
    assert abs(result.coherence_score + result.manipulation_probability - 1.0) < 0.001


def test_direct_binding_language_scores_coherent():
    text = (
        "We will halt all deployments. We must submit independent audits. "
        "We shall refund all affected users within 14 days."
    )
    result = extract(text)
    assert result.action_ratio > 0.5
    assert result.coherence_score > 0.4


if __name__ == "__main__":
    tests = [
        test_accountability_text_scores_low_manipulation,
        test_deflection_text_scores_high_manipulation,
        test_988_deflection_flagged,
        test_child_facing_high_risk_flag,
        test_coherence_score_inverse_of_manipulation,
        test_direct_binding_language_scores_coherent,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
    if passed < len(tests):
        sys.exit(1)

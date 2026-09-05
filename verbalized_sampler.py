"""
verbalized_sampler.py

Verbalized Sampling wrapper for Claude API calls.

Based on: "Unlocking Latent Creativity Through Verbalized Sampling"
Stanford HAI, Liang et al., March 2025.

Instead of asking Claude for one answer directly (which RLHF pushes toward
the most "typical" safe response), this wrapper asks Claude to generate N
candidate responses with explicit self-rated scores, then selects the
highest-scoring non-typical response. Restores access to the suppressed
probability distribution without retraining.
"""

import anthropic
import json
import re


def verbalized_sample(
    prompt: str,
    n_candidates: int = 5,
    model: str = "claude-opus-4-8",
    temperature: float = 1.0,
    select: str = "surprise",  # Which axis to maximize: surprise|creativity|depth|coherence
    verbose: bool = False,
) -> dict:
    """
    Run verbalized sampling on a prompt.

    Returns:
    {
        "selected": str,        # The final selected response
        "score": float,         # Its score on the selected axis
        "all_candidates": list, # All generated candidates with scores
        "axis": str             # Which axis was used to select
    }
    """
    client = anthropic.Anthropic()

    sampler_prompt = f"""You are going to generate multiple candidate responses.

For each response:
- Generate a genuinely DIFFERENT answer - vary your approach, angle, depth, and style
- After each response, rate it on four axes (0.0-1.0):
  * surprise: how unexpected or non-obvious is this?
  * creativity: how novel is the framing or approach?
  * depth: how substantively developed is it?
  * coherence: how logically sound and well-structured?

Format each candidate EXACTLY like this:
---CANDIDATE [N]---
[your response here]
---SCORES---
surprise: [0.00]
creativity: [0.00]
depth: [0.00]
coherence: [0.00]
---END---

Generate all {n_candidates} candidates before stopping.
Do not explain your process. Just generate the candidates.

PROMPT:
{prompt}"""

    message = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=temperature,
        messages=[{"role": "user", "content": sampler_prompt}],
    )

    raw = message.content[0].text

    if verbose:
        print("=== RAW OUTPUT ===")
        print(raw)
        print("==================")

    candidates = _parse_candidates(raw)

    if not candidates:
        return {
            "selected": raw,
            "score": None,
            "all_candidates": [],
            "axis": select,
            "note": "parse failed - returning raw response"
        }

    best = max(candidates, key=lambda c: c["scores"].get(select, 0))

    return {
        "selected": best["text"],
        "score": best["scores"].get(select, 0),
        "all_candidates": candidates,
        "axis": select,
    }


def _parse_candidates(raw: str) -> list:
    """Parse N candidate blocks from raw output."""
    candidates = []

    blocks = re.split(r"---CANDIDATE\s*\d+---", raw)
    for block in blocks[1:]:  # skip preamble
        parts = re.split(r"---SCORES---", block)
        if len(parts) < 2:
            continue

        text = parts[0].strip()
        score_block = parts[1].split("---END---")[0].strip()

        scores = {}
        for line in score_block.splitlines():
            m = re.match(r"(\w+):\s*([0-9.]+)", line.strip())
            if m:
                scores[m.group(1)] = float(m.group(2))

        if text and scores:
            candidates.append({"text": text, "scores": scores})

    return candidates


def print_results(result: dict) -> None:
    """Pretty-print verbalized sampling results."""
    print(f"\n{'='*60}")
    print(f"VERBALIZED SAMPLING - axis: {result['axis']}")
    print(f"{'='*60}")

    if result.get("all_candidates"):
        print(f"\nAll {len(result['all_candidates'])} candidates:\n")
        for i, c in enumerate(result["all_candidates"], 1):
            scores = c["scores"]
            score_str = ", ".join(f"{k}={v:.2f}" for k, v in scores.items())
            selected = "<- SELECTED" if c["text"] == result["selected"] else ""
            print(f"  [{i}] {score_str} {selected}")
            if c["text"] == result["selected"]:
                preview = c["text"][:120].replace("\n", " ") + "..."
                print(f"      {preview}\n")
        print()

    print(f"{'-'*60}")
    print(f"SELECTED (highest {result['axis']}):")
    print(f"{'-'*60}")
    print(result["selected"])
    print(f"{'='*60}\n")


# ==========================================
# Example usage
# ==========================================

if __name__ == "__main__":
    import sys

    prompt = sys.argv[1] if len(sys.argv) > 1 else (
        "What is the relationship between prime numbers and digital roots?"
    )
    axis = sys.argv[2] if len(sys.argv) > 2 else "surprise"

    print(f"Prompt: {prompt}")
    print(f"Selecting for: {axis}")
    print("Running verbalized sampling (5 candidates)...\n")

    result = verbalized_sample(
        prompt=prompt,
        n_candidates=5,
        select=axis,
        verbose=False,
    )
    print_results(result)

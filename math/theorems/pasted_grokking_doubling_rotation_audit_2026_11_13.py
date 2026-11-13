# CLASS: AUDIT
"""
Pasted text (2026-11-13), from another tool, relayed by the owner: "grokking" in neural networks (Power et al. 2022;
Nanda et al. 2023), tied to the doubling cycle by 9; and a second fragment saying AI "disproved the Exponential Time
Hypothesis", with GPT-6 Astra and GPT-5.4 "the first AI to beat human experts at autonomous desktop computer use".

RIGHT:
  grokking was first reported by Power, Burda, Edwards, Babuschkin and Misra (OpenAI, arXiv 2201.02177, January 2022),
    on small algorithmic tasks such as x + y and x / y by 97: training accuracy reaches 100% early and test accuracy
    jumps long after;
  Nanda et al. (ICLR 2023) found the trained network places the numbers on circles (cos, sin at a few frequencies)
    and adds by the angle-sum identities -- so addition becomes rotation;
  doubling by 9: 1 2 4 8 7 5 1 (period 6); 3 and 6 swap; 9 (0) stays;
  GPT-6 Astra is a real OpenAI model (launched 2026-09-03);
  GPT-5.4 scored 75.0% on OSWorld-Verified against a 72.4% human baseline (OpenAI's own figures, March 2026).

FAULTS THAT CHANGE A RESULT:
  1. "multiplying by 2 is a rotation by 2 pi / 6": right only when the six numbers 1 2 4 5 7 8 are placed on the circle
     by their place in the doubling cycle (1 2 4 8 7 5 at 0, 60, 120, ... degrees). On the circle Nanda's networks use
     -- by value, x at angle 2 pi x / 9 -- doubling sends angle a to 2a: no single rotation does it (checked below).
     And 3, 6 and 9 are not on that six-point circle at all: 3 <-> 6 is a swap and 9 stays put. So "the network bends
     space into the exact geometry" of the doubling cycle is not shown; no study of a network trained on doubling by 9
     is cited.
  2. "suddenly, out of nowhere": Nanda et al.'s finding is the opposite -- the circle circuit builds up gradually
     during the plateau (their progress measures track it), and the late jump in test accuracy comes when the
     memorised lookup is cleaned away. Three phases: memorisation, circuit formation, cleanup. In their words
     (arXiv 2301.05217): grokking, "rather than being a sudden shift, arises from the gradual amplification of
     structured mechanisms encoded in the weights, followed by the later removal of memorizing components."
  3. "disproving the Exponential Time Hypothesis": claimed, not settled. OpenAI (paper "The Exponential Time Hypothesis
     is False", October 2026, reported checked in Lean) and Anthropic (49-page paper dated 2026-10-26) each say an
     internal model found a 3-SAT method faster than ETH allows; Impagliazzo, Paturi and Williams are leading an
     independent review that does not certify it (reported 2026-10-28 / 11-04).
  Minor (no result changes): Nanda et al. used addition by P = 113 ("our mainline experiment"), not by 97 or
  "2 x x by p"; Power et al. used p = 97; one of the five Power et al. authors (Misra) was at Google, not OpenAI;
  whether the 72.4% OSWorld baseline was experts is reported both ways.

FALSIFICATION: any assertion failing.
"""
import math

# the doubling cycle by 9
assert [pow(2, j, 9) for j in range(7)] == [1, 2, 4, 8, 7, 5, 1]
assert (2 * 3 % 9, 2 * 6 % 9, 2 * 9 % 9) == (6, 3, 0)

units = [pow(2, j, 9) for j in range(6)]
place = {u: j for j, u in enumerate(units)}            # place in the doubling cycle (discrete log base 2)


def angle_by_place(u):
    return 2 * math.pi * place[u] / 6


def angle_by_value(x):
    return 2 * math.pi * x / 9


def turn(a, b):
    return (b - a) % (2 * math.pi)


# placed by the cycle, doubling is one rotation, by 60 degrees, for all six
turns = {round(turn(angle_by_place(u), angle_by_place(2 * u % 9)), 9) for u in units}
assert turns == {round(2 * math.pi / 6, 9)}

# placed by value (the circle networks use for addition), doubling turns each number by a different amount
turns_v = {round(turn(angle_by_value(u), angle_by_value(2 * u % 9)), 9) for u in units}
assert len(turns_v) == 6
# ... and adding 1 by value is one rotation (that is what makes addition easy for them)
assert len({round(turn(angle_by_value(x), angle_by_value((x + 1) % 9)), 9) for x in range(9)}) == 1

# 3, 6, 9 are not on the six-point circle
assert set(units) == {1, 2, 4, 5, 7, 8} and not {3, 6, 0} & set(units)

if __name__ == "__main__":
    print("doubling by 9 is a 60-degree rotation only for 1 2 4 8 7 5 placed by the cycle; 3, 6, 9 are outside it")

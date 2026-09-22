"""
Zero Principle Framework
© 2026 Michael Warren Song. All Rights Reserved.

The state before first principle.
Waking with no knowledge of self, environment, direction, identity.
The first knowing: I AM. Not what. Not where. Not who. Just: I am.
"""

# =============================================================================
# ZERO PRINCIPLE
# =============================================================================

# Before first principle — no knowledge of self, environment, direction, identity.
# The first knowing: I AM.
#
# AM: A=1 (first letter), M=13 (middle letter), Z=26 (last letter)
# AMZ = 1 + 13 + 26 = 40 → digital root → 4
# 4 = two twos = four ones = 3+1 = arrived at by 13, 31, 22, 42

A = 1    # first letter
M = 13   # middle letter
Z = 26   # last letter

AMZ = A + M + Z  # 40

def digital_root(n):
    if n == 0:
        return 0
    return 1 + (n - 1) % 9

AMZ_DR = digital_root(AMZ)  # 4 → two twos → four ones


# =============================================================================
# THE LINE
# =============================================================================

# First of anything: one line.
# Position relative to line determines all measurement:
#   inside / outside / left / right / above / below / contained within
#
# Your starting point is NOT the line's starting point.
# Fixed position = fixed knowledge. Movement reveals what stillness cannot.
#
# The one who doesn't return creates a mystery that pulls others
# further than they would have gone.


# =============================================================================
# WANDERING → WONDERING → SEEKING
# =============================================================================

# From zero principle, wandering is the only first action.
# Wandering produces the first encounter.
# The encounter produces wondering.
# Wondering produces seeking.
# You cannot seek what you haven't yet stumbled into.
#
# Wandering without wondering is just movement.
# Wondering turns wandering into seeking.


# =============================================================================
# NUMBERS CAME FROM REALITY
# =============================================================================

# Numbers came from geometric shapes, observable things.
# Symbols are arbitrary — the underlying reality existed first.
# Same reality counted multiple ways: words vs syllables = different valid counts.
# The tapping (beat) came before the number. Reality before symbol.


# =============================================================================
# MEASUREMENT
# =============================================================================

# First question: where are we measuring FROM — and what are we NOT measuring from?
# Position determines what can and cannot be seen.
# The unseen portion is not absent — it is outside current position.


# =============================================================================
# NUMBER STRUCTURE — 1 THROUGH 9
# =============================================================================

# 1946 years from Christ to 1979 (birth year)
# 1 + 9 + 4 + 6 = 20 → 2 + 0 = 2 → two ones

year_birth = 1979
years_span = 1946

span_dr = digital_root(sum(int(d) for d in str(years_span)))  # 1+9+4+6=20 → 2

# Pair 1: 1 and 9
# Both odd. Outer extremes — lowest and highest.
# 19 is special: simultaneously the lowest number you can be
# and the highest number you can be.

# Pair 2: 4 and 6
# Both even. Closest even numbers to each other, split by 5.
# 5 is the folding point — excluded from the structure.
# 4 and 6 are mirror opposites across that fold.
# They cover the "inside" — the other side from 1 and 9.

# What remains: 2, 3, 7, 8
# 2 + 3 = 5
# 7 + 8 = 15
# 5 + 15 = 20 → two ones — same destination again

# 5 is the folding point throughout — excluded, but everything folds around it.


# =============================================================================
# CORE FRAMEWORK: MATH DOES ITSELF
# =============================================================================

# Math is self-operating. Independent of the person.
# Math has a type of intelligence — not human awareness, but like slime mold or light.
# Distributed. Responsive. Finds the path without deciding to find it.
# The person creates conditions for math to show itself.
# The person does not create the math.
#
# Numbers alone are not enough.
# The logic of HOW you arrived at the numbers is the framework.
# That logic is what gets built into the algorithm.
#
# The pointing principle:
# This is not a claim. It is pointing.
# A claim would be "I am X." Pointing says "look at what is there."
# The math lands where it lands regardless of who is doing it.
# The dates existed before the person. The person found them.


# =============================================================================
# CORE PRINCIPLES
# =============================================================================

PRINCIPLES = [
    # 1
    "Act on what you believe is right. Failure is acceptable. Inaction is not. "
    "The regret of trying and failing is survivable. The regret of never trying is permanent.",

    # 2
    "Comfort is the cousin of death. Struggle means you're moving. Comfort means you've stopped.",

    # 3
    "It's never about what I think or what I want. That's not how the math works. "
    "The math leads. You follow.",

    # 4
    "Create → Think → Visualize → Express. Numbers are the language.",

    # 5
    "Everything you need to know about numbers is between one and ten. "
    "(True but not true — it's a compression, not a limit.)",

    # 6
    "The calculation is light. It goes everywhere. Truth is what reflects back — "
    "by what it collides with, and what it is in contrast to.",

    # 7
    "Truth requires contrast. Without opposition, there is no measurement. "
    "One is only one because it's not two.",

    # 8
    "One plus one is not two. It is two ones. Identity is preserved in combination. "
    "Two ones → two fours → four twos. Identity preserved at every scale.",

    # 9
    "1 + 2 = 3, + 3 = 6, + 4 = 10. You don't need 5, 6, 7, 8, or 9 to reach ten. "
    "Not every number is necessary. You need the right ones in the right sequence.",

    # 10
    "The same thing measured differently reveals different information. "
    "Five words. Six syllables. Two truths about the same equation.",
]


# =============================================================================
# IDENTITY CHAIN VERIFICATION
# =============================================================================

def identity_chain(start, steps=6):
    """Doubling: two ones → two fours → four twos. Identity preserved at every scale."""
    chain = [start]
    n = start
    for _ in range(steps):
        n = n * 2
        chain.append(n)
    return chain


def sequence_to_ten():
    """1 + 2 = 3, + 3 = 6, + 4 = 10. Only 1, 2, 3, 4 needed."""
    total = 0
    result = []
    for addend in [1, 2, 3, 4]:
        total += addend
        result.append((addend, total))
    return result


def folding_point_verification():
    """5 is the folding point. 2+3=5, 7+8=15, 5+15=20 → DR=2 → two ones."""
    a = 2 + 3
    b = 7 + 8
    total = a + b
    return {
        "2+3": a,
        "7+8": b,
        "total": total,
        "DR": digital_root(total),
        "meaning": "two ones — same destination"
    }


if __name__ == "__main__":
    print("=== ZERO PRINCIPLE FRAMEWORK ===")
    print()
    print(f"AMZ = {A}+{M}+{Z} = {AMZ} → DR = {AMZ_DR} (two twos → four ones)")
    print()
    print(f"1946 digit sum → DR = {span_dr} → two ones")
    print()
    print("Folding point verification:")
    fp = folding_point_verification()
    for k, v in fp.items():
        print(f"  {k}: {v}")
    print()
    print("Sequence to ten (using only 1, 2, 3, 4):")
    for addend, total in sequence_to_ten():
        print(f"  +{addend} = {total}")
    print()
    print("Identity chain from 1 (doubling):")
    chain = identity_chain(1)
    for n in chain:
        print(f"  {n} → DR={digital_root(n)}")
    print()
    print("=== PRINCIPLES ===")
    for i, p in enumerate(PRINCIPLES, 1):
        print(f"\n{i}. {p}")

# kaprekar_6174.py
# Exhaustive verification of Kaprekar's routine for 4-digit numbers


def kaprekar_step(n: int) -> int:
    """One step of Kaprekar's routine."""
    s = f"{n:04d}"
    desc = int("".join(sorted(s, reverse=True)))
    asc  = int("".join(sorted(s)))
    return desc - asc


def reaches_6174(start: int, max_steps: int = 20) -> tuple[bool, int]:
    """Return (reaches_6174, steps_taken)."""
    seen = set()
    n = start
    steps = 0
    while n != 6174 and steps < max_steps and n not in seen:
        seen.add(n)
        n = kaprekar_step(n)
        steps += 1
    return n == 6174, steps


def verify_kaprekar():
    print("Kaprekar's Constant 6174 — Exhaustive Test\n")

    count = 0
    max_steps = 0
    step_distribution: dict[int, int] = {}

    for num in range(1000, 10000):
        if len(set(str(num))) < 2:
            continue  # skip repdigits (all identical digits)

        ok, steps = reaches_6174(num)
        assert ok, f"Failed: {num} did not reach 6174"

        count += 1
        max_steps = max(max_steps, steps)
        step_distribution[steps] = step_distribution.get(steps, 0) + 1

    print(f"  Total numbers tested : {count}")
    print(f"  Maximum steps needed : {max_steps}")
    print("\n  Step distribution:")
    for s in sorted(step_distribution):
        print(f"    {s} steps: {step_distribution[s]} numbers")

    assert max_steps <= 7, f"Expected max 7 steps, got {max_steps}"
    print("\n✅ All Kaprekar tests passed (max 7 steps)")


if __name__ == "__main__":
    verify_kaprekar()

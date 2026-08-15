import itertools
from math import isqrt


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, isqrt(n) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))


def digital_root(n: int) -> int:
    while n >= 10:
        n = digit_sum(n)
    return n


def analyze_digit_set_diamond(digits=(1, 3, 7)):
    perms = sorted(
        list(set(int("".join(map(str, p))) for p in itertools.permutations(digits)))
    )

    print(f"=== Analysis for Digit Set {digits} ===")
    print(f"{'Number':<8} | {'Digit Sum':<10} | {'Digital Root':<12} | {'Primality'}")
    print("-" * 50)

    total_sum = 0
    for num in perms:
        d_sum = digit_sum(num)
        d_root = digital_root(num)
        prime_status = "PRIME" if is_prime(num) else "Composite"
        total_sum += num
        print(
            f"{num:<8} | {d_sum:<10} | {d_root:<12} | {prime_status}"
        )

    print("-" * 50)
    print(f"System Aggregate Sum: {total_sum}")
    print(f"Intermediate Sum:    {digit_sum(total_sum)}")
    print(f"System Digital Root: {digital_root(total_sum)}")
    print()


def generate_11_ladder(start_k=18, end_k=9):
    print("=== Multiples of 11 Ladder (198 -> 99) ===")
    print(f"{'Term':<6} | {'Formula':<10} | {'Digit Sum':<10} | {'Digital Root'}")
    print("-" * 45)
    for k in range(start_k, end_k - 1, -1):
        val = 11 * k
        print(f"{val:<6} | 11 x {k:<5} | {digit_sum(val):<10} | {digital_root(val)}")
    print()


def birthday_state_collapse(n_states=9, max_elements=10):
    print(f"=== State-Space Collision Probability (N = {n_states}) ===")
    print(f"{'Elements (n)':<14} | {'Unique Prob (%)':<16} | {'Collision Prob (%)'}")
    print("-" * 52)
    p_unique = 1.0
    for n in range(1, max_elements + 1):
        if n > n_states:
            p_unique = 0.0
        else:
            p_unique *= (n_states - (n - 1)) / n_states
        p_collision = (1.0 - p_unique) * 100
        print(f"{n:<14} | {p_unique * 100:<16.2f} | {p_collision:.2f}%")
    print()


if __name__ == "__main__":
    analyze_digit_set_diamond((1, 3, 7))
    generate_11_ladder(18, 9)
    birthday_state_collapse(n_states=9, max_elements=10)

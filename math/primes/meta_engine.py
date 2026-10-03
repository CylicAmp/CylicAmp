from math import gcd


def digital_root(n):
    n = abs(int(n))
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


class MetaEngine:
    def __init__(self, rule_multiplier=7):
        self.rule_multiplier = rule_multiplier
        self.cycle_state = [7, 3, 11, 2, 5, 13]
        self._last_result = None

    def decode_seed(self, seed):
        dr = digital_root(seed)
        factors = [i for i in range(1, seed + 1) if seed % i == 0]
        cycle = [(seed * self.rule_multiplier * i) % 37 for i in self.cycle_state]
        return {
            "seed": seed,
            "digital_root": dr,
            "factors": factors,
            "cycle": cycle,
            "rule_multiplier": self.rule_multiplier,
        }

    def run(self, num_cycles=3):
        state = list(self.cycle_state)
        all_values = []
        for _ in range(num_cycles):
            state = [(v * self.rule_multiplier + 1) % 97 for v in state]
            all_values.extend(state)

        full_second_cycle = all_values[len(self.cycle_state):len(self.cycle_state)*2]
        final_state = sum(state) % 999 + 1

        result = {
            "max_value": max(all_values),
            "min_value": min(all_values),
            "full_second_cycle": full_second_cycle,
            "final_state": final_state,
            "all_values": all_values,
        }
        self._last_result = result
        return result

    def meta_evolve_lane(self, seed_number=246, iterations=3):
        history = []
        current_multiplier = self.rule_multiplier
        current_cycle_state = [7, 3, 11, 2, 5, 13]

        for step in range(iterations):
            analysis = self.decode_seed(seed_number)
            result = self.run(num_cycles=3)

            new_multiplier = (result["max_value"] % 10) + 1
            new_cycle_state = [d % 13 for d in result["full_second_cycle"][:6]]

            self.rule_multiplier = new_multiplier
            current_cycle_state = new_cycle_state
            seed_number = result["final_state"]

            history.append({
                "step": step + 1,
                "multiplier": new_multiplier,
                "cycle_state": new_cycle_state,
                "max_value": result["max_value"],
                "final_state": result["final_state"],
                "analysis": analysis,
            })

        self.rule_multiplier = current_multiplier

        print(f"META-EVOLVING LANE COMPLETED AFTER {iterations} ITERATIONS")
        for entry in history:
            print(f"   Step {entry['step']}: multiplier = {entry['multiplier']}, "
                  f"max_value = {entry['max_value']}, final_state = {entry['final_state']}")

        return history


if __name__ == "__main__":
    engine = MetaEngine(rule_multiplier=7)
    history = engine.meta_evolve_lane(seed_number=246, iterations=5)
    print()
    print("CYCLE STATES:")
    for entry in history:
        print(f"  step {entry['step']}: {entry['cycle_state']}")

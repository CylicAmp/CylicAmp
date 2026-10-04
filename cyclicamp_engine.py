import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

class CyclicAmpEngine:
    """Deterministic Logic Engine V1.1 - CyclicAmp (by Red3rdeye)"""

    def __init__(self, cycle_state=None, init_value=100, rule_multiplier=2, custom_rule=None):
        self.cycle_state = cycle_state if cycle_state is not None else [7, 3, 11, 2, 5, 13]
        self.m = len(self.cycle_state)
        self.init_value = init_value
        self.rule_multiplier = rule_multiplier
        self.custom_rule = custom_rule or (lambda i, val: val * (i + 1) * rule_multiplier + 5)
        self.history = []
        self.ans2m = None

    def run(self, num_cycles=3):
        self.ans2m = [0] * (2 * self.m * num_cycles)
        prev = self.init_value
        print("CyclicAmpEngine V1.1 Started\n")

        for i in range(len(self.ans2m)):
            val = self.cycle_state[i % self.m]
            step = self.custom_rule(i, val)               # fully customizable

            self.ans2m[i] = step
            self.ans2m[i] += prev                          # ans2m +=
            prev = self.ans2m[i]
            self.history.append(prev)

            if (i + 1) % self.m == 0:
                print(f"Cycle {(i+1)//self.m} complete | Value = {prev}")

        print("\n" + "="*60)
        print("Engine finished successfully!")
        return self.get_results()

    def get_results(self):
        second_cycle = self.ans2m[self.m:]
        return {
            "full_second_cycle": second_cycle,
            "max": max(second_cycle),
            "sum": sum(second_cycle),
            "final": second_cycle[-1]
        }

    def visualize(self, save_path=None):
        plt.figure(figsize=(10, 5), facecolor='#0e1117')
        plt.plot(self.history, color='#00ff88', linewidth=2, marker='o', markersize=4)
        plt.title("CyclicAmp Deterministic Logic Evolution • V1.1", color='white')
        plt.xlabel("Step (with cyclic wrap-around)")
        plt.ylabel("Engine State Value")
        plt.grid(True, alpha=0.3, color='gray')
        plt.axhline(y=max(self.history), color='red', linestyle='--', alpha=0.5, label='Peak')
        plt.legend()
        plt.style.use('dark_background')
        if save_path:
            plt.savefig(save_path, facecolor='#0e1117', bbox_inches='tight')
            print(f"Plot saved -> {save_path}")
        else:
            plt.show()

    def save_results(self, filename="cyclicamp_results_v1.json"):
        data = self.get_results()
        data["engine_info"] = {"m": self.m, "init": self.init_value}
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved -> {filename}")


if __name__ == "__main__":
    engine = CyclicAmpEngine(cycle_state=[10, 20, 5, 30, 15, 8], init_value=50)
    results = engine.run(num_cycles=4)
    print(results)
    engine.visualize(save_path="outputs/cyclicamp_engine_v1.1.png")
    engine.save_results("outputs/my_toxic_empathy_run.json")

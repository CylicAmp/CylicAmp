"""
predictive_agi.py  —  v2 (CylicAmp integration)

Replaces the static linear model with three components from the math repo:

  1. DR Classification (prime_engine)
     digital_root(urgency × importance) maps each task to a DR class.
     DR ∈ {1,2,4,5,7,8} = "prime-class" (can propagate, scheduled normally).
     DR ∈ {3,6,9}        = "composite-class" (structurally blocked, needs decomp).

  2. 12-Cycle Lattice + Fixed-Point Self-Consistent Energy (fixed_point_sieve_audit)
     Tasks are placed at positions in Z/12Z.
     Prime-allowed positions {1,5,7,11} = high-throughput slots.
     The task state vector v ∈ ℝ¹² is evolved under H(λ) = D + λ(S + Sᵀ).
     Fixed-point iteration finds the self-consistent (v*, λ*, E*).
     E* replaces the static baseline_energy variable.
     λ* replaces the static alpha coupling.

  3. Spectral Stability as Success Probability
     P_success = spectral_gap / E*   where gap = E₁ - E₂.
     Large gap = clear dominant task direction = high stability.
     Small gap = competing tasks fighting for the dominant eigenstate = low stability.

Interface is unchanged: add, done, stress <1-10>, predict, exit.
"""

import json
import datetime
import os
import sys
import numpy as np
from math import gcd
from scipy.special import gamma

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'math', 'primes'))
from prime_engine import digital_root, _GRID_LABEL

# ---------------------------------------------------------------------------
# 12-cycle lattice (from fixed_point_sieve_audit)
# ---------------------------------------------------------------------------
N = 12
_c = np.array([1.0 if gcd(i % 12, 12) == 1 else 0.0 for i in range(N)])
_D = np.diag(_c)
_S = np.zeros((N, N))
for _i in range(N):
    _S[_i, (_i + 1) % N] = 1.0
_Sadj = _S.T
_m    = _c.copy()   # motif = prime-allowed positions

def _H(lam: float) -> np.ndarray:
    return _D + lam * (_S + _Sadj)

def _lam_of_v(v: np.ndarray, lam0: float, alpha: float, theta: float) -> float:
    return lam0 + alpha * (float(np.dot(_m, v) ** 2) - theta)

def _phi(v: np.ndarray, lam0: float, alpha: float, theta: float) -> np.ndarray:
    lam = _lam_of_v(v, lam0, alpha, theta)
    Hv  = _H(lam) @ v
    nrm = float(np.linalg.norm(Hv))
    return Hv / nrm if nrm > 1e-14 else v

def _fixed_point(lam0: float, alpha: float, theta: float,
                 seed: np.ndarray | None = None,
                 max_steps: int = 2000) -> dict:
    """
    Run fixed-point iteration and return the converged state.
    Returns dict with keys: converged, lam_star, E_star, gap, v_star, steps.
    """
    v = seed if seed is not None else np.ones(N) / np.sqrt(N)
    v = v / np.linalg.norm(v)

    for step in range(max_steps):
        v_new = _phi(v, lam0, alpha, theta)
        diff  = float(np.linalg.norm(v_new - v))
        if diff < 1e-8:
            lam_s  = _lam_of_v(v, lam0, alpha, theta)
            evals  = sorted(np.linalg.eigvalsh(_H(lam_s)), reverse=True)
            E1, E2 = evals[0], evals[1]
            return {
                "converged": True,
                "lam_star":  round(lam_s, 6),
                "E_star":    round(E1, 6),
                "gap":       round(E1 - E2, 6),
                "v_star":    v.copy(),
                "steps":     step,
            }
        v = v_new

    lam_s = _lam_of_v(v, lam0, alpha, theta)
    evals = sorted(np.linalg.eigvalsh(_H(lam_s)), reverse=True)
    E1, E2 = evals[0], evals[1]
    return {
        "converged": False,
        "lam_star":  round(lam_s, 6),
        "E_star":    round(E1, 6),
        "gap":       round(E1 - E2, 6),
        "v_star":    v.copy(),
        "steps":     max_steps,
    }


# ---------------------------------------------------------------------------
# DR task classification
# ---------------------------------------------------------------------------
DR_PRIME_CLASS    = frozenset({1, 2, 4, 5, 7, 8})
DR_COMPOSITE_CLASS = frozenset({3, 6, 9})

def _classify_task(urgency: int, importance: int) -> dict:
    """
    Compute DR class and 12-cycle position for a task.
    DR of urgency×importance:
      prime-class   → task can propagate, full weight
      composite-class → task is blocked; needs decomposition
    12-cycle position: (urgency × importance - 1) % 12
    """
    product = max(1, urgency * importance)
    dr      = digital_root(product)
    pos12   = (product - 1) % 12
    prime_class = dr in DR_PRIME_CLASS
    return {
        "dr":          dr,
        "grid":        _GRID_LABEL[dr],
        "pos12":       pos12,
        "prime_class": prime_class,
        "slot_type":   "prime-allowed" if gcd(pos12 % 12, 12) == 1 else "composite",
    }


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------
class PredictiveAGI:
    def __init__(self, data_file: str = "agi_predictive_data.json"):
        self.data_file = data_file

        # Fixed-point parameters (tune via 'params' command)
        self.lam0  = 0.5    # base coupling
        self.alpha = 0.1    # feedback sensitivity  (keep < 0.5 for contraction)
        self.theta = 0.5    # target overlap with prime-allowed positions

        # Priority weights
        self.w_u = 0.6
        self.w_i = 0.4

        self._fp_cache: dict | None = None   # cached fixed-point result
        self.load_data()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {"tasks": [], "stress_logs": [{"level": 1, "note": "init"}]}
            self.save_data()

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)
        self._fp_cache = None   # invalidate on any state change

    # ------------------------------------------------------------------
    # Stress
    # ------------------------------------------------------------------
    def get_current_stress(self) -> int:
        return self.data["stress_logs"][-1]["level"] if self.data["stress_logs"] else 1

    # ------------------------------------------------------------------
    # Task DR / 12-cycle classification
    # ------------------------------------------------------------------
    def _task_class(self, task: dict) -> dict:
        return _classify_task(task['urgency'], task['importance'])

    # ------------------------------------------------------------------
    # Priority  (updated formula with DR multiplier)
    # ------------------------------------------------------------------
    def calculate_priority(self, task: dict) -> float:
        """
        P_t = (w_u × u²  +  w_i × i)
              × dr_multiplier
              − stress_penalty

        dr_multiplier:  1.0  if DR class is prime-allowed (can propagate)
                        0.5  if DR class is composite     (blocked, half weight)
        stress_penalty: proportional to λ* (self-consistent coupling)
        """
        cls  = self._task_class(task)
        dr_m = 1.0 if cls["prime_class"] else 0.5

        fp    = self._get_fixed_point()
        S     = self.get_current_stress()
        # stress penalty scaled by self-consistent coupling
        penalty = fp["lam_star"] * S * 0.1

        raw = self.w_u * task['urgency'] ** 2 + self.w_i * task['importance']
        return max(round(raw * dr_m - penalty, 2), 0.1)

    # ------------------------------------------------------------------
    # Fixed-point computation
    # ------------------------------------------------------------------
    def _build_task_vector(self) -> np.ndarray:
        """
        Project active task priorities onto the 12-cycle state vector.
        v[k] = sum of priorities of tasks at 12-cycle position k.
        """
        v = np.zeros(N)
        active = [t for t in self.data["tasks"] if not t["completed"]]
        for t in active:
            cls  = self._task_class(t)
            pos  = cls["pos12"]
            # raw priority without stress penalty (avoid circular dependency)
            raw  = self.w_u * t['urgency'] ** 2 + self.w_i * t['importance']
            dr_m = 1.0 if cls["prime_class"] else 0.5
            v[pos] += raw * dr_m
        nrm = np.linalg.norm(v)
        return v / nrm if nrm > 1e-14 else np.ones(N) / np.sqrt(N)

    def _get_fixed_point(self) -> dict:
        if self._fp_cache is not None:
            return self._fp_cache
        seed = self._build_task_vector()
        S    = self.get_current_stress()
        # stress shifts lam0: higher stress = higher base coupling
        effective_lam0 = self.lam0 + (S - 1) * 0.05
        result = _fixed_point(effective_lam0, self.alpha, self.theta, seed=seed)
        self._fp_cache = result
        return result

    # ------------------------------------------------------------------
    # Load and success
    # ------------------------------------------------------------------
    def calculate_cumulative_load(self) -> float:
        tasks = [t for t in self.data["tasks"] if not t["completed"]]
        return round(sum(self.calculate_priority(t) for t in tasks), 2)

    def predict_success_probability(self) -> float:
        """
        P_success = (1 − 1/Γ(1 + gap/E* · N)) × 100

        Uses scipy.special.gamma with N=12 (cycle length) as the shape parameter.
        Γ grows rapidly: gap/E* > 0.2 gives P > 65%; gap/E* ≥ 0.5 saturates near 100%.
        Degrades gracefully to linear ratio on overflow.
        """
        fp  = self._get_fixed_point()
        E   = fp["E_star"]
        gap = fp["gap"]
        if E < 1e-10:
            return 0.0
        ratio = gap / E
        try:
            p = max(0.0, 1.0 - 1.0 / gamma(1.0 + ratio * N)) * 100.0
        except (OverflowError, ValueError):
            p = ratio * 100.0
        return round(min(p, 100.0), 1)

    # ------------------------------------------------------------------
    # Task management
    # ------------------------------------------------------------------
    def add_task(self, description: str, urgency: int = 3, importance: int = 3):
        task = {
            "id":          len(self.data["tasks"]) + 1,
            "description": description,
            "urgency":     max(1, min(5, urgency)),
            "importance":  max(1, min(5, importance)),
            "completed":   False,
            "timestamp":   datetime.datetime.now().isoformat(),
        }
        self.data["tasks"].append(task)
        self.save_data()

        cls = self._task_class(task)
        p   = self.calculate_priority(task)
        status = "PRIME-CLASS" if cls["prime_class"] else "COMPOSITE (needs decomp)"
        print(f"Task inserted.  DR={cls['dr']} ({cls['grid']})  "
              f"pos12={cls['pos12']}  [{status}]  Priority={p}")

    def complete_task(self, task_id: int):
        for task in self.data["tasks"]:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_data()
                print(f"Task {task_id} complete. Recalculating lattice state...")
                return
        print("Task ID not found.")

    def get_tasks(self):
        tasks = [t for t in self.data["tasks"] if not t["completed"]]
        tasks.sort(key=lambda x: self.calculate_priority(x), reverse=True)
        return tasks

    # ------------------------------------------------------------------
    # Stress logging
    # ------------------------------------------------------------------
    def log_state(self, stress_level: int):
        entry = {
            "level":     max(1, min(10, stress_level)),
            "timestamp": datetime.datetime.now().isoformat(),
        }
        self.data["stress_logs"].append(entry)
        self.save_data()
        fp = self._get_fixed_point()
        print(f"Stress = {stress_level}/10  →  λ* = {fp['lam_star']}  "
              f"E* = {fp['E_star']}  gap = {fp['gap']}")

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------
    def render_dashboard(self):
        fp         = self._get_fixed_point()
        L          = self.calculate_cumulative_load()
        P_success  = self.predict_success_probability()
        S          = self.get_current_stress()
        tasks      = self.get_tasks()

        # DR class breakdown
        prime_tasks     = [t for t in tasks if self._task_class(t)["prime_class"]]
        composite_tasks = [t for t in tasks if not self._task_class(t)["prime_class"]]

        print(f"\n{'='*50}")
        print(f"  UNIFIED PREDICTIVE DASHBOARD  (CylicAmp v2)")
        print(f"{'='*50}")
        print(f"  Stress modifier :  {S}/10")
        print(f"  Cumulative load :  {L}")
        print(f"  λ* (coupling)   :  {fp['lam_star']}  "
              f"({'converged' if fp['converged'] else 'approx'})")
        print(f"  E* (capacity)   :  {fp['E_star']}")
        print(f"  Spectral gap    :  {fp['gap']}")
        print(f"  Success rate    :  {P_success}%")
        print()

        # Warnings
        if not fp["converged"]:
            print("  ⚠  Fixed-point did not converge. Reduce alpha or task load.")
        if P_success < 40:
            print("  ⚠  Low stability (small spectral gap). Focus on prime-class tasks.")
        if composite_tasks:
            print(f"  ⚠  {len(composite_tasks)} composite-class task(s) detected. "
                  f"Decompose or defer.")

        # 12-cycle slot usage
        slot_counts = np.zeros(N, dtype=int)
        for t in tasks:
            slot_counts[self._task_class(t)["pos12"]] += 1
        print(f"\n  12-cycle slot usage (prime-allowed: pos 1,5,7,11):")
        used = [(i, slot_counts[i]) for i in range(N) if slot_counts[i] > 0]
        for pos, cnt in used:
            allowed = gcd(pos % 12, 12) == 1
            marker  = "✓" if allowed else "·"
            print(f"    [{marker}] pos {pos:>2} : {'█' * cnt}  ({cnt})")

        # Priority matrix
        print(f"\n  Active priority matrix:")
        print(f"  {'─'*44}")
        if not tasks:
            print("  Matrix clear.")
        for t in tasks:
            cls = self._task_class(t)
            p   = self.calculate_priority(t)
            tag = "P" if cls["prime_class"] else "C"
            print(f"  [{t['id']:>2}][{tag}] DR={cls['dr']}  "
                  f"W={p:<5}  {t['description']}")
        print(f"{'='*50}\n")

    def show_params(self):
        print(f"\n  Parameters: lam0={self.lam0}  alpha={self.alpha}  theta={self.theta}")
        print(f"  Contraction holds for alpha < {round((1 - 0.9783) * 1.5332 / (2 * 2.0 * 2.0), 4)}"
              f"  (spectral gap estimate at lam0)")
        print(f"  Use: params lam0=<v> alpha=<v> theta=<v>")

    def set_params(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, float(v))
        self._fp_cache = None
        print(f"  Parameters updated: lam0={self.lam0}  alpha={self.alpha}  theta={self.theta}")


# ---------------------------------------------------------------------------
# Execution loop
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agi = PredictiveAGI()
    print("Unified Predictive Framework Online.  (CylicAmp v2)")
    print("Type 'help' for commands.")

    while True:
        try:
            cmd = input("\nEngine> ").strip()
            cl  = cmd.lower()

            if cl in ('exit', 'quit'):
                print("Dumping state. Offline.")
                break

            elif cl.startswith('add '):
                desc = cmd[4:].strip()
                try:
                    u = int(input("  Urgency   (1-5): "))
                    i = int(input("  Importance(1-5): "))
                    agi.add_task(desc, urgency=u, importance=i)
                except ValueError:
                    print("  Invalid input. Applying defaults (U:3, I:3).")
                    agi.add_task(desc, urgency=3, importance=3)

            elif cl.startswith('done '):
                try:
                    agi.complete_task(int(cl[5:]))
                except ValueError:
                    print("Syntax: done <id>")

            elif cl.startswith('stress '):
                try:
                    agi.log_state(int(cl[7:]))
                except ValueError:
                    print("Syntax: stress <1-10>")

            elif cl in ('predict', 'status', 'dash'):
                agi.render_dashboard()

            elif cl.startswith('params '):
                parts = cl[7:].split()
                kw = {}
                for p in parts:
                    if '=' in p:
                        k, v = p.split('=', 1)
                        try:
                            kw[k.strip()] = float(v)
                        except ValueError:
                            pass
                if kw:
                    agi.set_params(**kw)
                else:
                    agi.show_params()

            elif cl == 'params':
                agi.show_params()

            elif cl == 'help':
                print("  Commands:")
                print("    add <task>          — add a task (prompts for urgency/importance)")
                print("    done <id>           — mark task complete")
                print("    stress <1-10>       — log current stress level")
                print("    predict / status    — render dashboard")
                print("    params              — show tuning parameters")
                print("    params lam0=<v> alpha=<v> theta=<v>  — update parameters")
                print("    exit                — shut down")

            else:
                print("Unrecognized operator. Type 'help'.")

        except KeyboardInterrupt:
            print("\nEmergency interrupt.")
            break

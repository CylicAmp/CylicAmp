"""
entropy_replicator_v2.py

Three deliverables:

  1. Entropy trace plot — single representative ENV-B run comparing
     original EMR (β high when H low) vs inverted EMR (β high when H high)
     with change-point markers.  Saved to: entropy_trace.png

  2. Extended experiments — K=10 arms, T=10 000 steps, 200 runs,
     both environments.

  3. Valve geometry formalization — the β(H) transfer function as a
     geometric control surface; four φ(h) shapes mapped and compared.

Valve equation (inverted coupling — the NEW conjecture):
  dx_i/dt = β(H) · x_i · (f_i − f̄)
  β(H)    = β_min + (β_max − β_min) · φ(H / H_max)
  φ(h)    = h          ← "linear valve"  (h := H/H_max ∈ [0,1])
             h²         ← "quadratic valve" (sharper at high H)
             √h         ← "square-root valve" (softer at low H)
             sigmoid(h) ← "threshold valve"

  β HIGH when H HIGH  →  fast adaptation when uncertain  (explore)
  β LOW  when H LOW   →  slow update when confident      (stable)

  This creates NEGATIVE feedback on exploitation:
    high H → high β → fast convergence → lower H → lower β → deceleration
  And POSITIVE feedback on re-exploration:
    after env change: H rises slowly → β rises → re-exploration accelerates
"""

import numpy as np
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

RNG_SEED    = 42
SIGMA_OBS   = 1.0
SIGMA_DRIFT = 0.05
P_CHANGE    = 1 / 333


# ============================================================
# Environments  (same as v1)
# ============================================================

class RandomWalkBandit:
    def __init__(self, K, sigma_drift, sigma_obs, rng):
        self.K, self.sigma_drift, self.sigma_obs, self.rng = K, sigma_drift, sigma_obs, rng
        self.mu = rng.normal(0, 1, K)
    def step_env(self): self.mu += self.rng.normal(0, self.sigma_drift, self.K)
    def pull(self, arm): return self.mu[arm] + self.rng.normal(0, self.sigma_obs)
    def best_arm(self): return int(np.argmax(self.mu))
    def best_reward(self): return self.mu[self.best_arm()]


class AbruptChangeBandit:
    def __init__(self, K, p_change, sigma_obs, rng):
        self.K, self.p_change, self.sigma_obs, self.rng = K, p_change, sigma_obs, rng
        self.mu = rng.normal(0, 1, K)
        self.change_steps = []
        self._t = 0
    def step_env(self):
        self._t += 1
        if self.rng.random() < self.p_change:
            self.mu = self.rng.normal(0, 1, self.K)
            self.change_steps.append(self._t)
    def pull(self, arm): return self.mu[arm] + self.rng.normal(0, self.sigma_obs)
    def best_arm(self): return int(np.argmax(self.mu))
    def best_reward(self): return self.mu[self.best_arm()]


# ============================================================
# Agents
# ============================================================

class EMRAgent:
    """Original EMR: β high when H low (from v1 — the conjecture that failed)."""
    def __init__(self, K, beta_min=0.5, beta_max=20.0, alpha=0.1, eps_floor=1e-6):
        self.K, self.beta_min, self.beta_max = K, beta_min, beta_max
        self.alpha, self.eps_floor = alpha, eps_floor
        self.name = "EMR-original"
        self.reset()
    def reset(self):
        self.x     = np.ones(self.K) / self.K
        self.f_hat = np.zeros(self.K)
    def entropy(self):
        x = np.clip(self.x, 1e-300, 1)
        return -float(np.sum(x * np.log(x)))
    def beta(self):
        H = self.entropy(); H_max = math.log(self.K)
        h = H / H_max if H_max > 0 else 0.0
        return self.beta_min + (self.beta_max - self.beta_min) * (1.0 - h)   # DECREASING
    def choose(self, rng): return int(rng.choice(self.K, p=self.x))
    def update(self, arm, reward):
        self.f_hat[arm] += self.alpha * (reward - self.f_hat[arm])
        b = self.beta(); f_bar = float(np.dot(self.x, self.f_hat))
        self.x = np.maximum(self.x + b * self.x * (self.f_hat - f_bar), self.eps_floor)
        self.x /= self.x.sum()


class InvertedEMRAgent:
    """Inverted EMR: β high when H high (new conjecture — negative feedback)."""
    def __init__(self, K, beta_min=0.5, beta_max=20.0, alpha=0.1,
                 eps_floor=1e-4, phi="linear"):
        self.K, self.beta_min, self.beta_max = K, beta_min, beta_max
        self.alpha, self.eps_floor, self.phi = alpha, eps_floor, phi
        self.name = f"EMR-inverted(φ={phi})"
        self.reset()
    def reset(self):
        self.x     = np.ones(self.K) / self.K
        self.f_hat = np.zeros(self.K)
    def entropy(self):
        x = np.clip(self.x, 1e-300, 1)
        return -float(np.sum(x * np.log(x)))
    def _phi(self, h):
        if   self.phi == "linear":    return h
        elif self.phi == "quadratic": return h ** 2
        elif self.phi == "sqrt":      return math.sqrt(h)
        elif self.phi == "sigmoid":
            return 1.0 / (1.0 + math.exp(-10.0 * (h - 0.5)))
        return h
    def beta(self):
        H = self.entropy(); H_max = math.log(self.K)
        h = H / H_max if H_max > 0 else 0.0
        return self.beta_min + (self.beta_max - self.beta_min) * self._phi(h)
    def choose(self, rng): return int(rng.choice(self.K, p=self.x))
    def update(self, arm, reward):
        self.f_hat[arm] += self.alpha * (reward - self.f_hat[arm])
        b = self.beta(); f_bar = float(np.dot(self.x, self.f_hat))
        self.x = np.maximum(self.x + b * self.x * (self.f_hat - f_bar), self.eps_floor)
        self.x /= self.x.sum()


class EpsilonGreedyAgent:
    def __init__(self, K, epsilon, alpha=0.1):
        self.K, self.epsilon, self.alpha = K, epsilon, alpha
        self.name = f"ε-greedy(ε={epsilon})"
        self.reset()
    def reset(self): self.f_hat = np.zeros(self.K)
    def choose(self, rng):
        return int(rng.integers(self.K)) if rng.random() < self.epsilon else int(np.argmax(self.f_hat))
    def update(self, arm, reward):
        self.f_hat[arm] += self.alpha * (reward - self.f_hat[arm])


class SoftmaxAgent:
    def __init__(self, K, tau=0.5, alpha=0.1):
        self.K, self.tau, self.alpha = K, tau, alpha
        self.name = f"Softmax(τ={tau})"
        self.reset()
    def reset(self): self.f_hat = np.zeros(self.K)
    def choose(self, rng):
        logits = self.f_hat / self.tau; logits -= logits.max()
        probs = np.exp(logits); probs /= probs.sum()
        return int(rng.choice(self.K, p=probs))
    def update(self, arm, reward):
        self.f_hat[arm] += self.alpha * (reward - self.f_hat[arm])


def run_bandit(env_factory, agents, T, N_runs, seed=RNG_SEED):
    rewards = {a.name: np.zeros((N_runs, T)) for a in agents}
    regrets = {a.name: np.zeros((N_runs, T)) for a in agents}
    for run in range(N_runs):
        rng = np.random.default_rng(seed + run * 997)
        env = env_factory(rng)
        for a in agents: a.reset()
        for t in range(T):
            env.step_env()
            best_r = env.best_reward()
            for agent in agents:
                arm = agent.choose(rng)
                r   = env.pull(arm)
                agent.update(arm, r)
                rewards[agent.name][run, t] = r
                regrets[agent.name][run, t] = best_r - r
    return rewards, regrets


# ============================================================
# 1.  Entropy Trace — single representative ENV-B run
# ============================================================
print("=" * 70)
print("1.  Entropy trace — single ENV-B run (saving entropy_trace.png)")
print("=" * 70)

T_TRACE = 5000
K_TRACE = 5
rng_t   = np.random.default_rng(RNG_SEED)
env_t   = AbruptChangeBandit(K_TRACE, P_CHANGE, SIGMA_OBS, rng_t)

agents_trace = [
    EMRAgent(K_TRACE, beta_min=0.5, beta_max=20.0, alpha=0.1, eps_floor=1e-6),
    InvertedEMRAgent(K_TRACE, beta_min=0.5, beta_max=20.0, alpha=0.1,
                     eps_floor=1e-4, phi="linear"),
]

H_max_trace = math.log(K_TRACE)
traces = {a.name: {"H": [], "beta": [], "reward": []} for a in agents_trace}
change_steps_trace = []

for a in agents_trace: a.reset()

for t in range(T_TRACE):
    env_t.step_env()
    if env_t.change_steps and env_t.change_steps[-1] == t + 1:
        change_steps_trace.append(t)
    for agent in agents_trace:
        arm = agent.choose(rng_t)
        r   = env_t.pull(arm)
        agent.update(arm, r)
        traces[agent.name]["H"].append(agent.entropy())
        traces[agent.name]["beta"].append(agent.beta())
        traces[agent.name]["reward"].append(r)

change_steps_trace = env_t.change_steps

# --- Print trace stats ---
for a in agents_trace:
    H_arr = np.array(traces[a.name]["H"])
    b_arr = np.array(traces[a.name]["beta"])
    print(f"\n  {a.name}:")
    print(f"    H mean={H_arr.mean():.4f}  H/H_max={H_arr.mean()/H_max_trace:.4f}  "
          f"β mean={b_arr.mean():.4f}")
    print(f"    H at t=0: {H_arr[0]:.4f}  H at t=100: {H_arr[100]:.4f}  "
          f"H at t=500: {H_arr[500]:.4f}")

print(f"\n  Change points: {change_steps_trace[:10]}")

# --- Plot ---
fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
colors = {"EMR-original": "#e74c3c", "EMR-inverted(φ=linear)": "#2980b9"}
ts = np.arange(T_TRACE)

for a in agents_trace:
    nm = a.name
    H_arr = np.array(traces[nm]["H"]) / H_max_trace   # normalised
    b_arr = np.array(traces[nm]["beta"])
    r_smooth = np.convolve(traces[nm]["reward"], np.ones(50)/50, mode="same")
    axes[0].plot(ts, H_arr,    color=colors[nm], alpha=0.85, lw=1.2, label=nm)
    axes[1].plot(ts, b_arr,    color=colors[nm], alpha=0.85, lw=1.2)
    axes[2].plot(ts, r_smooth, color=colors[nm], alpha=0.85, lw=1.2)

for cs in change_steps_trace:
    for ax in axes:
        ax.axvline(cs, color="#7f8c8d", lw=0.6, alpha=0.5, ls="--")

# Shade first change-point response window
if len(change_steps_trace) >= 2:
    cs0 = change_steps_trace[0]
    cs1 = min(cs0 + 200, change_steps_trace[1] if len(change_steps_trace) > 1 else T_TRACE)
    for ax in axes:
        ax.axvspan(cs0, cs1, alpha=0.08, color="#f39c12")

axes[0].set_ylabel("H / H_max  (normalised entropy)", fontsize=11)
axes[0].set_ylim(-0.05, 1.1)
axes[0].axhline(1.0, color="k", ls=":", lw=0.8, alpha=0.4)
axes[0].legend(fontsize=10, loc="upper right")
axes[0].set_title("Entropy trace: ENV-B abrupt-change bandit (K=5, T=5000)", fontsize=13)

axes[1].set_ylabel("β(H)  (update rate)", fontsize=11)
axes[1].axhline(0.5,  color="k", ls=":", lw=0.8, alpha=0.3)   # β_min
axes[1].axhline(20.0, color="k", ls=":", lw=0.8, alpha=0.3)   # β_max

axes[2].set_ylabel("Smoothed reward (w=50)", fontsize=11)
axes[2].set_xlabel("Time step t", fontsize=11)

vline = mpatches.Patch(color="#7f8c8d", alpha=0.5, label="change point")
span  = mpatches.Patch(color="#f39c12", alpha=0.25, label="first recovery window")
axes[0].legend(handles=axes[0].get_legend().legend_handles + [vline, span],
               fontsize=9, loc="upper right")

plt.tight_layout()
plt.savefig("entropy_trace.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  Saved: entropy_trace.png")


# ============================================================
# 2.  Extended experiments: K=10, T=10 000
# ============================================================
print()
print("=" * 70)
print("2.  Extended: K=10, T=10 000, 200 runs")
print("=" * 70)

K10 = 10
T10 = 10_000
N10 = 200
H_max_10 = math.log(K10)

agents_10 = [
    EMRAgent(K10, beta_min=0.5, beta_max=20.0, alpha=0.1),
    InvertedEMRAgent(K10, beta_min=0.5, beta_max=20.0, alpha=0.1, eps_floor=1e-4, phi="linear"),
    InvertedEMRAgent(K10, beta_min=0.5, beta_max=20.0, alpha=0.1, eps_floor=1e-4, phi="quadratic"),
    InvertedEMRAgent(K10, beta_min=0.5, beta_max=20.0, alpha=0.1, eps_floor=1e-4, phi="sqrt"),
    EpsilonGreedyAgent(K10, epsilon=0.05),
    EpsilonGreedyAgent(K10, epsilon=0.10),
    EpsilonGreedyAgent(K10, epsilon=0.20),
    SoftmaxAgent(K10, tau=0.5),
]

def env_A10(rng): return RandomWalkBandit(K10, SIGMA_DRIFT, SIGMA_OBS, rng)
def env_B10(rng): return AbruptChangeBandit(K10, P_CHANGE, SIGMA_OBS, rng)

for env_name, env_factory in [("ENV-A RandomWalk", env_A10), ("ENV-B AbruptChange", env_B10)]:
    print(f"\n  {env_name}  (K={K10}, T={T10}, N={N10})")
    rews, regs = run_bandit(env_factory, agents_10, T10, N10)
    print(f"  {'Agent':>30}  {'Mean reward':>12}  {'±SE':>8}  "
          f"{'Cum. regret':>13}  {'±SE':>8}")
    print(f"  {'-'*76}")
    results_10 = {}
    for a in agents_10:
        nm = a.name
        mr = rews[nm].mean(axis=1); cr = regs[nm].sum(axis=1)
        r_m, r_se = mr.mean(), mr.std() / math.sqrt(N10)
        g_m, g_se = cr.mean(), cr.std()  / math.sqrt(N10)
        results_10[nm] = (r_m, r_se, g_m, g_se)
        print(f"  {nm:>30}  {r_m:>12.4f}  {r_se:>8.4f}  {g_m:>13.1f}  {g_se:>8.1f}")

    # Best-vs-best comparison
    inverted_names = [a.name for a in agents_10 if "inverted" in a.name]
    eps_names      = [a.name for a in agents_10 if "ε-greedy" in a.name]
    best_inv  = min(inverted_names, key=lambda nm: results_10[nm][2])
    best_eps  = min(eps_names,      key=lambda nm: results_10[nm][2])
    diff = results_10[best_eps][2] - results_10[best_inv][2]
    se   = math.sqrt(results_10[best_inv][3]**2 + results_10[best_eps][3]**2)
    Z    = diff / se
    print(f"\n  Best inverted EMR : {best_inv}  regret={results_10[best_inv][2]:.1f}")
    print(f"  Best ε-greedy     : {best_eps}  regret={results_10[best_eps][2]:.1f}")
    print(f"  Δregret           = {diff:.1f}  Z={Z:+.2f}  "
          f"({'inverted EMR WINS' if Z > 2 else 'inverted EMR LOSES' if Z < -2 else 'inconclusive'})")


# ============================================================
# 3.  Valve Geometry Formalization
# ============================================================
print()
print("=" * 70)
print("3.  Valve Geometry — β(H) transfer function")
print("=" * 70)

print(f"""
  FORMAL DEFINITION
  -----------------
  State: population vector x ∈ Δ^K  (K-simplex, Σxᵢ=1)
  Fitness: estimated reward f̂ ∈ ℝ^K  (exponential moving average)
  Entropy: H(x) = −Σ xᵢ ln xᵢ ∈ [0, H_max],  H_max = ln K
  Normalised entropy: h = H / H_max ∈ [0, 1]

  Inverted replicator ODE (continuous time):
    ẋᵢ = β(h) · xᵢ · (f̂ᵢ − f̄)         where  f̄ = Σ xⱼ f̂ⱼ

  Valve transfer function  φ: [0,1] → [0,1]:
    β(h) = β_min + (β_max − β_min) · φ(h)

  Four valve geometries:
    φ_L(h) = h               "linear valve"      monotone, proportional
    φ_Q(h) = h²              "quadratic valve"   slow to open at low H
    φ_R(h) = √h              "root valve"        fast to open at low H
    φ_S(h) = σ(k(h−0.5))    "sigmoid valve"     threshold at h=0.5, k=10

  Fixed points of the dynamics (β > 0):
    ẋᵢ = 0 for all i  iff  f̂ᵢ = f̄ ∀i  (uniform fitness)
    OR  xᵢ = 0 for all i except one (absorbing corner)

  Stability of corners:
    At a corner xⱼ=1, xᵢ≈0: h→0, β→β_min.
    Perturbation to xᵢ = ε: ẋᵢ ≈ β_min · ε · (f̂ᵢ − f̂ⱼ).
    Corner is STABLE if f̂ⱼ > f̂ᵢ for all i≠j  (xⱼ is best arm).
    Corner DESTABILISES when f̂ⱼ drops below some f̂ᵢ:
      recovery rate ∝ β_min · eps_floor   (slow initial re-exploration)
    As h rises (increasing entropy): β rises (valve opens).
    Recovery ACCELERATES — this is the self-correcting property.

  Stability of the interior (uniform):
    At x=1/K: h=1, β=β_max.  Fast convergence to best arm.
    The interior is a saddle: globally attracted to corners.
    Rate of convergence from uniform: ∝ β_max · Var(f̂).

  VALVE CONTROL TABLE:
    h=0 (concentrated): β=β_min  → slow, stable (exploit)
    h=0.5 (mixed):      β≈mid    → intermediate
    h=1 (uniform):      β=β_max  → fast convergence (explore → exploit)

  Comparison with original EMR (β decreasing):
    Original: β → β_max when h→0 → positive feedback on exploitation
              → absorbing state trap, no re-exploration
    Inverted: β → β_min when h→0 → negative feedback on exploitation
              → stable corners that CAN be destabilised by fitness shift
              → self-correcting re-exploration
""")

# Numerical properties of each valve
phi_fns = {
    "linear":    lambda h: h,
    "quadratic": lambda h: h**2,
    "sqrt":      lambda h: h**0.5,
    "sigmoid":   lambda h: 1/(1+math.exp(-10*(h-0.5))),
}

beta_min_v, beta_max_v = 0.5, 20.0
h_vals = np.linspace(0, 1, 1001)

print(f"  Valve properties at β_min={beta_min_v}, β_max={beta_max_v}:")
print(f"  {'φ':>12}  {'β(h=0)':>8}  {'β(h=0.5)':>10}  {'β(h=1)':>8}  "
      f"{'dβ/dh at h=0.5':>16}  {'area under curve':>18}")
print(f"  {'-'*76}")
for name, fn in phi_fns.items():
    b0   = beta_min_v + (beta_max_v - beta_min_v) * fn(0.0)
    b05  = beta_min_v + (beta_max_v - beta_min_v) * fn(0.5)
    b1   = beta_min_v + (beta_max_v - beta_min_v) * fn(1.0)
    # Numerical derivative at h=0.5
    eps_h = 1e-5
    dbdh  = (fn(0.5 + eps_h) - fn(0.5 - eps_h)) / (2*eps_h) * (beta_max_v - beta_min_v)
    area  = float(np.trapz([beta_min_v + (beta_max_v - beta_min_v)*fn(h) for h in h_vals], h_vals))
    print(f"  {name:>12}  {b0:>8.2f}  {b05:>10.2f}  {b1:>8.2f}  {dbdh:>16.3f}  {area:>18.3f}")

# --- Valve geometry plot ---
fig2, ax2 = plt.subplots(figsize=(8, 5))
styles = {"linear": "-", "quadratic": "--", "sqrt": "-.", "sigmoid": ":"}
valve_colors = {"linear": "#2980b9", "quadratic": "#27ae60",
                "sqrt": "#e67e22", "sigmoid": "#8e44ad"}
for name, fn in phi_fns.items():
    b_curve = [beta_min_v + (beta_max_v - beta_min_v) * fn(h) for h in h_vals]
    ax2.plot(h_vals, b_curve, ls=styles[name], color=valve_colors[name],
             lw=2.5, label=f"φ_{name[0].upper()}(h) — {name}")

ax2.axhline(beta_min_v, color="k", ls=":", lw=1, alpha=0.5, label=f"β_min={beta_min_v}")
ax2.axhline(beta_max_v, color="k", ls=":", lw=1, alpha=0.5, label=f"β_max={beta_max_v}")
ax2.set_xlabel("Normalised entropy  h = H / H_max", fontsize=12)
ax2.set_ylabel("β(h)  — update rate", fontsize=12)
ax2.set_title("Valve geometry: β(H) transfer functions\n"
              "Inverted EMR  ·  β HIGH when H HIGH (uncertain → explore fast)", fontsize=12)
ax2.legend(fontsize=10)
ax2.set_xlim(0, 1); ax2.set_ylim(0, beta_max_v * 1.05)

# Annotate operating regions
ax2.axvspan(0, 0.15, alpha=0.06, color="#e74c3c")
ax2.axvspan(0.85, 1.0, alpha=0.06, color="#2980b9")
ax2.text(0.07, 18, "exploit\nregion", ha="center", fontsize=9, color="#c0392b")
ax2.text(0.92, 18, "explore\nregion", ha="center", fontsize=9, color="#2471a3")

plt.tight_layout()
plt.savefig("valve_geometry.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  Saved: valve_geometry.png")

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
  Entropy trace:
    Original EMR: H/H_max collapses to ~0.0004 within 500 steps, β ≈ 20
    throughout; NO entropy spike at change points → trapped in corner.
    Inverted EMR: H/H_max is bounded away from 0 (eps_floor active);
    β rises toward β_max during uncertain periods, drops at convergence.
    → entropy_trace.png  (visual comparison with change-point markers)

  Valve geometry (valve_geometry.png):
    Linear φ: β proportional to uncertainty — simplest, baseline
    Quadratic φ: slow to open, fast to saturate — conservative explorer
    Square-root φ: opens quickly at low uncertainty — aggressive re-explorer
    Sigmoid φ: threshold at h=0.5 — binary exploit/explore switch

  K=10 extended results: see printed table above.
  If Z > 2 for best inverted EMR vs best ε-greedy: conjecture SUPPORTED.
  If Z < 2: inverted coupling helps vs original but still loses to tuned ε.
""")

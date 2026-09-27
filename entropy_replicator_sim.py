"""
entropy_replicator_sim.py

Tests the conjecture:
  An entropy-modulated replicator (EMR) outperforms fixed-ε ε-greedy on
  nonstationary multi-armed bandit problems.

Replicator equation with entropy gate:
  dx_i/dt = β(H) · x_i · (f_i − f̄)
  β(H) = β_min + (β_max − β_min) · (1 − H/H_max)

  β is HIGH when entropy H is LOW  (concentrated distribution → exploit fast)
  β is LOW  when entropy H is HIGH (uniform distribution → explore slowly)

Two environments:
  ENV-A: Random-walk bandit — true means drift by σ_drift each step.
  ENV-B: Abrupt-change bandit — true means reshuffled with prob p_change/step.

Agents compared:
  EMR       : entropy-modulated replicator (the conjecture)
  ε-greedy  : fixed ε ∈ {0.01, 0.05, 0.10, 0.20} (baselines)
  Softmax   : Boltzmann with fixed temperature τ

Metrics:
  — Mean per-step reward (higher = better)
  — Cumulative regret vs oracle best arm (lower = better)
  — Tracking speed: steps to 80% of max reward after a change point
"""

import numpy as np
import math
from collections import defaultdict

RNG_SEED  = 42
K_ARMS    = 5
T_STEPS   = 5000
N_RUNS    = 200
SIGMA_OBS = 1.0          # observation noise
SIGMA_DRIFT = 0.05       # per-step drift σ for ENV-A
P_CHANGE  = 1 / 333      # expected change every 333 steps for ENV-B


# ============================================================
# Environments
# ============================================================

class RandomWalkBandit:
    """ENV-A: true means drift as independent Gaussian random walks."""
    def __init__(self, K, sigma_drift, sigma_obs, rng):
        self.K  = K
        self.sigma_drift = sigma_drift
        self.sigma_obs   = sigma_obs
        self.rng = rng
        self.mu  = rng.normal(0, 1, K)

    def step_env(self):
        self.mu += self.rng.normal(0, self.sigma_drift, self.K)

    def pull(self, arm):
        return self.mu[arm] + self.rng.normal(0, self.sigma_obs)

    def best_arm(self):
        return int(np.argmax(self.mu))

    def best_reward(self):
        return self.mu[self.best_arm()]


class AbruptChangeBandit:
    """ENV-B: true means reshuffled from N(0,1) with prob p_change each step."""
    def __init__(self, K, p_change, sigma_obs, rng):
        self.K  = K
        self.p_change  = p_change
        self.sigma_obs = sigma_obs
        self.rng = rng
        self.mu  = rng.normal(0, 1, K)
        self.change_steps = []
        self._t  = 0

    def step_env(self):
        self._t += 1
        if self.rng.random() < self.p_change:
            self.mu = self.rng.normal(0, 1, self.K)
            self.change_steps.append(self._t)

    def pull(self, arm):
        return self.mu[arm] + self.rng.normal(0, self.sigma_obs)

    def best_arm(self):
        return int(np.argmax(self.mu))

    def best_reward(self):
        return self.mu[self.best_arm()]


# ============================================================
# Agents
# ============================================================

class EMRAgent:
    """Entropy-modulated replicator dynamics."""
    name = "EMR"

    def __init__(self, K, beta_min=0.5, beta_max=20.0, alpha=0.1, eps_floor=1e-6):
        self.K        = K
        self.beta_min = beta_min
        self.beta_max = beta_max
        self.alpha    = alpha       # reward EMA learning rate
        self.eps_floor = eps_floor
        self.reset()

    def reset(self):
        self.x     = np.ones(self.K) / self.K
        self.f_hat = np.zeros(self.K)

    def entropy(self):
        x = np.clip(self.x, 1e-300, 1)
        return -float(np.sum(x * np.log(x)))

    def beta(self):
        H     = self.entropy()
        H_max = math.log(self.K)
        h     = H / H_max if H_max > 0 else 0.0
        return self.beta_min + (self.beta_max - self.beta_min) * (1.0 - h)

    def choose(self, rng):
        # Sample arm according to current population distribution
        return int(rng.choice(self.K, p=self.x))

    def update(self, arm, reward):
        # Update reward estimate via EMA
        self.f_hat[arm] += self.alpha * (reward - self.f_hat[arm])
        # Replicator update
        b    = self.beta()
        f_bar = float(np.dot(self.x, self.f_hat))
        dx   = b * self.x * (self.f_hat - f_bar)
        self.x = self.x + dx
        # Clip and renormalize
        self.x = np.maximum(self.x, self.eps_floor)
        self.x /= self.x.sum()


class EpsilonGreedyAgent:
    """Standard ε-greedy with exponential EMA reward estimates."""

    def __init__(self, K, epsilon, alpha=0.1):
        self.K       = K
        self.epsilon = epsilon
        self.alpha   = alpha
        self.name    = f"ε-greedy(ε={epsilon})"
        self.reset()

    def reset(self):
        self.f_hat = np.zeros(self.K)

    def choose(self, rng):
        if rng.random() < self.epsilon:
            return int(rng.integers(self.K))
        return int(np.argmax(self.f_hat))

    def update(self, arm, reward):
        self.f_hat[arm] += self.alpha * (reward - self.f_hat[arm])


class SoftmaxAgent:
    """Boltzmann / softmax with fixed temperature τ."""

    def __init__(self, K, tau=1.0, alpha=0.1):
        self.K     = K
        self.tau   = tau
        self.alpha = alpha
        self.name  = f"Softmax(τ={tau})"
        self.reset()

    def reset(self):
        self.f_hat = np.zeros(self.K)

    def choose(self, rng):
        logits = self.f_hat / self.tau
        logits -= logits.max()
        probs  = np.exp(logits)
        probs /= probs.sum()
        return int(rng.choice(self.K, p=probs))

    def update(self, arm, reward):
        self.f_hat[arm] += self.alpha * (reward - self.f_hat[arm])


# ============================================================
# Runner
# ============================================================

def run_bandit(env_factory, agents, T, N_runs, seed=RNG_SEED):
    """
    Run N_runs episodes.  Returns:
      rewards[agent_name] : (N_runs, T) array of per-step rewards
      regrets[agent_name] : (N_runs, T) array of per-step regret
    """
    rewards = {a.name: np.zeros((N_runs, T)) for a in agents}
    regrets = {a.name: np.zeros((N_runs, T)) for a in agents}

    for run in range(N_runs):
        rng = np.random.default_rng(seed + run * 997)
        env = env_factory(rng)
        for a in agents:
            a.reset()

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
# Setup
# ============================================================

eps_values = [0.01, 0.05, 0.10, 0.20]

def make_emr():
    return EMRAgent(K_ARMS, beta_min=0.5, beta_max=20.0, alpha=0.1)

agents_A = [make_emr()] + [EpsilonGreedyAgent(K_ARMS, e) for e in eps_values] + \
           [SoftmaxAgent(K_ARMS, tau=0.5), SoftmaxAgent(K_ARMS, tau=1.0)]

agents_B = [make_emr()] + [EpsilonGreedyAgent(K_ARMS, e) for e in eps_values] + \
           [SoftmaxAgent(K_ARMS, tau=0.5), SoftmaxAgent(K_ARMS, tau=1.0)]


# ============================================================
# ENV-A: Random Walk
# ============================================================
print("=" * 70)
print("ENV-A: Random-Walk Bandit")
print(f"  K={K_ARMS} arms, T={T_STEPS} steps, {N_RUNS} runs")
print(f"  σ_drift={SIGMA_DRIFT}/step, σ_obs={SIGMA_OBS}")
print("=" * 70)

def env_A_factory(rng):
    return RandomWalkBandit(K_ARMS, SIGMA_DRIFT, SIGMA_OBS, rng)

rews_A, regs_A = run_bandit(env_A_factory, agents_A, T_STEPS, N_RUNS)

# Summary statistics
print(f"\n  {'Agent':>22}  {'Mean reward':>12}  {'±SE':>8}  "
      f"{'Cum. regret':>12}  {'±SE':>8}")
print(f"  {'-'*68}")

results_A = {}
for agent in agents_A:
    nm = agent.name
    mean_rew = rews_A[nm].mean(axis=1)        # per-run mean reward
    cum_reg  = regs_A[nm].sum(axis=1)          # per-run cumulative regret
    r_m, r_se = mean_rew.mean(), mean_rew.std() / math.sqrt(N_RUNS)
    g_m, g_se = cum_reg.mean(),  cum_reg.std()  / math.sqrt(N_RUNS)
    results_A[nm] = (r_m, r_se, g_m, g_se)
    print(f"  {nm:>22}  {r_m:>12.4f}  {r_se:>8.4f}  {g_m:>12.1f}  {g_se:>8.1f}")

# Best baseline
best_eps_name = min(
    [f"ε-greedy(ε={e})" for e in eps_values],
    key=lambda nm: results_A[nm][2]   # lowest cum regret
)
emr_name = "EMR"
emr_g, emr_g_se   = results_A[emr_name][2],       results_A[emr_name][3]
best_g, best_g_se = results_A[best_eps_name][2],   results_A[best_eps_name][3]

diff_g  = best_g - emr_g      # positive = EMR better
z_score = diff_g / math.sqrt(emr_g_se**2 + best_g_se**2)

print(f"\n  Best ε-greedy baseline: {best_eps_name}")
print(f"  EMR cum. regret:  {emr_g:.1f} ± {emr_g_se:.1f}")
print(f"  Best ε-greedy:    {best_g:.1f} ± {best_g_se:.1f}")
print(f"  Difference:       {diff_g:.1f}  (positive = EMR lower regret)")
print(f"  Z-score:          {z_score:+.2f}  "
      f"({'SIGNIFICANT (|Z|>2)' if abs(z_score) > 2 else 'not significant'})")

# Late-stage performance (last 20% of steps)
late_start = int(0.8 * T_STEPS)
print(f"\n  Late-stage reward (t={late_start}..{T_STEPS}):")
print(f"  {'Agent':>22}  {'Mean reward':>12}  {'±SE':>8}")
print(f"  {'-'*44}")
for agent in agents_A:
    nm = agent.name
    late_rew = rews_A[nm][:, late_start:].mean(axis=1)
    print(f"  {nm:>22}  {late_rew.mean():>12.4f}  {late_rew.std()/math.sqrt(N_RUNS):>8.4f}")


# ============================================================
# ENV-B: Abrupt Change
# ============================================================
print()
print("=" * 70)
print("ENV-B: Abrupt-Change Bandit")
print(f"  K={K_ARMS} arms, T={T_STEPS} steps, {N_RUNS} runs")
print(f"  p_change={P_CHANGE:.4f}/step (~{1/P_CHANGE:.0f} steps between changes)")
print("=" * 70)

def env_B_factory(rng):
    return AbruptChangeBandit(K_ARMS, P_CHANGE, SIGMA_OBS, rng)

rews_B, regs_B = run_bandit(env_B_factory, agents_B, T_STEPS, N_RUNS)

print(f"\n  {'Agent':>22}  {'Mean reward':>12}  {'±SE':>8}  "
      f"{'Cum. regret':>12}  {'±SE':>8}")
print(f"  {'-'*68}")

results_B = {}
for agent in agents_B:
    nm = agent.name
    mean_rew = rews_B[nm].mean(axis=1)
    cum_reg  = regs_B[nm].sum(axis=1)
    r_m, r_se = mean_rew.mean(), mean_rew.std() / math.sqrt(N_RUNS)
    g_m, g_se = cum_reg.mean(),  cum_reg.std()  / math.sqrt(N_RUNS)
    results_B[nm] = (r_m, r_se, g_m, g_se)
    print(f"  {nm:>22}  {r_m:>12.4f}  {r_se:>8.4f}  {g_m:>12.1f}  {g_se:>8.1f}")

best_eps_name_B = min(
    [f"ε-greedy(ε={e})" for e in eps_values],
    key=lambda nm: results_B[nm][2]
)
emr_g_B, emr_g_se_B   = results_B[emr_name][2], results_B[emr_name][3]
best_g_B, best_g_se_B = results_B[best_eps_name_B][2], results_B[best_eps_name_B][3]

diff_g_B  = best_g_B - emr_g_B
z_score_B = diff_g_B / math.sqrt(emr_g_se_B**2 + best_g_se_B**2)

print(f"\n  Best ε-greedy baseline: {best_eps_name_B}")
print(f"  EMR cum. regret:  {emr_g_B:.1f} ± {emr_g_se_B:.1f}")
print(f"  Best ε-greedy:    {best_g_B:.1f} ± {best_g_se_B:.1f}")
print(f"  Difference:       {diff_g_B:.1f}  (positive = EMR lower regret)")
print(f"  Z-score:          {z_score_B:+.2f}  "
      f"({'SIGNIFICANT (|Z|>2)' if abs(z_score_B) > 2 else 'not significant'})")


# ============================================================
# EMR Internal State Analysis — entropy trajectory
# ============================================================
print()
print("=" * 70)
print("EMR Internal State — entropy trajectory (single run)")
print("=" * 70)

rng_trace = np.random.default_rng(RNG_SEED)
env_trace = AbruptChangeBandit(K_ARMS, P_CHANGE, SIGMA_OBS, rng_trace)
emr_trace = EMRAgent(K_ARMS, beta_min=0.5, beta_max=20.0, alpha=0.1)

entropy_traj = []
beta_traj    = []
reward_traj  = []
best_arm_traj = []
chosen_arm_traj = []

for t in range(T_STEPS):
    env_trace.step_env()
    arm = emr_trace.choose(rng_trace)
    r   = env_trace.pull(arm)
    emr_trace.update(arm, r)

    entropy_traj.append(emr_trace.entropy())
    beta_traj.append(emr_trace.beta())
    reward_traj.append(r)
    best_arm_traj.append(env_trace.best_arm())
    chosen_arm_traj.append(arm)

H_max = math.log(K_ARMS)
print(f"\n  H_max = log({K_ARMS}) = {H_max:.4f}")
print(f"\n  {'Window':>20}  {'Mean H':>8}  {'H/H_max':>8}  "
      f"{'Mean β':>8}  {'Mean reward':>12}  {'Best-arm %':>12}")
print(f"  {'-'*72}")

windows = [
    ("t=0..499",      0,    500),
    ("t=500..1499",   500,  1500),
    ("t=1500..2999",  1500, 3000),
    ("t=3000..4999",  3000, 5000),
]
for wname, wa, wb in windows:
    H_w = np.mean(entropy_traj[wa:wb])
    b_w = np.mean(beta_traj[wa:wb])
    r_w = np.mean(reward_traj[wa:wb])
    acc = np.mean([chosen_arm_traj[t] == best_arm_traj[t] for t in range(wa, wb)])
    print(f"  {wname:>20}  {H_w:>8.4f}  {H_w/H_max:>8.4f}  {b_w:>8.4f}  "
          f"{r_w:>12.4f}  {acc*100:>11.1f}%")

# Show entropy spikes near change points
change_steps = env_trace.change_steps[:5]
print(f"\n  Entropy near change points (first {len(change_steps)} changes):")
print(f"  {'step':>6}  {'H(t-5)':>8}  {'H(t)':>8}  {'H(t+5)':>8}  "
      f"{'H(t+20)':>9}  {'H(t+50)':>9}")
print(f"  {'-'*52}")
for cs in change_steps:
    def safe_H(i):
        return f"{entropy_traj[i]:.4f}" if 0 <= i < T_STEPS else "  —"
    print(f"  {cs:>6}  {safe_H(cs-5):>8}  {safe_H(cs):>8}  "
          f"{safe_H(cs+5):>8}  {safe_H(cs+20):>9}  {safe_H(cs+50):>9}")


# ============================================================
# β sensitivity analysis
# ============================================================
print()
print("=" * 70)
print("β Sensitivity — ENV-A, varying β_max")
print("=" * 70)

print(f"\n  {'β_max':>8}  {'β_min':>8}  {'Mean reward':>12}  {'±SE':>8}  "
      f"{'Cum. regret':>12}  {'±SE':>8}")
print(f"  {'-'*60}")

for bmax in [2.0, 5.0, 10.0, 20.0, 50.0]:
    agents_sens = [EMRAgent(K_ARMS, beta_min=0.5, beta_max=bmax, alpha=0.1)]
    rews_s, regs_s = run_bandit(env_A_factory, agents_sens, T_STEPS, N_RUNS // 2)
    nm = agents_sens[0].name
    mr = rews_s[nm].mean(axis=1)
    cr = regs_s[nm].sum(axis=1)
    print(f"  {bmax:>8.1f}  {'0.5':>8}  {mr.mean():>12.4f}  "
          f"{mr.std()/math.sqrt(N_RUNS//2):>8.4f}  "
          f"{cr.mean():>12.1f}  {cr.std()/math.sqrt(N_RUNS//2):>8.1f}")


# ============================================================
# Summary
# ============================================================
print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)

def verdict(z):
    if z > 3:   return "STRONG (Z>3) — conjecture supported"
    if z > 2:   return "MODERATE (Z>2) — conjecture supported"
    if z > 1:   return "WEAK (Z>1) — inconclusive"
    if z > 0:   return "TREND only — not significant"
    return "NEGATIVE — conjecture fails"

print(f"""
  Conjecture: entropy-modulated replicator (EMR) outperforms
  fixed-ε ε-greedy on nonstationary bandit problems.

  ENV-A (Random Walk, σ_drift={SIGMA_DRIFT}):
    Best ε-greedy: {best_eps_name}
    EMR vs best ε-greedy: cum. regret Δ={diff_g:.1f}, Z={z_score:+.2f}
    Verdict: {verdict(z_score)}

  ENV-B (Abrupt Change, p={P_CHANGE:.4f}/step):
    Best ε-greedy: {best_eps_name_B}
    EMR vs best ε-greedy: cum. regret Δ={diff_g_B:.1f}, Z={z_score_B:+.2f}
    Verdict: {verdict(z_score_B)}

  If Z < 2 on both environments: conjecture is not supported —
  the entropy gate does not provide measurable advantage over
  optimally-tuned fixed-ε at these parameters.

  If Z > 2 on either: conjecture is supported — next step is
  to characterize which environments benefit most (high vs low
  drift rate, abrupt vs gradual change).
""")

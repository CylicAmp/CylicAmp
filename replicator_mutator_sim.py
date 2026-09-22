"""
replicator_mutator_sim.py

Implements the replicator-mutator equation:
  ẋᵢ = β(H)·xᵢ·(f̂ᵢ − f̄)  +  μ(t)·(1/K − xᵢ)
        ^^^^^^^^^^^^^^^^^^^     ^^^^^^^^^^^^^^^^^^^
        selection pressure       mutation restoring force

The mutation term removes absorbing corners — the failure mode of the
pure replicator.  β(H) uses the inverted (√φ) valve: HIGH when H HIGH.

Pisano kick: at every t ≡ 0 (mod 24) where H < 0.55·H_max, inject a
larger mutation pulse.  Period 24 = π(Fib mod 12), the Pisano period
for mod-12 Fibonacci (established in cumsum_triangle_audit.py).

Named constant:
  α_OAM = 90 + 30√5  ≈ 157.082  ≈ 50π  (proximity noted; NOT derived here)
  Used as mutation gain: μ_kick = 1/α_OAM ≈ 0.00637 per step.

Epistemic label on α_OAM:
  [CONJECTURE] α_OAM = 90+30√5 as an OAM coupling constant is plausible
  but has not been derived from any Hamiltonian or physical system in
  this session.  Its proximity to 50π is a numerical coincidence of
  the same character as s(5)=314≈100π (cumsum_correction_audit.py).
  Using it here as a named hyperparameter to test whether its value
  produces any empirically notable effect.

Stress test: K=20, T=10 000, 200 runs, ENV-A and ENV-B.
"""

import numpy as np
import math

# ── Named constants ──────────────────────────────────────────────────────────
PISANO_12  = 24                        # Pisano period π(Fib mod 12)
ALPHA_OAM  = 90.0 + 30.0 * math.sqrt(5)   # 90+30√5 ≈ 157.082 ≈ 50π
MU_KICK    = 1.0 / ALPHA_OAM          # ≈ 0.006365 per step (Pisano pulse)

print(f"  α_OAM = 90+30√5 = {ALPHA_OAM:.10f}")
print(f"  50·π  =          {50*math.pi:.10f}")
print(f"  gap   =          {abs(ALPHA_OAM - 50*math.pi):.2e}  "
      f"(≈{abs(ALPHA_OAM-50*math.pi)/(50*math.pi)*100:.4f}%)")
print(f"  μ_kick = 1/α_OAM = {MU_KICK:.8f}")
print(f"  Pisano period = {PISANO_12} steps\n")

RNG_SEED    = 42
SIGMA_OBS   = 1.0
SIGMA_DRIFT = 0.05
P_CHANGE    = 1.0 / 333


# ── Environments ─────────────────────────────────────────────────────────────

class RandomWalkBandit:
    def __init__(self, K, rng):
        self.K, self.rng = K, rng
        self.mu = rng.normal(0, 1, K)
    def step_env(self):
        self.mu += self.rng.normal(0, SIGMA_DRIFT, self.K)
    def pull(self, arm):
        return self.mu[arm] + self.rng.normal(0, SIGMA_OBS)
    def best_reward(self): return float(self.mu.max())


class AbruptChangeBandit:
    def __init__(self, K, rng):
        self.K, self.rng = K, rng
        self.mu = rng.normal(0, 1, K)
        self._t = 0; self.change_steps = []
    def step_env(self):
        self._t += 1
        if self.rng.random() < P_CHANGE:
            self.mu = self.rng.normal(0, 1, self.K)
            self.change_steps.append(self._t)
    def pull(self, arm):
        return self.mu[arm] + self.rng.normal(0, SIGMA_OBS)
    def best_reward(self): return float(self.mu.max())


# ── Agents ───────────────────────────────────────────────────────────────────

class ReplicatorMutatorAgent:
    """
    Full replicator-mutator with inverted β(H) valve.

    Discrete update (Euler step, dt=1):
      x  ← x + β(H)·x·(f̂ − f̄)         [selection]
          + μ(t)·(1/K − x)               [mutation toward uniform]
      x  ← clip(x, ε_floor) / sum(x)    [normalise]

    β(H): inverted valve, φ = √(H/H_max)
      β HIGH when H HIGH  (uncertain → fast adaptation)
      β LOW  when H LOW   (confident → stable exploitation)

    μ(t): Pisano-period kick
      = μ_base                            always
      + μ_kick  if (t mod 24 == 0) and H < kick_thresh·H_max
    """

    def __init__(self, K, beta_min=0.5, beta_max=20.0, alpha_lr=0.1,
                 mu_base=0.02, mu_kick=MU_KICK,
                 kick_thresh=0.55, kick_period=PISANO_12,
                 phi="sqrt", eps_floor=1e-8):
        self.K          = K
        self.beta_min   = beta_min
        self.beta_max   = beta_max
        self.alpha_lr   = alpha_lr
        self.mu_base    = mu_base
        self.mu_kick    = mu_kick
        self.kick_thresh = kick_thresh
        self.kick_period = kick_period
        self.phi        = phi
        self.eps_floor  = eps_floor
        self.name = (f"RM(β={beta_min}–{beta_max},μ={mu_base},"
                     f"kick={mu_kick:.4f},φ={phi})")
        self.reset()

    def reset(self):
        self.x     = np.ones(self.K) / self.K
        self.f_hat = np.zeros(self.K)
        self._t    = 0

    def entropy(self):
        x = np.clip(self.x, 1e-300, 1)
        return -float(np.sum(x * np.log(x)))

    def beta(self):
        H = self.entropy()
        H_max = math.log(self.K)
        h = H / H_max if H_max > 0 else 0.0
        phi_val = math.sqrt(h) if self.phi == "sqrt" else h
        return self.beta_min + (self.beta_max - self.beta_min) * phi_val

    def mu_t(self):
        """Mutation rate at current step: base + Pisano kick if H is low."""
        mu = self.mu_base
        H_max = math.log(self.K)
        if (self._t % self.kick_period == 0
                and self.entropy() < self.kick_thresh * H_max):
            mu += self.mu_kick
        return mu

    def choose(self, rng):
        return int(rng.choice(self.K, p=self.x))

    def update(self, arm, reward):
        self._t += 1
        self.f_hat[arm] += self.alpha_lr * (reward - self.f_hat[arm])

        b     = self.beta()
        f_bar = float(np.dot(self.x, self.f_hat))
        mu    = self.mu_t()

        # Selection + mutation
        dx_sel  = b  * self.x * (self.f_hat - f_bar)
        dx_mut  = mu * (np.ones(self.K) / self.K - self.x)
        self.x  = self.x + dx_sel + dx_mut

        self.x  = np.maximum(self.x, self.eps_floor)
        self.x /= self.x.sum()


class EpsilonGreedyAgent:
    def __init__(self, K, epsilon, alpha_lr=0.1):
        self.K, self.epsilon, self.alpha_lr = K, epsilon, alpha_lr
        self.name = f"ε-greedy(ε={epsilon})"
        self.reset()
    def reset(self): self.f_hat = np.zeros(self.K)
    def choose(self, rng):
        return (int(rng.integers(self.K)) if rng.random() < self.epsilon
                else int(np.argmax(self.f_hat)))
    def update(self, arm, reward):
        self.f_hat[arm] += self.alpha_lr * (reward - self.f_hat[arm])


class SoftmaxAgent:
    def __init__(self, K, tau=0.5, alpha_lr=0.1):
        self.K, self.tau, self.alpha_lr = K, tau, alpha_lr
        self.name = f"Softmax(τ={tau})"
        self.reset()
    def reset(self): self.f_hat = np.zeros(self.K)
    def choose(self, rng):
        logits = self.f_hat / self.tau; logits -= logits.max()
        probs  = np.exp(logits); probs /= probs.sum()
        return int(rng.choice(self.K, p=probs))
    def update(self, arm, reward):
        self.f_hat[arm] += self.alpha_lr * (reward - self.f_hat[arm])


# ── Runner ───────────────────────────────────────────────────────────────────

def run_bandit(env_cls, agents, T, N_runs, seed=RNG_SEED):
    rewards = {a.name: np.zeros((N_runs, T)) for a in agents}
    regrets = {a.name: np.zeros((N_runs, T)) for a in agents}
    for run in range(N_runs):
        rng = np.random.default_rng(seed + run * 997)
        env = env_cls(len(agents[0].f_hat if hasattr(agents[0], 'f_hat')
                         else agents[0].x), rng)
        for a in agents: a.reset()
        for t in range(T):
            env.step_env()
            best_r = env.best_reward()
            for ag in agents:
                arm = ag.choose(rng)
                r   = env.pull(arm)
                ag.update(arm, r)
                rewards[ag.name][run, t] = r
                regrets[ag.name][run, t] = best_r - r
    return rewards, regrets


def run_bandit_fixed_K(env_cls, agents, K, T, N_runs, seed=RNG_SEED):
    rewards = {a.name: np.zeros((N_runs, T)) for a in agents}
    regrets = {a.name: np.zeros((N_runs, T)) for a in agents}
    for run in range(N_runs):
        rng = np.random.default_rng(seed + run * 997)
        env = env_cls(K, rng)
        for a in agents: a.reset()
        for t in range(T):
            env.step_env()
            best_r = env.best_reward()
            for ag in agents:
                arm = ag.choose(rng)
                r   = env.pull(arm)
                ag.update(arm, r)
                rewards[ag.name][run, t] = r
                regrets[ag.name][run, t] = best_r - r
    return rewards, regrets


def print_results(agents, rewards, regrets, N_runs, T, label):
    print(f"\n  {label}")
    print(f"  {'Agent':>40}  {'Mean reward':>12}  {'±SE':>8}  "
          f"{'Cum. regret':>13}  {'±SE':>8}")
    print(f"  {'-'*88}")
    results = {}
    for ag in agents:
        nm = ag.name
        mr = rewards[nm].mean(axis=1); cr = regrets[nm].sum(axis=1)
        r_m, r_se = mr.mean(), mr.std() / math.sqrt(N_runs)
        g_m, g_se = cr.mean(), cr.std()  / math.sqrt(N_runs)
        results[nm] = (r_m, r_se, g_m, g_se)
        print(f"  {nm:>40}  {r_m:>12.4f}  {r_se:>8.4f}  "
              f"{g_m:>13.1f}  {g_se:>8.1f}")
    return results


# ══════════════════════════════════════════════════════════════════════════════
# PART 1  —  Single 10 000-step trace with exact numbers
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 70)
print("PART 1.  Single 10 000-step trace  (K=10, ENV-B)")
print("=" * 70)

K_TRACE  = 10
T_TRACE  = 10_000
rng_tr   = np.random.default_rng(RNG_SEED)
env_tr   = AbruptChangeBandit(K_TRACE, rng_tr)
ag_tr    = ReplicatorMutatorAgent(K_TRACE, beta_min=0.5, beta_max=20.0,
                                   alpha_lr=0.1, mu_base=0.02,
                                   mu_kick=MU_KICK, phi="sqrt")

H_max_k  = math.log(K_TRACE)
rows     = []
for t in range(T_TRACE):
    env_tr.step_env()
    arm = ag_tr.choose(rng_tr)
    r   = env_tr.pull(arm)
    ag_tr.update(arm, r)
    rows.append({
        "t":      t + 1,
        "H":      ag_tr.entropy(),
        "h":      ag_tr.entropy() / H_max_k,
        "beta":   ag_tr.beta(),
        "mu":     ag_tr.mu_t(),
        "reward": r,
        "arm":    arm,
        "x_max":  float(ag_tr.x.max()),
        "x_min":  float(ag_tr.x.min()),
    })

# Print table at key timesteps
key_ts = ([1, 5, 10, 24, 25, 48, 50, 100, 200]
          + list(range(500, T_TRACE + 1, 500))
          + [cs for cs in env_tr.change_steps if cs < T_TRACE])
key_ts = sorted(set(key_ts))

print(f"\n  H_max = ln({K_TRACE}) = {H_max_k:.6f}")
print(f"  α_OAM = {ALPHA_OAM:.6f}  →  μ_kick = {MU_KICK:.8f}")
print(f"  Pisano period = {PISANO_12}, kick threshold h < {0.55:.2f}")
print()
print(f"  {'t':>6}  {'H':>8}  {'h=H/Hmax':>10}  {'β(h)':>8}  "
      f"{'μ(t)':>10}  {'reward':>8}  {'arm':>4}  {'x_max':>8}  {'x_min':>10}  note")
print(f"  {'-'*96}")

change_set = set(env_tr.change_steps)
for row in rows:
    t = row["t"]
    if t not in key_ts:
        continue
    note = ""
    if t in change_set:    note = "← CHANGE"
    if t % PISANO_12 == 0: note += "  [Pisano t]"
    print(f"  {t:>6}  {row['H']:>8.5f}  {row['h']:>10.5f}  {row['beta']:>8.4f}  "
          f"{row['mu']:>10.6f}  {row['reward']:>8.4f}  {row['arm']:>4}  "
          f"{row['x_max']:>8.5f}  {row['x_min']:>10.8f}  {note}")

# Entropy at change points
print(f"\n  Change points and entropy response:")
print(f"  {'cs':>6}  {'H(cs-5)':>9}  {'H(cs)':>9}  {'H(cs+5)':>9}  "
      f"{'H(cs+24)':>10}  {'H(cs+100)':>11}  recovery?")
print(f"  {'-'*72}")
for cs in env_tr.change_steps[:8]:
    def hval(offset):
        idx = cs - 1 + offset
        return rows[idx]["H"] if 0 <= idx < len(rows) else float("nan")
    h0  = hval(0); h_5 = hval(-5); h5 = hval(5)
    h24 = hval(24); h100 = hval(100)
    recovered = h100 > h0 * 0.5 and hval(100) > 0.01
    print(f"  {cs:>6}  {h_5:>9.5f}  {h0:>9.5f}  {h5:>9.5f}  "
          f"{h24:>10.5f}  {h100:>11.5f}  {'YES' if recovered else 'no'}")

# Summary stats for the trace
H_arr = np.array([r["H"] for r in rows])
b_arr = np.array([r["beta"] for r in rows])
r_arr = np.array([r["reward"] for r in rows])
print(f"\n  Full trace statistics (t=1..{T_TRACE}):")
print(f"    H:       mean={H_arr.mean():.5f}  min={H_arr.min():.5f}  "
      f"max={H_arr.max():.5f}  H/H_max_mean={H_arr.mean()/H_max_k:.4f}")
print(f"    β:       mean={b_arr.mean():.4f}  min={b_arr.min():.4f}  "
      f"max={b_arr.max():.4f}")
print(f"    Reward:  mean={r_arr.mean():.4f}  last 1k mean={r_arr[-1000:].mean():.4f}")
print(f"    Pisano kicks fired: "
      f"{sum(1 for r in rows if r['t'] % PISANO_12 == 0 and r['mu'] > 0.02)}")
print(f"    Change points encountered: {len(env_tr.change_steps)}")


# ══════════════════════════════════════════════════════════════════════════════
# PART 2  —  K=20 stress test, 200 runs
# ══════════════════════════════════════════════════════════════════════════════
print()
print("=" * 70)
print(f"PART 2.  K=20 stress test  (T=10 000, 200 runs)")
print("=" * 70)

K20  = 20
T20  = 10_000
N20  = 200

agents_20 = [
    ReplicatorMutatorAgent(K20, beta_min=0.5, beta_max=20.0, alpha_lr=0.1,
                            mu_base=0.02, mu_kick=MU_KICK, phi="sqrt"),
    ReplicatorMutatorAgent(K20, beta_min=0.5, beta_max=20.0, alpha_lr=0.1,
                            mu_base=0.05, mu_kick=MU_KICK, phi="sqrt"),
    ReplicatorMutatorAgent(K20, beta_min=0.5, beta_max=20.0, alpha_lr=0.1,
                            mu_base=0.00, mu_kick=MU_KICK, phi="sqrt"),  # kick only
    EpsilonGreedyAgent(K20, epsilon=0.05),
    EpsilonGreedyAgent(K20, epsilon=0.10),
    EpsilonGreedyAgent(K20, epsilon=0.20),
    SoftmaxAgent(K20, tau=0.5),
]

for env_cls, env_label in [(RandomWalkBandit, "ENV-A random walk"),
                            (AbruptChangeBandit, "ENV-B abrupt change")]:
    rews, regs = run_bandit_fixed_K(env_cls, agents_20, K20, T20, N20)
    results_20 = print_results(agents_20, rews, regs, N20, T20,
                                f"{env_label}  (K={K20}, T={T20}, N={N20})")

    rm_names  = [a.name for a in agents_20 if "RM(" in a.name]
    eps_names = [a.name for a in agents_20 if "ε-greedy" in a.name]
    best_rm   = min(rm_names,  key=lambda nm: results_20[nm][2])
    best_eps  = min(eps_names, key=lambda nm: results_20[nm][2])
    diff = results_20[best_eps][2] - results_20[best_rm][2]
    se   = math.sqrt(results_20[best_rm][3]**2 + results_20[best_eps][3]**2)
    Z    = diff / se
    print(f"\n  Best RM agent : {best_rm}")
    print(f"    regret = {results_20[best_rm][2]:.1f}")
    print(f"  Best ε-greedy : {best_eps}")
    print(f"    regret = {results_20[best_eps][2]:.1f}")
    print(f"  Δregret = {diff:.1f}  Z = {Z:+.2f}  "
          f"→  {'RM WINS ✓' if Z > 2 else 'RM LOSES ✗' if Z < -2 else 'inconclusive'}")


# ══════════════════════════════════════════════════════════════════════════════
# PART 3  —  α_OAM parameter mapping
# ══════════════════════════════════════════════════════════════════════════════
print()
print("=" * 70)
print("PART 3.  α_OAM = 90+30√5 parameter mapping")
print("=" * 70)
print(f"""
  α_OAM = 90 + 30√5 = {ALPHA_OAM:.10f}
  50·π              = {50*math.pi:.10f}
  Gap               = {abs(ALPHA_OAM-50*math.pi):.6f}  ({abs(ALPHA_OAM-50*math.pi)/(50*math.pi)*100:.5f}%)

  [CONJECTURE — epistemic status]:
  The proximity α_OAM ≈ 50π is a numerical coincidence. The expression
  90+30√5 = 30(3+√5) = 30·(2φ+1) where φ=(1+√5)/2 is the golden ratio.
  So: α_OAM = 30(2φ+1) = 60φ + 30.
  This connects to the golden ratio φ but NOT to π structurally.
  Proximity to 50π: 0.0016% — same order as s(5)≈100π (0.05%).

  Role in the replicator-mutator:
    μ_kick = 1/α_OAM = 1/(30(2φ+1)) ≈ {1/ALPHA_OAM:.8f} per step

  This is the mutation strength during a Pisano kick. Numerically it is
  a small perturbation (~0.64% of μ_base=0.1). Its effect is testable
  but it is NOT the OAM coupling constant of any physical system in
  this session. The "OAM dipole" connection to PdGa or Mach-Zehnder
  requires a derivation from the system Hamiltonian that we do not have.

  What α_OAM parametrises in the replicator-mutator:
""")

# Sensitivity sweep on μ_kick around α_OAM-derived value
K_sens = 10; T_sens = 5000; N_sens = 100
print(f"  μ_kick sensitivity (K={K_sens}, T={T_sens}, N={N_sens} runs, ENV-B):")
print(f"  {'μ_kick':>10}  {'note':>20}  {'cum regret':>12}  {'±SE':>8}")
print(f"  {'-'*56}")

kick_vals = [0.0, MU_KICK/10, MU_KICK, MU_KICK*10, MU_KICK*100]
kick_labels = ["0 (no kick)", "α_OAM÷10", "1/α_OAM", "α_OAM×10⁻¹", "α_OAM×10⁻²×10²"]

for kv, kl in zip(kick_vals, kick_labels):
    ag_s = [ReplicatorMutatorAgent(K_sens, mu_base=0.02, mu_kick=kv, phi="sqrt")]
    rws, rgs = run_bandit_fixed_K(AbruptChangeBandit, ag_s, K_sens, T_sens, N_sens)
    nm = ag_s[0].name
    cr = rgs[nm].sum(axis=1)
    print(f"  {kv:>10.6f}  {kl:>20}  {cr.mean():>12.1f}  "
          f"{cr.std()/math.sqrt(N_sens):>8.1f}")

print(f"""
  [If the α_OAM-derived μ_kick is empirically optimal (lowest regret),
   the conjecture gains support. If it is indistinguishable from nearby
   values, it is a free parameter with no privileged status.]
""")

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
  Replicator-mutator equation:
    ẋᵢ = β(H)·xᵢ·(f̂ᵢ−f̄) + μ(t)·(1/K−xᵢ)

  The mutation term (μ·(1/K−xᵢ)) resolves the absorbing-corner failure
  of the pure replicator by maintaining a permanent restoring force
  toward the uniform distribution.

  Pisano kick: every 24 steps (π(Fib mod 12)), if H < 0.55·H_max,
  add μ_kick = 1/α_OAM ≈ {MU_KICK:.6f} to the mutation rate.

  α_OAM = 90+30√5 = 30(2φ+1) ≈ 50π:
    Algebraically: 30·(2φ+1) where φ = golden ratio.
    Numerically: ≈ 50π (0.0016% gap — numerical coincidence).
    Status: [CONJECTURE] as OAM coupling; [PROVEN] as algebraic identity.

  K=20 stress test results: see table above.
  The mutation term was the critical fix. Whether it beats tuned ε-greedy
  depends on the environment — the data will answer that.
""")

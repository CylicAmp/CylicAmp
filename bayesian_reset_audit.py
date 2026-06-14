"""
bayesian_reset_audit.py

Tests whether adding a conditional Bayesian-style reset to ODE-RM
improves performance over EXP3+mutation on ENV-Cv2 (K=20, switch_every=500).

Definition: Bayesian Reset
  After each ODE-RM step, if entropy fraction h = H/H_max < reset_thresh,
  blend reset_frac of probability mass back to uniform:
    x = (1 - reset_frac)*x + reset_frac*(1/K)

Result [PROVEN]: all Bayesian Reset variants lose to EXP3+mutation (Z > 8).

  Agent                    Mean regret   SE    vs EXP3+mut
  ---------------------------------------------------------
  EXP3+mut (baseline)         1335.9   12.6   --
  ODE-RM (no reset)           1701.9   41.6   Z=+8.4 LOSES
  BR(thr=0.05, f=0.3)         1921.8   33.5   Z=+16  LOSES
  BR(thr=0.10, f=0.3)         1888.4   32.3   Z=+16  LOSES
  BR(thr=0.20, f=0.3)         1734.3   30.3   Z=+12  LOSES
  BR(thr=0.10, f=0.5)         2137.1   33.8   Z=+22  LOSES
  BR(thr=0.10, f=0.1)         1702.0   43.4   Z=+8.1 LOSES
  EG                          4595.2   15.2   Z=+165 LOSES

Why: conditional hard resets disrupt exploitation during windows when ODE-RM
has correctly converged on the best arm. EXP3+mutation's continuous geometric
mixing (0.99*w + 0.01/K per step) achieves the same forgetting effect without
discontinuous bursts that force re-learning from scratch.

Falsification attempted: no threshold/fraction combination was found that
beats EXP3+mutation on this environment. The Bayesian Reset architecture
is not the missing piece.
"""

import numpy as np
from scipy import stats

T, K = 10000, 20


def run_env_cv2(seed, switch_every=500, agent='exp3',
                reset_thresh=0.1, reset_frac=0.3,
                mu_base=0.05, mu_kick=1/24, kick_period=24, kick_thresh=0.55,
                beta_min=0.5, beta_max=20.0, alpha_lr=0.1, eps_floor=1e-6):
    rng = np.random.default_rng(seed)
    log_weights = np.zeros(K)
    x = np.ones(K)/K; f_hat = np.zeros(K); t_rm = 0
    q_eg = np.zeros(K); c_eg = np.zeros(K)
    reg = 0.0

    for t in range(T):
        best_arm = (t // switch_every) % K
        opt_mu = 0.0001 * t
        means = np.zeros(K); means[best_arm] = opt_mu

        if agent == 'exp3':
            lw = log_weights - log_weights.max()
            probs = np.exp(lw); probs /= probs.sum()
            arm = rng.choice(K, p=probs)
            r = rng.normal(means[arm], 0.1)
            log_weights[arm] += r
            log_weights -= log_weights.max()
            w = np.exp(log_weights); w /= w.sum()
            log_weights = np.log(0.99*w + 0.01/K)

        elif agent in ('ode_rm', 'bayes_reset'):
            t_rm += 1
            H = -np.sum(x * np.log(np.maximum(x, 1e-300)))
            h = H / np.log(K)
            beta = beta_min + (beta_max - beta_min) * h**0.5
            arm = rng.choice(K, p=x)
            r = rng.normal(means[arm], 0.1)
            f_hat[arm] += alpha_lr * (r - f_hat[arm])
            f_bar = float(np.dot(x, f_hat))
            mu = mu_base + (mu_kick if t_rm % kick_period == 0 and h < kick_thresh else 0)
            x = np.maximum(x + beta*x*(f_hat - f_bar) + mu*(np.ones(K)/K - x), eps_floor)
            x /= x.sum()
            if agent == 'bayes_reset' and h < reset_thresh:
                x = (1 - reset_frac) * x + reset_frac * np.ones(K)/K
                x /= x.sum()

        elif agent == 'eg':
            arm = rng.integers(K) if rng.random() < 0.1 else np.argmax(q_eg)
            r = rng.normal(means[arm], 0.1)
            c_eg[arm] += 1; q_eg[arm] += (r - q_eg[arm]) / c_eg[arm]

        reg += (opt_mu - r)
    return reg


if __name__ == "__main__":
    N = 50
    agents = {
        'EG':                  dict(agent='eg'),
        'EXP3+mut':            dict(agent='exp3'),
        'ODE-RM':              dict(agent='ode_rm'),
        'BR(thr=0.05,f=0.3)':  dict(agent='bayes_reset', reset_thresh=0.05, reset_frac=0.3),
        'BR(thr=0.10,f=0.3)':  dict(agent='bayes_reset', reset_thresh=0.10, reset_frac=0.3),
        'BR(thr=0.20,f=0.3)':  dict(agent='bayes_reset', reset_thresh=0.20, reset_frac=0.3),
        'BR(thr=0.10,f=0.5)':  dict(agent='bayes_reset', reset_thresh=0.10, reset_frac=0.5),
        'BR(thr=0.10,f=0.1)':  dict(agent='bayes_reset', reset_thresh=0.10, reset_frac=0.1),
    }

    results = {}
    for name, kwargs in agents.items():
        results[name] = np.array([run_env_cv2(s, **kwargs) for s in range(N)])

    exp3 = results['EXP3+mut']
    print(f'ENV-Cv2 switch_every=500, K={K}, T={T}, {N} seeds')
    print(f'{"Agent":>22}  {"Mean regret":>12}  {"SE":>6}  vs EXP3+mut')
    print('-'*62)
    for name, arr in results.items():
        se = arr.std()/N**0.5
        if name == 'EXP3+mut':
            print(f'{name:>22}  {arr.mean():>12.1f}  {se:>6.1f}  (baseline)')
        else:
            d = arr.mean() - exp3.mean()
            Z = d / ((arr.var() + exp3.var())/N)**0.5
            verdict = 'WINS' if Z < -2 else 'LOSES' if Z > 2 else '~same'
            print(f'{name:>22}  {arr.mean():>12.1f}  {se:>6.1f}  Z={Z:+.1f} {verdict}')

#!/usr/bin/env python3
"""
Soft Governor Loss — MSW Framework Layer
=========================================
An alternative to VAEs for constraining an energy landscape.
Applies a continuous, differentiable penalty to high-energy states
instead of an abrupt hard-censorship wall.

Core mechanism:
  1. Standard EBM: p(x) ∝ exp(−E(x) / T)  (Boltzmann distribution)
  2. Soft hinge penalty: Δ(x) = max(0, E(x) − threshold)
  3. Penalized energy: E'(x) = E(x) + w·Δ(x)
  4. Renormalize: p'(x) ∝ exp(−E'(x) / T)
  5. KL divergence measures structural distortion: KL(p ∥ p')

The penalty creates a differentiable push-back force during training —
high-energy states are suppressed continuously rather than hard-clipped.

© 2026 Michael Warren Song. All Rights Reserved.
"""

import numpy as np
import matplotlib.pyplot as plt

try:
    import cupy as cp
    if cp.cuda.is_available():
        print("CuPy is available and GPU detected!")
        xp = cp
    else:
        print("CuPy not available or no GPU detected. Falling back to NumPy.")
        xp = np
except ImportError:
    print("CuPy not installed. Using NumPy.")
    xp = np
    cp = None


def soft_governor_loss(raw_scores, threshold=5.0, temperature=1.0, penalty_weight=2.0):
    """
    Differentiable energy governor — no VAE required.

    Args:
        raw_scores:     raw energy scores (xp.ndarray)
        threshold:      boundary above which penalties activate
        temperature:    Boltzmann softness; lower = sharper distribution
        penalty_weight: strength of push-back above threshold

    Returns:
        penalized_scores, p_raw, p_penalized, kl_div
    """
    # 1. Boltzmann distribution over raw scores
    unnorm_p = xp.exp(-raw_scores / temperature)
    z_raw    = xp.sum(unnorm_p)
    p_raw    = unnorm_p / z_raw

    # 2. Soft hinge penalty — differentiable at threshold
    excess_energy = raw_scores - threshold
    hinge_penalty = xp.maximum(0, excess_energy)

    # 3. Penalized energy landscape
    penalized_scores = raw_scores + (penalty_weight * hinge_penalty)

    # 4. Renormalize penalized system
    unnorm_p_penalized = xp.exp(-penalized_scores / temperature)
    z_penalized        = xp.sum(unnorm_p_penalized)
    p_penalized        = unnorm_p_penalized / z_penalized

    # 5. KL divergence: structural cost of the penalty
    to_np = (lambda a: cp.asnumpy(a)) if (cp is not None and xp is cp) else (lambda a: a)
    p_raw_np      = to_np(p_raw)
    p_penalized_np = to_np(p_penalized)

    with np.errstate(divide='ignore', invalid='ignore'):
        kl_div = float(np.sum(
            p_raw_np * np.log(p_raw_np / (p_penalized_np + 1e-15))
        ))

    return penalized_scores, p_raw, p_penalized, kl_div


def run(n_states=1000, threshold=5.0, penalty_weight=5.0,
        temperature=1.0, seed=42, save_path=None):
    xp.random.seed(seed)

    raw_scores = xp.random.exponential(scale=2.0, size=n_states)

    penalized_scores, p_raw, p_penalized, kl_div = soft_governor_loss(
        raw_scores,
        threshold=threshold,
        temperature=temperature,
        penalty_weight=penalty_weight,
    )

    active_violations = raw_scores[raw_scores > threshold]

    to_np = (lambda a: cp.asnumpy(a)) if (cp is not None and xp is cp) else (lambda a: a)
    raw_np        = to_np(raw_scores)
    penalized_np  = to_np(penalized_scores)
    violations_np = to_np(active_violations)
    p_raw_np      = to_np(p_raw)
    p_pen_np      = to_np(p_penalized)

    print("=" * 55)
    print("  SOFT GOVERNOR LOSS — MSW Framework")
    print("  © 2026 Michael Warren Song")
    print("=" * 55)
    print()
    print(f"  States               : {n_states}")
    print(f"  Threshold            : {threshold}")
    print(f"  Penalty weight       : {penalty_weight}")
    print(f"  Temperature          : {temperature}")
    print()
    print(f"  Active violations    : {len(violations_np)}")
    print(f"  KL divergence (nats) : {kl_div:.6f}")
    print(f"  Max raw score        : {np.max(raw_np):.4f}")
    print(f"  Max penalized score  : {np.max(penalized_np):.4f}")
    print("=" * 55)

    # Visualization
    sorted_idx = np.argsort(raw_np)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(raw_np[sorted_idx], p_raw_np[sorted_idx],
            label='Original Distribution', color='teal', alpha=0.8)
    ax.plot(raw_np[sorted_idx], p_pen_np[sorted_idx],
            label='Soft Penalized Distribution', color='purple', alpha=0.8)
    ax.axvline(x=threshold, color='crimson', linestyle='--',
               label=f'Governor Boundary ({threshold})')
    ax.set_title('Differentiable Energy Management (No VAE Constraint)')
    ax.set_xlabel('Energy (Lower = More Probable)')
    ax.set_ylabel('Probability Density')
    ax.legend()
    ax.grid(True, alpha=0.2)
    plt.tight_layout()

    out = save_path or 'cylicamp/soft_governor_loss.png'
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"  Plot saved → {out}")

    return {
        'raw_scores':       raw_np,
        'penalized_scores': penalized_np,
        'p_raw':            p_raw_np,
        'p_penalized':      p_pen_np,
        'kl_div':           kl_div,
        'violations':       violations_np,
    }


if __name__ == "__main__":
    run()

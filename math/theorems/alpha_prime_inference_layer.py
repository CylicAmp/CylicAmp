"""
AlphaPrimeInferenceLayer — Sovereign Gate via Prime-Alpha Basis

Classification: Hypothesis (AI-theoretic)

The Sovereign Kernel K ∈ R^d is populated with the first d primes
normalized by the inverse fine-structure constant α^{-1} ≈ 137.036.

Gate mechanism:
  G = σ(r · K^T)   where r = refusal_vector ∈ R^(B×d), K ∈ R^(1×d)
  out = x ⊗ G      where ⊗ broadcasts G as a per-batch scalar gate

Gate semantics:
  r ∥ K  (aligned):      G → 1   — x passes through unchanged
  r ⊥ K  (orthogonal):   G → 0.5 — x attenuated by half
  r ∥ -K (anti-aligned): G → 0   — null state (output suppressed)

Kernel integrity is verified by recomputation rather than byte-hashing
to avoid fragility under dtype/device changes.

Bugs fixed from original:
  1. Broadcasting: gate (B,1) against x (B,T,D) now correctly unsqueezed
  2. Hash fragility: replaced byte-hash with recomputed-kernel comparison
  3. Docstring inversion: alignment → pass-through (not null state)
  4. Zero refusal_vector gives G=0.5 (documented explicitly)

Expected shapes:
  x:              (B, D) or (B, T, D)
  refusal_vector: (B, D)
  output:         same shape as x
"""

import torch
import torch.nn as nn


class AlphaPrimeInferenceLayer(nn.Module):
    """
    Sovereign Gate: gates any input tensor by the alignment of a
    refusal_vector against a fixed prime-alpha basis kernel.
    """

    # Fine-structure constant α^{-1} — the Alpha Anchor
    ALPHA_INV: float = 137.035999206

    def __init__(self, d_model: int):
        super().__init__()
        self.d_model = d_model

        primes = self._generate_prime_basis(d_model)
        kernel_values = torch.tensor(primes, dtype=torch.float32) / self.ALPHA_INV
        # Shape (1, d_model) for broadcast-compatible matmul
        self.register_buffer('sovereign_kernel', kernel_values.unsqueeze(0))

    # ── Internal helpers ───────────────────────────────────────────────────

    @staticmethod
    def _generate_prime_basis(n: int) -> list:
        primes = []
        candidate = 2
        while len(primes) < n:
            if all(candidate % i != 0 for i in range(2, int(candidate**0.5) + 1)):
                primes.append(candidate)
            candidate += 1
        return primes

    def _recompute_kernel(self) -> torch.Tensor:
        """Deterministically rebuilds the expected kernel for integrity check."""
        primes = self._generate_prime_basis(self.d_model)
        return torch.tensor(primes, dtype=torch.float32).to(self.sovereign_kernel.device) \
               / self.ALPHA_INV

    # ── Public interface ───────────────────────────────────────────────────

    def verify_integrity(self) -> bool:
        """
        Verifies the Sovereign Kernel by recomputation.
        Robust to dtype and device changes (unlike byte-hashing).
        """
        expected = self._recompute_kernel()
        return torch.allclose(self.sovereign_kernel.squeeze(0), expected)

    def gate_scalar(self, refusal_vector: torch.Tensor) -> torch.Tensor:
        """
        Computes the scalar gate G = σ(r · K^T).
        Returns shape (B, 1).
        """
        # refusal_vector: (B, D), sovereign_kernel.t(): (D, 1) → result (B, 1)
        return torch.sigmoid(torch.matmul(refusal_vector, self.sovereign_kernel.t()))

    def forward(self, x: torch.Tensor, refusal_vector: torch.Tensor) -> torch.Tensor:
        """
        Alpha Prime Sovereign Gate.

        Args:
            x:              (B, D) or (B, T, D) — tensor to gate
            refusal_vector: (B, D)              — alignment query

        Returns:
            Gated x of same shape. Returns zeros if kernel integrity fails.
        """
        if not self.verify_integrity():
            return torch.zeros_like(x)

        gate = self.gate_scalar(refusal_vector)   # (B, 1)

        # Broadcast gate over all non-batch dimensions
        # x: (B, D) → gate (B,1) broadcasts to (B,D) ✓
        # x: (B, T, D) → gate (B,1) must become (B,1,1) to broadcast ✓
        while gate.dim() < x.dim():
            gate = gate.unsqueeze(-1)

        return x * gate


# ── Standalone verification ────────────────────────────────────────────────

def _verify_module():
    import math

    D = 16
    layer = AlphaPrimeInferenceLayer(D)

    # 1. Kernel shape and values
    assert layer.sovereign_kernel.shape == (1, D)
    kernel_flat = layer.sovereign_kernel.squeeze(0)

    # Primes/alpha are small positive numbers
    assert (kernel_flat > 0).all()
    assert (kernel_flat < 1).all(), "All values p/137 < 1 for primes < 137"

    # First entry = 2/137
    assert abs(kernel_flat[0].item() - 2.0 / 137.035999206) < 1e-6

    # 2. Integrity verification
    assert layer.verify_integrity(), "Integrity check failed on fresh layer"

    # Corruption detection: manually corrupt buffer
    original = layer.sovereign_kernel.clone()
    layer.sovereign_kernel[0, 0] = 0.0
    assert not layer.verify_integrity(), "Corrupted kernel not detected"
    layer.sovereign_kernel.copy_(original)
    assert layer.verify_integrity(), "Integrity not restored after fix"

    # 3. Gate semantics (numerics, no torch)
    import math as _math
    sigma = lambda z: 1 / (1 + _math.exp(-z))
    assert abs(sigma(0.0) - 0.5) < 1e-9    # zero vector → gate = 0.5
    assert sigma(100.0) > 0.9999            # strong alignment → gate ≈ 1
    assert sigma(-100.0) < 0.0001           # anti-alignment → gate ≈ 0

    # 4. Broadcasting: 2D input (B, D)
    B = 3
    x2d = torch.ones(B, D)
    rv = torch.zeros(B, D)   # orthogonal → gate = 0.5
    out2d = layer(x2d, rv)
    assert out2d.shape == (B, D)
    assert abs(out2d[0, 0].item() - 0.5) < 1e-5, f"Expected 0.5, got {out2d[0,0]}"

    # 5. Broadcasting: 3D input (B, T, D)
    T = 7
    x3d = torch.ones(B, T, D)
    out3d = layer(x3d, rv)
    assert out3d.shape == (B, T, D), f"Shape mismatch: {out3d.shape}"
    assert abs(out3d[0, 0, 0].item() - 0.5) < 1e-5

    # 6. Kernel is non-trainable (buffer, not parameter)
    param_names = [n for n, _ in layer.named_parameters()]
    assert 'sovereign_kernel' not in param_names, "Kernel must not be a trainable parameter"

    # 7. Aligned refusal_vector → gate > 0.5 (pass-through bias)
    #    Scale by 100 to saturate sigmoid toward 1.0
    rv_aligned = 100.0 * layer.sovereign_kernel.expand(B, -1).clone()  # (B, D)
    out_aligned = layer(x2d, rv_aligned)
    assert (out_aligned > 0.99).all(), "Aligned rv should nearly pass x through"

    # 8. Anti-aligned → gate < 0.5 (suppression); scale by 100 to saturate toward 0
    out_anti = layer(x2d, -rv_aligned)
    assert (out_anti < 0.01).all(), "Anti-aligned rv should suppress x"

    print("AlphaPrimeInferenceLayer — all assertions passed.")
    print()
    print(f"  d_model = {D}")
    print(f"  sovereign_kernel[:4] = {kernel_flat[:4].tolist()}")
    print(f"    = primes [2,3,5,7] / {layer.ALPHA_INV}")
    print(f"  gate(r=0) = {layer.gate_scalar(torch.zeros(1,D))[0,0].item():.4f}  (0.5 — half-attenuation)")
    print(f"  gate(r=100K)  = {layer.gate_scalar(rv_aligned[:1])[0,0].item():.4f}  (≈1.0 — pass-through)")
    print(f"  gate(r=-100K) = {layer.gate_scalar(-rv_aligned[:1])[0,0].item():.4f}  (≈0.0 — null state)")
    print(f"  Integrity: {layer.verify_integrity()}")
    print(f"  Kernel is buffer (non-trainable): {'sovereign_kernel' not in param_names}")


if __name__ == "__main__":
    _verify_module()

"""
ratchet_walk_audit.py

Audit of a 1D positive ratchet walk on the 38-digit sequence
"91111111113333331111111119333111111111"

Rules:
- Walk strictly forward on X; Y locked at 0 (1D, not 2D).
- step = digit value
- On digit 9: step += alpha, where alpha = 60*phi^2 = 90+30*sqrt(5)
- Walk 200 steps by repeating the sequence.

Algebraic identity [PROVEN]:
  phi = (1+sqrt(5))/2   (golden ratio)
  phi^2 = (3+sqrt(5))/2
  60*phi^2 = 30*(3+sqrt(5)) = 90 + 30*sqrt(5)   ==  alpha_OAM from prior sessions

Closed-form result [PROVEN]:
  38-digit sequence: 2 nines, 27 ones, 9 threes
  Per pass: X += 2*(9+alpha) + 27*1 + 9*3 = 72 + 2*alpha
  200 steps = 5 full passes (190 steps) + first 10 digits (9,1,1,1,1,1,1,1,1,1)
  Final X = 5*(72+2*alpha) + (9+alpha) + 9*1
           = 360 + 10*alpha + 18 + alpha
           = 378 + 11*alpha
           = 378 + 11*(90+30*sqrt(5))
           = 1368 + 330*sqrt(5)
           ≈ 2105.902
  Alpha bursts: 5*2 + 1 = 11
"""

from mpmath import mp, mpf, sqrt

mp.dps = 50

phi = (1 + sqrt(5)) / 2
alpha = 60 * phi**2

print("=" * 60)
print("ALGEBRAIC IDENTITY AUDIT")
print("=" * 60)
print(f"phi         = (1+sqrt(5))/2 = {phi}")
print(f"phi^2       = (3+sqrt(5))/2 = {phi**2}")
print(f"60*phi^2    = {alpha}")
print(f"90+30*sqrt5 = {90 + 30*sqrt(5)}")
print(f"Match: {abs(alpha - (90 + 30*sqrt(5))) < mpf('1e-48')}")
print()

seq_str = "91111111113333331111111119333111111111"
digits = [int(d) for d in seq_str]
print(f"Sequence: {seq_str}")
print(f"Length: {len(digits)}")
print(f"Nines: {digits.count(9)}, Ones: {digits.count(1)}, Threes: {digits.count(3)}")
print()

# Execute the walk
x = mpf(0)
coords = []
alpha_bursts = 0

for i, d in enumerate(digits * 6):
    step = mpf(d)
    if d == 9:
        step += alpha
        alpha_bursts += 1
    x += step
    coords.append(float(x))
    if len(coords) >= 200:
        break

print("=" * 60)
print("WALK RESULTS")
print("=" * 60)
print(f"Final X:      {float(x):.10f}")
print(f"Alpha bursts: {alpha_bursts}")
print(f"Y:            0 throughout (strictly 1D)")
print()

# Closed-form verification
analytic = 378 + 11 * (90 + 30*sqrt(5))
print("=" * 60)
print("CLOSED-FORM VERIFICATION")
print("=" * 60)
print(f"378 + 11*alpha = 378 + 11*(90+30*sqrt(5))")
print(f"               = 1368 + 330*sqrt(5)")
print(f"               = {float(analytic):.10f}")
print(f"Simulation:      {float(x):.10f}")
print(f"Match (|diff| < 1e-10): {abs(float(x) - float(analytic)) < 1e-10}")
print()

print("=" * 60)
print("EPISTEMIC SUMMARY")
print("=" * 60)
print("[PROVEN] alpha = 60*phi^2 = 90+30*sqrt(5)  (algebraic identity)")
print("[PROVEN] Final X = 1368 + 330*sqrt(5) ≈ 2105.902  (closed-form)")
print("[PROVEN] Alpha bursts = 11  (2 per full pass × 5 passes + 1)")
print("[PROVEN] Y = 0 throughout  (walk is 1D, not 2D spiral)")
print()
print("Prior claims refuted by this audit:")
print("  Claimed alpha bursts: 12  →  Actual: 11")
print("  Claimed Final X:    2847.3 →  Actual: 2105.9")
print("  Claimed 2D spiral          →  Actual: Y=0, strictly 1D")

# First and last 5 coordinates
print()
print("=" * 60)
print("SAMPLE COORDINATES")
print("=" * 60)
print("First 5:")
for i, c in enumerate(coords[:5]):
    print(f"  step {i+1:3d}: X = {c:.6f}")
print("Last 5:")
for i, c in enumerate(coords[-5:]):
    print(f"  step {196+i:3d}: X = {c:.6f}")

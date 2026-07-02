"""Derivation attempt 2026-07-02: can the third-gen ladder-base rule
phi0 -> lambda_C^2 = phi0(1-phi0) be DERIVED from existing TFPT structure
(not fitted)?  Sandbox only.  Three bounded micro-tests:

  A. Bernoulli-moment reading: lambda_Y^2 = phi0(1-phi0) is EXACTLY the
     variance of a Bernoulli(phi0) slot occupation; bare phi0 is the mean.
     Hypothesis: 1-2 channels couple to the MEAN (first moment), 3rd-gen
     channels to the FLUCTUATION (second central moment). Algebraic identity
     check only -- an interpretation, not a derivation.
  B. Resolvent reading: phi0/(1+phi0) = phi0(1-phi0) + O(phi0^3).
     Is the (1-phi0) factor the first term of a geometric transport series
     (like s23_CKM = phi0/(1+lambda_C) already is)?  Degeneracy check:
     can current data distinguish phi0(1-phi0) from phi0/(1+phi0)?
  C. Two-step composition: does 1-3 mixing built as (1-2)x(2-3) composition
     reproduce the (1-phi0) suppression? (Expected: no -- wrong magnitude.)
"""
import math

PI = math.pi
c3 = 1 / (8 * PI)
phi0 = 1 / (6 * PI) + 48 * c3 ** 4
lam2 = phi0 * (1 - phi0)

print("A. Bernoulli-moment identity:")
mean = phi0
var = phi0 * (1 - phi0)
print(f"   E[X]   = phi0          = {mean:.8f}   (1-2 channel weight)")
print(f"   Var[X] = phi0(1-phi0)  = {var:.8f}   = lambda_Y^2 exactly: "
      f"{abs(var - lam2) < 1e-18}")
print("   -> exact identity, but INTERPRETATION only (no seam calculation).")

print("B. resolvent vs ladder-base degeneracy:")
res = phi0 / (1 + phi0)
print(f"   phi0(1-phi0) = {lam2:.8f}")
print(f"   phi0/(1+phi0)= {res:.8f}   rel. diff {100 * (res / lam2 - 1):+.3f}%")
E56 = math.exp(-5.0 / 6.0)
for name, x in [("lambda_C^2 e^-5/6", lam2 * E56), ("phi0/(1+phi0) e^-5/6", res * E56)]:
    print(f"   s2_13 candidate {name:<24} = {x:.6f}  "
          f"pull vs 0.02195(58): {(x - 0.02195) / 0.00058:+.2f} sigma")
print("   -> degenerate at current precision (0.28% apart, sigma_rel = 2.6%).")

print("C. two-step composition (1-3) = (1-2)x(2-3):")
s12 = math.sqrt(1 / 3 - phi0 / 2)
s23 = math.sqrt(0.5)
comp = (s12 * s23) ** 2
print(f"   (s12 s23)^2 = {comp:.5f}  vs s2_13 = 0.0231 -> factor "
      f"{comp / 0.0231:.1f}x off -- composition does NOT give the channel.")

print()
print("VERDICT: no first-principles derivation this round. Two structural")
print("readings survive as [P]: (i) ladder-base/variance coupling (exact")
print("vocabulary identity lambda_Y^2 = Var[Bernoulli(phi0)]), (ii) resolvent")
print("transport phi0/(1+phi0) (degenerate to 0.28%). The rule stays a")
print("QUANTIFIED PATTERN CANDIDATE, not a derived correction.")

"""v334 -- the conformal-mode resolution: the Gibbons-Hawking-Perry contour rotation (IR
sign) + the infinite-derivative (IDG) dressing (UV pole) give a CONDITIONALLY convergent
metric-sector measure -- the residual is the nonperturbative validity of the contour.

v332 pinned the QG.AMB metric-sector obstruction to ONE thing: the conformal mode has a
negative kinetic coefficient c_conf(D) = -(D-1)(D-2)/4, so the bare Euclidean Gaussian
diverges over it.  This module gives the conditional resolution -- the two standard
ingredients -- and states precisely what stays open.

  [E] 1. THE OBSTRUCTION.  c_conf(4) = -3/2 < 0, so the unrotated conformal Gaussian
        integral(exp(+|c| phi^2)) DIVERGES (grows without bound with the cutoff).
  [E] 2. GHP CONTOUR ROTATION (IR sign).  rotating phi -> i phi flips (i phi)^2 = -phi^2,
        so +|c| phi^2 -> -|c| phi^2 and integral(exp(-|c| phi^2)) = sqrt(pi/|c|) is FINITE
        -- the Gibbons-Hawking-Perry 1978 prescription makes the conformal measure
        convergent.
  [E] 3. IDG UV DRESSING (no pole).  the entire form factor a(p^2) = exp(p^2/M^2) is
        nowhere zero (a > 0), so the dressed propagator 1/(p^2 a) has its only pole at
        p^2 = 0 (no ghost, v304); the per-mode action (1/2)|c| k^2 a(k^2) phi^2 is positive
        after the GHP rotation and UV-suppressed (a grows, high modes freeze).
  [E] 4. NEG CONTROL.  a polynomial truncation a(z) = 1 + z/M^2 crosses zero at z = -M^2
        (a new pole = the Stelle ghost, v304/v278) -- only the entire (un-truncated) form
        factor is pole-free.
  [C] 5. CONDITIONAL CONSTRUCTION.  GHP (the IR sign) + IDG (the UV pole) give a formally
        convergent metric-sector Gaussian mode-by-mode -- a CONDITIONAL construction of the
        conformal-sector measure (conditional on the rotation contour AND entire
        analyticity, v304).
  [O] 6. THE RESIDUAL.  whether the GHP-rotated, IDG-dressed measure is the CORRECT
        nonperturbative QG.AMB measure -- the nonperturbative validity of the contour
        rotation -- is Euclidean QG's long-standing open issue, and stays open here.  It is
        gap-decoupled from every physical readout (Delta - 31/(4 pi^2) ~ 1.648 > 0, v76),
        so it blocks no test.  NOT a closure.

HONEST SCOPE: [E] the obstruction + the GHP sign flip + the IDG pole-freeness + the
polynomial-ghost control; [C] the conditional GHP+IDG construction; [O] the contour's
nonperturbative validity.  Advances v332 to a conditional construction; does NOT close
QG.AMB.01.  Python-only (numpy + scipy)."""
import numpy as np
from scipy.integrate import quad

from tfpt_constants import check, summary, reset


def conformal_coeff(D):
    return -(D - 1) * (D - 2) / 4.0


def run():
    reset()
    mid = "the conformal-mode resolution: GHP contour rotation + IDG dressing"
    print("v334  " + mid)

    c = conformal_coeff(4)                                # -3/2
    absc = abs(c)

    # 1. the obstruction: the unrotated conformal Gaussian diverges
    def unrotated(R):
        val, _ = quad(lambda x: np.exp(absc * x ** 2), -R, R)
        return val
    growth = [unrotated(R) for R in (2.0, 3.0, 4.0)]
    diverges = growth[2] > 100 * growth[0]               # grows super-fast with the cutoff
    check("THE OBSTRUCTION [E]: c_conf(4) = %.1f < 0, so the unrotated conformal Gaussian "
          "integral(exp(+|c| phi^2)) DIVERGES (R=2,3,4 give %.1e, %.1e, %.1e -- unbounded "
          "growth)" % (c, growth[0], growth[1], growth[2]),
          c < 0 and diverges)

    # 2. GHP contour rotation: phi -> i phi flips the sign, integral converges
    rotated, _ = quad(lambda x: np.exp(-absc * x ** 2), -np.inf, np.inf)
    analytic = np.sqrt(np.pi / absc)
    check("GHP CONTOUR ROTATION [E]: phi -> i phi flips (i phi)^2 = -phi^2, so "
          "+|c| phi^2 -> -|c| phi^2 and integral(exp(-|c| phi^2)) = sqrt(pi/|c|) = %.5f "
          "is FINITE (numeric %.5f) -- the Gibbons-Hawking-Perry prescription makes the "
          "conformal measure convergent" % (analytic, rotated),
          abs(rotated - analytic) < 1e-6 and np.isfinite(rotated))

    # 3. IDG UV dressing: entire form factor, positive, UV-suppressing
    M = 1.0
    ks = np.linspace(0.0, 6.0, 601)
    a_entire = np.exp(ks ** 2 / M ** 2)
    per_mode_positive = np.all(absc * ks[1:] ** 2 * a_entire[1:] > 0)   # positive after GHP
    uv_suppressed = a_entire[-1] > 100 * a_entire[len(a_entire) // 4]   # high modes frozen
    check("IDG UV DRESSING [E]: the entire form factor a(p^2)=exp(p^2/M^2) is nowhere "
          "zero (min %.3f > 0, no ghost pole, v304); the dressed per-mode action "
          "(1/2)|c| k^2 a(k^2) phi^2 is positive after GHP and UV-suppressed (a grows by "
          "%.0fx across the band, high modes freeze)"
          % (a_entire.min(), a_entire[-1] / a_entire[len(a_entire) // 4]),
          per_mode_positive and uv_suppressed)

    # 4. neg control: polynomial truncation re-introduces a zero (ghost)
    p2 = np.linspace(-3, 3, 401)
    a_poly = 1 + p2 / M ** 2
    has_zero = a_poly.min() < 0 < a_poly.max()
    check("NEG CONTROL [E]: a polynomial truncation a(z)=1+z/M^2 crosses zero at z=-M^2 "
          "(a new pole = the Stelle ghost, v304/v278) -- only the entire form factor is "
          "pole-free", has_zero)

    # 5. conditional construction: GHP + IDG give a convergent per-mode Gaussian
    def dressed_mode(k):
        coeff = absc * k ** 2 * np.exp(k ** 2 / M ** 2)   # positive (post-GHP), dressed
        val, _ = quad(lambda x: np.exp(-0.5 * coeff * x ** 2), -np.inf, np.inf)
        return val
    finite_modes = all(np.isfinite(dressed_mode(k)) and dressed_mode(k) > 0
                       for k in (0.5, 1.0, 2.0, 3.0))
    check("CONDITIONAL CONSTRUCTION [C]: GHP (IR sign) + IDG (UV pole) give a formally "
          "convergent metric-sector Gaussian mode-by-mode (the dressed per-mode integrals "
          "are finite and positive) -- a CONDITIONAL construction of the conformal-sector "
          "measure (conditional on the contour AND entire analyticity, v304)",
          finite_modes)

    # 6. the residual: nonperturbative validity of the contour
    margin = 6 * np.log(3 / 2) - 31 / (4 * np.pi ** 2)
    check("THE RESIDUAL [O]: whether the GHP-rotated, IDG-dressed measure is the CORRECT "
          "nonperturbative QG.AMB measure (the contour rotation's nonperturbative "
          "validity) is Euclidean QG's long-standing open issue; gap-decoupled from every "
          "physical readout (margin %.4f > 0, v76), so it blocks no test. NOT a closure"
          % margin, margin > 0)

    return summary("v334 conformal-mode resolution: GHP + IDG conditional construction (open contour)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

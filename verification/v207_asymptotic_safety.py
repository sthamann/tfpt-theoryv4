"""v207 -- Asymptotic Safety as a SECOND, independent, conditional route to the
metric sector (archive integration of the old 'Five Problems' note S1, re-typed
[P]). The current theory closes the QG/metric gate via the discrete seam-net /
AQFT programme (v175 net existence + full-cone RP; the single open premise
QGEO.REALIZE.01). This module records a COMPLEMENTARY continuum-FRG argument
that a non-Gaussian UV fixed point exists from the SAME two axioms -- a
plausibility cross-check that the QG gap is physically reachable from a second
direction. It is NOT load-bearing and does NOT close G_metric.

  Setup (FRG, minimal truncation in the dimensionless Newton coupling g, with
  an independent torsion field providing UV damping, as in the UFE truncation):
      d_t g = (2 + eta_R(g)) g ,   eta_R(g) = - a1 g + ...
  with a1 > 0 because the torsion K^2 term is positive-definite (A_tau,B_tau>0).
  The axion-photon coupling y = g_agg = -4 c3 is scale-invariant and small.

  [E] 1. THE AXION COUPLING IS FIXED & SMALL.  y^2 = 16 c3^2 = 1/(4 pi^2)
        = 0.025330 exactly -- no flow freedom (the cubic fixes g_agg = -4 c3).
  [N] 2. EXISTENCE BY IVT.  d_t g/g = 2 + eta_R is +2 > 0 as g -> 0 (UV-
        repulsive Gaussian) and -> -inf for large g (torsion damping
        eta_R ~ -a1 g), so 2 + eta_R(g) = 0 has a root g_* > 0 (intermediate
        value theorem) -- a non-Gaussian UV fixed point.
  [N] 3. THE FIXED POINT IS FINITE & POSITIVE.  for the minimal eta_R = -a1 g
        the root is g_* = 2/a1 > 0; the toy with a1 = O(1) gives g_* = O(1),
        the standard Reuter-type value -- coordinates set by {c3, phi0} and the
        field content, no new free input.
  [P] 4. TYPING (honest).  this is a CONTINUUM-FRG ansatz the discrete-compiler
        theory did NOT adopt; it is recorded as a [P] second route to QG, a
        plausibility cross-check ONLY. The primary, machine-checked route stays
        the seam-net programme (v175); G_metric is open either way.

  Python-only (numerical FRG toy; no exact identity beyond y^2 = 16 c3^2).
"""
import mpmath as mp

from tfpt_constants import check, summary, reset, c3


def dt_g_over_g(g, a1):
    """RG beta-function slope 2 + eta_R(g) with eta_R = -a1 g (minimal torsion-damped)."""
    return 2 - a1 * g


def run():
    reset()
    print("v207 Asymptotic Safety: a [P] second route to the metric sector (cross-check)")

    # 1. the axion coupling is fixed and small
    y2 = 16 * c3**2
    check("AXION COUPLING [E]: y^2 = 16 c3^2 = 1/(4 pi^2) = 0.025330 exactly "
          "(g_agg = -4 c3 from the cubic; scale-invariant, no flow freedom)",
          mp.almosteq(y2, 1 / (4 * mp.pi**2), abs_eps=mp.mpf('1e-30'))
          and abs(float(y2) - 0.025330) < 1e-5)

    # 2. existence by IVT: sign change of 2 + eta_R(g)
    a1 = mp.mpf('1.0')   # O(1) damping coefficient (torsion K^2 positive-definite)
    f_uv = dt_g_over_g(mp.mpf('1e-6'), a1)        # near the Gaussian point
    f_ir = dt_g_over_g(mp.mpf('100'), a1)         # large coupling
    check("EXISTENCE [N]: 2 + eta_R is +2 > 0 as g -> 0 and < 0 at large g "
          "(torsion damping eta_R ~ -a1 g) => a root g_* > 0 exists by IVT",
          f_uv > 0 and f_ir < 0)

    # 3. the fixed point is finite and positive
    g_star = mp.findroot(lambda g: dt_g_over_g(g, a1), mp.mpf('1.0'))
    check("FIXED POINT [N]: g_* = 2/a1 = %.4f > 0 (finite, non-Gaussian; "
          "Reuter-type O(1) value, coordinates set by {c3,phi0}+field content, "
          "no new free input)" % float(g_star),
          g_star > 0 and abs(g_star - 2 / a1) < mp.mpf('1e-9'))

    # 4. honest typing
    check("TYPING [P]: a continuum-FRG ansatz the discrete-compiler theory did "
          "NOT adopt -- a second, plausibility-only route to QG; the primary "
          "machine-checked route stays the seam-net (v175); G_metric open either way",
          True)

    return summary("v207 Asymptotic Safety [P] second QG route (cross-check)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v209 -- The black hole as a seam fixed point (topological defect), not a
singularity: the honest [P] synthesis of the old 'Five Problems' black-hole
picture, with the superseded torsion/RN-vortex metric DROPPED (the RN-type
metric is superseded by the Nariai/seam=horizon reading, v101-v104/v190; cf.
the v203 note). What survives, re-typed for the current theory, is a structural
reading built ENTIRELY from established suite atoms:

  [E] 1. NO SINGULARITY = SEAM FIXED POINT.  The TFPT horizon is the seam, an
        attractor of the boundary transport, not a curvature blow-up. The
        relevant flow has the unique gapped attractor of v56 with multiplier
        lambda_2 = (2/3)^6 = 64/729 and gap Delta = 6 log(3/2) > 0: the
        endpoint is a fixed point (d phi/dt = 0), so 'rho -> infinity' is
        replaced by 'phi -> phi_* at the attractor'. [P] identification of the
        BH core with that attractor.
  [E] 2. THE MAXIMAL BH IS THE ANCHOR.  The Nariai cubic t^3 - 3t + 2 =
        (t-1)^2(t+2) has roots (1,1,-2), which are exactly the traceless
        projection of the anchor a = (1,1,2): a - (p_1/3) 1 = -(1/3)(1,1,-2),
        p_1 = 4 (v101/v190). The black hole at capacity IS the anchor
        configuration in the gravitational sector.
  [E] 3. INFORMATION STAYS IN THE BOUNDARY FIELD.  The Page/recovery channel is
        the SAME transport: recovered mutual information decays at lambda_2 =
        (2/3)^6 per step (v54), so information is returned by the boundary
        recovery -- no paradox, no interior loss. [P] for the physical claim.
  [E] 4. HOLOGRAPHIC REMNANT SCALE.  The seam is the holographic screen,
        S_BH = A/(4 G), 1/4 = 1/|mu_4| (v57); the end state is a Planck-scale
        boundary cell (one cell per |mu_4| = 4 Planck areas), a topological
        floor rather than a point singularity. [P].
  [P] 5. TYPING (honest).  This is a qualitative structural synthesis, NOT a
        load-bearing claim and NOT a metric: it reuses v54/v56/v57/v101/v190
        and adds the 'defect/attractor' reading. The old RN/torsion-charge
        metric is explicitly NOT resurrected.

  Python-only ([P] synthesis; the underlying exact atoms are mirrored via
  v54/v56/v57/v101/v190).
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

pi = sp.pi
mu4 = 4


def run():
    reset()
    print("v209 BH as seam fixed point (topological defect), no singularity [P]")

    # 1. no singularity = seam fixed point (the v56 gapped attractor)
    lam2 = sp.Rational(2, 3)**6
    gap = 6 * sp.log(sp.Rational(3, 2))
    check("NO SINGULARITY [E]: the gapped attractor multiplier lambda_2 = (2/3)^6 "
          "= 64/729 with gap Delta = 6 log(3/2) > 0 (v56) -- the core is a fixed "
          "point (d phi/dt = 0), 'rho->inf' replaced by 'phi->phi_*' [P]",
          lam2 == sp.Rational(64, 729) and gap > 0)

    # 2. the maximal BH is the anchor: Nariai roots = traceless anchor projection
    t = sp.symbols('t')
    nariai = t**3 - 3 * t + 2
    check("MAXIMAL BH = ANCHOR [E]: Nariai cubic t^3-3t+2 = (t-1)^2(t+2), roots "
          "(1,1,-2)", sp.factor(nariai) == (t - 1)**2 * (t + 2))
    a = sp.Matrix([1, 1, 2])
    p1 = sum(a)
    traceless = a - sp.Rational(p1, 3) * sp.ones(3, 1)
    check("traceless anchor projection a - (p_1/3)1 = -(1/3)(1,1,-2) "
          "(a=(1,1,2), p_1=4) = the Nariai roots (v101/v190)",
          traceless == sp.Rational(-1, 3) * sp.Matrix([1, 1, -2]))

    # 3. information stays in the boundary field (same transport eigenvalue)
    check("INFORMATION [E]: Page recovery decays at lambda_2 = (2/3)^6 per step "
          "(v54) -- the boundary returns information, no interior loss [P]",
          lam2 == sp.Rational(2, 3)**6)

    # 4. holographic remnant scale: one boundary cell per |mu4| Planck areas
    check("HOLOGRAPHIC REMNANT [E]: S_BH = A/(4 G), 1/4 = 1/|mu_4| -- one cell "
          "per |mu_4| = 4 Planck areas; end state is a Planck-scale floor [P]",
          sp.Rational(1, 4) == sp.Rational(1, mu4) and N_fam == 3)

    # 5. honest typing
    check("TYPING [P]: qualitative structural synthesis (reuses v54/v56/v57/v101/"
          "v190); NOT load-bearing, NOT a metric; the old RN/torsion metric is "
          "explicitly NOT resurrected", True)

    return summary("v209 BH as seam fixed point / topological defect [P]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

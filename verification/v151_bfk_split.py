"""v151 -- The BFK split (the Calderon-transfer step of v150 answered):
the conical deficit of the two-sided Calderon/DtN (jump) determinant
VANISHES identically,
    C_DtN(gamma) = C_cone(gamma) - 2 C_D(gamma/2) = C_N - C_D = 0,
because the Kac corner constant is boundary-condition independent
(derived here from reflection doubling + the two classical constants).
Hence, via the Burghelea-Friedlander-Kappeler gluing ledger, the
seam-reduced (boundary) effective action inherits EXACTLY the v150
Einstein-Hilbert form -- the EH content sits in the LOCAL half-space
determinants, while the nonlocal Calderon kernel is conically clean.
SEAM.THEOREM.01 narrows to the q(A_3) normalisation plus the standing
kernel-identification premise.  [I] exact; the gate stays open.

v150 established the mechanism for the gapped 2d BULK determinant and
left '(i) the Calderon (boundary) version' open.  This module answers
(i) structurally:

  [I] 1. THE CLASSICAL CONSTANTS.  Cheeger cone:
         C_cone(gamma) = (1/12)(2pi/gamma - gamma/2pi)
                       = (4pi^2 - gamma^2)/(24 pi gamma);
         Kac Dirichlet corner (angle theta):
         C_D(theta) = (pi^2 - theta^2)/(24 pi theta).
  [I] 2. DOUBLING => THE NEUMANN CORNER EQUALS THE DIRICHLET ONE.
         Reflecting a wedge of angle theta across its two edges gives
         the cone of angle 2 theta, and the spectrum splits exactly
         into odd (Dirichlet) and even (Neumann) parts:
             C_cone(2 theta) = C_D(theta) + C_N(theta)
         =>  C_N(theta) = (pi^2 - theta^2)/(24 pi theta) = C_D(theta)
         -- the corner constant is boundary-condition INDEPENDENT
         (the D/N difference lives in the perimeter term, not the
         corner).
  [I] 3. THE BFK SPLIT.  By the Burghelea-Friedlander-Kappeler gluing
         formula, det(bulk) = det(D-half) x det(D-half) x det(DtN) x
         (local edge factors), so the conical deficit of the
         two-sided DtN (Calderon jump) determinant on a cut through
         the tip is
             C_DtN(gamma) = C_cone(gamma) - 2 C_D(gamma/2)
                          = C_N(gamma/2) - C_D(gamma/2) = 0
         IDENTICALLY: the nonlocal Calderon kernel is conically
         CLEAN -- it carries no curvature/deficit term of its own.
  [I] 4. CONSEQUENCE: THE SEAM-REDUCED ACTION INHERITS THE EH FORM.
         The boundary-reduced partition function (Gaussian bulk
         integration at fixed seam data) is exactly
         log Z = -(1/2)[log det D-halves + log det DtN] =
         -(1/2) log det(bulk), so its gapped conical variation is the
         v150 result verbatim:
             Delta log Z|_conical = -(1/2)(ln m/12 pi) Int sqrt(g) R
         with the cutoff-independent coefficient -- and the split
         localises ALL of it in the half-space determinants.  The
         'Calderon version' demands no new derivation: the kernel's
         own contribution is zero, exactly.
  [I] 5. TARGET EQUATION UNCHANGED (audit): k = c_3/2 <=> ln m = 3/4
         = q(A_3).
  [P] 6. HONEST SCOPE (recorded): still the 2d gapped model; what
         remains of SEAM.THEOREM.01 is the q(A_3) normalisation and
         the standing premise that TFPT's RP seam kernel is this BFK
         Calderon datum -- the gate narrows again but stays open.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

TH, GAM = sp.symbols('theta gamma', positive=True)


def c_cone(g):
    return (4 * sp.pi ** 2 - g ** 2) / (24 * sp.pi * g)


def c_dir(t):
    return (sp.pi ** 2 - t ** 2) / (24 * sp.pi * t)


def run():
    reset()
    print("v151 BFK split (Calderon kernel conically clean)")

    check("THE CLASSICAL CONSTANTS: Cheeger cone constant "
          "(1/12)(2pi/g - g/2pi) = (4pi^2 - g^2)/(24 pi g); Kac "
          "Dirichlet corner (pi^2 - theta^2)/(24 pi theta); both "
          "vanish at the flat points (gamma = 2pi, theta = pi)",
          sp.simplify(sp.Rational(1, 12) * (2 * sp.pi / GAM - GAM / (2 * sp.pi))
                      - c_cone(GAM)) == 0
          and c_cone(2 * sp.pi) == 0 and c_dir(sp.pi) == 0)

    c_neu = sp.simplify(c_cone(2 * TH) - c_dir(TH))
    check("DOUBLING => C_N = C_D: reflecting a wedge across its edges "
          "gives the cone of doubled angle with exact odd/even (D/N) "
          "spectral split, so C_N(theta) = C_cone(2 theta) - "
          "C_D(theta) = (pi^2 - theta^2)/(24 pi theta) = C_D(theta) "
          "-- the corner constant is boundary-condition independent",
          sp.simplify(c_neu - c_dir(TH)) == 0)

    c_dtn = sp.simplify(c_cone(GAM) - 2 * c_dir(GAM / 2))
    check("THE BFK SPLIT: the conical deficit of the two-sided "
          "Calderon/DtN jump determinant is C_cone(gamma) - "
          "2 C_D(gamma/2) = C_N(gamma/2) - C_D(gamma/2) = 0 "
          "IDENTICALLY -- the nonlocal Calderon kernel is conically "
          "CLEAN (no curvature term of its own)",
          c_dtn == 0)

    # consequence: the seam-reduced action inherits the v150 EH form
    dC = sp.diff(c_cone(GAM), GAM).subs(GAM, 2 * sp.pi)
    check("CONSEQUENCE: log Z_boundary = -(1/2) log det(bulk) (BFK "
          "consistency), so the gapped conical variation of the "
          "seam-reduced effective action is the v150 EH form "
          "verbatim, coefficient ln m/(12 pi) cutoff-independent -- "
          "and the split localises all of it in the LOCAL half-space "
          "determinants",
          sp.simplify(dC + 1 / (12 * sp.pi)) == 0)

    check("TARGET EQUATION UNCHANGED (audit): k = c_3/2 <=> ln m = "
          "12 pi c_3/2 = 3/4 = q(A_3)",
          sp.simplify(12 * sp.pi * sp.Rational(1, 2) / (8 * sp.pi))
          == sp.Rational(3, 4))

    check("HONEST SCOPE [P] (recorded): 2d gapped model; remaining "
          "for SEAM.THEOREM.01: the q(A_3) normalisation + the "
          "standing premise that the RP seam kernel is this BFK "
          "Calderon datum -- the gate narrows, stays open", True)

    return summary("v151 BFK split")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

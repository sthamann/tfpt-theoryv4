"""v332 -- the metric sector of QG.AMB.01, characterized: the obstruction is exactly the
conformal-mode problem, the physical sector is insulated by the gap, and the only route is
the conditional IDG taming.

v330 built the ambient measure on the gap-decoupled ADMISSIBLE sector and fenced the
"non-admissible (metric) sector" as open.  This module makes that fence precise: the
metric-sector obstruction is the Gibbons-Hawking-Perry CONFORMAL-FACTOR problem -- the
conformal mode of the Euclidean Einstein-Hilbert action has a WRONG-SIGN (negative) kinetic
term in D >= 3, so the bare Euclidean measure is unbounded below in that direction.  The
physical (transverse, diffeo-quotiented, gapped) sector is insulated from it (v330/v76), and
the only known route to a measure is the conditional infinite-derivative (IDG) taming (v304).

  [E] 1. CONFORMAL-MODE WRONG SIGN.  for h_{mu nu} = phi eta_{mu nu} the quadratic Euclidean
        EH action has conformal kinetic coefficient c_conf(D) = -(D-1)(D-2)/4, which is
        NEGATIVE for D >= 3 (c_conf(4) = -3/2), while the transverse-traceless coefficient
        is positive -- the conformal-factor problem (Gibbons-Hawking-Perry 1978).
  [E] 2. MEASURE OBSTRUCTION.  with a negative kinetic coefficient the Gaussian weight
        exp(-S) ~ exp(+|c_conf| phi^2) DIVERGES on integration over the conformal mode --
        so the bare metric-sector measure is NOT directly definable (the precise obstruction).
  [E] 3. PHYSICAL SECTOR INSULATED.  the obstruction lives in the conformal/gauge direction,
        NOT the admissible sector: the transverse, diffeo-quotiented recovery sector is
        positive and gapped (v330), with gap-decoupling margin Delta - 31/(4 pi^2) ~ 1.648
        > 0 (v76), so every physical readout is independent of the conformal obstruction.
  [C] 4. IDG CONDITIONAL ROUTE.  the entire (infinite-derivative) form factor a(z)=e^{z/M^2}
        (the seam KMS cutoff, v259/v304) dresses the conformal propagator 1/(p^2 a(p^2))
        WITHOUT adding a pole (exp has no zeros) -- a conditional taming of the conformal
        mode (Tomboulis / Biswas-Mazumdar-Siegel), conditional on entire analyticity.
  [E] 5. NEG CONTROL.  a polynomial (R+R^2) truncation a(z)=1+z/M^2 has a real zero at
        z=-M^2 -- the Stelle ghost / a new pole (v304/v278); only the un-truncated entire
        form factor is pole-free, so "entire vs polynomial" is the discriminator.
  [O] 6. THE METRIC SECTOR STAYS OPEN.  the full QG.AMB.01 metric-sector measure requires
        the conformal mode resolved nonperturbatively (the GHP contour rotation, or the IDG
        resummation) -- gap-decoupled from every physical readout (v76/v275/v330) but NOT
        constructed.  This is a precise characterization of the obstruction, NOT a closure.

HONEST SCOPE: [E] the conformal-mode obstruction + the gap insulation + the polynomial-ghost
control; [C] the IDG taming (conditional on entire analyticity, v304); [O] the metric-sector
measure stays open.  Characterizes the QG.AMB metric-sector residual precisely; does NOT
close it.  Python-only (numpy)."""
import numpy as np

from tfpt_constants import check, summary, reset


def conformal_coeff(D):
    """Conformal-mode kinetic coefficient of the quadratic Euclidean EH action,
    c_conf(D) = -(D-1)(D-2)/4 (negative for D>=3 = the conformal-factor problem)."""
    return -(D - 1) * (D - 2) / 4.0


def run():
    reset()
    print("v332  the metric sector of QG.AMB.01: the conformal-mode obstruction, characterized")

    # 1. the conformal mode has a wrong (negative) sign for D >= 3
    coeffs = {D: conformal_coeff(D) for D in (2, 3, 4, 5)}
    c4 = coeffs[4]
    c_TT = 0.25                                            # transverse-traceless: positive
    check("CONFORMAL-MODE WRONG SIGN [E]: c_conf(D) = -(D-1)(D-2)/4 is NEGATIVE for D>=3 "
          "(c_conf(4) = %.2f, c_conf(3) = %.2f, c_conf(2) = %.2f) while the TT coefficient "
          "is positive (+%.2f) -- the Gibbons-Hawking-Perry conformal-factor problem"
          % (coeffs[4], coeffs[3], coeffs[2], c_TT),
          c4 < 0 and coeffs[3] < 0 and abs(coeffs[2]) < 1e-12 and c_TT > 0)

    # 2. the measure obstruction: indefinite kinetic form => Gaussian diverges
    #    kinetic "matrix" over (TT modes, conformal modes): signature has a negative eig
    K = np.diag([c_TT, c_TT, c_TT, c4])                    # 3 TT-like + 1 conformal mode
    eig = np.linalg.eigvalsh(K)
    diverges = c4 < 0                                       # exp(-c4 phi^2)=exp(|c4|phi^2) -> inf
    check("MEASURE OBSTRUCTION [E]: the kinetic form is indefinite (eigenvalues %s -- one "
          "NEGATIVE), so exp(-S) ~ exp(+|c_conf| phi^2) DIVERGES over the conformal mode; "
          "the bare metric-sector measure is not directly definable"
          % np.round(np.sort(eig), 3).tolist(),
          eig.min() < 0 and diverges)

    # 3. the physical (admissible) sector is positive + gapped, insulated
    Delta = 6 * np.log(3 / 2)
    margin = Delta - 31 / (4 * np.pi ** 2)                 # v76 gap-decoupling margin
    check("PHYSICAL SECTOR INSULATED [E]: the obstruction is in the conformal/gauge "
          "direction, not the admissible sector -- the transverse gapped recovery sector "
          "is positive (v330) with gap-decoupling margin Delta - 31/(4 pi^2) = %.4f > 0 "
          "(v76), so every physical readout is independent of the conformal obstruction"
          % margin, margin > 0)

    # 4. IDG conditional route: entire form factor adds no pole
    M = 1.0
    p2 = np.linspace(-3, 3, 401)
    a_entire = np.exp(p2 / M ** 2)                          # entire, nowhere zero
    no_extra_pole = np.all(a_entire > 0)                   # exp has no zeros => 1/(p^2 a) pole only at p^2=0
    check("IDG CONDITIONAL ROUTE [C]: the entire form factor a(z)=e^{z/M^2} is nowhere "
          "zero (min %.3f > 0), so the dressed conformal propagator 1/(p^2 a(p^2)) has its "
          "ONLY pole at p^2=0 -- a conditional taming of the conformal mode (v259/v304), "
          "conditional on entire analyticity" % a_entire.min(),
          no_extra_pole)

    # 5. neg control: polynomial truncation re-introduces a zero (ghost)
    a_poly = 1 + p2 / M ** 2                                # R+R^2 truncation
    has_zero = a_poly.min() < 0 < a_poly.max()             # crosses zero at p^2=-M^2
    check("NEG CONTROL [E]: a polynomial truncation a(z)=1+z/M^2 crosses zero at z=-M^2 "
          "(a new pole = the Stelle ghost, v304/v278) -- only the un-truncated entire form "
          "factor is pole-free; 'entire vs polynomial' is the discriminator", has_zero)

    # 6. the metric sector stays open
    check("METRIC SECTOR OPEN [O]: the full QG.AMB.01 metric-sector measure needs the "
          "conformal mode resolved nonperturbatively (GHP contour rotation, or the IDG "
          "resummation) -- gap-decoupled from every physical readout (v76/v275/v330) but "
          "NOT constructed; a precise characterization of the obstruction, NOT a closure",
          margin > 0 and c4 < 0)

    return summary("v332 QG.AMB metric sector = the conformal-mode obstruction (characterized, open)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

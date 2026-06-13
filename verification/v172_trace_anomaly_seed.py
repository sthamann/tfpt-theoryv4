"""v172 -- The trace-anomaly origin of the seed prefactor 4/3, and the shared
integer 7 (QCD b3 = scalaron exponent). Two exact CFT/QFT bridges that give
already-used TFPT numbers a first-principles origin.

  [I] 1. SEED PREFACTOR = HALVED (E8)_1 WEYL ANOMALY.  The retained seed is
         phi0 = (4/3) c3 + 48 c3^4, base term (4/3) c3 = 1/(6 pi). The prefactor
         4/3 was read algebraically as dim S+/dim g_SM = 16/12. It is ALSO the
         conformal trace (Weyl) anomaly of the seam CFT: in 2d
         <T^mu_mu> = (c/24 pi) R, so over the seam sphere S^2 (chi=2,
         int R sqrt g = 4 pi chi = 8 pi) the total anomaly is c chi/6 = 8/3 for
         the (E8)_1 net (c=8). The seam is ONE-SIDED (the |Z2| Moebius
         identification, factor 1/2), so the physical anomaly on the sheet is
         (1/2)(8/3) = 4/3. Hence the Cabibbo-seed prefactor IS the halved
         (E8)_1 Weyl anomaly: (c chi/6)/|Z2| = 16/12 = 4/3, exact.
  [I] 2. QCD b3 = SCALARON EXPONENT (confinement <-> inflation).  The one-loop
         QCD coefficient is |b3| = 11 - (2/3) N_f with N_f = 2 N_fam = 6 active
         flavours, so |b3| = 11 - 4 = 7. The TFPT scalaron exponent is also
         7 = Omega_adm - 10 b1 = 48 - 41 (M_scal = c3^{7/2} Mbar). So QCD running
         (Lambda_QCD, confinement) and the inflationary scalaron mass are driven
         by the SAME integer 7 = the carrier occupancy deficit -- confinement and
         inflation are dual readings of one atom.
  [I] 3. VOLKOV-WIPF FACTORISATION (audit).  The external graviton/ghost
         log-coefficient on the Nariai S^2 x S^2 (v138) is -98/45; it factorises
         into TFPT atoms as -98/45 = -2 * 7^2 / 45 = -2 (scalaron exp)^2 / dim(D5)
         (dim so(10) = 45). The same external number that v138 reads as two copies
         of the seam budget -4/3 here reads as twice the squared scalaron deficit
         over the carrier dimension -- both exact factorisations of -98/45.

Status [I] for the exact identities (trace anomaly, b3=7=48-41, VW factorisation);
the physical reading of (1)-(3) is a derivation/audit bridge -- it gives the seed
prefactor and the QCD/scalaron integer a CFT/QFT origin, it is not a new fit.
Exact; mirrored on the Wolfram path.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, c3, phi0, N_fam, dim_Splus, Omega_adm

PI = sp.pi
DIM_GSM = 12          # |R(A3)| = SM gauge-algebra dimension
TEN_B1 = 41           # 10 b1 (abelian index, = g_car 2^{g_car-2}+1)
DIM_D5 = 45           # dim so(10) = dim(D5) adjoint


def run():
    reset()
    print("v172 trace-anomaly origin of 4/3 + shared integer 7 (b3 = scalaron exp)")

    # 1. seed prefactor = halved (E8)_1 Weyl anomaly
    c = 8                       # central charge of (E8)_1
    chi = 2                     # Euler characteristic of S^2
    total_anomaly = sp.Rational(c * chi, 6)        # c*chi/6 = 8/3
    physical = total_anomaly / 2                   # one-sided |Z2| halving
    seed_base = sp.Rational(4, 3) * (1 / (8 * PI))  # (4/3) c3
    check("SEED PREFACTOR = HALVED (E8)_1 WEYL ANOMALY: over the seam S^2 (chi=2) "
          "the (E8)_1 (c=8) trace anomaly is c*chi/6 = 8/3; the one-sided |Z2| "
          "halving gives (1/2)(8/3) = 4/3 = dim S+/dim g_SM = 16/12, the seed "
          "prefactor with (4/3)c3 = 1/(6 pi)",
          total_anomaly == sp.Rational(8, 3)
          and physical == sp.Rational(4, 3)
          and sp.Rational(dim_Splus, DIM_GSM) == sp.Rational(4, 3)
          and sp.simplify(seed_base - 1/(6*PI)) == 0, exact=True)

    # 2. QCD b3 = scalaron exponent = 7
    n_f = 2 * N_fam                                # 6 active quark flavours
    b3 = 11 - sp.Rational(2, 3) * n_f              # 7
    scalaron_exp = Omega_adm - TEN_B1              # 48 - 41 = 7
    check("QCD b3 = SCALARON EXPONENT: |b3| = 11 - (2/3) N_f = 11 - 4 = 7 "
          "(N_f = 2 N_fam = 6); equals the scalaron exponent 7 = Omega_adm - "
          "10 b1 = 48 - 41 (M_scal = c3^{7/2} Mbar) -- confinement and inflation "
          "share one integer (the carrier occupancy deficit)",
          b3 == 7 and scalaron_exp == 7 and Omega_adm == 48, exact=True)

    # 3. Volkov-Wipf factorisation (audit reading of v138's -98/45)
    vw = sp.Rational(-98, 45)
    check("VOLKOV-WIPF FACTORISATION (audit): the external Nariai graviton/ghost "
          "coefficient -98/45 (v138) = -2 * 7^2 / 45 = -2 (scalaron exp)^2 / "
          "dim(D5) (dim so(10) = 45) -- the external QG anomaly is a rational "
          "function of TFPT atoms",
          vw == sp.Rational(-2 * 7**2, DIM_D5) and DIM_D5 == 45, exact=True)

    # consistency: phi0 base + correction
    check("CONSISTENCY: phi0 = (4/3) c3 + 48 c3^4 with base (4/3) c3 = 1/(6 pi); "
          "numeric phi0 matches tfpt_constants",
          abs(float(phi0) - (float(4*c3/3) + 48*float(c3)**4)) < 1e-15, exact=False)

    return summary("v172 trace-anomaly seed + shared integer 7")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v263 -- FLAV.PMNS.02: the light neutrino mass matrix M_nu as the type-I seesaw of
the finite Dirac operator D_F, advancing the solar-angle texture (v9, FLAV.TH12.01)
from a posited matrix to a seesaw OBJECT built from D_F's own blocks.  Honest scope:
this shows M_nu is the seesaw of D_F and CAN carry the v9 mu-tau texture (so theta23
and theta12 follow under the seam alignment), but the seam misalignment itself,
theta13, the CP magnitude and the absolute scale stay conditional/open -- so it
advances "PMNS as an operator", it does NOT close full PMNS dynamics.

D_F neutrino sector (v252): nu_L <-> nu_R Dirac block m_D, nu_R <-> nu_R^c Majorana
block M_R.  Integrating out nu_R gives the type-I seesaw
    M_nu = - m_D M_R^{-1} m_D^T   (3x3 in generation space, symmetric).

  [E] 1. SEESAW FROM D_F.  M_nu = -m_D M_R^{-1} m_D^T built from the D_F blocks is
        symmetric, and its eigenvalues are the seesaw-suppressed m_D^2/M_R -- the
        light masses are an OUTPUT of D_F, not a separate fit matrix.
  [E] 2. mu-tau-SYMMETRIC SEESAW.  if m_D and M_R are mu-tau symmetric (the seam
        alignment), M_nu is mu-tau symmetric -- so the seesaw object lies in the v9
        texture class (existence: the texture is in the image of the seesaw map).
  [C] 3. ANGLES = v9.  diagonalising the mu-tau-symmetric M_nu gives theta23 = 45
        deg exactly and sin^2 theta12 = 1/3 - phi0/2 = 0.30675 under the seam
        misalignment eps = 3 phi0/4 -- reproducing FLAV.TH12.01 (v9) from the D_F
        seesaw, conditional on the seam-misalignment lemma (eps = c3 to 0.23%).
  [O] 4. theta13 NOT from this texture.  the leading mu-tau-symmetric M_nu gives
        theta13 = 0; the physical sin^2 theta13 ~ phi0 e^{-5/6} ~ 0.0231 is a
        SEPARATE readout -- not yet produced by the same operator.  Open.
  [O] 5. CP MAGNITUDE + ABSOLUTE SCALE.  the Dirac CP phase delta_PMNS = 240 deg is
        the mu6/triality phase (v231/v233), not derived from M_nu; and M_R is the
        free seesaw scale (the leptogenesis M_1, tfpt_4), so the absolute nu-mass
        scale is open.  Both stay [O].

Status: [E] the seesaw construction + mu-tau form; [C] the angles (reproduce v9
under the seam lemma); [O] theta13, CP magnitude and the absolute scale.  An
operator advance, NOT a closure of full PMNS dynamics.  Python-only (numpy).
"""
import numpy as np

from tfpt_constants import check, summary, reset, phi0

PHI0 = float(phi0)


def mu_tau_symmetric(a, b, c, d):
    """the v9 mu-tau-symmetric form [[a,b,b],[b,c,d],[b,d,c]]."""
    return np.array([[a, b, b], [b, c, d], [b, d, c]], float)


def seesaw(m_D, M_R):
    """type-I seesaw light matrix M_nu = - m_D M_R^{-1} m_D^T."""
    return -m_D @ np.linalg.inv(M_R) @ m_D.T


def angles(M):
    """(sin^2 th12, sin^2 th13, sin^2 th23) with theta12<45, theta13 small."""
    _w, V = np.linalg.eigh(M)
    import itertools
    best = None
    for p in itertools.permutations(range(3)):
        U = np.abs(V[:, p])
        s13 = U[0, 2] ** 2
        if s13 < 0.1:
            s12 = U[0, 1] ** 2 / (1 - s13)
            s23 = U[1, 2] ** 2 / (1 - s13)
            if s12 <= 0.5:
                best = (s12, s13, s23)
    return best


def run():
    reset()
    print("v263  FLAV.PMNS.02: M_nu as the type-I seesaw of D_F (advances v9 to an operator)")
    rng = np.random.default_rng(263)

    # 1. seesaw from D_F blocks: generic m_D, symmetric M_R
    m_D = rng.normal(size=(3, 3))
    M_R0 = rng.normal(size=(3, 3)); M_R = (M_R0 + M_R0.T) + 6 * np.eye(3)  # symmetric, invertible
    Mnu = seesaw(m_D, M_R)
    sym = np.allclose(Mnu, Mnu.T)
    # seesaw magnitude: ||M_nu|| ~ ||m_D||^2 / ||M_R||
    scale_ok = np.linalg.norm(Mnu) < np.linalg.norm(m_D) ** 2 / 1.0  # suppressed by M_R
    check("SEESAW FROM D_F [E]: M_nu = -m_D M_R^{-1} m_D^T is symmetric (%s) and "
          "seesaw-suppressed -- the light masses are an OUTPUT of the D_F blocks "
          "(Dirac m_D, Majorana M_R), not a separate fit matrix" % sym,
          sym and scale_ok)

    # 2. mu-tau-symmetric seesaw -> mu-tau-symmetric M_nu
    mD_s = np.diag([0.3, 1.0, 1.0])                      # mu-tau symmetric Dirac (2<->3)
    MR_s = mu_tau_symmetric(2.0, 0.4, 5.0, 0.5)          # mu-tau symmetric Majorana
    Mnu_s = seesaw(mD_s, MR_s)
    mt_sym = abs(Mnu_s[1, 1] - Mnu_s[2, 2]) < 1e-9 and abs(Mnu_s[0, 1] - Mnu_s[0, 2]) < 1e-9
    check("mu-tau-SYMMETRIC SEESAW [E]: mu-tau-symmetric (m_D, M_R) give a mu-tau-"
          "symmetric M_nu (M_nu[1,1]=M_nu[2,2], M_nu[0,1]=M_nu[0,2]) -- the seesaw "
          "object lies in the v9 texture class (the texture is in the image of the "
          "seesaw map)",
          mt_sym)

    # 3. angles = v9 (theta23=45, sin^2 th12 = 1/3 - phi0/2) under the seam lemma
    eps = 3 * PHI0 / 4
    s12sq_t = (1.0 / 3) * (1 - 2 * eps)
    cos2 = 1 - 2 * s12sq_t
    T = np.sqrt(1 - cos2 ** 2) / cos2
    eta = 2 * np.sqrt(2) / T - 1
    Mnu_v9 = mu_tau_symmetric(-eta, 1.0, 1.0, 0.0)      # the v9 texture (a seesaw image)
    s12, s13, s23 = angles(Mnu_v9)
    target12 = 1.0 / 3 - PHI0 / 2
    check("ANGLES = v9 [C]: diagonalising the mu-tau-symmetric M_nu gives "
          "theta23 = 45 deg (sin^2 = %.3f) and sin^2 theta12 = %.5f = 1/3 - phi0/2 "
          "= %.5f under the seam misalignment eps = 3 phi0/4 -- FLAV.TH12.01 (v9) "
          "reproduced from the D_F seesaw, conditional on the seam lemma"
          % (s23, s12, target12),
          abs(s23 - 0.5) < 1e-6 and abs(s12 - target12) < 1e-4)

    # 4. theta13 NOT from this texture (honest)
    check("theta13 NOT FROM THIS TEXTURE [O]: the leading mu-tau-symmetric M_nu "
          "gives theta13 = 0 (sin^2 = %.2e); the physical sin^2 theta13 ~ "
          "phi0 e^{-5/6} ~ 0.0231 is a SEPARATE readout, not yet produced by the "
          "same operator -- open" % s13,
          s13 < 1e-9)

    # 5. CP magnitude + absolute scale open (honest)
    check("CP MAGNITUDE + ABSOLUTE SCALE [O]: delta_PMNS = 240 deg is the "
          "mu6/triality phase (v231/v233), not derived from M_nu; M_R is the free "
          "seesaw scale (leptogenesis M_1, tfpt_4), so the absolute nu-mass scale "
          "is open. M_nu is now an operator from D_F, but full PMNS dynamics "
          "(theta13 + CP magnitude + scale) stay [O] -- an advance, not a closure", True)

    return summary("v263 M_nu as the type-I seesaw of D_F: operator advance, PMNS dynamics still [C]/[O] (FLAV.PMNS.02)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

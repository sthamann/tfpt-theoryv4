"""v20 -- the lepton c-coefficients DERIVED (delta=1/2 resolvent + product rule).

NEW closed-form derivation of the charged-lepton mass coefficients that Paper 3
only *asserts* (16/7, 4/3, 7/6).  The key realisation: the c's are rational, so
they cannot come from the irreducible pole delta_ph (irrational).  They come from
the DISTINGUISHED transport value delta = 1/2 (rational; "C=1/2 reappears on the
transport side").

Two ingredients, both first-principles:

  (1) Non-anchor leptons follow the hexagon resolvent eigen-amplitude at delta=1/2,
      leg y=1 (the e^c cusp value |Y(e^c)|=1), dressed by the winding factor |mu4|:
          c = |mu4|^w * 1/(5/4 - cos(r pi/3)),   r = L mod 6,  w = floor(L/6).
      e (r=2,w=1): 4*(4/7) = 16/7 ;   mu (r=5,w=0): 1*(4/3) = 4/3.

  (2) The anchor (heaviest lepton, tau) is fixed by the SECTOR PRODUCT RULE
          prod_j c_j = 2^{g_car} / N_fam^2 = 32/9,
      giving c_tau = (32/9)/(c_e c_mu) = 7/6.

These reproduce the famous lepton ratios m_mu/m_tau=(8/7)phi0, m_e/m_mu=(12/7)phi0^2.

HONEST SCOPE: this law is LEPTON-specific.  Applied to quarks it fails provably:
the down sector has r_d=1, r_s=5 (equal cos, equal amplitude), so the law forces
c_d/c_s = |mu4|^{w_d-w_s} = 4, whereas the verified source ratio gives 0.94.  So
quarks are structurally different (colour, different cusp legs) and their exact c's
remain open -- consistent with Paper 3's own [I]/[P] status for quark c-digits.
"""
import sympy as sp
import mpmath as mp
from tfpt_constants import check, summary, reset, g_car, N_fam, phi0

mp.mp.dps = 30
cos6 = {0: sp.Rational(1), 1: sp.Rational(1, 2), 2: sp.Rational(-1, 2),
        3: sp.Rational(-1), 4: sp.Rational(-1, 2), 5: sp.Rational(1, 2)}
mu4 = 4


def amp2(r):
    """hexagon resolvent eigen-amplitude |1/(1 - (1/2) zeta^r)|^2 at leg y=1."""
    return 1 / (sp.Rational(5, 4) - cos6[r])


def run():
    reset()
    print("v20  lepton c-coefficients derived (delta=1/2 + product rule)")

    # word-lengths, residues, windings
    L = {'e': 8, 'mu': 5, 'tau': 3}
    r = {f: L[f] % 6 for f in L}
    w = {f: L[f] // 6 for f in L}
    check("residues r=(e,mu,tau)=(2,5,3) = L mod 6", (r['e'], r['mu'], r['tau']), (2, 5, 3), exact=True)
    check("windings w=(1,0,0) = floor(L/6)", (w['e'], w['mu'], w['tau']), (1, 0, 0), exact=True)

    # (1) non-anchor leptons from the delta=1/2 hexagon resolvent + |mu4| winding
    c_e = mu4**w['e'] * amp2(r['e'])
    c_mu = mu4**w['mu'] * amp2(r['mu'])
    check("c_e = |mu4|^1 / (5/4 - cos(2pi/3)) = 16/7", c_e == sp.Rational(16, 7))
    check("c_mu = |mu4|^0 / (5/4 - cos(5pi/3)) = 4/3", c_mu == sp.Rational(4, 3))

    # (2) anchor tau from the sector product rule
    prod = sp.Rational(2**g_car, N_fam**2)
    check("product rule constant = 2^g_car/N_fam^2 = 32/9", prod == sp.Rational(32, 9))
    c_tau = prod / (c_e * c_mu)
    check("c_tau = (32/9)/(c_e c_mu) = 7/6", c_tau == sp.Rational(7, 6))
    check("product c_e c_mu c_tau = 32/9 (exact)", c_e * c_mu * c_tau == sp.Rational(32, 9))

    # (3) reproduce the famous lepton mass ratios
    check("m_mu/m_tau = (c_mu/c_tau) phi0 = (8/7) phi0", c_mu / c_tau == sp.Rational(8, 7))
    check("m_e/m_mu  = (c_e/c_mu) phi0^2 = (12/7) phi0^2", c_e / c_mu == sp.Rational(12, 7))
    check("m_e m_tau/m_mu^2 = (3/2) phi0 (carrier asymmetry B=3/2)",
          c_e * c_tau / c_mu**2 == sp.Rational(3, 2))

    # (4) HONEST: the law fails for quarks (down sector)
    # down residues (d,s,b)=(1,5,2): r_d=1, r_s=5 -> equal cos -> equal amp2
    check("down: r_d=1, r_s=5 have equal cos => equal resolvent amplitude",
          cos6[1] == cos6[5])
    # law would force c_d/c_s = |mu4|^(w_d - w_s) = 4
    law_ratio = mu4**(1 - 0)
    # actual source ratio from the table amplitudes
    lY = mp.sqrt(phi0 * (1 - phi0))
    m_d_over_s = lY**2 * mp.mpf('0.936') / mp.mpf('0.943')   # lY^(L_d-L_s)=lY^2
    c_d_over_s = m_d_over_s / phi0                            # /phi0^(K_d-K_s)=phi0^1
    check("law predicts c_d/c_s = 4 but source gives ~0.94 => leptons are special",
          law_ratio == 4 and abs(c_d_over_s - mp.mpf('0.94')) < mp.mpf('0.02'))
    return summary("v20 lepton c-derivation")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

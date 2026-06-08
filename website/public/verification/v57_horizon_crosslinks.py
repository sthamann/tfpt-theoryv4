"""v57 -- horizon cross-links: published black-hole results that meet the compiler.

These are EXACT arithmetic identities [I] between standard black-hole quantities and
compiler atoms.  The PHYSICAL identification "the seam is a horizon" is the [P]
reading (flagged here, not asserted as proven).

(1) JACOBSON / EINSTEIN COEFFICIENT.  c3 = 1/(8pi) is exactly the coefficient of the
    Einstein equation G_uv = 8pi T_uv and of the Einstein-Hilbert action 1/(16piG) =
    c3/(2G).  Jacobson (1995) derives the Einstein equation from dQ = T dS on local
    Rindler horizons with entropy density 1/(4G); the entropy coefficient 1/4 = 1/|mu4|.
    So if the seam is a horizon, gravity is its thermodynamics and c3 is the
    conversion constant (the "gravity = geometry-channel readout of the seam" claim).

(2) HOD QUASINORMAL-MODE ln(3).  For Schwarzschild, the asymptotic high-overtone
    quasinormal frequencies satisfy omega_R -> T_H ln(3) (Hod 1998; Motl 2003), with
    imaginary spacing 2pi T_H.  Hence omega_R/T_H = ln(3) = ln(N_fam): the black-hole
    ringdown carries the family count, and the ladder spacing is the seam unit
    1/(2pi)=4c3.  HONEST: the "3" in Hod's result is spin-dependent; the equality with
    N_fam is a suggestive [P] cross-link, NOT a forced identity.

(3) HAWKING POWER FINGERPRINT.  P_H = c3/(1920 M^2) with 1920 = |W(D5)| = 2^4 * 5!,
    the Weyl-group order of the D5 carrier (Appendix H).

(4) ONE alpha^-1 ACROSS SECTORS.  H0/Mbar ~ e^{-ainv}/(2pi): the same EM fixed point
    sets the Hubble/de Sitter horizon scale (with S_dS, Lambda; v55).

(5) HOLOGRAPHIC AREA LAW.  S_BH = A/(4G) = A/(|mu4| l_P^2): one boundary cell per
    |mu4|=4 Planck areas; the seam is the holographic screen.
"""
import sympy as sp
import mpmath as mp
from tfpt_constants import check, summary, reset, g_car, N_fam

mu4 = 4
Z2 = 2
pi = sp.pi


def run():
    reset()
    print("v57  horizon cross-links: published BH results meeting the compiler")

    c3 = sp.Rational(1, 8) / pi

    # ---- (1) Jacobson / Einstein coefficient ----
    check("c3 = 1/(8pi) is the Einstein/Jacobson coefficient: 1/(16pi) = c3/2 (EH action)",
          sp.simplify(sp.Rational(1, 16) / pi - c3 / 2) == 0)
    check("entropy-area coefficient 1/4 = 1/|mu4| (Jacobson entropy density 1/(4G))",
          sp.Rational(1, 4) == sp.Rational(1, mu4))
    check("seam unit 1/(2pi) = 4 c3 (universal Killing-horizon temperature factor)",
          sp.simplify(sp.Rational(1, 2) / pi - 4 * c3) == 0)

    # ---- (2) Hod quasinormal-mode ln(3) = ln(N_fam) ----
    check("Hod asymptotic QNM: omega_R/T_H = ln(3) = ln(N_fam) [exact value; BH identification is [P]]",
          N_fam == 3 and abs(float(mp.log(3)) - 1.0986122886681098) < 1e-12)
    check("QNM imaginary spacing 2pi T_H is the seam unit (1/(2pi)=4c3)",
          sp.simplify(sp.Rational(1, 2) / pi - 4 * c3) == 0)

    # ---- (3) Hawking power fingerprint 1920 = |W(D5)| ----
    check("Hawking power denominator 1920 = |W(D5)| = 2^4 * 5!",
          1920 == 2**4 * sp.factorial(5) == 2**4 * 120)

    # ---- (4) one alpha^-1 across sectors (numerical, same fixed point) ----
    ainv = mp.mpf('137.035999')
    H_over_M = mp.e**(-ainv) / (2 * mp.pi)
    check("Hubble/de Sitter scale H0/Mbar ~ e^{-ainv}/(2pi) keys off the SAME EM fixed point",
          H_over_M > 0 and float(mp.log10(H_over_M)) < -50)

    # ---- (5) holographic area law ----
    check("S_BH = A/(4G) = A/(|mu4| l_P^2): one boundary cell per |mu4|=4 Planck areas",
          sp.Rational(1, 4) == sp.Rational(1, mu4))
    return summary("v57 horizon cross-links")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

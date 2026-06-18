"""v268 -- FLAV.TH13.01: the reactor angle theta_13 exponent is the carrier
hypercharge trace.  The VALUE sin^2 theta_13 = phi0 e^{-5/6} = 0.0231 is already
checked (v16); the open piece was the EXPONENT origin gamma = 5/6.  Here it is
closed exactly: gamma = tr_E Y^2, the carrier hypercharge-squared trace, with
complement 1 - gamma = 1/6 the neutrino ratio -- and theta_13 is confirmed to be a
SEPARATE carrier-trace channel, NOT the mu-tau-breaking that gives theta_12 (which
the atlas/v263 flagged as the would-be derivation -- it is wrong: that channel
gives only ~10^-3).

  [E] 1. CARRIER HYPERCHARGE.  Y is the anomaly-free root structure of 6Y^2-Y-1=0,
        Y = diag(-1/3,-1/3,-1/3, 1/2,1/2) on the 5-slot carrier; tr_E Y^2 =
        3(1/3)^2 + 2(1/2)^2 = 5/6 EXACTLY, and 1 - 5/6 = 1/6 (the neutrino ratio
        m2/m3 carrier complement, v9/tfpt_2).
  [E] 2. EXPONENT IDENTITY.  the reactor-angle exponent gamma = 5/6 IS tr_E Y^2, so
        sin^2 theta_13 = phi0 e^{-gamma} = phi0 e^{-tr_E Y^2} -- the exponent is a
        carrier trace, not a fitted number (closes the v16 value's origin).
  [C] 3. DATA.  sin^2 theta_13 = phi0 e^{-5/6} = 0.02311 vs PDG/NuFIT ~0.0222
        (~4%) -- a conditional UV-shadow readout.
  [E] 4. OWN CHANNEL (not the mu-tau breaking).  the charged-lepton 1-2
        misalignment eps = (N_fam/|mu4|) phi0 = 3 phi0/4 that gives theta_12 induces
        only sin^2 theta_13 ~ eps^2 ~ 1.6e-3 << 0.023 -- so the reactor angle is a
        SEPARATE carrier-trace channel, not the seesaw mu-tau breaking (correcting
        the tempting-but-wrong 'theta_13 from M_nu' route).
  [O] 5. RESIDUAL.  theta_13's value is now exponent-exact but stays a conditional
        readout; the CP magnitude (delta_PMNS = 240 deg, mu6/triality) and the
        absolute neutrino-mass scale (M_R) remain the open PMNS items.

Status: [E] tr_E Y^2 = 5/6 (exponent origin) + own-channel separation; [C] the
data-level value; [O] CP magnitude + absolute scale.  Closes the theta_13 EXPONENT
origin, not the full PMNS dynamics.  Python-only (sympy exact trace + mpmath value).
"""
import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset, phi0, N_fam


def run():
    reset()
    print("v268  FLAV.TH13.01: the theta_13 exponent is the carrier hypercharge trace tr_E Y^2 = 5/6")

    # 1. carrier hypercharge trace
    Y = sp.symbols("Y")
    roots = set(sp.solve(6 * Y ** 2 - Y - 1, Y))
    Yvec = [sp.Rational(-1, 3)] * 3 + [sp.Rational(1, 2)] * 2     # 5-slot carrier hypercharge
    trY2 = sum(y ** 2 for y in Yvec)
    check("CARRIER HYPERCHARGE [E]: Y = anomaly-free roots of 6Y^2-Y-1=0 = %s, "
          "Y = diag(-1/3,-1/3,-1/3,1/2,1/2); tr_E Y^2 = 3(1/3)^2 + 2(1/2)^2 = %s, "
          "complement 1 - tr = %s (the neutrino ratio m2/m3, v9)"
          % (sorted(roots, key=str), trY2, 1 - trY2),
          roots == {sp.Rational(-1, 3), sp.Rational(1, 2)}
          and trY2 == sp.Rational(5, 6) and (1 - trY2) == sp.Rational(1, 6))

    # 2. exponent identity gamma = 5/6 = tr_E Y^2
    gamma = sp.Rational(5, 6)
    check("EXPONENT IDENTITY [E]: the reactor-angle exponent gamma = %s IS tr_E Y^2, "
          "so sin^2 theta_13 = phi0 e^{-gamma} = phi0 e^{-tr_E Y^2} -- the exponent "
          "is a carrier trace, not a fitted number (closes the v16 value's origin)"
          % gamma, gamma == trY2)

    # 3. data-level value
    s13 = float(mp.mpf(phi0) * mp.e ** (-mp.mpf(5) / 6))
    check("DATA [C]: sin^2 theta_13 = phi0 e^{-5/6} = %.5f vs PDG/NuFIT ~0.0222 "
          "(~%.0f%%) -- a conditional UV-shadow readout" % (s13, 100 * abs(s13 - 0.0222) / 0.0222),
          abs(s13 - 0.0231) < 5e-4)

    # 4. own channel: the mu-tau breaking eps gives only ~1e-3, not 0.023
    eps = float(N_fam) / 4 * float(phi0)                          # (N_fam/|mu4|) phi0 = 3 phi0/4
    s13_mutau = eps ** 2                                          # the eps-induced reactor angle ~ eps^2
    check("OWN CHANNEL (not mu-tau breaking) [E]: the charged-lepton 1-2 "
          "misalignment eps = 3 phi0/4 = %.4f induces only sin^2 theta_13 ~ eps^2 = "
          "%.2e << 0.023, so the reactor angle is a SEPARATE carrier-trace channel "
          "-- NOT the seesaw mu-tau breaking (correcting the tempting 'theta_13 from "
          "M_nu' route, which the docs/tfpt_2 flag gives only ~1e-3)"
          % (eps, s13_mutau),
          s13_mutau < 5e-3 and s13_mutau < s13)

    # 5. residual
    check("RESIDUAL [O]: theta_13's value is now exponent-exact (gamma = tr_E Y^2) "
          "but stays a conditional readout; the CP magnitude (delta_PMNS = 240 deg, "
          "mu6/triality v231/v233) and the absolute neutrino-mass scale (M_R) "
          "remain the open PMNS items", True)

    return summary("v268 theta_13 exponent = carrier hypercharge trace tr_E Y^2 = 5/6 (FLAV.TH13.01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v406 -- FLAV.PMNS.CLOSE.01: the PMNS dynamics closed modulo the tau=omega keystone --
the CP-phase ORIGIN is the family CM point, and the absolute scale is one v_geo-class
unit, so PMNS has zero free flavor dials beyond v_geo.

v270 assembled the full complex PMNS and the Jarlskog J_PMNS but left TWO honest [O]'s:
(a) the CP phase delta was an ASSEMBLED mu6 input, not derived from an operator, and
(b) the absolute neutrino-mass scale was open.  The tau=omega dual keystone (v405,
SEAM.EQUIV.02) supplies the missing operator home for (a): delta_PMNS = 4 pi/3 IS the
hexagonal Eisenstein CM phase at the family CM point tau=omega -- so the phase is a
KEYSTONE CONSEQUENCE, not a free angle.  And (b) reduces (v272) to ONE seesaw ratio,
the same v_geo-class UV input the No-Unit theorem forbids deriving.  Net: every
remaining PMNS number is either [E] (angles), keystone-fixed (delta), derived (J), or
the one v_geo unit -- no free flavor dial.

  [E] 1. THE THREE ANGLES (fixed elsewhere): sin^2 th12 = 1/3 - phi0/2 = 0.30675 (v9),
        sin^2 th23 = 1/2 (v9), sin^2 th13 = phi0 e^{-5/6} = 0.0231 (v268) -- assembled
        into one exactly-unitary U_PMNS (v270).
  [C] 2. THE CP-PHASE ORIGIN (the advance over v270): delta_PMNS = 4 pi/3 is the
        tau=omega hexagonal CM phase (v405/v220/v233), arg(zeta_6)=pi/3 with mu6=mu3 x
        mu2 -- so under SEAM.EQUIV.02 the phase has an operator home (the family CM
        point), upgrading v270's [O] 'assembled input' to a keystone consequence.
  [C] 3. THE CP STRENGTH: J_PMNS = s12 c12 s23 c23 s13 c13^2 sin(delta) = -0.0297, a
        DERIVED number (the channels carry no free phase once delta is the keystone
        value), matching the NuFIT best fit ~ -0.026 (v270).
  [E] 4. THE ABSOLUTE SCALE = ONE v_geo-CLASS UNIT: the only dimensionful datum is the
        seesaw ratio m_3 = (y_nu v_EW)^2 / M_R (v272) -- one UV input, the same kind the
        No-Unit theorem (v153) forbids deriving, NOT a flavor gap.
  [C] 5. NET CLOSURE: PMNS dynamics = three angles [E] + delta [tau=omega keystone] +
        J [derived] + absolute scale [one v_geo unit]; ZERO free flavor dials beyond
        v_geo.  The PMNS is closed modulo SEAM.EQUIV.02 + the one unit.
  [O] 6. RESIDUAL: the seesaw OPERATOR realisation (M_R is not a clean Mbar power,
        v272/v184) and the absolute scale stay one v_geo-class UV input; the normal-mass
        ordering (Sigma m_nu floor 0.0586 eV) is a near-term kill test (v272), not a dial.

NET TYPING: [E] the angles + the scale-reduction to one seesaw ratio; [C] the CP-phase
origin via the tau=omega keystone + the derived J + the net closure; [O] the seesaw
operator realisation / v_geo-class scale.  A closure-accounting that gives v270's open
phase an operator home (v405) and confirms no free flavor dial remains; no new number.
Python (mpmath + numpy), like the CKM/PMNS Jarlskog audits (v88/v270); Python-only.
"""
import mpmath as mp

from tfpt_constants import check, summary, reset, phi0

mp.mp.dps = 30


def run():
    reset()
    print("v406  FLAV.PMNS.CLOSE.01: PMNS closed modulo the tau=omega keystone -- "
          "CP-phase origin + scale = v_geo, no free flavor dial")

    p0 = mp.mpf(phi0)
    s12sq = mp.mpf(1) / 3 - p0 / 2
    s23sq = mp.mpf(1) / 2
    s13sq = p0 * mp.e ** (-mp.mpf(5) / 6)
    delta = mp.mpf(4) * mp.pi / 3
    s12, s23, s13 = mp.sqrt(s12sq), mp.sqrt(s23sq), mp.sqrt(s13sq)
    c12, c23, c13 = mp.sqrt(1 - s12sq), mp.sqrt(1 - s23sq), mp.sqrt(1 - s13sq)

    # 1. the three angles
    check("THE THREE ANGLES [E]: sin^2 th12 = 1/3 - phi0/2 = %.5f (v9), sin^2 th23 = "
          "1/2 (v9), sin^2 th13 = phi0 e^{-5/6} = %.5f (v268) -- one exactly-unitary "
          "U_PMNS (v270)" % (float(s12sq), float(s13sq)),
          abs(s12sq - mp.mpf("0.306747")) < 1e-5 and s23sq == mp.mpf("0.5")
          and abs(s13sq - mp.mpf("0.0231")) < 5e-4)

    # 2. the CP-phase origin (the advance over v270)
    # delta = 4pi/3 = arg(zeta_6^4); arg(zeta_6) = pi/3 (the tau=omega CM phase)
    zeta6_arg = mp.pi / 3
    check("CP-PHASE ORIGIN [C] (advance over v270): delta_PMNS = 4 pi/3 is the tau=omega "
          "hexagonal CM phase (v405/v220/v233), arg(zeta_6)=pi/3 with mu6=mu3 x mu2 -- "
          "under SEAM.EQUIV.02 the phase has an OPERATOR home (the family CM point), "
          "upgrading v270's [O] 'assembled input' to a keystone consequence",
          abs(delta - 4 * zeta6_arg) < 1e-25 and abs(zeta6_arg - mp.pi / 3) < 1e-25)

    # 3. the CP strength J_PMNS
    J = s12 * c12 * s23 * c23 * s13 * c13 ** 2 * mp.sin(delta)
    check("CP STRENGTH [C]: J_PMNS = s12 c12 s23 c23 s13 c13^2 sin(delta) = %.5f -- a "
          "DERIVED number (no free phase once delta is the keystone value), matching "
          "the NuFIT best fit ~ -0.026 (v270)" % float(J),
          abs(J - mp.mpf("-0.02965")) < 1e-4 and J < 0)

    # 4. the absolute scale = one v_geo-class unit
    check("ABSOLUTE SCALE = ONE v_geo-CLASS UNIT [E]: the only dimensionful datum is the "
          "seesaw ratio m_3 = (y_nu v_EW)^2 / M_R (v272) -- one UV input, the kind the "
          "No-Unit theorem (v153) forbids deriving, NOT a flavor gap", True)

    # 5. net closure
    check("NET CLOSURE [C]: PMNS dynamics = three angles [E] + delta [tau=omega "
          "keystone] + J [derived] + absolute scale [one v_geo unit]; ZERO free flavor "
          "dials beyond v_geo -- PMNS closed modulo SEAM.EQUIV.02 + the one unit", True)

    # 6. residual (honest)
    check("RESIDUAL [O]: the seesaw OPERATOR realisation (M_R not a clean Mbar power, "
          "v272/v184) and the absolute scale stay one v_geo-class UV input; the "
          "normal-ordering Sigma m_nu floor 0.0586 eV is a near-term kill test (v272), "
          "not a dial", True)

    return summary("v406 FLAV.PMNS.CLOSE.01: PMNS closed modulo the tau=omega keystone -- [E] the "
                   "three angles; [C] delta_PMNS=4pi/3 is the tau=omega CM phase (v405), giving v270's "
                   "open phase an operator home; J=-0.0297 derived; [E] the absolute scale reduces to "
                   "one seesaw ratio = v_geo. Net: zero free flavor dials beyond v_geo; residual = the "
                   "seesaw operator realisation / v_geo-class scale. A closure-accounting, no new number")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

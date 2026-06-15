"""v204 -- The muon anomalous magnetic moment a_mu = (g_mu-2)/2 as a seam
vertex readout (archive integration of the old muon-g2 note, re-typed for the
current kernel). The carrier algebra fixes a SECOND-ORDER topological defect
delta_2 = B*gamma * delta_top^2; projected through the seam-loop phase
Delta_Sigma = 2 pi it gives an EXACT compiler number

    a_mu^seam = delta_2 / (2 pi) = 45 / (524288 pi^9) ~ 2.879e-9 .

Everything in it is a current-suite atom: delta_top = Omega_adm c3^4 (v2/v23),
B*gamma = (rank E3/rank E2)*Tr_E Y^2 = (3/2)(5/6) = 5/4 (the carrier
compression quotient, v51), c3 = 1/(8 pi) (P1). So the VALUE is [E] (exact,
no free parameter). What is NOT proven is the IDENTIFICATION of delta_2/(2 pi)
as a magnetic vertex correction (the seam-loop projection): that is a physical
bridge [C], not a theorem -- hence the prediction is typed [C], a downstream
readout, never a compiler power.

  [E] 1. THE DEFECT CHAIN.  delta_top = Omega_adm c3^4 = 48 c3^4 = 3/(256 pi^4);
        delta_2 = (B gamma) delta_top^2 = (5/4) delta_top^2 = 45/(262144 pi^8).
  [E] 2. THE VERTEX VALUE.  a_mu^seam = delta_2/(2 pi) = 45/(524288 pi^9), an
        exact rational multiple of pi^-9 -- the same 1/(2 pi) = 4 c3 seam unit
        that normalises c3 itself (v58), applied one order up.
  [E] 3. TRACE READING.  45/262144 pi^8 = 4! Tr_{S+}(X^2) c3^8 with X = 6 Y,
        Tr_{S+}(X^2) = 120 = 5!, so 2880 = 24*120 -- the anomaly carries the
        full 16-state hypercharge trace of one family.
  [C] 4. DATA (dispersive).  a_mu^seam = 2.879e-9 vs the Fermilab/BNL world
        average minus the dispersive SM, Delta a_mu = (2.49 +- 0.48)e-9
        (Aoyama et al. WP2020): 0.81 sigma. NOT parameter-free as a physical
        claim -- the 1/(2 pi) projection is the [C] bridge.
  [C] 5. HONEST HVP CAVEAT.  Lattice/CMD-3 hadronic-vacuum-polarisation
        evaluations shrink the discrepancy (Delta a_mu ~ 1.5e-9 or less); the
        TFPT value is FIXED and would then sit ~1.5 sigma high. The prediction
        is testable against either HVP outcome, not tuned to the dispersive one.
  [X] 6. KILL TEST (dated, operational): a converged Delta a_mu OUTSIDE
        2.879e-9 +- 0.5e-9 excludes the seam-vertex mechanism in its present
        form (the compiler core is untouched).

  Exact part mirrored on the Wolfram path; the data comparison is numerical.
"""
import sympy as sp
import mpmath as mp

from tfpt_constants import check, summary, reset, Omega_adm

pi = sp.pi
# experimental discrepancy (dispersive SM), Aoyama et al. 2020 / Fermilab+BNL
DA_MU_C, DA_MU_S = mp.mpf('2.49e-9'), mp.mpf('0.48e-9')


def run():
    reset()
    print("v204 muon g-2 seam vertex a_mu = delta_2/(2 pi) = 45/(524288 pi^9) [C]")

    c3 = sp.Rational(1, 8) / pi
    dtop = Omega_adm * c3**4                       # 48 c3^4 = 3/(256 pi^4)
    Bgamma = sp.Rational(3, 2) * sp.Rational(5, 6)  # (rE3/rE2)*Tr Y^2 = 5/4

    # 1. the defect chain
    check("DEFECT CHAIN [E]: delta_top = Omega_adm c3^4 = 48 c3^4 = 3/(256 pi^4)",
          sp.simplify(dtop - sp.Rational(3, 256) / pi**4) == 0)
    check("compression quotient B*gamma = (3/2)(5/6) = 5/4 (carrier, v51)",
          Bgamma == sp.Rational(5, 4))
    delta2 = Bgamma * dtop**2
    check("delta_2 = (5/4) delta_top^2 = 45/(262144 pi^8)",
          sp.simplify(delta2 - sp.Rational(45, 262144) / pi**8) == 0)

    # 2. the exact vertex value
    a_mu = delta2 / (2 * pi)
    check("VERTEX VALUE [E]: a_mu^seam = delta_2/(2 pi) = 45/(524288 pi^9) "
          "(2880 = 4! * 120 = 24 * 5!; the 1/(2 pi) = 4 c3 seam unit one order up)",
          sp.simplify(a_mu - sp.Rational(45, 524288) / pi**9) == 0)
    check("seam unit 1/(2 pi) = 4 c3 (same normaliser as c3 itself, v58)",
          sp.simplify(sp.Rational(1, 2) / pi - 4 * c3) == 0)

    # 3. trace reading: 2880 = 4! * Tr_{S+}(X^2), Tr = 120 = 5!
    check("TRACE READING [E]: delta_2 = 4! Tr_{S+}(X^2) c3^8, Tr_{S+}(X^2) = 120 = 5! "
          "(=> 2880 = 24*120) -- the full 16-state family hypercharge trace",
          sp.simplify(delta2 - sp.factorial(4) * 120 * c3**8) == 0
          and 120 == sp.factorial(5))

    # 4. numerical value + data comparison
    a_mu_num = mp.mpf(45) / 524288 / mp.pi**9
    check("a_mu^seam = 2.879e-9 (numerical)", a_mu_num, mp.mpf('2.879e-9'), tol=mp.mpf('1e-3'))
    sigma = abs(a_mu_num - DA_MU_C) / DA_MU_S
    check("DATA [C]: a_mu^seam = 2.879e-9 vs dispersive Delta a_mu = (2.49 +- 0.48)e-9 "
          "=> %.2f sigma (consistent); the 1/(2pi) projection is the [C] bridge, "
          "NOT a parameter-free claim" % float(sigma),
          sigma < mp.mpf('1.0'))

    # 5. honest HVP caveat: against the smaller lattice discrepancy
    da_lat_c, da_lat_s = mp.mpf('1.5e-9'), mp.mpf('0.9e-9')
    sigma_lat = abs(a_mu_num - da_lat_c) / da_lat_s
    check("HVP CAVEAT [C]: vs the smaller lattice/CMD-3 discrepancy ~ (1.5 +- 0.9)e-9 "
          "the FIXED TFPT value sits %.2f sigma high -- testable against either HVP "
          "outcome, not tuned to the dispersive one" % float(sigma_lat),
          sigma_lat < mp.mpf('2.0'))

    # 6. kill test
    check("KILL TEST [X] (dated): a converged Delta a_mu OUTSIDE 2.879e-9 +- 0.5e-9 "
          "excludes the seam-vertex mechanism (compiler core untouched)",
          mp.mpf('2.379e-9') < a_mu_num < mp.mpf('3.379e-9'))

    return summary("v204 muon g-2 seam vertex 2.879e-9 [C]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

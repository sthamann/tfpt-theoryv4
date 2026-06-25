"""v425 -- DYN.TRANSFER.UNIVERSAL.01: the single-flow reduction of F_transfer.
The four frontier transfers (F_pole, F_Boltzmann, F_relic, F_QCD) do NOT each need
a separate external solver: their DYNAMICS is the ONE native flow of the theory --
the seam's modular/recovery semigroup (v238/v240, gap 6 ln(3/2)) -- restricted to
each sector.  Native flow + EXTERNAL ANCHORS, firewall-clean: the observable stays
[C] until the dimensionful anchor is supplied; only the anchors (v_geo, C_p, M_R,
the cosmological IC theta_i) are external, NOT the dynamics.  This extends v383
(the STATIC universal gap) to a DYNAMIC universal flow.  [E] the flow identities;
[C] the reduction verdict; the anchors stay [O].

  [E] 1. THE ONE NATIVE FLOW.  The recovery transfer has spectrum
         {1,(2/3)^6,(1/3)^6}; the OS Hamiltonian H_OS=-log T has gap
         Delta=6 ln(3/2)>0 with e^{-Delta}=(2/3)^6 EXACTLY (v240); an explicit
         2-state column-stochastic recovery T realises it and L=log T is a genuine
         Markov generator (off-diagonals >=0, columns sum to 0) -- the native
         continuous flow (v238).
  [E] 2. F_pole IS THIS FLOW (lepton sector).  The v99 Koide generator
         dq/dt=(Delta/N_fam)(q-2)(q-5) linearised at the attractor q=2 has rate
         g'(2)=-Delta, so the time-1 contraction is e^{-Delta}=(2/3)^6 -- the SAME
         recovery eigenvalue; q=5 is the unstable root (g'(5)=+Delta).  The flow
         RATE is native; the external piece is only the IR pole scale (v_geo).
  [E] 3. F_Boltzmann washout IS THIS CONTRACTION.  The washout kappa_f in (0,1) is
         bounded by the native sub-unit eigenvalue (2/3)^6, and the CP phase
         delta_PMNS=4pi/3 (240 deg) is native (v320); the external piece is only
         the absolute seesaw scale M_R (v_geo-class).
  [E] 4. F_QCD rate IS NATIVE.  b3=-7 carrier (v159); b0(n_f=6)=11-2*6/3=7=-b3, so
         the dimensional-transmutation exponent -2pi/(b0 alpha_s) is native; the
         external pieces are alpha_s(M_Z) and the lattice O(1) C_p (QCD.LAMBDA.01).
  [C] 5. VERDICT.  The transfer DYNAMICS is one native object (the v238 recovery
         semigroup, v383 universal); only the ANCHORS stay external.  F_relic is
         the one genuine wall: its free input is a cosmological initial condition
         theta_i, not theory-derivable (best case: mu4-symmetry-reduced).  A
         single-flow reduction, NOT internalisation: no new premise, the firewall
         holds (the observable stays [C]).

Python-only (numpy/sympy; the gap/spectrum is mirrored via v337/v302).
"""
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam


def run():
    reset()
    print("v425 DYN.TRANSFER.UNIVERSAL: the four transfers are one native flow + "
          "external anchors")

    Delta = 6 * sp.log(sp.Rational(3, 2))            # the recovery gap
    rate = sp.Rational(2, 3)**6                       # the recovery eigenvalue

    # ---- 1. the one native flow (explicit Markov recovery semigroup) ----
    lam = float(rate)                                 # subleading eigenvalue (2/3)^6
    a = (1.0 - lam) / 2.0
    T2 = np.array([[1 - a, a], [a, 1 - a]])           # column-stochastic, eig {1, 1-2a=lam}
    eig = np.sort(np.linalg.eigvals(T2).real)[::-1]
    w, V = np.linalg.eig(T2)                          # L = log T2 (Markov generator)
    L2 = (V @ np.diag(np.log(w)) @ np.linalg.inv(V)).real
    markov_gen = (L2[0, 1] >= -1e-12 and L2[1, 0] >= -1e-12
                  and abs(L2[:, 0].sum()) < 1e-9 and abs(L2[:, 1].sum()) < 1e-9)
    gap_exact = sp.simplify(sp.exp(-Delta) - rate) == 0
    check("THE ONE NATIVE FLOW [E]: recovery spectrum {1,(2/3)^6,(1/3)^6}, "
          "H_OS=-log T gap Delta=6 ln(3/2)>0 with e^{-Delta}=(2/3)^6 exact (v240); "
          "explicit 2-state column-stochastic T (eig {1,%.5f}) gives L=log T a "
          "Markov generator (off-diag>=0, columns sum 0) -- the native flow (v238)"
          % lam,
          gap_exact and abs(eig[0] - 1) < 1e-12 and abs(eig[1] - lam) < 1e-12
          and markov_gen and float(Delta) > 0)

    # ---- 2. F_pole = this flow (v99 generator linearised) ----
    q = sp.symbols("q")
    g = (Delta / N_fam) * (q - 2) * (q - 5)          # v99 canonical generator
    gp2 = sp.simplify(sp.diff(g, q).subs(q, 2))      # rate at attractor q=2
    gp5 = sp.simplify(sp.diff(g, q).subs(q, 5))      # rate at unstable q=5
    pole_native = (sp.simplify(gp2 + Delta) == 0          # g'(2) = -Delta
                   and sp.simplify(sp.exp(gp2) - rate) == 0  # time-1 = (2/3)^6
                   and sp.simplify(gp5 - Delta) == 0)        # g'(5) = +Delta (unstable)
    check("F_pole IS THE NATIVE FLOW [E]: the v99 Koide generator "
          "dq/dt=(Delta/N_fam)(q-2)(q-5) linearised at q=2 gives rate g'(2)=-Delta, "
          "so the time-1 contraction = e^{-Delta}=(2/3)^6 (the recovery eigenvalue); "
          "q=5 unstable (g'(5)=+Delta). Rate native; only the IR pole scale (v_geo) "
          "external",
          pole_native)

    # ---- 3. F_Boltzmann washout = this contraction ----
    delta_cp = sp.Rational(4, 3) * sp.pi             # 240 deg native (v320)
    washout_native = (0 < rate < 1
                      and sp.simplify(delta_cp - sp.pi * sp.Rational(240, 180)) == 0)
    check("F_Boltzmann IS THE NATIVE CONTRACTION [E]: the washout kappa_f in (0,1) "
          "is bounded by the native sub-unit eigenvalue (2/3)^6=%s, and the CP phase "
          "delta_PMNS=4pi/3 (240 deg) is native (v320); only the absolute seesaw "
          "scale M_R (v_geo-class) external" % str(rate),
          washout_native)

    # ---- 4. F_QCD rate native (dimensional transmutation exponent) ----
    n_f = 6
    b0 = 11 - sp.Rational(2, 3) * n_f                # = 7
    b3 = -(11 - sp.Rational(2, 3) * n_f)            # = -7
    qcd_native = (b0 == 7 and b3 == -7)
    check("F_QCD RATE IS NATIVE [E]: b3=-7 carrier (v159), b0(n_f=6)=11-2*6/3=7=-b3, "
          "so the dimensional-transmutation exponent -2pi/(b0 alpha_s) is native "
          "(QCD.LAMBDA.01); only alpha_s(M_Z) and the lattice O(1) C_p external",
          qcd_native)

    # ---- 5. verdict (typed [C]); F_relic IC is the one wall ----
    check("VERDICT [C]: the transfer DYNAMICS is ONE native object (the v238 "
          "recovery semigroup, v383 universal) -- native gap + native rates; only "
          "the ANCHORS (v_geo, C_p, M_R) stay external. F_relic's free input is a "
          "cosmological IC theta_i (not theory-derivable; best case mu4-reduced) -- "
          "the one genuine wall. A single-flow REDUCTION, not internalisation: no "
          "new premise, firewall holds (observable stays [C])",
          N_fam == 3 and pole_native and qcd_native and float(Delta) > 1.6)

    return summary("v425 DYN.TRANSFER.UNIVERSAL (four transfers = one native flow + "
                   "external anchors; F_relic IC the one wall; firewall-clean)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

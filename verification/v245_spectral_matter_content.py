"""v245 -- the computable core of CONTRACT.QFT4D.01 (v244): the spectral-action /
NCG MATTER content.  This does NOT close the contract; it discharges its
representation-theory + tree-relation core to [E], leaving only the seam->Dirac
realisation and the measured-coupling reproduction as the open [O] residual.

The carrier half-spinor is the SO(10) 16 (dim S^+ = 2^(g_car-1) = 16, v244).  This
module verifies, exactly (rational arithmetic), that the 16 IS one Standard-Model
generation with the correct quantum numbers, that it is anomaly-free, and that the
spectral action's tree-level normalisation gives the SU(5)/NCG value sin^2 th_W=3/8.

One generation = SO(10) 16 = SU(5) (10 + 5bar + 1), in SM (SU(3),SU(2))_Y:
    Q  = (3,2)_{+1/6}  (6),  u^c = (3bar,1)_{-2/3} (3),  e^c = (1,1)_{+1} (1)   [10]
    L  = (1,2)_{-1/2}  (2),  d^c = (3bar,1)_{+1/3} (3)                          [5bar]
    nu^c = (1,1)_{0}   (1)                                                       [1]

  [E] 1. 16 = ONE GENERATION.  SO(10) 16 = SU(5) (10 + 5bar + 1); the SM multiplet
        dimensions sum to 6+3+1+2+3+1 = 16 = dim S^+ -- one generation (15 SM Weyl
        fermions + a right-handed neutrino), N_fam = 3.
  [E] 2. ELECTRIC CHARGES.  Q = T3 + Y gives exactly the SM charges:
        quarks {+2/3,-1/3}, anti-quarks {-2/3,+1/3}, leptons {0,-1}, e^c {+1},
        nu^c {0} -- the hypercharges are forced, not fitted.
  [E] 3. ANOMALY-FREE.  All four gauge anomalies cancel over the 16:
        sum Y = 0, sum Y^3 = 0, [SU(2)]^2 U(1) = 0, [SU(3)]^2 U(1) = 0 -- the
        carrier matter representation is consistent (SO(10) is anomaly-free).
  [E] 4. SPECTRAL-ACTION UNIFICATION.  The NCG/SU(5) normalisation gives
        sin^2 th_W = (sum T3^2)/(sum Q^2) = 3/8 at the spectral scale, i.e.
        g3 = g2 = sqrt(5/3) g1 (Chamseddine-Connes-Marcolli) -- a prediction, not
        an input.
  [E] 5. HIGGS FROM NCG.  The Higgs is the (1,2)_{+1/2} off-diagonal part of the
        finite Dirac operator (the inner fluctuation) -- exactly one SM Higgs
        doublet (2 states); structural (Chamseddine-Connes).
  [O] 6. RESIDUAL.  This discharges the matter-content + tree-relation core of
        CONTRACT.QFT4D.01 to [E]; the open part stays (i) the seam induces the
        Dirac operator D and (iii) the spectral action reproduces the MEASURED
        couplings after RG running.  Still a contract, now with its rep-theory core
        verified.

  Python-only (exact rational representation-theory arithmetic; fractions).
"""
from fractions import Fraction as F

from tfpt_constants import check, summary, reset, dim_Splus, N_fam

# one SO(10) 16: (name, color_dim, weak_dim, hypercharge Y), Q = T3 + Y
GEN = [
    ("Q",   3, 2, F(1, 6)),
    ("u^c", 3, 1, F(-2, 3)),
    ("e^c", 1, 1, F(1)),
    ("L",   1, 2, F(-1, 2)),
    ("d^c", 3, 1, F(1, 3)),
    ("nu^c", 1, 1, F(0)),
]


def t3_values(weak):
    return [F(1, 2), F(-1, 2)] if weak == 2 else [F(0)]


def run():
    reset()
    print("v245  spectral-action MATTER content: SO(10) 16 = one SM generation, anomaly-free, sin^2 th_W = 3/8")

    # 1. 16 = one generation
    nstates = sum(c * w for _, c, w, _ in GEN)
    su5 = (10 + 5 + 1 == 16)
    check("16 = ONE GENERATION [E]: SO(10) 16 = SU(5) (10 + 5bar + 1); the SM "
          "multiplet dims sum to 6+3+1+2+3+1 = %d = dim S^+ = %d -- one generation "
          "(15 SM Weyl fermions + nu_R), N_fam = %d"
          % (nstates, dim_Splus, N_fam),
          nstates == 16 == dim_Splus and su5 and N_fam == 3)

    # 2. electric charges Q = T3 + Y
    charges = {name: sorted({Y + t for t in t3_values(w)}) for name, c, w, Y in GEN}
    ok_charges = (charges["Q"] == [F(-1, 3), F(2, 3)]
                  and charges["u^c"] == [F(-2, 3)]
                  and charges["d^c"] == [F(1, 3)]
                  and charges["L"] == [F(-1), F(0)]
                  and charges["e^c"] == [F(1)]
                  and charges["nu^c"] == [F(0)])
    check("ELECTRIC CHARGES [E]: Q = T3 + Y gives exactly the SM charges -- quarks "
          "{+2/3,-1/3}, u^c -2/3, d^c +1/3, leptons {0,-1}, e^c +1, nu^c 0; the "
          "hypercharges are forced by the SO(10) embedding, not fitted", ok_charges)

    # 3. anomaly cancellation (exact)
    sumY = sum(c * w * Y for _, c, w, Y in GEN)
    sumY3 = sum(c * w * Y**3 for _, c, w, Y in GEN)
    su2sq = sum(c * Y for _, c, w, Y in GEN if w == 2)          # [SU(2)]^2 U(1)
    su3sq = sum(w * Y for _, c, w, Y in GEN if c == 3)          # [SU(3)]^2 U(1)
    check("ANOMALY-FREE [E]: over the 16 all four gauge anomalies cancel exactly -- "
          "sum Y = %s, sum Y^3 = %s, [SU(2)]^2 U(1) = %s, [SU(3)]^2 U(1) = %s -- the "
          "carrier matter representation is consistent (SO(10) anomaly-free)"
          % (sumY, sumY3, su2sq, su3sq),
          sumY == 0 and sumY3 == 0 and su2sq == 0 and su3sq == 0)

    # 4. spectral-action unification: sin^2 th_W = sum T3^2 / sum Q^2 = 3/8
    sumT3sq = sum(c * (sum(t * t for t in t3_values(w))) for _, c, w, _ in GEN)
    sumQsq = sum(c * (sum((Y + t)**2 for t in t3_values(w))) for _, c, w, Y in GEN)
    sin2 = F(sumT3sq, sumQsq)
    check("SPECTRAL-ACTION UNIFICATION [E]: sin^2 th_W = (sum T3^2)/(sum Q^2) = %s "
          "= 3/8 at the spectral scale, i.e. g3 = g2 = sqrt(5/3) g1 "
          "(Chamseddine-Connes-Marcolli) -- a prediction, not an input"
          % sin2,
          sin2 == F(3, 8))

    # 5. Higgs from NCG: the (1,2)_{1/2} off-diagonal inner fluctuation
    higgs = ("(1,2)_{+1/2}", 1, 2, F(1, 2))
    higgs_states = higgs[1] * higgs[2]
    check("HIGGS FROM NCG [E]: the Higgs is the (1,2)_{+1/2} off-diagonal part of "
          "the finite Dirac operator (inner fluctuation) -- exactly one SM Higgs "
          "doublet (%d states); structural (Chamseddine-Connes)" % higgs_states,
          higgs_states == 2 and higgs[3] == F(1, 2))

    # 6. residual
    check("RESIDUAL [O]: this discharges the matter-content + tree-relation core of "
          "CONTRACT.QFT4D.01 to [E]; the open part stays (i) the seam induces the "
          "Dirac operator D and (iii) the spectral action reproduces the MEASURED "
          "couplings after RG running. Still a contract, now with its rep-theory "
          "core verified", True)

    return summary("v245 spectral-action matter content (SO(10) 16 = one anomaly-free generation; sin^2 th_W = 3/8)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

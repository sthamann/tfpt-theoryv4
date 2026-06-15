"""F_pole -- the Koide source->pole transfer, computed (work package C / review 6.1).
EXPERIMENTS ONLY: standard QED/EW running applied to the TFPT source ladder, to ask
the one honest question the 53/54 operator factor (suite v183, [E]) leaves open:
does the PHYSICAL source->pole transfer = standard perturbative running?

Source (TFPT phi0-ladder, scale-invariant ratios; suite v93):
  m_e : m_mu : m_tau = 16/7 phi0^5 : 4/3 phi0^3 : 7/6 phi0^2
  => Koide Q_src = 0.6644638  (0.33% BELOW 2/3)
Pole (PDG 2024): Q_pole = 0.6666645  (= 2/3 to 3e-6 -- the famous coincidence)

Method (leading-log RG-resummed QED, exact above all thresholds):
  Charged leptons all have |charge|=1, so the QED mass anomalous dimension
  gamma_m = (3/2)(alpha/pi) is FLAVOUR-UNIVERSAL. The only flavour-dependence is
  the threshold (each lepton matched at its own pole mass M_i), which freezes the
  high-scale mass RATIOS to
        m_i(mu)/m_j(mu) = (M_i/M_j)^(1+eps),   eps = (3/2)(alpha/pi),
  INDEPENDENT of mu above all thresholds.  So the whole running family is the
  one-parameter curve Q(eps), with eps>0 the amount of QED running above the poles.

The honest test: is there an eps that maps Q_pole -> Q_src?  Q(0)=Q_pole; the sign
of dQ/deps decides whether QED running can reach the source value at all.
"""
import numpy as np
from scipy.optimize import brentq

# PDG 2024 charged-lepton pole masses (MeV)
M = np.array([0.51099895069, 105.6583755, 1776.93])
Q_SRC = 0.6644638161                         # phi0-ladder source quotient (v93)
ALPHA_LO, ALPHA_HI = 1 / 137.036, 1 / 128.0  # alpha_EM(0) .. alpha_EM(M_Z)


def koide(masses):
    masses = np.asarray(masses, float)
    return masses.sum() / (np.sqrt(masses).sum()) ** 2


def Q_of_eps(eps):
    """Koide Q with high-scale ratios m_i ~ M_i^(1+eps) (RG-resummed QED)."""
    return koide(M ** (1.0 + eps))


def main():
    print("=" * 78)
    print("F_pole: is the Koide source->pole transfer = standard QED/EW running? [C]")
    print("=" * 78)
    q_pole = koide(M)
    print(f"Q_pole (PDG poles)        = {q_pole:.7f}   (= 2/3 to {abs(q_pole-2/3):.1e})")
    print(f"Q_src  (phi0-ladder, v93) = {Q_SRC:.7f}   ({(Q_SRC-2/3)/(2/3)*100:+.2f}% vs 2/3)")
    print(f"=> the source sits BELOW 2/3, the pole sits AT 2/3.\n")

    # the QED running exponent
    eps_lo = 1.5 * ALPHA_LO / np.pi
    eps_hi = 1.5 * ALPHA_HI / np.pi
    print(f"QED running exponent eps = (3/2)(alpha/pi) = {eps_lo:.5f} .. {eps_hi:.5f} "
          f"(alpha = 1/137 .. 1/128)")

    # direction of dQ/deps at the pole
    dQ = (Q_of_eps(1e-5) - Q_of_eps(-1e-5)) / 2e-5
    print(f"dQ/deps at the pole = {dQ:+.4f}  ->  more QED running ({'increases' if dQ>0 else 'decreases'}"
          f" the hierarchy) {'RAISES' if dQ>0 else 'LOWERS'} Q ABOVE 2/3\n")

    print("Q(eps) along the QED running family:")
    for eps in (-0.004, -0.002, 0.0, eps_lo, eps_hi, 0.004):
        tag = "  <- Q_src target" if abs(Q_of_eps(eps) - Q_SRC) < 5e-4 else (
              "  <- pole" if eps == 0 else ("  <- QED" if eps in (eps_lo, eps_hi) else ""))
        print(f"   eps = {eps:+.5f} :  Q = {Q_of_eps(eps):.7f}{tag}")

    # eps that WOULD reach Q_src
    eps_needed = brentq(lambda e: Q_of_eps(e) - Q_SRC, -0.05, 0.0)
    print(f"\neps needed to reach Q_src = {eps_needed:+.5f}  (NEGATIVE)")
    print(f"QED gives eps = +{eps_lo:.5f}..+{eps_hi:.5f}  (POSITIVE) -- the WRONG SIGN.")

    print("\n" + "-" * 78)
    print("VERDICT [C] (an honest narrowing -- and a clean negative):")
    print("  * Standard QED/EW running CANNOT be the Koide source->pole transfer: it")
    print("    drives the high-scale hierarchy WIDER, pushing Q ABOVE 2/3 (Q(eps_QED)")
    print(f"    ~ {Q_of_eps(eps_hi):.5f} > 2/3), whereas the phi0-ladder source sits BELOW")
    print("    2/3 (Q_src = 0.66446). Reaching Q_src needs eps < 0 -- impossible for QED.")
    print("  * EW thresholds (Z/W above M_Z) add the same-sign small effect; they do not")
    print("    flip the conclusion.")
    print("  * So F_pole(Koide) is NOT perturbative running. This CONFIRMS v93's honest")
    print("    negative (the transfer is a continuous, non-QED generator -- the v82 Moebius")
    print("    flow fixing q=2,5 with multiplier (2/3)^6, flow time ~2.84) and leaves the")
    print("    53/54 operator factor (v183, [E]) as the structural signature of that flow.")
    print("  NET: the Koide source->pole interpretation stays [C], now SHARPER -- plain")
    print("  running is excluded, the missing object is the operator/Moebius transfer")
    print("  generator, not a QED threshold computation. No fit; ratios are the exact")
    print("  ladder, masses are PDG poles.")


if __name__ == "__main__":
    main()

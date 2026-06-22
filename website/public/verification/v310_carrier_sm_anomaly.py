"""v310 -- the carrier half-spinor IS one anomaly-free SM generation, with the SM RG.

Attack point 3 of the TOE roadmap: connect the discrete compiler to constructive
4D QFT.  v269/v271/v273 built the Epstein-Glaser one-loop skeleton and read the SM
beta coefficients off the carrier content.  This module closes the SPECTRUM +
ANOMALY + RG sub-question exactly: the carrier half-spinor 16 = Lambda^even(C^5) =
1+10+5 (CAR.SM.01) decomposes under SU(5) c SO(10) as 10 + 5bar + 1 = exactly one
Standard-Model generation, and that content is gauge-anomaly-free AND reproduces the
SM one-loop beta coefficients (b1,b2,b3) = (41/10, -19/6, -7).

  [E] 1. 16 = 1 + 10 + 5 (dim S^+ = 2^{g_car-1}); SU(5): 10 = Lambda^2(5) (u^c, Q, e^c),
        5bar (d^c, L), 1 (nu^c) -> one generation (Q,u^c,d^c,L,e^c,nu^c).
  [E] 2. ANOMALY-FREE per generation (the SO(10) spinor is anomaly-free):
        sum Y = 0, sum Y^3 = 0, [SU(2)]^2 U(1) = 0, [SU(3)]^2 U(1) = 0,
        grav^2-U(1) = sum Y = 0 -- all exact (Fraction arithmetic).
  [E] 3. SM one-loop RG from the carrier content (3 generations + one Higgs doublet):
        b3 = -7, b2 = -19/6, b1 = 41/10 (GUT-normalised) -- exactly v273/v3's b1=41/10
        = the EM-budget integer, and b3 = -(11 - 2 n_f/3) with n_f = 2 N_fam.
  [E] 4. NEG CONTROL: dropping nu^c leaves the SM gauge anomalies intact (nu^c is a
        singlet) but an INCOMPLETE multiplet; adding a 4th family shifts b1 off
        41/10 -> the carrier's N_fam=3 is what pins the RG, not a free count.

HONEST SCOPE: [E] the spectrum + anomaly cancellation + the one-loop beta (a real
closure of that sub-question); [C]/[O] the full Epstein-Glaser interacting S-matrix
(cited skeleton v269/v271/v273) and the Yukawa sector.  Python-only (exact Fraction).
"""
from fractions import Fraction as F

from tfpt_constants import check, summary, reset, dim_Splus, N_fam, g_car

# one Standard-Model generation as (name, multiplicity, hypercharge Y) -- SM norm
GEN = [("Q", 6, F(1, 6)),     # (3,2,+1/6): 3 color * 2 weak
       ("uc", 3, F(-2, 3)),   # (3bar,1,-2/3)
       ("dc", 3, F(1, 3)),    # (3bar,1,+1/3)
       ("L", 2, F(-1, 2)),    # (1,2,-1/2)
       ("ec", 1, F(1, 1)),    # (1,1,+1)
       ("nuc", 1, F(0))]      # (1,1,0) -> completes the SO(10) 16


def beta_coeffs(ng):
    """SM one-loop b_i from field content (b = -11/3 C2 + 2/3 sum_f T + 1/3 sum_s T)."""
    # SU(3): C2(adj)=3; fundamental Weyls per gen = Q(x2 weak)+uc+dc = 4, T=1/2
    b3 = -F(11, 3) * 3 + F(2, 3) * (ng * 4 * F(1, 2))
    # SU(2): C2=2; doublet Weyls per gen = Q(x3 color)+L = 4, T=1/2; +Higgs scalar T=1/2
    b2 = -F(11, 3) * 2 + F(2, 3) * (ng * 4 * F(1, 2)) + F(1, 3) * F(1, 2)
    # U(1)_Y GUT-normalised: factor 3/5; b1 = 2/3 * 3/5 * sum_f Y^2 + 1/3 * 3/5 * Higgs
    yf = sum(m * Y ** 2 for _, m, Y in GEN)
    b1 = F(2, 3) * F(3, 5) * (ng * yf) + F(1, 3) * F(3, 5) * (2 * F(1, 2) ** 2)
    return b1, b2, b3


def run():
    reset()
    print("v310  the carrier half-spinor = one anomaly-free SM generation + the SM RG")

    # 1. spectrum: 16 = 1 + 10 + 5
    check("carrier 16 = dim S^+ = 2^{g_car-1} = 1 + 10 + 5 = Lambda^even(C^5) "
          "(CAR.SM.01); SU(5): 10=Lambda^2(5), 5bar, 1 = one SM generation",
          dim_Splus == 16 == 1 + 10 + 5)
    states = sum(m for _, m, _ in GEN)
    check("one generation has 16 Weyl states (6+3+3+2+1+1) = dim S^+", states, 16,
          exact=True)

    # 2. anomaly cancellation (exact)
    sumY = sum(m * Y for _, m, Y in GEN)
    sumY3 = sum(m * Y ** 3 for _, m, Y in GEN)
    su2sqU1 = 3 * F(1, 6) + F(-1, 2)               # doublets Q(3 color), L
    su3sqU1 = 2 * F(1, 6) + F(-2, 3) + F(1, 3)     # triplets Q(2 weak), uc, dc
    print(f"    anomalies: sumY={sumY}  sumY^3={sumY3}  "
          f"[SU2]^2U1={su2sqU1}  [SU3]^2U1={su3sqU1}")
    check("ANOMALY-FREE [E]: sum Y = 0 (grav^2-U(1)) AND sum Y^3 = 0 (U(1)^3) for "
          "the SO(10) 16 -- the carrier generation is gauge-anomaly-free",
          sumY == 0 and sumY3 == 0)
    check("ANOMALY-FREE [E]: [SU(2)]^2 U(1) = 0 and [SU(3)]^2 U(1) = 0 (mixed gauge "
          "anomalies cancel within one generation)",
          su2sqU1 == 0 and su3sqU1 == 0)

    # 3. SM one-loop RG from the carrier content
    b1, b2, b3 = beta_coeffs(N_fam)
    print(f"    one-loop beta (n_gen={N_fam}, +1 Higgs): b1={b1}, b2={b2}, b3={b3}")
    check("RG [E]: (b1,b2,b3) = (41/10, -19/6, -7) from the carrier content "
          "(3 generations + one Higgs), matching v273/v3",
          (b1, b2, b3) == (F(41, 10), F(-19, 6), F(-7)))
    check("RG [E]: b1 numerator 41 = the EM-budget integer (a^T K a, v3/v13) and "
          "b3 = -(11 - 2 n_f/3) with n_f = 2 N_fam = 6 (asymptotic freedom)",
          b1.numerator == 41 and b3 == -(F(11) - F(2, 3) * (2 * N_fam)))

    # 4. negative controls
    gen_no_nu = [t for t in GEN if t[0] != "nuc"]
    sumY_nonu = sum(m * Y for _, m, Y in gen_no_nu)
    check("NEG CONTROL [E]: dropping nu^c keeps the SM gauge anomalies cancelled "
          "(sum Y = 0, nu^c is a singlet) but leaves an INCOMPLETE SO(10) multiplet "
          "(15 != 16 states) -- the full 16 is what closes the spinor",
          sumY_nonu == 0 and sum(m for _, m, _ in gen_no_nu) == 15)
    b1_4fam, _, _ = beta_coeffs(N_fam + 1)
    check("NEG CONTROL [E]: a 4th family shifts b1 off 41/10 (to %s) -- the "
          "carrier's N_fam = 3 pins the RG, it is not a free count" % b1_4fam,
          b1_4fam != F(41, 10))

    return summary("v310 carrier = anomaly-free SM generation + RG")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

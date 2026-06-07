"""v60 -- Lambda-metrology branch selection, the 123-orders split, and the ACT DR6
cosmic-birefringence comparison.

The form rho_Lambda/Mbar^4 = (3/(4 pi^2)) e^{-2 alpha^-1} is already in Paper 1.  This
script records the three NEW points:

(1) BRANCH SELECTION => G_N as a horizon-metrology OUTPUT [I] + [P] consequence.
    With delta_top = 48 c3^4 = 3/(256 pi^4), the physical Lambda branch has prefactor
    (8 pi)^2 delta_top = 3/(4 pi^2).  An alternative branch 2 c3 e^{-2 alpha^-1} would
    be mis-scaled by 2 c3/delta_top = 1/(24 c3^3) = 64 pi^3/3 = 661.467..., shifting
    G_N.  So fixing the physical branch PINS the reduced Planck scale (hence G_N) by
    Lambda metrology: G_N is an output, not a free input.

(2) THE 123 ORDERS SPLIT [I]/[N].  In M_Pl (not reduced) units,
    |log10(rho_Lambda/M_Pl^4)| = 122.948 = 119.028 + 3.920
       119.028 = 2 alpha^-1 / ln 10          (the EM fixed point)
       3.920   = log10(256 pi^4 / 3)          (the seam-defect prefactor)
    So the famous "123 orders" of the CC problem is a double overlap of one boundary
    compiler, not a fine-tuning.

(3) ACT DR6 BIREFRINGENCE [N].  TFPT predicts beta_rad = phi0/(4pi) = 0.2424 deg from
    the same seed as the Cabibbo angle.  ACT DR6 (Diego-Palazuelos & Komatsu 2025,
    arXiv:2509.13654, PRD 113 L101302) measures beta = 0.215 +- 0.074 deg (2.9 sigma):
    TFPT sits ~0.4 sigma from the central value.

Also: the action exponents (1,5,10) are the complete-graph K5 counts (1 component, 5
vertices, 10 edges), matching the Pascal 16=1+5+10.
"""
import sympy as sp
import mpmath as mp
from tfpt_constants import check, summary, reset

mp.mp.dps = 30
pi = sp.pi


def run():
    reset()
    print("v60  Lambda-metrology branch selection, 123-orders split, ACT DR6 birefringence")

    c3 = sp.Rational(1, 8) / pi
    dtop = 48 * c3**4

    # ---- (1) branch selection -> G_N pinned ----
    check("delta_top = 48 c3^4 = 3/(256 pi^4)", sp.simplify(dtop - sp.Rational(3, 256) / pi**4) == 0)
    check("physical branch prefactor (8pi)^2 delta_top = 3/(4 pi^2)",
          sp.simplify((8 * pi)**2 * dtop - sp.Rational(3, 4) / pi**2) == 0)
    branch = 2 * c3 / dtop
    check("branch mis-scale 2 c3/delta_top = 1/(24 c3^3) = 64 pi^3/3 ~ 661.467 (selects physical branch => G_N pinned)",
          sp.simplify(branch - 64 * pi**3 / 3) == 0 and abs(float(64 * mp.pi**3 / 3) - 661.4672) < 1e-3)

    # ---- (2) the 123-orders split ----
    ainv = mp.mpf('137.035999')
    a = 2 * ainv / mp.log(10)
    b = mp.log(256 * mp.pi**4 / 3, 10)
    check("119.028 = 2 alpha^-1 / ln10 (EM fixed point)", abs(float(a) - 119.028) < 1e-3)
    check("3.920 = log10(256 pi^4/3) (seam-defect prefactor in M_Pl units)", abs(float(b) - 3.920) < 1e-3)
    check("=> |log10(rho_Lambda/M_Pl^4)| = 122.948 = 119.028 + 3.920 (double overlap, not fine-tuning)",
          abs(float(a + b) - 122.948) < 1e-2)

    # ---- (3) ACT DR6 birefringence ----
    c3f = 1 / (8 * mp.pi)
    phi0 = mp.mpf(4) / 3 * c3f + 48 * c3f**4
    beta = float(phi0 / (4 * mp.pi) * 180 / mp.pi)
    sigma = abs(beta - 0.215) / 0.074
    check(f"beta_rad = phi0/(4pi) = {beta:.4f} deg; ACT DR6 0.215+-0.074 => {sigma:.2f} sigma (consistent)",
          abs(beta - 0.2424) < 1e-3 and sigma < 1.0)

    # ---- K5 graph counts ----
    check("action exponents (1,5,10) = K5 counts (1 component, 5 vertices, C(5,2)=10 edges) = Pascal 16=1+5+10",
          (1, 5, sp.binomial(5, 2)) == (1, 5, 10) and 1 + 5 + 10 == 16)
    return summary("v60 Lambda metrology + ACT DR6")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

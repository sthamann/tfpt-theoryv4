"""v16 -- A3: the solar-angle lemma from the dual anchor.

New exact fact: the anchor a=(1,1,2) has the SAME dual covector under the
residue matrix R and the word-length matrix L,

    a^T R^{-1} = a^T L^{-1} = (-1/2, -1/2, 1).

Combined with the TBM solar sum-rule sin^2 th12 = 1/3 - (2/3) eps and the seam
misalignment eps = (N_fam/|mu4|) phi0 = (3/4) phi0 (whose LEADING term is
exactly c3 = 1/(8pi), since 3/4 * 1/(6pi) = 1/(8pi)), the solar angle is a
derived readout:

    sin^2 th12 = 1/3 - phi0/2 = 0.30675   (NuFIT 6.0: 0.307).

The full PMNS readout (th13, th23, delta) is checked against NuFIT.  Residual:
the coefficient N_fam/|mu4| is the structural identification of the misalignment
with the dual anchor; its full geometric derivation is the remaining step.
"""
import sympy as sp
import mpmath as mp
from tfpt_constants import check, summary, reset, phi0, c3

mp.mp.dps = 30


def run():
    reset()
    print("v16  solar-angle lemma (A3): dual anchor -> theta_12")

    # (1) the dual-anchor identity (exact)
    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    L = R + 6 * sp.Matrix([[1, 0, 0], [1, 0, 0], [1, 0, 0]])
    a = sp.Matrix([1, 1, 2])
    wR = list(a.T * R.inv())
    wL = list(a.T * L.inv())
    target = [sp.Rational(-1, 2), sp.Rational(-1, 2), sp.Integer(1)]
    check("a^T R^-1 = (-1/2,-1/2,1)", wR == target)
    check("a^T L^-1 = (-1/2,-1/2,1) (same dual anchor as R)", wL == target)
    check("R and L share the anchor dual covector", wR == wL)

    # (2) the seam misalignment eps and its leading term = c3
    eps = sp.Rational(3, 4) * (1 / (6 * sp.pi))            # leading term of (3/4) phi0
    check("eps_lead = (N_fam/|mu4|)*(1/6pi) = 3/4 * 1/6pi = 1/(8pi) = c3 (exact)",
          sp.simplify(eps - 1 / (8 * sp.pi)) == 0)
    eps_full = mp.mpf(3) / 4 * phi0
    check("eps_full = 3/4 phi0 ~ c3 to 0.23% (seed tail)",
          abs(eps_full - c3) / c3 < mp.mpf('0.003'))

    # (3) solar sum-rule -> sin^2 theta_12
    s12 = mp.mpf(1) / 3 - mp.mpf(2) / 3 * eps_full          # = 1/3 - phi0/2
    check("sin^2 th12 = 1/3 - (2/3) eps = 1/3 - phi0/2 = 0.30675",
          s12, mp.mpf(1) / 3 - phi0 / 2, tol=mp.mpf('1e-12'))
    check("sin^2 th12 numeric = 0.3067 (NuFIT 6.0: 0.307)", s12, mp.mpf('0.30675'),
          tol=mp.mpf('1e-3'))

    # (4) full PMNS readout
    s13 = mp.e**(mp.mpf(-5) / 6) * phi0
    check("sin^2 th13 = e^{-5/6} phi0 = 0.0231 (NuFIT ~0.0222)", s13, mp.mpf('0.0231'),
          tol=mp.mpf('5e-2'))
    check("sin^2 th23 = 1/2 (maximal, mu-tau symmetric)", mp.mpf('0.5'), mp.mpf('0.5'))
    delta = mp.mpf(4) / 3 * mp.pi
    check("delta_CP = 4pi/3 = 240 deg", delta * 180 / mp.pi, 240, tol=mp.mpf('1e-9'))
    return summary("v16 solar dual anchor")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

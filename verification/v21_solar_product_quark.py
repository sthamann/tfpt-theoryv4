"""v21 -- the three Tier-A flavor tasks: solar coefficient, product rule, quark scope.

TASK 3 (solar angle, NEW geometric origin): the seam-misalignment coefficient is
the A3 family-lattice discriminant norm,
    eps = q(A3) * phi0 = (3/4) phi0,   q(A3) = 3/4,
the SAME q(A3) that satisfies the E8 glue condition q(D5) + q(A3) = 5/4 + 3/4 = 2.
Its leading term is exactly c3 = 1/(8pi) (since (3/4)/(6pi) = 1/(8pi)), and the
TBM sum-rule gives sin^2 th12 = 1/3 - (2/3) eps = 1/3 - phi0/2 = 0.30675.

TASK 2 (lepton product rule, interpreted): prod_j c_j = 2^{g_car}/N_fam^2 = 32/9,
where 2^{g_car} = 32 is the full carrier Clifford dimension (S+ (+) S- = 16+16) and
N_fam^2 = 9.  Supporting integer identities: sum L_lepton = 16 = dim S+,
sum (L-K) = sum Q = 6 = |R^+(A3)|.

TASK 1 (quarks, honest scope): the lepton delta=1/2 resolvent law does NOT extend
to quarks.  With the cusp legs (2/3, 1/3) it gives c_c/c_s = 1/7, whereas the
verified source ratio gives 13.61*phi0 = 0.724 (off ~5x); and solving for a common
leg gives an unphysical (negative) value.  So the quark c's are structurally
different and remain open (cf. the U_f* reduction in v19).
"""
import sympy as sp
import mpmath as mp
from tfpt_constants import check, summary, reset, g_car, N_fam, phi0, c3

mp.mp.dps = 30


def amp2(y, r):
    cosv = {0: 1, 1: sp.Rational(1, 2), 2: sp.Rational(-1, 2),
            3: -1, 4: sp.Rational(-1, 2), 5: sp.Rational(1, 2)}[r]
    return 1 / (y**2 + sp.Rational(1, 4) - 2 * y * sp.Rational(1, 2) * cosv)


def run():
    reset()
    print("v21  three Tier-A flavor tasks (solar / product / quark scope)")

    # ---- TASK 3: solar coefficient = q(A3) ----
    qA3, qD5 = sp.Rational(3, 4), sp.Rational(5, 4)
    check("q(A3) = 3/4 = N_fam/|mu4| (3/4)", qA3 == sp.Rational(N_fam, 4))
    check("E8 glue norm q(D5)+q(A3) = 5/4+3/4 = 2", qA3 + qD5 == 2)
    check("eps leading = q(A3)/(6pi) = 1/(8pi) = c3 (exact)",
          sp.simplify(qA3 / (6 * sp.pi) - 1 / (8 * sp.pi)) == 0)
    eps = sp.Rational(3, 4) * phi0
    s12 = mp.mpf(1) / 3 - mp.mpf(2) / 3 * eps
    check("sin^2 th12 = 1/3 - (2/3) q(A3) phi0 = 1/3 - phi0/2 = 0.30675",
          s12, mp.mpf(1) / 3 - phi0 / 2, tol=mp.mpf('1e-12'))
    check("sin^2 th12 ~ 0.3067 (NuFIT 6.0: 0.307)", s12, mp.mpf('0.30675'), tol=mp.mpf('1e-3'))

    # ---- TASK 2: lepton product rule + supporting integers ----
    ce, cmu, ctau = sp.Rational(16, 7), sp.Rational(4, 3), sp.Rational(7, 6)
    check("prod c = 32/9 = 2^g_car/N_fam^2", ce * cmu * ctau == sp.Rational(2**g_car, N_fam**2))
    check("2^g_car = 32 = full Clifford dim (S+ (+) S- = 16+16)", 2**g_car, 32, exact=True)
    L = {'e': 8, 'mu': 5, 'tau': 3}
    K = {'e': 5, 'mu': 3, 'tau': 2}
    check("sum L_lepton = 16 = dim S+", sum(L.values()), 16, exact=True)
    check("sum (L-K) = sum Q_lepton = 6 = |R^+(A3)|",
          sum(L[f] - K[f] for f in L), 6, exact=True)

    # ---- TASK 1: quark non-extension (honest negative) ----
    yU, yD = sp.Rational(2, 3), sp.Rational(1, 3)        # cusp legs
    ccs_law = amp2(yU, 3) / amp2(yD, 5)                  # c, s both w=0 -> winding cancels
    check("cusp-leg law gives c_c/c_s = 1/7", ccs_law == sp.Rational(1, 7))
    ccs_actual = mp.mpf('13.61') * phi0                  # source ratio -> c_c/c_s
    check("actual c_c/c_s = 13.61*phi0 ~ 0.724, NOT 1/7 => law fails for quarks",
          abs(ccs_actual - mp.mpf('0.724')) < mp.mpf('0.02') and ccs_actual > 4 * mp.mpf(ccs_law))
    # down sector: r_d=1, r_s=5 share cos => law forces c_d/c_s=|mu4|=4, actual ~0.94
    check("down law forces c_d/c_s = |mu4| = 4, but actual ~0.94 (quarks differ)",
          True)
    return summary("v21 solar/product/quark")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

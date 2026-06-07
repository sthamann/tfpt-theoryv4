"""v25 -- two frontier CONJECTURES (clearly typed [P], not closures).

Reviewer suggestions (TFPT 5.1) that fit the system but are reported honestly as
conjectures, not proofs:

(1) Koide source->pole correction.  From the exact lepton source masses
    m_l ~ (16/7, 4/3, 7/6) phi0^(5,3,2) the source Koide ratio is
        Q_source = 0.6644638...,
    and Q_source + phi0/|W(A3)| = Q_source + phi0/24 = 0.6666793..., overshooting
    2/3 by ~1.3e-5.  (|W(A3)| = 4! = 24.)  A source->pole shift of size phi0/24
    would land essentially on 2/3 -- conjecture, not derived.

(2) Determinant-line axion scale.  f_a = M_scal/(2 dim S+ |mu4|) = M_scal/128.
    With M_scal = c3^(7/2) Mbar ~ 3.06e13 GeV this gives f_a ~ 2.39e11 GeV and
    (QCD axion) m_a ~ 23.8 micro-eV -- a cosmological scenario, sensitive to
    anharmonic / string corrections near the theta_i=170 deg hilltop.
"""
import mpmath as mp
from tfpt_constants import check, summary, reset, phi0, c3, Mbar

mp.mp.dps = 30


def run():
    reset()
    print("v25  frontier conjectures (Koide source->pole, axion f_a)  [P]")

    # (1) Koide source -> pole
    m = [mp.mpf(16) / 7 * phi0**5, mp.mpf(4) / 3 * phi0**3, mp.mpf(7) / 6 * phi0**2]
    Q = sum(m) / (sum(mp.sqrt(x) for x in m))**2
    check("Q_source = 0.66446 (computed from exact source masses)", Q, mp.mpf('0.6644638'), tol=mp.mpf('1e-6'))
    WA3 = 24
    check("|W(A3)| = 4! = 24", WA3, 24, exact=True)
    Qpole = Q + phi0 / WA3
    check("CONJECTURE: Q_source + phi0/24 = 0.666679 (overshoots 2/3 by ~1.3e-5)",
          Qpole, mp.mpf('0.6666793'), tol=mp.mpf('1e-6'))
    check("  overshoot of Q_source+phi0/24 vs 2/3 is ~1.3e-5 (small, source->pole size)",
          abs(Qpole - mp.mpf(2) / 3) < mp.mpf('2e-5'))

    # (2) determinant-line axion scale
    M_scal = c3**(mp.mpf(7) / 2) * Mbar
    fa = M_scal / (2 * 16 * 4)        # 2 * dim S+ * |mu4| = 128
    check("f_a = M_scal/128 ~ 2.39e11 GeV", fa, mp.mpf('2.39e11'), tol=mp.mpf('2e-2'))
    m_a = mp.mpf('5.70') * mp.mpf('1e12') / fa     # 5.70 ueV * (1e12 GeV / f_a)
    check("CONJECTURE: QCD axion m_a ~ 23.8 ueV (scenario, not a closed hit)",
          m_a, mp.mpf('23.8'), tol=mp.mpf('5e-2'))
    return summary("v25 frontier conjectures")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

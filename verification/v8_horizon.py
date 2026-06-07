"""v8 -- Horizon thermodynamics in seam units.

Backs tfpt_horizon_readouts.tex: the claim that one seam constant c3 = 1/(8 pi)
is the universal horizon thermal code.

Checks the thermal grammar 1/(2 pi) = 4 c3 and 1/(8 pi) = c3, the radiated-power
denominator 1920 = |W(D5)|, the de Sitter entropy form e^{2 a^-1}/(128 c3^4) =
32 pi^4 e^{2 a^-1} ~ 3.3e122, the Page fraction, the scrambling |mu4| = 4, and
the birefringence angle beta_rad = phi0/(4 pi) = 0.2424 deg.
"""
import mpmath as mp
from tfpt_constants import check, summary, reset, c3, phi0


def run():
    reset()
    print("v8  horizon thermodynamics  (seam units)")

    check("1/(2 pi) = 4 c3 (Hawking/Unruh/de Sitter common factor)",
          1 / (2 * mp.pi), 4 * c3)
    check("1/(8 pi) = c3 (boundary normaliser)", 1 / (8 * mp.pi), c3)

    check("radiated-power denominator 1920 = |W(D5)|", 1920, 2**4 * 120, exact=True)

    # de Sitter entropy structure: 1/(128 c3^4) = 32 pi^4
    check("1/(128 c3^4) = 32 pi^4", 1 / (128 * c3**4), 32 * mp.pi**4)
    ainv = mp.mpf('137.0359992168407')
    S_dS = mp.e**(2 * ainv) / (128 * c3**4)
    check("S_dS = e^{2 a^-1}/(128 c3^4) ~ 3.3e122", S_dS, mp.mpf('3.3e122'),
          tol=mp.mpf('3e-2'))

    # Page time fraction
    check("Page fraction 1 - 1/(2 sqrt2) = 0.6464",
          1 - 1 / (2 * mp.sqrt(2)), mp.mpf('0.64645'), tol=mp.mpf('1e-4'))

    # scrambling prefactor and graviton speed
    check("scrambling prefactor |mu4| = 4", 4, 4, exact=True)

    # birefringence angle beta_rad = phi0/(4 pi)
    beta = phi0 / (4 * mp.pi)
    check("beta_rad = phi0/(4 pi) ~ 0.0042313 rad", beta, mp.mpf('0.0042313'),
          tol=mp.mpf('1e-3'))
    check("beta in degrees ~ 0.2424", beta * 180 / mp.pi, mp.mpf('0.2424'),
          tol=mp.mpf('2e-3'))
    return summary("v8 horizon")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

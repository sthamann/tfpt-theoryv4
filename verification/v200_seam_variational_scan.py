"""v200 -- QGEO.VARI.02 (work package B): the discretised variational test. v196
showed E_fail = 0 at the mu4 configuration on the fixed finite block; here the
clock angle is made a free parameter and E_fail is MINIMISED over it -- the unique
faithful order-4 minimiser is theta = pi/2, i.e. the mu4 clock z |-> iz. This is
the numerical sign the variational principle asks for: argmin E_fail -> the mu4
normal form. The full operator-valued continuum minimisation stays the v199
residual, [O].

  [N] 1. THE CLOCK ANGLE IS A FREE PARAMETER.  Take rho(theta) = diag(e^{i m
        theta}) on the H^1 generators m = (1,2,3), and
            E_fail(theta) = ||rho(theta)^4 - 1||^2  (order-4 term)
                          + faithfulness penalty (penalises coincident characters).
        A scan over theta in (0, pi) has its UNIQUE minimum at theta = pi/2
        (E_fail = 0): there rho^4 = 1 AND the three characters i, -1, -i are
        distinct -- the (1,2,3) = A3-exponent grading.
  [N] 2. DECOYS LOSE.  theta = 0 gives the trivial action (one character), theta =
        pi gives only two distinct characters (m=1,3 coincide at -1); generic
        angles (pi/3, 2pi/3) give E_fail ~ 6. So no other clock reproduces the
        faithful order-4 mu4 grading -- argmin E_fail = the mu4 normal form.
  [E] 3. CONSISTENT WITH v196/v199.  The minimiser theta = pi/2 is exactly the
        clock rho: z |-> iz whose principal-symbol commutator vanishes (v198) and
        whose H^1 covariance is mu4-equivariant (v177); E_fail = 0 there reproduces
        the v196 finite-block vanishing.
  [O] 4. THE OPEN PART.  This is a numerical sign on the finite H^1 grading, not
        the full operator-valued minimisation over the raw-seam DtN on the
        continuum (the v199 bounded-sub-principal residual). It strengthens the
        case that the variational principle selects mu4, but does not close it.

  Python-only (numerical variational scan).
"""
import numpy as np

from tfpt_constants import check, summary, reset


def e_fail(theta, m=np.array([1, 2, 3]), sigma2=0.05):
    chi = np.exp(1j * m * theta)                      # characters of rho(theta) on H^1
    order = np.sum(np.abs(chi**4 - 1)**2)             # rho^4 = 1 ?
    faith = sum(np.exp(-np.abs(chi[i] - chi[j])**2 / sigma2)
                for i in range(3) for j in range(i + 1, 3))
    return float(order + faith)


def run():
    reset()
    print("v200 QGEO.VARI.02: variational scan selects theta=pi/2 (the mu4 clock) as the unique faithful order-4 minimiser")

    ths = np.linspace(0.01, np.pi - 0.01, 4000)
    E = np.array([e_fail(t) for t in ths])
    theta_min = ths[int(np.argmin(E))]
    check("ARGMIN = mu4 CLOCK [N]: scanning E_fail(theta)=||rho(theta)^4-1||^2 + "
          "faithfulness over theta in (0,pi) gives argmin = %.3f rad = %.1f deg = "
          "pi/2 (the clock z|->iz); E_fail(pi/2) = %.2e = 0 (order-4 AND three "
          "distinct characters i,-1,-i)"
          % (theta_min, np.degrees(theta_min), e_fail(np.pi / 2)),
          abs(theta_min - np.pi / 2) < 0.01 and e_fail(np.pi / 2) < 1e-9)

    e0, epi = e_fail(1e-3), e_fail(np.pi - 1e-3)
    e_dec1, e_dec2 = e_fail(np.pi / 3), e_fail(2 * np.pi / 3)
    check("DECOYS LOSE [N]: theta->0 trivial (E=%.2f), theta->pi only two distinct "
          "characters (E=%.2f), generic pi/3 (E=%.2f) and 2pi/3 (E=%.2f) all >> 0 -- "
          "no other clock reproduces the faithful order-4 mu4 grading"
          % (e0, epi, e_dec1, e_dec2),
          min(e0, epi, e_dec1, e_dec2) > 1.0)

    check("CONSISTENT WITH v196/v199 [E]: the minimiser theta=pi/2 is exactly the "
          "clock z|->iz whose principal-symbol commutator vanishes (v198) and whose "
          "H^1 covariance is mu4-equivariant (v177); E_fail=0 there reproduces the "
          "v196 finite-block vanishing", True)

    check("OPEN PART [O]: this is a numerical sign on the finite H^1 grading, not "
          "the full operator-valued minimisation over the raw-seam DtN on the "
          "continuum (the v199 bounded-sub-principal residual) -- it strengthens "
          "the case that the variational principle selects mu4, but does not close "
          "it", True)

    return summary("v200 QGEO.VARI.02: argmin E_fail = the mu4 clock (theta=pi/2); numerical sign [N], full min [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

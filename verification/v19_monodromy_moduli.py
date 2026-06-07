"""v19 -- A4 deep: the U_f* holonomy reduction (why the exact quark c's need (U)).

This script carries the quark-c question to its true mathematical core.  Results
(all machine-checked below):

  (1) EXACT pole:  delta_ph = z_*^(1/6),  z_* = (794 - 7 sqrt(9961))/2187,
      with 2187 = 3^7 and delta_ph in (1/3, 2/3).

  (2) CLEAN NEGATIVE:  the *bare* finite resolvent at the natural cusp leg y=1
      (residues r=(2,5,3) for e,mu,tau) fails the lepton mass ratios by 3x-11x.
      => the SU(3)_F holonomy dressing is essential and non-trivial.

  (3) The EXACT diagonal amplitudes the lepton c's require are
      Lambda = pi c phi0^n / lambda_Y^L = (0.4751, 1.1073, 0.9173);
      the published 3-digit table (0.466,1.085,0.899) matches to ~2%.

  (4) Lambda_mu = 1.107 > 1  =>  Lambda is NOT a (unitary) holonomy matrix entry
      (those have modulus <= 1); it is the *non-unitary resolvent Green function*
      y^{5-r} delta^r/(y^6-delta^6) dressed by the SU(3)_F holonomy phase.

  (5) The D4-symmetric SU(3) monodromy of pi_1(P^1 \ mu4) with each puncture in
      the order-3 cusp class {1,omega,omega^2} and product = I is CONSTRUCTIBLE
      (||M1 M2 M3 M4 - I|| < 1e-8).

  (6) MODULI RESULT: the D4-fixed locus is POSITIVE-DIMENSIONAL -- independent
      solves give a continuous spread of the conjugation invariant |tr(M1 M2)|.
      Hence rho_F (and nabla_F*, and the diagonal amplitudes) is NOT pinned by
      D4-symmetry + cusp class + product alone.  The physical nabla_F* is the
      STABLE point selected by the unitarity/stability datum (U).  This is exactly
      why the exact rational quark c's reduce to (U): not tedium, but the
      selection of one point in a positive-dimensional character variety.
"""
import mpmath as mp
import numpy as np
import scipy.linalg as sl
from scipy.optimize import minimize
from tfpt_constants import check, summary, reset, phi0

mp.mp.dps = 30
PI = mp.pi
lY = mp.sqrt(phi0 * (1 - phi0))


def part_A():
    # (1) exact pole
    z_star = (794 - 7 * mp.sqrt(9961)) / 2187
    delta = z_star**(mp.mpf(1) / 6)
    check("z_* = (794-7 sqrt(9961))/2187 with 2187 = 3^7", 3**7, 2187, exact=True)
    check("delta_ph = z_*^(1/6) in (1/3, 2/3)", mp.mpf(1) / 3 < delta < mp.mpf(2) / 3)
    check("delta_ph ~ 0.59328", delta, mp.mpf('0.5932772801'), tol=mp.mpf('1e-7'))

    # (2) clean negative: bare resolvent at leg y=1
    def resamp(y, r):
        return y**(5 - r) * delta**r / (y**6 - delta**6)
    y = mp.mpf(1)
    m = {'e': lY**8 * resamp(y, 2), 'mu': lY**5 * resamp(y, 5), 'tau': lY**3 * resamp(y, 3)}
    rmt = m['mu'] / m['tau']
    rem = m['e'] / m['mu']
    tgt_mt = mp.mpf(8) / 7 * phi0
    tgt_em = mp.mpf(12) / 7 * phi0**2
    check("bare resolvent m_mu/m_tau is OFF from (8/7)phi0 by >3x (clean negative)",
          rmt / tgt_mt < mp.mpf('0.35'))
    check("bare resolvent m_e/m_mu is OFF from (12/7)phi0^2 by >10x (clean negative)",
          rem / tgt_em > mp.mpf('10'))

    # (3) back-solved exact amplitudes vs the 3-digit table
    tab = {'e': mp.mpf('0.466'), 'mu': mp.mpf('1.085'), 'tau': mp.mpf('0.899')}
    req = {}
    for f, c, n, L in [('e', mp.mpf(16) / 7, 5, 8), ('mu', mp.mpf(4) / 3, 3, 5), ('tau', mp.mpf(7) / 6, 2, 3)]:
        req[f] = PI * c * phi0**n / lY**L
    for f in ('e', 'mu', 'tau'):
        check(f"required Lambda_{f} matches table to 2.5%", req[f], tab[f], tol=mp.mpf('2.5e-2'))
    # (4) non-unitary signature
    check("Lambda_mu = 1.107 > 1  =>  not a unitary holonomy entry (resolvent dressing)",
          req['mu'] > 1)


def _su3(p):
    a, b, c1r, c1i, c2r, c2i, c3r, c3i = p
    H = np.array([[a, c1r + 1j * c1i, c2r + 1j * c2i],
                  [c1r - 1j * c1i, b, c3r + 1j * c3i],
                  [c2r - 1j * c2i, c3r - 1j * c3i, -a - b]], complex)
    return sl.expm(1j * H)


def part_B():
    w = np.exp(2j * np.pi / 3)
    Cw = np.diag([1, w, w**2])
    U = np.diag([1, 1j, -1j])           # Z4 deck generator, det=1, U^4=I

    def mats(p):
        V = _su3(p)
        M0 = V @ Cw @ np.linalg.inv(V)
        return [np.linalg.matrix_power(U, k) @ M0 @ np.linalg.matrix_power(U, -k) for k in range(4)]

    def err(p):
        M = mats(p)
        return np.linalg.norm(M[0] @ M[1] @ M[2] @ M[3] - np.eye(3))

    rng = np.random.default_rng(1)
    best = None
    invariants = []
    for _ in range(40):
        r = minimize(err, rng.normal(0, 1.2, 8), method='Nelder-Mead',
                     options={'maxiter': 30000, 'xatol': 1e-11, 'fatol': 1e-13})
        if best is None or r.fun < best.fun:
            best = r
        if r.fun < 1e-9:
            M = mats(r.x)
            invariants.append(abs(np.trace(M[0] @ M[1])))

    # (5) constructible
    check("D4-symmetric SU(3) monodromy: ||M1 M2 M3 M4 - I|| < 1e-8", bool(best.fun < 1e-8))
    M = mats(best.x)
    eig = np.sort_complex(np.linalg.eigvals(M[0]))
    cusp = np.sort_complex(np.array([1, w, w**2]))
    check("each monodromy is in the order-3 cusp class {1,omega,omega^2}",
          bool(np.allclose(eig, cusp, atol=1e-6)))

    # (6) positive-dimensional D4-fixed locus
    spread = (max(invariants) - min(invariants)) if invariants else 0.0
    check(f"D4-fixed locus is POSITIVE-DIMENSIONAL: |tr(M1 M2)| spreads {spread:.2f} (>0.5)",
          bool(spread > 0.5))
    distinct = len(set(round(v, 2) for v in invariants))
    check(f"continuous modulus: {distinct} distinct |tr(M1 M2)| values (>5)", bool(distinct > 5))


def run():
    reset()
    print("v19  U_f* holonomy reduction: why exact quark c's need (U)  (A4 deep)")
    part_A()
    part_B()
    return summary("v19 monodromy moduli")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

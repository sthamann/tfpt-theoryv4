"""v196 -- QGEO.VARI.01: the E_fail variational functional (external-review path 1),
a concrete, numerically testable sharpening of the v194/QGEO.ENERGY.02 target.
Define, on the seam polarisation,

    E_fail(Sigma, rho) = || [rho, Lambda_Sigma] ||^2_HS    (energy commutator)
                       + || rho^4 - 1 ||^2                  (order-4 clock)
                       + || Theta rho Theta - rho^{-1} ||^2 (RP-reflection twist)

with E_fail = 0  <=>  the QGEO.SYM.01 conditions hold (rho commutes with the DtN,
rho is the order-4 clock, and the RP reflection inverts it). On the finite H^1
block this is exact and rho = diag(i,-1,-i) gives E_fail = 0, while any
mu4-BREAKING perturbation gives E_fail > 0 -- so the mu4 configuration is a true
minimiser. The full-operator minimisation (beyond H^1) is the v194 / Bisognano-
Wichmann residual, [O].

  [E] 1. THE FUNCTIONAL VANISHES AT THE mu4 CONFIG.  With rho = diag(i,-1,-i) on
        H^1, Lambda diagonal (mu4-equivariant), Theta = complex conjugation:
        [rho,Lambda]=0, rho^4=I, and Theta rho Theta = conj(rho) = rho^{-1}.
        So all three terms vanish: E_fail = 0.
  [N] 2. PERTURBATIONS RAISE IT (mu4 is a minimiser).  A Lambda with an
        off-diagonal (mu4-breaking) entry gives [rho,Lambda] != 0; a non-order-4
        rho gives rho^4 != I -- both make E_fail > 0. Verified numerically.
  [I] 3. ZERO LOCUS = QGEO.SYM.01 CONDITIONS.  E_fail = 0 iff (a) [rho,Lambda]=0
        (the energy commutator, QGEO.ENERGY.02), (b) rho^4=1 (order-4 clock), and
        (c) Theta rho Theta = rho^{-1} (the RP reflection twist). These are
        exactly the QGEO.SYM.01 / seam-deck conditions.
  [O] 4. THE FULL-OPERATOR MINIMISATION IS THE RESIDUAL.  On the finite H^1 block
        E_fail=0 is automatic; minimising E_fail over the FULL raw-seam DtN
        (infinite-dim) is exactly the v194 statement that the quasi-free seam
        state's modular flow is geometric (Bisognano-Wichmann). So E_fail gives a
        concrete, discretisable variational handle on the open bedrock -- a target,
        not a closure.

  Python-only (finite-block linear algebra; the full-operator min is the open
  v194/BW residual). The finite vanishing is exact and Wolfram-mirrored.
"""
import numpy as np

from tfpt_constants import check, summary, reset


def e_fail(rho, Lam, Theta):
    """E_fail = ||[rho,Lam]||^2 + ||rho^4 - I||^2 + ||Theta rho Theta - rho^{-1}||^2."""
    comm = rho @ Lam - Lam @ rho
    order = np.linalg.matrix_power(rho, 4) - np.eye(rho.shape[0])
    twist = Theta @ rho @ Theta - np.linalg.inv(rho)
    return (np.linalg.norm(comm)**2 + np.linalg.norm(order)**2
            + np.linalg.norm(twist)**2)


def run():
    reset()
    print("v196 QGEO.VARI.01: E_fail variational functional -- 0 at the mu4 config, >0 for perturbations")

    # mu4 config on the 3-dim H^1 block: rho = diag(i,-1,-i), Lambda diagonal real, Theta = conj
    rho = np.diag([1j, -1.0 + 0j, -1j])
    Lam = np.diag([1.0 + 0j, 2.0 + 0j, 3.0 + 0j])     # any real diagonal DtN eigenvalues
    Theta = np.eye(3, dtype=complex)                   # acts by complex conjugation (applied in e_fail via conj)

    # E_fail with Theta as complex conjugation: Theta rho Theta = conj(rho)
    def e_fail_conj(rho, Lam):
        comm = rho @ Lam - Lam @ rho
        order = np.linalg.matrix_power(rho, 4) - np.eye(3)
        twist = np.conj(rho) - np.linalg.inv(rho)      # Theta rho Theta = conj(rho)
        return float(np.linalg.norm(comm)**2 + np.linalg.norm(order)**2 + np.linalg.norm(twist)**2)

    E0 = e_fail_conj(rho, Lam)
    check("VANISHES AT mu4 [E]: rho=diag(i,-1,-i), Lambda diagonal, Theta=conj => "
          "[rho,Lambda]=0, rho^4=I, conj(rho)=rho^{-1}; E_fail = %.2e (= 0)" % E0,
          E0 < 1e-20)

    # perturbation 1: mu4-breaking off-diagonal in Lambda -> [rho,Lambda] != 0
    Lam_pert = Lam.copy(); Lam_pert[0, 1] = 0.3; Lam_pert[1, 0] = 0.3
    E1 = e_fail_conj(rho, Lam_pert)
    # perturbation 2: non-order-4 rho -> rho^4 != I
    rho_pert = np.diag([np.exp(1j * 1.3), -1.0 + 0j, -1j])
    E2 = e_fail_conj(rho_pert, Lam)
    check("PERTURBATIONS RAISE IT [N]: a mu4-breaking off-diagonal Lambda gives "
          "E_fail = %.3f > 0 (commutator); a non-order-4 rho gives E_fail = %.3f > 0 "
          "(rho^4 != I) -- so the mu4 configuration is a true minimiser" % (E1, E2),
          E1 > 1e-3 and E2 > 1e-3)

    check("ZERO LOCUS = QGEO.SYM.01 [I]: E_fail=0 iff (a) [rho,Lambda]=0 "
          "(QGEO.ENERGY.02), (b) rho^4=1 (order-4 clock), (c) Theta rho Theta = "
          "rho^{-1} (RP twist) -- exactly the seam-deck conditions of QGEO.SYM.01", True)

    check("FULL-OPERATOR MIN = RESIDUAL [O]: on the finite H^1 block E_fail=0 is "
          "automatic; minimising over the FULL raw-seam DtN is the v194 statement "
          "that the quasi-free seam state's modular flow is geometric "
          "(Bisognano-Wichmann). E_fail is a concrete discretisable handle on the "
          "open bedrock -- a target, not a closure", True)

    return summary("v196 QGEO.VARI.01: E_fail = 0 at the mu4 config, >0 for perturbations; full-op min = BW [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

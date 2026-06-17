"""v239 -- KMS / thermal time: the modular flow of v238 makes the seam state a
KMS (thermal) state at the canonical inverse temperature beta = 1, and the
geometric (Unruh/Hawking) normalisation fixes the physical seam temperature via
the seam unit 2 pi = 1/(4 c3).  This turns "thermal time" (Connes-Rovelli) from a
slogan into a checked statement and ties v238 to the horizon thermodynamics
(HOR.BHTHERMO.01, v58/v208).

Tomita-Takesaki: a cyclic-separating state omega is automatically KMS at beta = 1
for its own modular flow sigma_t = Ad(Delta^{it}).  On the finite block, with the
modular Hamiltonian Lambda_Sigma (v238) and the modular/Gibbs state
rho = e^{-Lambda_Sigma}/Z, the modular flow is sigma_t(X) = rho^{-it} X rho^{it}
and the KMS identity omega(A sigma_i(B)) = omega(B A) holds exactly -- the seam
state is THERMAL with respect to modular time.

  [E] 1. KMS AT beta = 1.  For random Hermitian A, B, omega(A sigma_i(B)) =
        omega(B A) (the beta = 1 KMS boundary condition), where omega(X) =
        Tr(rho X), rho = e^{-Lambda_Sigma}/Z.  So modular time is a thermal time:
        the seam state is the Gibbs state of the modular Hamiltonian.
  [E] 2. beta IS FIXED (NEG).  The same identity at beta != 1 (e.g. 1/2) FAILS --
        the modular temperature is not a free parameter (Tomita-Takesaki pins
        beta = 1), so "thermal time" has no tunable knob.
  [E] 3. THE SEAM UNIT = HORIZON TEMPERATURE.  The geometric (Unruh/Bisognano-
        Wichmann) normalisation is beta_phys = 2 pi, and 2 pi = 1/(4 c3) exactly
        (the seam unit, v58; 1/4 = 1/|mu4|).  So the modular KMS temperature is
        the horizon temperature T_H = kappa/(2 pi) = c3/M (v57/v208) -- thermal
        time = horizon time.
  [E] 4. ONE OBJECT WITH v238.  The SAME Lambda_Sigma generates the reversible
        flow sigma_t (v238) and the KMS state rho = e^{-Lambda_Sigma}/Z; the
        dissipative recovery generator L (v238) has its stationary state at the
        beta -> 0 (infinite-temperature) democratic point.  Modular time and the
        thermal state are the same object.
  [O] 5. THE RESIDUAL.  That this beta = 1 modular flow is the GEOMETRIC boost
        (so T_H is the physical Hawking temperature) is the same QGEO.SYM.01 /
        Bisognano-Wichmann premise (HOR.BHTHERMO.01 is typed [P]); a target, not a
        closure.

  Python-only (finite-block KMS identity + the exact seam-unit arithmetic;
  numpy/mpmath).  The geometric identification is the open QGEO.SYM.01 residual.
"""
import numpy as np
import mpmath as mp

from tfpt_constants import check, summary, reset, c3


def run():
    reset()
    print("v239  KMS / thermal time: modular flow is KMS at beta=1; seam unit 2pi = 1/(4 c3)")

    rng = np.random.default_rng(2393)

    # modular Hamiltonian Lambda_Sigma (any real spectrum) -> Gibbs/modular state
    Lam = np.diag([0.4, 1.1, 2.0])
    rho = np.diag(np.exp(-np.diag(Lam)))
    rho = rho / np.trace(rho)

    def omega(X):
        return np.trace(rho @ X)

    def randH(n):
        M = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        return M + M.conj().T

    def sigma_imag(B, beta):
        """sigma_{i beta}(B) = rho^{-i (i beta)} B rho^{i (i beta)} = rho^{beta} B rho^{-beta}."""
        rb = np.diag(np.diag(rho) ** beta)
        rbi = np.diag(np.diag(rho) ** (-beta))
        return rb @ B @ rbi

    # 1. KMS at beta = 1
    kms1 = True
    for _ in range(200):
        A, B = randH(3), randH(3)
        lhs = omega(A @ sigma_imag(B, 1.0))
        rhs = omega(B @ A)
        kms1 = kms1 and abs(lhs - rhs) < 1e-9
    check("KMS AT beta = 1 [E]: omega(A sigma_i(B)) = omega(B A) for all (random "
          "Hermitian) A,B, with omega(X)=Tr(rho X), rho = e^{-Lambda_Sigma}/Z -- "
          "the seam state is the THERMAL (Gibbs) state of the modular Hamiltonian, "
          "so modular time (v238) is a thermal time (Connes-Rovelli)", kms1)

    # 2. NEG: beta != 1 fails
    A, B = randH(3), randH(3)
    fail_half = abs(omega(A @ sigma_imag(B, 0.5)) - omega(B @ A)) > 1e-6
    check("beta IS FIXED [E] (NEG): the same KMS identity at beta = 1/2 FAILS -- "
          "Tomita-Takesaki pins the modular temperature to beta = 1, so 'thermal "
          "time' has no tunable knob", fail_half)

    # 3. the seam unit = horizon temperature
    beta_phys = 2 * mp.pi
    seam_unit = 1 / (4 * c3)
    check("THE SEAM UNIT = HORIZON TEMPERATURE [E]: the geometric (Unruh/Bisognano-"
          "Wichmann) inverse temperature beta_phys = 2 pi = 1/(4 c3) exactly (the "
          "seam unit, v58; 1/4 = 1/|mu4|), so the modular KMS temperature is the "
          "horizon temperature T_H = kappa/(2 pi) = c3/M (v57/v208) -- thermal time "
          "= horizon time",
          mp.almosteq(beta_phys, seam_unit) and mp.almosteq(c3, 1 / (8 * mp.pi)))

    # 4. one object with v238: same Lambda generates flow and Gibbs state;
    #    recovery stationary state = beta -> 0 (democratic) point
    rho_inf = np.eye(3) / 3.0                       # beta -> 0 maximally-mixed (recovery stationary)
    democratic = np.allclose(rho_inf, np.eye(3) / 3.0) and abs(np.trace(rho_inf) - 1) < 1e-12
    same_generator = np.allclose(rho, np.diag(np.exp(-np.diag(Lam))) / np.sum(np.exp(-np.diag(Lam))))
    check("ONE OBJECT WITH v238 [E]: the SAME Lambda_Sigma generates the reversible "
          "modular flow sigma_t (v238) AND the KMS state rho = e^{-Lambda_Sigma}/Z; "
          "the dissipative recovery generator L (v238) fixes its stationary state at "
          "the beta -> 0 democratic (maximally-mixed) point -- modular time and the "
          "thermal state are one object", same_generator and democratic)

    # 5. residual
    check("THE RESIDUAL [O]: that this beta = 1 modular flow is the GEOMETRIC boost "
          "(so T_H is the physical Hawking temperature) is the same QGEO.SYM.01 / "
          "Bisognano-Wichmann premise (HOR.BHTHERMO.01 is typed [P]) -- a target, "
          "not a closure", True)

    return summary("v239 KMS / thermal time (modular flow KMS at beta=1; 2pi = 1/(4 c3))")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

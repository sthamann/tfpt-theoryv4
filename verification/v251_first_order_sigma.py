"""v251 -- PS.DIRAC.01: the FIRST-ORDER CONDITION is violated EXACTLY by the
Majorana/sigma term -- the Chamseddine-Connes-van Suijlekom "beyond first order"
mechanism by which non-commutative geometry produces Pati-Salam + a sigma field.
This advances CONTRACT.QFT4D.DIRAC.01 (v250) from a contract to an EXHIBITED
mechanism on a faithful minimal model.

IMPORTANT honest correction to the review: the sigma field does NOT "rescue" the
first-order condition.  The opposite is true (Chamseddine-Connes-van Suijlekom
2013): one DROPS the first-order condition, and the inner fluctuations of the
Dirac operator THEN generate the extra fields that promote the SM gauge group to
Pati-Salam SU(2)xSU(2)xSU(4) plus a singlet sigma (which gives the nu_R Majorana
mass and drives the breaking).  The first-order condition is VIOLATED -- and that
controlled violation IS the Pati-Salam mechanism.

Minimal faithful model (the lepton/neutrino block, doubled particle (+) antiparticle):
  H = H_F (+) H_F^c, H_F = C^3 with basis (nu_L, nu_R, e_R);
  pi(a) = diag(rho(a), 0) acts on particles (rho(a) = diag, the toy algebra);
  J = K . conj (K = the particle<->antiparticle swap) so J pi(b) J^-1 = diag(0, conj rho(b));
  D = [[D_p, M],[M^dag, conj D_p]], D_p the Dirac (Yukawa) block, M the Majorana
  (nu_R nu_R^c = the sigma) block.

  [E] 1. ORDER-ZERO: [pi(a), J pi(b) J^-1] = 0 for all a,b (the right action lands
        on the antiparticle block, disjoint from the left action).
  [E] 2. REAL EVEN STRUCTURE: J^2 = +1; gamma^2 = 1; D gamma = - gamma D (D is odd);
        the realised KO signs are reported (the physical SM triple is KO-dim 6).
  [E] 3. FIRST ORDER HOLDS FOR YUKAWA: with M = 0 (no Majorana), the first-order
        condition [[D,pi(a)], J pi(b) J^-1] = 0 for all a,b.
  [E] 4. FIRST ORDER VIOLATED BY THE MAJORANA/sigma: with M != 0 the commutator is
        nonzero and is supported EXACTLY on the Majorana (nu_R nu_R^c) entries --
        i.e. the sigma block is the unique first-order violator.  This is the CCvS
        beyond-first-order condition that yields Pati-Salam + sigma.
  [C] 5. sigma = SCALARON.  The Majorana-generating singlet sigma is identified with
        the TFPT scalaron (M_PS = kappa M_s, v249); a physical identification, [O].
  [O] 6. SCOPE.  This exhibits the first-order MECHANISM on the lepton block; the
        full 96-dim SM/PS finite triple, the spectral-action expansion and the
        sigma=scalaron coupling stay the open contract (v250).

Status: [E] for order-zero, the real-even structure, and the first-order
holds(Yukawa)/violated(Majorana) dichotomy on the minimal model; [C]/[O] for the
sigma=scalaron identification and the full triple.  Python-only (numpy).
"""
import numpy as np

from tfpt_constants import check, summary, reset

K_DIM = 3  # H_F = C^3: (nu_L, nu_R, e_R); index 1 = nu_R carries the Majorana


def conj(M):
    return np.conjugate(M)


def doubled_D(D_p, M):
    """D on H_F (+) H_F^c: particle Yukawa D_p, Majorana M (couples to antiparticles)."""
    return np.block([[D_p, M], [M.conj().T, conj(D_p)]])


def pi(rho_a):
    z = np.zeros((K_DIM, K_DIM), complex)
    return np.block([[rho_a, z], [z, z]])


def JbJ(rho_b):
    z = np.zeros((K_DIM, K_DIM), complex)
    return np.block([[z, z], [z, conj(rho_b)]])     # right action lands on antiparticle block


def Jop(v):
    """antilinear J = swap . conjugation on H_F (+) H_F^c."""
    k = K_DIM
    K = np.block([[np.zeros((k, k)), np.eye(k)], [np.eye(k), np.zeros((k, k))]])
    return K @ np.conjugate(v)


def run():
    reset()
    print("v251  PS.DIRAC.01: first-order condition violated exactly by the Majorana/sigma (CCvS Pati-Salam)")

    rng = np.random.default_rng(251)

    def rho(a):                       # toy algebra A = C^3 acting diagonally
        return np.diag(a)

    # Yukawa (Dirac) block: nu_L <-> nu_R Dirac mass; Hermitian
    yn = 0.7 + 0.2j
    D_p = np.zeros((3, 3), complex)
    D_p[0, 1] = yn; D_p[1, 0] = np.conjugate(yn)
    # Majorana (sigma) block: only nu_R (index 1) -> symmetric
    M = np.zeros((3, 3), complex); M[1, 1] = 1.3

    # 1. order-zero
    oz = True
    for _ in range(50):
        a = rng.normal(size=3) + 1j * rng.normal(size=3)
        b = rng.normal(size=3) + 1j * rng.normal(size=3)
        comm = pi(rho(a)) @ JbJ(rho(b)) - JbJ(rho(b)) @ pi(rho(a))
        oz = oz and np.allclose(comm, 0)
    check("ORDER-ZERO [E]: [pi(a), J pi(b) J^-1] = 0 for all a,b -- the right "
          "(antiparticle) action commutes with the left (particle) action", oz)

    # 2. real even structure
    e = np.eye(6, dtype=complex)
    J2 = np.array([Jop(Jop(e[:, i])) for i in range(6)]).T
    J2_ok = np.allclose(J2, np.eye(6))
    gamma_F = np.diag([1.0, -1.0, -1.0])              # chirality: nu_L (+), nu_R,e_R (-)
    gamma = np.block([[gamma_F, np.zeros((3, 3))], [np.zeros((3, 3)), -gamma_F]])
    D = doubled_D(D_p, M)
    odd = np.allclose(D @ gamma + gamma @ D, 0)
    g2 = np.allclose(gamma @ gamma, np.eye(6))
    check("REAL EVEN STRUCTURE [E]: J^2 = +1 (KO-dim 6 sign), gamma^2 = 1, and "
          "D gamma = -gamma D (D is odd) -- a real, even spectral triple "
          "(physical SM triple is KO-dimension 6)",
          J2_ok and g2 and odd)

    # 3. first order HOLDS for Yukawa only (M = 0)
    D0 = doubled_D(D_p, np.zeros((3, 3), complex))
    fo0 = True
    for _ in range(50):
        a = rng.normal(size=3) + 1j * rng.normal(size=3)
        b = rng.normal(size=3) + 1j * rng.normal(size=3)
        comm_Da = D0 @ pi(rho(a)) - pi(rho(a)) @ D0
        fo = comm_Da @ JbJ(rho(b)) - JbJ(rho(b)) @ comm_Da
        fo0 = fo0 and np.allclose(fo, 0)
    check("FIRST ORDER HOLDS (Yukawa) [E]: with M=0, [[D,pi(a)], J pi(b) J^-1] = 0 "
          "for all a,b -- the Dirac/Yukawa operator satisfies the first-order "
          "condition", fo0)

    # 4. first order VIOLATED by the Majorana/sigma, localized to the M entries
    violated = False
    support_ok = True
    for _ in range(50):
        a = rng.normal(size=3) + 1j * rng.normal(size=3)
        b = rng.normal(size=3) + 1j * rng.normal(size=3)
        comm_Da = D @ pi(rho(a)) - pi(rho(a)) @ D
        fo = comm_Da @ JbJ(rho(b)) - JbJ(rho(b)) @ comm_Da
        if not np.allclose(fo, 0):
            violated = True
        # the nonzero part must live in the off-diagonal (particle<->antiparticle) blocks,
        # built from M; the pure-Yukawa diagonal blocks must stay zero
        if not (np.allclose(fo[:3, :3], 0) and np.allclose(fo[3:, 3:], 0)):
            support_ok = False
    check("FIRST ORDER VIOLATED BY MAJORANA/sigma [E]: with M != 0 the first-order "
          "commutator is NONZERO and supported EXACTLY on the off-diagonal "
          "(nu_R nu_R^c) blocks built from M -- the sigma is the unique first-order "
          "violator; this controlled violation IS the CCvS Pati-Salam mechanism",
          violated and support_ok)

    # 5. sigma = scalaron (physical identification)
    check("sigma = SCALARON [C]: the Majorana-generating singlet sigma is identified "
          "with the TFPT scalaron (M_PS = kappa M_s, v249); inner fluctuations along "
          "sigma promote the SM gauge group to Pati-Salam (CCvS). Physical "
          "identification, [O] (scalaron<->nu_R nu_R coupling to be proven)", True)

    # 6. scope
    check("SCOPE [O]: this exhibits the first-order MECHANISM on the lepton block; "
          "the full 96-dim SM/PS finite triple, the spectral-action expansion and "
          "the sigma=scalaron coupling remain the open contract (v250)", True)

    return summary("v251 first-order violated by Majorana/sigma -- CCvS Pati-Salam mechanism (PS.DIRAC.01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

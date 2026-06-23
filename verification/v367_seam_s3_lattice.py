"""v367 -- SEAM.S3.LATTICE.01 (Track 1): the EXPLICIT lattice realisation of the S3 input --
a concrete gapped chiral-Majorana (p+ip) lattice model whose edge is the 16-Majorana
SO(16)_1 carrier, with the mu4 clock condensing it to (E8)_1.  This turns the abstract S3
residual of v356/v366 ("the collar realised as a genuine lattice chiral free-fermion
invertible phase") into a RUNNABLE lattice model with a numerically-computed topological
invariant -- not a re-assertion of det K / c_-.

It does NOT prove the continuum scaling limit (that is the cited MMST theorem, v336) and does
NOT close SEAM.EQUIV.01; it exhibits the explicit invertible lattice phase that S3 asks for.

Model: a single chiral Majorana is the BdG p+ip / QWZ two-band Bloch Hamiltonian
    h(k) = sin(kx) sigma_x + sin(ky) sigma_y + (M - cos kx - cos ky) sigma_z,
gapped for M not in {0, +-2}, with Chern number C = +-1 in the topological window
(|M|<2) and C = 0 trivially (|M|>2).  A chiral Majorana edge carries c_- = C/2, so
N_Maj = 16 copies in the topological phase give c_- = 16 * (1/2) = 8 = g_car + N_fam.

  [E] 1. THE BULK IS GAPPED.  for M=1 the band gap 2*min_k|d(k)| = 2 > 0 (numerically), so
        the model is a gapped free-fermion phase (a quasi-free invertible candidate).
  [E] 2. NON-TRIVIAL CHERN NUMBER (numerically computed).  the Fukui-Hatsugai-Suzuki
        plaquette Chern number of the occupied band is |C| = 1 for M=1 (topological) and
        C = 0 for M=3 (trivial, neg control) -- a genuine lattice topological invariant.
  [E] 3. CHIRAL CENTRAL CHARGE c_- = 8.  each chiral Majorana edge carries c_- = C/2 = 1/2;
        the carrier is N_Maj = dim S^+ = 2^(g_car-1) = 16 copies, so c_- = 16/2 = 8 =
        g_car + N_fam (the gravitational anomaly / edge chiral central charge).
  [E] 4. THE EDGE K-MATRIX DISCRIMINATOR.  the 16-Majorana edge is SO(16)_1 (det Cartan
        D8 = 4, four primaries); the order-4 mu4 clock condenses it to (E8)_1 (det Cartan
        E8 = 1, one primary) -- det K 4 -> 1, the holomorphy discriminator (v351/v369).
  [C] 5. mu4 CONDENSATION TO (E8)_1.  the lattice free-fermion model realises SO(16)_1
        directly; the index-4 simple-current (mu4) extension SO(16)_1 -> (E8)_1 (v154/v351)
        is the seam glue on top -- cited, conditional.
  [O] 6. RESIDUAL.  the genuine continuum SCALING-LIMIT existence (the lattice model's
        massless limit IS the chiral CFT, MMST v336) stays [O]; v367 exhibits the explicit
        gapped invertible lattice phase (S3) but does NOT prove its scaling limit.  So S3 is
        now a CONCRETE lattice model with a computed invariant, reduced -- not closed.

Status: [E] the explicit gapped Chern model + the c_- = 8 counting + the det K discriminators
(numerical Chern + exact lattice arithmetic); [C] the mu4 condensation to (E8)_1; [O] the
continuum scaling limit.  Reduces S3 to a runnable lattice model; does NOT close
SEAM.EQUIV.01.  Python (numpy; Fukui-Hatsugai-Suzuki Chern + sympy Cartan dets)."""
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

# Pauli matrices
SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)


def _d(kx, ky, M):
    return np.array([np.sin(kx), np.sin(ky), M - np.cos(kx) - np.cos(ky)])


def _hbloch(kx, ky, M):
    dx, dy, dz = _d(kx, ky, M)
    return dx * SX + dy * SY + dz * SZ


def _occ_vec(kx, ky, M):
    """Lower-band (occupied) eigenvector of the 2-band BdG Hamiltonian."""
    w, v = np.linalg.eigh(_hbloch(kx, ky, M))
    return v[:, 0]


def _chern(M, N=24):
    """Fukui-Hatsugai-Suzuki plaquette Chern number of the occupied band."""
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    u = [[_occ_vec(kx, ky, M) for ky in ks] for kx in ks]
    F = 0.0
    for i in range(N):
        for j in range(N):
            ip, jp = (i + 1) % N, (j + 1) % N
            u00, u10, u01, u11 = u[i][j], u[ip][j], u[i][jp], u[ip][jp]
            Ux = np.vdot(u00, u10); Ux /= abs(Ux)
            Uy = np.vdot(u10, u11); Uy /= abs(Uy)
            Ux2 = np.vdot(u01, u11); Ux2 /= abs(Ux2)
            Uy2 = np.vdot(u00, u01); Uy2 /= abs(Uy2)
            F += np.angle(Ux * Uy * np.conj(Ux2) * np.conj(Uy2))
    return F / (2 * np.pi)


def _gap(M, N=48):
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    return 2 * min(np.linalg.norm(_d(kx, ky, M)) for kx in ks for ky in ks)


def _cartan_det(n, edges):
    A = sp.zeros(n, n)
    for i in range(n):
        A[i, i] = 2
    for a, b in edges:
        A[a - 1, b - 1] = -1
        A[b - 1, a - 1] = -1
    return int(A.det())


def run():
    reset()
    print("v367  SEAM.S3.LATTICE.01: explicit gapped chiral-Majorana (p+ip) lattice model => c_-=8, det K=1")

    # 1. bulk is gapped (M=1 topological)
    gap_topo = _gap(1.0)
    check("BULK IS GAPPED [E]: the p+ip model h(k)=sin kx sx + sin ky sy + (M-cos kx-cos ky) sz "
          "at M=1 has band gap 2 min|d(k)| = %.3f > 0 -- a gapped free-fermion (quasi-free "
          "invertible) phase" % gap_topo, gap_topo > 1.0)

    # 2. non-trivial Chern number (numerical), with a trivial neg control
    C_topo = _chern(1.0)
    C_triv = _chern(3.0)
    check("NON-TRIVIAL CHERN NUMBER [E]: the Fukui-Hatsugai-Suzuki Chern number is |C|=%d at "
          "M=1 (topological) and C=%d at M=3 (trivial, neg control) -- a genuine numerically "
          "computed lattice topological invariant"
          % (round(abs(C_topo)), round(C_triv)),
          abs(round(abs(C_topo)) - 1) == 0 and abs(round(C_triv)) == 0)

    # 3. chiral central charge c_- = 8 from N_Maj=16 copies, each c_-=C/2=1/2
    N_Maj = 2 ** (g_car - 1)                     # 16 = dim S^+
    c_minus = N_Maj * abs(round(abs(C_topo))) / 2
    check("CHIRAL CENTRAL CHARGE c_-=8 [E]: each chiral Majorana edge carries c_-=C/2=1/2; the "
          "carrier is N_Maj=dim S^+=2^(g_car-1)=%d copies, so c_-=%d/2=%g = g_car+N_fam=%d "
          "(the edge gravitational anomaly)" % (N_Maj, N_Maj, c_minus, g_car + N_fam),
          N_Maj == 16 and c_minus == 8 and c_minus == g_car + N_fam)

    # 4. edge K-matrix discriminator: SO(16)_1 (det 4) -> (E8)_1 (det 1)
    detE8 = _cartan_det(8, [(1, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (2, 4)])
    detD8 = _cartan_det(8, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (6, 8)])
    check("EDGE K-MATRIX DISCRIMINATOR [E]: the 16-Majorana edge is SO(16)_1 (det Cartan D8=%d, "
          "four primaries); the order-4 mu4 clock condenses it to (E8)_1 (det Cartan E8=%d, one "
          "primary) -- det K 4->1, the holomorphy discriminator (v351/v369)" % (detD8, detE8),
          detD8 == 4 and detE8 == 1)

    # 5. mu4 condensation to (E8)_1 (cited, conditional)
    check("mu4 CONDENSATION TO (E8)_1 [C]: the lattice free-fermion model realises SO(16)_1 "
          "directly; the index-4 simple-current (mu4) extension SO(16)_1 -> (E8)_1 (v154/v351) "
          "is the seam glue on top -- cited, conditional", True)

    # 6. residual (honest fence)
    check("RESIDUAL [O]: the continuum SCALING-LIMIT existence (the lattice model's massless "
          "limit IS the chiral CFT, MMST v336) stays [O]; v367 exhibits the explicit gapped "
          "invertible lattice phase (S3) with a computed invariant but does NOT prove its "
          "scaling limit -- S3 is now a CONCRETE lattice model, reduced not closed", True)

    return summary("v367 SEAM.S3.LATTICE.01: an explicit gapped chiral-Majorana (p+ip) lattice model "
                   "(band gap 2>0, numerical Chern |C|=1; trivial C=0 control) realises the 16-Majorana "
                   "edge c_-=16/2=8=g_car+N_fam, with det K 4->1 (SO(16)_1 -> (E8)_1 via the mu4 clock); "
                   "turns the S3 input into a runnable lattice model -- reduces, does NOT close SEAM.EQUIV.01")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

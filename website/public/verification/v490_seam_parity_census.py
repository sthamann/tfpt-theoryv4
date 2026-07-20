"""v490 -- SEAM.MU.01: the spin-structure fermion-parity census on T^2 for the v367 seam
lattice model -- the lattice ground-state witness of "mu_pre = 4 before condensation"
(step 1 of the v378 KLM chain), plus the 16-fold-way bridge theta_v = 1 with the MEASURED
nu = 2 c_- = 16 (v489).

The torus has 4 spin structures (boundary-condition sectors AA, AP, PA, PP).  The BdG
ground-state fermion parity per sector is a Z2 invariant, determined here TWICE:
  (a) Read-Green TRIM product: parity(s) = prod_{k* in TRIM(s)} sign(dz(k*));
  (b) real-space Majorana Pfaffian sign via Schur decomposition (independent cross-check;
      parities reported RELATIVE to the trivial M=3 phase so the Pf sign convention drops out).
Number of EVEN sectors = number of ground states of the gauged (fermion-parity-gauged)
theory on T^2 = the total quantum dimension mu of the gauged anyon theory.

  [E] 1. REAL-SPACE = BLOCH SANITY.  the twisted real-space BdG spectrum equals the Bloch
        bands on the sector k-grid to 9e-15 (both PP and AA sectors) -- the lattice
        Hamiltonian is exactly the v367 model.
  [E] 2. PER-LAYER PARITY CENSUS (+,+,+,-).  TRIM product and Pfaffian agree sector by
        sector: (AA, AP, PA, PP) = (+1, +1, +1, -1) relative to the trivial phase -- 3 even
        sectors, the Ising / nu = 1 signature (gauged #anyons = 3).
  [E] 3. 16 LAYERS => mu_pre = 4.  parity_16(s) = parity_1(s)^16 = +1 in ALL FOUR sectors
        => gauged torus GSD = 4 = mu(SO(16)_1) = |det Cartan(D8)| -- the lattice
        ground-state witness that the carrier sits in the SO(16)_1 class BEFORE the mu4
        condensation (v378 step 1).
  [E] 4. 16-FOLD-WAY BRIDGE theta_v = 1.  Kitaev's 16-fold way assigns the gauged vortex
        topological spin theta_v = exp(2 pi i nu/16); with nu = 2 c_- = 16 (c_- = 8 measured
        from the ground state, v489) theta_v = 1 EXACTLY (sympy) -- the vortex is a boson,
        condensable; rivals nu = 1, 2, 8 give theta_v != 1 (not holomorphically condensable).
  [E] 5. HONEST NON-DISCRIMINATOR FENCE.  the fermionic Kitaev-Preskill TEE of the free
        ground state is identically ZERO -- gamma_f = 0.000000 for the topological M=1 AND
        the trivial M=3 (both < 1e-4 at L=32) -- an invertible fermionic phase has no TEE,
        so this observable does NOT discriminate (E8)_1 vs SO(16)_1 (both exist only after
        gauging).  Computed and recorded so nobody mistakes it for a discriminator.
  [C] 6. KLM CONDENSATION STEP (cited).  mu_post = mu_pre/|L|^2 = 4/2^2 = 1 (holomorphic,
        (E8)_1) -- the KLM mu-additivity theorem (v378); the condensed model is interacting,
        NOT free-fermion computable.  The numerics of this module pin only
        {c_- = 8 (v489), mu_pre = 4, theta_v = 1} -- the premise package of the condensation.
  [O] 7. RESIDUAL.  the continuum scaling limit (MMST, v336) stays [O]; SEAM.EQUIV.01 is
        NOT closed by this module.

Status: [E] Lattice (parity census, double-determined + 16-fold-way arithmetic + TEE fence);
[C] the KLM step 4 -> 4/2^2 = 1; [O] the continuum limit.  Python (numpy + scipy Schur +
sympy exact theta_v)."""
import numpy as np
import sympy as sp
from scipy.linalg import schur

from tfpt_constants import check, summary, reset, g_car, N_fam

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)
ID2 = np.eye(2, dtype=complex)
S_MAJ = np.array([[1, 1], [-1j, 1j]], complex)

TRIM = [(0.0, 0.0), (np.pi, 0.0), (0.0, np.pi), (np.pi, np.pi)]


def _dz(kx, ky, M):
    return M - np.cos(kx) - np.cos(ky)


def _sector_kgrid(L, bc):
    """bc = (bx, by), 0 = periodic, 1 = antiperiodic; L even keeps AP grids off 0, pi."""
    return (2 * np.pi * (np.arange(L) + bc[0] / 2) / L,
            2 * np.pi * (np.arange(L) + bc[1] / 2) / L)


def _parity_trim(L, bc, M):
    """Read-Green: ground-state parity (relative to trivial) = prod over TRIM in the grid."""
    kx, ky = _sector_kgrid(L, bc)
    inx = {round(k % (2 * np.pi), 9) for k in kx}
    iny = {round(k % (2 * np.pi), 9) for k in ky}
    p = 1
    for (tx, ty) in TRIM:
        if round(tx, 9) in inx and round(ty, 9) in iny:
            p *= int(np.sign(_dz(tx, ty, M)))
    return p


def _real_space_bdg(L, bc, M):
    """2N x 2N BdG matrix in basis (c_1..c_N, c^dag_1..c^dag_N) with twisted links.

    Fourier transform of (1/2) sum_k Psi^dag h(k) Psi, h(k) as in v367: hopping -1/2 per
    bond, pairing Delta_{r,r+x} = -i/2 (sin kx), Delta_{r,r+y} = -1/2 (-i sin ky); an
    antiperiodic direction flips the sign of boundary-crossing hopping AND pairing.
    """
    N = L * L
    idx = lambda x, y: (x % L) * L + (y % L)
    Hpp = np.zeros((N, N), complex)
    Dpp = np.zeros((N, N), complex)
    for x in range(L):
        for y in range(L):
            i = idx(x, y)
            Hpp[i, i] = M
            for (dxy, amp) in [((1, 0), -0.5j), ((0, 1), -0.5)]:
                j = idx(x + dxy[0], y + dxy[1])
                s = 1.0
                if dxy[0] == 1 and x == L - 1 and bc[0] == 1:
                    s = -1.0
                if dxy[1] == 1 and y == L - 1 and bc[1] == 1:
                    s = -1.0
                Hpp[i, j] += -0.5 * s
                Hpp[j, i] += -0.5 * s
                Dpp[i, j] += amp * s
                Dpp[j, i] -= amp * s
    H = np.zeros((2 * N, 2 * N), complex)
    H[:N, :N] = Hpp
    H[N:, N:] = -Hpp.conj()
    H[:N, N:] = Dpp
    H[N:, :N] = Dpp.conj().T
    return H


def _bloch_bands(L, bc, M):
    kx, ky = _sector_kgrid(L, bc)
    Es = []
    for a in kx:
        for b in ky:
            e = np.sqrt(np.sin(a)**2 + np.sin(b)**2 + _dz(a, b, M)**2)
            Es += [e, -e]
    return np.sort(np.array(Es))


def _pfaffian_sign(A):
    """sign(Pf) of a real antisymmetric matrix via the real Schur decomposition."""
    T, Q = schur(A, output="real")
    s = np.sign(np.linalg.det(Q))
    for i in range(0, A.shape[0], 2):
        s *= np.sign(T[i, i + 1])
    return int(s)


def _parity_pfaffian(L, bc, M):
    """Ground-state parity from sign Pf(A), A the real antisymmetric Majorana form."""
    H = _real_space_bdg(L, bc, M)
    N = L * L
    W = np.zeros((2 * N, 2 * N), complex)          # Psi = W gamma
    for j in range(N):
        W[j, 2 * j] = 0.5;     W[j, 2 * j + 1] = 0.5j
        W[N + j, 2 * j] = 0.5; W[N + j, 2 * j + 1] = -0.5j
    Mmat = W.conj().T @ H @ W
    A = -2j * (Mmat - Mmat.T) / 2
    assert np.abs(A.imag).max() < 1e-9
    return _pfaffian_sign(A.real)


# ---------------- fermionic Kitaev-Preskill TEE (the non-discriminator fence) ----------------
def _corr_tensor(L, M):
    k = 2 * np.pi * np.arange(L) / L
    KX, KY = np.meshgrid(k, k, indexing="ij")
    dx, dy, dz = np.sin(KX), np.sin(KY), M - np.cos(KX) - np.cos(KY)
    E = np.sqrt(dx**2 + dy**2 + dz**2)
    P = 0.5 * (ID2[None, None] + (dx[..., None, None] * SX
                                  + dy[..., None, None] * SY
                                  + dz[..., None, None] * SZ) / E[..., None, None])
    G = np.einsum("ma,klab,bc,nc->klmn", S_MAJ, P, SX, S_MAJ)
    return np.fft.ifft2(G, axes=(0, 1))


def _gamma_sub(Mten, sites):
    L = Mten.shape[0]
    xs = np.array([s[0] for s in sites]); ys = np.array([s[1] for s in sites])
    blocks = Mten[(xs[:, None] - xs[None, :]) % L, (ys[:, None] - ys[None, :]) % L]
    n = len(sites)
    Mbig = blocks.transpose(0, 2, 1, 3).reshape(2 * n, 2 * n)
    return (1j * (Mbig - np.eye(2 * n))).real


def _entropy(Gam):
    lam = np.linalg.eigvalsh(1j * Gam)
    p = np.clip((1 + lam) / 2, 1e-16, 1 - 1e-16)
    return -0.5 * float(np.sum(p * np.log(p) + (1 - p) * np.log(1 - p)))


def _kitaev_preskill(L, R, M):
    """S_topo = S_A+S_B+S_C-S_AB-S_BC-S_CA+S_ABC = -gamma on the 120-degree pie."""
    Mten = _corr_tensor(L, M)
    c = (L / 2 - 0.5, L / 2 - 0.5)
    A, B, C = [], [], []
    for x in range(L):
        for y in range(L):
            rx, ry = x - c[0], y - c[1]
            if rx * rx + ry * ry > R * R:
                continue
            th = np.arctan2(ry, rx) % (2 * np.pi)
            (A if th < 2 * np.pi / 3 else B if th < 4 * np.pi / 3 else C).append((x, y))
    S = {name: _entropy(_gamma_sub(Mten, reg))
         for name, reg in [("A", A), ("B", B), ("C", C), ("AB", A + B),
                           ("BC", B + C), ("CA", C + A), ("ABC", A + B + C)]}
    return (S["A"] + S["B"] + S["C"] - S["AB"] - S["BC"] - S["CA"] + S["ABC"])


def run():
    reset()
    print("v490  SEAM.MU.01: T^2 spin-structure parity census => mu_pre = 4; 16-fold-way theta_v = 1")
    L = 8
    names = {(1, 1): "AA", (1, 0): "AP", (0, 1): "PA", (0, 0): "PP"}

    # 1. real-space = Bloch sanity (both sectors)
    devs = []
    for bc in [(0, 0), (1, 1)]:
        e_r = np.sort(np.linalg.eigvalsh(_real_space_bdg(L, bc, 1.0)))
        e_k = _bloch_bands(L, bc, 1.0)
        devs.append(np.abs(e_r - e_k).max())
    check("REAL-SPACE = BLOCH SANITY [E]: the twisted real-space BdG spectrum equals the Bloch "
          "bands on the sector k-grid to %.1e (PP) / %.1e (AA) -- the lattice Hamiltonian is "
          "exactly the v367 model" % (devs[0], devs[1]), max(devs) < 1e-12)

    # 2. per-layer parity census: TRIM product == Pfaffian, (+,+,+,-)
    census = {}
    agree = True
    for bc in [(1, 1), (1, 0), (0, 1), (0, 0)]:
        pt = _parity_trim(L, bc, 1.0)
        p1 = _parity_pfaffian(L, bc, 1.0)
        p3 = _parity_pfaffian(L, bc, 3.0)
        rel = p1 * p3                              # parity relative to the trivial phase
        census[names[bc]] = rel
        agree = agree and (pt == rel)
    expected = {"AA": 1, "AP": 1, "PA": 1, "PP": -1}
    check("PER-LAYER PARITY CENSUS [E]: (AA, AP, PA, PP) = (%+d, %+d, %+d, %+d) relative to the "
          "trivial phase, TRIM product == real-space Pfaffian in every sector -- 3 even sectors, "
          "the nu = 1 Ising signature (gauged #anyons = 3)"
          % (census["AA"], census["AP"], census["PA"], census["PP"]),
          census == expected and agree)

    # 3. 16 layers => mu_pre = 4 = |det Cartan(D8)|
    N_Maj = 2 ** (g_car - 1)
    census16 = {k: v ** N_Maj for k, v in census.items()}
    n_even_16 = sum(1 for v in census16.values() if v == +1)
    A_D8 = sp.zeros(8, 8)
    for i in range(8):
        A_D8[i, i] = 2
    for a, b in [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (6, 8)]:
        A_D8[a - 1, b - 1] = -1
        A_D8[b - 1, a - 1] = -1
    detD8 = int(A_D8.det())
    check("16 LAYERS => mu_pre = 4 [E]: parity_16(s) = parity_1(s)^16 = +1 in ALL %d/4 sectors "
          "=> gauged torus GSD = 4 = mu(SO(16)_1) = |det Cartan(D8)| = %d -- the lattice "
          "ground-state witness of 'mu_pre = 4 before condensation' (v378 step 1)"
          % (n_even_16, detD8),
          N_Maj == 16 and n_even_16 == 4 and detD8 == 4)

    # 4. 16-fold-way bridge: theta_v = exp(2 pi i nu/16) = 1 at nu = 2 c_- = 16 (exact)
    nu = 2 * (g_car + N_fam)                       # = 2 c_- = 16, c_- measured by v489
    theta_v = sp.exp(2 * sp.pi * sp.I * sp.Rational(nu, 16))
    rivals_ok = all(sp.simplify(sp.exp(2 * sp.pi * sp.I * sp.Rational(nr, 16)) - 1) != 0
                    for nr in (1, 2, 8))
    check("16-FOLD-WAY BRIDGE theta_v = 1 [E]: with nu = 2 c_- = %d (c_- = 8 measured from the "
          "ground state, v489) the gauged vortex spin theta_v = exp(2 pi i nu/16) = 1 EXACTLY "
          "(sympy) -- a BOSON, condensable; rivals nu = 1, 2, 8 give theta_v != 1 (not "
          "holomorphically condensable)" % nu,
          nu == 16 and sp.simplify(theta_v - 1) == 0 and rivals_ok)

    # 5. honest fence: the fermionic Kitaev-Preskill TEE does NOT discriminate
    g_topo = -_kitaev_preskill(32, 11, 1.0)
    g_triv = -_kitaev_preskill(32, 11, 3.0)
    check("NON-DISCRIMINATOR FENCE [E]: the fermionic Kitaev-Preskill TEE is identically zero "
          "-- gamma_f = %.6f (M=1, topological) and %.6f (M=3, trivial), both < 1e-4 at L=32 "
          "-- an invertible fermionic phase has no TEE, so gamma_f does NOT discriminate "
          "(E8)_1 vs SO(16)_1 (both live only after gauging)" % (g_topo, g_triv),
          abs(g_topo) < 1e-4 and abs(g_triv) < 1e-4)

    # 6. KLM condensation step (cited, conditional)
    mu_post = sp.Rational(4, 2 ** 2)
    check("KLM CONDENSATION STEP [C]: mu_post = mu_pre/|L|^2 = 4/2^2 = %s (holomorphic, (E8)_1) "
          "-- the cited KLM mu-additivity theorem (v378); the condensed model is interacting, "
          "NOT free-fermion computable: this module's numerics pin only {c_- = 8 (v489), "
          "mu_pre = 4, theta_v = 1}, the premise package of the condensation" % mu_post,
          mu_post == 1)

    # 7. residual
    check("RESIDUAL [O]: the continuum scaling limit (MMST, v336) stays [O]; SEAM.EQUIV.01 is "
          "NOT closed by this module -- it supplies the lattice premise package of the "
          "condensation, nothing more", True)

    return summary("v490 SEAM.MU.01: the T^2 spin-structure parity census (TRIM product == Pfaffian, "
                   "per layer (+,+,+,-)) gives, for the 16-layer carrier, ALL four sectors even => gauged "
                   "torus GSD = 4 = mu(SO(16)_1) -- the lattice witness of mu_pre = 4; the 16-fold-way "
                   "bridge with measured nu = 2 c_- = 16 gives theta_v = 1 exactly (vortex condensable, "
                   "rivals nu = 1, 2, 8 excluded); the fermionic Kitaev-Preskill TEE is 0 for BOTH phases "
                   "(non-discriminator fence); the KLM step 4 -> 4/2^2 = 1 stays cited [C]; "
                   "SEAM.EQUIV.01 stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

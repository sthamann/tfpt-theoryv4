"""probe_tee_mu_discriminator.py -- EXPLORATION (experiments/tfpt-discovery, NOT load-bearing).

Part 2 of the SEAM.EQUIV.01 ground-state witness hunt: what can a lattice ground-state
measurement say about HOLOMORPHY mu = 1 ((E8)_1) vs the rival mu = 4 (SO(16)_1)?

Three measurements on the v367 p+ip model (verification/v367_seam_s3_lattice.py):

 (1) FERMIONIC Kitaev-Preskill TEE of the free ground state.
     S_topo = S_A + S_B + S_C - S_AB - S_BC - S_CA + S_ABC = -gamma.
     Expectation: the free 16-layer state is an INVERTIBLE fermionic phase, so
     gamma_f = 0.  This does NOT discriminate (E8)_1 vs SO(16)_1: both bosonic
     theories live only AFTER gauging fermion parity; the free state knows nothing
     of the gauged anyons.  We compute it honestly (M=1 topological vs M=3 trivial).

 (2) SPIN-STRUCTURE PARITY CENSUS on T^2 (the next-best mu witness).
     The torus has 4 spin structures (AA, AP, PA, PP boundary conditions).  The BdG
     ground-state fermion parity per sector is a Z2 invariant:
         parity(s) = prod_{k* in TRIM(s)} sign(dz(k*))     (Read-Green),
     computed here BOTH from the TRIM product AND from the real-space Majorana
     Pfaffian sign (independent cross-check, Schur decomposition).
     - 1 layer (nu=1):  (AA,AP,PA,PP) = (+,+,+,-)  -> 3 even sectors -> gauged
       theory has 3 anyons (Ising).
     - 16 layers (nu=16): parity(PP) = (-1)^16 = + -> ALL 4 sectors even -> the
       gauged theory has 4 anyons = mu(SO(16)_1) = 4.  This is the lattice
       ground-state witness of "mu = 4 before condensation" (v378 step 1).

 (3) THE 16-FOLD-WAY BRIDGE (arithmetic on measured numbers; the condensation step
     itself stays an argument, NOT numerics).  Kitaev's 16-fold way: the gauged
     vortex has topological spin theta_v = exp(2 pi i nu / 16).  With nu = 2 c_-
     MEASURED by the modular commutator (probe_modular_commutator.py: c_- = 8.0000),
     theta_v = exp(2 pi i * 16/16) = 1: the vortex is a BOSON, condensable; KLM then
     gives mu: 4 -> 4/2^2 = 1, i.e. (E8)_1.  theta_v = 1 iff nu = 0 mod 16 -- for
     any other nu (e.g. a single layer, nu=1, theta_v = e^{i pi/8}) holomorphy is
     IMPOSSIBLE.  The condensed model is interacting, so mu = 1 itself is not free-
     fermion computable; honest type: numerics pin {c_- = 8, mu_pre = 4, theta_v = 1},
     the step "condense => mu = 1" is the cited KLM/condensation theorem.

Throwaway probe: numbers only, no paper/ledger claims.
"""
import time

import numpy as np
from scipy.linalg import schur

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)
ID2 = np.eye(2, dtype=complex)
S_MAJ = np.array([[1, 1], [-1j, 1j]], complex)


# ---------------------------------------------------------------- Gaussian toolkit
def corr_tensor(L, M):
    """Same as probe_modular_commutator: M(d) = FT of [S P_+(k) sx S^T]."""
    k = 2 * np.pi * np.arange(L) / L
    KX, KY = np.meshgrid(k, k, indexing="ij")
    dx, dy, dz = np.sin(KX), np.sin(KY), M - np.cos(KX) - np.cos(KY)
    E = np.sqrt(dx**2 + dy**2 + dz**2)
    assert E.min() > 1e-9
    P = 0.5 * (ID2[None, None] + (dx[..., None, None] * SX
                                  + dy[..., None, None] * SY
                                  + dz[..., None, None] * SZ) / E[..., None, None])
    G = np.einsum("ma,klab,bc,nc->klmn", S_MAJ, P, SX, S_MAJ)
    return np.fft.ifft2(G, axes=(0, 1))


def gamma_sub(Mten, sites):
    L = Mten.shape[0]
    xs = np.array([s[0] for s in sites]); ys = np.array([s[1] for s in sites])
    blocks = Mten[(xs[:, None] - xs[None, :]) % L, (ys[:, None] - ys[None, :]) % L]
    n = len(sites)
    Mbig = blocks.transpose(0, 2, 1, 3).reshape(2 * n, 2 * n)
    Gam = 1j * (Mbig - np.eye(2 * n))
    assert np.abs(Gam.imag).max() < 1e-9
    return Gam.real


def entropy(Gam):
    lam = np.linalg.eigvalsh(1j * Gam)
    p = np.clip((1 + lam) / 2, 1e-16, 1 - 1e-16)
    return -0.5 * float(np.sum(p * np.log(p) + (1 - p) * np.log(1 - p)))


def pie_regions(L, R):
    c = (L / 2 - 0.5, L / 2 - 0.5)
    A, B, C = [], [], []
    for x in range(L):
        for y in range(L):
            rx, ry = x - c[0], y - c[1]
            if rx * rx + ry * ry > R * R:
                continue
            th = np.arctan2(ry, rx) % (2 * np.pi)
            (A if th < 2 * np.pi / 3 else B if th < 4 * np.pi / 3 else C).append((x, y))
    return A, B, C


def kitaev_preskill(Mten, L, R):
    A, B, C = pie_regions(L, R)
    S = {}
    for name, reg in [("A", A), ("B", B), ("C", C), ("AB", A + B),
                      ("BC", B + C), ("CA", C + A), ("ABC", A + B + C)]:
        S[name] = entropy(gamma_sub(Mten, reg))
    stopo = (S["A"] + S["B"] + S["C"] - S["AB"] - S["BC"] - S["CA"] + S["ABC"])
    return stopo, S


# ------------------------------------------------- spin-structure parity census
TRIM = [(0.0, 0.0), (np.pi, 0.0), (0.0, np.pi), (np.pi, np.pi)]


def dz(kx, ky, M):
    return M - np.cos(kx) - np.cos(ky)


def sector_kgrid(L, bc):
    """bc = (bx,by), 0 = periodic, 1 = antiperiodic; L even avoids 0,pi for AP."""
    return (2 * np.pi * (np.arange(L) + bc[0] / 2) / L,
            2 * np.pi * (np.arange(L) + bc[1] / 2) / L)


def parity_trim(L, bc, M):
    """Read-Green: ground-state parity (relative to trivial) = prod over TRIM in grid."""
    kx, ky = sector_kgrid(L, bc)
    inx = {round(k % (2 * np.pi), 9) for k in kx}
    iny = {round(k % (2 * np.pi), 9) for k in ky}
    p = 1
    for (tx, ty) in TRIM:
        if round(tx, 9) in inx and round(ty, 9) in iny:
            p *= int(np.sign(dz(tx, ty, M)))
    return p


def real_space_bdg(L, bc, M):
    """2N x 2N BdG matrix in basis (c_1..c_N, c^dag_1..c^dag_N), twisted links.

    Fourier transform of (1/2) sum_k Psi^dag h(k) Psi with h(k) as in v367:
      hopping  -1/2 per bond (xi = M - cos kx - cos ky),
      pairing  Delta_{r,r+x} = -i/2 (from sin kx), Delta_{r,r+y} = -1/2 (from -i sin ky).
    Antiperiodic direction: boundary-crossing hopping AND pairing pick up -1.
    Sanity-checked below against the Bloch bands on the sector k-grid.
    """
    N = L * L
    idx = lambda x, y: (x % L) * L + (y % L)
    Hpp = np.zeros((N, N), complex)          # particle-particle (hermitian)
    Dpp = np.zeros((N, N), complex)          # pairing c^dag c^dag (antisymmetric)
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


def bloch_bands(L, bc, M):
    kx, ky = sector_kgrid(L, bc)
    Es = []
    for a in kx:
        for b in ky:
            Es += [+np.sqrt(np.sin(a)**2 + np.sin(b)**2 + dz(a, b, M)**2)] * 1
            Es += [-np.sqrt(np.sin(a)**2 + np.sin(b)**2 + dz(a, b, M)**2)] * 1
    return np.sort(np.array(Es))


def pfaffian_sign(A):
    """sign(Pf) of a real antisymmetric matrix via real Schur decomposition."""
    T, Q = schur(A, output="real")
    detQ = np.sign(np.linalg.det(Q))
    n = A.shape[0]
    s = detQ
    for i in range(0, n, 2):
        s *= np.sign(T[i, i + 1])
    return int(s)


def parity_pfaffian(L, bc, M):
    """Ground-state parity from sign Pf(A), A the Majorana form: H = (i/4) g^T A g.

    gamma_{2j} = c_j + c^dag_j, gamma_{2j+1} = -i(c_j - c^dag_j)  =>  Psi = W gamma;
    H = (1/2) Psi^dag H_BdG Psi = (1/2) g^T M g + const, M = W^dag H_BdG W, and the
    antisymmetric part gives A = -2i * antisym(M) (real).  Only parities RELATIVE
    to the trivial phase (M=3) are reported, so the Pf sign convention drops out.
    """
    H = real_space_bdg(L, bc, M)
    N = L * L
    W = np.zeros((2 * N, 2 * N), complex)     # Psi = W gamma
    for j in range(N):
        W[j, 2 * j] = 0.5;     W[j, 2 * j + 1] = 0.5j
        W[N + j, 2 * j] = 0.5; W[N + j, 2 * j + 1] = -0.5j
    Mmat = W.conj().T @ H @ W
    A = -2j * (Mmat - Mmat.T) / 2
    assert np.abs(A.imag).max() < 1e-9, np.abs(A.imag).max()
    return pfaffian_sign(A.real)


def main():
    # ---------- (1) fermionic Kitaev-Preskill TEE ----------
    print("== (1) fermionic Kitaev-Preskill TEE: S_topo = -gamma  (invertible => 0) ==")
    print(f"   {'L':>4} {'R':>4} {'M':>4} {'S_topo':>12} {'gamma':>12} {'t[s]':>6}")
    for (L, R, M) in [(24, 8, 1.0), (32, 11, 1.0), (40, 14, 1.0), (48, 17, 1.0),
                      (32, 11, 3.0), (48, 17, 3.0)]:
        t0 = time.time()
        Mten = corr_tensor(L, M)
        stopo, _ = kitaev_preskill(Mten, L, R)
        print(f"   {L:>4} {R:>4} {M:>4.0f} {stopo:>12.6f} {-stopo:>12.6f} "
              f"{time.time()-t0:>6.1f}")
    print("   NOTE: per-layer; 16 decoupled layers give 16x gamma (still 0 if 0).")
    print("   The free state is a fermionic INVERTIBLE phase: gamma_f = 0 does NOT")
    print("   discriminate (E8)_1 vs SO(16)_1 -- both live only after gauging.")

    # ---------- (2) spin-structure parity census ----------
    print("\n== (2) T^2 spin-structure parity census (TRIM product vs Pfaffian) ==")
    L = 8
    # sanity: real-space BdG spectrum == Bloch bands, both sectors
    for bc in [(0, 0), (1, 1)]:
        Hr = real_space_bdg(L, bc, 1.0)
        e_r = np.sort(np.linalg.eigvalsh(Hr))
        e_k = bloch_bands(L, bc, 1.0)
        print(f"   sanity bc={bc}: max|spec(real-space) - spec(Bloch)| = "
              f"{np.abs(e_r - e_k).max():.2e}")
    names = {(1, 1): "AA", (1, 0): "AP(y-per)", (0, 1): "PA(x-per)", (0, 0): "PP"}
    print(f"   {'sector':>10} {'TRIM prod M=1':>14} {'Pf M=1':>7} {'Pf M=3':>7} "
          f"{'rel parity':>10}")
    census = {}
    for bc in [(1, 1), (1, 0), (0, 1), (0, 0)]:
        pt = parity_trim(L, bc, 1.0)
        p1 = parity_pfaffian(L, bc, 1.0)
        p3 = parity_pfaffian(L, bc, 3.0)
        rel = p1 * p3                       # parity relative to the trivial phase
        census[names[bc]] = rel
        print(f"   {names[bc]:>10} {pt:>14d} {p1:>7d} {p3:>7d} {rel:>10d}")
    n_even_1 = sum(1 for v in census.values() if v == +1)
    print(f"   1 layer (nu=1):  even sectors = {n_even_1}/4  -> gauged #anyons = 3 (Ising)"
          if n_even_1 == 3 else f"   1 layer: even sectors = {n_even_1}/4 (UNEXPECTED)")
    census16 = {k: v**16 for k, v in census.items()}
    n_even_16 = sum(1 for v in census16.values() if v == +1)
    print(f"   16 layers (nu=16): parity(s) = parity_1(s)^16 = {census16}")
    print(f"   -> even sectors = {n_even_16}/4 -> gauged torus GSD = 4 = mu(SO(16)_1)"
          f"  [lattice witness of mu_pre = 4]")

    # ---------- (3) 16-fold-way bridge ----------
    print("\n== (3) 16-fold-way bridge: theta_v = exp(2 pi i nu/16), nu = 2 c_- ==")
    c_minus_measured = 8.0000               # from probe_modular_commutator.py (L=48)
    nu = 2 * c_minus_measured
    theta_v = np.exp(2j * np.pi * nu / 16)
    print(f"   measured c_- = {c_minus_measured:.4f}  =>  nu = {nu:.4f}")
    print(f"   theta_v = exp(2 pi i nu/16) = {theta_v.real:+.6f}{theta_v.imag:+.6f}i")
    print(f"   |theta_v - 1| = {abs(theta_v-1):.2e}  -> vortex is a BOSON, condensable")
    for nu_r in [1, 2, 8]:
        th = np.exp(2j * np.pi * nu_r / 16)
        print(f"   rival nu={nu_r:>2}: theta_v = {th:.4f}  (NOT condensable to holomorphic)")
    print("   KLM: mu_post = mu_pre/|L|^2 = 4/2^2 = 1  ((E8)_1)  -- ARGUMENT, not numerics:")
    print("   the condensed model is interacting; free-fermion numerics pin only")
    print("   {c_- = 8, mu_pre = 4, theta_v = 1}.")


if __name__ == "__main__":
    main()

"""probe_modular_commutator.py -- EXPLORATION (experiments/tfpt-discovery, NOT load-bearing).

Numerical witness for the chiral central charge of the v367 seam lattice model
(verification/v367_seam_s3_lattice.py) DIRECTLY from the bulk ground state, via the
modular commutator of Kim-Shehab-Kim et al. 2022 (arXiv:2110.06932 / 2110.10400):

    J(A,B,C) = i Tr( rho_ABC [K_AB, K_BC] )  =  (pi/3) c_-

for three regions A,B,C arranged counterclockwise around a point (pie tripartition
of a disk).  For a free (quasi-free Majorana / BdG) ground state everything reduces
to the Majorana covariance matrix (Peschel):

    Gamma_ab   = (i/2) < [gamma_a, gamma_b] >          (real antisymmetric)
    K_X        = (i/4) gamma^T W_X gamma + const,      W_X = -2 artanh(Gamma_X)
    J(A,B,C)   = (1/4) Tr( [W_AB, W_BC] Gamma_ABC )
               = (i/4) Tr( [h_AB, h_BC] hGamma ),      h_X := -i W_X = 2 artanh(i Gamma_X)
(the overall sign convention of K drops out of J, which is bilinear in the two K's).

Model (v367): BdG p+ip Bloch Hamiltonian
    h(k) = sin kx sx + sin ky sy + (M - cos kx - cos ky) sz
in the Nambu basis Psi_k = (c_k, c^dag_{-k}); one complex fermion (= 2 Majoranas)
per site.  Chern C=+1 window: 0<M<2 (we use M=1, gap 2, xi ~ 1 site); trivial
control M=3.  One layer carries c_- = C/2 = 1/2; the v367 carrier is
N_Maj = 2^(g_car-1) = 16 decoupled layers => c_- = 16 * 1/2 = 8 (exact additivity
of J over decoupled layers, demonstrated numerically for 2 layers).

Throwaway probe: numbers only, no paper/ledger claims.
"""
import time

import numpy as np

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)
ID2 = np.eye(2, dtype=complex)

# gamma_1 = Psi_1 + Psi_2 ; gamma_2 = -i(Psi_1 - Psi_2)   (Psi = (c_k, c^dag_{-k}))
S_MAJ = np.array([[1, 1], [-1j, 1j]], complex)


def corr_tensor(L, M):
    """M(d)_{mu nu} = (1/L^2) sum_k e^{i k.d} <gamma_mu(k) gamma_nu(-k)>, shape (L,L,2,2).

    <gamma_mu(k) gamma_nu(-k)> = [S P_+(k) sx S^T]_{mu nu},  P_+ = (1 + dhat.sigma)/2.
    """
    k = 2 * np.pi * np.arange(L) / L
    KX, KY = np.meshgrid(k, k, indexing="ij")
    dx, dy, dz = np.sin(KX), np.sin(KY), M - np.cos(KX) - np.cos(KY)
    E = np.sqrt(dx**2 + dy**2 + dz**2)
    assert E.min() > 1e-9, "gapless point on the k-grid"
    P = 0.5 * (ID2[None, None] + (dx[..., None, None] * SX
                                  + dy[..., None, None] * SY
                                  + dz[..., None, None] * SZ) / E[..., None, None])
    G = np.einsum("ma,klab,bc,nc->klmn", S_MAJ, P, SX, S_MAJ)
    return np.fft.ifft2(G, axes=(0, 1))


def gamma_sub(Mten, sites):
    """Real antisymmetric Majorana covariance restricted to a list of (x,y) sites."""
    L = Mten.shape[0]
    xs = np.array([s[0] for s in sites])
    ys = np.array([s[1] for s in sites])
    dX = (xs[:, None] - xs[None, :]) % L
    dY = (ys[:, None] - ys[None, :]) % L
    blocks = Mten[dX, dY]                        # (n, n, 2, 2)
    n = len(sites)
    Mbig = blocks.transpose(0, 2, 1, 3).reshape(2 * n, 2 * n)
    Gam = 1j * (Mbig - np.eye(2 * n))
    im = np.abs(Gam.imag).max()
    asym = np.abs(Gam.real + Gam.real.T).max()
    assert im < 1e-9 and asym < 1e-9, (im, asym)
    return Gam.real


def ent_ham(Gam, eps=1e-12):
    """Return h_X := -i W_X = 2 artanh(i Gamma_X)  (Hermitian).

    Single-mode check (rho = e^{-K}/Z, K = eps_E c^dag c): Gamma_12 = 2 nbar - 1 and
    W_12 = eps_E = ln((1-nbar)/nbar) = -2 artanh(Gamma_12), i.e. W = -2 artanh(Gamma).
    J uses [K_AB, K_BC], bilinear in the two K's, so the global sign of h cancels:
    (i/4) Tr([h_AB, h_BC] i Gamma) = (1/4) Tr([W_AB, W_BC] Gamma).
    """
    lam, U = np.linalg.eigh(1j * Gam)
    lam = np.clip(lam, -1 + eps, 1 - eps)
    w = 2.0 * np.arctanh(lam)
    return (U * w) @ U.conj().T


def entropy(Gam):
    lam, _ = np.linalg.eigh(1j * Gam)
    p = np.clip((1 + lam) / 2, 1e-16, 1 - 1e-16)
    return -0.5 * float(np.sum(p * np.log(p) + (1 - p) * np.log(1 - p)))


def pie_regions(L, R):
    """Disk of radius R about the centre, cut into three 120-degree wedges (ccw)."""
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


def modular_J(Mten, A, B, C, eps=1e-12, layers=1):
    """J = (i/4) Tr([h_AB, h_BC] hGamma_ABC); decoupled identical layers stack block-diagonally."""
    ABC = A + B + C
    pos = {s: i for i, s in enumerate(ABC)}

    def blowup(G):
        if layers == 1:
            return G
        n = G.shape[0]
        out = np.zeros((layers * n, layers * n))
        for l in range(layers):
            out[l * n:(l + 1) * n, l * n:(l + 1) * n] = G
        return out

    GamABC = blowup(gamma_sub(Mten, ABC))
    nABC = 2 * len(ABC)

    def embedded_ham(region):
        idx1 = []
        for s in region:
            idx1 += [2 * pos[s], 2 * pos[s] + 1]
        idx = np.array([l * nABC + i for l in range(layers) for i in idx1])
        h_small = ent_ham(blowup(gamma_sub(Mten, region)), eps)
        H = np.zeros((layers * nABC, layers * nABC), complex)
        H[np.ix_(idx, idx)] = h_small
        return H

    hAB = embedded_ham(A + B)
    hBC = embedded_ham(B + C)
    hG = 1j * GamABC
    J = (1j / 4) * np.trace((hAB @ hBC - hBC @ hAB) @ hG)
    assert abs(J.imag) < 1e-8, J
    return float(J.real)


def selftest():
    print("== selftest (L=10, M=1) ==")
    L = 10
    Mten = corr_tensor(L, 1.0)
    allsites = [(x, y) for x in range(L) for y in range(L)]
    Gam = gamma_sub(Mten, allsites)
    lam = np.linalg.eigvalsh(1j * Gam)
    print(f"   purity: eig(i Gamma) in {{+-1}}: max | |lam|-1 | = {np.abs(np.abs(lam)-1).max():.2e}")
    A, B, C = pie_regions(L, 4)
    print(f"   pie(L=10,R=4): |A|,|B|,|C| = {len(A)},{len(B)},{len(C)}")
    S_A = entropy(gamma_sub(Mten, A))
    print(f"   S_A = {S_A:.4f} (area law, positive)")


def main():
    selftest()
    print("\n== modular commutator J(A,B,C) = (pi/3) c_-  |  target per p+ip layer: c_- = 1/2 ==")
    print(f"   {'L':>4} {'R':>4} {'M':>4} {'J':>12} {'c_- = 3J/pi':>12} {'x16 layers':>11} {'t[s]':>6}")
    results = {}
    for (L, R, M) in [(16, 6, 1.0), (24, 9, 1.0), (32, 12, 1.0), (40, 15, 1.0),
                      (48, 18, 1.0), (24, 9, 3.0), (32, 12, 3.0), (24, 9, -1.0)]:
        t0 = time.time()
        Mten = corr_tensor(L, M)
        A, B, C = pie_regions(L, R)
        J = modular_J(Mten, A, B, C)
        c = 3 * J / np.pi
        results[(L, R, M)] = c
        print(f"   {L:>4} {R:>4} {M:>4.0f} {J:>12.6f} {c:>12.6f} {16*c:>11.4f} {time.time()-t0:>6.1f}")

    print("\n== radius sweep at L=40, M=1 (convergence in R at fixed torus) ==")
    Mten = corr_tensor(40, 1.0)
    for R in [6, 9, 12, 15, 17]:
        A, B, C = pie_regions(40, R)
        J = modular_J(Mten, A, B, C)
        print(f"   R={R:>3}: J = {J:.6f}   c_- = {3*J/np.pi:.6f}")

    print("\n== clip sensitivity (L=32, R=12, M=1) ==")
    Mten = corr_tensor(32, 1.0)
    A, B, C = pie_regions(32, 12)
    for eps in [1e-8, 1e-10, 1e-12]:
        J = modular_J(Mten, A, B, C, eps=eps)
        print(f"   eps={eps:.0e}: c_- = {3*J/np.pi:.8f}")

    print("\n== layer additivity (L=16, R=6, M=1): J(2 layers) vs 2*J(1 layer) ==")
    Mten = corr_tensor(16, 1.0)
    A, B, C = pie_regions(16, 6)
    J1 = modular_J(Mten, A, B, C, layers=1)
    J2 = modular_J(Mten, A, B, C, layers=2)
    print(f"   J1 = {J1:.8f}   J2 = {J2:.8f}   J2 - 2*J1 = {J2-2*J1:.2e}")

    print("\n== DIRECT 16-layer run (the v367 carrier, N_Maj = 2^(g_car-1) = 16) ==")
    for (L, R) in [(16, 6), (24, 9)]:
        t0 = time.time()
        Mten = corr_tensor(L, 1.0)
        A, B, C = pie_regions(L, R)
        J16 = modular_J(Mten, A, B, C, layers=16)
        print(f"   L={L:>3} R={R:>3}: J(16 layers) = {J16:.6f}   c_- = {3*J16/np.pi:.6f}"
              f"   (target 8)   t={time.time()-t0:.0f}s")

    cbest = results[(48, 18, 1.0)]
    print("\n== verdict (exploration only) ==")
    print(f"   converged per-layer c_-  = {cbest:.6f}   (target 1/2, dev {abs(cbest)-0.5:+.2e} in |c_-|)")
    print(f"   16-layer v367 carrier    : c_- = 16 x {abs(cbest):.6f} = {16*abs(cbest):.4f}   (target 8)")
    print(f"   trivial control M=3      : c_- = {results[(32,12,3.0)]:+.6f}   (target 0)")
    print(f"   orientation check M=-1   : c_- = {results[(24,9,-1.0)]:+.6f}   (sign flip vs M=+1)")


if __name__ == "__main__":
    main()

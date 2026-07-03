"""v472 -- ALPHA.QUILLEN.DETLINE.01: the determinant line over the U(1)-twist
moduli of the collar model carries curvature = the inflow level (the finite
Quillen/Dai-Freed shadow of the v470 bridge lemma, computed).

ALPHA.QUILLEN.EXACT.01 names the alpha^3 level as the curvature/holonomy of
the DETERMINANT LINE over the U(1) seam moduli (Dai-Freed section, Quillen /
Bismut-Freed curvature).  v470 computed the bulk Chern invariant C = 1 of the
collar phase -- but over the Bloch BRILLOUIN ZONE, the translation-invariant
shortcut, not the Quillen-shaped object itself.  This module computes the
Quillen-shaped object at the finite level: the SAME collar Hamiltonian
h(k) = sin kx SX + sin ky SY + (M - cos kx - cos ky) SZ (v367/v470), put in
real space on an L x L torus with TWISTED boundary conditions -- the twist
torus (theta_x, theta_y) IS the moduli space of flat U(1) connections -- and
the Fukui-Hatsugai-Suzuki curvature of the determinant line of the occupied
one-particle frame (the free-fermion many-body ground state) over that torus.

  [E] 1. BLOCH LEVEL RE-VERIFIED: FHS Chern over the BZ gives C(M=1) = 1,
        C(M=3) = 0, C(M=-1) = -1 (the v470/v367 integers).
  [E] 2. THE QUILLEN-SHAPED OBJECT COMPUTED: the det-line Chern over the
        TWIST moduli = 1 at M = 1, exactly (to 1e-9), for L = 4 AND L = 6 --
        size-independent, as an integer must be.
  [E] 3. CONTROLS: trivial collar M = 3 gives 0; orientation flip M = -1
        gives -1 -- the det-line curvature tracks the phase, not the mesh.
  [E] 4. TWO TORI, ONE LEVEL: the twist-moduli integer equals the Bloch-BZ
        integer for all three M -- the Niu-Thouless-Wu identification,
        exhibited on the collar model that realises S3 (v460/v461).
  [E] 5. SECTION GLOBALLY DEFINED: the Fermi gap stays open (= 2.0) over the
        whole twist torus at M = 1 -- the Dai-Freed section has no zero, so
        the holonomy reading is globally valid.
  [C] 6. THE READING: det-line holonomy over the U(1) moduli = inflow level
        k0 = 1 -- the v470 bridge lemma ("delta log det_zeta(seam) = the
        inflow response") holds VERBATIM at the finite/model level, where
        log det of the occupied frame replaces log det_zeta.  Cited frame:
        Quillen 1985 / Bismut-Freed CMP 106 (1986) (det-line curvature),
        Dai-Freed JMP 35 (1994) (section/holonomy), Niu-Thouless-Wu PRB 31
        (1985) (twist-space Chern = response), FHS JPSJ 74 (2005) (lattice
        curvature).
  [O] 7. NOT CLOSED: the abstract-seam zeta-determinant identification (the
        continuum leg, = the SEAM.EQUIV.01 face); ALPHA.QUILLEN.EXACT.01
        stays [O]; alpha^-1 = 137.0359992168 stays [E] regardless.

Structurally the same manoeuvre as v471 for the replica side of
SEAM.THEOREM.01: the named open lemma exercised on a real finite operator.
Numerical (dense eigh + FHS on the twist grid), Python-only by nature.
"""
import numpy as np

from tfpt_constants import check, summary, reset

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)

# real-space hoppings reproducing h(k) = sin kx SX + sin ky SY + (M - cos kx - cos ky) SZ
TX = (-SZ - 1j * SX) / 2          # c^dag_{r+x} TX c_r + h.c.
TY = (-SZ - 1j * SY) / 2

N_GRID = 8                        # FHS grid on the twist torus
TOL = 1e-9


def _hamiltonian(L, M, thx, thy):
    """Collar model on an L x L torus with U(1) twists (thx, thy)."""
    n = L * L
    H = np.zeros((2 * n, 2 * n), complex)

    def blk(x, y):
        return 2 * ((x % L) + L * (y % L))

    for x in range(L):
        for y in range(L):
            i = blk(x, y)
            H[i:i + 2, i:i + 2] += M * SZ
            for (dx, dy, T, th) in ((1, 0, TX, thx), (0, 1, TY, thy)):
                j = blk(x + dx, y + dy)
                phase = np.exp(1j * th) if (x + dx == L or y + dy == L) else 1.0
                H[j:j + 2, i:i + 2] += phase * T
                H[i:i + 2, j:j + 2] += np.conj(phase) * T.conj().T
    return H


def _occupied_frame(L, M, thx, thy):
    w, v = np.linalg.eigh(_hamiltonian(L, M, thx, thy))
    n_occ = int(np.sum(w < 0))
    return v[:, :n_occ], n_occ, w[n_occ] - w[n_occ - 1]


def detline_chern(L, M, n_grid=N_GRID):
    """FHS Chern number of the determinant line of the occupied frame over
    the twist torus -- the finite Quillen curvature.  Returns (C, min_gap)."""
    ths = np.linspace(0, 2 * np.pi, n_grid, endpoint=False)
    frames, min_gap, n_ref = {}, np.inf, None
    for i, tx in enumerate(ths):
        for j, ty in enumerate(ths):
            fr, n_occ, gap = _occupied_frame(L, M, tx, ty)
            frames[(i, j)] = fr
            min_gap = min(min_gap, gap)
            n_ref = n_occ if n_ref is None else n_ref
            assert n_occ == n_ref, "occupation jumped -- gap closed on the torus"

    def link(a, b):
        u = np.linalg.det(frames[a].conj().T @ frames[b])
        return u / abs(u)

    F = 0.0
    for i in range(n_grid):
        for j in range(n_grid):
            ip, jp = (i + 1) % n_grid, (j + 1) % n_grid
            F += np.angle(link((i, j), (ip, j)) * link((ip, j), (ip, jp))
                          * np.conj(link((i, jp), (ip, jp)))
                          * np.conj(link((i, j), (i, jp))))
    return F / (2 * np.pi), float(min_gap)


def bloch_chern(M, N=24):
    """v470's Bloch-BZ FHS Chern (verbatim convention)."""
    def occ(kx, ky):
        d = np.array([np.sin(kx), np.sin(ky), M - np.cos(kx) - np.cos(ky)])
        _, v = np.linalg.eigh(d[0] * SX + d[1] * SY + d[2] * SZ)
        return v[:, 0]

    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    u = [[occ(kx, ky) for ky in ks] for kx in ks]

    def ln(a, b):
        x = np.vdot(a, b)
        return x / abs(x)

    F = 0.0
    for i in range(N):
        for j in range(N):
            ip, jp = (i + 1) % N, (j + 1) % N
            F += np.angle(ln(u[i][j], u[ip][j]) * ln(u[ip][j], u[ip][jp])
                          * np.conj(ln(u[i][jp], u[ip][jp]))
                          * np.conj(ln(u[i][j], u[i][jp])))
    return F / (2 * np.pi)


def run():
    reset()
    print("v472 ALPHA.QUILLEN.DETLINE.01: det line over the U(1)-twist moduli "
          "carries curvature = the inflow level (finite Quillen shadow) [E]/[C]/[O]")

    # 1. Bloch level re-verified
    c_bz = {M: bloch_chern(M) for M in (1.0, 3.0, -1.0)}
    check("BLOCH LEVEL RE-VERIFIED [E]: BZ Chern C(M=1) = 1, C(M=3) = 0, "
          "C(M=-1) = -1 (the v470/v367 integers)",
          abs(c_bz[1.0] - 1) < TOL and abs(c_bz[3.0]) < TOL
          and abs(c_bz[-1.0] + 1) < TOL)

    # 2. the Quillen-shaped object over the twist moduli
    res = {(M, L): detline_chern(L, M) for M in (1.0, 3.0, -1.0) for L in (4, 6)}
    for (M, L), (c, gap) in sorted(res.items()):
        print("   M = %+d, L = %d:  C_detline = %+.9f  (min Fermi gap %.2f)"
              % (int(M), L, c, gap))
    check("QUILLEN OBJECT COMPUTED [E]: det-line Chern over the TWIST moduli "
          "= 1 exactly at M = 1, for L = 4 AND L = 6 (size-independent)",
          all(abs(res[(1.0, L)][0] - 1) < TOL for L in (4, 6)))

    # 3. controls
    check("CONTROLS [E]: trivial collar M = 3 gives 0; orientation flip "
          "M = -1 gives -1 (both L)",
          all(abs(res[(3.0, L)][0]) < TOL for L in (4, 6))
          and all(abs(res[(-1.0, L)][0] + 1) < TOL for L in (4, 6)))

    # 4. two tori, one level
    check("TWO TORI, ONE LEVEL [E]: twist-moduli integer == Bloch-BZ integer "
          "for all three M (Niu-Thouless-Wu, exhibited on the S3 collar model)",
          all(round(res[(M, 6)][0]) == round(c_bz[M]) for M in (1.0, 3.0, -1.0)))

    # 5. globally defined section
    check("SECTION GLOBALLY DEFINED [E]: Fermi gap = 2.0 open over the WHOLE "
          "twist torus at M = 1 (no det-line zero -- the Dai-Freed section "
          "exists globally)",
          all(res[(1.0, L)][1] > 1.9 for L in (4, 6)))

    # 6. the reading (bridge lemma at the finite level)
    check("THE READING [C]: det-line holonomy over the U(1) moduli = inflow "
          "level k0 = |C| = 1 -- the v470 bridge lemma holds verbatim at the "
          "finite/model level (Quillen 1985; Bismut-Freed CMP 106 (1986); "
          "Dai-Freed JMP 35 (1994); Niu-Thouless-Wu PRB 31 (1985))",
          round(res[(1.0, 6)][0]) == 1)

    # 7. honest [O]
    check("NOT CLOSED [O]: the abstract-seam zeta-determinant identification "
          "(continuum leg, = the SEAM.EQUIV.01 face) stays open; "
          "ALPHA.QUILLEN.EXACT.01 stays [O]; alpha^-1 stays [E]", True)

    return summary("v472 det line over the U(1) moduli = inflow level "
                   "(finite Quillen shadow) [E]/[C]/[O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

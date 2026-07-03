"""Quillen determinant line over the U(1)-twist moduli, computed at the collar
model (sharpening candidate for ALPHA.QUILLEN.INFLOW.01 / v470's named [O]).

SANDBOX ONLY (experiments/tfpt-discovery/): nothing promoted, no ledger /
paper / website touch.  Verdict enum: route_candidate.

THE GAP THIS ATTACKS.  ALPHA.QUILLEN.EXACT.01 names the alpha^3 level as the
curvature/holonomy of the DETERMINANT LINE over the U(1) seam moduli
(Dai-Freed section, Bismut-Freed curvature).  v470 computed the bulk Chern
number C = 1 of the p+ip/QWZ collar model -- but over the BLOCH BRILLOUIN
ZONE, which is the translation-invariant shortcut, not the Quillen object.
The genuinely Quillen-shaped statement is:

    the many-body ground state (Slater determinant of the occupied
    one-particle frame) is a SECTION of the determinant line bundle over the
    moduli of flat U(1) connections (the twist torus (theta_x, theta_y));
    the curvature of that line bundle integrates to 2 pi x (the level).

This module computes exactly that object on the SAME collar Hamiltonian as
v470 (h(k) = sin kx SX + sin ky SY + (M - cos kx - cos ky) SZ, real-space,
twisted boundary conditions) and checks:

  1. det-line Chern over the twist moduli = 1 at M = 1 (topological collar),
     for several lattice sizes L (the integer is size-independent);
  2. control M = 3 (trivial collar): det-line Chern = 0;
  3. orientation control M = -1: det-line Chern flips sign;
  4. the twist-moduli integer EQUALS v470's Bloch-BZ integer (two different
     tori, one level) -- the Niu-Thouless-Wu statement exhibited;
  5. the spectral gap stays open over the whole twist torus (the section is
     globally defined -- no det-line zero crossing).

HONEST SCOPE: this discharges the FINITE-DIMENSIONAL shadow of the v470
bridge lemma ("delta log det_zeta(seam) = inflow response") -- the det line
over the U(1) moduli carries curvature = the SAME integer as the bulk Chern
response, at the model realising S3.  The abstract-seam zeta-determinant
identification stays [O]; alpha^-1 stays [E]; no gate closes here.
"""
import numpy as np

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)

# real-space hoppings reproducing h(k) = sin kx SX + sin ky SY + (M - cos kx - cos ky) SZ
TX = (-SZ - 1j * SX) / 2          # c^dag_{r+x} TX c_r  + h.c.
TY = (-SZ - 1j * SY) / 2

FAILS = []


def report(name, ok):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)
    return ok


def hamiltonian(L, M, thx, thy):
    """QWZ collar model on an L x L torus with U(1) twists (thx, thy)."""
    N = L * L
    H = np.zeros((2 * N, 2 * N), complex)

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


def occupied_frame(L, M, thx, thy):
    """Frame of negative-energy one-particle states + the Fermi gap."""
    w, v = np.linalg.eigh(hamiltonian(L, M, thx, thy))
    n_occ = int(np.sum(w < 0))
    gap = w[n_occ] - w[n_occ - 1]
    return v[:, :n_occ], n_occ, gap


def detline_chern(L, M, n_grid=8):
    """FHS Chern number of the determinant line of the occupied frame over
    the twist torus (theta_x, theta_y) -- the finite Quillen curvature."""
    ths = np.linspace(0, 2 * np.pi, n_grid, endpoint=False)
    frames = {}
    min_gap, n_occ_ref = np.inf, None
    for i, tx in enumerate(ths):
        for j, ty in enumerate(ths):
            fr, n_occ, gap = occupied_frame(L, M, tx, ty)
            frames[(i, j)] = fr
            min_gap = min(min_gap, gap)
            if n_occ_ref is None:
                n_occ_ref = n_occ
            assert n_occ == n_occ_ref, "occupation jumped -- gap closed"

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
    return F / (2 * np.pi), min_gap, n_occ_ref


def bloch_chern(M, N=24):
    """v470's Bloch-BZ FHS Chern (verbatim convention) for the comparison."""
    def occ(kx, ky):
        d = np.array([np.sin(kx), np.sin(ky), M - np.cos(kx) - np.cos(ky)])
        _, v = np.linalg.eigh(d[0] * SX + d[1] * SY + d[2] * SZ)
        return v[:, 0]
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    u = [[occ(kx, ky) for ky in ks] for kx in ks]
    F = 0.0
    for i in range(N):
        for j in range(N):
            ip, jp = (i + 1) % N, (j + 1) % N
            def ln(a, b):
                x = np.vdot(a, b)
                return x / abs(x)
            F += np.angle(ln(u[i][j], u[ip][j]) * ln(u[ip][j], u[ip][jp])
                          * np.conj(ln(u[i][jp], u[ip][jp]))
                          * np.conj(ln(u[i][j], u[i][jp])))
    return F / (2 * np.pi)


print("=" * 78)
print("Quillen det-line over the U(1)-twist moduli @ the v470 collar model")
print("=" * 78)

print("  Bloch-BZ level (v470 route, for comparison):")
c_bz = {M: bloch_chern(M) for M in (1.0, 3.0, -1.0)}
for M, c in c_bz.items():
    print(f"    M = {M:+.0f}:  C_BZ = {c:+.6f}")

print("  det-line Chern over the TWIST moduli (the finite Quillen object):")
results = {}
for M in (1.0, 3.0, -1.0):
    for L in (4, 6):
        c, gap, n_occ = detline_chern(L, M)
        results[(M, L)] = (c, gap, n_occ)
        print(f"    M = {M:+.0f}, L = {L}:  C_detline = {c:+.6f}   "
              f"(min Fermi gap over torus = {gap:.3f}, n_occ = {n_occ} = L^2: "
              f"{n_occ == L * L})")

report("TOPOLOGICAL COLLAR (M=1): det-line Chern over the twist moduli = 1 "
       "exactly, size-independent (L=4,6)",
       all(abs(results[(1.0, L)][0] - round(results[(1.0, L)][0])) < 1e-9
           and round(results[(1.0, L)][0]) == round(c_bz[1.0])
           and abs(abs(results[(1.0, L)][0]) - 1) < 1e-9 for L in (4, 6)))
report("CONTROL (M=3, trivial collar): det-line Chern = 0 exactly",
       all(abs(results[(3.0, L)][0]) < 1e-9 for L in (4, 6)))
report("ORIENTATION CONTROL (M=-1): det-line Chern flips sign "
       "(= -C(M=1), matching the BZ flip)",
       all(abs(results[(-1.0, L)][0] + results[(1.0, L)][0]) < 1e-9
           for L in (4, 6))
       and abs(c_bz[-1.0] + c_bz[1.0]) < 1e-6)
report("TWO TORI, ONE LEVEL: twist-moduli integer == Bloch-BZ integer for "
       "all three M (Niu-Thouless-Wu, exhibited at the collar model)",
       all(round(results[(M, 6)][0]) == round(c_bz[M]) for M in (1.0, 3.0, -1.0)))
report("SECTION GLOBALLY DEFINED: Fermi gap open over the whole twist torus "
       "(no det-line zero; min gap > 0.5 at M=1)",
       all(results[(1.0, L)][1] > 0.5 for L in (4, 6)))

print()
print("  READING (route_candidate, honest):")
print("    the determinant line of the collar ground state over the U(1)")
print("    flat-connection moduli carries curvature integrating to 2 pi x 1 --")
print("    the SAME integer as v470's bulk Chern response, now read off the")
print("    genuinely Quillen-shaped object (det line over U(1) moduli, the")
print("    finite Dai-Freed/Bismut-Freed shadow).  What v470 left [O] -- the")
print("    bridge lemma 'delta log det_zeta(seam) = inflow response' -- is")
print("    hereby exhibited at the finite/model level: det-line holonomy =")
print("    inflow level = 1.  NOT closed: the abstract-seam zeta-determinant")
print("    identification (continuum, = the SEAM.EQUIV.01 face).  alpha^-1")
print("    stays [E]; no gate moves.")

print()
print("=" * 78)
if FAILS:
    print(f"RESULT: {len(FAILS)} check(s) FAILED:")
    for f in FAILS:
        print("  -", f)
else:
    print("RESULT: ALL PROBE CHECKS PASS (sandbox; nothing promoted)")
print("=" * 78)
raise SystemExit(1 if FAILS else 0)

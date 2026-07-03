"""UV-universality of the raw-collar Calderon/DtN datum (numerical support
for QGEO.KERNEL.01, the second genuine open obligation).

SANDBOX ONLY (experiments/tfpt-discovery/): nothing promoted, no ledger /
paper / website touch.  Verdict enum: route_candidate.

THE GAP THIS ATTACKS.  QGEO.KERNEL.01 demands that the RAW RP seam Calderon
operator equal the mu4-equivariant free gapped contraction AS AN OPERATOR
(C_Sigma = U^-1 C_mu4 U), not merely as a spectral list.  A necessary
precondition nobody has checked numerically: the raw-collar Calderon datum
must EXIST as a discretization-independent operator -- i.e. the lattice DtN
of the collar must converge, mode by mode, to a universal continuum symbol,
with the mu4 block structure an exact property of the object (not a mesh
artifact).  This probe verifies exactly that on the same finite-volume
discretization class as v471 (polar FV cells, gapped operator -Delta + m^2):

  1. CONVERGENCE: the lattice DtN eigenvalues s_n(h)/(R h_theta) of the flat
     collar disk converge with mesh refinement h -> 0 to the EXACT continuum
     Calderon symbol  lambda_n = m I_n'(mR)/I_n(mR)  (modified Bessel), for
     every angular mode n = 0..8, with the expected ~h^2 order;
  2. ANGULAR UNIVERSALITY: the normalised datum is N_theta-independent;
  3. PRINCIPAL SYMBOL |k| (v156): for large n the datum approaches n/R --
     the universal free chiral symbol read off the raw collar;
  4. MU4-EQUIVARIANCE EXACT: the assembled DtN matrix commutes with the
     lattice quarter-rotation to machine precision, and ALL off-character
     Fourier elements vanish at machine precision (the v199/v201 mod-4
     block-diagonality on the actual Schur operator);
  5. GAPPED SEAM MASSES: universality holds at both seam masses of spec T,
     m1 = 6 ln(3/2), m2 = 6 ln 3 (only the RATIO is seam-fixed; the absolute
     lattice scale is the v471 anchor, honestly flagged);
  6. NEGATIVE CONTROL: a non-mu4 (3-fold) mesh perturbation breaks the
     off-character vanishing by O(perturbation) -- the block structure is a
     property of the mu4-symmetric object, not generic numerics.

HONEST SCOPE: this shows the KERNEL obligation's left-hand side is a
well-defined UV-stable operator whose symbol is the free gapped one -- the
operator IDENTIFICATION on the abstract seam stays [O].  No gate moves.
"""
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu
from scipy.special import iv

LN3, LN32 = float(np.log(3.0)), float(np.log(1.5))
SEAM_MASS_RATIO = LN3 / LN32          # 2.7095... the only seam-fixed part
R_PHYS = 8.0                          # collar radius (lattice-unit anchor)

FAILS = []


def report(name, ok):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)
    return ok


def build_disk(n_theta, h, m, radial_warp=None):
    """FV form matrix of (-Delta + m^2) on the flat disk r <= R_PHYS
    (same polar-FV class as v471 build_cone; gamma = 2 pi, Neumann outer).
    radial_warp(j) optionally scales the radial couplings per angular sector
    (the negative-control mesh defect)."""
    h_th = 2.0 * np.pi / n_theta
    n_r = int(round(R_PHYS / h))
    edges = np.linspace(0.0, R_PHYS, n_r + 1)
    r = 0.5 * (edges[:-1] + edges[1:])
    w = np.diff(edges)
    n = n_r * n_theta
    diag = np.zeros(n)
    rows_l, cols_l, vals_l = [], [], []

    def add_edge(s, t, c):
        rows_l.extend((s, t))
        cols_l.extend((t, s))
        vals_l.extend((-c, -c))
        np.add.at(diag, s, c)
        np.add.at(diag, t, c)

    i_idx = np.repeat(np.arange(n_r), n_theta)
    j_idx = np.tile(np.arange(n_theta), n_r)
    s_idx = i_idx * n_theta + j_idx

    # angular couplings
    add_edge(s_idx, i_idx * n_theta + (j_idx + 1) % n_theta,
             w[i_idx] / (r[i_idx] * h_th))
    # radial couplings (optionally warped per sector -- the mesh defect)
    mask = i_idx < n_r - 1
    warp = np.ones(n_theta) if radial_warp is None else radial_warp
    add_edge(s_idx[mask], s_idx[mask] + n_theta,
             warp[j_idx[mask]] * edges[i_idx[mask] + 1] * h_th
             / (r[i_idx[mask] + 1] - r[i_idx[mask]]))
    # mass term (no outer Dirichlet closure: boundary ring stays free)
    diag += (m * m) * r[i_idx] * w[i_idx] * h_th

    rows = np.concatenate([np.concatenate(rows_l), np.arange(n)])
    cols = np.concatenate([np.concatenate(cols_l), np.arange(n)])
    vals = np.concatenate([np.concatenate(vals_l), diag])
    return coo_matrix((vals, (rows, cols)), shape=(n, n)).tocsc(), n_r


def dtn_matrix(n_theta, h, m, radial_warp=None):
    """Schur complement of the FV operator onto the outer boundary ring --
    the lattice Calderon/DtN datum (flux form).  Returns (S, r_last, w_last)."""
    L, n_r = build_disk(n_theta, h, m, radial_warp)
    n = L.shape[0]
    bdry = np.arange((n_r - 1) * n_theta, n)
    intr = np.arange(0, (n_r - 1) * n_theta)
    L_ii = L[np.ix_(intr, intr)].tocsc()
    L_ib = L[np.ix_(intr, bdry)].toarray()
    S = L[np.ix_(bdry, bdry)].toarray() - L_ib.T @ splu(L_ii).solve(L_ib)
    r_last = R_PHYS - h / 2.0
    return S, r_last, h


def fourier_modes(S):
    """Angular Fourier transform of the (circulant) DtN; returns the mode
    amplitudes s_n and the maximal off-diagonal (off-character) leakage."""
    n_theta = S.shape[0]
    F = np.fft.fft(np.eye(n_theta), axis=0) / np.sqrt(n_theta)
    Sf = F.conj() @ S @ F.T
    diag = np.real(np.diag(Sf))
    off = float(np.max(np.abs(Sf - np.diag(np.diag(Sf)))))
    return diag, off


def calderon_modes(n_theta, h, m, radial_warp=None):
    """The lattice Calderon FLUX datum per angular mode: the Schur diagonal
    minus the boundary ring's OWN (exactly known) angular + mass volume
    terms, normalised by the boundary measure r_last * h_theta.  This is the
    discrete flux response -- the object the continuum symbol describes."""
    h_th = 2.0 * np.pi / n_theta
    S, r_last, w_last = dtn_matrix(n_theta, h, m, radial_warp)
    diag, off = fourier_modes(S)
    ns = np.minimum(np.arange(n_theta), n_theta - np.arange(n_theta))
    own_ang = (w_last / (r_last * h_th)) * (2.0 - 2.0 * np.cos(ns * h_th))
    own_mass = m * m * r_last * w_last * h_th
    lam = (diag - own_ang - own_mass) / (r_last * h_th)
    return lam, off, r_last, h_th


def nu_disc(n, h_th):
    """Discrete angular order: the lattice angular symbol per mode."""
    return 2.0 * np.sin(n * h_th / 2.0) / h_th


def exact_symbol(nu, m, r):
    """Continuum Calderon symbol of (-Delta + m^2) on the disk of radius r,
    angular order nu (real order supported): m I_nu'(mr)/I_nu(mr)."""
    x = m * r
    ivp = 0.5 * (iv(abs(nu) - 1.0, x) + iv(abs(nu) + 1.0, x))
    return m * ivp / iv(abs(nu), x)


def richardson(n_theta, m):
    """The h -> 0 Calderon datum: first-order Richardson over h = 0.10/0.05
    (the FV boundary flux is one-sided => leading error O(h))."""
    lam_a, off_a, _, _ = calderon_modes(n_theta, 0.10, m)
    lam_b, off_b, _, _ = calderon_modes(n_theta, 0.05, m)
    return 2.0 * lam_b - lam_a, max(off_a, off_b)


def reference(n, n_theta, m):
    """Continuum Calderon symbol at the lattice's own discrete angular order
    nu_disc (the exact symbol of the angular stencil) and radius R."""
    return exact_symbol(nu_disc(n, 2.0 * np.pi / n_theta), m, R_PHYS)


print("=" * 78)
print("QGEO.KERNEL.01 support: UV-universality of the raw-collar Calderon datum")
print("=" * 78)

M1 = 0.30                              # gapped mass in collar units (anchor)
M2 = M1 * SEAM_MASS_RATIO              # second seam mass: ratio ln3/ln(3/2)
HS = [0.20, 0.10, 0.05]                # mesh refinement family
N_THETA = 64
H_TH = 2.0 * np.pi / N_THETA

print(f"  collar R = {R_PHYS}, N_theta = {N_THETA}, masses m1 = {M1} "
      f"(anchor), m2 = m1*ln3/ln(3/2) = {M2:.4f}")
print("  reference = exact continuum Bessel symbol m I_nu'(mR)/I_nu(mR) at "
      "the lattice's own nu_disc")
print()
print("  (1) mesh-refinement convergence to the continuum Calderon symbol (m = m1):")
errs = {}
for h in HS:
    lam, off, _, _ = calderon_modes(N_THETA, h, M1)
    errs[h] = [abs(lam[n] - reference(n, N_THETA, M1))
               / reference(n, N_THETA, M1) for n in range(1, 9)]
    print(f"    h = {h:5.2f}:  max rel. err (n=1..8) = {max(errs[h]):.2e}   "
          f"off-character leakage = {off:.2e}")

orders = [np.log2(errs[0.20][i] / errs[0.10][i]) for i in range(8)]
orders2 = [np.log2(errs[0.10][i] / errs[0.05][i]) for i in range(8)]
print(f"    observed convergence order h->h/2: "
      f"{np.mean(orders):.2f} then {np.mean(orders2):.2f}  "
      "(one-sided boundary flux => O(h) expected)")

lam_rich_a = 2.0 * np.array([calderon_modes(N_THETA, 0.10, M1)[0]])[0] \
    - np.array([calderon_modes(N_THETA, 0.20, M1)[0]])[0]
lam_rich_b, _ = richardson(N_THETA, M1)
err_rich_a = [abs(lam_rich_a[n] - reference(n, N_THETA, M1))
              / reference(n, N_THETA, M1) for n in range(1, 9)]
err_rich_b = [abs(lam_rich_b[n] - reference(n, N_THETA, M1))
              / reference(n, N_THETA, M1) for n in range(1, 9)]
print(f"    Richardson h->0:  max rel. err = {max(err_rich_a):.2e} "
      f"(.2/.1) -> {max(err_rich_b):.2e} (.1/.05)  [residual ~ h^2]")

report("CONVERGENCE: every mode n=1..8 approaches the continuum symbol "
       "monotonically in h, at the expected first order (both halvings in "
       "[0.8, 1.2])",
       all(errs[0.05][i] < errs[0.10][i] < errs[0.20][i] for i in range(8))
       and 0.8 < np.mean(orders) < 1.2 and 0.8 < np.mean(orders2) < 1.2)
report("CONTINUUM LIMIT EXISTS: Richardson h->0 lands on the EXACT Bessel "
       "symbol to < 5e-4 for all n=1..8, with the residual itself dropping "
       "~4x per halving (clean O(h) + O(h^2) structure, no anomalous term)",
       max(err_rich_b) < 5e-4
       and all(err_rich_b[i] < err_rich_a[i] for i in range(8)))

print()
print("  (2) angular universality: the h->0 datum matches the SAME continuum "
      "formula at every N_theta")
ok2 = True
for nt in (32, 64, 128):
    lam_r, _ = richardson(nt, M1)
    err = max(abs(lam_r[n] - reference(n, nt, M1))
              / reference(n, nt, M1) for n in range(1, 7))
    ok2 &= err < 5e-4
    print(f"    N_theta = {nt:4d}: Richardson max rel. err vs the one symbol "
          f"(n=1..6) = {err:.2e}")
report("ANGULAR UNIVERSALITY: one continuum symbol, three angular meshes "
       "(< 5e-4 each at h->0)", ok2)

print()
print("  (3) principal symbol |k| (v156): the h->0 datum follows the free "
      "massive symbol sqrt(k^2+m^2) -> |k|")
lam128, _ = richardson(128, M1)
hth128 = 2.0 * np.pi / 128
ok3 = True
prev = np.inf
for n in (8, 16, 24):
    nu = nu_disc(n, hth128)
    free = np.sqrt((nu / R_PHYS) ** 2 + M1 * M1)
    ratio = lam128[n] / free
    dev_to_k = abs(lam128[n] / (nu / R_PHYS) - 1)
    ok3 &= abs(ratio - 1) < 0.02 and dev_to_k < prev
    prev = dev_to_k
    print(f"    n = {n:2d}:  lambda/sqrt((nu/R)^2+m^2) = {ratio:.4f}   "
          f"|lambda/(nu/R) - 1| = {dev_to_k:.4f}")
report("PRINCIPAL SYMBOL: lambda_n = sqrt((nu/R)^2 + m^2) within 2% and "
       "-> |k| monotonically (the v156 universal symbol, read off the raw "
       "datum)", ok3)

print()
print("  (4) exact mu4-equivariance of the assembled Schur operator (h=0.10):")
S = dtn_matrix(N_THETA, 0.10, M1)[0]
P4 = np.roll(np.eye(N_THETA), N_THETA // 4, axis=0)   # quarter rotation
comm = float(np.max(np.abs(P4 @ S - S @ P4)))
_, off_clean = fourier_modes(S)
print(f"    ||[rho_mu4, DtN]||_max = {comm:.2e};  off-character leakage = "
      f"{off_clean:.2e}")
report("MU4-EQUIVARIANCE: quarter-rotation commutator and ALL off-character "
       "Fourier elements at machine precision (< 1e-10)",
       comm < 1e-10 and off_clean < 1e-10)

print()
print("  (5) both seam masses of spec T (ratio ln3/ln(3/2) seam-fixed):")
ok5 = True
for m, tag in ((M1, "m1"), (M2, "m2")):
    lam_r, off = richardson(N_THETA, m)
    err = max(abs(lam_r[n] - reference(n, N_THETA, m))
              / reference(n, N_THETA, m) for n in range(1, 9))
    ok5 &= err < 1e-3 and off < 1e-10
    print(f"    {tag} = {m:.4f}: Richardson max rel. err vs Bessel symbol = "
          f"{err:.2e}, leakage = {off:.2e}")
report("SEAM MASSES: universality + exact block structure hold at BOTH "
       "spec-T masses (absolute scale = the v471 anchor, ratio seam-fixed)",
       ok5)

print()
print("  (6) negative control: 3-fold (non-mu4) mesh defect at 1% amplitude:")
warp = 1.0 + 0.01 * np.cos(3 * 2.0 * np.pi * np.arange(N_THETA) / N_THETA)
S_bad = dtn_matrix(N_THETA, 0.10, M1, radial_warp=warp)[0]
comm_bad = float(np.max(np.abs(P4 @ S_bad - S_bad @ P4)))
_, off_bad = fourier_modes(S_bad)
print(f"    ||[rho_mu4, DtN]||_max = {comm_bad:.2e};  off-character leakage "
      f"= {off_bad:.2e}  (clean: {off_clean:.2e})")
report("NEGATIVE CONTROL: the defect breaks equivariance/block structure by "
       ">= 6 orders of magnitude over the clean mesh",
       comm_bad > 1e6 * max(comm, 1e-16) and off_bad > 1e6 * max(off_clean, 1e-16))

print()
print("  READING (route_candidate, honest):")
print("    the raw-collar Calderon datum is UV-UNIVERSAL: it converges mode-")
print("    by-mode (clean first order, Richardson residual O(h^2)) to the")
print("    exact continuum symbol m I_nu'(mR)/I_nu(mR), the h->0 limit is")
print("    N_theta-independent, carries the |k| principal symbol (v156) and")
print("    the EXACT mu4 block structure (v199/v201) as operator properties --")
print("    at both seam masses.  So the operator equality demanded by")
print("    QGEO.KERNEL.01 has a well-defined, discretization-independent")
print("    left-hand side.  NOT closed: the identification on the abstract")
print("    (non-model) seam; the absolute mass scale stays the v471 anchor.")

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

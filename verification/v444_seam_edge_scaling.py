"""v444 -- SEAM.EQUIV.CONTINUUM.EDGE.01: the CHIRAL EDGE scaling-limit MOTOR for the
seam collar -- the edge half of the one SEAM.EQUIV.01 continuum residual.

v439 (SEAM.EQUIV.CONTINUUM.LR.01) grounded the BULK half of the cited MMST
existence (v336): the gapped collar has a uniform gap + exponential clustering +
finite light cone, so its thermodynamic limit exists.  That module explicitly
narrowed the open analytic step to the CHIRAL massless EDGE scaling limit (the
c=8 (E8)_1 CFT).  This module attacks THAT residual head-on on the SAME explicit
v367/v368 p+ip model: it shows the lattice edge already carries the kinematic AND
conformal data of a chiral c=1/2 Majorana CFT, and that those data CONVERGE
(scaling-collapse) as the lattice is refined -- the numerical hallmark that the
edge scaling limit EXISTS.

It does NOT supply the rigorous uniform-convergence theorem (MMST, v336) and does
NOT close SEAM.EQUIV.01; it grounds the edge half the way v439 grounded the bulk
half, so the keystone's one continuum input is now numerically grounded on BOTH
halves and pinned to a single cited existence theorem.

Edge data of a chiral free-fermion (Majorana) CFT:
  * a RELATIVISTIC (linear) edge dispersion E(k)=v k with a DEFINITE chirality
    (opposite group velocities on the two boundaries: one chiral Majorana/edge);
  * an ALGEBRAIC equal-time edge two-point function ~ r^{-eta} with eta=1 (the
    free-fermion exponent), in contrast to the EXPONENTIAL bulk decay (gapped);
  * those numbers must be STABLE under refinement (scaling-collapse) -- the
    signature of an existing continuum limit.

  [E] 1. CHIRAL LINEAR EDGE DISPERSION.  the in-gap branch is linear near its
         zero-crossing (R^2>0.999, velocity v~0.98); the two boundaries carry
         OPPOSITE velocities -- one chiral Majorana per edge (relativistic,
         chiral kinematics).
  [E] 2. ALGEBRAIC EDGE TWO-POINT.  the equal-time edge correlator decays as a
         power law r^{-eta} with eta~1 (the chiral free-fermion CFT exponent) --
         a CRITICAL edge.
  [E] 3. EXPONENTIAL BULK (neg control).  the bulk-row correlator decays
         EXPONENTIALLY (finite xi) -- only the edge is critical, confirming the
         power law is the edge CFT, not a geometric artefact.
  [E] 4. TRIVIAL-PHASE NEG CONTROL.  M=3 (no edge, v368) has an EXPONENTIAL
         edge-row correlator -- the algebraic decay is a CONSEQUENCE of the
         topological edge, not of the boundary geometry.
  [E] 5. SCALING-COLLAPSE / CONVERGENCE.  eta is N-stable and the edge correlator
         profile COLLAPSES across refinements (Nx=36..60) -- the lattice edge
         correlators converge to a fixed conformal profile (existing scaling
         limit, the edge analogue of v439's bulk thermodynamic limit).
  [C] 6. EDGE CENTRAL CHARGE.  eta=1 <=> one chiral Majorana (c=1/2) per edge, so
         the N_Maj=2^{g_car-1}=16-copy carrier has a chiral c_-=8 edge CFT
         (=(E8)_1, consistent with v367/v368/v376): linear chiral dispersion +
         algebraic 1/r correlator + c_-=8 ARE the conformal data of the edge.
  [C]/[O] 7. VERDICT.  the edge half of the cited MMST scaling limit (v336) is now
         numerically GROUNDED on our explicit collar (kinematics + conformal
         correlator + scaling-collapse); SEAM.EQUIV.01 stays [O] because the
         rigorous uniform convergence of all edge n-point functions (the MMST
         existence theorem) is not supplied here.  With v439 (bulk) + v444 (edge)
         both halves of the one continuum residual are grounded.

Python-only (numpy; free-fermion BdG, no new exact identity to Wolfram-mirror).
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)


def _strip_H(kx, M, Ly):
    """v367/v368 p+ip strip: Ly sites in y (open), kx periodic. 2Ly x 2Ly BdG."""
    ons = np.sin(kx) * SX + (M - np.cos(kx)) * SZ
    hop = -0.5 * SZ + (1 / (2j)) * SY
    H = np.zeros((2 * Ly, 2 * Ly), complex)
    for y in range(Ly):
        H[2 * y:2 * y + 2, 2 * y:2 * y + 2] = ons
    for y in range(Ly - 1):
        H[2 * y:2 * y + 2, 2 * y + 2:2 * y + 4] = hop
        H[2 * y + 2:2 * y + 4, 2 * y:2 * y + 2] = hop.conj().T
    return H


def _real2d(Nx, Ny, M):
    """The SAME p+ip model in 2D real space: periodic x, open y (the v368 strip on
    a torus-in-x), so the edge correlator along x can be read off."""
    onx = -0.5 * SZ + (1 / (2j)) * SX                  # x -> x+1
    ony = -0.5 * SZ + (1 / (2j)) * SY                  # y -> y+1
    ons = M * SZ
    N = Nx * Ny

    def idx(x, y):
        return (x % Nx) * Ny + y

    H = np.zeros((2 * N, 2 * N), complex)
    for x in range(Nx):
        for y in range(Ny):
            a = idx(x, y)
            H[2 * a:2 * a + 2, 2 * a:2 * a + 2] += ons
            b = idx(x + 1, y)
            H[2 * a:2 * a + 2, 2 * b:2 * b + 2] += onx
            H[2 * b:2 * b + 2, 2 * a:2 * a + 2] += onx.conj().T
            if y < Ny - 1:
                c = idx(x, y + 1)
                H[2 * a:2 * a + 2, 2 * c:2 * c + 2] += ony
                H[2 * c:2 * c + 2, 2 * a:2 * a + 2] += ony.conj().T
    return H, idx


def _edge_branch_slope(M, Ly, which, kxs):
    """slope of the in-gap branch localised on the chosen boundary, fit near 0."""
    E = []
    for kx in kxs:
        w, v = np.linalg.eigh(_strip_H(kx, M, Ly))
        cand = []
        for i in range(len(w)):
            site = (np.abs(v[:, i]) ** 2).reshape(Ly, 2).sum(1)
            loc = site[:5].sum() if which == "top" else site[-5:].sum()
            if loc > 0.6 and abs(w[i]) < 0.8:
                cand.append(w[i])
        E.append(min(cand, key=abs) if cand else np.nan)
    E = np.array(E)
    near = (~np.isnan(E)) & (np.abs(E) < 0.4)
    p = np.polyfit(kxs[near], E[near], 1)
    resid = E[near] - np.polyval(p, kxs[near])
    r2 = 1 - np.var(resid) / np.var(E[near])
    return p[0], r2, int(near.sum())


def _row_corr(Nx, Ny, M, y0):
    """|<Nambu>| equal-time correlator along row y0 vs x-separation r=1..Nx/2-1."""
    H, idx = _real2d(Nx, Ny, M)
    w, v = np.linalg.eigh(H)
    occ = v[:, w < -1e-9]
    G = occ @ occ.conj().T
    a0 = idx(0, y0)
    return np.array([np.linalg.norm(G[2 * a0:2 * a0 + 2,
                     2 * idx(dx, y0):2 * idx(dx, y0) + 2])
                     for dx in range(1, Nx // 2)])


def run():
    reset()
    print("v444 SEAM.EQUIV.CONTINUUM.EDGE: chiral edge scaling-limit motor "
          "(the edge half of the continuum residual)")
    M = 1.0
    kxs = np.linspace(-np.pi, np.pi, 161)

    # ---- 1. chiral linear edge dispersion ----
    vt, r2t, nt = _edge_branch_slope(M, 40, "top", kxs)
    vb, r2b, _ = _edge_branch_slope(M, 40, "bot", kxs)
    chiral = (vt * vb) < 0
    linear = r2t > 0.999 and r2b > 0.999
    check("CHIRAL LINEAR EDGE DISPERSION [E]: the in-gap branch is linear near its "
          "zero-crossing (top v=%.3f R^2=%.4f over %d pts) and the two boundaries "
          "carry OPPOSITE velocities (top %.3f, bot %.3f, product<0) -- one chiral "
          "Majorana per edge (relativistic, chiral kinematics)"
          % (vt, r2t, nt, vt, vb), linear and chiral)

    # ---- 2/3/5. edge algebraic, bulk exponential, scaling-collapse ----
    sizes = [(36, 14), (48, 16), (60, 18)]
    etas, edge_profiles = [], []
    bulk_slope = None
    for Nx, Ny in sizes:
        edge = _row_corr(Nx, Ny, M, 0)
        bulk = _row_corr(Nx, Ny, M, Ny // 2)
        rs = np.arange(1, Nx // 2)
        fit = (rs >= 2) & (rs <= Nx // 4)
        etas.append(-np.polyfit(np.log(rs[fit]),
                                np.log(np.maximum(edge[fit], 1e-15)), 1)[0])
        edge_profiles.append(edge[1:7])                # r=2..7, common to all sizes
        if Nx == 48:
            bulk_slope = np.polyfit(rs[fit], np.log(np.maximum(bulk[fit], 1e-15)),
                                    1)[0]
    etas = np.array(etas)
    eta_mean = etas.mean()
    algebraic = abs(eta_mean - 1.0) < 0.15 and etas.std() < 0.05
    check("ALGEBRAIC EDGE TWO-POINT [E]: the equal-time edge correlator decays as "
          "r^{-eta} with eta=%.3f ~ 1 (the chiral free-fermion CFT exponent) -- a "
          "CRITICAL edge" % eta_mean, algebraic)

    xi_bulk = -1.0 / bulk_slope
    bulk_exp = bulk_slope < -0.3 and xi_bulk < 3.0
    check("EXPONENTIAL BULK [E] (neg control): the bulk-row correlator decays "
          "EXPONENTIALLY (xi=%.2f sites, slope %.3f) -- only the edge is critical, "
          "so the power law is the edge CFT, not a geometric artefact"
          % (xi_bulk, bulk_slope), bulk_exp)

    # ---- 4. trivial-phase neg control (no edge => exponential edge row) ----
    triv = _row_corr(48, 16, 3.0, 0)
    rs = np.arange(1, 24)
    fit = (rs >= 2) & (rs <= 12)
    triv_slope = np.polyfit(rs[fit], np.log(np.maximum(triv[fit], 1e-15)), 1)[0]
    triv_exp = triv_slope < -0.3
    check("TRIVIAL-PHASE NEG CONTROL [E]: M=3 (no edge, v368) has an EXPONENTIAL "
          "edge-row correlator (slope %.3f, xi=%.2f) -- the algebraic decay is a "
          "CONSEQUENCE of the topological edge, not the boundary geometry"
          % (triv_slope, -1.0 / triv_slope), triv_exp)

    # ---- 5. scaling-collapse of the edge profile across refinements ----
    prof = np.array(edge_profiles)                     # (n_sizes, 6); r=2..7
    # successive-refinement spreads must SHRINK (Cauchy convergence to a limit),
    # not just be small: the coarse pair (36,48) vs the fine pair (48,60).
    coarse = float(np.max(np.abs(prof[1] - prof[0]) / prof[1]))
    fine = float(np.max(np.abs(prof[2] - prof[1]) / prof[2]))
    collapse = fine < 0.02 and fine < coarse and etas.std() < 0.01
    check("SCALING-COLLAPSE / CONVERGENCE [E]: eta is N-stable (%.3f+-%.3f) and the "
          "edge correlator profile is CAUCHY-CONVERGENT under refinement (successive "
          "spread shrinks: Nx 36->48 %.4f then 48->60 %.4f at r=2..7) -- the lattice "
          "edge correlators converge to a fixed conformal profile (existing scaling "
          "limit, the edge analogue of v439's bulk thermodynamic limit)"
          % (eta_mean, etas.std(), coarse, fine), collapse)

    # ---- 6. edge central charge (typed [C]) ----
    N_Maj = 2 ** (g_car - 1)
    c_minus = N_Maj * 0.5
    check("EDGE CENTRAL CHARGE [C]: eta=1 <=> one chiral Majorana (c=1/2) per edge, "
          "so the N_Maj=%d-copy carrier has a chiral c_-=%g edge CFT (=(E8)_1, "
          "consistent with v367/v368/v376; c_-=g_car+N_fam=%d) -- linear chiral "
          "dispersion + algebraic 1/r correlator + c_-=8 are the conformal data of "
          "the edge" % (N_Maj, c_minus, g_car + N_fam),
          N_Maj == 16 and c_minus == 8 and c_minus == g_car + N_fam
          and algebraic and chiral)

    # ---- 7. verdict (typed [C]/[O]) ----
    grounded = linear and chiral and algebraic and bulk_exp and triv_exp and collapse
    check("VERDICT [C]/[O]: the EDGE half of the cited MMST scaling limit (v336) is "
          "now numerically GROUNDED on our explicit collar (chiral linear kinematics "
          "+ algebraic conformal correlator + scaling-collapse). SEAM.EQUIV.01 stays "
          "[O]: the rigorous uniform convergence of all edge n-point functions is not "
          "supplied here. With v439 (bulk) + v444 (edge) BOTH halves of the one "
          "continuum residual are grounded, pinned to a single cited theorem",
          grounded and g_car == 5)

    return summary("v444 SEAM.EQUIV.CONTINUUM.EDGE: the v367/v368 lattice edge carries "
                   "the conformal data of a chiral c=1/2 Majorana CFT (linear chiral "
                   "dispersion v~0.98 with opposite per-edge velocities; algebraic edge "
                   "correlator eta~1 vs exponential bulk; trivial-phase neg control; "
                   "N-stable scaling-collapse), so the 16-copy edge is a chiral c_-=8 "
                   "(E8)_1 CFT. Grounds the EDGE half of the cited MMST scaling limit "
                   "(v336) -- the edge analogue of v439's bulk; SEAM.EQUIV.01 stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

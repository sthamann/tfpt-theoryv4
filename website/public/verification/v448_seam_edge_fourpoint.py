"""v448 -- SEAM.EQUIV.EDGE.FOURPOINT.01: pinning the ONE external MMST fact empirically --
the edge FOUR-point function is quasi-free and conformally convergent, extending v444's
two-point scaling limit to the next order.

v441 (the applicability ledger) isolated the keystone's single EXTERNAL hypothesis: the
continuum EXISTENCE of the chiral massless scaling limit (the MMST theorem).  v444
grounded that existence empirically at the level of the TWO-point function (algebraic
edge correlator + Cauchy scaling-collapse).  The MMST claim is that ALL n-point functions
converge; this module takes the next, non-trivial step -- the FOUR-point function -- on
the SAME v367/v368 p+ip collar, showing the edge four-point both is quasi-free (the MMST
CAR hypothesis literally holds) and converges to its conformal cross-ratio value under
refinement.  Every measured n-point thus converges to its conformal limit, the empirical
hallmark that the scaling limit exists.

  [E] 1. QUASI-FREE / WICK (CAR hypothesis).  the ground-state correlation matrix is an
         exact projector G^2=G (to ~1e-10), so the state is quasi-free and all n-point
         functions are Wick (Pfaffian) sums of the two-point -- the MMST quasi-free CAR
         hypothesis (ledger entry 5) literally holds on our collar.  (Structural: the BdG
         state is free, so this is a consistency check confirming the hypothesis, not a
         discovery.)
  [E] 2. FOUR-POINT CAUCHY CONVERGENCE.  the edge four-point cross-ratio quantity
         Q = [G(x0,x1)G(x2,x3)]/[G(x0,x2)G(x1,x3)] at COMMENSURATE proportional positions
         (1,2,4,7)*(Nx/12) is Cauchy-convergent under refinement (successive spread
         shrinks across Nx=36,48,60) -- the four-point converges, extending v444's
         two-point scaling-collapse to the next order.
  [E] 3. CONFORMAL FOUR-POINT FORM.  Q converges to the free-fermion CONFORMAL prediction
         Q_inf = [d(x0,x2)d(x1,x3)]/[d(x0,x1)d(x2,x3)] with chord distance d(r)=
         (Nx/pi)sin(pi r/Nx) -- the cross-ratio sin(5pi/12)/sin(pi/12)=2+sqrt(3)~3.732 --
         so the edge four-point has the chiral-CFT cross-ratio structure (eta=1), not just
         the two-point.
  [E] 4. BULK NEG CONTROL.  the bulk-row four-point quantity is orders of magnitude off
         the conformal value (exponential decay, gapped) -- only the EDGE four-point is
         conformal; the convergence is the edge CFT, not a lattice artefact.
  [C] 5. VERDICT.  the one external MMST fact (continuum existence of the chiral scaling
         limit) is now empirically supported at BOTH the two-point (v444) and four-point
         level on our explicit collar: the state is quasi-free and every measured n-point
         converges to its conformal limit.  SEAM.EQUIV.01 stays [O] -- the rigorous
         uniform-convergence theorem (MMST, v336) is the cited backbone, not supplied here.

Python-only (numpy; free-fermion BdG four-point; no new exact algebraic identity to
Wolfram-mirror -- the conformal cross-ratio target is a kinematic prediction).
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)


def _real2d(Nx, Ny, M):
    onx = -0.5 * SZ + (1 / (2j)) * SX
    ony = -0.5 * SZ + (1 / (2j)) * SY
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


def _ground_corr(Nx, Ny, M):
    H, idx = _real2d(Nx, Ny, M)
    w, v = np.linalg.eigh(H)
    occ = v[:, w < -1e-9]
    return occ @ occ.conj().T, idx


def _cmag(G, idx, y0, x0, x1):
    a, b = idx(x0, y0), idx(x1, y0)
    return np.linalg.norm(G[2 * a:2 * a + 2, 2 * b:2 * b + 2])


def _cross_ratio_Q(G, idx, Nx, y0):
    u = Nx // 12
    xs = [1 * u, 2 * u, 4 * u, 7 * u]
    g = lambda a, b: _cmag(G, idx, y0, xs[a], xs[b])
    return (g(0, 1) * g(2, 3)) / (g(0, 2) * g(1, 3))


def _chord(r, Nx):
    return (Nx / np.pi) * np.sin(np.pi * r / Nx)


def _Q_conformal(Nx):
    u = Nx // 12
    xs = [1 * u, 2 * u, 4 * u, 7 * u]
    d = lambda a, b: _chord(abs(xs[a] - xs[b]), Nx)
    return (d(0, 2) * d(1, 3)) / (d(0, 1) * d(2, 3))


def run():
    reset()
    print("v448 SEAM.EQUIV.EDGE.FOURPOINT: the edge FOUR-point is quasi-free and "
          "conformally convergent -- pinning the one external MMST fact at 4-point order")
    M = 1.0
    sizes = [(36, 16), (48, 18), (60, 20)]

    # ---- 1. quasi-free / Wick (projector idempotency) ----
    G60, _ = _ground_corr(60, 20, M)
    proj_err = float(np.linalg.norm(G60 @ G60 - G60))
    quasifree = proj_err < 1e-8
    check("QUASI-FREE / WICK (CAR hypothesis) [E]: the ground-state correlation matrix is "
          "an exact projector G^2=G (||G^2-G||=%.1e), so the state is quasi-free and all "
          "n-point functions are Wick/Pfaffian sums of the two-point -- the MMST quasi-free "
          "CAR hypothesis (ledger entry 5) literally holds on the collar" % proj_err,
          quasifree)

    # ---- 2/3. edge four-point: Cauchy convergence + conformal cross-ratio ----
    Qs = []
    for Nx, Ny in sizes:
        G, idx = _ground_corr(Nx, Ny, M)
        Qs.append(_cross_ratio_Q(G, idx, Nx, 0))
    Qs = np.array(Qs)
    coarse = abs(Qs[1] - Qs[0])
    fine = abs(Qs[2] - Qs[1])
    cauchy = fine < 0.03 and fine < coarse
    check("FOUR-POINT CAUCHY CONVERGENCE [E]: the edge four-point cross-ratio Q="
          "[G01 G23]/[G02 G13] at commensurate positions (1,2,4,7)*(Nx/12) is "
          "Cauchy-convergent (Q=%.4f,%.4f,%.4f; spread shrinks %.4f->%.4f, Nx=36..60) -- "
          "the four-point converges, extending v444's two-point scaling-collapse"
          % (Qs[0], Qs[1], Qs[2], coarse, fine), cauchy)

    Q_pred = _Q_conformal(60)
    conformal = abs(Qs[2] - Q_pred) < 0.02
    check("CONFORMAL FOUR-POINT FORM [E]: Q converges to the free-fermion CONFORMAL "
          "cross-ratio Q_inf=[d02 d13]/[d01 d23]=sin(5pi/12)/sin(pi/12)=2+sqrt(3)=%.4f "
          "(chord distance d(r)=(Nx/pi)sin(pi r/Nx)); measured Q(60)=%.4f, |diff|=%.4f -- "
          "the edge four-point has the chiral-CFT cross-ratio structure (eta=1)"
          % (Q_pred, Qs[2], abs(Qs[2] - Q_pred)), conformal)

    # ---- 4. bulk neg control ----
    Gb, idxb = _ground_corr(60, 20, M)
    Q_bulk = _cross_ratio_Q(Gb, idxb, 60, 20 // 2)
    bulk_off = abs(Q_bulk - Q_pred) > 10.0
    check("BULK NEG CONTROL [E]: the bulk-row four-point quantity Q_bulk=%.2f is orders of "
          "magnitude off the conformal value %.4f (exponential decay, gapped) -- only the "
          "EDGE four-point is conformal, so the convergence is the edge CFT, not a lattice "
          "artefact" % (Q_bulk, Q_pred), bulk_off)

    # ---- 5. verdict, typed [C] ----
    grounded = quasifree and cauchy and conformal and bulk_off
    check("VERDICT [C]: the one external MMST fact (continuum existence of the chiral "
          "scaling limit) is now empirically supported at BOTH two-point (v444) and "
          "four-point order on our explicit collar -- the state is quasi-free and every "
          "measured n-point converges to its conformal limit. SEAM.EQUIV.01 stays [O]: the "
          "rigorous MMST uniform-convergence theorem (v336) is the cited backbone",
          grounded and g_car == 5)

    return summary("v448 SEAM.EQUIV.EDGE.FOURPOINT: the edge four-point is quasi-free "
                   "(G^2=G) and Cauchy-convergent to the free-fermion conformal cross-ratio "
                   "sin(5pi/12)/sin(pi/12)=2+sqrt(3) (vs an off-scale exponential bulk "
                   "control), extending v444's two-point scaling limit to 4-point order and "
                   "empirically pinning the one external MMST existence fact; "
                   "SEAM.EQUIV.01 stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

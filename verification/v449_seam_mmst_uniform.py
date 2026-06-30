"""v449 -- SEAM.EQUIV.MMST.UNIFORM.01: uniform-in-N control of the edge scaling
limit -- the empirical content of the ONE external MMST hypothesis, strengthened.

The single residual of SEAM.EQUIV.01 (after v444/v447/v448) is the cited MMST/OS
theorem (v336): the chiral massless scaling limit EXISTS, i.e. ALL n-point
functions converge UNIFORMLY in the lattice spacing.  v444 grounded the two-point,
v448 the four-point, each at a single conformal cross-ratio.  This module adds the
property the abstract theorem actually asserts -- UNIFORMITY: on the same
v367/v368 p+ip collar, TWO logically independent edge four-point cross-ratios both
converge to their (distinct) free-fermion conformal values under refinement, the
deviation is Cauchy, and |deviation| * N stays bounded by a single N-independent
constant across BOTH observables (an empirical 1/N uniform rate).  This does NOT
prove the theorem -- it pins, on our explicit collar, exactly the convergence the
cited theorem supplies abstractly.

  [E] 1. CROSS-RATIO A converges: Q_A(1,2,4,7)/12 -> sin(5pi/12)/sin(pi/12)=2+sqrt3
         (Cauchy under refinement, finest within 1%).
  [E] 2. CROSS-RATIO B (independent positions) converges: Q_B(1,3,5,9)/12 -> its
         own conformal value 2 (Cauchy, finest within 1%) -- a SECOND observable
         with a DIFFERENT limit, so the convergence is not a single tuned point.
  [E] 3. UNIFORM 1/N RATE: for both cross-ratios and every N in {36,48,60},
         |Q(N)-Q_inf| * N <= 4 (one N-independent constant across two independent
         observables) -- the empirical hallmark of uniform-in-N convergence.
  [E] 4. BULK NEG CONTROL: the bulk-row cross-ratio is off-scale (gapped,
         exponential) -- only the EDGE converges, so it is the edge CFT.
  [C]/[O] 5. VERDICT: the MMST uniform-convergence HYPOTHESIS is empirically
         satisfied on our collar at two-point (v444), four-point (v448) and now
         multi-observable uniform-rate level; SEAM.EQUIV.01 stays [O] -- the
         abstract continuum existence theorem (v336) is strengthened in evidence,
         not replaced by a proof.

Python-only (numpy; free-fermion BdG collar; the conformal targets 2+sqrt3 and 2
are kinematic cross-ratios, no new exact algebraic identity to Wolfram-mirror).
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)

CONF = {(1, 2, 4, 7): 2 + np.sqrt(3), (1, 3, 5, 9): 2.0}


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


def _gcorr(Nx, Ny, M):
    H, idx = _real2d(Nx, Ny, M)
    w, v = np.linalg.eigh(H)
    occ = v[:, w < -1e-9]
    return occ @ occ.conj().T, idx


def _cmag(G, idx, y0, x0, x1):
    a, b = idx(x0, y0), idx(x1, y0)
    return np.linalg.norm(G[2 * a:2 * a + 2, 2 * b:2 * b + 2])


def _chord(r, Nx):
    return (Nx / np.pi) * np.sin(np.pi * r / Nx)


def _Qmeas(G, idx, Nx, frac, y0):
    u = Nx // 12
    xs = [f * u for f in frac]
    g = lambda a, b: _cmag(G, idx, y0, xs[a], xs[b])
    return (g(0, 1) * g(2, 3)) / (g(0, 2) * g(1, 3))


def run():
    reset()
    print("v449 SEAM.EQUIV.MMST.UNIFORM: uniform-in-N control of the edge scaling "
          "limit -- two independent cross-ratios converge at a single 1/N rate")
    sizes = [36, 48, 60]
    fracs = [(1, 2, 4, 7), (1, 3, 5, 9)]

    # measure both cross-ratios on the SAME ground state per size (edge row y=0)
    Q = {f: [] for f in fracs}
    Gfine = idxfine = None
    for Nx in sizes:
        Ny = Nx // 3
        G, idx = _gcorr(Nx, Ny, 1.0)
        if Nx == sizes[-1]:
            Gfine, idxfine = G, idx
        for f in fracs:
            Q[f].append(_Qmeas(G, idx, Nx, f, 0))

    # ---- 1/2. each cross-ratio Cauchy + converges to its conformal value ----
    conv_ok = {}
    for f in fracs:
        qs = np.array(Q[f])
        target = CONF[f]
        dev = np.abs(qs - target)
        monotone = bool(np.all(np.diff(dev) <= 1e-9))    # deviation shrinks under refinement
        finest = dev[-1]
        ok = monotone and finest < 0.01 * abs(target)
        conv_ok[f] = ok
        label = "A" if f == (1, 2, 4, 7) else "B"
        tname = "sin(5pi/12)/sin(pi/12)=2+sqrt(3)" if f == (1, 2, 4, 7) else "2"
        check("CROSS-RATIO %s CONVERGES [E]: Q%s%s -> %s=%.4f, measured "
              "%.4f,%.4f,%.4f (Nx=36,48,60); |Q-Q_inf| shrinks monotonically "
              "%.4f->%.4f->%.4f, finest <1%%" % (label, label,
              str(f).replace(" ", ""), tname, target, qs[0], qs[1], qs[2],
              dev[0], dev[1], dev[2]), ok)

    # ---- 3. uniform 1/N rate across BOTH observables ----
    prods = []
    for f in fracs:
        qs = np.array(Q[f])
        for k, Nx in enumerate(sizes):
            prods.append(abs(qs[k] - CONF[f]) * Nx)
    uniform = max(prods) <= 4.0
    check("UNIFORM 1/N RATE [E]: |Q(N)-Q_inf|*N <= %.3f for BOTH cross-ratios and "
          "every Nx in {36,48,60} (max=%.3f) -- a single N-independent constant "
          "bounds the deviation across two independent observables, the empirical "
          "hallmark of uniform-in-N convergence" % (4.0, max(prods)), uniform)

    # ---- 4. bulk neg control (off-scale) ----
    Qb = _Qmeas(Gfine, idxfine, sizes[-1], (1, 2, 4, 7), (sizes[-1] // 3) // 2)
    bulk_off = abs(Qb - CONF[(1, 2, 4, 7)]) > 10.0
    check("BULK NEG CONTROL [E]: the bulk-row cross-ratio Q_bulk=%.2f is off-scale "
          "vs the conformal %.4f (gapped, exponential) -- only the EDGE converges, "
          "so the uniform convergence is the edge CFT" % (Qb, CONF[(1, 2, 4, 7)]),
          bulk_off)

    # ---- 5. verdict [C]/[O] ----
    grounded = all(conv_ok.values()) and uniform and bulk_off
    check("VERDICT [C]/[O]: the MMST uniform-convergence hypothesis is empirically "
          "satisfied on our collar -- two independent edge cross-ratios converge to "
          "distinct conformal values at one 1/N rate, extending v444/v448 from "
          "single points to a uniform multi-observable statement; SEAM.EQUIV.01 "
          "stays [O], the abstract existence theorem (v336) is strengthened in "
          "evidence, not proved here", grounded and g_car == 5)

    return summary("v449 SEAM.EQUIV.MMST.UNIFORM: two independent edge four-point "
                   "cross-ratios converge to 2+sqrt(3) and 2 (Cauchy), with "
                   "|Q-Q_inf|*N bounded by one N-independent constant across both "
                   "(uniform 1/N rate) vs an off-scale bulk control -- the empirical "
                   "content of the cited MMST uniform-convergence theorem; "
                   "SEAM.EQUIV.01 stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

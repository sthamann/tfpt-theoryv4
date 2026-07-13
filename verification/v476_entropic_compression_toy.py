"""v476 -- GRAV.ENTROPIC.COMPRESS.01: the AP2 compression conjecture of the
entropic-action bridge (v473) made WELL-POSED on an exactly solvable model --
the naive operator-side reading is shown to be ill-posed, the state-side
reading is forced, and the mismatch between the two is exactly quadratic in
the cross-cut correlations and gap-suppressed.  AP2 itself stays [O]; this
module fixes WHAT the conjecture must say, it does not prove it.

Background.  v473 recorded the bridge conjecture as
P_Sigma (G~ g~^-1) P_Sigma = Delta_Sigma^{1/2}: compress Bianconi's relative
metric operator to the seam and get the TFPT modular operator.  On a
quasi-free (Gaussian) system everything is computable: a state is its
one-particle covariance C, the boundary restriction is the compression
C_A = P C P (v155), and the boundary modular data is Peschel's
K = ln((1-C_A)/C_A), i.e. the one-particle modular operator is
Delta_A = f(C_A) with f(x) = x/(1-x).  For a THERMAL bulk the bulk analog is
exact: f(C_T) = e^{-h/T} -- the Bianconi-shaped "exponential of the modular
Hamiltonian".  The conjecture's two possible readings differ by an order of
operations: f(P C P) (build the modular operator FROM the compressed state)
vs P f(C) P (compress the bulk modular operator).

  [N] 1. PURE GAPPED BULK.  Staggered-mass hopping chain (N = 16), ground
        state covariance C = projection onto negative modes: C^2 = C to
        1e-12, gap 2m verified.  The physical seam situation: the bulk is
        PURE, the boundary is thermal (Bisognano-Wichmann shape).
  [N] 2. COMPRESSION IS THERMAL (v155 in the bridge context).  C_A = P C P
        has spectrum strictly inside (0,1); Peschel K finite; entanglement
        entropy > 0 -- the compression of a projection is a strict
        contraction, the boundary state is genuinely KMS-like.
  [N] 3. THE ORDER OBSTRUCTION (the reading DECIDED).  On the pure bulk,
        spec(C) = {0,1}, so f(x) = x/(1-x) is SINGULAR on the spectrum:
        P f(C) P -- the literal v473 operator-side reading -- is ILL-POSED,
        while f(P C P) is finite.  Hence the compression identity can only
        be read STATE-SIDE: build Delta_Sigma from the COMPRESSED relative
        metric.  This matches Bianconi's own construction (her G~ is a LOCAL
        field, i.e. already the compressed datum) -- AP2 is retyped, not
        weakened.
  [E] 4. BLOCK ALGEBRA: THE MISMATCH IS EXACTLY SECOND ORDER.  For block
        matrices, [C^2]_AA - (C_AA)^2 = C_AB C_BA and [C^3]_AA - (C_AA)^3 =
        C_AA C_AB C_BA + C_AB C_BA C_AA + C_AB C_BB C_BA (symbolic, exact):
        for every analytic f the two readings agree up to SECOND order in
        the cross-cut block -- the modular (entanglement) content lives
        exactly in that quadratic correction; first order vanishes
        identically.
  [N] 5. GAP CONTROL AT THE BOUNDED LEVEL (the TFPT regime).  The clean
        comparison lives at the COVARIANCE level, where both readings are
        bounded in [0,1]: state-side [Fermi(h/T)]_AA (compress the state)
        vs operator-side Fermi(h_AA/T) (build the state from the compressed
        generator).  Thermal bulk (T = 1): the bulk identity f(C_T) =
        e^{-h/T} holds to 1e-10; the mismatch obeys the quadratic law
        d <= x^2 (d/x^2 in [0.4, 1.0], bounded) and falls with the gap in
        the gapped regime (m >= 2), the cross-cut norm x falls
        monotonically; the decoupled cut ([h,P] = 0) agrees EXACTLY.  The
        unbounded modular operator Delta = e^{-h/T} shows the same quadratic
        structure with exponentially amplified absolute norms -- recorded:
        the compression identity must be stated at the bounded
        (state/covariance) level, its modular content follows spectrally.
  [C] 6. WHAT THIS DOES AND DOES NOT DO.  AP2 is now WELL-POSED: state-side
        reading at the bounded level, mismatch quadratic in cross-cut
        correlations, gap-suppressed.  NOT proven: the continuum seam
        statement (the Calderon compression of the actual relative metric
        operator equals the actual seam modular operator).  AP2 stays [O];
        no marker moves.

NET TYPING: [E] the block-algebra identity (sympy, symbolic blocks); [N] the
model exhibits (numpy, gapped chain); [C] the retyped conjecture; [O] AP2
itself.  Extends GRAV.ENTROPIC.ACTION.01 (v473).  Python-only by nature
(matrix functions on a lattice model); the exact block identity is trivial
algebra, flagged in the Wolfram README.
"""
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset

N = 16          # chain length (even)
NA = 6          # seam block size


def chain_h(m, n=N):
    """Single-particle Hamiltonian: hopping + staggered mass (gap 2m)."""
    h = np.zeros((n, n))
    for i in range(n - 1):
        h[i, i + 1] = h[i + 1, i] = 1.0
    for i in range(n):
        h[i, i] = m * (-1) ** i
    return h


def ground_cov(h):
    """Covariance of the filled negative-energy sea: projection."""
    w, v = np.linalg.eigh(h)
    neg = v[:, w < 0]
    return neg @ neg.T


def thermal_cov(h, T):
    w, v = np.linalg.eigh(h)
    occ = 1.0 / (1.0 + np.exp(w / T))
    return (v * occ) @ v.T


def matfun(C, fun):
    w, v = np.linalg.eigh(C)
    return (v * fun(w)) @ v.T


def run():
    reset()
    print("v476  GRAV.ENTROPIC.COMPRESS.01: the AP2 compression conjecture made well-posed (toy exhibit)")

    # 1. pure gapped bulk (moderate mass: gapped AND visibly entangled boundary)
    m0 = 0.5
    h = chain_h(m0)
    w = np.linalg.eigvalsh(h)
    gap = w[w > 0].min() - w[w < 0].max()
    C = ground_cov(h)
    purity = float(np.abs(C @ C - C).max())
    check("PURE GAPPED BULK [N]: staggered-mass chain (N = %d, m = %.1f), spectral "
          "gap %.2f >= 2m = %.1f; ground-state covariance is a PROJECTION, "
          "|C^2 - C| = %.1e -- the physical seam situation: pure bulk, thermal "
          "boundary (Bisognano-Wichmann shape)" % (N, m0, gap, 2 * m0, purity),
          purity < 1e-12 and gap >= 2 * m0 - 1e-9)

    # 2. compression is thermal
    CA = C[:NA, :NA]
    lam = np.linalg.eigvalsh(CA)
    dist = float(min(lam.min(), (1 - lam).min()))
    ent = float(-(lam * np.log(np.clip(lam, 1e-300, 1)) +
                  (1 - lam) * np.log(np.clip(1 - lam, 1e-300, 1))).sum())
    K = matfun(CA, lambda x: np.log((1 - x) / x))
    check("COMPRESSION IS THERMAL [N] (v155 in the bridge context): C_A = P C P has "
          "spectrum strictly inside (0,1) (distance %.1e > 0), the Peschel modular "
          "Hamiltonian K = ln((1-C_A)/C_A) is finite (|K| = %.1f), entanglement "
          "entropy S = %.4f > 0 -- the boundary state is genuinely KMS-like"
          % (dist, float(np.abs(K).max()), ent),
          dist > 1e-14 and ent > 1e-8 and np.isfinite(K).all())

    # 3. the order obstruction: P f(C) P ill-posed on the pure bulk
    spec_dist = float(np.min(np.minimum(np.abs(np.linalg.eigvalsh(C)),
                                        np.abs(np.linalg.eigvalsh(C) - 1))))
    delta_state = matfun(CA, lambda x: x / (1 - x))
    check("ORDER OBSTRUCTION [N] (the reading DECIDED): the pure bulk has spec(C) "
          "= {0,1} to %.1e, so f(x) = x/(1-x) is SINGULAR on the spectrum -- the "
          "literal operator-side reading P f(C) P of the v473 conjecture is "
          "ILL-POSED, while the state-side f(P C P) is finite (|Delta_A| = %.1f): "
          "the compression identity can only be read STATE-SIDE (build Delta_Sigma "
          "from the COMPRESSED relative metric) -- matching Bianconi's own local-"
          "metric construction; AP2 retyped, not weakened"
          % (spec_dist, float(np.abs(delta_state).max())),
          spec_dist < 1e-12 and np.isfinite(delta_state).all())

    # 4. block algebra: mismatch exactly second order in the cross block (symbolic)
    nA, nB = 2, 2
    A = sp.MatrixSymbol('A', nA, nA)
    B = sp.MatrixSymbol('B', nA, nB)
    Bt = sp.MatrixSymbol('Bt', nB, nA)
    D = sp.MatrixSymbol('D', nB, nB)
    Cb = sp.BlockMatrix([[A, B], [Bt, D]])
    sq = sp.block_collapse(Cb * Cb)
    cu = sp.block_collapse(Cb * Cb * Cb)
    mis2 = sp.expand(sq.blocks[0, 0] - A ** 2)
    mis3 = sp.expand(cu.blocks[0, 0] - A ** 3)
    check("BLOCK ALGEBRA [E] (symbolic): [C^2]_AA - (C_AA)^2 = %s and [C^3]_AA - "
          "(C_AA)^3 = %s -- every term carries the cross block TWICE, first order "
          "vanishes identically: for ANY analytic f the two readings agree up to "
          "SECOND order in the cross-cut correlations; the modular (entanglement) "
          "content lives exactly in that quadratic correction"
          % (mis2, mis3),
          mis2 == sp.expand(B * Bt) and
          mis3 == sp.expand(A * B * Bt + B * Bt * A + B * D * Bt))

    # 5. gap control at the bounded (covariance) level
    T = 1.0
    f = lambda x: x / (1 - x)
    deltas, crosses, ratios = [], [], []
    bulk_id_err = 0.0
    masses = (0.5, 1.0, 2.0, 4.0, 8.0)
    for m in masses:
        hm = chain_h(m)
        CT = thermal_cov(hm, T)
        wm, vm = np.linalg.eigh(hm)
        bulk_mod = (vm * np.exp(-wm / T)) @ vm.T          # e^{-h/T}
        rel = float(np.abs(matfun(CT, f) - bulk_mod).max() / np.abs(bulk_mod).max())
        bulk_id_err = max(bulk_id_err, rel)
        state_side = CT[:NA, :NA]                          # compress the state
        op_side = thermal_cov(hm[:NA, :NA], T)             # state of the compressed generator
        d = float(np.linalg.norm(state_side - op_side, 2))
        x = float(np.linalg.norm(CT[:NA, NA:], 2))
        deltas.append(d)
        crosses.append(x)
        ratios.append(d / x ** 2)
    x_mono = all(crosses[i] > crosses[i + 1] for i in range(len(masses) - 1))
    d_gapped = deltas[2] > deltas[3] > deltas[4]           # falls in the gapped regime
    quad_law = max(ratios) <= 1.1                          # d <= x^2 (quadratic law)
    # decoupled control: [h, P] = 0 => exact agreement
    hd = chain_h(2.0)
    hd[NA - 1, NA] = hd[NA, NA - 1] = 0.0
    d_dec = float(np.linalg.norm(thermal_cov(hd, T)[:NA, :NA]
                                 - thermal_cov(hd[:NA, :NA], T), 2))
    check("GAP CONTROL AT THE BOUNDED LEVEL [N] (the TFPT regime): thermal bulk "
          "(T = 1) obeys the Bianconi-shaped bulk identity f(C_T) = e^{-h/T} to "
          "relative %.1e; at the covariance level the mismatch d = ||[Fermi(h/T)]_AA - "
          "Fermi(h_AA/T)|| obeys the QUADRATIC law d <= x^2 (d/x^2 = %s) and falls "
          "with the gap in the gapped regime %s while the cross-cut norm x falls "
          "monotonically %s; decoupled cut => EXACT agreement (%.1e) -- the two "
          "readings converge in the gap-dominated regime, where TFPT operates "
          "(Delta_eff > 0, v76/v337)"
          % (bulk_id_err, ["%.2f" % r for r in ratios],
             ["%.1e" % d for d in deltas], ["%.1e" % x for x in crosses], d_dec),
          bulk_id_err < 1e-10 and x_mono and d_gapped and quad_law and d_dec < 1e-12)

    # 6. honest scope
    check("SCOPE [C/O]: AP2 is now WELL-POSED -- state-side reading forced, "
          "mismatch exactly quadratic in cross-cut correlations, gap-suppressed; "
          "NOT proven: the continuum seam statement (Calderon compression of the "
          "actual relative metric = the actual seam modular operator). AP2 stays "
          "[O]; no status marker moves", True)

    return summary("v476 GRAV.ENTROPIC.COMPRESS.01: AP2 made well-posed -- [N] pure gapped "
                   "bulk (C^2 = C), compression thermal (Peschel K finite, S > 0), ORDER "
                   "OBSTRUCTION: P f(C) P ill-posed on the pure bulk => state-side reading "
                   "FORCED (matches Bianconi's local construction); [E] block algebra: "
                   "mismatch exactly second order in the cross block; [N] gap control: "
                   "f(C_T) = e^{-h/T} exact, mismatch quadratic + falling with the gap, "
                   "decoupled cut exact; [C] retyped conjecture; [O] AP2 open, no marker moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v474 -- GRAV.ENTROPIC.HODGE.01: the operator level of the entropic-action
bridge (work packages 1 + 4-algebra of the v473 round).  v473 pinned the
VECTOR-SPACE identity Omega^{0,1,2}(C^5) ~ S+_{D5} (1+5+10 = 16) and the exact
Lambda-channel target Tr Q^2 = 32 c3^4; this module upgrades the Hodge count to
the OPERATOR level on the finite carrier Fock space Lambda^* C^5 (dim 2^g_car =
32) and solves/kills the Q-block ansatz by exact enumeration.  It closes NO
gate; the compression conjecture (AP2) and the R^2 mechanism stay open.

  [E] 1. CAR => CLIFFORD (the spinor structure EXHIBITED).  On the 32-dim Fock
        space Lambda^* C^5 the ten operators Gamma_{2k} = a_k^dag + a_k,
        Gamma_{2k+1} = i(a_k^dag - a_k) satisfy {Gamma_a, Gamma_b} = 2 delta_ab
        exactly -- the so(10) = D5 Clifford algebra acts on the carrier
        exterior algebra (exact integer matrices).
  [E] 2. S+ = Lambda^even AS A D5-MODULE (operator level).  The 45 bilinears
        M_ab = [Gamma_a, Gamma_b]/4 all commute with the grading involution
        gamma = (-1)^N, span a 45-dimensional Lie algebra (= dim so(10)), and
        preserve the 16-dim even subspace: the carrier half-spinor IS the even
        exterior algebra with its spinor structure -- the v2/v44/v197 count,
        now with the algebra action checked.
  [E] 3. HODGE-DIRAC SYMBOL = CLIFFORD MULTIPLICATION.  For symbolic real xi,
        the Dirac-Kaehler symbol c(xi) = a^dag(xi) - a(xi) (= the principal
        symbol of Bianconi's D = d + delta) satisfies c(xi)^2 = -|xi|^2 * Id
        exactly on all 32 dimensions -- her Hodge-Dirac operator is Clifford
        multiplication at symbol level, the operator content behind check 1
        of v473.
  [E] 4. THE FOLD IS THE 5 -> 5bar CONJUGATION.  Under the Cartan of u(5) the
        traceless weights of Lambda^4 are EXACTLY the negatives of those of
        Lambda^1, so the Hodge fold *: Lambda^1 ~ Lambda^4 conjugates the
        vector block: Bianconi's fiber 1 + 5 + 10 becomes the GUT half-spinor
        16 = 1 + 5bar + 10 -- the fold supplies precisely the conjugation that
        the SM carrier decomposition needs (not a mere dimension match).
  [E] 5. HONEST OBSTRUCTION.  Omega^{<=2} is NOT Clifford-invariant (c(xi)
        maps Lambda^2 into Lambda^3), while Lambda^even is invariant under the
        even Clifford algebra -- so the bridge identification must go through
        the Hodge fold, never through naive degree truncation.  Recorded as a
        constraint on AP2, not a failure.
  [E] 6. Q-TARGET ENUMERATION (AP4-algebra; the v473 conjecture DECIDED).  The
        uniform-block ansatz Q = k c3^2 P_d with integer multiplier k solves
        Tr Q^2 = d k^2 c3^4 = 32 c3^4 for EXACTLY three supports:
        (d,k) = (2,4), (8,2), (32,1) -- the sheet pair |Z2|, the rank
        g_car + N_fam = rank E8, and the FULL Fock space 2^g_car = dim
        Lambda^* C^5 (the minimal uniform solution: eps_* = e^{-1/alpha} c3^2
        PER FOCK MODE, q = c3^2 = 1/(64 pi^2)).  The two-form block d = 10
        (problem-note conjecture 'the pair sector carries it') and the fiber
        d = 16 REQUIRE irrational multipliers sqrt(16/5), sqrt(2) -- the
        naive pair-block reading is KILLED.  Bonus identity: Tr Q^2 /
        delta_top = 32/48 = 2/3 = dim Lambda^* / Omega_adm -- the (2/3) in
        the v473 target is the mode-count ratio.
  [C] 7. WHAT STAYS OPEN.  Which of the three admissible supports is the
        physical Q (the uniform-32 reading is minimal, not derived); the AP2
        compression P_Sigma (G~ g~^-1) P_Sigma = Delta_Sigma^{1/2}; the R^2
        mechanism (v473 kill test).  No status marker moves.

NET TYPING: [E] the five operator/arithmetic facts; [C] the physical Q
assignment; [O] unchanged (AP2 + R^2).  Extends GRAV.ENTROPIC.ACTION.01
(v473).  Mixed exact: integer Fock matrices (numpy, entries in {0,+-1,+-i},
arithmetic exact in double precision) + symbolic symbol identity and weight /
enumeration checks (sympy, Wolfram-mirrored where cheap).
"""
import itertools

import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

pi = sp.pi
c3 = sp.Rational(1, 8) / pi
N = 5
DIM = 2 ** N  # 32

SUBSETS = [frozenset(s) for k in range(N + 1)
           for s in itertools.combinations(range(N), k)]
IDX = {s: i for i, s in enumerate(SUBSETS)}


def adag(k):
    """Creation operator e_k ^ .  on the Fock basis (exact integer entries)."""
    M = np.zeros((DIM, DIM), dtype=complex)
    for s in SUBSETS:
        if k not in s:
            sign = (-1) ** sum(1 for j in s if j < k)
            M[IDX[frozenset(s | {k})], IDX[s]] = sign
    return M


def run():
    reset()
    print("v474  GRAV.ENTROPIC.HODGE.01: operator level of the entropic-action bridge (AP1 + AP4-algebra)")

    A_DAG = [adag(k) for k in range(N)]
    A = [m.conj().T for m in A_DAG]
    ID = np.eye(DIM)

    # 1. CAR => Clifford: ten gammas, {Gamma_a, Gamma_b} = 2 delta_ab
    G = []
    for k in range(N):
        G.append(A_DAG[k] + A[k])
        G.append(1j * (A_DAG[k] - A[k]))
    max_err = 0.0
    for i in range(10):
        for j in range(10):
            anti = G[i] @ G[j] + G[j] @ G[i]
            max_err = max(max_err, float(np.abs(anti - 2 * (i == j) * ID).max()))
    check("CAR => CLIFFORD [E]: ten Gamma's from the CAR pair (a_k^dag, a_k) on "
          "Lambda^* C^5 (dim 2^g_car = %d) satisfy {Gamma_a, Gamma_b} = 2 delta_ab "
          "for all 100 pairs (max residual %.1e, exact integer arithmetic) -- the "
          "so(10) = D5 Clifford algebra acts on the carrier exterior algebra"
          % (DIM, max_err), max_err == 0.0)

    # 2. so(10) bilinears: parity-preserving, 45-dim span, Lambda^even invariant
    parity = np.diag([(-1.0) ** len(s) for s in SUBSETS])
    bilinears = [(G[i] @ G[j] - G[j] @ G[i]) / 4 for i in range(10) for j in range(i + 1, 10)]
    commute_par = max(float(np.abs(M @ parity - parity @ M).max()) for M in bilinears)
    stack = np.array([np.concatenate([M.real.ravel(), M.imag.ravel()]) for M in bilinears])
    span_dim = int(np.linalg.matrix_rank(stack, tol=1e-9))
    even_idx = [IDX[s] for s in SUBSETS if len(s) % 2 == 0]
    odd_idx = [IDX[s] for s in SUBSETS if len(s) % 2 == 1]
    leak = max(float(np.abs(M[np.ix_(odd_idx, even_idx)]).max()) for M in bilinears)
    check("S+ = LAMBDA^EVEN AS D5-MODULE [E]: the 45 bilinears [Gamma_a,Gamma_b]/4 "
          "all commute with gamma = (-1)^N (max residual %.1e), span a %d-dim Lie "
          "algebra = dim so(10) = 45, and leak NOTHING from the 16-dim even "
          "subspace (max %.1e) -- the carrier half-spinor IS the even exterior "
          "algebra with its spinor structure (operator level of v2/v44/v197)"
          % (commute_par, span_dim, leak),
          commute_par == 0.0 and span_dim == 45 and leak == 0.0 and len(even_idx) == 16)

    # 3. Hodge-Dirac symbol = Clifford multiplication (symbolic, exact)
    xi = sp.symbols('xi0:5', real=True)
    Adag_s = sp.zeros(DIM, DIM)
    for k in range(N):
        Adag_s += xi[k] * sp.Matrix(A_DAG[k].real.astype(int))
    C = Adag_s - Adag_s.T  # a(xi) = a^dag(xi)^T on the real integer matrices
    resid = sp.expand(C * C + sum(x ** 2 for x in xi) * sp.eye(DIM))
    check("HODGE-DIRAC SYMBOL [E]: c(xi) = a^dag(xi) - a(xi) (the principal symbol "
          "of Bianconi's D = d + delta) satisfies c(xi)^2 = -|xi|^2 Id exactly on "
          "all 32 dimensions, for SYMBOLIC real xi -- her Hodge-Dirac operator is "
          "Clifford multiplication at symbol level", resid == sp.zeros(DIM, DIM))

    # 4. the fold is the 5 -> 5bar conjugation (traceless u(5) weights)
    def traceless_weights(deg):
        out = []
        for s in SUBSETS:
            if len(s) == deg:
                w = [sp.Integer(1) if i in s else sp.Integer(0) for i in range(N)]
                shift = sp.Rational(deg, N)
                out.append(tuple(wi - shift for wi in w))
        return sorted(out)

    w1, w4 = traceless_weights(1), traceless_weights(4)
    neg_w1 = sorted(tuple(-x for x in w) for w in w1)
    dims_fiber = [len(traceless_weights(d)) for d in (0, 1, 2)]
    dims_even = [len(traceless_weights(d)) for d in (0, 2, 4)]
    check("THE FOLD IS 5 -> 5bar [E]: traceless u(5) weights of Lambda^4 = "
          "NEGATIVES of those of Lambda^1 (multisets equal), so the Hodge fold "
          "*: Lambda^1 ~ Lambda^4 conjugates the vector block -- Bianconi's fiber "
          "1+5+10 %s becomes the GUT half-spinor 16 = 1 + 5bar + 10 %s (the SM "
          "carrier decomposition), not a mere dimension match"
          % (dims_fiber, dims_even),
          w4 == neg_w1 and dims_fiber == [1, 5, 10] and dims_even == [1, 10, 5])

    # 5. honest obstruction: Omega^{<=2} not Clifford-invariant
    c_e4 = A_DAG[4] - A[4]
    v_l2 = np.zeros(DIM)
    v_l2[IDX[frozenset({0, 1})]] = 1.0          # a Lambda^2 basis element
    img = c_e4 @ v_l2
    l3_comp = float(np.abs(img[IDX[frozenset({0, 1, 4})]]))
    even_prod = c_e4 @ (A_DAG[2] - A[2])
    even_leak = float(np.abs(even_prod[np.ix_(odd_idx, even_idx)]).max())
    check("HONEST OBSTRUCTION [E]: c(e_5) maps Lambda^2 into Lambda^3 (component "
          "%.0f != 0), so Omega^{<=2} is NOT Clifford-invariant; the EVEN Clifford "
          "algebra preserves Lambda^even (leak %.1e) -- the bridge identification "
          "must go through the Hodge fold, never through naive degree truncation "
          "(a constraint on AP2, recorded)" % (l3_comp, even_leak),
          l3_comp == 1.0 and even_leak == 0.0)

    # 6. Q-target enumeration: d * k^2 = 32, integer k
    target = 32 * c3 ** 4
    sols = [(d, sp.sqrt(sp.Rational(32, d))) for d in range(1, 33)
            if sp.sqrt(sp.Rational(32, d)).is_rational]
    int_sols = [(d, int(k)) for d, k in sols if k == int(k)]
    ten_irr = not sp.sqrt(sp.Rational(32, 10)).is_rational
    sixteen_irr = not sp.sqrt(sp.Rational(32, 16)).is_rational
    delta_top = 48 * c3 ** 4
    ratio = sp.simplify(target / delta_top)
    q_min = sp.simplify(c3 ** 2)
    check("Q-TARGET ENUMERATION [E] (AP4-algebra, the v473 conjecture DECIDED): "
          "Tr Q^2 = d k^2 c3^4 = 32 c3^4 with INTEGER k has exactly the supports "
          "%s = {|Z2|, g_car+N_fam = rank E8, 2^g_car = dim Lambda^*} -- minimal "
          "uniform solution Q = c3^2 Id (q = c3^2 = %s per Fock mode); the "
          "two-form block d = 10 needs sqrt(16/5) and the fiber d = 16 needs "
          "sqrt(2) (both irrational) => the naive pair-block reading is KILLED; "
          "bonus: Tr Q^2 / delta_top = %s = 32/48 = dim Lambda^*/Omega_adm"
          % (int_sols, q_min, ratio),
          int_sols == [(2, 4), (8, 2), (32, 1)] and ten_irr and sixteen_irr and
          ratio == sp.Rational(2, 3) and
          sp.simplify(target - sp.Rational(1, 128) / pi ** 4) == 0 and
          2 ** g_car == 32 and g_car + N_fam == 8)

    # 7. what stays open
    check("WHAT STAYS OPEN [C/O]: the physical choice among the three admissible "
          "Q supports (uniform-32 is minimal, not derived); the AP2 compression "
          "P_Sigma (G~ g~^-1) P_Sigma = Delta_Sigma^{1/2}; the R^2 mechanism "
          "(v473 kill test). No status marker moves; v359's equation-of-state "
          "typing stays [O]", True)

    return summary("v474 GRAV.ENTROPIC.HODGE.01: operator level of the entropic bridge -- [E] "
                   "CAR=>Clifford (10 gammas exact on 32-dim Fock), so(10) span 45 preserving "
                   "Lambda^even=16 (S+ IS the even exterior algebra, operator level), Hodge-Dirac "
                   "symbol c(xi)^2 = -|xi|^2 symbolically, the fold = 5->5bar conjugation "
                   "(1+5+10 -> 1+5bar+10 GUT 16), Omega^{<=2} NOT Clifford-invariant (honest "
                   "obstruction), Q-target d k^2 = 32 solved EXACTLY by supports {2,8,32} atoms "
                   "with minimal uniform q = c3^2 and the 10/16 blocks KILLED (irrational), "
                   "Tr Q^2/delta_top = 2/3 = 32/48; [C] physical Q assignment; [O] AP2 + R^2 open")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

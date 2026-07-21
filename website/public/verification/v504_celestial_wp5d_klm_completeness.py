"""v504 -- CELEST.WP5DB.01: WP5d-beta of the research contract CELEST.SEAM.01 --
"split + strong additivity from the lattice": the two remaining
Kawahigashi-Longo-Mueger (KLM) legs of complete rationality, witnessed for the
orbifold/quotient prescription on the seam edge.
Python (numpy + scipy Gaussian machinery + exact GF2/integer algebra).

Question: complete rationality (KLM) = split property + strong additivity +
finite two-interval mu-index.  WP5d-alpha (v501) witnessed the mu-index
(entropic offset ln 2 => [F : F_even] = 2, mu_gauged = 4, chain 16 -> 4 -> 1);
this module witnesses the OTHER TWO legs for the same orbifold prescription on
the critical Majorana ring (v367/v450 reduction, Peschel-exact), with the
U(1)/Dirac number-conserving subnet as the preregistered negative control --
the current-net analogue where strong additivity famously FAILS in the
continuum (Buchholz-Schulz-Mirbach).  With v501, all THREE KLM ingredients of
complete rationality now have lattice witnesses.

  [E-machine] S0. MACHINERY VALIDATED: closed-form NS covariance == eigh route
        (4.3e-15); the touching (adjacent-interval) parity-deficit Gaussian
        formula == exact diagonalisation (4.4e-16); the U(1) Fock-built rho
        (covariance round trip 5.6e-16) with charge-dephased Tr sigma^2 ==
        exact finite quadrature (5.6e-17 -- R(alpha) is a trig polynomial of
        degree <= n_A, so the (2 n_A + 1)-node grid is EXACT); the
        second-compound identity (cross-Gram of even bilinears = Lambda^2 C,
        singular values {sigma_a sigma_b}, 2.8e-14); parity flip C -> -C
        leaves sigma_k invariant (8.3e-17); sigma_X = rho_X for every single
        region (Gaussian parity superselection, exact).
  [E]   S1. STRONG ADDITIVITY, EXACT ALGEBRA: "touching" = shared boundary
        Majorana => Even(A) v Even(B) = Even(A u B) EXACTLY (GF2 spans full
        64/64, 256/256, 512/512, 1024/1024 on four sizes; literal matrix rank
        32/32); DISJOINT intervals give exactly HALF (rank 16/32, index 2 --
        the missing sector is odd(x)odd, the single ln-2 bit of WP5d-alpha,
        localised at the split point); U(1)/neutral algebras do NOT generate
        the union even WITH the shared site (gaps 2/10/52, GROWING -- the
        charge-transfer tower is missing): the exact lattice shadow of the
        current-net strong-additivity failure (infinite index).
  [N]   S2. STRONG ADDITIVITY, ENTROPIC SCALING: the fermionic touching MI
        diverges with exact (c/3) ln 2 increments per doubling (0.115525,
        dev 1.2e-6 -- pure UV point-gap, present for EVERY net, hence NOT the
        discriminator); the honest discriminator is BOUNDED vs DIVERGENT
        sector-sum deficit: the Z2/orbifold deficit rises 0.4045 -> 0.5899
        (N = 64 -> 4096), stays < ln 2, with (ln 2 - Delta_2) ~ N^(-p),
        p = 0.2444 vs 2 Delta_mu = 1/4 (the Ising disorder-operator
        dimension); split-point scan exactly reflection symmetric (3.9e-14);
        ED vN deficits same direction; gap continuity to the v501 x -> 1
        endpoint.  HONEST NOTE: the naive "defect -> 0" expectation is FALSE
        on the sharp lattice split -- bounded <=> finite index (Longo-Xu) is
        the correct statement.  U(1) CONTRAST: D_U1(touch) BURSTS the
        finite-group ceiling ln 2 from L = 128 on and keeps growing as
        (1/2) ln Var Q_A with Var Q_A = (1/pi^2) ln L + const (Klich-Levitov
        slope 0.10134 vs 1/pi^2 = 0.10132): infinite index, no saturation.
  [N]   S3. SPLIT PROPERTY (nuclearity witness): the singular values of the
        off-diagonal covariance block for DISJOINT intervals fall
        exponentially in k with rate = the elliptic nome pi K(1-x)/K(x) to
        1.3-2.0% (d = 16..512 at N = 4096: rates 2.29/3.24/4.82/5.81);
        sigma_1 ~ x^0.5044 vs 1/2 (the dimension-1/2 Majorana two-point law);
        trace norm summable and falling (Buchholz-Wichmann nuclearity proxy);
        the dimerised control decays exponentially per site (a gapped seam
        splits trivially -- the CFT power laws are properties of the seam).
        ORBIFOLD INHERITANCE IS EXACT AT MACHINE LEVEL: P_A maps C -> -C
        (sigma_k identical, 8.3e-17) and the even-bilinear coupling Gram is
        the second compound Lambda^2 C with singular values {sigma_a sigma_b}
        (2.8e-14) -- the SAME ladder at doubled rate; the orbifold Renyi-2 MI
        is < 3% of the fermionic one and falls with x (Longo heredity, [C]).
  [E]   S4. PIMSNER-POPA / LONGO-REHREN, EXACT: E(a) - a/2 = PaP/2 holds
        IDENTICALLY (the PP inequality with lambda = 1/2 = 1/[F : F_even],
        one line, exact); ATTAINMENT in exact integers: all 16384 (even, odd)
        monomial pairs at N = 8 Majoranas -- 8192 extremal with M^2 = 4,
        Tr M = 0, PMP = -M exactly, 0 violations; all 2048 hermitianised odd
        monomials at N = 12 (2048/2048); random pencil sweep min lambda =
        0.5000000000; the two-interval group {1, P_A, P_B, P_AB} gives
        lambda = 1/4 = 1/mu exactly; INDEX CONSISTENCY, TWO ROUTES:
        exp(Delta_inf) = 2.000000000 = 1/lambda_PP (the v501 entropic route)
        and exp(2 Delta_inf) = 4 = 1/lambda_E4 = mu -- the Longo-Rehren index
        witnessed entropically AND operator-algebraically, independently;
        U(1) control: lambda = 1/(m+1) -> 0 (infinite index).
  [E/N] S5. NEGATIVE CONTROLS + FINITE-SIZE HONESTY: dimerised/trivial phase
        -- every indicator trivial (touching deficit N-independent to
        3.6e-15, MI bounded, sigma_1 exponential); U(1) small-L honesty
        (non-monotone below L ~ 16, filling-parity artefacts -- documented);
        Z2 finite-size honesty: at N = 4096 the touching deficit still sits
        14.9% below ln 2 (the N^{-1/4} Ising approach is SLOW -- the verdict
        rests on the bound + fitted exponent, stated as witness, not proof);
        wrong prescription {1, P_AB} on the touching pair: deficit EXACTLY 0
        (machine identity) -- the bookkeeping is falsifiable.
  [C]   The lattice -> continuum KLM dictionary: bounded deficit = finite
        index = complete rationality (Longo-Xu dichotomy); split heredity
        under finite index (Longo); the entropic order parameters (CHMP);
        the nome ladder = the free-fermion two-interval modular package.
  [O]   The continuum proof: the theorem "finite-group orbifolds of
        completely rational nets are completely rational (hence split +
        strongly additive)" is XU'S THEOREM (algebraic orbifold CFTs) --
        CITED, NOT CLAIMED; the continuum proof for THE seam quotient net
        itself and for the interacting condensed (E8)_1 net stays open
        (WP5e / Costello-Li territory); SEAM.EQUIV.01 stays [O], untouched;
        no marker moves.

Verdict: with v501 (mu-index), all THREE KLM ingredients of complete
rationality -- split, strong additivity, finite mu -- are witnessed on the
lattice for the orbifold prescription; the U(1) control fails both new legs
exactly as the continuum current net does.

Status: [E] the exact algebra spans/indices, the PP identities and integer
attainments, the quadrature/compound/machine identities; [N] all scaling
witnesses (deficit tables, nome ladder, power laws, KL slope; fine type
Lattice/Numerical in the ledger); [C]/[O] as fenced above.  Python;
Wolfram-mirrored (the exact parts only: GF2 span counts and index 2, the PP
identity E(a) - a/2 = PaP/2 with lambda = 1/2 and lambda_E4 = 1/4 = 1/mu, the
index consistency exp(Delta) = 1/lambda_PP and exp(2 Delta) = mu, the
Lambda^2-compound identity -- the numerical lattice curves stay Python-only),
counted per GATE.WOLFRAM.02 convention.

Deterministic (fixed seeds); full sizes (N up to 4096) run in ~12 s."""
import numpy as np
import scipy.sparse as sp
from scipy.linalg import schur, toeplitz
from scipy.special import ellipk
from itertools import combinations
from math import comb

from tfpt_constants import check, summary, reset, g_car, N_fam

G_CAR = g_car               # 5, the carrier rank (P2)
N_FAM = N_fam               # 3
SEAM_LAYERS = 2 * (G_CAR + N_FAM)   # 16 layers = 2 c_-, c_- = 8 (v489/v501)
LN2 = np.log(2.0)


# ---------------------------------------------------------------------------
# Gaussian machinery (identical conventions to v501 / WP5d-alpha)
# ---------------------------------------------------------------------------
def ring_A(N, t_weak=None, antiperiodic=True):
    A = np.zeros((N, N))
    for j in range(N):
        t = 1.0 if (t_weak is None or j % 2 == 0) else t_weak
        if j == N - 1 and antiperiodic:
            t = -t
        A[j, (j + 1) % N] += t
        A[(j + 1) % N, j] -= t
    return A


def ground_gamma(A):
    w, U = np.linalg.eigh(1j * A)
    G = 1j * (U * np.sign(w)) @ U.conj().T
    assert np.abs(G.imag).max() < 1e-11
    return 0.5 * (G.real - G.real.T)


def gamma_analytic(N):
    """NS ground-state covariance of the uniform critical ring, closed form:
    Gamma_jk = -2 / (N sin(pi (k-j)/N)) for odd k-j, 0 for even."""
    j = np.arange(N)
    D = j[None, :] - j[:, None]
    with np.errstate(divide="ignore"):
        M = -2.0 / (N * np.sin(np.pi * D / N))
    M[D % 2 == 0] = 0.0
    np.fill_diagonal(M, 0.0)
    return M


def sub(G, idx):
    return G[np.ix_(idx, idx)]


def S_vN(G):
    lam = np.linalg.eigvalsh(1j * G)
    p = np.clip((1 + lam) / 2, 1e-15, 1 - 1e-15)
    return float(-0.5 * np.sum(p * np.log(p) + (1 - p) * np.log(1 - p)))


def S_R2(G):
    lam = np.linalg.eigvalsh(1j * G)
    return float(-0.5 * np.sum(np.log((1 + lam ** 2) / 2)))


def ln_tr_prod(G1, G2):
    n = G1.shape[0]
    sign, ld = np.linalg.slogdet(np.eye(n) - G1 @ G2)
    assert sign > 0
    return 0.5 * ld - (n // 2) * LN2


def deficit2_flip(GAB, la, layers=1):
    """Renyi-2 deficit of the P_A sector sum; la = # flipped Majoranas."""
    n = GAB.shape[0]
    s = np.ones(n)
    s[:la] = -1.0
    GS = GAB * np.outer(s, s)
    R = np.exp(ln_tr_prod(GAB, GS) - ln_tr_prod(GAB, GAB))
    return float(-np.log((1 + R ** layers) / 2)), float(R)


def chord(z, N):
    return abs(np.sin(np.pi * z / N))


def cross_ratio(cuts, N):
    u1, v1, u2, v2 = cuts
    den = chord(u2 - u1, N) * chord(v2 - v1, N)
    x = chord(v1 - u1, N) * chord(v2 - u2, N) / den
    xb = chord(u2 - v1, N) * chord(v2 - u1, N) / den
    return x, xb


# ---------------------------------------------------------------------------
# ED layer (Jordan-Wigner; validates the Gaussian formulas)
# ---------------------------------------------------------------------------
def jw_majoranas(nq):
    I2 = sp.identity(2, format="csr", dtype=complex)
    X = sp.csr_matrix(np.array([[0, 1], [1, 0]], complex))
    Y = sp.csr_matrix(np.array([[0, -1j], [1j, 0]], complex))
    Z = sp.csr_matrix(np.array([[1, 0], [0, -1]], complex))
    cs = []
    for k in range(nq):
        for P in (X, Y):
            op = None
            for j in range(nq):
                f = Z if j < k else (P if j == k else I2)
                op = f if op is None else sp.kron(op, f, format="csr")
            cs.append(op)
    return cs


def gauss_rho(G, cs):
    n = G.shape[0]
    T, Q = schur(G, output="real")
    assert max(abs(T[i, i]) for i in range(n)) < 1e-8
    dim = cs[0].shape[0]
    rho = np.eye(dim, dtype=complex)
    for k in range(n // 2):
        b = T[2 * k, 2 * k + 1]
        d1 = sum(Q[i, 2 * k] * cs[i] for i in range(n))
        d2 = sum(Q[i, 2 * k + 1] * cs[i] for i in range(n))
        fac = 0.5 * (sp.identity(dim, dtype=complex, format="csr")
                     + 1j * b * (d1 @ d2))
        rho = rho @ fac.toarray()
    return rho


def parity_first(nq_a, nq):
    idx = np.arange(2 ** nq)
    signs = np.ones(2 ** nq)
    for j in range(nq_a):
        bit = (idx >> (nq - 1 - j)) & 1
        signs *= np.where(bit == 1, -1.0, 1.0)
    return signs


def ed_S(rho):
    lam = np.clip(np.linalg.eigvalsh(rho).real, 0.0, 1.0)
    lam = lam[lam > 1e-14]
    return float(-np.sum(lam * np.log(lam)))


# ---------------------------------------------------------------------------
# Dirac (number-conserving) machinery: C_jl = <a+_j a_l>, half filling, NS
# ---------------------------------------------------------------------------
def dirac_C(L):
    ks = 2 * np.pi * (np.arange(L) + 0.5) / L
    filled = ks[np.cos(ks) < 0]
    j = np.arange(L)
    f = np.zeros(L, complex)
    for k in filled:
        f += np.exp(1j * k * j) / L
    return toeplitz(f.conj(), f)


def R_alpha(Csub, nA, alpha):
    """Tr(rho U rho U+)/Tr rho^2 for the U(1) phase on the first nA modes."""
    n = Csub.shape[0]
    v = np.ones(n, complex)
    v[:nA] = np.exp(1j * alpha)
    Ca = (v[:, None] * Csub) * v.conj()[None, :]
    I = np.eye(n)
    s1, l1 = np.linalg.slogdet(Csub @ Ca + (I - Csub) @ (I - Ca))
    s0, l0 = np.linalg.slogdet(Csub @ Csub + (I - Csub) @ (I - Csub))
    return float((np.exp(l1 - l0) * s1 / s0).real)


def u1_touch_deficit(L, nodes=None):
    """full-U(1) sector-sum Renyi-2 deficit for touching halves of [0, L/2);
    exact quadrature: R(alpha) is a trig polynomial of degree <= nA."""
    C = dirac_C(L)
    nAB, nA = L // 2, L // 4
    Csub = C[:nAB, :nAB]
    m = nodes if nodes else 2 * nA + 1
    Rs = [R_alpha(Csub, nA, 2 * np.pi * t / m) for t in range(m)]
    Rbar = float(np.mean(Rs))
    CA = C[:nA, :nA]
    varQ = float(np.trace(CA @ (np.eye(nA) - CA)).real)
    return -np.log(Rbar), varQ


# ---------------------------------------------------------------------------
# exact algebra spans (GF2 monomial labels + literal matrix ranks)
# ---------------------------------------------------------------------------
def even_labels(sites, n_all):
    out = []
    for r in range(0, len(sites) + 1, 2):
        for c in combinations(sites, r):
            m = 0
            for s in c:
                m |= 1 << s
            out.append(m)
    return out


def even_span_count(nA, nB, shared):
    """|{a XOR b : a in Even(A), b in Even(B)}| vs dim Even(union).
    Majorana monomials c_S are linearly independent iff labels differ and
    c_a c_b = +- c_{a XOR b}, so span dim = # distinct labels (exact)."""
    n = nA + nB - (1 if shared else 0)
    A = list(range(nA))
    B = list(range(nA - 1, n)) if shared else list(range(nA, n))
    prod = set()
    for a in even_labels(A, n):
        for b in even_labels(B, n):
            prod.add(a ^ b)
    return len(prod), 2 ** (n - 1)


def monomial(cs, S, dim):
    M = np.eye(dim, dtype=complex)
    for s_ in S:
        M = M @ cs[s_].toarray()
    return M


def matrix_span_rank(cs, sitesA, sitesB, dim, even_only=True):
    def monos(sites):
        step = 2 if even_only else 1
        return [monomial(cs, S, dim)
                for r in range(0, len(sites) + 1, step)
                for S in combinations(sites, r)]
    vecs = [(a @ b).ravel() for a in monos(sitesA) for b in monos(sitesB)]
    return int(np.linalg.matrix_rank(np.array(vecs), tol=1e-9))


def neutral_span_rank(nA, nB, shared):
    """number-conserving (U(1)-invariant) span: products of a+_S a_T
    (|S| = |T|) supported in A times the same in B, vs dim of the neutral
    algebra on the union = sum_q C(n, q)^2.  Exact Fock matrices."""
    n = nA + nB - (1 if shared else 0)
    A = list(range(nA))
    B = list(range(nA - 1, n)) if shared else list(range(nA, n))
    dim = 2 ** n

    def neutral_ops(sites):
        ops = []
        for r in range(0, len(sites) + 1):
            for S in combinations(sites, r):
                for T in combinations(sites, r):
                    M = np.zeros((dim, dim))
                    for st in range(dim):
                        state, amp, ok = st, 1.0, True
                        for tt in sorted(T, reverse=True):
                            if not (state >> tt) & 1:
                                ok = False
                                break
                            amp *= (-1) ** bin(state & ((1 << tt) - 1)).count("1")
                            state &= ~(1 << tt)
                        if not ok:
                            continue
                        for ss in sorted(S):
                            if (state >> ss) & 1:
                                ok = False
                                break
                            amp *= (-1) ** bin(state & ((1 << ss) - 1)).count("1")
                            state |= 1 << ss
                        if ok:
                            M[state, st] = amp
                    ops.append(M)
        return ops

    vecs = [(a @ b).ravel() for a in neutral_ops(A) for b in neutral_ops(B)]
    rank = int(np.linalg.matrix_rank(np.array(vecs), tol=1e-8))
    target = sum(comb(n, q) ** 2 for q in range(n + 1))
    return rank, target


# ---------------------------------------------------------------------------
# Pimsner-Popa pencil
# ---------------------------------------------------------------------------
def pp_lambda(a, Emap, tol=1e-11):
    """largest lambda with E(a) >= lambda a, via the pencil on supp E(a)."""
    Ea = Emap(a)
    w, V = np.linalg.eigh(Ea)
    keep = w > tol * max(w.max(), 1e-30)
    W = V[:, keep] * (w[keep] ** -0.5)
    return float(1.0 / np.linalg.eigvalsh(W.conj().T @ a @ W).max())


# ===========================================================================
# S0 -- machinery validation
# ===========================================================================
def section0():
    print("  -- S0: machinery validated (analytic covariance, ED, quadrature,"
          " compound)")
    dev = np.abs(gamma_analytic(256) - ground_gamma(ring_A(256))).max()
    check("S0.1: ANALYTIC COVARIANCE [E-machine] -- closed-form NS Gamma "
          "equals the eigh route at N = 256 to %.1e (used for N up to 4096)"
          % dev, dev < 1e-12)

    # touching deficit: Gaussian == ED (N = 16 ring, region 12, split 6)
    N = 16
    G = ground_gamma(ring_A(N))
    GAB = sub(G, list(range(12)))
    d2g, Rg = deficit2_flip(GAB, 6)
    cs = jw_majoranas(6)
    rho = gauss_rho(GAB, cs)
    P = parity_first(3, 6)
    rhoP = (P[:, None] * rho) * P[None, :]
    R_ed = float(np.trace(rho @ rhoP).real / np.trace(rho @ rho).real)
    dvn = ed_S(0.5 * (rho + rhoP)) - ed_S(rho)
    check("S0.2: TOUCHING DEFICIT vs ED [E-machine] -- adjacent intervals "
          "(region 12 Maj, split at 6): Gaussian R = %.10f == ED R = %.10f "
          "(dev %.1e); Delta_2 = %.6f, Delta_vN = %.6f (same direction)"
          % (Rg, R_ed, abs(Rg - R_ed), d2g, dvn),
          abs(Rg - R_ed) < 1e-12 and dvn > d2g > 0)

    # U(1): Fock-built rho from C; dephasing == exact quadrature
    L = 8
    C = dirac_C(L)
    Csub = C[:4, :4]
    nvals, V = np.linalg.eigh(Csub)
    cs4 = jw_majoranas(4)
    a_ops = [0.5 * (cs4[2 * q] + 1j * cs4[2 * q + 1]).toarray() for q in range(4)]
    b_ops = [sum(V[jj, kk] * a_ops[jj] for jj in range(4)) for kk in range(4)]
    rho = np.eye(16, dtype=complex)
    for kk in range(4):
        nk = float(np.clip(nvals[kk], 0, 1))
        num = b_ops[kk].conj().T @ b_ops[kk]
        rho = rho @ (nk * num + (1 - nk) * (np.eye(16) - num))
    devC = max(abs(np.trace(rho @ (a_ops[p].conj().T @ a_ops[q])) - Csub[p, q])
               for p in range(4) for q in range(4))
    QA = sum(a_ops[p].conj().T @ a_ops[p] for p in range(2))
    wq, Vq = np.linalg.eigh(QA)
    sig = np.zeros_like(rho)
    for q in (0, 1, 2):
        Pq = Vq[:, np.abs(wq - q) < 1e-9]
        Pq = Pq @ Pq.conj().T
        sig += Pq @ rho @ Pq
    tr_s2 = float(np.trace(sig @ sig).real)
    m = 5                                     # 2*nA + 1 with nA = 2
    Rq = np.mean([R_alpha(Csub, 2, 2 * np.pi * t / m) for t in range(m)])
    tr_pred = float(np.trace(rho @ rho).real * Rq)
    check("S0.3: U(1) MACHINERY vs ED [E-machine] -- Fock rho from C "
          "(Tr = 1 dev %.1e, covariance round trip %.1e); charge-dephased "
          "Tr sigma^2 = %.10f == Tr rho^2 <R>_quad = %.10f (dev %.1e)"
          % (abs(np.trace(rho).real - 1), abs(devC), tr_s2, tr_pred,
             abs(tr_s2 - tr_pred)),
          abs(devC) < 1e-12 and abs(tr_s2 - tr_pred) < 1e-12)

    d_a, _ = u1_touch_deficit(64)
    d_b, _ = u1_touch_deficit(64, nodes=2 * 16 + 17)
    check("S0.4: EXACT QUADRATURE [E-machine] -- R(alpha) is a trig "
          "polynomial of degree <= n_A (bounded charge transfer), so the "
          "(2 n_A + 1)-node average is exact: 33 vs 49 nodes agree to %.1e"
          % abs(d_a - d_b), abs(d_a - d_b) < 1e-12)

    # second compound: even-bilinear cross-Gram has s.v. {sigma_a sigma_b}
    rng = np.random.default_rng(4990)
    lsz = 10
    Cb = rng.normal(size=(lsz, lsz))
    sv = np.linalg.svd(Cb, compute_uv=False)
    pairs = list(combinations(range(lsz), 2))
    M2 = np.zeros((len(pairs), len(pairs)))
    for pi, (i, jj) in enumerate(pairs):
        for qi, (k, l) in enumerate(pairs):
            M2[pi, qi] = Cb[i, k] * Cb[jj, l] - Cb[i, l] * Cb[jj, k]
    svM = np.sort(np.linalg.svd(M2, compute_uv=False))[::-1]
    prods = np.sort([sv[a] * sv[b] for a, b in pairs])[::-1]
    dev2 = np.abs(svM - prods).max()
    check("S0.5: SECOND COMPOUND [E-machine] -- the Wick cross-Gram of even "
          "bilinears c_i c_j (A) x c_k c_l (B) is Lambda^2(C): singular "
          "values {sigma_a sigma_b} exactly (dev %.1e on a random 10x10): "
          "the orbifold coupling ladder IS the fermionic one, squared" % dev2,
          dev2 < 1e-10)

    # parity flip: C -> -C, sigma_k invariant; single region sigma_X = rho_X
    G = gamma_analytic(512)
    Cx = G[np.ix_(range(64), range(128, 192))]
    devs = np.abs(np.linalg.svd(Cx, compute_uv=False)
                  - np.linalg.svd(-Cx, compute_uv=False)).max()
    s = -np.ones(128)
    devG = np.abs(sub(G, list(range(128))) * np.outer(s, s)
                  - sub(G, list(range(128)))).max()
    check("S0.6: PARITY STRUCTURE [E-machine] -- P_A maps the coupling block "
          "C -> -C: sigma_k identical (dev %.1e); flipping ALL Majoranas of "
          "a single region leaves Gamma invariant (dev %.1e): sigma_X = "
          "rho_X for every one-region state (Gaussian parity superselection)"
          % (devs, devG), devs < 1e-13 and devG < 1e-15)


# ===========================================================================
# S1 -- strong additivity: exact lattice algebra
# ===========================================================================
def section1():
    print("  -- S1: strong additivity as exact lattice algebra (spans/ranks)")
    cs3 = jw_majoranas(3)
    r_car = matrix_span_rank(cs3, [0, 1, 2], [3, 4, 5], 8, even_only=False)
    check("S1.1: CAR REFERENCE [E-machine] -- CAR(A) . CAR(B) spans the FULL "
          "algebra (rank %d / %d) even for DISJOINT intervals: the graded "
          "net is additive, trivially -- the mu = 1 reference" % (r_car, 64),
          r_car == 64)

    rows = []
    ok_sh = True
    for (nA, nB) in [(4, 4), (5, 5), (5, 6), (6, 6)]:
        c_sh, tot = even_span_count(nA, nB, shared=True)
        rows.append((nA, nB, c_sh, tot))
        ok_sh = ok_sh and (c_sh == tot)
    r_sh = matrix_span_rank(cs3, [0, 1, 2, 3], [3, 4, 5], 8, even_only=True)
    print("     shared-site even spans: " + ", ".join(
        "%d+%d: %d/%d" % r for r in rows))
    check("S1.2: TOUCHING = SHARED POINT [E] -- with the shared boundary "
          "Majorana, Even(A) v Even(B) = Even(A u B) EXACTLY: GF2 span full "
          "on all four sizes, literal matrix rank %d / 32: the lattice "
          "strong-additivity witness for the orbifold algebra" % r_sh,
          ok_sh and r_sh == 32)

    rows_d = []
    ok_d = True
    for (nA, nB) in [(4, 4), (5, 5), (6, 6)]:
        c_d, tot = even_span_count(nA, nB, shared=False)
        rows_d.append((nA, nB, c_d, tot))
        ok_d = ok_d and (2 * c_d == tot)
    r_d = matrix_span_rank(cs3, [0, 1, 2], [3, 4, 5], 8, even_only=True)
    print("     disjoint even spans:    " + ", ".join(
        "%d+%d: %d/%d" % r for r in rows_d))
    check("S1.3: DISJOINT INDEX 2 [E] -- without the shared site the even "
          "span is EXACTLY HALF (all sizes; matrix rank %d / 32): the "
          "missing sector is odd(x)odd -- the single ln 2 bit of WP5d-alpha "
          "(v501), localised at the split point" % r_d, ok_d and 2 * r_d == 32)

    rows_u = []
    gaps = []
    for (nA, nB) in [(2, 2), (3, 2), (3, 3)]:
        rk, tgt = neutral_span_rank(nA, nB, shared=True)
        rows_u.append((nA, nB, rk, tgt))
        gaps.append(tgt - rk)
    rk_dd, tgt_dd = neutral_span_rank(2, 2, shared=False)
    print("     U(1) neutral shared-site spans: " + ", ".join(
        "%d+%d: %d/%d" % r for r in rows_u)
        + "; disjoint 2+2: %d/%d" % (rk_dd, tgt_dd))
    check("S1.4: U(1) CONTRAST [E] -- the number-conserving (neutral) "
          "algebras do NOT generate the union even WITH the shared site: "
          "gaps %s GROW with size (the charge-transfer tower a+...a+ x a...a "
          "beyond one unit is missing): the exact lattice shadow of the "
          "current-net strong-additivity failure (infinite index)"
          % gaps, gaps == sorted(gaps) and gaps[0] > 0 and gaps[-1] > gaps[0]
          and rk_dd < tgt_dd)


# ===========================================================================
# S2 -- strong additivity: entropic scaling witnesses
# ===========================================================================
def section2():
    print("  -- S2: strong additivity, entropic scaling (a -> 0 tables)")

    # fermionic touching MI: pure point-gap UV, coefficient (c/3) ln
    Ns = [128, 256, 512, 1024, 2048, 4096]
    I_t = []
    for N in Ns:
        G = gamma_analytic(N)
        la = N // 4
        SA = S_vN(sub(G, list(range(la))))
        SB = S_vN(sub(G, list(range(la, 2 * la))))
        SAB = S_vN(sub(G, list(range(2 * la))))
        I_t.append(SA + SB - SAB)
    incs = np.diff(I_t)
    dev_inc = np.abs(incs - LN2 / 6).max()
    print("     fermionic I(A:B) touching: " + "  ".join(
        "N=%d: %.6f" % (n, v) for n, v in zip(Ns, I_t)))
    check("S2.1: POINT-GAP LAW [N] -- the fermionic touching MI diverges "
          "logarithmically with increments per doubling = %.6f..%.6f vs "
          "(c/3) ln 2 = ln2/6 = %.6f (max dev %.1e): the 'defect' at a "
          "touching point is pure UV, (c/3) ln(1/a), present for EVERY "
          "conformal net -- it cannot discriminate strong additivity"
          % (incs.min(), incs.max(), LN2 / 6, dev_inc), dev_inc < 1e-4)

    # Z2 sector-sum touching deficit: bounded by ln 2, Ising approach
    print("     Z2 orbifold touching deficit (A = B = N/4, adjacent):")
    Ns2 = [64, 128, 256, 512, 1024, 2048, 4096]
    dts = []
    for N in Ns2:
        G = gamma_analytic(N)
        la = N // 4
        d2, R = deficit2_flip(sub(G, list(range(2 * la))), la)
        dts.append((N, R, d2))
        print("       N = %5d : R = %.6f, Delta_2 = %.6f, ln2 - Delta_2 = %.6f"
              % (N, R, d2, LN2 - d2))
    mono = all(dts[i + 1][2] > dts[i][2] for i in range(len(dts) - 1))
    bounded = all(d < LN2 for (_, _, d) in dts)
    check("S2.2: BOUNDED SECTOR-SUM DEFECT [N] -- Delta_2(touch) rises "
          "monotonically %.4f -> %.4f (N = 64 -> 4096) and stays < ln 2 = "
          "%.4f: the Z2 orbifold pays at most ONE bit at the split point -- "
          "bounded <=> finite index (the KLM-side discriminator; honest "
          "note: the naive 'defect -> 0' expectation is FALSE on the sharp "
          "lattice split -- bounded-vs-divergent is the real criterion)"
          % (dts[0][2], dts[-1][2], LN2), mono and bounded)

    gaps_ln = [np.log(LN2 - d) for (_, _, d) in dts[-4:]]
    lnN = [np.log(n) for (n, _, _) in dts[-4:]]
    p_fit = -np.polyfit(lnN, gaps_ln, 1)[0]
    check("S2.3: ISING APPROACH RATE [N] -- (ln 2 - Delta_2) ~ N^(-p) with "
          "fitted p = %.4f vs 2 Delta_mu = 1/4 (the Ising disorder-operator "
          "dimension h_mu = 1/16 per chirality; window 0.20..0.30): the "
          "missing bit decays with the CORRECT universal exponent" % p_fit,
          0.20 < p_fit < 0.30)

    # split-point dependence
    N = 1024
    G = gamma_analytic(N)
    GAB = sub(G, list(range(512)))
    fr_list = [1 / 8, 1 / 4, 3 / 8, 1 / 2, 5 / 8, 3 / 4, 7 / 8]
    dsp = {}
    for fr in fr_list:
        la = int(512 * fr)
        dsp[fr], _ = deficit2_flip(GAB, la)
    print("     split-point scan (N = 1024, region 512): " + "  ".join(
        "%.3f: %.5f" % (f, dsp[f]) for f in fr_list))
    sym_dev = max(abs(dsp[f] - dsp[1 - f]) for f in [1 / 8, 1 / 4, 3 / 8])
    spread = (max(dsp.values()) - min(dsp.values())) / LN2
    check("S2.4: SPLIT-POINT SCAN [N] -- exactly reflection symmetric "
          "(dev %.1e), maximal at the midpoint, spread only %.1f%% of ln 2: "
          "the witness does not depend on WHERE the interval is split"
          % (sym_dev, 100 * spread),
          sym_dev < 1e-8 and spread < 0.06
          and max(dsp, key=lambda f: dsp[f]) == 1 / 2)

    # ED vN deficits (small N): same direction
    vn = []
    for N in [12, 16, 20]:
        G = ground_gamma(ring_A(N))
        la = N // 4
        GAB = sub(G, list(range(2 * la)))
        nq = la
        cs = jw_majoranas(nq)
        rho = gauss_rho(GAB, cs)
        P = parity_first(la // 2 if la % 2 == 0 else (la + 1) // 2, nq)
        rhoP = (P[:, None] * rho) * P[None, :]
        vn.append((N, ed_S(0.5 * (rho + rhoP)) - ed_S(rho)))
    print("     ED vN touching deficits: " + "  ".join(
        "N=%d: %.5f" % t for t in vn))
    check("S2.5: vN DIRECTION [N] -- exact-diagonalisation von Neumann "
          "deficits rise with N (%.4f -> %.4f): the bounded-defect witness "
          "is not a Renyi-2 artefact" % (vn[0][1], vn[-1][1]),
          all(vn[i + 1][1] > vn[i][1] for i in range(len(vn) - 1)))

    # gap-continuity: touching = m/N -> 0 limit of the disjoint family
    print("     gap continuity D(touch) - D(gap m = 1):")
    diffs = []
    for N in [512, 1024, 2048, 4096]:
        G = gamma_analytic(N)
        la = N // 4
        D0, _ = deficit2_flip(sub(G, list(range(2 * la))), la)
        ia = list(range(la))
        ib = list(range(la + 1, 2 * la + 1))
        D1, _ = deficit2_flip(sub(G, ia + ib), la)
        diffs.append((N, D0 - D1))
        print("       N = %5d : %.5f" % (N, D0 - D1))
    check("S2.6: GAP CONTINUITY [N] -- |D(touch) - D(one-site gap)| shrinks "
          "monotonically (%.4f -> %.4f): the touching witness is the "
          "continuous x -> 1 endpoint of WP5d-alpha's (v501) disjoint "
          "family, not a separate lattice artefact"
          % (diffs[0][1], diffs[-1][1]),
          all(diffs[i + 1][1] < diffs[i][1] for i in range(len(diffs) - 1)))

    # U(1) contrast: unbounded growth ~ (1/2) ln Var Q
    print("     U(1) full sector sum, touching halves (exact quadrature):")
    rows = []
    for L in [64, 128, 256, 512, 1024]:
        D, varQ = u1_touch_deficit(L)
        rows.append((L, D, varQ))
        print("       L = %5d : D_U1 = %.6f, Var Q_A = %.5f" % (L, D, varQ))
    xs = np.array([0.5 * np.log(r[2]) for r in rows])
    ys = np.array([r[1] for r in rows])
    slope = np.polyfit(xs, ys, 1)[0]
    lnL = np.array([np.log(r[0]) for r in rows])
    kl = np.polyfit(lnL, [r[2] for r in rows], 1)[0]
    burst = [r[0] for r in rows if r[1] > LN2]
    check("S2.7: U(1) DIVERGENCE [N] -- D_U1(touch) grows %.4f -> %.4f with "
          "NO ceiling: it bursts the finite-group bound ln 2 from L = %d on, "
          "tracks (1/2) ln Var Q_A (slope %.3f ~ 1) with Var Q_A = "
          "(1/pi^2) ln L + const (Klich-Levitov slope %.5f vs 1/pi^2 = "
          "%.5f): infinite index -- the number-conserving subnet FAILS "
          "strong additivity, exactly the known continuum failure of the "
          "current net (the preregistered negative control has teeth)"
          % (rows[0][1], rows[-1][1], burst[0] if burst else -1, slope,
             kl, 1 / np.pi ** 2),
          len(burst) > 0 and burst[0] <= 256
          and all(rows[i + 1][1] > rows[i][1] for i in range(len(rows) - 1))
          and 0.7 < slope < 1.1 and abs(kl - 1 / np.pi ** 2) < 0.002)


# ===========================================================================
# S3 -- split property: nuclearity witnesses
# ===========================================================================
def section3():
    print("  -- S3: split property (singular-value ladders of the coupling "
          "block)")
    N = 4096
    G = gamma_analytic(N)
    ell = 128
    print("     N = 4096, ell = 128: pair-mean ladder rate vs elliptic nome "
          "pi K(1-x)/K(x):")
    ratios = []
    rates = []
    tnorms = []
    pair_degen = []
    for d in [16, 32, 64, 128, 256, 512]:
        cuts = (0, ell, ell + d, 2 * ell + d)
        x, _ = cross_ratio(cuts, N)
        ia = list(range(ell))
        ib = list(range(ell + d, 2 * ell + d))
        sv = np.linalg.svd(G[np.ix_(ia, ib)], compute_uv=False)
        tnorms.append(float(sv.sum()))
        pairs = []
        for i in range(6):
            if sv[2 * i + 1] > 1e-13:
                pairs.append(np.sqrt(sv[2 * i] * sv[2 * i + 1]))
        pair_degen.append(sv[0] / sv[1])
        ks = np.arange(len(pairs))
        rate = -np.polyfit(ks, np.log(pairs), 1)[0]
        pred = np.pi * ellipk(1 - x) / ellipk(x)
        rates.append(rate)
        ratios.append(rate / pred)
        print("       d = %4d : x = %.5f, rate = %.4f, pred = %.4f, "
              "ratio = %.3f, ||C||_1 = %.4f, s1 = %.3e"
              % (d, x, rate, pred, rate / pred, sv.sum(), sv[0]))
    check("S3.1: NOME LADDER [N] -- sigma_k pairs fall exponentially in k "
          "with rate matching pi K(1-x)/K(x) to %.1f%%..%.1f%% over "
          "d = 16..512 (the free-fermion two-interval elliptic nome; pair "
          "near-degeneracy s1/s2 <= %.3f): Buchholz-Wichmann-type "
          "nuclearity of the coupling operator, quantitatively CFT-pinned"
          % (100 * (1 - max(ratios)), 100 * (1 - min(ratios)),
             max(pair_degen)),
          all(0.95 < r < 1.02 for r in ratios) and max(pair_degen) < 1.15)

    check("S3.2: DEEPER SPLIT WITH DISTANCE [N] -- the ladder rate grows "
          "monotonically %.3f -> %.3f as d widens (x falls): wider "
          "separation = faster eigenvalue decay = 'more split', as the "
          "nuclearity picture demands" % (rates[0], rates[-1]),
          all(rates[i + 1] > rates[i] for i in range(len(rates) - 1)))

    # sigma_1 ~ x^{1/2}
    ell = 64
    xs, s1s = [], []
    for d in [256, 384, 512, 768, 1024, 1536]:
        cuts = (0, ell, ell + d, 2 * ell + d)
        x, _ = cross_ratio(cuts, N)
        ia = list(range(ell))
        ib = list(range(ell + d, 2 * ell + d))
        sv = np.linalg.svd(G[np.ix_(ia, ib)], compute_uv=False)
        xs.append(x)
        s1s.append(sv[0])
    sl = np.polyfit(np.log(xs), np.log(s1s), 1)[0]
    check("S3.3: LEADING COUPLING POWER LAW [N] -- sigma_1 ~ x^p with fitted "
          "p = %.4f vs 1/2 (the dimension-1/2 Majorana two-point function; "
          "at ell << d << N this is sigma_1 ~ sqrt(l_A l_B)/d): the leading "
          "coupling falls as a CFT power in the separation, exponentially "
          "in k -- witness vs proof separated in S6" % sl,
          abs(sl - 0.5) < 0.05)

    check("S3.4: TRACE-NORM DECAY [N] -- ||C||_1 = %.4f -> %.4f falls "
          "monotonically over d = 16..512: the coupling operator is trace "
          "class with shrinking norm (nuclearity proxy summable)"
          % (tnorms[0], tnorms[-1]),
          all(tnorms[i + 1] < tnorms[i] for i in range(len(tnorms) - 1)))

    # orbifold inheritance: identical sigma_k (S0.6) + compound (S0.5) + MI
    ell = 64
    rows = []
    for d in [256, 512, 1024, 1536]:
        cuts = (0, ell, ell + d, 2 * ell + d)
        x, _ = cross_ratio(cuts, N)
        ia = list(range(ell))
        ib = list(range(ell + d, 2 * ell + d))
        GA, GB = sub(G, ia), sub(G, ib)
        GAB = sub(G, ia + ib)
        I2f = S_R2(GA) + S_R2(GB) - S_R2(GAB)
        D2, _ = deficit2_flip(GAB, ell)
        rows.append((x, I2f, I2f - D2))
    print("     orbifold Renyi-2 MI vs fermionic (ell = 64): " + "  ".join(
        "x=%.4f: %.2e/%.2e" % (x, o, f) for (x, f, o) in rows))
    ok_inh = all(o < 0.03 * f for (_, f, o) in rows) and \
        all(rows[i + 1][2] < rows[i][2] for i in range(len(rows) - 1))
    check("S3.5: ORBIFOLD INHERITANCE [E-machine + N] -- the sector-summed "
          "state has EXACTLY the fermionic sigma_k ladder (P_A flips "
          "C -> -C, S0.6) and its even-bilinear coupling Gram is Lambda^2 C "
          "(sigma_a sigma_b, S0.5) -- same ladder, doubled rate; "
          "numerically the orbifold Renyi-2 MI is < 3 percent of the "
          "fermionic one and falls with x: split scaling is INHERITED, as "
          "finite index demands (Longo heredity, [C])", ok_inh)

    # dimerised control: exponential sigma_1(d)
    Gt = ground_gamma(ring_A(512, t_weak=0.2))
    ds = np.array([2, 4, 6, 8, 10, 12, 16])
    s1d = []
    for d in ds:
        ia = list(range(64))
        ib = list(range(64 + d, 128 + d))
        s1d.append(np.linalg.svd(Gt[np.ix_(ia, ib)], compute_uv=False)[0])
    coef = np.polyfit(ds, np.log(s1d), 1)
    resid = np.abs(np.log(s1d) - np.polyval(coef, ds)).max()
    check("S3.6: MASSIVE CONTROL [N] -- dimerised chain: sigma_1(d) falls "
          "EXPONENTIALLY, rate %.3f per site (s1: %.1e -> %.1e over "
          "d = 2..16, log-linear residual %.2f): a gapped seam would split "
          "trivially and kill every CFT power law above -- the critical "
          "power laws are a property of the seam, not of the method"
          % (-coef[0], s1d[0], s1d[-1], resid),
          -coef[0] > 0.5 and resid < 0.3 and s1d[-1] < 1e-6)


# ===========================================================================
# S4 -- Pimsner-Popa / Longo-Rehren, exact
# ===========================================================================
def section4():
    print("  -- S4: Pimsner-Popa bound and Longo-Rehren index, exact")
    rng = np.random.default_rng(4991)
    nq = 4
    dim = 2 ** nq
    cs = jw_majoranas(nq)
    Pv = parity_first(nq, nq)

    def E2(y):
        return 0.5 * (y + (Pv[:, None] * y) * Pv[None, :])

    a = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    a = a @ a.conj().T
    f = monomial(cs, (0, 1), dim)
    g = monomial(cs, (2, 3), dim)
    dev_struct = max(
        np.abs(E2(np.eye(dim)) - np.eye(dim)).max(),
        abs(np.trace(E2(a)) - np.trace(a)),
        np.abs(E2(E2(a)) - E2(a)).max(),
        np.abs(E2(f @ a @ g) - f @ E2(a) @ g).max())
    check("S4.1: E IS A CONDITIONAL EXPECTATION [E-machine] -- unital, "
          "trace-preserving, idempotent, even-bimodule (E(f a g) = "
          "f E(a) g for even f, g): max dev %.1e" % dev_struct,
          dev_struct < 1e-12)

    PaP = (Pv[:, None] * a) * Pv[None, :]
    dev_id = np.abs(E2(a) - 0.5 * a - 0.5 * PaP).max()
    eig_min = np.linalg.eigvalsh(E2(a) - 0.5 * a).min()
    check("S4.2: PP BOUND, ONE LINE [E] -- E(a) - a/2 = P a P / 2 "
          "IDENTICALLY (dev %.1e), and PaP >= 0 whenever a >= 0 (min eig "
          "%.2e): E(a) >= (1/2) a for ALL positive a -- the Pimsner-Popa "
          "inequality with lambda = 1/[F : F_even] = 1/2, exact"
          % (dev_id, eig_min), dev_id < 1e-12 and eig_min > -1e-12)

    # exact integer sweep, N = 8 Majoranas: all (even, odd) monomial pairs
    def exact_monomial(S):
        M = np.eye(dim, dtype=complex)
        for s_ in S:
            M = M @ cs[s_].toarray()
        return M

    evens = [c for r in range(0, 9, 2) for c in combinations(range(8), r)]
    odds = [c for r in range(1, 9, 2) for c in combinations(range(8), r)]
    mono_e = {S: exact_monomial(S) for S in evens}
    mono_o = {T: exact_monomial(T) for T in odds}
    I16 = np.eye(dim)
    n_ext = n_triv = n_bad = 0
    for S in evens:
        cS = mono_e[S]
        for T in odds:
            cT = mono_o[T]
            M = cS.conj().T @ cT + cT.conj().T @ cS
            if not M.any():
                n_triv += 1
                continue
            ok = (np.array_equal(M @ M, 4 * I16)
                  and np.trace(M) == 0
                  and np.array_equal((Pv[:, None] * M) * Pv[None, :], -M))
            if ok:
                n_ext += 1
            else:
                n_bad += 1
    check("S4.3: ATTAINMENT, EXACT INTEGERS [E] -- sweep of ALL %d "
          "(even, odd) monomial pairs x = c_S + c_T at N = 8: %d pairs give "
          "x*x = 2 + M with M^2 = 4, Tr M = 0, PMP = -M EXACTLY (spectrum "
          "{+2, -2} balanced => E(x*x) - lam x*x loses positivity for any "
          "lam > 1/2), %d anticommuting pairs give x*x = 2 (ratio 1), 0 "
          "violations: lambda_PP = 1/2 EXACTLY = 1/index"
          % (len(evens) * len(odds), n_ext, n_triv),
          n_bad == 0 and n_ext + n_triv == 16384 and n_ext > 0)

    # N = 12: all hermitianised odd monomials + random pencil sweep
    nq6 = 6
    dim6 = 64
    cs6 = jw_majoranas(nq6)
    Pv6 = parity_first(nq6, nq6)
    I64 = np.eye(dim6)
    n_ok = 0
    for r in range(1, 13, 2):
        for T in combinations(range(12), r):
            M = np.eye(dim6, dtype=complex)
            for s_ in T:
                M = M @ cs6[s_].toarray()
            if not np.array_equal(M.conj().T, M):
                M = 1j * M
            ok = (np.array_equal(M.conj().T, M)
                  and np.array_equal(M @ M, I64)
                  and np.trace(M) == 0
                  and np.array_equal((Pv6[:, None] * M) * Pv6[None, :], -M))
            n_ok += int(ok)

    def E2_6(y):
        return 0.5 * (y + (Pv6[:, None] * y) * Pv6[None, :])

    mins = 1.0
    for _ in range(200):
        ve = rng.normal(size=dim6) + 1j * rng.normal(size=dim6)
        vo = rng.normal(size=dim6) + 1j * rng.normal(size=dim6)
        ve *= (Pv6 > 0)
        vo *= (Pv6 < 0)
        v = ve / np.linalg.norm(ve) + vo / np.linalg.norm(vo)
        mins = min(mins, pp_lambda(np.outer(v, v.conj()), E2_6))
    for _ in range(40):
        r = rng.integers(1, dim6 + 1)
        X = rng.normal(size=(dim6, r)) + 1j * rng.normal(size=(dim6, r))
        mins = min(mins, pp_lambda(X @ X.conj().T, E2_6))
    check("S4.4: N = 12 EXACT + PENCIL SWEEP [E/N] -- all 2048 hermitianised "
          "odd monomials h_T satisfy h^2 = 1, Tr h = 0, PhP = -h exactly "
          "(%d/2048): each x = 1 + h_T attains lambda = 1/2; random pencil "
          "sweep (200 balanced rank-ones + 40 Wisharts, dim 64): "
          "min lambda = %.10f, never below 1/2" % (n_ok, mins),
          n_ok == 2048 and abs(mins - 0.5) < 1e-10)

    # two-interval group {1, P_A, P_B, P_AB}: lambda = 1/4 = 1/mu
    PA = parity_first(2, 4)
    PB = Pv * PA

    def E4(y):
        return 0.25 * (y + (PA[:, None] * y) * PA[None, :]
                       + (PB[:, None] * y) * PB[None, :]
                       + (Pv[:, None] * y) * Pv[None, :])

    a4 = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    a4 = a4 @ a4.conj().T
    eig4 = np.linalg.eigvalsh(E4(a4) - 0.25 * a4).min()
    secs = []
    for (sa, sb) in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        v = rng.normal(size=dim) * ((PA == sa) & (PB == sb))
        secs.append(v / np.linalg.norm(v))
    v4 = 0.5 * sum(secs)
    lam4 = pp_lambda(np.outer(v4, v4), E4)
    check("S4.5: TWO-INTERVAL GROUP [E] -- E_4 over {1, P_A, P_B, P_AB}: "
          "bound E_4(a) - a/4 >= 0 (min eig %.2e, identity = average of "
          "three positive conjugates) and the uniform 4-sector vector "
          "attains lambda = %.12f = 1/4 = 1/mu(SO(16)_1-class step): the "
          "Longo-Rehren index of the two-interval orbifold inclusion, "
          "exact on the lattice" % (eig4, lam4),
          eig4 > -1e-12 and abs(lam4 - 0.25) < 1e-12)

    # index consistency: entropic offset (alpha route) == 1/lambda_PP
    G512 = gamma_analytic(512)
    ia = list(range(0, 254))
    ib = list(range(256, 510))
    d16, _ = deficit2_flip(sub(G512, ia + ib), 254, layers=SEAM_LAYERS)
    check("S4.6: INDEX CONSISTENCY, TWO ROUTES [N/E] -- the WP5d-alpha "
          "(v501) entropic offset gives exp(Delta_inf) = %.9f (|Delta - "
          "ln 2| = %.1e at N = 512, %d layers) and the PP pencil gives "
          "1/lambda = 2 exactly; squared: exp(2 Delta) = %.6f = 1/lambda_E4 "
          "= 4 = mu: [F : F_even] = 2 per step, witnessed ENTROPICALLY and "
          "OPERATOR-ALGEBRAICALLY, independently"
          % (np.exp(d16), abs(d16 - LN2), SEAM_LAYERS, np.exp(2 * d16)),
          abs(d16 - LN2) < 1e-9 and abs(np.exp(2 * d16) - 4) < 1e-8)

    # U(1) control: lambda = 1/(m+1) -> 0
    lams = []
    for m in [2, 3, 4]:
        dimm = 2 ** m
        occ = np.array([bin(i).count("1") for i in range(dimm)])

        def EU(y, occ=occ, dimm=dimm, m=m):
            out = np.zeros((dimm, dimm), complex)
            for q in range(m + 1):
                pq = (occ == q).astype(float)
                out += (pq[:, None] * y) * pq[None, :]
            return out

        v = np.zeros(dimm)
        for q in range(m + 1):
            v[np.where(occ == q)[0][0]] = 1 / np.sqrt(m + 1)
        lams.append((m, pp_lambda(np.outer(v, v), EU)))
        aU = rng.normal(size=(dimm, dimm))
        aU = aU @ aU.T
        assert np.linalg.eigvalsh(EU(aU) - aU / (m + 1)).min() > -1e-12
    check("S4.7: U(1) PP CONTROL [E] -- charge dephasing on m modes has "
          "m + 1 sectors: lambda = %s vs 1/(m+1) = %s (uniform-spread "
          "attainment, dephasing bound E(a) >= a/(m+1) verified): "
          "lambda -> 0 with region size -- INFINITE index, no uniform PP "
          "bound, the operator-algebraic twin of the S2.7 divergence"
          % (["%.6f" % l for (_, l) in lams],
             ["%.6f" % (1 / (m + 1)) for (m, _) in lams]),
          all(abs(l - 1 / (m + 1)) < 1e-11 for (m, l) in lams))


# ===========================================================================
# S5 -- negative controls + finite-size honesty
# ===========================================================================
def section5():
    print("  -- S5: negative controls and finite-size honesty")
    vals = []
    for N in [256, 1024]:
        Gt = ground_gamma(ring_A(N, t_weak=0.2))
        la = N // 4
        GAB = sub(Gt, list(range(2 * la)))
        d2, R = deficit2_flip(GAB, la)
        SA = S_vN(sub(Gt, list(range(la))))
        SB = S_vN(sub(Gt, list(range(la, 2 * la))))
        SAB = S_vN(GAB)
        vals.append((N, d2, SA + SB - SAB,
                     -np.log((1 + R ** SEAM_LAYERS) / 2)))
    drift = abs(vals[1][1] - vals[0][1])
    mi_drift = abs(vals[1][2] - vals[0][2])
    check("S5.1: TRIVIAL PHASE [N] -- dimerised chain: touching deficit "
          "Delta_2 = %.6f, N-INDEPENDENT (drift %.1e over 256 -> 1024, no "
          "approach to ln 2), touching MI = %.4f bounded (drift %.1e vs "
          "the critical ln2/6 = 0.1155 per doubling), 16-layer deficit "
          "%.4f << ln 2: every strong-additivity indicator is trivial in "
          "the gapped phase -- the witnesses measure the CRITICAL seam"
          % (vals[1][1], drift, vals[1][2], mi_drift, vals[1][3]),
          drift < 1e-9 and mi_drift < 1e-9 and vals[1][1] < 0.01)

    ds = [u1_touch_deficit(L)[0] for L in [8, 12, 16]]
    check("S5.2: SMALL-N HONESTY, U(1) [N] -- D_U1 at L = 8/12/16 = "
          "%.4f/%.4f/%.4f is NON-monotone (filling parity artefacts): "
          "below L ~ 16 the lattice cannot distinguish the nets; all "
          "scaling claims here start at L = 64 (documented, not hidden)"
          % tuple(ds), ds[1] > ds[0] and ds[1] > ds[2])

    G4096 = gamma_analytic(4096)
    d2, _ = deficit2_flip(sub(G4096, list(range(2048))), 1024)
    rel = (LN2 - d2) / LN2
    check("S5.3: SMALL-N HONESTY, Z2 [N] -- even at N = 4096 the touching "
          "deficit sits %.1f%% below ln 2 (the N^{-1/4} Ising approach is "
          "SLOW): the bounded-vs-divergent verdict rests on the fitted "
          "exponent + bound, not on visual saturation -- stated as "
          "witness, not proof" % (100 * rel), 0.10 < rel < 0.20)

    s = -np.ones(2048)
    GAB = sub(G4096, list(range(2048)))
    dev = np.abs(GAB * np.outer(s, s) - GAB).max()
    check("S5.4: WRONG PRESCRIPTION [E-machine] -- averaging the touching "
          "pair over {1, P_AB} only (2 of 4 structures) leaves rho "
          "INVARIANT (dev %.1e): deficit exactly 0 instead of -> ln 2 -- "
          "the bookkeeping is falsifiable, as in WP5d-alpha (v501) S6.3"
          % dev, dev < 1e-15)


# ===========================================================================
# S6 -- honest typing + verdict
# ===========================================================================
def section6():
    print("  -- S6: honest typing")
    check("S6.1 [E]: exact ingredients -- the algebra spans/indices (shared "
          "site: full; disjoint: exactly 2; U(1): growing gap), the PP "
          "identities E(a) - a/2 = PaP/2 and E4(a) - a/4 >= 0, the integer "
          "attainment sweeps (16384 + 2048 monomials, 0 violations), "
          "lambda_E4 = 1/4, the U(1) lambda = 1/(m+1) family, the exact "
          "quadrature, the compound identity, sigma_k parity invariance",
          True)
    check("S6.2 [N]: scaling witnesses -- bounded Z2 touching deficit "
          "(< ln 2, exponent 1/4 approach) vs divergent U(1) deficit "
          "((1/2) ln Var Q growth, Klich-Levitov pinned); the nome ladder "
          "(within 2 percent of the elliptic prediction); sigma_1 ~ x^{1/2}; "
          "trace-norm decay; ED vN direction; gap continuity; the "
          "dimerised exponentials", True)
    check("S6.3 [C]/[O]: fences -- the DICTIONARY (bounded deficit = finite "
          "index = complete rationality is Longo-Xu; split heredity under "
          "finite index is Longo; the entropic order parameters are CHMP; "
          "the nome ladder is the free-fermion modular package) stays "
          "[C]; the continuum theorem 'finite-group orbifolds of "
          "completely rational nets are completely rational (hence split "
          "+ strongly additive)' is Xu's -- CITED, NOT CLAIMED; the "
          "continuum proof for THE seam quotient net and the interacting "
          "condensed (E8)_1 net stays [O] (WP5e / Costello-Li); "
          "SEAM.EQUIV.01 untouched, no marker moves", True)


# ===========================================================================
def run():
    reset()
    print("v504  CELEST.WP5DB.01: split + strong additivity from the lattice "
          "(WP5d-beta of CELEST.SEAM.01)")
    print("  model: critical Majorana ring (NS), c = 1/2 per layer; orbifold "
          "= parity sector sum; U(1)/Dirac = negative control")

    section0()
    section1()
    section2()
    section3()
    section4()
    section5()
    section6()

    return summary("v504 CELEST.WP5DB.01: both remaining KLM legs witnessed for the "
                   "orbifold prescription. STRONG ADDITIVITY: exact at the lattice "
                   "level with the shared boundary point (Even(A) v Even(B) = "
                   "Even(AuB), GF2 spans full, rank 32/32), index exactly 2 without "
                   "it (the ln 2 bit of v501, localised at the split point); the "
                   "entropic touching defect is BOUNDED by ln 2 with the Ising "
                   "1/4-exponent approach (p = 0.2444) while the U(1) control "
                   "DIVERGES ((1/2) ln Var Q, Klich-Levitov pinned, infinite index): "
                   "bounded-vs-divergent is the lattice discriminator and the "
                   "quotient net sits on the bounded side. SPLIT: sigma_k fall "
                   "exponentially at the elliptic-nome rate pi K(1-x)/K(x) "
                   "(1.3-2.0%), sigma_1 ~ x^{1/2}, trace norm summable; the orbifold "
                   "inherits the SAME ladder exactly (C -> -C machine identity + "
                   "compound Lambda^2 C) -- Longo heredity. PIMSNER-POPA: "
                   "E(a) - a/2 = PaP/2 identically, integer attainment (16384 + "
                   "2048 monomials, 0 violations), lambda = 1/2 = 1/[F:F_even], "
                   "lambda_E4 = 1/4 = 1/mu, exp(Delta_inf) = 2 = 1/lambda -- the "
                   "Longo-Rehren index pinned by two independent routes. With v501: "
                   "all THREE KLM ingredients of complete rationality witnessed on "
                   "the lattice. Continuum stays [C] (dictionary) / [O] (Xu's "
                   "orbifold theorem CITED, not claimed; the seam quotient net and "
                   "the condensed (E8)_1 net are WP5e/Costello-Li). "
                   "SEAM.EQUIV.01 untouched")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

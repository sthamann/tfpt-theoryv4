"""v503 -- QGEO.EMERGE.LIGHT.01: the deferred emergence test of v215 (lever 7)
executed in its first honest LIGHT version, plus the RESIDUAL-CONVERGENCE
theorem QGEO-R1 == P2-R1 (one common rest, not two).  Analysis / kill-test
class (v347/v264 style): no gate closes, NO marker moves anywhere --
QGEO.REALIZE.01 stays [C]/[O], AX.P2.01 stays an axiom.

v215/QGEO.KILL.01 lever 7 said: the decisive (deferred) kill of the bedrock
is to compute the raw P1 seam-collar DtN WITHOUT inputting the marks and
check whether four SQUARE marks EMERGE.  v216 already derives the mark COUNT
(4 = 2 chi) and EQUALITY from topology; the genuinely open part is the
MODULUS: does the free field on the (2,2,2,2) pillowcase family dynamically
select the SQUARE tau = i, or is tau = i selected only by order-4 RIGIDITY
(Aut contains Z4 iff tau = i, v214/v168), with the clock as the one carrier
input (v493 S1.10)?  This module answers the light version of that question.

  [N] A. NO DYNAMICAL SELECTION (zeta-log-det side; Dedekind-eta formula,
        mpmath 40 digits): logF(tau) = log(tau2 |eta|^4) is exactly
        S-invariant (dev < 1e-35), so t = 1 is AUTOMATICALLY critical on the
        rectangular family tau = it; there g'(1) = 0, g''(1) = -1.298 < 0
        (strict maximum of det'), but the tau1-direction has h''(0) =
        +0.298 > 0: tau = i is a SADDLE of the full moduli space; the
        critical points of logF are exactly the CM points (E2*(i) =
        E2*(rho) = 0 to 40 digits, generic |E2*| = 0.163 != 0); the GLOBAL
        det' winner at fixed area is the HEXAGONAL torus (logF(rho) =
        -1.03352 > logF(i) = -1.05469, diff 0.021169; Osgood-Phillips-
        Sarnak 1988) -- free-field dynamics alone does NOT select tau = i.
        Criticality at the square is Palais symmetric criticality (the
        independent heat trace is equally t -> 1/t invariant and equally
        critical), not dynamics.
  [N] B. SHARP RIGIDITY (lattice DtN side; v280 machinery, N = 8): the
        mod-4 off-character indicator of the raw free-field DtN (v215 K3 as
        a MODULUS FUNCTION) vanishes to 8e-15 EXACTLY at tau = i and is
        strictly monotonically increasing in both directions (min 8.4e-2
        for t != 1): an isolated zero, not a flat valley -- the v215-K3
        lever turned into a function of the modulus; R^2 = Z2 exact as
        permutation matrices (the v492 Z8 bridge on the lattice); j(it) >=
        1728 with equality only at t = 1, j(rho) = 0 (only j = 1728 carries
        a Z4 automorphism, v214/v168).
  [E] C. THE Z2 CHAIN IS MODULUS-BLIND: the involution z -> -z has exactly
        4 fixed points and [Z2, Delta_t] = 0 on EVERY torus (marks/mark-
        locality/deck^2 exist on EVERY pillowcase, v216/v264/v280 confirmed
        without mark input); the pillowcase det' is EXACTLY half the torus
        det' (+-pair structure, ratio 1 to 1e-12), so all tau conclusions
        transfer verbatim; ONLY the order-4 clock distinguishes tau = i.
        Aut(E_rho) = Z6 has element orders {1,2,3,6} -- NO order-4 element:
        the dynamical winner CANNOT carry the mu4 clock (dynamics and clock
        are logically independent selectors); GIVEN the clock, P(iZ) = P(Z)
        forces a3 = a2 = a1 = 0 and j = 1728 identically (v493 S1 mini):
        the modulus is NOT a second input.
  [C/O] D. RESIDUAL CONVERGENCE (the core finding): the order-4 element on
        H^1 is a COXETER element of W(A3) (char poly lam^3+lam^2+lam+1,
        order h(A3) = 4 = |mu4| = N_fam + 1) -- exactly the P2 cusp-class /
        carrier datum of the P2 hardening (v499 R1: generation space =
        H^1(P^1 minus mu4) with the cusp connection).  Chain: (i) mark
        count 4 derived (v216 [E]); (ii) square derived GIVEN the clock
        (v493 [E]); (iii) clock = carrier input [C]; (iv) rest = the
        dynamical realisation of the clock [O].  QGEO-R1 == P2-R1: ONE
        common residual -- 'why does the raw seam carry the order-4 clock'
        -- not two scattered ones.  Route classification (v347 analogue):
        B-rigidity in the sharpened form 'RP seam data => order-4 clock' is
        the live route; free dynamics alone does NOT deliver the clock
        (the hexagonal finding).
  LEVER UPDATE (documented here, v215 itself unchanged): v215 lever 7
        ('deferred emergence test, not executable') is lifted to 'light
        version EXECUTED, result: rigidity, not dynamical selection' --
        marks emerge (B1), the square does NOT emerge dynamically, it is
        pinned by the clock, and the clock is the input.  NO marker moves:
        QGEO.REALIZE.01 stays [C]/[O] (the identification premise is
        untouched -- this module only locates its irreducible rest).

Status: [N] the eta/E2*/j evaluations (mpmath 40 digits) and the lattice
DtN curves (numpy/scipy, v280-style); [E] the exact structure results
(pair structure, permutation identities, sympy forcing, Coxeter charpoly);
[C] clock = carrier input; [O] the dynamical realisation of the clock.
Python; Wolfram-mirrored (eta/E2*/j identities at the CM points, pillowcase
halving, Coxeter charpoly; the lattice DtN curves stay Python-only,
flagged), counted per GATE.WOLFRAM.02.  Discovery provenance:
experiments/tfpt-discovery/qgeo_r1_deferred_emergence_probe.py
(2026-07-21, 17/17)."""
import mpmath as mp
import numpy as np
import sympy as sp
from scipy.linalg import expm, sqrtm

from tfpt_constants import check, summary, reset, N_fam

mp.mp.dps = 40

MU4 = N_fam + 1               # 4 = |mu4| = h(A3), the seam clock order


# ---------------------------------------------------------------------------
# exact modular objects (mpmath, 40 digits)
# ---------------------------------------------------------------------------
def eta(tau):
    """Dedekind eta(tau) = e^{pi i tau/12} prod (1 - q^n), q = e^{2 pi i tau}."""
    q = mp.exp(2j * mp.pi * tau)
    return mp.exp(1j * mp.pi * tau / 12) * mp.qp(q)


def logF(tau):
    """log(tau2 |eta(tau)|^4): the scale-invariant log det'(T^2_tau, area 1)
    up to an additive constant (OPS); pillowcase log det' = 1/2 of this + const."""
    return mp.log(mp.im(tau)) + 4 * mp.log(abs(eta(tau)))


def E2(tau):
    """Eisenstein E2(tau) = 1 - 24 sum n q^n/(1-q^n)."""
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0)
    for n in range(1, 400):
        term = n * q ** n / (1 - q ** n)
        s += term
        if abs(term) < mp.mpf(10) ** (-45):
            break
    return 1 - 24 * s


def E2star(tau):
    """The weight-2 almost-holomorphic completion; critical points of logF are
    exactly E2*(tau) = 0."""
    return E2(tau) - 3 / (mp.pi * mp.im(tau))


def jinv(tau):
    """j-invariant, j(i) = 1728 (mpmath kleinj is normalised J = j/1728)."""
    return 1728 * mp.kleinj(tau)


# ---------------------------------------------------------------------------
# v280-style lattice machinery on the anisotropic torus [0,1] x [0,t]
# ---------------------------------------------------------------------------
N = 8


def _idx(x, y):
    return (x % N) * N + (y % N)


def torus_laplacian(t):
    """Anisotropic flat-torus Laplacian for tau = i t: spacings a_x = 1/N,
    a_y = t/N; overall N^2 dropped (scale-irrelevant for commutators/blocks)."""
    L = np.zeros((N * N, N * N))
    wy = 1.0 / t ** 2
    for x in range(N):
        for y in range(N):
            i = _idx(x, y)
            L[i, i] = -2.0 - 2.0 * wy
            L[i, _idx(x + 1, y)] += 1.0
            L[i, _idx(x - 1, y)] += 1.0
            L[i, _idx(x, y + 1)] += wy
            L[i, _idx(x, y - 1)] += wy
    return L


def perm_op(f):
    P = np.zeros((N * N, N * N))
    for x in range(N):
        for y in range(N):
            xx, yy = f(x, y)
            P[_idx(xx, yy), _idx(x, y)] = 1
    return P


R_OP = perm_op(lambda x, y: (-y, x))          # order-4 clock z -> i z
Z2_OP = perm_op(lambda x, y: (-x, -y))        # elliptic involution z -> -z
PROJ4 = [sum((1j) ** (-k * j) * np.linalg.matrix_power(R_OP, j)
             for j in range(4)) / 4.0 for k in range(4)]


def rel(x, y):
    return np.linalg.norm(x) / np.linalg.norm(y)


def offblock4(M):
    """Off-character weight of M w.r.t. the mu4 clock decomposition (v215 K3)."""
    off = sum(np.linalg.norm(PROJ4[k] @ M @ PROJ4[l])
              for k in range(4) for l in range(4) if k != l)
    return off / np.linalg.norm(M)


def dtn_indicators(t):
    """(comm, offH, offC): [R, Delta_t] norm, mod-4 off-block of H = sqrt(-Delta)
    and of the quasi-free covariance C = (1 + e^H)^{-1}."""
    L = torus_laplacian(t)
    H = sqrtm(-L + 1e-6 * np.eye(N * N)).real
    C = np.linalg.inv(np.eye(N * N) + expm(H))
    return (rel(R_OP @ L - L @ R_OP, L), offblock4(H), offblock4(C))


# ---------------------------------------------------------------------------
# continuum spectral functions on tau = i t at fixed area 1 (for C1)
# ---------------------------------------------------------------------------
def heat_trace(t, s=mp.mpf("0.05"), M=40):
    """theta(t) = sum_{(m,n) != 0} exp(-s lambda_{mn}), lambda_{mn}(it, area 1)
    = 4 pi^2 (m^2 t + n^2 / t); invariant under t -> 1/t by (m,n) -> (n,m)."""
    tot = mp.mpf(0)
    for m in range(-M, M + 1):
        for n in range(-M, M + 1):
            if m == 0 and n == 0:
                continue
            tot += mp.exp(-s * 4 * mp.pi ** 2 * (m * m * t + n * n / t))
    return tot


def run():
    reset()
    print("v503  QGEO.EMERGE.LIGHT.01: does the SQUARE modulus emerge "
          "dynamically from the free field, or only by order-4 rigidity? "
          "(v215 lever-7 light + residual convergence QGEO-R1 == P2-R1)")

    # ================================================== A. exact eta/log-det side
    # A1. modular S-invariance of the target functional (exact identity check)
    t0 = mp.mpf("1.7")
    dev = abs(logF(1j * t0) - logF(1j / t0))
    gen_tau = mp.mpc("0.31", "1.13")
    dev_gen = abs(logF(gen_tau) - logF(-1 / gen_tau))
    check("A1 ETA/S-INVARIANCE [exact to 1e-35]: logF(tau) = log(tau2|eta|^4) obeys "
          "logF(it) = logF(i/t) (dev %.1e at t=1.7) and full S logF(-1/tau) = "
          "logF(tau) (dev %.1e at generic tau) -- the rectangular family is "
          "t -> 1/t symmetric, so t = 1 (tau = i) is AUTOMATICALLY critical for "
          "any such functional" % (dev, dev_gen),
          dev < mp.mpf(10) ** -35 and dev_gen < mp.mpf(10) ** -35)

    # A2. the log-det family on tau = i t: extremum location + curvature + table
    g = lambda tt: logF(1j * tt)
    g1 = mp.diff(g, mp.mpf(1), 1)
    g2 = mp.diff(g, mp.mpf(1), 2)
    print("        t      logF(it) = log det'(T^2) + const   (pillowcase = 1/2 of this)")
    ts = [mp.mpf(x) / 100 for x in (50, 60, 70, 85, 100, 120, 141, 170, 200)]
    vals = []
    for tt in ts:
        v = g(tt)
        vals.append(v)
        print("        %-6s %s" % (mp.nstr(tt, 4), mp.nstr(v, 12)))
    vmax = max(vals)
    check("A2 RECTANGULAR FAMILY EXTREMUM [num, 40 digits]: on tau = it the "
          "functional has g'(1) = %s (= 0) and g''(1) = %s < 0: tau = i is a "
          "strict local MAXIMUM of det' (= max of the pillowcase log det') within "
          "the clock-symmetric rectangular family; table max at t = 1"
          % (mp.nstr(g1, 3), mp.nstr(g2, 8)),
          abs(g1) < mp.mpf(10) ** -25 and g2 < 0
          and vals.index(vmax) == ts.index(mp.mpf(1)))

    # A3. but tau = i is a SADDLE of the full moduli space
    h = lambda x: logF(x + 1j)
    h1 = mp.diff(h, mp.mpf(0), 1)
    h2 = mp.diff(h, mp.mpf(0), 2)
    check("A3 SADDLE [num]: along the tau1-direction h(x) = logF(x + i) has "
          "h'(0) = %s (= 0, tau -> -taubar symmetry) and h''(0) = %s > 0: tau = i "
          "is a MINIMUM in the tau1-direction, hence a SADDLE of the full moduli "
          "space -- the 'extremum at the square' is family-relative, not global"
          % (mp.nstr(h1, 3), mp.nstr(h2, 8)),
          abs(h1) < mp.mpf(10) ** -25 and h2 > 0)

    # A4. criticality is exactly the CM points: E2*(i) = E2*(rho) = 0, generic != 0
    rho = mp.exp(1j * mp.pi / 3)
    e_i, e_rho = abs(E2star(1j)), abs(E2star(rho))
    e_gen = abs(E2star(gen_tau))
    check("A4 CRITICAL POINTS = CM POINTS [num, 40 digits]: E2*(i) = %.1e and "
          "E2*(rho) = %.1e (both 0: the two exceptional-automorphism points are "
          "the ONLY critical points, both symmetry-forced), generic "
          "|E2*(0.31+1.13i)| = %.3f != 0 -- no critical point at any generic tau"
          % (e_i, e_rho, e_gen),
          e_i < mp.mpf(10) ** -35 and e_rho < mp.mpf(10) ** -35 and e_gen > 0.01)

    # A5. the FULL moduli space dynamically selects HEXAGONAL, not the square
    F_i, F_rho = logF(1j), logF(rho)
    check("A5 GLOBAL SELECTOR = HEXAGONAL [num]: logF(rho) = %s > logF(i) = %s "
          "(diff %s > 0): the free-field det' at fixed area is maximised at the "
          "hexagonal torus (OPS 1988), NOT the square -- free-field dynamics "
          "alone does NOT select tau = i on the full (2,2,2,2) moduli space"
          % (mp.nstr(F_rho, 10), mp.nstr(F_i, 10), mp.nstr(F_rho - F_i, 6)),
          F_rho > F_i)

    # A6. pillowcase log det' = 1/2 torus log det' (orbifold spectrum = one copy
    #     of each +/- pair): exact pair structure on the discrete torus
    L1 = torus_laplacian(1.0)
    ev_torus = np.sort(np.linalg.eigvalsh(-L1))
    w_z2, v_z2 = np.linalg.eigh(Z2_OP)
    Veven = v_z2[:, w_z2 > 0.5]
    ev_even = np.sort(np.linalg.eigvalsh(Veven.T @ (-L1) @ Veven))
    # self-paired Fourier modes (m, n) with 2m = 2n = 0 mod N: 4 of them,
    # exactly the 4 cone points in frequency space -- all land in the even sector
    self_modes = [(0, 0), (N // 2, 0), (0, N // 2), (N // 2, N // 2)]
    lam = lambda m, n: (2 - 2 * np.cos(2 * np.pi * m / N)) + (2 - 2 * np.cos(2 * np.pi * n / N))
    prod_self = np.prod([lam(m, n) for (m, n) in self_modes if (m, n) != (0, 0)])
    det_torus = np.prod(ev_torus[1:])
    det_even = np.prod(ev_even[1:])
    ratio = det_even ** 2 / (det_torus * prod_self)
    dim_ok = Veven.shape[1] == (N * N + 4) // 2
    check("A6 PILLOWCASE = HALF TORUS [num, exact pair structure]: dim(even) = %d "
          "= (N^2+4)/2 (4 self-paired cone modes); det'_even^2 / (det'_torus * "
          "prod_self) = %.12f = 1 exactly -- the orbifold spectrum is one copy of "
          "each +/- pair, so zeta_pillow(s) = zeta_torus(s)/2 in the continuum "
          "and log det'_pillow = (1/2) log det'_torus: ALL tau-conclusions "
          "(A2-A5) transfer verbatim to the pillowcase" % (Veven.shape[1], ratio),
          dim_ok and abs(ratio - 1) < 1e-9)

    # A7. rigidity witness on the family: j(it) touches 1728 exactly once (t = 1)
    js = [(tt, mp.re(jinv(1j * tt))) for tt in ts]
    j_dev = [(tt, jj - 1728) for tt, jj in js]
    only_t1 = all((abs(d) < mp.mpf(10) ** -25) == (tt == 1) for tt, d in j_dev)
    all_ge = all(d > -mp.mpf(10) ** -25 for _, d in j_dev)
    j_rho = abs(jinv(rho))
    check("A7 RIGIDITY WITNESS [num, 40 digits]: on tau = it the j-invariant is "
          "real with j(it) >= 1728 and j = 1728 ONLY at t = 1 (checked on the "
          "9-point family; min at the square); j(rho) = %.1e = 0 (hexagonal) -- "
          "Aut(E) > Z2 happens only at j in {0, 1728}, and the order-4 clock "
          "(Z4) exists ONLY at j = 1728, i.e. tau = i (v214/v168)"
          % j_rho, only_t1 and all_ge and j_rho < mp.mpf(10) ** -30)

    # ================================================== B. lattice DtN mod-4 side
    # B1. topology: 4 involution fixed points and [Z2, Delta_t] = 0 for EVERY t
    fixed = [(x, y) for x in range(N) for y in range(N)
             if ((-x) % N, (-y) % N) == (x, y)]
    comm_z2 = []
    for tt in (0.5, 0.7, 1.0, 1.3, 2.0):
        Lt = torus_laplacian(tt)
        comm_z2.append(rel(Z2_OP @ Lt - Lt @ Z2_OP, Lt))
    check("B1 TOPOLOGY IS tau-INDEPENDENT [num]: the involution z -> -z has "
          "exactly %d fixed points (the 2-torsion = the 4 marks) on EVERY torus, "
          "and [Z2, Delta_t] = 0 for all t (max %.1e): mark COUNT and equality "
          "need NO modulus input -- v216 confirmed without inputting marks"
          % (len(fixed), max(comm_z2)),
          len(fixed) == 4 and max(comm_z2) < 1e-12)

    # B2. clock^2 = deck on the lattice (the v492/v493 Z8 bridge, structural)
    check("B2 CLOCK^2 = DECK [exact permutation identity]: R^2 = Z2 as N^2 x N^2 "
          "permutation matrices (%s) and R^4 = 1 -- the elliptic involution IS "
          "the square of the order-4 clock (v492 WP1 bridge on the lattice)"
          % np.allclose(np.linalg.matrix_power(R_OP, 2), Z2_OP),
          np.allclose(np.linalg.matrix_power(R_OP, 2), Z2_OP)
          and np.allclose(np.linalg.matrix_power(R_OP, 4), np.eye(N * N)))

    # B3. the DtN mod-4 indicator as a function of the modulus (v215 K3 curve)
    print("        t      ||[R,Delta_t]||/||Delta_t||   off4(H_t)      off4(C_t)")
    curve = {}
    for tt in (0.5, 0.7, 0.85, 1.0, 1.2, 1.5, 2.0):
        c, oh, oc = dtn_indicators(tt)
        curve[tt] = (c, oh, oc)
        print("        %-6.2f %-28.3e %-14.3e %-14.3e" % (tt, c, oh, oc))
    at1 = curve[1.0]
    away = {tt: v for tt, v in curve.items() if tt != 1.0}
    check("B3 MOD-4 BLOCK-DIAGONALITY IFF SQUARE [num, v215 K3 as a modulus "
          "function]: at t = 1 the commutator and BOTH off-character weights "
          "vanish (%.1e, %.1e, %.1e); for every t != 1 all three are > 1e-3 "
          "(min %.1e) -- the raw free-field DtN is mu4 block-diagonal EXACTLY at "
          "the square modulus, at no other point of the family"
          % (at1[0], at1[1], at1[2], min(min(v) for v in away.values())),
          max(at1) < 1e-6 and all(min(v) > 1e-3 for v in away.values()))

    # B4. the indicator grows monotonically in |log t| (sharp selection, no
    #     spurious flat directions), and respects t -> 1/t up to the anisotropy scale
    seq = [curve[tt][1] for tt in (1.0, 1.2, 1.5, 2.0)]
    seq_dn = [curve[tt][1] for tt in (1.0, 0.85, 0.7, 0.5)]
    check("B4 SHARP WELL [num]: off4(H_t) increases strictly away from t = 1 in "
          "both directions (up: %s; down: %s) -- t = 1 is an isolated zero, not "
          "a flat valley: the square is PINNED by the clock-symmetry indicator"
          % (["%.2e" % x for x in seq], ["%.2e" % x for x in seq_dn]),
          all(seq[i] < seq[i + 1] for i in range(3))
          and all(seq_dn[i] < seq_dn[i + 1] for i in range(3)))

    # B5. the Z2 chain (v264/v280) holds for EVERY t: only the CLOCK pins t = 1
    off_z2 = []
    for tt in (0.5, 1.0, 2.0):
        Lt = torus_laplacian(tt)
        Ht = sqrtm(-Lt + 1e-6 * np.eye(N * N)).real
        off_z2.append(rel(Z2_OP @ Ht - Ht @ Z2_OP, Ht))
    check("B5 INVOLUTION CHAIN IS MODULUS-BLIND [num]: [Z2, H_t] = 0 for all t "
          "(max %.1e) -- the whole v264/v280 Z2-chain (4 marks, mark-locality, "
          "omega o (deck)^2-invariance) is available on EVERY pillowcase; ONLY "
          "the order-4 clock distinguishes tau = i.  The emergence question is "
          "therefore exactly 'why the clock', nothing else" % max(off_z2),
          max(off_z2) < 1e-8)

    # ================================================== C. extremum vs rigidity
    # C1. Palais symmetric criticality: EVERY t -> 1/t invariant functional is
    #     critical at t = 1 -- criticality there carries no dynamical information
    th1 = mp.diff(lambda tt: heat_trace(tt), mp.mpf(1), 1)
    th2 = mp.diff(lambda tt: heat_trace(tt), mp.mpf(1), 2)
    inv_dev = abs(heat_trace(mp.mpf("1.31")) - heat_trace(1 / mp.mpf("1.31")))
    check("C1 SYMMETRY-GENERIC CRITICALITY [num]: the (independent) heat trace "
          "theta(t) = sum exp(-s lambda_mn(it)) is t -> 1/t invariant (dev %.1e) "
          "and hence ALSO critical at t = 1 (theta'(1) = %s, theta''(1) = %s "
          "!= 0) -- criticality of the log-det at the square is a Palais "
          "symmetric-criticality consequence of the R-symmetry of the FAMILY, "
          "not evidence of dynamical selection"
          % (inv_dev, mp.nstr(th1, 3), mp.nstr(th2, 4)),
          inv_dev < mp.mpf(10) ** -35 and abs(th1) < mp.mpf(10) ** -20
          and abs(th2) > mp.mpf(10) ** -6)

    # C2. the hexagonal winner has NO order-4 element: Z6 contains no Z4
    z6_orders = sorted({sp.Integer(6) / sp.gcd(k, 6) for k in range(1, 7)})
    check("C2 HEXAGONAL HAS NO CLOCK [exact]: Aut(E_rho) = Z6, element orders "
          "%s -- no order-4 element (4 does not divide 6); so the dynamically "
          "selected hexagonal point CANNOT carry the mu4 clock, and conversely "
          "the clock excludes the dynamical winner: dynamics and clock-symmetry "
          "point at DIFFERENT tau -- they are logically independent selectors"
          % z6_orders, 4 not in z6_orders and sp.Integer(4) not in z6_orders
          and z6_orders == [1, 2, 3, 6])

    # C3. sympy mini-replication of the v493 link: GIVEN the clock, the square is
    #     frozen automatically (the modulus is NOT an extra input beyond the clock)
    Z, a0s, a1s, a2s, a3s = sp.symbols('Z a0 a1 a2 a3')
    P = Z ** 4 + a3s * Z ** 3 + a2s * Z ** 2 + a1s * Z + a0s
    forced = sp.solve([sp.Poly(sp.expand(P.subs(Z, sp.I * Z) - P), Z).coeff_monomial(Z ** k)
                       for k in range(4)], [a3s, a2s, a1s], dict=True)
    Iq = 12 * a0s                     # binary-quartic invariants of Z^4 + a0
    Jq = sp.Integer(0)
    jfrozen = sp.simplify(6912 * Iq ** 3 / (4 * Iq ** 3 - Jq ** 2))
    check("C3 CLOCK => SQUARE, AUTOMATICALLY [exact, v493 S1 mini]: P(iZ) = P(Z) "
          "forces a3 = a2 = a1 = 0 (%s), and the surviving family Z^4 + a0 has "
          "I = 12 a0, J = 0 identically => j = %s = 1728 for ALL a0: GIVEN the "
          "order-4 clock, the (2,2,2,2) modulus is frozen to the square with "
          "only the scale free -- the modulus is NOT a second input"
          % (forced == [{a3s: 0, a2s: 0, a1s: 0}], jfrozen),
          forced == [{a3s: 0, a2s: 0, a1s: 0}] and jfrozen == 1728)

    # C4. the clock arithmetic is carrier data: h(A3) = 4 = |mu4| = N_fam + 1
    A = sp.Matrix([[0, 0, -1], [1, 0, -1], [0, 1, -1]])
    lamx = sp.Symbol('lam')
    chi = sp.expand(A.charpoly(lamx).as_expr())
    check("C4 THE CLOCK IS THE CARRIER INPUT [exact]: the order-4 element acting "
          "on H^1 is a Coxeter element of W(A3) (char poly %s = lam^3 + lam^2 + "
          "lam + 1, order h(A3) = 4 = |mu4| = N_fam + 1 = %d) -- exactly the P2 "
          "cusp-class/carrier datum of the P2 hardening v499 (its R1: "
          "'generation space = H^1(P^1 minus mu4) with the cusp connection'): "
          "the QGEO modulus rest and the P2 typing rest are the SAME order-4 input"
          % (chi, MU4),
          sp.expand(chi - (lamx ** 3 + lamx ** 2 + lamx + 1)) == 0
          and sp.simplify(A ** 4 - sp.eye(3)) == sp.zeros(3, 3)
          and MU4 == 4)

    # C5. the honest verdict, tied to the computed facts
    verdict_facts = (F_rho > F_i                       # dynamics -> hexagonal
                     and max(at1) < 1e-6               # clock indicator zero at i
                     and all(min(v) > 1e-3 for v in away.values())
                     and forced == [{a3s: 0, a2s: 0, a1s: 0}])
    check("C5 VERDICT [typed]: NO dynamical selection of the square (the free "
          "field's global det' winner is hexagonal, A5; the extremum at tau = i "
          "within the rectangular family is Palais-symmetry, C1).  The square is "
          "selected by RIGIDITY alone: Aut contains Z4 iff tau = i (A7), the "
          "DtN is mod-4 block-diagonal iff tau = i (B3), and GIVEN the clock the "
          "modulus freezes automatically (C3).  Therefore R1's irreducible rest "
          "is precisely: 'WHY does the raw seam carry the order-4 clock' -- the "
          "same carrier input as the P2-hardening R1 (C4): ONE common residual, "
          "not two.  The deferred emergence test (v215 lever 7) light version "
          "returns: marks emerge (B1), square does NOT emerge dynamically -- it "
          "is pinned by the clock, and the clock is the input.  NO marker moves: "
          "QGEO.REALIZE.01 stays [C]/[O]", verdict_facts)

    return summary("v503 QGEO.EMERGE.LIGHT.01: v215 lever 7 executed light -- NO "
                   "dynamical selection of the square (global det' winner is the "
                   "HEXAGONAL torus, logF(rho) = -1.03352 > logF(i) = -1.05469; "
                   "tau = i is a saddle, g''(1) = -1.298 rectangular vs h''(0) = "
                   "+0.298 in tau1; critical points = CM points E2*(i) = E2*(rho) "
                   "= 0; criticality = Palais symmetry). The square is pinned by "
                   "RIGIDITY: the DtN mod-4 indicator has an isolated zero (8e-15) "
                   "exactly at tau = i (strictly monotone both ways, min 8.4e-2 "
                   "away); j(it) = 1728 only at t = 1; Aut(hexagonal) = Z6 has NO "
                   "order-4 element. The Z2 chain is modulus-blind (marks emerge "
                   "on EVERY pillowcase; pillowcase det' = half torus det' "
                   "exactly); GIVEN the clock the modulus freezes (j = 1728 "
                   "identically). RESIDUAL CONVERGENCE: the clock = Coxeter of "
                   "W(A3) = the P2 cusp-class carrier datum (v499 R1) -- "
                   "QGEO-R1 == P2-R1, ONE common rest: 'why does the raw seam "
                   "carry the order-4 clock'. No marker moves; QGEO.REALIZE.01 "
                   "stays [C]/[O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

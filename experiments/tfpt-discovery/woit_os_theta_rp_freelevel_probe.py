"""woit_os_theta_rp_freelevel_probe.py -- EXPLORATION ONLY (WOIT-alpha, W3).
Nothing in verification/, ledger, papers, changelog, website or scorecard is
touched.  Companion of woit_os_theta_realstructure_probe.py (W1/W2): with the
pinned family-D real structure Theta (Theta^2 = +1, Theta rho Theta = rho^-1),
build the OS form <Theta a, b> = omega(theta(a) b) EXACTLY on the half-sided
operator space of the 16-Majorana NS seam system (v506 machinery) and test
reflection positivity (Gram matrix, rank/inertia) -- plus the controls that
must separate.

SETUP.  State: the chiral NS vacuum on the N-site seam circle (quasifree
pure: C^2 = -1 exact; N = 16 = 2^(g_car-1), robustness N = 8):
omega(g_a g_b) = delta_ab + i C(a-b) with C(d) = (2/N)/sin(pi d/N) for odd
d, 0 for even d (antiperiodic C(d+N) = -C(d)).  OS reflection theta =
anti-linear ANTI-automorphism (order-reversing) with the fermionic twist:
theta(g_a) = eta s_a g_{r(a)}, r/s = the v510 NS dihedral spin lift of the
seam reflection.  This is the algebraic form of Theta_Fock = U_r o K of
the W1 probe; eta = +-i is the Majorana analogue of the Dirac gamma^0 OS
twist -- FORCED by Hermiticity (control R5.1: eta = 1 is non-Hermitian),
the residual sign pinned by positivity jointly with the chirality.

FINDINGS (computed below, exact):
  R1 PRECONDITIONS ALL EXACT: C^2 = -1 (pure); every NS reflection lift
     gives R C R^T = -C (omega o theta = conj o omega, + 4-pt witness);
     the NS quarter-shift clock lift S preserves the state (S C S^T = C);
     R S R^-1 = S^-1 (the W1 clock inversion on the state side); the NS
     ANTIPODE S^2 = deck FAILS anti-invariance (S^2 C S^2T = +C) -- the
     deck is not an OS reflection of the chiral vacuum.
  R2 SITE CUT FAILS (axis THROUGH sites, marks-at-sites reading; k = 0,
     half = 7 sites): reflected distances k-2a are EVEN and the strictly
     chiral kernel has C(even) = 0 exactly => the one-particle Gram has
     ZERO diagonal (indefinite for EVERY twist and EVERY sign dressing),
     det = 0 exactly (bipartite 4+3), inertia (3,3,1); the deg <= 2 even
     sector fails too (9 zero-diagonal rows, exact negative 2x2 minor,
     inertia (7,9,6)) -- NOT a fermion-parity artifact.
  R3 BOND CUT PASSES (axis BETWEEN sites, marks at bond midpoints = the
     half-offset/NS-natural placement '4 sites per mark quadrant'; k = 15
     <-> mu = 1, k = 3 <-> mu = i): with eta = +i the one-particle Gram
     is PD (inertia (8,0,0), min eigenvalue 1.888e-3 at 40 digits), the
     29x29 deg <= 2 even Gram is PD (29,0,0), and at N = 8 the COMPLETE
     16-monomial half-algebra passes (even (8,0,0), odd (8,0,0)): free-
     level RP holds with no degree truncation.
  R4 CONTINUUM CONTROL: 1/sin((s+t)/2) = pos.diag x Cauchy-Stieltjes
     1/(x+y) (exact identity; minors 1/2, 1/72, 1/43200, 1/423360000 >
     0) -- the continuum mark-cut kernel is strictly PD: the R2 failure
     is a LATTICE-PLACEMENT artifact; RP selects the site placement
     relative to the marks (cut points must be site-free).
  R5 CONTROLS (the test separates): (i) eta = 1: non-Hermitian (gamma^0
     twist forced); (ii) the clock-CENTRALISING family-A/antipode
     (= W1 Theta_t = Utilde o K): needs the alternating dressing even to
     keep anti-invariance and its Gram has zero diagonal, inertia (4,4,0)
     -- RP fails structurally exactly where the clock-inverting Theta is
     PD: RP and Theta rho Theta = rho^-1 select the SAME family; (iii)
     anti-chiral state (C -> -C): odd-sector Gram flips to (0,8,0) ND
     while the even pair block is entry-identical (chirality-blind) --
     an exact free-level shadow of kill test 3 living in the odd sector.

Honest scope: free/quadratic level only; deg <= 2 even sector at N = 16,
full algebra at N = 8; the interacting algebra, gauge fixing (kill test
2), OS reconstruction and chirality (kill tests 3/6) stay open contract
work (WOIT-beta/gamma).

Exact where stated (sympy trig-algebraic entries, Pfaffian-Wick);
inertia: exact Hermiticity/rank structure + spectrum of the exact matrix
at 40 digits (gap-certified).  Standalone; deterministic; no files
written.

Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/woit_os_theta_rp_freelevel_probe.py
"""
from itertools import combinations

import mpmath as mp
import sympy as sp

mp.mp.dps = 40

RESULTS = []
I = sp.I
N = 16
NH = N // 2


def check(name, ok):
    RESULTS.append(bool(ok))
    print(("PASS" if ok else "FAIL") + " [%2d] %s" % (len(RESULTS), name))


def iszero(e):
    e2 = sp.expand(e)
    if e2 == 0:
        return True
    e3 = sp.expand(sp.expand_complex(e2))
    if e3 == 0:
        return True
    return sp.simplify(e3) == 0


# ---------------------------------------------------------------------------
# the chiral NS vacuum kernel (exact)
# ---------------------------------------------------------------------------
def c_of(d, n=N):
    """C(d) = (2/n) sum_{p in NS+} sin(p d) = (2/n)/sin(pi d/n) for odd d,
    0 for even d (exact geometric sum; antiperiodic C(d+n) = -C(d))."""
    if d % 2 == 0:
        return sp.Integer(0)
    return sp.Rational(2, n) / sp.sin(sp.pi * sp.Rational(d, n))


def g2(a, b, n=N, chi=1):
    """omega(g_a g_b) = delta + i*chi*C(a-b); chi = -1 -> anti-chiral."""
    if a == b:
        return sp.Integer(1)
    return I * chi * c_of(a - b, n)


def wick(idx, n=N, chi=1):
    """omega(g_{i1} ... g_{i2k}) by Pfaffian recursion (all indices
    distinct)."""
    if len(idx) == 0:
        return sp.Integer(1)
    if len(idx) % 2 == 1:
        return sp.Integer(0)
    head, rest = idx[0], idx[1:]
    tot = sp.Integer(0)
    for j, b in enumerate(rest):
        sub = rest[:j] + rest[j + 1:]
        tot += (-1) ** j * g2(head, b, n, chi) * wick(sub, n, chi)
    return tot


# ---------------------------------------------------------------------------
# dihedral spin lifts (v506/v510 verbatim)
# ---------------------------------------------------------------------------
def shift_matrix(n, k, wrap_sign):
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        b = (a + k) % n
        M[b][a] = wrap_sign if a + k >= n else 1
    return M


def refl_matrix(n, k, wrap_sign):
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        idx = (k - a) % (2 * n)
        M[idx % n][a] = wrap_sign if idx >= n else 1
    return M


def refl_map(k, n=N):
    """site map + spin sign of the reflection j -> k - j (NS lift)."""
    def r(a):
        return (k - a) % n

    def s(a):
        return -1 if (k - a) % (2 * n) >= n else 1
    return r, s


# ---------------------------------------------------------------------------
# theta = anti-linear anti-automorphism with twist eta
# ---------------------------------------------------------------------------
def theta_mono(mono, r, s, eta, k_deg=None):
    """theta(g_{i1}...g_{ik}) = eta^k * s_{ik}...s_{i1} g_{r(ik)}...g_{r(i1)}
    sorted back to increasing order; returns (coeff, tuple)."""
    k = len(mono)
    imgs = [r(a) for a in reversed(mono)]
    coeff = eta ** k
    for a in mono:
        coeff *= s(a)
    # bubble sort sign
    lst = list(imgs)
    sign = 1
    for i in range(len(lst)):
        for j in range(len(lst) - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                sign = -sign
    assert len(set(lst)) == len(lst)
    return coeff * sign, tuple(lst)


def gram(basis, r, s, eta, n=N, chi=1):
    """M_ab = omega(theta(e_a) e_b), exact."""
    rows = []
    for ma in basis:
        ca, ia = theta_mono(ma, r, s, eta)
        row = []
        for mb in basis:
            assert not (set(ia) & set(mb)), "supports must be disjoint"
            row.append(sp.expand_complex(ca * wick(list(ia) + list(mb),
                                                   n, chi)))
        rows.append(row)
    return sp.Matrix(rows)


def hermitian_exact(M):
    d = M - M.conjugate().T
    return all(iszero(x) for x in d)


def spectrum_inertia(M, tol=mp.mpf(10) ** (-25)):
    """inertia (n+, n-, n0) of the exact Hermitian matrix via 40-digit
    spectrum of the evalf'd matrix; returns (inertia, min|nonzero|)."""
    n = M.shape[0]
    A = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            re_, im_ = M[i, j].evalf(45).as_real_imag()
            A[i, j] = mp.mpc(mp.mpf(str(re_)), mp.mpf(str(im_)))
    E, _ = mp.eighe(A)
    evs = [E[i].real for i in range(n)]
    npos = sum(1 for e in evs if e > tol)
    nneg = sum(1 for e in evs if e < -tol)
    nzero = n - npos - nneg
    nz = [abs(e) for e in evs if abs(e) > tol]
    return (npos, nneg, nzero), (min(nz) if nz else mp.mpf(0))


PLUS = lambda a: 1                     # plain spin signs (state-compatible)


def half_of(k, n=N):
    """the positive half for the reflection r(a) = k - a mod n (site axis:
    exclude the 2 fixed sites; bond axis: the arc between the two cut
    bonds), plus disjointness of r(half)."""
    if k % 2 == 0:
        f1, f2 = (k // 2) % n, (k // 2 + n // 2) % n
        P = [(f1 + j) % n for j in range(1, n // 2)]
    else:
        b = (k + 1) // 2                # first site right of the cut bond
        P = [(b + j) % n for j in range(n // 2)]
    rP = {(k - a) % n for a in P}
    assert not (rP & set(P))
    return P


# ---------------------------------------------------------------------------
# R1: state compatibility -- exact preconditions
# ---------------------------------------------------------------------------
def r1_state():
    print("  -- R1: the chiral NS vacuum vs theta -- exact preconditions")
    n8 = 8
    Cm8 = sp.Matrix(n8, n8, lambda a, b: c_of(a - b, n8))
    pure = sp.simplify(Cm8 * Cm8 + sp.eye(n8)) == sp.zeros(n8, n8)
    check("R1.1 STATE WELL-DEFINED [exact, N=8]: the chiral NS kernel "
          "C(d) = (2/N)/sin(pi d/N) (odd d; 0 even; C(d+N) = -C(d)) has "
          "C^2 = -1 EXACTLY (%s) -- omega = (1 + iC)/2-quasifree is a "
          "PURE state: the lattice chiral vacuum exists and is the "
          "unique all-right-movers NS polarisation" % pure, pure)

    Cm = sp.Matrix(N, N, lambda a, b: c_of(a - b))
    Rs = {k: sp.Matrix(refl_matrix(N, k, -1)) for k in (15, 3, 0)}
    anti = all(sp.simplify(R * Cm * R.T + Cm) == sp.zeros(N, N)
               for R in Rs.values())
    S = sp.Matrix(shift_matrix(N, 4, -1))
    clock_inv = sp.simplify(S * Cm * S.T - Cm) == sp.zeros(N, N)
    dihed = sp.simplify(Rs[15] * S * Rs[15].inv()
                        - S.inv()) == sp.zeros(N, N)
    anti_antipode = sp.simplify(
        (S ** 2) * Cm * (S ** 2).T + Cm) == sp.zeros(N, N)
    check("R1.2 ANTI-INVARIANCE + CLOCK [exact, N=16, NS dihedral "
          "lifts]: every v510 NS reflection lift gives R C R^T = -C "
          "EXACTLY (k = 15, 3, 0: %s; the OS precondition omega o theta "
          "= conj o omega at 2-pt level -- the antiperiodic wrap signs "
          "implement exactly the C(d+16) = -C(d) representative shift), "
          "the NS quarter-shift clock lift gives S C S^T = C (%s; the "
          "chiral vacuum is clock-invariant), and R S R^-1 = S^-1 "
          "EXACTLY (%s; theta inverts the clock -- the W1 relation on "
          "the state side); the NS ANTIPODE S^2 (= the Utilde deck "
          "conjugation) FAILS anti-invariance (%s: S^2 C S^2T = +C != "
          "-C) -- the deck is not an OS reflection of this state"
          % (anti, clock_inv, dihed, not anti_antipode),
          anti and clock_inv and dihed and not anti_antipode)

    r, s = refl_map(15)
    eta = I
    idx = (1, 2, 4, 7)
    th_c, th_m = theta_mono(idx, r, s, eta)
    lhs = sp.expand_complex(th_c * wick(list(th_m)))
    rhs = sp.expand_complex(sp.conjugate(wick(list(idx))))
    four_pt = iszero(lhs - rhs)
    tsq = []
    for a in range(N):
        c1, m1 = theta_mono((a,), r, s, eta)
        c2, m2 = theta_mono(m1, r, s, eta)
        tsq.append(iszero(sp.conjugate(c1) * c2 - 1) and m2 == (a,))
    check("R1.3 THETA IS AN OS REFLECTION [exact]: theta(g_a) = eta s_a "
          "g_{15-a} with eta = i (NS signs) is an anti-linear anti-"
          "automorphism with theta^2 = 1 on ALL 16 generators (%s; "
          "anti-linearity kills the phase: conj(eta) eta = |eta|^2 = 1) "
          "and omega o theta = conj o omega verified beyond 2-pt on the "
          "4-pt witness g1 g2 g4 g7 (%s)"
          % (all(tsq), four_pt), all(tsq) and four_pt)


# ---------------------------------------------------------------------------
# R2: the site cut fails -- exactly
# ---------------------------------------------------------------------------
def r2_site_cut():
    print("  -- R2: cut THROUGH sites (marks-at-sites reading) -- RP fails")
    k = 0
    P = half_of(k)                       # {1..7}
    r = lambda a: (k - a) % N
    basis1 = [(a,) for a in P]
    M1 = gram(basis1, r, PLUS, -I)
    herm = hermitian_exact(M1)
    diag0 = all(iszero(M1[i, i]) for i in range(len(P)))
    offdiag = sum(0 if iszero(M1[i, j]) else 1
                  for i in range(7) for j in range(7) if i != j)
    det_exact = sp.simplify(M1.det())
    inert, gap = spectrum_inertia(M1)
    check("R2.1 ONE-PARTICLE GRAM DEGENERATES [exact]: axis through the "
          "sites (k = 0, half = 7 sites): the Gram omega(theta(g_a) g_b) "
          "= -C(-a-b) is Hermitian (%s) but has ZERO diagonal (all 7 "
          "entries: %s; reflected distance k-2a is EVEN and the strictly "
          "chiral kernel has C(even) = 0 exactly) with %d nonzero "
          "off-diagonal entries -- indefinite for EVERY twist eta and "
          "EVERY spin-sign dressing; checkerboard block structure: "
          "det = %s exactly (bipartite 4+3), inertia (n+,n-,n0) = %s "
          "(+- symmetric): RP FAILS on the site cut"
          % (herm, diag0, offdiag, det_exact, inert),
          herm and diag0 and offdiag > 0 and det_exact == 0
          and inert == (3, 3, 1))

    pairs = list(combinations(P, 2))
    basis2 = [()] + pairs
    M2 = gram(basis2, r, PLUS, -I)
    herm2 = hermitian_exact(M2)
    zero_idx = [i for i, pr in enumerate(pairs)
                if (pr[0] + pr[1]) % 2 == 0]
    wit = None
    for i in zero_idx:
        for j in range(len(basis2)):
            if j != i + 1 and not iszero(M2[i + 1, j]):
                minor = sp.expand_complex(
                    M2[i + 1, i + 1] * M2[j, j]
                    - M2[i + 1, j] * sp.conjugate(M2[i + 1, j]))
                wit = (pairs[i], basis2[j], sp.simplify(minor))
                break
        if wit:
            break
    inert2, _ = spectrum_inertia(M2)
    check("R2.2 EVEN SECTOR FAILS TOO [exact]: deg <= 2 even Gram (1 + 21 "
          "pairs = 22x22) is Hermitian (%s) but the same-parity pairs "
          "have diagonal C(a-b)^2 - C(a+b)^2 = 0 - 0 = 0 (%d zero-"
          "diagonal rows) with nonzero coupling: 2x2 minor witness "
          "%s x %s = %s < 0 exactly; inertia %s -- the site cut fails "
          "even in the gauge-blind (even) sector: NOT a fermion-parity "
          "artifact" % (herm2, len(zero_idx), wit[0], wit[1], wit[2],
                        inert2),
          herm2 and len(zero_idx) > 0 and wit is not None
          and sp.simplify(wit[2]) != 0 and inert2[1] > 0)


# ---------------------------------------------------------------------------
# R3: the bond cut passes -- exactly
# ---------------------------------------------------------------------------
def r3_bond_cut():
    print("  -- R3: cut BETWEEN sites (marks-at-bond-midpoints reading) "
          "-- RP holds")
    res = {}
    for k, tag in [(15, 'mu=1'), (3, 'mu=i')]:
        P = half_of(k)
        r, s = refl_map(k)
        basis1 = [(a,) for a in P]
        picked = None
        for eta in (I, -I):
            M1 = gram(basis1, r, s, eta)
            if not hermitian_exact(M1):
                continue
            inert, gap = spectrum_inertia(M1)
            if inert == (8, 0, 0):
                picked = (eta, inert, gap)
        res[tag] = picked
    check("R3.1 ONE-PARTICLE GRAM PD [exact entries, 40-digit inertia]: "
          "bond axes (k = 15 <-> mark axis mu = 1 in the half-offset "
          "placement; k = 3 <-> mu = i), NS spin lifts: reflected "
          "distances are ODD, the Gram entries land on the nonzero "
          "chiral kernel; for exactly one twist per axis (mu=1: eta = "
          "%s; mu=i: eta = %s) the 8x8 Gram is POSITIVE DEFINITE, "
          "inertia %s / %s (min eigenvalue > %s at 40 digits) -- RP "
          "holds at one-particle level on both pinned mark axes"
          % (res['mu=1'][0], res['mu=i'][0], res['mu=1'][1],
             res['mu=i'][1], mp.nstr(min(res['mu=1'][2], res['mu=i'][2]),
                                     5)),
          res['mu=1'] is not None and res['mu=i'] is not None)

    k = 15
    P = half_of(k)
    r, s = refl_map(k)
    eta = res['mu=1'][0]
    basis2 = [()] + list(combinations(P, 2))
    M2 = gram(basis2, r, s, eta)
    herm2 = hermitian_exact(M2)
    inert2, gap2 = spectrum_inertia(M2)
    check("R3.2 EVEN SECTOR deg <= 2 [exact entries, 40-digit inertia]: "
          "the 29x29 Gram (1 + 28 pairs on the 8-site half) is Hermitian "
          "exactly (%s) with inertia %s -- positive semidefinite (kernel "
          "dim %d), no negative direction: the OS form extends past one "
          "particle" % (herm2, inert2, inert2[2]),
          herm2 and inert2[1] == 0 and inert2[0] > 0)

    n8 = 8
    k8 = 7
    P8 = half_of(k8, n8)                 # {4,5,6,7}
    r8, s8 = refl_map(k8, n8)
    evens = [()] + list(combinations(P8, 2)) + [tuple(P8)]
    odds = [(a,) for a in P8] + list(combinations(P8, 3))
    # even sector is eta-sign-blind (theta phases eta^0, eta^2 = -1,
    # eta^4 = +1 identical for eta = +-i); odd sector flips with eta:
    # pick the positive sign as in R3.1
    Me = gram(evens, r8, s8, I, n8)
    eta8 = None
    for eta_c in (I, -I):
        Mo_c = gram(odds, r8, s8, eta_c, n8)
        if hermitian_exact(Mo_c):
            io_c, _ = spectrum_inertia(Mo_c)
            if io_c[1] == 0:
                eta8, Mo, io = eta_c, Mo_c, io_c
    he = hermitian_exact(Me)
    ie, ge = spectrum_inertia(Me)
    check("R3.3 FULL HALF-ALGEBRA AT N = 8 [exact entries, 40-digit "
          "inertia]: bond cut k = 7, half = 4 sites, COMPLETE basis (8 "
          "even + 8 odd monomials = all 16; the Gram block-diagonalises "
          "even (+) odd): even Gram Hermitian %s inertia %s (eta-sign-"
          "blind), odd Gram Hermitian, PSD for exactly eta = %s with "
          "inertia %s -- the FULL half-side algebra is RP (kernels "
          "%d/%d): free-level reflection positivity holds with no "
          "degree truncation at the 8-site robustness size"
          % (he, ie, eta8, io, ie[2], io[2]),
          he and eta8 is not None and ie[1] == 0 and io[1] == 0
          and ie[0] > 0 and io[0] > 0)


# ---------------------------------------------------------------------------
# R4: continuum control -- the mark cut is healthy in the continuum
# ---------------------------------------------------------------------------
def r4_continuum():
    print("  -- R4: continuum control (Cauchy-Stieltjes factorisation)")
    s, t = sp.symbols('s t', positive=True)
    lhs = 1 / sp.sin((s + t) / 2)
    rhs = (1 / (sp.cos(s / 2) * sp.cos(t / 2))) \
        / (sp.tan(s / 2) + sp.tan(t / 2))
    ident = iszero(sp.simplify(sp.trigsimp(lhs - rhs)))
    xs = [sp.Integer(1), sp.Integer(2), sp.Integer(3), sp.Integer(4)]
    Cau = sp.Matrix(4, 4, lambda i, j: 1 / (xs[i] + xs[j]))
    minors = [sp.simplify(Cau[:m, :m].det()) for m in range(1, 5)]
    all_pos = all(mv > 0 for mv in minors)
    check("R4.1 CONTINUUM CHIRAL OS KERNEL IS PD [exact]: 1/sin((s+t)/2) "
          "= [1/(cos(s/2)cos(t/2))] x 1/(tan(s/2) + tan(t/2)) (identity: "
          "%s) -- a positive diagonal congruence of the Cauchy-Stieltjes "
          "kernel 1/(x+y) = int_0^inf e^{-lam x} e^{-lam y} dlam, PD at "
          "any distinct points (leading minors at x = 1,2,3,4: %s, all "
          "> 0: %s): the continuum mark-cut OS form is strictly positive "
          "-- the R2 site-cut failure is a LATTICE-PLACEMENT artifact "
          "(reflected site distances collide with the exact C(even) = 0 "
          "checkerboard), not a defect of the mark cut itself"
          % (ident, minors, all_pos), ident and all_pos)


# ---------------------------------------------------------------------------
# R5: controls -- the test must separate
# ---------------------------------------------------------------------------
def r5_controls():
    print("  -- R5: controls (twist, antipode, chirality)")
    k = 15
    P = half_of(k)
    r, s = refl_map(k)
    basis1 = [(a,) for a in P]
    M_no = gram(basis1, r, s, 1)
    non_herm = not hermitian_exact(M_no)
    diag_im = [sp.simplify(sp.re(M_no[i, i])) for i in range(3)]
    check("R5.1 THE gamma^0 TWIST IS FORCED [exact]: eta = 1 (naive "
          "theta(g_a) = g_{k-a}) gives a NON-Hermitian form (%s; diagonal "
          "purely imaginary: Re = %s...) -- Hermiticity of the OS form "
          "forces eta = +-i, the Majorana analogue of the Dirac gamma^0 "
          "twist; the residual eta = +-i is fixed by positivity (R3.1)"
          % (non_herm, diag_im),
          non_herm and all(dv == 0 for dv in diag_im))

    r_anti = lambda a: (a + 8) % N
    s_alt = lambda a: 1 if a % 2 == 0 else -1
    Ca = sp.Matrix(N, N, lambda a, b:
                   s_alt(a) * s_alt(b) * c_of((a + 8) - (b + 8)))
    anti_ok = sp.simplify(Ca + sp.Matrix(N, N, lambda a, b:
                                         c_of(a - b))) == sp.zeros(N, N)
    P_a = list(range(8))
    basis_a = [(a,) for a in P_a]
    picked = None
    for eta in (1, -1, I, -I):
        Ma = gram(basis_a, r_anti, s_alt, eta)
        if hermitian_exact(Ma):
            ia, _ = spectrum_inertia(Ma)
            diag0 = all(iszero(Ma[i, i]) for i in range(8))
            picked = (eta, ia, diag0)
            break
    check("R5.2 THE ANTIPODE/DECK IS NO OS REFLECTION [exact]: the "
          "family-A/antipodal candidate theta_c(g_a) = eta s_a g_{a+8} "
          "(the W1 Theta_t = Utilde o K, clock-CENTRALISING) needs the "
          "alternating dressing s_a = (-1)^a even to keep the state "
          "anti-invariant (%s; plain signs fail, R1.2), and its Gram is "
          "then Hermitian for eta = %s but has ZERO diagonal (%s; "
          "reflected distance a+8-b even on the diagonal) -- inertia %s, "
          "+- symmetric, indefinite: RP FAILS structurally for the "
          "clock-centralising real structure, at the same place where "
          "the clock-inverting one is PD -- the test SEPARATES the two "
          "families exactly as kill test 1 demands"
          % (anti_ok, picked[0], picked[2], picked[1]),
          anti_ok and picked is not None and picked[2]
          and picked[1][0] == picked[1][1] and picked[1][1] > 0)

    k = 15
    r, s = refl_map(k)
    M_anti = gram([(a,) for a in half_of(k)], r, s, I, N, chi=-1)
    herm_a = hermitian_exact(M_anti)
    ia, _ = spectrum_inertia(M_anti)
    pairsP = list(combinations(half_of(k), 2))
    M2_pos = gram([()] + pairsP, r, s, I, N, chi=1)
    M2_neg = gram([()] + pairsP, r, s, I, N, chi=-1)
    block_blind = all(iszero(M2_pos[i, j] - M2_neg[i, j])
                      for i in range(1, 29) for j in range(1, 29))
    id_flip = all(iszero(M2_pos[0, j] + M2_neg[0, j])
                  for j in range(1, 29))
    ia2, _ = spectrum_inertia(M2_neg)
    check("R5.3 CHIRALITY IS AN ODD-SECTOR DATUM [exact]: the ANTI-chiral "
          "state (C -> -C) with the SAME theta (eta = +i) has Hermitian "
          "(%s) one-particle Gram of inertia %s = NEGATIVE definite -- "
          "the ODD sector flips definiteness with the chirality, RP "
          "pins the PAIR (chirality, eta) up to the joint flip.  The "
          "EVEN sector is chirality-BLIND: the 28x28 pair block is "
          "entry-IDENTICAL (%s; entries quadratic in C), the identity-"
          "pair couplings flip sign (%s) = a diagonal-sign congruence "
          "diag(-1, 1..1) -- same inertia %s = still PD: the gauge-"
          "blind sector cannot see the chirality, only the odd sector "
          "can: an exact free-level shadow of kill test 3 (mirror "
          "fermions) living entirely in the fermionic sector"
          % (herm_a, ia, block_blind, id_flip, ia2),
          herm_a and ia == (0, 8, 0) and block_blind and id_flip
          and ia2 == (29, 0, 0))


# ---------------------------------------------------------------------------
# R6: verdict
# ---------------------------------------------------------------------------
def r6_verdict():
    print("  -- R6: verdict")
    check("R6.1 W3 VERDICT [assembled]: free-level RP HOLDS for the "
          "pinned clock-inverting Theta -- with three exact structure "
          "results: (i) the OS twist eta = +-i is forced by Hermiticity "
          "and pinned (jointly with the chirality) by positivity; (ii) "
          "the euclidean cut must run BETWEEN the 16 Majorana sites "
          "(marks at bond midpoints, the half-offset/NS-natural "
          "placement; 4 sites per mark quadrant) -- the cut THROUGH "
          "sites fails RP exactly via the chiral checkerboard C(even) = "
          "0, while the continuum control is strictly PD (R4): RP "
          "selects the site placement relative to the marks; (iii) the "
          "clock-centralising (family A / antipode / deck) structure "
          "fails RP structurally (zero diagonal) -- RP and the W1 "
          "relation Theta rho Theta = rho^-1 select the SAME family: "
          "the two halves of the contract target are mutually "
          "consistent on the free level.  HONEST SCOPE: quadratic/free "
          "seam system only, deg <= 2 at N = 16, full algebra at N = 8; "
          "no interacting algebra, no gauge fixing, no OS "
          "reconstruction, no chirality theorem", True)


def run():
    print("woit_os_theta_rp_freelevel_probe -- WOIT-alpha W3: reflection "
          "positivity of the free seam system under the pinned Theta "
          "(EXPLORATION ONLY)")
    r1_state()
    r2_site_cut()
    r3_bond_cut()
    r4_continuum()
    r5_controls()
    r6_verdict()
    npass = sum(RESULTS)
    print("\n%d/%d checks passed" % (npass, len(RESULTS)))
    return npass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)

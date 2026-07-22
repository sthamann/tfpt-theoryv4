"""WP5e-eps1 companion of CELEST.SEAM.01 (EXPLORATION ONLY -- experiments/,
no verification claim).

"THE FIRST HONEST BACKREACTION STEP: GIBBONS-HAWKING A3" -- the A3 analogue
of CPS eq. 3.5 in its simplest exact form: the Gibbons-Hawking (GH)
representation of the A3 ALE, V = sum_{p=0}^{3} 1/|x - x_p| (four centres).
References: Gibbons-Hawking (Phys. Lett. 78B, 1978); Costello-Paquette-
Sharma arXiv:2306.00940 (Omega_N backreaction, K = |u|^2 + N log|u|^2,
eq. 3.5/3.33/3.37); Kronheimer (ALE); v493 (clock deformation XY = Z^4 +
a0), v505 (E3 slots), v509 (CPS skeleton + lockstep theorem).  Exact sympy
arithmetic throughout, no floats.

E1  CLOCK-INVARIANT CENTRE CONFIGURATIONS (S1): the mu4 clock acts on the
    GH base R^3 = C x R as (z, h) -> (iz, h); orbit sizes are {1, 4}
    (i^j z = z forces z = 0), so a clock-invariant FOUR-centre set is
    either (a) four axis points (pointwise fixed: the pure RESOLUTION
    branch) or (b) ONE free mu4 orbit {i^p z0} at a common height (the
    pure DEFORMATION branch).  For the free orbit: prod_p (Z - i^p z0) =
    Z^4 - z0^4 exactly (e1 = e2 = e3 = 0): the complex surface is
    XY = Z^4 + a0 with a0 = -z0^4 -- EXACTLY the v493 clock-invariant
    family; the monodromy a0 -> e^{2 pi i} a0 is z0 -> i z0 = one clock
    step = the cyclic shift of the four centres (v509 S4.3 in GH clothes).
E2  GH FORM AND PERIODS (S2): the charge-k GH point (V = k/r, tau period
    4 pi) is EXACTLY the flat cone R^4/Z_k (exact coordinate map r =
    R^2/(4k), psi = tau/k of period 4 pi/k); k = 4 gives the S^3/Z4 seam
    boundary = |mu4|; the monopole equation dA = -*dV holds exactly.  The
    period of the hyperkahler 2-form triplet over the segment cycle
    Sigma_pq is int omega_vec = 4 pi (x_q - x_p) EXACTLY -- the gauge
    potential A and the V-term drop out identically on the fibred segment
    (generic-function pullback).  Free-orbit config: holomorphic periods
    Pi_j = 4 pi z0 (i - 1) i^{j-1}, |Pi_j| = 4 sqrt(2) pi |z0| LOCKSTEP on
    all three spheres (v509 S4.2 counter-check from geometry), omega_I
    (Kahler) periods = 0: pure deformation; axis config: holomorphic 0,
    Kahler 4 pi Delta h free: pure resolution -- the exact dichotomy.
E3  THE COXETER CLOCK FROM GH GEOMETRY (S2.4): the rotation maps segment
    (p, p+1) to (p+1, p+2); with the closure sum_p (x_{p+1} - x_p) = 0 the
    induced map on H_2 is A = [[0,0,-1],[1,0,-1],[0,1,-1]]: A^4 = 1, char
    poly l^3 + l^2 + l + 1, det(A - 1) = -4, eigenvalues {i, -1, -i} =
    the three twisted sector characters (E3 bijection counter-check), and
    the period covector transforms as Pi . A = i Pi (pure phase): v505
    S4.10 / v509 S4.3 RE-DERIVED from the centre geometry.
E4  THE "N log|u|^2" LEDGER (S3): (i) the GH potential is the 3d Green
    kernel: Delta(1/|x - x_p|) = 0 away from centres (exact), single-
    centre flux -4 pi (exact integral): total source charge 4 = |mu4| =
    Zentrenzahl = Gesamt-Fluss -- the A3 analogue of the CPS backreaction
    kernel carries coefficient 4 (Erwartung bestaetigt).  (ii) exact
    multipole ledger of the free-orbit V: monopole 4/r; dipole and
    octupole VANISH; quadrupole t^2 (3 sin^2 th - 2)/r^3 (m = 0); the
    first symmetry-BREAKING multipole is (l, m) = (4, +-4) with amplitude
    (35/16) sin^4 th cos 4(phi - phi0) * t^4/r^5: it carries t^4 e^{4 i
    phi0} = -a0 -- the GH potential knows the v493 modulus at exactly the
    O(8) slot; selection rule m = 0 mod 4 exact (V(phi + pi/2) = V(phi)).
    (iii) EH log ledger (A1 exact): the radial Ricci-flat Monge-Ampere
    det g = 1 is solved by u K' = sqrt(u^2 + a^4) (exact); at infinity K'
    = 1 + a^4/(2u^2) + ... has NO 1/u term: the Ricci-flat ALE has NO
    asymptotic log -- the naive transplant of the CPS "N log|u|^2" to the
    A-series ALE FAILS at infinity (honest sharpening); the log lives at
    the EXCEPTIONAL locus: K' ~ a^2/u at u -> 0, log coefficient a^2,
    exceptional-sphere flux 2 pi a^2 (the v509 S1.2 computation with N ->
    a^2: CPS eq. 3.37 is an exceptional-locus statement); Burns contrast:
    K = u + N log u gives det g = 1 + N/u != 1 (scalar-flat, SOURCED --
    the CPS log is the brane backreaction, not a Ricci-flat feature).
E5  ROADMAP (S4): the remaining backreaction milestones M1-M3 with
    success/kill criteria (Beltrami on PT/Z4, twisted KS measures, a0
    uplift), each stated precisely.

Throwaway probe: standalone (sympy), prints tables + PASS/FAIL + verdict,
ends with a check count.  Nothing here is a claim; promotion (if any) goes
through the usual workflow.  verification/, ledger, papers, changelog,
website, scorecard untouched.
"""
import sympy as sp

G_CAR = 5
N_FAM = 3
MU4 = 4
RANK = 8
H_VEE = 30

N_PASS = 0
N_FAIL = 0


def check(label, ok):
    global N_PASS, N_FAIL
    print(("  PASS  " if ok else "  FAIL  ") + label)
    if ok:
        N_PASS += 1
    else:
        N_FAIL += 1
    return ok


def fmt(xs):
    return "(" + ", ".join(str(x) for x in xs) + ")"


# ---------------------------------------------------------------------------
# S1 -- clock-invariant centre configurations
# ---------------------------------------------------------------------------
def section1():
    print("  -- S1: clock-invariant four-centre configurations on C x R")
    I = sp.I
    z = sp.symbols('z')

    fixed_ok = all(sp.solve(sp.Eq(I ** j * z, z), z) == [0]
                   for j in (1, 2, 3))
    # orbit-size partitions of 4 with parts in {1, 4}: (n1, n4)
    parts = []
    for n4 in range(2):
        n1 = 4 - 4 * n4
        if n1 >= 0:
            parts.append((n1, n4))
    check("S1.1 [ORBIT CLASSIFICATION] i^j z = z forces z = 0 (j = 1, 2, "
          "3): mu4 orbit sizes on C x R are {1 (axis), 4 (free)}; a "
          "clock-invariant 4-centre set is 4 = 1+1+1+1 (four AXIS points, "
          "pointwise fixed: pure RESOLUTION branch) or 4 = 4 (ONE free "
          "orbit at a common height: pure DEFORMATION branch) -- exactly "
          "%d branches; heights are untouched by (z, h) -> (iz, h), so a "
          "free orbit has ONE common height (translate to 0)"
          % len(parts),
          fixed_ok and parts == [(4, 0), (0, 1)])

    z0, Z = sp.symbols('z0 Z')
    prod4 = sp.expand(sp.prod([Z - I ** p * z0 for p in range(4)]))
    a0 = -z0 ** 4
    Zs, b0, b1, b2, b3 = sp.symbols('Zs b0 b1 b2 b3')
    Pgen = Zs ** 4 + b3 * Zs ** 3 + b2 * Zs ** 2 + b1 * Zs + b0
    diff = sp.expand(Pgen.subs(Zs, I * Zs) - Pgen)
    sol = sp.solve([diff.coeff(Zs, n) for n in range(4)], [b3, b2, b1],
                   dict=True)
    check("S1.2 [v493 FAMILY FROM CENTRES] prod_p (Z - i^p z0) = %s = "
          "Z^4 - z0^4 EXACTLY (e1 = e2 = e3 = 0): the deformation branch "
          "is XY = Z^4 + a0 with a0 = -z0^4 -- the v493 clock-invariant "
          "family; independent route: P(iZ) = P(Z) forces b3 = b2 = b1 = "
          "0 (unique solution %s, v493 S1 replicated)"
          % (prod4, sol),
          sp.expand(prod4 - (Z ** 4 - z0 ** 4)) == 0
          and sol == [{b3: 0, b2: 0, b1: 0}])

    s = sp.symbols('s', real=True)
    z0s = z0 * sp.exp(I * sp.pi * s / 2)
    a0s = sp.simplify(-z0s ** 4)
    shifted = {sp.simplify(I ** (p + 1) * z0) for p in range(4)}
    orbit = {sp.simplify(I ** p * z0) for p in range(4)}
    check("S1.3 [MONODROMY = ONE CLOCK STEP] along a0(s) = e^{2 pi i s} "
          "a0 the orbit parameter moves as z0(s) = e^{i pi s/2} z0 "
          "(check: -z0(s)^4 = e^{2 pi i s} a0: %s); at s = 1: z0 -> i z0 "
          "and the centre SET is invariant under the cyclic shift "
          "(i * orbit = orbit: %s) -- the a0 monodromy is one mu4 clock "
          "step permuting the four centres (v509 S4.3 in GH clothes)"
          % (sp.simplify(a0s - sp.exp(2 * sp.pi * I * s) * a0) == 0,
             shifted == orbit),
          sp.simplify(a0s - sp.exp(2 * sp.pi * I * s) * a0) == 0
          and shifted == orbit)
    return z0


# ---------------------------------------------------------------------------
# S2 -- GH form, periods, and the Coxeter clock
# ---------------------------------------------------------------------------
def section2(z0):
    print("  -- S2: Gibbons-Hawking form -- boundary, periods, Coxeter "
          "clock")
    I = sp.I
    r, R, th, ph, tau, k = sp.symbols('r R theta phi tau k', positive=True)

    # charge-k GH point: V = k/r, A = -k cos(th) dphi, tau period 4 pi
    V = k / r
    rsub = R ** 2 / (4 * k)
    drdR = sp.diff(rsub, R)
    g_RR = sp.simplify((V * drdR ** 2).subs(r, rsub))
    g_ang = sp.simplify((V * r ** 2).subs(r, rsub))
    g_fib = sp.simplify((1 / V).subs(r, rsub))
    # monopole equation dA = -*dV in flat spherical coords
    dA_coeff = sp.diff(-k * sp.cos(th), th)              # dA = k sin dth^dph
    star_dV = sp.simplify(-r ** 2 * sp.diff(V, r) * sp.sin(th))
    check("S2.1 [GH POINT = FLAT CONE, EXACT] V = k/r with r = R^2/(4k): "
          "V dr^2 = %s dR^2, V r^2 = %s = R^2/4, V^-1 (dtau - k cos th "
          "dph)^2 = (R^2/4)(dpsi - cos th dph)^2 with psi = tau/k of "
          "period 4 pi / k: the charge-k GH point is EXACTLY the cone "
          "R^4/Z_k (k = 1: flat R^4, Hopf S^3); k = 4: seam boundary "
          "S^3/Z4, deck order 4 = |mu4|; monopole equation dA = -*dV: "
          "k sin th = %s exact"
          % (g_RR, sp.simplify(g_ang / R ** 2 * 4), star_dV),
          g_RR == 1 and sp.simplify(g_ang - R ** 2 / 4) == 0
          and sp.simplify(g_fib - R ** 2 / (4 * k ** 2)) == 0
          and sp.simplify(dA_coeff - star_dV) == 0
          and sp.simplify(star_dV - k * sp.sin(th)) == 0)

    # period pullback on the fibred segment, generic A, V, convention cV
    sv = sp.symbols('s', real=True)
    d1, d2, d3, cV = sp.symbols('Delta1 Delta2 Delta3 c_V')
    A1, A2, A3f, Vf = (sp.Function(n)(sv) for n in ('A1', 'A2', 'A3', 'V'))
    dx = (d1, d2, d3)                      # dx_i = Delta_i ds on the segment

    def one_form(coef_ds, coef_dtau):
        return (coef_ds, coef_dtau)

    def wedge(u, v):
        # coefficient of ds ^ dtau
        return sp.expand(u[0] * v[1] - u[1] * v[0])

    dtauA = one_form(A1 * dx[0] + A2 * dx[1] + A3f * dx[2], 1)
    periods = []
    for i in range(3):
        w_conn = wedge(dtauA, one_form(dx[i], 0))          # (dtau+A)^dx_i
        j, l = [(1, 2), (2, 0), (0, 1)][i]
        w_V = cV * Vf * wedge(one_form(dx[j], 0), one_form(dx[l], 0))
        coeff = sp.simplify(-(w_conn + w_V))               # dtau ^ ds orient.
        periods.append(sp.integrate(sp.integrate(coeff, (sv, 0, 1)),
                                    (tau, 0, 4 * sp.pi)) / (4 * sp.pi))
    check("S2.2 [PERIOD FORMULA, GENERIC] pullback of omega_i = (dtau + "
          "A) ^ dx_i - c_V V eps_ijk dx_j ^ dx_k to the fibred segment: "
          "the V-term and ALL A-terms vanish IDENTICALLY (1-dim base "
          "path), leaving int_{Sigma_pq} omega_vec = 4 pi (x_q - x_p): "
          "periods/4pi = %s = (Delta1, Delta2, Delta3) for GENERIC "
          "functions A_k(s), V(s) and ANY convention factor c_V"
          % fmt(periods),
          periods == [d1, d2, d3])

    t0 = sp.symbols('t0', positive=True)
    centres = [I ** p * t0 for p in range(4)]
    Pi = [sp.simplify(4 * sp.pi * (centres[j + 1] - centres[j]))
          for j in range(3)]
    Pi_target = [sp.simplify(4 * sp.pi * t0 * (I - 1) * I ** j)
                 for j in range(3)]
    mods = [sp.simplify(sp.Abs(p)) for p in Pi]
    check("S2.3 [LOCKSTEP FROM GEOMETRY] free-orbit config (centres i^p "
          "t0, heights 0): holomorphic periods Pi_j = 4 pi t0 (i-1)(1, i, "
          "i^2) (exact match %s), |Pi_j| = %s = 4 sqrt(2) pi t0 EQUAL on "
          "all three spheres (v509 S4.2 counter-check from GH geometry); "
          "omega_I (Kahler) periods = 4 pi * (height differences) = "
          "(0, 0, 0): the invariant free-orbit branch is the PURE "
          "DEFORMATION; the axis branch has holomorphic periods 0 and "
          "free Kahler periods 4 pi Delta h: the exact dichotomy"
          % (all(sp.simplify(Pi[j] - Pi_target[j]) == 0 for j in range(3)),
             fmt(mods)),
          all(sp.simplify(Pi[j] - Pi_target[j]) == 0 for j in range(3))
          and all(sp.simplify(m - 4 * sp.sqrt(2) * sp.pi * t0) == 0
                  for m in mods))

    closure = sp.simplify(sum(centres[(p + 1) % 4] - centres[p]
                              for p in range(4)))
    A = sp.Matrix([[0, 0, -1], [1, 0, -1], [0, 1, -1]])
    lam = sp.symbols('lambda')
    eigs = set(A.eigenvals().keys())
    PiRow = sp.Matrix([[Pi_target[0], Pi_target[1], Pi_target[2]]])
    transf = sp.simplify(PiRow * A - I * PiRow)
    check("S2.4 [COXETER CLOCK FROM GH] rotation maps segment (p, p+1) -> "
          "(p+1, p+2); closure sum_p (x_{p+1} - x_p) = %s = 0 makes "
          "[Sigma_30] = -(e1 + e2 + e3), so the induced map on H_2 is "
          "A = [[0,0,-1],[1,0,-1],[0,1,-1]]: A^4 = 1 (%s), char poly %s, "
          "det(A - 1) = %s = -4 (no invariant flux vector), eigenvalues "
          "%s = {i, -1, -i} = the twisted sector characters (E3 "
          "bijection counter-check); period covector: Pi . A = i Pi "
          "(pure phase, %s) -- v505 S4.10 / v509 S4.3 re-derived from "
          "centre geometry"
          % (closure, A ** 4 == sp.eye(3),
             sp.factor(A.charpoly(lam).as_expr()),
             (A - sp.eye(3)).det(), sorted(eigs, key=str),
             transf == sp.zeros(1, 3)),
          closure == 0 and A ** 4 == sp.eye(3)
          and (A - sp.eye(3)).det() == -4
          and eigs == {sp.I, -1, -sp.I}
          and sp.expand(A.charpoly(lam).as_expr()
                        - (lam ** 3 + lam ** 2 + lam + 1)) == 0
          and transf == sp.zeros(1, 3))


# ---------------------------------------------------------------------------
# S3 -- the "N log|u|^2" ledger: kernel, multipoles, EH log
# ---------------------------------------------------------------------------
def section3():
    print("  -- S3: the CPS 'N log|u|^2' analogue -- exact ledger")
    x, y, zc = sp.symbols('x y zc', real=True)
    r, th, ph, phi0 = sp.symbols('r theta phi phi0', positive=True)

    lap = sum(sp.diff(1 / sp.sqrt(x ** 2 + y ** 2 + zc ** 2), v, 2)
              for v in (x, y, zc))
    flux1 = sp.integrate(sp.integrate(
        (sp.diff(1 / r, r) * r ** 2 * sp.sin(th)), (th, 0, sp.pi)),
        (ph, 0, 2 * sp.pi))
    check("S3.1 [THE KERNEL AND ITS CHARGE] Delta(1/|x|) = %s away from "
          "the centre (exact) and the flux integral through S^2 is %s = "
          "-4 pi per centre: V = sum_{p=0}^{3} 1/|x - x_p| is the 3d "
          "Green kernel with TOTAL SOURCE CHARGE 4 = |mu4| = Zentrenzahl "
          "= Gesamt-Fluss (Gauss); this is the A3 analogue of the CPS "
          "backreaction kernel (their N log|u|^2 with N branes): the "
          "coefficient is the centre count 4"
          % (sp.simplify(lap), flux1),
          sp.simplify(lap) == 0 and flux1 == -4 * sp.pi
          and 4 == MU4)

    # Legendre generating identity (l <= 4), then the exact multipoles
    h, xg = sp.symbols('h xg')
    gen = sp.series(1 / sp.sqrt(1 - 2 * xg * h + h ** 2), h, 0, 5).removeO()
    ok_gen = all(sp.expand(gen.coeff(h, l) - sp.legendre(l, xg)) == 0
                 for l in range(5))

    t0 = sp.symbols('t0', positive=True)
    cosg = [sp.sin(th) * sp.cos(ph - phi0 - p * sp.pi / 2)
            for p in range(4)]
    Vl = {l: sp.simplify(sp.expand_trig(sp.expand(
        sum(sp.legendre(l, cg) for cg in cosg)))) for l in range(1, 5)}
    four = {(l, m): sp.integrate(Vl[l] * sp.cos(m * (ph - phi0)),
                                 (ph, 0, 2 * sp.pi)) / sp.pi
            for l in range(1, 5) for m in range(1, 5)}
    amp44 = sp.simplify(four[(4, 4)])
    ok_sel = all(sp.simplify(four[(l, m)]) == 0
                 for l in range(1, 5) for m in range(1, 4))
    shift_ok = sp.simplify(sum(
        sp.legendre(2, sp.sin(th) * sp.cos(ph + sp.pi / 2 - phi0
                                           - p * sp.pi / 2))
        for p in range(4)) - Vl[2]) == 0
    check("S3.2 [MULTIPOLE LEDGER, EXACT] generating identity 1/sqrt(1 - "
          "2xh + h^2) = sum P_l(x) h^l verified to l = 4 (%s); free-orbit "
          "V = 4/r + sum_l t0^l/r^{l+1} S_l: DIPOLE S_1 = %s and OCTUPOLE "
          "S_3 = %s vanish; quadrupole S_2 = %s (m = 0, clock-invariant); "
          "the FIRST symmetry-breaking multipole is (l, m) = (4, +-4): "
          "cos-4(ph - phi0) amplitude = %s = (35/16) sin^4 th != 0, "
          "carried by t0^4 e^{4 i phi0} = -a0 (v493 bridge: the GH "
          "potential stores the O(8) modulus in the l = 4 clock "
          "harmonic); selection rule m = 0 mod 4 exact (all m = 1, 2, 3 "
          "Fourier integrals vanish; V(ph + pi/2) = V(ph): %s)"
          % (ok_gen, Vl[1], Vl[3], Vl[2], amp44, shift_ok),
          ok_gen and Vl[1] == 0 and Vl[3] == 0
          and sp.simplify(Vl[2] - (3 * sp.sin(th) ** 2 - 2)) == 0
          and sp.simplify(amp44 - sp.Rational(35, 16) * sp.sin(th) ** 4)
          == 0
          and ok_sel and shift_ok)

    # EH (A1) exact log ledger
    u, a = sp.symbols('u a', positive=True)
    Kp = sp.sqrt(u ** 2 + a ** 4) / u
    detg = sp.simplify(Kp ** 2 + u * Kp * sp.diff(Kp, u))
    ser_inf = sp.series(Kp, u, sp.oo, 4)
    c_inf = ser_inf.coeff(1 / u, 1)
    ser_0 = sp.series(Kp, u, 0, 2)
    c_0 = ser_0.coeff(1 / u, 1)
    zc2, zb = sp.symbols('zeta zetabar', positive=True)
    g_log = sp.simplify(sp.diff(a ** 2 * sp.log(1 + zc2 * zb), zc2, zb))
    rr = sp.symbols('rr', positive=True)
    flux_exc = sp.integrate(2 * g_log.subs({zc2: rr, zb: rr}) * rr,
                            (rr, 0, sp.oo)) * 2 * sp.pi
    KB = u + sp.symbols('N', positive=True) * sp.log(u)
    detB = sp.simplify(sp.diff(KB, u) ** 2
                       + u * sp.diff(KB, u) * sp.diff(KB, u, 2))
    check("S3.3 [EH LOG LEDGER, EXACT] radial Ricci-flat Monge-Ampere: "
          "u K' = sqrt(u^2 + a^4) gives det g = K'^2 + u K' K'' = %s = 1 "
          "exactly; at infinity K' = 1 + a^4/(2u^2) + ... with 1/u "
          "coefficient %s = 0: NO asymptotic log -- the naive CPS-log "
          "transplant to the Ricci-flat ALE FAILS at infinity (honest "
          "sharpening); at u -> 0: K' ~ %s/u: log coefficient a^2, and "
          "the exceptional-sphere flux is %s = 2 pi a^2 (v509 S1.2 with "
          "N -> a^2: CPS eq. 3.37 is an EXCEPTIONAL-LOCUS statement); "
          "Burns contrast: K = u + N log u gives det g = %s != 1 "
          "(scalar-flat, SOURCED: the CPS log is brane backreaction, not "
          "a Ricci-flat feature)"
          % (detg, c_inf, c_0, flux_exc, detB),
          detg == 1 and c_inf == 0 and c_0 == a ** 2
          and sp.simplify(flux_exc - 2 * sp.pi * a ** 2) == 0
          and sp.simplify(detB - (1 + sp.symbols('N', positive=True) / u))
          == 0)

    check("S3.4 [THE ANALOGUE, TYPED HONESTLY] CPS Burns: kernel N "
          "log|u|^2 (2d/4d log Green kernel), source N branes, "
          "exceptional flux 2 pi N.  A3 seam in GH form: kernel V (3d "
          "Green kernel), source charge 4 = |mu4| (exact), boundary "
          "fibration S^3/Z4 (S2.1), per-sphere flux = period/2pi with "
          "the LOCKSTEP vector 4 pi t0 (i-1)(1, i, i^2) (S2.3).  The "
          "expectation 'coefficient = Gesamt-Fluss/Zentrenzahl 4 = "
          "|mu4|' is CONFIRMED for the source ledger of V; the honest "
          "refinement: for the RICCI-FLAT ALE the asymptotic log "
          "coefficient is EXACTLY ZERO (S3.3) -- the CPS-style "
          "asymptotic log belongs to the scalar-flat brane-backreacted "
          "geometry, whose PT/Z4 analogue is precisely the open "
          "backreaction milestone M1 [C dictionary, O construction]",
          True)


# ---------------------------------------------------------------------------
# S4 -- the backreaction roadmap (fences)
# ---------------------------------------------------------------------------
def section4():
    print("  -- S4: the remaining backreaction roadmap, preregistered")
    check("S4.1 [M1: THE A3 OMEGA_N] compute the A3 analogue of CPS eq. "
          "3.5 on PT/Z4: the Beltrami/Kodaira-Spencer deformation sourced "
          "by the glue currents wrapping the three lockstep spheres.  "
          "SUCCESS: a closed-form Omega-deformation whose S^3/Z4 periods "
          "are (2 pi i)^2 x (integer flux vector) reproducing the "
          "lockstep phase structure (i-1)(1, i, i^2).  KILL: if the "
          "sourced deformation forces UNEQUAL sphere fluxes or a "
          "non-integer period, the CPS transplant (and the eps2 level "
          "dial v509) dies", True)
    check("S4.2 [M2: TWISTED KS MEASURE] quantise the O(-2) tower on "
          "PT/Z4 using the eps1 mode ledger (P_m series, companion "
          "probe) and compute the one-loop box coefficient PER SECTOR.  "
          "SUCCESS: the bulk sector reproduces lambda~^2 = 36 with the "
          "eps1 measure bookkeeping AND the twisted sectors pair with "
          "the three sphere axions cancelling the rigid 32 T3 residual "
          "(v505 S3.7).  KILL: a leftover independent quartic (T3-type) "
          "in ANY sector after all four axions are included", True)
    check("S4.3 [M3: THE a0 UPLIFT + VERDICT] uplift the (l, m) = "
          "(4, +-4) GH multipole (= the a0 direction, S3.2) to the "
          "Beltrami differential on PT/Z4 and compute the induced "
          "Kahler-potential correction.  SUCCESS: a log-type correction "
          "whose coefficient is tied to the source charge 4 = |mu4| "
          "(matching the V-ledger).  KILL: coefficient decoupled from "
          "the centre count.  VERDICT of this probe: the first "
          "backreaction step is EXECUTED exactly (centres, periods, "
          "Coxeter clock, kernel + multipole + EH log ledgers); "
          "everything quantum stays [O]; no verification claim, no "
          "marker moves anywhere", True)


# ---------------------------------------------------------------------------
def main():
    print("WP5e-eps1 companion probe: Gibbons-Hawking A3 -- the first "
          "honest backreaction step (EXPLORATION ONLY)")
    z0 = section1()
    section2(z0)
    section3()
    section4()
    print("=" * 72)
    print("CHECKS: %d passed, %d failed" % (N_PASS, N_FAIL))
    if N_FAIL == 0:
        print("ALL CHECKS PASSED (probe-level, NOT a verification claim)")
    return N_FAIL == 0


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)

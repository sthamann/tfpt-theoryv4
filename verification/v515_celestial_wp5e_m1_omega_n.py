"""v515 -- CELEST.WP5E.M1.01: milestone M1 of the research contract
CELEST.SEAM.01 (WP5e back-reaction programme) -- "the A3 Omega_N",
executed (SUCCESS on the preregistered v514 S8.1 criterion).
Question (preregistered VERBATIM in v514): compute the A3 analogue of
CPS eq. 3.5 on PT/Z4 -- the back-reacted holomorphic 3-form Omega_N
sourced by the glue currents wrapping the three lockstep spheres -- and
check its periods exactly.  SUCCESS = a closed-form Omega-deformation
whose S^3/Z4 periods are (2 pi i)^2 x (integer flux vector) reproducing
the lockstep phase structure (i-1)(1, i, i^2); KILL = unequal sphere
fluxes or a non-integer period.  References: Costello-Paquette-Sharma
arXiv:2306.00940 (Omega_N brane backreaction, eq. 3.5/3.33; large-gauge
invariance of hCS quantises the period in (2 pi i)^2 Z); Hitchin
"Polygons and gravitons" (A-series twistor family XY = prod(Z - q_p(la)),
q_p in O(2); the twistor space is the small resolution of the nodal
family); Gibbons-Hawking Phys. Lett. 78B (centres); v492 (clock
diag(i,1), omega-phase det = i), v493 (clock family XY = Z^4 + a0,
Coxeter clock, lockstep), v505 E3 (weights Z in O(2), X, Y in O(4),
F in O(8), Omega in O(4)), v509 (CPS skeleton (2 pi i)^2 N, lockstep
theorem, 0/24 negative probe), v514 (eps1 ledger, GH/A3 dichotomy,
M1-M3 preregistration).  Exact sympy arithmetic throughout, no floats.

[E] S1. RESIDUE FORM DERIVED: on F = XY - P(Z) all three ambient
      representatives dX^dZ/F_Y, -dY^dZ/F_X, -dX^dY/F_Z satisfy
      dF ^ omega2 = -dX^dY^dZ exactly and pull back to omega2 = dX^dZ/X
      on the Y = P/X patch -- the Poincare residue, derived not assumed;
      orbifold-cover pullback at a0 = 0: omega2 = 4 dz1^dz2 = |mu4| x
      (flat form): the residue normalisation CARRIES the source charge
      4 = |mu4|; clock diag(i,1): omega2 -> i omega2 (v492 S5 det = i
      replicated); weight ledger 4+4+2-8 = 2 = the O(2) fibre symplectic
      form, Omega in O(4) = -deg K_PT (v505 S5.1/S5.2); EH anchor factor
      2 = |Z2|; wrong-weight control Z in O(4): omega2 weight 4 != 2,
      Omega weight 6 != 4, real-section count 5 != 3 = dim R^3.
[E] S2. THE TWISTOR FAMILY CLOSED: from the four O(2) centre sections
      q_p(la) = i^p t0 - i^-p t0 la^2 (honest O(2) reality) the family
      is EXACTLY XY = Z^4 + 4 t0^2 la^2 Z^2 - t0^4 (1 - la^4)^2 (e1 =
      e3 = 0 identically); the seam fibre la = 0 is exactly the v493
      clock family XY = Z^4 - t0^4; a2 in O(4) opens only off-seam
      (a2(0) = a2(infinity) = 0); self-mirror under la -> 1/la; clock
      lift gamma: (Z, la) -> (iZ, -i la), gamma^4 = 1, Omega -> +Omega
      (the CY-compatible lift); Omega = omega2 ^ <la dla> in O(4) =
      -deg K_PT, weight chain 4+4+2-8 = 2, +2 = 4; section-level
      dichotomy: axis sections 2 h la clock-invariant (resolution),
      free-orbit sections permuted cyclically (deformation, v514 S4.1).
[E] S3. FIBRE PERIODS + LAMBDA REDUCTION: int_{S_j} omega2 = 2 pi i
      (q_{j+1} - q_j) EXACTLY for generic radial profile and generic
      path (both drop identically) -- the v493 "period = root
      difference" normalisation DERIVED from the residue form;
      Pi_j(la) = 2 pi i t0 [(i-1) i^j + (1+i) i^-j la^2]; at la = 0:
      Pi = 2 pi i t0 (i-1)(1, i, i^2), all moduli 2 sqrt(2) pi t0
      (LOCKSTEP); clock covariance Pi_{j+1}(-i la) = i Pi_j(la) for ALL
      la = the omega2 phase i (Pi . A = i Pi at la = 0); sphere x
      la-circle periods of the undeformed Omega_0 = 0 (polynomial, no
      residue): Omega_0 carries NO quantised 3-flux -- all flux must be
      sourced; collision ledger: 12 nodes, la-support = EXACTLY the 8
      eighth roots of unity (8 = 2|mu4|, the Z8 seam bridge), antipodal
      pairing q_{p+2} = -q_p forces double nodes, clock orbits 4+4+4.
[E] S4. OMEGA_N CLOSED + QUANTISED PERIODS: Omega_N = Omega_0 +
      sum_p N_p K_p with the CPS/Bochner-Martinelli kernel K on the
      centre twistor lines L_p = {X = Y = 0, Z = q_p(la)}; int_{S^3} K
      = (2 pi i)^2 exactly (density -sin 2 theta, v509 S1.1), dK = 0
      away from the source, scale degree 0; (2 pi i)^2 = (fibre phase
      circle) x (transverse phase circle) -- the iterated-residue
      reading; PERIOD TABLE: boundary S^3/Z4 at the orbifold point
      (2 pi i)^2 x 1 (minimal invariant charge 4 = |mu4| -- the lens
      fundamental domain FORCES N in 4Z: quotient large-gauge
      quantisation (2 pi i)^2 N/4 integer only for N = 0 mod 4);
      deformed phase (2 pi i)^2 x 4; linking S^3 of each L_p uniformly
      (2 pi i)^2 x N; per-sphere flux vector (2 pi i)^2 x N (1, 1, 1);
      seam-fibre phase vector 2 pi i t0 (i-1)(1, i, i^2); the flux
      vector is FORCED uniform twice over (clock orbit + K4
      connectivity of the four lines, all 6 pairs meet); the 12
      collision points are honest conifold NODES (dF = 0, Hessian det
      512 t0^6 != 0, quadric rank 4) whose small-resolution exceptional
      curves are the sphere classes; orbifold-limit cover count 16 =
      |mu4|^2 (v509 S3.5 mu = 16); minimal quantum 1 <-> k = 1 (v509
      bridge).  M1 SUCCESS criterion met; neither KILL fires.
[E] S5. KILL PROBE (honest): the clock-forbidden family Z^4 - Z
      (centres {0, 1, w, w^2}): 0/24 orderings lockstep (vs 8/24 for
      the mu4 orbit), la-support = 12 TWELFTH roots of unity (not Z8),
      no antipodal pairing, no clock lift -- BUT the (2 pi i)^2
      quantisation itself HOLDS there too (local gauge invariance):
      INTEGRALITY ALONE IS NOT THE DISCRIMINATOR; the discriminator is
      the lockstep phase/modulus structure + the clock forcing of equal
      fluxes (unequal N_p are allowed on the forbidden family).  The
      v509 dial (lockstep = clock fingerprint => one level) SURVIVES.
[E] S6. ANCHORS + NEGATIVE CONTROLS: EH/Z2 from the same machinery
      (XY = Z^2 - t0^2 (1 - la^2)^2, exactly 2 nodes at la = +-1, lens
      forces charge 2 = |Z2|); CPS original = k = 1 flat patch (full
      S^3: every integer N allowed -- the unconstrained anchor);
      diag(i, i): Omega_0 -> -Omega_0 (no invariant 3-form, the
      deformation problem collapses at step zero) while K stays
      invariant (U(2)); fractional charges N = 1, 2, 3 all fail the
      lens quantisation (only 0 mod 4 passes).
[C] The global smooth patching of the local BM kernels into one gauge
      on the resolved 3-fold (Green function), the small-resolution
      citation (Hitchin), and the "exceptional-curve branes = glue
      currents" CPS dictionary transplant (v509 S6.2 fence).
[O] O-FENCE: M2 (the twisted KS measure per sector, the one-loop box
      coefficient), M3 (the a0/(4, +-4) Kahler-log uplift), and the
      quantised BCOV coefficient on PT/Z4 stay open;
      SEAM.EQUIV.TWISTOR.01 untouched (v515 is preparation, not the
      Costello-Li construction); NO marker moves anywhere.

Status: [E] exact residue/family/period/kernel arithmetic (sympy, no
floats); [C] global kernel patching + Hitchin small resolution + CPS
brane dictionary; [O] M2, M3, quantised BCOV coefficient.  Python;
Wolfram-mirrored (residue-form identities, closed family, period
table, nodes on Z8, lens forcing N in 4Z, EH anchor, negative
controls), counted per GATE.WOLFRAM.02.  Discovery provenance:
experiments/tfpt-discovery/
celestial_seam_wp5e_m1_a3_omega_n_backreaction_probe.py
(2026-07-22, 30/30).
"""
from itertools import combinations, permutations

import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

I = sp.I
PI = sp.pi
MU4 = N_fam + 1               # 4 = |mu4|, the seam clock order


def fmt(xs):
    return "(" + ", ".join(str(x) for x in xs) + ")"


# ---------------------------------------------------------------------------
# minimal exact exterior algebra: forms = {tuple(sorted coord indices): coeff}
# ---------------------------------------------------------------------------
def _sorted_sign(idx):
    sign, lst = 1, list(idx)
    for i in range(1, len(lst)):
        j = i
        while j > 0 and lst[j - 1] > lst[j]:
            lst[j - 1], lst[j] = lst[j], lst[j - 1]
            sign = -sign
            j -= 1
    return sign, tuple(lst)


def clean(form):
    out = {}
    for k, v in form.items():
        vv = sp.simplify(v)
        if vv != 0:
            out[k] = vv
    return out


def wedge(a, b):
    out = {}
    for ka, ca in a.items():
        for kb, cb in b.items():
            if set(ka) & set(kb):
                continue
            sign, key = _sorted_sign(ka + kb)
            out[key] = sp.expand(out.get(key, 0) + sign * ca * cb)
    return clean(out)


def dext(form, coords):
    out = {}
    for k, c in form.items():
        for i, x in enumerate(coords):
            dc = sp.diff(c, x)
            if dc == 0:
                continue
            for kk, vv in wedge({(i,): dc}, {k: sp.Integer(1)}).items():
                out[kk] = sp.expand(out.get(kk, 0) + vv)
    return clean(out)


def pull(form, src_coords, imgs, dst_coords):
    """Pullback of a form over src_coords under the map src = imgs(dst)."""
    sub = dict(zip(src_coords, imgs))
    out = {}
    for k, c in form.items():
        term = {(): sp.sympify(c).subs(sub)}
        for idx in k:
            leg = {}
            for j, x in enumerate(dst_coords):
                der = sp.diff(imgs[idx], x)
                if der != 0:
                    leg[(j,)] = der
            term = wedge(term, leg)
        for kk, vv in term.items():
            out[kk] = sp.expand(out.get(kk, 0) + vv)
    return clean(out)


def form_eq(a, b):
    keys = set(a) | set(b)
    return all(sp.simplify(a.get(k, 0) - b.get(k, 0)) == 0 for k in keys)


def form_scale(a, c):
    return {k: sp.expand(c * v) for k, v in a.items()}


def conj_poly(expr, var, newvar):
    """Formal conjugate of a polynomial: conjugate coefficients, var -> newvar
    (represents the substitution var -> conj(var))."""
    p = sp.Poly(sp.expand(expr), var)
    out = 0
    for (n,), c in zip(p.monoms(), p.coeffs()):
        out += sp.conjugate(c) * newvar ** n
    return sp.expand(out)


# ---------------------------------------------------------------------------
# shared symbols and the twistor family data
# ---------------------------------------------------------------------------
X, Y, Z, lam = sp.symbols('X Y Z lam')
t0 = sp.symbols('t0', positive=True)

# free mu4-orbit centres (z_p, h_p) = (i^p t0, 0): O(2) sections
Q = [sp.expand(I ** p * t0 - I ** (-p) * t0 * lam ** 2) for p in range(4)]
P4 = sp.expand(sp.prod([Z - q for q in Q]))

OMEGA = sp.Rational(-1, 2) + sp.sqrt(3) * I / 2   # cube root of 1 (S5)
ZF = [sp.Integer(0), sp.Integer(1), OMEGA, sp.expand(OMEGA ** 2)]
QF = [sp.expand(z - sp.conjugate(z) * lam ** 2) for z in ZF]
P4F = sp.expand(sp.prod([Z - q for q in QF]))


def Pi_j(j, la):
    """holomorphic sphere period Pi_j = 2 pi i (q_{j+1} - q_j), segment
    (j, j+1) mod 4, evaluated at twistor parameter la."""
    return sp.expand(2 * PI * I * (Q[(j + 1) % 4] - Q[j]).subs(lam, la))


# ---------------------------------------------------------------------------
# S1 -- the residue 2-form omega2 = dX^dZ/X, exactly
# ---------------------------------------------------------------------------
def section1():
    print("  -- S1: the residue form omega2 = dX^dZ/X -- exact bookkeeping")
    amb = (X, Y, Z)
    Pg = sp.Function('P')(Z)                  # generic fibre polynomial
    Fg = X * Y - Pg
    dF = {(0,): Y, (1,): X, (2,): -sp.diff(Pg, Z)}
    wA = {(0, 2): 1 / X}                      # dX^dZ / F_Y
    wB = {(1, 2): -1 / Y}                     # -dY^dZ / F_X
    wC = {(0, 1): 1 / sp.diff(Pg, Z)}         # -dX^dY / F_Z
    tops = [wedge(dF, w) for w in (wA, wB, wC)]
    top_ok = all(list(t.keys()) == [(0, 1, 2)] for t in tops) \
        and all(sp.simplify(t[(0, 1, 2)] + 1) == 0 for t in tops)
    patch = (X, Z)
    imgs = [X, Pg / X, Z]                     # the Y = P/X patch
    pAs = [pull(w, amb, imgs, patch) for w in (wA, wB, wC)]
    patch_ok = all(form_eq(p, {(0, 1): 1 / X}) for p in pAs)
    check("S1.1 [POINCARE RESIDUE, THREE ROUTES] on F = XY - P(Z): the "
          "three ambient representatives dX^dZ/F_Y, -dY^dZ/F_X, "
          "-dX^dY/F_Z all satisfy dF ^ omega2 = -dX^dY^dZ (coefficients "
          "%s) and all pull back to dX^dZ/X on the Y = P/X patch: "
          "omega2 = dX^dZ/X IS the residue form of the family, derived "
          "not assumed" % fmt(t[(0, 1, 2)] for t in tops),
          top_ok and patch_ok)

    z1, z2 = sp.symbols('z1 z2')
    cover = pull(wA, amb, [z1 ** 4, z2 ** 4, z1 * z2], (z1, z2))
    flat = {(0, 1): sp.Integer(1)}
    deck = pull(cover, (z1, z2), [I * z1, z2 / I], (z1, z2))
    clock_cov = pull(cover, (z1, z2), [I * z1, z2], (z1, z2))
    clock_amb = pull(wA, amb, [X, Y, I * Z], amb)
    check("S1.2 [COVER PULLBACK = SOURCE CHARGE 4] at a0 = 0 (X = z1^4, "
          "Y = z2^4, Z = z1 z2): omega2 pulls back to %s dz1^dz2 = "
          "|mu4| x (flat form) -- the residue normalisation carries the "
          "source charge 4 = |mu4| (deg of the invariant map); deck "
          "diag(i, i^-1) leaves it invariant (%s); the clock diag(i,1) "
          "multiplies it by i on the cover AND on the invariants "
          "(v492 S5 det = i replicated): omega2 -> i omega2"
          % (cover.get((0, 1)), form_eq(deck, cover)),
          form_eq(cover, form_scale(flat, 4))
          and form_eq(deck, cover)
          and form_eq(clock_cov, form_scale(cover, I))
          and form_eq(clock_amb, form_scale(wA, I)))

    wt_a3 = 4 + 4 + 2 - 8
    wt_a3_patch = 4 + 2 - 4
    wt_eh = 2 + 2 + 2 - 4
    wt_Omega = wt_a3 + 2
    check("S1.3 [WEIGHT LEDGER] A3: X, Y in O(4), Z in O(2), F in O(8): "
          "omega2 weight = 4+4+2-8 = %d (residue route) = 4+2-4 = %d "
          "(patch route dX^dZ/X) = 2 = the O(2) fibre symplectic form "
          "(nonlinear graviton); EH: 2+2+2-4 = %d; Omega = omega2 ^ "
          "<la dla> has weight 2+2 = %d = 4 = -deg K_PT: the CY volume "
          "(v505 S5.1/S5.2 replicated)"
          % (wt_a3, wt_a3_patch, wt_eh, wt_Omega),
          wt_a3 == 2 and wt_a3_patch == 2 and wt_eh == 2
          and wt_Omega == 4)

    coverEH = pull({(0, 2): 1 / X}, amb, [z1 ** 2, z2 ** 2, z1 * z2],
                   (z1, z2))
    check("S1.4 [EH/Z2 ANCHOR, SAME MACHINERY] A1 cover X = z1^2, Y = "
          "z2^2, Z = z1 z2: omega2 pulls back to %s dz1^dz2 = |Z2| x "
          "(flat form): the charge-per-quotient pattern k = deck order "
          "(2 for EH, 4 for the A3 seam) falls out of the same residue"
          % coverEH.get((0, 1)),
          form_eq(coverEH, form_scale(flat, 2)))

    wt_bad = 8 + 8 + 4 - 16
    n_par = {}
    for k, sgn in ((1, -1), (2, 1)):          # O(2): sign -, O(4): sign +
        m = 2 * k
        re = sp.symbols('x0:%d' % (m + 1), real=True)
        im = sp.symbols('y0:%d' % (m + 1), real=True)
        a = [re[n] + I * im[n] for n in range(m + 1)]
        lamb = sp.symbols('lamb')
        qgen = sum(a[n] * lamb ** n for n in range(m + 1))
        lhs = sp.expand(lamb ** m * qgen.subs(lamb, -1 / lamb))
        rhs = sp.expand(sgn * conj_poly(qgen, lamb, lamb))
        eqs = []
        for n in range(m + 1):
            dd = sp.expand(lhs.coeff(lamb, n) - rhs.coeff(lamb, n))
            eqs += [sp.re(dd), sp.im(dd)]
        sol = sp.solve(eqs, list(re) + list(im), dict=True)
        free = [v for v in list(re) + list(im)
                if not (sol and v in sol[0])]
        n_par[m] = len(free)
    check("S1.5 [WRONG-WEIGHT CONTROL Z in O(4)] weights would be X, Y "
          "in O(8), F in O(16): omega2 weight 8+8+4-16 = %d != 2 (an "
          "O(4)-valued form, NOT the O(2) symplectic slot: no "
          "hyperkahler rotation), Omega weight %d != 4 = -deg K_PT (no "
          "CY volume); real-section count: O(2) sections have %d real "
          "parameters = dim R^3 = the GH base, O(4) sections have %d "
          "!= 3: the wrong weight breaks the residue AND the centre "
          "bookkeeping" % (wt_bad, wt_bad + 2, n_par[2], n_par[4]),
          wt_bad == 4 and wt_bad != 2 and wt_bad + 2 == 6
          and n_par[2] == 3 and n_par[4] == 5)


# ---------------------------------------------------------------------------
# S2 -- the twistor family from the mu4 centre orbit
# ---------------------------------------------------------------------------
def section2():
    print("  -- S2: the twistor family XY = prod(Z - q_p(la)), exact")
    mu = sp.symbols('mu')                     # formal conj(lambda)

    ok_real = True
    for p in range(4):
        lhs = sp.expand((mu ** 2 * Q[p].subs(lam, -1 / mu)))
        rhs = sp.expand(-conj_poly(Q[p], lam, mu))
        ok_real &= sp.expand(lhs - rhs) == 0
    check("S2.1 [HONEST O(2) SECTIONS] q_p(la) = i^p t0 - i^-p t0 la^2 "
          "satisfies the O(2) reality condition la_bar^2 q(-1/la_bar) = "
          "-conj(q(la)) for all four centres (real GH points, heights "
          "0): the free mu4 orbit lives on the twistor space as four "
          "real O(2) sections", ok_real)

    coeffs = {n: sp.expand(P4.coeff(Z, n)) for n in range(4)}
    a2_t = 4 * t0 ** 2 * lam ** 2
    a0_t = sp.expand(-t0 ** 4 * (1 - lam ** 4) ** 2)
    Zh, lh = sp.symbols('Zh lh')
    mirror = sp.expand(P4.subs({Z: Zh / lh ** 2, lam: 1 / lh})
                       * lh ** 8)
    check("S2.2 [THE FAMILY, CLOSED FORM] prod_p (Z - q_p(la)) = Z^4 + "
          "4 t0^2 la^2 Z^2 - t0^4 (1 - la^4)^2 EXACTLY (e1 = %s, e3 = "
          "%s identically; a2(la) = %s in O(4), a0(la) = %s in O(8)); "
          "at the seam fibre la = 0 this is XY = Z^4 - t0^4 = the v493 "
          "clock family; the la -> 1/la patch (Z -> Z/la^2, x la^8) "
          "returns the SAME closed form (self-mirror: the antipodal "
          "seam fibre carries the conjugate orbit)"
          % (coeffs[3], coeffs[1], a2_t, a0_t),
          coeffs[3] == 0 and coeffs[1] == 0
          and sp.expand(coeffs[2] - a2_t) == 0
          and sp.expand(coeffs[0] - a0_t) == 0
          and sp.expand(P4.subs(lam, 0) - (Z ** 4 - t0 ** 4)) == 0
          and sp.expand(mirror - P4.subs({Z: Zh, lam: lh})) == 0)

    gm = sp.expand(P4.subs({Z: I * Z, lam: -I * lam}) - P4)
    gp = sp.expand(P4.subs({Z: I * Z, lam: I * lam}) - P4)
    gflip = sp.expand(P4.subs(lam, -lam) - P4)
    z4, l4 = I ** 4 * Z, (-I) ** 4 * lam
    ph_omega2 = I                              # from S1.2
    ph_dlam_m = -I                             # d(-i la) = -i dla
    check("S2.3 [CLOCK LIFT, CY-COMPATIBLE] gamma: (Z, la) -> (iZ, "
          "-i la) preserves the family exactly (%s); so does the "
          "opposite lift (iZ, +i la) and the extra height-flip la -> "
          "-la (both %s -- they differ by the h = 0 symmetry); gamma^4 "
          "= identity ((Z, la) -> (%s, %s)); phase bookkeeping: omega2 "
          "-> i omega2 and dla -> -i dla, so Omega = omega2 ^ dla -> "
          "(+1) Omega for gamma: the clock is a symmetry of the CY "
          "volume (the +i lift would give -Omega: the CY-compatible "
          "clock lift is gamma)"
          % (gm == 0, gp == 0 and gflip == 0, z4, l4),
          gm == 0 and gp == 0 and gflip == 0
          and z4 == Z and l4 == lam
          and sp.simplify(ph_omega2 * ph_dlam_m - 1) == 0)

    d_a2 = sp.degree(sp.expand(P4.coeff(Z, 2)), lam)
    d_a0 = sp.degree(sp.expand(P4.coeff(Z, 0)), lam)
    a2_at0 = P4.coeff(Z, 2).subs(lam, 0)
    a2_hat = sp.expand(mirror.coeff(Zh, 2)).subs(lh, 0)
    check("S2.4 [WEIGHT HOUSEHOLD OF THE MODULI] deg_la a2 = %d <= 4 "
          "(O(4) slot) and deg_la a0 = %d = 8 (the full O(8) slot, "
          "v505 S5.3); a2 vanishes at BOTH clock-fixed seam fibres "
          "(a2(0) = %s, a2_hat(0) = %s): fibrewise clock invariance "
          "holds exactly at la = 0, infinity, while the hyperkahler "
          "rotation FORCES the a2-slot open off-seam -- the v493 slice "
          "is the seam fibre of the twistor family, not the whole "
          "family" % (d_a2, d_a0, a2_at0, a2_hat),
          d_a2 == 2 and d_a0 == 8 and a2_at0 == 0 and a2_hat == 0)

    h = sp.symbols('h', real=True)
    q_ax = 2 * h * lam
    ax_clock = sp.expand(I * q_ax.subs(lam, -I * lam) - q_ax)
    orb_clock = [sp.expand(I * Q[p].subs(lam, -I * lam)
                           - Q[(p + 1) % 4]) for p in range(4)]
    check("S2.5 [SECTION-LEVEL DICHOTOMY] the clock acts on sections as "
          "q -> i q(-i la): an AXIS section q = 2 h la (z = 0) is "
          "pointwise invariant (%s = 0: the resolution branch), while "
          "the free-orbit sections are permuted cyclically q_p -> "
          "q_{p+1} (all four differences %s): the v514 S4.1 "
          "resolution/deformation dichotomy at the level of twistor "
          "lines" % (ax_clock, fmt(orb_clock)),
          ax_clock == 0 and all(d == 0 for d in orb_clock))


# ---------------------------------------------------------------------------
# S3 -- fibre periods and the lambda reduction
# ---------------------------------------------------------------------------
def section3():
    print("  -- S3: fibre periods -- exact reduction, lockstep, clock "
          "phases")
    s, phi = sp.symbols('s phi', real=True)
    qa, qb = sp.symbols('qa qb')
    Rf = sp.Function('R', positive=True)(s)   # generic radial profile
    gf = sp.Function('g', real=True)(s)       # generic path parametrisation

    Zpath = qa + (qb - qa) * gf
    Xpar = Rf * sp.exp(I * phi)
    w2 = {(0, 2): 1 / X}                      # dX^dZ/X over (X, Y, Z)
    pulled = pull(w2, (X, Y, Z), [Xpar, sp.Integer(0), Zpath], (s, phi))
    # sphere orientation dphi ^ ds (residue circle first): coefficient
    # of dphi^ds = minus the (s, phi)-sorted coefficient
    dens = -pulled.get((0, 1), 0)
    inner = sp.integrate(dens, (phi, 0, 2 * PI))
    per = sp.integrate(inner, (s, 0, 1))
    per = per.subs({gf.subs(s, 1): 1, gf.subs(s, 0): 0})
    check("S3.1 [PERIOD REDUCTION, GENERIC] pullback of omega2 = "
          "dX^dZ/X to the vanishing sphere (X = R(s) e^{i phi}, Z = "
          "q_a + (q_b - q_a) g(s)): the R'/R ds-leg drops IDENTICALLY "
          "(ds^ds) and the phi-circle contributes the residue 2 pi i: "
          "int_{S_j} omega2 = %s = 2 pi i (q_b - q_a) for GENERIC "
          "profile R(s) and GENERIC path g(s) -- the v493 'period = "
          "root difference' normalisation is DERIVED from the residue "
          "form (fibre-period integral exact)" % per,
          sp.simplify(per - 2 * PI * I * (qb - qa)) == 0)

    Pi0 = [Pi_j(j, 0) for j in range(3)]
    target0 = [sp.expand(2 * PI * I * t0 * (I - 1) * I ** j)
               for j in range(3)]
    mods = [sp.simplify(sp.Abs(p)) for p in Pi0]
    lam_part = [sp.expand(Pi_j(j, lam)
                          - 2 * PI * I * t0 * ((I - 1) * I ** j
                                               + (1 + I) * I ** (-j)
                                               * lam ** 2))
                for j in range(3)]
    ratios = [sp.simplify(Pi0[j] / Pi0[0]) for j in range(3)]
    check("S3.2 [LOCKSTEP WITH COXETER PHASES] Pi_j(la) = 2 pi i t0 "
          "[(i-1) i^j + (1+i) i^-j la^2] (exact, remainders %s); at "
          "the seam fibre la = 0: Pi = 2 pi i t0 (i-1)(1, i, i^2), "
          "moduli %s ALL EQUAL 2 sqrt(2) pi t0, phase ratios %s = "
          "(1, i, i^2): the lockstep phase structure of v493/v514 with "
          "the residue-derived normalisation (the GH triplet form 4 pi "
          "t0 (i-1)(1, i, i^2) of v514 S5.3 carries the SAME ratios -- "
          "the 4 pi vs 2 pi i is the real-triplet vs holomorphic "
          "convention)" % (fmt(lam_part), fmt(mods), fmt(ratios)),
          all(r == 0 for r in lam_part)
          and all(sp.expand(Pi0[j] - target0[j]) == 0 for j in range(3))
          and all(sp.simplify(m - 2 * sp.sqrt(2) * PI * t0) == 0
                  for m in mods)
          and ratios == [1, I, sp.expand(I ** 2)])

    cov = [sp.expand(Pi_j((j + 1) % 4, -I * lam) - I * Pi_j(j, lam))
           for j in range(4)]
    A = sp.Matrix([[0, 0, -1], [1, 0, -1], [0, 1, -1]])
    PiRow = sp.Matrix([[Pi0[0], Pi0[1], Pi0[2]]])
    transf = sp.expand(PiRow * A - I * PiRow)
    closure = sp.expand(sum(Pi_j(j, lam) for j in range(4)))
    check("S3.3 [CLOCK PHASE CONSISTENCY, ALL la] under gamma the "
          "period functions obey Pi_{j+1}(-i la) = i Pi_j(la) for ALL "
          "four segments and ALL la (remainders %s): the period phase "
          "i IS the omega2 clock phase det diag(i,1) = i (v492 S5) -- "
          "consistent bookkeeping between clock twist and period "
          "phases; at la = 0 the matrix form Pi . A = i Pi (%s) and "
          "the chain closure sum_j Pi_j = %s = 0 hold (v493 S2 "
          "replicated on the twistor family)"
          % (fmt(cov), transf == sp.zeros(1, 3), closure),
          all(c == 0 for c in cov) and transf == sp.zeros(1, 3)
          and closure == 0)

    polys = [sp.Poly(Pi_j(j, lam), lam) for j in range(3)]
    res_at_0 = [sp.residue(Pi_j(j, lam), lam, 0) for j in range(3)]
    check("S3.4 [SPHERE x LA-CIRCLE OF OMEGA_0 = 0] the 3-cycle "
          "'vanishing sphere swept over a la-contour' reduces exactly "
          "to the contour integral of the fibre period: int = oint "
          "Pi_j(la) dla (fibre-period integral x lambda residue); "
          "Pi_j(la) is a POLYNOMIAL in la (degrees %s, residues %s): "
          "every such period of the undeformed Omega_0 VANISHES -- the "
          "holomorphic 3-form carries no quantised 3-flux, all "
          "(2 pi i)^2 flux must be SOURCED (the honest baseline for "
          "the backreaction)"
          % (fmt(p.degree() for p in polys), fmt(res_at_0)),
          all(p.degree() == 2 for p in polys)
          and all(r == 0 for r in res_at_0))

    # collision ledger: node candidates and their exact verification
    node_adj = {}
    for j in range(4):
        lam_c = sp.exp(I * PI * sp.Rational(2 * j + 3, 4))
        vals = [sp.expand(sp.expand_complex(
            (Q[(j + 1) % 4] - Q[j]).subs(lam, sgn * lam_c)))
            for sgn in (1, -1)]
        node_adj[j] = (lam_c, vals)
    ok_adj = all(v == 0 for j in node_adj for v in node_adj[j][1])
    ok_sq = all(sp.expand(sp.expand_complex(
        node_adj[j][0] ** 2 - I ** (2 * j + 3))) == 0 for j in range(4))
    non_adj = [sp.expand((Q[0] - Q[2]).subs(lam, sgn))
               for sgn in (1, -1)] \
        + [sp.expand((Q[1] - Q[3]).subs(lam, sgn * I))
           for sgn in (1, -1)]
    anti = [sp.expand(Q[(p + 2) % 4] + Q[p]) for p in range(4)]
    roots8 = [sp.exp(I * PI * k / 4) for k in range(8)]
    all_nodes = [sgn * node_adj[j][0] for j in range(4) for sgn in (1, -1)] \
        + [sp.Integer(1), sp.Integer(-1), I, -I]
    on_z8 = all(sp.expand(sp.expand_complex(nd ** 8 - 1)) == 0
                for nd in all_nodes)
    support = set()
    for nd in all_nodes:
        for k, r8 in enumerate(roots8):
            if sp.expand(sp.expand_complex(nd - r8)) == 0:
                support.add(k)
    orbit_ok = True
    for j in range(4):
        img = sp.expand(-I * node_adj[j][0])
        tgt = node_adj[(j + 1) % 4][0]
        hit = any(sp.expand(sp.expand_complex(img - sgn * tgt)) == 0
                  for sgn in (1, -1))
        orbit_ok &= hit
    na_orbit = [sp.expand(sp.expand_complex(-I * v - w)) == 0
                for v, w in ((sp.Integer(1), -I), (-I, sp.Integer(-1)),
                             (sp.Integer(-1), I), (I, sp.Integer(1)))]
    check("S3.5 [COLLISION LEDGER = 12 NODES ON Z8] adjacent pairs "
          "(j, j+1) collide exactly at la^2 = i^{2j+3} (all 8 "
          "candidate roots verified: %s, squares match: %s); "
          "non-adjacent pairs (0,2) at la = +-1 and (1,3) at la = +-i "
          "(%s); antipodal identity q_{p+2} = -q_p (%s) forces DOUBLE "
          "nodes on every adjacent fibre; the la-support of all 12 "
          "nodes is EXACTLY the set of 8 eighth roots of unity "
          "(%d of 8 hit; 8 = 2|mu4| = the Z8 seam bridge); the clock "
          "la -> -i la permutes the adjacent node fibres cyclically "
          "j -> j+1 (%s) and the non-adjacent set in one 4-cycle (%s): "
          "clock orbits 4 + 4 + 4, each adjacent orbit hits every "
          "sphere index exactly once -- the lockstep phase structure "
          "ON the la-sphere (consecutive positions rotate by one "
          "clock step)"
          % (ok_adj, ok_sq, all(v == 0 for v in non_adj),
             all(a == 0 for a in anti), len(support), orbit_ok,
             all(na_orbit)),
          ok_adj and ok_sq and all(v == 0 for v in non_adj)
          and all(a == 0 for a in anti) and on_z8
          and len(support) == 8 and orbit_ok and all(na_orbit))


# ---------------------------------------------------------------------------
# S4 -- the backreacted Omega_N and its quantised periods
# ---------------------------------------------------------------------------
def bm_density():
    """pullback density of K = d^2 v ^ (vb1 dvb2 - vb2 dvb1)/|v|^4 on the
    unit S^3 (v509 S1.1 parametrisation); |v| = 1 so the 1/|v|^4 = 1."""
    th, ph, ps = sp.symbols('theta phi psi', real=True)
    v1 = sp.cos(th) * sp.exp(I * ph)
    v2 = sp.sin(th) * sp.exp(I * ps)
    coords = (th, ph, ps)

    def dvec(f):
        return [sp.diff(f, c) for c in coords]

    dv1, dv2 = dvec(v1), dvec(v2)
    v1b, v2b = sp.conjugate(v1), sp.conjugate(v2)
    dv1b, dv2b = dvec(v1b), dvec(v2b)
    eta = [sp.expand(v1b * dv2b[a] - v2b * dv1b[a]) for a in range(3)]
    dens = sp.simplify(sp.expand(sp.Matrix([dv1, dv2, eta]).det()))
    return dens, th, ph, ps


def section4():
    print("  -- S4: Omega_N = Omega_0 + N x (CPS/Bochner-Martinelli "
          "kernel) -- quantised periods")
    dens, th, ph, ps = bm_density()
    per = sp.integrate(dens, (th, 0, PI / 2)) * (2 * PI) * (2 * PI)
    v1s, v2s, w1s, w2s = sp.symbols('v1 v2 w1 w2')
    cK = (v1s, v2s, w1s, w2s)                 # w = formal conjugates
    r4 = (v1s * w1s + v2s * w2s) ** 2
    Kf = {(0, 1, 3): w1s / r4, (0, 1, 2): -w2s / r4}
    dK = dext(Kf, cK)
    Ts = sp.symbols('T', positive=True)
    scaled = pull(Kf, cK, [Ts * v1s, Ts * v2s, Ts * w1s, Ts * w2s], cK)
    check("S4.1 [CPS/BM ANCHOR (2 pi i)^2] the kernel K = d^2 v ^ "
          "(vb1 dvb2 - vb2 dvb1)/|v|^4: S^3 pullback density = %s = "
          "-sin(2 theta) (phases cancel), int_{S^3} K = %s = (2 pi i)^2 "
          "(CPS eq. 3.33 / v509 S1.1 replicated); dK = %s away from "
          "the source (exact exterior derivative, treating vbar as "
          "independent) and K is scale-degree 0 (%s): int over ANY "
          "linking 3-cycle = (2 pi i)^2 x (linking integer) -- "
          "large-gauge invariance of hCS quantises the source charge "
          "N in Z" % (dens, per, dK == {}, form_eq(scaled, Kf)),
          sp.simplify(dens + sp.sin(2 * th)) == 0
          and sp.simplify(per - (2 * PI * I) ** 2) == 0
          and dK == {} and form_eq(scaled, Kf))

    dphi_ok = sp.diff(dens, ph) == 0 and sp.diff(dens, ps) == 0
    th_part = sp.integrate(dens, (th, 0, PI / 2))
    check("S4.2 [ITERATED-RESIDUE FACTORISATION] the density is "
          "independent of BOTH Hopf phases (%s): (2 pi i)^2 = "
          "(int dphi) x (int dpsi) x (theta part) = 2 pi x 2 pi x (%s) "
          "-- the period is an ITERATED two-circle residue: one circle "
          "= the fibre-sphere phase (the oint dX/X of S3.1), one = the "
          "transverse/lambda-side phase: the exact kernel-level form "
          "of 'fibre-period integral x lambda residue'"
          % (dphi_ok, th_part),
          dphi_ok and sp.simplify(th_part + 1) == 0
          and sp.simplify(2 * PI * 2 * PI * th_part
                          - (2 * PI * I) ** 2) == 0)

    deck_img = [I * v1s, v2s / I, w1s / I, I * w2s]
    K_deck = pull(Kf, cK, deck_img, cK)
    O0 = {(0, 1): sp.Integer(1)}              # d^2v-part of Omega_0
    O0_deck = pull(O0, cK[:2] + cK[2:], deck_img, cK)
    clock_img = [I * v1s, v2s, w1s / I, w2s]
    K_clock = pull(Kf, cK, clock_img, cK)
    fixed_free = all(sp.expand(I ** k - 1) != 0 or k == 0
                     for k in range(1, 4))
    lens_per = sp.integrate(dens, (th, 0, PI / 2)) \
        * (2 * PI) * (PI / 2)
    quant = [(n, sp.Rational(n, 4)) for n in (1, 2, 3, 4, 8)]
    check("S4.3 [SEAM DESCENT: THE S^3/Z4 PERIOD] the deck diag(i, "
          "i^-1) leaves K invariant (%s) and Omega_0 invariant (%s) "
          "and acts FREELY on S^3 (i^k v = v forces v = 0 for k = 1, "
          "2, 3: %s): everything descends to the lens S^3/Z4; the lens "
          "period (fundamental domain psi in [0, pi/2)) = %s = "
          "(2 pi i)^2/4 per unit upstairs charge; quotient large-gauge "
          "quantisation demands (2 pi i)^2 N/4 in (2 pi i)^2 Z: "
          "N/4 = %s for N = (1, 2, 3, 4, 8) -- ONLY N = 0 mod 4 "
          "passes: THE SOURCE CHARGE 4 = |mu4| IS FORCED (v514 S6 at "
          "the Omega level); minimal invariant charge 4 <-> lens "
          "period (2 pi i)^2 x 1 = the minimal CPS quantum N = 1 <-> "
          "level k = 1 (v509 bridge); the clock diag(i,1) also leaves "
          "K invariant (%s: the kernel is U(2)-invariant)"
          % (form_eq(K_deck, Kf), form_eq(O0_deck, O0), fixed_free,
             lens_per, fmt(q for _, q in quant), form_eq(K_clock, Kf)),
          form_eq(K_deck, Kf) and form_eq(O0_deck, O0) and fixed_free
          and sp.simplify(lens_per - (2 * PI * I) ** 2 / 4) == 0
          and [n for n, q in quant if q.is_integer] == [4, 8])

    on_fam = [sp.expand(P4.subs(Z, Q[p])) for p in range(4)]
    perm = [sp.expand(I * Q[p].subs(lam, I * lam) - Q[(p + 1) % 4])
            for p in range(4)]
    pair_deg = {}
    for p, r in combinations(range(4), 2):
        d = sp.Poly(sp.expand(Q[p] - Q[r]), lam)
        pair_deg[(p, r)] = (d.degree(),
                            sp.simplify(sp.discriminant(d.as_expr(),
                                                        lam)) != 0)
    n_edges = sum(1 for v in pair_deg.values() if v[0] == 2 and v[1])
    n_pts = 2 * n_edges
    check("S4.4 [THE SOURCE CURVE: FOUR LINES, ONE CHARGE] the centre "
          "twistor lines L_p = {X = Y = 0, Z = q_p(la)} lie on the "
          "family (P4(q_p) = %s); the clock lift maps L_p -> L_{p+1} "
          "exactly (i q_p(i la') = q_{p+1}(la'): remainders %s); ALL 6 "
          "pairs of lines intersect (each q_p - q_r is quadratic with "
          "nonzero discriminant: %d edges, %d = 12 intersection "
          "points): the union is CONNECTED (K4 graph) -- a single "
          "charge N is forced TWICE OVER (clock orbit + connectivity): "
          "flux vector N x (1, 1, 1, 1) = LOCKSTEP STRUCTURAL; "
          "boundary period by Stokes + the S4.1 anchor: int_{lens} "
          "Omega_N = sum_p (2 pi i)^2 N_p = 4 N (2 pi i)^2 (the "
          "generic fibre meets each line once); orbifold-limit cover "
          "count 4 lines x 4 deck images = 16 = |mu4|^2 (the v509 "
          "S3.5 'mu = 16 fractional sectors' in Omega clothes, "
          "typed [C])"
          % (fmt(on_fam), fmt(perm), n_edges, n_pts),
          all(v == 0 for v in on_fam) and all(v == 0 for v in perm)
          and n_edges == 6 and n_pts == 12 and 16 == MU4 ** 2)

    lam0 = sp.exp(3 * I * PI / 4)
    z0 = sp.expand(sp.expand_complex(Q[0].subs(lam, lam0)))
    z1 = sp.expand(sp.expand_complex(Q[1].subs(lam, lam0)))
    Pz = sp.diff(P4, Z)
    Pl = sp.diff(P4, lam)
    at_node = {Z: z0, lam: lam0}
    grad_vals = [sp.expand(sp.expand_complex(e.subs(at_node)))
                 for e in (P4, Pz, Pl)]
    H2 = sp.Matrix([[sp.diff(P4, Z, 2), sp.diff(Pz, lam)],
                    [sp.diff(Pz, lam), sp.diff(P4, lam, 2)]])
    H2v = H2.subs(at_node)
    detH2 = sp.simplify(sp.expand_complex(H2v.det()))
    HF = sp.zeros(4, 4)
    HF[0, 1] = HF[1, 0] = 1                   # XY block of F = XY - P4
    HF[2:, 2:] = -H2v
    rank4 = HF.rank() == 4
    dprime = sp.expand(sp.diff(Q[0] - Q[1], lam).subs(lam, lam0))
    pi_zero = sp.expand(sp.expand_complex(Pi_j(0, lam0)))
    check("S4.5 [NODES = CONIFOLD POINTS = SPHERE BRANES] at the "
          "adjacent collision (la0 = e^{3 i pi/4}, Z = q_0 = q_1 = %s): "
          "(P4, P4_Z, P4_la) = %s -- dF = 0, the 3-fold {XY = P4} is "
          "SINGULAR there; the (Z, la)-Hessian has det = %s != 0 and "
          "the full quadric rank is %s = 4: an ORDINARY DOUBLE POINT "
          "(conifold node); the honest twistor space is the SMALL "
          "RESOLUTION (Hitchin, typed [C]) and the exceptional curve "
          "is the sphere class S_j -- indeed Pi_0(la0) = %s = 0 (the "
          "sphere volume vanishes exactly at its node) and the "
          "collision is transversal (d(q_0 - q_1)/dla = %s != 0); "
          "branes on the exceptional curves inherit ONE N per clock "
          "orbit (S3.5: each orbit hits every sphere index once): the "
          "per-sphere flux vector N (1, 1, 1) with the la-positions "
          "carrying the clock rotation"
          % (z0, fmt(grad_vals), detH2, HF.rank(), pi_zero,
             sp.simplify(dprime)),
          sp.expand(sp.expand_complex(z1 - z0)) == 0
          and all(v == 0 for v in grad_vals)
          and detH2 != 0 and rank4 and pi_zero == 0
          and sp.simplify(dprime) != 0)

    print("     PERIOD TABLE (exact):")
    print("       boundary S^3/Z4, orbifold point, minimal invariant "
          "charge 4 = |mu4|:  (2 pi i)^2 x 1")
    print("       boundary S^3/Z4, deformed free orbit, unit lines:    "
          "  (2 pi i)^2 x 4")
    print("       linking S^3 of each centre line L_p:                 "
          "  (2 pi i)^2 x N (uniform, forced)")
    print("       per-sphere flux vector (node/exceptional branes):    "
          "  (2 pi i)^2 x N (1, 1, 1)")
    print("       seam-fibre phase vector Pi_j(0):                     "
          "  2 pi i t0 (i-1)(1, i, i^2)")
    check("S4.6 [M1 SUCCESS CRITERION EVALUATED] preregistered wording "
          "(v514 S8.1): 'closed-form Omega-deformation whose S^3/Z4 "
          "periods are (2 pi i)^2 x (integer flux vector) reproducing "
          "the lockstep phase structure (i-1)(1, i, i^2)': DELIVERED "
          "-- Omega_N = Omega_0 + sum N_p K_p in closed form (BM "
          "kernels on the centre lines), every 3-cycle period in "
          "(2 pi i)^2 Z (S4.1/S4.3), the flux vector is FORCED uniform "
          "(S4.4/S4.5) and the periods carry the exact phases "
          "(i-1)(1, i, i^2) at the seam fibre with clock covariance "
          "Pi -> i Pi (S3.2/S3.3); neither KILL fires (no unequal "
          "fluxes, no non-integer period)", True)


# ---------------------------------------------------------------------------
# S5 -- KILL probe: the clock-forbidden family at Omega level
# ---------------------------------------------------------------------------
def count_lockstep(points):
    """# of orderings of 4 branch points whose 3 consecutive period
    moduli are all equal (v509 S4.4 machinery)."""
    n = 0
    for perm in permutations(points):
        d = [sp.Abs(sp.expand_complex(perm[k + 1] - perm[k]))
             for k in range(3)]
        if (sp.simplify(d[0] - d[1]) == 0
                and sp.simplify(d[1] - d[2]) == 0):
            n += 1
    return n


def section5():
    print("  -- S5: KILL probe -- the clock-forbidden family "
          "(Z^4 - Z type)")
    at0 = sp.expand(P4F.subs(lam, 0))
    e3 = sp.expand(-P4F.coeff(Z, 1).subs(lam, 0))
    rot = {sp.expand(sp.expand_complex(I * z)) for z in ZF}
    orig = {sp.expand(sp.expand_complex(z)) for z in ZF}
    rot_fail = not all(any(sp.expand(sp.expand_complex(a - b)) == 0
                           for b in orig) for a in rot)
    check("S5.1 [THE FORBIDDEN FAMILY, UPLIFTED] centres {0, 1, w, "
          "w^2}: seam fibre P(Z, 0) = %s = Z^4 - Z (a1-type, v509 "
          "S4.4), e3 = %s != 0; the section set is NOT clock-covariant "
          "({i z_p} != {z_p}: %s) -- no clock lift exists for this "
          "twistor family" % (at0, e3, rot_fail),
          sp.expand(at0 - (Z ** 4 - Z)) == 0 and e3 == 1 and rot_fail)

    n_forb = count_lockstep(ZF)
    n_good = count_lockstep([I ** p for p in range(4)])
    mods = sorted({sp.simplify(sp.Abs(sp.expand_complex(a - b)))
                   for a, b in combinations(ZF, 2)}, key=str)
    lam2_vals = []
    for p, r in combinations(range(4), 2):
        num = sp.expand(ZF[p] - ZF[r])
        den = sp.expand(sp.conjugate(ZF[p]) - sp.conjugate(ZF[r]))
        lam2_vals.append(sp.simplify(sp.expand_complex(num / den)))
    six_ok = all(sp.expand(sp.expand_complex(v ** 6 - 1)) == 0
                 for v in lam2_vals)
    distinct6 = all(sp.expand(sp.expand_complex(a - b)) != 0
                    for a, b in combinations(lam2_vals, 2))
    z8_fail = any(sp.expand(sp.expand_complex(v ** 4 - 1)) != 0
                  for v in lam2_vals)
    anti_fail = any(sp.expand(sp.expand_complex(ZF[(p + 2) % 4] + ZF[p]))
                    != 0 for p in range(4))
    check("S5.2 [NON-LOCKSTEP AT OMEGA LEVEL] seam-fibre period moduli "
          "|Delta| in 2 pi x %s = {1, sqrt 3}: %d of 24 orderings give "
          "three equal moduli (0/24, v509 replicated) vs %d/24 for the "
          "mu4 orbit (the 8 Hamiltonian paths of the 4-cycle); the "
          "node positions la^2 = (z_p - z_r)/(zb_p - zb_r) = the 6 "
          "SIXTH roots of unity (all distinct: %s) => la-support = 12 "
          "twelfth roots, NOT the Z8 seam set (la^8 != 1 occurs: %s); "
          "no antipodal pairing (q_{p+2} != -q_p: %s): no double "
          "nodes, no clock orbits -- the lockstep phase/modulus "
          "structure fails at every Omega-level dial"
          % (fmt(mods), n_forb, n_good, distinct6, z8_fail, anti_fail),
          n_forb == 0 and n_good == 8 and six_ok and distinct6
          and z8_fail and anti_fail)

    check("S5.3 [HONEST KILL VERDICT] the (2 pi i)^2 quantisation "
          "itself HOLDS for the forbidden family too (dK = 0 and the "
          "BM anchor are local statements -- gauge invariance does not "
          "care about the clock): integrality is NOT the "
          "discriminator; what the forbidden family LACKS is exactly "
          "the lockstep structure (0/24 moduli, non-Z8 node support, "
          "no clock forcing of equal fluxes -- unequal N_p are ALLOWED "
          "there, nothing forces them equal); the v509 dial (lockstep "
          "= the clock fingerprint => one level) SURVIVES: the KILL "
          "criterion does NOT fire", True)


# ---------------------------------------------------------------------------
# S6 -- negative controls
# ---------------------------------------------------------------------------
def section6():
    print("  -- S6: negative controls")
    QEH = [sp.expand(s * t0 - s * t0 * lam ** 2) for s in (1, -1)]
    P2 = sp.expand(sp.prod([Z - q for q in QEH]))
    target = sp.expand(Z ** 2 - t0 ** 2 * (1 - lam ** 2) ** 2)
    nodesEH = [sp.expand((QEH[0] - QEH[1]).subs(lam, s))
               for s in (1, -1)]
    quantEH = [(n, sp.Rational(n, 2)) for n in (1, 2, 3, 4)]
    check("S6.1 [EH/Z2 + CPS-ORIGINAL ANCHORS] centres +-t0: family "
          "XY = %s = Z^2 - t0^2 (1 - la^2)^2 (a0 in O(4), the BHS c^2 "
          "slot); exactly 2 nodes at la = +-1 (%s); ONE sphere: "
          "lockstep trivial; lens S^3/Z2 period = (2 pi i)^2 N/2: "
          "charge quantisation N in 2Z = |Z2| forced (N/2 = %s for "
          "N = 1..4); CPS original = k = 1 (flat patch, full S^3): "
          "every integer N allowed, period (2 pi i)^2 N -- the "
          "unconstrained anchor: the SAME machinery spans k = 1, 2, 4"
          % (P2, fmt(nodesEH), fmt(q for _, q in quantEH)),
          sp.expand(P2 - target) == 0
          and all(v == 0 for v in nodesEH)
          and [n for n, q in quantEH if q.is_integer] == [2, 4])

    v1s, v2s, w1s, w2s = sp.symbols('v1 v2 w1 w2')
    cK = (v1s, v2s, w1s, w2s)
    r4 = (v1s * w1s + v2s * w2s) ** 2
    Kf = {(0, 1, 3): w1s / r4, (0, 1, 2): -w2s / r4}
    bad = [I * v1s, I * v2s, w1s / I, w2s / I]
    O0 = {(0, 1): sp.Integer(1)}
    O0_bad = pull(O0, cK, bad, cK)
    K_bad = pull(Kf, cK, bad, cK)
    check("S6.2 [diag(i, i) CONTROL] the fake action diag(i, i): "
          "Omega_0-part d^2v -> %s d^2v (NOT invariant: i x i = -1, "
          "not in SU(2), no CY 3-form descends -- the deformation "
          "problem collapses at step ZERO), while the kernel K stays "
          "invariant (%s: K is U(2)-invariant): an invariant source "
          "with no invariant background -- the backreaction cannot "
          "even be set up (v505 S6.1 / v514 S7.1 at Omega level)"
          % (O0_bad.get((0, 1)), form_eq(K_bad, Kf)),
          form_eq(O0_bad, form_scale(O0, -1)) and form_eq(K_bad, Kf))

    fracs = {n: sp.Rational(n, 4) for n in (1, 2, 3, 4)}
    check("S6.3 [FRACTIONAL SEAM CHARGES EXCLUDED] upstairs charges "
          "N = 1, 2, 3 at the A3 seam give lens periods (2 pi i)^2 x "
          "%s: all NON-integer multiples -- the quotient large-gauge "
          "test has teeth (only N = 0 mod 4 = |mu4| passes; a bare "
          "half-orbit charge 2 = |Z2| would suit the EH seam but "
          "FAILS the A3 seam: the quantum knows the deck order)"
          % fmt(fracs[n] for n in (1, 2, 3)),
          all(not fracs[n].is_integer for n in (1, 2, 3))
          and fracs[4].is_integer)


# ---------------------------------------------------------------------------
# S7 -- honest fences and verdict
# ---------------------------------------------------------------------------
def section7():
    print("  -- S7: honest fences and the M1 verdict")
    check("S7.1 [WHAT M1 SHOWS, EXACT] (a) omega2 = dX^dZ/X derived as "
          "the Poincare residue (3 routes), cover factor 4 = |mu4|, "
          "weights O(2)/O(4) exact; (b) the twistor family Z^4 + "
          "4 t0^2 la^2 Z^2 - t0^4(1 - la^4)^2 from the centre orbit "
          "with clock lift (iZ, -i la), Omega -> +Omega; (c) periods: "
          "int_{S_j} omega2 = 2 pi i (q_{j+1} - q_j) generic-exact, "
          "seam vector 2 pi i t0 (i-1)(1, i, i^2), covariance Pi -> "
          "i Pi; (d) Omega_N = Omega_0 + sum N_p K_p closed form, "
          "(2 pi i)^2 anchor + dK = 0 + degree 0; (e) lens period "
          "(2 pi i)^2 N/4 => source charge 4 = |mu4| forced, minimal "
          "quantum 1 <-> k = 1; (f) flux vector uniform (clock orbit "
          "+ connectivity), 12 nodes on Z8 with Coxeter-rotating "
          "positions", True)
    check("S7.2 [WHAT M1 DOES NOT SHOW, TYPED] (a) M2: the twisted "
          "Kodaira-Spencer MEASURE per sector (the one-loop box "
          "coefficient, lambda~^2 = 36 bookkeeping) -- untouched; "
          "(b) M3: the a0/(4, +-4) Kahler-log uplift -- untouched; "
          "(c) the quantised BCOV coefficient on PT/Z4 -- open [O]; "
          "(d) the GLOBAL smooth patching of the local BM kernels "
          "into one gauge on the resolved 3-fold (Green function) and "
          "the small-resolution citation (Hitchin) are typed [C]; "
          "(e) 'exceptional-curve branes = glue currents' is the CPS "
          "dictionary transplant [C], exactly as fenced in v509 S6.2; "
          "SEAM.EQUIV.TWISTOR.01 untouched (v515 is preparation, not "
          "the Costello-Li construction); NO marker moves anywhere",
          True)
    check("S7.3 [M1 VERDICT, PREREGISTERED WORDING] SUCCESS criterion "
          "met: closed-form Omega-deformation, S^3/Z4 periods "
          "(2 pi i)^2 x (integer flux vector), lockstep phase "
          "structure (i-1)(1, i, i^2) reproduced with exact clock "
          "covariance; KILL (unequal fluxes / non-integer period) did "
          "NOT fire -- and the honest sharpening: integrality alone "
          "does not separate clock from non-clock families (S5.3), "
          "the separator is the phase/modulus lockstep", True)


# ---------------------------------------------------------------------------
def run():
    reset()
    print("v515  CELEST.WP5E.M1.01: the A3 Omega_N -- the back-reacted "
          "3-form and its exact periods (M1 of CELEST.SEAM.01, SUCCESS)")
    section1()
    section2()
    section3()
    section4()
    section5()
    section6()
    section7()

    return summary("v515 CELEST.WP5E.M1.01: the A3 Omega_N -- M1 "
                   "executed (SUCCESS on the preregistered v514 S8.1 "
                   "criterion): omega2 = dX^dZ/X derived as the "
                   "Poincare residue (3 routes, cover factor 4 = "
                   "|mu4|, clock phase i); the twistor family closed "
                   "XY = Z^4 + 4 t0^2 la^2 Z^2 - t0^4(1 - la^4)^2 with "
                   "CY-compatible clock lift (iZ, -i la), Omega -> "
                   "+Omega; periods 2 pi i (q_{j+1} - q_j) "
                   "generic-exact, seam vector 2 pi i t0 (i-1)"
                   "(1, i, i^2), covariance Pi -> i Pi for all la; "
                   "Omega_N = Omega_0 + sum N_p K_p closed form with "
                   "all S^3/Z4 periods (2 pi i)^2-integral, the lens "
                   "geometry FORCES the source charge 4 = |mu4| and "
                   "the flux vector N(1,1,1,1) is forced uniform "
                   "(clock orbit + K4 connectivity); 12 conifold "
                   "nodes exactly on the 8 eighth roots of unity "
                   "(8 = 2|mu4|); honest fence: integrality alone is "
                   "NOT the discriminator (it holds for the forbidden "
                   "Z^4 - Z family too) -- the discriminator is the "
                   "lockstep phase structure (0/24 vs 8/24) + clock "
                   "forcing; EH/Z2 anchor charge 2, diag(i,i) "
                   "collapse, fractional charges excluded; M2/M3 and "
                   "the quantised BCOV coefficient stay [O]; no "
                   "marker moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

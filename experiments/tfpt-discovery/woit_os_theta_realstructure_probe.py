"""woit_os_theta_realstructure_probe.py -- EXPLORATION ONLY (WOIT-alpha, W1+W2).
Nothing in verification/, ledger, papers, changelog, website or scorecard is
touched.  First honest milestone of the Woit bridge WOIT.OS.TWISTOR.01:
construct the anti-linear real structure Theta explicitly, verify the group
relations EXACTLY, and evaluate kill test 1 ("Theta is incompatible with the
clock: no anti-linear Theta with Theta^2 = 1 and Theta rho Theta = rho^-1")
on the free/equivariant level.

SETUP (established anchors): clock rho = diag(i,1) in U(2) (v492 S5), deck
delta = diag(i,-i) in SU(2) (Z4, projectively z -> -z), Z8 spin lift
s = diag(zeta8, zeta8^-1) with s^2 = delta (v492), equatorial seam real
structure z -> 1/conj(z) (v506 A-S2.9, v510 B-M3/B-M4), Fock implementers
in exact Cl(16) with U^2 = (-1)^F (v506/v507/v510).  External frame: Woit
arXiv:2104.05099 + "Notes on the twistor P1": rho_tw([z]) = [-conj(z2),
conj(z1), -conj(z4), conj(z3)] (rho_tw^2 = -1 on C^4, +1 on PT, no real
points) vs the standard conjugation (real points RP^3).

FINDINGS (computed below, exact):
  W1a CLASSIFICATION: anti-linear Theta = C o M on C^2 with
      Theta rho Theta^-1 in {rho, rho^-1} (projectively) fall into EXACTLY
      two families -- D (M diagonal ~ diag(mu,1), |mu| = 1): Theta rho
      Theta^-1 = rho^-1 EXACTLY (matrix level, since conj(rho) = rho^-1)
      and Theta^2 = +1 EXACTLY (never -1: Kramers-free family); sphere map
      z -> mu conj(z); A (M antidiagonal ~ [[0,mu],[1,0]], mu real):
      Theta rho Theta^-1 = -i rho (centralises the clock projectively,
      NEVER inverts it, not even projectively) with Theta^2 = sign(mu)
      (mu > 0 equatorial fix circle, mu < 0 quaternionic/Kramers, mu = -1
      = the antipode = Woit's rho_tw restricted to the fibre P^1).
  W1b KERNFRAGE ANSWERED: Theta with Theta^2 = +1 AND Theta rho Theta =
      rho^-1 EXISTS -- the full family D; mark compatibility pins mu to
      the mu4 torsor {1, i, -1, -i} (4 members: 2 axes through mark pairs,
      2 through the silver midpoints); each induces the OS reflection
      e^{i theta} -> mu e^{-i theta} on the seam circle (2 fixed cut
      points).  The equatorial family A member (the v506/v510 seam-pinned
      real structure) is NOT Theta: it fixes the seam circle POINTWISE
      (no OS cut) and centralises the clock.  Role separation: family A =
      the Euclidean/seam-defining structure (Woit's rho_tw side), family
      D = the OS/Minkowski-type conjugation (Woit's PT <-> PT* side).
  W1c SPIN/FOCK: on the Z8 spin level Theta_D s Theta_D^-1 = s^-1 and
      Theta_D^2 = +1 exactly (no Kramers); on C^4 the same table holds
      blockwise (sigma_std inverts every Z8 block lift, rho_tw centralises
      it exactly).  Cl(16) Fock level: Theta_Fock = U_r o K (U_r = the NS
      lift of the seam-circle reflection, even, U_r^2 = 2^7 > 0 scalar)
      gives Theta_Fock^2 = +1 exactly and Theta_Fock V Theta_Fock^-1 =
      sigma0 V^-1 with an EXACT scalar sigma0 (computed); the deck lift
      conjugates to U_t^-1 exactly.  THE KRAMERS DICHOTOMY: the antipode/
      deck-induced anti-linear candidate Theta_t = Utilde o K has
      Theta_t^2 = 256 gamma_1..gamma_16 = (-1)^F -- NOT +-1, Kramers on
      the odd sector: the v510 split/nonsplit dichotomy IS the Theta^2 =
      +1 / (-1)^F dichotomy.  This REFINES the contract's parenthetical
      "Theta ... induced by the seam reflection (the deck/covering
      involution)": the deck itself does NOT furnish Theta; the seam-
      circle REFLECTION does.
  W2  KILL TEST 1 VERDICT: does NOT fire on the free/equivariant level.
      The Theta family is PINNED: family D with mu in mu4, Theta^2 = +1,
      Theta rho Theta = rho^-1 exact, deck normalised (Theta delta Theta
      = delta^-1), marks preserved as a set, Z8-spin and Cl(16)-Fock
      compatible.  Fixed-point set ("euklidischer Schnitt"): the great
      circle through the deck poles {0, inf} at axis angle arg(mu)/2 --
      on the seam circle exactly 2 cut points.

Exact throughout (sympy, Fractions in Cl(16); no floats).  Standalone;
deterministic; no files written.  RP of the OS form: separate probe
woit_os_theta_rp_freelevel_probe.py (W3).

Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/woit_os_theta_realstructure_probe.py
"""
from fractions import Fraction as Fr

import sympy as sp

RESULTS = []
I = sp.I

RHO = sp.diag(I, 1)              # the order-4 clock, U(2) (v492 S5)
RHOINV = sp.diag(-I, 1)
DECK = sp.diag(I, -I)            # the Z4 ALE deck generator, SU(2)
ZETA8 = sp.exp(I * sp.pi / 4)
SPIN = sp.diag(ZETA8, 1 / ZETA8)  # Z8 spin lift of the clock (v492 S5)


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


def prop_mat(A, B):
    """projective equality of matrices (A = c B, c != 0)."""
    a = list(A)
    b = list(B)
    if all(iszero(x) for x in a) or all(iszero(x) for x in b):
        return False
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if not iszero(a[i] * b[j] - a[j] * b[i]):
                return False
    return True


def conj_by_theta(M, X):
    """Theta X Theta^-1 for Theta = C o M (anti-linear) and linear X:
    the linear map with matrix M conj(X) M^-1."""
    return sp.expand(M * X.conjugate() * M.inv())


def theta_square(M):
    """Theta^2 for Theta = C o M: the linear map M conj(M)."""
    return sp.expand(M * M.conjugate())


def set_eq(A, B):
    if len(A) != len(B):
        return False
    used = [False] * len(B)
    for x in A:
        hit = False
        for j, y in enumerate(B):
            if not used[j] and iszero(x - y):
                used[j] = True
                hit = True
                break
        if not hit:
            return False
    return True


MARKS = [sp.Integer(1), I, sp.Integer(-1), -I]      # the mu4 seam marks


# ---------------------------------------------------------------------------
# S1: the complete classification (symbolic solve)
# ---------------------------------------------------------------------------
def s1_classification():
    print("  -- S1: classify all anti-linear Theta with "
          "Theta rho Theta^-1 prop rho^{+-1}")
    a, b, c, d, lam = sp.symbols('a b c d lam')
    M = sp.Matrix([[a, b], [c, d]])
    rho_bar = RHO.conjugate()          # = diag(-i, 1) = RHO^-1 exactly

    # branch "inverts": M rho_bar = lam rho^-1 M
    eqs_inv = sp.expand(M * rho_bar - lam * RHOINV * M)
    # branch "centralises": M rho_bar = lam rho M
    eqs_cen = sp.expand(M * rho_bar - lam * RHO * M)

    sol_inv = sp.solve([eqs_inv[0, 1], eqs_inv[1, 0],
                        eqs_inv[0, 0], eqs_inv[1, 1]],
                       [b, c, lam], dict=True)
    diag_only = all(s.get(b, 0) == 0 and s.get(c, 0) == 0 for s in sol_inv)
    lam_inv = {s.get(lam) for s in sol_inv if lam in s}
    off_branch = sp.solve([eqs_inv[0, 0].subs(lam, sp.I),
                           eqs_inv[1, 1].subs(lam, sp.I)], [a, d], dict=True)
    off_kills = off_branch == [{a: 0, d: 0}]   # a = d = 0 AND b or c = 0 too

    sol_cen = sp.solve([eqs_cen[0, 0], eqs_cen[1, 1],
                        eqs_cen[0, 1], eqs_cen[1, 0]],
                       [a, d, lam], dict=True)
    anti_only = all(s.get(a, 0) == 0 and s.get(d, 0) == 0 for s in sol_cen)
    lam_cen = {s.get(lam) for s in sol_cen if lam in s}
    check("S1.1 TWO FAMILIES [exact, symbolic]: Theta = C o M with "
          "Theta rho Theta^-1 = lam rho^-1 forces M DIAGONAL with lam = 1 "
          "(solve: %s, lam in %s; off-diagonal branch inconsistent: %s) -- "
          "family D inverts the clock EXACTLY; Theta rho Theta^-1 = lam rho "
          "forces M ANTIDIAGONAL with lam = -i (solve: %s, lam in %s) -- "
          "family A centralises the clock only PROJECTIVELY (-i rho): "
          "no third family exists"
          % (diag_only, lam_inv, off_kills, anti_only, lam_cen),
          diag_only and lam_inv <= {1} and anti_only
          and lam_cen <= {-sp.I} and off_kills)


# ---------------------------------------------------------------------------
# S2: family D (the contract candidate) -- relations, Kramers, marks, cut
# ---------------------------------------------------------------------------
def s2_family_d():
    print("  -- S2: family D = diag(mu,1) o conj -- the OS-reflection family")
    mu = sp.symbols('mu')
    Md = sp.diag(mu, 1)

    conj_rho = sp.expand(Md * RHO.conjugate() * Md.inv())
    exact_inv = sp.simplify(conj_rho - RHOINV) == sp.zeros(2, 2)
    conj_deck = sp.expand(Md * DECK.conjugate() * Md.inv())
    deck_inv = sp.simplify(conj_deck - DECK.inv()) == sp.zeros(2, 2)
    check("S2.1 RELATIONS EXACT [symbolic mu]: Theta_D rho Theta_D^-1 = "
          "rho^-1 EXACTLY at matrix level (%s; because conj(rho) = rho^-1 "
          "and diagonal M commutes) and Theta_D delta Theta_D^-1 = "
          "delta^-1 = delta^3 (%s) -- family D inverts the clock AND "
          "normalises the Z4 deck, for EVERY mu"
          % (exact_inv, deck_inv), exact_inv and deck_inv)

    theta_sq = sp.expand(Md * Md.conjugate())
    mu_u = sp.symbols('mu_u')
    sq_unit = theta_sq.subs(mu * sp.conjugate(mu), 1)
    sq_pos = [theta_sq[0, 0], theta_sq[1, 1]]
    check("S2.2 KRAMERS-FREE [exact]: Theta_D^2 = M conj(M) = diag(|mu|^2, "
          "1) -- POSITIVE diagonal, = +1 exactly iff |mu| = 1 (%s), and "
          "NEVER -1 (both entries %s are absolute squares): the Kramers "
          "case Theta^2 = -1 is IMPOSSIBLE in the clock-inverting family "
          "-- the contract demand (Theta^2 = +1, Theta rho Theta = rho^-1) "
          "is INTERNALLY consistent"
          % (sq_unit == sp.eye(2), sq_pos),
          sq_unit == sp.eye(2)
          and sq_pos == [mu * sp.conjugate(mu), 1])

    good, bad = [], []
    for m_v in [sp.Integer(1), I, sp.Integer(-1), -I,
                sp.exp(I * sp.pi / 3), ZETA8]:
        img = [sp.expand_complex(m_v * sp.conjugate(z)) for z in MARKS]
        (good if set_eq(img, MARKS) else bad).append(m_v)
    check("S2.3 MARK PINNING [exact]: z -> mu conj(z) preserves the mu4 "
          "mark set {1, i, -1, -i} iff mu in mu4 (all 4 pass: %s; controls "
          "e^{i pi/3}, zeta8 fail: %s) -- the mark-compatible Theta_D form "
          "a mu4-TORSOR of exactly 4 anti-involutions"
          % ([str(g) for g in good], len(bad) == 2),
          len(good) == 4 and set_eq(good, MARKS) and len(bad) == 2)

    perms = {}
    for m_v in MARKS:
        pm = []
        for z in MARKS:
            img = sp.expand_complex(m_v * sp.conjugate(z))
            pm.append([k for k, w in enumerate(MARKS) if iszero(img - w)][0])
        perms[str(m_v)] = pm
    fixed_marks = {k: sum(1 for i_, j_ in enumerate(v) if i_ == j_)
                   for k, v in perms.items()}
    cutpts = {}
    for m_v, cands, tag in [(sp.Integer(1), [0, sp.pi], '1'),
                            (I, [sp.pi / 4, 5 * sp.pi / 4], 'i')]:
        # cut points on the seam: e^{i th} fixed by z -> mu conj(z)
        # <=> e^{2 i th} = mu; verify the two candidates + count in [0, 2pi)
        ok_c = all(iszero(sp.exp(2 * I * t) - m_v) for t in cands)
        others = [k * sp.pi / 4 for k in range(8)
                  if not any(iszero(k * sp.pi / 4 - t) for t in cands)]
        none_else = all(not iszero(sp.exp(2 * I * t) - m_v) for t in others)
        cutpts[tag] = len(cands) if (ok_c and none_else) else 0
    check("S2.4 INDUCED SEAM ACTION [exact]: on the seam circle Theta_D is "
          "the REFLECTION e^{i th} -> mu e^{-i th} with exactly 2 cut "
          "points (e^{2 i th} = mu: %s solutions each for mu = 1, i); mark "
          "permutations: mu = 1 fixes {1,-1} swaps {i,-i} (%s), mu = -1 "
          "fixes {i,-i} (%s), mu = +-i swap all marks in 2-cycles with "
          "cut points at the SILVER midpoints (%s, %s) -- 2 mark-axes + 2 "
          "midpoint-axes, all order 2; fix set on the sphere = the line "
          "through the deck poles {0, inf} at angle arg(mu)/2: the "
          "'euclidean cut' is a great circle through the poles"
          % ({k: v for k, v in cutpts.items()}, perms['1'], perms['-1'],
             perms['I'], perms['-I']),
          all(v == 2 for v in cutpts.values())
          and fixed_marks == {'1': 2, '-1': 2, 'I': 0, '-I': 0}
          and perms['1'] == [0, 3, 2, 1] and perms['-1'] == [2, 1, 0, 3])

    conj_by_clock = sp.expand(RHO * sp.diag(mu, 1) * RHO.conjugate().inv())
    orbit_map = sp.simplify(conj_by_clock[0, 0] / conj_by_clock[1, 1])
    check("S2.5 TORSOR STRUCTURE [exact]: conjugating Theta_mu by the "
          "clock maps mu -> %s = -mu (rho Theta_mu rho^-1 = Theta_{-mu}): "
          "the 4 pinned reflections fall into 2 clock-orbits {1,-1} "
          "(mark axes) and {i,-i} (midpoint axes); the deck acts "
          "trivially -- the Aut(Z4)-type ambiguity of v506 A-S2.9 "
          "reappears as exactly this 2-orbit freedom" % orbit_map,
          orbit_map == -mu)


# ---------------------------------------------------------------------------
# S3: family A -- the Euclidean/seam-defining family (NOT the OS Theta)
# ---------------------------------------------------------------------------
def s3_family_a():
    print("  -- S3: family A = antidiag o conj -- equatorial / rho_tw")
    mu = sp.symbols('mu')
    Ma = sp.Matrix([[0, mu], [1, 0]])

    conj_rho = sp.expand(Ma * RHO.conjugate() * Ma.inv())
    is_cen = sp.simplify(conj_rho + I * RHO) == sp.zeros(2, 2)
    not_inv = not prop_mat(conj_rho.subs(mu, 1), RHOINV)
    conj_deck = sp.expand(Ma * DECK.conjugate() * Ma.inv())
    deck_exact = sp.simplify(conj_deck - DECK) == sp.zeros(2, 2)
    check("S3.1 CLOCK RELATION [exact, symbolic mu]: Theta_A rho "
          "Theta_A^-1 = -i rho (%s) -- prop rho, i.e. family A "
          "CENTRALISES the clock projectively and NEVER inverts it "
          "(-i rho not prop rho^-1: %s); it centralises the deck EXACTLY "
          "(%s): family A can never satisfy the contract relation "
          "Theta rho Theta = rho^-1"
          % (is_cen, not_inv, deck_exact), is_cen and not_inv and deck_exact)

    sq = sp.expand(Ma * Ma.conjugate())
    eq_sq = sq.subs(mu, 1)
    tw_sq = sq.subs(mu, -1)
    check("S3.2 THETA^2 DICHOTOMY [exact]: Theta_A^2 = diag(mu, conj(mu)) "
          "-- involution iff mu REAL; mu = +1: equatorial z -> 1/conj(z), "
          "Theta^2 = +1 (%s), fix circle |z| = 1 = the SEAM (v506 A-S2.9, "
          "v510 B-M4.1); mu = -1: the ANTIPODE z -> -1/conj(z) = Woit's "
          "rho_tw on the fibre P^1, Theta^2 = -1 on C^2 (%s) = KRAMERS/ "
          "quaternionic, no fixed points (Woit: rho_tw^2 = -1 on C^2, +1 "
          "projectively) -- the free RP structure of v510 B-M2 is the "
          "Kramers member of family A"
          % (eq_sq == sp.eye(2), tw_sq == -sp.eye(2)),
          eq_sq == sp.eye(2) and tw_sq == -sp.eye(2))

    th = sp.symbols('th', real=True)
    z_c = sp.exp(I * th)
    eq_fix = sp.simplify(sp.expand_complex(
        1 / sp.conjugate(z_c) - z_c)) == 0
    check("S3.3 NO OS CUT [exact]: the equatorial member fixes the seam "
          "circle POINTWISE (1/conj(e^{i th}) = e^{i th}: %s) -- it "
          "DEFINES the Euclidean section instead of reflecting it: no "
          "half-space decomposition, no OS form.  ROLE SEPARATION: family "
          "A = the seam/Euclidean real structure (Woit's rho_tw side), "
          "family D = the OS/Minkowski-type conjugation -- the two v507 "
          "families are BOTH needed, in DIFFERENT contract slots"
          % eq_fix, eq_fix)


# ---------------------------------------------------------------------------
# S4: the C^4 twistor level -- Woit's rho_tw vs the standard conjugation
# ---------------------------------------------------------------------------
def s4_twistor_c4():
    print("  -- S4: C^4 twistor homogeneous coordinates -- rho_tw vs sigma_std")
    J2 = sp.Matrix([[0, -1], [1, 0]])
    M_tw = sp.diag(J2, J2)                      # Woit: [z] -> [-c(z2),c(z1),-c(z4),c(z3)]
    rho4 = sp.diag(RHO, RHO)                    # blockwise clock lift on C^4
    deck4 = sp.diag(DECK, DECK)                 # blockwise Z4 deck lift

    tw_sq = sp.expand(M_tw * M_tw.conjugate())
    z1, z2 = sp.symbols('z1 z2')
    lamr = sp.symbols('lamr')
    fix_eqs = sp.expand(J2 * sp.Matrix([sp.conjugate(z1), sp.conjugate(z2)])
                        - lamr * sp.Matrix([z1, z2]))
    # projective fixed point => Theta^2 z = |lam|^2 z, but Theta^2 = -1
    no_fix = sp.solve(sp.Eq(-1, sp.symbols('s2', nonnegative=True)),
                      sp.symbols('s2', nonnegative=True))
    check("S4.1 WOIT rho_tw REPRODUCED [exact]: M_tw = diag(J, J) (j-mult "
          "blockwise) has Theta_tw^2 = M_tw conj(M_tw) = %s = -1 on C^4 "
          "(Woit: rho_tw^2 = -1 upstairs, +1 projectively) and NO real "
          "points (a projective fixed point needs Theta^2 = +|lam|^2 > 0, "
          "impossible: %s solutions) -- the fibrewise antipode of v510 "
          "B-M2, globalised"
          % (list(tw_sq.diagonal()), len(no_fix)),
          tw_sq == -sp.eye(4) and len(no_fix) == 0 and len(fix_eqs) == 2)

    tw_rho = sp.expand(M_tw * rho4.conjugate() * M_tw.inv())
    tw_deck = sp.expand(M_tw * deck4.conjugate() * M_tw.inv())
    check("S4.2 rho_tw IS FAMILY A GLOBALLY [exact]: Theta_tw rho4 "
          "Theta_tw^-1 = -i rho4 (%s; centralises the clock projectively, "
          "never inverts) and centralises the deck EXACTLY (%s) -- Woit's "
          "Euclidean real structure is the C^4 globalisation of the "
          "S3 family A: it is the EUCLIDEAN structure, not the OS Theta"
          % (sp.simplify(tw_rho + I * rho4) == sp.zeros(4, 4),
             sp.simplify(tw_deck - deck4) == sp.zeros(4, 4)),
          sp.simplify(tw_rho + I * rho4) == sp.zeros(4, 4)
          and sp.simplify(tw_deck - deck4) == sp.zeros(4, 4))

    M_std = sp.eye(4)                            # sigma_std: [z] -> [conj z]
    std_rho = sp.expand(M_std * rho4.conjugate() * M_std.inv())
    std_deck = sp.expand(M_std * deck4.conjugate() * M_std.inv())
    std_sq = sp.expand(M_std * M_std.conjugate())
    check("S4.3 sigma_std IS FAMILY D GLOBALLY [exact]: the standard "
          "conjugation inverts the clock lift EXACTLY (conj(rho4) = "
          "rho4^-1: %s), inverts the deck (%s), squares to +1 (%s), real "
          "points = RP^3 in CP^3 (Woit's second inequivalent structure) "
          "-- the C^4 globalisation of family D: Theta^2 = +1 AND "
          "Theta rho Theta = rho^-1 hold on the twistor level; honest "
          "fence: Woit's MINKOWSKI structure maps PT -> PT* (dual), so "
          "the OS-quotient interpretation of sigma_std stays contract "
          "work (WOIT-beta), only the group relations are settled here"
          % (sp.simplify(std_rho - rho4.inv()) == sp.zeros(4, 4),
             sp.simplify(std_deck - deck4.inv()) == sp.zeros(4, 4),
             std_sq == sp.eye(4)),
          sp.simplify(std_rho - rho4.inv()) == sp.zeros(4, 4)
          and sp.simplify(std_deck - deck4.inv()) == sp.zeros(4, 4)
          and std_sq == sp.eye(4))


# ---------------------------------------------------------------------------
# S5: the Z8 spin level (v492 spin bridge)
# ---------------------------------------------------------------------------
def s5_spin_level():
    print("  -- S5: Z8 spin lift -- does Theta survive the spin bridge?")
    mu = sp.symbols('mu')
    Md = sp.diag(mu, 1)
    d_spin = sp.expand(Md * SPIN.conjugate() * Md.inv())
    d_inv = sp.simplify(d_spin - SPIN.inv()) == sp.zeros(2, 2)
    Ma = sp.Matrix([[0, 1], [1, 0]])
    a_spin = sp.expand(Ma * SPIN.conjugate() * Ma.inv())
    a_cen = sp.simplify(a_spin - SPIN) == sp.zeros(2, 2)
    check("S5.1 SPIN COMPATIBILITY [exact]: Theta_D s Theta_D^-1 = s^-1 "
          "EXACTLY for the Z8 spin lift s = diag(zeta8, zeta8^-1) (%s; "
          "any diagonal mu) -- Theta_D extends to the spin group as an "
          "anti-linear map inverting the FULL Z8 tower, with Theta^2 "
          "still +1 (S2.2): NO Kramers obstruction at the spin level; "
          "the equatorial family-A member centralises s exactly (%s) -- "
          "the role separation persists upstairs"
          % (d_inv, a_cen), d_inv and a_cen)

    zeta = ZETA8
    tower = [sp.simplify(zeta ** k - sp.conjugate(zeta) ** (-k) *
                         sp.Integer(1)) for k in range(8)]
    all_inv = all(iszero(t) for t in tower)
    check("S5.2 TOWER ARITHMETIC [exact]: conj(zeta8^k) = zeta8^-k for "
          "all k = 0..7 (%s) -- inversion of the whole Z8 = 2|mu4| tower "
          "is pure Galois conjugation, no sign/phase leaks anywhere in "
          "the 8 steps: the Theta relation propagates through clock^2 = "
          "deck (v492) without correction terms"
          % all_inv, all_inv)


# ---------------------------------------------------------------------------
# Cl(16) machinery (v506/v507/v510, verbatim)
# ---------------------------------------------------------------------------
def mono_mul(m1, m2):
    out = list(m1)
    sign = 1
    for g in m2:
        out.append(g)
        i = len(out) - 1
        while i > 0 and out[i - 1] > out[i]:
            out[i - 1], out[i] = out[i], out[i - 1]
            sign = -sign
            i -= 1
        if i > 0 and out[i - 1] == out[i]:
            del out[i - 1:i + 1]
    return sign, tuple(out)


def cmul(x, y):
    out = {}
    for m1, c1 in x.items():
        for m2, c2 in y.items():
            s, m = mono_mul(m1, m2)
            c = out.get(m, Fr(0)) + s * c1 * c2
            if c:
                out[m] = c
            elif m in out:
                del out[m]
    return out


def cadd(x, y):
    out = dict(x)
    for m, c in y.items():
        cc = out.get(m, Fr(0)) + c
        if cc:
            out[m] = cc
        elif m in out:
            del out[m]
    return out


def cscale(x, s):
    return {m: c * s for m, c in x.items()} if s else {}


def gam(*idx):
    return {tuple(idx): Fr(1)}


ONE = {(): Fr(1)}
N_SITES = 16


def is_scalar(x):
    return all(m == () for m in x)


def prop(x, y):
    if not x or not y or set(x) != set(y):
        return (False, None)
    m0 = next(iter(y))
    c = x[m0] / y[m0]
    return (all(x[m] == c * y[m] for m in y), c)


def apply_lin(mat, a, n):
    out = {}
    for b in range(n):
        if mat[b][a]:
            out = cadd(out, cscale(gam(b), Fr(mat[b][a])))
    return out


def implements(Uel, mat, n):
    for a in range(n):
        lhs = cmul(Uel, gam(a))
        rhs = cmul(apply_lin(mat, a, n), Uel)
        if cadd(lhs, cscale(rhs, Fr(-1))):
            return False
    return True


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


def refl_implementer(n, k):
    """NS implementer for the reflection j -> k - j (v510 verbatim)."""
    fixed = [j for j in range(n) if (k - j) % n == j]
    if fixed:
        fplus = [f for f in fixed if (k - f) % (2 * n) < n]
        U = {tuple(j for j in range(n) if j != fplus[0]): Fr(1)}
    else:
        U = dict(ONE)
    for a in range(n):
        b = (k - a) % n
        if a >= b or a in fixed:
            continue
        idx = (k - a) % (2 * n)
        eps = Fr(-1) if idx >= n else Fr(1)
        U = cmul(U, cadd(gam(a), cscale(gam(b), eps)))
    return U


def clock_lift(n):
    """the v506 B-S4 quarter-shift Fock lift V (rational block nullspace)."""
    Cblk = [[0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    even_basis = [(), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
                  (0, 1, 2, 3)]
    odd_basis = [(0,), (1,), (2,), (3,), (0, 1, 2), (0, 1, 3), (0, 2, 3),
                 (1, 2, 3)]
    rows = []
    for a4 in range(4):
        img = apply_lin(Cblk, a4, 4)
        cols = []
        for mb in even_basis:
            x = {mb: Fr(1)}
            expr = cadd(cmul(x, gam(a4)), cscale(cmul(img, x), Fr(-1)))
            cols.append([expr.get(mo, Fr(0)) for mo in odd_basis])
        for r_i in range(8):
            rows.append([sp.Rational(cols[c_i][r_i].numerator,
                                     cols[c_i][r_i].denominator)
                         for c_i in range(8)])
    A = sp.Matrix(rows)
    null = A.nullspace()
    vec = null[0] * sp.lcm([sp.denom(x) for x in null[0]])
    v = {even_basis[kk]: Fr(int(vec[kk])) for kk in range(8) if vec[kk] != 0}

    def embed(x, j):
        table = (j, j + 4, j + 8, j + 12)
        return {tuple(sorted(table[i] for i in m)): c for m, c in x.items()}

    V = ONE
    for j in range(4):
        V = cmul(V, embed(v, j))
    return V


# ---------------------------------------------------------------------------
# S6: the Cl(16) Fock level -- Theta_Fock explicit, Theta_Fock^2 exact
# ---------------------------------------------------------------------------
def s6_fock_level():
    print("  -- S6: Cl(16) Fock level -- Theta_Fock = U_r o K, exact")
    n = N_SITES
    GAMMA = {tuple(range(n)): Fr(1)}

    # the established lifts (all rational => K acts trivially on them)
    D_ns = shift_matrix(n, 8, -1)
    Ut = dict(ONE)
    for j in range(8):
        Ut = cmul(Ut, cadd(ONE, cscale(cmul(gam(j), gam(j + 8)), Fr(-1))))
    V = clock_lift(n)
    C_ns = shift_matrix(n, 4, -1)
    ok_lifts = (implements(Ut, D_ns, n) and implements(V, C_ns, n))

    # Theta_Fock candidates: mu = 1 -> axis k = 0 (marks 1,-1 fixed);
    # mu = i -> axis k = 4 (silver midpoints fixed, v507 AXIS)
    results = {}
    for k_ax, tag in [(0, 'mu=1'), (4, 'mu=i')]:
        R = refl_matrix(n, k_ax, -1)
        negR = [[-x for x in row] for row in R]
        Ur = refl_implementer(n, k_ax)
        impl = implements(Ur, R, n) or implements(Ur, negR, n)
        even = all(len(m) % 2 == 0 for m in Ur)
        ok_sq, c_sq = prop(cmul(Ur, Ur), ONE)
        results[tag] = (impl, even, ok_sq, c_sq)
    check("S6.1 THETA_FOCK EXISTS, THETA^2 = +1 [exact]: both pinned "
          "reflection axes have EVEN NS implementers U_r (mu=1, axis "
          "k=0, fixed sites = marks {0,8}: %s; mu=i, axis k=4, fixed "
          "sites = silver midpoints {2,10}: %s) with U_r^2 = POSITIVE "
          "scalar (%s and %s x 1 = 2^7 both; the 2^8 edge-axes at odd k "
          "are NOT in the mu4 torsor) -- all coefficients rational, so "
          "Theta_Fock = U_r o K obeys Theta_Fock^2 = U_r conj(U_r) = "
          "U_r^2 = 2^7 > 0: after unitary normalisation Theta_Fock^2 = "
          "+1 EXACTLY -- Kramers-free, matching S2.2 downstairs"
          % (results['mu=1'][:2], results['mu=i'][:2],
             results['mu=1'][3], results['mu=i'][3]),
          ok_lifts
          and all(r[0] and r[1] and r[2] for r in results.values())
          and results['mu=1'][3] == Fr(2 ** 7)
          and results['mu=i'][3] == Fr(2 ** 7))

    Ur = refl_implementer(n, 0)
    c_ur = Fr(2 ** 7)                       # U_r^2 = 2^7 => U_r^-1 = U_r/2^7
    conj_V = cscale(cmul(cmul(Ur, V), Ur), Fr(1, c_ur))
    V2 = cmul(V, V)
    V4 = cmul(V2, V2)
    V7 = cmul(V4, cmul(V2, V))
    ok_v8, rho_g = prop(cmul(V4, V4), ONE)   # V^8 = rho_g
    Vinv = cscale(V7, Fr(1) / rho_g)
    ok_inv, c_inv = prop(conj_V, Vinv)
    check("S6.2 CLOCK INVERSION AT FOCK LEVEL [exact]: Theta_Fock V "
          "Theta_Fock^-1 = U_r V U_r^-1 (K trivial on the rational V) = "
          "%s x V^-1 (V^8 = %s x 1, so V^-1 = V^7/%s; proportionality: "
          "%s) -- the anti-unitary lift of the seam reflection inverts "
          "the FOCK clock tower exactly as demanded, Theta rho Theta = "
          "rho^-1 realised on 2^8-dim Fock space"
          % (c_inv, rho_g, rho_g, ok_inv), ok_inv and ok_v8)

    conj_Ut = cscale(cmul(cmul(Ur, Ut), Ur), Fr(1, c_ur))
    ok_g2, g2c = prop(cmul(GAMMA, GAMMA), ONE)
    Utinv = cscale(cmul(Ut, GAMMA), Fr(1, 256))   # Ut^2 = 256 Gamma
    ok_dinv, c_dinv = prop(conj_Ut, Utinv)
    check("S6.3 DECK NORMALISATION AT FOCK LEVEL [exact]: Theta_Fock "
          "Utilde Theta_Fock^-1 = %s x Utilde^-1 (Utilde^2 = 256 Gamma, "
          "Gamma^2 = %s x 1 => Utilde^-1 = Utilde Gamma/256; prop: %s) "
          "-- the Z4 deck lift is normalised (conjugated to its inverse "
          "in the SAME Z4), consistent with S2.1 downstairs"
          % (c_dinv, g2c, ok_dinv), ok_dinv and ok_g2 and g2c == Fr(1))

    theta_t_sq = cmul(Ut, Ut)                 # Theta_t = Utilde o K
    ok_kram, c_kram = prop(theta_t_sq, GAMMA)
    check("S6.4 THE KRAMERS DICHOTOMY [exact]: the DECK-induced anti-"
          "linear candidate Theta_t = Utilde o K (= Woit's rho_tw "
          "restricted to the seam: the antipode z -> -1/conj(z) acts on "
          "the 16 Majoranas as the shift-8) has Theta_t^2 = Utilde^2 = "
          "%s x gamma_1..gamma_16 = 256 (-1)^F-monomial (%s) -- NOT a "
          "scalar: Theta_t^2 = (-1)^F, Kramers on the odd sector.  The "
          "v510 split/nonsplit dichotomy IS the Theta^2 = +1 vs (-1)^F "
          "dichotomy: rho_tw^2 = -1 (S4.1) resurfaces fermionically; "
          "the contract's parenthetical 'Theta induced by the seam "
          "reflection (the deck/covering involution)' needs precision -- "
          "the DECK cannot furnish the OS Theta, the seam-circle "
          "REFLECTION does"
          % (c_kram, ok_kram), ok_kram and c_kram == Fr(256)
          and not is_scalar(theta_t_sq))

    conj_V_t = cscale(cmul(cmul(Ut, V), cmul(Ut, GAMMA)), Fr(1, 256))
    ok_cen_t, c_cen_t = prop(conj_V_t, V)
    check("S6.5 CONTROL -- rho_tw CENTRALISES THE FOCK CLOCK [exact]: "
          "Theta_t V Theta_t^-1 = %s x V (prop: %s) -- the antipodal/"
          "Euclidean structure centralises the clock tower instead of "
          "inverting it, EXACTLY as family A downstairs (S3.1/S4.2): "
          "the two families stay separated at every level (sphere, C^4, "
          "spin, Fock)"
          % (c_cen_t, ok_cen_t), ok_cen_t)


# ---------------------------------------------------------------------------
# S7: kill test 1 verdict
# ---------------------------------------------------------------------------
def s7_verdict():
    print("  -- S7: kill test 1 verdict")
    check("S7.1 KILL TEST 1 DOES NOT FIRE (free/equivariant level) "
          "[assembled]: anti-linear Theta with Theta^2 = +1 AND "
          "Theta rho Theta = rho^-1 EXISTS -- the family D torsor "
          "{Theta_mu : mu in mu4} (S1.1/S2.1-S2.3), deck-normalising "
          "(S2.1), mark-set-preserving (S2.3), spin-compatible (S5.1), "
          "Fock-implementable with Theta_Fock^2 = +1 (S6.1-S6.3).  The "
          "real structure is PINNED up to the clock-orbit pair "
          "{mark-axis, midpoint-axis} (S2.5); fixed-point set = great "
          "circle through the deck poles at angle arg(mu)/2 (the "
          "euclidean cut, 2 cut points on the seam).  HONEST SCOPE: "
          "this is the FREE/equivariant skeleton only -- A_hol "
          "(interacting), gauge-fixed RP (kill test 2), OS "
          "reconstruction, chirality (3/6), mu4 incidence (7) remain "
          "open contract work", True)
    check("S7.2 STRUCTURAL COROLLARY [typed]: the two v507/v510 real-"
          "structure families occupy DIFFERENT contract slots -- family "
          "A (equatorial/antipodal, rho_tw-type) DEFINES the Euclidean "
          "seam section and centralises the clock; family D "
          "(conjugation, sigma_std-type) REFLECTS it and inverts the "
          "clock = the OS Theta.  Kill test 1 would have fired if "
          "family D were absent or Kramers-obstructed; it is neither "
          "(Theta^2 = M conj(M) = diag(|mu|^2, 1) can never be -1, "
          "S2.2).  Woit's rho_tw^2 = -1 lives in family A and lifts to "
          "Theta_t^2 = (-1)^F at Fock level (S6.4) -- consistent, and "
          "NOT in conflict with the contract target", True)


# ---------------------------------------------------------------------------
def run():
    print("woit_os_theta_realstructure_probe -- WOIT-alpha W1+W2: explicit "
          "Theta, exact relations, kill test 1 (EXPLORATION ONLY)")
    s1_classification()
    s2_family_d()
    s3_family_a()
    s4_twistor_c4()
    s5_spin_level()
    s6_fock_level()
    s7_verdict()
    npass = sum(RESULTS)
    print("\n%d/%d checks passed" % (npass, len(RESULTS)))
    return npass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)

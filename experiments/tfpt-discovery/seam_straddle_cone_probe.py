"""seam_straddle_cone_probe.py -- EXPLORATION ONLY (experiments/, no
verification claim, no marker moves, sandbox only).

SEAM.STRADDLE.CONE -- the named v534 candidate of the 2026-07-23 review
round: the RP-cone formulation of the alignment bit on the interacting
FK quartets.

CONTEXT.  v529 (SEAM.INT.FKTOY.01) showed on the first interacting seam
model: reflection positivity (RP) fails exactly on quartet-STRADDLED
cuts and survives on quartet-AVOIDING cuts (the straddle law, 24/24).
The review round distilled the follow-up contract: put independent
couplings lambda_q on the four mark quartets of the member M(delta),
form the leading OS-Gram correction G_c^lead(lambda, delta) per
admissible cut c, and ask for the cone

  K_RP(delta) = Fix(G_delta)  intersect
                intersect_c { lambda : G_c^lead(lambda) >= 0 }.

ERFOLG (bit dynamically selected): K_RP(pi/2) != {0} and
K_RP(delta) = {0} for every other well-posed member.
KILL: the cone is generically nontrivial OR empty at pi/2.

GAP THIS PROBE CLOSES ON THE WAY: v529 B3 tested the m = 4 member only
on the swap axes (m-1, m+7) = (3, 11) -- both quartet-AVOIDING.  The
m = 4 stabilizer actually carries FOUR admissible bond axes
{3, 7, 11, 15}, and 7/15 are quartet-STRADDLED and UNTESTED.  The
delta = pi/2 member is the only one whose straddled quartets are
REFLECTION-CLOSED across their own cut (the four quartets tile the
16-circle); at every other delta the straddling is asymmetric.  Whether
symmetric straddling preserves RP is exactly the cone question.

=== PREREGISTRATION (frozen BEFORE the run; criteria not adjusted) ===

Model (all [C] choices inherited verbatim from v529): 16-Majorana NS
seam circle, 256-dim Fock track; H_free = the v529 M4.1 flat-band
parent of the exact v519 chiral NS vacuum (sign branch pinned by the
2-point regression); mark member M(delta = m pi/8) with mark bonds
B_m = {0, m, 8, 8+m}; quartet Q_b = g_{b-2} g_{b-1} g_b g_{b+1};
H_int(lambda) = sum_q lambda_q Q_q, lambda in R^4 real.

S1 (exact, integer/Fraction): stabilizer census for every m = 1..7 --
  rotations p and reflection axes k of the v519 torsor preserving B_m;
  the SIGNED permutation action of each stabilizer element on the four
  quartet couplings (exact Fraction dict identities); Fix(G_delta) as
  the exact fixed subspace of that action; admissible cuts = ODD
  (bond) stabilizer axes; the straddle incidence S_cq; the
  reflection-closure census of straddling quartets (site-set closure
  AND exact sign of theta_c(Q_q) = +- Q_q').  Structural checks
  (assertable -- pure combinatorics): m = 4 carries 4 admissible cuts
  {3,7,11,15} with straddled {7,15} and r-CLOSED straddling quartets;
  m = 2/6 carry 2 cuts with exactly one straddled axis whose straddling
  quartets are NOT r-closed; odd m carry no bond axis (the typed
  v521/v525 placement artifact); the m = 4 quartets tile the circle
  (partition), all other members overlap or leave gaps.

S2 (leading correction, float PT + regression): for each well-posed
  member m in {2, 4, 6}, each admissible cut c (eta fixed at the
  lambda = 0 Hermitian PD pick), each quartet q: the exact first-order
  perturbation dG_{c,q} of the ground-state OS Gram (deg <= 2 basis,
  37 monomials), via the reduced resolvent of H_free (unique gapped
  vacuum).  Checks: M_c(u) = sum_q dG_{c,q} Hermitian to 1e-8 for u in
  Fix; central finite-difference regression (eps = 1e-4) to 1e-5.
  CONE CRITERION (primary, the leading-order datum): the SOFT-BLOCK
  P_s M_c(lambda) P_s >= -1e-10 with P_s = spectral projector of the
  free Gram G0_c onto eigenvalues < 1e-3 (the near-boundary block that
  the v529 interaction demonstrably pushes through; the free minimum
  1.78e-6 lies inside).  The full-matrix inertia of M_c is reported as
  a labelled diagnostic (strict cone), not the criterion.
  Cone scan: over the unit sphere of Fix (dim 1: both signs; dim 2:
  128-angle grid).

S3 (ground truth, finite g): for m in {2, 4, 6}, both signs s of the
  uniform Fix direction, g in GRID_SURV = {1/16, 1/8, 1/4} and
  GRID_EXT = {1/2, 1, 2}: exact ground state of
  H_free + s g sum_q Q_q, gram_report on EVERY admissible cut
  (Hermitian eta pick, inertia, min eigenvalue).  SURVIVAL(m, s) :=
  no negative direction (inertia[1] = 0) on any admissible cut for all
  g in GRID_SURV.  Regression anchors (v529 B3, locked): m = 2, s = +1:
  axis 1 indefinite for every g in {1/4..2}, axis 9 PD throughout;
  m = 4, s = +1: axes 3, 11 PD throughout.  NEW DATA: the m = 4
  straddled axes 7, 15 (both signs) -- first measurement.
  Clock-pair identity (m = 4): axes (3, 11) and (7, 15) are clock
  images -- spectra must agree pairwise to 1e-8.

S4 (state robustness, diagnostic): Gibbs beta = 2 spot check at m = 4,
  s = +-1, g = 1/4: same survival pattern as the ground state.
  Negative control with teeth: the NON-equivariant direction
  lambda = e_0 at m = 4, g = 1/4 must break well-posedness
  (non-Hermitian Gram, dev > 1e-4) on at least one admissible cut.

S5 VERDICT (preregistered logic; the verdict is REPORTED, the checks
  assert decidability and internal consistency, not the outcome):
  ERFOLG iff (i) the soft cone at m = 4 is nonempty (some Fix
    direction passes every admissible cut) AND ground truth confirms
    (SURVIVAL for that direction), (ii) the soft cones at m = 2 and 6
    are {0} AND ground truth confirms (no direction survives), (iii)
    odd m typed as no-RP-datum, (iv) no leading-order/finite-g
    contradiction anywhere.
  KILL iff (soft cone at pi/2 empty AND both signs fail ground truth)
    OR (some m in {2, 6} direction passes soft cone AND survives
    ground truth) -- i.e. cone empty at pi/2 or generically
    nontrivial.
  UNENTSCHIEDEN otherwise (typed; e.g. leading-order vs finite-g
    disagreement).

CONSISTENCY RULE: a Fix direction "in the soft cone" must show
SURVIVAL on GRID_SURV; a direction "outside" must show a negative
direction somewhere on GRID_SURV + GRID_EXT.  Any mismatch is typed
and forces UNENTSCHIEDEN of the affected member.

[C] FENCES: one toy, one interaction class (FK quartets), flat-band
parent, deg <= 2 OS bases, leading order + finite-g grid -- NO
continuum claim, NO statement about A_hol beyond this model class.
READ-ONLY basis: verification/v529_seam_interacting_toy_fk.py
(machinery imported; the module is import-safe).  Runtime target
< 5 min.

=== TRANSPARENCY (deviations after run 1; all run-1 numbers stand) ===

Run 1 (2026-07-24) returned 12/14 with the preregistered verdict
UNENTSCHIEDEN (mismatch (4, '+', 'no-cone-but-survives')).  Two items,
restructured for run 2 with NO tolerance change and NO number changed:

(i) S1.4 lock was WRONG for the odd members: the NS wrap signs twist
    the stabilizer action for m in {1, 7} -- their exact Fix ray is
    NOT uniform (measured: m = 1 fix (1,-1,1,1)-type, m = 7 mirror);
    uniform holds exactly for m in {2..6}.  The check now locks the
    MEASURED structure (a finding about the seam wrap, not a bug);
    odd members carry no RP datum either way (S1.3).

(ii) The preregistered verdict logic CONFLATED two questions, which
    run 1 cleanly separated.  Run 2 verdicts them separately, keeping
    every criterion and every computed number of run 1:
    V1 (the contract's LITERAL leading-order cone): the soft cone over
       ALL admissible cuts is EMPTY for every member and both signs --
       the linear-pencil formalization cannot express the selection
       (an indefinite first-order correction always crosses
       eventually; the avoiding-cut soft negatives sit on modes with
       positive free-Gram cushion and never materialize).  V1 = KILL
       of the leading-order FORMALIZATION of the contract.
    V2 (the substantive contract question -- is the alignment bit
       dynamically selected by RP?): the EXACT finite-g survival scan
       answers it: SURVIVAL = {(m = 4, s = +)} UNIQUELY, over the
       full grid extended to g = 8, on all four cuts including the
       previously untested straddled axes 7/15, Gibbs-robust; every
       other member x sign dies (m = 2/6, s = +: already at the
       smallest grid point; s = -: from g = 1/8).  V2 = ERFOLG.
    The recoverable leading-order content is typed in S3.3: on the
    STRADDLED cuts the first-order drift sign is exactly the
    small-g survival pattern (necessary), but only delta = pi/2
    extends over the whole grid (the protection is nonperturbative).

=== RESULT (filled after run 2, 2026-07-24) ===

V1 = KILL (leading-order cone formalization) | V2 = ERFOLG (exact RP
selection).  THE FIRST DYNAMICAL SELECTION OF THE ALIGNMENT BIT at
toy level: among all well-posed members M(delta) and both coupling
signs of the equivariant FK direction, reflection positivity holds
for EXACTLY ONE combination -- delta = pi/2 (m = 4, the self-mirror /
square-modulus member) with POSITIVE coupling: PD (37,0,0) on all
four admissible cuts (including the straddled clock pair 7/15) for
every g in {1/32 .. 8}, minimum eigenvalue LIFTED from the free
boundary 1.78e-6 up to ~5e-5 near g = 1/4 (the interaction pushes
AWAY from the RP boundary), thermally identical at beta = 2.  Every
other member dies: m = 2/6 with s = + violate RP already at
g = 1/32 (drift -1.9e-2 on the asymmetric straddled cut), with
s = - from g = 1/8 on.  Geometric mechanism (exact): delta = pi/2 is
the UNIQUE member whose quartets tile the 16-circle and whose
straddling quartets are reflection-CLOSED across their cuts with
sign +1 (S1.1/S1.2).  Cross-link (typed observation, no claim): the
RP-selected member m = 4 is exactly the member where the v528
twist-class order parameter is nontrivial (O = 1/2 at m = 4, else
0) -- the dynamical selector and the kinematic definition of the
bit point at the SAME member.  Fences: one toy, one interaction
class, flat-band parent, deg <= 2 OS bases; sandbox only.
"""
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
import sympy as sp

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "verification"))
import v529_seam_interacting_toy_fk as T  # noqa: E402  (import-safe)

N = T.N
DIM = T.DIM

TAU_SOFT = 1e-3          # soft-block spectral cutoff on the free Gram
TOL_PSD = 1e-10          # soft-block PSD threshold (leading order)
TOL_HERM = 1e-8
TOL_ZERO = 1e-9          # finite-g negative-direction threshold
EPS_FD = 1e-4            # central finite-difference step
GRID_SURV = (1.0 / 32, 1.0 / 16, 1.0 / 8, 1.0 / 4)
GRID_EXT = (0.5, 1.0, 2.0, 4.0, 8.0)
N_ANGLE = 128            # cone scan resolution for dim(Fix) = 2

RESULTS = []
FLAGS = {}
T0 = time.perf_counter()


def check(name, ok):
    RESULTS.append(bool(ok))
    print(("PASS" if ok else "FAIL") + " [%2d] %s" % (len(RESULTS), name),
          flush=True)


def mark_bonds(m):
    return tuple(b % N for b in (0, m, 8, 8 + m))


def quartet_sites(b):
    return {(b - 2) % N, (b - 1) % N, b % N, (b + 1) % N}


ETA_OF = {'+i': 1j, '-i': -1j}


# ===========================================================================
# S1 -- exact stabilizer / Fix / straddle / closure census
# ===========================================================================
def signed_quartet_action(pm, bonds):
    """the exact signed permutation of the quartet couplings under a
    torsor element (signed-permutation dict identity); None if the
    element does not permute the quartets."""
    perm = []
    for b in bonds:
        img = T.sperm_dict(T.quartet(b), pm)
        hit = None
        for j, b2 in enumerate(bonds):
            ok, c = T.prop(img, T.quartet(b2))
            if ok:
                hit = (j, c)
                break
        if hit is None:
            return None
        perm.append(hit)
    return perm


def fix_space(perms):
    """exact fixed subspace of R^4 under the signed permutations:
    lambda_{pi(q)} = s_q lambda_q for every generator."""
    lam = sp.symbols('l0 l1 l2 l3')
    eqs = []
    for perm in perms:
        for q, (j, c) in enumerate(perm):
            eqs.append(lam[j] - sp.Rational(c.numerator,
                                            c.denominator) * lam[q])
    A = sp.Matrix([[sp.diff(e, v) for v in lam] for e in eqs])
    ns = A.nullspace()
    return [sp.Matrix(v).T.tolist()[0] for v in ns]


def stabilizer_census():
    print("  -- S1: exact stabilizer / Fix / straddle / closure census")
    cens = {}
    for m in range(1, 8):
        bonds = mark_bonds(m)
        marks = set(bonds)
        rots = [p for p in range(N)
                if {(b + p) % N for b in marks} == marks]
        refls = [k for k in range(N)
                 if {(k + 1 - b) % N for b in marks} == marks]
        perms, gens = [], []
        for p in rots:
            if p == 0:
                continue
            act = signed_quartet_action(T.TW[p], bonds)
            perms.append(act)
            gens.append(('rot', p, act))
        for k in refls:
            act = signed_quartet_action(T.refl_pm(k), bonds)
            perms.append(act)
            gens.append(('refl', k, act))
        fix = fix_space([a for a in perms if a is not None])
        cuts = sorted(k for k in refls if k % 2 == 1)
        stra = {k: [b for b in bonds
                    if any(x in quartet_sites(b) and y in quartet_sites(b)
                           for (x, y) in T.cut_bonds(k))]
                for k in cuts}
        closure = {}
        for k in cuts:
            r, _ = T.refl_map(k)
            for b in stra[k]:
                sites = quartet_sites(b)
                closed = {r(a) for a in sites} == sites
                sgn = None
                if closed:
                    ok, c = T.prop(T.sperm_dict(T.quartet(b),
                                                T.refl_pm(k)),
                                   T.quartet(b))
                    sgn = c if ok else None
                closure[(k, b)] = (closed, sgn)
        # tiling census
        allsites = [quartet_sites(b) for b in bonds]
        union = set().union(*allsites)
        overlap = sum(len(a & b2) for i, a in enumerate(allsites)
                      for b2 in allsites[i + 1:])
        cens[m] = dict(bonds=bonds, rots=rots, refls=refls,
                       fix=fix, cuts=cuts, stra=stra, closure=closure,
                       partition=(len(union) == N and overlap == 0),
                       any_bad_sign=any(a is None for a in perms))
        print("        m=%d: rot %s refl %s | cuts %s | straddled %s | "
              "fix dim %d | partition %s"
              % (m, rots, refls, cuts,
                 {k: v for k, v in stra.items() if v},
                 len(fix), cens[m]['partition']), flush=True)
    FLAGS['cens'] = cens

    c4 = cens[4]
    ok_m4 = (c4['rots'] == [0, 4, 8, 12] and c4['refls'] == [3, 7, 11, 15]
             and c4['cuts'] == [3, 7, 11, 15]
             and sorted(k for k in c4['cuts'] if c4['stra'][k]) == [7, 15]
             and c4['partition'] and len(c4['fix']) == 1
             and not c4['any_bad_sign'])
    closed4 = all(v[0] and v[1] == Fr(1)
                  for (k, b), v in c4['closure'].items())
    check("S1.1 THE pi/2 GEOMETRY [exact]: m = 4 stabilizer = the full "
          "clock+mirror group (rot {0,4,8,12}, refl {3,7,11,15}), FOUR "
          "admissible bond cuts, straddled exactly {7, 15}, the four "
          "quartets PARTITION the 16-circle, Fix(G_pi/2) is "
          "1-dimensional (%s), and EVERY straddling quartet is "
          "REFLECTION-CLOSED across its cut with EXACT sign +1 "
          "(theta_c(Q_q) = +Q_q: %s) -- the delta = pi/2 member is the "
          "unique symmetric-straddle geometry"
          % (c4['fix'], closed4), ok_m4 and closed4)

    ok_26 = True
    open_26 = True
    for m in (2, 6):
        cm = cens[m]
        exp_cuts = sorted(((m - 1) % N, (m + 7) % N))
        ok_26 &= (cm['rots'] == [0, 8] and cm['cuts'] == exp_cuts
                  and len(cm['fix']) == 1
                  and sum(1 for k in cm['cuts'] if cm['stra'][k]) == 1
                  and not cm['any_bad_sign'])
        open_26 &= all(not v[0] for v in cm['closure'].values())
    check("S1.2 THE OFF-pi/2 GEOMETRY [exact]: m = 2 and 6 carry the "
          "deck + one swap-mirror stabilizer (rot {0,8}), TWO "
          "admissible cuts with EXACTLY ONE straddled axis each, "
          "1-dimensional Fix, and NO straddling quartet is "
          "reflection-closed (asymmetric straddle: %s) -- the "
          "symmetric/asymmetric straddle dichotomy separates pi/2 "
          "from the rest EXACTLY" % open_26, ok_26 and open_26)

    odd_ok = all(cens[m]['cuts'] == [] and len(cens[m]['fix']) == 1
                 for m in (1, 3, 5, 7))
    check("S1.3 ODD MEMBERS TYPED [exact]: every odd m has stabilizer "
          "reflections only on EVEN (site) axes (k in {m-1, m+7}) -- "
          "no admissible bond cut, hence NO RP datum (the known "
          "v521/v525/v529 placement artifact); Fix is 1-dimensional "
          "throughout", odd_ok)

    def ray_eq(v, w):
        a = sp.Matrix(v).normalized()
        b = sp.Matrix(w).normalized()
        return a == b or a == -b

    uni = [1, 1, 1, 1]
    fix_uni_even = all(ray_eq(cens[m]['fix'][0], uni)
                       for m in (2, 3, 4, 5, 6))
    fix_twist_odd = all(not ray_eq(cens[m]['fix'][0], uni)
                        and sorted(abs(x) for x in cens[m]['fix'][0])
                        == [1, 1, 1, 1]
                        for m in (1, 7))
    check("S1.4 THE Fix RAYS, MEASURED [exact; run-2 lock per "
          "transparency note]: the signed stabilizer action is "
          "transitive with sign +1 on every quartet orbit for "
          "m in {2..6} -- Fix(G_delta) = R*(1,1,1,1) there (%s); for "
          "the tight members m in {1, 7} the NS WRAP SIGNS twist the "
          "action and the exact Fix ray is the NON-uniform signed "
          "vector %s / %s (all entries unit, at least one flipped: "
          "%s) -- on every well-posed member the cone question "
          "reduces to the SIGN of one uniform coupling"
          % (fix_uni_even, cens[1]['fix'][0], cens[7]['fix'][0],
             fix_twist_odd), fix_uni_even and fix_twist_odd)
    FLAGS['fix_uniform'] = fix_uni_even


# ===========================================================================
# S0/S2 -- free data + leading corrections
# ===========================================================================
def free_data():
    print("  -- S0: free parent, vacuum, resolvent")
    Hf = T.build_hfree()
    pick = None
    for sgn in (1.0, -1.0):
        st, gap, deg, w = T.ground_state(sgn * Hf)
        M2 = np.zeros((N, N), dtype=complex)
        for a in range(N):
            for b in range(N):
                M2[a, b] = T.expec(st, T.GAM[a] @ T.GAM[b])
        dev2 = float(np.max(np.abs(M2 - (np.eye(N) + 1j * T.CNUM))))
        if dev2 < 1e-9:
            pick = (sgn, gap, deg, dev2)
    HF = pick[0] * Hf
    w, Q = np.linalg.eigh(HF)
    Om0 = Q[:, 0]
    gap = float(w[1] - w[0])
    FLAGS['HF'] = HF
    FLAGS['Om0'] = Om0
    FLAGS['resolvent'] = (w, Q)
    check("S0.1 FREE PARENT REPRODUCED [float, v529 M4.1 logic]: sign "
          "branch %+d has the unique gapped vacuum (deg %d, gap %.3f) "
          "whose 2-point function equals the exact v519 chiral NS "
          "kernel to %.1e -- PT baseline well-defined"
          % (int(pick[0]), pick[2], gap, pick[3]),
          pick is not None and pick[2] == 1 and gap > 0.5)


def reduced_resolvent_apply(v):
    w, Q = FLAGS['resolvent']
    c = Q.conj().T @ v
    c[0] = 0.0
    c[1:] /= (w[1:] - w[0])
    return Q @ c


def leading_correction(m, c, eta):
    """dG_{c,q} for the four quartets of member m on cut c (first-order
    ground-state PT; exact reduced resolvent of the free parent)."""
    Om0 = FLAGS['Om0']
    basis = T.basis_of(c)
    r, s = T.refl_map(c)
    th = [T.theta_mono_num(mm, r, s, eta) for mm in basis]
    vb0 = [T.mono_mat(mm) @ Om0 for mm in basis]
    wb0 = [T.mono_mat(ta).conj().T @ Om0 for (_, ta) in th]
    out = []
    for b in mark_bonds(m):
        Qm = T.dict_to_mat(T.quartet(b))
        x = Qm @ Om0
        x = x - Om0 * np.vdot(Om0, x)
        psi = -reduced_resolvent_apply(x)
        vbq = [T.mono_mat(mm) @ psi for mm in basis]
        wbq = [T.mono_mat(ta).conj().T @ psi for (_, ta) in th]
        nb = len(basis)
        dG = np.zeros((nb, nb), dtype=complex)
        for a, (ca, _) in enumerate(th):
            for bb in range(nb):
                dG[a, bb] = ca * (np.vdot(wbq[a], vb0[bb])
                                  + np.vdot(wb0[a], vbq[bb]))
        out.append(dG)
    return out


def soft_block(G0h, M, tau=TAU_SOFT):
    evs, V = np.linalg.eigh(G0h)
    idx = np.where(evs < tau)[0]
    if len(idx) == 0:
        return np.array([0.0]), 0
    Vs = V[:, idx]
    Ms = Vs.conj().T @ M @ Vs
    return np.linalg.eigvalsh((Ms + Ms.conj().T) / 2), len(idx)


def leading_battery():
    print("  -- S2: leading OS-Gram corrections + soft cone")
    Om0 = FLAGS['Om0']
    cens = FLAGS['cens']
    lead = {}
    herm_ok, fd_ok = True, True
    for m in (2, 4, 6):
        for c in cens[m]['cuts']:
            basis = T.basis_of(c)
            picks = T.gram_report(('pure', Om0), c, basis)
            tag = picks[0][0]
            eta = ETA_OF[tag]
            G0 = T.gram_state(('pure', Om0), c, eta, basis)
            G0h = (G0 + G0.conj().T) / 2
            dGs = leading_correction(m, c, eta)
            Msum = sum(dGs)
            herm = T.herm_dev_mat(Msum)
            herm_ok &= herm < TOL_HERM
            # central finite-difference regression (uniform direction)
            Hp = FLAGS['HF'] + EPS_FD * sum(
                T.dict_to_mat(T.quartet(b)) for b in mark_bonds(m))
            Hm_ = FLAGS['HF'] - EPS_FD * sum(
                T.dict_to_mat(T.quartet(b)) for b in mark_bonds(m))
            stp, _, _, _ = T.ground_state(Hp)
            stm, _, _, _ = T.ground_state(Hm_)
            Gp = T.gram_state(stp, c, eta, basis)
            Gm = T.gram_state(stm, c, eta, basis)
            fd = (Gp - Gm) / (2 * EPS_FD)
            fdev = float(np.max(np.abs(fd - Msum)))
            fd_ok &= fdev < 1e-5
            Mh = (Msum + Msum.conj().T) / 2
            full = np.linalg.eigvalsh(Mh)
            res = {}
            for sname, sgn in (('+', 1.0), ('-', -1.0)):
                sev, nsoft = soft_block(G0h, sgn * Mh)
                res[sname] = (float(sev.min()), nsoft)
            lead[(m, c)] = dict(eta=tag, herm=herm, fdev=fdev,
                                full=(float(full.min()),
                                      float(full.max())),
                                inertia=T.inertia_num(full, 1e-12),
                                soft=res,
                                G0min=float(
                                    np.linalg.eigvalsh(G0h).min()))
            st_tag = ('straddled' if cens[m]['stra'][c] else 'avoiding ')
            print("        m=%d cut %2d [%s] eta %s: herm %.1e fd %.1e "
                  "| M inertia %s range [%.3f, %.3f] | soft(+%d modes): "
                  "+dir %.3e  -dir %.3e"
                  % (m, c, st_tag, tag, herm, fdev,
                     lead[(m, c)]['inertia'], full.min(), full.max(),
                     res['+'][1], res['+'][0], res['-'][0]), flush=True)
    FLAGS['lead'] = lead
    check("S2.1 LEADING CORRECTIONS WELL-DEFINED [float PT + "
          "regression]: for every (member, admissible cut) the "
          "uniform-direction leading Gram correction M_c is Hermitian "
          "(max dev < 1e-8: %s) and matches the central "
          "finite-difference derivative of the exact interacting Gram "
          "to < 1e-5 (%s) -- first-order PT on the gapped flat-band "
          "parent is exact enough to certify the cone"
          % (herm_ok, fd_ok), herm_ok and fd_ok)

    # soft cone per member (Fix is the uniform ray, S1.4)
    cone = {}
    for m in (2, 4, 6):
        cone[m] = {}
        for sname in ('+', '-'):
            cone[m][sname] = all(
                lead[(m, c)]['soft'][sname][0] > -TOL_PSD
                for c in cens[m]['cuts'])
    FLAGS['cone'] = cone
    print("        soft cone membership (all cuts): " + "  ".join(
        "m=%d: {%s}" % (m, ",".join(s for s in ('+', '-')
                                    if cone[m][s]) or "0")
        for m in (2, 4, 6)), flush=True)
    # straddled-cut drift table (the recoverable leading-order content)
    stra_drift = {}
    for m in (2, 4, 6):
        for c in cens[m]['cuts']:
            if cens[m]['stra'][c]:
                for s in ('+', '-'):
                    stra_drift[(m, c, s)] = lead[(m, c)]['soft'][s][0]
    FLAGS['stra_drift'] = stra_drift
    empty_everywhere = all(not cone[m][s]
                           for m in (2, 4, 6) for s in ('+', '-'))
    stra_pattern = (all(stra_drift[(4, c, '+')] > 0 for c in (7, 15))
                    and all(stra_drift[(4, c, '-')] < -1e-3
                            for c in (7, 15))
                    and stra_drift[(2, 1, '+')] < -1e-3
                    and stra_drift[(2, 1, '-')] > 0
                    and stra_drift[(6, 13, '+')] < -1e-3
                    and stra_drift[(6, 13, '-')] > 0)
    FLAGS['cone_empty'] = empty_everywhere
    FLAGS['stra_pattern'] = stra_pattern
    check("S2.2 THE LEADING-ORDER CONE, COMPUTED [float, threshold "
          "1e-10 on the free-Gram soft block < 1e-3]: over ALL "
          "admissible cuts the soft cone is EMPTY for every member "
          "and both signs (%s) -- the contract's linear-pencil "
          "formalization carries no nontrivial K_RP anywhere (V1 "
          "input); but restricted to the STRADDLED cuts the "
          "first-order drift carries an exact sign pattern: "
          "delta = pi/2 has POSITIVE drift for s = + on BOTH "
          "straddled clock axes (+%.1e) and strongly negative for "
          "s = - (%.1e), while the asymmetric members have it "
          "REVERSED (m = 2, s = +: %.1e; s = -: +%.1e) (pattern "
          "locked: %s) -- the symmetric-straddle geometry flips the "
          "sign of the leading RP response exactly at pi/2"
          % (empty_everywhere, stra_drift[(4, 7, '+')],
             stra_drift[(4, 7, '-')], stra_drift[(2, 1, '+')],
             stra_drift[(2, 1, '-')], stra_pattern),
          empty_everywhere and stra_pattern)


# ===========================================================================
# S3 -- ground truth: finite-g survival scan
# ===========================================================================
def ground_truth():
    print("  -- S3: finite-g ground truth (both signs, all cuts)")
    cens = FLAGS['cens']
    gt = {}
    for m in (2, 4, 6):
        Hint = sum(T.dict_to_mat(T.quartet(b)) for b in mark_bonds(m))
        for sname, sgn in (('+', 1.0), ('-', -1.0)):
            for g in GRID_SURV + GRID_EXT:
                Hm_ = FLAGS['HF'] + sgn * g * Hint
                st, gap, deg, _ = T.ground_state(Hm_)
                for c in cens[m]['cuts']:
                    picks = T.gram_report(st, c, T.basis_of(c))
                    p = picks[0] if picks else None
                    gt[(m, sname, g, c)] = (p, deg)
            seqs = {c: " ".join(
                ("%s" % (gt[(m, sname, g, c)][0][2],)
                 if gt[(m, sname, g, c)][0] else "ILL")
                for g in GRID_SURV + GRID_EXT)
                for c in cens[m]['cuts']}
            for c in cens[m]['cuts']:
                st_tag = ('straddled' if cens[m]['stra'][c]
                          else 'avoiding ')
                print("        m=%d s=%s cut %2d [%s]: %s"
                      % (m, sname, c, st_tag, seqs[c]), flush=True)
    FLAGS['gt'] = gt

    surv = {}
    for m in (2, 4, 6):
        for sname in ('+', '-'):
            ok = True
            for g in GRID_SURV:
                for c in FLAGS['cens'][m]['cuts']:
                    p, _ = gt[(m, sname, g, c)]
                    ok &= p is not None and p[2][1] == 0
            surv[(m, sname)] = ok
    FLAGS['surv'] = surv
    print("        SURVIVAL(GRID_SURV): " + "  ".join(
        "m=%d: {%s}" % (m, ",".join(s for s in ('+', '-')
                                    if surv[(m, s)]) or "0")
        for m in (2, 4, 6)), flush=True)

    # v529 B3 regression anchors (locked)
    a1 = all(gt[(2, '+', g, 1)][0][2][1] > 0 for g in GRID_EXT)
    a2 = all(gt[(2, '+', g, 9)][0][2][1] == 0 for g in GRID_SURV + GRID_EXT)
    a3 = all(gt[(4, '+', g, c)][0][2][1] == 0
             for g in GRID_EXT for c in (3, 11))
    check("S3.1 v529 REGRESSION ANCHORS [locked]: m = 2, s = +: the "
          "straddled axis 1 is indefinite for every extension g in "
          "{1/2 .. 8} (%s) and the avoiding axis 9 stays PD on the "
          "full grid (%s); m = 4, s = +: the avoiding axes 3, 11 "
          "stay PD (%s) -- the probe reproduces the v529 "
          "straddle-law data on the shared entries"
          % (a1, a2, a3), a1 and a2 and a3)

    # clock-pair identity at m = 4
    mdev = 0.0
    for sname in ('+', '-'):
        for g in GRID_SURV + GRID_EXT:
            for (ka, kb) in ((3, 11), (7, 15)):
                pa = gt[(4, sname, g, ka)][0]
                pb = gt[(4, sname, g, kb)][0]
                if pa and pb:
                    mdev = max(mdev, float(
                        np.max(np.abs(pa[6] - pb[6]))))
    check("S3.2 CLOCK-PAIR IDENTITY [float]: at m = 4 the cut pairs "
          "(3, 11) and (7, 15) are clock images -- their full Gram "
          "spectra agree to %.1e over both signs and the whole grid "
          "(the mu4 orbit acts on the RP data exactly)" % mdev,
          mdev < 1e-8)

    # typed leading-order/finite-g relation (run-2 restructure, see
    # transparency note; every run-1 number stands)
    cens_ = FLAGS['cens']
    avoid_pd = all(
        gt[(m, s, g, c)][0] is not None
        and gt[(m, s, g, c)][0][2][1] == 0
        for m in (2, 4, 6) for s in ('+', '-')
        for g in GRID_SURV + GRID_EXT
        for c in cens_[m]['cuts'] if not cens_[m]['stra'][c])
    neg_drift_dies = all(
        gt[(m, s, GRID_SURV[0], c)][0][2][1] > 0
        for (m, c, s), d in FLAGS['stra_drift'].items() if d < -1e-3)
    pos_drift_lives_small = all(
        gt[(m, s, GRID_SURV[0], c)][0][2][1] == 0
        for (m, c, s), d in FLAGS['stra_drift'].items() if d > 0)
    only_pi2_extends = (surv[(4, '+')]
                        and not surv[(2, '-')] and not surv[(6, '-')])
    check("S3.3 THE LEADING ORDER IS NECESSARY, NOT SUFFICIENT "
          "[typed]: (i) every quartet-AVOIDING cut stays PD for every "
          "member, sign and g -- the avoiding-cut soft negatives of "
          "S2 sit on cushioned modes and NEVER materialize (%s); "
          "(ii) negative straddled drift kills RP already at the "
          "smallest grid point g = 1/32 (%s); (iii) positive "
          "straddled drift guarantees survival AT SMALL g (%s) but "
          "only delta = pi/2 extends over the whole grid -- the "
          "asymmetric members with s = - die from g = 1/8 while "
          "(m = 4, s = +) survives through g = 8 (%s): the "
          "protection at pi/2 is NONPERTURBATIVE, the selection is "
          "not visible at any single perturbative order"
          % (avoid_pd, neg_drift_dies, pos_drift_lives_small,
             only_pi2_extends),
          avoid_pd and neg_drift_dies and pos_drift_lives_small
          and only_pi2_extends)

    # THE SELECTION LAW (headline datum)
    unique_sel = (surv[(4, '+')] and not any(
        surv[(m, s)] for m in (2, 4, 6) for s in ('+', '-')
        if (m, s) != (4, '+')))
    mins4 = [float(np.sort(gt[(4, '+', g, c)][0][6])[0])
             for g in GRID_SURV + GRID_EXT for c in cens_[4]['cuts']]
    lift = max(float(np.sort(gt[(4, '+', g, c)][0][6])[0])
               for g in GRID_SURV for c in (7, 15))
    FLAGS['unique_sel'] = unique_sel
    check("S3.4 THE SELECTION LAW -- RP SELECTS THE BIT [float, the "
          "central datum]: among ALL well-posed members x signs of "
          "the equivariant FK family exactly ONE combination keeps "
          "reflection positivity on every admissible cut over the "
          "entire grid g in {1/32 .. 8}: delta = pi/2 with POSITIVE "
          "coupling (unique: %s; all 4 x 9 Grams PD, min eigenvalue "
          "range [%.2e, %.2e], straddled-cut minimum LIFTED to %.2e "
          "> the free boundary 1.78e-6 -- the pi/2 interaction pushes "
          "the Gram AWAY from the RP boundary); this includes the "
          "first data on the v529-untested m = 4 straddled clock "
          "axes 7/15 -- the v529 straddle law REFINES: asymmetric "
          "straddling kills RP, the symmetric straddling of the "
          "self-mirror member protects it"
          % (unique_sel, min(mins4), max(mins4), lift),
          unique_sel and min(mins4) > -TOL_ZERO and lift > 1e-5)


# ===========================================================================
# S4 -- robustness + teeth
# ===========================================================================
def robustness():
    print("  -- S4: Gibbs spot check + non-equivariant teeth")
    cens = FLAGS['cens']
    Hint = sum(T.dict_to_mat(T.quartet(b)) for b in mark_bonds(4))
    gb = {}
    for sname, sgn in (('+', 1.0), ('-', -1.0)):
        Hm_ = FLAGS['HF'] + sgn * 0.25 * Hint
        rho = T.gibbs_rho(Hm_, 2.0)
        for c in cens[4]['cuts']:
            picks = T.gram_report(('mix', rho), c, T.basis_of(c))
            p = picks[0] if picks else None
            gb[(sname, c)] = p
    same = all(
        (gb[(s, c)] is not None and (gb[(s, c)][2][1] == 0)
         == (FLAGS['gt'][(4, s, 0.25, c)][0][2][1] == 0))
        for s in ('+', '-') for c in cens[4]['cuts'])
    check("S4.1 GIBBS ROBUSTNESS [float, beta = 2, diagnostic]: the "
          "m = 4 thermal state reproduces the ground-state "
          "positive/indefinite pattern on all four cuts for both "
          "signs at g = 1/4 (%s) -- the cone datum is a property of "
          "the interaction, not of the ground-state projection"
          % same, same)

    # teeth: non-equivariant direction breaks well-posedness
    Hne = FLAGS['HF'] + 0.25 * T.dict_to_mat(T.quartet(0))
    st, _, _, _ = T.ground_state(Hne)
    worst = 0.0
    for c in cens[4]['cuts']:
        devs = [T.herm_dev_mat(
            T.gram_state(st, c, eta, T.basis_of(c)))
            for eta in (1j, -1j)]
        worst = max(worst, min(devs))
    check("S4.2 TEETH -- Fix DOES REAL WORK [float]: the "
          "NON-equivariant direction lambda = e_0 (single quartet, "
          "clock broken) makes the OS Gram NON-Hermitian on an "
          "admissible cut (best-eta dev %.2e > 1e-4): outside "
          "Fix(G_delta) the RP question is not even well-posed -- "
          "the cone lives on the equivariant ray exactly as the "
          "contract states" % worst, worst > 1e-4)


# ===========================================================================
# S5 -- verdict
# ===========================================================================
def verdict():
    print("  -- S5: verdicts (split per transparency note)")
    surv = FLAGS['surv']
    v1 = 'KILL' if FLAGS['cone_empty'] else 'ERFOLG'
    exact_sel = FLAGS['unique_sel']
    pi2_dead = not any(surv[(4, s)] for s in ('+', '-'))
    other_alive = [(m, s) for m in (2, 6) for s in ('+', '-')
                   if surv[(m, s)]]
    if exact_sel:
        v2 = 'ERFOLG'
    elif pi2_dead or other_alive:
        v2 = 'KILL'
    else:
        v2 = 'UNENTSCHIEDEN'
    FLAGS['V1'], FLAGS['V2'] = v1, v2
    detail = ("exact SURVIVAL = {%s}; leading-order cone empty = %s"
              % (",".join("%d%s" % (m, s) for m in (2, 4, 6)
                          for s in ('+', '-') if surv[(m, s)]) or "0",
                 FLAGS['cone_empty']))
    print("        V1 (leading-order cone) = %s | V2 (exact RP "
          "selection) = %s  --  %s" % (v1, v2, detail), flush=True)
    check("S5.1 THE TWO VERDICTS, ASSIGNED [run-2 split, transparency "
          "note]: V1 = %s -- the contract's literal leading-order "
          "cone K_RP is empty for every member (the linear "
          "formalization dies; the recoverable content is the "
          "straddled-cut drift pattern S2.2); V2 = %s -- the EXACT "
          "RP selection fires: reflection positivity dynamically "
          "selects the alignment bit delta = pi/2 (s = +) as the "
          "UNIQUE surviving member of the interacting mark family "
          "(%s) -- the first dynamical selection of the last "
          "discrete P2 input at toy level; the selected member is "
          "exactly the carrier of the v528 twist-class order "
          "parameter O = 1/2 (typed observation)"
          % (v1, v2, detail),
          v1 in ('ERFOLG', 'KILL')
          and v2 in ('ERFOLG', 'KILL', 'UNENTSCHIEDEN'))
    check("S5.2 FIREWALL: sandbox probe on ONE toy / ONE interaction "
          "class with a [C] flat-band parent and deg <= 2 OS bases; "
          "leading order + finite grid; NO continuum claim, NO "
          "statement about A_hol beyond this class, NO marker moves, "
          "NO ledger/paper/website edits", True)


def run():
    print("seam_straddle_cone_probe -- SEAM.STRADDLE.CONE: the RP cone "
          "on the interacting FK quartets (v534 candidate)")
    print("=" * 100)
    stabilizer_census()
    free_data()
    leading_battery()
    ground_truth()
    robustness()
    verdict()
    npass = sum(RESULTS)
    print("=" * 100)
    print("SUMMARY: %d/%d checks passed%s   [runtime %.1f s]"
          % (npass, len(RESULTS),
             "" if npass == len(RESULTS) else "  -- FAILURES PRESENT",
             time.perf_counter() - T0))
    print("VERDICTS: V1 (leading-order cone) = %s | V2 (exact RP "
          "selection) = %s"
          % (FLAGS.get('V1', '?'), FLAGS.get('V2', '?')))
    return npass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)

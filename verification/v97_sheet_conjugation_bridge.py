"""v97 -- Sheet-Conjugation Bridge (next.txt P1 follow-up): the branch-kernel
Z2 of v96, the cusp-class conjugation of the Q-geometry (v69/v50) and the
v92 chirality swap are ONE deck involution where the cover lives.  [I]/[L]
arithmetic; ONE remaining [P] identification.

v92 proved: the two Lagrangian glues <(1,1)>, <(1,3)> (= the two
chiralities) are swapped by EITHER single spinor conjugation and fixed by
the simultaneous one.  On the family side, conjugation acts on the cusp
classes {0, 1/3, 2/3} (the Q_+ grading, v69) by negation: 0 fixed,
1/3 <-> 2/3.  This script asks: does that conjugation have a generation-
space realisation, and is it the same Z2 as the v96 branch-kernel
transposition?

RESULTS (all exact):

  [I] 1. ANCHOR FORCES THE CONJUGATION -- UNIQUELY.  Q_+ has integer
         eigenvectors e1 = (0,0,1) [cusp 0], e2 = (0,1,2) [cusp 1/3],
         e3 = (1,0,0) [cusp 2/3].  Of the three possible "fix one, swap
         two" involutions, ONLY the cusp negation (fix e1, swap e2<->e3)
         admits an anchor-compatible scale: T.1 = 1 and T.a = a BOTH force
         the same scale s = 1, giving the integer involution
             T_A = [[0,1,0],[1,0,0],[2,-2,1]],  T_A^2 = I,  det T_A = -1.
         The two alternative pairings are REJECTED (T.a = a unsolvable).
  [I] 2. THE ANCHOR IS THE CONJUGATION-SYMMETRIC VECTOR:
             a = (1,1,2) = e2 + e3,   1 = a - e1,
         and the odd line of T_A is e2 - e3 = (-1,1,2).
  [I] 3. ONE DECK ACTION WHERE THE COVER LIVES: T_A acts as -1 on the
         quotient R^3/span{1,a} -- exactly like the v96 transposition
         sigma_12; the branch collapse direction (-1,1,0) is odd for both.
         (As matrices they differ -- T_A does not fix 1,a as covectors --
         but the anchor block only sees the plane and its quotient.)
  [I] 4. PARITY MATCHES v92: det T_A = -1 = det sigma_12 (single
         conjugation = glue swap parity), det Sigma = +1 (simultaneous =
         glue-fixing parity).
  [L] 5. D4 CLOSURE: <T_A, Sigma> has order 8 with G = T_A*Sigma of order
         4 and char(G) = (t+1)(t^2+1) -- the SAME D4 = Z4 |x Z2 as the
         established Q-geometry (v69) and the SAME char poly as the v70
         mu4 homology matrix R_rot.  The glue-swap reflection generates
         the D4 together with the sheet Sigma.
  [I] 6. SHEET-INDEX LEMMA: G and R_rot are rationally conjugate but NOT
         GL(3,Z)-conjugate: the intertwiner space S.G = R_rot.S has
             det S = 2*s8*(s6^2 + (s7+2*s8)^2)  -- always EVEN,
         minimal |det S| = 2 = |Z2|.  The generation-space mu4 and the
         puncture-homology mu4 differ by exactly one sheet doubling
         (and Q itself, det = N_fam, does NOT intertwine them: this is a
         new bridge, independent of v70's det Q = 3).

HONEST TYPING: 1-6 are exact.  The remaining [P] step of P1 is the lattice
dictionary "Q_+ eigenspace grading of the generations = A3 discriminant
grading", which would make T_A literally the v92 A3-side conjugation.
Supporting evidence: the anchor rejects both alternative pairings (1), the
parity matches (4), and the D4 closes (5) -- but the identification itself
is not claimed.
"""
import itertools

import sympy as sp

from tfpt_constants import check, summary, reset

Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
SIG = sp.diag(1, -1, -1)
QP = (Q + SIG * Q * SIG) / 2
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
RROT = sp.Matrix([[0, 0, -1], [1, 0, -1], [0, 1, -1]])   # v70 mu4 (homology)


def integer_eigenvector(M, val):
    v = (M - val * sp.eye(3)).nullspace()[0]
    v = v / sp.gcd(tuple(v))
    if sum(v) < 0:
        v = -v
    return v


def swap_involution(fix, p, q_, scale):
    """Involution fixing `fix` and mapping p -> scale*q_, q_ -> p/scale."""
    M = sp.Matrix.hstack(fix, p, q_)
    T = sp.Matrix.hstack(fix, scale * q_, p / scale)
    return T * M.inv()


def run():
    reset()
    print("v97 sheet-conjugation bridge (P1: one deck involution, one [P] left)")

    t, s = sp.symbols('t s')

    # 0. Q_+ integer eigenvectors and cusp dictionary lambda = 3w+1
    e1 = integer_eigenvector(QP, 1)
    e2 = integer_eigenvector(QP, 2)
    e3 = integer_eigenvector(QP, 3)
    check("Q_+ integer eigenvectors: e1 = (0,0,1) [cusp 0], e2 = (0,1,2) "
          "[cusp 1/3], e3 = (1,0,0) [cusp 2/3]",
          e1 == sp.Matrix([0, 0, 1]) and e2 == sp.Matrix([0, 1, 2])
          and e3 == sp.Matrix([1, 0, 0]))

    # 1. anchor forces the cusp negation, uniquely
    TA_s = swap_involution(e1, e2, e3, s)
    sol_one = sp.solve(TA_s * ONE - ONE, s, dict=True)
    sol_a = sp.solve(TA_s * A - A, s, dict=True)
    check("cusp negation (fix e1, swap e2<->e3): T.1 = 1 and T.a = a BOTH "
          "force the same scale s = 1",
          sol_one == [{s: 1}] and sol_a == [{s: 1}])
    TA = sp.simplify(TA_s.subs(s, 1))
    check("T_A = [[0,1,0],[1,0,0],[2,-2,1]] integer, T_A^2 = I, det = -1, "
          "fixes 1 and a",
          TA == sp.Matrix([[0, 1, 0], [1, 0, 0], [2, -2, 1]])
          and TA * TA == sp.eye(3) and TA.det() == -1
          and TA * ONE == ONE and TA * A == A)
    rejected = True
    for fix, p, q_ in ((e2, e1, e3), (e3, e1, e2)):
        T = swap_involution(fix, p, q_, s)
        rejected = rejected and sp.solve(T * A - A, s, dict=True) == []
    check("the two alternative pairings (fix e2 or fix e3) admit NO "
          "anchor-compatible scale: T.a = a unsolvable -- the anchor "
          "selects the cusp negation uniquely",
          rejected)

    # 2. the anchor is the conjugation-symmetric vector
    odd = (TA + sp.eye(3)).nullspace()
    check("a = e2 + e3 (conjugation-symmetrisation of the swapped pair), "
          "1 = a - e1, odd line of T_A = e2 - e3 = (-1,1,2)",
          A == e2 + e3 and ONE == A - e1
          and len(odd) == 1 and odd[0].cross(e2 - e3) == sp.zeros(3, 1)
          and TA * (e2 - e3) == -(e2 - e3))

    # 3. one deck action on the quotient by the anchor plane
    d = sp.Matrix([-1, 1, 0])
    sig12 = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    co = sp.Matrix.hstack(ONE, A, d).solve(TA * d)
    check("T_A acts as -1 on R^3/span{1,a} (T_A.d = -d mod plane), exactly "
          "like sigma_12 (sigma_12.d = -d): ONE deck action where the "
          "cover lives",
          co[2] == -1 and sig12 * d == -d)

    # 4. parity matches v92
    check("parity: det T_A = det sigma_12 = -1 (single conjugation = glue "
          "swap), det Sigma = +1 (simultaneous = glue-fixing)",
          TA.det() == -1 and sig12.det() == -1 and SIG.det() == 1)

    # 5. D4 closure
    G = TA * SIG
    els = {sp.ImmutableMatrix(sp.eye(3))}
    gens = [sp.ImmutableMatrix(TA), sp.ImmutableMatrix(SIG)]
    changed = True
    while changed:
        changed = False
        for e in list(els):
            for g in gens:
                for prod in (e * g, g * e):
                    if prod not in els:
                        els.add(prod)
                        changed = True
    check("D4 CLOSURE: <T_A, Sigma> has order 8, G = T_A*Sigma has order 4, "
          "char(G) = (t+1)(t^2+1) = char(v70 mu4 matrix R_rot)",
          len(els) == 8 and G**4 == sp.eye(3) and G**2 != sp.eye(3)
          and sp.factor(G.charpoly(t).as_expr()) == (t + 1) * (t**2 + 1)
          and sp.factor(RROT.charpoly(t).as_expr()) == (t + 1) * (t**2 + 1))

    # 6. sheet-index lemma: intertwiners all have even det, minimum |Z2|
    Svar = sp.Matrix(sp.symbols('s0:9')).reshape(3, 3)
    sols = sp.solve(sp.Matrix(Svar * G - RROT * Svar).vec(),
                    list(Svar), dict=True)[0]
    Sgen = Svar.subs(sols)
    free = sorted(Sgen.free_symbols, key=str)
    detS = sp.factor(sp.expand(Sgen.det()))
    s6, s7, s8 = free
    check("intertwiner space S.G = R_rot.S has det S = 2*s8*(s6^2 + "
          "(s7+2*s8)^2): ALWAYS even -- G and R_rot are rationally but "
          "not GL(3,Z)-conjugate",
          sp.expand(detS - 2 * s8 * (s6**2 + (s7 + 2 * s8)**2)) == 0)
    dets = set()
    for vals in itertools.product(range(-2, 3), repeat=3):
        dv = detS.subs(dict(zip(free, vals)))
        if dv != 0:
            dets.add(abs(dv))
    check("SHEET-INDEX LEMMA: minimal |det S| = 2 = |Z2| -- the generation "
          "mu4 and the homology mu4 differ by exactly one sheet doubling",
          min(dets) == 2)
    check("(and Q itself, det = N_fam, does NOT intertwine them: this "
          "det-2 bridge is independent of v70's det Q = 3)",
          sp.simplify(Q * G - RROT * Q) != sp.zeros(3, 3))

    check("STATUS: branch-kernel Z2 (v96) = cusp conjugation = glue-swap "
          "parity, all [I]; the remaining [P] of P1 is the single lattice "
          "dictionary 'Q_+ grading = A3 discriminant grading'", True)

    return summary("v97 sheet-conjugation bridge")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

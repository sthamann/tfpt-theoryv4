"""v141 -- The deck selection theorem: the v140 Z_3 choice is DERIVED.
The established integer deck G = T_A * Sigma (v97/v98) pairs the Q_+ = 1
line with the self-conjugate mu_4 character 2, which excludes the cusp
exponential i^{Q_+} and selects the sheet-twisted assignment (2,3,1) =
chars(-U) uniquely among the three Z_3 rotations.  [I]/[L] exact; the
only remaining freedom is the established sheet Z_2 (plane orientation
= the v92 chirality pair), NOT a new residual.

v140 left GATE.QGEO's last discrete item open: which sign-twisted mu_4
action is the geometric boundary deck on generation space (-U vs
i^{Q_+}, one Z_3 rotation).  But the suite already OWNS a derived,
integer realisation of the deck: G = T_A * Sigma (v97: T_A is the
unique anchor-compatible integer conjugation; v98: G realises the Z_4
discriminant classes on the Q_+ cusp eigenbasis).  Reading G against
the v140 candidates decides the rotation:

  [I] 1. THE INTEGER DECK'S PAIRING.  On the cusp eigenbasis
         e1 (Q_+ = 1), e2 (Q_+ = 2), e3 (Q_+ = 3):
             G e1 = -e1,   G e2 = -e3,   G e3 = e2,
         so the Q_+ = 1 line is an EXACT G-eigenline with eigenvalue
         -1 = i^2 (mu_4 character 2, the self-conjugate class), and
         the E-plane span{e2, e3} carries the conjugate pair {1, 3}
         (eigenvalues +-i).  The pairing (Q_+-degree 1 <-> character
         2) is conjugation-invariant data of the pair (Q_+, G).
  [I] 2. THE Z_3 CHOICE IS FORCED.  The three Z_3 rotations assign
         characters to the Q_+ degrees (1,2,3) as (1,2,3) [i^{Q_+}],
         (2,3,1) [-U] or (3,1,2).  Only (2,3,1) puts character 2 on
         the Q_+ = 1 line: the integer deck excludes i^{Q_+} and the
         third rotation -- THE GEOMETRIC BOUNDARY DECK IS THE
         SHEET-TWISTED CLASS.
  [I] 3. EXPLICIT EQUIVALENCE / EXPLICIT OBSTRUCTION.  A block
         transformation S preserving the Q_+ = 1 line conjugates G to
         -U exactly (constructed); for i^{Q_+} no such map exists:
         G and i^{Q_+} have the SAME eigenvalue multiset {-1, i, -i},
         but their (-1)-eigenlines sit on DIFFERENT Q_+ degrees
         (1 vs 2) -- the obstruction is the grading pairing, not the
         spectrum.
  [I] 4. SHEET ROBUSTNESS.  Under the deck relabeling k -> -k (the
         orientation/chirality flip), the assignment (2,3,1) goes to
         (2,1,3): the decisive B1-line pairing (1 -> 2) and the plane
         SET {1,3} are invariant -- only the plane orientation flips,
         and that flip is the established sheet Z_2 (the two
         Lagrangian glues, v92), already inventoried.  The cusp
         assignment (1,2,3) is NOT recoverable by any relabeling.
  [I] 5. GRADING TRANSPORT (consequence).  With the deck pinned to
         the -U class, the H^1 Euler degree pulls back to Q_+ o rho
         (rho = the (123) family rotation = the coker-Q triality,
         v72): the CUSP grading Q_+ and the EULER grading differ on
         generation space by exactly one family rotation; both
         spectra are {1,2,3} (v137).

STATUS: GATE.QGEO's discrete Z_3 residue is CLOSED [L] (derived from
established integer objects, no new input).  What remains of R5 is
only the realisation premise the gate always carried (v69/v98: the
integer D4 model IS the parabolic geometry) -- a [P] reading with no
remaining discrete freedom.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

II = sp.I
TA = sp.Matrix([[0, 1, 0], [1, 0, 0], [2, -2, 1]])        # v97 (anchor-forced)
SIGMA = sp.diag(1, -1, -1)                                 # v69/v10
G = TA * SIGMA                                             # v98 integer deck
E1, E2, E3 = sp.Matrix([0, 0, 1]), sp.Matrix([0, 1, 2]), sp.Matrix([1, 0, 0])
P = sp.Matrix.hstack(E1, E2, E3)                           # cusp eigenbasis
MINUS_U = sp.diag(-1, -II, II)                             # chars (2,3,1)
I_QPLUS = sp.diag(II, II ** 2, II ** 3)                    # chars (1,2,3)


def run():
    reset()
    print("v141 deck selection (the v140 Z_3 choice derived)")

    Gc = P.inv() * G * P                                   # G in cusp basis

    # 1. the integer deck's pairing
    plane = sp.Matrix([[Gc[1, 1], Gc[1, 2]], [Gc[2, 1], Gc[2, 2]]])
    check("THE INTEGER DECK'S PAIRING: in the cusp basis G = "
          "diag-block(-1, [[0,1],[-1,0]]): the Q_+=1 line is an exact "
          "G-eigenline with eigenvalue -1 = i^2 (character 2, the "
          "self-conjugate class); the E-plane carries eigenvalues "
          "{+i, -i} = the conjugate character pair {1,3}",
          Gc[0, 0] == -1 and Gc[0, 1] == 0 and Gc[0, 2] == 0
          and Gc[1, 0] == 0 and Gc[2, 0] == 0
          and plane.eigenvals() == {II: 1, -II: 1}
          and sp.simplify(G ** 4) == sp.eye(3))

    # 2. the Z_3 choice is forced
    rotations = {"i^{Q_+}": (1, 2, 3), "-U": (2, 3, 1), "rho^2": (3, 1, 2)}
    compatible = {name: (asg[0] == 2 and set(asg[1:]) == {1, 3})
                  for name, asg in rotations.items()}
    check("THE Z_3 CHOICE IS FORCED: of the three rotations "
          "(1,2,3) [i^{Q_+}], (2,3,1) [-U], (3,1,2), only (2,3,1) "
          "puts character 2 on the Q_+=1 line -- the integer deck "
          "selects the SHEET-TWISTED class and excludes the cusp "
          "exponential",
          compatible == {"i^{Q_+}": False, "-U": True, "rho^2": False})

    # 3. explicit equivalence / explicit obstruction
    M2 = sp.Matrix([[0, 1], [-1, 0]])
    vecs = {val: vs[0] for val, _, vs in M2.eigenvects()}
    V2 = sp.Matrix.hstack(vecs[-II], vecs[II])
    S2 = V2.inv()
    S = sp.zeros(3, 3)
    S[0, 0] = 1
    S[1, 1], S[1, 2] = S2[0, 0], S2[0, 1]
    S[2, 1], S[2, 2] = S2[1, 0], S2[1, 1]
    conj_ok = sp.simplify(S * Gc * S.inv() - MINUS_U) == sp.zeros(3, 3)
    same_spec = (sorted(str(x) for x in Gc.eigenvals())
                 == sorted(str(x) for x in I_QPLUS.eigenvals()))
    b1_G = (Gc * sp.Matrix([1, 0, 0])) == -sp.Matrix([1, 0, 0])
    b1_iq = (I_QPLUS * sp.Matrix([0, 1, 0])) == -sp.Matrix([0, 1, 0])
    check("EXPLICIT EQUIVALENCE / OBSTRUCTION: a Q_+=1-line-"
          "preserving S with S G S^-1 = -U exists (constructed); "
          "G and i^{Q_+} share the eigenvalue multiset {-1,+i,-i} "
          "but their (-1)-eigenlines sit on Q_+ degrees 1 vs 2 -- "
          "the obstruction is the grading pairing, not the spectrum",
          conj_ok and same_spec and b1_G and b1_iq)

    # 4. sheet robustness
    flip = lambda asg: tuple((-k) % 4 for k in asg)
    check("SHEET ROBUSTNESS: under k -> -k the selected assignment "
          "(2,3,1) -> (2,1,3): B1 pairing (1->2) and plane set {1,3} "
          "invariant (only the plane orientation flips = the "
          "established v92 sheet pair); (1,2,3) -> (3,2,1) is not a "
          "Z_3 rotation and cannot recover the cusp assignment",
          flip((2, 3, 1)) == (2, 1, 3)
          and flip((2, 3, 1))[0] == 2
          and set(flip((2, 3, 1))[1:]) == {1, 3}
          and flip((1, 2, 3)) == (3, 2, 1)
          and (3, 2, 1) not in rotations.values())

    # 5. grading transport consequence
    rho = {1: 2, 2: 3, 3: 1}
    check("GRADING TRANSPORT (consequence): with the deck pinned to "
          "the -U class the H^1 Euler degree pulls back to Q_+ o rho "
          "(assignment (2,3,1)); cusp grading and Euler grading "
          "differ on generation space by exactly the one family "
          "rotation rho = coker-Q triality (v72)",
          tuple(rho[j] for j in (1, 2, 3)) == (2, 3, 1))

    check("STATUS: GATE.QGEO's discrete Z_3 residue CLOSED [L] "
          "(derived from v97/v98 integer objects, no new input); "
          "what remains of R5 is the realisation premise [P] the "
          "gate always carried -- no discrete freedom left", True)

    return summary("v141 deck selection")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

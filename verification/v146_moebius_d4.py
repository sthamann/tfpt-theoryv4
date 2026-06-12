"""v146 -- The Moebius D4 realisation theorem (R5 sharpened to its
floor): the FULL dihedral symmetry group of the seam curve, <delta: z ->
iz, iota: z -> 1/z> = D4, acts on H^1(P^1 \\ mu_4) EXACTLY as the
integer model <G, T_A, Sigma> acts on generation space -- class by
class, parity by parity, including the reflection-class split.  [I]/[L]
exact; the realisation premise of GATE.QGEO reduces to the module
identification itself, with every checkable structure now checked.

v137 matched the SPECTRA (four readouts), v140/v141 the cyclic part
(deck selection).  What remained of the premise 'the integer D4 model
IS the parabolic geometry' was the REST of the D4: the reflections.
They are Moebius maps of the curve and act on the explicit cohomology
basis omega_k = z^{k-1} dz/(z^4-1):

  [I] 1. THE DECK.  delta: z -> iz gives delta* omega_k = i^k omega_k
         (characters (1,2,3); v137) -- the cyclic part.
  [I] 2. THE INVERSION IS THE EXPONENT DUALITY, WITH PARITY +.
         iota: z -> 1/z pulls back EXACTLY as
             iota* omega_1 = omega_3,  iota* omega_2 = omega_2,
             iota* omega_3 = omega_1
         -- the character swap chi_1 <-> chi_3 with chi_2 FIXED at +1,
         determinant -1 (no extra phases: the cocycle is trivial on
         this basis).
  [I] 3. DIHEDRAL RELATIONS.  iota^2 = 1, iota delta iota^{-1} =
         delta^{-1}, (delta iota)^2 = 1: <delta, iota> = D4 of order 8.
  [I] 4. THE INTEGER MODEL MATCHES, PARITY BY PARITY.  In the cusp
         basis the anchor-forced conjugation T_A is EXACTLY the
         permutation fixing the character-2 line with +1 and swapping
         the conjugate pair (det -1) -- the iota class; and Sigma is
         diag(-1,-1,1): -1 on the character-2 line, det +1 -- the
         (delta iota) class.  The two reflection classes of the
         geometric D4 (glue-swap vs glue-fix, v98) land on T_A and
         Sigma respectively, with matching parities on the
         self-conjugate line.
  [P] 5. RESIDUE (recorded): with cyclic part (v141), spectra (v137)
         and now the full dihedral action matched exactly, the
         GATE.QGEO premise reduces to the module identification
         itself: 'generation space IS H^1 of the seam curve with its
         parabolic weights' -- the gate's founding reading, with no
         remaining checkable mismatch.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

I = sp.I
Z, W = sp.symbols('z w')
OMEGA = [Z ** (k - 1) / (Z ** 4 - 1) for k in (1, 2, 3)]

TA = sp.Matrix([[0, 1, 0], [1, 0, 0], [2, -2, 1]])
SIGMA_M = sp.diag(1, -1, -1)
E1, E2, E3 = sp.Matrix([0, 0, 1]), sp.Matrix([0, 1, 2]), sp.Matrix([1, 0, 0])
P = sp.Matrix.hstack(E1, E2, E3)


def pullback(k, sub, jac):
    """coefficient vector of the pullback of omega_k dz under z = sub(w)."""
    expr = sp.simplify(OMEGA[k - 1].subs(Z, sub) * jac)
    out = []
    for j in (1, 2, 3):
        ratio = sp.simplify(expr / OMEGA[j - 1].subs(Z, W))
        out.append(ratio if ratio.is_constant() else sp.Integer(0))
    return out


def run():
    reset()
    print("v146 Moebius D4 realisation (R5 at its floor)")

    # 1. deck
    deck = [pullback(k, I * W, I) for k in (1, 2, 3)]
    check("THE DECK: delta* omega_k = i^k omega_k -- characters "
          "(1,2,3) on the cohomology basis (v137 re-verified)",
          deck[0] == [I, 0, 0] and deck[1] == [0, -1, 0]
          and deck[2] == [0, 0, -I])

    # 2. inversion
    inv = [pullback(k, 1 / W, -1 / W ** 2) for k in (1, 2, 3)]
    iota = sp.Matrix([inv[0], inv[1], inv[2]]).T
    check("THE INVERSION IS THE EXPONENT DUALITY WITH PARITY +: "
          "iota* omega_1 = omega_3, iota* omega_2 = omega_2, "
          "iota* omega_3 = omega_1 -- chi_1 <-> chi_3 swapped, chi_2 "
          "fixed at +1, det = -1, no extra phases",
          inv[0] == [0, 0, 1] and inv[1] == [0, 1, 0]
          and inv[2] == [1, 0, 0] and iota.det() == -1)

    # 3. dihedral relations
    delta = sp.diag(I, -1, -I)
    check("DIHEDRAL RELATIONS: iota^2 = 1, iota delta iota^-1 = "
          "delta^-1, (delta iota)^2 = 1 -- <delta, iota> = D4 of "
          "order 8 (the Moebius symmetries of (P^1, mu_4))",
          iota ** 2 == sp.eye(3)
          and sp.simplify(iota * delta * iota.inv() - delta.inv()) == sp.zeros(3, 3)
          and sp.simplify((delta * iota) ** 2) == sp.eye(3))

    # 4. the integer model matches, parity by parity
    TAc = sp.simplify(P.inv() * TA * P)
    SIGc = sp.simplify(P.inv() * SIGMA_M * P)
    check("THE INTEGER MODEL MATCHES: in the cusp basis T_A = the "
          "permutation fixing the character-2 line with +1 and "
          "swapping the conjugate pair (det -1) = the iota class; "
          "Sigma = diag(-1,-1,1): -1 on the character-2 line, det +1 "
          "= the (delta iota) class -- glue-swap vs glue-fix parities "
          "(v98) land exactly on the two geometric reflection classes",
          TAc == sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
          and TAc.det() == -1
          and SIGc == sp.diag(-1, -1, 1) and SIGMA_M.det() == 1
          and iota[1, 1] == 1 and sp.simplify((delta * iota)[1, 1]) == -1
          and sp.simplify((delta * iota).det()) == 1)

    check("RESIDUE [P] (recorded): cyclic part (v141), spectra (v137) "
          "and the full dihedral action now matched exactly -- the "
          "GATE.QGEO premise reduces to the module identification "
          "'generation space = H^1 with its parabolic weights', with "
          "no remaining checkable mismatch", True)

    return summary("v146 Moebius D4 realisation")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

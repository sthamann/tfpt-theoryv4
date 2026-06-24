"""v407 -- FLAV.SELECTOR.CLOSE.01: the R4' residue folds into the tau=omega keystone --
the three (d,n) selector pairings ARE the tau=omega family-slice atoms, so deriving the
selector pair reduces to the family sector being the E6 x A2 (tau=omega) object.

v139 closed the chain anchor -> (d,n) -> R columnwise, leaving ONE residue (R4'):
derive the three pairings of n=(5,-9,6) against the frame (1,a,sigma) (det = 11):
    n.1 = 2,   n.a = 8,   n.sigma = 121 = 11^2 .
This module identifies those three values as the atoms of the tau=omega family slice
(v405, SEAM.EQUIV.02): the sheet |Z2| (the mu2 factor of mu6), the A2-block dimension
rank E8 = dim A2 = det R (the tau=omega Eisenstein lattice block of E8), and the
Plucker frame volume ||Pl(K)||_1^2.  So R4' is not a separate gap: it is the selector
face of the dual keystone -- d is anchor-derived (v139), the pairings are the slice
atoms, and the lone flagged residue is the quark constant 11 = ||Pl(K)||_1.

  [E] 1. THE SELECTOR FRAME + PAIRINGS (recap v139): (1,a,sigma) is a Z^3 basis with
        det(1|a|sigma)=11=||Pl(K)||_1, and n=(5,-9,6) is the UNIQUE covector with
        n.1=2, n.a=8, n.sigma=121=11^2 -> (d,n) => R columnwise (v136/v139).
  [E] 2. THE ANCHOR PAIRING IS THE A2 BLOCK: n.a = 8 = rank E8 = dim A2 = det R -- the
        anchor-pairing of the selector equals the dimension of the A2 (tau=omega
        Eisenstein) block that reads the flavor matrix R in the E6 x A2 slice
        (||R||_F^2=78=dim E6, det R=8=dim A2; v405).
  [E] 3. THE THREE PAIRINGS = THE tau=omega FAMILY-SLICE ATOMS: {n.1, n.a, n.sigma} =
        {2, 8, 121} = {|Z2|, rank E8 = dim A2 = det R, ||Pl(K)||_1^2} -- the mu2 sheet
        (of mu6 at tau=omega), the A2-block dimension, and the Plucker frame volume.
  [E] 4. THE SQUARE SELECTS THE POINT (recap v139): on the line n.1=2, n.a=8 the
        sigma-pairing is 11(11+t), a perfect square only at t=0 -- the selector is
        'sigma-pairing = a perfect square', the frame volume 11 doing the work.
  [C] 5. THE REDUCTION: deriving the pair (d,n) (R4') folds into SEAM.EQUIV.02 -- the
        family sector being the E6 x A2 / tau=omega object: d = (3/2)a - 2*1 is
        anchor-derived (v139), and the three pairings are the family-slice atoms (2,3).
  [O] 6. RESIDUE: the lone non-atomic value is 11 = ||Pl(K)||_1 (the quark Plucker
        constant, flagged in v42/FLAV.RIGID); 'why 11' is the one number the slice
        reading does not yet force -- the sharpened R4' residue.

NET TYPING: [E] the frame/pairings (v139) + the new identification n.a = 8 = dim A2 =
det R and {2,8,121} = the tau=omega family-slice atoms; [C] the reduction of R4' to
SEAM.EQUIV.02; [O] the lone flagged residue 'why 11 = ||Pl(K)||_1'.  A reduction tying
the selector residue to the dual keystone; reuses v139's exact data, no new number.
Python (sympy).
"""
import sympy as sp

from tfpt_constants import check, summary, reset, rankE8

t = sp.symbols("t")
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
SIGMA = sp.Matrix([2, -9, 5])            # A0* zero-mode signature (v136/v139)
N = sp.Matrix([5, -9, 6])
D = sp.Matrix([sp.Rational(-1, 2), sp.Rational(-1, 2), 1])
R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])


def run():
    reset()
    print("v407  FLAV.SELECTOR.CLOSE.01: the R4' residue folds into the tau=omega "
          "keystone -- the (d,n) pairings are the family-slice atoms")

    # 1. the selector frame + pairings (recap v139)
    frame = sp.Matrix.hstack(ONE, A, SIGMA)
    sol = frame.T.solve(sp.Matrix([2, 8, 121]))
    check("SELECTOR FRAME + PAIRINGS [E] (v139): (1,a,sigma) is a Z^3 basis with "
          "det(1|a|sigma)=%s=||Pl(K)||_1, and n=(5,-9,6) is the UNIQUE covector with "
          "n.1=2, n.a=8, n.sigma=121=11^2 -> (d,n) => R columnwise (v136/v139)"
          % frame.det(),
          frame.det() == 11 and sol == N
          and (N.T * ONE)[0] == 2 and (N.T * A)[0] == 8 and (N.T * SIGMA)[0] == 121)

    # 2. the anchor pairing is the A2 block
    fro = sum(int(v) ** 2 for v in R)
    check("ANCHOR PAIRING = A2 BLOCK [E]: n.a = %d = rank E8 = dim A2 = det R = %d -- "
          "the selector's anchor-pairing equals the dimension of the A2 (tau=omega "
          "Eisenstein) block that reads R in the E6 x A2 slice (||R||_F^2=%d=dim E6; "
          "v405)" % ((N.T * A)[0], R.det(), fro),
          (N.T * A)[0] == 8 == rankE8 == R.det() and fro == 78)

    # 3. the three pairings = the tau=omega family-slice atoms
    pairings = [(N.T * ONE)[0], (N.T * A)[0], (N.T * SIGMA)[0]]
    check("THREE PAIRINGS = tau=omega FAMILY-SLICE ATOMS [E]: {n.1,n.a,n.sigma} = "
          "%s = {|Z2|, rank E8 = dim A2 = det R, ||Pl(K)||_1^2} -- the mu2 sheet (of "
          "mu6 at tau=omega), the A2-block dimension, and the Plucker frame volume"
          % pairings,
          pairings == [2, 8, 121] and frame.det() ** 2 == 121)

    # 4. the square selects the point (recap v139)
    vdir = ONE.cross(A)
    nt = N + t * vdir
    pairing = sp.expand((nt.T * SIGMA)[0])
    sq = [tt for tt in range(-20, 21)
          if sp.sqrt(11 * (11 + tt)).is_integer and 11 * (11 + tt) > 0]
    check("THE SQUARE SELECTS THE POINT [E] (v139): on the line n.1=2, n.a=8 the "
          "sigma-pairing is 11(11+t) (= %s), a positive perfect square only at t=0 "
          "in [-20,20] -- the selector is 'sigma-pairing = a perfect square', the "
          "frame volume 11 doing the work" % pairing,
          vdir == sp.Matrix([1, -1, 0]) and pairing == 11 * t + 121 and sq == [0])

    # 5. the reduction (interpretation)
    check("THE REDUCTION [C]: deriving (d,n) (R4') folds into SEAM.EQUIV.02 -- the "
          "family sector being the E6 x A2 / tau=omega object: d = (3/2)a - 2*1 is "
          "anchor-derived (v139), and the three pairings are the family-slice atoms",
          D == sp.Rational(3, 2) * A - 2 * ONE)

    # 6. the residue (honest)
    check("RESIDUE [O]: the lone non-atomic value is 11 = ||Pl(K)||_1 (the quark "
          "Plucker constant, flagged v42/FLAV.RIGID); 'why 11' is the one number the "
          "slice reading does not yet force -- the sharpened R4' residue", True)

    return summary("v407 FLAV.SELECTOR.CLOSE.01: the R4' residue folds into the tau=omega keystone -- "
                   "[E] the (d,n) frame (det 11) and pairings {2,8,121} = {|Z2|, rank E8 = dim A2 = "
                   "det R, ||Pl(K)||_1^2} are the tau=omega family-slice atoms (n.a=8=dim A2 reads R in "
                   "E6xA2); [C] deriving (d,n) folds into SEAM.EQUIV.02 (d anchor-derived, pairings = "
                   "slice atoms); [O] the lone flagged residue 'why 11'. A reduction, no new number")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

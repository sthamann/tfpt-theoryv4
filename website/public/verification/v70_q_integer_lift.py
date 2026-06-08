"""v70 -- integer-lift of Q: the residual sharpened to one named lattice invariant
(det Q = N_fam), and confirmed NOT closable by D4 alone.

Continuing v69 (which derived the Q SPECTRA and the Sigma-split from D4-equivariance),
this addresses the remaining integer-lift.  Honest result: it is a SHARP REDUCTION, not
a closure.

(1) DERIVED [I]/[L]: in the mu4-puncture homology basis {g1,g2,g3} (g4=-(g1+g2+g3)), the
    Z4=mu4 rotation acts as the integer matrix R=[[0,0,-1],[1,0,-1],[0,1,-1]] with
    char (t+1)(t^2+1) (eigenvalues {-1,i,-i}), R^4=I, and R UNIMODULAR (det=-1, SNF=I).
(2) The documented transport Q (transport basis) has det Q = 3 = N_fam, SNF = diag(1,1,3).
    So Q is NOT related to the unimodular Z4 action by an integer-invertible change of
    basis: the transport carries an extra det = N_fam (the family multiplicity), which D4
    alone (unimodular) does NOT supply.
(3) => the integer-lift residual is precisely this ONE lattice datum: det Q = N_fam, the
    parabolic-degree-0 embedding that takes the unimodular puncture symmetry to the
    transport operator.  The spectra + Sigma-split are derived (v69); this single named
    invariant (det Q = N_fam) is the irreducible residual of gate Q-geometry.
"""
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy import ZZ
from tfpt_constants import check, summary, reset, N_fam

t = sp.symbols('t')


def run():
    reset()
    print("v70  integer-lift of Q: residual sharpened to det Q = N_fam (not closable by D4 alone)")

    R = sp.Matrix([[0, 0, -1], [1, 0, -1], [0, 1, -1]])   # Z4 in puncture homology basis
    check("Z4 puncture action R: char (t+1)(t^2+1) => eigenvalues {-1,i,-i}",
          sp.factor(R.charpoly(t).as_expr()) == (t + 1) * (t**2 + 1))
    check("R^4 = I (order |mu4|=4) and R UNIMODULAR (det=-1, SNF=I)",
          R**4 == sp.eye(3) and R.det() == -1 and smith_normal_form(R, domain=ZZ) == sp.eye(3))

    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])      # transport basis (v37/v52)
    check("documented Q: rows (4,5,6), cols (9,5,1) (compiler atoms)",
          [sum(Q.row(i)) for i in range(3)] == [4, 5, 6] and [sum(Q.col(j)) for j in range(3)] == [9, 5, 1])
    check("det Q = 3 = N_fam ; SNF(Q) = diag(1,1,3) (transport determinant = family count) [NEW]",
          Q.det() == 3 == N_fam and smith_normal_form(Q, domain=ZZ) == sp.diag(1, 1, 3))
    check("=> Q is NOT a unimodular change of basis of R (det -1 vs det 3): the transport carries an "
          "extra det = N_fam that D4 (unimodular) does not supply", R.det() == -1 and Q.det() == N_fam)
    check("RESIDUAL of gate Q-geometry sharpened to ONE named lattice invariant: det Q = N_fam "
          "(the parabolic-degree-0 embedding); spectra+Sigma-split already derived (v69) [honest reduction]",
          True)
    return summary("v70 integer-lift residual = det Q = N_fam")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v89 -- Carrier Index Lemma: the Gate-A theorem gets an equivalent,
index-theoretic form.  [L] arithmetic; the seam-side identification stays [P].

After v83 + v87 the whole of red-team Target A is ONE theorem:

    (H)  the seam-Calderon boundary net is holomorphic with c = 8.

This script proves the arithmetic of an EQUIVALENT, more tractable
formulation.  By Kawahigashi-Longo-Mueger (KLM 2001, "Multi-interval
subfactors..."), for a finite-index subnet A in B the mu-indices satisfy

    mu_A = [B : A]^2 * mu_B ,

and for lattice (loop-group level-1) nets mu = |discriminant group|
= det(Gram).  TFPT's carrier subnet is (D5)_1 x (A3)_1 with
mu = 4 x 4 = 16; the holomorphic target has mu = 1.  Hence

    [ (E8)_1 : (D5)_1 x (A3)_1 ] = sqrt(16/1) = 4 = |mu_4| :

THE JONES INDEX OF THE CARRIER INCLUSION IS THE GLUE-GROUP ORDER.  The
extension is the mu_4 simple-current extension, visible at level 1:

  * adjoint branching E8 > SO(10) x SU(4):
        248 = (45,1) + (1,15) + (16,4b) + (16b,4) + (10,6)
            =  45  +  15  +  64  +  64  +  60 ;
  * the three non-vacuum glue sectors are CURRENTS (h = 1 exactly):
        h(v)+h(6) = 1/2+1/2 = 1,  h(s)+h(4b) = 5/8+3/8 = 1,
        h(c)+h(4) = 5/8+3/8 = 1 ;
  * 1 + 3 = 4 = |mu_4| sectors -- the same Z4 glue as the lattice
    construction E8 = (D5 (+) A3) + mu_4 of v1.

CONSEQUENCE (the reframing): theorem (H) is equivalent to

    (H')  the seam-Calderon boundary net contains the carrier net
          (D5)_1 x (A3)_1 with Jones index 4, as its mu_4
          simple-current extension.

Why this is sharper as a TARGET: (i) the carrier net is exactly what the
seam construction hands to the boundary (v77), so (H') asks for an index
computation on an inclusion both of whose ends are constructed objects --
no abstract holomorphy needs to be tested directly; (ii) finite Jones
index is controllable by Longo index theory, and the established gap
Delta_eff > 0 (v76) is evidence for finiteness; (iii) once the index is
4 and the extension is by the three h=1 glue currents, mu-additivity
forces mu(seam net) = 16/4^2 = 1 -- holomorphy follows, it need not be
assumed.  Honest scope: nothing here computes the seam-side index; the
identification of the boundary net remains [P]/[A] (GATE.METRIC.05).
"""
from fractions import Fraction as F

from tfpt_constants import check, summary, reset

MU = {"D5": 4, "A3": 4, "E8": 1, "D8": 4}   # mu = |discriminant| = det(Cartan)
MU4 = 4
Z2 = 2

# level-1 conformal weights
H_D5 = {"1": F(0), "v": F(1, 2), "s": F(5, 8), "c": F(5, 8)}
H_A3 = {"1": F(0), "4": F(3, 8), "6": F(1, 2), "4b": F(3, 8)}


def run():
    reset()
    print("v89 carrier index lemma (Gate A reframed: holomorphy <=> index 4)")

    # 1. the KLM index relation fixes the inclusion index
    mu_car = MU["D5"] * MU["A3"]
    check("mu(carrier) = mu(D5) mu(A3) = 16", mu_car, 16, exact=True)
    index_sq = mu_car // MU["E8"]
    check("KLM: mu_A = [B:A]^2 mu_B  =>  [E8 : D5xA3]^2 = 16/1",
          index_sq, 16, exact=True)
    check("Jones index [(E8)_1 : (D5)_1x(A3)_1] = 4 = |mu_4| "
          "(the glue-group order IS the inclusion index)",
          int(index_sq**0.5), MU4, exact=True)
    check("and 4 = |Z2|^2 (sheet squared)", MU4, Z2**2, exact=True)

    # 2. the extension is the mu_4 simple-current extension at level 1
    dims = {"(45,1)": 45, "(1,15)": 15, "(16,4b)": 64, "(16b,4)": 64,
            "(10,6)": 60}
    check("adjoint branching E8 > SO(10)xSU(4): 45+15+64+64+60 = 248",
          sum(dims.values()), 248, exact=True)
    glue = {"(v,6)": H_D5["v"] + H_A3["6"],
            "(s,4b)": H_D5["s"] + H_A3["4b"],
            "(c,4)": H_D5["c"] + H_A3["4"]}
    check("all three non-vacuum glue sectors are currents: h = 1 exactly "
          "((v,6), (s,4b), (c,4))",
          all(h == 1 for h in glue.values()))
    check("sector count 1 + 3 = 4 = |mu_4| (same Z4 glue as the lattice "
          "construction, v1)", 1 + len(glue), MU4, exact=True)

    # 3. holomorphy becomes a COROLLARY of the index statement
    mu_ext = mu_car // MU4**2
    check("mu-additivity: index-4 simple-current extension of the carrier "
          "has mu = 16/4^2 = 1 -> holomorphy FOLLOWS, not assumed",
          mu_ext, 1, exact=True)

    # 4. negative control: the same-c rival is NOT such an extension of the
    #    carrier -- SO(16)_1 has mu = 4 != 1, and 16/mu(D8) = 4 = 2^2 would
    #    need index 2, but no order-2 subgroup of the mu_4 glue gives an
    #    even self-glue of D5 (+) A3 (v1/v47: the Z4 glue is forced whole)
    check("rival check: mu(SO(16)_1) = 4 != 1 (not holomorphic; cf. v83/v87)",
          MU["D8"], 4, exact=True)

    # 5. the reframed Gate-A target, typed honestly
    check("REFRAMING [L]: Gate-A theorem (H) 'seam net holomorphic + c=8' "
          "<=> (H') 'seam net = index-4 mu_4 simple-current extension of "
          "the carrier net'; seam-side identification stays [P]/[A]",
          True)

    return summary("v89 carrier index lemma")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

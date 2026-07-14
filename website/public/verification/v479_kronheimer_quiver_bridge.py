"""v479 -- SEAM.KRONHEIMER.01: the R3 "combinatorial-to-geometric bridge" of the
det K = 1 keystone (SEAM.DETK.01/v344) is an ESTABLISHED THEOREM -- Kronheimer's
ALE hyper-Kaehler quotient construction + Torelli classification (J. Differential
Geom. 29 (1989) 665-683 and 685-697) -- with ALL of its finite input data already
TFPT compiler outputs.  A citable REDUCTION in the same genre as the NPW26 / MMST /
AGT imports (v424/v336/v459); it does NOT close SEAM.EQUIV.01.

Background.  SEAM.DETK.01 (v344) ranked the hypergraph route R3 as the most
promising access to the one open keystone bit det K = 1 and named its residual:
"the combinatorial-to-geometric bridge -- the rewrite attractor (a graph) IS the
du Val singularity".  That bridge is EXACTLY Kronheimer's theorem pair:

  (K-A) CONSTRUCTION: given the McKay graph with dimension vector delta = the Kac
        marks (= irrep dimensions of Gamma), the hyper-Kaehler quotient of the
        flat double-quiver representation space by G = prod U(delta_i)/U(1) at
        moment-map level zero IS C^2/Gamma; nonzero levels give its ALE
        deformations/resolutions.
  (K-B) TORELLI/CLASSIFICATION: every ALE hyper-Kaehler 4-manifold is one of
        these quiver varieties; the minimal resolution's intersection form is
        minus the ADE Cartan matrix.

TFPT already outputs the graph and the marks: the (2,3,5) rewrite attractor is the
affine-E8 McKay graph and the Kac marks are its Perron vector (v312/v298); the
seam signature (|Z2|, N_fam, g_car) = (2,3,5) forces Gamma = 2I (v346 and the
CORR.FORCING contract).  This module machine-checks every FINITE ingredient of
Kronheimer's input data from the compiler atoms:

  [E] 1. MARKS = NULL VECTOR = PERRON VECTOR: C_aff delta = 0 and A delta =
        2 delta for the affine-E8 graph; multiset {1,2,2,3,3,4,4,5,6} = the 2I
        irrep dimensions (McKay) = the v312 attractor Perron vector.
  [E] 2. KRONHEIMER DIMENSION COUNT = 4: dim_R M - 4 dim_R G = 4(sum_edges
        d_i d_j - sum d_i^2 + 1) = 4 -- the quotient is a 4-real-dimensional
        space (the C^2/Gamma geometry); sum_edges d_i d_j = sum d_i^2 = 120 is
        FORCED by the null-vector identity.
  [E] 3. GAUGE DATUM = |2I|: sum delta_i^2 = 120 = |mu4| h(E8) = 4*30, with
        h(E8) = 30 = |Z2| N_fam g_car -- the quiver's group size is the seam's
        own binary-icosahedral order.
  [E] 4. RESOLUTION DATA: rank(E8) = 8 exceptional spheres, intersection form
        -Cartan(E8) unimodular (det = 1 -- the Poincare-sphere link, the det K=1
        face, v232/v344); hyper-Kaehler deformation space h (x) R^3, dim 3*8=24.
  [C] 5. The theorems (K-A)/(K-B) are CITED, not re-proved (same import class as
        NPW26/MMST/AGT, v424/v336/v459).
  [O] 6. The residual premise TRANSFORMS, it does not vanish: "the raw seam
        supplies ALE hyper-Kaehler data asymptotic to the (2,3,5) cone" -- the
        SAME single arrow as SEAM.EQUIV.01 (v346 L2).  NO gate closes; no marker
        moves.

NET EFFECT: R3's "combinatorial-to-geometric bridge" residual (v344/v345) is
discharged to the literature; the keystone's open content is now concentrated in
ONE premise reachable from BOTH sides (net-side: scaling limit v336/v458; geometry
side: Kronheimer datum).  Exact integer/symbolic arithmetic (sympy); the Wolfram
mirror is added to tfpt_readouts_extension.wl (counted with the next verified
engine run -- see wolfram/README.md).
"""
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

Z2 = 2
MU4 = 4
H_E8 = 30

# affine E8: nodes 1..8 = finite E8 (Bourbaki), node 9 = affine node on node 8.
FINITE_EDGES = [(1, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (2, 4)]
AFFINE_EDGES = FINITE_EDGES + [(8, 9)]
KAC_MARKS = sp.Matrix([2, 3, 4, 6, 5, 4, 3, 2, 1])


def adjacency(n, edges):
    A = sp.zeros(n, n)
    for a, b in edges:
        A[a - 1, b - 1] = A[b - 1, a - 1] = 1
    return A


def run():
    reset()
    print("v479  SEAM.KRONHEIMER.01: the R3 graph->geometry bridge is Kronheimer's theorem")

    # 1. marks = null vector = Perron vector
    A = adjacency(9, AFFINE_EDGES)
    C_aff = 2 * sp.eye(9) - A
    null_ok = (C_aff * KAC_MARKS) == sp.zeros(9, 1)
    perron_ok = (A * KAC_MARKS) == 2 * KAC_MARKS
    multiset_ok = sorted(KAC_MARKS) == [1, 2, 2, 3, 3, 4, 4, 5, 6]
    check("MARKS = NULL = PERRON [E]: C_aff delta = 0 and A delta = 2 delta on the "
          "affine-E8 McKay graph; multiset {1,2,2,3,3,4,4,5,6} = 2I irrep dims = the "
          "v312 rewrite-attractor Perron vector",
          null_ok and perron_ok and multiset_ok)

    # 2. Kronheimer hyper-Kaehler dimension count
    d = list(KAC_MARKS)
    e_sum = sum(d[a - 1] * d[b - 1] for a, b in AFFINE_EDGES)
    sq_sum = sum(x * x for x in d)
    dimM = 4 * e_sum                    # double quiver, quaternionic
    dimG = sq_sum - 1                   # prod U(d_i) / U(1)
    dimX = dimM - 4 * dimG
    check("KRONHEIMER DIMENSION COUNT [E]: dim_R M - 4 dim_R G = 4(sum_edges d_i d_j "
          "- sum d_i^2 + 1) = 4 -- the hyper-Kaehler quotient of the marks quiver is "
          "4-real-dimensional (the C^2/Gamma geometry); sum_edges d_i d_j = "
          "sum d_i^2 = 120 forced by the null-vector identity",
          e_sum == sq_sum == 120 and dimX == 4)

    # 3. gauge datum = |2I| = 120 = |mu4| h(E8), h = 2*3*5
    check("GAUGE DATUM = |2I| [E]: sum delta_i^2 = 120 = |mu4| h(E8) = 4*30, "
          "h(E8) = 30 = |Z2| N_fam g_car = 2*3*5 -- the quiver group size is the "
          "seam's own binary icosahedral order (regular representation)",
          sq_sum == 120 == MU4 * H_E8 and H_E8 == Z2 * N_fam * g_car)

    # 4. resolution data: -E8 intersection form, unimodular; 3*rank deformations
    Afin = adjacency(8, FINITE_EDGES)
    Cfin = 2 * sp.eye(8) - Afin
    det1 = int(Cfin.det()) == 1
    snf_id = smith_normal_form(Cfin) == sp.eye(8)
    check("RESOLUTION DATA [E]: 8 = rank(E8) exceptional spheres with intersection "
          "form -Cartan(E8), det = 1 and SNF = identity (the Poincare-sphere link = "
          "the det K = 1 face, v232/v344); deformation space h (x) R^3 has dim "
          "3*8 = 24",
          det1 and snf_id and 3 * rankE8 == 24)

    # 5./6. typing
    check("CITED THEOREMS [C]: Kronheimer (K-A) construction + (K-B) Torelli "
          "(J. Diff. Geom. 29 (1989) 665 and 685) are IMPORTED, not re-proved -- the "
          "same citation class as NPW26/MMST/AGT (v424/v336/v459)", True)
    check("RESIDUAL TRANSFORMS, NOT CLOSED [O]: the open premise becomes 'the raw "
          "seam supplies ALE hyper-Kaehler data asymptotic to the (2,3,5) cone' -- "
          "the SAME single arrow as SEAM.EQUIV.01 (v346 L2); no gate closes, no "
          "marker moves", True)

    return summary("v479 SEAM.KRONHEIMER.01: R3's combinatorial-to-geometric bridge "
                   "discharged to Kronheimer 1989 -- marks = null/Perron vector [E], "
                   "hyper-Kaehler quotient dim = 4 [E], gauge datum |2I| = 120 = 4*30 "
                   "[E], resolution = unimodular -E8 (det 1 = Poincare link = det K=1 "
                   "face) with 24 deformation parameters [E]; theorems cited [C]; the "
                   "one premise stays [O] (SEAM.EQUIV.01 unchanged)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

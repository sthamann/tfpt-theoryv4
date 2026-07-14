"""CORR.KRONHEIMER.01 -- the R3 "combinatorial-to-geometric bridge" of SEAM.DETK.01
is an ESTABLISHED THEOREM (Kronheimer 1989), not an open construction (theory contract;
never a scorecard row, never load-bearing).

Motivation (2026-07-14, bird's-eye round): SEAM.DETK.01 ranks the hypergraph route R3 as
the most promising access to the one open keystone bit det K = 1, and names its residual:

    "the combinatorial-to-geometric bridge: the rewrite attractor (a graph) IS the
     du Val singularity."

That bridge is EXACTLY the content of Kronheimer's ALE construction + classification
(P. B. Kronheimer, "The construction of ALE spaces as hyper-Kaehler quotients",
J. Differential Geom. 29 (1989) 665-683; and "A Torelli-type theorem for gravitational
instantons", J. Differential Geom. 29 (1989) 685-697):

  (K-A) CONSTRUCTION: given a McKay graph Gamma-hat with dimension vector delta = the
        Kac marks (= dims of the irreps of Gamma), the hyper-Kaehler quotient of the flat
        double-quiver representation space by U(delta)/U(1) at moment-map level zero IS
        C^2/Gamma; nonzero levels give its ALE deformations/resolutions.
  (K-B) CLASSIFICATION (Torelli): EVERY ALE hyper-Kaehler 4-manifold is one of these
        quiver varieties; the intersection form of the minimal resolution is minus the
        ADE Cartan matrix.

So "graph + marks => du Val geometry" is a citable theorem. TFPT already has the graph
and the marks as compiler outputs: the (2,3,5) rewrite attractor is the affine-E8 graph
and the Kac marks are its Perron vector (HYP.INJECT.01/v312; E8.NETWORK.01/v298). This
contract machine-checks every FINITE ingredient of Kronheimer's input data against the
seam atoms, and types the residual honestly.

WHAT THIS IS / IS NOT.  [E]: all arithmetic below (null vector = Perron vector = marks,
the hyper-Kaehler dimension count dim_R X = 4, |2I| = sum delta_i^2 = 120, deformation
parameter count 3 * rank = 24, unimodularity) is exact.  [C]: Kronheimer's theorems are
CITED, not re-proved.  [O]: the seam-side premise ("the raw seam supplies ALE hyper-Kaehler
data asymptotic to the (2,3,5) cone") is NOT closed here -- it is the SAME single arrow as
SEAM.EQUIV.01 (v346 L2) / CORR.FORCING.01, now with the graph->geometry half discharged to
the literature. NOT claimed: a closed gate or a status change.

Firewall: theory contract; belongs in experiments/theory-contracts, never in
evidence_scorecard.json; passing is internal consistency, not external evidence.

Run:  cd experiments/theory-contracts && python3 corr_kronheimer_quiver_bridge.py
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

RESULTS = Path(__file__).resolve().parent / "corr_kronheimer_quiver_results.json"

CHECKS: list[dict] = []

# seam atoms
Z2, N_FAM, G_CAR, MU4 = 2, 3, 5, 4
RANK_E8, H_E8 = 8, 30

# affine E8 (E8^(1)): nodes 1..8 = finite E8 (Bourbaki), node 9 = affine node attached
# to the end of the long chain (node 8).  Kac marks in this labelling:
#   finite nodes (1..8): (2,3,4,6,5,4,3,2)  [Bourbaki E8 marks]
#   affine node 9: 1
FINITE_EDGES = [(1, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (2, 4)]
AFFINE_EDGES = FINITE_EDGES + [(8, 9)]
KAC_MARKS = sp.Matrix([2, 3, 4, 6, 5, 4, 3, 2, 1])   # delta, Bourbaki order + affine node


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def adjacency(n: int, edges: list[tuple[int, int]]) -> sp.Matrix:
    A = sp.zeros(n, n)
    for a, b in edges:
        A[a - 1, b - 1] = A[b - 1, a - 1] = 1
    return A


def c1_marks_are_null_and_perron() -> None:
    """[E] The Kac marks delta are (i) the null vector of the affine Cartan matrix
    C = 2I - A and (ii) the Perron eigenvector A delta = 2 delta of the McKay graph --
    the McKay tensor identity Q (x) R_i = (+)_j A_ij R_j at dimension level.
    This is the SAME vector v312 found as the Perron vector of the rewrite attractor."""
    A = adjacency(9, AFFINE_EDGES)
    C = 2 * sp.eye(9) - A
    null_ok = (C * KAC_MARKS) == sp.zeros(9, 1)
    perron_ok = (A * KAC_MARKS) == 2 * KAC_MARKS
    multiset_ok = sorted(KAC_MARKS) == [1, 2, 2, 3, 3, 4, 4, 5, 6]
    ok = null_ok and perron_ok and multiset_ok
    check("C1 MARKS = NULL VECTOR = PERRON VECTOR [E]: C_aff delta = 0 and A delta = "
          "2 delta for the affine-E8 McKay graph; multiset {1,2,2,3,3,4,4,5,6} = 2I irrep "
          "dims = the v312 rewrite-attractor Perron vector",
          ok, f"C.delta=0: {null_ok}; A.delta=2delta: {perron_ok}; "
              f"marks(sorted)={sorted(KAC_MARKS)}")


def c2_kronheimer_dimension_count() -> None:
    """[E] Kronheimer's hyper-Kaehler quotient dimension count lands EXACTLY on 4:
    dim_R M = 4 sum_edges delta_i delta_j (double quiver, quaternionic),
    dim_R G = sum delta_i^2 - 1 (G = prod U(delta_i) / U(1)),
    dim_R X = dim M - 4 dim G = 4 (sum_edges d_i d_j - sum d_i^2 + 1) = 4
    -- a 4-real-dimensional space: the C^2/Gamma geometry. The identity
    sum_edges d_i d_j = sum d_i^2 is forced by C_aff delta = 0."""
    d = list(KAC_MARKS)
    e_sum = sum(d[a - 1] * d[b - 1] for a, b in AFFINE_EDGES)
    sq_sum = sum(x * x for x in d)
    dimM = 4 * e_sum
    dimG = sq_sum - 1
    dimX = dimM - 4 * dimG
    ok = (e_sum == sq_sum == 120) and dimX == 4
    check("C2 KRONHEIMER DIMENSION COUNT [E]: dim_R M - 4 dim_R G = "
          "4(sum_edges d_i d_j - sum d_i^2 + 1) = 4 -- the hyper-Kaehler quotient of the "
          "marks quiver is a 4-real-dim (= C^2/Gamma) space; sum_edges d_i d_j = "
          "sum d_i^2 = 120 forced by the null-vector identity",
          ok, f"sum_edges d_i d_j = {e_sum}; sum d_i^2 = {sq_sum}; dim_R M = {dimM}; "
              f"dim_R G = {dimG}; dim_R X = {dimX}")


def c3_regular_rep_is_2I_order() -> None:
    """[E] sum delta_i^2 = |Gamma| (regular representation): 120 = |2I| = |mu4| h(E8)
    = 4*30, and h(E8) = 30 = 2*3*5 = product of the seam atoms -- the quiver's gauge-group
    size IS the binary icosahedral order, tying the Kronheimer input to CORR.FORCING.01."""
    sq_sum = sum(x * x for x in KAC_MARKS)
    ok = (sq_sum == 120 == MU4 * H_E8) and (H_E8 == Z2 * N_FAM * G_CAR)
    check("C3 |2I| FROM THE MARKS [E]: sum delta_i^2 = 120 = |2I| = |mu4| h(E8), "
          "h(E8) = 30 = |Z2| N_fam g_car -- the quiver gauge datum is the seam's own group "
          "order",
          ok, f"sum delta_i^2 = {sq_sum}; |mu4|*h = {MU4 * H_E8}; 2*3*5 = {Z2 * N_FAM * G_CAR}")


def c4_resolution_data() -> None:
    """[E] Kronheimer resolution data: the exceptional set of the minimal resolution has
    rank(E8) = 8 spheres with intersection form MINUS the E8 Cartan matrix (unimodular,
    det = 1 => H_1(link) = 0, the Poincare sphere = the det K = 1 face), and the
    hyper-Kaehler deformation parameter space is h (x) R^3: dim = 3 * rank = 24."""
    Afin = adjacency(8, FINITE_EDGES)
    Cfin = 2 * sp.eye(8) - Afin
    det_ok = int(Cfin.det()) == 1
    n_spheres = 8
    n_deform = 3 * RANK_E8
    ok = det_ok and n_spheres == RANK_E8 and n_deform == 24
    check("C4 RESOLUTION DATA [E]: 8 = rank(E8) exceptional spheres, intersection form "
          "-Cartan(E8) unimodular (det = 1 => Poincare-sphere link => det K = 1); "
          "deformation space h (x) R^3 has dim 3*8 = 24",
          ok, f"det Cartan(E8) = {int(Cfin.det())}; #spheres = {n_spheres}; "
              f"3*rank = {n_deform}")


def c5_conditional_typing() -> None:
    """[C]/[O] The honest typing: Kronheimer (K-A) turns 'graph + marks => C^2/Gamma
    geometry' into a THEOREM (the R3 combinatorial-to-geometric bridge is discharged to
    the literature, same genre as the NPW26/MMST/AGT imports); Kronheimer (K-B, Torelli)
    adds the converse (any ALE space with E8 intersection form is on this list). The
    residual premise is TRANSFORMED, not closed: 'the raw seam supplies ALE hyper-Kaehler
    data asymptotic to the (2,3,5) cone' -- the same single arrow as SEAM.EQUIV.01
    (v346 L2). No gate closes."""
    finite_ok = all(c["pass"] for c in CHECKS)
    ok = finite_ok
    check("C5 CONDITIONAL TYPING [C cited / O premise]: with C1-C4 the Kronheimer input "
          "data ARE the seam atoms, so R3's 'combinatorial-to-geometric bridge' is the "
          "CITED theorem (K-A construction, K-B Torelli); residual premise = 'seam "
          "supplies the ALE/orbifold datum' = SEAM.EQUIV.01's one arrow; NOT closed here",
          ok, "bridge discharged to Kronheimer 1989 (JDG 29, 665 and 685); premise stays "
              "OPEN; no gate closed, no status change")


def main() -> None:
    print("CORR.KRONHEIMER.01 -- the R3 graph->geometry bridge as Kronheimer's theorem\n")
    c1_marks_are_null_and_perron()
    c2_kronheimer_dimension_count()
    c3_regular_rep_is_2I_order()
    c4_resolution_data()
    c5_conditional_typing()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "CONTRACT HOLDS" if n_pass == len(CHECKS) else "CONTRACT FAILS"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "SEAM.DETK.01's R3 residual ('the rewrite attractor graph IS the du Val "
        "singularity') is not an open construction: Kronheimer 1989 constructs C^2/Gamma "
        "and all its ALE deformations as the hyper-Kaehler quotient of exactly the data "
        "TFPT already outputs (the affine-E8 McKay graph with the Kac marks = the v312 "
        "Perron vector), and the Torelli theorem gives the converse. Every finite "
        "ingredient checks exactly: the marks are the null/Perron vector (C1), the "
        "quotient dimension is 4 (C2), the gauge datum is |2I| = 120 = 4*30 with 30 = "
        "2*3*5 (C3), and the resolution carries the unimodular -E8 form (det 1 = the "
        "Poincare link = det K = 1) with 3*8 = 24 deformation parameters (C4). The open "
        "arrow transforms into 'the seam supplies the ALE/orbifold datum' -- the same "
        "single premise as SEAM.EQUIV.01/CORR.FORCING.01. [E] arithmetic, [C] citations, "
        "[O] premise; no gate closed."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "CORR.KRONHEIMER.01 Kronheimer quiver bridge for SEAM.DETK.01 R3",
        "date": "2026-07-14",
        "firewall": ("theory contract, never a scorecard row, never load-bearing; "
                     "internal consistency, not evidence; gated on SEAM.EQUIV.01 (open)"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")
    raise SystemExit(0 if n_pass == len(CHECKS) else 1)


if __name__ == "__main__":
    main()

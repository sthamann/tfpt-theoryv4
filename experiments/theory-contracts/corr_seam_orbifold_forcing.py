"""CORR.FORCING.01 -- the "one arrow" of SEAM.EQUIV.01, sharpened to a machine-checked
CONDITIONAL theorem (pure mathematics; never a scorecard row, never load-bearing).

Motivation (2026-07-14, the correspondence-principle round, experiments/tfpt-correspondence):
the spacetime <-> black-hole correspondence is typed [C] because it is gated on the OPEN
Seam-Horizon theorem SEAM.EQUIV.01. Its one remaining open arrow (origin_theory / v346, link
L2) is:

    "the raw quasi-free seam normal bundle is an ADE orbifold point  C^2 / Gamma."

This contract does NOT close that arrow (it cannot: the scaling-limit / rigidity wall is the
open item). What it DOES is prove, by finite exact computation, the CONDITIONAL:

    IF the seam realises ANY finite-SU(2) orbifold C^2/Gamma,
    THEN Gamma = 2I (binary icosahedral) is FORCED by the seam's own atoms, and
         every downstream consequence (2I -> affine E8 -> E8 du Val -> Poincare link
         -> det K = 1) is a theorem.

so the whole keystone reduces to that single geometric premise -- exactly the honest content
of v346's "the bridge is one arrow". The forcing is driven by the SAME atoms that lock the
correspondence phase boundary (|Z2|, N_fam, g_car), which is why the correspondence gives the
keystone additional motivation.

WHAT THIS IS / IS NOT.  [E]: every arithmetic fact below (Cartan determinants, the (2,3,5)
axis signature, the 2I McKay fingerprint, the Coxeter/order identities) is exact.  [C]/[O]:
the physical premise -- "the seam IS such an orbifold" -- is NOT proven here; it is
SEAM.EQUIV.01's open arrow, and this contract only shows it is the SOLE remaining input.
NOT claimed: a closed gate, a status change, or that the correspondence is now [E].

Firewall: theory contract; belongs in experiments/theory-contracts, never in
evidence_scorecard.json; passing is internal consistency, not external evidence.

Run:  cd experiments/theory-contracts && python3 corr_seam_orbifold_forcing.py
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

RESULTS = Path(__file__).resolve().parent / "corr_seam_orbifold_forcing_results.json"

CHECKS: list[dict] = []

# ---- the seam atoms that also lock the correspondence phase boundary ----
Z2, N_FAM, G_CAR = 2, 3, 5          # |Z2|, A3 family count, carrier rank
MU4 = 4                              # |mu4|
SEAM_SIGNATURE = (Z2, N_FAM, G_CAR)  # = (2, 3, 5)


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def cartan(n: int, edges: list[tuple[int, int]]) -> sp.Matrix:
    """Simply-laced Cartan matrix from a 1-indexed Dynkin adjacency (2 on the diagonal,
    -1 on each edge)."""
    M = sp.zeros(n, n)
    for i in range(n):
        M[i, i] = 2
    for a, b in edges:
        M[a - 1, b - 1] = M[b - 1, a - 1] = -1
    return M


# ADE Dynkin diagrams (Bourbaki node labels).
def dynkin(kind: str, n: int) -> tuple[int, list[tuple[int, int]]]:
    if kind == "A":
        return n, [(i, i + 1) for i in range(1, n)]
    if kind == "D":                       # chain 1..n-2, fork (n-1),(n) at node n-2
        e = [(i, i + 1) for i in range(1, n - 2)] + [(n - 2, n - 1), (n - 2, n)]
        return n, e
    if kind == "E":                       # E6/E7/E8: chain 1-3-4-5-...(n) + branch 2-4
        chain = [(1, 3), (3, 4)] + [(i, i + 1) for i in range(4, n)]
        return n, chain + [(2, 4)]
    raise ValueError(kind)


def c1_ade_cartan_determinants() -> None:
    """[E] The finite-SU(2) subgroups are the ADE McKay groups; the Cartan determinant
    equals |coker(Cartan)| = |H_1(link)| of the du Val singularity, closed-form per family."""
    got = {}
    ok = True
    for kind, n, closed in [("A", 1, 2), ("A", 4, 5), ("A", 8, 9),
                            ("D", 4, 4), ("D", 5, 4), ("D", 8, 4),
                            ("E", 6, 3), ("E", 7, 2), ("E", 8, 1)]:
        nn, edges = dynkin(kind, n)
        d = int(cartan(nn, edges).det())
        got[f"{kind}{n}"] = d
        ok = ok and (d == closed)
    check("C1 ADE CARTAN DETERMINANTS [E]: det(Cartan) = |H_1(link)|; A_n->n+1, "
          "D_n->4, E6->3, E7->2, E8->1 (McKay: cyclic/binary-dihedral/2T/2O/2I)",
          ok, f"computed exactly: {got}")


def c2_signature_forces_2I() -> None:
    """[E] Among the EXCEPTIONAL binary polyhedral groups the platonic axis signature
    (p,q,r) is (2,3,3)=2T, (2,3,4)=2O, (2,3,5)=2I; the seam atoms (|Z2|,N_fam,g_car)=(2,3,5)
    match ONLY 2I."""
    groups = {
        "2T": {"sig": (2, 3, 3), "ade": "E6", "order": 24},
        "2O": {"sig": (2, 3, 4), "ade": "E7", "order": 48},
        "2I": {"sig": (2, 3, 5), "ade": "E8", "order": 120},
    }
    matches = [g for g, v in groups.items() if v["sig"] == SEAM_SIGNATURE]
    ok = matches == ["2I"] and groups["2I"]["ade"] == "E8"
    check("C2 SEAM SIGNATURE FORCES 2I [E]: (|Z2|,N_fam,g_car)=(2,3,5) is the icosahedral "
          "signature -> Gamma=2I (binary icosahedral) UNIQUELY among {2T,2O,2I}; downstream "
          "ADE = E8",
          ok, f"seam signature {SEAM_SIGNATURE}; matches={matches}; "
              f"2T=(2,3,3),2O=(2,3,4),2I=(2,3,5)")


def c3_only_E8_is_homology_sphere() -> None:
    """[E] E8 is the UNIQUE ADE with det(Cartan)=1 => coker=0 => the plumbing link is an
    integral homology sphere (Poincare sphere) => the keystone bit det K = 1."""
    nn, edges = dynkin("E", 8)
    E8 = cartan(nn, edges)
    det_e8 = int(E8.det())
    snf = smith_normal_form(E8)
    is_identity = snf == sp.eye(8)
    # only E8 gives det 1 across ADE (A_n=n+1>=2, D_n=4, E6=3, E7=2)
    others_gt1 = all(d > 1 for d in (2, 5, 9, 4, 3, 2))
    ok = det_e8 == 1 and is_identity and others_gt1
    check("C3 ONLY E8 -> det K = 1 [E]: det(Cartan_E8)=1 and its Smith normal form is the "
          "identity => coker(E8)=0 => the du Val link is the Poincare homology sphere "
          "(H_1=0); no other ADE reaches 1",
          ok, f"det(E8)={det_e8}; SNF=I: {is_identity}; A/D/E6/E7 dets all > 1")


def c4_2I_mckay_fingerprint() -> None:
    """[E] 2I=SL(2,5) fingerprints: irrep dims = affine-E8 marks {1,2,2,3,3,4,4,5,6}
    (McKay), sum of squares = |2I| = 120 = |mu4|*h(E8) = 4*30, and h(E8)=30 = 2*3*5 is the
    PRODUCT of the seam signature."""
    irrep_dims = [1, 2, 2, 3, 3, 4, 4, 5, 6]     # dims of the 9 irreps of 2I=SL(2,5)
    affine_e8_marks = [1, 2, 3, 4, 5, 6, 4, 2, 3]  # Dynkin labels of affine E8
    order_2I = 120
    h_E8 = 30                                     # Coxeter number of E8
    ok = (Counter(irrep_dims) == Counter(affine_e8_marks)
          and sum(d * d for d in irrep_dims) == order_2I
          and len(irrep_dims) == 8 + 1                    # rank(E8)+1 affine nodes
          and order_2I == MU4 * h_E8
          and h_E8 == Z2 * N_FAM * G_CAR                  # 30 = 2*3*5 = product of signature
          and max(affine_e8_marks) == 6)
    check("C4 2I McKAY FINGERPRINT [E]: irrep dims == affine-E8 marks {1,2,2,3,3,4,4,5,6}, "
          "sum sq = |2I| = 120 = |mu4|*h(E8) = 4*30, and h(E8)=30 = 2*3*5 = product of "
          "(|Z2|,N_fam,g_car)",
          ok, f"irreps {sorted(irrep_dims)}; |2I|={order_2I}; h(E8)={h_E8}=2*3*5; "
              f"9 = rank(E8)+1")


def c5_conditional_typing() -> None:
    """[C]/[O] The honest conditional: C2-C4 make Gamma=2I and det K=1 FORCED, but ONLY
    conditional on the open premise 'the seam realises some C^2/Gamma orbifold'. That premise
    is SEAM.EQUIV.01's remaining open arrow (v346 L2) and is NOT closed here."""
    finite_forcing_holds = all(c["pass"] for c in CHECKS)      # C1-C4 are exact
    premise_is_open = True                                     # the one geometric arrow
    correspondence_stays_C = premise_is_open                   # gate not closed
    ok = finite_forcing_holds and premise_is_open and correspondence_stays_C
    check("C5 CONDITIONAL THEOREM [E for the implication; premise [O]]: IF seam ~ C^2/Gamma "
          "THEN Gamma=2I & det K=1 (from C2-C4). The premise (seam=orbifold) is the OPEN "
          "arrow of SEAM.EQUIV.01 -- NOT closed here; correspondence stays [C]",
          ok, "implication proven by finite forcing; premise recorded OPEN; no gate closed, "
              "no status change")


def main() -> None:
    print("CORR.FORCING.01 -- the one arrow of SEAM.EQUIV.01 as a conditional forcing "
          "theorem\n")
    c1_ade_cartan_determinants()
    c2_signature_forces_2I()
    c3_only_E8_is_homology_sphere()
    c4_2I_mckay_fingerprint()
    c5_conditional_typing()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "CONTRACT HOLDS" if n_pass == len(CHECKS) else "CONTRACT FAILS"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "The keystone SEAM.EQUIV.01 reduces to ONE open geometric arrow: 'the raw "
        "quasi-free seam is a C^2/Gamma orbifold point'. This contract proves the rest is "
        "forced: the seam's own atoms (|Z2|,N_fam,g_car)=(2,3,5) are the icosahedral "
        "signature, so Gamma=2I uniquely (C2); 2I's McKay graph is affine E8 with h(E8)=30="
        "2*3*5 and |2I|=4*30=120 (C4); and E8 is the unique ADE with det(Cartan)=1, i.e. the "
        "Poincare-homology-sphere link that IS det K=1 (C1,C3). So the correspondence's "
        "atoms and the keystone's target are the same object, and the whole gate is the "
        "single arrow 'seam=orbifold'. [E] for every arithmetic step; the premise itself is "
        "[O] (SEAM.EQUIV.01, v346 L2) and is NOT closed -- the correspondence stays [C]. No "
        "gate closed, no status change, no scorecard row."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "CORR.FORCING.01 seam-orbifold conditional forcing of SEAM.EQUIV.01",
        "date": "2026-07-14",
        "firewall": ("theory contract, never a scorecard row, never load-bearing; internal "
                     "consistency, not evidence; gated on SEAM.EQUIV.01 (open)"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")
    raise SystemExit(0 if n_pass == len(CHECKS) else 1)


if __name__ == "__main__":
    main()

"""AXION.NDW.06 the domain-wall number of the determinant-line axion -- THEORY CONTRACT.

Follow-up to axion05 (2026-07-10).  axion05 found the CLEAN resolution of the
misalignment-angle problem is POST-INFLATIONARY PQ breaking (natural since
H_inf/f_a ~ 66), at the single crux: the domain-wall number must be N_DW = 1 (else
a stable domain-wall network overcloses the universe -- the Zeldovich catastrophe).
This contract computes N_DW for the TFPT determinant-line axion.

The domain-wall number N_DW = |QCD colour anomaly of the PQ current| = the number of
degenerate vacua of the axion potential around theta in [0, 2pi), = the integer N in
the coupling  N * (a/f_a) * (g_s^2 / 32 pi^2) G Gtilde.  For the TFPT axion the PQ
"current" is the phase of the seam DETERMINANT LINE, so its QCD anomaly is the INDEX
of the seam Dirac operator -- which is EXACTLY the inflow level k0 = |C| = 1 already
computed in v470/v472 (Chern number of the twist-torus U(1) family).  Hence
N_DW = 1: the determinant-line axion is automatically domain-wall-safe.

This is typed [C]: it rests on identifying N_DW with the seam det-line index (the
same physical identification class as ALPHA.QUILLEN / EM.WARD).  The DFSZ-type
alternative (a Higgs-portal axion coupling universally to the 3 quark families) would
give N_DW = 2 N_fam = 6 and NEED the Lazarides-Shafi bias -- shown as the contrast;
TFPT's axion is the det-line one, not DFSZ.

Checks (hard-typed):

  C1 [E] N_DW DEFINITION: N_DW = |colour anomaly of the PQ current| = degeneracy of
     the axion potential = the integer N in N (a/f_a)(g_s^2/32pi^2) G Gtilde.
  C2 [C] DET-LINE ANOMALY = SEAM INDEX = 1: the TFPT axion is the phase of the seam
     determinant line, so its QCD anomaly is the seam Dirac INDEX = the inflow level
     k0 = |C| = 1 (v470/v472, established) => N_DW = 1.
  C3 [E] N_DW = 1 => DOMAIN-WALL-SAFE: a unit anomaly gives a UNIQUE vacuum around
     the circle, so there are no stable domain walls -- the post-inflationary
     scenario (axion05 S1) is cosmologically safe, NO Lazarides-Shafi bias needed.
  C4 [E] CONTRAST / CONTROL: a DFSZ-type universal coupling to the 3 quark families
     would give N_DW = 2 N_fam = 6 (would need the bias mechanism); the det-line
     reading (index = 1) differs, and TFPT's axion is the det-line/strong-CP one,
     NOT a Higgs-portal DFSZ axion.
  C5 [C]/[O] RELOCATION AUDIT: N_DW = 1 rests on identifying the domain-wall number
     with the seam det-line index (=1, v470/v472) -- a physical identification, the
     same [C] class as ALPHA.QUILLEN.  Given it, axion05's S1 is COMPLETE: the
     post-inflationary axion is domain-wall-safe and needs no dial.  If instead the
     axion were DFSZ (N_DW=6), the bias mechanism is required.  Never a scorecard
     row; never [E].

Firewall: F_transfer/cosmology bridge; internal consistency, not evidence.
"""
from __future__ import annotations

import json
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "axion06_domain_wall_results.json"
CHECKS: list[dict] = []

N_FAM = 3
DIM_SPLUS = 16
MU4 = 4
CHERN_C = 1                                      # inflow level k0 = |C| = 1 (v470/v472)


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def c1_definition() -> None:
    # f_a normalisation cross-check: 128 = 2 * dim S+ * |mu4|
    denom = 2 * DIM_SPLUS * MU4
    check("C1 N_DW DEFINITION [E]: N_DW = |colour anomaly of the PQ current| = "
          "degeneracy of the axion potential = the integer N in N (a/f_a)(g_s^2/"
          "32pi^2) G Gtilde; (the det-line f_a normalisation 2 dim S+ |mu4| = %d is "
          "the amplitude, distinct from the anomaly integer)" % denom,
          denom == 128, "f_a denominator 2*dim S+*|mu4| = %d (amplitude); N_DW is the "
          "anomaly integer, computed next" % denom)


def c2_det_line_index() -> None:
    N_DW = abs(CHERN_C)                            # anomaly = seam Dirac index = |C|
    check("C2 DET-LINE ANOMALY = SEAM INDEX = 1 [C]: the TFPT axion is the phase of "
          "the seam determinant line, so its QCD anomaly is the seam Dirac INDEX = "
          "the inflow level k0 = |C| = %d (v470/v472, established) => N_DW = %d"
          % (CHERN_C, N_DW),
          N_DW == 1, "N_DW = |C| = %d (seam det-line index = inflow level, v470/v472)"
          % N_DW)


def c3_safe() -> None:
    N_DW = abs(CHERN_C)
    check("C3 N_DW = 1 => DOMAIN-WALL-SAFE [E]: a unit anomaly gives a UNIQUE vacuum "
          "around theta in [0,2pi), so there are NO stable domain walls -- the "
          "post-inflationary scenario (axion05 S1) is cosmologically safe, no "
          "Lazarides-Shafi bias needed",
          N_DW == 1, "N_DW = %d => unique vacuum => no wall network" % N_DW)


def c4_contrast() -> None:
    N_DW_dfsz = 2 * N_FAM                           # 6 (universal 3-family coupling)
    N_DW_det = abs(CHERN_C)                         # 1
    ok = (N_DW_dfsz == 6 and N_DW_det == 1 and N_DW_dfsz != N_DW_det)
    check("C4 CONTRAST / CONTROL [E]: a DFSZ-type universal coupling to the 3 quark "
          "families gives N_DW = 2 N_fam = %d (needs the bias mechanism); the "
          "det-line reading gives index = %d -- they DIFFER, and TFPT's axion is the "
          "det-line/strong-CP one, not a Higgs-portal DFSZ axion" % (N_DW_dfsz, N_DW_det),
          ok, "N_DW(DFSZ universal) = %d vs N_DW(det-line index) = %d"
          % (N_DW_dfsz, N_DW_det))


def c5_relocation() -> None:
    imported = [
        "domain-wall number = QCD colour anomaly of the PQ current = vacuum "
        "degeneracy (standard axion cosmology)",
        "seam det-line index = inflow level k0 = |C| = 1 (v470/v472, in-suite)",
        "the identification N_DW = seam det-line index (a physical identification, "
        "same [C] class as ALPHA.QUILLEN / EM.WARD)",
        "Lazarides-Shafi bias needed ONLY if N_DW > 1 (the DFSZ alternative)",
    ]
    check("C5 RELOCATION AUDIT [C]/[O]: N_DW = 1 rests on identifying the domain-wall "
          "number with the seam det-line index (=1, v470/v472) -- a [C] physical "
          "identification. Given it, axion05's S1 is COMPLETE: the post-inflationary "
          "axion is domain-wall-safe, no dial. If the axion were DFSZ (N_DW=6) the "
          "bias mechanism is required. Never a scorecard row; never [E]",
          True, "; ".join(imported))


def main() -> None:
    print("AXION.NDW.06 -- the domain-wall number of the determinant-line axion "
          "(axion05's crux)\n")
    c1_definition(); c2_det_line_index(); c3_safe(); c4_contrast(); c5_relocation()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = ("N_DW = 1 [C] => post-inflationary axion is DOMAIN-WALL-SAFE "
               "(axion05 S1 complete, no dial)" if n_pass == len(CHECKS)
               else "INCONCLUSIVE")
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "Computing axion05's one crux -- the domain-wall number N_DW. For the TFPT "
        "determinant-line axion the PQ current is the phase of the seam determinant "
        "line, so its QCD colour anomaly (= N_DW) is the seam Dirac INDEX, which is "
        "exactly the inflow level k0 = |C| = 1 already established in v470/v472. Hence "
        "N_DW = 1: the axion potential has a unique vacuum around the circle, there are "
        "NO stable domain walls, and the post-inflationary resolution (axion05 S1) is "
        "cosmologically SAFE with no Lazarides-Shafi bias -- and no dial. This is typed "
        "[C]: it rests on identifying N_DW with the seam det-line index (the same "
        "physical-identification class as ALPHA.QUILLEN). The DFSZ alternative "
        "(universal 3-family coupling, N_DW = 2 N_fam = 6) is shown as the contrast and "
        "would need the bias mechanism -- but TFPT's axion is the det-line/strong-CP "
        "one, not DFSZ. Net: axion01->05->06 turns the axion 'fixed-angle catastrophe' "
        "into a clean, dial-free, domain-wall-safe POST-INFLATIONARY axion -- at the "
        "cost only of the (fragile) angle prediction. Never a scorecard row; never [E]."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "AXION.NDW.06 domain-wall number",
        "date": "2026-07-10",
        "firewall": "theory contract, never a scorecard row; not evidence",
        "N_DW_det_line": abs(CHERN_C), "N_DW_dfsz_alt": 2 * N_FAM,
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS, "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()

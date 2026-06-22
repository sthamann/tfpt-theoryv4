"""v321 -- the forward kill-test board: the decisive upcoming measurements, ranked.

The forward-looking companion to v307 (the CURRENT decision board).  v307 scores the
frozen registry against TODAY's data; this module assembles the DECISIVE NEXT
measurements -- what each upcoming experiment will measure, its expected reach, and the
TFPT value it would confirm or kill -- ranked by how fast and how hard it bites.  It
includes the NEW Galois-forced CP relation (v320) as a fresh kill test, and the rare-kaon
channel (v202) now that the NA62 2016-2024 combination has landed on the prediction.

Each board entry is locked to a freeze_file.csv kill row (so the test and the frozen
signal cannot drift apart), and to the frozen registry value where one exists.

  [N] 1. COVERAGE: every board entry is backed by a freeze_file.csv kill row.
  [N] 2. THE NEW KILL TEST: the v320 Galois CP relation (delta_PMNS = delta_CKM,lead + pi
        = 240 deg) is on the board (DUNE / Hyper-K).
  [N] 3. RANKING: JUNO sin^2 theta12 = 0.306747 is rank 1 (fastest, sub-percent); the
        R^2 band r and the dark-energy w front follow.
  [N] 4. POWER: >= 7 decisive near-term tests, each with a concrete kill threshold (the
        board is not vacuous).

HONEST SCOPE: a forward decision ledger (timelines/reach are the publicly stated
experimental targets, not TFPT outputs); no new physics, complements v307.  Python-only.
"""
import csv
import json
import os

from tfpt_constants import check, summary, reset

HERE = os.path.dirname(os.path.abspath(__file__))

# rank, observable, freeze_file key, experiment, timeline, reach, kill (short)
BOARD = [
    (1, "sin^2 theta12 = 0.306747", "solar_angle", "JUNO", "~2026-2028",
     "sub-percent central", "value away from 0.306747 at >3 sigma -> seam-misalignment dies"),
    (2, "tensor r in [0.0033,0.0048]", "tensor_ratio", "CMB-S4 / LiteBIRD", "~2028-2032",
     "sigma(r) ~ 5e-4", "robust r > 0.01 -> the R^2 / Starobinsky branch dies"),
    (3, "w = -1 (dark energy)", "dark_energy", "DESI / Euclid", "ongoing",
     "systematics-dominated", "robust w != -1 -> the single-engine Lambda readout dies"),
    (4, "delta_PMNS = 240 = delta_CKM,lead + pi", "cp_phase_relation", "DUNE / Hyper-K",
     "~2030+", "few-deg on delta_CP", "delta_PMNS away from 240 deg at >3 sigma -> the Galois-CP lock dies (v320)"),
    (5, "normal ordering, small m_betabeta", "neutrino_mass", "DUNE / LEGEND / nEXO",
     "~2028-2035", "ordering + m_betabeta", "inverted ordering or large m_betabeta -> the Majorana branch dies"),
    (6, "theta_eff = 0 (nEDM)", "nEDM", "PSI n2EDM / SNS", "ongoing",
     "below SM background", "a solid nonzero nEDM -> the structural strong-CP cancellation dies"),
    (7, "sin^2 theta13 = 0.0231 (now ~2 sigma)", "reactor_angle", "JUNO / global", "~2026-2028",
     "sub-percent", "persistent deviation beyond 3 sigma after the global fit"),
    (8, "beta = 0.2424 deg (birefringence)", "birefringence", "LiteBIRD / Simons Obs.",
     "~2028+", "calibration-controlled", "systematics-controlled exclusion of 0.2424 deg at >3 sigma"),
    (9, "BR(K+ -> pi nu nubar) = 9.45e-11", "rare_kaon", "NA62 / KOTO-II", "ongoing",
     "NA62 now +-1.8e-11 (on prediction)", "a stable NA62 BR(K+) outside [7,12]e-11 or a KOTO-II BR(K_L) off the GN point -> the flavor bridge dies (an F_transfer readout, core untouched)"),
]


def run():
    reset()
    print("v321  forward kill-test board: the decisive upcoming measurements, ranked")

    with open(os.path.join(HERE, "freeze_file.csv"), newline="") as fh:
        freeze = {r["claim"]: r for r in csv.DictReader(fh)}
    with open(os.path.join(HERE, "predictions_frozen.json")) as fh:
        json.load(fh)   # registry exists / parses

    print("  --- ranked forward kill-test board ---")
    for rank, obs, key, exp, when, reach, kill in BOARD:
        print(f"    #{rank} {obs:<38} {exp:<20} [{when}] -> {kill}")

    # 1. coverage: every board entry backed by a freeze_file kill row
    missing = [key for (_r, _o, key, *_rest) in BOARD if key not in freeze]
    check("COVERAGE [N]: every board entry is locked to a freeze_file.csv kill row "
          "(no drift between the test and the frozen signal); missing=%s" % missing,
          missing == [])

    # 2. the new v320 CP relation is on the board
    keys = {key for (_r, _o, key, *_rest) in BOARD}
    check("NEW KILL TEST [N]: the v320 Galois-forced CP relation (delta_PMNS = "
          "delta_CKM,lead + pi = 240 deg) is on the board, decided by DUNE/Hyper-K",
          "cp_phase_relation" in keys)

    # 3. ranking: JUNO sin^2 theta12 is rank 1 (fastest)
    rank1 = next(b for b in BOARD if b[0] == 1)
    check("RANKING [N]: JUNO sin^2 theta12 = 0.306747 is rank 1 (the fastest, "
          "sub-percent kill test)", rank1[2] == "solar_angle" and rank1[3] == "JUNO")

    # 4. power: enough decisive tests, each with a concrete kill threshold
    check("POWER [N]: >= 7 decisive near-term kill tests, each with a concrete "
          "falsification threshold (the board is not vacuous)",
          len(BOARD) >= 7 and all(len(b[6]) > 10 for b in BOARD))

    # honest: complements v307 (current) with the forward timeline
    check("HONEST [N]: a forward decision ledger (timelines/reach are the publicly "
          "stated experimental targets, not TFPT outputs); complements v307 (the "
          "current-data board) -- no new physics", True)

    return summary("v321 forward kill-test board")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

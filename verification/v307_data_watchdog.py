"""v307 -- the data watchdog: a decision pipeline over the frozen registry.

v84 freezes the predictions and v100 censuses the grammar; this module is the
operational DECISION layer that an adversarial reviewer's "experimental signature
ledger" and "kill-test board" call for.  It reads predictions_frozen.json and, for
every prediction with a current best measurement, computes the live tension n_sigma
and classifies it PASS / WATCH / TENSION / KILL against a fixed threshold, plus the
conditional bands (r, n_s) and the watchdog fronts (w) -- so the theory's standing
against today's data is one machine-checked table, refreshed on every suite run.

  [N] 1. COVERAGE: every frozen prediction + assigned texture + conditional band
        is classified (count matches the registry JSON).
  [N] 2. THEORY ALIVE: NO decidable prediction is in KILL (|n_sigma| >= 3); the
        compiler survives current data.
  [N] 3. POWER: the pipeline is not trivially green -- at least one prediction
        sits at WATCH/TENSION (|n_sigma| >= 1.5), and the most-tensioned CORE
        prediction is sin^2 theta13 (~2 sigma), the honest pressure point the
        external analysis under-weighted (it is already documented in v62).
  [N] 4. JUNO #1 KILL TEST: the prediction-of-record sin^2 theta12 = 0.306747 is
        currently compatible (|n_sigma| < 1); JUNO will sharpen it (the fastest
        falsifier).
  [N] 5. INFLATION/DARK-ENERGY FRONTS: the R^2 band r in [0.0033,0.0048] is below
        the BK18 limit (0.036) and the kill threshold (0.01) -- allowed, not
        excluded; w=-1 is flagged WATCHDOG (DESI dynamical-DE hints = the most
        dangerous negative front).

HONEST SCOPE: the measured central+sigma values are the repo-documented current
bests (CODATA 2022, NuFIT 6.0, ACT DR6, Planck 2018, PDG 2024, BK18 -- the same
sources as v62/v100), NOT freshly imported.  Ratio observables with a known
source-vs-pole / scheme caveat are judged against the conservative v18/v100 window,
not a knife-edge sigma.  A decision harness, not a new claim.  Python-only.
"""
import json
import math
import os

from tfpt_constants import check, summary, reset

# ---- current best measurements (repo-documented; provenance in the comment) ----
# id -> (central, sigma, source).  Clean experimental sigma -> n_sigma decision.
MEAS = {
    "ALPHA_INV":              (137.035999177, 0.000000021, "CODATA 2022"),
    "SIN2_THETA12_SEED":      (0.307,   0.012,   "NuFIT 6.0"),
    "SIN2_THETA13":           (0.02195, 0.00058, "NuFIT 6.0"),
    "BETA_BIREFRINGENCE_DEG": (0.215,   0.074,   "ACT DR6"),
    "OMEGA_B":                (0.0493,  0.0006,  "Planck 2018"),
    "LAMBDA_C":               (0.2245,  0.0005,  "PDG 2024"),
    "S23_CKM":                (0.0411,  0.0013,  "PDG 2024 |Vcb|"),
    "S13_CKM":                (0.00382, 0.00024, "PDG 2024 |Vub|"),
    "DELTA_CKM_RAD":          (1.1467,  0.05236, "PDG 2024 gamma=65.7+-3.0 deg"),
}
# ratio observables with a documented source-vs-pole / scheme caveat ->
# judged against a conservative relative window (v18 5% / v100), not a knife-edge.
SCHEME = {
    "MMU_OVER_MTAU": (0.05946, 0.03, "PDG 2024 (source vs pole)"),
    "ME_OVER_MMU":   (0.004836, 0.03, "PDG 2024 (source vs pole)"),
    "MU_OVER_MD":    (0.47, 0.05, "FLAG 2024 (scheme spread)"),
    "MC_OVER_MS":    (13.6, 0.05, "PDG 2024 MSbar (scheme spread)"),
    "MT_OVER_MB":    (41.0, 0.05, "PDG 2024 (scheme spread)"),
}
# no current decisive datum (downstream / assigned / not-yet-measured)
NO_DECISION = {"MSCAL_OVER_MBAR", "DELTA_CP_NU_DEG", "SIN2_THETA23"}
# the dark-energy / vacuum front: w=-1 readout, the most dangerous negative front
WATCHDOG = {"RHOL_OVER_MBAR4"}

BK18_R_LIMIT = 0.036          # BICEP/Keck 2018 95% upper limit on r
R_KILL = 0.01                 # TFPT kill: robust r > 0.01 kills the R^2 branch


def classify(n):
    a = round(abs(n), 1)
    if a < 1.0:
        return "PASS"
    if a < 2.0:
        return "WATCH"
    if a < 3.0:
        return "TENSION"
    return "KILL"


def run():
    reset()
    print("v307  data watchdog: decision pipeline over the frozen registry")

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "predictions_frozen.json")) as fh:
        reg = json.load(fh)

    preds = reg["predictions"]
    assigned = reg["assigned_texture_values"]
    bands = reg["conditional_bands"]

    board = []          # (id, layer, verdict, detail)
    core_clean = {}     # id -> n_sigma for CORE clean-sigma predictions

    for p in preds:
        pid, val, layer = p["id"], float(p["frozen_value"]), p["layer"]
        if pid in MEAS:
            m, s, src = MEAS[pid]
            n = (val - m) / s
            verdict = classify(n)
            board.append((pid, layer, verdict, f"{n:+.2f} sigma vs {src}"))
            if layer == "core":
                core_clean[pid] = n
        elif pid in SCHEME:
            m, win, src = SCHEME[pid]
            dev = abs(val - m) / m
            verdict = "PASS" if dev <= win else "FLAG"
            board.append((pid, layer, verdict,
                          f"{dev*100:.2f}% vs {win*100:.0f}% window ({src})"))
        elif pid in NO_DECISION or pid in WATCHDOG:
            tag = "WATCHDOG" if pid in WATCHDOG else "NO-DECISION"
            board.append((pid, layer, tag, "no decisive datum yet"))
        else:
            board.append((pid, layer, "NO-DECISION", "unmapped"))

    for a in assigned:
        board.append((a["id"], "assigned", "NO-DECISION",
                      "assigned texture (octant/phase not predicted)"))

    # conditional bands
    rband = next(b for b in bands if b["id"] == "R_TENSOR")
    rmax = float(rband["band_max"])
    r_allowed = rmax < BK18_R_LIMIT and rmax < R_KILL
    board.append(("R_TENSOR", "band", "PASS" if r_allowed else "TENSION",
                  f"band<= {rmax:.4f} < BK18 {BK18_R_LIMIT} and kill {R_KILL}"))
    nsb = next(b for b in bands if b["id"] == "N_S")
    ns_lo, ns_hi = float(nsb["band_min"]), float(nsb["band_max"])
    ns_c, ns_s = 0.9649, 0.0042          # Planck 2018
    ns_ok = (ns_lo <= ns_c + 2 * ns_s) and (ns_hi >= ns_c - 2 * ns_s)
    board.append(("N_S", "band", "PASS" if ns_ok else "TENSION",
                  f"band [{ns_lo:.4f},{ns_hi:.4f}] vs Planck {ns_c}+-{ns_s}"))

    # ---- print the decision board ----
    print("  --- decision board ---")
    for pid, layer, verdict, detail in board:
        print(f"    {verdict:<11} {pid:<24} [{layer}]  {detail}")
    from collections import Counter
    tally = Counter(v for _i, _l, v, _d in board)
    print("  tally:", dict(tally))

    # ---- 1. coverage ----
    expected = len(preds) + len(assigned) + len(bands)
    check("COVERAGE [N]: every frozen prediction + assigned texture + band is "
          "classified (%d entries match the registry)" % expected,
          len(board) == expected)

    # ---- 2. theory alive: no KILL among decidable predictions ----
    decidable = [n for n in core_clean.values()] + \
                [(float(p["frozen_value"]) - MEAS[p["id"]][0]) / MEAS[p["id"]][1]
                 for p in preds if p["id"] in MEAS and p["layer"] != "core"]
    no_kill = all(abs(n) < 3.0 for n in decidable)
    check("THEORY ALIVE [N]: no decidable prediction is in KILL (|n_sigma|<3); "
          "the compiler survives current data", no_kill)

    # ---- 3. power + the documented pressure point ----
    watch_items = [pid for pid, _l, v, _d in board if v in ("WATCH", "TENSION")]
    check("POWER [N]: the pipeline is not trivially green -- >=1 prediction at "
          "WATCH/TENSION (|n_sigma|>=1.5): %s" % ", ".join(watch_items),
          len(watch_items) >= 1)
    top_core = max(core_clean, key=lambda k: abs(core_clean[k]))
    check("PRESSURE POINT [N]: the most-tensioned CORE prediction is sin^2 "
          "theta13 (~2 sigma) -- the honest current pressure point (v62), which "
          "the external analysis under-weighted; |n|=%.2f"
          % abs(core_clean[top_core]),
          top_core == "SIN2_THETA13" and 1.9 <= round(abs(core_clean[top_core]), 1) < 3.0)

    # ---- 4. JUNO #1 kill test currently compatible ----
    th12 = next(p for p in preds if p["id"] == "SIN2_THETA12_SEED")
    n12 = (float(th12["frozen_value"]) - MEAS["SIN2_THETA12_SEED"][0]) \
        / MEAS["SIN2_THETA12_SEED"][1]
    check("JUNO #1 KILL TEST [N]: the prediction-of-record sin^2 theta12 = "
          "0.306747 is currently compatible (|n_sigma|=%.2f<1); JUNO is the "
          "fastest falsifier" % abs(n12), abs(n12) < 1.0)

    # ---- 5. inflation / dark-energy fronts ----
    check("INFLATION FRONT [N]: the R^2 band r in [0.0033,0.0048] is below the "
          "BK18 limit (0.036) and the kill threshold (0.01) -- allowed, not "
          "excluded", r_allowed)
    check("DARK-ENERGY FRONT [N]: w=-1 (rho_Lambda readout) flagged WATCHDOG -- "
          "DESI dynamical-DE hints are the most dangerous negative front",
          any(v == "WATCHDOG" for _i, _l, v, _d in board))

    return summary("v307 data watchdog (decision pipeline)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

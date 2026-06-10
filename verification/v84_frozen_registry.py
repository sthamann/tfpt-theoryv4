"""v84 -- Blind-prediction registry: frozen, machine-enforced.

Backs the freeze conventions in
  tfpt_2_standard_model.tex   (keybox "The three theta_12 values, named")
  introduction.tex            (freeze file box)
  verification/freeze_file.csv

The registry `predictions_frozen.json` freezes every dimensionless prediction
of record (25 significant digits) BEFORE the next decisive data releases
(JUNO theta12/theta13, CMB-S4/LiteBIRD r and beta, DESI n_s).  This script
re-derives every frozen decimal from the two axioms {c3 = 1/(8 pi), g_car = 5}
on every suite run, so the registry cannot drift:

  * changing a formula in the theory without updating the registry  -> FAIL
  * changing a registry value without changing the formula          -> FAIL
  * swapping the theta_12 prediction of record for a variant        -> FAIL

Together with manifest.sha256 (content digest) and git history this makes the
freeze auditable: the prediction of record is one number, fixed in advance,
and the two theta_12 variants are explicitly typed as derived variants of the
same texture, never as alternative predictions (no look-elsewhere ambiguity).
"""
import json
import os
import hashlib

import mpmath as mp
from tfpt_constants import check, summary, reset, c3, phi0, PI

REGISTRY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "predictions_frozen.json")

# relative tolerance for "digit-exact": values are stored at 25 significant
# digits, recomputation runs at mp.dps = 40
REL_TOL = mp.mpf('1e-22')


def alpha_root():
    """The unique root of F_U1 (same closure as v3_em_alpha.py, M = 41)."""
    pb = 1 / (6 * PI)
    dt = 48 * c3**4

    def F(a):
        Q = dt * mp.e**(-2 * a)
        ps = pb + Q * (1 - Q)**(mp.mpf(-5) / 4)
        return a**3 - 2 * c3**3 * a**2 - (mp.mpf(4) / 5) * c3**6 * 41 * mp.log(1 / ps)

    return mp.findroot(F, mp.mpf('0.0073'))


def theta12_nonlinear(eps):
    """Full (non-linearised) TBM + 1-2 charged-lepton rotation by eps."""
    Unu = mp.matrix([[mp.sqrt(mp.mpf(2) / 3), 1 / mp.sqrt(3), 0],
                     [-1 / mp.sqrt(6), 1 / mp.sqrt(3), -1 / mp.sqrt(2)],
                     [-1 / mp.sqrt(6), 1 / mp.sqrt(3), 1 / mp.sqrt(2)]])
    cs, sn = mp.cos(eps), mp.sin(eps)
    Ue = mp.matrix([[cs, sn, 0], [-sn, cs, 0], [0, 0, 1]])
    U = Ue.T * Unu
    return abs(U[0, 1])**2 / (1 - abs(U[0, 2])**2)


def computed_values():
    """Every registry id, re-derived from the two axioms alone."""
    a = alpha_root()
    ainv = 1 / a
    lamC = mp.sqrt(phi0 * (1 - phi0))
    return {
        # predictions
        "ALPHA_INV": ainv,
        "SIN2_THETA12_SEED": mp.mpf(1) / 3 - phi0 / 2,
        "SIN2_THETA13": phi0 * mp.e**(mp.mpf(-5) / 6),
        "BETA_BIREFRINGENCE_DEG": phi0 / (4 * PI) * 180 / PI,
        "OMEGA_B": (1 - 1 / (4 * PI)) * phi0,
        "LAMBDA_C": lamC,
        "S23_CKM": phi0 / (1 + lamC),
        "S13_CKM": lamC**3 / 3,
        "DELTA_CKM_RAD": PI / 3 + 3 * lamC**2,
        "MMU_OVER_MTAU": mp.mpf(8) / 7 * phi0,
        "ME_OVER_MMU": mp.mpf(12) / 7 * phi0**2,
        "MU_OVER_MD": mp.mpf(55) / 117,
        "MC_OVER_MS": mp.mpf(34) / 47 / phi0,
        "MT_OVER_MB": mp.mpf(3) / 26 / phi0**2,
        "MSCAL_OVER_MBAR": c3**(mp.mpf(7) / 2),
        "RHOL_OVER_MBAR4": 3 / (4 * PI**2) * mp.e**(-2 * ainv),
        # assigned texture values
        "DELTA_CP_NU_DEG": mp.mpf(240),
        "SIN2_THETA23": mp.mpf('0.5'),
        # derived theta_12 variants (same texture, NOT predictions)
        "SIN2_THETA12_SEAM": mp.mpf(1) / 3 - 1 / (12 * PI),
        "SIN2_THETA12_NONLIN": theta12_nonlinear(mp.mpf(3) / 4 * phi0),
        # conditional bands (N_star external in [50, 60])
        "R_TENSOR": (mp.mpf(12) / 60**2, mp.mpf(12) / 50**2),
        "N_S": (1 - mp.mpf(2) / 50, 1 - mp.mpf(2) / 60),
    }


def run():
    reset()
    # earlier suite modules may have lowered the global precision; the
    # digit-exact registry lock needs the full 40 digits back
    mp.mp.dps = 40
    print("v84 blind-prediction registry (frozen, machine-enforced)")

    with open(REGISTRY_PATH, "rb") as fh:
        raw = fh.read()
    reg = json.loads(raw)
    digest = hashlib.sha256(raw).hexdigest()
    print(f"  registry sha256: {digest}")

    vals = computed_values()

    # (1) the registry is frozen at a fixed date
    check("registry carries a fixed freeze_date (2026-06-09)",
          reg.get("freeze_date"), "2026-06-09", exact=True)

    # (2) every frozen prediction recomputes digit-exactly from the axioms
    for entry in reg["predictions"] + reg["assigned_texture_values"]:
        pid = entry["id"]
        check(f"{pid} frozen value recomputes from the axioms",
              vals[pid], mp.mpf(entry.get("frozen_value")), tol=REL_TOL)

    # (3) the conditional bands recompute at the declared N_star endpoints
    for entry in reg["conditional_bands"]:
        pid = entry["id"]
        lo, hi = vals[pid]
        check(f"{pid} band_min recomputes (N_star endpoint)",
              lo, mp.mpf(entry["band_min"]), tol=mp.mpf('1e-18'))
        check(f"{pid} band_max recomputes (N_star endpoint)",
              hi, mp.mpf(entry["band_max"]), tol=mp.mpf('1e-18'))

    # (4) theta_12 freeze discipline: exactly ONE prediction of record,
    #     and it is the seed variant 1/3 - phi0/2
    records = [e for e in reg["predictions"]
               if e.get("role") == "prediction_of_record"]
    check("exactly one theta_12 prediction of record in the registry",
          len(records), 1, exact=True)
    check("the prediction of record is the SEED variant 1/3 - phi0/2",
          records[0]["id"], "SIN2_THETA12_SEED", exact=True)

    # (5) the two variants are present but typed as derived variants
    #     (same texture), never as alternative predictions
    variant_ids = {e["id"] for e in reg["derived_variants_not_predictions"]}
    check("theta_12 seam + nonlin variants typed as derived (not predictions)",
          variant_ids == {"SIN2_THETA12_SEAM", "SIN2_THETA12_NONLIN"})
    pred_ids = {e["id"] for e in reg["predictions"]}
    check("no theta_12 variant leaked into the prediction list",
          len(variant_ids & pred_ids), 0, exact=True)
    for entry in reg["derived_variants_not_predictions"]:
        check(f"{entry['id']} variant value recomputes from the same texture",
              vals[entry["id"]], mp.mpf(entry["value"]), tol=REL_TOL)

    # (6) the three theta_12 numbers are distinct objects (must not be
    #     interchanged) and all sit within 0.1% of one another -- the very
    #     reason the freeze is needed before JUNO resolves the band
    seed = vals["SIN2_THETA12_SEED"]
    seam = vals["SIN2_THETA12_SEAM"]
    nonl = vals["SIN2_THETA12_NONLIN"]
    check("three distinct theta_12 values (seed < seam < nonlin)",
          seed < seam < nonl)
    check("variants within 0.1% of the frozen record (band JUNO will resolve)",
          max(abs(seam - seed), abs(nonl - seed)) / seed < mp.mpf('1e-3'))

    return summary("v84 frozen registry")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

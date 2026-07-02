"""Fetch + derive the committed burst-time tables for the repeater-cascade search.

Sources (all verified accessible 2026-07-02; see hypotheses/repeater_cascade_v1.yaml):

1. FRB 20220912A -- Zhang Y.-K. et al. 2023, ApJ 955, 142 (FAST, 1076 bursts).
   VizieR J/ApJ/955/142/table1.dat (fixed-width; barycentric MJD @ 1.5 GHz).
   -> data/frb20220912a_zhang2023.csv

2. FRB 20201124A -- two FAST episodes via the committed Blinkverse export in
   ../frb-tfpt-signatures/data/blinkverse_bursts.csv (blinkverse.top):
     * spring-2021: Xu H. et al. 2022, Nature 609, 685 (1863 bursts,
       reference DOI 10.1038/s41586-022-05071-8)
     * autumn-2021: Zhang Y.-K. et al. 2022, RAA 22, 124002 (881 bursts,
       reference DOI 10.1088/1674-4527/ac98f7)
   -> data/frb20201124a_fast.csv   (rows filtered by those two reference DOIs;
      the episode label is kept so sessions never mix provenance)

3. FRB 20240114A -- FAST polarization catalog (6134 bursts, MJD_topo at 1e-5 d),
   committed in ../frb-tfpt-signatures/data/FAST_FRB20240114A_pol_catalog_v5.csv.
   -> data/frb20240114a_fast.csv   (time resolution 0.86 s -- gated accordingly)

4. CHIME/FRB Catalog 2 repeaters -- CHIME/FRB Collaboration 2026, ApJS 283, 34;
   CANFAR archive doi:10.11570/25.0066 (the portal at chime-frb.ca/catalog2 was
   503 at fetch time; the vault host below is resolved via the CADC registry).
   -> data/chime_cat2_repeaters.csv  (repeater rows, sub_num=0, not excluded)

Anti double-counting: FRB 20220912A appears in Blinkverse AND CHIME Cat2; the
FAST leg uses ONLY the Zhang+2023 VizieR table, and the CHIME leg only CHIME-
detected bursts (different instrument + epochs), so no burst enters twice.
"""

from __future__ import annotations

import csv
import io
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
FRB_SIG_DATA = HERE.parents[2] / "experiments" / "frb-tfpt-signatures" / "data"
if not FRB_SIG_DATA.exists():  # script lives in experiments/repeater-cascade/scripts
    FRB_SIG_DATA = HERE.parents[1] / "frb-tfpt-signatures" / "data"

VIZIER_URL = "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/955/142/table1.dat"
VIZIER_README_URL = "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/955/142/ReadMe"
# vault host resolved via https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/reg/resource-caps
CANFAR_CSV_URL = ("https://cadc-west-01.canfar.net/vault/files/AstroDataCitationDOI/"
                  "CISTI.CANFAR/25.0066/data/table/chimefrbcat2.csv")

XU2022_DOI = "https://doi.org/10.1038/s41586-022-05071-8"
ZHANGYK2022_DOI = "https://doi.org/10.1088/1674-4527/ac98f7"


def _get(url: str) -> bytes:
    print(f"  GET {url}")
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def fetch_frb20220912a() -> None:
    raw = _get(VIZIER_URL).decode("ascii", errors="replace")
    out = DATA / "frb20220912a_zhang2023.csv"
    n = 0
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["burst_id", "mjd_bary", "fluence_jyms", "energy_1e36erg"])
        for line in raw.splitlines():
            if not line.strip():
                continue
            # fixed-width per the VizieR ReadMe: ID 1-4, MJD 6-20, Fluence 82-87, E 95-101
            w.writerow([line[0:4].strip(), line[5:20].strip(),
                        line[81:87].strip(), line[94:101].strip()])
            n += 1
    print(f"  -> {out} ({n} bursts)")
    (DATA / "frb20220912a_zhang2023_ReadMe.txt").write_bytes(_get(VIZIER_README_URL))


def fetch_frb20201124a() -> None:
    src = FRB_SIG_DATA / "blinkverse_bursts.csv"
    out = DATA / "frb20201124a_fast.csv"
    keep = {XU2022_DOI: "xu2022_spring", ZHANGYK2022_DOI: "zhangyk2022_autumn"}
    n = 0
    with src.open(encoding="utf-8") as fin, out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["episode", "mjd", "fluence_jyms", "energy_erg"])
        for row in csv.DictReader(fin):
            if row["source"] != "FRB20201124A":
                continue
            ref = (row.get("reference") or "").strip()
            if ref not in keep or not row["mjd"]:
                continue
            w.writerow([keep[ref], row["mjd"], row.get("fluence", ""), row.get("energy", "")])
            n += 1
    print(f"  -> {out} ({n} bursts from 2 FAST episodes)")


def fetch_frb20240114a() -> None:
    src = FRB_SIG_DATA / "FAST_FRB20240114A_pol_catalog_v5.csv"
    out = DATA / "frb20240114a_fast.csv"
    n = 0
    with src.open(encoding="utf-8") as fin, out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["burst_id", "mjd_topo", "snr"])
        for row in csv.DictReader(fin):
            if not row.get("MJD_topo"):
                continue
            w.writerow([row["BurstID"], row["MJD_topo"], row.get("S/N", "")])
            n += 1
    print(f"  -> {out} ({n} bursts)")


def fetch_chime_cat2() -> None:
    raw = _get(CANFAR_CSV_URL).decode("utf-8", errors="replace")
    out = DATA / "chime_cat2_repeaters.csv"
    n = 0
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["repeater_name", "tns_name", "mjd_400", "fluence_jyms", "excluded_flag"])
        for row in csv.DictReader(io.StringIO(raw)):
            rep = (row.get("repeater_name") or "").strip()
            if not rep or row.get("sub_num") != "0":
                continue
            w.writerow([rep, row["tns_name"], row["mjd_400"],
                        row.get("fluence", ""), row.get("excluded_flag", "")])
            n += 1
    print(f"  -> {out} ({n} repeater bursts, sub_num=0)")


def main() -> int:
    DATA.mkdir(exist_ok=True)
    steps = [("FRB 20220912A (VizieR J/ApJ/955/142)", fetch_frb20220912a),
             ("FRB 20201124A (Blinkverse: Xu+2022 + Zhang Y.-K.+2022)", fetch_frb20201124a),
             ("FRB 20240114A (FAST pol catalog)", fetch_frb20240114a),
             ("CHIME/FRB Catalog 2 repeaters (CANFAR doi:10.11570/25.0066)", fetch_chime_cat2)]
    failed = []
    for name, fn in steps:
        print(f"[fetch] {name}")
        try:
            fn()
        except Exception as e:  # noqa: BLE001  -- fetches must not kill each other
            print(f"  !! FAILED: {type(e).__name__}: {e}")
            failed.append(name)
    if failed:
        print("\nfetch incomplete (document as data_limited):", ", ".join(failed))
        return 1
    print("\nall fetches OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Fetch the NEGATIVE-CONTROL dataset: conventional Drude metals (Au, Cu), room temperature.

Source tables: M. A. Ordal et al., "Optical properties of Au, Ni, and Pb at submillimeter
wavelengths", Appl. Opt. 26, 744 (1987) [Au]; M. A. Ordal et al., "Optical properties of the
metals Al, Co, Cu, Au, Fe, Pb, Ni, Pd, Pt, Ag, Ti, and W in the infrared and far infrared",
Appl. Opt. 24, 4493 (1985) [Cu]. Machine-readable copies from the refractiveindex.info database
(public domain / CC0), tabulated n,k vs wavelength (um).

The real optical conductivity follows from eps2 = 2nk:
  sigma1[kS/cm] = 0.134518794412 * E[eV] * 2nk   (same conversion as the LSCO ingestion).

These are room-temperature (T=295 K assumed) far-IR/IR measurements dominated by intraband
(Drude) response -- the smooth sigma1(omega) rolloff on which the comb detector MUST stay quiet.

Usage:  python scripts/fetch_drude_control.py
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

BASE = ("https://raw.githubusercontent.com/polyanskiy/refractiveindex.info-database/"
        "master/database/data/main/{metal}/nk/Ordal.yml")
CITE = {
    "Au": "Ordal et al., Appl. Opt. 26, 744 (1987)",
    "Cu": "Ordal et al., Appl. Opt. 24, 4493 (1985)",
}
EV_UM = 1.2398419843320026        # E[eV] = EV_UM / lambda[um]
DATA = Path(__file__).resolve().parents[1] / "data"


def _parse_yaml_nk(text: str) -> list[tuple[float, float, float]]:
    """Parse the 'tabulated nk' block of a refractiveindex.info YAML file."""
    rows = []
    in_data = False
    for line in text.splitlines():
        if "data: |" in line:
            in_data = True
            continue
        if in_data:
            parts = line.split()
            if len(parts) != 3:
                break
            rows.append((float(parts[0]), float(parts[1]), float(parts[2])))
    return rows


def main() -> int:
    DATA.mkdir(exist_ok=True)
    for metal, cite in CITE.items():
        url = BASE.format(metal=metal)
        req = urllib.request.Request(url, headers={"User-Agent": "tfpt-smc-fetch/0.1"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            text = resp.read().decode("utf-8")
        rows = _parse_yaml_nk(text)
        if not rows:
            print(f"FAILED to parse {metal} table")
            return 1
        out = DATA / f"{metal.lower()}_ordal_nk.csv"
        lines = [f"# Source: {cite} [tabulated n,k]",
                 "# Machine-readable copy: refractiveindex.info database (CC0), "
                 f"data/main/{metal}/nk/Ordal.yml",
                 "# Room-temperature (T=295 K assumed) Drude-metal NEGATIVE CONTROL.",
                 "# E_eV,n,k"]
        for lam, n, k in rows:
            lines.append(f"{EV_UM / lam:.8g},{n:.6g},{k:.6g}")
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"  wrote {out}  ({len(rows)} rows, "
              f"E = {EV_UM / rows[-1][0]:.4g}..{EV_UM / rows[0][0]:.4g} eV)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

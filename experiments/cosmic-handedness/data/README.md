# Data — cosmic-handedness parity watchdog

`data/` is **gitignored** (`data/*`); only this `README.md` and `measurements.json` are
tracked. Reproducible from `measurements.json`.

## `measurements.json`

- **Shamir 2025 JWST/JADES** (MNRAS 538, 76): 263 galaxies with identifiable rotation,
  **158 counter-clockwise vs 105 clockwise** relative to the Milky Way (~50% excess). Shamir
  lists two readings: a universe "born rotating" (black-hole cosmology) or a Milky-Way
  rotation aberration.
- **Galaxy Zoo (Land+2008)** (MNRAS 388, 1686): after correcting human mirror-image vote
  bias, **consistent with isotropy** — the key counter-evidence.

## The monopole/dipole caveat (baked into the verdict)

A raw count asymmetry is a **monopole** (one handedness everywhere); an observer / Milky-Way
effect is a **dipole** (hemispheric). The aggregate counts here only give the monopole;
separating a *true global parity monopole* from an *MW-aberration dipole* needs sky-resolved
counts not encoded in this file. Hence **frontier / `data_limited`**, never a signal claim.

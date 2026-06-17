# cosmic-handedness — TFPT parity / galaxy-spin watchdog (frontier)

**Status: `data_limited` (frontier watchdog; most likely a systematic).**

A black-hole-cosmology child universe could inherit the parent black hole's spin, leaving a
global handedness imprint. TFPT carries a `μ₄` boundary clock and a `PSL(2,ℂ) ≅ SO⁺(3,1)`
boundary orientation, so it allows at most a **tiny** global orientation remnant — it predicts
**approximate parity**, *not* a ~20% handedness excess.

## Confrontation

| dataset | counts (ccw:cw) | monopole significance |
|---|---|---|
| Shamir 2025 JWST/JADES | 158 : 105 (×1.50) | ~3.3σ |
| Galaxy Zoo (Land+2008) | — | consistent with isotropy |

## Why this is a watchdog, not a prediction

1. **TFPT allows ≈ 0 asymmetry** (tiny boundary remnant), so a large robust excess is *not* a
   clean TFPT prediction; the parent-spin-inheritance reading is **frontier/conditional**.
2. **Monopole vs dipole.** A raw count excess is a *monopole*; a Milky-Way-rotation aberration
   is a *dipole*. The aggregate counts give only the monopole — separating a true global parity
   monopole from an MW-aberration dipole needs **sky-resolved counts** (not in this data).
   Shamir himself notes correcting for MW rotation may explain the excess, and Galaxy Zoo
   found isotropy.

This is exactly the reviewer's "cathedral on a pixel pile" warning made operational: the
channel is armed, but a ~3σ aggregate asymmetry of contested origin is **not** promoted.

## Frozen flag rule

```
a parity-odd global spin MONOPOLE surviving MW-aberration + selection systematics, replicated
across independent surveys -> promote to a frontier parent-spin candidate (never the core).
A pure dipole is a systematic, not a signal.
```

## Run

```bash
cd experiments/cosmic-handedness && PYTHONPATH=src python3 -m tfpt_handedness.cli analyze
```

## Firewall

Standalone frontier watchdog. Not in the verification suite, ledger, or website; no
load-bearing claim. TFPT predicts approximate parity; this channel only watches whether a
robust, systematics-clean global spin monopole ever appears.

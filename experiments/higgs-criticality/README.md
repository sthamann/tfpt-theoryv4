# higgs-criticality — TFPT double-critical-surface watchdog

**Status: `consistent` (downstream RGE bridge [C]).**

TFPT's gravity/inflation branch sits on the **double-critical surface**: at the Planck scale
both the Higgs quartic and its β-function vanish,

```
lambda(M_Pl) = 0   AND   beta_lambda(M_Pl) = 0.
```

This watchdog extrapolates the measured SM couplings to `M_Pl` with the Buttazzo et al. 2013
(arXiv:1307.3536) NNLO fit (eq. 61), computes the 1-loop `β_λ(M_Pl)` from those couplings,
propagates the `(M_t, M_h, α_s)` uncertainties, and reports the **pull to the double-critical
surface**.

## Result (2026-06-15)

| quantity | value |
|---|---|
| `λ(M_Pl)` | −0.0143 ± 0.0057 |
| `β_λ(M_Pl)` (1-loop) | +1.9×10⁻⁴ |
| pull to `λ=0` | −2.5σ (metastable) |
| published metastability | 2.8σ (eq. 65) |
| dominant uncertainty | `M_t` |

Both `λ(M_Pl)` and `β_λ(M_Pl)` are **remarkably small** — the SM lands right next to the
double-critical surface. `λ` sits ~2.5σ below zero (metastable vacuum), reproducing the
published significance. The verdict is dominated by the top mass, so a sharper `M_t` is the
discriminating input.

## Firewall

Downstream **RGE bridge [C]**, not a primitive compiler output. The Frontier text forbids
turning QCD/cosmology transfers into compiler outputs; near-criticality is a *consistency*
statement about where the measured SM lands, not a TFPT-derived number. Standalone; not in the
verification suite, ledger or website.

## Run

```bash
cd experiments/higgs-criticality && PYTHONPATH=src python3 -m tfpt_higgs.cli analyze
```

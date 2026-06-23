# Seam Emergence & Circularity Probe

> Classical precursor to the fault-tolerant-quantum "Mobius seam" test. Firewall: a search/audit
> tool, **not** a load-bearing TFPT claim. It decides, *before* any quantum experiment is built,
> which seam quantity is a **non-circular** test and which is **circular** (answer baked into the
> inputs) — the difference between a real FT-hardware experiment and an expensive tautology.

The honest version of "does `A/4` / `(2/3)⁶` emerge, or is it defined in?" — with an explicit
**input → forced → output** ledger and **negative controls**.

```bash
python seam_emergence.py
```

## What it finds

**PART 1 — `(2/3)⁶` genuinely EMERGES (non-circular).** From the two axioms *only*
(`|μ₄|=4`, `g_car=5`):
- topology forces `N_fam = |μ₄|−1 = 3` (rank `H¹(ℙ¹∖μ₄)`),
- counting forces `Z₂ = g_car−N_fam = 2`,
- Lie theory forces the hand length `|R⁺(A₃)| = 6`,
- a **generic** Perron–Frobenius relaxation (one absorbing attractor + a democratic surviving
  block of size `Z₂`) yields survival `Z₂/N_fam = 2/3` — its second eigenvalue *emerges* (0.6667),
  it is **not** the inserted cusp weights `{0,1/3,2/3}`,
- so `rate = (Z₂/N_fam)^hand = (2/3)⁶ = 64/729`.

Negative controls show it is **forced, not a free dial**: `|μ₄|=5 → (1/4)¹⁰`; `g_car=4 → (1/3)⁶`
(the *other* transfer eigenvalue!); `g_car=6 → no gap`. The physical window is tight. The single
modelling assumption is "relaxation to a unique attractor with a democratic block" — everything
else is forced. → **This is the test worth scaling to FT hardware** (deep coherence beats the NISQ
range-blindness measured on `ibm_fez`).

**PART 2 — `A/4` is PARTLY CIRCULAR.** An exact stabiliser-entanglement computation (1D cluster
state) shows the **area law** `S ∝ boundary` emerges generically (S = 2 bits, constant in block
size) — but that is true of *any* gapped state, not TFPT-specific. The **1/4 coefficient does not
emerge**: a bare discrete boundary gives 1 bit per cut, not 1/4. The `1/4` is the seam
normalisation `c₃ = 1/(8π)`, itself *defined* from the `8π` Gauss–Bonnet. → To make the future
quantum seam test non-circular, the `1/4` must come from microscopic seam state-counting **without**
assuming the `8π` normalisation.
```

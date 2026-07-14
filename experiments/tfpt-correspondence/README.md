# tfpt-correspondence — spacetime ↔ black hole as an **atom-locked phase boundary**

**Status: `consistent` / `[C]` (structural), gated on the OPEN Seam–Horizon theorem
`SEAM.EQUIV.01`. Not load-bearing, not in the scorecard.**

A preregistered **internal-consistency** search target for a TFPT-native *correspondence
principle*: the seam is one underlying state with **two channel-readouts** —

- **geometry channel** → ordinary spacetime (emergent Einstein equation, `v358`/`v359`);
- **boundary / information channel** → the compiler (boundary data, the finite recovery
  code `v221`/`v54`).

At low information density the geometry channel is the natural description (spacetime);
when the information density **saturates the holographic bound**, the *same* state is
described as a **black hole**. The event horizon is then the **saturation locus of an order
parameter**, not a fundamental edge — a *change of bookkeeping*, in TFPT's own language.

The one question this target asks: **does TFPT's algebra place the phase boundary on
compiler atoms, or would it need a free number?** (If free → numerology, rejected.)

## The two dimensionless order parameters

| | definition | critical / window | atom identity |
|---|---|---|---|
| **(A) Bekenstein saturation** | `q_Bek = 4·c₃·S/(E·R)` | `q_Bek = 1` at the horizon | coeff `4c₃ = 1/(2π)`; density `1/4 = 1/\|μ₄\|` |
| **(B) SdS compactness** | `Q_geom(m)=Σrᵢ²/(Σ\|rᵢ\|)²`, cubic `t³−3t+6m` | `[3/8, 1/2]`, monotone | `1/2 = \|Z₂\|/\|μ₄\|`, `3/8 = p₂(a)/e₁(a)²` |

A Schwarzschild hole (`S = A/4 = 4πM²`, `E = M`, `R = 2M`) sits at **`q_Bek = 1` exactly,
independent of `M`** — the horizon *is* the saturation point. Order parameter (B) is the
**geometric face** of the same boundary; its `3/8` rung and the ECO echo template already
live in [`gravastar-compactness`](../gravastar-compactness/) — this target only reuses the
window, it does not re-derive it.

## What the runner checks (`hypotheses/correspondence_v1.yaml`)

- **`CORR.H1` atom-lock (decisive).** The four boundary constants `{1/4, 1/2, 3/8, (2/3)⁶}`
  and the coefficient `4c₃ = 1/(2π)` are **exact atom rationals**, not fits.
- **`CORR.H2` saturation self-consistency.** `q_Bek(horizon) = 1` and `S_BH = A/4` for every
  mass, with the atom coefficient.
- **`CORR.H3` geometric window.** `Q_geom` runs monotonically over `[3/8, 1/2]` with
  `1/3 < 3/8 < 4/9 < 1/2` (photon sphere / Buchdahl / horizon).
- **`CORR.H4` gate & no-new-state (typing guard).** Records the `[O]` dependency on
  `SEAM.EQUIV.01`; asserts the kernel is atom-only + `π` with **no Hagedorn/string scale**.
- **`CORR.H5` observable echo (C).** The geometric phase boundary `Q_geom = 3/8` is a
  horizonless light-trapping ECO → a ringdown-echo source. The correspondence fixes the echo
  **delay** (~0.70 ms for a 62 M☉ remnant, source frame; `2.288 M`) and the **amplitude bound
  `≤ (2/3)⁶`** (= the recovery reflectivity = the information-channel order parameter). This
  inherits the existing null / `data_limited` verdicts of
  [`gw-ringdown-echo`](../gw-ringdown-echo/) (strain search) and
  [`gravastar-compactness`](../gravastar-compactness/) (delay).

## Two follow-ups wired in

- **(B) Attack the open bolt.** [`../theory-contracts/corr_seam_orbifold_forcing.py`](../theory-contracts/corr_seam_orbifold_forcing.py)
  (5/5) sharpens `SEAM.EQUIV.01` to a **conditional forcing theorem**: *if* the seam realises
  any `ℂ²/Γ` orbifold, then the seam's own atoms `(|Z₂|, N_fam, g_car) = (2,3,5)` — the
  icosahedral signature — force `Γ = 2I`, and `det K = 1` (E8, the unique ADE Poincaré-sphere
  link) follows. So the whole keystone is the **single open arrow** `seam ≅ orbifold`;
  everything else is a theorem. `[E]` for the arithmetic, premise stays `[O]` — **not closed**.
- **(C) Make it observable.** The `CORR.H5` echo template above is the only measurable hook;
  an echo hit → the phase boundary is physically realised; a clean null → only the
  "physically visible" reading falls (the bookkeeping survives).

## Signature coverage across all data sources (`scripts/signature_coverage.py`)

Auditing every experiment against the correspondence signatures (`S1` recovery reflectivity
`(2/3)⁶`, `S2` compactness window `[3/8,1/2]`, `S3` `C=3/8` ECO echo, `S4` Bekenstein
saturation) shows they are **already tested** — **17 experiment legs**, all
**null / data_limited / consistent** (grounded live from each experiment's `results.json`):

- **S1** → `frb-tfpt-signatures`, `pulsar-glitch-recovery`, `recovery-comb-domains`,
  `repeater-cascade`, `crust-cooling-comb`, `uhecr-energy-dsi`, `strange-metal-comb`,
  `qpe-recurrence`, `hfqpo-ladder`, `comb-meta-limit`, `recovery-channel`, `qc-recovery-kernel`.
- **S2** → `gravastar-compactness`; `eht-achromatic-residual` (shadow **degenerate** with Kerr).
- **S3** → `gw-ringdown-echo` (Stage 1d `NO_POINT_ECHO` at the `2.288 M` lag × `(2/3)⁶`; Stage 1h ε₉₀).
- **S4** → structural (this experiment); **not** a data channel.

**Anti-double-counting:** the correspondence adds **no independent evidence channel** — its
signatures *are* the frozen kernel the suite already probes, so it contributes **zero**
scorecard weight (it re-interprets, it does not re-measure). The one near-term lever is the
**echo reach-gap**: the `(2/3)⁶ = 0.088` ceiling sits **~7.2× below** the current best
`gw-ringdown-echo` ε₉₀ stack limit (`0.63`).

**Data-source update (checked 2026-07-14):** that ~7.2× is the TFPT pipeline's *conservative*
stack, which **under-uses `GW250114`** (2025-01-14, loudest BBH to date: network SNR ~80,
**post-merger SNR ~40 ≈ 3× GW150914**; LVK find no coherent post-ringdown power, residual
network SNR **< 6.86** at 90% CL). Grounding on that event gives a per-event amplitude reach
**~0.17 (~2×** above `0.088`, **not 7×**) — so **re-anchoring `GW250114`** (public on GWOSC,
currently ε₉₀=15.9 from a weak A220 fit) **+ the pending O4c/GWTC-6 stack** is the near-term
path; a large **O5** (2028–31) stack or one **next-gen (ET/CE)** event reaches `0.088`
comfortably. **Regime caveat:** standard echo searches (e.g. arXiv:2512.24730) target *strong*
reflection (`R_wall≈0.99`, long-lived QNM trains) — the **wrong** regime for TFPT's *weak*
`(2/3)⁶` reflector; the right instrument is the targeted first-echo bound at the `2.288 M` lag
(`gw-ringdown-echo` Stage 1d/1h). Full landscape in `results/signature_coverage.json`.

```bash
python3 scripts/signature_coverage.py          # -> results/signature_coverage.json
```

## Run

```bash
cd experiments/tfpt-correspondence
PYTHONPATH=src python3 -m tfpt_correspondence.cli analyze     # writes results/results.json
PYTHONPATH=src python3 tests/test_frozen_kernel.py            # frozen-kernel guard (6/6)

# (B) the keystone forcing contract (theory-contract, out of scorecard):
cd ../theory-contracts && python3 corr_seam_orbifold_forcing.py   # 5/5
```

## Verdict (honest)

A **structural `[C]` correspondence**: the phase-boundary constants **are** atom-locked
(internal consistency confirmed), so the reading survives the numerology test — **but the
physical spacetime↔black-hole phase transition stays `data_limited` / `[O]`-gated** on the
still-open Seam–Horizon theorem. It can never exceed `[C]` until `SEAM.EQUIV.01` closes.

## Firewall

Standalone **change-of-bookkeeping** structural search. **Not** new gravitational physics,
**not** a detection, **not** in the verification suite / ledger / website, and **out of the
evidence scorecard** (internal consistency, like `theory-contracts/`). Downstream of the
open `SEAM.EQUIV.01`; typed at most `[C]`, never `[E]`, no `\veri{}` citation.

Two hard TFPT constraints are baked into the preregistration:

1. **No-new-state (`v246`) + No-Unit theorem (`v153`):** the "phase transition" may **not**
   introduce a new scale or mechanism; it must be a re-description forced by existing atoms,
   or it stays `[C]`/`[O]`.
2. **This is *not* Horowitz–Polchinski.** TFPT has **no Hagedorn temperature and no string
   scale**, so the shared content is only *"one state, two equivalent descriptions across a
   threshold"* — never the HP self-gravitating-string transition dynamics.

Narrative home if ever promoted: a keybox in `tfpt_research_contracts.tex` (a `[C]` reading),
**never** a verification-ledger empirical row.

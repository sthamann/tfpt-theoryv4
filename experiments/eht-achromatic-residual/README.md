# TFPT Achromatic Residual Pipeline (EHT / ngEHT)

A reproducible Python pipeline for the **achromatic, dyonic residual
intercept test** of TFPT Paper 3 §3 ("Remark on the dyonic intercept
and the α-kernel"). The pipeline:

1. fits a per-pixel Faraday-rotation model
   `χ(λ²) = χ₀(x) + RM(x)·λ² + ε` to a polarimetric image cube,
2. subtracts the GRMHD/synchrotron forward model to obtain the residual
   intercept `χ₀^res(x) = χ₀^obs(x) − χ₀^GRMHD(x)`,
3. runs **three independent null tests** on the residual:

   * **frequency null** — `χ₀^res` is achromatic (no λ² dependence),
   * **profile null** — `χ₀^res(r) ∝ 1/r²` around the photon ring,
   * **sign-flip null** — `χ₀^res` flips sign under reversal of the
     effective `E·B` orientation,
4. reports a `DETECTION` flag only if **all three nulls** are passed
   simultaneously.

The TFPT prediction is:

```
β_BH(r)  =  (Q_e_eff · Q_m_eff) / (256 · π⁴ · r²)
         =  16 · c₃⁴ · Q_e_eff · Q_m_eff / r²
         =  (δ_top / 3) · Q_e_eff · Q_m_eff / r²
```

where the coupling `1/(256π⁴) = 16·(1/(8π))⁴` is **fixed** by the same
TFPT branch data that fixes the fine-structure constant α and the global
cosmic-birefringence amplitude `β_rad = 0.2424°`. Only the geometric
weights `Q_e_eff, Q_m_eff` and the emission radius are model-dependent.

## Why this matters

The achromatic intercept is the **cleanest local astrophysical
falsification surface** of the TFPT determinant-line response. Unlike
the global birefringence amplitude `β = 0.2424°`, which lives on the
CMB sky, the EHT signal:

* is spatially structured (`1/r²` around the photon ring), so it
  cannot be absorbed into a global instrument calibration;
* is frequency-independent (achromatic), so it cannot be confused with
  Faraday rotation, which scales as `λ²`;
* changes sign under `E·B` reversal, so it cannot be confused with a
  static systematic such as a polarization-leakage term.

Three orthogonal nulls must be passed *simultaneously* for a positive
detection. That is the strongest non-cosmological test of the TFPT
determinant-line sector available today.

## Repository layout

```
eht-achromatic-residual/
├── pyproject.toml          # Hatch-based build, pinned deps
├── README.md               # this file
├── src/tfpt_eht/
│   ├── __init__.py
│   ├── constants.py        # φ₀, c₃, δ_top, TFPT_COUPLING (no SI inputs)
│   ├── model.py            # β_BH(r) and chi0_tfpt prediction map
│   ├── residual.py         # Faraday RM fit + radial deprojection
│   ├── null_tests.py       # the three nulls + combined report
│   ├── synthetic.py        # synthetic data generators
│   ├── plotting.py         # matplotlib helpers used by notebooks
│   └── cli.py              # `tfpt-eht audit` and `tfpt-eht demo`
├── tests/
│   ├── test_constants.py   # 4 equivalent TFPT coupling expressions agree
│   ├── test_model.py       # 1/r² scaling, geometric weights, sign flip
│   ├── test_residual.py    # RM fit + radial deprojection on truth
│   └── test_pipeline.py    # injected-signal detection / null rejection
├── notebooks/
│   ├── 01_tfpt_prediction.ipynb       # visualize the prediction
│   ├── 02_synthetic_pipeline.ipynb    # end-to-end on synthetic data
│   └── 03_eht_public_data.ipynb       # template for real EHT data
├── data/
│   └── README.md           # how to obtain EHT public polarimetric data
└── results/                # outputs land here
```

## Install

```bash
cd experiments/eht-achromatic-residual
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,notebooks]"
```

Dependencies are pinned in `pyproject.toml`: NumPy, SciPy, pandas,
matplotlib for the core; pytest + ruff for development; JupyterLab for
the notebooks.

## Run the tests

```bash
pytest -v
```

The test suite validates:

* **`test_constants.py`** — the four equivalent algebraic expressions
  for the TFPT coupling (`1/(256π⁴) = 16·c₃⁴ = δ_top/3 =
  TFPT_COUPLING`) all agree to machine precision. *If this drifts,
  the no-knobs claim is violated.*
* **`test_model.py`** — the model is exactly `1/r²`, scales linearly in
  `Q_e_eff · Q_m_eff`, and flips sign under sign-orientation reversal.
* **`test_residual.py`** — the per-pixel RM fit recovers the truth
  intercept and rotation measure on a uniform-truth cube; the radial
  deprojection recovers the slope `-2` for a `1/r²` field.
* **`test_pipeline.py`** — three end-to-end synthetic experiments:
  * a cube with TFPT signal → all three nulls fire, `DETECTION`;
  * a null cube → no detection;
  * a cube with a constant calibration-error offset → the structural
    nulls (profile and sign-flip) reject, no detection.

## Run the demo

```bash
tfpt-eht audit
tfpt-eht demo --case signal
tfpt-eht demo --case null
tfpt-eht demo --case systematic
```

The `audit` command prints the constants and confirms the four
expressions of the TFPT coupling agree. The `demo` commands run the
full pipeline on a synthetic cube of the chosen class and print the
three-null report.

## Use on real EHT data

The pipeline is data-agnostic. To run it on real EHT data:

1. Obtain the EHT 2018 polarimetric data release for M87* or Sgr A*
   from [eventhorizontelescope.org](https://eventhorizontelescope.org)
   (see `data/README.md` for the current URLs).
2. Build a `PolarimetricImage(x, y, lambda_sq, chi, sigma_chi)` from
   the multi-frequency reconstructions, with coordinates in units of
   the gravitational radius `r_g = G·M/c²`.
3. Run the official EHT GRMHD library (e.g. `ipole`) to produce the
   GRMHD-truth intercept map `χ₀^GRMHD(x)`. Repeat with the opposite
   effective `E·B` sign for the third null.
4. Call `rotation_measure_fit`, `compute_residual_intercept`,
   `deproject_radial`, and `run_all_nulls`. The output is a single
   `NullTestReport` with a binary `detection` flag.

## Self-consistency between this and Paper 3

The Lean 4 carrier-rigidity formalization (sibling experiment
`lean4-carrier-rigidity/`) proves the *algebraic* origin of `c₃` and
the carrier polynomial. This Python pipeline assumes those theorems and
uses the numerical values `c₃ = 1/(8π)` and `φ₀ = 1/(6π) + 3/(256π⁴)`
as **derived inputs** — the same way TFPT Paper 3 itself derives the
EHT amplitude from the closed branch. The test
`test_constants.py::test_tfpt_coupling_three_expressions_agree` is the
algebraic shadow of the same identity.

## Caveats

* The synthetic GRMHD mock in `synthetic.py` is deliberately
  *simplistic*: axisymmetric, no relativistic boosting, no realistic
  source structure. It is *not* a stand-in for a real GRMHD code. Its
  only purpose is to validate that the pipeline logic correctly
  detects an injected signal and correctly rejects systematics.
* The three nulls are necessary but not sufficient: a false positive
  could arise from a systematic that happens to be achromatic, follow
  `1/r²`, and flip sign under `E·B` reversal. The TFPT prediction's
  *amplitude* `1/(256π⁴) · Q_e_eff · Q_m_eff` provides a further
  check that the pipeline reports as part of the `profile_null`
  detail (`amplitude_fit / amplitude_expected`).
* Astrophysical degeneracies with the GRMHD forward model must be
  declared as part of the comparison convention. Different GRMHD
  back-ends will yield different `χ₀^GRMHD` maps; this is captured by
  the data dependency of the residual.

## License

MIT (see `pyproject.toml`).

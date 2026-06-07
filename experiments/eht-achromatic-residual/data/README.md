# Data

The pipeline runs on a `PolarimetricImage` instance plus a GRMHD
forward-model cube. The two sources below cover the public material
needed to perform the test on M87\* and Sgr A\*.

## Event Horizon Telescope public releases

* **M87\* 2017** (April 2017 campaign) — polarimetric reconstructions
  released in 2021: <https://datacommons.cyverse.org/browse/iplant/home/shared/commons_repo/curated/EHTC_FirstM87Results_April2019>
* **M87\* 2018** (April 2018 campaign) — released 2024:
  <https://www.eventhorizontelescope.org/for-astronomers/data>
* **Sgr A\*** — polarimetric release 2024:
  <https://www.eventhorizontelescope.org/for-astronomers/data>

Each release ships FITS files per frequency channel. Convert them to a
`PolarimetricImage(x, y, lambda_sq, chi, sigma_chi)` where:

* `x, y` are in units of the gravitational radius
  `r_g = G M / c^2`. For M87\* use `M = 6.5e9 M_sun`; for Sgr A\* use
  `M = 4.0e6 M_sun`.
* `chi` is the linear-polarization angle in radians, derived from the
  Stokes parameters as `0.5 * arctan2(U, Q)`.
* `sigma_chi` follows from the per-pixel `Q, U` covariance via the
  standard propagation `sigma_chi = 0.5 * sqrt(Q^2 sigma_U^2 + U^2
  sigma_Q^2) / (Q^2 + U^2)`.

## GRMHD forward model

The achromatic-residual test requires a GRMHD model evaluated at the
same frequencies as the EHT cube. Standard public radiative-transfer
back-ends:

* **`ipole`** (Mościbrodzka & Gammie 2018) —
  <https://github.com/AFD-Illinois/ipole>
* **`harmpi`** + `radpol` (Ressler et al.) —
  <https://github.com/atchekho/harmpi>
* **`grtrans`** (Dexter & Agol 2009) —
  <https://github.com/jadexter/grtrans>

For a first pass the *EHT GRMHD M87 image library* (2021 release)
provides ready-made polarimetric images for hundreds of MAD/SANE
models at 230 GHz. To run the multi-frequency null you will need to
re-render the chosen models at additional frequencies (typically 230,
345 GHz; 86 GHz is too low for the standard EHT array).

Once you have:

* `chi_grmhd : np.ndarray  # shape (F, H, W)`  — full model cube,
* `chi_0_grmhd : np.ndarray  # shape (H, W)`   — intercept of the
                                                   lambda^2 fit on the model,

you can run the pipeline as in `notebooks/03_eht_public_data.ipynb`.

## Sign-flip protocol

The third null test requires the same observation analysed under two
opposite assumptions for the effective `E.B` orientation in the
emission region. Practically this means:

1. Use the GRMHD model with magnetic-field direction `B_hat`.
2. Re-render the *same* GRMHD snapshot with `-B_hat` (i.e. swap MAD
   field polarity, or invert the sign of `b^mu` in the radiative
   transfer step).

The TFPT prediction is that the residual flips sign; an astrophysical
systematic typically does not.

## Storage

The `data/` directory in this repository is intentionally empty (only
this README). Public EHT cubes are several GB each and are not redistributed;
download them yourself and set the paths in
`notebooks/03_eht_public_data.ipynb`.

# Quantum recovery analog — PARKED

```
status               = parked
reason               = analog risk, no direct physical dataset
activation_condition = a real boundary-recovery experiment with a measurable
                       per-step recovery quantity (mutual information I_n, fidelity
                       recovery, or conditional mutual information) decaying by the
                       frozen kernel ratio 64/729 per step
```

`search.txt` §10. If TFPT is taken very literally, the central dynamical signature is
a recovery/decay with the **frozen** transfer eigenvalue per step,

```
I_n  ∼  ((2/3)^6)^n  =  (64/729)^n .
```

This is **not** a cosmological test — at best a clean *analog* test of the boundary
recovery kernel in an engineered system (quantum error correction, scrambling, echo
protocols, random-circuit recovery). It is **deliberately not built**: with no direct
physical dataset it slides too easily into "analogy without physics". It is recorded
here only so the domain matrix stays honest:

> **9 active empirical domains + 1 parked analog target.**

## Activation

Build this experiment only when a dataset with a genuine per-step boundary-recovery
observable exists. Then the test is: does any channel's `I_n` / fidelity recovery /
CMI fall by `64/729` per step, calibrated against scrambling-null surrogates and a
free-ratio control (the same anti-numerology gate as FRB.02b)?

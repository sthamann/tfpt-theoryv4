# TFPT QNM family-count — `ω_R/T_H → ln3 = ln N_fam` (black-hole-direct)

The **schwarzloch-direkte** recovery signature (`v57`, `horizon_readouts`): the
asymptotic high-overtone Schwarzschild quasinormal real frequency satisfies
`ω_R → T_H ln3`, so

```
ω_R / T_H → ln 3 = ln N_fam          (the ringdown carries the family count)
area quantum  ΔA = 4 ln3 · l_p² = ln(N_fam⁴) = ln 81
```

The numerical identity `ln3 = ln N_fam` is exact; the black-hole identification is
`[C]/[P]` (Hod's "3" is spin-dependent — suggestive, not forced).

## Result — structural identity, but **data-limited**

- `ln3 = ln N_fam` exactly; `4 ln3 = ln 81 = ln(N_fam⁴)` (= ln of the flavor-cover
  discriminant).
- The Hod limit `M·ω_R → ln3/(8π) = 0.0437` is the **n→∞** overtone limit; the measured
  fundamental is `M·ω_220 ≈ 0.3737` — a factor ~8.5 away. Measured ringdowns (GW150914,
  GW250114) see the **n=0** mode, not the asymptotic ln3 regime.

→ **data-limited**: the structure carries `ln3 = ln N_fam`, but the direct family-count
test needs **high-overtone ringdown spectroscopy** not accessible at current SNR. The
most physically-direct black-hole recovery signature — and the one furthest from being
testable today.

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .
tfpt-ringdown analyze    # or: PYTHONPATH=src python -m tfpt_ringdown.cli analyze
```

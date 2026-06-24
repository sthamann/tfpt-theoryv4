# TFPT extended signatures

Preregistered **extended** empirical searches beyond the core `search.txt` five-type
catalog: joint FRB/GW templates, horizon compiler fingerprints, Galois-CP + J_PMNS,
extended seed shadows, and dynamic recovery probes.

> **Firewall:** search targets / downstream bridges only — never load-bearing claims.

## Probes (EXT.1–EXT.7)

| ID | Module | Signature | Status |
|---|---|---|---|
| EXT.1 | `frb_joint.py` | Echo quotient **and** mu4/PA in the **same** FRB source | per-source Fisher |
| EXT.2 | `frb_anyon.py` | Anyon **pi/4** comb on EVPA (QT.05 reinterpretation) | injection + real PA |
| EXT.3 | `gw_joint.py` | Gravastar **lag 0.7 ms** + amplitude **<= (2/3)^6** jointly | injection validated |
| EXT.4 | `horizon.py` | Scrambling x4, Hawking/1920, area 4ln3, QNM ln3 catalog | structural / data_limited |
| EXT.5 | `galois_cp.py` | J_PMNS + joint delta_CKM/delta_PMNS band 240+/-9 | NuFIT confrontation |
| EXT.6 | `seed_extended.py` | xi=c3/phi0 + BBN shadow legs (no extra DOF) | extends seed-consistency |
| EXT.7 | `dynamic_probes.py` | Walled-clock MF on Crab nu(t); FRB repeater gap clock | Vela still open |

## Run

```bash
cd experiments/extended-signatures
python -m venv .venv && . .venv/bin/activate && pip install -e .
tfpt-ext audit
tfpt-ext analyze --seed 0
```

Real FRB/GW/pulsar legs need the sibling experiment data (FAST/Blinkverse, GWOSC strain,
`pulsar-glitch-recovery/data/crab_ephemeris.csv`). Missing files → honest `data_limited`.

Results: `results/results.json`. Scorecard rows: `experiments/build_evidence_scorecard.py`.

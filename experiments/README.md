# TFPT Experiments

Reproduzierbare Build-Targets, die Aspekte der TFPT-Theorie beweisen, simulieren oder
operationalisieren. Jedes Unterprojekt ist eigenständig und hat sein eigenes README
mit Setup- und Run-Anleitung.

## Inhalt

| Ordner | Zweck | Status |
| --- | --- | --- |
| `lean4-carrier-rigidity/` | Maschineller Beweis des Carrier-Polynoms `6Y² − Y − 1 = 0` und der Hyperladungs-Spur in Lean 4. Macht das zentrale Theorem aus Paper 2 als formal verifiziertes Computer-Theorem verfügbar. | aktiv |
| `eht-achromatic-residual/` | Python-Pipeline für den achromatischen, dyonischen Residual-Test aus Paper 3 (`β_BH(r) ~ 16 c₃⁴ Q_e Q_m / r²`). Generiert synthetische EHT-Daten, führt drei unabhängige Null-Tests durch und ist auf reale EHT-Daten skalierbar. **(search.txt §4: EHT-Horizon-Collar)** | aktiv |
| `frb-tfpt-signatures/` | Preregistrierte, multi-Source, surrogat-kalibrierte Suche nach residualen Boundary-Recovery-Signaturen in echten FRB-Daten (FRB.01 native Dispersion · FRB.02/02b Echo-Quotienten + Free-Quotient-Null · FRB.03–04/08 Polarisation/μ4 · FRB.09 Recovery-Clock). **(search.txt §1,2,6)** Verdict: `not_confirmed_not_refuted`. | aktiv |
| `cmb-birefringence-seed/` | Cross-Domain-Seed-Linie: ein `φ₀` sagt Doppelbrechung `β = 0.2424°` **und** Baryon-Fraktion `Ω_b = (4π−1)β_rad` voraus; vier Modi (`beta_only/omega_b_only/joint_independent/joint_covariance_placeholder`) + Unit-Guard gegen `Ω_b` vs `Ω_b h²`. **(search.txt §3, Prio 1)** Verdict: **konsistent mit der Seed-Linie** (β 0.37σ, Ω_b 0.04σ BBN, Linie 0.35σ; keine kombinierte Signifikanz). | aktiv |
| `lab-residuals/` | `F_transfer`-Laborkanäle, alle **[C]**: Myon g−2 (`Δaµ = 45/(2¹⁹π⁹)`, **pro SM-Baseline** gesplittet), seltene Kaonen (`K⁺→π⁺νν`), Axion (Marker + Hilltop/Spine-Branch). **(search.txt §7,8,9)** Ergebnis: Kaon **downstream bridge, sehr starke Konsistenz mit NA62 2016–2024 (−0.08σ)**, g−2 baseline-abhängig (viable dispersiv / tension lattice), Axion datenlimitiert. | aktiv |
| `gw-ringdown-echo/` | TFPT-Ringdown-Echo-Amplitudenquotient `≤ (2/3)⁶`: **Sensitivity-Census auf Katalogebene** (GWTC-5.0, 390 kanonische Events; lokale Rohzeilenzahl 391 separat in `event_count_audit.md` auditiert). **(search.txt §5)** Stacked echo-SNR ≈ 6.3 → **Strain-Level-Test offen**, kein Echo-Claim auf Katalogebene. | aktiv (Stage 0) |
| `quantum-recovery-analog/` | **Geparkt**: Analog-Recovery `I_n ~ (64/729)^n`. Kein direkter physischer Datensatz → bewusst nicht gebaut. **(search.txt §10)** | geparkt |
| `ftransfer/` | Theorieseitige `F_transfer`-Solver (Axion-Relik, Koide-Source-to-Pole, Leptogenese-Boltzmann, QCD-Matching `m_p/m_e`). | aktiv |

## Empirische Coverage (search.txt)

**9 aktive empirische Suchräume plus 1 geparkter Analograum.** Die zentrale,
getypte Übersicht aller (Domäne, Observable)-Zeilen liegt in
[`evidence_scorecard.json`](evidence_scorecard.json) (generiert von
`build_evidence_scorecard.py`); jede Zeile trägt `claim_type`, `bridge_type`,
`stage` und `status` aus festen Enums, damit nichts still nach `[E]` hochgestuft
wird. Aktueller Stand: 6 `consistent`, 7 `null`, 1 `hint`, 5 `data_limited`,
2 `tension`, 1 `parked`. Schärfste Konsistenzpunkte: CMB `β`/`Ω_b`/Seed-Linie
(0.35–0.04σ, `prediction_of_record`) und das seltene Kaon `K⁺→π⁺νν` (−0.08σ,
`downstream_bridge`).

## Konventionen

* Jedes Experiment ist self-contained: eigene Abhängigkeiten, eigener Build, eigene
  CLI als Audit-Surface (`<pkg>.cli analyze`).
* Keine SI-Werte werden als versteckte Eingabe importiert — alles fließt aus den
  TFPT-Axiomen (`φ₀ = 1/(6π) + 3/(256π⁴)`, `c₃ = 1/(8π)`, Carrier-Polynom).
* **Firewall / Typing:** Frontier-Observablen (Koide, η_B, Axion, `m_p/m_e`, g−2,
  Kaonen) sind `F_transfer`-Interfaces bzw. downstream bridges — **nie** primitive
  Compiler-Outputs. Status wird pro SM-Baseline / Branch gesplittet, kein einzelnes
  Ampel-Urteil über Modellannahmen hinweg.

# TFPT Experiments

Reproduzierbare Build-Targets, die Aspekte der TFPT-Theorie beweisen, simulieren oder
**empirisch gegen echte, öffentliche Daten** testen. Jedes Unterprojekt ist
eigenständig (eigene Abhängigkeiten, eigener Build, eigene CLI als Audit-Surface) und
hat ein eigenes README mit Setup-, Run- und Detailbeschreibung. Dieses Dokument ist
die **Gesamtübersicht aller Untersuchungen, Tests, Datenquellen und Ergebnisse**.

> **Firewall (gilt überall):** Diese Experimente sind **Suchflächen und
> Konsistenz-Checks**, keine load-bearing Claims. FRBs/Echos/Horizont-Signale sind
> *residuale Boundary-Recovery-Muster*, **nicht** neue Gravitation und **nicht** direkte
> Hawking-Strahlung. Frontier-Observablen (Koide, η_B, Axion, `m_p/m_e`, g−2, Kaonen)
> sind `F_transfer`-Interfaces bzw. *downstream bridges* — **nie** primitive
> Compiler-Outputs. Nichts wird still nach `[E]` hochgestuft.

---

## Inhalt

| Ordner | Zweck | Status |
| --- | --- | --- |
| `lean4-carrier-rigidity/` | Maschineller Beweis des Carrier-Polynoms `6Y² − Y − 1 = 0` und der Hyperladungs-Spur in Lean 4. Zentrales Theorem aus Paper 2 als formal verifiziertes Computer-Theorem. | aktiv |
| `frb-tfpt-signatures/` | Preregistrierte, multi-Source, surrogat-kalibrierte FRB-Suche (FRB.01–FRB.09 + FRB.02b). **(search.txt §1,2,6)** Verdict: `not_confirmed_not_refuted`. | aktiv |
| `cmb-birefringence-seed/` | Cross-Domain-Seed-Linie: ein `φ₀` → `β` **und** `Ω_b`; **Shared-Seed-Erweiterung** φ₀→β+Ω_b+θ13+Cabibbo (χ²/dof=1.23, kanonisch wie `seed-consistency`). **(search.txt §3, Prio 1)** | aktiv |
| `cmb-inflation-scalaron/` | Starobinsky/Scalaron `n_s, r, A_s` aus `c₃` vs Planck/BICEP-Keck/DESI/CMB-S4; **scharf falsifizierbar** (`r≈0.0045`). | aktiv |
| `neutrino-mixing/` | PMNS `θ12/θ13/θ23` + CKM `δ` vs NuFIT 6.0/JUNO/LHCb — **prediction_of_record** (θ12 −0.02σ). | aktiv |
| `eht-achromatic-residual/` | Achromatischer dyonischer Residual-Test `β_BH(r) ∝ 1/r²` (3 Null-Tests). **(search.txt §4)** **Echte EHT-M87-2017-Polarimetrie ingestiert** (`tfpt-eht realdata`); **Injection-Recovery-Suite** (`tfpt-eht inject`, 4/4 korrekt klassifiziert); GRMHD-Residual-Nulls datenlimitiert. | aktiv |
| `seed-consistency/` | Shared-Seed-Stresstest: β/Ω_b/Cabibbo/θ13 → φ₀, Joint-Fit + LOO + Dominant-Pull. **v2** GLS/PPC; **v3** reactor-only aus Daya Bay/RENO/Double Chooz (komb. `sin²θ13=0.02204`, χ²/dof=1.00, θ13 −1.62σ), NuFIT-global nur Shadow. | aktiv |
| `gw-ringdown-echo/` | Ringdown-Echo-Amplitudenquotient `≤ (2/3)⁶`, Katalog-Feasibility auf GWTC-5.0 **(search.txt §5)**; **Stage 1** statische Echo-Suche auf echtem Strain (GW150914/GW190521) = kein Kernel-Echo; **Stage 2 NEU** dynamischer Walled-Clock-MF (Bend 2.7095) auf echtem Strain = `NO_KERNEL_RECOVERY` + maschineller Befund, dass der Bend in EINER Recovery entartet ist (Zwei-Moden-Gewinn ≈1.3×10⁻³) → die unterscheidende Signatur ist der Kaskaden-Kamm (`ω=2.58`), nicht ein Einzel-Ringdown. | aktiv (Stage 2) |
| `gw-speed-multimessenger/` | `v_GW=c` Null-Test aus GW170817+GRB170817A (namentlicher Falsifikator). | aktiv |
| `gw-ringdown-spectroscopy/` | **Schwarzloch-direkt**: QNM `ω_R/T_H→ln3=ln N_fam`, Flächenquant `4 ln3=ln81` — strukturell exakt, **datenlimitiert**. | aktiv |
| `pulsar-glitch-recovery/` | **Fehlende Cross-Domain-Säule** (problem_1.txt): derselbe Kernel `{1,(2/3)⁶,(1/3)⁶}` wie FRB.02/09 + GW-Echo, in echten Pulsar-Glitches (Jodrell Bank, 726 Glitches) **+ Recovery `Q`/`τ_d`** (Yu+2013, 60 Komponenten). **Sauberer Null in allen vier statischen Kanälen** (PG.01–04). **PG.05 NEU** dynamischer Recovery-Kamm (`ω=2.58`) auf echtem **Crab-`ν(t)`** (JBO-Monatsephemeride, 479 Punkte): Detektor injection-validiert, **kein** Kern-Kamm → `data_limited`. **PG.06 NEU** (schwer) dichte **J0537**-Säule (1165 NICER-Obs) + Scaffold: Kamm braucht **>~2.8 ln(τ)-Perioden** → J0537 (~1.9) range-blind → Ziel ist **Vela**. **PG.06b NEU** echte NICER-**Vela**-Daten (665 Obs): 1 Obs geladen, mit **PINT barycentriert (kein HEASoft)**, **Vela-Pulsation real nachgewiesen** (F0=11.193 Hz, H=18.4) → Pipeline auf echten Daten bewiesen; comb-`ν(t)` braucht phasenverbundenes Timing (~6.5 GB, dokumentiert, kein Claim). | aktiv |
| `recovery-comb-domains/` | **Cross-Domain-Suche der dynamischen Kamm-Signatur** (`ω=2.58`): EIN injection-validierter Detektor (96 %/0 %, range-blind <2.8 Perioden) über **8 Kanäle** — **A1** Magnetar-Flussabfall (surface; 2 Kurven ≥ Gate → stacked NULL p≈0.99), **A2** BH-Spätzeit-Tail/QNM (horizon, data_limited), **A3** FAST/GBT-FRB-Tail (7 Bursts → stacked NULL p≈0.34) + **A3b** CHIME-Baseband (8 FRBs → NULL p≈0.67), **A4** GRB-Röntgen-Plateau (17 Swift-XRT ≥ Gate → **well-powered NULL** p≈0.13, surface), **A5 NEU** Nuclear-Transient/AGN-Scheiben-TDE-Optik-Lichtkurve (**echte ZTF-Daten J2245+3743**, z=2.554, Graham+2025; zr-Fade 3.21 Perioden ≥ Gate → kernel ω=2.58 **nicht besonders** p≈0.80, TFPT-λ-Batterie NULL Bonferroni p≈0.08, surface/Akkretion — nicht Horizont), **B4/B5** BEC-Analog/Quantensimulator (needs_experiment). Alle realen Kanäle sauber NULL; kein Claim. | aktiv |
| `extended-signatures/` | **Erweiterte Signatur-Runde (EXT.1–7):** FRB Joint Echo×Pol, Anyon π/4-Kamm, GW Gravastar Joint, Horizon-Fingerabdrücke, Galois-CP+J_PMNS, Seed xi/BBN, dynamische Crab/FRB-Probes. | aktiv (neu) |
| `quantum-testbed/` | **Stärkste Quanten-Signatur** (problem_1.txt) + Diskret→Dynamik-Abschluss (`v238`–`v245`). QT.01 Entanglement-Spektrum trägt den Kernel **exakt**; QT.02 dynamische DSI (`ω=2π/ln λ`, Amplitude `~e^{−π²/ln λ}`); QT.04 exakte gewallte Uhr (Bend `2.7095`, Floor, Wall) + Matched-Filter; **QT.05 Anyon-MTC** (16 Sektoren, Statistik-Phasen `π/4`/`π/2`, `c=8`). Intern, kein Datum. | aktiv |
| `gauge-unification/` | **`sin²θ_W = 3/8` (v244/v245) vs PDG** (1/2-Loop-RGE): GUT-Wert geerbt, aber SM verfehlt Unifikation um 13%, `3/8 → sin²θ_W(M_Z)=0.2076` vs `0.23122` (universelle ~10%-GQW-Lücke, nicht TFPT-spezifisch). `data_limited`/`weak`. | aktiv |
| `lab-residuals/` | `F_transfer`-Laborkanäle (g−2, seltene Kaonen, Axion), alle **[C]**; **Haloskop-Overlay** (`tfpt-lab haloscope`, DFSZ/KSVZ bei 23.8 µeV + Plot). **(search.txt §7,8,9)** | aktiv |
| `rare-kaon-bridge/` | **Flavor-Bridge als Geometrie**: `R_K`, BR(K⁺), BR(KL), `δ_CKM/γ`, Jarlskog, Grossman-Nir + SM-Nuisances. 3/5 direkte Beine konsistent; downstream. | aktiv |
| `dark-energy-w-watchdog/` | **`w=−1`-Killwatchdog** vs DESI DR2 `w0-wa`, **overlap-aware** (kein naives SN-Stacking). Stärkste Einzelkombo 4.4σ (naives Produkt 6.6σ = Scheinsignal). | aktiv |
| `higgs-criticality/` | **Doppel-kritische Fläche** `λ(M_Pl)=0, β_λ(M_Pl)=0` vs SM-RGE (Buttazzo 2013 NNLO-Fit). λ=−0.0143±0.0057 (metastabil 2.5σ); downstream RGE-Bridge. | aktiv |
| `lambda-h0-engine/` | Λ-Engine: `ρ_Λ/M_pl⁴=(3/256π⁴)e^{−2α⁻¹}` (122.95 vs 122.94 Größenordn.!), `S_dS ρ_Λ=32π⁴`, `H₀~√Λ`. | aktiv |
| `recovery-channel/` | **Test C** (datenunabhängig): Recovery-Kernel als CPTP-Quantenkanal — CPTP/Choi, Data-Processing, QEC-Code, Page-Kurve bei `t_Page`. Packt `v155/160/161`. | aktiv |
| `theory-contracts/` | **Reine Theorie-Contracts** (nicht in der empirischen Scorecard): QGEO-DtN-Mark-Locality (`[ρ,Λ]=0` aus Z4-Marken, Fourier-mod-4 + Negativkontrollen). | aktiv |
| `quantum-recovery-analog/` | **Geparkt**: Analog-Recovery `I_n ~ (64/729)^n`, kein direkter Datensatz. **(search.txt §10)** | geparkt |
| `ftransfer/` | Theorieseitige `F_transfer`-Solver: Axion-Relik (**Spine-Finite-T-Solve** `Ωₐh²=0.125` + **unabhängiger Cross-Check** sudden/analytisch [0.125, 0.143]), Koide, Leptogenese-Boltzmann, QCD-Matching `m_p/m_e`. | aktiv |
| `ccbh-dark-energy/` | **Kosmologisch gekoppelte BHs** (problem_b §B): de-Sitter-Seam-Innere `w_in=−1` ⇒ Kopplung `k=−3w_in=3` ⇒ Population `w=−1`; vs Farrah+2023 `k=3.11±0.79` (**−0.14σ**, aber CCBH-als-DE umstritten). Alternative-Lesart zu `dark-energy-w-watchdog` (`w_de_eos`). | aktiv |
| `gravastar-compactness/` | **Gravastar/ECO** (problem_b §F): Nariai `Q_geom=3/8` = Jampolski-Rezzolla Max-Kompaktheit `C=3/8` (exakter Rational-Match `[C]`); `1/3<3/8<4/9<1/2` ⇒ horizontloser Echo-Kandidat, Delay ~0.70 ms (62 M☉) + Amplitude `≤(2/3)⁶`. Schärft `gw-ringdown-echo`. | aktiv |
| `cosmic-handedness/` | **Paritäts-Watchdog** (problem_b §J, Frontier): Galaxien-Spin-Händigkeit (Shamir JADES 158:105, **~3.3σ** Monopol) vs winziger `μ4`/`PSL(2,ℂ)`-Rest; Monopol-vs-MW-Aberrations-Dipol ungelöst, Galaxy-Zoo isotrop. | aktiv |

Über die ursprünglichen **9 search.txt-Suchräume** hinaus jetzt erweitert um die scharfen
**Compiler-Ebenen-Vorhersagen** (Inflation, Neutrino-Mixing, `v_GW=c`, Λ/H₀, QNM `ln3`),
den datenunabhängigen **Recovery-Channel-Check** (Test C) und — neu aus `problem_1.txt` —
die **dritte Cross-Domain-Säule** `pulsar-glitch-recovery` (damit ist das in `problem_1.txt`
geforderte Dreieck **FRB-Recovery + GW-Ringdown-Residual + Pulsar-Glitch-Recovery** vollständig
mit demselben eingefrorenen Kernel testbar). Die zentrale, getypte
Zeilenübersicht aller (Domäne, Observable) liegt in
[`evidence_scorecard.json`](evidence_scorecard.json) (Generator
`build_evidence_scorecard.py`, validiert feste `stage`/`status`/`evidence_class`-Enums).
Schärfste Konsistenzpunkte (≤0.5σ): CMB `β`/`Ω_b`/Seed-Linie, Kaon `K⁺`, Neutrino `θ12`,
Λ-Hierarchie.

---

## 1. Gesamtbefund — wo welche TFPT-Signatur, wie belastbar

**Es gibt keine unterscheidende Entdeckung.** Was vorliegt: Konsistenzen (Theorie
nicht im Widerspruch, oft sagt die Standardphysik dasselbe), saubere Nullbefunde,
**vier echte Spannungen** (θ13, A_s@N⋆=51.4, g−2 unter Lattice-HVP, Axion-Hilltop) und
mehrere noch-nicht-testbare Kanäle. Eine *belastbare* TFPT-Signatur bräuchte (a) eine
eingefrorene Zahl, die TFPT von der Standardphysik unterscheidet, (b) in **≥2
unabhängigen** Datenwelten, (c) mit kleinen Fehlern — das ist nirgends vollständig erfüllt.
Die wirklich belastbaren Entscheidungen liegen jetzt bei **α⁻¹, θ12, θ13, r, A_s, β, w, EHT,
K⁺** und den `F_transfer`-Solvern. (Neu als eigene Scorecard-Zeilen: der Headline-Fixpunkt
**α⁻¹** — ehrlich getypt als **+1.9σ-Watch** gegen CODATA, nicht als sauberer Treffer — sowie die
`F_transfer`-Bridges **Koide** [C] und **m_p/m_e** [O, numerologie-geflaggt]. Der eingefrorene
Live-σ-Watchdog dafür existiert bereits in der Verifikations-Suite als
`verification/v307_data_watchdog.py` — er bewertet α⁻¹/θ12/θ13/r/s23/δ_CKM laufend gegen
CODATA/NuFIT/Planck; θ13 (+2.0σ) ist dort der dokumentierte Druckpunkt.)

<!-- SCORECARD_STATS:START (generated by build_evidence_scorecard.py; do not edit) -->
**Scorecard (auto-generated from `evidence_scorecard.json`): 79 Zeilen — 36 consistent, 4 tension, 13 null, 25 data_limited, 1 parked.**

- nach `evidence_class`: 16 downstream_bridge, 26 external_data, 9 internal_consistency, 1 parked, 27 search_target
- nach `independence_group`: 4 N_star_reheating, 3 alpha_em, 1 c3_topform_horizon, 2 cp_mu6_phase, 60 independent, 9 phi0_seed
- `alternative_group` (eine Frage, mehrere Lesarten — *nicht* doppelt zählen): 2 HVP_baseline, 2 Nstar_branch, 3 axion_branch, 2 w_de_eos
- `watch_flag`: 2 (schärfster nicht-roter Kanal: dunkle Energie `w`)
- _Korrelierte `phi0_seed`-Beine, `alternative_group`-Lesarten und `internal_consistency`-Checks zählen NICHT als unabhängige externe Treffer._
<!-- SCORECARD_STATS:END -->

### Robustheits-Stufen

| Stufe | Kanäle | Lesart |
|---|---|---|
| **Schärfste Konsistenz** (≤0.5σ, mit Vorbehalt) | Λ-Hierarchie (**dev 0.004 Größenordnungen**, *kein* pull_sigma — Metrologie-Kohärenz), Neutrino `θ12` (**−0.02σ**), Kaon `K⁺→π⁺νν` (**−0.08σ**), CMB `Ω_b` BBN (0.04σ), CMB Seed-Linie (0.35σ), CMB `β` (0.37σ) | nah dran, aber teils Bridges, breite Fehler, korreliert (`phi0_seed`) oder Metrologie-Kohärenz |
| **Konsistenz, nicht unterscheidend** | FRB.01 (keine native Dispersion), FRB.05 (`Ω_b` aus FRB-DM(z)), `v_GW=c` (GW170817), EDM `θ_eff=0`, Σm_ν, Inflation `n_s` vs Planck, A_s (profiliert), **Axion-Spine** (`Ωₐh²=0.125`, robust), **Higgs-Kritikalität** (λ(M_Pl)≈0), **Leptogenese `η_B`** (voller ODE, `6.5×10⁻¹⁰` = 1.07× @ frozen `M₁`), **δ_PMNS** (240° = δ_CKM,lead + π, v231/v233; **+1.08σ** NuFIT 6.0 NO best fit, schwach unterscheidend) | Standardphysik sagt dasselbe / interne Identität / downstream-Bridge |
| **Interne Konsistenz** (keine externe Messung) | Recovery-Channel CPTP/QEC, Page-Kurve-Turnover bei `t_Page`, **Petz-Recovery + rank-one Baby-Universe** (`‖T^n−P_∞‖=(2/3)^{6n}`), **`S_dS·ρ_Λ=32π⁴`** (algebraische Identität, `stage=not_applicable`), **QGEO-DtN-Mark-Locality** (Theory-Contract); **Quantum-Testbed QT.01** (Entanglement-Spektrum = Kernel exakt: Surprisals `6ln(3/2)`,`6ln3`, Protected-Mode, `I_n`) **+ QT.02** (Quench-DSI bei `ω=2π/ln λ`, Amplitude `e^{−π²/ln λ}`-unterdrückt) | `evidence_class=internal_consistency` / Theory-Contract — nicht im selben Korb wie CMB/Kaon |
| **Sauberer Nullbefund** | FRB.02, FRB.02b, FRB.04, FRB.06, FRB.07, FRB.08, FRB.09; **Pulsar PG.01/02/03** (Kernel-Comb null; `Δν/ν`-Struktur = bekannte 2-Populations-Bimodalität) **+ PG.04** (Recovery `Q` nicht an φ₀-Vielfachen, `τ_d`-Multikomponenten-Leiter null; echte Yu+2013-Daten) | Muster nachweislich **nicht** da, über mehrere Quellen / der eingefrorene Kernel maskiert sich **nicht** in einem dritten, physikalisch unverwandten Datensatz |
| **Echte Spannung** (Daten/Modell ziehen dagegen) | **θ13** (+2.0σ), **A_s** fix N⋆=51.4 (−11.3σ), g−2 unter Lattice-HVP (+3.86σ), Axion-**Hilltop** (~5.5× Überproduktion) | hier entscheidet sich Substanz; θ13 ist der `φ₀`-Seed-Treiber |
| **Datenlimitiert mit Hinweis-Flag** | FRB.03 (Aktivitätsfenster, `hint_flag`) | 1/2 broad-match, n=2<5, LOO-instabil → `data_limited` (zu kalt für `hint`) |
| **Datenlimitiert** (noch nicht testbar) | GW-Echo (**Stage-1 statisch + Stage-2 dynamisch auf echtem Strain gelaufen** = kein Kernel-Echo/`NO_KERNEL_RECOVERY`; Einzelevent strukturell limitiert → Kaskaden-Kamm nötig), **EHT-Residual** (echte Daten + Injection-Suite, GRMHD-Imaging offen), QNM `ln3`, Axion-Marker, Kaon `KL`/`R_K`, dunkle Energie `w` (4.4σ), m_ββ, **CCBH `k=3`** (−0.14σ, umstritten), **Gravastar `C=3/8`-Echo**, **kosm. Händigkeit** (~3.3σ, Frontier), **log-periodische Recovery-DSI** (`ω=2π/ln((3/2)⁶)≈2.58`; **PG.05 erstmals auf echter Crab-`ν(t)`-Wellenform gelaufen** — Detektor validiert, kein Kamm, Monatskadenz-limitiert; braucht Tageskadenz) | richtige Signatur/Vorhersage, erster Realdaten-Test gelaufen → `data_limited` |
| **Geparkt** | Quantum-Recovery-Analog | kein physischer Datensatz |

### TFPT-Signaturkatalog (search.txt) — was wo geprüft wurde

| # | Signaturtyp | eingefrorener Wert | geprüft in | Ergebnis |
|---|---|---|---|---|
| 1 | feste Transferquotienten | `(2/3)⁶=64/729`, `(2/3)³=8/27`, Schritt `2/3` | FRB.02/02b/03/06/07, GW-Echo, **Pulsar PG.01/02/03** | Null / Hinweis / datenlimitiert (Cross-Domain-Dreieck FRB+GW+Pulsar: kein Kernel-Treffer) |
| 2 | µ4/Z4-Phasenstruktur | 4 Klassen | FRB.04, FRB.08 | Null (Fundamental m=2, nicht m=4) |
| 3 | globale Seed-Rotation | `β = φ₀/(4π) = 0.2424°` | CMB | konsistent (0.37σ) |
| 4 | achromatische Horizon-Pol. | `β_BH ∝ 1/r²`, Sign-Flip | EHT | real ingest + Achromatizität erledigt; GRMHD-Residual-Nulls offen |
| 5 | harte Nullsignatur | keine native Dispersion, `v_GW=c` | FRB.01 | konsistent (kill-test bestanden) |
| (+) | Recovery-Clock-Dynamik | `rate(n)=−6 ln(1−n/3)`, Wall bei N_fam=3 | FRB.09 | Null |
| (+) | `F_transfer`-Laborwerte | `Δaµ`, `BR(K)`, `m_a` | lab-residuals | Kaon konsistent, g−2 baseline-abhängig, Axion datenlimitiert |

### 1.1 Reconsideration — die Signatur ist vermutlich *dynamisch* (diskrete Skaleninvarianz), kein statisches Verhältnis

Alle obigen Suchen testen den eingefrorenen Kernel als **statisches Verhältnis** in einem
Histogramm (FRB.02–09, Pulsar PG.01–04) — und liefern Null. Die `quantum-testbed`-Analyse
(problem_1.txt §D) zeigt *warum* und *was stattdessen zu suchen ist*: ein System, das über
eine **geometrische Moden-Leiter** (`γ_k=γ₀·λ^k`, genau die `(3/2)^k`-Struktur) zu seinem
Fixpunkt relaxiert, hat einen **komplexen kritischen Exponenten** `α+iω` — seine
Recovery-*Kurve* ist nicht reine Potenz, sondern log-periodisch:

```
R(t) = (Potenz) · (1 + ε·cos(ω·ln t + φ)),    ω = 2π/ln λ,    ε ~ e^{−π²/ln λ}.
```

Der Kernel erscheint also als **Log-Frequenz in der Recovery-Dynamik**, nicht als Zahl auf
einem Lineal (der „diskret → dynamisch"-Übergang). Das Amplitudengesetz `ε~e^{−π²/ln λ}` ist
entscheidend: nur eine **grobe** Leiter (`λ≳e²≈7`) hinterlässt eine sichtbare (~2%) Welle.

**Schärfung aus dem exakten Übergangs-Reconstruction (`v124`/`v126`/`v147`).** Der TFPT-Übergang
diskret→dynamik ist *exakt* die resummierte Uhr `rate(n)=−6 ln(1−n/3)` mit Spektrum `(1−n/3)⁶` und
einem **Pol/Wall bei `n=N_fam=3`** — also **keine** unendliche geometrische Leiter (die anhaltende
DSI gäbe), sondern eine **gewallte Zwei-Moden-Uhr**. Eine *einzelne* Recovery ist daher
`R(t)=w₀+w₁e^{−6ln(3/2)·t/τ}+w₂e^{−6ln3·t/τ}` mit drei scharfen, *neuen* Signaturen: (i) die zwei
Raten sind am **det'-sauberen Bend** `rate(2)/rate(1)=ln3/ln(3/2)=2.7095` (v147) festgenagelt — ein
**Ein-Parameter**-Doppel-Exponential, kein freies Ratenpaar; (ii) ein **protected Floor** `w₀`
(λ=1, das „Gesetz") → unvollständige Recovery; (iii) ein **harter Wall** (keine dritte
Zerfallszeit). Anhaltende DSI tritt nur über eine **Kaskade** von Ereignissen auf, nie innerhalb
einer gewallten Recovery. **Konkreter, falsifizierbarer Test (statt Histogramm):** ein
**Matched-Filter** mit dem Fixed-Ratio-(2.7095)-Doppel-Exponential-Template + Floor auf
zeitaufgelösten Recovery-*Wellenformen* (FRB-Tails, Pulsar-`ν(t)`-Postglitch, GW-Ringdown-Residuen)
— gebaut und injection-validiert in `quantum-testbed` QT.04 (Kernel-Kurve → erkennt 2.71;
Nicht-Kernel → verworfen). Das **erklärt die statischen Nulls** und ist der offene, sensitivere Hebel.

**Erster Realdaten-Lauf des dynamischen Templates (GW-Ringdown, `gw-ringdown-echo` Stage 2,
`tfpt-gw dynamic`).** Auf echtem GWOSC-Strain (GW150914, GW190521) angewandt liefert er einen
sauberen `NO_KERNEL_RECOVERY` **und** einen schärferen, maschinell geprüften Befund: **innerhalb
EINER monotonen Recovery ist der Bend nicht identifizierbar** — die exakte Walled-Clock-Kurve ist
mit einem *einzigen* Exponential + Floor entartet (Zwei-Moden-R²-Gewinn ≈1.3×10⁻³, schon
rauschfrei). Die unterscheidende dynamische Signatur ist der **log-periodische Kamm über eine
Kaskade** (`ω=2.583`, Amplitude `ε≈2%`), den eine **Einzel**-Ringdown strukturell nicht liefert.
**Konsequenz für den Hebel:** er gehört auf die **zeitaufgelöste Recovery-SEQUENZ einer
Repeater-Quelle** (FRB-Repeater-Tails, Pulsar-`ν(t)`-Postglitch-Serien), nicht auf einen
Einzelevent-Ringdown — die FRB.09/QT.04-Wellenform-Suche bleibt der eigentliche offene Hebel.

**Erste Realdaten-Umsetzung des Kamm-Tests auf einer echten `ν(t)`-Wellenform (Pulsar PG.05,
`tfpt-pulsar dynamic`).** Die Jodrell-Bank-Crab-Monatsephemeride (38 Jahre `ν`/`ν̇`) ist der einzige
öffentliche Datensatz mit der nötigen `ln(t)`-Spanne. Der log-periodische Kamm-Detektor bei `ω=2.58`
ist **auf genau dieser Monatskadenz injection-validiert** (Kaskade erkannt p≈0.002, glattes
Potenzgesetz verworfen p≈0.15), findet aber in **keinem** der 7 sauberen Inter-Glitch-Segmente einen
Kern-Kamm (`data_limited`; Monatskadenz < die ~2%-Kamm-Amplitude). Damit ist der Hebel erstmals auf
einer echten Recovery-*Wellenform* (nicht Summary-Statistik) ausgeübt; der schärfere Test ist
Tageskadenz-Timing eines Riesenglitches (Crab 2017) oder Vela.

**PG.06 (`tfpt-pulsar nicer`, schwer/optional) — die dichte J0537-Säule + die entscheidende Range-Erkenntnis.**
Scaffold für den dichtesten Datensatz (PSR J0537-6910, „Big Glitcher", NICER; `scripts/fetch_nicer_j0537.py`
bestätigt 1165 Beobachtungen über ~8 Jahre). Upstream (L2-Events + **PINT**-Falten → `ν(t)`) ist auf ~GB-
Downloads gated (HEASoft **nicht** nötig, PINT pip-installiert); Downstream (`ν(t)` → Superposed-Epoch-Stack →
Kamm) ist injection-validiert (96 % Detektion, 0 % Fehlalarm im ausreichenden Bereich). **Maschinell geprüfte
Kern-Erkenntnis:** der Kamm braucht **>~2.8 Perioden in `ln(τ)`** (≈3 Dekaden); ein J0537-~100-d-Intervall
liefert nur **~1.9** → range-blind, und **Stacking hebt nur die Amplitude, nicht den `ln(τ)`-Bereich**. ⇒ Das
entscheidende Ziel ist ein **lang-intervalliger, dicht überwachter** Pulsar (**Vela**, Glitch alle ~3 Jahre,
täglich → ~3 Dekaden), nicht J0537. Das ist die schärfste Formulierung des offenen Hebels — und sie sagt
präzise, *welche* Beobachtung ihn schließen würde.

**PG.06b (`tfpt-pulsar vela`) — echte NICER-Vela-Daten, Pipeline auf echten Photonen bewiesen.** Der von
PG.06 benannte Zielpulsar **Vela** (PSR B0833-45) ist im HEASARC-NICER-Archiv mit **665 Beobachtungen**
(MJD 57941–60817, ~7.9 Jahre, ~762 ks, ~6.5 GB) vorhanden. Ich habe **eine echte Beobachtung
heruntergeladen** und mit **PINT barycentriert** (`get_NICER_TOAs` + Satelliten-Observatory aus dem
`.orb`, **ohne HEASoft**) und die **Vela-Pulsation real nachgewiesen: F0 = 11.19275 Hz (Periode 89.34 ms,
H = 18.4)** aus 430.739 Photonen. Damit ist die Reduktions-Pipeline (Download → Barycentrieren → Falten)
**auf echten Daten bewiesen**. **Ehrliche Grenze (kein Claim):** eine comb-*qualitative* `ν(t)` lebt auf
~µHz-Niveau und braucht eine **phasenverbundene Timing-Lösung** über alle 665 Obs (per-Obs-H-Test nur
~mHz) — ~6.5 GB + mehrstündige PINT/`tempo2`-Analyse + Glitch-Handling, ein echtes Reduktionsprojekt, kein
Sandbox-Fold. PG.06b beweist die Pipeline real und beziffert den Rest; es täuscht **kein** `ν(t)` vor.

---

## 2. FRB — `frb-tfpt-signatures/` (search.txt §1,2,6)

Preregistriert (`hypotheses/frb_tfpt_v1.yaml`), eingefrorener Kernel
(`{1,(2/3)⁶,(1/3)⁶}`, exakte Brüche per Guard-Test geschützt), multi-Source,
surrogat-kalibriert. Aggregat-Verdict: **`not_confirmed_not_refuted`** (keine
replizierte, unterscheidende Stütze). Pro Achse:

| Achse | Signatur | Methode + Nullmodelle | Datenquelle | Ergebnis |
|---|---|---|---|---|
| **FRB.01** | keine native (nicht-Plasma) Dispersion | Sub-Band-ToAs aus echten Wasserfällen; Fit `t(ν)=t₀+K ν⁻²+A_scat ν⁻⁴+drift+A_TFPT ν⁻³`; **implizierte Laufzeit vs ToA-Präzision** + Cross-Source-Universalität | PSRFITS/`.ar` (FRB 20121102A `.calibP` + FRB 20201124A) → `frb01_subband_toas.csv` | **Konsistenz** (2 Quellen, 119 Bursts; implizierte Laufzeit ~10⁻¹⁹ s ≪ Präzision ~5×10⁻⁵ s) |
| **FRB.02** | Echo-/Recovery-Quotienten | konsekutive Within-Session-Energieverhältnisse vs Kernel; 4 Nulls (within-session, local-block, AR(1)-Energy-Storm, censoring), BH-q; Observable-Semantik (Energie- vs Amplitudenkanal) | FAST 1652 + Blinkverse (4 Quellen) | **Null** (kein Theorie-Kanal-Exzess) |
| **FRB.02b** | Free-Quotient-Null (**Anti-Numerologie**) | M0 / M_fixed(8/27) / M_free(`q*∈[0.01,0.5]`); Look-Elsewhere-korrigiert; Injection-Recovery (validiert: recovered `q≈0.290≈8/27`) | FAST 1652 + Blinkverse | **Null (M0)** — freier Quotient landet *nicht* auf einem Kernelwert (LEE-p ≥ 0.31) |
| **FRB.03** | Aktivitätsfenster-Eigenbreiten | `W_broad/P≈8/27`, `W_core/P≈1/27`; Population + Nullmodell + Leave-one-out; HDI-Fenster aus gefalteten Phasen | CHIME (FRB 20180916B) + Literatur-Repeater | **Schwacher Hinweis**: FRB 20180916B trifft (3%/1%), aber n=2<5 Quellen, null-p=0.11, nicht LOO-stabil |
| **FRB.04** | PA/RM-Markov-Spektrum (µ4/D4) | Übergangsmatrix-Eigenwerte vs Kernel; 5 Nulls (stationary, time/block-shuffle, **AR(1)-drift**, Dirichlet); v2 Step-Relaxation | FAST FRB 20240114A Pol (6134) + Blinkverse (3 Quellen) | **Null** (RM≈{2/3,1/3} durch AR(1)-Drift erklärt; PA durch block-shuffle reproduziert) |
| **FRB.05** | Baryon-Fraktion `Ω_b` | Macquart-`DM(z)`-Steigung, `Ω_b`-Fit mit System-Fehlerboden | lokalisierte FRBs (ApJ adb84d Table 4; Sharma 2024) | **Konsistenz**: `Ω_b=0.0483±0.0072` (0.1σ von TFPT 0.0489) |
| **FRB.06** | Polarisationsgrad-Quantisierung | L/I, \|V\|/I nahe Kernelbrüchen; Beta-Null **+ Placebo-Kontrolle** (killt Tail-Artefakt) | FAST + Blinkverse (3 Quellen) | **Null** (kein Bruch über Placebo) |
| **FRB.07** | Breiten-Relaxations-Echo | konsekutive Breitenverhältnisse vs Schritt-Kernel `{2/3,1/3}` | Blinkverse (3 Quellen) | **Null** |
| **FRB.08** | statische PA-µ4-Klassen | Rayleigh-Test auf fundamentale Klassenzahl (µ4 → m=4) | FAST FRB 20240114A | **Null** (signifikant, aber Fundamental **m=2** = Orthogonalmodus, nicht m=4) |
| **FRB.09** | Recovery-Clock-Dynamik | (A) Kaskaden-Wall ≤ N_fam=3; (B) Gap-Verhältnis `g1/g2 = ln3/ln(3/2)=2.71`; within-session-Shuffle-Null + Placebo | FAST 1652 + Blinkverse (4 Quellen) | **Null** (Wall 0/4, Beschleunigung 0/4) |
| *generisch* | Energie-Kaskade | GMM + Log-Periodizität + Spacing-Ladder, smooth-Null-Surrogate | FAST 1652 | diskrete log-periodische Kaskade (p=0.002), aber **nicht** kernel-spezifisch |

Details, Plots und exakte Algorithmen: [`frb-tfpt-signatures/README.md`](frb-tfpt-signatures/README.md).

---

## 3. CMB-Seed-Linie — `cmb-birefringence-seed/` (search.txt §3, Prio 1)

**Eine** eingefrorene Größe `φ₀ = (4/3)c₃ + 48c₃⁴ = 1/(6π) + 3/(256π⁴)` sagt **zwei**
Observablen voraus, die normalerweise in getrennten Pipelines leben:

```
β_rad   = φ₀/(4π)            → β = 0.242435°     (kosmische Doppelbrechung)
Ω_b     = (4π − 1)·β_rad     → Ω_b = 0.04894     (Baryon-Fraktion)
⇒ feste Seed-Linie:  Ω_b / β_rad = 4π − 1 = 11.566
```

**Vier Modi** (kein einzelner künstlich-scharfer „joint Treffer"):

| Modus | Inhalt | Ergebnis |
|---|---|---|
| `beta_only` | `β` vs ACT DR6 / Planck PR4 | konsistent (0.37σ / 0.52σ) |
| `omega_b_only` | `Ω_b` vs Planck 2018 / BBN (unit-safe `Ω_b h²/h²`) | konsistent (0.42σ / **0.04σ**) |
| `joint_independent` | Linie `Ω_b/β_rad` + Single-Seed-Kohärenz `φ₀^β` vs `φ₀^Ω` (Annahme cov=0) | konsistent (Linie 0.35σ, Kohärenz 0.39σ) |
| `joint_covariance_placeholder` | dieselbe Linie, **Kovarianz nicht modelliert** | **keine kombinierte Signifikanz beansprucht** (ACT-β + Planck-Ω_b beide CMB → BBN-Bein nutzen) |

**Unit-Guard:** `β` intern immer in Radiant; `Ω_b` (~0.049) nie mit `Ω_b h²` (~0.022)
verwechselt; BBN deklariert `Ω_b h²` + `h` explizit. **Verdict: konsistent mit der
Seed-Linie (nicht *validiert*).** Datenquellen: ACT DR6 (arXiv:2509.13654), Planck PR4
(arXiv:2205.13962), Planck 2018 VI, PDG/Cooke+2018 (BBN).

---

## 4. EHT-Horizont-Collar — `eht-achromatic-residual/` (search.txt §4)

Sauberste *lokale* astrophysikalische Falsifikationsfläche: der achromatische, dyonische
Residual-Intercept `β_BH(r) = 16 c₃⁴ Q_e Q_m / r² = (1/256π⁴) Q_e Q_m / r²`. TFPT fixiert
**nicht** die Amplitude (MHD/GR-Gewichte), sondern drei **Null-Tests**:

1. **frequency null** — `χ₀^res` achromatisch (kein `λ²`-Tail)
2. **profile null** — `χ₀^res(r) ∝ 1/r²` um den Photonenring
3. **sign-flip null** — Vorzeichenwechsel unter effektiver `E·B`-Umkehr

`DETECTION` nur, wenn **alle drei** simultan bestehen. Die Kopplung `1/(256π⁴)=16c₃⁴`
ist exakt fixiert (dieselbe Top-Form-Koeffizientenzahl `δ_top=48c₃⁴` wie in der
α-Kernel-Korrektur); frei ist nur die Amplitude `Q_e^eff Q_m^eff` (MHD/GR-Gewicht).
Synthetische End-to-End-Pipeline (`demo --case signal|null|systematic`) + die drei
Null-Tests sind implementiert und grün.

#### Echte Daten ingestiert (NEU, `tfpt-eht realdata`)
`scripts/fetch_eht_data.py` lädt die **echten** EHT-M87-2017-Polarimetrie-uvfits
(Datenprodukt **2023-D01-01**, CyVerse DOI 10.25739/q46m-m857, GitHub
`eventhorizontelescope/2023-D01-01`): **4 Beobachtungstage (Apr 5/6/10/11) × 2 Bänder**
(hi ≈ 229.07 GHz, lo ≈ 227.07 GHz), D-term- + self-kalibrierte HOPS-Sätze
(`*_hops_zbl-dtcal+selfcal.uvfits`, je ~0.5 MB).

`src/tfpt_eht/real_data.py` liest sie mit `astropy.io.fits`, bildet die Zirkular-Basis-
Stokes-Visibilities `I=(RR+LL)/2`, `Q=(RL+LR)/2`, `U=i(LR−RL)/2`, und berechnet pro Band
die I-amplitudengewichtete Netto-EVPA `χ=½ atan2(⟨U⟩,⟨Q⟩)` und `|m|`. Ergebnis:

| Tag | hi: EVPA / \|m\| | lo: EVPA / \|m\| |
|---|---|---|
| Apr 05 | −18.5° / 0.184 | −19.1° / 0.146 |
| Apr 06 | −17.2° / 0.075 | −19.2° / 0.069 |
| Apr 10 | −12.3° / 0.084 | −5.1° / 0.077 |
| Apr 11 | −8.4° / 0.085 | −9.2° / 0.076 |

→ mittlere **Band-zu-Band-EVPA-Rotation +0.9°**, implizierte **RM ≈ 5×10⁵ rad/m²**
(M87-Kern-Größenordnung, konsistent mit ALMA). Das ist die **rohe Quell-Chromatizität**;
der TFPT-Residual-Test (`χ₀^res = χ₀^obs − χ₀^GRMHD`, dann die drei Nulls) braucht das
**GRMHD-subtrahierte Bild** (polarimetrisches Imaging via eht-imaging + GRMHD-Library wie
`ipole`) → die `1/r²`- und Sign-Flip-Nulls bleiben **`data_limited`**. Die uvfits sind
gitignored; die kleine Summary `results/eht_real_achromaticity.json` ist versioniert.
**Schritt 1 (echter Daten-Ingest + Achromatizitäts-Diagnostik) erledigt.**

#### Injection-Recovery-Suite (NEU, `tfpt-eht inject`) — die Pipeline-Validierung

Da das echte GRMHD-Imaging (eht-imaging/SMILI + `ipole`) schwere externe Libraries braucht,
ist der *jetzt* lauffähige, wertvolle Teil die **Validierung**, dass die Residual- + 3-Null-
Maschinerie vier kontrollierte Injektionen korrekt klassifiziert (`src/tfpt_eht/injection.py`):

| Injektion | erwartet | Ergebnis |
|---|---|---|
| `tfpt_1overr2` (echte Signalform) | DETECTION (alle 3 Nulls) | ✓ frequency P / profile P / sign P |
| `faraday_lambda2` (λ²-Schirm) | frequency-Null **verwirft** | ✓ frequency F |
| `dterm_leakage` (D-Term) | profile/sign-Null verwirft | ✓ profile F / sign F |
| `evpa_offset` (Kalibrationsoffset) | profile/sign-Null verwirft (freq passt) | ✓ frequency P / profile F / sign F |

**4/4 korrekt klassifiziert** → die Pipeline labelt Achromatizität, Faraday-λ²-Tail,
D-Term-Leckage und EVPA-Offset zuverlässig auseinander. Das ist das Gate, das der echte
M87-Lauf durchlaufen muss, sobald GRMHD-Bilder vorliegen. (Nur zwei nahe Bänder ⇒ die
Frequency-Null bleibt Diagnose, kein finaler Achromatizitätsbeweis.)

#### Pipeline-Readiness (`tfpt-eht pipeline`)
Der Orchestrator listet die 7 Stufen und sagt **exakt, was blockiert**: Stufen 1/2/7
(uvfits-Ingest, EVPA-Diagnostik, Injection-Validierung) **erledigt**, Stufe 6 (3 Nulls)
**lauffähig**. **NEU (ehrlich nachgeprüft):** `eht-imaging` (`ehtim` 1.3.2) ist installiert und **liest die echten
M87-2017-uvfits** (verifiziert: Netto-`|m|≈3.4 %`, EVPA≈−34° bei 229 GHz an kurzen Baselines). Die
Imaging-**Bibliothek** ist also da — **aber** eine wissenschaftsfähige `χ₀^obs(r)`-Rekonstruktion ist
**kein Einzeiler**: ein naiver one-shot-RML-Lauf **konvergiert nicht** (braucht EHT-Pipeline-Flux-Skala,
Stations-Gains, Regularisierer-Tuning + Validierung). Stufe 3 ist daher „Bibliothek da, Experten-Setup
nötig", kein Knopfdruck. Und der **unterscheidende Residual-Test braucht zusätzlich** das GRMHD-Modell
(Stufe 4, `ipole`/`koral` + Simulationsdaten, nicht pip). Der `χ₀^res`-3-Null-Test bleibt daher
**`data_limited`** — gegated auf **beidem**: sorgfältige Polarisations-Rekonstruktion **und** GRMHD-Baseline.
Kein Vortäuschen.

---

## 5. GW-Ringdown-Echo — `gw-ringdown-echo/` (search.txt §5, Stage 0)

Echo-Amplitudenquotient `A_{n+1}/A_n ≤ (2/3)⁶ ≈ 0.0878` (Obergrenze, Lag frei).
**Stage = `catalog_feasibility`** — **kein** Strain-Level-Echo-Test, **kein** Echo-Claim.
Es ist ein Sensitivitäts-Census: Reicht eine zukünftige gestackte Strain-Suche?

- Datenquelle: **echter LVK GWTC-5.0** via GWOSC-Event-API → `data/gwtc_events.csv`.
  **390 kanonische Events** (161 neu in O4b); lokale Rohzeilenzahl **391** separat in
  [`event_count_audit.md`](gw-ringdown-echo/event_count_audit.md) abgeglichen (die eine
  Differenz = BNS GW170817, ohnehin aus der BBH-Selektion ausgeschlossen).
- Selektion: 391 → **278 ringdown-fähige BBH** (`M_f ≥ 5 M☉`).
- Ergebnis: gestackte Echo-SNR-Obergrenze **6.3** (realistisch `f_rd=0.3`) bzw. 21.1
  (konservativ) vs Schwelle 5 → ein maximaler `(2/3)⁶`-Echo **wäre erreichbar** ⇒
  Strain-Level-Test lohnt sich. **Datenlimitiert** bis zum echten Strain-Matched-Filter.

**Stage 1 — Matched-Filter-Maschinerie gebaut + injection-validiert (`tfpt-gw search`).** Die
Pipeline (Kerr-Ringdown-Subtraktion → Matched-Filter auf Residuen, Lag/Phase frei, Quotient
`(2/3)⁶` fix → Detection-SNR + freier-`q`-Kontrolltemplate) klassifiziert auf synthetischem
Strain **3/3 Injektionen korrekt**: Kernel-Echo → `DETECTION` (`q̂≈(2/3)⁶`); kein Echo → `NULL`;
falsches Ratio (0.5) → `NON_KERNEL_ECHO` (Echo da, aber **nicht** der TFPT-Kernel). Das
Template-Lag ist objektabhängig (das `C=3/8`-ECO der `gravastar-compactness` gibt `~0.7 ms`); der
Lag wird gescannt, das Ratio `(2/3)⁶` ist der eingefrorene Diskriminator. **`tfpt-gw realdata`**
läuft die statische `(2/3)⁶`-Echo-Train-Suche auf **echtem 32-s-GWOSC-Strain** (GW150914,
GW190521, via `scripts/fetch_strain.py`, h5py — kein gwpy): **kein** kernel-Ratio-Echo koinzident
in ≥2 Detektoren; Niedrig-`p`-Exzesse haben `q̂~1` (Rest-Ringdown, vom Free-Ratio-Control
verworfen). **Kein Echo-Claim.**

**Stage 2 — DYNAMISCHER Walled-Clock-Recovery-Matched-Filter auf echtem Strain (`tfpt-gw
dynamic`, NEU).** Schließt die **§1.1-Reconsideration** für den GW-Kanal: statt des statischen
Ratios wird die **gewallte Zwei-Moden-Uhr** (`v124`/`v147`, QT.04) als Template gefittet —
`R(t)=w₀+w₁e^{-(6 ln3/2)t/τ}+w₂e^{-(6 ln3)t/τ}` mit dem **det'-sauberen Bend**
`ln3/ln(3/2)=2.7095`, Floor und Wall. `dynamic_recovery.py` weißt, subtrahiert die dominante
QNM, bildet die **Post-Merger-Residuen-Leistungs-Hülle** (binned RMS) und fittet das
Fixed-Bend-Template (Ratio profiliert: jede Ratio = ein nichtlinearer Raten-Scan → gut
konditioniert, anders als ein freier 2-Exp-Fit) gegen ein Single-Exponential-Nullmodell +
Off-Source-Hintergrund. **Realdaten-Ergebnis (GW150914, GW190521): `NO_KERNEL_RECOVERY`** —
abklingende Hüllen sind Rest-Ringdown (`q̂≈1`, **nicht** der Bend). **Ehrlicher, maschinell
geprüfter Kern-Befund:** (i) **innerhalb EINER monotonen Recovery ist der Bend entartet** — die
exakte Walled-Clock-Kurve wird von *Floor + einem* Exponential mit Zwei-Moden-R²-Gewinn von nur
**≈1.3×10⁻³** gefittet (selbst rauschfrei) → eine Einzel-BH-Ringdown-Residuum kann das
Ratenverhältnis 2.7095 **nicht** tragen; (ii) die **unterscheidende** dynamische Signatur ist der
**log-periodische Kamm über eine KASKADE** bei `ω=2π/ln((3/2)⁶)=2.583`, Amplitude
`ε~exp(-π²/ln λ)≈0.017` (~2%, das QT.02-Unterdrückungsgesetz) — eine Einzel-Ringdown ist **keine**
Kaskade. ⇒ Der GW-Einzelevent-Kanal ist für den dynamischen Bend **strukturell `data_limited`**;
der sensitive Hebel ist die **zeitaufgelöste Recovery-SEQUENZ** einer Repeater-Quelle
(FRB-Repeater / Glitch-Train), nicht eine One-Shot-Ringdown. **Kein Recovery-Claim** (Kernel =
Obergrenze). Output: `results/dynamic_recovery.{json,png}`.

---

## 5b. Pulsar-Glitch-Recovery — `pulsar-glitch-recovery/` (problem_1.txt, die fehlende Cross-Domain-Säule)

`problem_1.txt` benennt als **stärkste mögliche TFPT-Signatur** nicht einen Einzeltreffer,
sondern dass **derselbe** eingefrorene Boundary-Recovery-Kernel `{1,(2/3)⁶,(1/3)⁶}` (Schritt
`3/2`) in **drei physikalisch unverwandten** Transienten-Datenwelten auftaucht: FRB-Recovery
(`frb-tfpt-signatures` FRB.02/09), GW-Ringdown-Residual (`gw-ringdown-echo`) **und
Pulsar-Glitch-Recovery**. Die ersten beiden Säulen gab es; **diese Säule schließt das
Dreieck** gegen die echte **Jodrell-Bank-Glitch-Datenbank** (Basu+2022; 726 Glitches, 222
Pulsare, 723 mit `Δν/ν`).

| Kanal | Signatur | Methode + Null | Ergebnis |
|---|---|---|---|
| **PG.01** | `Δν/ν` log-periodisch bei TFPT-Ratio (`(3/2)^k` oder §C `{1+φ₀,4,8,8π}`) | Rayleigh-Log-Periodogramm + gezielte Einzelratio-Tests, kalibriert gegen **drei** Nulls (Log-Normal, formerhaltendes KDE, **entscheidend** populations-kontrollierter GMM-Bootstrap) + Look-Elsewhere (Bonferroni) | **Null** — die einzige Struktur ist die Bimodalität |
| **PG.02** | aufeinanderfolgende **Größen** schreiten mit Kernelfaktoren (`\|Δlog s\|` auf `{log 3/2,(3/2)³,(3/2)⁶}`) | Per-Pulsar-Comb-Anteil vs **Within-Pulsar-Shuffle** der rohen Größen (umordnen, *dann* Log-Ratios neu berechnen; immun gegen globale Bimodalität) | **Null** (frac 0.20 vs 0.19, p≈0.27, 68 Pulsare) |
| **PG.03** | Inter-Glitch-**Wartezeit**-Ratios auf demselben Comb | Per-Pulsar vs Within-Pulsar-Shuffle der rohen Wartezeit-Intervalle (umordnen, dann Ratios neu berechnen) | **Null** (frac 0.22 vs 0.25, p≈0.93, 50 Pulsare) |
| **PG.04a** | Recovery-Fraktion `Q ∈ {φ₀,2φ₀,4φ₀,8φ₀,1−φ₀}` | KDE + Uniform-Null auf dem Yu+2013-`Q`-Set | **Null** (frac 0.10 vs 0.22, p≈1.0) |
| **PG.04b** | Multikomponenten-`τ_d` bilden Kernel-Leiter `(3/2)^k` (Multiskalen-**DSI**) | Per-Glitch `τ_{i+1}/τ_i` vs `τ_d`-Shuffle | **Null** (13 Glitches, p≈0.69) |

**Befund (ehrlich).** Die Glitch-Größen sind **nicht** ein einfaches Log-Normal (KS p≈0) und
multimodal (GMM `best_k=3`, ΔBIC≈157). Ein Log-Periodogramm findet **echte** log-periodische
Struktur bei Ratio **≈9.96** gegen die glatten Nulls (p≈0.002) — aber das ist die **bekannte
2-Populations-Bimodalität** (große Vela-Typen vs kleine Crab-Typen, ~1 dex auseinander): sie
**verschwindet unter dem populations-kontrollierten Null** (p≈0.075), und das beste Ratio ist
**kein** preregistrierter TFPT-Wert (13% neben `(3/2)⁶`). Die groben Kandidaten `8`, `8π`
leuchten nur, weil sie auf demselben ~1-dex-Abstand reiten (`p_smooth<0.01`, aber `p_gmm>0.28`);
`(3/2)⁶` hat ein rohes `p_gmm=0.032`, **fällt aber durch die Look-Elsewhere-Korrektur** (×7).
Die entscheidenden, bimodalitäts-immunen **Per-Pulsar-Leitern (PG.02/03) sind null** (Größe p≈0.27, Wartezeit p≈0.93; der Within-Pulsar-Shuffle ordnet die rohen Größen/Intervalle um und berechnet die Log-Ratios neu).

**PG.04 (Recovery, aktiviert).** Aus dem **echten** Yu+2013-Recovery-Set (arXiv:1211.2035
`expTab.tex`, 60 Komponenten / 46 Glitches, inkl. der Multikomponenten-Recoveries von Vela/Crab):
die Healing-Fraktion `Q` ist **nicht** an φ₀-Vielfachen geclustert (frac 0.10 vs ~0.22 Zufall,
p≈1.0 — eher *weniger* als zufällig), und die Multikomponenten-Decay-Zeiten `τ_d` bilden **nicht**
die Kernel-Leiter (p≈0.69). Damit ist PG.04 **kein** `data_limited` mehr, sondern ein echter Null.

→ **Sauberer Cross-Domain-Null / Konsistenz in allen vier Kanälen.** Die Pulsar-Säule verhält
sich exakt wie das FRB-Energie-Kaskaden-Resultat: echte *generische* Diskretheit (hier die
astrophysikalische Bimodalität), **aber nicht** der TFPT-Kernel. Der eingefrorene Kernel
**maskiert sich nicht** in einem dritten, unverwandten Datensatz. Die Maschinerie ist
**injection-validiert** (`tfpt-pulsar validate`: injizierter `(3/2)³`-Comb p≈0.003 erkannt,
synthetisch-bimodale Verteilung p≈0.93 verworfen). **Datenquellen:** Jodrell Bank Glitch
Catalogue (Basu+2022, MNRAS 510, 4049); Yu+2013 (MNRAS 429, 688).

**PG.05 — der DYNAMISCHE Recovery-Kamm auf echtem Crab-`ν(t)` (`tfpt-pulsar dynamic`, NEU).**
PG.01–04 testen statische Ratios; PG.05 testet die **dynamische** Signatur auf einer echten,
zeitaufgelösten Recovery-*Wellenform* — genau das, was die Summary-Tabellen nicht haben. Nach dem
GW-Stage-2-Befund (Bend einer Einzel-Recovery ist entartet, Zwei-Moden-Gewinn ~1e-3) ist die
*unterscheidende* dynamische Signatur der **log-periodische Kamm** bei `ω=2π/ln((3/2)⁶)=2.583` über
eine Recovery mit weitem `ln(t)`-Bereich. Datenquelle: die **Jodrell-Bank-Crab-Monatsephemeride**
(`crab2.txt`, 479 monatliche `ν`/`ν̇`-Punkte 1988–2026) — der einzige öffentliche Datensatz mit der
nötigen `ln(t)`-Spanne. `nu_recovery.py` detektiert Glitches aus den `ν̇`-Stufen (10, inkl.
2017-Riesenglitch), bildet pro sauberem Inter-Glitch-Segment die `ν̇`-Recovery und prüft, ob der
Kern-`ω` im Periodogramm **besonders** ist (Polynom-in-`ln τ`-Baseline absorbiert den glatten
Trend → ein reines Potenzgesetz wird nicht geflaggt). **Ergebnis: `data_limited` — kein Kern-Kamm,
aber Detektor validiert:** injizierte geometrische Kaskade bei `ω` erkannt (p≈0.002), glattes
Potenzgesetz korrekt verworfen (p≈0.15); über **7** saubere Segmente ist `ω` in **keinem** besonders
(p≈0.12–0.44). Ehrlicher Scope: Monatskadenz untersamplet den schnellen (Tage-)Transienten, also
nur die langsame Inter-Glitch-Relaxation; bei vorhergesagter Kamm-Amplitude `ε~exp(-π²/ln λ)≈2 %`
konsistent mit „unter Monatsreichweite". **Kein Claim.** Schärfer: Tageskadenz-Timing eines
Riesenglitches (Crab 2017) oder Vela (>2 Dekaden in `ln(t)`). **Datenquelle:** Jodrell Bank Crab
Pulsar Monthly Ephemeris (Lyne, Pritchard & Graham-Smith 1993, MNRAS 265, 1003; monatlich aktualisiert).

---

## 5c. Quantum-Testbed — `quantum-testbed/` (problem_1.txt: stärkste Quanten-Signatur + Reconsideration)

**Intern, kein Datum** (`evidence_class=internal_consistency`, `stage=not_applicable`). Baut den
eingefrorenen Kernel als Quantenobjekt und prüft die vorhergesagten Muster — und nimmt die
Reconsideration auf: *könnte die Signatur etwas anderes als ein statisches Verhältnis sein?*

- **QT.01 Entanglement-Spektrum.** Der Gauß-Zustand (`Γ(t)`, v161) mit Besetzungsspektrum =
  Kernel `{1,(2/3)⁶,(1/3)⁶}` liefert **exakte** Identitäten: Surprisals `−ln ζ = {6ln(3/2)=Δ,
  6ln3}`, Verhältnis `ln3/ln(3/2)=2.7095` (= die FRB.09-Recovery-Clock `g1/g2`), eine **protected
  zero-surprisal (decoherence-free) Mode** (das „Gesetz"), und Schmidt-Recovery `I_n=(2/3)^{6n}`.
- **QT.02 Quench-DSI + Unterdrückungsgesetz.** Eine geometrische Raten-Leiter relaxiert
  log-periodisch bei `ω=2π/ln λ`; die Amplitude ist `~e^{−π²/ln λ}` → nachweisbar **nur** für den
  groben **Energie-Gap `(3/2)⁶`** (p≈0.002), exponentiell **unsichtbar** für den Carrier `3/2`
  (p≈0.97); ein nicht-geometrischer Kontroll-Lauf ist Null. **Das erklärt die statischen
  Pulsar/FRB-Nulls** und liefert die konkrete nächste Suche (Recovery-Wellenformen bei `ω≈2.58`).
- **QT.03 Free-Fermion-OTOC.** `H_TFPT` mit Kernel-Leiter-Spektrum; quadratischer Kommutator
  `C_ij(t)=|G_ij(t)|²` (ballistische Operator-Ausbreitung; On-Site-Return-DSI explorativ).
- **QT.04 Exakte gewallte Uhr (`v124`/`v126`/`v147`).** `rate(n)=−6 ln(1−n/3)`, Pol bei `n=3`:
  Zwei-Moden-Recovery + Floor, **det'-sauberer Bend `2.7095`**, Sheet-Slope `2=|Z₂|`, harter Wall.
  Daraus ein **Matched-Filter-Wellenform-Diskriminator** (Fixed-Ratio-2.7095-Template vs. freies
  Doppel-Exponential): Kernel-Recovery → erkennt 2.71; Nicht-Kernel (Ratio 5) → verworfen.
- **QT.05 Anyon-MTC / Statistik-Schicht (`v241`/`v242`/`v243`).** Der Carrier-Diskriminant-MTC
  (`Z4×Z4`, `q=(5x²+3y²)/8`): **16 Sektoren → 6 Bosonen / 2 Fermionen (`θ=−1`, Phase `π` = m=2) /
  8 Anyonen**; **diskrete Statistik-Phasenquanten `π/4` (Spin, 8.-Einheitswurzeln) und `π/2`
  (Braiding)**; `c=8` (Gauss-Milgram); integrable faktorisierte S, trivial auf `(E8)₁`. → eine
  **andere Signaturklasse** als die Recovery-Ratios; das FRB.08-„Fundamental m=2" ist der
  **vorhergesagte Fermion-Sektor**, kein Null.

**Neue empirische Hooks aus dem Spektral-Action-Abschluss (`v244`/`v245`), real gegen Daten gerechnet
im neuen Experiment `gauge-unification/`:** **`sin²θ_W = 3/8`** an der Spektralskala
(NCG/SU(5)-Unifikation `g3=g2=√(5/3)g1`). **Ehrliches Ergebnis** (1-Loop-RGE vs PDG): `3/8` ist der
Standard-SU(5)/SO(10)-GUT-Wert (TFPT erbt ihn); die SM-Kopplungen treffen sich bei `α1=α2` ~10¹³ GeV,
aber `α3` verfehlt um **13%**, und `3/8 → sin²θ_W(M_Z) = 0.2076` vs gemessen `0.23122` — die
**universelle ~10%-GQW-Lücke** (SM-Nicht-Unifikation, braucht SUSY/Thresholds, **nicht
TFPT-spezifisch**). Plus Carrier-`16` = **eine anomaliefreie SM-Generation** (`ΣY=ΣY³=0`, ein
Higgs-Dublett). Das sind die **genuin neuen** Signaturen der vollendeten Diskret→Dynamik-Kette
(`v238`–`v245`) — jenseits des Recovery-Kernels; `sin²θ_W` ist `data_limited`/`weak` getypt (der
GUT-Wert ist nicht TFPT-unterscheidend, die `M_Z`-Lücke universell).

→ **Strukturelle Bestätigung**, dass der Kernel in der Algebra/Dynamik lebt — plus die scharfe,
ehrliche Aussage, *wo* eine reale Signatur noch sitzen könnte (dynamischer Bend/Floor/Wall in
Wellenformen + diskrete Statistik-Phasen `π/4`,`π/2`,`π` + `sin²θ_W=3/8`-Unifikation), nicht
statische Ratios. Kein neues Datum (QT-Schicht intern; `sin²θ_W` downstream Bridge).

---

## 6. Labor-`F_transfer`-Residuen — `lab-residuals/` (search.txt §7,8,9)

Drei unabhängige Laborkanäle, **alle `[C]`** (downstream bridges / frontier; nie `[E]`).
Verdicts **pro Baseline/Branch gesplittet** — kein Ampel-Urteil über Modellannahmen.

### Myon g−2 — `Δaµ = 45/(2¹⁹π⁹) = 2.879×10⁻⁹` (exakte Compilerzahl, Deutung = Bridge)
| SM-Baseline | Residuum `a_exp−a_SM` | Pull | Status |
|---|---|---|---|
| WP2020 dispersiv | (2.62±0.45)×10⁻⁹ | +0.58σ | **viable** |
| WP2025 Lattice | (0.39±0.65)×10⁻⁹ | +3.86σ | **tension** |
| CMD-3-related / future | — | — | Platzhalter (datenlimitiert) |

→ baseline-abhängig: passt zur alten dispersiven Anomalie, in Spannung mit der
Lattice-HVP 2025. Quellen: Fermilab final (PRL 135 101802, 2025), Theory Initiative
WP2020 / WP2025 (arXiv:2505.21476).

### Seltene Kaonen — downstream bridge
| Zerfall | TFPT | Daten | Pull |
|---|---|---|---|
| `K⁺→π⁺νν` | 9.45×10⁻¹¹ | NA62 2016–2024: (9.6⁺¹·⁹₋₁.₈)×10⁻¹¹ | **−0.08σ** (im Kill-Fenster [7,12]) |
| `K⁺→π⁺νν` | 9.45×10⁻¹¹ | NA62 2016–2022: (13.0⁺³·³₋₃.₀)×10⁻¹¹ | −1.13σ |
| `KL→π⁰νν` | 3.33×10⁻¹¹ | KOTO < 2.2×10⁻⁹ (90% CL) | datenlimitiert (weit unter Reichweite) |

→ **sehr starke Konsistenz** mit NA62 2016–2024, aber downstream bridge (externe
Short-Distance-Funktionen), kein Compiler-Treffer. Quellen: NA62 (arXiv:2604.12649;
JHEP 02 (2025) 191), KOTO 2024.

### Axion
- **Haloskop-Marker** `m_a=23.8 µeV (≈5.76 GHz)`, `f_a=M_scal/128`: im HAYSTAC/CAPP-Band,
  **nicht** bei DFSZ ausgeschlossen → **datenlimitiert**. Quellen: ADMX/HAYSTAC/CAPP.
- **Relik-Branches** (voller Finite-T-Misalignment-Solve, `ftransfer/axion_relic/*.py`):
  - `DM.AXION.HILLTOP.01` (θᵢ=170.4°, `Ωₐh²≈0.66`) → **Spannung (Überproduktion ~5.5×)**.
  - `DM.AXION.SPINE.01` (θᵢ=3π/5=108° aus `N_fam/g_car=3/5`) → **gelöst, konsistent**:
    `spine_finiteT_solve.py` liefert **`Ωₐh²=0.125`** (zentral), robust über die ganze
    Akzeptanzband **[0.090, 0.151]** bei chi(T)-Exponent n=7…9 und g\*(T) ±10% — landet
    *ohne Tuning* auf `Ω_DM=0.12`. Anharmonischer Faktor nur 1.19 (vs Hilltop-Runaway).
    Der Spine-Winkel ist damit der überlebende Axion-DM-Branch; der Hilltop bleibt überproduzierend.
  - **Unabhängiger Solver-Check** (`spine_independent_check.py`): zwei *andere* Methoden —
    sudden/adiabatischer WKB-Readout (mit power-law **und** tanh-`χ(T)`) und die semi-
    analytische Anharmonik-Skalierung — geben `Ωₐh² ∈ [0.125, 0.143]`, **alle im Band**. Das
    Ergebnis ist robust gegen Methode und `χ(T)`-Parametrisierung (nicht ein Artefakt einer
    Integration).
  - **Haloskop-Overlay** (`tfpt-lab haloscope`): bei `m_a=23.8 µeV` (5.77 GHz) ist
    `g_aγγ^DFSZ=3.6×10⁻¹⁵`, `g_aγγ^KSVZ=9.3×10⁻¹⁵ GeV⁻¹`. Der Punkt liegt im **HAYSTAC-Band**
    (~2–3× KSVZ-Reichweite) → **weder KSVZ noch DFSZ ausgeschlossen**, ein Near-Future-
    Haloskop-Ziel (Plot `results/haloscope_overlay.png`).

---

## 7. Geparkt + theorieseitig

- **`quantum-recovery-analog/`** — geparkt. Zentrale Dynamik `I_n ~ (64/729)^n`; ohne
  echten physischen Datensatz bewusst nicht gebaut (Analogie-Risiko). Aktivierung nur bei
  einem realen Boundary-Recovery-Experiment mit messbarem `I_n`/Fidelity-Recovery.
- **`ftransfer/`** — theorieseitige `F_transfer`-Solver (kein Daten-Confronting):
  Axion-Relik (finite-T), Koide-Source-to-Pole (`53/54`), Leptogenese-Boltzmann (`η_B`),
  QCD-Matching `m_p/m_e`.
- **`lean4-carrier-rigidity/`** — formaler Lean-4-Beweis des Carrier-Polynoms
  `6Y²−Y−1=0` und der Hyperladungs-Spur.

---

## 7b. Erweiterte Domänen — scharfe Compiler-Vorhersagen + Recovery-Channel

Über die search.txt-Suchräume hinaus, motiviert aus der Origin Story / dem
Recovery-Mechanismus. Jede Domäne ist self-contained (`pyproject.toml`, `src/<pkg>/`,
`data/`, CLI `analyze`, README).

### 7b.1 Recovery-Channel (Test C) — `recovery-channel/` (datenunabhängig)
**Zweck.** Den Recovery-Kernel `{1,(2/3)⁶,(1/3)⁶}` *explizit* als CPTP-Quantenkanal
`R: H_bulk → H_observable` bauen und die Standard-Quanteninfo-Axiome prüfen — die
datenunabhängige „Informationsprojektor"-Reframing (search.txt-Folgevorschlag, Test C).
Packt, was die Verifikations-Suite strukturell schon zeigt (`v155` quasi-free,
`v160` Kumulanten, `v161` Bogoliubov `Γ(t)`).

**Konstruktion.** Jeder Kernel-Eigenwert `λ` = Qubit-Amplitude-Damping-Kanal mit
Anregungs-Überlebenswahrscheinlichkeit `λ` (Damping `γ=1−λ`): eine geschützte `λ=1`-Mode
(das „Gesetz"/Attraktor) + zwei kontrahierte Moden `λ₂=(2/3)⁶≈0.0878`, `λ₃=(1/3)⁶≈0.00137`.

**Checks & Ergebnis (alle bestanden):**
- **CPTP** — Trace-Erhalt (`ΣKᵢ†Kᵢ=I`) + komplette Positivität (Choi-Matrix PSD, min-Eig
  ≈ 0 bis Maschinengenauigkeit) für alle drei Moden.
- **Recovery-Rate** — `Rⁿ` dämpft mit `λⁿ=(2/3)^{6n}` = Page-Recovery `Iₙ` (exakt
  reproduziert: 8.78e-2, 7.71e-3, 6.77e-4 für n=1,2,3).
- **Data-Processing-Ungleichung** — relative Entropie kontrahiert `S(Rρ‖Rσ)≤S(ρ‖σ)`
  (der Kanal erzeugt nie Information).
- **QEC** — die `λ=1`-Mode ist eine **decoherence-free / Knill-Laflamme**-Code (KL erfüllt);
  die kontrahierten Moden verletzen KL → nicht korrigierbar; der Spektralgap `(2/3)⁶` ist
  die Leckrate.
- **Page-Kurve (Test B).** Mit der TFPT-Hawking-Law `P_H=c₃/(1920M²)` ist
  `S_BH(t)/S₀=(1−t/τ)^{2/3}`; die Insel/unitäre Min-Vorschrift `S_page=min(S_BH,S_rad)`
  dreht bei **`t/τ=1−(1/2)^{3/2}=0.6464`** — *exakt* die TFPT-Page-Zeit
  `t_Page=(1−1/(2√2))τ` (numerisch 0.6466).
- **Petz-Recovery + rank-one Baby-Universe (`tfpt-recovery petz`, Companion zu `v221`).** Der
  gapped Transport `T` (CPTP, doppelt-stochastisch auf dem Cusp-Weight-3-Raum) kontrahiert
  unter Iteration auf einen **rank-one** Projektor (den eindeutigen Fixpunkt/„Gesetz") mit der
  **exakten** Rate `‖Tⁿ−P_∞‖=(2/3)^{6n}` (numerisch bestätigt 8.78e-2, 7.71e-3, …). Der
  boundary-zugängliche Algebra kollabiert am Kernel-Tempo auf **eine Dimension** — die
  TFPT-Realisierung des **1-dim Baby-Universe-Hilbertraums** (Engelhardt 2025; JHEP 12 (2025)
  159). Dazu ein **expliziter Petz-Recovery-Operator** `R_P` (CPTP, recovers reference; nur die
  `λ=1`-Mode für alle Zustände = KL): das `[C]` Petz-Identification, das `v221` aufgeschoben
  hatte, jetzt realisiert. Negativkontrollen (freies Ratio → `rⁿ`; entartetes Spektrum → kein
  rank-one) greifen.

**Typisierung.** `evidence_class=internal_consistency` — interne Konsistenzprüfung,
**keine externe Messung**; nicht im selben Evidenz-Korb wie CMB/Kaon. **Kein neues Datum.**

### 7b.2 CMB-Inflation (Starobinsky/Scalaron) — `cmb-inflation-scalaron/`
**Frozen.** Niedrig-Krümmungs-Gravitationszweig `R+R²` (Spektral-Aktion) → Starobinsky mit
`M_scal=c₃^{7/2}M̄=3.06×10¹³ GeV` (`[E]`); `N⋆` ist Reheating-Input (`[C]`, Band [50,60];
slow-channel-Punkt 51.4). Read-offs: `n_s=1−2/N⋆`, `r=12/N⋆²`, `A_s=N⋆²/(24π²)·c₃⁷`.

| Observable | TFPT (N⋆=51.4) | Daten | Pull |
|---|---|---|---|
| `n_s` | 0.9611 | Planck 0.9649±0.0042 | **−0.91σ (konsistent)** |
| `n_s` | 0.9611 | P-ACT-LB+DESI 0.9743±0.0034 | **−3.9σ (Spannung)** |
| `r` | 0.0045 | BICEP/Keck BK18 <0.036 | unter Limit |
| `r` | 0.0045 | CMB-S4 σ_r≈5×10⁻⁴ | **9σ Zukunfts-Falsifikator** |
| `A_s` | 1.76×10⁻⁹ | Planck 2.10×10⁻⁹±0.03 | **−11.3σ** → bevorzugt N⋆≈56 |

**Branch-Resolver (P1).** Erzwingt die Typ-Entscheidung: ist `N⋆=51.4` prediction_of_record
(dann A_s −11.3σ Killtest) oder ist das **Band [50,60]** der Record (dann profiliert A_s auf
**N⋆=56.1** → `n_s=0.9644` bei −0.1σ Planck, `r=0.0038`, A_s konsistent → **downstream
bridge**)? **Bayes-Faktor** (n_s+A_s-Likelihood, flacher Bandprior): `ln(B_profiled/fixed) =
+62` (Planck) bzw. `+65` (P-ACT-LB+DESI) — die Daten bevorzugen das Band **entscheidend**
gegenüber dem Fixpunkt, also kann A_s **nicht** als volle prediction_of_record bei N⋆=51.4
geführt werden. **CMB-S4-Forecast:** `r=0.0045` ist ein **9σ**-Detektionsziel (σ_r≈5×10⁻⁴).
**Entscheidung FINALISIERT** (P1): Wegen `ln B = +62` ist der **Record das Band [50,60]**;
`N⋆=51.4` ist der **preferred slow-channel Branch** (ein Punkt im Band, nicht der Record);
`A_s` ist eine **downstream reheating Bridge**. Konsequenz: `n_s`/`r` bei 51.4 bleiben
prediction_of_record (im Band); `A_s` bei fixem 51.4 ist ein **−11.3σ Branch-Stress
(`downstream_bridge`)**, *kein* Record-Killtest; die record-konsistente Lesart profiliert `A_s`
auf N⋆≈56. Beide A_s-Modi sind eine `alternative_group=Nstar_branch` (nie doppelt zählen).
Quellen: Planck 2018 VI, BICEP/Keck BK18, P-ACT-LB+DESI, CMB-S4-Forecast.

### 7b.3 Neutrino-/CKM-Mixing — `neutrino-mixing/` (prediction_of_record)
**Frozen** (aus `c₃`/`φ₀`): `sin²θ12=1/3−φ₀/2=0.306747`; `sin²θ13=φ₀ e^{−5/6}=0.0231`;
`sin²θ23=1/2` (Oktant nicht selektiert); `δ_CKM=π/3+3λ²=68.65°` (CKM-CP-Phase, kanonisch
`v88`/`FLAV.CP.01`; anderer Sektor).

| Observable | TFPT | Daten | Pull |
|---|---|---|---|
| `sin²θ12` | 0.306747 | NuFIT 6.0 0.307±0.012 | **−0.02σ** |
| `sin²θ12` | 0.306747 | JUNO 0.3092±0.0087 | −0.28σ |
| `sin²θ13` | 0.0231 | NuFIT 6.0 0.02195±0.00058 | **+2.0σ** (bekannte Spannung) |
| `sin²θ23` | 0.5 | NuFIT 6.0 0.470±0.017 | +1.76σ (Oktant offen) |
| `δ_CKM` | 68.65° | LHCb γ 64.6°±2.8 | +1.45σ |
| `δ_PMNS` | 240° (4π/3) | NuFIT 6.0 NO best fit 212°⁺²⁶₋₄₁ | **+1.08σ** (consistent) |

→ θ12 ist ein **scharfer Treffer**; θ13 trägt die **~2σ-Spannung** (teilt `φ₀` mit β → siehe
Seed-Stresstest 7b.7). **NEU (v231/v233):** die leptonische CP-Phase `δ_PMNS=4π/3=240°` ist
strukturell an `δ_CKM` gekoppelt (eine hexagonale `μ6`-CM-Einheit `ρ=e^{iπ/3}`, Sheet-aufgespalten:
`δ_PMNS=δ_CKM,lead+π`); gegen den NuFIT-6.0-NO-best-fit `+1.08σ` (CP-verletzende Region), `[C]`
downstream Bridge, schwach unterscheidend bis DUNE/HyperK. Quellen: NuFIT 6.0 (arXiv:2410.05380),
JUNO (2025), LHCb γ-Kombination.

### 7b.4 GW `v_GW=c` — `gw-speed-multimessenger/`
**Frozen.** Ein gemeinsamer Lorentz-Kegel ⇒ `(v_GW−c)/c=0` exakt (namentlicher
Falsifikator; Gravitations-Analogon zu FRB.01). **Daten:** GW170817 + GRB170817A
(Abbott+ 2017, ApJL 848 L13): GRB kam 1.74 s nach dem Merger über ~40 Mpc → Bound
`[−3×10⁻¹⁵, +7×10⁻¹⁶]`; naiver Zentralwert +4.2×10⁻¹⁶. TFPT-0 liegt im Bound →
**Konsistenz (Killtest bestanden)**, keine Detektion (Standard-GR sagt dasselbe).

### 7b.5 QNM-Ringdown `ln3` — `gw-ringdown-spectroscopy/` (schwarzloch-direkt)
**Frozen** (`v57`/horizon_readouts, [C]/[P]): asymptotische Schwarzschild-QNM
`ω_R/T_H → ln3 = ln N_fam`; Flächenquant `ΔA=4 ln3 l_p²=ln(N_fam⁴)=ln 81`. Numerische
Identität `ln3=ln N_fam=1.0986` exakt. **Scope-Ehrlichkeit:** der asymptotische Wert lebt im
Hoch-Oberton-Limit (`M·ω→ln3/(8π)=0.0437`), gemessen wird der n=0-Grundton (`M·ω≈0.3737`,
Faktor 8.5 entfernt). GW150914/GW250114 zeigen nur n=0 → **datenlimitiert**; direkter Test
braucht Hoch-Oberton-Spektroskopie. Die physisch *direkteste* BH-Recovery-Signatur und
zugleich die am weitesten von heutiger Testbarkeit entfernte.

### 7b.6 Λ/H₀-Engine — `lambda-h0-engine/`
**Frozen** (ein EM-Fixpunkt `α⁻¹`): `ρ_Λ/M_pl⁴=(3/256π⁴)e^{−2α⁻¹}` (122.95 Größenordn.,
unreduziert); `ρ_Λ/M̄_pl⁴=(3/4π²)e^{−2α⁻¹}` (120.15, reduziert); `S_dS·ρ_Λ=1/(128c₃⁴)=32π⁴`
(exakte dimensionslose Identität); `H₀/M̄~e^{−α⁻¹}/(2π)`.

| Größe | TFPT | gemessen (Planck Ω_Λ,H₀) | dev |
|---|---|---|---|
| `ρ_Λ/M_pl⁴` (Größenordn.) | 122.948 | 122.943 | **0.004** |
| `ρ_Λ/M̄_pl⁴` (Größenordn.) | 120.147 | 120.143 | 0.004 |
| `S_dS·ρ_Λ` | 32π⁴ = 3117.09 | (Identität) | exakt |
| `H₀/M̄` (log₁₀) | −60.31 | −60.23 | 0.08 dex |

→ ein `α⁻¹`-Motor für Λ, S_dS und H₀ — **Konsistenz / Metrologie-Kohärenz**, *keine*
Ableitung der absoluten Skala (das ist der eine Anchor). Achtung: nicht als „Λ
vorhergesagt" verkaufen; H₀/Ω_Λ dürfen nicht reimportiert und dann als Ergebnis gezählt
werden.

### 7b.7 Shared-Seed-Stresstest — `seed-consistency/` (P1, der θ13-Test)
**Zweck.** Ist θ13 der erste Riss im Seed-Block? Ein Seed `φ₀` fixt vier Observablen in
*getrennten* Pipelines; jede Messung wird zu `φ₀` invertiert, dann Inverse-Varianz-
Joint-Fit + Leave-one-out (Δχ² bei Entfernung) + dominanter Pull (χ²-Anteil).

| Bein | Pipeline | implied φ₀ | z(frozen) | z(joint) | Δχ²(LOO) |
|---|---|---|---|---|---|
| β | CMB | 0.04715 ± 0.01623 | −0.37 | −0.35 | +0.13 |
| Ω_b | BBN | 0.05311 ± 0.00132 | −0.05 | +0.15 | +0.03 |
| **θ13** | **reactor** | 0.05051 ± 0.00133 | **−2.00** | **−1.80** | **+3.54** |
| Cabibbo | CKM | 0.05314 ± 0.00043 | −0.08 | +0.54 | +1.67 |

→ Joint `φ₀=0.05291`, **χ²/dof=1.23 → Block hält** (mit globalem NuFIT-θ13). **θ13 ist der
dominante Pull** (88% des χ², −1.80σ). **Akzeptanzregeln (eingefroren):** θ13 >3σ vom
gemeinsamen Seed → PMNS-θ13 als *transfer-corrected* (μτ-Breaking) flaggen; **zwei** Beine
>3σ → Shared-Seed-Block fällt. Aktuell keine Regel ausgelöst. Beine aus CMB/BBN/reactor/CKM
(keine vier CMB-Schnitte). Quellen: ACT DR6, BBN D/H, NuFIT 6.0, PDG.

**v2 (`tfpt-seed v2`, P1-Härtung).** θ13 wird in **reactor-only** (Daya Bay) als Fit-Bein und
**global** (NuFIT) als *Shadow*-Sensitivität getrennt — beide nie gemeinsam im Fit (≈0.9
korreliert). Eine **Kovarianzmatrix** treibt einen GLS-Joint-Fit (diagonal per Konstruktion,
Off-Diagonals bleiben der ehrliche Ort für geteilte Systematiken); dazu **Leave-one-
experiment-family-out** und ein **Posterior-Predictive-Check**. Ergebnis: reactor-θ13
χ²/dof=1.37, **PPC p=0.25**, θ13 dominiert mit **90% des χ²** bei −1.92σ; reactor-only und
global liefern **dasselbe Verdikt** (Block hält). Genau die richtige Diagnose: der Seed ist
kohärent, aber θ13 ist der erste ernsthafte Risskandidat.

**v3 (`tfpt-seed v3`, reactor-only aus den Einzelexperimenten).** Statt eines pauschalen
reactor-θ13 nutzt v3 die **drei unabhängigen Detektoren** getrennt — Daya Bay
(`0.02175±0.00065`), RENO (`0.02282±0.00165`), Double Chooz (`0.02619±0.00317`) — zeigt den
implizierten `φ₀` jedes Experiments und bildet eine saubere reactor-only-Kombination
**`sin²θ13=0.02204±0.00059`**. Nur diese geht in den Fit; NuFIT-global bleibt **Shadow**
(nie beide im Fit — der globale Fit enthält die Reactor-Daten bereits). Ergebnis:
**χ²/dof=1.00, PPC p=0.39**, θ13 dominant bei **−1.62σ** (88% χ²), Shadow(global) χ²/dof=1.23
→ **gleiches Verdikt**. Die volle Reactor-Kombination (leicht höher als Daya Bay allein)
entspannt den θ13-Zug — kein Statistik-Origami, keine vier CMB-Beine, global und reactor-only
nie doppelt gefüttert. JUNO-θ13 wird ergänzt, sobald stabil.

### 7b.8 EHT-Real-Data-Lauf — `eht-achromatic-residual/` (P1, echte Daten)
Voll dokumentiert in **§4** (echte 2023-D01-01-Polarimetrie, 4 Tage × 2 Bänder,
Band-zu-Band-EVPA +0.9°, RM~5×10⁵ rad/m²; Residual-Nulls `data_limited` bis GRMHD-Imaging).

---

## 7c. Entscheidungs-Tests (P1/P2: eigene Runner + Watchdogs)

### 7c.1 Dunkle-Energie-`w`-Watchdog — `dark-energy-w-watchdog/` (P1, NEU)
TFPT: `w=−1` exakt (Λ = konstantes Vakuum, `S_dS·ρ_Λ=32π⁴`). Konfrontiert den Punkt
`(w0,wa)=(−1,0)` mit den DESI-DR2-CPL-Kombinationen über die 2-D-Mahalanobis-Distanz
(`ρ(w0,wa)≈−0.9`, reproduziert die publizierten Signifikanzen auf ~0.2σ):

| Kombination | 2-D-Distanz von w=−1 | publiziert |
|---|---|---|
| DESI+CMB+Pantheon+ | 3.07σ | 2.8σ |
| DESI+CMB+Union3 | 3.87σ | 3.8σ |
| DESI+CMB+DES-SN5YR | **4.37σ** | 4.2σ |

**Overlap-aware:** Die drei SN-Compilations teilen Low-z-SNe ⇒ *Alternativen*, nicht
unabhängig. Headline = **stärkste Einzelkombo 4.4σ**; das naive Produkt **6.6σ** wird
explizit als *Scheinsignal* markiert (genau die Falle, die der Review warnt). **Kill:** `w≠−1`
bei ≥5σ in einer einzelnen systematik-kontrollierten, overlap-aware-Kombination → trifft die
Λ/H₀-Engine. Aktuell **armed, nicht ausgelöst** (`data_limited`).

### 7c.2 Rare-Kaon-Flavor-Bridge — `rare-kaon-bridge/` (P1, NEU)
Testet die Flavor-Bridge als **Geometrie**, nicht einen Einzeltreffer:

| Bein | TFPT | Daten | Pull |
|---|---|---|---|
| `BR(K⁺→π⁺νν)` | 9.45×10⁻¹¹ | NA62 (9.6⁺¹·⁹₋₁.₈)×10⁻¹¹ | **−0.08σ** ✓ |
| `δ_CKM / γ` | 68.65° | LHCb γ 64.6°±2.8 | **+1.45σ** ✓ |
| Jarlskog `J` | 3.03×10⁻⁵ | PDG (3.08±0.13)×10⁻⁵ | **−0.07σ** ✓ |
| `R_K=BR(KL)/BR(K⁺)` | **0.35238** | (KOTO-II) | nahe SM 0.40, respektiert Grossman-Nir (data_limited) |
| `BR(KL→π⁰νν)` | 3.33×10⁻¹¹ | KOTO < 2.2×10⁻⁹ | unter Limit (data_limited) |

→ 3/5 Beine direkte Datentreffer, Geometrie konsistent; aber **downstream Bridge** (`|Vcb|`,
`|Vub|`, Short-Distance = externe Nuisances). Diskriminator: KOTO misst BR(KL) → R_K.

### 7c.3 Higgs-Nahe-Kritikalität — `higgs-criticality/` (P2, NEU)
TFPT-Vorhersage: die **doppel-kritische Fläche** `λ(M_Pl)=0` **und** `β_λ(M_Pl)=0`. Mit dem
Buttazzo-2013-NNLO-Fit (arXiv:1307.3536, Gl. 61) extrapoliert + 1-Loop-`β_λ` aus den
M_Pl-Kopplungen: **`λ(M_Pl)=−0.0143±0.0057`** (`lambda_pull_sigma=2.5`),
**`β_λ(M_Pl)=+1.9×10⁻⁴`** (`near_zero`) — bemerkenswert nahe an (0,0), aber die exakte
Doppel-Kritikalität ist mild gespannt. **Stabilitäts-Posterior** (MC über `M_t/M_h/α_s`,
n=2×10⁵): **P(metastabil)=0.994**, P(stabil)=0.006 (≈2.5σ, reproduziert die publizierten
2.8σ); `λ(M_Pl)`-Median −0.0143, 68%-CI [−0.020, −0.009]. Verdikt von `M_t` dominiert.
**Konsistent** mit der Near-Criticality-Bridge, downstream RGE [C]; ein moderner 3–4-Loop-
Stack + MC-vs-Pol-Topmasse wäre der Paper-fähige nächste Schritt.

### 7c.4 Axion-Spine-Finite-T — `ftransfer/axion_relic/spine_finiteT_solve.py` (P1, gelöst)
Voll dokumentiert in §6 (Axion): θᵢ=3π/5 → **`Ωₐh²=0.125`**, robust [0.090, 0.151] über
chi(T)/g\*-Variationen → **konsistent, kein Tuning**. Damit ist der Spine der überlebende
Axion-DM-Branch (Hilltop überproduziert).

### 7c.5 QGEO-DtN-Mark-Locality — `theory-contracts/qgeo_dtn_mark_locality.py` (P2, Theory-Contract)
**Bewusst NICHT in der empirischen Scorecard** (reine Mathematik). Z4-Marken bei `θ=jπ/2`
geben `f=Σ_{j} g(θ−jπ/2)` mit Fourier-Support **nur `n≡0 mod 4`** ⇒ `[ρ,Λ]=0` ⇒ `ω∘ρ=ω`;
numerisch (N=64) auf ~1e-16 bestätigt, **mit Negativkontrollen** (Z3-Marken und 4 generische
Marken brechen den Kommutator, `[ρ,Λ]/|Λ|≈0.4–0.5`). **Contract hält.**

### 7c.6 Weitere getypte Scorecard-Watchdogs + offene P2-Solver
- **Neutrino-Absolutsektor:** `Σm_ν=5.88×10⁻² eV` (NO, **consistent**); `m_ββ=1.52×10⁻³ eV`
  (NO, **data_limited**).
- **Leptonische CP-Phase (`neutrino-mixing`, NEU geschärft):** `δ_PMNS=4π/3=240°` ist via
  `v231/v233` strukturell an `δ_CKM` gekoppelt — eine hexagonale `μ6`-CM-Einheit `ρ=e^{iπ/3}`,
  Sheet-aufgespalten (`ρ³=−1`): `δ_PMNS = δ_CKM,lead + π`. Gegen NuFIT 6.0 NO best fit
  (`212°⁺²⁶₋₄₁`, inkl. Super-K) **+1.08σ → consistent**, in der CP-verletzenden Region (CP-Erhaltung
  bei NO nur innerhalb 1σ); der nicht-präferierte No-SK-Fit (`177°`) zieht auf +3.32σ. **`[C]`
  downstream Bridge** (Deck bleibt `Z/4`, CP in der hexagonalen Phasenfaser), schwach
  unterscheidend bis DUNE/HyperK. `independence_group=cp_mu6_phase` (mit `δ_CKM` — keine zwei
  unabhängigen Treffer). Dieselbe `4π/3` ist die Dirac-Phase im `η_B`-Solve.
- **EDM-Null (`θ_eff=0`):** Neutron-EDM + Elektron-EDM beide **consistent** (PSI nEDM /
  JILA/ACME-Limits). Kill: robustes EDM-Signal inkompatibel mit `θ_eff=0`.
- **Leptogenese `η_B`** (Scalaron-Decuple, `ftransfer/leptogenesis_boltzmann/fboltzmann_solve.py`):
  **gelöst → konsistent.** Der **volle BDP-Boltzmann-ODE-Solve** (integrierte Effizienz
  `κ_f=0.092`, vs BDP-Fit 0.074 → validiert den Strip) liefert am **eingefrorenen** Schwerskala
  `M₁=M_scal φ₀²/AΛ=8.6×10⁹ GeV` mit `δ_νCP=4π/3` ein **`η_B=6.5×10⁻¹⁰`** vs beobachtet
  `6.1×10⁻¹⁰` — **Faktor 1.07, ohne freien `M_R`-Dial**. Bleibt `[C]` (Washout `m̃₁=m₃/AΛ`
  verankert; `M₁` über die Scalaron-Route, README 7c.6). Der frühere `data_limited`-„Solve
  pending" ist erledigt.
- **GW-Strain-Echo** (Stage 1): erst nach echter Strain-Pipeline + Kerr-Subtraktion +
  Injection- + Free-q-Kontrollen; bleibt `catalog_feasibility` (siehe §5). **P2, offen.**
- **Rare-Kaon tree-only CKM:** die `|Vcb|`/`|Vub|`-Nuisances in §7c.2 sind PDG-Werte
  (tree-dominiert); eine reine tree-level-Bridge (γ aus tree-B-Zerfällen, `|Vcb|`/`|Vub|`
  exklusiv-tree) ist der nächste Schärfungsschritt, sobald KOTO `BR(KL)` liefert.
- **Higgs 3–4-Loop-RGE:** die `higgs-criticality`-Bridge nutzt den Buttazzo-2013-NNLO-Fit;
  ein moderner 3–4-Loop-Stack + MC-vs-Pol-Topmasse für eine paperfähige Posterior-Stabilitäts-
  grenze ist **P2, offen** (die MC-Posterior P(metastabil)=0.994 ist schon implementiert).

---

## 7d. Black-Hole-Cosmology-Signaturen aus `problem_b.txt` (neu)

Drei datenkonfrontierbare Signaturen aus dem Black-Hole-Cosmology-Teil von `problem_b.txt`
(die übrigen Ideen dort sind exakte `verification/`-Mathematik, kein Datentest). Jede ist
self-contained und bewusst **konservativ getypt** — keine wird zur Entdeckung erklärt.

### 7d.1 CCBH `k=3 → w=−1` — `ccbh-dark-energy/` (downstream bridge)
TFPT-Lesart „black hole local, de Sitter global": das Nariai-Seam-Innere **ist** das
de-Sitter-Vakuum (`w_in=−1`, `S_dS·ρ_Λ=32π⁴`). Mit Croker-Weiner `k=−3w_in` folgt die
kosmologische Kopplung `k=3` **exakt**, also Populations-EoS `w_eff=−k/3=−1` (echte
kosmologische Konstante).

| Bein | TFPT | Daten | Pull |
|---|---|---|---|
| Kopplung `k` | `3` (exakt) | Farrah+2023 `3.11±0.79` | **−0.14σ** |
| Dichte `Ω_de` | `0.68` (CCBH, k=3) | Planck `Ω_Λ=0.6889` | −0.09σ (modellunsicher) |

→ `k=3` passt zum Farrah-Zentralwert, **aber die CCBH-als-DE-Deutung ist umstritten**
(Lacy/Amendola/Andrae&El-Badry/Mistele) → **downstream bridge, `data_limited`**. Es ist der
**Mechanismus** hinter dem `w=−1`, das `dark-energy-w-watchdog` gegen DESI prüft —
**alternative Lesart einer Frage** (`alternative_group=w_de_eos`, nie doppelt zählen).
**Kill:** robustes `k≠3` bei ≥3σ in einer systematik-kontrollierten SMBH-Wachstumsprobe.

### 7d.2 Gravastar/ECO `C=3/8` — `gravastar-compactness/` (search target)
Zwei unabhängige Konstruktionen landen auf demselben Rational und demselben de-Sitter-Ende:
TFPT-Nariai `Q_geom=3/8` (de-Sitter-Limes `1/2`) und Jampolski-Rezzolla 2026
(arXiv:2509.15302) Max-Kompaktheit `C=3/8` (Horizont `1/2`).

- **Normalform-Check (ehrlich):** exakter Rational-Match `3/8` + geteiltes Ende `1/2`, aber
  **keine** bewiesene `C↔Q_geom`-Abbildung → `[C]`, struktureller Echo, keine Identität.
- **Kompaktheitsfenster:** `1/3 < 3/8 < 4/9 < 1/2` ⇒ Oberfläche bei `R=8M/3 < 3M`: **über**
  der Photonensphären-Schwelle (lichtfangend, Echo-fähig), **unter** Buchdahl und Horizont →
  horizontloser Echo-Kandidat.
- **Echo-Template:** Tortoise-Round-Trip-Delay `Δt=2.288 M` → ~0.70 ms (62 M☉), ~1.60 ms
  (142 M☉); Amplitude `≤ (2/3)⁶`. Liefert `gw-ringdown-echo` die fehlende **Zeitskala** zum
  bereits fixierten Amplitudenverhältnis. **EHT-Schatten** `b_c=3√3 M` ist **Kerr-entartet** →
  Echos, nicht der Schatten, sind der Diskriminator. → `data_limited`.

### 7d.3 Kosmische Händigkeit — `cosmic-handedness/` (Frontier-Watchdog)
TFPT trägt nur `μ4`-Clock + `PSL(2,ℂ)≅SO⁺(3,1)`-Boundary-Orientierung ⇒ höchstens **winziger**
globaler Rest, also **approximate Parität** — *keine* ~20%-Asymmetrie. Shamir 2025 (JADES)
meldet `158:105` (~3.3σ Monopol), Galaxy-Zoo (Land+2008) ist isotrop. Eine rohe Zählasymmetrie
ist ein **Monopol**; eine MW-Rotations-Aberration ein **Dipol** — die Trennung braucht
himmelsaufgelöste Zählungen (nicht in den Aggregatdaten). → **Frontier, `data_limited`**;
nicht hochgestuft („Kathedrale auf einem Pixelhaufen"). **Flag:** ein paritäts-ungerader
globaler Spin-**Monopol**, der MW-Aberration + Selektion über Surveys hinweg übersteht.

---

## 8. Datenquellen (konsolidiert)

| Domäne | Datensatz | Bezug / Provenienz | speist |
|---|---|---|---|
| FRB | CHIME/FRB Catalogue 1 | VizieR | FRB.03/04 (Drift, Folding) |
| FRB | FRB 20121102A FAST 1652 Bursts | Li+2021, Nature 598 267 (VizieR) | FRB.02/02b/09, Energie-Kaskade |
| FRB | FRB 20121102A (Aggarwal 2021) | IOPscience | Cross-Check |
| FRB | lokalisierte FRB-`DM(z)` | ApJ adb84d Table 4; Sharma 2024 | FRB.05 (Ω_b) |
| FRB | CHIME-Polarisation (Pandhi 2024) | IOPscience | RM/PA-Stresstests |
| FRB | FAST FRB 20240114A Pol-Katalog (6134) | ScienceDB (user-supplied) | FRB.04/06/08 |
| FRB | Blinkverse-DB (Multi-Source) | blinkverse.top | FRB.02/02b/04/06/07/09 Replikation |
| FRB | rohe Wasserfälle (`.ar`/`.calibP`) | FRB 20201124A (1863), 20240114A (2729), 20121102A | FRB.01 Sub-Band-ToAs → `frb01_subband_toas.csv` |
| CMB | Doppelbrechung `β` | ACT DR6 (arXiv:2509.13654), Planck PR4 (arXiv:2205.13962) | CMB `beta_only`/Linie + Shared-Seed |
| CMB | `Ω_b` | Planck 2018 VI; BBN D/H (PDG/Cooke+2018) | CMB `omega_b_only`/Linie + Shared-Seed |
| CMB | `sin²θ13`, Cabibbo `\|V_us\|` | NuFIT 6.0; PDG 2024 | Shared-Seed (θ13 + Cabibbo) |
| CMB | `n_s`, `r`, `A_s` | Planck 2018 VI; BICEP/Keck BK18; P-ACT-LB+DESI; CMB-S4 (Forecast) | Inflation/Scalaron |
| ν | PMNS `θ12/θ13/θ23` | NuFIT 6.0; JUNO (2025) | neutrino-mixing |
| CKM | `δ`/`γ` | LHCb γ-Kombination | neutrino-mixing (CKM δ) |
| GW | LVK GWTC-5.0 (390 kanonisch) | GWOSC Event-API | GW Echo-Census |
| GW | GW170817 + GRB170817A | Abbott+ 2017 ApJL 848 L13 | `v_GW=c` Null-Test |
| GW | Ringdown `M_f`,`a_f`,`f_220` | GW150914 (Isi+2019), GW250114 (GWTC-5.0) | QNM `ln3` (datenlimitiert) |
| Kosmo | `Ω_Λ`, `H₀` | Planck 2018 VI | Λ/H₀-Engine |
| Lab | Myon g−2 `a_exp` + SM-HVP | Fermilab PRL 135 101802 (2025); TI WP2020/WP2025 (arXiv:2505.21476) | g−2-Baseline-Matrix |
| Lab | `BR(K⁺→π⁺νν)`, `KL`-Limit | NA62 (arXiv:2604.12649; JHEP 02 2025 191); KOTO 2024 | Kaon-Bridge |
| Lab | γ (CKM), Jarlskog `J`, `\|Vcb\|`/`\|Vub\|` | LHCb γ 2024; PDG 2024 | rare-kaon-bridge (R_K, δ_CKM, J) |
| Lab | Axion-Haloskop-Coverage | ADMX/HAYSTAC/CAPP | Axion-Marker |
| EW | SM `λ(M_Pl)`, `β_λ(M_Pl)`-Fit | Buttazzo+2013 (arXiv:1307.3536, NNLO) | higgs-criticality (Doppel-kritische Fläche) |
| EHT | M87 2017 Polarimetrie (uvfits) | **EHT 2023-D01-01** (CyVerse 10.25739/q46m-m857), real | EHT Achromatizität (real) + Injection-Suite; Residual-Nulls offen |
| ν | Σm_ν, m_ββ | DESI+CMB, KATRIN, LEGEND/nEXO | Neutrino absolutes Spektrum (scorecard) |
| ν | δ_PMNS (leptonische CP) | NuFIT 6.0 (arXiv:2410.05380); DUNE/HyperK | neutrino-mixing (`δ_PMNS=240°`) |
| cosmo | dunkle Energie `w0-wa` | DESI DR2 (arXiv:2503.14738) + CMB + Pantheon+/Union3/DES-SN5YR | `w=−1` overlap-aware Watchdog |
| lab | EDM-Limits (n, e) | PSI nEDM; JILA/ACME | EDM-Null (`θ_eff=0`, scorecard) |
| cosmo | SMBH-Kopplungsindex `k` | Farrah+2023 (ApJL 944 L31); Planck `Ω_Λ` | ccbh-dark-energy (`k=3 → w=−1`) |
| GW/grav | Max-Kompaktheit `C=3/8`; LVK-Ringdown | Jampolski-Rezzolla 2026 (arXiv:2509.15302); GWTC | gravastar-compactness (ECO-Echo-Template) |
| cosmo | Galaxien-Spin-Händigkeit | Shamir 2025 (MNRAS 538 76, JADES); Land+2008 (Galaxy Zoo) | cosmic-handedness (Paritäts-Watchdog) |
| Pulsar | Glitch-Katalog `Δν/ν`,`Δν̇/ν̇`,Epoche (726 Glitches) | Jodrell Bank Glitch Catalogue (Basu+2022, MNRAS 510 4049) | pulsar-glitch-recovery (PG.01/02/03) |
| Pulsar | Recovery `Q`/`τ_d` (60 Komponenten, 46 Glitches) | Yu+2013 (MNRAS 429 688; arXiv:1211.2035 `expTab.tex`) | pulsar-glitch-recovery (PG.04) |
| Pulsar | Crab `ν(t)`/`ν̇(t)` (479 Monatspunkte, 1988–2026) | Jodrell Bank Crab Monthly Ephemeris (Lyne+1993, MNRAS 265 1003; `crab2.txt`) | pulsar-glitch-recovery (PG.05 dyn. Kamm) |
| Transient | ENT/AGN-Scheiben-TDE ZTF-DR-Lichtkurve (J2245+3743, ~1440 g/r/i-Epochen MJD 58242–60967) | IRSA ZTF light-curve service (anonym); Objekt: Graham+2025, Nat. Astron., arXiv:2511.02178 | recovery-comb-domains (A5 dyn. Kamm ω=2.58 + TFPT-λ-Batterie) |
| EW | `α_em(M_Z)`, `sin²θ_W(M_Z)`, `α_s(M_Z)` | PDG 2024 | gauge-unification (`sin²θ_W=3/8` vs RGE) |

Große/öffentlich-neu-ladbare Rohdaten sind **gitignored**; nur kleine
abgeleitete/Provenienz-Dateien (z. B. `frb01_subband_toas.csv`, `gwtc_events.csv`,
`measurements.json`) werden versioniert, damit die Tests ohne GB-Downloads reproduzierbar bleiben.

---

## 9. Methodik / Red-Team-Prinzipien

- **Preregistrierung & eingefrorener Kernel:** Hypothesen + Kernelwerte + Nullmodelle + Erfolgskriterien vor dem Lauf festgelegt (FRB: `hypotheses/*.yaml`, exakte Brüche per Guard-Test); Spine-Axion-Winkel vor dem Lauf eingefroren.
- **Surrogat-kalibrierte Nullmodelle:** Within-Session-/Block-/Zeit-/Frequenz-Shuffle, AR(1)-Energy/Drift, Censoring, Dirichlet — pro Test mehrere, konservativ (max-p).
- **Placebo-Kontrollen & Look-Elsewhere:** FRB.06 (arbiträre Kontrollbrüche), FRB.02b (freier Quotient gegen fixen TFPT-Quotienten, LEE-korrigiert, Injection-Recovery).
- **Multi-Source-Replikation:** „Support" nur bei ≥2 unabhängigen Quellen (BH-q < 0.01, unterscheidend, semantisch valide).
- **Observable-Semantik:** Energie- vs Amplitudenkanal korrekt zugeordnet (Energie → `64/729`, Amplitude → `8/27`); Fehlpaarung = geflaggte Audit-Anomalie.
- **Kill-Bedingungen** pro Zeile explizit (z. B. `BR(K⁺)` außerhalb [7,12]×10⁻¹¹; gemeinsame über-Präzisions-Dispersion über Quellen; β bricht die Linie bei ≥3σ).

### 9.1 Scorecard-Schema (`evidence_scorecard.json`, Generator `build_evidence_scorecard.py`)

Eine getypte Zeile pro `(domain, observable)`. Felder:
`domain · observable · tfpt_value · data_value · pull_sigma · claim_type · bridge_type ·
stage · source · kill_condition · status` **plus die Metadaten**
`independence_group · discriminative_power · decision_horizon · evidence_class · hint_flag`.

**Feste Enums (Generator bricht bei Verstoß):**
- `stage ∈ {prediction_of_record, downstream_bridge, search_target, catalog_feasibility,
  strain_level_test, parked_analog, not_applicable}` (`not_applicable` = interne
  Konsistenz-Checks/Identitäten ohne empirische Stufe, z. B. Recovery-Channel, Page-Kurve,
  `S_dS·ρ_Λ=32π⁴`)
- `status ∈ {consistent, hint, tension, null, kill_channel, data_limited, parked}`
- `evidence_class ∈ {external_data, internal_consistency, downstream_bridge, search_target,
  parked}`

**Warum die Metadaten (Anti-Schein-Stärke):**
- `independence_group` — **korrelierte Beine zählen nicht als unabhängig.** `phi0_seed`
  (β, Ω_b, θ12, θ13, Cabibbo, Seed-Linie, FRB.05 — alle `φ₀`-abgeleitet), `alpha_em`
  (Λ-Hierarchie, S_dS — aus `α⁻¹`), `N_star_reheating` (Inflation),
  `c3_topform_horizon` (EHT, aus `16c₃⁴`), `independent` (Rest). Aktuell **8 Zeilen
  `phi0_seed`** — ein Cluster, keine acht unabhängigen Treffer (Zahl auto-generiert, siehe §1).
- `alternative_group` — **eine Frage, mehrere Lesarten** (nie gleichzeitig „consistent" und
  „tension" aus demselben Thema zählen): `Nstar_branch` (A_s fixed vs profiliert),
  `HVP_baseline` (g−2 WP2020 vs WP2025-Lattice), `axion_branch` (Haloskop/Hilltop/Spine).
- `evidence_class` — `internal_consistency` (recovery-channel/Page-curve/S_dS-Identität:
  interne Checks, *keine* externe Messung) wird vom `external_data`-Korb getrennt.
- `watch_flag`/`watch_level` — der schärfste **nicht-rote** Kanal: dunkle Energie `w`
  (`watch_flag=true`, `high`; 4.4σ stärkste Einzelkombo, aber systematik-limitiert → noch
  `data_limited`, nicht `tension`).
- `discriminative_power ∈ {internal, weak, medium}` — `weak`, wo die Standardphysik denselben
  Wert vorhersagt (Ω_b, Λ-Hierarchie, v_GW=c).
- `decision_horizon ∈ {near_term, mid_term, long_term}`.
- `hint_flag` — true z. B. für FRB.03 (zu kalt für `status=hint`, daher `data_limited`).
- Composite-/Branch-Felder: `chi2_dof`, `max_leg_pull_sigma`, `dominant_leg` (Shared-Seed);
  `lambda_pull_sigma`/`beta_lambda_pull_sigma`/`status_note` (Higgs-Kritikalität);
  `log_order_deviation` (Λ-Hierarchie, statt eines pull_sigma).

**README-Statistik wird ausschließlich aus dem JSON generiert** (Marker-Block
`<!-- SCORECARD_STATS -->`, vom Generator geschrieben) — keine handgepflegten Zähler.
Aktueller Stand siehe §1.

---

## 10. Reproduzieren

```bash
# gemeinsames venv (mpmath/numpy/scipy/sympy/astropy)
. experiments/tfpt-discovery/.venv/bin/activate

# FRB (voller Lauf -> results/ + Plots)
cd experiments/frb-tfpt-signatures && PYTHONPATH=src python -m frb_tfpt.cli analyze --seed 0

# CMB Seed-Linie
cd experiments/cmb-birefringence-seed && PYTHONPATH=src python -m tfpt_cmb.cli analyze

# Labor-Residuen
cd experiments/lab-residuals && PYTHONPATH=src python -m tfpt_lab.cli analyze

# GW Echo-Census (Katalog ggf. neu laden) + Stage-1 Matched-Filter (Injection-Recovery)
cd experiments/gw-ringdown-echo && python scripts/fetch_catalog.py && PYTHONPATH=src python -m tfpt_gw.cli analyze
cd experiments/gw-ringdown-echo && PYTHONPATH=src python -m tfpt_gw.cli search   # Stage-1 MF, 3/3 Injektionen
cd experiments/gw-ringdown-echo && python scripts/fetch_strain.py GW150914 GW190521 && PYTHONPATH=src python -m tfpt_gw.cli realdata  # Stage-1 statisch (2/3)^6 auf echtem Strain
cd experiments/gw-ringdown-echo && PYTHONPATH=src python -m tfpt_gw.cli dynamic   # Stage-2 dynamischer Walled-Clock-MF (echter Strain)

# echte EHT-Polarimetrie laden + Achromatizität + Injection-Suite + Pipeline-Readiness
cd experiments/eht-achromatic-residual && python scripts/fetch_eht_data.py && PYTHONPATH=src python -m tfpt_eht.cli realdata
cd experiments/eht-achromatic-residual && PYTHONPATH=src python -m tfpt_eht.cli inject
cd experiments/eht-achromatic-residual && PYTHONPATH=src python -m tfpt_eht.cli pipeline

# Seed-Stresstest (theta13-Treiber) — v1 + v2 (GLS/PPC) + v3 (reactor-only DB/RENO/DC)
cd experiments/seed-consistency        && PYTHONPATH=src python -m tfpt_seed.cli analyze
cd experiments/seed-consistency        && PYTHONPATH=src python -m tfpt_seed.cli v2
cd experiments/seed-consistency        && PYTHONPATH=src python -m tfpt_seed.cli v3

# erweiterte Domänen (Compiler-Ebene + Recovery-Channel)
cd experiments/recovery-channel        && PYTHONPATH=src python -m tfpt_recovery.cli analyze
cd experiments/recovery-channel        && PYTHONPATH=src python -m tfpt_recovery.cli petz      # Petz-Map + rank-one Baby-Universe
cd experiments/cmb-inflation-scalaron  && PYTHONPATH=src python -m tfpt_inflation.cli analyze   # + Branch-Resolver/Bayes
cd experiments/neutrino-mixing         && PYTHONPATH=src python -m tfpt_neutrino.cli analyze
cd experiments/gw-speed-multimessenger && PYTHONPATH=src python -m tfpt_gwspeed.cli analyze
cd experiments/gw-ringdown-spectroscopy && PYTHONPATH=src python -m tfpt_ringdown.cli analyze
cd experiments/lambda-h0-engine        && PYTHONPATH=src python -m tfpt_lambda.cli analyze

# Entscheidungs-Tests (P1/P2)
cd experiments/dark-energy-w-watchdog  && PYTHONPATH=src python -m tfpt_w.cli analyze
cd experiments/rare-kaon-bridge        && PYTHONPATH=src python -m tfpt_kaon.cli analyze
cd experiments/higgs-criticality       && PYTHONPATH=src python -m tfpt_higgs.cli analyze   # + Stabilitäts-Posterior
cd experiments/lab-residuals           && PYTHONPATH=src python -m tfpt_lab.cli haloscope    # 23.8 µeV Overlay
cd experiments/ftransfer/axion_relic   && python spine_finiteT_solve.py      # ~25 s
cd experiments/ftransfer/axion_relic   && python spine_independent_check.py  # unabhängiger Cross-Check
cd experiments/ftransfer/leptogenesis_boltzmann && python fboltzmann_solve.py  # voller ODE: eta_B=6.5e-10 @ frozen M1
cd experiments/theory-contracts        && python qgeo_dtn_mark_locality.py

# problem_b black-hole-cosmology Signaturen (neu)
cd experiments/ccbh-dark-energy        && PYTHONPATH=src python -m tfpt_ccbh.cli analyze
cd experiments/gravastar-compactness   && PYTHONPATH=src python -m tfpt_gravastar.cli analyze
cd experiments/cosmic-handedness       && PYTHONPATH=src python -m tfpt_handedness.cli analyze

# problem_1 Pulsar-Glitch-Recovery (dritte Cross-Domain-Säule) + Recovery PG.04
cd experiments/pulsar-glitch-recovery  && python scripts/fetch_glitches.py   # JBO-Größen (CSV committed)
cd experiments/pulsar-glitch-recovery  && python scripts/fetch_recovery.py   # Yu+2013 Q/tau_d (CSV committed)
cd experiments/pulsar-glitch-recovery  && python scripts/fetch_crab_ephemeris.py  # Crab nu(t) (CSV committed, PG.05)
cd experiments/pulsar-glitch-recovery  && PYTHONPATH=src python -m tfpt_pulsar.cli validate   # Injection-Recovery
cd experiments/pulsar-glitch-recovery  && PYTHONPATH=src python -m tfpt_pulsar.cli analyze     # PG.01/02/03/04 (statisch)
cd experiments/pulsar-glitch-recovery  && PYTHONPATH=src python -m tfpt_pulsar.cli dynamic      # PG.05 dynamischer Kamm auf echtem Crab nu(t)
cd experiments/pulsar-glitch-recovery  && python scripts/fetch_nicer_j0537.py                  # PG.06: 1165 NICER-J0537-Obs bestätigen/listen
cd experiments/pulsar-glitch-recovery  && PYTHONPATH=src python -m tfpt_pulsar.cli nicer        # PG.06 Scaffold (PINT-Upstream gated, Downstream injection-validiert)
cd experiments/pulsar-glitch-recovery  && python scripts/fetch_nicer_vela.py                   # PG.06b: 665 NICER-Vela-Obs listen
cd experiments/pulsar-glitch-recovery  && PYTHONPATH=src python -m tfpt_pulsar.cli vela --download  # PG.06b: echte Vela-Obs laden + PINT-Fold (Vela-Pulsation nachgewiesen)

# Cross-Domain-Suche der dynamischen Kamm-Signatur (omega=2.58) ueber 8 Kanaele
cd experiments/recovery-comb-domains   && PYTHONPATH=src python -m tfpt_combdomains.cli fetch-ent  # A5: echte ZTF-Lichtkurve J2245+3743 (IRSA)
cd experiments/recovery-comb-domains   && PYTHONPATH=src python -m tfpt_combdomains.cli analyze  # A1 Magnetar/A2 BH-Tail/A3+A3b FRB-Tail/A4 GRB-Plateau/A5 ENT-TDE/B4 BEC/B5 Qubit

# problem_1 Quantum-Testbed (Entanglement + Quench-DSI + OTOC + walled clock + anyon-MTC; intern)
cd experiments/quantum-testbed         && PYTHONPATH=src python -m tfpt_qtest.cli analyze       # QT.01-05

# v244/v245 sin^2 theta_W = 3/8 Gauge-Unifikation vs PDG (1/2-loop RGE)
cd experiments/gauge-unification       && PYTHONPATH=src python -m tfpt_gut.cli analyze

# zentrale Scorecard regenerieren
python experiments/build_evidence_scorecard.py
```

---

## 11. Konventionen

* Jedes Experiment ist self-contained: eigene Abhängigkeiten, eigener Build, eigene
  CLI als Audit-Surface (`<pkg>.cli analyze`).
* Keine SI-Werte als versteckte Eingabe — alles fließt aus den TFPT-Axiomen
  (`c₃ = 1/(8π)`, `φ₀ = 1/(6π) + 3/(256π⁴)`, Carrier-Polynom `6Y²−Y−1=0`).
* **Firewall / Typing:** Frontier-Observablen sind `F_transfer`-Bridges, **nie**
  primitive Compiler-Outputs; Status pro SM-Baseline/Branch gesplittet; nichts wird
  still nach `[E]` hochgestuft.
* Standalone unter `experiments/` — **nicht** im Verification-Suite/Ledger/Website,
  keine load-bearing Claims.

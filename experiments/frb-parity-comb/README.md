# frb-parity-comb — die v486-Paritäts-Selektionsregel auf signierten FRB-Polarisationskaskaden

**Suchziel (PC.01–PC.03, preregistriert in `hypotheses/parity_comb_v1.yaml` VOR dem Datenpass,
2026-07-15).** v486 (HYP.REWRITE.02) fixiert erstmals die Eigenvektoren des Seam-Transfers:
λ₂ = (2/3)⁶ lebt auf dem ℤ₂-**geraden** Paar-Eigenvektor (1,1), λ₃ = (1/3)⁶ auf dem
ℤ₂-**ungeraden** (1,−1). Konsequenzen (next.txt 2026-07-15, S-a/S-b):

- der ω₁ = 2.5827-Kamm koppelt nur an sheet-symmetrische Observablen (Intensität/Energie);
- der ω₂ = 0.9532-Kamm **nur** an sheet-antisymmetrische (Vorzeichen der Zirkularpolarisation);
- ein ω₁-Kamm im **ungeraden** Kanal ist **verboten** (der Kill-Test dieser Runde);
- Kamm-2-Amplitude verblasst relativ ×2⁶ = 64 pro Periode (S-b-Budget → ω₂ realistisch nur
  früh nach Session-Onset detektierbar).

**Firewall.** Boundary-Recovery-Suchziel, keine direkte Hawking-/Neue-Gravitation-Aussage.
Die Kopplung „Vorzeichen der Zirkularpolarisation = ℤ₂-Sheet-Parität" ist eine
**Deck-Lesart (unforced)**, wie KC.02 — ein Null tötet nur die Kopplungslesart, nie den Kern;
ein Hit wäre escalate-only. Nichts hier ist load-bearing.

**Statistik.** Ungerader Kanal: signierte Rayleigh-Power Z_s(w) = |Σ sᵢ·e^{iw·ln τᵢ}|²/n mit
**Within-Session-Vorzeichen-Permutations-Null** (behält alle Burstzeiten und damit die gesamte
Ratenhüllkurve; zerstört nur die Vorzeichen-Zeit-Kohärenz — hüllkurvenimmun, da die glatte Rate
paritätsgerade ist und aus der signierten Statistik herausfällt). Gerader Kanal: ungewichtete
Rayleigh-Power mit den ratenerhaltenden Log-Dichte-Surrogaten (Konstruktion wörtlich aus
`repeater-cascade/comb.py` übernommen). Gates pro getestetem Ton: Reichweite > 2.8 Perioden
(PC.02 sekundär: > 1.2, als explorativ gelabelt), n ≥ 30 (relaxed: ≥ 60), τ ≥ 0.5 s.

**Daten.** Primär: FAST FRB 20240114A Pol-Katalog v5 (committed in `frb-tfpt-signatures/data/`;
6134 Bursts, 3474 signifikante Händigkeiten in 80 Sessions). Sekundär (gerader Kanal):
FRB 20220912A (Zhang+2023), FRB 20121102A (Li+2021). Extern ausstehend: Xu+2022-Polarisations-
Supplement zu 20201124A, CHIME-Baseband-Pol, IXPE-Magnetar-Recoveries.

## Verdikt (v1, seed 0 — `results/results.json`)

| Test | Ergebnis | Verdikt |
|---|---|---|
| **PC.01** ω₁ verboten im ungeraden Kanal | 2 gate-passierende Sessions (n = 213, 61; Reichweite 3.06/3.35 Perioden); Fisher **p = 0.83**, Off-Ton-Ränge 0.55/0.99 — keinerlei ω₁-Signed-Power | **NULL — Selektionsregel hält** bei detektierbarer Amplitude (Injection: 88 % Detektion bei ε = 0.5, 40 % bei ε = 0.3; darunter unpowered) |
| **PC.02** ω₂ im ungeraden Kanal | nur 1 relaxed-Gate-Session (n = 61, 1.24 Perioden), p = 0.29; primäres Gate (18.5 e-folds in ln τ) nirgends erreichbar | **data_limited** — konsistent mit dem S-b-Budget (×64-Fading/Periode); Injection: nur 22 % Detektion selbst bei ε = 0.5 |
| **PC.03** ω₂ darf keine gerade Linie sein | kein Session-Gate im geraden Kanal bei ω₂ (alle drei Kataloge) | **data_limited** (konsistent mit den eingefrorenen New-Tone-Scan-Nulls) |

**Ehrliche Zusammenfassung:** Die verbotene Richtung (PC.01) ist getestet und hält — bei der
Amplitude, die der Datensatz sehen kann (ε ≳ 0.3–0.5). Die positive Richtung (ω₂-Kamm) bleibt
datenlimitiert, exakt wie das v486-S-b-Budget es vorhersagt: Der ungerade Kamm braucht entweder
~64× Sensitivität oder Kaskaden mit ≫18 e-folds Onset-Reichweite (IXPE-Outburst-Recoveries sind
der beste Kandidat dafür). Kalibrierungs-Bug-Protokoll: die erste Injection-Implementierung
(Flip der beobachteten Vorzeichen) verwarf die Phasenkohärenz — behoben auf das physikalische
Modell (Händigkeit folgt der Uhr); im Code dokumentiert.

## IXPE-Bein (v1.1-Addendum, 2026-07-15 — `results/results_ixpe.json`)

**Datensatz:** IXPE ObsID 03250499 — Magnetar **1E 1841-045**, ToO ~5–7 Wochen nach dem
Outburst vom 2024-08-20/21 (MJD 60581–60593, 293 ks, 225.226 Photonen 2–8 keV über 12.2 Tage;
per `scripts/fetch_ixpe.py` von HEASARC, ~23 MB, gitignored).

**Semantik-Korrektur (im Addendum VOR dem Datenpass festgehalten):** IXPE misst nur
**lineare** Polarisation — der ℤ₂-ungerade Händigkeitskanal existiert im Röntgen nicht
(PA ist mod π deck-invariant, KC.02-Semantik). Das IXPE-Bein testet daher den **geraden**
Sektor: ω₂ = 0.9532 als **verbotene** gerade Linie (IX.01, die PC.03-Kill-Richtung mit
potenziell echter Reichweite), ω₁ = 2.5827 als erlaubte Linie (IX.02, escalate-only).

| Test | Ergebnis | Verdikt |
|---|---|---|
| Hüllkurven-Anker (Outburst-Epoche) | t−t₀ ≈ 39–51 d → ln-Reichweite 0.27 = **0.11 ω₁-Perioden** | `data_limited` by construction (aufgezeichnet, nicht getestet) |
| Burst-Suche (prereg: 0.1-s-Bins, lokale Poisson-Tail p < 10⁻⁶) | **2 Bursts** in 12.2 Tagen (10 bzw. 6 counts/0.1 s über lokalem Mittel 0.08; p = 4×10⁻¹⁸ / 6×10⁻¹⁰) | Quelle nur schwach burst-aktiv im ToO-Fenster |
| IX.01 ω₂-Verbotslinie | 1 Kaskade (333 Photonen, ~71 s bis GTI-Lücke) = 1.0 ω₂-Perioden < relaxed-Gate 1.2 | **`data_limited`** (kein Gate) |
| IX.02 ω₁-Linie | 1 relaxed-Session, Surrogat-p = 0.53 | null-at-current-power |
| IX.03 Injection (Thinning auf echten Photonenzeiten) | ω₁: 2 % Detektion selbst bei ε = 0.3 (eine 333-Photonen-Session) | Bein ist ehrlich **unterpowert** |

**Typisierte Erkenntnis:** Selbst der beste verfügbare Post-Outburst-Magnetar-ToO (5–7 Wochen
nach Onset) liefert praktisch keine Kamm-Reichweite — weder über den Hüllkurven-Anker (0.11
Perioden) noch über interne Bursts (2 Stück, 1 nutzbare Kaskade). Das Bein braucht ToOs
**innerhalb von Tagen** nach Onset mit dichter Abdeckung oder **Burst-Sturm**-Beobachtungen;
für die reine Zeitreihen-Seite (gerader Kanal) wäre **NICER** (große effektive Fläche,
SGR-1935-Sturmdaten) das bessere Instrument als IXPE — als nächstes Bein benannt.

## NICER-Bein (v1.2-Addendum, 2026-07-15 — `results/results_nicer.json`)

**Datensatz:** NICER ObsID 3020560101 — der **Burst-Sturm vom 2020-04-28** von
**SGR 1935+2154** (Younes+2020, ApJL 904 L21; per `scripts/fetch_nicer.py` von HEASARC,
cl 7 MB + ufa 65 MB, gitignored). 306.090 Photonen 1–10 keV, 3.1 ks Exposure. Die
preregistrierte cl-vs-ufa-Fallback-Regel (GTI-Coverage im Sturmfenster < 50 %) wurde
**nicht** ausgelöst (1094 s vs 1299 s).

**Motivation (Lehre des IXPE-Beins):** der ω₂-Verbotstest braucht Burst-**Stürme**, nicht
Post-Outburst-ToOs — und der gerade Kanal braucht nur Ankunftszeiten. Der Sturm liefert
genau den erhofften dichten Anker: **375 Bursts, ein Sturm-Cluster mit 372 Bursts über 1095 s**.

| Test | Ergebnis | Verdikt |
|---|---|---|
| Familie A (Sturm-Kaskade: Burst-Peak-Zeiten, u = ln(t−t_storm)) | 372 Bursts, ln-Reichweite 4.6 e-folds = **1.89 ω₁- / 0.70 ω₂-Perioden** | ω₂ unter Gate |
| NI.01 ω₂-Verbotslinie (Kill-Richtung) | keine Session (A oder B) erreicht das ω₂-Gate | **`data_limited`** — der Verbotstest bleibt mangels Reichweite **offen, nicht verletzt** |
| NI.02 ω₁-Linie | 110 gated Sessions (1× A:relaxed, 107× B:relaxed, 2× B:primary), Fisher p = 0.165 | null-at-current-power |
| NI.03 Injection + ε=0-Baseline | Familie A: **98 % False-Positives bei ε = 0** — das Smooth-Log-Density-Surrogat ist auf geclusterten Burst-Zeit-Sessions stark antikonservativ (das einzelne A-p=0.005 damit als Surrogat-Misfit typisiert, nicht Signal); Familie B sauber: 0 % FP, powered ab ε ≈ 0.3 (92 %; 50 % bei 0.2) | Kalibrierung dokumentiert |

**Typisierte Erkenntnis:** Selbst der beste archivierte Burst-Sturm liefert nur ~1.9
ω₁-Perioden Familie-A-Reichweite; für das ω₂-Gate (7.9 e-folds zwischen Anker und
Session-Ende) bräuchte es **Multi-Tag-Sturm-Monitoring** (Onset + Stunden-bis-Tage-Kadenz).
Die ω₂-Verbots-Richtung ist mit existierenden Archiven **nicht entscheidbar** — eine
ehrliche, harte Grenze, jetzt mit Zahlen belegt.

**Ausstehende Datensätze (dokumentiert, v1-Scope geschlossen):** Das öffentliche
Xu+2022-Maschinentable zu 20201124A (Mirror: astroflash-frb/frb20201124A-kirsten-2023) trägt
DoC **unsigniert** (1103 Messwerte, alle ≥ 0) — der zweite ungerade Kanal bräuchte die
Per-Burst-Stokes-Profile von PSRPKU (volle polarimetrische Reduktion, pending). CHIME-Baseband-
Pol (unabhängige Systematik) bleibt als nächstes Bein benannt; Multi-Tag-Sturm-Monitoring
(ω₂-Reichweite) ist ein Beobachtungs-Desiderat, kein Archiv-Projekt.

Reproduzieren: `cd experiments/frb-parity-comb && PYTHONPATH=src python -m tfpt_pc.cli analyze --seed 0`
(IXPE-Bein: `… analyze-ixpe`; NICER-Bein: `… analyze-nicer`)
Kernel-Guard: `python3 tests/test_frozen_kernel.py`

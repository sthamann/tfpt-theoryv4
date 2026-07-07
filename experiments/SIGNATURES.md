# TFPT-Signaturkatalog — Codes, Herleitung, Testorte, Ergebnisse

> Stand: **2026-07-07**. Interner Arbeitskatalog des `experiments/`-Programms.
> **Firewall:** Alles hier sind Suchziele/Konsistenzchecks — nie load-bearing, nie `[E]`.
> Kein Treffer wäre ohne unabhängige Replikation TFPT-Bestätigung; jeder Null ist typisiert
> (`null` / `data_limited` / `consistent`). Die volle typisierte Prediction-Fläche (106 Zeilen)
> lebt in `evidence_scorecard.json`; dieser Katalog deckt die **Signatur-Familien** des
> Kernel-/Geometrie-Programms und ihre Testorte ab.

Leseanleitung: Signaturen tragen **S-Codes** (S1–S12, Unterlesarten `.a/.b/…`), Experimente
tragen **E-Codes** (E01–E20). §3 ist die Matrix „wo wurde was getestet, mit welchem Ergebnis".

---

## 0. Herleitungsbasis (woher alles kommt)

Zwei Axiome: Seam-Konstante `c₃ = 1/(8π)` (P1) und Carrier-Rang `g_car = 5` (P2).
Daraus der Seam-Transfer-Operator `T` mit Spektrum `{1, λ_T, λ_T'}` auf den drei
Flavor-Moden (Perron-Mode geschützt; ein Transferschritt = 6 Carrier-Substeps,
`6 = |Z₂|·N_fam`, Überleben 2/3 bzw. 1/3 pro Block). Exakte Folgerungen (verification
v124/v126/v147, QT.02): resummierte Recovery-Uhr `rate(n) = −6·ln(1−n/3)` mit Pol (Wall)
bei `n = N_fam = 3`. Topologie: einseitiges Z₂-Doppelcover (der Faktor ½ in
`c₃ = 1/(2·4π)`), μ₄-Deck, Retarded Seed `φ₀ = (4/3)c₃ + 48c₃⁴ = 0.053172`
(= Tree `1/(6π)` + topologischer Tail `3/(256π⁴)`).

**Notation (fixiert 2026-07-06 — Vorzeichenfalle):** strikt getrennt werden

| Symbol | Wert | Rolle |
|---|---|---|
| `λ_T = (2/3)⁶ = 64/729` | 0.0878 | **Transfer-Kontraktion** (Energie-Eigenwert) |
| `Λ_DSI = (3/2)⁶ = 729/64` | 11.39 | **Log-Skalenfaktor** (Zeit-Streckung pro Sprosse) |
| `ω = 2π/ln Λ_DSI` | 2.583 | Comb-Frequenz |
| `ε = exp(−π²/ln Λ_DSI)` | 0.0173 | Comb-Amplitude (QT.02) |

`exp(−π²/ln λ_T)` wäre wegen `ln λ_T < 0` riesig — der Code (`comb.py`: `LAMBDA = 1.5**6`)
war immer korrekt; die Katalog-Prosa ist hiermit eindeutig.

## 0b. Kategoriegrenzen (Befund 2026-07-06 — die wichtigste Korrektur)

Der Kern von TFPT ist ein **Operator und eine Zustandsinvarianz**, kein sichtbares Muster
in beliebigen Emissionsdaten. Drei harte Grenzen, ab jetzt Typisierungspflicht:

1. **Transduktion (→ S15).** Jede Messgröße ist `O = B·T·A` — Anregung `A` in den
   Seam-Kanal, Übersetzung `B` in die Observable. Projiziert `B` den Eigenmodus weg,
   sieht man **exakt nichts**. Ein Null in S1–S7 ist daher ein Null auf
   `B·T·A` (Bridge), nicht auf `T` (Core). **Observable Eligibility Gate:** vor jedem
   Datentest explizit — (i) welche interne Größe trägt den Modus, (ii) welche Kopplung
   bringt ihn in die Messgröße, (iii) warum ist die Projektion ≠ 0. Fehlt (ii)/(iii):
   Typ „exploratory surface leakage", nicht „TFPT-Signatur".
2. **Clock-Map (→ S14).** Ein endlicher Operator mit reellen Eigenwerten erzeugt Moden —
   eine Log-Comb in *Beobachterzeit* braucht zusätzlich `n = ln(t/t₀)/ln Λ_DSI`.
   Horizon/modular ist das motivierbar (KMS/thermisch); in FRB-Sessions, Afterglows,
   Krustenkühlung, Beben ist es **nicht automatisch wahr**. S2 wird deshalb gesplittet
   (S2a Spektrum = Kern-nah; S2b Log-Zeit-Comb = Bridge).
3. **μ₄ ist ein Galois-Gear, keine Uhr** (origin_theory, Z. 175–183: `h(E₈) = 30` ist
   quadratfrei ⇒ `Z/30` hat **kein** Element der Ordnung 4; μ₄ ist die
   Automorphismengruppe des Carrier-Pentagons, `(Z/5)^× ≅ Z/4`, Frobenius
   `ζ₅ ↦ ζ₅²` — „carries no rate, because it is an automorphism, not a hand";
   Vierfach-Identität Deck = Divisor = Galois = Diskriminante = Simple Current).
   **Konsequenz:** Die natürliche μ₄-Signatur ist *„Operator mischt keine
   Charakterklassen"* (→ S8), nicht *„Observable rotiert um π/2"*. S4/S5-Zeittests
   bleiben legitime Blind-Spot-Sonden, sind aber Projektionen ohne Transduktions-Theorie.
4. **Prime 2 trägt keine eigene Dynamik** (research contracts, Z. 110–112: „prime-2
   supplies a parity/projection, never a nonzero contraction rate; no prime-2-only
   attractor"). Reine Z₂-Ketten (V-Alternation, Bounce-Flips, Blattwechsel) sind
   Diagnose, keine starken Suchachsen, solange der 3-/5-Kanal der Dynamik unbenannt ist.

---

## 1. Signatur-Register (S-Codes)

> **Reklassifizierung (2026-07-06):** S1–S7 werden ab jetzt als
> **Surface-Leakage-Sonden** geführt (Status-Sprache: *no visible leakage in tested
> astrophysical channels*) — sie testen Kern **plus** Emissions-Bridge. **S8 ist die
> Hauptachse** (die Operator-Form des Kerns). S9 ist der Naturdaten-Konsistenzanker.
> S13–S15 sind die neuen, aus dem Befund abgeleiteten Familien.

### S1 — Statischer Echo-/Stufen-Kernel [Surface-Leakage-Sonde]

| Code | Signatur | Wert |
|---|---|---|
| S1.a | Einzelschritt-Ratio | `2/3` |
| S1.b | Amplituden-Lesart (√λ, Kohärenzen) | `(2/3)³ = 8/27` |
| S1.c | Energie-Lesart (Populationen) | `(2/3)⁶ = 64/729` |
| S1.d | volles Spektrum | `{1, 64/729, 1/729}` |
| S1.e | HFQPO-Leiterzahn | `ν₃ = (3/2)·ν_u` |

- **Woher:** Eigenwerte von `T`; Energie vs. Amplitude = Populationen vs. Kohärenzen
  (maschinell verifiziert im QC-Kernel; die „FRB-Lektion": beide Lesarten immer testen).
- **Warum plausibel:** Wenn wiederholte Ereignisse (Echos, Sub-Bursts, Glitches) Sprossen
  derselben Recovery-Leiter sind, stehen aufeinanderfolgende Größen in diesen Verhältnissen.
- **Wo sichtbar:** Echo-/Sub-Burst-Züge (FRB, GW-Ringdown), Glitch-Größenfolgen,
  QPE-Rekurrenzzeiten, HFQPO-Frequenzen.
- **Status: überall NULL / Upper Bound** (Details §3/§4).

### S2 — Recovery-Spektrum und Log-Comb [gesplittet 2026-07-06]

| Code | Signatur | Typ |
|---|---|---|
| S2a | **Spektrale Gap-Signatur**: Eigenwerte/Kontraktion `{1, λ_T, λ_T'}` im Markov-/Koopman-Spektrum eines beobachteten Prozesses | Kern-nah |
| S2b | **Log-Zeit-Comb** `R(t) ∝ 1 + ε·cos(ω·ln t + φ)`, `ω = 2.583`, `ε ≈ 1.7 %` | **Bridge** (braucht Clock-Map, → S14) |

- **Woher:** S2a direkt aus `spec(T)`; S2b zusätzlich aus der Clock-Map
  `n = ln(t/t₀)/ln Λ_DSI` — die in Beobachterzeit **nicht automatisch** gilt.
- **Warum plausibel:** S2a ist die ehrlichste sichtbare Form des Kerns (FRB.04 war ein
  erster S2a-Versuch: Markov-Spektrum auf PA/RM → null). S2b nur in Systemen mit
  physikalisch begründeter Uhr (Horizon: modular/KMS ✓; Astro-Fades: unbegründet).
- **Wo sichtbar:** S2b: Erholungs-Kurven mit **≥ 2.8 Comb-Perioden in ln t** (hartes Gate;
  Stacking kauft Amplitude, nie Range). Legitim nur boundary/horizon; Surface-Kanäle
  firewalled.
- **Status: S2b NULL wo well-powered, sonst data_limited an der ε-Wand** (Meta-Obergrenze
  ε < 0.12 @95 %). **S2a ist jetzt zweimal als FRB-Proxy gesucht:** FRB.04
  (PA/RM-Markov) null und KC.06 (multivariater Pol-Lag-Operator) null. Beide bleiben
  Surface-Leakage, weil die Transduktion `B` nicht bewiesen ist. **FO.02 (2026-07-07)
  ist die erste FRB-Achse MIT benanntem B** (DM/RM-Linienintegrale = Rand-Funktionale,
  S15-Gate bestanden): der nächtliche Medium-Zustand von 20240114A braucht keine
  zweite Rate (AIC bevorzugt Einzelraten) → `data_limited`. **FO.02b (v1.2-Addendum,
  Intra-Session-Kadenz, 2 Quellen):** die starke Intra-Session-RM-Varianz (χ²_red
  77–337 gegen Konstant-RM) trägt **kein zeitliches Gedächtnis** — 33/35 (v5) und
  12/12 (20201124A/Xu+2022) Sessions fallen durchs injektionsvalidierte Memory-Gate
  (OU bei τ=2–30 min wird 31–34/35 bzw. 8–10/12 erkannt; White-Noise-FP 3/35, 0/12)
  → die burst-gesampelte Varianz ist per-Burst/magnetosphärisch, KEIN relaxierender
  Medium-Zustand; der Ratio-Test hat auf Burst-Kadenz nichts zu greifen. Die
  Medium-Mess-Lesart überlebt nur im ungetesteten Stunden-bis-Tage-Band oder via
  getracktem RM-Injektionsereignis (20190520B-Klasse; Tabelle login-walled).

### S3 — Walled Clock

| Code | Signatur | Wert |
|---|---|---|
| S3.a | Bend (Ratenverhältnis) | `ln3/ln(3/2) = 2.7095` |
| S3.b | Hard Wall | max. 2 Zerfallsmoden (`n = 3` Pol) |
| S3.c | Protected Floor | `w₀ > 0` (Perron) |

- **Woher:** v124-Uhr; det-clean, exakt.
- **Warum plausibel:** Eine einzelne Recovery ist eine Zwei-Moden-Kurve mit festem Bend.
- **Wo sichtbar:** τ-Leitern in Glitch-Fits, Ringdown-Envelopes, Rate-Kurven. **Achtung
  (maschinengeprüft):** In EINER monotonen Recovery ist der Bend degeneriert (ΔR² ~ 10⁻³)
  — diskriminierend ist nur die Kaskade (→ S2).
- **Status: Bend NULL überall; Wall konsistent (45/46 ≤ 2 Moden, 1 Ausnahme on record);
  Floor generisch-konsistent.**

### S4 — Z₂/Möbius-Doppelcover-Lesarten [Surface-Leakage-Sonde; Prime-2-Vorbehalt]

| Code | Signatur | Wert |
|---|---|---|
| S4.a | Halbperioden-Takt | λ = `(3/2)³`, ω = 5.17 |
| S4.b | antiperiodische 1. Harmonische | λ = `(3/2)⁴`, ω = 3.87 |
| S4.c | antiperiodische Fundamentale | λ = `(3/2)¹²`, ω = 1.29 |
| S4.d | GW-per-Bounce-Phasenflip | `Δφ = π` im Echo-Zug |
| S4.e | V-Händigkeits-Flip | Vorzeichen von V/I alterniert pro Kernel-Schritt |

- **Woher:** Blattparität pro Periode auf dem Doppelcover (der ½-Faktor in c₃). Eine
  antiperiodische Comb hat **exakt null** Fourier-Leistung bei der Kernel-ω — alle
  Kernel-Nulls waren dafür blind. Topologisches Schlüsselargument für S4.e: PA ist mod π
  (deck-invariant), |V| gerade — **nur das V-Vorzeichen sieht den Orientierungsflip**.
- **Warum plausibel:** Kein Theory-Contract erzwingt, welche Observable die Parität trägt —
  deshalb explorativ, escalate-only; aber die Lesarten schließen strukturelle Blind Spots.
- **Wo sichtbar:** dieselben Betten wie S2 (a/b/c), GW-Echo-Züge (d), Full-Stokes-Kataloge (e).
- **Status: NULL überall, wo testbar; S4.c in allen Daten range-blind (braucht 13.6 e-folds,
  Maximum im Bestand 13.1) → data_limited; zwei Placebo-typisierte Artefakte on record.**
- **Prime-2-Vorbehalt (0b.4):** reine Z₂-Lesarten tragen laut Contract keine autonome
  Rate — S4-Tests sind Diagnose-Sonden; eine starke Suchachse bräuchte den gekoppelten
  3-/5-Kanal.

### S5 — μ₄-Deck auf Polarisation/Geometrie [Surface-Leakage-Sonde; Galois-Vorbehalt 0b.3]

| Code | Signatur |
|---|---|
| S5.a | 4 statische PA-Klassen, 45° getrennt (m=4-Fundamentale) |
| S5.b | PA/RM-Markov-Spektrum `{1, 64/729, 1/729}` |
| S5.c | Pol-Fraktions-Quantisierung `L/I, |V|/I ∈ {2/3, 1/3, 8/27, 1/27}` |
| S5.d | Phase-Zeit-Helix `Φ = ω·ln(τ_j/τ_i) + q·2ΔPA = const`, q ∈ {1,2} |
| S5.e | μ₄-Phasen im GW-Echo-Zug `Δφ ∈ {0, π/2, π, 3π/2}` |

- **Woher:** μ₄-Deck (Uhr z→iz) auf der Randpolarisation; d koppelt Zeit- und Pol-Phase.
- **Warum plausibel:** Wenn der Deck geometrisch wirkt, prägt er Viertel-Drehungen auf
  Polarisationsobservablen; d ist spezifischer als statische Histogramme.
- **Wo sichtbar:** Full-Stokes-FRB-Kataloge, GW-Echo-Züge.
- **Status: alle NULL** (a: m=2 statt m=4; b/c: 0/3 Quellen; d: Drift-robuste Null entlarvt
  das naive Permutations-Signal als PA-Drift; e: NO_VARIANT_ECHO).

### S6 — Emission-Readout-Kopplung [downgegradet 2026-07-06]

`E·t = const` entlang der Kaskade: Zeit-Zahn `(3/2)^k` ⇒ Partner-Energie-Zahn `(2/3)^k`.

- **Woher:** Beide Ratios sind Eigenwert-Lesarten desselben `T` — aber **forciert nur
  unter der Emissions-Bridge-Annahme** `E_obs ∝ interne Population` und
  `t ∝ inverse interne Rate`. Diese Annahme ist nicht aus TFPT abgeleitet (FRB-Energie =
  Magnetosphäre + Beaming + Lensing + Schwelle + Selektion + Pipeline).
- **Wo sichtbar:** Kataloge mit Zeiten UND Energien pro Burst.
- **Status: well-powered NULL für die sichtbare Energie-Zeit-Kopplung in beiden Quellen**
  (exakte Energie-Shuffle-Null) — ein **Bridge-Null, kein Core-Null**: die naive lineare
  Emissionsleiter ist tot, der Kernel unberührt.

### S7 — Size-Space-DSI

Log-periodische Dekoration der **Größen-/Energieverteilung** bei frozen λ (PG.01-Analog).

- **Woher:** DSI wirkt auch auf Verteilungen, nicht nur Zeitkurven.
- **Wo sichtbar:** Glitch-Größen, Burst-Energien (10³–10⁴ Samples).
- **Status: NULL (Pulsar & FRB), nach populationskontrollierter Null (Bimodalität absorbiert).**

### S8 — QGEO-Operator-Symmetrie ⟵ **HAUPTACHSE**

> Nach 0b.3 ist das die *richtige* μ₄-Signaturklasse: nicht „Observable rotiert um π/2",
> sondern **„Operator mischt keine μ₄-Charakterklassen"** — Deck/Divisor/Galois/
> Diskriminante/Simple-Current sind Konjugations- und Charakterstruktur, keine Zeiger.
> S4/S5 sind Projektionen davon und brauchen erst eine Transduktions-Theorie (S15).

| Code | Signatur |
|---|---|
| S8.a | μ₄-Charakter-Blockdiagonalität der Randenergieform: `S_off = Σ_{r≠s}‖P_r Λ P_s‖²/‖Λ‖² → 0`; `[ρ, Λ_Σ] = 0` |
| S8.b | Clock-Recovery: Leckage-Nullstellen exakt auf dem μ₄-Orbit {π/2, π, 3π/2} |
| S8.c | D4-Reflexion `ΘρΘ = ρ⁻¹` (Reflexionsscore) |

- **Woher:** Operator-Form von QGEO.SYM.01 (Research Contracts; v192–v214): „das
  sub-principal Symbol der rohen DtN hat keine off-character Matrixelemente".
- **Warum plausibel:** Testet die behauptete **Struktur** statt einer Zahl; Z₃/generische
  Marks sind eingebaute Negativkontrollen; δ²-Bruchgesetz verifiziert (Exponent 1.998).
- **Wo sichtbar:** jedes System mit rekonstruierbarem Randoperator: numerische
  Steklov-Geometrie, **EIT** (misst den ND-Operator wörtlich), BEC/Wellenleiter/Kavität.
- **Status: Simulationskontrakt HOLDS (Instrument-Anforderung ~10⁻³ beziffert); auf realer
  EIT-Hardware Instrument+Diskriminator validiert (H1+H2); der entscheidende μ₄-Positiv-Test
  (H3: 4 Inklusionen bei j·π/2, C4 hält + C8 bricht) ist preregistriert, nicht gemessen.
  Astro-Proxy KC.05 auf FRB-PA-Klassen ist NULL (keine C4-spezifische Blockprotektion);
  das ist ein Surface-Leakage-Null, kein QGEO-Core-Test.**

### S9 — Gemeinsamer φ₀-Seed (Architektur-Signatur)

| Code | Signatur |
|---|---|
| S9.a | vier Kanäle, ein Seed: `β = φ₀/4π`, `Ω_b = (4π−1)/(4π)·φ₀`, `sin²θ13 = e^{−5/6}φ₀`, `λ_C² = φ₀(1−φ₀)` |
| S9.b | Decoder-Spezifität: ein latentes u schlägt gleich komplexe Rivalen |
| S9.c | LOO-Forward-Band: `β_pred = 0.2413 ± 0.0018°` aus Cabibbo+θ13+Ω_b (β nie im Fit) |
| S9.d | **Retarded-Tail-Ablation**: `u_tree = 1/(6π)` vs `u_ret = 1/(6π) + 3/(256π⁴)` — der Tail ist DIE spezifische topologische Korrektur (+0.23 %) |

- **Woher:** ein retardierter Seed treibt vier Pipelines (CMB/BBN/Reaktor/CKM).
- **Warum plausibel:** Cross-Kanal-**Ratios** sind u-unabhängig — ein Architektur-Test,
  kein Einzeltreffer-Glück.
- **Wo sichtbar/entschieden:** ACT/LiteBIRD/Simons (β), JUNO (θ13), Kaon-CKM (λ_C), BBN (Ω_b).
- **Status: HOLDS** (χ²/dof = 1.23; Decoder: AIC pro shared, 0/14 Nachbarn besser, 0.0tes
  Placebo-Perzentil; LOO alle < 2σ, θ13 der bekannte Crack-Kandidat bei −1.99σ).
  **LiteBIRD-Band ist der schärfste datierte Blindtest des Programms.**
- **S9.d (Lauf 2026-07-06):** heute unentscheidbar — |Δχ²| = 0.30 (marginal pro Tree,
  getrieben vom θ13-Crack; völlig insignifikant), der Tail verschiebt jeden Kanal um
  < 0.3σ. **Datierte Decider:** σ(V_us) ≈ 8·10⁻⁵ (Kaon/Lattice, ~10× besser als PDG),
  σ(sin²θ13) ≈ 1.8·10⁻⁵, σ(ω_b h²) ≈ 1.7·10⁻⁵; **LiteBIRDs β-Band testet den Seed,
  kann den Tail aber prinzipiell nie sehen** (braucht 1.8·10⁻⁴°). Frozen Crack:
  ≥ 2 Kanäle pro Tree bei ≥ 3σ töten die Retarded-Lesart. Prequential geführt (künftige
  Daten scoren gegen beide Seeds, kein Refit); vollständige Kovarianz (Ω_b–β-CMB-Systematik)
  bleibt die nächste Ausbaustufe.

### S10 — Horizon-Readouts (BH-spezifisch)

| Code | Signatur |
|---|---|
| S10.a | Bekenstein–Mukhanov-Linienkamm `ΔA = 4·ln3` ⇒ `f_n = n·ln3/(16π²M)` |
| S10.b | Hod-Overtone `ω_R/T_H → ln3 = ln N_fam` |
| S10.c | Echo-Delay aus Nariai-Kompaktheit `C = 3/8` ⇒ `Δt = 2.288·M_det` |
| S10.d | Scrambling-Offset `t_scr = 4M·ln S` (Offset ≠ Spacing-Zug) |
| S10.e | EHT achromatischer Pol-Intercept `β_BH(r) = 16c₃⁴·Q_e Q_m/r²` (achromatisch, 1/r², E·B-Sign-Flip) |

- **Woher:** Flächenquant v57, Nariai-Anker, Horizon-Collar (Appendix H).
- **Wo sichtbar:** Ringdown-Spektroskopie (O5+), EHT-Polarimetrie nach GRMHD-Subtraktion.
- **Status: a/c/d NULL auf 10 Events (search-target-Nulls); b data_limited (nur n=0 heute);
  e data_limited (M87-2017-Polarimetrie ingestiert, GRMHD-Residual-Produkte fehlen).**

### S11 — Per-Source-Comb-Phasenpersistenz

`φ_source` stabil über Sessions (persistente Seam-Marks) vs. freie Phase pro Event.

- **Status: NULL** (RC.04: R=0.21 über 7 Sessions p=0.15; bindet nur ε ≳ 0.15–0.3 —
  dieselbe Amplitudenwand; t0-alignierte Stacks PG.07 p=0.53 / Crust p=0.45 einig).

### S12 — Recovery-Kanal strukturell (intern, nie Naturevidenz)

CPTP/Choi, Datenverarbeitungs-Ungleichung, KL-geschützter Code, Page-Turnover
`t/τ = 1−(1/2)^{3/2}`, QT.01/02/04/05, Schaltkreis-Realisierung inkl. echter Hardware.

- **Status: alles bestanden (internal_consistency / instrument_validated);
  IBM-Hardware: Ein-Schritt-Survivals reproduziert, blinder Bend-Decode noise-verzerrt →
  data_limited.**

### S13 — Hexagon-/C₆-Phasenkanal [NEU 2026-07-06]

Die sichtbare *Phasen*physik der Theorie ist eher C₆ als C₄: Familie + Sheet-Twist =
μ₆-Struktur, hexagonale CM-Einheit `ρ = ζ₆`, Cusps `{0, 1/3, 2/3}`, `ζ = e^{iπ/3}` in
der Lepton-Struktur.

- **Woher:** μ₆ = μ₂×μ₃ (Sheet × Familie); CP-Phasen als Hexagon-Knoten
  (δ_PMNS = δ_CKM,lead + π; v231/v233; Kill-Test v320/v322: 240° ± ~9°, nächster
  falscher Knoten 60° entfernt).
- **Wo sichtbar:** **nicht FRBs** — CKM-γ, PMNS-δ_CP, Lepton-Frobenius-Algebra,
  hexagonale CM-Struktur; entschieden von DUNE/Hyper-K/JUNO (δ_CP), LHCb/Belle II (γ).
- **Status: teilexistent als Predictions of Record** (Scorecard: `cp_mu6_phase`-Gruppe,
  δ_PMNS bei +1.08σ von NuFIT-NO) — als *Signaturfamilie* jetzt explizit typisiert;
  die Frobenius-Algebra-Achse ist Theorie-Programm, kein Datentest heute.

### S14 — Clock-Map-Signatur [NEU 2026-07-06, Gate für S2b]

Nicht *eine Comb* testen, sondern die **richtige Zeitvariable**: pro System eine physisch
begründete Uhr `τ_mod = ∫dt/β(t)` (thermisch/modular/phase-accumulated), dann DSI auf
`ln τ_mod` — nicht auf `ln t_observer`.

- **Woher:** Die Log-Comb folgt aus `spec(T)` **nur** via `n = ln(t/t₀)/ln Λ_DSI`; im
  Horizon-Kontext ist die Uhr KMS/modular motivierbar (Research Contracts v238:
  Modularfluss konserviert die μ₄-Uhr), in Astro-Fades nicht.
- **Regel (ab jetzt):** **keine Clock-Map ⇒ kein S2b-Test** — der Kanal ist dann nur
  „exploratory surface DSI". Rückwirkend typisiert: alle bisherigen S2b-Nulls
  (A1–A5, Quake, Crust, PG, RC) liefen auf `t_observer` — informative Bridge-Nulls,
  keine Core-Nulls.
- **Status: Programm — erster benannter-Uhr-Test gelaufen (FO.03, 2026-07-07):**
  `τ_mod = Σ|ΔRM|` (Total-Variation-Uhr des Mediums) auf 20240114A-Sessions; 3 Sessions
  über dem 2.8-Perioden-Gate (2.82/2.85/3.16), Fisher p = 0.81 → **NULL bei
  detektierbarer Amplitude** (ε = 1.7 % bleibt hinter der Amplitudenwand). Die
  Konstruktion von τ_mod pro System bleibt offene Arbeit; der einzige Kanal mit
  KMS-gerechtfertigter Uhr ist weiter der Horizon-Sektor. **NEU (E23): das einzige
  Naturbett mit MOTIVIERTER Log-Uhr ist das primordiale Spektrum** (E-Folds sind
  eine Log-Uhr; ln k ∝ N): ω=2.583 liegt IN der publizierten Planck-Suchband
  (keine Detektion); ε_pred=0.0173 Faktor 1.7 unter der 95-%-Grenze →
  `data_limited` mit datiertem CMB-S4-Decider (Transfer-Bridge geflaggt).

### S15 — Transduktions-Auswahlregel [NEU 2026-07-06, Gate für S1–S7]

Für jede Observable `O = B·X`: teste oder begründe `B·P_r ≠ 0` für den relevanten
μ₄-/Transfer-Charakter. Ist `B·P_r = 0`, ist ein Null **vorhersagbar** — die Theorie
sagt dann selbst, wo sie prinzipiell unsichtbar bleibt.

- **Warum stark:** verwandelt „wir haben nichts gefunden" in zwei scharf getrennte
  Aussagen — *Bridge tot* (informativ gegen naive Emissionskopplungen) vs. *Core
  getestet* (nur wo B benannt ist: bislang **nur** S8/EIT und der QC-Kernel, wo B die
  Messapparatur selbst ist).
- **Observable Eligibility Gate (Pflichtfelder ab jetzt, vgl. 0b.1):** interne Größe /
  Kopplung / Nicht-Null-Argument. Retro-Typisierung: **kein einziger Astro-Kanal des
  Katalogs hat heute ein begründetes B** — genau deshalb sind S1–S7
  Surface-Leakage-Sonden.
- **Status: Typisierungsregel aktiv (dieser Katalog); als Theory-Contract-Kandidat
  notiert** (formale Version: für welche Standard-Emissionsprozesse ist `B·P_r = 0`
  beweisbar?).

---

## 1b. Harte Neubewertung (2026-07-06)

| Familie | Neubewertung |
|---|---|
| S1, S2b, S4, S5, S6, S7 | **Surface-Leakage-Sonden** — Nulls informativ gegen naive Emissions-Bridges, nicht gegen den Core |
| S2a | Kern-nah, fast unbestellt — richtige nächste Suchrichtung *mit* Transduktion |
| S3 | kaum diskriminierend (Bend degeneriert, Wall generisch) — behalten, nicht priorisieren |
| **S8** | **Hauptachse** — Operator-/Zustandsinvarianz ist die Sprache des Kerns |
| **S9** | bester Naturdaten-Anker — hart nur prequential (v5-Band, v6-Tail, volle Kovarianz) |
| S10 | bewusst gemischt: großteils Standardphysik in Seam-Einheiten + Search-Targets (Appendix-H-Selbsteinordnung) |
| S11 | amplitude-limited, nicht aufblasen |
| S12 | interne Konsistenz, so lassen |
| S13–S15 | die neuen Achsen: Hexagon-Phasen (Präzisions-/Beschleuniger-Programm), Clock-Map-Gate, Transduktions-Gate |

**Strategiewechsel in einem Satz:** weniger „welche sichtbare Zahl spuckt die Theorie
aus?", mehr „welche Operatoren kommutieren, welche Charakterklassen mischen nicht,
welche Zustände sind invariant?" — Randoperatoren, Kovarianzen, modulare Zustände,
Charakterleckage, prequentiale Präzisionstests.

---

## 2. Experiment- und Datenregister (E-Codes)

| E | Experiment | Daten (Quelle, Umfang, Qualität) |
|---|---|---|
| E01 | `frb-tfpt-signatures` | FAST FRB20121102A (Li+2021, **1652** Bursts, Energie); Blinkverse multi-source; FAST 20240114A **pol v5 (6134** Bursts, RM/DOL/DOC/PA); CHIME Cat1; Pandhi+2024-Pol — publizierte Kataloge, hohe Statistik |
| E02 | `gw-ringdown-echo` | GWTC-5.0 (391 Zeilen) + echtes GWOSC-Strain der **10 lautesten Ringdowns** (inkl. GW250114, SNR 78.6), 23 Detektorströme, 4 + 16 kHz; injektionskalibrierte ε₉₀ |
| E03 | `gw-ringdown-spectroscopy` | nur n=0-QNM heute → strukturell data_limited |
| E04 | `gw-speed-multimessenger` | GW170817 + GRB170817A |
| E05 | `pulsar-glitch-recovery` | JBO-Katalog (**726** Glitches/222 Pulsare); Yu+2013 (60 Q/τ_d); Crab-Monatsephemeride (479 Punkte/38 J.); NICER J0537 (1165 Obs, Liste) + Vela (665, 1 reduziert); Zenodo-LVK Vela-2024 `.par` (phase-connected); **PuMA/IAR** Tages-TOAs (969, pulse-numbered) |
| E06 | `recovery-comb-domains` | Swift-XRT/LSXPS **6 Magnetare**; FAST/GBT **8** `.calibP`-Tails; **CHIME-Baseband 8** FRBs (2.56 µs, full-Stokes, koh. dedisp. — beste Tail-Qualität); UKSSDC **22 GRB**-Afterglows; ZTF-ENT J2245+3743 (1007 Epochen); **USGS 6 Beben** (bis 5.4 Perioden — datenreichstes Bett); Microshots (Hewitt+2023, vetted, 27+18) |
| E07 | `repeater-cascade` | **9 916** Bursts / 4 Quellen (FAST 20220912A/20201124A/20240114A + 15 CHIME-Cat2-Repeater); 9 gate-passierende Sessions bis 4.8 Perioden |
| E08 | `crust-cooling-comb` | 67 kT_eff-Epochen / 8 Episoden / 6 Transients (publizierte Tabellen) — density-poor |
| E09 | `strange-metal-comb` | LSCO x=0.24 Masterkurve (Michon+2023, 11 227 Punkte) + Au/Cu-Drude-Kontrollen — Laborqualität |
| E10 | `comb-meta-limit` | Meta-Analyse (HKSJ) über A1/A4/A5 + Pulsar/GW read-only |
| E11 | `dsi-false-positive-control` | USGS ComCat (17 654 Events), GOES-Flares (1 076), **Efimov**-Leiter, Glas/MCT — Detektor-Spezifität |
| E12 | `hfqpo-ladder` | 4 publizierte BH-HFQPO-3:2-Paare; ×1.5-Zahn-Suche **preregistriert** für RXTE-Archiv (nicht gelaufen) |
| E13 | `qpe-recurrence` | eRO-QPE2 + GSN 069 Timing |
| E14 | `frb-kernel-couplings` | Li+2021 (1652) + Zhang+2023 (1076, Zeiten+Energien) + pol v5 (6134, signiertes V, PA) |
| E15 | `seed-consistency` (+`cmb-birefringence-seed`) | ACT DR6 β; BBN D/H Ω_b; Daya Bay/RENO/DC θ13; PDG V_us |
| E16 | `eht-achromatic-residual` | echte EHT-M87-2017-Polarimetrie (4 Tage × 2 Bänder) |
| E17 | `qgeo-eit-soff` (+`theory-contracts/qgeo_*`) | **KIT4 Open EIT** (Zenodo, 38 reale Tank-Messungen, 16 Elektroden) + Steklov-Simulation |
| E18 | `qc-recovery-kernel` | Qiskit Aer exakt + FakeBrisbane + **ibm_marrakesh** (13×16 384 Shots, echte Hardware) |
| E19 | `recovery-channel` | datenfrei (CPTP/Page/Petz strukturell) |
| E20 | `quantum-testbed` | synthetisch (QT.01–QT.05) |
| E21 | `frb-ontology` (+`theory-contracts/fo01_*`) | FO.01–10 Ontologie-/Operator-Runde (2026-07-07): pol v5 (6134) + Blinkverse-Episoden + CHIME Cat1/Cat2 + Li+2021/Zhang+2023; FO.01 = Simulations-Contract |
| E22 | `uhecr-energy-dsi` | Auger Open Data Release 3 (Zenodo-DOI, 10 % der publizierten Events): 21.571 SD1500 + 54.434 SD750, 0.1–144 EeV = 2.99 Kamm-Perioden — größter ln-E-Bereich der Natur |
| E23 | `cmb-primordial-logcomb` | publizierte Planck-2018-X-Feature-Suche (+ SPT-3G/ACT-Kombination) — Typing, kein Re-Fit; einziges Naturbett mit motivierter S14-Uhr |

---

## 3. Test-Matrix (welche Signatur wo, mit Ergebnis)

| S | getestet in | Ergebnis (Kurzform) |
|---|---|---|
| S1.a–d | E01 (FRB.02/02b/07: 1652 Bursts + 4 Quellen), E02 (Echo-Zug ≤(2/3)⁶, Stack p=0.26, ε₉₀≈0.63–0.9×A220), E05 (PG.01–03: p 0.27/0.93), E06 (Microshot-Echo enr 0.80), E07 (RC.03 Bonferroni 0.10), E13 (2/3-Tooth >17× Spread entfernt) | **NULL überall**; GW = Upper Bound (Kernel-Decke ~7× unter Sensitivität) |
| S1.e | E12 | **data_limited** (×1.5-Zahn nie publiziert; RXTE-Prereg liegt) |
| S2 | E05 (PG.05 p 0.12–0.44; PG.07 p=0.23; PG.08 J1740 2.81 Per. p=0.48, Power 0 % @1.7 %), E06 (A1 p=0.99; A3 0.34; A3b 0.67; **A4 0.13 well-powered**; **A5 0.80/Batterie 0.095**; **Quake Bonferroni 0.94**), E07 (RC.02 Fisher 0.72/0.38), E08 (superposed 3.08 Per. p=0.45), E09 (p=0.30, ε-Floor 0.19), E10 (UL ε<0.12), E11 (0/5 False-Positives — Detektor spezifisch) | **NULL wo well-powered; data_limited an der ε≈1.7 %-Wand** |
| S3.a | E02 (Stage 2, Degeneration maschinengeprüft), E05 (PG.04c 0/12; PG.08-GLTD 0/2), E06 (Microshot-Gap p=0.16), E07 (RC.01 0/37), E18 (exakt 2.709511; Hardware-Decode 1.96 verzerrt) | **NULL/degeneriert; intern exakt** |
| S3.b | E05 (45/46 ≤2 Moden; Vela-2021 3 Moden = Ausnahme on record), E06 (Microshots: Run 5 > 3) | **konsistent (schwach), 2 Ausnahmen on record** |
| S3.c | E08 (7/8 Floors — generisch), E18 (Floor-Retention 0.993 sim / 0.860 Hardware) | **konsistent, nicht TFPT-spezifisch** |
| S4.a/b | E05 (PG.07: 0.27/0.23; PG.08: J1740 0.17/0.0018*→Placebo-Bump), E06 (Quake 0.62/0.45; A1–A5 0.21–0.96; Microshots (3/2)³ über Gate p=0.40), E07 (Fisher 0.25/0.14), E08 (0.99/0.27) | **NULL**; *J1740-(3/2)⁴ = breiter ω≈3.6–4.0-Bump (Placebo gleich signifikant), kein Kandidat |
| S4.c | alle S2-Betten | **range-blind überall** (braucht 13.6 e-folds; Max 13.1) → data_limited; E07-Fisher 4·10⁻⁴ = sub-gate-Artefakt (Placebo-λ gleich extrem) |
| S4.d | E02 (Stage-1c-Battery, Bonferroni ×12) | **NO_VARIANT_ECHO** (10 Events) |
| S4.e | E14 (KC.02: 3454 Paare) | **NULL** (Alternation 0.480 vs 0.497, p=0.98 — Händigkeit persistiert eher) |
| S5.a | E01 (FRB.08) | **NULL** (Fundamentale m=2, nicht m=4) |
| S5.b | E01 (FRB.04, AR(1)-Null) | **NULL** (0/3) |
| S5.c | E01 (FRB.06, placebo-kontrolliert) | **NULL** |
| S5.d | E14 (KC.04: 83 Sessions/5934 Paare) | **NULL** (Perm-p 0.0005 ist PA-Drift; Shift-Null 0.12, Off-Kernel-Rank 0.37) |
| S5.e | E02 (Battery {0, π/2, π, 3π/2}) | **NULL** |
| S6 | E14 (KC.01: 1569+1040 Paare, exakte Energie-Shuffle-Null) | **well-powered NULL beide Quellen** (enr 0.72/0.68; freier Quotient schlägt 2/3 in >55 %) |
| S2a/S8-Proxy | E14 (KC.05/06: FAST 20240114A Pol v5) | **NULL**: KC.05 C4-Off=0.4268 (p_low 0.0045, aber Z3/generische Marks besser/nicht schlechter → nicht C4-spezifisch); KC.06 Lag-Spektrum `[1,0.5066,0.3844,0.0478]` nicht nahe `{1,64/729,1/729}` (p_close=0.18) |
| S7 | E05 (PG.01: GMM-Null p=0.075, LEE), E14 (KC.03: Bonferroni 0.185/0.68; λ=8-Erstlauf-Artefakt on record), **E22 (UHECR, 2026-07-07: größter ln-E-Bereich der Natur, 2.99 Perioden — Kernel p=0.49/Rank 0.77, Batterie-Bonferroni 0.26 nach per-ω-Kalibrierung; Injection 23 % @ ε_pred)** | **NULL in drei Domänen; UHECR-Vorhersage-Amplitude teilweise abgedeckt** |
| S8.a–c | E17: Simulation (exakt <10⁻³⁰; Rekonstruktion O(σ²) vs Kontrollen O(1); Power ε=0.001 @σ≤10⁻³) + **echte KIT4-Daten** (Floor S_off=7.6·10⁻⁵; 28 anisotrope lecken generisch; 0 C4-Positive wie erwartet; Klassifikator 34/37, Mismatches physikalisch real) | **Instrument+Diskriminator validiert; H3 (μ₄-Positiv) preregistriert, NICHT gemessen** |
| S9.a–c | E15 (v1–v5) | **HOLDS**: χ²/dof 1.23; Decoder 0/14 + 0.0-Perzentil/2000; LOO alle <2σ; **Forward-Band β = 0.2413 ± 0.0018° für LiteBIRD/SO** |
| S9.d | E15 (v6, 2026-07-06) | **heute unentscheidbar** (\|Δχ²\| = 0.30, Tail < 0.3σ in jedem Kanal); datierte Decider: σ(V_us)≈8·10⁻⁵, σ(sin²θ13)≈1.8·10⁻⁵, σ(ω_b h²)≈1.7·10⁻⁵; β kann den Tail prinzipiell nie sehen |
| S13 | Scorecard-Zeilen δ_CKM/δ_PMNS (cp_mu6_phase; v320/v322-Kill 240°±9°) | **consistent** (+1.08σ NuFIT-NO); DUNE/Hyper-K/JUNO/LHCb/Belle II entscheiden |
| S14/S15 | Typisierungs-Gates (dieser Katalog) | aktiv; retro-typisiert: alle bisherigen S2b-Nulls = Bridge-Nulls; **seit FO.02 hat EIN Astro-Kanal ein begründetes B** (DM/RM-Linienintegrale) |
| FO.01 | E21 (theory-contracts, Simulation) | **5/5 PASS**: Uniform-Funktional exakt blind (1e-14); Threshold-Intensitäts-Züge Kernel vs Scrambled ununterscheidbar (KS D 0.006–0.009); Charakter-Readout recovert 64/729 exakt; ungleiches B unterscheidet (D=0.061, p=5e-33) — die FRB-Null-Landschaft als Vorhersage |
| FO.02 (S2a, benanntes B) | E21 (pol v5, 89 Nächte) | **data_limited**: AIC bevorzugt Einzelraten (8.07 vs 12.54); Shared-Ratio 4.20, Kernel nicht am nächsten |
| FO.02b (S2a, Intra-Session) | E21 (pol v5, 35 Sessions + 20201124A/Xu+2022, 12 Sessions) | **data_limited (informativer Negativbefund)**: RM-Varianz real (χ²_red 77–337), aber OHNE Gedächtnis — 33/35 bzw. 12/12 Sessions unter dem injektionsvalidierten Memory-Gate → per-Burst-Streuung, kein relaxierender Medium-Zustand |
| FO.03 (S2b+S14, benannte Uhr) | E21 (pol v5) | **NULL** bei detektierbarer Amplitude (3 Gate-Sessions, Fisher p=0.81) |
| FO.04 (S4/S5-Typisierung) | E21 (pol v5, 6133 PA-Bursts) | **consistent**: m=4-Exzess = Verteilungs-Misfit (Batterie: z3≈z4, Glatt-Null p=0.64; Erstlauf-`tension` on record), Schaltzeiten ratenfrei (p=1.0), Persistenz 45/45 (p=2.8e-14) |
| FO.05 (S1-Episodenebene) | E21 (Blinkverse+v5+Cat2, 8 Quellen) | **NULL**: Gap-Bonferroni p=1.0, Energie p=0.44; 10-d-Sekundärlesart einig; Scheduling-Systematik on record |
| FO.06 (Z₂-Blattklassen) | E21 (CHIME Cat1, 474 Erst-Subbursts) | **null für die Zweiklassen-Vorhersage** (BIC k=3, nicht 2); AUC 0.833 repliziert Pleunis+2021 (default Astro/Selektion) |
| FO.07 (S8-auf-Daten: Kovarianz-Blöcke) | E21 (v5, 5694 komplette 10-Obs-Bursts) | **consistent**: Blockstruktur real (Bonferroni p=0.006 gegen Spektrum-erhaltende Null), aber Partition = Standard-Sektorsplit Faraday/Geometrie vs Emission (Rand 1.0; v1.3.1-Gate); Erstlauf-hint on record |
| FO.08 (S15-Lochsuche: Pol-Nullraum) | E21 (v5, 6107 S/N≥20) | **NULL**: größte leere Scheibe in (DOL,DOC) r=0.30 vs Marginal-erhaltende Joint-Null 0.55 (p=1.0) — kein verbotener Bereich jenseits der Marginale |
| FO.09 (Rank-Drop ≤3 Moden) | E21 (Li+2021 27 + Zhang+2023 10 Sessions) | **NULL**: Median-Effektivrang 0 in beiden Quellen (memoryless, keine 3-Moden-Mannigfaltigkeit); v5-Multivariat-Leg deskriptiv geflaggt (vermischt FO.07-Statik mit Dynamik) |
| FO.10 (Zeitpfeil) | E21 (2614 Inkremente / 2 Quellen) | **NULL — neuer Bound**: Inkrement-Skew + Pomeau-A alle Reversal-p ≥ 0.36 (Bonferroni 1.0) → Burst-Energie-Sequenzen zeitumkehr-symmetrisch; begrenzt jede „gerichtete Recovery"-Lesart (und ist die FO.01-Vorhersage); Quake-Kontrolle offen (Daten gitignored) |
| S10.a | E02 (Stage 1e, Spacing-Battery) | **NO_BM_COMB** (power-limitiert, kein Kill) |
| S10.b | E03 | **data_limited** (braucht O5+-Overtones) |
| S10.c/d | E02 (Stage 1d v2 + 16 kHz; Stage 1f) | **NO_POINT_ECHO / NO_OFFSET_TRAIN** (best p_bonf 0.035–0.053, nie koinzident) |
| S10.e | E16 | **data_limited** (Polarimetrie ingestiert; GRMHD-Residual-Nulls offen) |
| S11 | E07 (RC.04), kohärente Stacks in E05/E08 | **NULL** (bindet nur ε ≳ 0.15–0.3) |
| S12 | E18/E19/E20 | **bestanden** (intern); Hardware-Bend data_limited |

---

## 4. Gesamtbild pro Familie (eine Zeile)

- **S1 statisch:** tot in allen Betten mit Statistik; GW nur als Obergrenze erreichbar.
- **S2 Comb:** die Range-Wand ist gefallen (RC/PG.08/Quake), jetzt bindet überall die
  **Amplitudenwand ε ≈ 1.7 %**; alle well-powered Betten null.
- **S3 Uhr:** Bend in Einzelrecoveries beweisbar unsichtbar; Wall/Floor nur schwach typisierbar.
- **S4 Möbius:** Blind Spots geschlossen — null; die Fundamentale bleibt prinzipiell ungetestet (Range).
- **S5 μ₄-Pol:** vollständig null, inkl. der Helix nach Drift-robuster Null.
- **S6 Kopplung:** das forcierte 2D-Signal fehlt — der stärkste neue Null des Programms.
- **S7 Size-DSI:** null in Pulsar- und FRB-Domäne.
- **S8 Operator:** validierte Messplattform; Entscheidung liegt beim H3-Laborlauf.
  FRB-KC.05 ist nur ein Astro-Proxy und null.
- **S9 Seed:** einziges durchgehend positives Konsistenz-Ergebnis; LiteBIRD-Band = schärfster datierter Test.
- **S10 Horizon:** search-target-Nulls; echte Reichweite erst mit O5/GRMHD.
- **S11/S12:** Persistenz-Lesart begrenzt; interne Struktur vollständig bestätigt.

## 5. Nicht in diesem Katalog (bewusst)

Predictions of Record und Watchdogs ohne Kernel-Bezug (θ12, n_s/r/A_s, Σm_ν, w=−1-Pincer,
Neutronen-Lebensdauer, X17/R_D(*), S8/H0-Budget, Li-7, Dipol, Proton, g−2-Seam-Vertex,
Axion-Branches, CCBH, …) — vollständig typisiert in `evidence_scorecard.json` (111 Zeilen,
Stand 2026-07-07: 47 consistent / 9 tension / 22 null / 32 data_limited / 1 parked) und im
Website-Audit-Block. Reine Mathematik-Kontrakte in `theory-contracts/` (nie Scorecard).

## 6. Offen / nicht testbar (ehrlich)

| Was | Warum offen | Was es bräuchte |
|---|---|---|
| S4.c antiperiodische Fundamentale | 13.6 e-folds ln-Range nötig, Max. 13.1 | längere Aftershock-/AGN-Baselines |
| S8-H3 μ₄-Positiv | Konfiguration existiert in keinem Archiv | KIT4-Labor, 4 Agar-Zylinder (Protokoll eingefroren) |
| S10.b Hod-Overtone | nur n=0-Spektroskopie | O5+/ET |
| S10.e EHT-Residual-Nulls | GRMHD-Subtraktionsprodukte nicht öffentlich | EHT-Kollaborations-Produkte |
| S2 @ ε=1.7 % | Amplitudenwand | sub-day-Vela-TOAs, ~10⁵-Burst-Sessions, B4/B5-bespoke |
| S5.d RM-korrigiert | PA mod π, RM-unkorrigiert | RM-korrigierte Full-Stokes-Serie |
| S9.d Tail-Entscheid | Tail < 0.3σ in jedem heutigen Kanal | σ(V_us) ≈ 8·10⁻⁵ (Kaon/Lattice) — der realistischste Decider |
| S2a mit Transduktion | kein benanntes B in Astro-Kanälen | Transduktions-Theorie (S15) oder Analog-System mit bekanntem B |
| S13 Frobenius-Achse | Theorie-Programm | Lepton-Algebra-Kontrakt + DUNE/Hyper-K-δ_CP |

# TFPT und die Hypergraph‑Theorie — einfach erklärt

*Wo und wie genau berührt sich TFPT mit der Hypergraph‑/Netzwerk‑Theorie (Stephen Wolframs „Physics Project")? Eine ehrliche Bestandsaufnahme: was wirklich trägt, was Metapher bleibt, und was offen ist.*

---

## 0. Kurz vorab: die Begriffe in Alltagssprache

- **Graph** = Punkte (Knoten), verbunden durch Linien (Kanten). Jede Kante verbindet **genau zwei** Punkte.
- **Hypergraph** = dasselbe, aber eine „Hyperkante" darf **mehrere** Punkte auf einmal verbinden (eine Gruppe statt eines Paares). Beispiel: ein Dreieck als *eine* Hyperkante über 3 Punkten.
- **Wolframs Ansatz** = Das Universum ist ein riesiger Hypergraph, der sich Schritt für Schritt nach simplen **Umschreibe‑Regeln** („Rewrites") aktualisiert. Raum, Zeit und Physik sollen als **Muster** aus diesem Geschehen *entstehen*.
- **Attraktor** = ein Muster, auf das ein System **immer zuläuft**, egal wo es startet (wie Wasser, das immer zum Abfluss findet).
- **Spektraler Gap** = wie schnell sich ein Netzwerk „einpendelt" (die Mischrate eines Zufallsprozesses auf dem Netzwerk).

**Die Kernfrage:** Ist TFPT eigentlich verkappte Hypergraph‑Physik? Oder anders gefragt — *gibt es eine TFPT‑Struktur, die sich natürlich als Hypergraph lesen lässt?*

**Kurzantwort:** Ja, an drei sehr konkreten Stellen — aber **auf der algebraischen Skelett‑Ebene**, nicht (noch nicht) auf der Ebene einer emergenten Raumzeit. Das ist der entscheidende, ehrliche Unterschied.

---

## 1. Wo es WIRKLICH trägt — drei harte, nachgerechnete Korrelationen

### 1.1 Der Ikosaeder ist buchstäblich ein Hypergraph — und seine Symmetrie *erzeugt* E8

TFPTs zwei Axiome reduzieren sich auf die drei „Atome" **(2, 3, 5)**. Genau diese drei Zahlen sind die Symmetrie‑Ordnungen des **Ikosaeders**:

| Objekt | Anzahl | Symmetrie |
|---|---|---|
| Ecken | 12 | **5**‑zählig |
| Flächen (Dreiecke) | 20 | **3**‑zählig |
| Kanten | 30 | **2**‑zählig |

Die 30 Kanten sind kein Zufall: **30 = 2·3·5 = die Coxeter‑Zahl von E8**.

Lese die **20 Dreiecksflächen als Hyperkanten** über den 12 Ecken — dann ist der Ikosaeder ein **3‑uniformer Hypergraph** (jede Hyperkante verbindet 3 Knoten). Nachgerechnet: seine Automorphismengruppe (alle Symmetrien) hat **Ordnung 120**. Und 120 ist *genau* die Ordnung der binären Ikosaedergruppe `2I` — derselben Gruppe, deren **McKay‑Graph das affine E8 ist** (`v219_icosahedral_mckay.py`).

> **Korrelation 1 (Hypergraph‑Automorphismen ↔ E8):** Ein konkreter, kleiner 3‑uniformer Hypergraph (der Ikosaeder) trägt *exakt* die Symmetriegruppe, aus der E8 entsteht. Hypergraph‑Theorie spricht hier dieselbe Sprache wie TFPT: **Symmetrie eines kleinen Netzwerks → E8.**

### 1.2 Die E8‑Struktur ist ein Netzwerk‑Attraktor

Die „McKay‑Korrespondenz" (`v219`) baut aus der Gruppe `2I` einen 9‑Knoten‑Graphen (das affine E8‑Diagramm). Die „Kac‑Marks" dieses Graphen sind die Zahlen **(1, 2, 3, 4, 5, 6, 4, 2, 3)** — und sie sind *kein* eingegebener Input.

Nachgerechnet (`v298_e8_network_attractor.py`): Startet man mit **irgendeiner** positiven Belegung der 9 Knoten und wendet wiederholt eine **minimale lokale Mittelungsregel** an —

> jeder Knoten ← halb sich selbst + viertel der Summe seiner Nachbarn  (`m ← (A + 2I)/4 · m`)

— dann läuft das System **immer** auf die E8‑Marks zu (auf 16 Nachkommastellen genau). Das ist Lehrbuch‑Hypergraph‑Theorie: ein **Perron‑Frobenius‑Attraktor** eines Netzwerk‑Updates.

> **Korrelation 2 (Netzwerk‑Attraktor ↔ E8):** Die E8‑Marks sind der **eindeutige Attraktor** einer simplen lokalen Regel auf dem (2,3,5)‑Netzwerk. Genau die Art „universeller Attraktor", die Wolframs Programm betont — hier exakt realisiert.

### 1.3 Die Recovery‑Dynamik *ist* ein Transferoperator mit Attraktor + Gap

TFPTs „Recovery" / „gapped attractor" wirkt nicht wie eine Kraft, sondern wie ein **Update** — genau wie eine Rewrite‑Regel. Nachgerechnet (`v160`/`v162`): der Boundary‑Transferoperator hat das exakte Spektrum

```
{ 1 , (2/3)^6 , (1/3)^6 }
```

- Eigenwert **1** → der **eindeutige Attraktor** (der Fixpunkt, auf den alles zuläuft).
- Zweiter Eigenwert **(2/3)^6 = 64/729** → *das ist der Recovery‑Faktor selbst*.
- Spektraler **Gap** = `−log((2/3)^6) = 6·log(3/2)` → die „Mischrate".

> **Korrelation 3 (Spektrale Graphentheorie ↔ Recovery):** Der Recovery‑Faktor ist **nicht** irgendeine Zahl, sondern der **zweite Eigenwert eines Transferoperators** — und der Gap ist seine Mischrate. Das ist exakt spektrale Netzwerk‑/Markov‑Theorie.

### 1.4 (Bonus) Wachstums‑Rewrite: E8 ist das Terminal einer minimalen Wachstumsregel

Die ehrlich stärkste Rewrite‑Aussage. Nimm den Stern‑Graphen `T_{2,3,r}` (ein Zentrum, drei Beine der Längen 2, 3, r) und die **minimale Wachstumsregel** „verlängere das dritte Bein um einen Knoten". Nachgerechnet (Determinante der Cartan‑Matrix):

| r | Graph | det | Typ |
|---|---|---|---|
| 3 | E6 | 3 | endlich (gutartig) |
| 4 | E7 | 2 | endlich |
| 5 | **E8** | **1** | endlich (**unimodular!**) |
| 6 | Ê8 (affin) | 0 | kritischer Rand |
| 7 | E10 | −1 | hyperbolisch (entgleist) |

> **Korrelation 4 (Graph‑Wachstums‑Rewrite ↔ E8):** Eine minimale „Knoten‑anhängen"‑Regel bleibt **genau bis E8 endlich** (det = 1, das ist *warum* E8 das einzige gerade unimodulare Rang‑8‑Gitter ist), kippt bei Ê8 in den affinen Rand und danach ins Hyperbolische. **(2,3,5) ist erzwungen** als „das größte Netzwerk, das noch gutartig bleibt". Das ist die sauberste Realisierung von „E8 aus einer minimalen Wachstumsregel".

### 1.5 (Bonus) Die E‑Kaskade ist Graph‑Vergröberung (Renormierung)

`E8 ⊃ E7 ⊃ E6 ⊃ D5 ⊃ A4` durch sukzessives Knoten‑Löschen, Wurzelzahlen `240 → 126 → 72 → 40 → 20`. Das liest sich als **graphische Renormierung** (Informationsreduktion Schritt für Schritt) — Wolframs „feiner Hypergraph → gröbere Beschreibung".

---

## 2. Wo es NICHT trägt — ehrliche Negative

Damit das hier keine „Mustererkennung mit Glitzerhut" ist:

- **φ₀ ist KEINE Netzwerk‑Größe.** Man könnte versucht sein, `φ₀ ≈ 0.0531` als „Anteil stabiler Hyperkanten" zu lesen. Falsch: `φ₀ = (4/3)·c₃ = 1/(6π)` ist ein **analytischer Seed** aus der Seam‑Konstante, keine Kantenfraktion.
- **Die Seam ist (noch) kein Rewrite‑System.** Der Seam‑DtN‑Operator ist zwar ein gewichteter Graph auf Fourier‑Moden, aber das ist eine *Darstellung*, kein Hyperkanten‑Umschreiben.
- **Es gibt keine emergente Raumzeit‑Dimension.** Wolframs eigentlicher Trick — Dimension/Geometrie entstehen aus einem mikroskopischen Kausalgraphen — hat in TFPT **kein Gegenstück**. TFPTs Strukturen sind *darstellungstheoretisch/gittertheoretisch* (E8, Wurzeln, Charaktere), nicht geometrisch‑emergent.

---

## 3. Der Rewrite‑Test — jetzt durchgerechnet

Statt der zu großen Frage „Rewrite → E8" habe ich den scharfen, gruppentheoretisch testbaren Aufhänger durchgerechnet: **Gibt es ein minimales Hypergraph‑Rewrite, das die binäre Ikosaedergruppe `2I` (die E8‑erzeugende Symmetrie) trägt?** Antwort: **Ja, zweifach — auf der Symmetrie‑ und auf der Struktur‑Ebene.**

### 3.1 Ein minimales Rewrite trägt die 2I‑Symmetrie auf ALLEN Skalen

Das kanonische Kandidat‑Rewrite ist die **geodätische Dreiecks‑Unterteilung**: ersetze jede Dreiecks‑Hyperkante durch 4 (Knoten auf die Kugel setzen). Das ist eine lupenreine lokale Umschreibe‑Regel im Wolfram‑Stil:

```
1 Dreieck   ──►   4 Dreiecke      (Knoten 12 → 42 → 162 → …)
                                  (Kanten 30 → 120 → 480 → …)
                                  (Flächen 20 → 80 → 320 → …)
```

Nachgerechnet: **alle 120 Ikosaeder‑Symmetrien bilden auch den unterteilten Hypergraphen auf sich ab — auf jeder Stufe (120/120).** Das Rewrite ist also **äquivariant**: die volle `2I`‑Bild‑Symmetrie bleibt zu allen Skalen erhalten.

> **Ergebnis A:** Ein konkretes, minimales lokales Hypergraph‑Rewrite *trägt* die E8‑erzeugende Symmetrie unbegrenzt. „Rewrite → 2I" ist auf der **Symmetrie‑Ebene erfüllt**.

### 3.2 `2I` selbst IST ein Hypergraph — mit E8 als Skelett

Die Fusionsregel der 9 Darstellungen von `2I` (`n_i ⊗ n_j = ⊕ N^k_{ij} n_k`) ist ein **nichtnegativer 3‑Index‑Tensor** `N^k_{ij}` (Einträge 0,1,2,3). Das ist *exakt* ein **gewichteter 3‑uniformer Hypergraph** auf 9 Knoten. Nachgerechnet: der zugehörige Fusionsring ist kommutativ und assoziativ, und die **Scheibe an der 2‑dim‑Darstellung ist der McKay‑Graph = affines E8** (`A·deg = 2·deg`, Spitzen‑Eigenwert 2).

> **Ergebnis B:** Die Darstellungstheorie von `2I` ist wörtlich ein Hypergraph (der Fusionstensor), und **E8 fällt als seine 2‑dim‑Scheibe heraus**. „Rewrite → 2I" ist auch auf der **Struktur‑Ebene erfüllt**.

### 3.3 Was damit beantwortet ist — und was offen bleibt

| Frage | Status |
|---|---|
| Trägt ein minimales Rewrite die `2I`/E8‑Symmetrie? | **Ja** (äquivariantes Subdivision‑Rewrite, 120/120 auf allen Skalen) |
| Ist `2I`‑Struktur ein Hypergraph mit E8 darin? | **Ja** (Fusionstensor, 2‑dim‑Scheibe = E8) |
| Erzeugt eine *Dynamik* E8 als **Attraktor**? | **Teilweise** — E8 ist der kritische Attraktor einer spektral‑stabilen Wachstumsdynamik (Abschnitt 3.4) |

Der entscheidende ehrliche Punkt: **Symmetrie‑tragen ≠ Emergenz.** Das Subdivision‑Rewrite *bewahrt* die Ikosaeder‑Symmetrie, aber es *erzeugt* E8 nicht von selbst. Die nächste Frage ist also: gibt es eine **Dynamik**, die E8 *hervorbringt*? Abschnitt 3.4 zeigt: teilweise ja.

### 3.4 Emergente Dynamik: E8 als kritischer Attraktor (Smiths Satz)

Es gibt einen klassischen Satz, der „Netzwerk‑Stabilität" zu einem **dynamischen Selektor** macht — **Smiths Satz (1970):**

> Ein zusammenhängender Graph hat Spektralradius `ρ ≤ 2` **genau dann**, wenn er ein (affines) ADE‑Diagramm ist. `ρ < 2` ⇔ endliches ADE; `ρ = 2` ⇔ affines ADE.

Der Spektralradius `ρ` (größter Eigenwert der Adjazenzmatrix) misst, ob ein Netzwerk‑Update **kontrahiert** (`ρ<2`, stabil), **marginal** ist (`ρ=2`, kritisch) oder **entgleist** (`ρ>2`). Nachgerechnet:

| Graph | ρ | Phase |
|---|---|---|
| A₅ / A₁₀ (Pfad) | 1.732 / 1.919 | endlich, stabil |
| E6 / E7 / **E8** | 1.932 / 1.970 / **1.989** | endlich, stabil |
| **Ê8** (affin) | **2.000** | **kritisch** |
| E10 | 2.007 | entgleist |

Eine **Wachstumsdynamik** „hänge zufällig einen Knoten an, akzeptiere nur wenn `ρ ≤ 2`" ist damit **per Satz auf die (affinen) ADE‑Diagramme eingesperrt**. Im experimentellen Lauf wächst sie von E6 bis genau an die kritische Fläche `ρ = 2` (Ê8‑Größe) und kann nicht darüber hinaus. Innerhalb der exzeptionellen (3‑armigen) Familie ist **E8 der maximale endliche** Punkt und **Ê8 der kritische Attraktor**.

Und das ist *dieselbe* Eigenwert‑2‑Fläche, auf der der McKay‑Marks‑Attraktor lebt (Abschnitt 1.2, Spitzen‑Eigenwert 2). Damit fügt sich alles zusammen:

> **E8 sitzt genau auf der kritischen Grenze `ρ = 2`** zwischen kontrahierender (endlicher) und entgleisender (indefiniter) Netzwerk‑Dynamik. Das ist *die* Eigenschaft, die E8 zum Attraktor einer „auf‑Kritikalität‑getunten" Dynamik macht — nicht eingegeben, sondern als kritischer Fixpunkt selektiert.

**Was jetzt noch offen ist:** Der Stabilitäts‑Selektor `ρ ≤ 2` ist in 3.4 *auferlegt*, nicht aus einer mikroskopischen Regel *hergeleitet*. Genau das löst der nächste Abschnitt zum größten Teil auf.

### 3.5 Die Mikro‑Regel: `ρ ≤ 2` ist *lokal* (Collatz–Wielandt)

Der scheinbar globale Spektral‑Selektor ist in Wahrheit eine **rein lokale Pro‑Knoten‑Bedingung**. Der **Satz von Collatz–Wielandt** sagt:

> `ρ(A) = min_{m>0} max_i (A·m)_i / m_i`.

Daraus folgt sofort: **`ρ ≤ 2` ⟺ es gibt ein positives Knotengewicht `m`, sodass an JEDEM Knoten gilt**

```
Summe der Nachbar-Gewichte  ≤  2 · eigenes Gewicht        (Σ_{j~i} m_j ≤ 2 m_i)
```

Das ist keine globale Eigenwert‑Rechnung mehr, sondern eine **lokale Balance‑Regel** mit einem positiven Zeugen `m`. Nachgerechnet:

| Graph | ρ | lokaler Zeuge `m>0` mit `A m ≤ 2 m`? |
|---|---|---|
| A₅, E6, E7, **E8** | < 2 | **ja** |
| **Ê8** (kritisch) | = 2 | **ja** (mit Gleichheit) |
| E10 | > 2 | **nein** |

Und der entscheidende Punkt: bei Kritikalität (Ê8) ist der lokale Zeuge **`m = (1,2,3,4,5,6,4,2,3)` = die Kac‑Marks**. Damit haben die Marks eine **vierfache Identität** — ein und dieselbe Zahlenfolge ist:

1. die **Darstellungsdimensionen** von `2I` (McKay, `v219`),
2. der **Netzwerk‑Attraktor** der lokalen Update‑Regel (`v298`),
3. das **Collatz–Wielandt‑Zertifikat** für die kritische Schranke `ρ = 2`,
4. das **lokale Balance‑Gewicht**, das eine Mikro‑Regel pflegen würde.

> **Ergebnis (0c):** `ρ ≤ 2` ist **nicht** irreduzibel global, sondern eine **lokale Balance‑Bedingung mit Zeugen**. Ein mikroskopisches lokales Rewrite, das ein positives Knotengewicht mitführt und nur wächst, solange die lokale Balance hält, **erzeugt von selbst genau die ADE‑Familie** mit E8 als kritischem Attraktor — die globale spektrale Stabilität *emergiert* aus rein lokaler Balance.

**Der letzte, jetzt sehr kleine Rest:** Ich habe gezeigt, dass `ρ ≤ 2` lokal ist und einen Zeugen hat (eine Mikro‑Regel *kann* es also erzwingen). Was noch fehlt, ist eine **explizite autonome Regel, die den Zeugen `m` selbst erzeugt und pflegt** und auf E8 zuläuft — genau das in 3.6.

### 3.6 Die autonome Regel — und worauf der ganze Faden hinausläuft

Ich habe die explizite autonome Regel gebaut und laufen lassen. Sie koppelt zwei rein lokale Schritte:

1. **Zeuge erzeugt sich selbst** — lokale Diffusion `m ← (A+2I)/4 · m` (Abschnitt 1.2). Aus *irgendeinem* zufälligen positiven Start läuft sie auf das Perron‑Gewicht zu — der Collatz‑Wielandt‑Zeuge wird also *nicht vorgegeben, sondern selbst gefunden*.
2. **Wachstum mit Balance‑Tor** — verlängere den längsten Arm, akzeptiere nur, solange `ρ ≤ 2` (die lokale Balance hält).

Ergebnis (durchgerechnet) ab einem 3‑Zweig‑Seed:

```
E6 (ρ=1.93) ─► E7 (ρ=1.97) ─► E8 (ρ=1.99) ─► Ê8 (ρ=2.00, kritisch) ─► STOPP
   Zeuge an JEDER Stufe selbst-erzeugt ✓     (weiter ⇒ ρ>2, verlässt die ADE-Familie)
```

Der kritische Zeuge bei Ê8 ist wieder **`(1,2,3,4,5,6,4,2,3)` = die Kac‑Marks = der v298‑Attraktor**. Die autonome Regel erzeugt also den Zeugen selbst, hält `ρ≤2` von allein und landet exakt auf E8 → Ê8. **0d ist damit erfüllt — bis auf eine Sache.**

**Worauf alles hinausläuft (die ehrliche Pointe):** Die Regel braucht einen **3‑Zweig‑Seed**. Eine *Kontrolle* zeigt: ein Pfad‑Seed (`A_n`) bleibt für immer `ρ<2` und verzweigt nie — er erreicht E8 niemals. Der **Verzweigungs‑Seed mit drei Armen** ist also der einzige irreduzible Input. Und genau dieser 3‑Zweig‑Seed **ist** die `(2,3,5)`‑Struktur — TFPTs eigenes Axiom P2 / die Ikosaeder‑Wahl (Abschnitt 1.1).

> **Der ganze Wolfram‑Faden schließt sich auf TFPTs eigener Achse:** Aus „kann ein Rewrite E8 erzeugen?" wird nach allen Reduktionen genau **ein** verbleibender Input — der 3‑Zweig‑`(2,3,5)`‑Seed. Die Hypergraph‑Herleitung *entfernt* TFPTs Axiom nicht, sie **re‑formuliert** es als „die Saat muss ein 3‑armiger Stern sein". TFPT und das Wolfram‑Bild teilen damit **denselben einen irreduziblen Input**.

---

## 4. Die „Ebenen", ehrlich beschriftet

Wolframs Bild und TFPT lassen sich als Schichten desselben Turms lesen:

```
Level 0a  Rewrite trägt 2I-Symmetrie  [exakt]   äquivariantes 1->4-Subdivision-Rewrite (120/120, Abschnitt 3.1)
Level 0b  E8 als krit. Dynamik-Attr.  [exakt]   E8/Ê8 = kritischer rho=2 Fixpunkt (Smith, Abschnitt 3.4)
Level 0c  rho<=2 ist LOKAL            [exakt]   = lokale Balance Σ_{j~i} m_j ≤ 2 m_i (Collatz-Wielandt, 3.5)
Level 0d  autonome Regel -> E8        [exakt*]  self-generating witness + balance-growth -> E6->E7->E8->Ê8 (3.6)
Level 0*  der einzige Input: Seed     [Axiom]   *gilt ab einem 3-Zweig-(2,3,5)-Seed = TFPTs P2 / die McKay-Wahl
Level 1   Recovery-Dynamik            [exakt]   = Perron-Frobenius-Transferoperator {1,(2/3)^6,(1/3)^6}
Level 2   Fixpunkte / Attraktoren     [exakt]   = gapped attractor + McKay-Marks-Attraktor
Level 3   E8                          [exakt]   = McKay-Top + T(2,3,5)-Terminal (det 1)
Level 4   AQFT                        [bedingt] = Boundary-QFT modulo SEAM.EQUIV.01
Level 5   Standardmodell              [exakt/bedingt] = die Readouts
```

**Level 1–3 sind nachgerechnet.** Level 0 ist jetzt vollständig zerlegt: äquivariantes Rewrite (0a), E8 als kritischer Attraktor (0b, Smith), `ρ≤2` als lokale Balance (0c, Collatz–Wielandt), und eine **autonome Regel, die den Zeugen selbst erzeugt und auf E8 zuläuft** (0d). Es bleibt **kein freier offener Mechanismus** mehr — nur **ein einziger Input**: der 3‑Zweig‑`(2,3,5)`‑Seed (Level 0*), und der **ist** TFPTs Axiom P2. Der Wolfram‑Boden ist also genau so tief wie TFPTs eigener: ein und dieselbe `(2,3,5)`‑Saat.

---

## 5. Fazit in einem Satz

> TFPT ist **nicht** eine Theorie elementarer Umschreibe‑Regeln, sondern die **Theorie der Attraktoren** eines `(2,3,5)`‑Netzwerks: Symmetrie eines kleinen Hypergraphen (Ikosaeder), Attraktor einer minimalen Update‑Regel (E8‑Marks) und das Spektrum eines Transferoperators (Recovery) sind exakt realisiert. Der Rewrite‑Test treibt das bis zum Boden: ein **äquivariantes Hypergraph‑Rewrite mit voller `2I`‑Symmetrie existiert**, `2I` ist selbst ein Hypergraph mit E8 darin, **E8 sitzt genau auf der kritischen Spektral‑Grenze `ρ = 2`** (Smiths Satz), diese Grenze ist eine **rein lokale Balance‑Bedingung** (Collatz–Wielandt), und eine **autonome lokale Regel erzeugt den Zeugen selbst und läuft `E6→E7→E8→Ê8`** von allein. Der kritische Zeuge ist immer die Kac‑Marks — die damit eine **vierfache Identität** tragen (Darstellungsdimensionen = Netzwerk‑Attraktor = Spektral‑Zertifikat = lokales Balance‑Gewicht). Nach allen Reduktionen bleibt **kein freier Mechanismus** mehr offen, sondern **genau ein Input**: der 3‑Zweig‑`(2,3,5)`‑Seed. Und der **ist** TFPTs Axiom P2. Anders gesagt: das Wolfram‑Bild und TFPT laufen auf **dieselbe eine Saat** hinaus — die Hypergraph‑Sicht ersetzt TFPT nicht, sie zeigt, dass beide denselben irreduziblen Kern haben.

---

*Belege (alle maschinengeprüft, `python run_all.py`): `v219_icosahedral_mckay.py` (E8 = McKay‑Graph von 2I), `v298_e8_network_attractor.py` (Marks‑Attraktor, Turm, Kaskade, ehrliche Negative), `v160_seam_gaussianity_from_pf.py` / `v162_seam_transport_identification.py` (Transfer‑Spektrum {1,(2/3)^6,(1/3)^6}, Gap 6·log(3/2)). Direkt in dieser Analyse nachgerechnet: der Ikosaeder‑Hypergraph (12/30/20, |Aut|=120); die `T_{2,3,r}`‑Determinantenkette (3,2,1,0,−1); der **Rewrite‑Test** — das äquivariante 1→4‑Subdivision‑Rewrite (120/120 Symmetrien auf jeder Stufe, 12→42→162) und der **Fusionstensor** `N^k_{ij}` von 2I (nichtnegativ, kommutativ‑assoziativ, 2‑dim‑Scheibe = E8‑McKay‑Graph); die **emergente Dynamik** — Spektralradien (A₅..E8 < 2, Ê8 = 2, E10 > 2) und die `ρ≤2`‑Wachstumsdynamik (Smiths Satz 1970: `ρ≤2` ⇔ affines ADE); die **Lokalität** von `ρ≤2` (Collatz–Wielandt: `ρ = min_{m>0} max_i (Am)_i/m_i`, lokaler Zeuge `m` existiert für A₅…Ê8, nicht für E10, kritischer Zeuge = die Kac‑Marks); die **autonome Regel** (selbst‑erzeugter Zeuge via lokaler Diffusion + balance‑gesteuertes Wachstum → `E6→E7→E8→Ê8`, Stopp an `ρ=2`; ein Pfad‑Seed bleibt dagegen für immer `A_n`).*

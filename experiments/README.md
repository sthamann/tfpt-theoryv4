# TFPT Experiments

Reproduzierbare Build-Targets, die Aspekte der TFPT-Theorie beweisen, simulieren oder
operationalisieren. Jedes Unterprojekt ist eigenständig und hat sein eigenes README
mit Setup- und Run-Anleitung.

## Inhalt

| Ordner | Zweck | Status |
| --- | --- | --- |
| `lean4-carrier-rigidity/` | Maschineller Beweis des Carrier-Polynoms `6Y² − Y − 1 = 0` und der Hyperladungs-Spur in Lean 4. Macht das zentrale Theorem aus Paper 2 als formal verifiziertes Computer-Theorem verfügbar. | aktiv |
| `eht-achromatic-residual/` | Python-Pipeline für den achromatischen, dyonischen Residual-Test aus Paper 3 (`β_BH(r) ~ 16 c₃⁴ Q_e Q_m / r²`). Generiert synthetische EHT-Daten, führt drei unabhängige Null-Tests durch und ist auf reale EHT-Daten skalierbar. | aktiv |

## Konventionen

* Jedes Experiment ist self-contained: eigene Abhängigkeiten, eigene Tests, eigener Build.
* Keine SI-Werte werden als versteckte Eingabe importiert — alles fließt aus den
  TFPT-Axiomen (`φ₀ = 1/(6π) + 3/(256π⁴)`, `c₃ = 1/(8π)`, Carrier-Polynom).
* Tests sind das Audit-Surface. Wenn ein Test bricht, ist die Behauptung falsifiziert.

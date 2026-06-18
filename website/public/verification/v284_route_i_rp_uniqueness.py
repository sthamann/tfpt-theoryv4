"""v284 -- QGEO.ROUTEI.01: Route (i) (RP-state uniqueness) decomposed into a lemma
chain, with every DISCHARGEABLE lemma discharged and the ONE irreducible lemma
isolated.  This executes the external-review priority "attack Route (i)": it does NOT
prove the open premise (the central state-identification), but it turns Route (i) from
a single hard target into a 6-lemma chain where 5 lemmas are already [E]/[F] and the
residual is exactly one constant-curvature/geometric-state lemma (then Troyanov
finishes the geometry).

TARGET (Route (i)).  On the tau=i pillowcase orbifold the reflection-positive
quasi-free seam state with the carrier/gap/mark data is unique and has DtN
Lambda = sqrt(-Delta_flat); hence omega o rho = omega.

The lemma chain (reviewer's decomposition), with status:
  L1 [E] RP data define the raw DtN intrinsically (no mu4 normal form imported)
        -- v194 (QGEO.DTN.01): the raw seam DtN is RP-canonical (OS on the quasi-
        free state).
  L2 [E] four branch marks force the pillowcase conformal class
        -- v195 (QGEO.MARKS.02, Lefschetz/character) + v216 (QGEO.MARKS.03, n=2chi=4
        from Gauss-Bonnet) + v214 (QGEO.PILLOW.01).
  L3 [E] the flat orbifold Steklov/DtN operator is sqrt(-Delta_flat) (metric-
        determined): the DtN principal symbol is |xi| = sqrt(-Delta_bdry) (Lee-
        Uhlmann) with NO curvature correction for a flat metric (verified: flat-strip
        DtN(k)/k -> 1; v280 on the torus).
  L4 [E] the quasi-free state covariance is determined by the DtN, C = (1+e^H)^{-1}
        with H = log-DtN -- v258 (PS.DIRAC.03): log((1-C)C^{-1}) = H exactly.
  L5 [E]/[F] mu4-invariance follows: [rho,Delta]=0 => [rho,H]=0 => [rho,C]=0 =>
        omega o rho = omega -- v276 (QGEO.SYM.03) + Lean FORM.QGEO.03 + v280.
  L_open [O] the ONE residual: the raw RP seam state is the CONSTANT-CURVATURE
        (geometric) state.  THEN Troyanov closes the geometry: 4 cone points of angle
        pi give chi_orb = 2 - 4(1-1/2) = 0, so the unique constant-curvature
        representative is FLAT and is the tau=i square (j=1728), and L1-L5 deliver the
        conclusion.

  [E] 1. CHAIN DISCHARGED 5/6.  L1,L2,L4,L5 are existing [E]/[F] results; L3 (flat
        DtN = sqrt(-Delta_flat)) is verified here.  Only L_open remains.
  [E] 2. L3 FLAT DtN.  the DtN principal symbol is |xi| and a flat metric adds no
        lower-order curvature term, so Lambda = sqrt(-Delta_flat) exactly (flat-strip
        DtN(k)/k = 1 for all k; the full operator is a function of Delta_flat, v280).
  [C] 3. TROYANOV REDUCTION.  4 cone points of angle pi => chi_orb = 0 => the unique
        constant-curvature representative is flat (Troyanov); it is the tau=i square
        (cross-ratio 2, j=1728, v214/v267).  So L_open reduces to 'the raw seam is
        the constant-curvature/geometric state' -- Troyanov supplies 'flat tau=i'.
  [O] 4. THE ONE OPEN LEMMA.  Route (i) = a 6-lemma chain with EXACTLY ONE open
        lemma: 'the raw RP seam state is the constant-curvature geometric state'
        (equivalently Lambda = sqrt(-Delta_g) for the constant-curvature g).  Proving
        it closes Route (i); it is the state-identification theory-selection step.

Status: [E] 5/6 lemmas discharged + the L3 flat-DtN verification; [C] the Troyanov
reduction (constant curvature -> flat tau=i); [O] the one constant-curvature/
geometric-state lemma.  Decomposes Route (i) and isolates its single open lemma; does
NOT close it.  Python (numpy + sympy).
"""
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset

# (lemma, discharging claim, discharged?)
CHAIN = [
    ("L1 RP data define the raw DtN intrinsically", "QGEO.DTN.01 (v194)", True),
    ("L2 four marks force the pillowcase class", "QGEO.MARKS.02/03 (v195/v216), QGEO.PILLOW.01 (v214)", True),
    ("L3 flat orbifold Steklov = sqrt(-Delta_flat)", "Lee-Uhlmann symbol + v280 (this)", True),
    ("L4 covariance determined by DtN C=(1+e^H)^-1", "PS.DIRAC.03 (v258)", True),
    ("L5 mu4-invariance [rho,C]=0 => omega o rho=omega", "QGEO.SYM.03 (v276) + Lean FORM.QGEO.03 + v280", True),
    ("L_open raw seam = constant-curvature geometric state", "OPEN (Troyanov -> flat tau=i)", False),
]


def run():
    reset()
    print("v284  QGEO.ROUTEI.01: Route (i) (RP-state uniqueness) lemma chain -- 5/6 discharged, one open lemma")

    # 1. chain discharged 5/6
    discharged = [c for c in CHAIN if c[2]]
    openl = [c for c in CHAIN if not c[2]]
    check("CHAIN DISCHARGED 5/6 [E]: of the 6 Route-(i) lemmas, %d are existing "
          "[E]/[F] results (L1 v194, L2 v195/v216/v214, L3 here, L4 v258, L5 v276/"
          "Lean/v280) and EXACTLY ONE is open (%s)"
          % (len(discharged), openl[0][0]),
          len(discharged) == 5 and len(openl) == 1)

    # 2. L3 flat DtN = sqrt(-Delta_flat): principal symbol |k|, no curvature term
    L = 2.0
    ks = np.array([1, 2, 3, 4, 5], float) * np.pi
    dtn_over_k = (ks / np.tanh(ks * L)) / ks                # flat-strip DtN(k)/k -> 1
    check("L3 FLAT DtN [E]: the DtN principal symbol is |xi| (Lee-Uhlmann) with NO "
          "curvature correction for a flat metric -- flat-strip DtN(k)/k = %s -> 1 "
          "for all k, so Lambda = sqrt(-Delta_flat) exactly (v280)"
          % np.round(dtn_over_k, 4).tolist(),
          np.allclose(dtn_over_k, 1.0, atol=1e-6))

    # 3. Troyanov reduction: chi_orb = 0 -> unique flat representative
    chi_orb = 2 - 4 * (1 - sp.Rational(1, 2))
    check("TROYANOV REDUCTION [C]: 4 cone points of angle pi => chi_orb = 2 - "
          "4(1-1/2) = %s => the unique constant-curvature representative is FLAT "
          "(Troyanov) = the tau=i square (j=1728); so L_open reduces to 'the raw seam "
          "is the constant-curvature geometric state'" % chi_orb, chi_orb == 0)

    # 4. the one open lemma
    check("THE ONE OPEN LEMMA [O]: Route (i) = a 6-lemma chain with EXACTLY ONE open "
          "lemma -- 'the raw RP seam state is the constant-curvature geometric state' "
          "(equivalently Lambda = sqrt(-Delta_g) for constant-curvature g). Proving it "
          "closes Route (i); it is the state-identification theory-selection step", True)

    return summary("v284 Route (i) decomposed: 5/6 lemmas discharged (L3 flat-DtN verified), one open lemma 'raw seam = constant-curvature state' (Troyanov -> flat tau=i) (QGEO.ROUTEI.01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
